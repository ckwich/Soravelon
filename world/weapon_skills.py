"""Broad weapon-family skill helpers.

Weapon-family skills are general proficiencies. They reward repeated handling
with a modest basic-attack bonus, but loot quality remains controlled by the
loot table's authored relevant_skill contract.
"""

from __future__ import annotations


MAX_WEAPON_SKILL_DAMAGE_BONUS = 0.10


WEAPON_FAMILY_SKILLS = {
    "blade": {
        "name": "Blades",
        "skill_id": "weapon_blades",
        "domain_bonus": "combat",
        "aliases": (
            "blade",
            "blades",
            "sword",
            "swords",
            "shortsword",
            "longsword",
            "greatsword",
            "claymore",
            "dagger",
            "daggers",
            "cutlass",
            "knife",
            "knives",
            "stiletto",
        ),
        "keywords": (
            "blade",
            "sword",
            "shortsword",
            "longsword",
            "greatsword",
            "claymore",
            "dagger",
            "cutlass",
            "knife",
            "stiletto",
        ),
        "description": (
            "Handle edged weapons with clean alignment, fast recovery, and "
            "reliable cuts or thrusts."
        ),
        "thresholds": {
            25: "Simple edge alignment and recovery become instinctive.",
            50: "You read openings well enough to keep a blade moving.",
            75: "Cuts, thrusts, and feints flow without wasted motion.",
            90: "Even unfamiliar blades settle into your hand quickly.",
            100: "Blade work becomes quiet, exact, and frighteningly sure.",
        },
    },
    "axe": {
        "name": "Axes",
        "skill_id": "weapon_axes",
        "domain_bonus": "combat",
        "aliases": ("axe", "axes", "hatchet", "battleaxe", "greataxe"),
        "keywords": ("axe", "hatchet", "battleaxe", "greataxe"),
        "description": (
            "Use axe-family weapons for committed cuts, hooks, shields, and "
            "armor-breaking pressure."
        ),
        "thresholds": {
            25: "You stop over-swinging and recover after heavy cuts.",
            50: "Hooks and haft pressure become part of your rhythm.",
            75: "You can turn an axe's weight into reliable advantage.",
            90: "Armored targets feel less secure under your angles.",
            100: "Every axe swing lands with brutal economy.",
        },
    },
    "hafted": {
        "name": "Hafted Weapons",
        "skill_id": "weapon_hafted",
        "domain_bonus": "combat",
        "aliases": (
            "hafted",
            "mace",
            "maces",
            "hammer",
            "hammers",
            "warhammer",
            "club",
            "clubs",
            "maul",
            "morningstar",
            "flail",
        ),
        "keywords": (
            "mace",
            "hammer",
            "warhammer",
            "club",
            "maul",
            "morningstar",
            "flail",
        ),
        "description": (
            "Handle blunt hafted weapons, turning impact, leverage, and armor "
            "pressure into controlled strikes."
        ),
        "thresholds": {
            25: "You keep the head of the weapon from dragging your guard open.",
            50: "Impact timing improves against armor and shields.",
            75: "You can punish footing mistakes with compact force.",
            90: "Heavy heads become precise instead of merely punishing.",
            100: "Every strike lands like a verdict, not a guess.",
        },
    },
    "polearm": {
        "name": "Polearms",
        "skill_id": "weapon_polearms",
        "domain_bonus": "tactics",
        "aliases": (
            "polearm",
            "polearms",
            "spear",
            "spears",
            "halberd",
            "glaive",
            "pike",
            "lance",
        ),
        "keywords": ("spear", "halberd", "glaive", "pike", "lance", "polearm"),
        "description": (
            "Control distance with long-reach weapons, bracing, driving lines, "
            "and threatening approach paths."
        ),
        "thresholds": {
            25: "You keep point and haft from tangling in close quarters.",
            50: "Reach becomes a tool rather than just a measurement.",
            75: "You can threaten movement before enemies commit.",
            90: "Bracing and redirection become nearly seamless.",
            100: "The space around you belongs to the point of your weapon.",
        },
    },
    "bow": {
        "name": "Bows",
        "skill_id": "weapon_bows",
        "domain_bonus": "tactics",
        "aliases": ("bow", "bows", "shortbow", "longbow", "composite_bow"),
        "keywords": ("bow", "shortbow", "longbow", "composite bow"),
        "description": (
            "Use bow weapons with steadier draw, cleaner release, and better "
            "combat timing."
        ),
        "thresholds": {
            25: "Your draw and release grow more consistent.",
            50: "You loose under pressure without wasting breath.",
            75: "Range judgment and target timing become reliable.",
            90: "Difficult angles feel like problems, not barriers.",
            100: "A drawn bow becomes an answer waiting for the question.",
        },
    },
    "thrown": {
        "name": "Thrown Weapons",
        "skill_id": "weapon_thrown",
        "domain_bonus": "subterfuge",
        "aliases": (
            "thrown",
            "throwing",
            "dart",
            "darts",
            "javelin",
            "javelins",
            "sling",
            "throwing_knife",
        ),
        "keywords": ("throwing", "thrown", "dart", "javelin", "sling"),
        "description": (
            "Use thrown weapons with cleaner timing, better release, and "
            "more reliable short-window opportunities."
        ),
        "thresholds": {
            25: "Short throws stop wobbling out of your hand.",
            50: "You find openings while already in motion.",
            75: "Release timing becomes difficult to read.",
            90: "You can punish tiny windows before they close.",
            100: "If it can be thrown, your hand already knows the line.",
        },
    },
    "staff": {
        "name": "Staves",
        "skill_id": "weapon_staves",
        "domain_bonus": "resonance",
        "aliases": ("staff", "staves", "stave", "quarterstaff", "rod"),
        "keywords": ("staff", "stave", "quarterstaff", "rod"),
        "description": (
            "Handle staff weapons through leverage, spacing, warding motions, "
            "and clean two-ended pressure."
        ),
        "thresholds": {
            25: "You stop crowding your own reach.",
            50: "Two-ended pressure starts to feel natural.",
            75: "You can turn defense into counter-lines without resetting.",
            90: "A staff becomes a moving boundary around you.",
            100: "Every step, turn, and ward lands in one continuous line.",
        },
    },
    "shield": {
        "name": "Shields",
        "skill_id": "weapon_shields",
        "domain_bonus": "combat",
        "aliases": ("shield", "shields", "buckler", "kite_shield"),
        "keywords": ("shield", "buckler", "kite shield"),
        "description": (
            "Use shield weapons and defensive off-hands for timing, cover, "
            "bashes, and protected advances."
        ),
        "thresholds": {
            25: "You catch blows without overcommitting your guard.",
            50: "Shield pressure starts to create attacking windows.",
            75: "You can advance through danger with fewer openings.",
            90: "Bashes, binds, and covers become one language.",
            100: "Your shield feels less like armor and more like terrain.",
        },
    },
    "unarmed": {
        "name": "Unarmed",
        "skill_id": "weapon_unarmed",
        "domain_bonus": "combat",
        "aliases": ("unarmed", "fist", "fists", "knuckle", "brawling"),
        "keywords": ("unarmed", "fist", "knuckle", "brawling"),
        "description": (
            "Fight without a held weapon, using stance, clinch pressure, "
            "strikes, and recovery."
        ),
        "thresholds": {
            25: "You can strike without giving away your balance.",
            50: "Close range stops feeling like panic.",
            75: "Clinch, recovery, and pressure become deliberate tools.",
            90: "You can stay dangerous even when disarmed.",
            100: "Your body is a weapon that cannot be confiscated.",
        },
    },
}


