"""
Custom CmdHelp override with dynamic ability lookup.

Intercepts `help <ability_name>` queries and renders formatted info from the
ABILITIES registry. All other queries fall through to Evennia's standard help.
"""

from evennia.commands.default.help import CmdHelp as EvenniaCmdHelp


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

        # Try direct ability_id match
        ability = ABILITIES.get(query)

        # Try name match if no direct hit
        if not ability:
            for ab in ABILITIES.values():
                if ab["name"].lower() == query:
                    ability = ab
                    break

        if ability:
            self._display_ability_help(ability)
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
