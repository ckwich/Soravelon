"""
Lore fragment registry -- static mapping of fragment_id to metadata.

Provides zone-grouped lookup for the CmdLore journal command.
All fragments defined in area files are registered here so CmdLore
can display them without scanning room objects at runtime.
"""

LORE_FRAGMENTS = {
    # ------------------------------------------------------------------
    # Cantera Edge (13 fragments)
    # ------------------------------------------------------------------
    "cantera_history_001": {
        "zone": "Cantera Edge",
        "zone_id": "cantera_edge",
        "title": "Woodcutter's Journal",
        "text": (
            "A woodcutter's journal, water-damaged but legible: "
            "'Third week. The saws dull faster here than anywhere else on the "
            "contract. Foreman says it is the sap -- amber-colored, thick as "
            "honey. It gums the blades. The trees do not want to be cut. I am "
            "starting to think he is right about that in ways he does not mean.'"
        ),
    },
    "cantera_history_002": {
        "zone": "Cantera Edge",
        "zone_id": "cantera_edge",
        "title": "Survey Marker",
        "text": (
            "Carved into the bridge rail in blocky Imperial script: 'SURVEY "
            "MARKER XII-IV. CANTERA QUARRY ROAD. BY ORDER OF THE THIRD "
            "SURVEY COMMISSION.' Below it, scratched in a different hand: "
            "'They were not quarrying stone.'"
        ),
    },
    "cantera_druid_001": {
        "zone": "Cantera Edge",
        "zone_id": "cantera_edge",
        "title": "Druid Marker Pattern",
        "text": (
            "The spiraling grooves on the marker stone are not decorative. "
            "Traced with a fingertip, they form a pattern that repeats "
            "every eight turns -- a mathematical relationship. Druids "
            "carved these, but the pattern predates druidic tradition "
            "by millennia. Someone taught it to them."
        ),
    },
    "cantera_amber_001": {
        "zone": "Cantera Edge",
        "zone_id": "cantera_edge",
        "title": "Warm Amber Sap",
        "text": (
            "The amber sap is warm. Not sun-warm -- warm from within, "
            "as if the tree's blood carries heat from deep underground. "
            "Alchemists prize it because it holds enchantment better "
            "than any mineral substrate. The trees are pulling something "
            "up from the earth. Something old."
        ),
    },
    "cantera_pala_001": {
        "zone": "Cantera Edge",
        "zone_id": "cantera_edge",
        "title": "Grown Symbols",
        "text": (
            "The marks on the interior walls are not carved -- they are "
            "grown. The heartwood formed around shapes that were placed "
            "inside the tree centuries ago and absorbed. The symbols are "
            "three-dimensional, embedded in the wood at different depths. "
            "Eight distinct symbols. Always eight."
        ),
    },
    "cantera_shrine_001": {
        "zone": "Cantera Edge",
        "zone_id": "cantera_edge",
        "title": "Shrine Stones",
        "text": (
            "The eight stones are carved from a material not found "
            "anywhere in the Cantera. Basalt, perhaps, from the coastal "
            "cliffs far to the northeast. Someone carried them here. "
            "The symbols on each are different but share a common "
            "structural element -- four strokes each, intersecting "
            "at a central point."
        ),
    },
    "cantera_crystal_001": {
        "zone": "Cantera Edge",
        "zone_id": "cantera_edge",
        "title": "Vibrating Crystals",
        "text": (
            "The crystals vibrate at a frequency that changes throughout "
            "the day -- faster at dawn and dusk, slower at noon and "
            "midnight. The cycle is not solar. It is a harmonic of "
            "something deeper. An alchemist with resonance-tuned "
            "instruments could map it. The pattern would have eight "
            "nodes."
        ),
    },
    "cantera_node_lore_001": {
        "zone": "Cantera Edge",
        "zone_id": "cantera_edge",
        "title": "Standing Stone Anchors",
        "text": (
            "The eight standing stones are not merely placed -- they are "
            "anchored. Each one extends deep into the earth, far deeper "
            "than its visible height. They are keystones in a structure "
            "that continues underground. The symbols on each stone are "
            "different, but together they form a complete statement in "
            "a language that predates all known writing systems. "
            "Four strokes per symbol. Eight symbols total. Thirty-two "
            "strokes. A base-eight expression."
        ),
    },
    "cantera_node_lore_002": {
        "zone": "Cantera Edge",
        "zone_id": "cantera_edge",
        "title": "The Resonance Lens",
        "text": (
            "The stone disc at the center is not a lid or a marker. It "
            "is a lens. The concentric rings focus something -- not "
            "light, but the resonance itself. The disc amplifies the "
            "vibration from below and distributes it through the stone "
            "circle. This was designed. Engineered. By something that "
            "understood mathematics and resonance frequencies at a "
            "level no current civilization possesses."
        ),
    },
    "cantera_stabilization_001": {
        "zone": "Cantera Edge",
        "zone_id": "cantera_edge",
        "title": "The Regulator Channels",
        "text": (
            "The channel system is a regulator. When sap flows through "
            "all channels unobstructed, the node operates at a stable "
            "baseline. Blockages cause feedback -- resonance that "
            "amplifies instead of dispersing. The system was designed "
            "to be maintained. Whoever built it expected someone to "
            "keep the channels clear. That maintenance stopped long ago."
        ),
    },
    "cantera_l1_lore_001": {
        "zone": "Cantera Edge",
        "zone_id": "cantera_edge",
        "title": "Beneath the Lens",
        "text": (
            "When the node is active, the stone disc becomes translucent. "
            "Through it, shapes are visible -- structures beneath the "
            "earth, extending far deeper than any root system. Corridors "
            "of shaped stone. Chambers with geometric precision. This "
            "is not a natural formation. Something was built here, and "
            "the forest grew over it."
        ),
    },
    "cantera_l1_lore_002": {
        "zone": "Cantera Edge",
        "zone_id": "cantera_edge",
        "title": "The Singing Stones",
        "text": (
            "In the node's active state, the standing stones sing in "
            "harmony. The eight notes form an octave -- but not a human "
            "octave. The intervals are different. Base-eight. The melody "
            "repeats every eight measures, each repetition introducing "
            "a variation so subtle it takes hours to detect. This is "
            "not music. It is communication. Something is speaking."
        ),
    },
    "cantera_l1_lore_003": {
        "zone": "Cantera Edge",
        "zone_id": "cantera_edge",
        "title": "Growing Infrastructure",
        "text": (
            "The crystals in the garden rearrange themselves during "
            "node activation. Their positions shift -- slowly, over "
            "hours -- into a configuration that mirrors the standing "
            "stones above. An octagonal pattern. The crystals ARE the "
            "same material as the standing stones, just younger. The "
            "node is growing its own infrastructure. Or trying to."
        ),
    },
    # ------------------------------------------------------------------
    # Stormhaven Coast (5 fragments)
    # ------------------------------------------------------------------
    "lore_standing_stones": {
        "zone": "Stormhaven Coast",
        "zone_id": "stormhaven_coast",
        "title": "Standing Stones of Storm Bluffs",
        "text": (
            "The three standing stones on Storm Bluffs are carved from "
            "basalt -- a volcanic rock found nowhere within five hundred "
            "miles. Someone transported them here at enormous cost and "
            "effort. Their alignment corresponds to no known astronomical "
            "pattern. Their grain and tool marks match samples from "
            "pre-human ruins on the western continent."
        ),
    },
    "lore_seaspray_log": {
        "zone": "Stormhaven Coast",
        "zone_id": "stormhaven_coast",
        "title": "Captain's Log of the Seaspray",
        "text": (
            "The captain's log of the Seaspray is mostly destroyed by "
            "water, but one entry remains legible: 'Day 47 -- the crew "
            "reports lights beneath the water near the reef. Not "
            "bioluminescence. Structured. Geometric. The navigator "
            "refuses to chart this section. I understand why.' The "
            "next page is blank."
        ),
    },
    "lore_fossil_wall": {
        "zone": "Stormhaven Coast",
        "zone_id": "stormhaven_coast",
        "title": "Fossil Wall Specimen",
        "text": (
            "The fossils in this wall span millions of years of marine "
            "history. One specimen stands out: a creature with traits "
            "of both serpent and something mammalian, preserved in "
            "perfect detail. It matches no known taxonomy. Marine "
            "biologists of the Naturalism guild have theorized about "
            "these creatures -- sea serpents, they call them. Not all "
            "are fossils. Some are still out there."
        ),
    },
    "lore_ancient_cairn": {
        "zone": "Stormhaven Coast",
        "zone_id": "stormhaven_coast",
        "title": "Ancient Landing Cairn",
        "text": (
            "The cairn at the cliff's highest point is a navigation "
            "marker -- not for ships, but for something that approached "
            "from the air. The stones are positioned to be visible from "
            "directly above, forming a pattern that reads as a landing "
            "glyph in pre-human notation. Dragons used this coast long "
            "before humans fished it."
        ),
    },
    "lore_smuggler_charts": {
        "zone": "Stormhaven Coast",
        "zone_id": "stormhaven_coast",
        "title": "Captain Wrack's Charts",
        "text": (
            "Captain Wrack's charts reveal more than smuggling routes. "
            "One chart maps the underwater topography offshore with "
            "impossible accuracy -- depths, currents, and structures "
            "that should be invisible from the surface. A note in the "
            "margin reads: 'They showed me. The price was fair. The "
            "old ones beneath the reef know things the Empire does not.'"
        ),
    },
    # ------------------------------------------------------------------
    # Reth Foothills (5 fragments)
    # ------------------------------------------------------------------
    "lore_reth_mine_symbols": {
        "zone": "Reth Foothills",
        "zone_id": "reth_foothills",
        "title": "Mine Alcove Symbols",
        "text": (
            "The symbols in the hidden alcove predate the Greystone Mine "
            "by millennia. They are arranged in groups of eight -- the same "
            "notation found on the Ashwatch Tower in Vael's Crossing. "
            "The warmth radiating from them is consistent and sourceless. "
            "A careful survey would mark this as a dormant node signature "
            "-- the mine was dug through it without knowing what lay in "
            "the rock."
        ),
    },
    "lore_reth_golem_terrace": {
        "zone": "Reth Foothills",
        "zone_id": "reth_foothills",
        "title": "Broken Golem",
        "text": (
            "The broken golem on the terrace is of a design that matches "
            "no known Imperial construction period. Its joints are fitted "
            "with eight-fold symmetry -- the same mathematical base that "
            "appears in dragon-era architecture. The golem was not built "
            "by humans. It was built by something that thought in eights."
        ),
    },
    "lore_reth_foundation": {
        "zone": "Reth Foothills",
        "zone_id": "reth_foothills",
        "title": "Ancient Foundation",
        "text": (
            "The ancient foundation's layout -- a central circle with "
            "eight radiating chambers -- matches theoretical diagrams "
            "of a node resonance amplifier. If this building functioned "
            "as designed, it would have been capable of amplifying node "
            "energy across the entire Reth mountain range. The builders "
            "understood something about the infrastructure that has been "
            "forgotten for a thousand years."
        ),
    },
    "lore_reth_summit_pillar": {
        "zone": "Reth Foothills",
        "zone_id": "reth_foothills",
        "title": "Summit Pillar",
        "text": (
            "The stone pillar at the summit is carved with a single word "
            "in a script that predates all known writing systems. The word "
            "has no translation. Standing beside it in wind, the air "
            "moves in a pattern -- a vortex with eight arms. The pillar "
            "is not decorative. It is functional. It still works."
        ),
    },
    "lore_reth_old_nest": {
        "zone": "Reth Foothills",
        "zone_id": "reth_foothills",
        "title": "Old Nest Inscriptions",
        "text": (
            "Behind the rotting silk in the old nest, the cave wall "
            "bears the familiar eight-circle notation. But here, the "
            "circles are arranged differently -- they overlap, forming "
            "a chain. The pattern reads like a sequence diagram: "
            "instructions, not labels. Whatever "
            "process these symbols describe, it was meant to be "
            "performed in order. Grandmother Spider built her first "
            "nest directly over these instructions. Coincidence seems "
            "unlikely."
        ),
    },
    # ------------------------------------------------------------------
    # Ashreach Plains (5 fragments)
    # ------------------------------------------------------------------
    "ashreach_octagonal_01": {
        "zone": "Ashreach Plains",
        "zone_id": "ashreach_plains",
        "title": "Octagonal Platform",
        "text": (
            "The octagonal platform's geometry is deliberate -- eight sides, "
            "eight posts. The pattern recurs in every ruin across the Ashreach. "
            "Whoever built this counted differently than we do."
        ),
    },
    "ashreach_sunken_carving_01": {
        "zone": "Ashreach Plains",
        "zone_id": "ashreach_plains",
        "title": "Sunken Chamber Carvings",
        "text": (
            "The carvings in the sunken chamber are remarkably precise -- "
            "circles divided into eight equal parts, repeated in cascading "
            "scales. Mathematical, not decorative. The toolwork predates "
            "anything Imperial."
        ),
    },
    "ashreach_ash_basin_01": {
        "zone": "Ashreach Plains",
        "zone_id": "ashreach_plains",
        "title": "Ash Basin",
        "text": (
            "The ash in the basin is too fine to be from wood. It carries "
            "a faint metallic tang, and when disturbed, motes hang in the "
            "air far longer than gravity should allow. The locals avoid "
            "this place after dark."
        ),
    },
    "ashreach_wind_channel_01": {
        "zone": "Ashreach Plains",
        "zone_id": "ashreach_plains",
        "title": "Wind Channel",
        "text": (
            "The acoustic properties of the wind channel are not natural. "
            "The walls are slightly curved in a way that amplifies certain "
            "frequencies. An engineer would say this was a communication "
            "device. A scholar would wonder who was speaking to whom."
        ),
    },
    "ashreach_carved_seat_01": {
        "zone": "Ashreach Plains",
        "zone_id": "ashreach_plains",
        "title": "Carved Seat",
        "text": (
            "The seat faces east -- toward the sunrise, toward The Reth, "
            "toward something. Its proportions are wrong for any living "
            "ancestry. The armrests are scored with claw marks, four "
            "parallel grooves repeated on each side."
        ),
    },
    # ------------------------------------------------------------------
    # Vael's Crossing (4 fragments)
    # ------------------------------------------------------------------
    "lore_ashwatch_symbols": {
        "zone": "Vael's Crossing",
        "zone_id": "vaels_crossing",
        "title": "Ashwatch Tower Symbols",
        "text": (
            "The symbols carved into the Ashwatch Tower parapet are "
            "arranged in groups of eight. Each group follows a pattern -- "
            "four primary symbols, four modifiers. The notation system "
            "is mathematical, not linguistic. It predates every known "
            "human writing system by at least two thousand years."
        ),
    },
    "lore_sunken_temple_warmth": {
        "zone": "Vael's Crossing",
        "zone_id": "vaels_crossing",
        "title": "Sunken Temple Warmth",
        "text": (
            "The warmth emanating from beneath the Sunken Temple has "
            "no natural source. It is consistent, never varying. A "
            "careful comparison against old survey notes identifies it "
            "as the thermal signature of an intact sub-surface node -- "
            "dormant but not dead. The temple was built directly over it. "
            "Not coincidentally."
        ),
    },
    "lore_old_cistern_stones": {
        "zone": "Vael's Crossing",
        "zone_id": "vaels_crossing",
        "title": "Old Cistern Stones",
        "text": (
            "The stones of the old cistern are fitted with dragon-era "
            "precision. No mortar, no gaps. The symbols carved into "
            "the walls match those on the Ashwatch Tower and the "
            "Sunken Temple. Three locations in one city, all built by "
            "the same hands. Or claws."
        ),
    },
    "lore_guild_tree": {
        "zone": "Vael's Crossing",
        "zone_id": "vaels_crossing",
        "title": "Guild Quarter Tree",
        "text": (
            "The ancient tree in the Guild Quarter courtyard is of no "
            "known species. Its bark bears the same unfamiliar symbols. "
            "It has stood here longer than the city. The guilds built "
            "around it -- not the other way around."
        ),
    },
}


def get_zone_fragments(zone_id):
    """Return dict of {frag_id: frag_data} for a zone."""
    return {k: v for k, v in LORE_FRAGMENTS.items() if v["zone_id"] == zone_id}


def get_all_zones():
    """Return sorted list of unique (zone_id, zone_name) tuples."""
    zones = {}
    for frag in LORE_FRAGMENTS.values():
        zones[frag["zone_id"]] = frag["zone"]
    return sorted(zones.items(), key=lambda x: x[1])


def get_fragment(fragment_id):
    """Return fragment data or None."""
    return LORE_FRAGMENTS.get(fragment_id)
