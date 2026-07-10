"""
Ability execution engine.

Dispatches all abilities through effect-type handlers. Manages cooldowns
(ndb, per-encounter) and domain resources (ndb, volatile).

Effect handlers delegate to combat_engine.py for damage/heal resolution
and status_effects.py for buff/debuff/DoT application.

Resource handlers provide type-aware build/spend/decay for all 10 domain
resource systems (Focus, Balance, Resonance, Influence, Momentum, Mana,
Reagents, Command, Components, Echoes).

Exports:
    use_ability, clear_encounter_cooldowns, decrement_cooldowns,
    build_domain_resource, spend_domain_resource, get_domain_resource,
    initialize_domain_resource, EFFECT_HANDLERS, RESOURCE_HANDLERS,
    decay_resonance, on_round_end_resources, on_encounter_end_resources,
    handle_focus_miss, get_balance_modifier, build_momentum_on_damage,
    get_command_round_preview
"""

import random


# ---------------------------------------------------------------------------
# Effect handlers -- wired to real combat resolution via combat_engine and
# status_effects (lazy imports to avoid circular dependencies)
# ---------------------------------------------------------------------------

def _is_player(combatant):
    """Return True when combatant is a player character rather than a mob."""
    return bool(getattr(combatant.db, "base_stats", None))


def _description_mentions_group_allies(ability):
    """Infer group-support behavior from legacy ability descriptions."""
    desc = (ability.get("description") or "").lower()
    phrases = (
        "all allies",
        "entire group",
        "group heal",
        "the whole team",
        "everyone fights better",
        "allies gain",
        "group tactical buff",
    )
    return any(phrase in desc for phrase in phrases)


def _description_mentions_enemy_aoe(ability):
    """Infer multi-enemy behavior from legacy ability descriptions."""
    desc = (ability.get("description") or "").lower()
    phrases = (
        "all enemies",
        "all nearby",
        "nearby enemies",
        "all enemies in the room",
        "all enemies in the area",
        "everyone in range",
        "all nearby foes",
    )
    return any(phrase in desc for phrase in phrases)


def _collect_ally_targets(character):
    """Return reachable ally targets for group-oriented abilities."""
    if not _is_player(character):
        return [character]

    leader_id = getattr(character.ndb, "group_leader_id", None)
    if leader_id:
        from world.group_engine import _get_leader, _get_group_members

        leader = _get_leader(character)
        if leader:
            members = []
            for member in _get_group_members(leader):
                if member and getattr(member, "location", None) == getattr(character, "location", None):
                    members.append(member)
            if members:
                return members
    return [character]


def _collect_enemy_targets(character, target=None, include_all=False):
    """Return enemy targets in combat, or the explicit target as fallback."""
    handler = getattr(character.ndb, "combat_handler", None)
    if handler:
        if _is_player(character):
            enemies = [enemy for enemy in handler.get_mob_combatants() if enemy]
        else:
            enemies = [enemy for enemy in handler.get_player_combatants() if enemy]
        if target and target in enemies:
            if include_all:
                ordered = [target] + [enemy for enemy in enemies if enemy != target]
                return ordered
            return [target]
        if include_all:
            return enemies
    return [target] if target else []


def _build_effect_data(params, effect_type=None, extra=None):
    """Extract effect metadata needed by runtime-backed status effects."""
    data = {}
    for key in (
        "value",
        "stats",
        "reflect_percent",
        "damage_per_round",
        "heal_per_round",
        "damage_per_tick",
        "heal_source_per_round",
        "heal_allies_per_round",
        "component_type",
        "reagent_type",
        "action_budget_bonus",
        "bonus_poison_damage",
        "status_effect",
        "duration",
        "magnitude",
        "secondary_effects",
        "applies_to_next_attack",
    ):
        if key in params:
            data[key] = params[key]
    if params.get("reflect_damage"):
        data["reflect_percent"] = params.get("reflect_percent", data.get("reflect_percent", 0.25))
    if "bonus_actions" in params:
        data["action_budget_bonus"] = params["bonus_actions"]
    if "absorb" in params:
        data["absorb"] = params["absorb"]
        data["remaining"] = params["absorb"]
    if "value" in params and effect_type == "damage_absorb":
        data["remaining"] = params["value"]
    if params.get("resource_refund") and "refund_percent" in params:
        data["value"] = params["refund_percent"]
    if extra:
        data.update(extra)
    return data


def _apply_effects_to_targets(source, targets, effect_type, duration, magnitude=1.0, data=None):
    """Apply the same status effect to a list of targets."""
    from world import status_effects

    results = []
    for target in targets:
        if data:
            ok, msg = status_effects.apply_effect(
                target,
                effect_type,
                duration,
                magnitude,
                source.id,
                data=data,
            )
        else:
            ok, msg = status_effects.apply_effect(
                target,
                effect_type,
                duration,
                magnitude,
                source.id,
            )
        results.append((target, ok, msg))
    return results


def _apply_secondary_buffs(source, targets, params):
    """Apply optional follow-up buffs authored on multi-effect abilities."""
    secondary_buffs = list(params.get("secondary_buffs", []) or [])
    party_scale = 1.0
    if params.get("party_size_scaling"):
        party_scale = min(1.30, 1.0 + (0.05 * max(0, len(targets) - 1)))
    if params.get("buff_type") and "buff_value" in params:
        secondary_buffs.append(
            {
                "buff_type": params["buff_type"],
                "duration": params.get("buff_duration", params.get("duration", 3)),
                "magnitude": params.get("buff_value", 1.0),
                "value": params.get("buff_value"),
            }
        )

    applied = 0
    for buff in secondary_buffs:
        buff = dict(buff)
        for numeric_key in ("value", "magnitude"):
            if isinstance(buff.get(numeric_key), (int, float)):
                buff[numeric_key] = buff[numeric_key] * party_scale
        effect_type = buff.get("buff_type")
        if not effect_type:
            continue
        results = _apply_effects_to_targets(
            source,
            targets,
            effect_type,
            buff.get("duration", 3),
            buff.get("magnitude", buff.get("value", 1.0)),
            data=_build_effect_data(buff, effect_type=effect_type),
        )
        applied += sum(1 for _, ok, _ in results if ok)
    return applied


def _count_negative_effects(target):
    """Count the active hostile effects on a target for finisher scaling."""
    negative_types = {
        "poison", "bleed", "burn", "weaken", "slow", "root", "blind",
        "shocked", "stun", "charm", "silence", "frozen", "drain",
        "petrify", "steam", "discharge", "corruption", "venom_lag",
    }
    effects = getattr(target.ndb, "active_effects", []) or []
    return sum(1 for entry in effects if entry.get("type") in negative_types)


