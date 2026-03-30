"""
Stormhaven Coast -- Starter Zone 4: Coastal Biome

A jagged northeastern coastline zone east of Vael's Crossing. Salt-scoured
cliffs, sea caves, tidal pools, a small fishing village, a smuggler's cove,
a crumbling lighthouse, and a shipwreck on the rocks.

100+ rooms across 8 sub-areas:
    1. Harbor Road Approach  (~8 rooms)  -- Trail from Vael's Crossing
    2. Cliff Path North      (~14 rooms) -- Rocky clifftop trail
    3. Stormhaven Village    (~10 rooms) -- Fishing settlement + harbor
    4. Tidal Flats           (~14 rooms) -- Beaches, tide pools, shoreline
    5. Sea Caves             (~16 rooms) -- Underground coastal caverns
    6. Smuggler's Cove       (~10 rooms) -- Hidden criminal hideout
    7. Lighthouse Point      (~8 rooms)  -- Watchtower landmark area
    8. The Wreck of the Seaspray (~8 rooms) -- Shipwreck ruins
    9. Cliff Path South      (~14 rooms) -- Southern coastal cliffs
   10. Storm Bluffs          (~6 rooms)  -- High windswept overlook

No levels -- zone scaling makes all content universal.
"""

from world.area_builder import AreaBuilder


