"""
Combat script -- room-attached Evennia Script that manages all combat state.

CombatScript drives initiative order, processes turns, handles round
progression, and orchestrates calls to combat_engine, combat_ai,
status_effects, and ability_engine.

One CombatScript per active encounter. Attaches to the room where combat
takes place. Individual initiative with interleaved player/mob turns (D-15).
Solo combat waits indefinitely for player input; group combat has a
configurable round timeout with auto-attack fallback (D-18).

Exports:
    CombatScript, start_combat, join_combat
"""

import random


# ---------------------------------------------------------------------------
# CombatScript
# ---------------------------------------------------------------------------

class CombatScript:
    """
    Room-attached combat manager. One per active encounter.

    Inherits from SoravelonScript (lazy import at creation time).
    This class body is injected into the real typeclass in _build_class().
    We define it as a plain class here and dynamically subclass in the
    module-level helpers so that importing this module does NOT trigger
    Evennia typeclass resolution at import time (same pattern as other
    world/ modules).
    """

    # -- lifecycle -----------------------------------------------------------

    def at_script_creation(self):
        """Called once when the script is first created."""
        super().at_script_creation()
        self.key = "combat_script"
        self.interval = 0  # Event-driven, not self-ticking
        self.persistent = True  # Survive server reload

        # Persistent state (db)
        self.db.combatant_ids = []
        self.db.round_number = 1
        self.db.current_turn_index = 0
        self.db.initiative_order = []  # [{id, initiative_value}] sorted desc
        self.db.is_group_combat = False
        self.db.round_timeout = 30  # seconds, only active if is_group_combat
        self.db.active_effects_db = {}  # {combatant_id: [effect_list]}

        # Volatile state (ndb)
        self.ndb.turn_timer_id = None
        self.ndb.pending_charged = {}  # {char_id: {ability_id, rounds_left, target_id}}
        self.ndb.pending_mob_casts = {}  # {combatant_db_id: {ability, target_id, rounds_left}}
        self.ndb.call_for_help_count = 0

    def at_start(self):
        """Called on creation AND on server reload. Rebuild volatile state."""
        super().at_start()

        # Rebuild ndb defaults
        if self.ndb.turn_timer_id is None:
            self.ndb.turn_timer_id = None
        if self.ndb.pending_charged is None:
            self.ndb.pending_charged = {}
        if self.ndb.call_for_help_count is None:
            self.ndb.call_for_help_count = 0
        if self.ndb.pending_mob_casts is None:
            self.ndb.pending_mob_casts = {}

        # Restore active_effects from db to each combatant's ndb
        from evennia import search_object
        stored_effects = self.db.active_effects_db or {}
        for cid_str, effects in stored_effects.items():
            cid = int(cid_str)
            results = search_object(str(cid), exact=False, use_dbref="#" + str(cid))
            if results:
                combatant = results[0]
                combatant.ndb.active_effects = list(effects)

        # Re-add CombatCmdSet to connected players and re-prompt or auto-process
        for combatant in self._resolve_combatants():
            if combatant is None:
                continue
            combatant.ndb.combat_handler = self
            if _is_player(combatant):
                _add_combat_cmdset(combatant)

        # Resume combat flow
        current = self.get_current_combatant()
        if current is None:
            return
        if _is_mob(current):
            self._process_mob_turn(current)
        elif _is_player(current) and _is_connected(current):
            self._prompt_player_turn(current)

    # -- combatant management ------------------------------------------------

    def add_combatant(self, combatant):
        """
        Compute initiative for combatant and insert into sorted order.
        Internal method called by start_combat and join_combat.
        """
        from world.base_attributes import get_initiative

        initiative_val = get_initiative(combatant)
        entry = {"id": combatant.id, "initiative_value": initiative_val}

        # Insert into initiative_order maintaining descending sort
        order = list(self.db.initiative_order)
        inserted = False
        for i, existing in enumerate(order):
            if initiative_val > existing["initiative_value"]:
                order.insert(i, entry)
                inserted = True
                break
            elif initiative_val == existing["initiative_value"]:
                # Tie-break: random coin flip for insertion position
                if random.random() < 0.5:
                    order.insert(i, entry)
                else:
                    order.insert(i + 1, entry)
                inserted = True
                break
        if not inserted:
            order.append(entry)
        self.db.initiative_order = order

        # Rebuild combatant_ids from initiative_order
        self.db.combatant_ids = [e["id"] for e in self.db.initiative_order]

        # Set ndb references on combatant
        combatant.ndb.combat_handler = self
        combatant.ndb.actions_remaining = 0
        combatant.ndb.ability_used_this_turn = False

        if _is_player(combatant):
            _add_combat_cmdset(combatant)

    def remove_combatant(self, combatant):
        """
        Remove combatant from combat. Cleans up ndb references.
        If was current turn, advances to next. If no enemies remain, ends combat.
        """
        cid = combatant.id
        was_current = False
        current_idx = self.db.current_turn_index or 0
        ids = list(self.db.combatant_ids)

        if cid in ids:
            remove_idx = ids.index(cid)
            was_current = (remove_idx == current_idx)

        # Remove from initiative_order
        order = [e for e in self.db.initiative_order if e["id"] != cid]
        self.db.initiative_order = order
        self.db.combatant_ids = [e["id"] for e in order]

        # Clean up ndb
        combatant.ndb.combat_handler = None
        combatant.ndb.actions_remaining = 0
        combatant.ndb.ability_used_this_turn = False

        if _is_player(combatant):
            _remove_combat_cmdset(combatant)

        # Remove from pending_charged
        charged = dict(self.ndb.pending_charged or {})
        if cid in charged:
            del charged[cid]
        self.ndb.pending_charged = charged

        # Remove from pending_mob_casts (mob died mid-cast)
        pending_casts = dict(self.ndb.pending_mob_casts or {})
        if cid in pending_casts:
            del pending_casts[cid]
            self.ndb.pending_mob_casts = pending_casts

        # Remove from active_effects_db
        stored = dict(self.db.active_effects_db or {})
        if str(cid) in stored:
            del stored[str(cid)]
        self.db.active_effects_db = stored

        # Check if combat should end
        if not self.get_mob_combatants() or not self.get_player_combatants():
            self.end_combat()
            return

        # Cancel turn timer if removing the active combatant
        if was_current and self.ndb.turn_timer_id is not None:
            try:
                self.ndb.turn_timer_id.cancel()
            except (AttributeError, RuntimeError):
                pass
            self.ndb.turn_timer_id = None

        # Adjust turn index if needed
        if was_current:
            # Keep index (next combatant shifts into this slot)
            if self.db.current_turn_index >= len(self.db.combatant_ids):
                self.db.current_turn_index = 0
            self.advance_turn()
        elif remove_idx < current_idx:
            # Removed someone before current -- shift index back
            self.db.current_turn_index = max(0, current_idx - 1)

    def get_player_combatants(self):
        """Return list of player characters currently in combat."""
        return [c for c in self._resolve_combatants() if c and _is_player(c)]

    def get_mob_combatants(self):
        """Return list of mobs currently in combat."""
        return [c for c in self._resolve_combatants() if c and _is_mob(c)]

    def get_current_combatant(self):
        """Return the combatant whose turn it is, or None."""
        ids = self.db.combatant_ids or []
        idx = self.db.current_turn_index or 0
        if not ids or idx >= len(ids):
            return None
        return _resolve_by_id(ids[idx])

    def is_combatant(self, obj):
        """Check if obj is in this combat."""
        return obj.id in (self.db.combatant_ids or [])

    # -- turn management -----------------------------------------------------

    def advance_turn(self):
        """Advance to the next combatant's turn."""
        ids = self.db.combatant_ids or []
        if not ids:
            self.end_combat()
            return

        idx = (self.db.current_turn_index + 1) % len(ids)

        # Round wrap -- end_round when we cycle back to start
        if idx <= self.db.current_turn_index and self.db.current_turn_index > 0:
            self.end_round()
            # Re-check after round end (DoT kills may have ended combat)
            if not self.db.combatant_ids:
                return
            ids = self.db.combatant_ids
            idx = idx % len(ids) if ids else 0

        self.db.current_turn_index = idx
        combatant = self.get_current_combatant()
        if combatant is None:
            return

        # Skip dead or disconnected combatants
        from world.combat_engine import check_death
        if check_death(combatant) or (_is_player(combatant) and not _is_connected(combatant)):
            self.advance_turn()
            return

        # Skip stunned/charmed combatants
        from world.status_effects import get_effect_modifiers
        mods = get_effect_modifiers(combatant)
        if mods.get("skip_turn", False):
            name = combatant.key
            room = self.obj
            if room:
                room.msg_contents(f"|y{name} is incapacitated and loses their turn.|n")
            self.advance_turn()
            return

        # Dispatch turn
        if _is_mob(combatant):
            self._process_mob_turn(combatant)
        else:
            self._prompt_player_turn(combatant)

    def _prompt_player_turn(self, character):
        """Set up a player's turn: compute actions, handle charged abilities, prompt."""
        from world.base_attributes import get_actions_per_turn
        from world.status_effects import get_effect_modifiers
        from world.ability_engine import use_ability

        mods = get_effect_modifiers(character)
        base_actions = get_actions_per_turn(character)
        action_penalty = mods.get("action_budget_penalty", 0)
        action_bonus = mods.get("action_budget_bonus", 0)
        actions = max(1, base_actions - action_penalty + action_bonus)

        character.ndb.actions_remaining = actions
        character.ndb.ability_used_this_turn = False

        # Check pending charged abilities
        charged = dict(self.ndb.pending_charged or {})
        if character.id in charged:
            charge_info = charged[character.id]
            charge_info["rounds_left"] -= 1
            if charge_info["rounds_left"] <= 0:
                # Fire the charged ability
                ability_id = charge_info["ability_id"]
                target = _resolve_by_id(charge_info.get("target_id"))
                ok, msg = use_ability(character, ability_id, target=target)
                character.msg(f"|w{msg}|n")
                if self.obj:
                    self.obj.msg_contents(msg, exclude=[character])
                del charged[character.id]
                # Check death of target
                if target:
                    from world.combat_engine import check_death, handle_mob_death, handle_player_death
                    if check_death(target):
                        if _is_mob(target):
                            death_msg = handle_mob_death(target, character)
                        else:
                            death_msg = handle_player_death(target)
                        if self.obj:
                            self.obj.msg_contents(death_msg)
                        self.remove_combatant(target)
                        return
            else:
                charged[character.id] = charge_info
            self.ndb.pending_charged = charged

        # Build turn prompt
        _send_turn_prompt(character, self)

        # Push OOB combat update
        from world.oob_publisher import push_combat_update
        push_combat_update(character, _build_combat_oob(character, self))

        # Group combat timeout
        if self.db.is_group_combat:
            from evennia.utils.utils import delay
            self.ndb.turn_timer_id = delay(
                self.db.round_timeout,
                self._auto_attack_timeout,
                character.id,
            )

    def _process_mob_turn(self, mob):
        """Process a mob's turn via combat_ai, resolve returned actions."""
        from world.combat_ai import process_mob_turn
        from world.combat_engine import (
            resolve_basic_attack, check_death,
            handle_mob_death, handle_player_death,
        )

        actions = process_mob_turn(mob, self)

        for action in actions:
            action_type = action.get("type", "")
            target = _resolve_by_id(action.get("target_id"))

            if action_type == "basic_attack" and target:
                ok, msg, dmg = resolve_basic_attack(mob, target)
                if self.obj:
                    self.obj.msg_contents(msg)
                if check_death(target):
                    if _is_player(target):
                        death_msg = handle_player_death(target)
                    else:
                        death_msg = handle_mob_death(target, mob)
                    if self.obj:
                        self.obj.msg_contents(death_msg)
                    self.remove_combatant(target)
                    return  # Combat may have ended

            elif action_type == "ability" and target:
                ability_id = action.get("ability_id", "")
                # Mob abilities use inline data from combat_ai, not the player
                # ability registry. Build a compatible ability dict and resolve
                # damage directly through combat_engine.
                mob_ability = {
                    "name": ability_id or "ability",
                    "damage_base": action.get("damage_base", 0),
                    "element": action.get("element", "physical"),
                    "effect_params": {"damage_base": action.get("damage_base", 0)},
                }
                from world.combat_engine import resolve_ability_damage
                ok, msg, dmg = resolve_ability_damage(mob, mob_ability, target)
                if self.obj:
                    self.obj.msg_contents(msg)
                # Apply status effect if ability has one
                status = action.get("status_effect")
                if status and ok:
                    # Check application chance before applying
                    import random
                    app_chance = action.get("application_chance", 1.0)
                    if random.random() <= app_chance:
                        from world.status_effects import apply_effect
                        apply_effect(
                            target, status,
                            duration=action.get("effect_duration", 2),
                            magnitude=action.get("effect_magnitude", 1),
                            source_id=mob.id if mob else None,
                        )
                # Set cooldown on mob
                cooldown = action.get("cooldown", 0)
                if cooldown and ability_id:
                    cds = dict(getattr(mob.ndb, "ability_cooldowns", None) or {})
                    cds[ability_id] = cooldown
                    mob.ndb.ability_cooldowns = cds
                if check_death(target):
                    if _is_player(target):
                        death_msg = handle_player_death(target)
                    else:
                        death_msg = handle_mob_death(target, mob)
                    if self.obj:
                        self.obj.msg_contents(death_msg)
                    self.remove_combatant(target)
                    return

            elif action_type == "flee":
                if self.obj:
                    self.obj.msg_contents(f"|y{mob.key} flees!|n")
                self.remove_combatant(mob)
                return

            elif action_type == "call_for_help":
                self.ndb.call_for_help_count = (self.ndb.call_for_help_count or 0) + 1
                if self.obj:
                    self.obj.msg_contents(
                        f"|y{mob.key} calls for reinforcements!|n"
                    )

            elif action_type == "cast_start":
                # Telegraph emote fires immediately; cast registered by combat_ai
                emote = action.get("emote") or action.get("text", "")
                if emote and self.obj:
                    self.obj.msg_contents(emote)

            elif action_type == "echo":
                text = action.get("text", "")
                if text and self.obj:
                    self.obj.msg_contents(text)

            elif action_type == "zone_echo":
                text = action.get("text", "")
                if text and self.obj:
                    self.obj.msg_contents(text)

            elif action_type == "spawn":
                mob_key = action.get("mob_key", "")
                count = action.get("count", 1)
                if mob_key and self.obj:
                    from world.mob_spawner import spawn_single_mob
                    spawn_def = {"mob": mob_key}
                    for _ in range(count):
                        spawned = spawn_single_mob(spawn_def, self.obj)
                        if spawned:
                            self.add_combatant(spawned)
                    self.obj.msg_contents(
                        f"|YReinforcements arrive: {mob_key}!|n"
                    )

            elif action_type == "modify_behavior":
                new_behavior = action.get("behavior")
                if new_behavior:
                    mob.ndb.behavior_override = new_behavior

        # Mob turn complete -- advance
        self.advance_turn()

    def process_player_action(self, character, action_type, target=None, ability_id=None):
        """
        Called by combat commands. Validates turn, executes action, advances.

        Args:
            character: The player character acting.
            action_type: One of "basic_attack", "ability", "charge", "flee", "pass".
            target: Target combatant (optional, uses current target if None).
            ability_id: Ability ID for "ability" or "charge" actions.
        """
        # Validate it's this character's turn
        current = self.get_current_combatant()
        if current is None or current.id != character.id:
            character.msg("|rIt's not your turn.|n")
            return

        # Cancel round timer if active
        if self.ndb.turn_timer_id is not None:
            try:
                self.ndb.turn_timer_id.cancel()
            except Exception:
                pass
            self.ndb.turn_timer_id = None

        # Default target
        if target is None:
            target = _get_default_target(character, self)

        from world.combat_engine import (
            resolve_basic_attack, check_death,
            handle_mob_death, handle_player_death,
        )
        from world.base_attributes import record_stat_use, get_damage_modifier

        if action_type == "basic_attack":
            if target is None:
                character.msg("|rNo valid target.|n")
                return
            # Look up equipped main-hand weapon (Fix 3.8)
            from world.inventory_engine import get_equipped_items
            weapon = None
            for item, record in get_equipped_items(character):
                if record.equipment_slot in ("main_hand", "weapon"):
                    weapon = item
                    break
            ok, msg, dmg = resolve_basic_attack(character, target, weapon=weapon)
            character.msg(f"|w{msg}|n")
            if self.obj:
                self.obj.msg_contents(msg, exclude=[character])
            record_stat_use(character, "combat")
            character.ndb.actions_remaining = max(0, (character.ndb.actions_remaining or 1) - 1)

            # Track for Command resource ally-action build
            ally_counts = dict(getattr(self.ndb, "ally_action_count", None) or {})
            for cid in (self.db.combatant_ids or []):
                if cid != character.id:
                    key = str(cid)
                    ally_counts[key] = ally_counts.get(key, 0) + 1
            self.ndb.ally_action_count = ally_counts

            if check_death(target):
                if _is_mob(target):
                    death_msg = handle_mob_death(target, character)
                else:
                    death_msg = handle_player_death(target)
                if self.obj:
                    self.obj.msg_contents(death_msg)
                self.remove_combatant(target)
                return

            if (character.ndb.actions_remaining or 0) <= 0:
                self.advance_turn()

        elif action_type == "ability":
            if ability_id is None:
                character.msg("|rSpecify an ability.|n")
                return
            from world.ability_engine import use_ability
            ok, msg = use_ability(character, ability_id, target=target)
            character.msg(f"|w{msg}|n")
            if self.obj:
                self.obj.msg_contents(msg, exclude=[character])
            character.ndb.ability_used_this_turn = True

            # Track for Command resource ally-action build
            ally_counts = dict(getattr(self.ndb, "ally_action_count", None) or {})
            for cid in (self.db.combatant_ids or []):
                if cid != character.id:
                    key = str(cid)
                    ally_counts[key] = ally_counts.get(key, 0) + 1
            self.ndb.ally_action_count = ally_counts
            # Abilities consume all remaining actions per D-09
            character.ndb.actions_remaining = 0
            if target and check_death(target):
                if _is_mob(target):
                    death_msg = handle_mob_death(target, character)
                else:
                    death_msg = handle_player_death(target)
                if self.obj:
                    self.obj.msg_contents(death_msg)
                self.remove_combatant(target)
                return
            self.advance_turn()

        elif action_type == "charge":
            if ability_id is None:
                character.msg("|rSpecify an ability to charge.|n")
                return
            from world.ability_registry import ABILITIES
            ability = ABILITIES.get(ability_id)
            if not ability:
                character.msg("|rUnknown ability.|n")
                return
            charge_turns = ability.get("charge_turns", 0)
            if charge_turns <= 0:
                character.msg("|rThat ability cannot be charged.|n")
                return
            charged = dict(self.ndb.pending_charged or {})
            charged[character.id] = {
                "ability_id": ability_id,
                "rounds_left": charge_turns,
                "target_id": target.id if target else None,
            }
            self.ndb.pending_charged = charged
            ability_name = ability.get("name", ability_id)
            character.msg(
                f"|yYou begin channeling {ability_name}... "
                f"({charge_turns} rounds)|n"
            )
            if self.obj:
                self.obj.msg_contents(
                    f"|y{character.key} begins channeling {ability_name}...|n",
                    exclude=[character],
                )
            # Character can still basic attack during charge (remaining actions)
            # Don't auto-advance -- let them use remaining actions

        elif action_type == "flee":
            from world.status_effects import get_effect_modifiers
            mods = get_effect_modifiers(character)
            if mods.get("prevents_flee", False):
                character.msg("|rYou are rooted and cannot flee!|n")
                return
            if mods.get("skip_turn", False):
                character.msg("|rYou are incapacitated and cannot flee!|n")
                return
            # Speed + skill check (simple roll)
            base_stats = character.db.base_stats or {}
            agility = base_stats.get("agility", 10)
            flee_roll = random.randint(1, 20) + agility // 5
            if flee_roll >= 12:
                # Success -- move to random adjacent exit
                if self.obj:
                    exits = [
                        e for e in self.obj.exits
                        if e.destination and e.destination != self.obj
                    ]
                    if exits:
                        chosen_exit = random.choice(exits)
                        self.obj.msg_contents(f"|y{character.key} flees the battle!|n")
                        self.remove_combatant(character)
                        character.move_to(chosen_exit.destination, quiet=True)
                        character.msg(f"|gYou flee to {chosen_exit.destination.key}.|n")
                    else:
                        character.msg("|rThere is nowhere to flee!|n")
                else:
                    self.remove_combatant(character)
            else:
                character.msg("|rYou fail to escape!|n")
                character.ndb.actions_remaining = 0
                self.advance_turn()

        elif action_type == "pass":
            character.msg("|yYou pass your turn.|n")
            character.ndb.actions_remaining = 0
            self.advance_turn()

    def _auto_attack_timeout(self, character_id):
        """Called when group combat round timer expires (D-18)."""
        from world.combat_engine import resolve_basic_attack, check_death
        from world.combat_engine import handle_mob_death, handle_player_death

        character = _resolve_by_id(character_id)
        if character is None or not self.is_combatant(character):
            return

        current = self.get_current_combatant()
        if current is None or current.id != character_id:
            return

        target = _get_default_target(character, self)
        if target:
            character.msg("|yTime's up! Auto-attacking...|n")
            # Look up equipped main-hand weapon (Fix 3.8)
            from world.inventory_engine import get_equipped_items
            weapon = None
            for item, record in get_equipped_items(character):
                if record.equipment_slot in ("main_hand", "weapon"):
                    weapon = item
                    break
            ok, msg, dmg = resolve_basic_attack(character, target, weapon=weapon)
            if self.obj:
                self.obj.msg_contents(msg)
            if check_death(target):
                if _is_mob(target):
                    death_msg = handle_mob_death(target, character)
                else:
                    death_msg = handle_player_death(target)
                if self.obj:
                    self.obj.msg_contents(death_msg)
                self.remove_combatant(target)
                return

        self.ndb.turn_timer_id = None
        self.advance_turn()

    # -- round management ----------------------------------------------------

    def end_round(self):
        """
        Process round-end effects for all combatants (D-11).

        Ticks status effects (DoTs, durations), decrements ability cooldowns,
        checks for DoT kills, persists effects to db, increments round number.
        """
        from world.status_effects import tick_effects
        from world.ability_engine import decrement_cooldowns, on_round_end_resources
        from world.combat_engine import check_death, handle_mob_death, handle_player_death

        # Reset ally action counter for Command resource tracking
        self.ndb.ally_action_count = {}

        # Reset took_damage_this_round at round end before tick processing.
        # The flag was set during the round's damage resolution and is consumed
        # by tick_effects (petrify break-on-damage check).  After ticking, reset
        # so it's clean for the next round.
        dead = []
        for combatant in self._resolve_combatants():
            if combatant is None:
                continue
            # Tick effects (reads took_damage_this_round for petrify)
            tick_effects(combatant)
            # Reset the flag after tick processing for the next round
            combatant.ndb.took_damage_this_round = False
            # Decrement cooldowns
            decrement_cooldowns(combatant)
            # Per-round resource hooks (Resonance decay, Focus skip reset, Command ally build)
            on_round_end_resources(combatant, self)
            # Check for DoT kills
            if check_death(combatant):
                dead.append(combatant)

        # Handle deaths from DoTs
        for combatant in dead:
            if _is_mob(combatant):
                # DoT kill -- attribute to last attacker or None
                death_msg = handle_mob_death(combatant, None)
            else:
                death_msg = handle_player_death(combatant)
            if self.obj:
                self.obj.msg_contents(death_msg)
            self.remove_combatant(combatant)

        if not self.db.combatant_ids:
            return

        # Persist active_effects to db for reload survival (Pitfall 1)
        stored = {}
        for combatant in self._resolve_combatants():
            if combatant is None:
                continue
            effects = combatant.ndb.active_effects
            if effects:
                stored[str(combatant.id)] = list(effects)
        self.db.active_effects_db = stored

        self.db.round_number = (self.db.round_number or 1) + 1

        # Notify round change
        if self.obj:
            self.obj.msg_contents(
                f"|c--- Round {self.db.round_number} ---|n"
            )

        # Resolve pending mob casts at the start of the new round (D-11)
        from world.combat_ai import resolve_pending_casts
        resolved = resolve_pending_casts(self)
        for cast_action in resolved:
            self._dispatch_resolved_cast(cast_action)

    def _dispatch_resolved_cast(self, cast_action):
        """
        Dispatch a resolved mob cast through the normal ability resolution path.

        Called when a pending mob cast timer reaches zero and the mob is not
        interrupted. Resolves damage/effects via ability_engine.

        Args:
            cast_action: Action dict from resolve_pending_casts() with combatant_db_id,
                        target_id, ability_id, and ability parameters.
        """
        mob = _resolve_by_id(cast_action.get("combatant_db_id"))
        target = _resolve_by_id(cast_action.get("target_id"))
        if mob is None or target is None:
            return

        from world.combat_engine import check_death, handle_mob_death, handle_player_death

        # Skip if either is already dead
        if check_death(mob) or check_death(target):
            return

        ability_id = cast_action.get("ability_id", "")
        from world.ability_engine import use_ability
        ok, msg = use_ability(mob, ability_id, target=target)
        if self.obj:
            self.obj.msg_contents(msg)

        # Apply cooldown
        cooldown = cast_action.get("cooldown", 0)
        if cooldown > 0 and ability_id:
            cooldowns = dict(getattr(mob.ndb, "ability_cooldowns", None) or {})
            cooldowns[ability_id] = cooldown
            mob.ndb.ability_cooldowns = cooldowns

        # Check death of target
        if check_death(target):
            if _is_player(target):
                death_msg = handle_player_death(target)
            else:
                death_msg = handle_mob_death(target, mob)
            if self.obj:
                self.obj.msg_contents(death_msg)
            self.remove_combatant(target)

    # -- combat end ----------------------------------------------------------

    def end_combat(self):
        """
        Clean up all combat state and delete this script.

        Removes CombatCmdSet from players, clears encounter cooldowns,
        clears all effects, resets ndb combat state.
        """
        from world.ability_engine import clear_encounter_cooldowns, on_encounter_end_resources
        from world.status_effects import clear_all_effects

        for combatant in self._resolve_combatants():
            if combatant is None:
                continue

            # Clear effects on all combatants (players and mobs)
            clear_all_effects(combatant)

            if _is_player(combatant):
                _remove_combat_cmdset(combatant)
                clear_encounter_cooldowns(combatant)
                on_encounter_end_resources(combatant)

            combatant.ndb.combat_handler = None
            combatant.ndb.actions_remaining = 0
            combatant.ndb.ability_used_this_turn = False

            patrol_scripts = combatant.scripts.get("patrol_script") if hasattr(combatant, "scripts") else []
            for patrol_script in patrol_scripts or []:
                try:
                    patrol_script.on_combat_end("combat_ended")
                except Exception:
                    continue

        # Clear pending charged and mob casts
        self.ndb.pending_charged = {}
        self.ndb.pending_mob_casts = {}

        # Cancel active timers
        if self.ndb.turn_timer_id:
            try:
                self.ndb.turn_timer_id.cancel()
            except Exception:
                pass
        self.ndb.turn_timer_id = None
        self.ndb.call_for_help_count = 0

        # Notify
        if self.obj:
            self.obj.msg_contents("|c--- Combat has ended. ---|n")

        self.delete()

    # -- internal helpers ----------------------------------------------------

    def _resolve_combatants(self):
        """Resolve combatant_ids to actual objects. Returns list (may contain None)."""
        ids = self.db.combatant_ids or []
        return [_resolve_by_id(cid) for cid in ids]