def _restore_companion_state(character):
    """Best-effort construct restoration for engineering capstones."""
    restored = False

    for current_key, max_key in (
        ("companion_hp", "companion_hp_max"),
        ("companion_durability", "companion_max_durability"),
    ):
        current = getattr(character.db, current_key, None)
        maximum = getattr(character.db, max_key, None)
        if isinstance(current, (int, float)) and isinstance(maximum, (int, float)):
            setattr(character.db, current_key, maximum)
            restored = True

    state = getattr(character.db, "companion_state", None)
    if isinstance(state, dict):
        updated = dict(state)
        for current_key, max_key in (("hp", "max_hp"), ("durability", "max_durability")):
            if isinstance(updated.get(current_key), (int, float)) and isinstance(updated.get(max_key), (int, float)):
                updated[current_key] = updated[max_key]
                restored = True
        if restored:
            character.db.companion_state = updated

    return restored

def _handle_damage(character, ability, target):
    """Resolve single-target or area damage via combat_engine."""
    from world.combat_engine import resolve_ability_damage
    from world.combat_engine import resolve_heal
    from world import status_effects

    params = ability.get("effect_params", {})
    enemy_targets = _collect_enemy_targets(
        character,
        target=target,
        include_all=params.get("aoe") or params.get("area") or _description_mentions_enemy_aoe(ability),
    )
    ally_targets = _collect_ally_targets(character)
    if not enemy_targets and not params.get("heal_allies"):
        return False, f"{ability['name']} has no valid target."

    total_damage = 0
    hits = []
    hit_targets = []
    hit_cycles = 1
    resource = getattr(character.ndb, "domain_resource", None) or {}
    focus_spent = resource.get("current", 0) if resource.get("type") == "focus" else 0
    for index, enemy in enumerate(enemy_targets):
        working_ability = dict(ability)
        working_params = dict(params)
        if index > 0 and params.get("aoe_damage_base"):
            working_params["damage_base"] = params["aoe_damage_base"]
        if params.get("is_multi_hit"):
            hit_cycles = max(1, focus_spent) if params.get("consumes_all_focus") else max(1, params.get("hit_count", 2))
            base_per_hit = working_params.get(
                "damage_per_hit",
                max(1, int((working_params.get("damage_base") or ability.get("damage_base", 15)) / max(1, hit_cycles))),
            )
            base_per_hit += max(0, _count_negative_effects(enemy) * 6)
            if params.get("consumes_all_focus"):
                base_per_hit += max(0, focus_spent - 1) * 8

            chained_damage = 0
            for hit_index in range(hit_cycles):
                chained_params = dict(working_params)
                chained_params["damage_base"] = base_per_hit + max(0, hit_index - 1) * 4
                chained_ability = dict(working_ability)
                chained_ability["effect_params"] = chained_params
                ok, _, dmg = resolve_ability_damage(character, chained_ability, enemy)
                if ok:
                    chained_damage += dmg
            if chained_damage > 0:
                total_damage += chained_damage
                hits.append((enemy, chained_damage))
                hit_targets.append(enemy)
        else:
            if params.get("random_bonus"):
                working_params["damage_base"] = int(working_params.get("damage_base", ability.get("damage_base", 15)) * random.uniform(0.8, 1.25))
            if params.get("ancient_effect"):
                working_params["guaranteed_crit"] = True
            if params.get("world_effect"):
                working_params["piercing"] = True
            if params.get("summon_duration") and target is not None:
                working_params["periodic_target_id"] = getattr(target, "id", None)
            working_ability["effect_params"] = working_params
            ok, _, dmg = resolve_ability_damage(character, working_ability, enemy)
            if ok:
                total_damage += dmg
                hits.append((enemy, dmg))
                hit_targets.append(enemy)

    total_healing = 0
    if params.get("heal_allies"):
        heal_ability = dict(ability)
        heal_params = dict(params)
        heal_params["heal_base"] = params["heal_allies"]
        heal_ability["effect_params"] = heal_params
        for ally in ally_targets:
            _, _, healed = resolve_heal(character, heal_ability, ally)
            total_healing += healed

    debuffs_applied = 0
    if hit_targets and params.get("debuff_type"):
        debuff_duration = params.get("debuff_duration", params.get("duration", ability.get("effect_duration", 3)))
        debuff_magnitude = params.get("debuff_magnitude", params.get("magnitude", ability.get("effect_magnitude", 1.0)))
        for enemy in hit_targets:
            results = _apply_effects_to_targets(
                character,
                [enemy],
                params["debuff_type"],
                debuff_duration,
                debuff_magnitude,
                data=_build_effect_data(
                    params,
                    effect_type=params["debuff_type"],
                    extra={
                        "ability_name": ability["name"],
                    },
                ),
            )
            debuffs_applied += sum(1 for _, ok, _ in results if ok)
        if params.get("secondary_debuff"):
            _apply_effects_to_targets(
                character,
                hit_targets,
                params["secondary_debuff"],
                params.get("secondary_duration", debuff_duration),
                params.get("secondary_magnitude", debuff_magnitude),
                data=_build_effect_data(params, effect_type=params["secondary_debuff"]),
            )

    direct_buffs = 0
    buff_targets = []
    if params.get("buff_type"):
        buff_targets = (
            ally_targets
            if params.get("group_buff") or _description_mentions_group_allies(ability)
            else [character]
        )
        results = _apply_effects_to_targets(
            character,
            buff_targets,
            params["buff_type"],
            params.get("buff_duration", params.get("duration", ability.get("effect_duration", 3))),
            params.get("buff_value", params.get("magnitude", ability.get("effect_magnitude", 1.0))),
            data=_build_effect_data(
                params,
                effect_type=params["buff_type"],
                extra={
                    "ability_name": ability["name"],
                    "scaling_primary": ability.get("scaling_primary"),
                    "scaling_secondary": ability.get("scaling_secondary"),
                    "element": ability.get("element", "physical"),
                    "periodic_target_id": getattr(target, "id", None) if target else None,
                },
            ),
        )
        direct_buffs = sum(1 for _, ok, _ in results if ok)

    summon_applied = 0
    if params.get("summon_duration"):
        periodic_damage = params.get(
            "damage_per_round",
            max(20, int((params.get("damage_base") or ability.get("damage_base", 30)) * 0.45)),
        )
        summon_results = _apply_effects_to_targets(
            character,
            [character],
            "sustained_attack",
            params["summon_duration"],
            1.0,
            data=_build_effect_data(
                params,
                effect_type="sustained_attack",
                extra={
                    "damage_per_round": periodic_damage,
                    "ability_name": ability["name"],
                    "scaling_primary": ability.get("scaling_primary"),
                    "scaling_secondary": ability.get("scaling_secondary"),
                    "element": ability.get("element", "physical"),
                    "periodic_target_id": getattr(target, "id", None) if target else None,
                    "status_effect": params.get("status_effect"),
                    "status_duration": params.get("status_duration", params.get("duration", 3)),
                    "status_magnitude": params.get("status_magnitude", params.get("magnitude", 1.0)),
                    "secondary_effects": params.get("secondary_effects", []),
                },
            ),
        )
        summon_applied = sum(1 for _, ok, _ in summon_results if ok)

    buffs_applied = _apply_secondary_buffs(character, buff_targets or ally_targets, params) + direct_buffs

    bonus_notes = []
    if hit_targets and params.get("random_bonus"):
        bonus = random.choice(("heal", "haste", "resource"))
        if bonus == "heal":
            heal_ability = {"name": ability["name"], "scaling_primary": ability.get("scaling_primary"), "effect_params": {"heal_base": 45}}
            _, _, healed = resolve_heal(character, heal_ability, character)
            if healed > 0:
                bonus_notes.append(f"The anomalous surge restores |g{healed}|n health.")
        elif bonus == "haste":
            status_effects.apply_effect(character, "haste", 2, 1.0, character.id, data={"action_budget_bonus": 1})
            bonus_notes.append("The anomaly accelerates your next movements.")
        else:
            gained = build_domain_resource(character, 15)
            bonus_notes.append("The anomaly feeds your resource reserves.")

    if hit_targets and params.get("ancient_effect"):
        ancient_effect = random.choice(("accuracy", "warding", "echoes"))
        if ancient_effect == "accuracy":
            status_effects.apply_effect(character, "accuracy", 3, 0.20, character.id, data={"value": 0.20})
            bonus_notes.append("Ancient alignment sharpens your aim.")
        elif ancient_effect == "warding":
            status_effects.apply_effect(character, "warding", 3, 0.20, character.id, data={"value": 0.20})
            bonus_notes.append("Ancient geometry hardens around you.")
        else:
            build_domain_resource(character, 10)
            bonus_notes.append("Ancient resonance floods your reserves.")

    if hit_targets and params.get("world_effect"):
        world_targets = _collect_enemy_targets(character, target=target, include_all=True)
        if world_targets:
            _apply_effects_to_targets(character, world_targets, "slow", 2, 1.0, data={"action_budget_penalty": 1})
            _apply_effects_to_targets(character, world_targets, "weaken", 2, 0.15)
            bonus_notes.append("The local pattern destabilizes and drags every foe off balance.")

    hit_count = len(hits)
    if hit_count == 1:
        enemy, dmg = hits[0]
        if params.get("is_multi_hit"):
            msg = (
                f"{character.key} uses {ability['name']} on {enemy.key}, landing "
                f"{hit_cycles} linked strikes for |r{dmg}|n total damage."
            )
        else:
            msg = f"{character.key} uses {ability['name']} on {enemy.key} for |r{dmg}|n damage."
    elif hit_count == 0:
        msg = f"{character.key} unleashes {ability['name']}."
    else:
        msg = (
            f"{character.key} uses {ability['name']} and hits {hit_count} foes "
            f"for |r{total_damage}|n total damage."
        )
    if total_healing:
        msg += f" {len(ally_targets)} allies recover |g{total_healing}|n HP."
    if debuffs_applied:
        msg += f" {debuffs_applied} enemies are left reeling."
    if buffs_applied:
        msg += f" Follow-up battlefield effects spread across the group."
    if summon_applied:
        msg += " A lingering construct keeps fighting after the first strike."
    if bonus_notes:
        msg += " " + " ".join(bonus_notes)
    return bool(hits) or total_healing > 0 or buffs_applied > 0 or summon_applied > 0, msg


