"""
Ability display and use commands.

CmdAbilities shows known abilities and active loadout (D-26).
CmdUseAbility is the unified dispatcher for `use`:
  - If args match an inventory consumable -> consume item (D-13, D-14)
  - If args match a known ability -> route to ability_engine (ABL-02)
  - Ability use gated by active_loadout (PSC-06)
Handles ambiguous prefix matching by listing options instead of
silently picking the first match.
"""

from commands.command import Command


class CmdAbilities(Command):
    """
    View your known abilities and active loadout.

    Usage:
      abilities
    """

    key = "abilities"
    aliases = ["abs"]
    locks = "cmd:all()"
    help_category = "Abilities"

    def func(self):
        character = self.caller

        from world.ability_registry import ABILITIES
        from world.models import CharacterAbility
        from world.remnance_visibility import ability_is_player_visible

        known_ids = list(
            CharacterAbility.objects.filter(
                character=character
            ).values_list("ability_id", flat=True)
        )

        if not known_ids:
            character.msg("You have not yet unlocked any abilities.")
            return

        # Group by domain and tier
        grouped = {}
        for aid in known_ids:
            ability = ABILITIES.get(aid)
            if not ability:
                continue
            if not ability_is_player_visible(ability, character):
                continue
            domain = ability["domain"]
            tier = ability["tier"]
            grouped.setdefault(domain, {}).setdefault(tier, []).append(ability)

        lines = ["|wKnown Abilities|n", ""]

        for domain in sorted(grouped.keys()):
            lines.append(f"  |w{domain.capitalize()}|n")
            for tier in sorted(grouped[domain].keys()):
                for ab in grouped[domain][tier]:
                    cost_str = f"{ab['resource_cost']} {ab['resource_type']}"
                    cd_str = f"CD: {ab['cooldown']}t" if ab["cooldown"] else ""
                    lines.append(
                        f"    T{tier} |g{ab['name']:25}|n {cost_str:20} {cd_str}"
                    )
            lines.append("")

        # Active loadout
        loadout = character.db.active_loadout or []
        if loadout:
            lines.append("|wActive Loadout|n")
            for aid in loadout:
                ability = ABILITIES.get(aid)
                if ability and not ability_is_player_visible(ability, character):
                    continue
                name = ability["name"] if ability else aid
                lines.append(f"  |g{name}|n")
        else:
            lines.append("|wActive Loadout:|n (none set)")

        character.msg("\n".join(lines))