# ---------------------------------------------------------------------------
# Module-level functions
# ---------------------------------------------------------------------------

def start_combat(room, initiator, targets):
    """
    Start or join combat in a room.

    If the room already has a CombatScript, joins the existing one.
    Otherwise creates a new one.

    Args:
        room: The room where combat takes place.
        initiator: The combatant starting the fight (player or mob).
        targets: List of combatants being engaged.

    Returns:
        CombatScript: The active combat script.
    """
    # Check for existing combat
    existing = _get_room_combat(room)
    if existing:
        # Join existing combat
        if not existing.is_combatant(initiator):
            join_combat(existing, initiator)
        for target in targets:
            if not existing.is_combatant(target):
                join_combat(existing, target)
        return existing

    # Create new CombatScript on room
    ScriptClass = _get_script_class()
    script = ScriptClass.create(
        key="combat_script",
        obj=room,
        autostart=True,
    )

    # Break node stabilization on combat entry (D-10)
    from world.node_helpers import break_stabilization_on_combat

    # Add all combatants
    all_combatants = [initiator] + list(targets)
    for combatant in all_combatants:
        break_stabilization_on_combat(combatant)
        script.add_combatant(combatant)

    # Check group combat
    script.db.is_group_combat = any(
        _is_player(c) and getattr(c.ndb, "group_state", None)
        for c in all_combatants
    )

    # Notify room
    names = ", ".join(c.key for c in all_combatants)
    room.msg_contents(f"|r--- Combat begins! Combatants: {names} ---|n")
    room.msg_contents(
        f"|cInitiative order: "
        + ", ".join(
            f"{_resolve_by_id(e['id']).key if _resolve_by_id(e['id']) else '?'}"
            for e in script.db.initiative_order
        )
        + "|n"
    )

    # Begin first turn
    script.db.current_turn_index = -1  # advance_turn will increment to 0
    script.advance_turn()

    return script


