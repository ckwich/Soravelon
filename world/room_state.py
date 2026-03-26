"""
world/room_state.py

Lightweight room state tracker using room.ndb.
Temporary flags represent recent events in a room.
Decays lazily -- no global ticker required.

Flag vocabulary is the design contract between all systems.
Always use flag names from FLAG_VOCABULARY below.
Never invent new flag names in system code -- add them here first.
"""

import time

# One combat round = approximately 3 seconds (tune during combat design)
ROUND_DURATION_SECONDS = 3


# ---------------------------------------------------------------------------
# Flag vocabulary -- the complete list of valid room state flags
# ---------------------------------------------------------------------------
# DO NOT use flag names outside this list in any system code.
# To add a new flag: add it here with description and typical duration,
# then document the writer (which system sets it) and readers (which
# systems respond to it).

FLAG_VOCABULARY = {

    # --- Elemental / energy flags ---

    "charged": {
        "description": "Electrical or arcane energy recently discharged here.",
        "typical_duration": 5,
        "writers": ["lightning abilities", "arcane burst abilities",
                    "node pulse (temporal/cognitive)"],
        "readers": ["Resonance Sense", "Sparkshaper companion",
                    "Arcana chain abilities"],
    },
    "burning": {
        "description": "Active fire or heat present in the room.",
        "typical_duration": 4,
        "writers": ["fire abilities", "Alchemy incendiary compounds",
                    "node pulse (thermal)"],
        "readers": ["Resonance Sense", "Wet status interaction",
                    "Naturalism Balance"],
    },
    "frozen": {
        "description": "Ice or extreme cold recently applied here.",
        "typical_duration": 4,
        "writers": ["ice abilities", "node pulse (temporal)"],
        "readers": ["Resonance Sense", "movement ability modifiers"],
    },
    "toxic_air": {
        "description": "Airborne poison or alchemical compound present.",
        "typical_duration": 3,
        "writers": ["Fumehand companion delivery",
                    "Alchemy gas abilities", "Poison DoT above threshold"],
        "readers": ["all combatants (passive damage)",
                    "Resonance Sense", "Alchemy compound triggers"],
    },
    "resonant": {
        "description": "Old magic is active or recently disturbed here.",
        "typical_duration": 10,
        "writers": ["node pulse", "Resonance ability detonation",
                    "lore fragment investigated", "ancient site visited"],
        "readers": ["Resonance Sense (primary reader)",
                    "Remnance Echoes bonus",
                    "Arcana Mana regen rate"],
    },
    "void_touched": {
        "description": "Something pre-curse has been active here recently.",
        "typical_duration": 8,
        "writers": ["Remnance high-tier abilities",
                    "Vaelborn guild investigation actions",
                    "dragon proximity"],
        "readers": ["Resonance Sense", "Remnance Echoes bonus (amplified)",
                    "Vaelborn-only ability variants"],
    },

    # --- Biological / nature flags ---

    "fading_life": {
        "description": "A creature with strong nature affinity died here recently.",
        "typical_duration": 3,
        "writers": ["Naturalism-affinity mob death",
                    "companion death", "grove/nature NPC death"],
        "readers": ["Resonance Sense", "Naturalism Balance push",
                    "Growsmith companion regen modifier"],
    },
    "blood_soaked": {
        "description": "Significant combat violence occurred here recently.",
        "typical_duration": 4,
        "writers": ["mob death (any)", "player death",
                    "Bleed DoT above threshold"],
        "readers": ["Resonance Sense", "Ironblood Momentum build rate",
                    "Ashfang compound trigger"],
    },
    "living_wood": {
        "description": "Living plant material or organic growth is active here.",
        "typical_duration": 6,
        "writers": ["Growsmith companion presence",
                    "Naturalism high-tier abilities",
                    "node pulse (cognitive/resonance in forest zones)"],
        "readers": ["Resonance Sense", "Growsmith regen rate modifier",
                    "Naturalism Balance push toward Calm"],
    },

    # --- Tactical / combat flags ---

    "fortified": {
        "description": "Defensive position established here by a Tactics ability.",
        "typical_duration": 5,
        "writers": ["Tactics territorial abilities",
                    "Vanguard guard mechanics",
                    "Siegewright companion defensive setup"],
        "readers": ["all allies (defense bonus)",
                    "Resonance Sense (minor)"],
    },
    "scouted": {
        "description": "This room has been cased -- weak points identified.",
        "typical_duration": 10,
        "writers": ["Subterfuge scouting abilities",
                    "Gearhand companion reconnaissance"],
        "readers": ["Subterfuge player initiative bonus",
                    "Resonance Sense (minor)"],
    },
    "disrupted": {
        "description": "Magical interference or anti-magic field present.",
        "typical_duration": 4,
        "writers": ["Spellbreaker anti-magic abilities",
                    "certain node failure states"],
        "readers": ["Arcana ability cost increase",
                    "Resonance Sense", "Resonance resource decay rate"],
    },

    # --- Environmental / world flags ---

    "power_vacuum": {
        "description": "A significant entity died here. Faction presence weakened.",
        "typical_duration": 30,
        "writers": ["named mob death", "boss mob death",
                    "LLM quest consequence"],
        "readers": ["faction Standing gain rate (amplified)",
                    "Resonance Sense", "Diplomacy Influence build rate"],
    },
    "unsettled": {
        "description": "Something disturbed the normal order here recently.",
        "typical_duration": 8,
        "writers": ["trigger system (area builder authored)",
                    "quest consequence", "node destabilization event"],
        "readers": ["NPC reaction modifier", "Resonance Sense",
                    "investigation success rate modifier"],
    },
    "ancient_presence": {
        "description": "Pre-curse construction or entity recently activated here.",
        "typical_duration": 15,
        "writers": ["Runewright base-8 interaction",
                    "Bucketborn companion action",
                    "Dragonwright construction",
                    "ancient site trigger"],
        "readers": ["Resonance Sense (strong signal)",
                    "Remnance Echoes bonus",
                    "Vaelborn-only ability variants",
                    "Engineering companion charge efficiency"],
    },
    "still": {
        "description": "Unusual quiet -- no recent combat, magic, or movement.",
        "typical_duration": 20,
        "writers": ["passive accumulation when no other flags present "
                    "for N rounds -- set by room_state module automatically"],
        "readers": ["Resonance Sense (baseline reading)",
                    "Subterfuge stealth bonus",
                    "Naturalism Calm push"],
    },

    # --- Subterfuge-written flags ---

    "shadow_marked": {
        "description": "Shadows here feel deliberately deepened.",
        "typical_duration": 4,
        "writers": ["Subterfuge vanish abilities",
                    "Veilcraft area abilities",
                    "Gearhand companion stealth mode"],
        "readers": ["Subterfuge Focus window extension (+1 round)",
                    "Tactics ambush bonus on first round",
                    "Resonance Sense"],
    },

    # --- Death-specific flags ---

    "predator_kill": {
        "description": "An aggressive predator fell here. The zone feels quieter.",
        "typical_duration": 6,
        "writers": ["aggressive/territorial mob death"],
        "readers": ["Diplomacy Influence build bonus",
                    "Tactics Command bonus",
                    "Resonance Sense"],
    },
    "corrupted_death": {
        "description": "The death here left something wrong behind.",
        "typical_duration": 8,
        "writers": ["node_touched affix mob death",
                    "Resonance-afflicted mob death"],
        "readers": ["Resonance free Resonance stack on next ability",
                    "Remnance +5 starting Echoes bonus",
                    "Resonance Sense (strong signal)"],
    },

    # --- Node state flags ---

    "node_critical": {
        "description": "The air feels wrong. Like the world is holding its breath.",
        "typical_duration": -1,  # -1 = persists until NodeScript state changes
        "writers": ["NodeScript critical state (failure 75+)"],
        "readers": ["Resonance Overcharge threshold lower",
                    "Arcana Mana costs reduced (panic efficiency)",
                    "all combatants -- minor arcane damage per round (passive)",
                    "Resonance Sense (urgent -- highest priority after void_touched)"],
    },
    "node_calming": {
        "description": "Something that was agitated is quieting.",
        "typical_duration": 6,
        "writers": ["NodeScript stabilization in progress"],
        "readers": ["Naturalism Balance snap-to-neutral bonus",
                    "Resonance resource build rate +50%",
                    "Resonance Sense"],
    },
}


