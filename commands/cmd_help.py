"""
Custom CmdHelp override with dynamic ability lookup.

Intercepts `help <ability_name>` queries and renders formatted info from the
ABILITIES registry. All other queries fall through to Evennia's normal help
pipeline, including file-based help entries.
"""

from evennia.commands.default.help import CmdHelp as EvenniaCmdHelp


def resolve_ability_help_query(query, abilities):
    """
    Resolve a help query against the ability registry.

    Returns ``(ability, matches)`` where ``ability`` is a single resolved
    ability dict or ``None`` and ``matches`` is a list of ambiguous matches.
    """
    normalized = (query or "").strip().lower()
    if not normalized:
        return None, []

    normalized_id = normalized.replace(" ", "_")

    ability = abilities.get(normalized) or abilities.get(normalized_id)
    if ability:
        return ability, []

    exact_name_matches = [
        ability_data
        for ability_data in abilities.values()
        if ability_data.get("name", "").lower() == normalized
    ]
    if len(exact_name_matches) == 1:
        return exact_name_matches[0], []
    if len(exact_name_matches) > 1:
        return None, exact_name_matches

    matches = []
    for ability_id, ability_data in abilities.items():
        name_lower = ability_data.get("name", "").lower()
        if ability_id.startswith(normalized_id) or name_lower.startswith(normalized):
            matches.append(ability_data)

    if len(matches) == 1:
        return matches[0], []

    matches.sort(key=lambda ability_data: ability_data.get("name", ""))
    return None, matches


class CmdHelp(EvenniaCmdHelp):
    """
    View help on commands, systems, and abilities.

    Usage:
      help
      help <topic>

    Displays help for any game topic. If the topic matches an ability
    name, dynamic help is generated from the ability registry.
    """

    def func(self):
        query = self.args.strip().lower()
        if not query:
            super().func()
            return

        # Lazy import to avoid import-time issues
        from world.ability_registry import ABILITIES

        ability, matches = resolve_ability_help_query(query, ABILITIES)

        if ability:
            self._display_ability_help(ability)
            return

        if matches:
            names = ", ".join(match["name"] for match in matches[:6])
            if len(matches) > 6:
                names += ", ..."
            self.caller.msg(f"Which ability did you mean? {names}")
            return

        # Fall through to standard help
        super().func()

    def _display_ability_help(self, ability):
        """Format and display dynamic ability help."""
        name = ability["name"]
        tier = ability["tier"]
        domain = ability["domain"].capitalize()
        effect_type = ability["effect_type"].replace("_", " ").capitalize()
        description = ability["description"]
        resource_cost = ability["resource_cost"]
        resource_type = ability["resource_type"].capitalize()
        cooldown = ability["cooldown"]
        scaling_primary = ability["scaling_primary"].capitalize()
        scaling_secondary = ability.get("scaling_secondary")
        charge_turns = ability.get("charge_turns", 0)
        subclass_id = ability.get("subclass_id")

        lines = []
        lines.append(f"|wAbility: {name}|n")
        lines.append(f"|xTier {tier} | {domain} | {effect_type}|n")
        lines.append("")
        lines.append(description)
        lines.append("")
        lines.append(f"|cResource:|n {resource_cost} {resource_type}")
        lines.append(f"|cCooldown:|n {cooldown} rounds")

        scaling_text = scaling_primary
        if scaling_secondary:
            scaling_text += f" / {scaling_secondary.capitalize()}"
        lines.append(f"|cScaling:|n {scaling_text}")

        if charge_turns:
            lines.append(f"|cCharge:|n {charge_turns} turns")

        if subclass_id:
            lines.append(f"|cSubclass:|n {subclass_id.replace('_', ' ').title()}")

        self.caller.msg("\n".join(lines))
