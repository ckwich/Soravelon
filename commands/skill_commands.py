"""
Skill commands for Soravelon.

CmdSkills: View skill summary or details, filtered by category.
CmdPractice: Practice a skill (24hr rolling cooldown per skill).
CmdTrain: Train with an NPC trainer (framework ready for content phase).

All commands use the (bool, str) return tuple convention from skill_engine.
"""

from commands.command import Command


class CmdSkills(Command):
    """
    View your skills.

    Usage:
      skills               - summary of all non-zero skills
      skills general       - general proficiency skills
      skills attunement    - zone, node, and creature attunement skills
      skills <skill_name>  - detailed view of a specific skill

    Only shows skills with a value above 0.
    """

    key = "skills"
    aliases = ["skill"]
    locks = "cmd:all()"
    help_category = "Character"

    def func(self):
        from world.skill_definitions import SKILL_DEFINITIONS
        from world.skill_engine import get_skill_value, get_skills_by_type

        caller = self.caller
        args = self.args.strip().lower()

        if not args:
            self._show_summary(caller)
        elif args == "general":
            self._show_category(caller, "general", "General Proficiencies")
        elif args == "attunement":
            self._show_attunement(caller)
        else:
            self._show_detail(caller, args)

    def _show_summary(self, caller):
        """Show count of non-zero skills per category and top 3."""
        from world.skill_engine import get_skills_by_type

        general = get_skills_by_type(caller, "general")
        zone_att = get_skills_by_type(caller, "zone_attunement")
        node_att = get_skills_by_type(caller, "node_attunement")
        creature_att = get_skills_by_type(caller, "creature_attunement")

        lines = ["|w--- Skills ------|n"]
        lines.append(f"  General: {len(general)} skills")
        att_count = len(zone_att) + len(node_att) + len(creature_att)
        lines.append(f"  Attunement: {att_count} skills")

        # Top 3 highest across all categories
        all_skills = general + zone_att + node_att + creature_att
        all_skills.sort(key=lambda s: s["value"], reverse=True)
        top = all_skills[:3]
        if top:
            lines.append("")
            lines.append("|wTop Skills:|n")
            for s in top:
                color = "|g" if s["value"] >= 75 else "|y"
                lines.append(
                    f"  {s['name']:20s} {color}{s['value']:.0f}|n"
                )

        if not all_skills:
            lines.append("")
            lines.append("  No skills learned yet.")

        caller.msg("\n".join(lines))

    def _show_category(self, caller, skill_type, header):
        """Show all non-zero skills of a given type."""
        from world.skill_engine import get_skills_by_type

        skills = get_skills_by_type(caller, skill_type)
        lines = [f"|w--- {header} ------|n"]

        if not skills:
            lines.append("  No skills in this category yet.")
        else:
            lines.append(f"  {'Name':20s} {'Value':>5s}")
            lines.append(f"  {'-' * 20} {'-' * 5}")
            for s in skills:
                color = "|g" if s["value"] >= 75 else "|y" if s["value"] >= 25 else "|n"
                lines.append(
                    f"  {s['name']:20s} {color}{s['value']:5.0f}|n"
                )

        caller.msg("\n".join(lines))

    def _show_attunement(self, caller):
        """Show zone, node, and creature attunement skills."""
        from world.skill_engine import get_skills_by_type

        lines = ["|w--- Attunement Skills ------|n"]

        for stype, label in [
            ("zone_attunement", "Zone"),
            ("node_attunement", "Node"),
            ("creature_attunement", "Creature"),
        ]:
            skills = get_skills_by_type(caller, stype)
            if skills:
                lines.append(f"\n  |w{label}:|n")
                for s in skills:
                    color = "|g" if s["value"] >= 75 else "|y"
                    lines.append(
                        f"    {s['name']:20s} {color}{s['value']:5.0f}|n"
                    )

        if len(lines) == 1:
            lines.append("  No attunement skills yet.")

        caller.msg("\n".join(lines))

    def _show_detail(self, caller, search_term):
        """Show detailed view of a specific skill."""
        from world.skill_definitions import SKILL_DEFINITIONS
        from world.skill_engine import get_skill_value
        from world.skill_affordances import get_skill_implementation_notice

        # Match against SKILL_DEFINITIONS keys: startswith then substring
        match = None
        for skill_id, defn in SKILL_DEFINITIONS.items():
            if skill_id == search_term or defn["name"].lower() == search_term:
                match = (skill_id, defn)
                break

        if not match:
            # Try startswith
            candidates = []
            for skill_id, defn in SKILL_DEFINITIONS.items():
                if skill_id.startswith(search_term) or defn["name"].lower().startswith(search_term):
                    candidates.append((skill_id, defn))
            if len(candidates) == 1:
                match = candidates[0]
            elif len(candidates) > 1:
                names = ", ".join(c[1]["name"] for c in candidates)
                caller.msg(f"|yMultiple matches: {names}. Be more specific.|n")
                return
            else:
                # Try substring
                for skill_id, defn in SKILL_DEFINITIONS.items():
                    if search_term in skill_id or search_term in defn["name"].lower():
                        candidates.append((skill_id, defn))
                if len(candidates) == 1:
                    match = candidates[0]
                elif len(candidates) > 1:
                    names = ", ".join(c[1]["name"] for c in candidates)
                    caller.msg(f"|yMultiple matches: {names}. Be more specific.|n")
                    return

        if not match:
            caller.msg("|yNo skill found matching that name.|n")
            return

        skill_id, defn = match
        value = get_skill_value(caller, skill_id)
        color = "|g" if value >= 75 else "|y" if value >= 25 else "|n"

        lines = [f"|w--- {defn['name']} ------|n"]
        lines.append(f"  {defn['description']}")
        notice = get_skill_implementation_notice(skill_id)
        lines.append(f"  |wStatus:|n {notice['label']}")
        lines.append(f"  {notice['summary']}")
        lines.append(f"  Current value: {color}{value:.0f}|n")
        if defn.get("domain_bonus"):
            lines.append(f"  Domain bonus: {defn['domain_bonus']}")

        # Thresholds
        thresholds = defn.get("thresholds", {})
        if thresholds:
            lines.append("")
            if notice["status"] == "live":
                lines.append("  |wThresholds:|n")
            else:
                lines.append("  |wDesign targets (not live thresholds):|n")
            for threshold, desc in sorted(thresholds.items()):
                marker = "|g*" if value >= threshold else " "
                lines.append(f"  {marker} {threshold:3d}: {desc}|n")

        trainer_above = defn.get("trainer_required_above", 50)
        lines.append(f"\n  |wTrainer recommended above: {trainer_above}|n")

        caller.msg("\n".join(lines))