def _handle_dot(character, ability, target):
    """Apply a damage-over-time status effect to the target."""
    params = ability.get("effect_params", {})
    effect_type = params.get("dot_type") or params.get("status_effect") or ability.get("status_effect", "poison")
    chance = ability.get("application_chance", 1.0)
    duration = params.get("duration") or ability.get("effect_duration", 3)
    magnitude = params.get("magnitude") or ability.get("effect_magnitude", ability.get("damage_base", 8))
    targets = _collect_enemy_targets(
        character,
        target=target,
        include_all=params.get("aoe") or params.get("area") or _description_mentions_enemy_aoe(ability),
    )
    if not targets:
        return False, f"{ability['name']} has no valid target."
    applied = 0
    for enemy in targets:
        if random.random() > chance:
            continue
        results = _apply_effects_to_targets(
            character,
            [enemy],
            effect_type,
            duration,
            magnitude,
            data=_build_effect_data(
                params,
                effect_type=effect_type,
                extra={
                    "ability_name": ability["name"],
                    "scaling_primary": ability.get("scaling_primary"),
                    "scaling_secondary": ability.get("scaling_secondary"),
                    "element": ability.get("element", "physical"),
                },
            ),
        )
        if any(ok for _, ok, _ in results):
            applied += 1
            if params.get("secondary_effects"):
                for secondary_effect in params["secondary_effects"]:
                    _apply_effects_to_targets(
                        character,
                        [enemy],
                        secondary_effect,
                        params.get("secondary_duration", duration),
                        params.get("secondary_magnitude", magnitude),
                        data=_build_effect_data(params, effect_type=secondary_effect),
                    )
            if params.get("debuff_type"):
                _apply_effects_to_targets(
                    character,
                    [enemy],
                    params["debuff_type"],
                    params.get("debuff_duration", duration),
                    params.get("debuff_magnitude", magnitude),
                    data=_build_effect_data(params, effect_type=params["debuff_type"]),
                )
    if applied == 1:
        return True, f"{character.key} applies {ability['name']} to {targets[0].key}."
    return (applied > 0), f"{character.key} spreads {ability['name']} across {applied} foes."


def _handle_buff(character, ability, target):
    """Apply a self-buff or group-support buff."""
    params = ability.get("effect_params", {})
    effect_type = params.get("buff_type") or ability.get("buff_type", "haste")
    duration = params.get("duration") or ability.get("effect_duration", 3)
    targets = (
        _collect_ally_targets(character)
        if params.get("group_buff") or _description_mentions_group_allies(ability)
        else [character]
    )
    party_scale = 1.0
    if params.get("party_size_scaling"):
        party_scale = min(1.30, 1.0 + (0.05 * max(0, len(targets) - 1)))
    scaled_params = dict(params)
    for numeric_key in ("value", "magnitude"):
        if isinstance(scaled_params.get(numeric_key), (int, float)):
            scaled_params[numeric_key] = scaled_params[numeric_key] * party_scale
    magnitude = scaled_params.get("magnitude") or ability.get("effect_magnitude", 1.0)
    results = _apply_effects_to_targets(
        character,
        targets,
        effect_type,
        duration,
        magnitude,
        data=_build_effect_data(
            scaled_params,
            effect_type=effect_type,
            extra={
                "ability_name": ability["name"],
                "scaling_primary": ability.get("scaling_primary"),
                "scaling_secondary": ability.get("scaling_secondary"),
                "element": ability.get("element", "physical"),
                "periodic_target_id": getattr(target, "id", None) if target else None,
            },
        ),
    )
    applied = sum(1 for _, ok, _ in results if ok)
    if params.get("resource_refund") and params.get("refund_percent"):
        _apply_effects_to_targets(
            character,
            targets,
            "resource_efficiency",
            duration,
            params["refund_percent"],
            data={"value": params["refund_percent"]},
        )
    _apply_secondary_buffs(character, targets, params)
    if applied == 1 and len(targets) == 1:
        return True, f"{character.key} activates {ability['name']}."
    return (applied > 0), f"{character.key} activates {ability['name']} for {applied} allies."


