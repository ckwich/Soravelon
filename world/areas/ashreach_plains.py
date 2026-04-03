"""
Ashreach Plains -- Starter Zone 1

A windswept grassland south of Vael's Crossing where the Ashway road
stretches into the broad central plains of Varath. Named for ancient fires
nobody living remembers. Open terrain, scattered ruins, wolf packs, bandit
camps, and hardy settlers who scratch a living from the dry earth.

100+ rooms across 6 sub-regions, 5 mob types, 1 named mob, 3 field NPCs.
No levels -- zone scaling makes all content universal.

Sub-regions:
    1. The Ashway Road       (~18 rooms) -- Main road from city to deep plains
    2. Windswept Grasslands  (~20 rooms) -- Open rolling plains, wolf territory
    3. Drystone Ruins        (~15 rooms) -- Crumbling pre-Imperial structures
    4. Wolf Den Ridge        (~15 rooms) -- Rocky ridge, wolf pack lair
    5. Bandit's Hollow       (~18 rooms) -- Concealed ravine camp
    6. Warden Outpost        (~16 rooms) -- Ranger station, eastern trails
"""

from world.area_builder import AreaBuilder


def build():
    area = AreaBuilder("ashreach_plains")

    # ------------------------------------------------------------------
    # Zone setup
    # ------------------------------------------------------------------
    area.zone(
        name="The Ashreach",
        zone_type="plains",
        continent="varath",
        faction_territory="imperial",
        faction_presence=["empire", "wardens"],
        world_x=-50,
        world_y=-30,
        world_radius=60,
    )

    # ==================================================================
    #  MATERIALS (D-24)
    # ==================================================================
    area.material("iron_ore", tier=1, terrain="rocky",
                  absorbed_property="hardite",
                  profession_bonus={"smithing": 0.1})
    area.material("wolfsbane", tier=1, terrain="grassland",
                  absorbed_property="toxic",
                  profession_bonus={"alchemy": 0.1})
    area.material("ashgrass_fiber", tier=1, terrain="grassland",
                  absorbed_property=None,
                  profession_bonus={"cooking": 0.05})
    area.material("flint_shard", tier=1, terrain="rocky",
                  absorbed_property="sharpness",
                  profession_bonus={"smithing": 0.05})

    # ==================================================================
    #  REGION 1: THE ASHWAY ROAD (~18 rooms)
    #  The main overland route from Vael's Crossing southward into the
    #  Ashreach. Well-traveled, relatively safe, with a few diversions.
    # ==================================================================

    ash_road_01 = area.room(
        "ash_road_01",
        name="The Ashway - Northern Approach",
        desc=(
            "The packed-earth road widens here where it leaves the last "
            "scrubby line of hill country behind. Southward, the Ashreach "
            "opens up -- a vast expanse of dry grassland under a pale sky. "
            "Wagon ruts cut deep grooves into the yellowed earth, and ash-grey "
            "dust clings to everything. A weathered milestone reads 'Vael's "
            "Crossing -- 1 league'."
        ),
        room_type="path",
        indoor=False,
        ambient_echoes=[
            "Wind stirs the dry grass, sending up puffs of grey dust.",
            "A distant wagon creaks along the road behind you.",
            "Insects hum in the roadside scrub.",
        ],
    )

    ash_road_02 = area.room(
        "ash_road_02",
        name="The Ashway - Open Road",
        desc=(
            "Flat grassland stretches in every direction, broken only by the "
            "road underfoot and the occasional stunted thornbush. The sky is "
            "enormous here -- a vault of pale blue bruised with thin cloud. "
            "The air smells of sun-baked earth and dry sage."
        ),
        room_type="path",
        indoor=False,
    )

    ash_road_03 = area.room(
        "ash_road_03",
        name="The Ashway - Wayside Rest",
        desc=(
            "A ring of fire-blackened stones marks a common rest stop along "
            "the Ashway. Someone has left a stack of bundled thornbush for "
            "travelers' fires. A crude wooden sign points south: 'Ashreach "
            "proper -- keep to the road after dark'."
        ),
        room_type="path",
        indoor=False,
        ambient_echoes=[
            "Embers from someone's old fire still glow faintly in the ring.",
            "A hawk circles high overhead, riding a thermal.",
        ],
    )

    ash_road_04 = area.room(
        "ash_road_04",
        name="The Ashway - Dusty Bend",
        desc=(
            "The road curves gently around a low hummock covered in pale "
            "grass. Hoofprints and bootprints overlay each other in the dust, "
            "a palimpsest of recent travel. To the east, the grassland rises "
            "toward a rocky ridge."
        ),
        room_type="path",
        indoor=False,
    )

    ash_road_05 = area.room(
        "ash_road_05",
        name="The Ashway - Trader's Marker",
        desc=(
            "A tall cairn of stacked stones stands beside the road, festooned "
            "with faded cloth strips tied by passing merchants for luck. "
            "The Consortium seal is chiseled into the base stone. A well-worn "
            "track branches westward toward a line of low bluffs."
        ),
        room_type="path",
        indoor=False,
        ambient_echoes=[
            "Cloth strips flutter from the cairn in the wind.",
            "A trader's pack-mule brays somewhere out of sight.",
        ],
    )

    ash_road_06 = area.room(
        "ash_road_06",
        name="The Ashway - Wide Prairie",
        desc=(
            "The road runs straight as an arrow through shoulder-high golden "
            "grass that rustles and whispers in the perpetual wind. The sense "
            "of distance is disorienting -- the horizon is a flat line in "
            "every direction but north, where the foothills of The Reth are "
            "a faint grey smudge."
        ),
        room_type="path",
        indoor=False,
    )

    ash_road_07 = area.room(
        "ash_road_07",
        name="The Ashway - Thornbrake Crossing",
        desc=(
            "A dense thicket of grey thorn has encroached on the road from "
            "both sides, narrowing it to a single wagon width. Thorns "
            "scratch at anyone who strays too close to the edges. Animal "
            "trails disappear into the brake."
        ),
        room_type="path",
        indoor=False,
    )

    ash_road_08 = area.room(
        "ash_road_08",
        name="The Ashway - Dry Streambed",
        desc=(
            "The road crosses a shallow dip where a seasonal stream once "
            "ran. Now the bed is cracked mud and bleached stones. A few "
            "hardy weeds push through the cracks. The crossing is bridged "
            "by flat stones laid long ago."
        ),
        room_type="path",
        indoor=False,
    )

    ash_road_09 = area.room(
        "ash_road_09",
        name="The Ashway - Merchant Campsite",
        desc=(
            "A wider clearing beside the road serves as a regular camping "
            "spot for trade caravans. Wheel ruts radiate outward from a "
            "trampled circle. A hitching post and stone-lined fire pit are "
            "the only amenities. Dung piles attest to recent pack animal "
            "traffic."
        ),
        room_type="clearing",
        indoor=False,
        crafting_stations=["campfire"],
        ambient_echoes=[
            "Wind whistles through the hitching post's iron ring.",
            "Flies buzz around the old dung heaps.",
        ],
    )

    ash_road_10 = area.room(
        "ash_road_10",
        name="The Ashway - Hilltop View",
        desc=(
            "The road crests a gentle rise, offering a rare vantage point "
            "over the plains. To the south, the grassland fades to brown "
            "at the horizon. Smoke trails from distant homesteads mark the "
            "scattered settlements of the Ashreach. Eastward, a rocky ridge "
            "cuts across the landscape."
        ),
        room_type="path",
        indoor=False,
    )

    ash_road_11 = area.room(
        "ash_road_11",
        name="The Ashway - Burned Grass",
        desc=(
            "A patch of recently burned grass darkens both sides of the "
            "road. The fire line is sharp and deliberate -- controlled "
            "burning, a prairie management technique older than the Empire. "
            "The air still carries a faint char smell. New green shoots "
            "already push through the black."
        ),
        room_type="path",
        indoor=False,
    )

    ash_road_12 = area.room(
        "ash_road_12",
        name="The Ashway - Signpost Fork",
        desc=(
            "The road splits at a leaning wooden signpost. The main route "
            "continues south. A narrower trail veers east toward what the "
            "sign calls 'Wolf Den Ridge -- DANGER'. Claw marks scar the "
            "signpost's base."
        ),
        room_type="path",
        indoor=False,
    )

    ash_road_13 = area.room(
        "ash_road_13",
        name="The Ashway - Shallow Ditch",
        desc=(
            "Imperial engineers dug drainage ditches along this stretch of "
            "road, long since filled with wind-blown dirt and dead grass. "
            "The road surface is better here -- harder packed, fewer ruts. "
            "A patrol marker post stands in the ditch, painted with the "
            "faded Imperial sigil."
        ),
        room_type="path",
        indoor=False,
    )

    ash_road_14 = area.room(
        "ash_road_14",
        name="The Ashway - Prairie Dog Colony",
        desc=(
            "Dozens of small mounds dot the ground on both sides of the "
            "road, riddled with burrow holes. Small furry heads pop up and "
            "disappear at the approach of travelers. The ground here is "
            "treacherous for wagons -- more than one rut has been caused by "
            "a wheel dropping into a burrow."
        ),
        room_type="path",
        indoor=False,
        ambient_echoes=[
            "A prairie dog chirps a warning, and dozens vanish underground.",
            "The ground shifts slightly underfoot -- burrows everywhere.",
        ],
    )

    ash_road_15 = area.room(
        "ash_road_15",
        name="The Ashway - Southern Reach",
        desc=(
            "The road enters its final stretch before the deep Ashreach. "
            "The grass is taller here, waving in golden sheets. The "
            "footprints thin out -- fewer travelers venture this far from "
            "Vael's Crossing without purpose. A buzzard circles overhead."
        ),
        room_type="path",
        indoor=False,
    )

    ash_road_16 = area.room(
        "ash_road_16",
        name="Ashway Crossroads",
        desc=(
            "A major intersection where the Ashway meets east-west tracks "
            "leading to the coast and the forest. A large flat stone serves "
            "as an impromptu meeting place. Travelers sometimes leave "
            "messages scratched into its surface."
        ),
        room_type="clearing",
        indoor=False,
        ambient_echoes=[
            "Wind gusts raise a spiral of dust from the crossroads.",
            "Boot and hoofprints overlap in the dirt -- heavy traffic here.",
        ],
    )

    ash_road_17 = area.room(
        "ash_road_17",
        name="The Ashway - Deep South",
        desc=(
            "The road grows fainter here, more suggestion than structure. "
            "The Ashreach has begun to reclaim it -- grass shoots push "
            "through what remains of the packed surface. Civilization feels "
            "distant. The wind carries the howl of something animal."
        ),
        room_type="path",
        indoor=False,
    )

    ash_road_18 = area.room(
        "ash_road_18",
        name="The Ashway - Terminus",
        desc=(
            "The road simply ends, swallowed by the endless grassland. "
            "Beyond this point there is only the Ashreach -- trackless "
            "plains stretching to the southern horizon. A last cairn marks "
            "the road's end, smaller and less tended than its northern "
            "cousins."
        ),
        room_type="clearing",
        indoor=False,
    )

    # -- Ashway Road exits --
    area.exit(ash_road_01, "vaels_crossing:hg_south_road", "north")  # cross-zone
    area.exit(ash_road_01, ash_road_02, "south")
    area.exit(ash_road_02, ash_road_01, "north")
    area.exit(ash_road_02, ash_road_03, "south")
    area.exit(ash_road_03, ash_road_02, "north")
    area.exit(ash_road_03, ash_road_04, "south")
    area.exit(ash_road_04, ash_road_03, "north")
    area.exit(ash_road_04, ash_road_05, "south")
    area.exit(ash_road_05, ash_road_04, "north")
    area.exit(ash_road_05, ash_road_06, "south")
    area.exit(ash_road_06, ash_road_05, "north")
    area.exit(ash_road_06, ash_road_07, "south")
    area.exit(ash_road_07, ash_road_06, "north")
    area.exit(ash_road_07, ash_road_08, "south")
    area.exit(ash_road_08, ash_road_07, "north")
    area.exit(ash_road_08, ash_road_09, "south")
    area.exit(ash_road_09, ash_road_08, "north")
    area.exit(ash_road_09, ash_road_10, "south")
    area.exit(ash_road_10, ash_road_09, "north")
    area.exit(ash_road_10, ash_road_11, "south")
    area.exit(ash_road_11, ash_road_10, "north")
    area.exit(ash_road_11, ash_road_12, "south")
    area.exit(ash_road_12, ash_road_11, "north")
    area.exit(ash_road_12, ash_road_13, "south")
    area.exit(ash_road_13, ash_road_12, "north")
    area.exit(ash_road_13, ash_road_14, "south")
    area.exit(ash_road_14, ash_road_13, "north")
    area.exit(ash_road_14, ash_road_15, "south")
    area.exit(ash_road_15, ash_road_14, "north")
    area.exit(ash_road_15, ash_road_16, "south")
    area.exit(ash_road_16, ash_road_15, "north")
    area.exit(ash_road_16, ash_road_17, "south")
    area.exit(ash_road_17, ash_road_16, "north")
    area.exit(ash_road_17, ash_road_18, "south")
    area.exit(ash_road_18, ash_road_17, "north")

    # -- Ashway Road spawns (D-19: moderate density) --
    area.spawn(ash_road_03, "dust_beetle", count_min=1, count_max=2,
               respawn_minutes=15, respawn_variance=5)
    area.spawn(ash_road_07, "plains_viper", count_min=1, count_max=1,
               respawn_minutes=20, respawn_variance=5)
    area.spawn(ash_road_11, "ash_wolf", count_min=1, count_max=2,
               respawn_minutes=15, respawn_variance=5)
    area.spawn(ash_road_14, "dust_beetle", count_min=1, count_max=1,
               respawn_minutes=15, respawn_variance=5)
    area.spawn(ash_road_17, "steppe_hawk", count_min=1, count_max=1,
               respawn_minutes=20, respawn_variance=5)
    area.spawn(ash_road_06, "ashreach_bandit", count_min=1, count_max=1,
               respawn_minutes=25, respawn_variance=10)

    # ==================================================================
    #  REGION 2: WINDSWEPT GRASSLANDS (~20 rooms)
    #  Open rolling plains east and west of the road. Wolf territory.
    # ==================================================================

    grass_01 = area.room(
        "grass_01",
        name="Windswept Grassland - West Edge",
        desc=(
            "The road is a dark line to the east, already feeling distant. "
            "Grass reaches waist-high here, thick and pale gold, swaying "
            "in rhythmic waves under the ceaseless wind. Small creatures "
            "rustle unseen through the stems."
        ),
        room_type="clearing",
        indoor=False,
    )

    grass_02 = area.room(
        "grass_02",
        name="Windswept Grassland - Tall Grass",
        desc=(
            "The grass grows even taller here, chest-high in places, "
            "reducing visibility to a few paces. Animal trails thread "
            "through the stems in narrow paths. The ground is soft "
            "underfoot -- a mixture of loam and ancient ash."
        ),
        room_type="clearing",
        indoor=False,
    )

    grass_03 = area.room(
        "grass_03",
        name="Windswept Grassland - Shallow Depression",
        desc=(
            "A shallow dip in the terrain collects the last traces of "
            "moisture. The grass here is greener and thicker than the "
            "surrounding plain. Animal tracks converge from all directions "
            "-- a natural watering point in dry seasons."
        ),
        room_type="clearing",
        indoor=False,
        ambient_echoes=[
            "Something splashes in the shallow muddy water.",
            "Bird calls echo from the wetter grass.",
        ],
    )

    grass_04 = area.room(
        "grass_04",
        name="Windswept Grassland - Rock Cluster",
        desc=(
            "A scattering of grey boulders breaks the monotony of the "
            "grassland. Lichen and dry moss cling to their surfaces. "
            "The rocks provide the only shade for leagues -- and judging "
            "by the gnawed bones at their base, predators know this."
        ),
        room_type="clearing",
        indoor=False,
    )

    grass_05 = area.room(
        "grass_05",
        name="Windswept Grassland - Exposed Bluff",
        desc=(
            "A low bluff of crumbling sandstone rises above the grass "
            "line, its face eroded into strange organic shapes. Iron-red "
            "striations run through the stone. A good vantage point -- "
            "the grass parts for a hundred paces in every direction."
        ),
        room_type="clearing",
        indoor=False,
    )

    grass_06 = area.room(
        "grass_06",
        name="Windswept Grassland - Lone Tree",
        desc=(
            "A single twisted thornwood tree stands defiantly against the "
            "wind, its branches permanently bent eastward. Carved initials "
            "and crude symbols mark its trunk -- travelers' graffiti "
            "spanning decades. A hawk's nest sits in the upper branches."
        ),
        room_type="clearing",
        indoor=False,
        ambient_echoes=[
            "The thornwood creaks in the wind like old bones.",
            "A hawk shrieks from its nest in the twisted branches.",
        ],
    )

    grass_07 = area.room(
        "grass_07",
        name="Windswept Grassland - Beetle Grounds",
        desc=(
            "The ground is pockmarked with beetle burrows -- smooth-edged "
            "holes the size of a fist, disappearing into darkness. Broken "
            "carapace fragments litter the surface between the grass stems. "
            "A faint clicking rises from underground."
        ),
        room_type="clearing",
        indoor=False,
    )

    grass_08 = area.room(
        "grass_08",
        name="Windswept Grassland - Game Trail",
        desc=(
            "A well-worn animal trail cuts through the grass, wider than "
            "the narrower paths. The prints are mixed -- wolf, deer, "
            "something heavier with broad pads. The trail leads east "
            "toward higher ground."
        ),
        room_type="path",
        indoor=False,
    )

    grass_09 = area.room(
        "grass_09",
        name="Windswept Grassland - Open Flat",
        desc=(
            "Nothing but grass and sky. The flatness is absolute, almost "
            "disorienting. Wind moves through the grass in visible waves, "
            "creating patterns that shift and vanish. The isolation is "
            "profound."
        ),
        room_type="clearing",
        indoor=False,
    )

    grass_10 = area.room(
        "grass_10",
        name="Windswept Grassland - Old Boundary Ditch",
        desc=(
            "A shallow ditch, long overgrown, marks what was once a "
            "property boundary or defensive line. The earth was moved with "
            "purpose -- straight sides, regular depth. Whatever settlement "
            "it protected is long gone."
        ),
        room_type="clearing",
        indoor=False,
    )

    grass_11 = area.room(
        "grass_11",
        name="Windswept Grassland - East Slope",
        desc=(
            "The ground rises gradually eastward toward a line of rocky "
            "outcroppings. The grass thins as soil gives way to gravel "
            "and loose stone. Lizards bask on the sun-warmed rocks."
        ),
        room_type="clearing",
        indoor=False,
    )

    grass_12 = area.room(
        "grass_12",
        name="Windswept Grassland - Ash Circle",
        desc=(
            "A perfect circle of blackened earth interrupts the grassland, "
            "perhaps ten paces across. The grass refuses to grow here. "
            "The soil is fine grey ash, soft as powder. Whatever burned "
            "here left no recognizable debris -- just the circle and the "
            "silence."
        ),
        room_type="clearing",
        indoor=False,
    )

    grass_13 = area.room(
        "grass_13",
        name="Windswept Grassland - South Field",
        desc=(
            "The grass stretches endlessly south, undulating in the wind "
            "like a golden sea. Small blue flowers dot the ground near "
            "ankle level -- wolfsbane, growing wild. The air carries a "
            "faint bitter scent from the blooms."
        ),
        room_type="clearing",
        indoor=False,
    )

    grass_14 = area.room(
        "grass_14",
        name="Windswept Grassland - Snake Run",
        desc=(
            "The grass is lower here, cropped short by grazing animals "
            "or recent fire. The exposed ground is cracked and dry, "
            "with narrow fissures where vipers shelter from the sun. "
            "Shed snakeskins curl like parchment in the dirt."
        ),
        room_type="clearing",
        indoor=False,
    )

    grass_15 = area.room(
        "grass_15",
        name="Windswept Grassland - Western Reach",
        desc=(
            "The grassland extends westward toward a dark tree line that "
            "marks the edge of another zone entirely. The transition is "
            "gradual -- grass gives way to scrub, scrub to saplings, "
            "saplings to forest."
        ),
        room_type="clearing",
        indoor=False,
    )

    grass_16 = area.room(
        "grass_16",
        name="Windswept Grassland - Anthill Field",
        desc=(
            "Red earth anthills rise from the grassland like miniature "
            "towers, some reaching knee height. The ants are large and "
            "industrious, carving paths through the grass in neat lines. "
            "Beetle remains litter the approach to the largest mound."
        ),
        room_type="clearing",
        indoor=False,
    )

    grass_17 = area.room(
        "grass_17",
        name="Windswept Grassland - Hawk Hunting Ground",
        desc=(
            "An open stretch where the grass is naturally short and thin. "
            "Steppe hawks patrol this area -- dark shapes wheeling overhead, "
            "occasionally stooping with startling speed. Feathers and small "
            "bones scatter the ground."
        ),
        room_type="clearing",
        indoor=False,
    )

    grass_18 = area.room(
        "grass_18",
        name="Windswept Grassland - Dusty Hollow",
        desc=(
            "A low hollow where wind-blown dust has accumulated in soft "
            "drifts. The grass is patchy here, choked by the pale grey "
            "dust that gives the Ashreach its name. Beetle tracks criss-cross "
            "the dust like tiny roads."
        ),
        room_type="clearing",
        indoor=False,
    )

    grass_19 = area.room(
        "grass_19",
        name="Windswept Grassland - Sunset Rise",
        desc=(
            "A gentle swell in the terrain offers a view westward. On "
            "clear evenings, the sunset turns the grassland copper and "
            "crimson. The wind is stronger here on the exposed rise, "
            "and the grass lays almost flat."
        ),
        room_type="clearing",
        indoor=False,
    )

    grass_20 = area.room(
        "grass_20",
        name="Windswept Grassland - Pack Territory Marker",
        desc=(
            "The grass is trampled flat in a wide area. Claw marks score "
            "a boulder, and the musky scent of predator urine hangs in "
            "the air. Wolf scat is everywhere. This is marked territory. "
            "A low ridge to the east is visible through gaps in the grass."
        ),
        room_type="clearing",
        indoor=False,
    )

    # -- Grassland exits --
    area.exit(ash_road_02, grass_01, "west")
    area.exit(grass_01, ash_road_02, "east")
    area.exit(grass_01, grass_02, "south")
    area.exit(grass_02, grass_01, "north")
    area.exit(grass_02, grass_03, "south")
    area.exit(grass_03, grass_02, "north")
    area.exit(grass_03, grass_04, "west")
    area.exit(grass_04, grass_03, "east")
    area.exit(grass_04, grass_05, "south")
    area.exit(grass_05, grass_04, "north")
    area.exit(grass_03, grass_06, "east")
    area.exit(grass_06, grass_03, "west")
    area.exit(grass_06, grass_07, "south")
    area.exit(grass_07, grass_06, "north")
    area.exit(grass_07, grass_08, "east")
    area.exit(grass_08, grass_07, "west")
    area.exit(grass_08, grass_11, "east")
    area.exit(grass_11, grass_08, "west")
    area.exit(grass_05, grass_09, "west")
    area.exit(grass_09, grass_05, "east")
    area.exit(grass_09, grass_10, "south")
    area.exit(grass_10, grass_09, "north")
    area.exit(grass_10, grass_15, "west")
    area.exit(grass_15, grass_10, "east")
    area.exit(grass_11, grass_12, "south")
    area.exit(grass_12, grass_11, "north")
    area.exit(grass_07, grass_16, "south")
    area.exit(grass_16, grass_07, "north")
    area.exit(grass_16, grass_13, "south")
    area.exit(grass_13, grass_16, "north")
    area.exit(grass_13, grass_14, "west")
    area.exit(grass_14, grass_13, "east")
    area.exit(ash_road_06, grass_17, "east")
    area.exit(grass_17, ash_road_06, "west")
    area.exit(grass_17, grass_18, "south")
    area.exit(grass_18, grass_17, "north")
    area.exit(grass_18, grass_19, "west")
    area.exit(grass_19, grass_18, "east")
    area.exit(grass_12, grass_20, "east")
    area.exit(grass_20, grass_12, "west")

    # -- Grassland spawns --
    area.spawn(grass_02, "ash_wolf", count_min=1, count_max=2,
               respawn_minutes=15, respawn_variance=5)
    area.spawn(grass_04, "dust_beetle", count_min=1, count_max=2,
               respawn_minutes=12, respawn_variance=4)
    area.spawn(grass_06, "steppe_hawk", count_min=1, count_max=1,
               respawn_minutes=20, respawn_variance=5)
    area.spawn(grass_07, "dust_beetle", count_min=2, count_max=3,
               respawn_minutes=12, respawn_variance=4)
    area.spawn(grass_09, "ash_wolf", count_min=1, count_max=1,
               respawn_minutes=15, respawn_variance=5)
    area.spawn(grass_11, "plains_viper", count_min=1, count_max=1,
               respawn_minutes=20, respawn_variance=5)
    area.spawn(grass_14, "plains_viper", count_min=1, count_max=2,
               respawn_minutes=20, respawn_variance=5)
    area.spawn(grass_17, "steppe_hawk", count_min=1, count_max=2,
               respawn_minutes=20, respawn_variance=5)
    area.spawn(grass_19, "ash_wolf", count_min=1, count_max=1,
               respawn_minutes=15, respawn_variance=5)
    area.spawn(grass_20, "ash_wolf", count_min=2, count_max=3,
               respawn_minutes=15, respawn_variance=5)
    area.spawn(grass_16, "dust_beetle", count_min=1, count_max=1,
               respawn_minutes=12, respawn_variance=4)

    # ==================================================================
    #  REGION 3: DRYSTONE RUINS (~15 rooms)
    #  Crumbling pre-Imperial structures. Lore fragments, resonant air.
    # ==================================================================

    ruins_01 = area.room(
        "ruins_01",
        name="Drystone Ruins - Outer Wall",
        desc=(
            "Low walls of unmortared stone trace the outline of a "
            "structure far older than the Empire. The stones are "
            "fire-blackened and wind-worn, their surfaces oddly smooth. "
            "Grass grows through every gap. Whatever stood here was "
            "large -- the foundation stretches in both directions."
        ),
        room_type="ruins",
        indoor=False,
    )

    ruins_02 = area.room(
        "ruins_02",
        name="Drystone Ruins - Collapsed Hall",
        desc=(
            "Massive stones lie tumbled in a pattern that suggests a great "
            "hall brought low by force rather than time. Scorch marks "
            "blacken the inner surfaces. A few column bases still stand, "
            "knee-high stubs of what must have been impressive pillars."
        ),
        room_type="ruins",
        indoor=False,
    )

    ruins_03 = area.room(
        "ruins_03",
        name="Drystone Ruins - Inner Court",
        desc=(
            "A roughly rectangular space enclosed by ruined walls. The "
            "ground is paved with flat stones set in a geometric pattern "
            "-- a pattern that seems to repeat in groups of eight. Moss "
            "fills the joints. The air feels heavier here, still and "
            "watchful."
        ),
        room_type="ruins",
        indoor=False,
    )

    ruins_04 = area.room(
        "ruins_04",
        name="Drystone Ruins - Sunken Chamber",
        desc=(
            "Steps descend into a half-buried chamber, its ceiling long "
            "since collapsed. Rubble chokes the far end. The walls that "
            "remain are carved with repeating geometric designs -- circles "
            "within circles, divided into eight segments. The carvings are "
            "crisp despite their age."
        ),
        room_type="ruins",
        indoor=True,
    )

    ruins_05 = area.room(
        "ruins_05",
        name="Drystone Ruins - Crumbled Tower Base",
        desc=(
            "A circular foundation marks where a tower once stood. The "
            "base is three paces across, the stones fitted with inhuman "
            "precision. Scattered blocks radiate outward from the base "
            "-- the tower fell, or was felled, and its remains were "
            "scavenged for building material long ago."
        ),
        room_type="ruins",
        indoor=False,
    )

    ruins_06 = area.room(
        "ruins_06",
        name="Drystone Ruins - Ash-Filled Basin",
        desc=(
            "A large stone basin, cracked but intact, sits in a cleared "
            "space between ruined walls. It is filled with fine grey ash "
            "-- the same pale powder that gives the Ashreach its character. "
            "Nothing grows within arm's reach of the basin."
        ),
        room_type="ruins",
        indoor=False,
    )

    ruins_07 = area.room(
        "ruins_07",
        name="Drystone Ruins - Fallen Arch",
        desc=(
            "A stone arch lies on its side, still intact as a single "
            "piece. The keystone is carved with a symbol that might be "
            "a stylized flame or a coiled serpent -- weathering makes it "
            "ambiguous. The arch frames a view of empty grassland."
        ),
        room_type="ruins",
        indoor=False,
    )

    ruins_08 = area.room(
        "ruins_08",
        name="Drystone Ruins - Offering Alcove",
        desc=(
            "A niche carved into a standing wall, sheltered from the "
            "wind. Old offerings -- clay shards, dried flowers, a tarnished "
            "coin -- suggest the local population treats this place with "
            "wary respect. The stone inside the alcove is warm to the "
            "touch, even in cool weather."
        ),
        room_type="ruins",
        indoor=False,
    )

    ruins_09 = area.room(
        "ruins_09",
        name="Drystone Ruins - Broken Floor",
        desc=(
            "The floor has partially collapsed into a void beneath, "
            "revealing earth and stone a body-length below. The edges "
            "are ragged. Whatever space existed underneath has filled "
            "with dirt and debris over the centuries."
        ),
        room_type="ruins",
        indoor=False,
    )

    ruins_10 = area.room(
        "ruins_10",
        name="Drystone Ruins - Wind Channel",
        desc=(
            "Two parallel walls still stand tall enough to channel the "
            "wind between them with a low, constant moan. The acoustics "
            "are eerie -- whispered words carry the full length of the "
            "passage with startling clarity."
        ),
        room_type="ruins",
        indoor=False,
        ambient_echoes=[
            "The wind moans through the stone channel like a voice.",
            "Dust spirals between the parallel walls in miniature tornadoes.",
        ],
    )

    ruins_11 = area.room(
        "ruins_11",
        name="Drystone Ruins - Carved Seat",
        desc=(
            "A stone seat, clearly intentional, is carved from a single "
            "block and positioned to face east. The armrests bear the same "
            "octagonal motifs found elsewhere in the ruins. The seat is "
            "too large for a human -- or perhaps sized for someone wearing "
            "something bulky."
        ),
        room_type="ruins",
        indoor=False,
    )

    ruins_12 = area.room(
        "ruins_12",
        name="Drystone Ruins - Weed-Choked Passage",
        desc=(
            "A narrow passage between two ruined buildings, almost "
            "impassable with thorny weeds. The walls on both sides show "
            "tool marks -- this was a maintained space once. Beetle shells "
            "crunch underfoot."
        ),
        room_type="ruins",
        indoor=False,
    )

    ruins_13 = area.room(
        "ruins_13",
        name="Drystone Ruins - Octagonal Platform",
        desc=(
            "An octagonal stone platform rises a hand-span above the "
            "surrounding rubble. Eight stone posts -- most broken at "
            "various heights -- ring its edge. The center is perfectly "
            "flat and polished smooth despite centuries of exposure. "
            "The air tastes metallic here."
        ),
        room_type="ruins",
        indoor=False,
    )

    ruins_14 = area.room(
        "ruins_14",
        name="Drystone Ruins - Southern Edge",
        desc=(
            "The ruins thin out here, giving way to open grassland. "
            "Scattered stones mark where the settlement's edge once was. "
            "A few foundation outlines are visible as rectangular "
            "depressions in the ground, already being absorbed by the "
            "plains."
        ),
        room_type="ruins",
        indoor=False,
    )

    ruins_15 = area.room(
        "ruins_15",
        name="Drystone Ruins - Hidden Cellar",
        desc=(
            "Beneath a collapsed section, a narrow gap leads down into "
            "a partially intact cellar. The walls are damp stone, the air "
            "cool and still. Old pottery fragments and corroded metal "
            "fittings lie in the dirt. Something scuttles in the darkness."
        ),
        room_type="ruins",
        indoor=True,
    )

    # -- Ruins exits --
    area.exit(ash_road_05, ruins_01, "west")
    area.exit(ruins_01, ash_road_05, "east")
    area.exit(ruins_01, ruins_02, "south")
    area.exit(ruins_02, ruins_01, "north")
    area.exit(ruins_02, ruins_03, "west")
    area.exit(ruins_03, ruins_02, "east")
    area.exit(ruins_03, ruins_04, "down")
    area.exit(ruins_04, ruins_03, "up")
    area.exit(ruins_02, ruins_05, "south")
    area.exit(ruins_05, ruins_02, "north")
    area.exit(ruins_05, ruins_06, "south")
    area.exit(ruins_06, ruins_05, "north")
    area.exit(ruins_03, ruins_07, "south")
    area.exit(ruins_07, ruins_03, "north")
    area.exit(ruins_07, ruins_08, "west")
    area.exit(ruins_08, ruins_07, "east")
    area.exit(ruins_07, ruins_09, "south")
    area.exit(ruins_09, ruins_07, "north")
    area.exit(ruins_09, ruins_10, "east")
    area.exit(ruins_10, ruins_09, "west")
    area.exit(ruins_06, ruins_11, "west")
    area.exit(ruins_11, ruins_06, "east")
    area.exit(ruins_10, ruins_12, "south")
    area.exit(ruins_12, ruins_10, "north")
    area.exit(ruins_12, ruins_13, "south")
    area.exit(ruins_13, ruins_12, "north")
    area.exit(ruins_13, ruins_14, "south")
    area.exit(ruins_14, ruins_13, "north")
    area.exit(ruins_09, ruins_15, "down")
    area.exit(ruins_15, ruins_09, "up")

    # -- Ruins spawns --
    area.spawn(ruins_01, "dust_beetle", count_min=1, count_max=2,
               respawn_minutes=12, respawn_variance=4)
    area.spawn(ruins_05, "plains_viper", count_min=1, count_max=1,
               respawn_minutes=20, respawn_variance=5)
    area.spawn(ruins_09, "dust_beetle", count_min=1, count_max=2,
               respawn_minutes=12, respawn_variance=4)
    area.spawn(ruins_12, "plains_viper", count_min=1, count_max=1,
               respawn_minutes=20, respawn_variance=5)
    area.spawn(ruins_15, "dust_beetle", count_min=2, count_max=3,
               respawn_minutes=12, respawn_variance=4)

    # -- Ruins lore fragments (D-24) --
    area.lore_fragment(
        "ashreach_octagonal_01", ruins_13,
        discovery_method="search",
        scholar_path="remnance",
        text=(
            "The octagonal platform's geometry is deliberate -- eight sides, "
            "eight posts. The pattern recurs in every ruin across the Ashreach. "
            "Whoever built this counted differently than we do."
        ),
        insight_gain=5,
    )

    area.lore_fragment(
        "ashreach_sunken_carving_01", ruins_04,
        discovery_method="search",
        scholar_path="remnance",
        text=(
            "The carvings in the sunken chamber are remarkably precise -- "
            "circles divided into eight equal parts, repeated in cascading "
            "scales. Mathematical, not decorative. The toolwork predates "
            "anything Imperial."
        ),
        insight_gain=5,
    )

    area.lore_fragment(
        "ashreach_ash_basin_01", ruins_06,
        discovery_method="search",
        scholar_path="resonance",
        text=(
            "The ash in the basin is too fine to be from wood. It carries "
            "a faint metallic tang, and when disturbed, motes hang in the "
            "air far longer than gravity should allow. The locals avoid "
            "this place after dark."
        ),
        insight_gain=5,
    )

    area.lore_fragment(
        "ashreach_wind_channel_01", ruins_10,
        discovery_method="search",
        scholar_path="arcana",
        text=(
            "The acoustic properties of the wind channel are not natural. "
            "The walls are slightly curved in a way that amplifies certain "
            "frequencies. An engineer would say this was a communication "
            "device. A scholar would wonder who was speaking to whom."
        ),
        insight_gain=3,
    )

    area.lore_fragment(
        "ashreach_carved_seat_01", ruins_11,
        discovery_method="search",
        scholar_path="remnance",
        text=(
            "The seat faces east -- toward the sunrise, toward The Reth, "
            "toward something. Its proportions are wrong for any living "
            "ancestry. The armrests are scored with claw marks, four "
            "parallel grooves repeated on each side."
        ),
        insight_gain=8,
    )

    # ==================================================================
    #  REGION 4: WOLF DEN RIDGE (~15 rooms)
    #  Rocky ridge east of the grasslands. Wolf pack lair. Named mob.
    # ==================================================================

    ridge_01 = area.room(
        "ridge_01",
        name="Wolf Den Ridge - Lower Slope",
        desc=(
            "The grassland gives way to stony ground as a ridge of dark "
            "rock rises to the east. Loose scree makes footing uncertain. "
            "Wolf tracks are pressed into every patch of soft earth between "
            "the stones."
        ),
        room_type="path",
        indoor=False,
    )

    ridge_02 = area.room(
        "ridge_02",
        name="Wolf Den Ridge - Narrow Trail",
        desc=(
            "A narrow trail switchbacks up the rocky ridge, barely wide "
            "enough for single file. Claw marks score the stone on both "
            "sides. Tufts of grey-brown fur snag on sharp rock edges."
        ),
        room_type="path",
        indoor=False,
    )

    ridge_03 = area.room(
        "ridge_03",
        name="Wolf Den Ridge - Exposed Ledge",
        desc=(
            "A flat ledge extends from the ridge face, exposed to wind "
            "from three sides. Gnawed bones are scattered across the "
            "stone -- a feeding spot used regularly. The view westward "
            "shows the grasslands stretching to the horizon."
        ),
        room_type="clearing",
        indoor=False,
    )

    ridge_04 = area.room(
        "ridge_04",
        name="Wolf Den Ridge - Boulder Field",
        desc=(
            "Large boulders, some taller than a person, create a maze "
            "of narrow passages on the ridge. Deep shadows pool between "
            "the rocks. The smell of animal musk is strong. Eyes might "
            "be watching from the darkness between stones."
        ),
        room_type="path",
        indoor=False,
    )

    ridge_05 = area.room(
        "ridge_05",
        name="Wolf Den Ridge - Pack Gathering",
        desc=(
            "A natural amphitheater in the rock where the ridge curves "
            "inward. The ground is packed hard by countless paws. Bones "
            "and hide scraps are pushed to the edges. This is where the "
            "pack gathers -- their central meeting ground."
        ),
        room_type="clearing",
        indoor=False,
        ambient_echoes=[
            "A wolf howl rises from somewhere deeper in the ridge.",
            "Claws click on stone as something moves just out of sight.",
        ],
    )

    ridge_06 = area.room(
        "ridge_06",
        name="Wolf Den Ridge - Upper Lookout",
        desc=(
            "The highest accessible point on the ridge, a wind-scoured "
            "platform of flat stone. On clear days, Vael's Crossing is "
            "visible as a dark smudge to the north. The entire grassland "
            "spreads below like a map. Wolf urine marks every projecting "
            "rock."
        ),
        room_type="clearing",
        indoor=False,
    )

    ridge_07 = area.room(
        "ridge_07",
        name="Wolf Den Ridge - Den Entrance",
        desc=(
            "A dark opening in the ridge face, partly obscured by a "
            "fallen slab. The smell of animal is overpowering. Scratch "
            "marks deepen the opening's edges. Fur, bones, and dried "
            "blood decorate the threshold."
        ),
        room_type="cave",
        indoor=False,
    )

    ridge_08 = area.room(
        "ridge_08",
        name="Wolf Den Ridge - Outer Den",
        desc=(
            "A shallow cave lit by filtered daylight from the entrance. "
            "The floor is packed earth covered with shed fur and gnawed "
            "bones. Nesting hollows are scooped into the dirt along the "
            "walls. The ceiling is low -- a crouching height for a human."
        ),
        room_type="cave",
        indoor=True,
    )

    ridge_09 = area.room(
        "ridge_09",
        name="Wolf Den Ridge - Deep Den",
        desc=(
            "Beyond the outer cave, the den narrows and descends. The "
            "light fades to near-darkness. The air is warm with animal "
            "heat and thick with musk. This is the core of the pack's "
            "territory -- their most defended ground."
        ),
        room_type="cave",
        indoor=True,
    )

    ridge_10 = area.room(
        "ridge_10",
        name="Wolf Den Ridge - Kill Drag",
        desc=(
            "A depression between boulders where the pack drags larger "
            "kills to feed. The ground is dark with old blood. Flies "
            "swarm over remnants of recent meals. The skull of something "
            "horned sits propped against a rock."
        ),
        room_type="clearing",
        indoor=False,
    )

    ridge_11 = area.room(
        "ridge_11",
        name="Wolf Den Ridge - East Face",
        desc=(
            "The ridge's eastern face drops away steeply into a dry "
            "gully. A narrow path hugs the cliff edge, barely passable. "
            "Hawks nest in the cliff face, their droppings whitening the "
            "stone below."
        ),
        room_type="path",
        indoor=False,
    )

    ridge_12 = area.room(
        "ridge_12",
        name="Wolf Den Ridge - Gully Bottom",
        desc=(
            "The bottom of the dry gully east of the ridge. Smooth "
            "water-worn stones line a channel that only flows during "
            "heavy rain. Scrubby bushes cling to the gully walls. "
            "Animal trails lead north and south along the gully floor."
        ),
        room_type="path",
        indoor=False,
    )

    ridge_13 = area.room(
        "ridge_13",
        name="Wolf Den Ridge - South Approach",
        desc=(
            "The ridge slopes downward to the south, the rock giving way "
            "to gravelly earth and then grassland. A few scraggly trees "
            "mark the transition zone. Wolf tracks converge here from "
            "multiple directions."
        ),
        room_type="path",
        indoor=False,
    )

    ridge_14 = area.room(
        "ridge_14",
        name="Wolf Den Ridge - Hidden Spring",
        desc=(
            "A small spring seeps from a crack in the rock, trickling "
            "into a natural basin before disappearing underground. The "
            "water is cold and clean. Green moss surrounds the basin -- "
            "the only true green on the entire ridge."
        ),
        room_type="clearing",
        indoor=False,
    )

    ridge_15 = area.room(
        "ridge_15",
        name="Wolf Den Ridge - North Slope",
        desc=(
            "The ridge descends northward in a series of rocky steps. "
            "The transition back to grassland is abrupt -- stone and "
            "scree giving way to packed earth and yellow grass within "
            "a few paces."
        ),
        room_type="path",
        indoor=False,
    )

    # -- Ridge exits --
    area.exit(grass_11, ridge_01, "east")
    area.exit(ridge_01, grass_11, "west")
    area.exit(ash_road_12, ridge_15, "east")
    area.exit(ridge_15, ash_road_12, "west")
    area.exit(ridge_01, ridge_02, "east")
    area.exit(ridge_02, ridge_01, "west")
    area.exit(ridge_02, ridge_03, "north")
    area.exit(ridge_03, ridge_02, "south")
    area.exit(ridge_02, ridge_04, "east")
    area.exit(ridge_04, ridge_02, "west")
    area.exit(ridge_04, ridge_05, "east")
    area.exit(ridge_05, ridge_04, "west")
    area.exit(ridge_05, ridge_06, "up")
    area.exit(ridge_06, ridge_05, "down")
    area.exit(ridge_05, ridge_07, "east")
    area.exit(ridge_07, ridge_05, "west")
    area.exit(ridge_07, ridge_08, "in")
    area.exit(ridge_08, ridge_07, "out")
    area.exit(ridge_08, ridge_09, "in")
    area.exit(ridge_09, ridge_08, "out")
    area.exit(ridge_03, ridge_10, "east")
    area.exit(ridge_10, ridge_03, "west")
    area.exit(ridge_10, ridge_11, "east")
    area.exit(ridge_11, ridge_10, "west")
    area.exit(ridge_11, ridge_12, "down")
    area.exit(ridge_12, ridge_11, "up")
    area.exit(ridge_04, ridge_13, "south")
    area.exit(ridge_13, ridge_04, "north")
    area.exit(ridge_12, ridge_14, "south")
    area.exit(ridge_14, ridge_12, "north")
    area.exit(ridge_15, ridge_03, "south")
    area.exit(ridge_03, ridge_15, "north")

    # -- Ridge spawns --
    area.spawn(ridge_01, "ash_wolf", count_min=1, count_max=2,
               respawn_minutes=12, respawn_variance=4)
    area.spawn(ridge_03, "ash_wolf", count_min=2, count_max=3,
               respawn_minutes=12, respawn_variance=4)
    area.spawn(ridge_04, "ash_wolf", count_min=1, count_max=2,
               respawn_minutes=12, respawn_variance=4)
    area.spawn(ridge_05, "ash_wolf", count_min=2, count_max=3,
               respawn_minutes=10, respawn_variance=3)
    area.spawn(ridge_08, "ash_wolf", count_min=1, count_max=2,
               respawn_minutes=10, respawn_variance=3)
    area.spawn(ridge_10, "ash_wolf", count_min=1, count_max=1,
               respawn_minutes=15, respawn_variance=5)
    area.spawn(ridge_11, "steppe_hawk", count_min=1, count_max=1,
               respawn_minutes=20, respawn_variance=5)
    area.spawn(ridge_13, "ash_wolf", count_min=1, count_max=1,
               respawn_minutes=15, respawn_variance=5)

    # -- Named mob (D-20): Alpha Ash Wolf --
    area.named_mob(
        "alpha_ash_wolf", ridge_09,
        respawn_minutes=120,
        respawn_variance=30,
        prestige_modifier=2.0,
        behavior=["pack_leader"],
        base_disposition=-0.8,
        flee_threshold=5,
        tome_drop="ashreach_pack_alpha_tome",
    )

    # ==================================================================
    #  REGION 5: BANDIT'S HOLLOW (~18 rooms)
    #  A concealed ravine southwest of the road. Bandit encampment.
    # ==================================================================

    bandit_01 = area.room(
        "bandit_01",
        name="Bandit's Hollow - Scrub Approach",
        desc=(
            "Dense thornbush and tall grass conceal a narrow track leading "
            "southwest from the road. Boot prints and broken branches mark "
            "the path of regular foot traffic. Someone has been cutting "
            "a way through the scrub."
        ),
        room_type="path",
        indoor=False,
    )

    bandit_02 = area.room(
        "bandit_02",
        name="Bandit's Hollow - Hidden Track",
        desc=(
            "The track descends into a shallow ravine, the walls rising "
            "on both sides. The thornbush closes in overhead, creating "
            "a tunnel of sorts. The light dims. Discarded apple cores and "
            "gnawed bone suggest someone camps nearby."
        ),
        room_type="path",
        indoor=False,
    )

    bandit_03 = area.room(
        "bandit_03",
        name="Bandit's Hollow - Ravine Bend",
        desc=(
            "The ravine curves sharply, blocking sightlines in both "
            "directions. A natural defensive position -- anyone rounding "
            "the corner would be exposed. Scuff marks on the ravine wall "
            "suggest someone climbs up here to keep watch."
        ),
        room_type="path",
        indoor=False,
    )

    bandit_04 = area.room(
        "bandit_04",
        name="Bandit's Hollow - Sentry Post",
        desc=(
            "A flat rock overlooking the ravine approach, with a crude "
            "lean-to of branches for shade. A wooden stool and a jug of "
            "stale water sit beside the rock. Dried mud has been scraped "
            "from boot soles onto the stone."
        ),
        room_type="clearing",
        indoor=False,
    )

    bandit_05 = area.room(
        "bandit_05",
        name="Bandit's Hollow - Camp Edge",
        desc=(
            "The ravine opens into a wider hollow, partly hidden by "
            "overhanging scrub and a jutting rock shelf. The smell of "
            "woodsmoke and unwashed bodies drifts from further in. "
            "Crude rope lines stretch between posts for drying clothes."
        ),
        room_type="clearing",
        indoor=False,
    )

    bandit_06 = area.room(
        "bandit_06",
        name="Bandit's Hollow - Central Camp",
        desc=(
            "The heart of the bandit encampment. A fire pit surrounded "
            "by logs and flat stones serves as the gathering point. "
            "Bedrolls and canvas shelters ring the fire. Stolen goods "
            "are stacked in haphazard piles -- crates, barrels, a few "
            "bolts of cloth with Consortium stamps."
        ),
        room_type="clearing",
        indoor=False,
        ambient_echoes=[
            "Embers crackle in the fire pit.",
            "Rough laughter comes from one of the canvas shelters.",
            "A stolen chicken clucks nervously in a makeshift pen.",
        ],
    )

    bandit_07 = area.room(
        "bandit_07",
        name="Bandit's Hollow - Supply Cache",
        desc=(
            "A shallow cave in the ravine wall, its opening screened by "
            "a canvas flap. Inside, barrels of water, sacks of grain, "
            "and bundles of dried meat are stacked neatly. The bandits "
            "are well-provisioned -- this is no desperate hideout."
        ),
        room_type="cave",
        indoor=True,
    )

    bandit_08 = area.room(
        "bandit_08",
        name="Bandit's Hollow - Weapon Rack",
        desc=(
            "A section of camp dedicated to arms. A crude wooden rack "
            "holds swords, axes, and crossbow bolts. A grinding stone "
            "sits nearby, its surface worn smooth. The weapons are "
            "mismatched but serviceable -- stolen from travelers and "
            "patrols."
        ),
        room_type="clearing",
        indoor=False,
    )

    bandit_09 = area.room(
        "bandit_09",
        name="Bandit's Hollow - Leader's Tent",
        desc=(
            "The largest shelter in camp -- an actual tent of oiled "
            "canvas, with a cot, a chest, and a crude table. A map "
            "of the Ashway is pinned to the tent pole, with Xs marking "
            "what must be ambush points. The chest has a heavy iron lock."
        ),
        room_type="building",
        indoor=True,
    )

    bandit_10 = area.room(
        "bandit_10",
        name="Bandit's Hollow - Prisoner Pit",
        desc=(
            "A deep hole dug into the ravine floor, covered with a "
            "wooden grate. It is empty now, but rope marks on the grate "
            "and scratches on the pit walls tell their own story. A "
            "bucket sits beside the pit -- the prisoners' only comfort."
        ),
        room_type="clearing",
        indoor=False,
    )

    bandit_11 = area.room(
        "bandit_11",
        name="Bandit's Hollow - Back Exit",
        desc=(
            "A narrow crack in the ravine wall, just wide enough for "
            "a person to squeeze through sideways. This is the camp's "
            "escape route -- a quick path to the open grassland if "
            "the front entrance is compromised."
        ),
        room_type="path",
        indoor=False,
    )

    bandit_12 = area.room(
        "bandit_12",
        name="Bandit's Hollow - Cooking Fire",
        desc=(
            "A separate fire pit for cooking, set apart from the main "
            "camp to manage smoke. A spit holds the remains of something "
            "charred. Pots and pans, most dented, hang from a frame of "
            "bound sticks."
        ),
        room_type="clearing",
        indoor=False,
    )

    bandit_13 = area.room(
        "bandit_13",
        name="Bandit's Hollow - Lookout Bluff",
        desc=(
            "A scramble up the ravine wall leads to a concealed bluff "
            "overlooking the grassland to the east. From here, the "
            "Ashway is visible as a pale line through the grass. "
            "Approaching travelers can be spotted a league away."
        ),
        room_type="clearing",
        indoor=False,
    )

    bandit_14 = area.room(
        "bandit_14",
        name="Bandit's Hollow - Gambling Corner",
        desc=(
            "A flat stone serves as a card table, surrounded by "
            "overturned crates for seats. Carved bone dice and greasy "
            "playing cards litter the surface. Small piles of copper "
            "coins and buttons mark recent wagers."
        ),
        room_type="clearing",
        indoor=False,
    )

    bandit_15 = area.room(
        "bandit_15",
        name="Bandit's Hollow - Latrine Trench",
        desc=(
            "The least pleasant corner of camp. A trench dug into the "
            "earth, screened by a canvas sheet that provides minimal "
            "privacy and no dignity. Lime dust is scattered along the "
            "edges in a half-hearted attempt at sanitation."
        ),
        room_type="clearing",
        indoor=False,
    )

    bandit_16 = area.room(
        "bandit_16",
        name="Bandit's Hollow - Old Mine Entrance",
        desc=(
            "Behind the camp, an old mine shaft opens in the ravine "
            "wall. The timbers are rotting and the entrance is partially "
            "collapsed. A faint draft blows from within, carrying the "
            "smell of wet earth and rust. The bandits seem to avoid it."
        ),
        room_type="cave",
        indoor=True,
    )

    bandit_17 = area.room(
        "bandit_17",
        name="Old Mine - Shallow Gallery",
        desc=(
            "A short tunnel into the hillside, roughly hewn from grey "
            "stone. Iron ore veins are visible in the walls -- reddish "
            "streaks that someone once followed into the earth. The "
            "mining stopped abruptly -- tools still hang on a wall peg."
        ),
        room_type="cave",
        indoor=True,
    )

    bandit_18 = area.room(
        "bandit_18",
        name="Old Mine - Dead End",
        desc=(
            "The mine tunnel ends in a cave-in. Rubble fills the passage "
            "from floor to ceiling. Among the fallen stone, something "
            "glints -- iron ore, dense and rich, exposed by the collapse. "
            "The draft still whistles through cracks in the debris."
        ),
        room_type="cave",
        indoor=True,
    )

    # -- Bandit exits --
    area.exit(ash_road_10, bandit_01, "southwest")
    area.exit(bandit_01, ash_road_10, "northeast")
    area.exit(bandit_01, bandit_02, "south")
    area.exit(bandit_02, bandit_01, "north")
    area.exit(bandit_02, bandit_03, "south")
    area.exit(bandit_03, bandit_02, "north")
    area.exit(bandit_03, bandit_04, "up")
    area.exit(bandit_04, bandit_03, "down")
    area.exit(bandit_03, bandit_05, "south")
    area.exit(bandit_05, bandit_03, "north")
    area.exit(bandit_05, bandit_06, "south")
    area.exit(bandit_06, bandit_05, "north")
    area.exit(bandit_06, bandit_07, "west")
    area.exit(bandit_07, bandit_06, "east")
    area.exit(bandit_06, bandit_08, "east")
    area.exit(bandit_08, bandit_06, "west")
    area.exit(bandit_06, bandit_09, "south")
    area.exit(bandit_09, bandit_06, "north")
    area.exit(bandit_09, bandit_10, "west")
    area.exit(bandit_10, bandit_09, "east")
    area.exit(bandit_09, bandit_11, "south")
    area.exit(bandit_11, bandit_09, "north")
    area.exit(bandit_11, grass_10, "out")
    area.exit(grass_10, bandit_11, "in")
    area.exit(bandit_05, bandit_12, "east")
    area.exit(bandit_12, bandit_05, "west")
    area.exit(bandit_04, bandit_13, "up")
    area.exit(bandit_13, bandit_04, "down")
    area.exit(bandit_08, bandit_14, "south")
    area.exit(bandit_14, bandit_08, "north")
    area.exit(bandit_12, bandit_15, "south")
    area.exit(bandit_15, bandit_12, "north")
    area.exit(bandit_14, bandit_16, "east")
    area.exit(bandit_16, bandit_14, "west")
    area.exit(bandit_16, bandit_17, "in")
    area.exit(bandit_17, bandit_16, "out")
    area.exit(bandit_17, bandit_18, "south")
    area.exit(bandit_18, bandit_17, "north")

    # -- Bandit spawns --
    area.spawn(bandit_03, "ashreach_bandit", count_min=1, count_max=1,
               respawn_minutes=20, respawn_variance=5)
    area.spawn(bandit_04, "ashreach_bandit", count_min=1, count_max=1,
               respawn_minutes=20, respawn_variance=5)
    area.spawn(bandit_05, "ashreach_bandit", count_min=1, count_max=2,
               respawn_minutes=15, respawn_variance=5)
    area.spawn(bandit_06, "ashreach_bandit", count_min=2, count_max=3,
               respawn_minutes=15, respawn_variance=5)
    area.spawn(bandit_08, "ashreach_bandit", count_min=1, count_max=2,
               respawn_minutes=15, respawn_variance=5)
    area.spawn(bandit_12, "ashreach_bandit", count_min=1, count_max=1,
               respawn_minutes=20, respawn_variance=5)
    area.spawn(bandit_14, "ashreach_bandit", count_min=1, count_max=1,
               respawn_minutes=20, respawn_variance=5)
    area.spawn(bandit_13, "ashreach_bandit", count_min=1, count_max=1,
               respawn_minutes=25, respawn_variance=5)
    area.spawn(bandit_17, "dust_beetle", count_min=1, count_max=2,
               respawn_minutes=12, respawn_variance=4)

    # ==================================================================
    #  REGION 6: WARDEN OUTPOST (~16 rooms)
    #  Ranger station on the eastern trails. NPCs, quest hooks.
    # ==================================================================

    outpost_01 = area.room(
        "outpost_01",
        name="Eastern Trail - Junction",
        desc=(
            "A well-maintained trail branches east from the Ashway, "
            "marked by a carved wooden sign reading 'Warden Outpost "
            "Ashreach -- 1/4 league'. The trail is narrower than the "
            "road but clear and well-trodden."
        ),
        room_type="path",
        indoor=False,
    )

    outpost_02 = area.room(
        "outpost_02",
        name="Eastern Trail - Patrol Path",
        desc=(
            "The trail follows a gentle contour along a low ridge. "
            "Boot prints -- all the same make, regulation Imperial "
            "issue -- march in both directions. A trail marker painted "
            "with the Warden's green-and-brown crest stands at a bend."
        ),
        room_type="path",
        indoor=False,
    )

    outpost_03 = area.room(
        "outpost_03",
        name="Eastern Trail - Stream Crossing",
        desc=(
            "A small stream crosses the trail here, bridged by a pair "
            "of flat logs. The water is shallow but clear. Watercress "
            "grows along the banks. A wooden bucket on a rope suggests "
            "the outpost draws water here."
        ),
        room_type="path",
        indoor=False,
    )

    outpost_04 = area.room(
        "outpost_04",
        name="Warden Outpost - Gate",
        desc=(
            "A simple wooden gate set between two stout posts marks the "
            "entrance to the Warden outpost. The posts are carved with "
            "the Warden emblem -- a hawk over crossed arrows. A bell "
            "hangs from a rope for visitors to announce themselves."
        ),
        room_type="building",
        indoor=False,
    )

    outpost_05 = area.room(
        "outpost_05",
        name="Warden Outpost - Yard",
        desc=(
            "A packed-earth yard surrounded by low wooden buildings. "
            "A training post stands in one corner, its surface hacked "
            "to splinters. A watering trough and hitching rail serve "
            "the outpost's few horses. The place is functional, clean, "
            "and austere."
        ),
        room_type="building",
        indoor=False,
        ambient_echoes=[
            "A warden sharpens a blade on a whetstone.",
            "Horses stamp and snort in their stalls.",
        ],
    )

    outpost_06 = area.room(
        "outpost_06",
        name="Warden Outpost - Barracks",
        desc=(
            "A long, low building with a row of cots along each wall. "
            "Gear is stored in footlockers. Maps and patrol schedules "
            "are pinned to a board near the door. The room smells of "
            "leather, oil, and the sharp herbs wardens use to keep "
            "vermin out of their bedrolls."
        ),
        room_type="building",
        indoor=True,
    )

    outpost_07 = area.room(
        "outpost_07",
        name="Warden Outpost - Commander's Office",
        desc=(
            "A small room with a heavy desk and a single chair. Maps "
            "of the Ashreach cover every wall, marked with patrol routes "
            "and animal sighting pins. A detailed log book lies open on "
            "the desk. The entries are recent and meticulous."
        ),
        room_type="building",
        indoor=True,
    )

    outpost_08 = area.room(
        "outpost_08",
        name="Warden Outpost - Watch Tower",
        desc=(
            "A wooden tower rises above the outpost, offering a "
            "commanding view of the surrounding plains. A spyglass "
            "is mounted on a swivel. Signal flags and a lantern for "
            "night signals hang from pegs. The platform sways slightly "
            "in the wind."
        ),
        room_type="building",
        indoor=False,
    )

    outpost_09 = area.room(
        "outpost_09",
        name="Warden Outpost - Supply Shed",
        desc=(
            "A sturdy shed stocked with field supplies -- rope, "
            "bandages, dried rations, signal flares, and wolf traps. "
            "Everything is organized with military precision. A notice "
            "on the door reads 'Inventory checked weekly'."
        ),
        room_type="building",
        indoor=True,
    )

    outpost_10 = area.room(
        "outpost_10",
        name="Warden Outpost - Stable",
        desc=(
            "A three-stall stable, currently housing two lean horses "
            "with the Warden brand. Hay and oats are stored in a loft "
            "above. The horses eye visitors with the calm confidence "
            "of well-trained mounts."
        ),
        room_type="building",
        indoor=True,
    )

    outpost_11 = area.room(
        "outpost_11",
        name="Eastern Trail - Clifftop View",
        desc=(
            "The trail reaches a clifftop overlook. Far to the east, "
            "the plains give way to a shimmering line that might be "
            "distant water -- the northeastern coast of Varath. The "
            "wind is fiercer here, tugging at clothes and hair."
        ),
        room_type="clearing",
        indoor=False,
    )

    outpost_12 = area.room(
        "outpost_12",
        name="Eastern Trail - Descent",
        desc=(
            "The trail descends eastward in a series of switchbacks "
            "carved into the hillside. The terrain is changing -- "
            "rockier, with salt-tolerant scrub replacing the grassland. "
            "The coast zone lies ahead."
        ),
        room_type="path",
        indoor=False,
    )

    outpost_13 = area.room(
        "outpost_13",
        name="Hermit's Hill - Path",
        desc=(
            "A faint side trail climbs a rocky hillock set apart from "
            "the main path. Cairns of stacked stones mark the way at "
            "intervals. Someone has lived here long enough to build "
            "a path."
        ),
        room_type="path",
        indoor=False,
    )

    outpost_14 = area.room(
        "outpost_14",
        name="Hermit's Hill - Summit",
        desc=(
            "A flat-topped hillock with a panoramic view of the Ashreach. "
            "A small stone hut, barely more than four walls and a slab "
            "roof, sits beneath a weathered thornwood tree. Books and "
            "scrolls are visible through the open doorway. The air "
            "smells of pipe smoke and old paper."
        ),
        room_type="building",
        indoor=False,
    )

    outpost_15 = area.room(
        "outpost_15",
        name="Hermit's Hut",
        desc=(
            "A cramped stone hut packed with books, scrolls, and crude "
            "drawings pinned to every surface. A narrow cot is pushed "
            "against one wall. The drawings show geometric patterns -- "
            "octagons, spirals, base-eight number sequences -- copied "
            "from the Drystone Ruins."
        ),
        room_type="building",
        indoor=True,
    )

    outpost_16 = area.room(
        "outpost_16",
        name="Eastern Trail - Forest Edge",
        desc=(
            "The eastern trail's westward branch leads into thickening "
            "scrub that gradually becomes proper forest. The air is "
            "cooler here, sheltered from the Ashreach wind. The canopy "
            "closes overhead."
        ),
        room_type="path",
        indoor=False,
    )

    # -- Outpost exits --
    area.exit(ash_road_08, outpost_01, "east")
    area.exit(outpost_01, ash_road_08, "west")
    area.exit(outpost_01, outpost_02, "east")
    area.exit(outpost_02, outpost_01, "west")
    area.exit(outpost_02, outpost_03, "east")
    area.exit(outpost_03, outpost_02, "west")
    area.exit(outpost_03, outpost_04, "east")
    area.exit(outpost_04, outpost_03, "west")
    area.exit(outpost_04, outpost_05, "east")
    area.exit(outpost_05, outpost_04, "west")
    area.exit(outpost_05, outpost_06, "north")
    area.exit(outpost_06, outpost_05, "south")
    area.exit(outpost_05, outpost_07, "east")
    area.exit(outpost_07, outpost_05, "west")
    area.exit(outpost_05, outpost_08, "up")
    area.exit(outpost_08, outpost_05, "down")
    area.exit(outpost_05, outpost_09, "south")
    area.exit(outpost_09, outpost_05, "north")
    area.exit(outpost_06, outpost_10, "east")
    area.exit(outpost_10, outpost_06, "west")
    area.exit(outpost_07, outpost_11, "east")
    area.exit(outpost_11, outpost_07, "west")
    area.exit(outpost_11, outpost_12, "east")
    area.exit(outpost_12, outpost_11, "west")
    area.exit(outpost_02, outpost_13, "north")
    area.exit(outpost_13, outpost_02, "south")
    area.exit(outpost_13, outpost_14, "north")
    area.exit(outpost_14, outpost_13, "south")
    area.exit(outpost_14, outpost_15, "in")
    area.exit(outpost_15, outpost_14, "out")
    area.exit(outpost_01, outpost_16, "northwest")
    area.exit(outpost_16, outpost_01, "southeast")

    # -- Cross-zone exits (D-25) --
    area.exit(outpost_12, "coastal_zone:coast_entry", "east")     # east to coast
    area.exit(outpost_16, "cantera_forest:forest_entry", "west")  # west to forest
    area.exit(ash_road_16, "coastal_zone:coast_crossroads", "east")  # crossroads east

    # -- Outpost spawns --
    area.spawn(outpost_02, "plains_viper", count_min=1, count_max=1,
               respawn_minutes=20, respawn_variance=5)
    area.spawn(outpost_11, "steppe_hawk", count_min=1, count_max=1,
               respawn_minutes=20, respawn_variance=5)
    area.spawn(outpost_13, "dust_beetle", count_min=1, count_max=1,
               respawn_minutes=15, respawn_variance=5)
    area.spawn(outpost_03, "dust_beetle", count_min=1, count_max=1,
               respawn_minutes=15, respawn_variance=5)
    area.spawn(outpost_16, "ash_wolf", count_min=1, count_max=1,
               respawn_minutes=15, respawn_variance=5)

    # -- Additional grassland and road spawns for density target --
    area.spawn(grass_03, "plains_viper", count_min=1, count_max=1,
               respawn_minutes=20, respawn_variance=5)
    area.spawn(grass_05, "steppe_hawk", count_min=1, count_max=1,
               respawn_minutes=20, respawn_variance=5)
    area.spawn(grass_10, "ash_wolf", count_min=1, count_max=1,
               respawn_minutes=15, respawn_variance=5)
    area.spawn(grass_13, "dust_beetle", count_min=1, count_max=2,
               respawn_minutes=12, respawn_variance=4)
    area.spawn(grass_15, "ash_wolf", count_min=1, count_max=1,
               respawn_minutes=15, respawn_variance=5)
    area.spawn(grass_18, "dust_beetle", count_min=1, count_max=1,
               respawn_minutes=12, respawn_variance=4)
    area.spawn(ash_road_04, "dust_beetle", count_min=1, count_max=1,
               respawn_minutes=15, respawn_variance=5)
    area.spawn(ash_road_15, "plains_viper", count_min=1, count_max=1,
               respawn_minutes=20, respawn_variance=5)

    # ==================================================================
    #  NPCs (D-22, D-23: field NPCs with quest stubs)
    # ==================================================================

    # NPC 1: Warden Ranger at the outpost
    area.npc(outpost_07, "npc_warden_captain_ashwyn", faction="wardens")

    # NPC 2: Hermit scholar near the ruins
    area.npc(outpost_15, "npc_hermit_scholar_obed", faction=None)

    # NPC 3: Traveling merchant on the Ashway
    area.npc(ash_road_09, "npc_merchant_reva", faction="consortium")

    # ==================================================================
    #  QUESTS (enriched specs — D-21/D-22)
    # ==================================================================

    area.quest(
        "ashreach_wolf_overpopulation",
        name="Wolf Cull",
        description="Captain Ashwyn reports the ash wolf packs are growing bolder, threatening travelers on the Ashway. The beasts have lost their fear of fire and steel alike. Thin their numbers before someone gets killed.",
        quest_type="kill",
        quest_giver="npc_warden_captain_ashwyn",
        objectives=[
            {"type": "kill", "target": "ash_wolf", "count": 10,
             "description": "Cull ash wolves on the plains"},
        ],
        rewards=[
            {"action_type": "give_scales", "amount": 80},
            {"action_type": "modify_standing", "faction_id": "wardens", "delta": 200},
            {"action_type": "echo", "message": "|gAshwyn marks your tally with grim satisfaction. \"Good hunting. The Ashway will be safer for it -- but I've another matter, if you're willing.\"|n"},
        ],
        next_quest_id="ashreach_bandit_problem",
        # Legacy fields (backward compat)
        objective_type="kill",
        objective_target="ash_wolf",
        objective_count=10,
        reward_tiers={},
        consequence_small="Warden standing gain",
        consequence_medium="Wolf population decrease, safer Ashreach travel",
    )

    area.quest(
        "ashreach_bandit_problem",
        name="Ashway Brigands",
        description="With the wolves thinned, Ashwyn turns to the next problem: bandits have established a camp near the old trade route. They prey on merchants and refugees alike, and the Wardens are spread too thin to deal with them.",
        quest_type="kill",
        quest_giver="npc_warden_captain_ashwyn",
        objectives=[
            {"type": "kill", "target": "ashreach_bandit", "count": 6,
             "description": "Eliminate Ashreach bandits along the Ashway"},
        ],
        rewards=[
            {"action_type": "give_scales", "amount": 100},
            {"action_type": "modify_standing", "faction_id": "wardens", "delta": 300},
            {"action_type": "give_skill_xp", "skill_id": "combat", "count": 3},
            {"action_type": "echo", "message": "|gAshwyn clasps your arm in the Warden salute. \"The Ashway breathes easier tonight. You've done the Wardens a true service.\"|n"},
        ],
        # Legacy fields (backward compat)
        objective_type="kill",
        objective_target="ashreach_bandit",
        objective_count=6,
        reward_tiers={},
        consequence_small="Warden standing gain",
        consequence_medium="Bandit camp weakened, Ashway safer",
    )

    area.quest(
        "ashreach_ruin_investigation",
        name="Voices in the Dust",
        description="Scholar Obed believes the wind-worn ruins scattered across the plains hold records of a civilization that predates the Dragon Empire. The inscriptions are fading fast -- document what remains before the ash-winds erase them entirely.",
        quest_type="investigate",
        quest_giver="npc_hermit_scholar_obed",
        objectives=[
            {"type": "investigate", "target": "ashreach_ancient_ruins", "count": 3,
             "description": "Investigate ancient ruin sites on the Ashreach plains"},
        ],
        rewards=[
            {"action_type": "give_scales", "amount": 70},
            {"action_type": "give_skill_xp", "skill_id": "investigation", "count": 5},
            {"action_type": "echo", "message": "|gObed's eyes widen as he reads your rubbings. \"Remarkable. These glyphs predate everything in my collection. The world was old before the dragons came, it seems.\"|n"},
        ],
        # Legacy fields (backward compat)
        objective_type="discover",
        objective_target="lore_fragment",
        objective_count=3,
        reward_tiers={},
        consequence_small="Scholar's gratitude, lore insight",
        consequence_medium="Knowledge of pre-Imperial civilization",
    )

    # ==================================================================
    #  ROOM STATE FLAGS (D-30)
    #  Using existing FLAG_VOCABULARY entries only.
    # ==================================================================

    # Ruins have lingering ancient presence (discoverable by Sense)
    # These are set as initial room state via room db attributes.
    # The room_state system handles display; we set initial flags here.
    ruins_13.db.initial_room_flags = {
        "resonant": {"duration": -1},       # permanent, discoverable
        "ancient_presence": {"duration": -1},  # permanent, discoverable
    }
    ruins_04.db.initial_room_flags = {
        "resonant": {"duration": -1},
    }
    ruins_06.db.initial_room_flags = {
        "resonant": {"duration": -1},
    }
    # Ash circle has a visible resonant quality
    grass_12.db.initial_room_flags = {
        "resonant": {"duration": -1},
    }

    # ==================================================================
    #  TRAINER NPCs (09-02: wilderness trainers)
    # ==================================================================

    # Fishing trainer near stream crossing
    area.npc(
        outpost_03, "npc_trainer_fishing_ashreach",
        name="Neddra",
        title="Fishing Instructor",
        desc="A weathered woman with sun-darkened skin sits on the bank, mending a fishing net with practiced fingers. Several rods lean against a rock beside her, each rigged differently.",
        faction=None,
        trainer_id="npc_trainer_fishing_ashreach",
        dialogue={"greeting": "Neddra glances at your empty hands. 'Heading through the plains without knowing how to fish? The rivers here are generous if you know where to cast. I can show you, for a fair price.'", "topics": {"fish": "'The silverscale trout run heavy in spring. Use grubs, not worms -- the trout here are picky. And stay upstream of the ashfall zones. The fish there taste like sulfur.'"}},
    )

    # Herbalism trainer in the grasslands
    area.npc(
        grass_03, "npc_trainer_herbalism_ashreach",
        name="Senna",
        title="Plains Herbalist",
        desc="A young woman kneels among the grasses, carefully separating dried stalks into bundles. Her satchel overflows with cuttings. She hums tunelessly as she works.",
        faction="wardens",
        trainer_id="npc_trainer_herbalism_ashreach",
        dialogue={"greeting": "Senna looks up with grass-stained fingers. 'The ashreach grasses look dead but they are not. Half these stalks have medicinal properties if you know how to prepare them. Want me to show you?'", "topics": {"herbs": "'Ash sage grows where the soil is darkest -- near old burn patches. Bittervine clings to rocks along the ridgeline. And never eat the red-tipped grass. It looks like everything else but it will put you down for days.'"}},
    )

    # ==================================================================
    #  TRIGGERS (09-02: zone entry and atmospheric)
    # ==================================================================

    # Zone entry — first visit atmospheric welcome
    area.trigger(
        ash_road_01, "on_first_visit",
        [{"action_type": "echo", "message": "|yThe wind carries the scent of ash and dry grass. The Ashreach stretches before you -- an endless expanse of golden plains scarred by ancient fires. In the distance, smoke rises from what might be a campfire or another burn.|n"}],
        trigger_id="ashreach_first_entry",
        once_per_character=True,
    )

    # ==================================================================
    #  BUILD
    # ==================================================================

    return area.build()