class CmdPractice(Command):
    """
    Practice a skill to improve it.

    Usage:
      practice <skill_name>

    Each skill has a 24-hour rolling cooldown between practice sessions.
    Higher skill values gain less from practice (diminishing returns).
    Training with an NPC beforehand enhances the next practice gain.
    """

    key = "practice"
    locks = "cmd:all()"
    help_category = "Character"

    def func(self):
        from world.skill_definitions import SKILL_DEFINITIONS
        from world.skill_engine import practice_skill

        caller = self.caller
        args = self.args.strip().lower()

        if not args:
            caller.msg("Usage: practice <skill_name>")
            return

        # Match skill name: exact, startswith, then substring
        skill_id = self._resolve_skill(args)
        if not skill_id:
            return

        success, message = practice_skill(caller, skill_id)
        caller.msg(message)

    def _resolve_skill(self, search_term):
        """Resolve a search term to a skill_id."""
        from world.skill_definitions import SKILL_DEFINITIONS

        # Exact match
        if search_term in SKILL_DEFINITIONS:
            return search_term
        for skill_id, defn in SKILL_DEFINITIONS.items():
            if defn["name"].lower() == search_term:
                return skill_id

        # Startswith
        candidates = []
        for skill_id, defn in SKILL_DEFINITIONS.items():
            if skill_id.startswith(search_term) or defn["name"].lower().startswith(search_term):
                candidates.append((skill_id, defn))
        if len(candidates) == 1:
            return candidates[0][0]
        if len(candidates) > 1:
            names = ", ".join(c[1]["name"] for c in candidates)
            self.caller.msg(f"|yMultiple matches: {names}. Be more specific.|n")
            return None

        # Substring
        candidates = []
        for skill_id, defn in SKILL_DEFINITIONS.items():
            if search_term in skill_id or search_term in defn["name"].lower():
                candidates.append((skill_id, defn))
        if len(candidates) == 1:
            return candidates[0][0]
        if len(candidates) > 1:
            names = ", ".join(c[1]["name"] for c in candidates)
            self.caller.msg(f"|yMultiple matches: {names}. Be more specific.|n")
            return None

        self.caller.msg("|yNo skill found matching that name.|n")
        return None


