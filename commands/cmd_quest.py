"""
Quest management commands.

Usage:
    quest             - List active quests
    quest <name>      - Show quest details
    quest abandon <name> - Abandon a quest
    quest share <name>   - Offer a shareable quest to nearby group members
    quest accept <name>  - Accept a shared quest offer
    quest decline <name> - Decline a shared quest offer
    quest offers         - Review pending shared quest offers
"""

from commands.command import Command


class CmdQuest(Command):
    """
    View and manage your active quests.

    Usage:
      quest                   List all active quests
      quest <name>            Show quest details
      quest abandon <name>    Abandon a quest
      quest share <name>      Offer a shareable quest to nearby allies
      quest accept <name>     Accept a shared quest offer
      quest decline <name>    Decline a shared quest offer
      quest offers             Review pending shared quest offers

    Shows quest name, progress, giver, and objectives.
    """

    key = "quest"
    aliases = ["quests"]
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        character = self.caller
        args = self.args.strip()

        if args.lower() == "offers":
            self._list_share_offers(character)
            return

        for subcommand, handler in (
            ("abandon", self._abandon),
            ("share", self._share),
            ("accept", self._accept_shared),
            ("decline", self._decline_shared),
        ):
            prefix = f"{subcommand} "
            if args.lower().startswith(prefix):
                handler(character, args[len(prefix):].strip())
                return

        if not args:
            self._list_quests(character)
        else:
            self._detail(character, args)

    def _list_quests(self, character):
        """List all active quests (D-15, D-16)."""
        from world.quest_engine import get_active_quests, get_character_quest_spec
        quests = get_active_quests(character)

        if not quests:
            character.msg("|yYou have no active quests.|n")
            return

        lines = ["|w=== Active Quests ===|n"]
        for cq in quests:
            spec = get_character_quest_spec(cq)
            if spec:
                name = spec.get("name", cq.quest_id)
                giver = spec.get("quest_giver", "unknown")
                # Build progress bar
                objectives = spec.get("objectives", [])
                total_required = 0
                total_done = 0
                progress_dict = cq.progress or {}
                for obj in objectives:
                    obj_key = f"{obj.get('type', 'unknown')}_{obj.get('target', 'unknown')}"
                    count = obj.get("count", 1)
                    done = progress_dict.get(obj_key, 0)
                    total_required += count
                    total_done += min(done, count)
                if total_required > 0:
                    pct = int(total_done / total_required * 100)
                    bar_filled = int(pct / 10)
                    bar_empty = 10 - bar_filled
                    bar = f"|g{'#' * bar_filled}|x{'.' * bar_empty}|n"
                    progress_str = f"[{bar}] {pct}%"
                else:
                    progress_str = "[|x..........|n]"
            else:
                name = cq.quest_id
                giver = "?"
                progress_str = "[?]"

            # Replace underscores in giver name for display
            giver_display = giver.replace("npc_", "").replace("_", " ").title()
            lines.append(f"  |w{name}|n  {progress_str}  (from {giver_display})")

        character.msg("\n".join(lines))

    def _detail(self, character, quest_name):
        """Show detailed quest info (D-16)."""
        from world.quest_engine import get_active_quests, get_character_quest_spec

        quests = get_active_quests(character)
        # Match by name (case-insensitive partial)
        match = None
        for cq in quests:
            spec = get_character_quest_spec(cq)
            if spec:
                name = spec.get("name", cq.quest_id)
                if quest_name.lower() in name.lower() or quest_name.lower() in cq.quest_id.lower():
                    match = (cq, spec)
                    break

        if not match:
            character.msg(f"|rNo active quest matching '{quest_name}'.|n")
            return

        cq, spec = match
        name = spec.get("name", cq.quest_id)
        desc = spec.get("description", "No description.")
        giver = spec.get("quest_giver", "unknown")
        giver_display = giver.replace("npc_", "").replace("_", " ").title()
        progress_dict = cq.progress or {}

        lines = [
            f"|w=== {name} ===|n",
            f"|x{desc}|n",
            f"|xGiven by: {giver_display}|n",
            "",
            "|wObjectives:|n",
        ]

        for obj in spec.get("objectives", []):
            obj_type = obj.get("type", "unknown")
            obj_target = obj.get("target", "unknown")
            obj_count = obj.get("count", 1)
            obj_desc = obj.get("description", f"{obj_type} {obj_target}")
            obj_key = f"{obj_type}_{obj_target}"
            done = progress_dict.get(obj_key, 0)
            done = min(done, obj_count)
            if done >= obj_count:
                status = "|g[DONE]|n"
            else:
                status = f"|y[{done}/{obj_count}]|n"
            lines.append(f"  {status} {obj_desc}")

        # Rewards preview
        rewards = spec.get("rewards", [])
        if rewards:
            lines.append("")
            lines.append("|wRewards:|n")
            for r in rewards:
                rtype = r.get("action_type", "?")
                if rtype == "give_scales":
                    lines.append(f"  |y{r.get('amount', 0)} Scales|n")
                elif rtype == "modify_standing":
                    faction = r.get("faction_id", "?").replace("_", " ").title()
                    delta = r.get("delta", 0)
                    sign = "+" if delta > 0 else ""
                    lines.append(f"  |c{sign}{delta} {faction} Standing|n")
                elif rtype == "give_item":
                    lines.append(f"  |w{r.get('template_id', 'item').replace('_', ' ').title()}|n")
                elif rtype == "give_skill_xp":
                    skill = r.get("skill_id", "?").replace("_", " ").title()
                    lines.append(f"  |gSkill insight: {skill}|n")
                elif rtype == "grant_practice":
                    skills = sorted((r.get("skill_awards") or r.get("skills") or {}).keys())
                    if skills:
                        skill_names = ", ".join(s.replace("_", " ").title() for s in skills)
                        lines.append(f"  |gMeaningful practice: {skill_names}|n")
                    else:
                        lines.append("  |gMeaningful practice|n")
                elif rtype == "learn_recipe":
                    lines.append(f"  |mRecipe: {r.get('recipe_id', '?').replace('_', ' ').title()}|n")
                # Skip echo/teleport/spawn_mob in rewards preview

        character.msg("\n".join(lines))

    def _abandon(self, character, quest_name):
        """Abandon a quest (D-04, D-15)."""
        from world.quest_engine import abandon_quest, get_active_quests, get_character_quest_spec

        quests = get_active_quests(character)
        match_id = None
        for cq in quests:
            spec = get_character_quest_spec(cq)
            if spec:
                name = spec.get("name", cq.quest_id)
                if quest_name.lower() in name.lower() or quest_name.lower() in cq.quest_id.lower():
                    match_id = cq.quest_id
                    break

        if not match_id:
            character.msg(f"|rNo active quest matching '{quest_name}'.|n")
            return

        success, msg = abandon_quest(character, match_id)
        character.msg(f"|y{msg}|n" if success else f"|r{msg}|n")

    def _share(self, character, quest_name):
        from world.quest_engine import share_quest

        success, message = share_quest(character, quest_name)
        character.msg(f"|g{message}|n" if success else f"|r{message}|n")

    def _accept_shared(self, character, quest_name):
        from world.quest_engine import accept_shared_quest

        success, message = accept_shared_quest(character, quest_name)
        character.msg(f"|g{message}|n" if success else f"|r{message}|n")

    def _decline_shared(self, character, quest_name):
        from world.quest_engine import decline_shared_quest

        success, message = decline_shared_quest(character, quest_name)
        character.msg(f"|y{message}|n" if success else f"|r{message}|n")

    def _list_share_offers(self, character):
        from world.quest_engine import get_pending_share_offers

        offers = list(get_pending_share_offers(character))
        if not offers:
            character.msg("|yYou have no pending shared quest offers.|n")
            return

        lines = ["|w=== Shared Quest Offers ===|n"]
        for offer in offers:
            name = offer.quest_spec.get("name") or offer.quest_id
            lines.append(f"  |w{name}|n — offered by {offer.sender.key}")
            lines.append(
                f"    |xquest accept {name}  /  quest decline {name}|n"
            )
        character.msg("\n".join(lines))