def join_combat(combat_script, newcomer):
    """
    Insert a new combatant into an ongoing combat.

    Args:
        combat_script: The active CombatScript.
        newcomer: The combatant joining.

    Returns:
        (bool, str): Success flag and message.
    """
    if combat_script.is_combatant(newcomer):
        return False, f"{newcomer.key} is already in combat."

    combat_script.add_combatant(newcomer)

    if combat_script.obj:
        combat_script.obj.msg_contents(
            f"|y{newcomer.key} joins the battle!|n"
        )

    # Recalculate group combat flag
    players = combat_script.get_player_combatants()
    combat_script.db.is_group_combat = any(
        getattr(p.ndb, "group_state", None) for p in players
    )

    return True, f"{newcomer.key} has joined combat."


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------

def _get_room_combat(room):
    """Return existing CombatScript on room, or None."""
    scripts = room.scripts.all()
    for script in scripts:
        if script.key == "combat_script":
            return script
    return None


def _get_script_class():
    """
    Dynamically build and cache the CombatScript typeclass.

    This avoids importing Evennia typeclass infrastructure at module level.
    """
    if not hasattr(_get_script_class, "_cls"):
        from typeclasses.scripts import SoravelonScript as Base

        # Merge CombatScript methods into a proper Evennia script subclass
        cls = type("CombatScript", (Base,), dict(CombatScript.__dict__))
        cls.typename = "CombatScript"
        _get_script_class._cls = cls

    return _get_script_class._cls