class CmdUseAbility(Command):
    """
    Use an ability or consume an item.

    Usage:
      use <ability_name> [<target>]
      use <item>

    Examples:
      use momentum strike
      use resonant strike goblin
      use healing potion
    """

    key = "use"
    locks = "cmd:all()"
    help_category = "Abilities"

    def func(self):
        character = self.caller

        if not self.args or not self.args.strip():
            character.msg("Usage: use <ability_name> [<target>]  or  use <item>")
            return

        raw_args = self.args.strip()

        # --- ITEM CONSUMPTION BRANCH (D-13, D-14) ---
        # Search inventory for a matching consumable item by name
        item_matches = character.search(raw_args, location=character, quiet=True)
        if item_matches:
            item = item_matches[0] if isinstance(item_matches, list) else item_matches
            if getattr(item.db, "item_type", "") == "consumable":
                self._consume_item(character, item)
                return

        # --- ABILITY BRANCH (existing logic) ---
        from world.ability_registry import ABILITIES
        from world.models import CharacterAbility
        from world.remnance_visibility import ability_is_player_visible

        # Get character's known ability ids
        known_ids = list(
            CharacterAbility.objects.filter(
                character=character
            ).values_list("ability_id", flat=True)
        )
        known_ids = [
            aid for aid in known_ids
            if ability_is_player_visible(ABILITIES.get(aid), character)
        ]

        if not known_ids:
            character.msg("You have not yet unlocked any abilities.")
            return

        # Try to resolve ability name and target
        ability_id, target_str = self._resolve_ability_and_target(
            raw_args, known_ids
        )

        if ability_id is None:
            return  # Error already messaged

        # --- LOADOUT GATE (PSC-06) ---
        # If player has configured a loadout, ability must be in it.
        # Empty loadout = unrestricted (backward compat until player sets one up).
        active_loadout = character.db.active_loadout or []
        if active_loadout and ability_id not in active_loadout:
            character.msg(
                "That ability is not in your active loadout. "
                "Use |wloadout add <ability>|n first."
            )
            return

        # Target resolution
        target = None
        if target_str:
            target = character.search(target_str)
            if not target:
                return  # search() already sends error message

        # Route through CombatScript if in combat (enforces turn order)
        combat_handler = getattr(character.ndb, "combat_handler", None)
        if combat_handler and hasattr(combat_handler, "process_player_action"):
            combat_handler.process_player_action(
                character, action_type="ability",
                ability_id=ability_id, target=target
            )
        else:
            from world.ability_engine import use_ability
            ok, msg = use_ability(character, ability_id, target)
            character.msg(msg)

        # Attuned variant display (D-23)
        ability = ABILITIES.get(ability_id, {})
        variants = ability.get("attuned_variants")
        if variants:
            # Determine current environment from zone_type or room node tags
            current_env = None
            loc = character.location
            if loc:
                # Check room tags for node type first (more specific)
                for env_key in variants:
                    if loc.tags.get(env_key, category="node_type"):
                        current_env = env_key
                        break
                # Fall back to zone_type from the zone object
                if not current_env:
                    zone_id = loc.db.zone_id
                    if zone_id:
                        from world.zone_scaling import get_zone_obj_for_room
                        zone_obj = get_zone_obj_for_room(loc)
                        if zone_obj:
                            zt = zone_obj.db.zone_type
                            if zt and zt in variants:
                                current_env = zt
            if current_env:
                variant_name = variants[current_env]
                character.msg(
                    f"|c[Attuned: {variant_name} -- this ability is "
                    f"enhanced in this environment.]|n"
                )
            else:
                env_names = ", ".join(sorted(variants.keys()))
                character.msg(
                    f"|C[This ability has attuned variants in: "
                    f"{env_names}.]|n"
                )

    def _resolve_ability_and_target(self, raw_args, known_ids):
        """
        Resolve ability name from raw args. Returns (ability_id, target_str)
        or (None, None) if resolution fails (error messaged).
        """
        from world.ability_registry import ABILITIES

        # Build lookup for known abilities
        known_abilities = {}
        for aid in known_ids:
            ability = ABILITIES.get(aid)
            if ability:
                known_abilities[aid] = ability

        # Try exact match first: replace spaces with underscores
        words = raw_args.lower().split()

        # Try progressively longer ability name matches
        best_match = None
        best_target = None

        for i in range(len(words), 0, -1):
            candidate_id = "_".join(words[:i])
            if candidate_id in known_abilities:
                best_match = candidate_id
                best_target = " ".join(words[i:]) if i < len(words) else None
                break

        if best_match:
            return best_match, best_target

        # No exact match — try prefix matching
        input_lower = raw_args.lower()
        matches = []

        for aid, ability in known_abilities.items():
            name_lower = ability["name"].lower()
            if name_lower.startswith(input_lower):
                matches.append(ability)
            elif input_lower.startswith(name_lower):
                # Input starts with ability name — rest is target
                rest = raw_args[len(ability["name"]):].strip()
                return aid, rest if rest else None

        # Also try prefix on partial input (first few words)
        if not matches:
            for num_words in range(len(words), 0, -1):
                partial = " ".join(words[:num_words])
                partial_matches = []
                for aid, ability in known_abilities.items():
                    if ability["name"].lower().startswith(partial):
                        partial_matches.append((aid, ability))
                if len(partial_matches) == 1:
                    aid, ability = partial_matches[0]
                    rest = " ".join(words[num_words:])
                    return aid, rest if rest else None
                elif len(partial_matches) > 1:
                    matches = [ab for _, ab in partial_matches]
                    break

        if len(matches) == 1:
            return matches[0]["id"], None

        if len(matches) > 1:
            names = ", ".join(ab["name"] for ab in matches)
            self.caller.msg(f"Which ability did you mean? {names}")
            return None, None

        self.caller.msg(
            f"You don't know an ability matching '{raw_args}'. "
            "Type 'abilities' to see your known abilities."
        )
        return None, None

    def _consume_item(self, character, item):
        """Dispatch consumable usage to world.item_effects engine."""
        from world.item_effects import consume_item
        ok, msg = consume_item(character, item)
        character.msg(msg)