def _handle_debuff(character, ability, target):
    """Apply a debuff to the target."""
    params = ability.get("effect_params", {})
    effect_type = params.get("debuff_type") or ability.get("debuff_type", "weaken")
    chance = ability.get("application_chance", 1.0)
    duration = params.get("duration") or ability.get("effect_duration", 3)
    magnitude = params.get("magnitude") or ability.get("effect_magnitude", 1.0)
    targets = _collect_enemy_targets(
        character,
        target=target,
        include_all=params.get("aoe") or params.get("area") or _description_mentions_enemy_aoe(ability),
    )
    if not targets:
        return False, f"{ability['name']} has no valid target."
    applied = 0
    successful_targets = []
    for enemy in targets:
        if random.random() > chance:
            continue
        results = _apply_effects_to_targets(
            character,
            [enemy],
            effect_type,
            duration,
            magnitude,
            data=_build_effect_data(params, effect_type=effect_type),
        )
        if any(ok for _, ok, _ in results):
            applied += 1
            successful_targets.append(enemy)
    if params.get("secondary_debuff"):
        _apply_effects_to_targets(
            character,
            successful_targets,
            params["secondary_debuff"],
            params.get("secondary_duration", duration),
            params.get("secondary_magnitude", magnitude),
            data=_build_effect_data(params, effect_type=params["secondary_debuff"]),
        )
    if applied == 1:
        return True, f"{character.key} casts {ability['name']} on {successful_targets[0].key}."
    return (applied > 0), f"{character.key} casts {ability['name']} across {applied} enemies."


def _handle_utility(character, ability, target):
    """Context-dependent utility effect."""
    params = ability.get("effect_params", {})
    utility_action = params.get("utility_action") or ability.get("utility_action")
    if params.get("mana_restored"):
        restored = build_domain_resource(character, params["mana_restored"])
        return True, f"{character.key} uses {ability['name']} and restores mana."
    if utility_action == "flee_boost":
        from world import status_effects
        status_effects.apply_effect(
            character, "haste", 2, 1.0, character.id
        )
        return True, f"{character.key} uses {ability['name']} to gain a burst of speed."
    elif utility_action == "reveal":
        # Reveal a mob's affix (if target is a mob)
        if target and hasattr(target, "reveal_affix"):
            affixes = target.db.affix_list or []
            for affix_tag in affixes:
                reveal_msg = target.reveal_affix(character, affix_tag)
                if reveal_msg:
                    return True, f"{character.key} uses {ability['name']}. {reveal_msg}"
        return True, f"{character.key} uses {ability['name']} to scan the area."
    return True, f"{character.key} uses {ability['name']}."


def _handle_social(character, ability, target):
    """Apply charm or social influence to the target."""
    from world import status_effects
    params = ability.get("effect_params", {})
    ok = True
    if target and target.db.base_stats is None:
        # Mob target: apply charm effect
        duration = params.get("duration") or ability.get("effect_duration", 2)
        magnitude = params.get("magnitude") or ability.get("effect_magnitude", 1.0)
        ok, msg = status_effects.apply_effect(
            target, "charm",
            duration,
            magnitude,
            character.id,
        )
    else:
        msg = "Social influence applied."
    from world.base_attributes import record_stat_use
    record_stat_use(character, "social_ability")
    return ok, f"{character.key} invokes {ability['name']}. {msg}"


def _handle_tactical(character, ability, target):
    """Apply tactical buff to group members or self."""
    from world.base_attributes import record_stat_use
    params = ability.get("effect_params", {})
    tactical_action = params.get("tactical_action") or ability.get("tactical_action", "self_buff")
    buff_type = params.get("buff_type") or ability.get("buff_type", "haste")
    duration = params.get("duration") or ability.get("effect_duration", 3)
    magnitude = params.get("magnitude") or ability.get("effect_magnitude", 1.0)
    ally_targets = _collect_ally_targets(character)

    if tactical_action in ("group_buff", "sacrifice_actions"):
        buff_params = dict(params)
        if tactical_action == "sacrifice_actions":
            buff_params["action_budget_bonus"] = params.get("bonus_actions", 1)
            character.ndb.actions_remaining = 0
        results = _apply_effects_to_targets(
            character,
            ally_targets,
            buff_type,
            duration,
            magnitude,
            data=_build_effect_data(buff_params, effect_type=buff_type),
        )
        applied = sum(1 for _, ok, _ in results if ok)
        _apply_secondary_buffs(character, ally_targets, params)
        record_stat_use(character, "social_ability")
        return True, (
            f"{character.key} directs {ability['name']} across {applied} allies."
        )

    if tactical_action == "mark_target" and target:
        results = _apply_effects_to_targets(
            character,
            [target],
            "weaken",
            params.get("duration", 2),
            params.get("magnitude", 0.15),
            data=_build_effect_data(params, effect_type="weaken"),
        )
        applied = sum(1 for _, ok, _ in results if ok)
        coordinated_results = _apply_effects_to_targets(
            character,
            ally_targets,
            "coordinated_strike",
            1,
            params.get("ally_next_attack_bonus", 0.20),
            data={
                "target_id": target.id,
                "damage_bonus": params.get("ally_next_attack_bonus", 0.20),
            },
        )
        coordinated = sum(1 for _, ok, _ in coordinated_results if ok)
        for ally, ok, _ in coordinated_results:
            if ok and ally is not character:
                ally.msg(
                    f"|c{ability['name']}: your next strike against "
                    f"{target.key} deals bonus damage.|n"
                )
        record_stat_use(character, "social_ability")
        return (applied > 0), (
            f"{character.key} marks {target.key} with {ability['name']} "
            f"for {coordinated} allies' next strikes."
        )

    if tactical_action == "group_disengage":
        data = {"action_budget_bonus": 1}
        _apply_effects_to_targets(character, ally_targets, "haste", 1, 1.0, data=data)
        record_stat_use(character, "social_ability")
        return True, f"{character.key} signals an orderly withdrawal with {ability['name']}."

    _apply_effects_to_targets(
        character,
        [character],
        buff_type,
        duration,
        magnitude,
        data=_build_effect_data(params, effect_type=buff_type),
    )
    record_stat_use(character, "social_ability")
    return True, f"{character.key} deploys {ability['name']}."