def _resolve_by_id(obj_id):
    """Resolve a single object by its database ID."""
    if obj_id is None:
        return None
    try:
        from evennia import search_object
        results = search_object(str(obj_id), exact=False, use_dbref="#" + str(obj_id))
        if results:
            return results[0]
    except Exception:
        pass
    return None


def _is_player(combatant):
    """Check if combatant is a player character."""
    account = getattr(combatant, "account", None)
    if account is not None:
        return True
    return bool(
        hasattr(combatant, "tags")
        and combatant.tags.has("player_character", category="character_type")
    )


def _is_mob(combatant):
    """Check if combatant is a mob (not a player)."""
    return not _is_player(combatant)


def _is_connected(combatant):
    """Check if a player combatant has an active session."""
    account = getattr(combatant, "account", None)
    if account is None:
        return False
    return bool(account.sessions.all())


def _add_combat_cmdset(character):
    """Add CombatCmdSet to a player character."""
    try:
        from commands.combat_commands import CombatCmdSet
        character.cmdset.add(CombatCmdSet, persistent=False)
    except ImportError:
        pass


def _remove_combat_cmdset(character):
    """Remove CombatCmdSet from a player character."""
    try:
        from commands.combat_commands import CombatCmdSet
        character.cmdset.remove(CombatCmdSet)
    except (ImportError, Exception):
        pass