def build():
    area = AreaBuilder("stormhaven_coast")

    # ------------------------------------------------------------------
    # Zone setup
    # ------------------------------------------------------------------
    area.zone(
        name="Stormhaven Coast",
        zone_type="coastal",
        continent="varath",
        faction_territory=None,
        world_x=60,
        world_y=10,
        world_radius=60,
    )

    # ==================================================================
    #  SUB-AREA 1: HARBOR ROAD APPROACH (~8 rooms)
    #  Trail connecting Vael's Crossing to the coast.
    # ==================================================================

    hr_junction = area.room(
        "hr_junction",
        name="Harbor Road - Coastal Junction",
        desc=(
            "The Harbor Road crests a low rise and the world changes. Salt "
            "air hits like a wall, replacing the dust of the Ashreach plains. "
            "To the east, the road descends toward a distant shoreline where "
            "grey waves crash against dark rock. Gulls wheel overhead in lazy "
            "circles, their cries sharp and mocking. A weathered signpost "
            "points east to Stormhaven Village and north along the cliff path."
        ),
        room_type="path",
        indoor=False,
        ambient_echoes=[
            "A gull cries overhead, circling on the coastal wind.",
            "Salt air stings your nostrils as the breeze shifts.",
            "The distant crash of waves is a constant low thunder.",
        ],
    )

    hr_descent_1 = area.room(
        "hr_descent_1",
        name="Harbor Road - Seaward Descent",
        desc=(
            "The road angles downward, switching back and forth along the "
            "hillside. Hardy scrub grass clings to the verge, bent permanently "
            "eastward by the prevailing wind. The soil underfoot shifts from "
            "brown earth to grey sand mixed with crushed shell. Below, the "
            "rooftops of a small settlement are visible through sea mist."
        ),
        room_type="path",
        indoor=False,
    )

    hr_descent_2 = area.room(
        "hr_descent_2",
        name="Harbor Road - Lower Switchback",
        desc=(
            "The road levels briefly before another descent. Driftwood has "
            "been used to shore up the embankment where winter storms eroded "
            "the hillside. A crude wooden railing marks the drop-off to the "
            "right -- a sheer twenty-foot fall to the rocks below. Someone "
            "has carved initials into the railing posts."
        ),
        room_type="path",
        indoor=False,
    )

    hr_salt_flat = area.room(
        "hr_salt_flat",
        name="Harbor Road - Salt Flat Crossing",
        desc=(
            "The road crosses a flat expanse of salt-crusted earth where "
            "nothing grows. White mineral deposits crackle underfoot like "
            "thin ice. During high tide, seawater creeps up through the "
            "ground here, leaving behind these crystalline residues. The "
            "air is thick with brine."
        ),
        room_type="path",
        indoor=False,
    )

    hr_fisherman_rest = area.room(
        "hr_fisherman_rest",
        name="Fisherman's Rest",
        desc=(
            "A flat stone beside the road where travelers pause before the "
            "final approach to the village. Old nets have been strung between "
            "posts to dry, their frayed edges fluttering in the wind. A "
            "fire pit shows signs of recent use -- fish bones and charred "
            "driftwood. Someone left a battered tin cup on the stone."
        ),
        room_type="clearing",
        indoor=False,
        ambient_echoes=[
            "Dried nets crackle and snap in the wind.",
            "A crab picks through the remains of a fish skeleton near the fire pit.",
        ],
    )

    hr_coastal_scrub = area.room(
        "hr_coastal_scrub",
        name="Coastal Scrubland",
        desc=(
            "Low, wind-bent bushes cover a slope between the road and the "
            "cliffs. The vegetation is tough and thorny, grey-green leaves "
            "coated with a permanent sheen of salt spray. Narrow animal "
            "trails thread between the bushes -- rabbits, or something "
            "that hunts them."
        ),
        room_type="clearing",
        indoor=False,
    )

    hr_overlook = area.room(
        "hr_overlook",
        name="Coastal Overlook",
        desc=(
            "A natural ledge juts from the hillside, providing a sweeping "
            "view of the coastline. To the north, jagged cliffs march "
            "toward a distant headland where a lighthouse stands, its "
            "beacon dark. South, the coast curves into a sheltered bay. "
            "The sea is the color of old iron, streaked with white where "
            "waves break on hidden reefs."
        ),
        room_type="clearing",
        indoor=False,
        ambient_echoes=[
            "Wind whips across the overlook, tugging at loose clothing.",
            "Far below, waves explode against the cliff base in white bursts.",
        ],
    )

    hr_bridge = area.room(
        "hr_bridge",
        name="Driftwood Bridge",
        desc=(
            "A makeshift bridge spans a gully carved by rainwater runoff. "
            "Built from salvaged ship timbers and driftwood, it creaks "
            "ominously underfoot. Barnacles still cling to some of the "
            "planks. Below, a trickle of brackish water winds toward the "
            "sea. The bridge has been repaired many times -- each section "
            "is a different color of wood."
        ),
        room_type="path",
        indoor=False,
    )

    # Harbor Road exits
    area.exit(hr_junction, hr_descent_1, "east")
    area.exit(hr_descent_1, hr_junction, "west")
    area.exit(hr_descent_1, hr_descent_2, "east")
    area.exit(hr_descent_2, hr_descent_1, "west")
    area.exit(hr_descent_2, hr_salt_flat, "south")
    area.exit(hr_salt_flat, hr_descent_2, "north")
    area.exit(hr_salt_flat, hr_fisherman_rest, "east")
    area.exit(hr_fisherman_rest, hr_salt_flat, "west")
    area.exit(hr_junction, hr_overlook, "south")
    area.exit(hr_overlook, hr_junction, "north")
    area.exit(hr_overlook, hr_coastal_scrub, "east")
    area.exit(hr_coastal_scrub, hr_overlook, "west")
    area.exit(hr_coastal_scrub, hr_bridge, "east")
    area.exit(hr_bridge, hr_coastal_scrub, "west")

    # Cross-zone exit: west to Vael's Crossing
    area.exit(hr_junction, "vaels_crossing:hg_east_road", "west")

    # ==================================================================
    #  SUB-AREA 2: CLIFF PATH NORTH (~14 rooms)
    #  Rocky clifftop trail along the northern coast. Harpy territory.
    # ==================================================================

    cn_trailhead = area.room(
        "cn_trailhead",
        name="Cliff Path - Northern Trailhead",
        desc=(
            "A narrow path branches north from the road, following the edge "
            "of the coastal cliffs. A rope has been strung between iron stakes "
            "driven into the rock -- a guide rail for the brave or foolish. "
            "The cliff edge is crumbling in places. Below, the sea churns "
            "against the rocks with a sound like grinding bones."
        ),
        room_type="path",
        indoor=False,
    )

    cn_narrow_ledge = area.room(
        "cn_narrow_ledge",
        name="Cliff Path - Narrow Ledge",
        desc=(
            "The path narrows to barely shoulder-width. The cliff face rises "
            "to the left, streaked with salt and bird droppings. To the right, "
            "nothing but a long drop to the sea. Handholds have been chipped "
            "into the rock -- some look ancient, others recent. The wind is "
            "a physical force here, shoving from the east."
        ),
        room_type="path",
        indoor=False,
    )

    cn_gull_roost = area.room(
        "cn_gull_roost",
        name="Cliff Path - Gull Roost",
        desc=(
            "A wider section of cliff where thousands of seabirds have claimed "
            "nesting rights. The rock is white with guano, and the noise is "
            "deafening -- a cacophony of shrieks, croaks, and fluttering wings. "
            "The birds are not afraid of travelers. They are, however, extremely "
            "territorial about their eggs."
        ),
        room_type="clearing",
        indoor=False,
        ambient_echoes=[
            "A gull shrieks directly in your face, defending its nest.",
            "The stench of guano is overwhelming.",
            "Wings beat the air as hundreds of birds shuffle for position.",
        ],
    )

    cn_wind_gap = area.room(
        "cn_wind_gap",
        name="Cliff Path - Wind Gap",
        desc=(
            "A natural gap in the cliff wall funnels the coastal wind into "
            "a howling channel. Crossing it requires leaning into the gale "
            "at an almost comical angle. Someone has strung a chain across "
            "the gap at waist height -- grab it or be pushed off the path. "
            "On the far side, the cliff widens again."
        ),
        room_type="path",
        indoor=False,
    )

    cn_harpy_nests = area.room(
        "cn_harpy_nests",
        name="Cliff Path - Harpy Nesting Grounds",
        desc=(
            "The upper cliffs here are riddled with shallow caves and ledges "
            "where cliff harpies nest. Bone fragments and shredded fish litter "
            "the ground. Crude nests of driftwood and seaweed cling to every "
            "available ledge. The air reeks of rotting fish. Scratching sounds "
            "echo from above."
        ),
        room_type="clearing",
        indoor=False,
        ambient_echoes=[
            "A shriek echoes from the upper ledges -- harpy or gull?",
            "Claws scrape on rock somewhere above.",
            "Bones crunch underfoot on the guano-covered ground.",
        ],
    )

    cn_sea_stack_view = area.room(
        "cn_sea_stack_view",
        name="Cliff Path - Sea Stack Vista",
        desc=(
            "The path rounds a headland and reveals a dramatic vista: three "
            "towering sea stacks rise from the waves like broken fingers. "
            "The largest is capped with a harpy nest the size of a cart. "
            "Birds -- and things that are not quite birds -- circle the "
            "stacks in overlapping spirals. The path continues north along "
            "the cliff edge."
        ),
        room_type="path",
        indoor=False,
    )

    cn_rockfall = area.room(
        "cn_rockfall",
        name="Cliff Path - Rockfall",
        desc=(
            "A recent rockfall has partially blocked the path. Boulders "
            "of dark stone, some as large as barrels, lie scattered where "
            "they tumbled from the cliff above. The path is still passable "
            "but requires careful navigation. Fresh claw marks score the "
            "rock face -- something used this route to climb."
        ),
        room_type="path",
        indoor=False,
    )

    cn_tidal_cave_entrance = area.room(
        "cn_tidal_cave_entrance",
        name="Cliff Path - Tidal Cave Entrance",
        desc=(
            "A break in the cliff reveals a steep, slippery path descending "
            "to a cave mouth at the waterline. At low tide, the entrance is "
            "accessible -- a dark arch in the rock, crusted with barnacles "
            "and draped with kelp. At high tide, the sea swallows the opening "
            "entirely. The rocks are treacherous with wet algae."
        ),
        room_type="path",
        indoor=False,
    )

    cn_wind_carved = area.room(
        "cn_wind_carved",
        name="Cliff Path - Wind-Carved Passage",
        desc=(
            "Millennia of coastal wind have carved the rock into bizarre "
            "organic shapes -- arches, pillars, and hollows that whistle "
            "and moan when the breeze shifts. The passage threads between "
            "these formations like a corridor in a natural cathedral. Some "
            "of the shapes look almost deliberate."
        ),
        room_type="path",
        indoor=False,
        ambient_echoes=[
            "Wind moans through the carved stone formations.",
            "A low whistle rises from a hollow in the rock, eerie and sustained.",
        ],
    )

    cn_cairn = area.room(
        "cn_cairn",
        name="Cliff Path - Ancient Cairn",
        desc=(
            "A stone cairn stands at the highest point of the northern cliff "
            "path. It is old -- impossibly old. The stones are fitted without "
            "mortar in a style that predates Imperial construction by ages. "
            "Offerings have been left at its base: fish bones, sea glass, "
            "a copper coin so corroded it is barely recognizable. The view "
            "from here spans the entire coastline."
        ),
        room_type="ruins",
        indoor=False,
    )

    cn_descent_beach = area.room(
        "cn_descent_beach",
        name="Cliff Path - Beach Descent",
        desc=(
            "A series of crude steps carved into the cliff face provides "
            "access to the beach far below. The steps are worn smooth by "
            "generations of fishermen carrying their catch upward. Rope "
            "loops serve as handholds at the steepest sections. The descent "
            "is dizzying but manageable."
        ),
        room_type="path",
        indoor=False,
    )

    cn_eagle_perch = area.room(
        "cn_eagle_perch",
        name="Cliff Path - Eagle's Perch",
        desc=(
            "A flat-topped rock jutting from the cliff edge, worn smooth "
            "by countless visitors who paused here to catch their breath. "
            "A massive sea eagle has claimed the highest point as its lookout, "
            "and the surrounding rock is streaked with white. The eagle "
            "watches travelers with golden eyes, undisturbed."
        ),
        room_type="clearing",
        indoor=False,
    )

    cn_crevice = area.room(
        "cn_crevice",
        name="Cliff Path - Narrow Crevice",
        desc=(
            "The path squeezes through a vertical crack in the cliff, "
            "barely wide enough to pass through sideways. The walls are "
            "damp and slick with condensation. Daylight is visible at "
            "both ends but the middle section is dim enough to require "
            "feeling your way. Something has webbed across the gap at "
            "head height."
        ),
        room_type="path",
        indoor=False,
    )

    cn_headland = area.room(
        "cn_headland",
        name="Northern Headland",
        desc=(
            "The cliff path ends at the northernmost point of the coast -- "
            "a windswept headland of dark stone jutting into the sea. Waves "
            "crash on three sides, sending spray high enough to soak anyone "
            "standing here. The lighthouse on the western point is visible "
            "from this vantage. So is the wreck of a ship on the rocks "
            "below the southern bluffs."
        ),
        room_type="clearing",
        indoor=False,
        ambient_echoes=[
            "Spray lashes across the headland as a wave breaks below.",
            "The wind is so strong it is difficult to stand upright.",
            "Gulls ride the updraft, hanging motionless in the air.",
        ],
    )

    # Cliff Path North exits
    area.exit(cn_trailhead, hr_junction, "south")
    area.exit(hr_junction, cn_trailhead, "north")
    area.exit(cn_trailhead, cn_narrow_ledge, "north")
    area.exit(cn_narrow_ledge, cn_trailhead, "south")
    area.exit(cn_narrow_ledge, cn_gull_roost, "north")
    area.exit(cn_gull_roost, cn_narrow_ledge, "south")
    area.exit(cn_gull_roost, cn_wind_gap, "northeast")
    area.exit(cn_wind_gap, cn_gull_roost, "southwest")
    area.exit(cn_wind_gap, cn_harpy_nests, "north")
    area.exit(cn_harpy_nests, cn_wind_gap, "south")
    area.exit(cn_harpy_nests, cn_sea_stack_view, "northeast")
    area.exit(cn_sea_stack_view, cn_harpy_nests, "southwest")
    area.exit(cn_sea_stack_view, cn_rockfall, "north")
    area.exit(cn_rockfall, cn_sea_stack_view, "south")
    area.exit(cn_rockfall, cn_tidal_cave_entrance, "east")
    area.exit(cn_tidal_cave_entrance, cn_rockfall, "west")
    area.exit(cn_rockfall, cn_wind_carved, "north")
    area.exit(cn_wind_carved, cn_rockfall, "south")
    area.exit(cn_wind_carved, cn_cairn, "northeast")
    area.exit(cn_cairn, cn_wind_carved, "southwest")
    area.exit(cn_cairn, cn_headland, "north")
    area.exit(cn_headland, cn_cairn, "south")
    area.exit(cn_narrow_ledge, cn_descent_beach, "east")
    area.exit(cn_descent_beach, cn_narrow_ledge, "west")
    area.exit(cn_wind_gap, cn_eagle_perch, "east")
    area.exit(cn_eagle_perch, cn_wind_gap, "west")
    area.exit(cn_wind_carved, cn_crevice, "east")
    area.exit(cn_crevice, cn_wind_carved, "west")

    # ==================================================================
    #  SUB-AREA 3: STORMHAVEN VILLAGE (~10 rooms)
    #  Small fishing settlement with harbor, inn, and fish market.
    # ==================================================================

    sv_village_square = area.room(
        "sv_village_square",
        name="Stormhaven Village - Square",
        desc=(
            "The center of Stormhaven is a muddy square of packed earth "
            "and crushed shells. A well stands at the center, its bucket "
            "rope frayed. Low stone buildings with slate roofs cluster "
            "around the square -- each one built to withstand the storms "
            "that give this place its name. Fishing nets are strung between "
            "buildings like festival bunting."
        ),
        room_type="building",
        indoor=False,
        ambient_echoes=[
            "A fisherman mends a net, humming a tuneless sea shanty.",
            "The well bucket creaks in the wind.",
            "Smoke from a chimney whips sideways in the coastal breeze.",
        ],
    )

    sv_harbor = area.room(
        "sv_harbor",
        name="Stormhaven Harbor",
        desc=(
            "A small natural harbor sheltered by a stone breakwater that "
            "has seen better centuries. Fishing boats rock at their moorings -- "
            "shallow-draft vessels with patched sails and names painted on "
            "their hulls in fading letters. The harbor master's shack leans "
            "precariously at the water's edge. The smell of fish, tar, and "
            "brine is inescapable."
        ),
        room_type="building",
        indoor=False,
        ambient_echoes=[
            "Rigging clanks against a mast as a boat rocks.",
            "A fisherman heaves a crate of catch onto the dock.",
            "Water slaps against the stone breakwater in steady rhythm.",
        ],
    )

    sv_fish_market = area.room(
        "sv_fish_market",
        name="Stormhaven Fish Market",
        desc=(
            "Open-air stone slabs where the day's catch is cleaned, sorted, "
            "and sold. Blood gutters channel offal into the harbor. Gulls "
            "crowd the rooftops, waiting for scraps. A chalkboard lists "
            "today's prices -- or yesterday's, nobody updates it regularly. "
            "The fish here are strange, deep-water species with too many "
            "teeth and luminous eyes."
        ),
        room_type="building",
        indoor=False,
    )

    sv_tavern = area.room(
        "sv_tavern",
        name="The Drowning Sailor",
        desc=(
            "A squat stone tavern with a driftwood sign carved into the "
            "shape of a drowning man. The interior is dark, low-ceilinged, "
            "and warm. Fishing trophies -- mounted jaws, preserved specimens, "
            "and impossible-looking lures -- cover every wall. The ale is "
            "thick and dark and tastes of salt. So does everything else."
        ),
        room_type="building",
        indoor=True,
        ambient_echoes=[
            "A fisherman slams a tankard on the bar, demanding another.",
            "Someone in the corner tells a story about a fish the size of a boat.",
            "The fire crackles, throwing shadows across mounted sea creature jaws.",
        ],
    )

    sv_chandlery = area.room(
        "sv_chandlery",
        name="Stormhaven Chandlery",
        desc=(
            "A cramped shop selling rope, tar, sailcloth, hooks, and "
            "everything else a coastal settlement needs. Coils of rope "
            "hang from the ceiling. Barrels of pitch line the walls. "
            "The shopkeeper, an old woman with salt-stiffened hair, "
            "knows the name and purpose of every knot ever invented."
        ),
        room_type="building",
        indoor=True,
    )

    sv_smokehouse = area.room(
        "sv_smokehouse",
        name="Stormhaven Smokehouse",
        desc=(
            "A long, low building where fish are preserved for transport "
            "inland. Rows of gutted fish hang from hooks, wreathed in "
            "smoke from a driftwood fire that never goes out. The walls "
            "are blackened with years of soot. The smell is simultaneously "
            "appetizing and overwhelming."
        ),
        room_type="building",
        indoor=True,
    )

    sv_boatyard = area.room(
        "sv_boatyard",
        name="Stormhaven Boatyard",
        desc=(
            "An open yard where boats are hauled up for repair. A half-built "
            "hull sits on wooden cradles, its ribs exposed like the skeleton "
            "of some beached creature. Wood shavings carpet the ground. Tools "
            "hang from pegs on a weathered rack. The boatwright works in "
            "silence, measuring twice, cutting once."
        ),
        room_type="building",
        indoor=False,
    )

    sv_shrine = area.room(
        "sv_shrine",
        name="Seafarer's Shrine",
        desc=(
            "A tiny shrine built into a natural alcove in the cliff behind "
            "the village. Candle stubs, shell offerings, and small carvings "
            "cluster around a central stone that has been worn smooth by "
            "generations of touching hands. The shrine is dedicated to no "
            "specific deity -- fishermen pray to whatever might listen. "
            "The stone is always warm, even in winter."
        ),
        room_type="building",
        indoor=True,
    )

    sv_beach_landing = area.room(
        "sv_beach_landing",
        name="Village Beach Landing",
        desc=(
            "A strip of coarse grey sand where boats are dragged ashore. "
            "Above the tide line, racks of drying nets and stacks of "
            "lobster pots create a maze of fishermen's equipment. "
            "Children play in the shallows while their parents work. "
            "The beach continues south toward the tidal flats."
        ),
        room_type="clearing",
        indoor=False,
    )

    sv_dock = area.room(
        "sv_dock",
        name="Stormhaven Dock",
        desc=(
            "A wooden dock extending into the harbor, its planks warped "
            "and grey from years of salt exposure. Mooring posts are worn "
            "smooth by countless ropes. A lantern hangs at the dock's end, "
            "lit at dusk to guide returning boats. The water below is "
            "surprisingly clear -- you can see crabs scuttling across "
            "the sandy bottom."
        ),
        room_type="building",
        indoor=False,
    )

    # Village exits
    area.exit(sv_village_square, sv_harbor, "east")
    area.exit(sv_harbor, sv_village_square, "west")
    area.exit(sv_village_square, sv_tavern, "north")
    area.exit(sv_tavern, sv_village_square, "south")
    area.exit(sv_village_square, sv_fish_market, "south")
    area.exit(sv_fish_market, sv_village_square, "north")
    area.exit(sv_village_square, sv_chandlery, "west")
    area.exit(sv_chandlery, sv_village_square, "east")
    area.exit(sv_harbor, sv_dock, "east")
    area.exit(sv_dock, sv_harbor, "west")
    area.exit(sv_harbor, sv_boatyard, "north")
    area.exit(sv_boatyard, sv_harbor, "south")
    area.exit(sv_fish_market, sv_smokehouse, "east")
    area.exit(sv_smokehouse, sv_fish_market, "west")
    area.exit(sv_village_square, sv_shrine, "northwest")
    area.exit(sv_shrine, sv_village_square, "southeast")
    area.exit(sv_fish_market, sv_beach_landing, "south")
    area.exit(sv_beach_landing, sv_fish_market, "north")

    # Connect village to harbor road
    area.exit(hr_fisherman_rest, sv_village_square, "east")
    area.exit(sv_village_square, hr_fisherman_rest, "west")

    # ==================================================================
    #  SUB-AREA 4: TIDAL FLATS (~14 rooms)
    #  Beaches, tide pools, and shoreline. Shore crab territory.
    # ==================================================================

    tf_upper_beach = area.room(
        "tf_upper_beach",
        name="Upper Beach - Driftwood Line",
        desc=(
            "The upper beach is littered with driftwood deposited by high "
            "tides. Grey sand gives way to a band of debris: bleached wood, "
            "tangled kelp, broken shells, and the occasional rusted artifact "
            "from a ship that did not survive the coast. The tideline is a "
            "history of storms written in wreckage."
        ),
        room_type="clearing",
        indoor=False,
    )

    tf_tide_pool_1 = area.room(
        "tf_tide_pool_1",
        name="Tidal Pool - Shallow Basin",
        desc=(
            "A shallow rock pool left by the retreating tide. Anemones "
            "wave their tentacles lazily. Small crabs scuttle between "
            "crevices. A starfish clings to the side with stubborn patience. "
            "The water is crystal clear, warm from trapped sunlight. "
            "Everything here is small, patient, and tenacious."
        ),
        room_type="clearing",
        indoor=False,
    )

    tf_tide_pool_2 = area.room(
        "tf_tide_pool_2",
        name="Tidal Pool - Deep Basin",
        desc=(
            "A deeper pool, waist-high at the center, filled with dark "
            "water that suggests a connection to the sea below the rocks. "
            "Something moves in the depths -- quick silver flashes of fish "
            "too fast to identify. The rocks around the pool are sharp with "
            "barnacles. Sea glass fragments glint between the stones."
        ),
        room_type="clearing",
        indoor=False,
    )

    tf_sand_bar = area.room(
        "tf_sand_bar",
        name="Exposed Sand Bar",
        desc=(
            "A low ridge of sand and broken shell exposed at low tide. "
            "At high tide this is underwater -- the kelp and barnacles "
            "that coat its surface tell the story. Shore crabs patrol the "
            "bar in numbers, clicking their claws like disapproval. A "
            "few larger specimens are the size of dinner plates."
        ),
        room_type="clearing",
        indoor=False,
        ambient_echoes=[
            "Crabs click and scuttle across the exposed sand bar.",
            "A wave breaks nearby, sending foam racing across the sand.",
        ],
    )

    tf_kelp_strand = area.room(
        "tf_kelp_strand",
        name="Kelp Strand",
        desc=(
            "Thick ropes of kelp drape across the rocks and sand, torn "
            "from the seabed by storms. The kelp is dark brown, rubbery, "
            "and pops underfoot. Hidden beneath the strands, rock pools "
            "harbor tiny ecosystems. The smell is intensely marine -- "
            "salt, iodine, and the green tang of living ocean."
        ),
        room_type="clearing",
        indoor=False,
    )

    tf_crab_field = area.room(
        "tf_crab_field",
        name="Crab Feeding Grounds",
        desc=(
            "The beach here is pockmarked with burrows -- hundreds of them. "
            "Shore crabs emerge in waves, picking through tidal debris with "
            "methodical precision. The larger ones are aggressive, raising "
            "their claws at any approach. Fishermen from the village harvest "
            "here but always in groups."
        ),
        room_type="clearing",
        indoor=False,
        ambient_echoes=[
            "The sound of hundreds of tiny legs on wet sand is unsettling.",
            "A large crab raises its claws and sidesteps toward you, clicking.",
        ],
    )

    tf_rock_arch = area.room(
        "tf_rock_arch",
        name="Natural Rock Arch",
        desc=(
            "A dramatic natural arch of dark stone frames a view of the "
            "open sea. The arch is wide enough to walk through at low tide, "
            "though waves surge through it unpredictably. Salt crystals "
            "coat the inner surface, catching what little light penetrates. "
            "Beyond the arch, a path of exposed rocks leads toward the "
            "sea caves."
        ),
        room_type="path",
        indoor=False,
    )

    tf_flotsam_beach = area.room(
        "tf_flotsam_beach",
        name="Flotsam Beach",
        desc=(
            "A stretch of grey beach where the currents deposit everything "
            "the sea does not want. Broken barrels, waterlogged rope, a "
            "shattered figurehead with its face worn blank -- the detritus "
            "of maritime misfortune. Occasionally something valuable washes "
            "up. More often it is just wood and disappointment."
        ),
        room_type="clearing",
        indoor=False,
    )

    tf_mudflat = area.room(
        "tf_mudflat",
        name="Coastal Mudflat",
        desc=(
            "The beach transitions to thick grey mud that sucks at boots "
            "with each step. Wading birds stalk through the shallows on "
            "stilt legs, stabbing at things beneath the surface. The mud "
            "is treacherous -- locals say a man was swallowed whole last "
            "winter, though nobody can name him."
        ),
        room_type="clearing",
        indoor=False,
    )

    tf_shell_midden = area.room(
        "tf_shell_midden",
        name="Ancient Shell Midden",
        desc=(
            "A mound of ancient shells rises from the beach -- an old "
            "refuse heap from a settlement that predates Stormhaven by "
            "millennia. The shells are packed so densely they have become "
            "a kind of stone. Erosion has exposed layers of different "
            "species, some of which no longer exist in these waters. "
            "A crude stone tool protrudes from the mound's side."
        ),
        room_type="ruins",
        indoor=False,
    )

    tf_wave_cut_platform = area.room(
        "tf_wave_cut_platform",
        name="Wave-Cut Platform",
        desc=(
            "A flat expanse of rock scoured smooth by centuries of wave "
            "action. Shallow channels crisscross the surface, draining "
            "water back to the sea between swells. The platform extends "
            "thirty yards from the cliff base before dropping off sharply "
            "into deeper water. Walking on it requires care -- the surface "
            "is slick with algae."
        ),
        room_type="path",
        indoor=False,
    )

    tf_sea_glass_cove = area.room(
        "tf_sea_glass_cove",
        name="Sea Glass Cove",
        desc=(
            "A tiny sheltered cove where the sand is mixed with tumbled "
            "sea glass -- green, blue, amber, and rare pieces of deep "
            "red. The glass comes from centuries of broken bottles, "
            "shattered windows, and shipwreck lanterns, rounded smooth "
            "by the tireless sea. Collectors from the village come here "
            "but the supply never runs out."
        ),
        room_type="clearing",
        indoor=False,
    )

    tf_reef_edge = area.room(
        "tf_reef_edge",
        name="Reef Edge",
        desc=(
            "The beach ends at a line of dark, jagged reef exposed at "
            "low tide. The reef is alive -- encrusted with mussels, "
            "limpets, and tiny organisms that pop and hiss as the air "
            "reaches them. Pools between the reef sections are deep "
            "enough to harbor small fish and predatory crabs. The reef "
            "continues out to sea, marking the boundary of safe waters."
        ),
        room_type="clearing",
        indoor=False,
    )

    tf_stranded_boat = area.room(
        "tf_stranded_boat",
        name="Stranded Fishing Boat",
        desc=(
            "A fishing boat sits at a permanent angle on the sand, its "
            "hull stoved in by whatever rock it struck. The mast is "
            "broken, the sails long gone. The cabin is still accessible "
            "through a hatch. Someone has been using it as a shelter -- "
            "there are blankets, a fire ring of stones, and empty bottles "
            "inside."
        ),
        room_type="ruins",
        indoor=False,
    )

    # Tidal Flats exits
    area.exit(sv_beach_landing, tf_upper_beach, "south")
    area.exit(tf_upper_beach, sv_beach_landing, "north")
    area.exit(tf_upper_beach, tf_tide_pool_1, "east")
    area.exit(tf_tide_pool_1, tf_upper_beach, "west")
    area.exit(tf_tide_pool_1, tf_tide_pool_2, "east")
    area.exit(tf_tide_pool_2, tf_tide_pool_1, "west")
    area.exit(tf_upper_beach, tf_sand_bar, "south")
    area.exit(tf_sand_bar, tf_upper_beach, "north")
    area.exit(tf_sand_bar, tf_kelp_strand, "east")
    area.exit(tf_kelp_strand, tf_sand_bar, "west")
    area.exit(tf_sand_bar, tf_crab_field, "south")
    area.exit(tf_crab_field, tf_sand_bar, "north")
    area.exit(tf_crab_field, tf_rock_arch, "east")
    area.exit(tf_rock_arch, tf_crab_field, "west")
    area.exit(tf_crab_field, tf_flotsam_beach, "south")
    area.exit(tf_flotsam_beach, tf_crab_field, "north")
    area.exit(tf_flotsam_beach, tf_mudflat, "south")
    area.exit(tf_mudflat, tf_flotsam_beach, "north")
    area.exit(tf_upper_beach, tf_shell_midden, "west")
    area.exit(tf_shell_midden, tf_upper_beach, "east")
    area.exit(tf_tide_pool_2, tf_wave_cut_platform, "south")
    area.exit(tf_wave_cut_platform, tf_tide_pool_2, "north")
    area.exit(tf_wave_cut_platform, tf_sea_glass_cove, "east")
    area.exit(tf_sea_glass_cove, tf_wave_cut_platform, "west")
    area.exit(tf_kelp_strand, tf_reef_edge, "south")
    area.exit(tf_reef_edge, tf_kelp_strand, "north")
    area.exit(tf_mudflat, tf_stranded_boat, "east")
    area.exit(tf_stranded_boat, tf_mudflat, "west")

    # Connect tidal flats to cliff path
    area.exit(cn_descent_beach, tf_upper_beach, "south")
    area.exit(tf_upper_beach, cn_descent_beach, "north")

    # ==================================================================
    #  SUB-AREA 5: SEA CAVES (~16 rooms)
    #  Underground coastal caverns. Salt lurker territory.
    # ==================================================================

    sc_entrance = area.room(
        "sc_entrance",
        name="Sea Cave - Entrance",
        desc=(
            "The cave mouth is a wide arch of dark stone, draped with "
            "curtains of kelp and crusted with barnacles up to the high "
            "tide mark. Inside, the air is cool, damp, and echoing. "
            "The floor is wet rock, slippery with algae. Daylight "
            "penetrates perhaps twenty feet before the darkness takes over. "
            "The sound of the sea reverberates from deeper within."
        ),
        room_type="cave",
        indoor=True,
    )

    sc_tidal_channel = area.room(
        "sc_tidal_channel",
        name="Sea Cave - Tidal Channel",
        desc=(
            "A narrow channel of seawater runs through the cave floor, "
            "connecting to the sea outside. At high tide this passage "
            "floods entirely. The walls are smooth, carved by centuries "
            "of water flow. Bioluminescent organisms in the water cast "
            "a faint blue-green glow -- enough to see shapes, not details."
        ),
        room_type="cave",
        indoor=True,
        ambient_echoes=[
            "Water gurgles through the tidal channel with a sound like breathing.",
            "A faint blue glow pulses in the water -- bioluminescence.",
        ],
    )

    sc_grotto = area.room(
        "sc_grotto",
        name="Sea Cave - Crystal Grotto",
        desc=(
            "The cave opens into a natural grotto where salt crystals have "
            "grown across the ceiling in thick clusters. They catch and "
            "scatter the bioluminescent glow from below, creating a "
            "shifting constellation of blue-green points. The effect is "
            "beautiful and disorienting. A pool of still water occupies "
            "the center, its surface mirror-perfect."
        ),
        room_type="cave",
        indoor=True,
    )

    sc_salt_formation = area.room(
        "sc_salt_formation",
        name="Sea Cave - Salt Formations",
        desc=(
            "Pillars of crystallized salt grow from floor to ceiling, "
            "formed over millennia by evaporating seawater. Some are "
            "translucent, revealing trapped air bubbles and tiny sea "
            "creatures preserved in mineral. The formations creak and "
            "groan as they shift -- infinitesimally slowly, but audible "
            "in the silence of the cave."
        ),
        room_type="cave",
        indoor=True,
        ambient_echoes=[
            "A salt pillar groans almost imperceptibly, shifting under its own weight.",
            "Your footstep echoes back from six different directions.",
        ],
    )

    sc_pool_chamber = area.room(
        "sc_pool_chamber",
        name="Sea Cave - Submerged Pool",
        desc=(
            "A large chamber partially flooded with dark, still water. "
            "The pool is of unknown depth -- dropped stones vanish without "
            "a splash. Wet rock shelves provide precarious footing around "
            "the edges. Something occasionally disturbs the surface from "
            "below -- concentric ripples expanding outward from no visible "
            "source."
        ),
        room_type="cave",
        indoor=True,
    )

    sc_narrow_squeeze = area.room(
        "sc_narrow_squeeze",
        name="Sea Cave - Narrow Squeeze",
        desc=(
            "The passage contracts to a gap barely wide enough to crawl "
            "through. The rock is wet, cold, and uncomfortably close. "
            "Beyond the squeeze, the air changes -- drier, with a mineral "
            "sharpness that stings the nostrils. Whatever is on the other "
            "side is above the tideline."
        ),
        room_type="cave",
        indoor=True,
    )

    sc_air_pocket = area.room(
        "sc_air_pocket",
        name="Sea Cave - Air Pocket Chamber",
        desc=(
            "A dome-shaped chamber above the waterline, sealed by the "
            "sea on all sides except the passage you entered through. "
            "The air is stale but breathable. The walls are covered in "
            "a slick orange growth -- some kind of cave lichen that "
            "produces a faint glow. Bones are scattered on the floor -- "
            "fish, mostly, but not exclusively."
        ),
        room_type="cave",
        indoor=True,
    )

    sc_brine_pool = area.room(
        "sc_brine_pool",
        name="Sea Cave - Brine Pool",
        desc=(
            "A perfectly circular pool of hyper-concentrated brine sits "
            "in the cave floor like a dark mirror. The brine is so dense "
            "that objects float on its surface. Salt deposits ring the "
            "pool in concentric circles of white and amber. The air "
            "above the pool shimmers with evaporation."
        ),
        room_type="cave",
        indoor=True,
    )

    sc_stalactite_gallery = area.room(
        "sc_stalactite_gallery",
        name="Sea Cave - Stalactite Gallery",
        desc=(
            "Hundreds of stalactites hang from the ceiling like stone "
            "teeth in a vast mouth. Water drips from their tips in a "
            "constant percussion -- each drop a different note, creating "
            "an accidental music that never repeats. The floor is covered "
            "in corresponding stalagmites, some of which have joined "
            "their ceiling counterparts to form columns."
        ),
        room_type="cave",
        indoor=True,
        ambient_echoes=[
            "Water drips from a hundred stalactites, each drop a different pitch.",
            "The cave breathes -- air moves in and out with the tide.",
        ],
    )

    sc_fossil_wall = area.room(
        "sc_fossil_wall",
        name="Sea Cave - Fossil Wall",
        desc=(
            "An entire wall of the cave is embedded with fossils -- shells, "
            "fronds, and the coiled forms of creatures that swam before "
            "memory. Some of the fossils are enormous, suggesting animals "
            "far larger than anything in current seas. A few have been "
            "carefully chipped free, leaving clean rectangular holes. "
            "Someone was here before you, and they were interested in "
            "the same things."
        ),
        room_type="cave",
        indoor=True,
    )

    sc_echo_chamber = area.room(
        "sc_echo_chamber",
        name="Sea Cave - Echo Chamber",
        desc=(
            "A roughly spherical chamber where sound behaves strangely. "
            "Whispers carry across the full width. A shout returns as "
            "multiple overlapping echoes, each slightly different in "
            "pitch. The acoustic effect is naturally occurring but "
            "feels designed. Standing in the center, you can hear "
            "the sea, the dripping water, and something else -- "
            "a low, rhythmic pulse that might be your own heartbeat."
        ),
        room_type="cave",
        indoor=True,
    )

    sc_coral_chamber = area.room(
        "sc_coral_chamber",
        name="Sea Cave - Coral Chamber",
        desc=(
            "The walls of this chamber are encrusted with dead coral -- "
            "ancient, calcite-hard formations that grew when these caves "
            "were submerged. The coral is beautiful in a skeletal way: "
            "branching, fractal patterns preserved in stone. Living coral "
            "still grows near the waterline, adding color to the grey."
        ),
        room_type="cave",
        indoor=True,
    )

    sc_deep_pool = area.room(
        "sc_deep_pool",
        name="Sea Cave - The Deep Pool",
        desc=(
            "The deepest chamber of the sea caves. A vast, lightless pool "
            "fills most of the floor space. The water is black and still "
            "and very, very cold. The ceiling is lost in darkness above. "
            "Locals claim something lives in the deep pool -- something "
            "large enough to make the water surge when it moves. They "
            "are not wrong."
        ),
        room_type="cave",
        indoor=True,
        ambient_echoes=[
            "Something large shifts in the water. The surface ripples.",
            "A cold current of air rises from the pool, carrying a salt-and-metal smell.",
            "Silence -- then a sound like breathing from the depths.",
        ],
    )

    sc_smuggler_cache = area.room(
        "sc_smuggler_cache",
        name="Sea Cave - Hidden Cache",
        desc=(
            "A small side chamber concealed behind a natural rock curtain. "
            "Someone has been using this space to store contraband -- "
            "waterproof crates are stacked against the walls, marked "
            "with coded symbols. A lantern hook has been driven into the "
            "stone. The floor is scuffed by boot prints. This cache is "
            "actively maintained."
        ),
        room_type="cave",
        indoor=True,
    )

    sc_seaweed_tunnel = area.room(
        "sc_seaweed_tunnel",
        name="Sea Cave - Seaweed Tunnel",
        desc=(
            "Long strands of dark seaweed hang from the ceiling like "
            "curtains, trailing into the shallow water that covers the "
            "floor. Pushing through them is like wading through hair. "
            "The weed conceals the passage ahead -- anything could be "
            "waiting on the other side."
        ),
        room_type="cave",
        indoor=True,
    )

    sc_shell_graveyard = area.room(
        "sc_shell_graveyard",
        name="Sea Cave - Shell Graveyard",
        desc=(
            "The floor of this chamber is covered in shells -- thousands "
            "of them, heaped in mounds. The shells are from enormous "
            "mollusks, each one large enough to use as a bowl. Whatever "
            "creature consumed them left nothing but the casings, cracked "
            "and discarded in piles. Some of the shells show tooth marks "
            "too large for any known animal."
        ),
        room_type="cave",
        indoor=True,
    )

    # Sea Cave exits
    area.exit(tf_rock_arch, sc_entrance, "east")
    area.exit(sc_entrance, tf_rock_arch, "west")
    area.exit(cn_tidal_cave_entrance, sc_entrance, "down")
    area.exit(sc_entrance, cn_tidal_cave_entrance, "up")
    area.exit(sc_entrance, sc_tidal_channel, "east")
    area.exit(sc_tidal_channel, sc_entrance, "west")
    area.exit(sc_tidal_channel, sc_grotto, "north")
    area.exit(sc_grotto, sc_tidal_channel, "south")
    area.exit(sc_grotto, sc_salt_formation, "east")
    area.exit(sc_salt_formation, sc_grotto, "west")
    area.exit(sc_tidal_channel, sc_pool_chamber, "south")
    area.exit(sc_pool_chamber, sc_tidal_channel, "north")
    area.exit(sc_pool_chamber, sc_narrow_squeeze, "east")
    area.exit(sc_narrow_squeeze, sc_pool_chamber, "west")
    area.exit(sc_narrow_squeeze, sc_air_pocket, "east")
    area.exit(sc_air_pocket, sc_narrow_squeeze, "west")
    area.exit(sc_salt_formation, sc_brine_pool, "north")
    area.exit(sc_brine_pool, sc_salt_formation, "south")
    area.exit(sc_salt_formation, sc_stalactite_gallery, "east")
    area.exit(sc_stalactite_gallery, sc_salt_formation, "west")
    area.exit(sc_stalactite_gallery, sc_fossil_wall, "north")
    area.exit(sc_fossil_wall, sc_stalactite_gallery, "south")
    area.exit(sc_stalactite_gallery, sc_echo_chamber, "east")
    area.exit(sc_echo_chamber, sc_stalactite_gallery, "west")
    area.exit(sc_echo_chamber, sc_coral_chamber, "south")
    area.exit(sc_coral_chamber, sc_echo_chamber, "north")
    area.exit(sc_coral_chamber, sc_deep_pool, "east")
    area.exit(sc_deep_pool, sc_coral_chamber, "west")
    area.exit(sc_pool_chamber, sc_smuggler_cache, "south")
    area.exit(sc_smuggler_cache, sc_pool_chamber, "north")
    area.exit(sc_air_pocket, sc_seaweed_tunnel, "south")
    area.exit(sc_seaweed_tunnel, sc_air_pocket, "north")
    area.exit(sc_seaweed_tunnel, sc_shell_graveyard, "south")
    area.exit(sc_shell_graveyard, sc_seaweed_tunnel, "north")
    area.exit(sc_shell_graveyard, sc_deep_pool, "east")
    area.exit(sc_deep_pool, sc_shell_graveyard, "west")

    # ==================================================================
    #  SUB-AREA 6: SMUGGLER'S COVE (~10 rooms)
    #  Hidden criminal hideout. Coastal raider territory.
    # ==================================================================

    sm_hidden_trail = area.room(
        "sm_hidden_trail",
        name="Hidden Coastal Trail",
        desc=(
            "A barely visible trail branches from the cliff path, concealed "
            "by scrub brush and deliberately placed stones. Following it "
            "leads down a steep, switchback descent through a crack in the "
            "cliff face. The trail shows signs of regular use -- the stones "
            "are worn smooth -- but someone has gone to considerable effort "
            "to make it invisible from the main path."
        ),
        room_type="path",
        indoor=False,
    )

    sm_lookout_rock = area.room(
        "sm_lookout_rock",
        name="Smuggler's Lookout",
        desc=(
            "A flat rock overlooking the approach to the cove. Someone "
            "stationed here can see anyone coming from either direction "
            "while remaining invisible from below. A crude shelter of "
            "driftwood and oilcloth provides protection from rain. Discarded "
            "food wrappers and a jug of stale water suggest someone was "
            "here recently."
        ),
        room_type="clearing",
        indoor=False,
    )

    sm_cove_entrance = area.room(
        "sm_cove_entrance",
        name="Smuggler's Cove - Entrance",
        desc=(
            "The trail ends at a narrow beach hemmed in by towering cliffs "
            "on three sides. The cove is nearly invisible from the sea -- "
            "the cliff walls create a natural screen. A boat ramp of "
            "placed stones leads into the water. Crates and barrels are "
            "stacked under an overhang, covered with tarps."
        ),
        room_type="clearing",
        indoor=False,
    )

    sm_warehouse = area.room(
        "sm_warehouse",
        name="Smuggler's Warehouse",
        desc=(
            "A natural cave expanded with crude stonework to create a "
            "rough warehouse. Shelves line the walls, stacked with goods "
            "that bear no customs stamps: wine, weapons, alchemical "
            "ingredients, and sealed boxes whose contents are best not "
            "discussed. A ledger on a makeshift desk tracks inventory "
            "in coded shorthand."
        ),
        room_type="cave",
        indoor=True,
    )

    sm_mess_area = area.room(
        "sm_mess_area",
        name="Smuggler's Mess",
        desc=(
            "A cave chamber fitted out as a communal eating area. A "
            "rough table of salvaged ship planks seats a dozen. The "
            "remains of a meal -- fish stew, hardtack, a half-empty rum "
            "bottle -- sit on the table. Playing cards are scattered "
            "across one end. The smugglers eat well when they eat at all."
        ),
        room_type="cave",
        indoor=True,
    )

    sm_sleeping_quarters = area.room(
        "sm_sleeping_quarters",
        name="Smuggler's Quarters",
        desc=(
            "Hammocks strung between iron hooks driven into the cave walls. "
            "Personal effects hang from pegs -- sea bags, weatherproofed "
            "coats, a battered fiddle. The hammocks are clean, the floor "
            "swept. These smugglers take some pride in their living space, "
            "or at least their captain demands it."
        ),
        room_type="cave",
        indoor=True,
    )

    sm_captain_cabin = area.room(
        "sm_captain_cabin",
        name="Captain's Cabin",
        desc=(
            "A private chamber separated from the rest by a heavy curtain. "
            "A proper bed frame salvaged from a ship, a desk with charts "
            "and navigational instruments, and a locked strongbox. The "
            "walls are hung with maps of the coastline -- some marked "
            "with routes and timing notations that correspond to Imperial "
            "patrol schedules."
        ),
        room_type="cave",
        indoor=True,
    )

    sm_dock = area.room(
        "sm_dock",
        name="Hidden Dock",
        desc=(
            "A wooden dock built into a cave that opens directly to the "
            "sea. The dock is large enough for a single shallow-draft "
            "vessel. Rope, anchor chain, and barrels of pitch are stored "
            "along the walls. The cave mouth faces east, invisible from "
            "the harbor -- a smuggler's dream anchorage."
        ),
        room_type="building",
        indoor=True,
    )

    sm_weapons_cache = area.room(
        "sm_weapons_cache",
        name="Weapons Cache",
        desc=(
            "A small chamber stacked with weapons -- cutlasses, crossbows, "
            "boarding pikes, and a few barrels of black powder stored "
            "with dangerous casualness. The weapons are of mixed quality: "
            "some Imperial surplus, some foreign make, all functional. "
            "Enough to arm thirty."
        ),
        room_type="cave",
        indoor=True,
    )

    sm_escape_tunnel = area.room(
        "sm_escape_tunnel",
        name="Escape Tunnel",
        desc=(
            "A narrow, hand-dug tunnel angling upward through the cliff. "
            "Timber shoring keeps the worst of the collapses at bay. The "
            "tunnel connects the smuggler's cove to the cliff path above -- "
            "an escape route for when the Imperial navy comes knocking. "
            "The exit is concealed behind a loose boulder."
        ),
        room_type="cave",
        indoor=True,
    )

    # Smuggler's Cove exits
    area.exit(hr_bridge, sm_hidden_trail, "south")
    area.exit(sm_hidden_trail, hr_bridge, "north")
    area.exit(sm_hidden_trail, sm_lookout_rock, "south")
    area.exit(sm_lookout_rock, sm_hidden_trail, "north")
    area.exit(sm_lookout_rock, sm_cove_entrance, "south")
    area.exit(sm_cove_entrance, sm_lookout_rock, "north")
    area.exit(sm_cove_entrance, sm_warehouse, "east")
    area.exit(sm_warehouse, sm_cove_entrance, "west")
    area.exit(sm_cove_entrance, sm_mess_area, "south")
    area.exit(sm_mess_area, sm_cove_entrance, "north")
    area.exit(sm_mess_area, sm_sleeping_quarters, "east")
    area.exit(sm_sleeping_quarters, sm_mess_area, "west")
    area.exit(sm_sleeping_quarters, sm_captain_cabin, "south")
    area.exit(sm_captain_cabin, sm_sleeping_quarters, "north")
    area.exit(sm_cove_entrance, sm_dock, "west")
    area.exit(sm_dock, sm_cove_entrance, "east")
    area.exit(sm_warehouse, sm_weapons_cache, "east")
    area.exit(sm_weapons_cache, sm_warehouse, "west")
    area.exit(sm_escape_tunnel, sm_sleeping_quarters, "south")
    area.exit(sm_sleeping_quarters, sm_escape_tunnel, "north")
    # Connect escape tunnel to cliff path
    area.exit(sm_escape_tunnel, cn_rockfall, "up")
    area.exit(cn_rockfall, sm_escape_tunnel, "down")

    # ==================================================================
    #  SUB-AREA 7: LIGHTHOUSE POINT (~8 rooms)
    #  Watchtower landmark area. Spectacular views.
    # ==================================================================

    lh_approach = area.room(
        "lh_approach",
        name="Lighthouse Path - Approach",
        desc=(
            "A maintained stone path leads west along a narrow promontory "
            "toward the lighthouse. The path is bordered by low stone "
            "walls, built more to prevent accidental falls than deliberate "
            "ones. Wind-blasted grass grows in the cracks. Ahead, the "
            "lighthouse rises against the grey sky -- a tapering column "
            "of dark stone with a glass-enclosed lantern room at the top."
        ),
        room_type="path",
        indoor=False,
    )

    lh_garden = area.room(
        "lh_garden",
        name="Lighthouse Keeper's Garden",
        desc=(
            "A small walled garden that somehow survives the constant "
            "salt wind. Hardy herbs -- thyme, rosemary, sea lavender -- "
            "grow in raised beds protected by stone windbreaks. The "
            "keeper tends this patch with obsessive care. It is the "
            "only green thing on the promontory."
        ),
        room_type="clearing",
        indoor=False,
    )

    lh_base = area.room(
        "lh_base",
        name="Stormhaven Lighthouse - Base",
        desc=(
            "The base of the lighthouse is a thick-walled circular room "
            "that serves as the keeper's quarters. A spiral staircase of "
            "iron winds upward through a central shaft. The walls are "
            "hung with nautical charts, tide tables, and pencil-marked "
            "calendars going back decades. A cat sleeps on a chair by "
            "the cold fireplace."
        ),
        room_type="building",
        indoor=True,
    )

    lh_mid_level = area.room(
        "lh_mid_level",
        name="Stormhaven Lighthouse - Storage Level",
        desc=(
            "The middle level of the lighthouse stores lamp oil, spare "
            "wicks, lenses, and tools. Everything is meticulously organized "
            "and labeled. The keeper's handwriting is precise and small. "
            "A window faces east, framing a view of the open sea that "
            "is either beautiful or terrifying depending on the weather."
        ),
        room_type="building",
        indoor=True,
    )

    lh_lantern_room = area.room(
        "lh_lantern_room",
        name="Stormhaven Lighthouse - Lantern Room",
        desc=(
            "The summit of the lighthouse. A massive Fresnel lens of "
            "polished crystal occupies the center, surrounded by a "
            "walkway and glass walls. The view is absolute: north, south, "
            "east, west -- nothing but sea, coast, and sky. The beacon "
            "has been dark for weeks. The keeper says the lens cracked "
            "during the last storm. He is lying."
        ),
        room_type="building",
        indoor=True,
        ambient_echoes=[
            "Wind whistles through a hairline crack in the glass enclosure.",
            "The view from here is dizzying -- sea in every direction.",
        ],
    )

    lh_cliff_edge = area.room(
        "lh_cliff_edge",
        name="Lighthouse Point - Cliff Edge",
        desc=(
            "The westernmost tip of the promontory. Beyond the low stone "
            "wall there is nothing but a vertical drop to the sea. Waves "
            "crash against the base of the cliff with enough force to "
            "send spray up past the edge. On clear days, you can see "
            "the mainland coast stretching south toward the Ashreach "
            "plains. This is where the land ends."
        ),
        room_type="clearing",
        indoor=False,
    )

    lh_tide_stairs = area.room(
        "lh_tide_stairs",
        name="Lighthouse Point - Tide Stairs",
        desc=(
            "Stone stairs carved into the cliff face, descending from "
            "the lighthouse promontory to a tiny landing at the waterline. "
            "The stairs are ancient, their edges rounded by centuries of "
            "use. At the bottom, a mooring ring is set into the rock -- "
            "a remnant of when the lighthouse was resupplied by sea."
        ),
        room_type="path",
        indoor=False,
    )

    lh_signal_platform = area.room(
        "lh_signal_platform",
        name="Signal Platform",
        desc=(
            "A flat stone platform on the seaward side of the lighthouse "
            "where signal fires were once lit to warn ships. The fire "
            "pit is cold and filled with ash from the last burning. "
            "Iron brackets once held a signal brazier but it has been "
            "removed -- or stolen. Someone left a spyglass here, "
            "battered but functional."
        ),
        room_type="clearing",
        indoor=False,
    )

    # Lighthouse exits
    area.exit(cn_headland, lh_approach, "west")
    area.exit(lh_approach, cn_headland, "east")
    area.exit(lh_approach, lh_garden, "south")
    area.exit(lh_garden, lh_approach, "north")
    area.exit(lh_approach, lh_base, "west")
    area.exit(lh_base, lh_approach, "east")
    area.exit(lh_base, lh_mid_level, "up")
    area.exit(lh_mid_level, lh_base, "down")
    area.exit(lh_mid_level, lh_lantern_room, "up")
    area.exit(lh_lantern_room, lh_mid_level, "down")
    area.exit(lh_base, lh_cliff_edge, "west")
    area.exit(lh_cliff_edge, lh_base, "east")
    area.exit(lh_cliff_edge, lh_tide_stairs, "down")
    area.exit(lh_tide_stairs, lh_cliff_edge, "up")
    area.exit(lh_approach, lh_signal_platform, "north")
    area.exit(lh_signal_platform, lh_approach, "south")

    # ==================================================================
    #  SUB-AREA 8: WRECK OF THE SEASPRAY (~8 rooms)
    #  Shipwreck ruins on the southern rocks.
    # ==================================================================

    wr_approach = area.room(
        "wr_approach",
        name="Wreck Approach - Rocky Shore",
        desc=(
            "The shore here is all jagged rock, no sand. Dark stone "
            "juts from the water at angles that explain why ships avoid "
            "this stretch. Ahead, the wreck of a large vessel sits "
            "impaled on a reef -- its hull broken amidships, masts "
            "snapped, rigging trailing in the current like kelp. The "
            "name Seaspray is still visible on the stern in faded gold."
        ),
        room_type="path",
        indoor=False,
    )

    wr_main_deck = area.room(
        "wr_main_deck",
        name="Wreck of the Seaspray - Main Deck",
        desc=(
            "The main deck of the Seaspray tilts at a permanent fifteen "
            "degrees, wedged on the reef that killed it. Planks are "
            "warped and green with algae. The masts are stumps, broken "
            "off by the storm that drove it onto the rocks. Personal "
            "belongings are scattered across the deck -- a boot, a "
            "shattered lantern, a waterlogged book. The ship has been "
            "dead for perhaps a year."
        ),
        room_type="ruins",
        indoor=False,
    )

    wr_forecastle = area.room(
        "wr_forecastle",
        name="Wreck of the Seaspray - Forecastle",
        desc=(
            "The bow section of the ship, raised above the main deck. "
            "The bowsprit is snapped short. A figurehead -- a woman with "
            "kelp for hair -- stares blindly at the horizon. The "
            "anchor chain trails overboard into the water. Up here the "
            "tilt is worst; everything slides toward the starboard rail."
        ),
        room_type="ruins",
        indoor=False,
    )

    wr_captain_quarters = area.room(
        "wr_captain_quarters",
        name="Wreck of the Seaspray - Captain's Quarters",
        desc=(
            "The stern cabin, largely intact though waterlogged. A desk "
            "is bolted to the floor at an angle. Charts and logs have "
            "fused into a papier-mache mass. A locked chest sits in the "
            "corner, too heavy to move easily. The captain's coat still "
            "hangs from a peg, salt-stiffened into a standing shape."
        ),
        room_type="ruins",
        indoor=True,
    )

    wr_cargo_hold = area.room(
        "wr_cargo_hold",
        name="Wreck of the Seaspray - Cargo Hold",
        desc=(
            "Below the main deck, the cargo hold is knee-deep in dark "
            "water. Crates and barrels float or sit half-submerged, "
            "their contents ruined by the sea. The hull breach that "
            "sank the ship is visible on the port side -- a ragged hole "
            "punched by the reef. Something moves in the water between "
            "the crates."
        ),
        room_type="ruins",
        indoor=True,
    )

    wr_crew_quarters = area.room(
        "wr_crew_quarters",
        name="Wreck of the Seaspray - Crew Quarters",
        desc=(
            "Narrow bunks stacked three high, most of them collapsed. "
            "Seawater has turned everything to rot and rust. Personal "
            "items float in the ankle-deep water: a tin mirror, a "
            "carved wooden figure, a letter sealed in wax that the "
            "sea could not destroy. The crew escaped -- their bodies "
            "are not here."
        ),
        room_type="ruins",
        indoor=True,
    )

    wr_reef_base = area.room(
        "wr_reef_base",
        name="Reef Base",
        desc=(
            "The reef that killed the Seaspray. At low tide, its jagged "
            "spine rises from the water like a row of dark teeth. The "
            "hull of the ship is pinned across it, creaking with every "
            "wave. Below the waterline, the reef is alive with marine "
            "life that has colonized the wreck. Anemones bloom along "
            "the hull breach."
        ),
        room_type="clearing",
        indoor=False,
    )

    wr_stern_platform = area.room(
        "wr_stern_platform",
        name="Stern Platform",
        desc=(
            "The stern of the Seaspray, partially collapsed but still "
            "accessible. The rudder hangs loose, swinging with the waves. "
            "From here you can see the full extent of the damage -- the "
            "ship is bent across the reef like a broken back. The sea "
            "is slowly taking it apart, plank by plank."
        ),
        room_type="ruins",
        indoor=False,
    )

    # Wreck exits
    area.exit(tf_flotsam_beach, wr_approach, "east")
    area.exit(wr_approach, tf_flotsam_beach, "west")
    area.exit(wr_approach, wr_main_deck, "east")
    area.exit(wr_main_deck, wr_approach, "west")
    area.exit(wr_main_deck, wr_forecastle, "north")
    area.exit(wr_forecastle, wr_main_deck, "south")
    area.exit(wr_main_deck, wr_captain_quarters, "south")
    area.exit(wr_captain_quarters, wr_main_deck, "north")
    area.exit(wr_main_deck, wr_cargo_hold, "down")
    area.exit(wr_cargo_hold, wr_main_deck, "up")
    area.exit(wr_cargo_hold, wr_crew_quarters, "south")
    area.exit(wr_crew_quarters, wr_cargo_hold, "north")
    area.exit(wr_approach, wr_reef_base, "south")
    area.exit(wr_reef_base, wr_approach, "north")
    area.exit(wr_captain_quarters, wr_stern_platform, "south")
    area.exit(wr_stern_platform, wr_captain_quarters, "north")

    # ==================================================================
    #  SUB-AREA 9: CLIFF PATH SOUTH (~14 rooms)
    #  Southern coastal cliffs. Mixed mob territory.
    # ==================================================================

    cs_south_trailhead = area.room(
        "cs_south_trailhead",
        name="Cliff Path - Southern Trailhead",
        desc=(
            "The coastal path branches south from the tidal flats, "
            "climbing steeply onto the clifftops. The vegetation here is "
            "thicker -- gorse and sea buckthorn forming dense barriers "
            "that have been hacked back to keep the path passable. "
            "The trail is well-worn by fishermen and the occasional "
            "Imperial patrol."
        ),
        room_type="path",
        indoor=False,
    )

    cs_gorse_tunnel = area.room(
        "cs_gorse_tunnel",
        name="Cliff Path - Gorse Tunnel",
        desc=(
            "The gorse bushes have grown over the path to form a natural "
            "tunnel. Yellow flowers bloom in season, filling the enclosed "
            "space with a coconut scent. Out of season, the thorny "
            "branches scrape at anyone who passes. The tunnel is dark "
            "enough to require care."
        ),
        room_type="path",
        indoor=False,
    )

    cs_sea_view = area.room(
        "cs_sea_view",
        name="Cliff Path - Sea View",
        desc=(
            "The path emerges from the gorse onto an exposed clifftop "
            "with an unobstructed view of the sea. The water below is "
            "deep and dark blue, streaked with the white lines of "
            "breaking waves. On the horizon, the dark shapes of distant "
            "islands are sometimes visible in clear weather."
        ),
        room_type="path",
        indoor=False,
    )

    cs_eroded_bluff = area.room(
        "cs_eroded_bluff",
        name="Cliff Path - Eroded Bluff",
        desc=(
            "Recent erosion has eaten away the cliff edge here, leaving "
            "the path uncomfortably close to a crumbling drop. Fence "
            "posts lean at angles where the ground shifted beneath them. "
            "The soil is sandy and unstable. Locals avoid this stretch "
            "after rain."
        ),
        room_type="path",
        indoor=False,
    )

    cs_nesting_colony = area.room(
        "cs_nesting_colony",
        name="Cliff Path - Nesting Colony",
        desc=(
            "The cliffs here host a colony of seabirds that nest in "
            "burrows dug into the soft soil. The ground is riddled with "
            "holes -- step carefully or risk a twisted ankle. The birds "
            "are noisy and unafraid, waddling across the path with "
            "the entitlement of residents."
        ),
        room_type="clearing",
        indoor=False,
    )

    cs_wave_watcher = area.room(
        "cs_wave_watcher",
        name="Wave Watcher's Seat",
        desc=(
            "A natural stone seat on the cliff edge, shaped by wind and "
            "perhaps by deliberate chipping. The view is mesmerizing -- "
            "wave after wave rolling in from the open sea, breaking "
            "against the rocks in patterns that never quite repeat. "
            "Someone carved a date into the stone: a year that predates "
            "the Empire by centuries."
        ),
        room_type="clearing",
        indoor=False,
    )

    cs_cave_mouth = area.room(
        "cs_cave_mouth",
        name="Cliff Path - Southern Cave Mouth",
        desc=(
            "A cave entrance in the southern cliffs, smaller than the "
            "northern sea caves but still large enough to enter. Cool "
            "air flows outward, carrying a mineral smell. The entrance "
            "is partially concealed by hanging vegetation. Animal tracks "
            "-- or something like animal tracks -- lead inside."
        ),
        room_type="path",
        indoor=False,
    )

    cs_south_cave_1 = area.room(
        "cs_south_cave_1",
        name="Southern Cave - Entrance Chamber",
        desc=(
            "A low-ceilinged chamber just inside the cave mouth. The "
            "walls are damp and streaked with mineral deposits in "
            "rust and green. A shallow pool fills one corner, fed by "
            "seepage from the cliff above. The air is cool and still "
            "after the constant wind outside."
        ),
        room_type="cave",
        indoor=True,
    )

    cs_south_cave_2 = area.room(
        "cs_south_cave_2",
        name="Southern Cave - Salt Lurker Den",
        desc=(
            "A deeper chamber where the ceiling rises and the floor "
            "drops away into darkness. Thick deposits of salt coat every "
            "surface in crystalline layers. Tracks in the salt show "
            "where something large and heavy has dragged itself through "
            "the chamber. A brackish smell fills the air."
        ),
        room_type="cave",
        indoor=True,
        ambient_echoes=[
            "Something scrapes across salt-crusted stone in the darkness ahead.",
            "A wet, heavy breathing echoes through the chamber.",
        ],
    )

    cs_cliff_face = area.room(
        "cs_cliff_face",
        name="Cliff Path - Face Traverse",
        desc=(
            "The path narrows to a ledge carved into the vertical cliff "
            "face. Iron handholds, green with corrosion, have been "
            "hammered into the rock at intervals. The traverse is "
            "perhaps fifty feet long and entirely exposed. The sea "
            "churns far below."
        ),
        room_type="path",
        indoor=False,
    )

    cs_driftwood_shelter = area.room(
        "cs_driftwood_shelter",
        name="Driftwood Shelter",
        desc=(
            "Someone has built a rough lean-to from driftwood and "
            "salvaged sailcloth at the base of the cliff. A fire ring "
            "of stones, a pile of dried seaweed for bedding, and "
            "a collection of shells arranged in a pattern suggest this "
            "is home to someone -- but they are not here now."
        ),
        room_type="clearing",
        indoor=False,
    )

    cs_tide_race = area.room(
        "cs_tide_race",
        name="Cliff Path - Tide Race",
        desc=(
            "The path overlooks a narrow channel between the mainland "
            "and an offshore rock stack. At tide change, water rushes "
            "through this gap with violent force -- the sound is like "
            "a river in flood. At slack tide, the channel is deceptively "
            "calm. Fishermen time their crossings carefully."
        ),
        room_type="path",
        indoor=False,
    )

    cs_south_junction = area.room(
        "cs_south_junction",
        name="Southern Coast Junction",
        desc=(
            "The coastal path meets a wider trail heading south inland. "
            "A weathered signpost, barely legible, points south toward "
            "the plains. The ground transitions from salt-crusted rock "
            "to dusty earth. The coastal wind dies here, blocked by "
            "the rising terrain. This is where the coast ends and the "
            "interior begins."
        ),
        room_type="path",
        indoor=False,
    )

    # Cliff Path South exits
    area.exit(tf_mudflat, cs_south_trailhead, "south")
    area.exit(cs_south_trailhead, tf_mudflat, "north")
    area.exit(cs_south_trailhead, cs_gorse_tunnel, "south")
    area.exit(cs_gorse_tunnel, cs_south_trailhead, "north")
    area.exit(cs_gorse_tunnel, cs_sea_view, "south")
    area.exit(cs_sea_view, cs_gorse_tunnel, "north")
    area.exit(cs_sea_view, cs_eroded_bluff, "east")
    area.exit(cs_eroded_bluff, cs_sea_view, "west")
    area.exit(cs_sea_view, cs_nesting_colony, "south")
    area.exit(cs_nesting_colony, cs_sea_view, "north")
    area.exit(cs_nesting_colony, cs_wave_watcher, "east")
    area.exit(cs_wave_watcher, cs_nesting_colony, "west")
    area.exit(cs_nesting_colony, cs_cave_mouth, "south")
    area.exit(cs_cave_mouth, cs_nesting_colony, "north")
    area.exit(cs_cave_mouth, cs_south_cave_1, "in")
    area.exit(cs_south_cave_1, cs_cave_mouth, "out")
    area.exit(cs_south_cave_1, cs_south_cave_2, "south")
    area.exit(cs_south_cave_2, cs_south_cave_1, "north")
    area.exit(cs_cave_mouth, cs_cliff_face, "south")
    area.exit(cs_cliff_face, cs_cave_mouth, "north")
    area.exit(cs_cliff_face, cs_driftwood_shelter, "south")
    area.exit(cs_driftwood_shelter, cs_cliff_face, "north")
    area.exit(cs_driftwood_shelter, cs_tide_race, "east")
    area.exit(cs_tide_race, cs_driftwood_shelter, "west")
    area.exit(cs_cliff_face, cs_south_junction, "south")
    area.exit(cs_south_junction, cs_cliff_face, "north")

    # Cross-zone exit: south to plains zone
    area.exit(cs_south_junction, "ashreach_expanse:ae_north_trail", "south")

    # ==================================================================
    #  SUB-AREA 10: STORM BLUFFS (~6 rooms)
    #  High windswept overlook area. Scenic.
    # ==================================================================

    sb_trail = area.room(
        "sb_trail",
        name="Storm Bluffs - Trail",
        desc=(
            "A steep trail climbs from the village toward the high bluffs "
            "above the coast. The path is carved into the hillside, "
            "switching back twice before reaching the top. Wind increases "
            "with each step. At the second switchback, someone has piled "
            "stones into a small cairn."
        ),
        room_type="path",
        indoor=False,
    )

    sb_summit = area.room(
        "sb_summit",
        name="Storm Bluffs - Summit",
        desc=(
            "The highest point on the Stormhaven coast. The wind up here "
            "is ferocious and unrelenting, strong enough to lean into "
            "without falling. The view encompasses the entire coastline: "
            "the village below, the lighthouse to the north, the wreck "
            "to the south, and the sea stretching east to infinity. "
            "During storms, this is where lightning strikes first."
        ),
        room_type="clearing",
        indoor=False,
        ambient_echoes=[
            "Wind howls across the bluff summit with primal force.",
            "You can see the entire coastline from up here.",
            "A gull fights the wind, hovering motionless in the air.",
        ],
    )

    sb_windswept_flat = area.room(
        "sb_windswept_flat",
        name="Storm Bluffs - Windswept Flat",
        desc=(
            "A flat expanse of bare rock at the top of the bluffs where "
            "nothing grows. The stone is scoured smooth by wind and "
            "weather. Shallow depressions in the rock fill with rainwater "
            "that evaporates within hours. The wind carves patterns in "
            "any dust that accumulates."
        ),
        room_type="clearing",
        indoor=False,
    )

    sb_ancient_stones = area.room(
        "sb_ancient_stones",
        name="Storm Bluffs - Standing Stones",
        desc=(
            "Three standing stones rise from the bluff, arranged in a "
            "triangle. They are old -- far older than Stormhaven or "
            "the Empire. The stones are unmarked, featureless, and "
            "made from a rock type not found anywhere on this coast. "
            "Someone brought them here, long ago, for reasons unknown. "
            "The wind sounds different between the stones."
        ),
        room_type="ruins",
        indoor=False,
    )

    sb_eagle_nest = area.room(
        "sb_eagle_nest",
        name="Storm Bluffs - Eagle's Nest",
        desc=(
            "A ledge below the bluff summit where a pair of sea eagles "
            "have built an enormous nest of sticks, driftwood, and "
            "kelp. The nest is the size of a wagon. The eagles tolerate "
            "quiet observers but react aggressively to sudden movement. "
            "Bones -- fish, rabbit, and larger -- litter the ledge."
        ),
        room_type="clearing",
        indoor=False,
    )

    sb_rain_shelter = area.room(
        "sb_rain_shelter",
        name="Storm Bluffs - Rain Shelter",
        desc=(
            "A natural overhang in the rock provides the only shelter "
            "from weather on the bluffs. The space is small -- room "
            "for three or four at most. Charcoal marks on the ceiling "
            "show it has been used for centuries. Someone scratched "
            "a crude map of the coastline on the back wall."
        ),
        room_type="cave",
        indoor=True,
    )

    # Storm Bluffs exits
    area.exit(sv_shrine, sb_trail, "north")
    area.exit(sb_trail, sv_shrine, "south")
    area.exit(sb_trail, sb_summit, "north")
    area.exit(sb_summit, sb_trail, "south")
    area.exit(sb_summit, sb_windswept_flat, "east")
    area.exit(sb_windswept_flat, sb_summit, "west")
    area.exit(sb_summit, sb_ancient_stones, "north")
    area.exit(sb_ancient_stones, sb_summit, "south")
    area.exit(sb_windswept_flat, sb_eagle_nest, "east")
    area.exit(sb_eagle_nest, sb_windswept_flat, "west")
    area.exit(sb_summit, sb_rain_shelter, "west")
    area.exit(sb_rain_shelter, sb_summit, "east")

    # ==================================================================
    #  MOB SPAWNS (D-19: moderate density, ~1-2 per 2 rooms)
    # ==================================================================

    # Shore crabs -- passive scavengers, wander beaches (D-27)
    area.spawn(tf_sand_bar, "shore_crab", count_min=1, count_max=2,
               respawn_minutes=8, respawn_variance=3)
    area.spawn(tf_crab_field, "shore_crab", count_min=2, count_max=3,
               respawn_minutes=8, respawn_variance=3)
    area.spawn(tf_kelp_strand, "shore_crab", count_min=1, count_max=2,
               respawn_minutes=10, respawn_variance=3)
    area.spawn(tf_reef_edge, "shore_crab", count_min=1, count_max=2,
               respawn_minutes=10, respawn_variance=3)
    area.spawn(tf_upper_beach, "shore_crab", count_min=0, count_max=1,
               respawn_minutes=10, respawn_variance=5)
    area.spawn(tf_tide_pool_2, "shore_crab", count_min=1, count_max=1,
               respawn_minutes=12, respawn_variance=3)
    area.spawn(tf_wave_cut_platform, "shore_crab", count_min=1, count_max=2,
               respawn_minutes=10, respawn_variance=3)
    area.spawn(tf_flotsam_beach, "shore_crab", count_min=0, count_max=1,
               respawn_minutes=12, respawn_variance=5)
    area.spawn(sv_beach_landing, "shore_crab", count_min=0, count_max=1,
               respawn_minutes=15, respawn_variance=5)

    # Sea serpents -- aggressive, rare, near deep water
    area.spawn(sc_deep_pool, "sea_serpent", count_min=1, count_max=1,
               respawn_minutes=30, respawn_variance=10)
    area.spawn(sc_pool_chamber, "sea_serpent", count_min=0, count_max=1,
               respawn_minutes=45, respawn_variance=15)
    area.spawn(tf_reef_edge, "sea_serpent", count_min=0, count_max=1,
               respawn_minutes=60, respawn_variance=20)

    # Coastal raiders -- cautious humanoids, smuggler areas
    area.spawn(sm_cove_entrance, "coastal_raider", count_min=1, count_max=2,
               respawn_minutes=15, respawn_variance=5,
               base_disposition=-0.3)
    area.spawn(sm_lookout_rock, "coastal_raider", count_min=1, count_max=1,
               respawn_minutes=15, respawn_variance=5,
               base_disposition=-0.3)
    area.spawn(sm_warehouse, "coastal_raider", count_min=1, count_max=1,
               respawn_minutes=15, respawn_variance=5,
               base_disposition=-0.3)
    area.spawn(sm_dock, "coastal_raider", count_min=1, count_max=2,
               respawn_minutes=15, respawn_variance=5,
               base_disposition=-0.3)
    area.spawn(sm_weapons_cache, "coastal_raider", count_min=1, count_max=1,
               respawn_minutes=20, respawn_variance=5,
               base_disposition=-0.4)
    area.spawn(cs_eroded_bluff, "coastal_raider", count_min=0, count_max=1,
               respawn_minutes=20, respawn_variance=10,
               base_disposition=-0.2)
    area.spawn(cs_driftwood_shelter, "coastal_raider", count_min=1, count_max=1,
               respawn_minutes=20, respawn_variance=5,
               base_disposition=-0.2)

    # Cliff harpies -- aggressive, clifftops (D-28: 1 is_hunter)
    area.spawn(cn_harpy_nests, "cliff_harpy", count_min=1, count_max=2,
               respawn_minutes=12, respawn_variance=4)
    area.spawn(cn_sea_stack_view, "cliff_harpy", count_min=1, count_max=1,
               respawn_minutes=15, respawn_variance=5)
    area.spawn(cn_gull_roost, "cliff_harpy", count_min=0, count_max=1,
               respawn_minutes=20, respawn_variance=5)
    area.spawn(sb_eagle_nest, "cliff_harpy", count_min=0, count_max=1,
               respawn_minutes=25, respawn_variance=10)
    area.spawn(cn_headland, "cliff_harpy", count_min=1, count_max=1,
               respawn_minutes=15, respawn_variance=5,
               is_hunter=True, detection_range=3)

    # Salt lurkers -- passive ambush, cave-dwelling
    area.spawn(sc_air_pocket, "salt_lurker", count_min=1, count_max=1,
               respawn_minutes=15, respawn_variance=5)
    area.spawn(sc_shell_graveyard, "salt_lurker", count_min=1, count_max=1,
               respawn_minutes=15, respawn_variance=5)
    area.spawn(sc_brine_pool, "salt_lurker", count_min=0, count_max=1,
               respawn_minutes=20, respawn_variance=5)
    area.spawn(cs_south_cave_2, "salt_lurker", count_min=1, count_max=1,
               respawn_minutes=15, respawn_variance=5)
    area.spawn(sc_seaweed_tunnel, "salt_lurker", count_min=0, count_max=1,
               respawn_minutes=20, respawn_variance=8)
    area.spawn(sc_stalactite_gallery, "salt_lurker", count_min=0, count_max=1,
               respawn_minutes=25, respawn_variance=10)

    # Additional spawns for density (mixed types)
    area.spawn(wr_cargo_hold, "shore_crab", count_min=1, count_max=2,
               respawn_minutes=10, respawn_variance=3)
    area.spawn(wr_reef_base, "shore_crab", count_min=1, count_max=2,
               respawn_minutes=10, respawn_variance=3)
    area.spawn(sc_coral_chamber, "sea_serpent", count_min=0, count_max=1,
               respawn_minutes=45, respawn_variance=15)
    area.spawn(hr_coastal_scrub, "shore_crab", count_min=0, count_max=1,
               respawn_minutes=15, respawn_variance=5)
    area.spawn(cs_tide_race, "cliff_harpy", count_min=0, count_max=1,
               respawn_minutes=20, respawn_variance=10)
    area.spawn(cn_wind_gap, "cliff_harpy", count_min=0, count_max=1,
               respawn_minutes=20, respawn_variance=10)
    area.spawn(sc_echo_chamber, "salt_lurker", count_min=0, count_max=1,
               respawn_minutes=25, respawn_variance=10)
    area.spawn(sm_mess_area, "coastal_raider", count_min=0, count_max=1,
               respawn_minutes=15, respawn_variance=5,
               base_disposition=-0.2)
    area.spawn(wr_main_deck, "coastal_raider", count_min=0, count_max=1,
               respawn_minutes=30, respawn_variance=10,
               base_disposition=-0.2)
    area.spawn(sc_entrance, "shore_crab", count_min=0, count_max=1,
               respawn_minutes=15, respawn_variance=5)
    area.spawn(cs_cliff_face, "cliff_harpy", count_min=0, count_max=1,
               respawn_minutes=25, respawn_variance=10)
    area.spawn(tf_sea_glass_cove, "shore_crab", count_min=1, count_max=2,
               respawn_minutes=12, respawn_variance=3)
    area.spawn(tf_stranded_boat, "shore_crab", count_min=0, count_max=1,
               respawn_minutes=15, respawn_variance=5)
    area.spawn(cn_crevice, "cliff_harpy", count_min=0, count_max=1,
               respawn_minutes=25, respawn_variance=10)
    area.spawn(cn_rockfall, "cliff_harpy", count_min=0, count_max=1,
               respawn_minutes=20, respawn_variance=8)
    area.spawn(sc_grotto, "salt_lurker", count_min=0, count_max=1,
               respawn_minutes=25, respawn_variance=10)
    area.spawn(sc_tidal_channel, "shore_crab", count_min=0, count_max=1,
               respawn_minutes=15, respawn_variance=5)
    area.spawn(wr_crew_quarters, "shore_crab", count_min=0, count_max=1,
               respawn_minutes=12, respawn_variance=5)
    area.spawn(sm_sleeping_quarters, "coastal_raider", count_min=0, count_max=1,
               respawn_minutes=15, respawn_variance=5,
               base_disposition=-0.2)
    area.spawn(cs_south_cave_1, "salt_lurker", count_min=0, count_max=1,
               respawn_minutes=20, respawn_variance=8)

    # ==================================================================
    #  NAMED MOB (D-20): Captain Wrack
    #  Infamous raider captain. Unique loot, 120-min respawn.
    # ==================================================================

    area.named_mob(
        sm_captain_cabin,
        "captain_wrack",
        template="coastal_raider",
        count_min=1,
        count_max=1,
        respawn_minutes=120,
        respawn_variance=30,
        base_disposition=-0.5,
    )

    # ==================================================================
    #  FIELD NPCs (D-22)
    # ==================================================================

    # 1. Old Fisherman -- harbor rumors about deep caves
    area.npc(sv_harbor, "npc_fisherman_old_korrin", faction=None)

    # 2. Smuggler contact in the cove (Resistance-adjacent)
    area.npc(sm_mess_area, "npc_smuggler_contact_veyra", faction=None)

    # 3. Imperial coastguard patrol captain
    area.npc(lh_base, "npc_coastguard_captain_aldren", faction="empire")

    # ==================================================================
    #  MATERIALS (D-24: salt, driftwood, sea glass, coral fragments)
    # ==================================================================

    area.material("salt", tier=1, terrain="clearing",
                  profession_bonus={"alchemy": 0.1, "cooking": 0.05})
    area.material("driftwood", tier=1, terrain="clearing",
                  profession_bonus={"smithing": 0.05})
    area.material("sea_glass", tier=1, terrain="clearing",
                  profession_bonus={"alchemy": 0.05})
    area.material("coral_fragment", tier=1, terrain="cave",
                  profession_bonus={"alchemy": 0.1})

    # ==================================================================
    #  LORE FRAGMENTS (D-24: maritime history in caves and shipwreck)
    # ==================================================================

    area.lore_fragment(
        "lore_standing_stones", sb_ancient_stones,
        discovery_method="search",
        scholar_path="remnance",
        text=(
            "The three standing stones on Storm Bluffs are carved from "
            "basalt -- a volcanic rock found nowhere within five hundred "
            "miles. Someone transported them here at enormous cost and "
            "effort. Their alignment corresponds to no known astronomical "
            "pattern. A Remnance scholar might recognize the stone as "
            "matching samples from pre-human ruins on the western continent."
        ),
        insight_gain=8,
    )

    area.lore_fragment(
        "lore_seaspray_log", wr_captain_quarters,
        discovery_method="search",
        text=(
            "The captain's log of the Seaspray is mostly destroyed by "
            "water, but one entry remains legible: 'Day 47 -- the crew "
            "reports lights beneath the water near the reef. Not "
            "bioluminescence. Structured. Geometric. The navigator "
            "refuses to chart this section. I understand why.' The "
            "next page is blank."
        ),
        insight_gain=5,
    )

    area.lore_fragment(
        "lore_fossil_wall", sc_fossil_wall,
        discovery_method="search",
        scholar_path="naturalism",
        text=(
            "The fossils in this wall span millions of years of marine "
            "history. One specimen stands out: a creature with traits "
            "of both serpent and something mammalian, preserved in "
            "perfect detail. It matches no known taxonomy. Marine "
            "biologists of the Naturalism guild have theorized about "
            "these creatures -- sea serpents, they call them. Not all "
            "are fossils. Some are still out there."
        ),
        insight_gain=6,
    )

    area.lore_fragment(
        "lore_ancient_cairn", cn_cairn,
        discovery_method="search",
        text=(
            "The cairn at the cliff's highest point is a navigation "
            "marker -- not for ships, but for something that approached "
            "from the air. The stones are positioned to be visible from "
            "directly above, forming a pattern that reads as a landing "
            "glyph in pre-human notation. Dragons used this coast long "
            "before humans fished it."
        ),
        insight_gain=7,
    )

    area.lore_fragment(
        "lore_smuggler_charts", sm_captain_cabin,
        discovery_method="search",
        scholar_path="subterfuge",
        text=(
            "Captain Wrack's charts reveal more than smuggling routes. "
            "One chart maps the underwater topography offshore with "
            "impossible accuracy -- depths, currents, and structures "
            "that should be invisible from the surface. A note in the "
            "margin reads: 'They showed me. The price was fair. The "
            "old ones beneath the reef know things the Empire does not.'"
        ),
        insight_gain=10,
    )

    # ==================================================================
    #  QUEST STUBS (D-23)
    # ==================================================================

    area.quest("sc_q_raider_bounty",
               quest_type="combat",
               quest_giver="npc_coastguard_captain_aldren",
               objective_type="kill",
               objective_target="coastal_raider",
               objective_count=10)

    area.quest("sc_q_deep_cave_rumors",
               quest_type="exploration",
               quest_giver="npc_fisherman_old_korrin",
               objective_type="investigate",
               objective_target="sea_cave_deep_pool",
               objective_count=1)

    area.quest("sc_q_smuggler_delivery",
               quest_type="delivery",
               quest_giver="npc_smuggler_contact_veyra",
               objective_type="deliver",
               objective_target="contraband_package",
               objective_count=1)

    # ==================================================================
    #  BUILD
    # ==================================================================

    return area.build()