def _handle_compound_trigger(character, ability, target):
    """Check and trigger compound effects on the target."""
    from world.status_effects import check_compound_triggers
    compounds = check_compound_triggers(target)
    ability_name = ability["name"]
    if compounds:
        triggered = ", ".join(compounds)
        return True, (
            f"{character.key} triggers {ability_name}! "
            f"Compound effects: {triggered}!"
        )
    return True, f"{character.key} triggers {ability_name}, but no compounds activate."



def _handle_heal(character, ability, target):
    """Resolve healing for one target or the caster's current group."""
    from world.combat_engine import resolve_heal
    from world import status_effects

    params = ability.get("effect_params", {})
    if params.get("group_heal") or params.get("heal_allies") or _description_mentions_group_allies(ability):
        heal_targets = _collect_ally_targets(character)
    else:
        heal_targets = [target or character]

    total_healed = 0
    companion_restored = False
    for heal_target in heal_targets:
        _, _, healed = resolve_heal(character, ability, heal_target)
        total_healed += healed
        if params.get("heal_over_time"):
            hot_duration = params.get("hot_duration", 3)
            hot_total = params.get("heal_amount") or params.get("heal_base") or 30
            hot_per_round = max(1, int(hot_total / max(1, hot_duration)))
            status_effects.apply_effect(
                heal_target,
                "regeneration",
                hot_duration,
                1.0,
                character.id,
                data={"heal_per_round": hot_per_round},
            )
        if params.get("buff_type"):
            effect_data = _build_effect_data(params, effect_type=params["buff_type"])
            if effect_data:
                status_effects.apply_effect(
                    heal_target,
                    params["buff_type"],
                    params.get("duration") or ability.get("effect_duration", 3),
                    params.get("magnitude") or ability.get("effect_magnitude", 1.0),
                    character.id,
                    data=effect_data,
                )
            else:
                status_effects.apply_effect(
                    heal_target,
                    params["buff_type"],
                    params.get("duration") or ability.get("effect_duration", 3),
                    params.get("magnitude") or ability.get("effect_magnitude", 1.0),
                    character.id,
                )
        if params.get("cleanse_negative"):
            status_effects.cleanse_one_negative_effect(heal_target)
    if params.get("companion_restore"):
        companion_restored = _restore_companion_state(character)

    if len(heal_targets) == 1:
        msg = f"{character.key} heals {heal_targets[0].key} with {ability['name']}."
    else:
        msg = (
        f"{character.key} channels {ability['name']} through {len(heal_targets)} allies "
        f"for |g{total_healed}|n total healing."
        )
    if companion_restored:
        msg += " Their construct is restored to fighting condition."
    return True, msg


def _handle_status(character, ability, target):
    """Apply a status effect with application chance roll."""
    params = ability.get("effect_params", {})
    effect_type = params.get("status_effect") or ability.get("status_effect", "slow")
    chance = ability.get("application_chance", 1.0)
    duration = params.get("duration") or ability.get("effect_duration", 3)
    magnitude = params.get("magnitude") or ability.get("effect_magnitude", 1.0)
    if params.get("applies_to_next_attack"):
        effect_type = "venom_coat"
        targets = [character]
    else:
        targets = _collect_enemy_targets(
            character,
            target=target,
            include_all=params.get("aoe") or params.get("area") or _description_mentions_enemy_aoe(ability),
        )
    if not targets:
        return False, f"{ability['name']} has no valid target."

    applied = 0
    for enemy in targets:
        if random.random() > chance:
            continue
        results = _apply_effects_to_targets(
            character,
            [enemy],
            effect_type,
            duration,
            magnitude,
            data=_build_effect_data(
                params,
                effect_type=effect_type,
                extra={
                    "ability_name": ability["name"],
                    "status_effect": params.get("status_effect"),
                    "duration": duration,
                    "magnitude": magnitude,
                },
            ),
        )
        applied += sum(1 for _, ok, _ in results if ok)

    if applied == 0:
        return False, f"{character.key} uses {ability['name']}, but the effect is resisted!"
    if applied == 1:
        return True, f"{character.key} uses {ability['name']} successfully."
    return True, f"{character.key} spreads {ability['name']} across {applied} targets."


EFFECT_HANDLERS = {
    "damage": _handle_damage,
    "dot": _handle_dot,
    "buff": _handle_buff,
    "debuff": _handle_debuff,
    "utility": _handle_utility,
    "social": _handle_social,
    "tactical": _handle_tactical,
    "heal": _handle_heal,
    "status": _handle_status,
}


# ---------------------------------------------------------------------------
# Resource handlers -- type-aware spend/build per domain (D-03 through D-13)
# ---------------------------------------------------------------------------

def _handle_momentum_spend(character, ability):
    """Momentum: traditional pool spend. Build happens elsewhere."""
    cost = ability.get("resource_cost", 0)
    if cost <= 0:
        return True, ""
    return spend_domain_resource(character, cost)


def _handle_focus_spend(character, ability):
    """Focus combo points: builders free, spenders cost 1-5, consumes_all needs >= 1."""
    params = ability.get("effect_params", {})
    if params.get("is_builder"):
        return True, ""  # Builders cost nothing; Focus added after hit
    cost = ability.get("resource_cost", 0)
    if cost <= 0:
        return True, ""
    if params.get("consumes_all_focus"):
        res = character.ndb.domain_resource
        if not res or res["current"] < 1:
            return False, "No Focus points to spend."
        return True, ""  # Consumed in post-ability hook
    res = character.ndb.domain_resource
    if not res or res["current"] < cost:
        current = res["current"] if res else 0
        return False, f"Insufficient Focus ({current}/{cost} needed)."
    res = dict(res)
    res["current"] -= cost
    character.ndb.domain_resource = res
    return True, ""


def _handle_balance_spend(character, ability):
    """Balance pendulum: shift position, never spend. resource_cost always 0."""
    params = ability.get("effect_params", {})
    shift = params.get("balance_shift", 0)
    if shift == 0:
        return True, ""
    res = character.ndb.domain_resource
    if not res:
        return True, ""
    res = dict(res)
    res["current"] = max(0, min(100, res["current"] + shift))
    character.ndb.domain_resource = res
    return True, ""