def _get_default_target(character, combat_handler):
    """Get the character's current or default combat target."""
    # Try current target
    target_id = getattr(character.ndb, "combat_target_id", None)
    if target_id:
        target = _resolve_by_id(target_id)
        if target and combat_handler.is_combatant(target):
            from world.combat_engine import check_death
            if not check_death(target):
                return target

    # Fall back to first living mob
    mobs = combat_handler.get_mob_combatants()
    if mobs:
        from world.combat_engine import check_death
        for mob in mobs:
            if not check_death(mob):
                character.ndb.combat_target_id = mob.id
                return mob
    return None


def _send_turn_prompt(character, combat_handler):
    """Build and send a formatted turn prompt to the character."""
    actions = character.ndb.actions_remaining or 0
    target = _get_default_target(character, combat_handler)
    target_name = target.key if target else "none"
    target_hp = ""
    if target and hasattr(target.ndb, "hp") and target.ndb.hp is not None:
        hp_max = getattr(target.db, "hp_max", None) or getattr(target.ndb, "hp_max", 0)
        if hp_max:
            pct = int(100 * target.ndb.hp / hp_max)
            target_hp = f" ({pct}% HP)"

    char_hp = ""
    if hasattr(character.ndb, "hp") and character.ndb.hp is not None:
        hp_max = getattr(character.ndb, "hp_max", 0) or 1
        char_hp = f" | HP: {character.ndb.hp}/{hp_max}"

    # Check for charged ability
    charged_msg = ""
    pending = (combat_handler.ndb.pending_charged or {}).get(character.id)
    if pending:
        charged_msg = f" | Charging: {pending['ability_id']} ({pending['rounds_left']} rounds)"

    rnd = combat_handler.db.round_number or 1
    prompt = (
        f"|c--- Your Turn (Round {rnd}) ---|n\n"
        f"|wTarget: {target_name}{target_hp}{char_hp}{charged_msg}|n\n"
        f"|wActions remaining: {actions}|n\n"
        f"|yCommands: attack, use <ability>, charge <ability>, flee, pass|n"
    )
    character.msg(prompt)


def _build_combat_oob(character, combat_handler):
    """Build OOB data dict for combat_update push."""
    target = _get_default_target(character, combat_handler)
    return {
        "round": combat_handler.db.round_number or 1,
        "actions_remaining": character.ndb.actions_remaining or 0,
        "target_id": target.id if target else None,
        "target_name": target.key if target else None,
        "target_hp": target.ndb.hp if target else None,
        "target_hp_max": (
            getattr(target.db, "hp_max", None) or getattr(target.ndb, "hp_max", None)
        ) if target else None,
        "hp": character.ndb.hp,
        "hp_max": getattr(character.ndb, "hp_max", None),
        "combatants": [
            {"id": c.id, "name": c.key, "is_player": _is_player(c)}
            for c in combat_handler._resolve_combatants() if c
        ],
    }