WEAPON_SKILL_IDS = tuple(
    config["skill_id"] for config in WEAPON_FAMILY_SKILLS.values()
)
WEAPON_FAMILY_BY_SKILL = {
    config["skill_id"]: family
    for family, config in WEAPON_FAMILY_SKILLS.items()
}

_ALIAS_TO_FAMILY = {}
for _family, _config in WEAPON_FAMILY_SKILLS.items():
    _ALIAS_TO_FAMILY[_family] = _family
    for _alias in _config.get("aliases", ()):
        _ALIAS_TO_FAMILY[_alias.replace(" ", "_").lower()] = _family

_TEXT_INFERENCE_ORDER = (
    "thrown",
    "bow",
    "polearm",
    "axe",
    "hafted",
    "staff",
    "shield",
    "blade",
    "unarmed",
)


WEAPON_SKILL_DEFINITIONS = {
    config["skill_id"]: {
        "name": config["name"],
        "skill_type": "general",
        "description": config["description"],
        "domain_bonus": config["domain_bonus"],
        "trainer_required_above": 50,
        "thresholds": dict(config["thresholds"]),
    }
    for config in WEAPON_FAMILY_SKILLS.values()
}


def _read_item_value(item, key):
    if item is None:
        return None
    if isinstance(item, dict):
        return item.get(key)

    db = getattr(item, "db", None)
    if db is not None:
        value = getattr(db, key, None)
        if value is not None:
            return value

    value = getattr(item, key, None)
    if value is not None:
        return value
    return None