# ---------------------------------------------------------------------------
# Core functions
# ---------------------------------------------------------------------------

def get_room_flags(room):
    """
    Return dict of currently active flags for this room.
    Applies lazy decay -- expired flags removed on read.
    Returns {} if no active flags.
    """
    state = room.ndb.room_state
    if not state:
        return {}

    now = time.time()
    last = state.get("last_updated", now)
    elapsed = now - last
    rounds_passed = int(elapsed / ROUND_DURATION_SECONDS)

    if rounds_passed == 0:
        return dict(state.get("flags", {}))

    # Decay
    active = {}
    for flag, rounds_remaining in state.get("flags", {}).items():
        if rounds_remaining == -1:
            # Persistent flag -- never decays
            active[flag] = -1
        else:
            new_remaining = rounds_remaining - rounds_passed
            if new_remaining > 0:
                active[flag] = new_remaining

    # Write back decayed state
    room.ndb.room_state = {
        "flags": active,
        "last_updated": now,
    }

    return active


def add_room_flag(room, flag_name, duration=None):
    """
    Add or refresh a flag on a room.
    Uses FLAG_VOCABULARY default duration if not specified.
    Silently ignores unknown flag names -- log warning instead
    of crashing, but flag the error for builders.

    Args:
        room:      SoravelonRoom object
        flag_name: string -- must be in FLAG_VOCABULARY
        duration:  int rounds (None = use vocabulary default)
    """
    if flag_name not in FLAG_VOCABULARY:
        import evennia
        evennia.logger.log_warn(
            f"add_room_flag: unknown flag '{flag_name}' on room "
            f"'{room.key}' (#{room.id}). Add to FLAG_VOCABULARY first."
        )
        return

    if duration is None:
        duration = FLAG_VOCABULARY[flag_name]["typical_duration"]

    # Get current flags (with decay applied)
    current_flags = get_room_flags(room)

    # Add or refresh (take the longer duration if already present)
    current_flags[flag_name] = max(
        current_flags.get(flag_name, 0), duration
    )

    room.ndb.room_state = {
        "flags": current_flags,
        "last_updated": time.time(),
    }