def _handle_resonance_spend(character, ability):
    """Resonance: builders free (generate after), spenders cost from pool."""
    params = ability.get("effect_params", {})
    if params.get("resonance_generated"):
        return True, ""  # Builder; resonance added in post-ability hook
    cost = ability.get("resource_cost", 0)
    if cost <= 0:
        return True, ""
    return spend_domain_resource(character, cost)


def _handle_mana_spend(character, ability):
    """Mana: traditional pool spend. Persists across encounters."""
    cost = ability.get("resource_cost", 0)
    if cost <= 0:
        return True, ""
    return spend_domain_resource(character, cost)


def _handle_influence_spend(character, ability):
    """Influence: encounter-scoped pool, no regen. Standard spend."""
    cost = ability.get("resource_cost", 0)
    if cost <= 0:
        return True, ""
    return spend_domain_resource(character, cost)


def _handle_reagents_spend(character, ability):
    """Reagents: finite stock, standard spend. Reads reagent_type variant."""
    cost = ability.get("resource_cost", 0)
    if cost <= 0:
        return True, ""
    reagent_type = ability.get("effect_params", {}).get("reagent_type", "generic")
    return spend_domain_resource(character, cost)


def _handle_command_spend(character, ability):
    """Command: pool spend. Builds from ally actions."""
    cost = ability.get("resource_cost", 0)
    if cost <= 0:
        return True, ""
    return spend_domain_resource(character, cost)


def _handle_components_spend(character, ability):
    """Components: finite stock like reagents. Reads component_type variant."""
    cost = ability.get("resource_cost", 0)
    if cost <= 0:
        return True, ""
    component_type = ability.get("effect_params", {}).get("component_type", "generic")
    return spend_domain_resource(character, cost)


def _handle_echoes_spend(character, ability):
    """Echoes: pool spend. Builds from abilities and investigation bonus."""
    cost = ability.get("resource_cost", 0)
    if cost <= 0:
        return True, ""
    return spend_domain_resource(character, cost)


RESOURCE_HANDLERS = {
    "momentum": _handle_momentum_spend,
    "focus": _handle_focus_spend,
    "balance": _handle_balance_spend,
    "resonance": _handle_resonance_spend,
    "mana": _handle_mana_spend,
    "influence": _handle_influence_spend,
    "reagents": _handle_reagents_spend,
    "command": _handle_command_spend,
    "components": _handle_components_spend,
    "echoes": _handle_echoes_spend,
}


# ---------------------------------------------------------------------------
# Post-ability resource hooks
# ---------------------------------------------------------------------------

def _post_ability_resource_hook(character, ability, result):
    """Apply post-ability resource effects (builders, consumers)."""
    res = character.ndb.domain_resource
    if not res:
        return
    rtype = res["type"]
    params = ability.get("effect_params", {})

    if rtype == "focus":
        if params.get("is_builder") and result:
            # Focus builder: add 1 combo point on successful ability (cap at max 5)
            res = dict(res)
            res["current"] = min(res["max"], res["current"] + 1)
            character.ndb.domain_resource = res
        elif params.get("consumes_all_focus"):
            # Consume all Focus points (damage already scaled by caller)
            res = dict(res)
            res["current"] = 0
            character.ndb.domain_resource = res
    elif rtype == "resonance" and params.get("resonance_generated"):
        # Resonance builder: add generated amount
        amount = params["resonance_generated"]
        res = dict(res)
        res["current"] = min(res["max"], res["current"] + amount)
        character.ndb.domain_resource = res
    elif rtype == "momentum" and result:
        # Momentum: build 10 on successful ability use
        res = dict(res)
        res["current"] = min(res["max"], res["current"] + 10)
        character.ndb.domain_resource = res
    elif rtype == "echoes" and result:
        # Echoes: build 5 on each ability use
        res = dict(res)
        gain = 5 + int(params.get("echoes_generated", 0))
        res["current"] = min(res["max"], res["current"] + gain)
        character.ndb.domain_resource = res
    elif rtype == "command" and result:
        # Command: build 5 on successful ability (solo rate)
        res = dict(res)
        res["current"] = min(res["max"], res["current"] + 5)
        character.ndb.domain_resource = res


# ---------------------------------------------------------------------------
# Focus miss handler (exported)
# ---------------------------------------------------------------------------

def handle_focus_miss(character):
    """Reset Focus to 0 on miss. Called from combat_engine on ability miss."""
    res = character.ndb.domain_resource
    if res and res["type"] == "focus":
        res = dict(res)
        res["current"] = 0
        character.ndb.domain_resource = res


# ---------------------------------------------------------------------------
# Balance scaling helper (exported)
# ---------------------------------------------------------------------------

def get_balance_modifier(character, balance_type):
    """Return damage/heal modifier based on Balance pendulum position.
    position 0 (Feral) = 1.5x damage, position 100 (Calm) = 1.5x heal,
    position 50 = 1.0x both. Linear interpolation."""
    res = character.ndb.domain_resource
    if not res or res["type"] != "balance":
        return 1.0
    position = res["current"]
    if balance_type == "feral":
        return 1.0 + (50 - position) * 0.01
    elif balance_type == "calm":
        return 1.0 + (position - 50) * 0.01
    return 1.0


# ---------------------------------------------------------------------------
# Decay and lifecycle functions (exported)
# ---------------------------------------------------------------------------

def decay_resonance(combatant):
    """Decay Resonance by 10 per round. Called from combat_script.end_round."""
    res = combatant.ndb.domain_resource
    if res and res["type"] == "resonance":
        res = dict(res)
        res["current"] = max(0, res["current"] - 10)
        combatant.ndb.domain_resource = res


def on_round_end_resources(combatant, combat_handler):
    """Per-round resource hooks. Called from combat_script.end_round for each combatant."""
    from world.status_effects import get_effect_modifiers

    res = combatant.ndb.domain_resource
    if not res:
        return
    command_preview = None
    rtype = res["type"]
    if rtype == "resonance":
        decay_resonance(combatant)
    elif rtype == "focus":
        # Reset Focus if subterfuge character skipped their turn this round
        if not getattr(combatant.ndb, "ability_used_this_turn", False):
            res = dict(res)
            res["current"] = 0
            combatant.ndb.domain_resource = res
    elif rtype == "command":
        # Build Command from ally actions (group combat)
        command_preview = _build_command_from_allies(combatant, combat_handler)
    regen = get_effect_modifiers(combatant).get("resource_regen_per_round", 0)
    if regen > 0:
        build_domain_resource(combatant, regen)
    return command_preview