def _iter_text_values(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for entry in value.values():
            if isinstance(entry, str):
                yield entry
    elif isinstance(value, (list, tuple, set)):
        for entry in value:
            if isinstance(entry, str):
                yield entry


def _wordish(text):
    return text.replace("_", " ").replace("-", " ").lower()


def normalize_weapon_family(value):
    """Return a canonical weapon family key, or None for unknown values."""
    if not isinstance(value, str):
        return None
    normalized = value.strip().replace(" ", "_").replace("-", "_").lower()
    return _ALIAS_TO_FAMILY.get(normalized)


def display_weapon_family(family):
    """Return the player-facing family name for a canonical family key."""
    normalized = normalize_weapon_family(family) or family
    config = WEAPON_FAMILY_SKILLS.get(normalized)
    return config["name"] if config else None


def weapon_skill_for_family(family):
    """Return the skill id for a weapon family key or alias."""
    normalized = normalize_weapon_family(family)
    if not normalized:
        return None
    return WEAPON_FAMILY_SKILLS[normalized]["skill_id"]


def _family_from_tags(item):
    for field_name in ("tags", "source_tags", "lore_tags"):
        for tag in _iter_text_values(_read_item_value(item, field_name)):
            family = normalize_weapon_family(tag)
            if family:
                return family
    return None


def _looks_weapon_like(item):
    item_type = _read_item_value(item, "item_type")
    if isinstance(item_type, str) and item_type != "equipment":
        return False

    equip_slot = (
        _read_item_value(item, "equip_slot")
        or _read_item_value(item, "equipment_slot")
    )
    if equip_slot in {"main_hand", "weapon", "off_hand"}:
        return True
    if _read_item_value(item, "damage_min") or _read_item_value(item, "damage_max"):
        return True
    if item_type == "equipment":
        return True
    return False


def _family_from_archetype(item):
    archetype_id = _read_item_value(item, "equipment_archetype")
    if not isinstance(archetype_id, str):
        return None

    from world.equipment_archetypes import EQUIPMENT_ARCHETYPES

    archetype = EQUIPMENT_ARCHETYPES.get(archetype_id) or {}
    return normalize_weapon_family(archetype.get("weapon_family"))


def _family_from_text(item):
    if not _looks_weapon_like(item):
        return None

    text_parts = []
    for field_name in ("item_id", "key", "name"):
        value = _read_item_value(item, field_name)
        if isinstance(value, str):
            text_parts.append(value)
    text = f" {_wordish(' '.join(text_parts))} "

    for family in _TEXT_INFERENCE_ORDER:
        config = WEAPON_FAMILY_SKILLS[family]
        for keyword in config.get("keywords", ()):
            if f" {_wordish(keyword)} " in text:
                return family
    return None


def infer_weapon_family_from_item(item):
    """Infer a canonical weapon family key from an item object or item_def dict."""
    explicit = normalize_weapon_family(_read_item_value(item, "weapon_family"))
    if explicit:
        return explicit

    return (
        _family_from_archetype(item)
        or _family_from_tags(item)
        or _family_from_text(item)
    )


def weapon_skill_for_item(item):
    """Return the matching weapon-family skill id for an item, if known."""
    return weapon_skill_for_family(infer_weapon_family_from_item(item))


def weapon_skill_for_attack(weapon):
    """Return the skill id trained by a basic attack using this weapon."""
    if weapon is None:
        return WEAPON_FAMILY_SKILLS["unarmed"]["skill_id"]
    return weapon_skill_for_item(weapon)


def weapon_skill_damage_bonus(skill_value):
    """Return the fractional damage bonus for a weapon-family skill value."""
    try:
        value = float(skill_value or 0.0)
    except (TypeError, ValueError):
        value = 0.0
    value = max(0.0, min(100.0, value))
    return min(MAX_WEAPON_SKILL_DAMAGE_BONUS, value * 0.001)


def weapon_skill_damage_bonus_for_attack(attacker, weapon):
    """Return the current handling bonus for an attacker's weapon family."""
    skill_id = weapon_skill_for_attack(weapon)
    if not skill_id:
        return 0.0

    from world.skill_engine import get_skill_value

    skill_value = get_skill_value(attacker, skill_id)
    return weapon_skill_damage_bonus(skill_value)


def accumulate_weapon_skill_for_attack(attacker, weapon):
    """Record one successful use of the attacker's active weapon family."""
    skill_id = weapon_skill_for_attack(weapon)
    if not skill_id:
        return None

    from world.skill_engine import accumulate_skill_use

    accumulate_skill_use(attacker, skill_id)
    return skill_id