def remove_room_flag(room, flag_name):
    """Explicitly remove a flag before it expires naturally."""
    current_flags = get_room_flags(room)
    current_flags.pop(flag_name, None)
    room.ndb.room_state = {
        "flags": current_flags,
        "last_updated": time.time(),
    }


def get_dominant_flag(room):
    """
    Return the single most significant flag for Sense display.
    Priority order defined in SENSE_PRIORITY below.
    Returns None if room has no active flags and is not still.
    """
    active = get_room_flags(room)
    if not active:
        return "still" if _room_qualifies_as_still(room) else None

    for flag in SENSE_PRIORITY:
        if flag in active:
            return flag

    # Fall back to whatever is present with most rounds remaining
    return max(active, key=active.get)


def _room_qualifies_as_still(room):
    """
    A room with no active flags and no recent combat is 'still'.
    Checks room.ndb for recent activity timestamp.
    """
    last_activity = room.ndb.last_activity or 0
    return (time.time() - last_activity) > (ROUND_DURATION_SECONDS * 20)


# ---------------------------------------------------------------------------
# Sense display -- priority order and atmospheric text
# ---------------------------------------------------------------------------

# Priority order for Sense display -- most significant first
SENSE_PRIORITY = [
    "void_touched",
    "node_critical",
    "ancient_presence",
    "resonant",
    "corrupted_death",
    "power_vacuum",
    "toxic_air",
    "burning",
    "charged",
    "frozen",
    "shadow_marked",
    "living_wood",
    "predator_kill",
    "fading_life",
    "blood_soaked",
    "disrupted",
    "node_calming",
    "unsettled",
    "fortified",
    "scouted",
    "still",
]

# Player-facing atmospheric descriptions for each flag.
# Sense displays the dominant flag's text after room entry and combat rounds.
SENSE_DISPLAY = {
    "charged":          "The air here hums with discharged energy.",
    "burning":          "Heat lingers. Something burned here recently.",
    "frozen":           "A cold that goes deeper than temperature.",
    "toxic_air":        "You taste something wrong in the air.",
    "resonant":         "The old patterns are awake here. You can feel them.",
    "void_touched":     ("Something that predates everything you know "
                         "was active here. Recently."),
    "fading_life":      "Something died here that had deep roots in the world.",
    "blood_soaked":     "The violence is recent. You can still feel it.",
    "living_wood":      "Living growth is threading through this place.",
    "fortified":        "Someone has thought carefully about this ground.",
    "scouted":          ("You know this room. The angles. The exits. "
                         "The weak points."),
    "disrupted":        "Magic doesn't sit right here.",
    "power_vacuum":     ("Something significant is gone. The space it left "
                         "is still raw."),
    "unsettled":        "The normal order of this place has been disturbed.",
    "ancient_presence": ("The old infrastructure is awake here. Base-8. "
                         "Dragon-made. Recent."),
    "still":            ("This place is quiet in a way that goes "
                         "beneath the surface."),
    "shadow_marked":    "The shadows here feel intentional.",
    "predator_kill":    ("Something that hunted here is gone. "
                         "The room knows it."),
    "corrupted_death":  ("The death here didn't end cleanly. "
                         "Something lingers."),
    "node_critical":    ("The world is holding its breath here. "
                         "Something is very wrong."),
    "node_calming":     "A tension you didn't notice is releasing.",
    None:               "",
}