def get_command_round_preview(combatant, combat_handler):
    """Return the current round's Command gain, capped by the resource maximum."""
    res = combatant.ndb.domain_resource
    if not res or res["type"] != "command":
        return None

    ally_action_count = getattr(combat_handler.ndb, "ally_action_count", None) or {}
    ally_actions = ally_action_count.get(str(combatant.id), 0)
    uncapped_gain = ally_actions * 10 if ally_actions > 0 else 5
    current = res["current"]
    maximum = res["max"]
    return {
        "current": current,
        "max": maximum,
        "ally_actions": ally_actions,
        "gain": min(maximum - current, uncapped_gain),
        "source": "allies" if ally_actions > 0 else "solo",
    }


def _build_command_from_allies(combatant, combat_handler):
    """Build Command resource based on ally actions this round."""
    preview = get_command_round_preview(combatant, combat_handler)
    if not preview:
        return None

    res = dict(combatant.ndb.domain_resource)
    res["current"] += preview["gain"]
    combatant.ndb.domain_resource = res
    return preview


def on_encounter_end_resources(combatant):
    """Encounter-end resource lifecycle. Called from combat_script.end_combat."""
    res = combatant.ndb.domain_resource
    if not res:
        return
    rtype = res["type"]
    if rtype == "mana":
        # Mana recovers 15% at encounter end, persists
        res = dict(res)
        recovery = int(res["max"] * 0.15)
        res["current"] = min(res["max"], res["current"] + recovery)
        combatant.ndb.domain_resource = res
    elif rtype in ("focus", "influence", "command"):
        # Reset encounter-scoped resources
        res = dict(res)
        res["current"] = 0
        combatant.ndb.domain_resource = res
    elif rtype == "momentum":
        # Momentum decays between encounters
        res = dict(res)
        res["current"] = 0
        combatant.ndb.domain_resource = res
    elif rtype == "echoes":
        # Decrement investigation bonus persistence
        bonus = combatant.db.echoes_investigation_bonus
        if bonus and bonus.get("encounters_remaining", 0) > 0:
            bonus = dict(bonus)
            bonus["encounters_remaining"] -= 1
            if bonus["encounters_remaining"] <= 0:
                bonus["amount"] = 0
            combatant.db.echoes_investigation_bonus = bonus
    # resonance: no decay between encounters (persists)
    # reagents/components: persist as-is (finite stock, no regen)


def build_momentum_on_damage(character, amount=10):
    """Build Momentum when character lands a hit or takes damage.
    Called from combat_engine. Only applies if resource type is momentum."""
    res = character.ndb.domain_resource
    if res and res["type"] == "momentum":
        res = dict(res)
        res["current"] = min(res["max"], res["current"] + amount)
        character.ndb.domain_resource = res


# ---------------------------------------------------------------------------
# Resource management (D-13)
# ---------------------------------------------------------------------------

def get_domain_resource(character):
    """Return current domain resource dict or None if no guild."""
    return character.ndb.domain_resource


def build_domain_resource(character, amount):
    """Add resource (capped at max). Returns new current value."""
    res = character.ndb.domain_resource
    if not res:
        return 0
    res = dict(res)
    res["current"] = min(res["max"], res["current"] + amount)
    character.ndb.domain_resource = res
    return res["current"]


def spend_domain_resource(character, amount):
    """Spend resource. Returns (bool, str). Fails if insufficient."""
    res = character.ndb.domain_resource
    if not res:
        return False, "No domain resource available."
    if res["current"] < amount:
        return False, (
            f"Insufficient {res['type']} "
            f"({res['current']}/{amount} needed)."
        )
    res = dict(res)
    res["current"] = res["current"] - amount
    character.ndb.domain_resource = res
    return True, ""


def initialize_domain_resource(character):
    """
    Set up domain resource from guild fingerprint.
    Called at encounter start or session start for guild members.
    Type-aware: each domain starts with different pool values.
    """
    guild_id = character.db.guild_id
    if not guild_id:
        character.ndb.domain_resource = None
        return
    from world.guild_engine import GUILDS, FINGERPRINTS
    guild = GUILDS.get(guild_id, {})
    domain = guild.get("primary_domain")
    fp = FINGERPRINTS.get(domain, {})
    resource_type = fp.get("resource_type", fp.get("resource", domain))

    # Type-aware initialization
    if resource_type == "focus":
        current, pool_max = 0, 5
    elif resource_type == "balance":
        current, pool_max = 50, 100
    elif resource_type == "mana":
        pool_max = fp.get("resource_max", 100)
        current = pool_max  # Mana starts full, persists across encounters
    elif resource_type == "influence":
        from world.world_state import get_dimension_score
        pool_max = int(20 + get_dimension_score(character, "reputation") * 0.5)
        pool_max = max(20, pool_max)
        current = pool_max  # Full pool each encounter
    elif resource_type == "reagents":
        current = character.db.reagent_stock or 50
        pool_max = 100
    elif resource_type == "components":
        current = character.db.component_stock or 50
        pool_max = 100
    elif resource_type == "echoes":
        bonus = getattr(character.db, "echoes_investigation_bonus", None)
        investigation_bonus = bonus.get("amount", 0) if isinstance(bonus, dict) else 0
        current = investigation_bonus
        pool_max = 100
    elif resource_type == "momentum":
        current, pool_max = 0, 100
    elif resource_type == "resonance":
        current, pool_max = 0, 100
    elif resource_type == "command":
        current, pool_max = 0, 100
    else:
        # Generic fallback
        pool_max = fp.get("resource_max", 100)
        current = 0

    character.ndb.domain_resource = {
        "type": resource_type,
        "current": current,
        "max": pool_max,
    }


# ---------------------------------------------------------------------------
# Cooldown management (D-12)
# ---------------------------------------------------------------------------

def decrement_cooldowns(character):
    """Decrement all ability cooldowns by 1 round. Called each combat round."""
    cooldowns = dict(character.ndb.ability_cooldowns or {})
    expired = []
    for ability_id, remaining in cooldowns.items():
        cooldowns[ability_id] = remaining - 1
        if cooldowns[ability_id] <= 0:
            expired.append(ability_id)
    for ability_id in expired:
        del cooldowns[ability_id]
    character.ndb.ability_cooldowns = cooldowns


def clear_encounter_cooldowns(character):
    """Clear all cooldowns and reset ancestry ability. Called at encounter end."""
    character.ndb.ability_cooldowns = {}
    character.ndb.ancestry_ability_used = False


# ---------------------------------------------------------------------------
# Unlock synchronization
# ---------------------------------------------------------------------------