class CmdTrain(Command):
    """
    Train with an NPC trainer to enhance your next practice session.

    Usage:
      train with <npc_name>
      train <skill_name> with <npc_name>

    Training costs Scales and applies a bonus multiplier to your next
    practice session for the trained skill.
    """

    key = "train"
    locks = "cmd:all()"
    help_category = "Character"

    def func(self):
        from world.skill_definitions import TRAINER_REGISTRY
        from world.skill_engine import train_with_trainer

        caller = self.caller
        args = self.args.strip()

        if not args:
            caller.msg("Usage: train with <npc_name> OR train <skill> with <npc>")
            return

        if not TRAINER_REGISTRY:
            caller.msg("|yNo trainers available yet.|n")
            return

        # Parse: "train with <npc>" or "train <skill> with <npc>"
        skill_name = None
        npc_name = None

        if " with " in args.lower():
            parts = args.lower().split(" with ", 1)
            if parts[0].strip():
                skill_name = parts[0].strip()
            npc_name = parts[1].strip()
        else:
            caller.msg("Usage: train with <npc_name> OR train <skill> with <npc>")
            return

        if not npc_name:
            caller.msg("Which NPC do you want to train with?")
            return

        # Find NPC in room by name
        npc = None
        for obj in caller.location.contents:
            if obj == caller:
                continue
            if npc_name in obj.key.lower():
                npc = obj
                break

        if not npc:
            caller.msg(f"|yYou don't see '{npc_name}' here.|n")
            return

        # Look up trainer_id from NPC
        trainer_id = npc.tags.get(category="trainer_id") or npc.db.trainer_id
        if not trainer_id:
            caller.msg(f"|y{npc.key} is not a trainer.|n")
            return

        trainer_data = TRAINER_REGISTRY.get(trainer_id)
        if not trainer_data:
            caller.msg(f"|y{npc.key} is not a registered trainer.|n")
            return

        # Determine skill to train
        if skill_name:
            # Resolve skill name
            from world.skill_definitions import SKILL_DEFINITIONS
            resolved = None
            for sid, defn in SKILL_DEFINITIONS.items():
                if sid == skill_name or defn["name"].lower() == skill_name:
                    resolved = sid
                    break
            if not resolved:
                for sid, defn in SKILL_DEFINITIONS.items():
                    if sid.startswith(skill_name) or defn["name"].lower().startswith(skill_name):
                        resolved = sid
                        break
            if not resolved:
                caller.msg(f"|yNo skill found matching '{skill_name}'.|n")
                return
            skill_id = resolved
        else:
            # If trainer teaches only one skill, use it
            taught = trainer_data.get("skills_taught", [])
            if len(taught) == 1:
                skill_id = taught[0]
            else:
                from world.skill_definitions import SKILL_DEFINITIONS
                names = ", ".join(
                    SKILL_DEFINITIONS.get(s, {}).get("name", s)
                    for s in taught
                )
                caller.msg(
                    f"|y{npc.key} teaches: {names}. "
                    f"Specify which skill: train <skill> with {npc.key}|n"
                )
                return

        success, message = train_with_trainer(caller, skill_id, trainer_id)
        caller.msg(message)