def get_expected_unlocked_ability_ids(character):
    """
    Return the ordered list of abilities the character should know.

    Grants are additive:
    - ancestry starting ability, if any
    - all primary-domain abilities up to the current guild tier
    - subclass signature abilities whose authored tier has been reached
    """
    from world.ability_registry import ABILITIES, DOMAIN_ABILITIES, SUBCLASS_SIGNATURES
    from world.ancestry_engine import ANCESTRY_TRAITS

    ordered = []

    ancestry_id = getattr(character.db, "ancestry", None)
    ancestry_ability = ANCESTRY_TRAITS.get(ancestry_id, {}).get("starting_ability")
    if ancestry_ability in ABILITIES:
        ordered.append(ancestry_ability)

    guild_id = getattr(character.db, "guild_id", None)
    if guild_id:
        from world.guild_engine import GUILDS, get_guild_tier

        primary_domain = GUILDS.get(guild_id, {}).get("primary_domain")
        current_tier = get_guild_tier(character)
        for tier in range(1, current_tier + 1):
            ordered.extend(DOMAIN_ABILITIES.get(primary_domain, {}).get(tier, []))

        subclass_id = getattr(character.db, "subclass_id", None)
        for ability_id in SUBCLASS_SIGNATURES.get(subclass_id, []):
            ability = ABILITIES.get(ability_id)
            if ability and ability.get("tier", 99) <= current_tier:
                ordered.append(ability_id)

    # Preserve authored order while removing duplicates defensively.
    return list(dict.fromkeys(ordered))


def sync_character_ability_unlocks(character):
    """
    Ensure CharacterAbility records exist for all earned abilities.

    This is intentionally additive: missing earned abilities are granted, but
    previously learned abilities are never stripped away here.
    """
    from world.models import CharacterAbility

    granted = []
    for ability_id in get_expected_unlocked_ability_ids(character):
        _, created = CharacterAbility.objects.get_or_create(
            character=character,
            ability_id=ability_id,
        )
        if created:
            granted.append(ability_id)
    return granted


# ---------------------------------------------------------------------------
# Access check
# ---------------------------------------------------------------------------

def _check_ability_access(character, ability_id):
    """Check if character knows and can use this ability. Returns (bool, str)."""
    from world.ability_registry import ABILITIES
    ability = ABILITIES.get(ability_id)
    if not ability:
        return False, "Unknown ability."

    # Mobs use db.abilities list — skip CharacterAbility unlock check
    if character.db.abilities:
        return True, ""

    # Check CharacterAbility model for unlock (ABL-03)
    from world.models import CharacterAbility
    if not CharacterAbility.objects.filter(
        character=character, ability_id=ability_id
    ).exists():
        if ability_id in get_expected_unlocked_ability_ids(character):
            sync_character_ability_unlocks(character)
            return True, ""
        return False, f"You have not unlocked {ability['name']}."

    return True, ""


# ---------------------------------------------------------------------------
# Resource check helper
# ---------------------------------------------------------------------------

def _check_and_spend_resource(character, ability):
    """Check and deduct resource cost. Returns (bool, str).
    Uses type-aware dispatch via RESOURCE_HANDLERS."""
    from world.status_effects import get_effect_modifiers

    effective_ability = ability
    modifiers = get_effect_modifiers(character)
    reduction_pct = modifiers.get("resource_cost_reduction_pct", 0.0)
    if reduction_pct > 0 and ability.get("resource_cost", 0) > 0:
        effective_ability = dict(ability)
        effective_ability["resource_cost"] = max(
            0,
            int(round(ability.get("resource_cost", 0) * (1 - reduction_pct))),
        )

    res = character.ndb.domain_resource
    if not res:
        cost = effective_ability.get("resource_cost", 0)
        if cost <= 0:
            return True, ""
        return False, "No domain resource available."
    handler = RESOURCE_HANDLERS.get(res["type"])
    if handler:
        return handler(character, effective_ability)
    # Fallback to generic spend
    cost = effective_ability.get("resource_cost", 0)
    if cost <= 0:
        return True, ""
    return spend_domain_resource(character, cost)


# ---------------------------------------------------------------------------
# Main dispatch (D-10)
# ---------------------------------------------------------------------------

def use_ability(character, ability_id, target=None):
    """
    Execute an ability. Returns (bool, str).

    Checks: known, cooldown, resource, then dispatches to effect handler.
    Per D-10: effect-type dispatch, no per-ability callables.
    """
    # Dead characters cannot use abilities
    if getattr(character.ndb, "hp", None) is not None and character.ndb.hp <= 0:
        return False, "|rYou cannot use abilities while dead.|n"

    from world.ability_registry import ABILITIES
    ability = ABILITIES.get(ability_id)
    if not ability:
        return False, "Unknown ability."

    if (
        _is_player(character)
        and ability.get("charge_turns", 0) > 0
        and getattr(character.ndb, "combat_handler", None)
        and not getattr(character.ndb, "resolving_charged_ability", False)
    ):
        return (
            False,
            f"{ability['name']} must be charged first. "
            "Use the charge command to begin channeling it.",
        )

    from world.status_effects import get_effect_modifiers

    if get_effect_modifiers(character).get("silenced", False):
        return False, f"{ability['name']} fails because you are silenced."

    # Check character has unlocked this ability
    ok, msg = _check_ability_access(character, ability_id)
    if not ok:
        return False, msg

    # Check cooldown (D-12)
    cooldowns = character.ndb.ability_cooldowns or {}
    remaining = cooldowns.get(ability_id, 0)
    if remaining > 0:
        return False, (
            f"{ability['name']} is on cooldown "
            f"({remaining} rounds remaining)."
        )

    # Check and spend resource (D-13)
    resource_before = None
    if character.ndb.domain_resource:
        resource_before = dict(character.ndb.domain_resource)
    ok, msg = _check_and_spend_resource(character, ability)
    if not ok:
        return False, msg

    # Dispatch to effect handler (D-10)
    handler = EFFECT_HANDLERS.get(ability["effect_type"])
    if not handler:
        if resource_before is not None:
            character.ndb.domain_resource = resource_before
        return False, f"Unhandled effect type: {ability['effect_type']}"

    ok, msg = handler(character, ability, target)

    if not ok:
        if resource_before is not None:
            character.ndb.domain_resource = resource_before
        return False, msg

    # Post-ability resource hooks
    _post_ability_resource_hook(character, ability, ok)

    # Set cooldown (D-12)
    if ability.get("cooldown", 0) > 0:
        cooldowns = dict(character.ndb.ability_cooldowns or {})
        cooldowns[ability_id] = ability["cooldown"]
        character.ndb.ability_cooldowns = cooldowns

    # Write room flag if specified (D-24)
    if ability.get("room_flag_written") and character.location:
        from world.room_state import add_room_flag
        add_room_flag(character.location, ability["room_flag_written"])

    # Increment times_used
    try:
        from django.db.models import F
        from world.models import CharacterAbility as CA
        CA.objects.filter(
            character=character, ability_id=ability_id
        ).update(times_used=F("times_used") + 1)
    except Exception:
        pass  # Non-fatal -- counter is informational

    return ok, msg
