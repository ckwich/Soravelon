"""
The Reth Foothills -- Starter Zone 2

A rugged mountain foothills zone north of Vael's Crossing where the
Ashreach plains give way to the grey teeth of The Reth -- Varath's
north-south mountain spine. Rocky switchbacks, cave networks, abandoned
mine shafts, and windswept overlooks.

100+ rooms across 8 sub-areas, 5 mob types, 1 named mob, 3 field NPCs.
No levels -- zone scaling makes all content universal.

Sub-areas:
    1. Rethward Approach   (~12 rooms) -- Transition from plains, road north
    2. Lower Switchbacks   (~14 rooms) -- Rocky paths ascending into foothills
    3. Greystone Mine      (~14 rooms) -- Abandoned mine shafts, underground
    4. Cave Networks       (~16 rooms) -- Branching cave system, spider dens
    5. Western Ridge       (~12 rooms) -- High paths, eagle territory
    6. Mountain Overlooks  (~10 rooms) -- Scenic viewpoints, golem fragments
    7. The Deepcavern      (~12 rooms) -- Deep cave, named mob lair
    8. Eastern Descent     (~12 rooms) -- Connects to forest zone westward
"""

from world.area_builder import AreaBuilder


def build():
    area = AreaBuilder("reth_foothills")

    # ------------------------------------------------------------------
    # Zone setup
    # ------------------------------------------------------------------
    area.zone(
        name="The Reth Foothills",
        zone_type="mountain",
        continent="varath",
        faction_territory="imperial",
        faction_presence=["empire", "consortium", "wardens"],
        world_x=0,
        world_y=50,
        world_radius=60,
    )

    # ==================================================================
    #  SUB-AREA 1: RETHWARD APPROACH (~12 rooms)
    #  Transition from Ashreach plains into foothills. Rocky terrain
    #  begins, the road narrows, and the mountains loom ahead.
    # ==================================================================

    ra_road_south = area.room(
        "ra_road_south",
        name="Rethward Pass - Southern Terminus",
        desc=(
            "The wide dirt road from Vael's Crossing narrows here as the "
            "flat Ashreach gives way to broken ground. Loose shale crunches "
            "underfoot. Ahead, the foothills of The Reth rise in grey-brown "
            "ridges, each higher than the last, building toward the jagged "
            "peaks that locals call the Greyteeth. Mile markers -- Imperial "
            "stone pillars with distances scratched in the old reckoning -- "
            "stand at intervals along the road."
        ),
        room_type="path",
        indoor=False,
        ambient_echoes=[
            "Wind sweeps down from the mountains, carrying the smell of cold stone.",
            "A loose rock clatters downhill, dislodged by nothing visible.",
            "Far ahead, a hawk circles above the ridgeline.",
        ],
    )

    ra_scrub_flat = area.room(
        "ra_scrub_flat",
        name="Scrubland Flat",
        desc=(
            "A stretch of flat ground between the road and the first "
            "true ridge. Hardy scrub bushes and grey-green thornweed "
            "cling to thin soil over rock. Animal tracks -- something "
            "large and clawed -- cross the ground in dried mud. The "
            "air is drier here than on the plains, thinner."
        ),
        room_type="clearing",
        indoor=False,
    )

    ra_old_camp = area.room(
        "ra_old_camp",
        name="Abandoned Campsite",
        desc=(
            "A fire ring of blackened stones sits in a sheltered hollow "
            "between two boulders. Someone camped here not long ago -- "
            "the ashes are relatively fresh. A tent stake still protrudes "
            "from the ground, the canvas long gone. Empty provision tins "
            "are scattered nearby, gnawed by animals."
        ),
        room_type="clearing",
        indoor=False,
        ambient_echoes=[
            "Something rustles in the scrub beyond the boulders.",
        ],
    )

    ra_ridge_base = area.room(
        "ra_ridge_base",
        name="Ridge Base",
        desc=(
            "The first true ridge of The Reth rises sharply here -- a "
            "wall of grey stone and loose scree. The road cuts north "
            "along the base of the ridge, following a natural shelf. "
            "To the east, the ground drops away into a dry ravine "
            "choked with dead thornbush."
        ),
        room_type="path",
        indoor=False,
    )

    ra_ravine_edge = area.room(
        "ra_ravine_edge",
        name="Ravine Edge",
        desc=(
            "The lip of a dry ravine, twenty feet deep, cut by ancient "
            "water that no longer flows. The walls are layered stone -- "
            "pale bands of limestone alternating with darker iron-rich "
            "rock. At the bottom, bleached bones of some large animal "
            "are half-buried in gravel."
        ),
        room_type="path",
        indoor=False,
    )

    ra_road_bend = area.room(
        "ra_road_bend",
        name="Rethward Pass - First Bend",
        desc=(
            "The road turns sharply here, following the contour of the "
            "hillside. A crude wooden sign has been nailed to a post: "
            "'GREYSTONE -- 2 LEAGUES.' The paint is peeling and the "
            "arrow points northwest. Below the sign, someone has "
            "scratched in charcoal: 'TROLLS.'"
        ),
        room_type="path",
        indoor=False,
    )

    ra_boulder_field = area.room(
        "ra_boulder_field",
        name="Boulder Field",
        desc=(
            "House-sized boulders litter the slope here, tumbled down "
            "from the ridge above in some ancient landslide. The spaces "
            "between them form narrow passages -- some barely wide enough "
            "to squeeze through. Moss grows thick on the north-facing "
            "sides. The ground is permanently damp in the shadows."
        ),
        room_type="path",
        indoor=False,
        ambient_echoes=[
            "Water drips somewhere between the boulders.",
            "A mountain cat's yowl echoes from the ridge above -- distant but distinct.",
        ],
    )

    ra_spring = area.room(
        "ra_spring",
        name="Mountain Spring",
        desc=(
            "A clear spring bubbles up from between rocks at the base of "
            "a boulder, collecting in a shallow natural basin before "
            "trickling away downhill. The water is ice-cold and tastes "
            "of minerals. Animal tracks are thick around the pool -- "
            "this is a watering hole for everything on the lower slopes."
        ),
        room_type="clearing",
        indoor=False,
        ambient_echoes=[
            "The spring gurgles softly, a constant sound.",
            "A bird calls from a stunted pine nearby.",
        ],
    )

    ra_warden_camp = area.room(
        "ra_warden_camp",
        name="Warden Patrol Camp",
        desc=(
            "A small, orderly camp set up in the lee of a rock outcrop. "
            "Two canvas tents, a banked fire, and a rope line with drying "
            "jerky strung between two iron stakes. Warden insignia -- a "
            "silver dragon wing on green -- is stitched into the tent "
            "flaps. A patrol log book sits on a flat stone near the fire, "
            "weighted down by a river rock."
        ),
        room_type="clearing",
        indoor=False,
    )

    ra_road_north = area.room(
        "ra_road_north",
        name="Rethward Pass - Northern Stretch",
        desc=(
            "The road climbs steadily here, the footing increasingly "
            "uncertain as loose gravel replaces packed dirt. The views "
            "open up -- to the south, the Ashreach stretches to the "
            "horizon, a brown smear under haze. To the north, the "
            "switchbacks of the upper foothills are visible, cutting "
            "back and forth across the mountainside like scars."
        ),
        room_type="path",
        indoor=False,
    )

    ra_fallen_pine = area.room(
        "ra_fallen_pine",
        name="Fallen Pine Crossing",
        desc=(
            "A massive dead pine has fallen across the path, its root "
            "ball torn from the hillside by some storm. The trunk is "
            "wide enough to walk on, if you trust your balance. Someone "
            "has hacked a narrow passage through the branches on the "
            "uphill side. Pine resin still oozes from the cut marks."
        ),
        room_type="path",
        indoor=False,
    )

    ra_lookout_rock = area.room(
        "ra_lookout_rock",
        name="Lookout Rock",
        desc=(
            "A flat-topped boulder juts out from the hillside, offering "
            "an unobstructed view of the approach road and the plains "
            "beyond. Scratched into the rock surface are tally marks -- "
            "hundreds of them, grouped in eights. Someone has been "
            "counting something from this vantage point for a very "
            "long time."
        ),
        room_type="path",
        indoor=False,
        ambient_echoes=[
            "The wind is constant up here, a low moan through the rocks.",
            "You can see the rooftops of Vael's Crossing far to the south.",
        ],
    )

    # Rethward Approach exits
    area.exit(ra_road_south, ra_scrub_flat, "east")
    area.exit(ra_scrub_flat, ra_road_south, "west")
    area.exit(ra_road_south, ra_road_bend, "north")
    area.exit(ra_road_bend, ra_road_south, "south")
    area.exit(ra_scrub_flat, ra_old_camp, "north")
    area.exit(ra_old_camp, ra_scrub_flat, "south")
    area.exit(ra_road_bend, ra_ridge_base, "east")
    area.exit(ra_ridge_base, ra_road_bend, "west")
    area.exit(ra_ridge_base, ra_ravine_edge, "east")
    area.exit(ra_ravine_edge, ra_ridge_base, "west")
    area.exit(ra_road_bend, ra_boulder_field, "west")
    area.exit(ra_boulder_field, ra_road_bend, "east")
    area.exit(ra_boulder_field, ra_spring, "north")
    area.exit(ra_spring, ra_boulder_field, "south")
    area.exit(ra_spring, ra_warden_camp, "east")
    area.exit(ra_warden_camp, ra_spring, "west")
    area.exit(ra_road_bend, ra_road_north, "north")
    area.exit(ra_road_north, ra_road_bend, "south")
    area.exit(ra_road_north, ra_fallen_pine, "northeast")
    area.exit(ra_fallen_pine, ra_road_north, "southwest")
    area.exit(ra_road_north, ra_lookout_rock, "east")
    area.exit(ra_lookout_rock, ra_road_north, "west")
    area.exit(ra_old_camp, ra_ridge_base, "northeast")
    area.exit(ra_ridge_base, ra_old_camp, "southwest")

    # Cross-zone exit south to Vael's Crossing
    area.exit(ra_road_south, "vaels_crossing:hg_north_road", "south", one_way=True)

    # ==================================================================
    #  SUB-AREA 2: LOWER SWITCHBACKS (~14 rooms)
    #  Rocky paths cutting back and forth up the mountainside.
    #  Mountain cats and rock trolls begin appearing.
    # ==================================================================

    ls_first_turn = area.room(
        "ls_first_turn",
        name="Lower Switchback - First Turn",
        desc=(
            "The path doubles back sharply, a crude retaining wall of "
            "stacked stones holding the uphill side in place. The footing "
            "is treacherous -- loose gravel over slick stone. Iron pitons "
            "have been hammered into the rock face at intervals, remnants "
            "of a rope guide that rotted away long ago."
        ),
        room_type="path",
        indoor=False,
    )

    ls_narrow_ledge = area.room(
        "ls_narrow_ledge",
        name="Narrow Ledge",
        desc=(
            "The path narrows to a ledge barely three feet wide, the "
            "mountainside dropping away to the right into a rocky gully "
            "far below. Claw marks score the stone wall to the left -- "
            "deep, parallel grooves from something large using this "
            "ledge as a scratching post."
        ),
        room_type="path",
        indoor=False,
        ambient_echoes=[
            "Small stones dislodge and rattle down the drop-off.",
            "A shadow passes overhead -- something with wings.",
        ],
    )

    ls_second_turn = area.room(
        "ls_second_turn",
        name="Lower Switchback - Second Turn",
        desc=(
            "Another hairpin turn. The retaining wall here has partially "
            "collapsed, spilling rocks across the path. Wild rosemary "
            "grows in the gaps between stones, its sharp scent released "
            "when crushed underfoot. A mountain cat's pawprint is pressed "
            "into dried mud at the turn's apex."
        ),
        room_type="path",
        indoor=False,
    )

    ls_goat_trail = area.room(
        "ls_goat_trail",
        name="Goat Trail",
        desc=(
            "A narrow side trail branches off the main switchback, "
            "following a route that only mountain goats would consider "
            "reasonable. The path is steep, barely visible, and littered "
            "with droppings. It climbs sharply toward a rocky shelf above."
        ),
        room_type="path",
        indoor=False,
    )

    ls_rocky_shelf = area.room(
        "ls_rocky_shelf",
        name="Rocky Shelf",
        desc=(
            "A natural shelf of stone, perhaps twenty feet across, "
            "overlooking the switchbacks below. Mountain goats have "
            "worn the surface smooth with generations of use. Tufts "
            "of coarse hair cling to the rock edges. The view is "
            "impressive -- the Ashreach spreads south, and the foothills "
            "fold away in grey-brown ridges to east and west."
        ),
        room_type="clearing",
        indoor=False,
    )

    ls_third_turn = area.room(
        "ls_third_turn",
        name="Lower Switchback - Third Turn",
        desc=(
            "The switchback rounds a massive outcrop of dark stone. "
            "The rock here is different from the surrounding grey -- "
            "almost black, with a glassy sheen. It feels warm to the "
            "touch even in cold weather. A vein of this dark rock runs "
            "up the mountainside like a scar."
        ),
        room_type="path",
        indoor=False,
        ambient_echoes=[
            "The dark stone hums faintly if you press your ear to it.",
        ],
    )

    ls_scree_slope = area.room(
        "ls_scree_slope",
        name="Scree Slope",
        desc=(
            "A wide slope of loose rock fragments -- scree -- that "
            "shifts and slides underfoot. Crossing it is slow and "
            "noisy. Every step sends a cascade of small stones "
            "rattling downhill. Anything living within earshot knows "
            "you are here."
        ),
        room_type="path",
        indoor=False,
    )

    ls_troll_hollow = area.room(
        "ls_troll_hollow",
        name="Troll Hollow",
        desc=(
            "A shallow depression between two ridges, the ground littered "
            "with cracked bones and the remains of small animals. The "
            "stench is unmistakable -- something large and unwashed lives "
            "here. Deep gouges in the surrounding rock suggest massive "
            "fingers gripping stone. The hollow is sheltered from wind "
            "but open to the sky."
        ),
        room_type="clearing",
        indoor=False,
        ambient_echoes=[
            "A deep, rumbling grunt echoes from somewhere nearby.",
            "Flies buzz around gnawed bones in the hollow.",
        ],
    )

    ls_fourth_turn = area.room(
        "ls_fourth_turn",
        name="Lower Switchback - Fourth Turn",
        desc=(
            "The path turns again, climbing higher. Stunted pines cling "
            "to cracks in the rock, bent permanently by wind. The air is "
            "noticeably thinner here, and the views stretch farther. A "
            "cairn of stacked stones marks the turn -- someone's attempt "
            "at a trail marker, or a grave."
        ),
        room_type="path",
        indoor=False,
    )

    ls_wind_gap = area.room(
        "ls_wind_gap",
        name="Wind Gap",
        desc=(
            "A natural gap in the ridge funnels wind through with "
            "surprising force. The constant gale has stripped the rock "
            "bare and polished it smooth. Crossing the gap requires "
            "leaning into the wind. On the far side, the path widens "
            "and the wind drops to nothing."
        ),
        room_type="path",
        indoor=False,
        ambient_echoes=[
            "The wind howls through the gap like a living thing.",
            "Your cloak snaps and pulls in the constant gale.",
        ],
    )

    ls_miners_rest = area.room(
        "ls_miners_rest",
        name="Miner's Rest",
        desc=(
            "A flat area where miners once rested on their way to the "
            "Greystone workings. A stone bench has been carved from "
            "a boulder, worn smooth by generations of use. Empty water "
            "skins and discarded mining gloves litter the ground. A "
            "rusted pickaxe head, separated from its handle, lies "
            "half-buried in gravel."
        ),
        room_type="clearing",
        indoor=False,
    )

    ls_upper_trail = area.room(
        "ls_upper_trail",
        name="Upper Trail Junction",
        desc=(
            "The switchback path meets a broader trail running east-west "
            "along the mountainside. To the west, the trail leads toward "
            "a dark opening in the rock face -- the Greystone Mine. To "
            "the east, it winds along the ridge toward higher ground. "
            "Wagon ruts in the rock show this was once a working road."
        ),
        room_type="path",
        indoor=False,
    )

    ls_herb_ledge = area.room(
        "ls_herb_ledge",
        name="Herb Ledge",
        desc=(
            "A sheltered ledge on the south-facing slope where mountain "
            "herbs grow in surprising abundance. Silvervein -- a pale "
            "plant with metallic-sheened leaves -- clusters in the "
            "cracks. Stonecap mushrooms dot the damp rock beneath an "
            "overhang. Someone has been harvesting here recently; "
            "clean-cut stems show where plants were carefully taken."
        ),
        room_type="clearing",
        indoor=False,
    )

    ls_eagles_perch = area.room(
        "ls_eagles_perch",
        name="Eagle's Perch",
        desc=(
            "A jutting spur of rock high above the switchbacks. A large "
            "nest of sticks and bone occupies the flat top -- a Reth "
            "eagle's perch. White streaks of droppings paint the rock "
            "below. Scattered feathers, each nearly two feet long, "
            "drift in the updraft. The eagles tolerate no trespass."
        ),
        room_type="clearing",
        indoor=False,
        ambient_echoes=[
            "A piercing shriek from above -- an eagle warns of your approach.",
            "Massive wings beat the air somewhere overhead.",
        ],
    )

    # Lower Switchbacks exits
    area.exit(ra_fallen_pine, ls_first_turn, "north")
    area.exit(ls_first_turn, ra_fallen_pine, "south")
    area.exit(ls_first_turn, ls_narrow_ledge, "north")
    area.exit(ls_narrow_ledge, ls_first_turn, "south")
    area.exit(ls_narrow_ledge, ls_second_turn, "north")
    area.exit(ls_second_turn, ls_narrow_ledge, "south")
    area.exit(ls_second_turn, ls_goat_trail, "east")
    area.exit(ls_goat_trail, ls_second_turn, "west")
    area.exit(ls_goat_trail, ls_rocky_shelf, "up")
    area.exit(ls_rocky_shelf, ls_goat_trail, "down")
    area.exit(ls_second_turn, ls_third_turn, "north")
    area.exit(ls_third_turn, ls_second_turn, "south")
    area.exit(ls_third_turn, ls_scree_slope, "west")
    area.exit(ls_scree_slope, ls_third_turn, "east")
    area.exit(ls_scree_slope, ls_troll_hollow, "north")
    area.exit(ls_troll_hollow, ls_scree_slope, "south")
    area.exit(ls_third_turn, ls_fourth_turn, "north")
    area.exit(ls_fourth_turn, ls_third_turn, "south")
    area.exit(ls_fourth_turn, ls_wind_gap, "east")
    area.exit(ls_wind_gap, ls_fourth_turn, "west")
    area.exit(ls_fourth_turn, ls_miners_rest, "north")
    area.exit(ls_miners_rest, ls_fourth_turn, "south")
    area.exit(ls_miners_rest, ls_upper_trail, "north")
    area.exit(ls_upper_trail, ls_miners_rest, "south")
    area.exit(ls_wind_gap, ls_herb_ledge, "northeast")
    area.exit(ls_herb_ledge, ls_wind_gap, "southwest")
    area.exit(ls_herb_ledge, ls_eagles_perch, "up")
    area.exit(ls_eagles_perch, ls_herb_ledge, "down")

    # ==================================================================
    #  SUB-AREA 3: GREYSTONE MINE (~14 rooms)
    #  Abandoned mine shafts, underground room types. Iron and copper
    #  ore. Mining foreman NPC near entrance.
    # ==================================================================

    gm_entrance = area.room(
        "gm_entrance",
        name="Greystone Mine - Entrance",
        desc=(
            "A dark opening in the rock face, framed by rotting timber "
            "supports. The words 'GREYSTONE WORKS' are carved into the "
            "lintel stone, though weather has softened the letters to "
            "near-illegibility. Rusty ore cart tracks run from the "
            "entrance down the slope. The air flowing out of the mine "
            "is cold and smells of damp stone and old iron."
        ),
        room_type="cave",
        indoor=False,
        ambient_echoes=[
            "Cold air flows steadily from the mine entrance.",
            "A distant metallic clang echoes from deep inside.",
        ],
    )

    gm_main_shaft = area.room(
        "gm_main_shaft",
        name="Greystone Mine - Main Shaft",
        desc=(
            "The main shaft runs straight into the mountain, wide enough "
            "for two ore carts side by side. Timber supports line the "
            "walls at regular intervals, some bowed under the weight "
            "above. The ore cart tracks continue into darkness. Patches "
            "of luminescent fungus cling to the ceiling, casting a "
            "sickly green glow."
        ),
        room_type="underground",
        indoor=True,
        ambient_echoes=[
            "Timbers creak under the weight of the mountain.",
            "Water drips from the ceiling in a steady rhythm.",
        ],
    )

    gm_tool_room = area.room(
        "gm_tool_room",
        name="Greystone Mine - Tool Room",
        desc=(
            "A small chamber off the main shaft where mining tools were "
            "stored. Racks line the walls, most empty now. A few rusted "
            "pickaxes, bent pry bars, and coils of frayed rope remain. "
            "A work bench holds a grinding wheel, its handle still intact. "
            "Someone has been here recently -- the dust on the bench is "
            "disturbed."
        ),
        room_type="underground",
        indoor=True,
    )

    gm_north_drift = area.room(
        "gm_north_drift",
        name="Greystone Mine - North Drift",
        desc=(
            "A narrower passage branching north from the main shaft. "
            "The rock walls show pick marks where miners followed a "
            "vein of iron ore. The vein is still visible -- a dark "
            "reddish-brown streak in the grey stone. The passage is "
            "low enough to require ducking in places."
        ),
        room_type="underground",
        indoor=True,
    )

    gm_iron_face = area.room(
        "gm_iron_face",
        name="Greystone Mine - Iron Face",
        desc=(
            "The end of the north drift, where the iron vein widens "
            "into a broad face of ore-bearing rock. Fresh pick marks "
            "show someone has been working this face recently -- the "
            "exposed iron gleams dully in the lamplight. Ore fragments "
            "litter the floor."
        ),
        room_type="underground",
        indoor=True,
    )

    gm_south_drift = area.room(
        "gm_south_drift",
        name="Greystone Mine - South Drift",
        desc=(
            "A passage heading south, following a different mineral "
            "vein. The walls here show traces of copper -- green "
            "oxidation staining the stone in streaks and patches. "
            "The air is staler here, the ventilation poor. A canary "
            "cage hangs empty from a ceiling hook."
        ),
        room_type="underground",
        indoor=True,
    )

    gm_copper_chamber = area.room(
        "gm_copper_chamber",
        name="Greystone Mine - Copper Chamber",
        desc=(
            "A wider chamber where copper-bearing rock has been excavated, "
            "leaving a rough dome shape. The walls are streaked with "
            "vivid green and blue copper deposits. Some patches have "
            "been chipped away; others remain untouched, too deep "
            "in the wall to reach without serious effort."
        ),
        room_type="underground",
        indoor=True,
    )

    gm_collapse = area.room(
        "gm_collapse",
        name="Greystone Mine - Collapsed Section",
        desc=(
            "The passage ahead is blocked by a cave-in. Broken timbers "
            "jut from a wall of fallen rock and earth. The collapse "
            "looks old -- decades at least. Dust has settled into every "
            "crevice. Through gaps in the rubble, cold air flows from "
            "whatever lies beyond. Something scratches and clicks on "
            "the other side."
        ),
        room_type="underground",
        indoor=True,
        ambient_echoes=[
            "Scratching sounds come from behind the collapsed rubble.",
            "Cold air whistles through gaps in the cave-in.",
        ],
    )

    gm_flooded_shaft = area.room(
        "gm_flooded_shaft",
        name="Greystone Mine - Flooded Shaft",
        desc=(
            "A vertical shaft drops into dark water. The shaft was "
            "once used for hoisting ore, but groundwater has filled "
            "the lower levels. The water is black and still, reflecting "
            "nothing. A rusted winch mechanism sits at the shaft's edge, "
            "its cable trailing into the depths."
        ),
        room_type="underground",
        indoor=True,
    )

    gm_foreman_office = area.room(
        "gm_foreman_office",
        name="Greystone Mine - Foreman's Office",
        desc=(
            "A small carved-out room near the entrance, once the mine "
            "foreman's office. A battered desk, a chair with one leg "
            "shorter than the others, and a wall of wooden cubbyholes "
            "for organizing claims and shift rosters. A Consortium "
            "assessment notice is pinned to the wall -- dated three "
            "years ago, recommending the mine be re-evaluated for "
            "'profitable re-opening pending safety inspection.'"
        ),
        room_type="underground",
        indoor=True,
    )

    gm_ore_cart_bay = area.room(
        "gm_ore_cart_bay",
        name="Greystone Mine - Ore Cart Bay",
        desc=(
            "A widened section of the main shaft where ore carts were "
            "loaded and unloaded. Two rusted carts sit on the tracks, "
            "one overturned. The loading platform is a raised stone "
            "ledge with iron bolts set into it. Ore dust -- red-brown "
            "and grey -- coats everything in a fine gritty layer."
        ),
        room_type="underground",
        indoor=True,
    )

    gm_ventilation_shaft = area.room(
        "gm_ventilation_shaft",
        name="Greystone Mine - Ventilation Shaft",
        desc=(
            "A narrow vertical shaft open to the sky far above. Light "
            "filters down, illuminating drifting dust motes. The shaft "
            "draws air through the mine -- without it, the deeper "
            "sections would be unbreathable. Iron rungs are set into "
            "the wall, climbing up to a distant circle of grey sky."
        ),
        room_type="underground",
        indoor=True,
    )

    gm_deep_crosscut = area.room(
        "gm_deep_crosscut",
        name="Greystone Mine - Deep Crosscut",
        desc=(
            "A horizontal passage connecting the north and south drifts "
            "at the deepest worked level. The timbers here are older, "
            "darker, and dangerously bowed. The rock walls are slick "
            "with moisture. Something has been scratching at the stone "
            "down here -- not pick marks, but irregular, organic gouges."
        ),
        room_type="underground",
        indoor=True,
        ambient_echoes=[
            "A faint chittering echoes from deeper in the mine.",
            "Water seeps from a crack in the wall, pooling on the floor.",
        ],
    )

    gm_hidden_alcove = area.room(
        "gm_hidden_alcove",
        name="Greystone Mine - Hidden Alcove",
        desc=(
            "Behind a partially collapsed wall, a small natural alcove "
            "opens up. The walls here are not mine-cut -- this is a "
            "natural void in the rock. Strange symbols are scratched "
            "into the back wall, arranged in groups of eight. They "
            "predate the mine by an unknowable span. A faint warmth "
            "radiates from the symbols."
        ),
        room_type="underground",
        indoor=True,
    )

    # Greystone Mine exits
    area.exit(ls_upper_trail, gm_entrance, "west")
    area.exit(gm_entrance, ls_upper_trail, "east")
    area.exit(gm_entrance, gm_main_shaft, "in")
    area.exit(gm_main_shaft, gm_entrance, "out")
    area.exit(gm_entrance, gm_foreman_office, "north")
    area.exit(gm_foreman_office, gm_entrance, "south")
    area.exit(gm_main_shaft, gm_tool_room, "east")
    area.exit(gm_tool_room, gm_main_shaft, "west")
    area.exit(gm_main_shaft, gm_north_drift, "north")
    area.exit(gm_north_drift, gm_main_shaft, "south")
    area.exit(gm_north_drift, gm_iron_face, "north")
    area.exit(gm_iron_face, gm_north_drift, "south")
    area.exit(gm_main_shaft, gm_south_drift, "south")
    area.exit(gm_south_drift, gm_main_shaft, "north")
    area.exit(gm_south_drift, gm_copper_chamber, "south")
    area.exit(gm_copper_chamber, gm_south_drift, "north")
    area.exit(gm_main_shaft, gm_ore_cart_bay, "west")
    area.exit(gm_ore_cart_bay, gm_main_shaft, "east")
    area.exit(gm_ore_cart_bay, gm_collapse, "west")
    area.exit(gm_collapse, gm_ore_cart_bay, "east")
    area.exit(gm_ore_cart_bay, gm_flooded_shaft, "down")
    area.exit(gm_flooded_shaft, gm_ore_cart_bay, "up")
    area.exit(gm_main_shaft, gm_ventilation_shaft, "up")
    area.exit(gm_ventilation_shaft, gm_main_shaft, "down")
    area.exit(gm_south_drift, gm_deep_crosscut, "west")
    area.exit(gm_deep_crosscut, gm_south_drift, "east")
    area.exit(gm_deep_crosscut, gm_north_drift, "northwest")
    area.exit(gm_north_drift, gm_deep_crosscut, "southeast")
    area.exit(gm_deep_crosscut, gm_hidden_alcove, "in")
    area.exit(gm_hidden_alcove, gm_deep_crosscut, "out")

    # ==================================================================
    #  SUB-AREA 4: CAVE NETWORKS (~16 rooms)
    #  Branching natural cave system. Spider dens, underground streams,
    #  cave spider mobs. Connects to the Deepcavern.
    # ==================================================================

    cn_mouth = area.room(
        "cn_mouth",
        name="Cave Mouth",
        desc=(
            "A wide, low-ceilinged opening at the base of a cliff face. "
            "The entrance is curtained with pale roots dangling from "
            "above, and thick webs fill the upper corners. The air "
            "inside is cool and damp, carrying the faint metallic "
            "tang of underground water. Footprints in the mud -- both "
            "human and animal -- lead into the darkness."
        ),
        room_type="cave",
        indoor=False,
        ambient_echoes=[
            "Water drips somewhere in the cave ahead.",
            "A web trembles in the cave mouth, disturbed by air current.",
        ],
    )

    cn_entrance_hall = area.room(
        "cn_entrance_hall",
        name="Cave Entrance Hall",
        desc=(
            "A natural cavern opens up beyond the entrance, the ceiling "
            "rising to fifteen feet. Stalactites hang like stone teeth "
            "above. The floor is uneven limestone, worn smooth by water. "
            "Passages branch in three directions -- north, east, and "
            "a narrow crack leading down."
        ),
        room_type="underground",
        indoor=True,
    )

    cn_stream_passage = area.room(
        "cn_stream_passage",
        name="Stream Passage",
        desc=(
            "A narrow passage follows an underground stream. The water "
            "is ankle-deep and shockingly cold, running over smooth "
            "pebbles. The stream has carved the passage over millennia, "
            "leaving the walls scalloped and smooth. Pale, eyeless fish "
            "dart away from any light."
        ),
        room_type="underground",
        indoor=True,
        ambient_echoes=[
            "The stream burbles over stones, a constant murmur.",
            "Something pale flashes through the water -- a cave fish.",
        ],
    )

    cn_mushroom_grotto = area.room(
        "cn_mushroom_grotto",
        name="Mushroom Grotto",
        desc=(
            "A damp chamber where fungi flourish in extraordinary "
            "variety. Clusters of luminescent mushrooms cast a soft "
            "blue-green glow over everything. Shelf fungi the size "
            "of dinner plates climb the walls. The air is thick with "
            "spores -- earthy, sweet, and faintly intoxicating."
        ),
        room_type="underground",
        indoor=True,
    )

    cn_web_gallery = area.room(
        "cn_web_gallery",
        name="Web Gallery",
        desc=(
            "Thick webs span this passage from wall to wall, floor "
            "to ceiling. The silk is incredibly strong -- it resists "
            "cutting and clings to everything it touches. Desiccated "
            "husks of insects and small mammals hang wrapped in cocoons "
            "at various heights. The webs vibrate with any movement, "
            "transmitting your presence deeper into the cave."
        ),
        room_type="underground",
        indoor=True,
        ambient_echoes=[
            "The webs vibrate with a low thrumming sound.",
            "Something clicks in the darkness above the webs.",
        ],
    )

    cn_spider_den = area.room(
        "cn_spider_den",
        name="Spider Den",
        desc=(
            "A wide, low chamber entirely carpeted in webbing. The "
            "ceiling is a mass of silk, moving faintly with the "
            "breathing of the cave. Empty egg sacs -- each the size "
            "of a fist -- litter the floor. The spiders that live "
            "here are fast, aggressive, and protective of their "
            "territory. Bones of various animals protrude from the "
            "web carpet."
        ),
        room_type="underground",
        indoor=True,
    )

    cn_crystal_alcove = area.room(
        "cn_crystal_alcove",
        name="Crystal Alcove",
        desc=(
            "A small side chamber where mineral-rich water has deposited "
            "clusters of crystals on every surface. They catch and "
            "multiply any light source, filling the alcove with "
            "prismatic reflections. The crystals are primarily quartz "
            "with veins of something darker -- the same glassy black "
            "stone seen on the switchbacks above."
        ),
        room_type="underground",
        indoor=True,
    )

    cn_chimney = area.room(
        "cn_chimney",
        name="Cave Chimney",
        desc=(
            "A vertical shaft in the cave ceiling, narrow enough to "
            "climb with back and feet braced against opposing walls. "
            "Light filters down from somewhere above. The rock is "
            "worn smooth by water. Iron-rich deposits have stained "
            "the shaft walls in bands of rust and ochre."
        ),
        room_type="underground",
        indoor=True,
    )

    cn_underground_pool = area.room(
        "cn_underground_pool",
        name="Underground Pool",
        desc=(
            "The stream widens into a still, dark pool. The water is "
            "crystal clear near the edges, revealing a smooth limestone "
            "bottom covered in fine silt. Further out, the pool deepens "
            "beyond sight -- the water turns from clear to deep blue "
            "to black. A faint current stirs the surface at the far "
            "end, suggesting a submerged outflow."
        ),
        room_type="underground",
        indoor=True,
    )

    cn_bat_chamber = area.room(
        "cn_bat_chamber",
        name="Bat Chamber",
        desc=(
            "A high-ceilinged chamber alive with the rustle and squeak "
            "of hundreds of bats. They hang from the ceiling in dense "
            "clusters, their leathery wings folded tight. The floor is "
            "thick with guano -- the smell is powerful and ammonia-sharp. "
            "Despite the unpleasantness, the guano makes excellent "
            "fertilizer; traces of harvesting are visible."
        ),
        room_type="underground",
        indoor=True,
        ambient_echoes=[
            "Bats chitter and rustle overhead in restless waves.",
            "The ammonia smell makes your eyes water.",
        ],
    )

    cn_narrow_squeeze = area.room(
        "cn_narrow_squeeze",
        name="Narrow Squeeze",
        desc=(
            "The passage narrows to a crack barely wide enough to "
            "squeeze through sideways. The walls press in on both "
            "sides. The rock is damp and cold against your body. "
            "Beyond the squeeze, the passage opens up again into "
            "a larger space."
        ),
        room_type="underground",
        indoor=True,
    )

    cn_fossil_wall = area.room(
        "cn_fossil_wall",
        name="Fossil Wall",
        desc=(
            "One wall of this passage is dense with fossils -- the "
            "preserved remains of ancient sea creatures from when this "
            "mountain was an ocean floor. Spiral shells, fan-shaped "
            "organisms, and the long sinuous outline of something "
            "serpentine are pressed into the stone. Time made visible."
        ),
        room_type="underground",
        indoor=True,
    )

    cn_echo_chamber = area.room(
        "cn_echo_chamber",
        name="Echo Chamber",
        desc=(
            "A perfectly round chamber where sound behaves strangely. "
            "Every whisper is amplified and reflected, every footstep "
            "returned tenfold. The acoustics are uncanny -- almost "
            "engineered. The walls are unnervingly smooth, as if "
            "polished by something other than water."
        ),
        room_type="underground",
        indoor=True,
        ambient_echoes=[
            "Your breathing echoes back at you from every direction.",
            "A distant sound -- something large moving -- reverberates through the chamber.",
        ],
    )

    cn_drip_gallery = area.room(
        "cn_drip_gallery",
        name="Drip Gallery",
        desc=(
            "A long, narrow gallery where stalactites and stalagmites "
            "have grown so close together they nearly meet, forming "
            "slender columns of mineral-stained stone. Water drips "
            "from every stalactite tip, each drop a tiny percussion. "
            "The combined sound is like distant rain."
        ),
        room_type="underground",
        indoor=True,
    )

    cn_web_bridge = area.room(
        "cn_web_bridge",
        name="Web Bridge",
        desc=(
            "A deep crevasse splits the cave floor. Spanning it is a "
            "bridge of spider silk -- layer upon layer, thick as rope, "
            "woven into a structure strong enough to bear considerable "
            "weight. The bridge was not built by any human hand. Below, "
            "darkness. The silk is disturbingly fresh."
        ),
        room_type="underground",
        indoor=True,
    )

    cn_lower_junction = area.room(
        "cn_lower_junction",
        name="Lower Junction",
        desc=(
            "A meeting point of several passages deep in the cave "
            "system. The air is warmer here than expected -- heat "
            "rises from somewhere below. Three passages lead away: "
            "one north, one south, and one descending steeply into "
            "the deepest part of the mountain."
        ),
        room_type="underground",
        indoor=True,
    )

    # Cave Networks exits
    area.exit(ls_scree_slope, cn_mouth, "west")
    area.exit(cn_mouth, ls_scree_slope, "east")
    area.exit(cn_mouth, cn_entrance_hall, "in")
    area.exit(cn_entrance_hall, cn_mouth, "out")
    area.exit(cn_mouth, "cantera_edge:rc_reth_exit", "south",
              desc="A rough trail descends south through the roots toward Cantera Edge.")
    area.exit(cn_entrance_hall, cn_stream_passage, "north")
    area.exit(cn_stream_passage, cn_entrance_hall, "south")
    area.exit(cn_stream_passage, cn_mushroom_grotto, "north")
    area.exit(cn_mushroom_grotto, cn_stream_passage, "south")
    area.exit(cn_entrance_hall, cn_web_gallery, "east")
    area.exit(cn_web_gallery, cn_entrance_hall, "west")
    area.exit(cn_web_gallery, cn_spider_den, "east")
    area.exit(cn_spider_den, cn_web_gallery, "west")
    area.exit(cn_entrance_hall, cn_narrow_squeeze, "down")
    area.exit(cn_narrow_squeeze, cn_entrance_hall, "up")
    area.exit(cn_stream_passage, cn_underground_pool, "east")
    area.exit(cn_underground_pool, cn_stream_passage, "west")
    area.exit(cn_mushroom_grotto, cn_crystal_alcove, "east")
    area.exit(cn_crystal_alcove, cn_mushroom_grotto, "west")
    area.exit(cn_mushroom_grotto, cn_bat_chamber, "north")
    area.exit(cn_bat_chamber, cn_mushroom_grotto, "south")
    area.exit(cn_bat_chamber, cn_chimney, "up")
    area.exit(cn_chimney, cn_bat_chamber, "down")
    area.exit(cn_narrow_squeeze, cn_fossil_wall, "south")
    area.exit(cn_fossil_wall, cn_narrow_squeeze, "north")
    area.exit(cn_narrow_squeeze, cn_echo_chamber, "west")
    area.exit(cn_echo_chamber, cn_narrow_squeeze, "east")
    area.exit(cn_echo_chamber, cn_drip_gallery, "south")
    area.exit(cn_drip_gallery, cn_echo_chamber, "north")
    area.exit(cn_spider_den, cn_web_bridge, "east")
    area.exit(cn_web_bridge, cn_spider_den, "west")
    area.exit(cn_web_bridge, cn_lower_junction, "down")
    area.exit(cn_lower_junction, cn_web_bridge, "up")
    area.exit(cn_drip_gallery, cn_lower_junction, "south")
    area.exit(cn_lower_junction, cn_drip_gallery, "north")

    # ==================================================================
    #  SUB-AREA 5: WESTERN RIDGE (~12 rooms)
    #  High mountain paths, eagle territory, wind-blasted ridges.
    #  Connects westward toward the forest zone.
    # ==================================================================

    wr_ridge_trail = area.room(
        "wr_ridge_trail",
        name="Western Ridge Trail",
        desc=(
            "A trail follows the ridgeline west, the ground falling "
            "away steeply on both sides. The wind is relentless up "
            "here, scouring exposed skin. Stunted pines bend eastward, "
            "shaped by decades of prevailing gales. To the west, the "
            "dark smudge of a forest is visible in the lowlands below."
        ),
        room_type="path",
        indoor=False,
        ambient_echoes=[
            "Wind screams along the ridge, never letting up.",
            "A stunted pine creaks and groans in the gale.",
        ],
    )

    wr_broken_cairn = area.room(
        "wr_broken_cairn",
        name="Broken Cairn",
        desc=(
            "A cairn of stacked stones has been toppled, its rocks "
            "scattered across the trail. The stones are old and "
            "lichen-covered. At the cairn's base, a flat stone bears "
            "carved symbols -- the same groups-of-eight notation seen "
            "in the mine. Someone toppled the cairn deliberately, "
            "perhaps looking for what was buried beneath."
        ),
        room_type="path",
        indoor=False,
    )

    wr_eagles_nest = area.room(
        "wr_eagles_nest",
        name="Eagle Nesting Ground",
        desc=(
            "Multiple Reth eagle nests occupy the crags here -- massive "
            "constructions of branches, bones, and shed feathers. Adult "
            "eagles circle overhead, their wingspans casting shadows "
            "wide enough to cover a man. The birds are territorial and "
            "aggressive. Eggshell fragments and prey remains litter "
            "the ground between nests."
        ),
        room_type="clearing",
        indoor=False,
        ambient_echoes=[
            "Eagles scream warnings from their nests.",
            "The sound of massive wings beating the air fills the crag.",
        ],
    )

    wr_windblast_pass = area.room(
        "wr_windblast_pass",
        name="Windblast Pass",
        desc=(
            "A narrow gap between two peaks where the wind accelerates "
            "to a shrieking gale. Walking through is possible only by "
            "crouching low and bracing against the rock. Sand and grit "
            "blast exposed skin raw. On the far side, the wind drops "
            "abruptly, and the western slopes open up."
        ),
        room_type="path",
        indoor=False,
    )

    wr_western_descent = area.room(
        "wr_western_descent",
        name="Western Descent",
        desc=(
            "The path descends the western face of the ridge, "
            "switchbacking down toward the tree line far below. The "
            "vegetation changes rapidly -- mountain scrub gives way to "
            "dwarf oaks, then to taller trees whose canopy blocks the "
            "wind. The air warms and softens with each step down."
        ),
        room_type="path",
        indoor=False,
    )

    wr_treeline = area.room(
        "wr_treeline",
        name="Mountain Treeline",
        desc=(
            "The boundary between mountain and forest. Above, bare "
            "rock and wind. Below, trees and shelter. The transition "
            "is sharp -- a single stride takes you from exposed stone "
            "to leaf-shadowed ground. The first real trees are twisted "
            "dwarfs, gnarled by altitude, but they grow taller with "
            "each step downhill."
        ),
        room_type="path",
        indoor=False,
    )

    wr_cliff_face = area.room(
        "wr_cliff_face",
        name="Cliff Face",
        desc=(
            "A sheer cliff drops away to the west, offering a "
            "vertiginous view of the lowlands. The rock face is "
            "streaked with mineral deposits -- white calcite, red "
            "iron, and that same glassy black stone. A narrow ledge "
            "runs along the cliff base, barely passable."
        ),
        room_type="path",
        indoor=False,
    )

    wr_golem_debris = area.room(
        "wr_golem_debris",
        name="Golem Debris Field",
        desc=(
            "Scattered across a windswept shelf are fragments of what "
            "was once a massive stone construct. The pieces are too "
            "regular to be natural rock -- joints, hinges, curved "
            "panels of fitted stone. Whatever this golem was, it fell "
            "or was cast down from somewhere higher. The fragments "
            "are ancient, weathered to near-anonymity."
        ),
        room_type="clearing",
        indoor=False,
    )

    wr_hermit_cave = area.room(
        "wr_hermit_cave",
        name="Hermit's Cave",
        desc=(
            "A small, dry cave on the western ridge, made habitable "
            "by its occupant. A sleeping pallet of dried grass, a "
            "fire ring of blackened stones, shelves carved into the "
            "rock wall holding dozens of glass bottles and clay jars. "
            "The smell of dried herbs, mineral spirits, and something "
            "acrid fills the space. An alchemist's workspace, sparse "
            "but functional."
        ),
        room_type="cave",
        indoor=True,
    )

    wr_overhang = area.room(
        "wr_overhang",
        name="Stone Overhang",
        desc=(
            "A natural stone overhang provides shelter from wind and "
            "weather. The ground beneath is dry and flat. Scorch marks "
            "on the ceiling show this has served as a campsite for "
            "generations. Carved into the back wall are names and "
            "dates -- miners, prospectors, and travelers who sheltered "
            "here over the decades."
        ),
        room_type="cave",
        indoor=False,
    )

    wr_slide = area.room(
        "wr_slide",
        name="Rock Slide",
        desc=(
            "A recent rock slide has carved a raw wound in the "
            "mountainside. Fresh stone -- pale and unweathered -- is "
            "exposed where the slide tore away the surface. The debris "
            "forms a chaotic slope of boulders and rubble. Something "
            "glints in the newly exposed rock -- a vein of ore or "
            "mineral, uncovered by the slide."
        ),
        room_type="path",
        indoor=False,
    )

    wr_peak_trail = area.room(
        "wr_peak_trail",
        name="Peak Trail",
        desc=(
            "The trail climbs toward a minor peak, the path narrowing "
            "to a footpath worn into bare rock. Lichen covers every "
            "surface not regularly trodden. The summit is visible "
            "ahead -- a bare crown of grey stone. Mountain goats watch "
            "from impossible perches on the cliffs above."
        ),
        room_type="path",
        indoor=False,
    )

    # Western Ridge exits
    area.exit(ls_upper_trail, wr_ridge_trail, "east")
    area.exit(wr_ridge_trail, ls_upper_trail, "west")
    area.exit(wr_ridge_trail, wr_broken_cairn, "north")
    area.exit(wr_broken_cairn, wr_ridge_trail, "south")
    area.exit(wr_broken_cairn, wr_eagles_nest, "north")
    area.exit(wr_eagles_nest, wr_broken_cairn, "south")
    area.exit(wr_ridge_trail, wr_windblast_pass, "southwest")
    area.exit(wr_windblast_pass, wr_ridge_trail, "northeast")
    area.exit(wr_windblast_pass, wr_western_descent, "west")
    area.exit(wr_western_descent, wr_windblast_pass, "east")
    area.exit(wr_western_descent, wr_treeline, "west")
    area.exit(wr_treeline, wr_western_descent, "east")
    area.exit(wr_ridge_trail, wr_cliff_face, "south")
    area.exit(wr_cliff_face, wr_ridge_trail, "north")
    area.exit(wr_cliff_face, wr_golem_debris, "west")
    area.exit(wr_golem_debris, wr_cliff_face, "east")
    area.exit(wr_eagles_nest, wr_hermit_cave, "east")
    area.exit(wr_hermit_cave, wr_eagles_nest, "west")
    area.exit(wr_ridge_trail, wr_overhang, "east")
    area.exit(wr_overhang, wr_ridge_trail, "west")
    area.exit(wr_cliff_face, wr_slide, "south")
    area.exit(wr_slide, wr_cliff_face, "north")
    area.exit(wr_eagles_nest, wr_peak_trail, "up")
    area.exit(wr_peak_trail, wr_eagles_nest, "down")

    # Cross-zone exit west to forest zone
    area.exit(wr_treeline, "cantera_edge:fe_trailhead", "west", one_way=True)

    # ==================================================================
    #  SUB-AREA 6: MOUNTAIN OVERLOOKS (~10 rooms)
    #  Scenic viewpoints, golem fragments, high-altitude clearings.
    # ==================================================================

    mo_south_overlook = area.room(
        "mo_south_overlook",
        name="Southern Overlook",
        desc=(
            "A broad ledge of flat stone jutting from the mountainside, "
            "offering a commanding view southward. The entire Ashreach "
            "is visible -- a vast brown expanse punctuated by the tiny "
            "dark cluster of Vael's Crossing. Dragon courier routes are "
            "visible as thin lines of disturbed air in the distance. "
            "The wind up here carries the scent of stone and distance."
        ),
        room_type="clearing",
        indoor=False,
        ambient_echoes=[
            "The wind carries sounds from impossibly far away.",
            "A courier dragon is a speck against the distant sky.",
        ],
    )

    mo_east_overlook = area.room(
        "mo_east_overlook",
        name="Eastern Overlook",
        desc=(
            "The mountain drops away to the east, revealing range "
            "after range of lower hills fading into blue distance. "
            "The jagged northeastern coastline of Varath is a faint "
            "glitter on the horizon. Closer, the foothills are a "
            "rumpled grey-green carpet of scrub and stunted forest."
        ),
        room_type="clearing",
        indoor=False,
    )

    mo_golem_terrace = area.room(
        "mo_golem_terrace",
        name="Golem Terrace",
        desc=(
            "A flat terrace of unnaturally smooth stone, clearly "
            "shaped by something other than natural erosion. At the "
            "center sits the torso of a massive stone golem -- split "
            "vertically, one half fallen, the other still upright. "
            "The remaining half stands twelve feet tall, its surface "
            "covered in worn carvings. Its single visible hand is "
            "open, palm up, as if offering or receiving."
        ),
        room_type="ruins",
        indoor=False,
    )

    mo_high_meadow = area.room(
        "mo_high_meadow",
        name="High Meadow",
        desc=(
            "An improbable patch of green in the grey mountain terrain. "
            "Mountain grasses and small wildflowers grow in a sheltered "
            "depression between ridges, fed by snowmelt that seeps "
            "from above. The meadow hums with insects in season. "
            "Mountain goats graze here, untroubled by anything short "
            "of a direct threat."
        ),
        room_type="clearing",
        indoor=False,
    )

    mo_ruins_arch = area.room(
        "mo_ruins_arch",
        name="Ruined Arch",
        desc=(
            "A stone arch stands alone on the mountainside, leading "
            "to and from nothing. It was once part of a larger "
            "structure -- foundation stones are visible beneath thin "
            "soil -- but whatever building it belonged to is long "
            "gone. The arch stones are fitted without mortar, in the "
            "old style. Carved into the keystone: eight interlocking "
            "circles."
        ),
        room_type="ruins",
        indoor=False,
    )

    mo_foundation = area.room(
        "mo_foundation",
        name="Ancient Foundation",
        desc=(
            "Stone foundations trace the outline of a vanished "
            "building. The walls were massive -- the foundation "
            "stones are each the size of a cart. The layout suggests "
            "something ceremonial: a central circular space surrounded "
            "by eight radiating chambers. Mountain plants have "
            "reclaimed most of the stone, but the geometry is unmistakable."
        ),
        room_type="ruins",
        indoor=False,
    )

    mo_summit_trail = area.room(
        "mo_summit_trail",
        name="Summit Trail",
        desc=(
            "A faint trail climbs toward the summit of one of The "
            "Reth's lower peaks. The path is little more than a "
            "suggestion -- a slightly clearer route through loose "
            "rock. The air is thin and sharp. Grey clouds move at "
            "eye level, close enough to seem touchable."
        ),
        room_type="path",
        indoor=False,
    )

    mo_minor_summit = area.room(
        "mo_minor_summit",
        name="Minor Summit",
        desc=(
            "The top of a minor peak in The Reth range. The view is "
            "vast and empty -- mountains stretching north until they "
            "disappear into haze, the plains south, the forest west, "
            "the coast a distant glitter east. A stone pillar stands "
            "at the peak, carved in a style that matches no known "
            "Imperial period. Its purpose is unclear. Standing beside "
            "it, the wind feels different -- directed, purposeful."
        ),
        room_type="clearing",
        indoor=False,
        ambient_echoes=[
            "The wind swirls around the summit pillar in a pattern that seems deliberate.",
            "Clouds pass at eye level, cold and wet.",
        ],
    )

    mo_north_vista = area.room(
        "mo_north_vista",
        name="Northern Vista",
        desc=(
            "The mountain continues north -- peak after peak, grey "
            "teeth biting at the sky. The Reth is a spine that runs "
            "the length of Varath, and from here its true scale is "
            "apparent. Somewhere in those northern peaks lies Tremen, "
            "the half-dwarf city carved into the mountain itself. "
            "That is far beyond these foothills."
        ),
        room_type="clearing",
        indoor=False,
    )

    mo_wind_carved = area.room(
        "mo_wind_carved",
        name="Wind-Carved Passage",
        desc=(
            "Wind has carved a passage through soft stone, creating "
            "a natural tunnel with walls sculpted into flowing, "
            "organic shapes. The effect is beautiful and unsettling -- "
            "the stone looks like frozen water. The passage runs "
            "east-west through a ridge, emerging on both sides."
        ),
        room_type="path",
        indoor=False,
    )

    # Mountain Overlooks exits
    area.exit(ls_rocky_shelf, mo_south_overlook, "north")
    area.exit(mo_south_overlook, ls_rocky_shelf, "south")
    area.exit(mo_south_overlook, mo_east_overlook, "east")
    area.exit(mo_east_overlook, mo_south_overlook, "west")
    area.exit(mo_south_overlook, mo_golem_terrace, "north")
    area.exit(mo_golem_terrace, mo_south_overlook, "south")
    area.exit(mo_golem_terrace, mo_high_meadow, "west")
    area.exit(mo_high_meadow, mo_golem_terrace, "east")
    area.exit(mo_golem_terrace, mo_ruins_arch, "north")
    area.exit(mo_ruins_arch, mo_golem_terrace, "south")
    area.exit(mo_ruins_arch, mo_foundation, "east")
    area.exit(mo_foundation, mo_ruins_arch, "west")
    area.exit(mo_ruins_arch, mo_summit_trail, "north")
    area.exit(mo_summit_trail, mo_ruins_arch, "south")
    area.exit(mo_summit_trail, mo_minor_summit, "up")
    area.exit(mo_minor_summit, mo_summit_trail, "down")
    area.exit(mo_minor_summit, mo_north_vista, "north")
    area.exit(mo_north_vista, mo_minor_summit, "south")
    area.exit(mo_east_overlook, mo_wind_carved, "east")
    area.exit(mo_wind_carved, mo_east_overlook, "west")

    # ==================================================================
    #  SUB-AREA 7: THE DEEPCAVERN (~12 rooms)
    #  Deepest cave system. Named mob "Grandmother Spider" lair.
    # ==================================================================

    dc_upper_descent = area.room(
        "dc_upper_descent",
        name="Deepcavern - Upper Descent",
        desc=(
            "A steep, winding passage descends into the mountain's "
            "heart. The air grows warmer and more humid with each "
            "step down. The walls are slick with condensation and "
            "covered in a thin film of something organic -- the silk "
            "residue of spiders that have traveled this route for "
            "generations."
        ),
        room_type="underground",
        indoor=True,
        ambient_echoes=[
            "A faint clicking echoes from below -- rhythmic, patient.",
        ],
    )

    dc_silk_chamber = area.room(
        "dc_silk_chamber",
        name="Deepcavern - Silk Chamber",
        desc=(
            "The walls, ceiling, and floor of this chamber are coated "
            "in thick layers of ancient spider silk. The silk has "
            "hardened over time into something resembling lacquer -- "
            "smooth, white, and faintly translucent. Behind the silk "
            "layer, the shapes of trapped objects are dimly visible: "
            "bones, equipment, and something that might be a carved "
            "stone tablet."
        ),
        room_type="underground",
        indoor=True,
    )

    dc_egg_gallery = area.room(
        "dc_egg_gallery",
        name="Deepcavern - Egg Gallery",
        desc=(
            "Rows of spider egg sacs hang from the ceiling in neat, "
            "deliberate lines. Not random -- arranged. Each sac is "
            "the size of a human head, pulsing faintly with movement "
            "inside. The precision of their arrangement is unsettling. "
            "This is not the work of ordinary spiders."
        ),
        room_type="underground",
        indoor=True,
        ambient_echoes=[
            "The egg sacs pulse in slow, synchronized rhythm.",
            "A soft rustling from within the nearest sac.",
        ],
    )

    dc_bone_corridor = area.room(
        "dc_bone_corridor",
        name="Deepcavern - Bone Corridor",
        desc=(
            "The floor of this passage is paved with bones -- hundreds "
            "of them, from dozens of species. They have been arranged "
            "and pressed into the silk-coated floor in a deliberate "
            "pattern, forming a mosaic of calcium white against silk "
            "grey. The bones lead deeper, a macabre carpet laid by "
            "intelligence, not instinct."
        ),
        room_type="underground",
        indoor=True,
    )

    dc_warmth_vent = area.room(
        "dc_warmth_vent",
        name="Deepcavern - Warmth Vent",
        desc=(
            "Warm air rises from a crack in the floor, filling this "
            "chamber with tropical humidity. Pale, threadlike plants "
            "grow in the warmth -- blind, white, subsisting on minerals "
            "and geothermal heat. The vent may connect to deeper "
            "volcanic systems. The warmth is steady and ancient."
        ),
        room_type="underground",
        indoor=True,
    )

    dc_silk_bridge = area.room(
        "dc_silk_bridge",
        name="Deepcavern - Silk Bridge",
        desc=(
            "A chasm splits the cave, thirty feet across. Spanning it "
            "is a bridge of woven spider silk -- but this bridge is "
            "different from the one above. It is architectural. "
            "Guy-wires anchor it to the walls. Cross-bracing prevents "
            "sway. This was designed by something that understands "
            "engineering. The silk is old but impossibly strong."
        ),
        room_type="underground",
        indoor=True,
    )

    dc_trophy_wall = area.room(
        "dc_trophy_wall",
        name="Deepcavern - Trophy Wall",
        desc=(
            "One wall of this chamber is covered in objects suspended "
            "in silk: weapons, armor pieces, tools, lanterns, a boot, "
            "a compass, a prayer bead necklace. Trophies taken from "
            "those who ventured too deep. Some are recent. Some are "
            "centuries old, preserved perfectly in the airless silk. "
            "A miner's helmet with a Consortium stamp hangs near the "
            "bottom."
        ),
        room_type="underground",
        indoor=True,
    )

    dc_grand_web = area.room(
        "dc_grand_web",
        name="Deepcavern - Grand Web",
        desc=(
            "An immense cavern opens up, and at its center hangs the "
            "Grand Web -- a structure of spider silk spanning the "
            "entire space, anchored to every wall and the ceiling "
            "above. It is not a web for catching prey. It is a home. "
            "Platforms, chambers, corridors, and storage pods are woven "
            "into the structure with architectural precision. This is "
            "the work of a lifetime -- or several lifetimes."
        ),
        room_type="underground",
        indoor=True,
        ambient_echoes=[
            "The Grand Web vibrates with a low, continuous hum.",
            "Something massive shifts in the upper reaches of the web.",
            "Click. Click. Click. Patient and deliberate.",
        ],
    )

    dc_lair = area.room(
        "dc_lair",
        name="Grandmother Spider's Lair",
        desc=(
            "The heart of the Grand Web. A circular chamber woven from "
            "layers of silk so thick the walls glow faintly -- "
            "bioluminescent fungi trapped within the layers provide "
            "a ghostly blue-white light. The floor is a platform of "
            "compressed silk over a void. In the center, a depression "
            "shaped like a massive body -- the resting place of "
            "something ancient, patient, and very, very large."
        ),
        room_type="underground",
        indoor=True,
    )

    dc_old_nest = area.room(
        "dc_old_nest",
        name="Deepcavern - Old Nest",
        desc=(
            "An abandoned section of the web, older and deteriorating. "
            "The silk here has yellowed and grown brittle. Empty egg "
            "sacs hang like paper lanterns, long hatched. This was "
            "the original lair before the Grand Web was constructed. "
            "Scratched into the cave wall behind the rotting silk: "
            "symbols in groups of eight. The same notation. Always."
        ),
        room_type="underground",
        indoor=True,
    )

    dc_deep_pool = area.room(
        "dc_deep_pool",
        name="Deepcavern - Deep Pool",
        desc=(
            "At the lowest point of the cave system, a pool of still "
            "black water. The water is warm -- heated from below. The "
            "surface is perfectly smooth, reflecting nothing. Dropping "
            "a stone into it produces no sound for a very long time. "
            "Then, very faintly, a splash. The pool is deep beyond "
            "measurement."
        ),
        room_type="underground",
        indoor=True,
    )

    dc_mineral_seep = area.room(
        "dc_mineral_seep",
        name="Deepcavern - Mineral Seep",
        desc=(
            "Mineral-rich water seeps from the cave wall here, "
            "depositing layers of colorful stone. The deposits form "
            "terraced pools in miniature -- each pool a different "
            "color as different minerals precipitate out. Copper green, "
            "iron red, sulfur yellow. An alchemist would find this "
            "place invaluable."
        ),
        room_type="underground",
        indoor=True,
    )

    # Deepcavern exits
    area.exit(cn_lower_junction, dc_upper_descent, "down")
    area.exit(dc_upper_descent, cn_lower_junction, "up")
    area.exit(dc_upper_descent, dc_silk_chamber, "south")
    area.exit(dc_silk_chamber, dc_upper_descent, "north")
    area.exit(dc_silk_chamber, dc_egg_gallery, "east")
    area.exit(dc_egg_gallery, dc_silk_chamber, "west")
    area.exit(dc_silk_chamber, dc_bone_corridor, "south")
    area.exit(dc_bone_corridor, dc_silk_chamber, "north")
    area.exit(dc_bone_corridor, dc_warmth_vent, "east")
    area.exit(dc_warmth_vent, dc_bone_corridor, "west")
    area.exit(dc_bone_corridor, dc_silk_bridge, "south")
    area.exit(dc_silk_bridge, dc_bone_corridor, "north")
    area.exit(dc_silk_bridge, dc_trophy_wall, "east")
    area.exit(dc_trophy_wall, dc_silk_bridge, "west")
    area.exit(dc_silk_bridge, dc_grand_web, "south")
    area.exit(dc_grand_web, dc_silk_bridge, "north")
    area.exit(dc_grand_web, dc_lair, "in")
    area.exit(dc_lair, dc_grand_web, "out")
    area.exit(dc_grand_web, dc_old_nest, "west")
    area.exit(dc_old_nest, dc_grand_web, "east")
    area.exit(dc_warmth_vent, dc_deep_pool, "down")
    area.exit(dc_deep_pool, dc_warmth_vent, "up")
    area.exit(dc_old_nest, dc_mineral_seep, "south")
    area.exit(dc_mineral_seep, dc_old_nest, "north")

    rf_mountain_passage = area.room(
        "rf_mountain_passage",
        name="Collapsed Mountain Passage",
        desc=(
            "The passage narrows here, the walls scarred by recent pick-marks "
            "and surveyor's chalk. A rope line leads deeper but ends abruptly "
            "where the ceiling has caved in. Scattered equipment -- a lantern, "
            "a half-drawn map, a spilled water skin -- tells the story of a "
            "hasty retreat. Or something worse."
        ),
        room_type="underground",
        indoor=True,
    )
    area.exit(gm_deep_crosscut, rf_mountain_passage, "down")
    area.exit(rf_mountain_passage, gm_deep_crosscut, "up")

    # ==================================================================
    #  SUB-AREA 8: EASTERN DESCENT (~12 rooms)
    #  Lower eastern slopes, transition terrain, connects to other zones.
    # ==================================================================

    ed_high_trail = area.room(
        "ed_high_trail",
        name="Eastern High Trail",
        desc=(
            "A trail winds down the eastern face of the foothills. "
            "The terrain here is gentler than the western ridge -- "
            "longer slopes, rounder hills, more vegetation. Scrub oak "
            "and mountain laurel line the path. The air smells of "
            "sun-warmed stone and dry grass."
        ),
        room_type="path",
        indoor=False,
    )

    ed_dry_creek = area.room(
        "ed_dry_creek",
        name="Dry Creek Bed",
        desc=(
            "A creek bed carved into the hillside, currently dry. "
            "Rounded stones mark where water flows in spring snowmelt. "
            "The banks are steep and eroded, exposing layers of clay "
            "and gravel. Animal tracks converge here -- even dry, "
            "the creek bed is a natural highway through the brush."
        ),
        room_type="path",
        indoor=False,
    )

    ed_old_prospector = area.room(
        "ed_old_prospector",
        name="Old Prospector's Claim",
        desc=(
            "A small cleared area where a prospector once worked a "
            "surface claim. A shallow test pit, now partially filled "
            "with debris, sits beside a crude lean-to of stacked "
            "stone and brush. A rusted pan, its bottom worn through, "
            "lies in the dirt. Whatever the prospector found here "
            "wasn't worth staying for."
        ),
        room_type="clearing",
        indoor=False,
    )

    ed_thorn_thicket = area.room(
        "ed_thorn_thicket",
        name="Thorn Thicket",
        desc=(
            "Dense thornbush chokes the hillside here, forcing the "
            "path into a narrow tunnel through the vegetation. The "
            "thorns are long, curved, and sharp enough to tear cloth "
            "and skin. Something moves in the thicket -- too large "
            "to be a rabbit, too cautious to be a troll."
        ),
        room_type="path",
        indoor=False,
        ambient_echoes=[
            "Something rustles through the thorn thicket nearby.",
            "A thorn branch springs back with a sharp snap.",
        ],
    )

    ed_hunters_blind = area.room(
        "ed_hunters_blind",
        name="Hunter's Blind",
        desc=(
            "A crude hunting blind built from stacked stones and "
            "woven branches, positioned to overlook a game trail "
            "below. The blind is maintained -- someone uses it "
            "regularly. Empty water skins and gnawed jerky are "
            "tucked into a niche in the wall. Scratched into the "
            "stone: 'Good cat hunting. -K'"
        ),
        room_type="clearing",
        indoor=False,
    )

    ed_game_trail = area.room(
        "ed_game_trail",
        name="Game Trail",
        desc=(
            "A well-worn animal trail cuts across the hillside, "
            "winding between boulders and through gaps in the scrub. "
            "The trail is marked by scat, claw marks on tree bark, "
            "and shed fur caught on thorns. Predators and prey both "
            "use this route -- the claw marks of mountain cats "
            "overlay the hoof prints of deer."
        ),
        room_type="path",
        indoor=False,
    )

    ed_rockfall_clearing = area.room(
        "ed_rockfall_clearing",
        name="Rockfall Clearing",
        desc=(
            "A recent rockfall has cleared the vegetation from a "
            "section of hillside, creating an open area littered "
            "with fresh rubble. The exposed earth is raw and red. "
            "Young plants are already colonizing the disturbed soil. "
            "The rockfall exposed a small cave opening in the "
            "hillside that was previously hidden."
        ),
        room_type="clearing",
        indoor=False,
    )

    ed_small_cave = area.room(
        "ed_small_cave",
        name="Small Cave",
        desc=(
            "A shallow cave exposed by the rockfall. Only about "
            "fifteen feet deep, it holds no mysteries -- just damp "
            "stone, a few spiders, and the faint smell of minerals. "
            "But scratched into the back wall, barely visible: eight "
            "circles, the same pattern found throughout these mountains."
        ),
        room_type="cave",
        indoor=True,
    )

    ed_lower_meadow = area.room(
        "ed_lower_meadow",
        name="Lower Meadow",
        desc=(
            "A gently sloping meadow on the lower eastern foothills. "
            "The grass here is thicker and greener than higher up. "
            "Wildflowers dot the meadow in clusters -- yellow, white, "
            "and pale blue. The transition from mountain to lowlands "
            "is nearly complete. The Ashreach is visible to the south."
        ),
        room_type="clearing",
        indoor=False,
    )

    ed_boulder_gap = area.room(
        "ed_boulder_gap",
        name="Boulder Gap",
        desc=(
            "Two massive boulders lean against each other, forming a "
            "natural gateway. The gap between them is just wide enough "
            "for a single person. Beyond the gap, the terrain levels "
            "out into gentler hills. The boulders are covered in old "
            "lichen, suggesting they have stood like this for centuries."
        ),
        room_type="path",
        indoor=False,
    )

    ed_shrine_stones = area.room(
        "ed_shrine_stones",
        name="Shrine Stones",
        desc=(
            "Three standing stones arranged in a triangle, each about "
            "waist height. The stones are smooth and dark -- not local "
            "granite but something transported here deliberately. The "
            "triangle they form is precise. At the center, a shallow "
            "depression in the ground holds rainwater. Offerings -- "
            "a coin, a feather, a carved bone -- sit at the base of "
            "each stone. Someone still visits."
        ),
        room_type="ruins",
        indoor=False,
    )

    ed_foothill_edge = area.room(
        "ed_foothill_edge",
        name="Foothills Edge",
        desc=(
            "The last of the foothills, where mountain gives way to "
            "rolling lowlands. The Reth rises behind -- grey, massive, "
            "indifferent. Ahead, the land flattens into scrubby hills "
            "that will eventually become the Ashreach or the coast. "
            "The transition feels significant -- a boundary between "
            "worlds."
        ),
        room_type="path",
        indoor=False,
    )

    # Eastern Descent exits
    area.exit(ls_wind_gap, ed_high_trail, "east")
    area.exit(ed_high_trail, ls_wind_gap, "west")
    area.exit(ed_high_trail, ed_dry_creek, "south")
    area.exit(ed_dry_creek, ed_high_trail, "north")
    area.exit(ed_high_trail, ed_old_prospector, "east")
    area.exit(ed_old_prospector, ed_high_trail, "west")
    area.exit(ed_dry_creek, ed_thorn_thicket, "east")
    area.exit(ed_thorn_thicket, ed_dry_creek, "west")
    area.exit(ed_thorn_thicket, ed_hunters_blind, "north")
    area.exit(ed_hunters_blind, ed_thorn_thicket, "south")
    area.exit(ed_thorn_thicket, ed_game_trail, "south")
    area.exit(ed_game_trail, ed_thorn_thicket, "north")
    area.exit(ed_game_trail, ed_rockfall_clearing, "east")
    area.exit(ed_rockfall_clearing, ed_game_trail, "west")
    area.exit(ed_rockfall_clearing, ed_small_cave, "in")
    area.exit(ed_small_cave, ed_rockfall_clearing, "out")
    area.exit(ed_game_trail, ed_lower_meadow, "south")
    area.exit(ed_lower_meadow, ed_game_trail, "north")
    area.exit(ed_lower_meadow, ed_boulder_gap, "east")
    area.exit(ed_boulder_gap, ed_lower_meadow, "west")
    area.exit(ed_boulder_gap, ed_shrine_stones, "south")
    area.exit(ed_shrine_stones, ed_boulder_gap, "north")
    area.exit(ed_lower_meadow, ed_foothill_edge, "south")
    area.exit(ed_foothill_edge, ed_lower_meadow, "north")

    # ==================================================================
    #  MOB SPAWNS
    # ==================================================================

    # --- Rock Trolls (aggressive, high HP, slow) ---
    area.spawn(ls_troll_hollow, "rock_troll", count_min=1, count_max=2,
               respawn_minutes=15, respawn_variance=5,
               base_disposition=-0.4)
    area.spawn(ra_boulder_field, "rock_troll", count_min=0, count_max=1,
               respawn_minutes=20, respawn_variance=5,
               base_disposition=-0.3)
    area.spawn(wr_golem_debris, "rock_troll", count_min=1, count_max=1,
               respawn_minutes=20, respawn_variance=5,
               base_disposition=-0.3)
    area.spawn(ed_boulder_gap, "rock_troll", count_min=0, count_max=1,
               respawn_minutes=25, respawn_variance=8,
               base_disposition=-0.3)
    # Rock troll as hunter near mine entrance (D-28)
    area.spawn(gm_entrance, "rock_troll", count_min=1, count_max=1,
               respawn_minutes=20, respawn_variance=5,
               base_disposition=-0.5)
    area.spawn(ls_scree_slope, "rock_troll", count_min=0, count_max=1,
               respawn_minutes=20, respawn_variance=8,
               base_disposition=-0.3)
    area.spawn(ra_ridge_base, "rock_troll", count_min=0, count_max=1,
               respawn_minutes=25, respawn_variance=8,
               base_disposition=-0.3)
    area.spawn(ls_fourth_turn, "rock_troll", count_min=0, count_max=1,
               respawn_minutes=20, respawn_variance=5,
               base_disposition=-0.3)
    area.spawn(ed_rockfall_clearing, "rock_troll", count_min=0, count_max=1,
               respawn_minutes=25, respawn_variance=8,
               base_disposition=-0.3)

    # --- Mountain Cats (cautious ambush predator, some wander D-27) ---
    area.spawn(ls_narrow_ledge, "mountain_cat", count_min=1, count_max=1,
               respawn_minutes=12, respawn_variance=4,
               base_disposition=-0.2)
    area.spawn(ed_game_trail, "mountain_cat", count_min=1, count_max=2,
               respawn_minutes=12, respawn_variance=4,
               base_disposition=-0.2)
    area.spawn(ed_thorn_thicket, "mountain_cat", count_min=0, count_max=1,
               respawn_minutes=15, respawn_variance=5,
               base_disposition=-0.2)
    area.spawn(ra_ravine_edge, "mountain_cat", count_min=1, count_max=1,
               respawn_minutes=15, respawn_variance=5,
               base_disposition=-0.2)
    area.spawn(wr_cliff_face, "mountain_cat", count_min=0, count_max=1,
               respawn_minutes=18, respawn_variance=5,
               base_disposition=-0.2)
    area.spawn(mo_high_meadow, "mountain_cat", count_min=1, count_max=1,
               respawn_minutes=15, respawn_variance=5,
               base_disposition=-0.1)
    area.spawn(ra_old_camp, "mountain_cat", count_min=0, count_max=1,
               respawn_minutes=18, respawn_variance=5,
               base_disposition=-0.2)
    area.spawn(ls_second_turn, "mountain_cat", count_min=0, count_max=1,
               respawn_minutes=15, respawn_variance=5,
               base_disposition=-0.2)
    area.spawn(ls_rocky_shelf, "mountain_cat", count_min=1, count_max=1,
               respawn_minutes=15, respawn_variance=5,
               base_disposition=-0.2)
    area.spawn(wr_overhang, "mountain_cat", count_min=0, count_max=1,
               respawn_minutes=18, respawn_variance=5,
               base_disposition=-0.2)
    area.spawn(ed_lower_meadow, "mountain_cat", count_min=0, count_max=1,
               respawn_minutes=18, respawn_variance=5,
               base_disposition=-0.1)
    area.spawn(ed_hunters_blind, "mountain_cat", count_min=0, count_max=1,
               respawn_minutes=20, respawn_variance=5,
               base_disposition=-0.2)

    # --- Cave Spiders (aggressive, low HP, underground areas) ---
    area.spawn(cn_web_gallery, "cave_spider", count_min=1, count_max=2,
               respawn_minutes=10, respawn_variance=3,
               base_disposition=-0.3)
    area.spawn(cn_spider_den, "cave_spider", count_min=2, count_max=3,
               respawn_minutes=10, respawn_variance=3,
               base_disposition=-0.4)
    area.spawn(cn_web_bridge, "cave_spider", count_min=1, count_max=2,
               respawn_minutes=10, respawn_variance=3,
               base_disposition=-0.3)
    area.spawn(gm_deep_crosscut, "cave_spider", count_min=1, count_max=2,
               respawn_minutes=12, respawn_variance=4,
               base_disposition=-0.3)
    area.spawn(gm_collapse, "cave_spider", count_min=0, count_max=1,
               respawn_minutes=15, respawn_variance=5,
               base_disposition=-0.3)
    area.spawn(dc_egg_gallery, "cave_spider", count_min=1, count_max=2,
               respawn_minutes=10, respawn_variance=3,
               base_disposition=-0.4)
    area.spawn(dc_silk_chamber, "cave_spider", count_min=1, count_max=1,
               respawn_minutes=12, respawn_variance=4,
               base_disposition=-0.3)
    area.spawn(cn_entrance_hall, "cave_spider", count_min=0, count_max=1,
               respawn_minutes=12, respawn_variance=4,
               base_disposition=-0.3)
    area.spawn(cn_narrow_squeeze, "cave_spider", count_min=1, count_max=1,
               respawn_minutes=12, respawn_variance=4,
               base_disposition=-0.3)
    area.spawn(cn_echo_chamber, "cave_spider", count_min=0, count_max=1,
               respawn_minutes=15, respawn_variance=5,
               base_disposition=-0.3)
    area.spawn(cn_lower_junction, "cave_spider", count_min=1, count_max=2,
               respawn_minutes=10, respawn_variance=3,
               base_disposition=-0.4)
    area.spawn(dc_bone_corridor, "cave_spider", count_min=1, count_max=2,
               respawn_minutes=10, respawn_variance=3,
               base_disposition=-0.4)
    area.spawn(dc_grand_web, "cave_spider", count_min=1, count_max=2,
               respawn_minutes=10, respawn_variance=3,
               base_disposition=-0.5)
    area.spawn(gm_south_drift, "cave_spider", count_min=0, count_max=1,
               respawn_minutes=15, respawn_variance=5,
               base_disposition=-0.3)
    area.spawn(gm_flooded_shaft, "cave_spider", count_min=0, count_max=1,
               respawn_minutes=15, respawn_variance=5,
               base_disposition=-0.3)

    # --- Stone Golem Fragments (passive until attacked, very high HP) ---
    area.spawn(mo_golem_terrace, "stone_golem_fragment", count_min=1, count_max=1,
               respawn_minutes=30, respawn_variance=10,
               base_disposition=0.0)
    area.spawn(wr_golem_debris, "stone_golem_fragment", count_min=0, count_max=1,
               respawn_minutes=30, respawn_variance=10,
               base_disposition=0.0)
    area.spawn(mo_foundation, "stone_golem_fragment", count_min=1, count_max=1,
               respawn_minutes=30, respawn_variance=10,
               base_disposition=0.0)
    area.spawn(mo_ruins_arch, "stone_golem_fragment", count_min=0, count_max=1,
               respawn_minutes=35, respawn_variance=10,
               base_disposition=0.0)

    # --- Reth Eagles (aggressive flyer, moderate stats) ---
    area.spawn(ls_eagles_perch, "reth_eagle", count_min=1, count_max=2,
               respawn_minutes=12, respawn_variance=4,
               base_disposition=-0.3)
    area.spawn(wr_eagles_nest, "reth_eagle", count_min=2, count_max=3,
               respawn_minutes=12, respawn_variance=4,
               base_disposition=-0.4)
    area.spawn(wr_peak_trail, "reth_eagle", count_min=1, count_max=1,
               respawn_minutes=15, respawn_variance=5,
               base_disposition=-0.3)
    area.spawn(mo_minor_summit, "reth_eagle", count_min=0, count_max=1,
               respawn_minutes=18, respawn_variance=5,
               base_disposition=-0.2)
    area.spawn(ed_high_trail, "reth_eagle", count_min=0, count_max=1,
               respawn_minutes=20, respawn_variance=5,
               base_disposition=-0.2)
    area.spawn(wr_broken_cairn, "reth_eagle", count_min=0, count_max=1,
               respawn_minutes=18, respawn_variance=5,
               base_disposition=-0.2)
    area.spawn(mo_south_overlook, "reth_eagle", count_min=0, count_max=1,
               respawn_minutes=20, respawn_variance=5,
               base_disposition=-0.2)
    area.spawn(wr_windblast_pass, "reth_eagle", count_min=0, count_max=1,
               respawn_minutes=20, respawn_variance=5,
               base_disposition=-0.2)
    area.spawn(ra_lookout_rock, "reth_eagle", count_min=0, count_max=1,
               respawn_minutes=20, respawn_variance=5,
               base_disposition=-0.2)
    area.spawn(ls_herb_ledge, "reth_eagle", count_min=0, count_max=1,
               respawn_minutes=20, respawn_variance=5,
               base_disposition=-0.2)
    area.spawn(ed_dry_creek, "mountain_cat", count_min=0, count_max=1,
               respawn_minutes=18, respawn_variance=5,
               base_disposition=-0.2)

    # ==================================================================
    #  NAMED MOB -- Grandmother Spider (D-20)
    #  Ancient cave spider, 120-min respawn, deepest cave
    # ==================================================================

    area.named_mob(
        "grandmother_spider", dc_lair,
        respawn_minutes=120,
        respawn_variance=30,
        prestige_modifier=3.0,
        base_disposition=-0.8,
        tome_drop="lore_grandmother_spider",
    )

    # ==================================================================
    #  FIELD NPCs (D-22: 3 NPCs with dialogue and quest hooks)
    # ==================================================================

    # 1. Mining Foreman (Consortium faction) -- quest hook about lost miners
    area.npc(
        gm_foreman_office, "npc_foreman_halvek",
        faction="consortium",
        trainer_id="npc_trainer_smithing_reth",
        dialogue={
            "greeting": (
                "Halvek flattens a survey map with both hands. 'If the mine "
                "wanted to be quiet, it chose a poor week for it. I need facts "
                "before the Consortium turns fear into policy.'"
            ),
            "topics": {
                "miners": (
                    "'Three went below with chalk, rope, and enough sense to "
                    "turn back. Their last marks point from the collapse to "
                    "the lower passage, then into the deep caverns. Follow the "
                    "marks in order or you will learn nothing useful.'"
                ),
                "survey": (
                    "'A productive cut is one thing. A productive cut punched "
                    "through old working stone is another. If the hidden alcove, "
                    "the foundation, and that old nest agree, I close the seam.'"
                ),
                "consortium": (
                    "'Profit keeps lamps lit. I know that. But coin spends "
                    "poorly if the mountain starts answering back.'"
                ),
            },
            "base_hints": [
                "Halvek's map links the collapse, lower passage, and deep caverns with fresh chalk.",
                "A second sheet on Halvek's desk compares mine cuts against older stonework.",
            ],
        },
    )

    # 2. Warden Patrol Captain -- quest about troll activity
    area.npc(
        ra_warden_camp, "npc_warden_captain_serra",
        faction="wardens",
        dialogue={
            "greeting": (
                "Serra rolls a patrol token between two scarred fingers. 'The "
                "foothills look open until a boulder stands up and swings. "
                "Tell me you brought patience as well as steel.'"
            ),
            "topics": {
                "trolls": (
                    "'They are not wandering at random. The hollow below the "
                    "switchbacks is active again, and every troll we drive off "
                    "there buys a safer shift for the mine camps.'"
                ),
                "patrol": (
                    "'Cold ruins judgment faster than fear. Renn's tonic keeps "
                    "my patrols moving when the wind comes down wrong, which is "
                    "why a delivery can matter as much as a blade.'"
                ),
                "line": (
                    "'The line is not a wall. It is people watching routes, "
                    "sharing warnings, and refusing to let one bad pass become "
                    "everyone's disaster.'"
                ),
            },
            "base_hints": [
                "Serra's stones mark the troll hollow, the mine entrance, and the western ridge.",
                "A folded tonic request sits under Serra's patrol knife.",
            ],
        },
    )

    # 3. Hermit Alchemist -- rare ingredient dialogue
    area.npc(
        wr_hermit_cave, "npc_hermit_alchemist_old_renn",
        faction=None,
        dialogue={
            "greeting": (
                "Renn looks up from a steaming clay cup. 'If you are bleeding, "
                "sit. If you are asking, speak softly. The mountain gives better "
                "answers to people who do not shout over it.'"
            ),
            "topics": {
                "tonic": (
                    "'Serra's patrol tonic is not bravery in a bottle. It is "
                    "warm hands, clear breath, and fewer foolish deaths on a "
                    "ridge that does not care who outranks whom.'"
                ),
                "ingredients": (
                    "'Good alpine stock grows where stone holds memory: the herb "
                    "ledge, the high meadow, the lower meadow, and the spring. "
                    "Take enough for medicine, not enough to teach the ledges "
                    "mistrust.'"
                ),
                "foundation": (
                    "'Halvek thinks in claims and supports. I think in patterns "
                    "that keep turning up where no one planted them. Between us, "
                    "we may yet become almost wise.'"
                ),
            },
            "base_hints": [
                "Renn's drying cord separates alpine cuttings by where the stone around them held warmth.",
                "A half-finished tonic recipe is written over an older sketch of eight radiating chambers.",
            ],
        },
    )

    # ==================================================================
    #  LORE FRAGMENTS (D-24: 5 fragments in ruins/caves)
    # ==================================================================

    area.lore_fragment(
        "lore_reth_mine_symbols", gm_hidden_alcove,
        discovery_method="search",
        scholar_path="remnance",
        text=(
            "The symbols in the hidden alcove predate the Greystone Mine "
            "by millennia. They are arranged in groups of eight -- the same "
            "notation found on the Ashwatch Tower in Vael's Crossing. "
            "The warmth radiating from them is consistent and sourceless. "
            "A careful survey would mark this as a dormant node signature "
            "-- the mine was dug through it without knowing what lay in "
            "the rock."
        ),
        insight_gain=8,
    )

    area.lore_fragment(
        "lore_reth_golem_terrace", mo_golem_terrace,
        discovery_method="search",
        text=(
            "The broken golem on the terrace is of a design that matches "
            "no known Imperial construction period. Its joints are fitted "
            "with eight-fold symmetry -- the same mathematical base that "
            "appears in the oldest surviving engineered sites. The golem was not built "
            "by humans. It was built by something that thought in eights."
        ),
        insight_gain=6,
    )

    area.lore_fragment(
        "lore_reth_foundation", mo_foundation,
        discovery_method="search",
        scholar_path="remnance",
        text=(
            "The ancient foundation's layout -- a central circle with "
            "eight radiating chambers -- matches theoretical diagrams "
            "of a node resonance amplifier. If this building functioned "
            "as designed, it would have been capable of amplifying node "
            "energy across the entire Reth mountain range. The builders "
            "understood something about the infrastructure that has been "
            "forgotten for a thousand years."
        ),
        insight_gain=10,
    )

    area.lore_fragment(
        "lore_reth_summit_pillar", mo_minor_summit,
        discovery_method="search",
        text=(
            "The stone pillar at the summit is carved with a single word "
            "in a script that predates all known writing systems. The word "
            "has no translation. Standing beside it in wind, the air "
            "moves in a pattern -- a vortex with eight arms. The pillar "
            "is not decorative. It is functional. It still works."
        ),
        insight_gain=5,
    )

    area.lore_fragment(
        "lore_reth_old_nest", dc_old_nest,
        discovery_method="search",
        scholar_path="remnance",
        text=(
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
        insight_gain=12,
    )

    # ==================================================================
    #  QUESTS (enriched specs — D-21/D-22)
    # ==================================================================

    area.quest("rf_q_lost_miners",
        name="Lost in the Deep",
        description="Foreman Halvek's survey team went silent while tracing a fresh collapse, a blocked passage, and the deeper caverns beyond it. Follow their route in order and learn whether the mountain took them, or whether they opened something they should have left buried.",
        quest_type="investigation",
        quest_giver="npc_foreman_halvek",
        prerequisite_quests=["vc_q_forging_commission"],
        objectives=[
            {"type": "investigate", "target": "gm_collapse", "count": 1,
             "description": "Search the collapsed section for the survey team's trail"},
            {"type": "investigate", "target": "rf_mountain_passage", "count": 1,
             "description": "Check the blocked mountain passage the team was mapping"},
            {"type": "investigate", "target": "dc_bone_corridor", "count": 1,
             "description": "Follow the route into the deep caverns below the dig"},
        ],
        rewards=[
            {"action_type": "give_scales", "amount": 90},
            {"action_type": "modify_standing", "faction_id": "consortium", "delta": 200},
            {"action_type": "echo", "message": "|gHalvek's weathered face creases with relief. \"Alive, then. Thank the stone. The Consortium will remember this -- and so will I.\"|n"},
        ],
        next_quest_id="rf_q_foundation_survey",
        one_chance=True,
        # Legacy fields (backward compat)
        objective_type="investigate",
        objective_target="gm_collapse",
        objective_count=1,
        consequence_small="Halvek pins the survey team's route beside the mine map, turning rumor into a route others can check",
        consequence_medium="Consortium mine talk can remember that your first answer in Reth was evidence before extraction",
    )

    area.quest("rf_q_troll_menace",
        name="Troll Country",
        description="Captain Serra warns that trolls have moved into the lower foothills from their highland territories. They must be driven back before they threaten the mining camps and cut off the ore supply entirely.",
        quest_type="combat",
        quest_giver="npc_warden_captain_serra",
        objectives=[
            {"type": "investigate", "target": "ls_troll_hollow", "count": 1,
             "description": "Find the active troll hollow feeding attacks toward the road"},
            {"type": "kill", "target": "rock_troll", "count": 5,
             "description": "Drive rock trolls back from the lower foothill routes"},
        ],
        rewards=[
            {"action_type": "give_scales", "amount": 120},
            {"action_type": "modify_standing", "faction_id": "wardens", "delta": 250},
            {"action_type": "give_skill_xp", "skill_id": "reflexes", "count": 4},
            {"action_type": "echo", "message": "|gSerra examines the troll-tooth trophies with a soldier's eye. \"Five less to worry about. The foothills won't thank you, but the miners will.\"|n"},
        ],
        # Legacy fields (backward compat)
        objective_type="kill",
        objective_target="rock_troll",
        objective_count=5,
        one_chance=True,
        consequence_small="Serra moves a patrol token back onto the lower route after your report proves the troll hollow can be checked",
        consequence_medium="Warden patrol dialogue can treat you as someone who reads threat routes, not only a tally of bodies",
    )

    area.quest("rf_q_rare_ingredients",
        name="Mountain Remedies",
        description="Old Renn needs rare alpine ingredients from the herb ledge, the high meadow, and the colder eastern slopes. Gather them while the season still holds; once the frost locks in, the patrol line loses its best tonic for the whole winter.",
        quest_type="gathering",
        quest_giver="npc_hermit_alchemist_old_renn",
        prerequisite_quests=["vc_q_herbalist_gathering", "rf_q_patrol_request"],
        objectives=[
            {"type": "collect", "target": "rare_alpine_ingredient", "count": 4,
             "description": "Gather rare alpine ingredients from the high foothills"},
        ],
        rewards=[
            {"action_type": "give_scales", "amount": 70},
            {"action_type": "give_skill_xp", "skill_id": "herbalism", "count": 4},
            {"action_type": "learn_recipe", "recipe_id": "mountain_tonic"},
            {"action_type": "echo", "message": "|gRenn sniffs each ingredient with an alchemist's precision. \"Perfect specimens. Here -- I'll teach you the mountain tonic. The recipe is old, older than the Empire.\"|n"},
        ],
        one_chance=True,
        # Legacy fields (backward compat)
        objective_type="gather",
        objective_target="rare_mountain_ingredient",
        objective_count=4,
        consequence_small="Renn labels your gathered stock by ledge and weather, making the next patrol tonic a record of where the mountain helped",
        consequence_medium="The mountain tonic recipe enters your practice history as medicine learned from place, season, and restraint",
    )

    area.quest("rf_q_patrol_request",
        name="A Tonic for the Line",
        description="Captain Serra needs Renn to prepare a fresh tonic batch for the lower-pass patrols before the next cold front rolls down. Carry the request west to the hermit's cave; Serra cannot spare a runner while trolls are testing the road.",
        quest_type="delivery",
        quest_giver="npc_warden_captain_serra",
        objectives=[
            {"type": "deliver", "target": "npc_hermit_alchemist_old_renn", "count": 1,
             "description": "Carry Serra's tonic request to Old Renn on the western ridge"},
        ],
        flagged_drop="patrol_tonic_request",
        rewards=[
            {"action_type": "give_scales", "amount": 65},
            {"action_type": "modify_standing", "faction_id": "wardens", "delta": 125},
            {"action_type": "echo", "message": "|gSerra folds Renn's answer into her map case. \"Good. The line keeps men alive because somebody thinks ahead. Today that somebody was you.\"|n"},
        ],
        next_quest_id="rf_q_rare_ingredients",
        one_chance=True,
        objective_type="deliver",
        objective_target="npc_hermit_alchemist_old_renn",
        objective_count=1,
        consequence_small="Serra tucks Renn's answer into the patrol case, and the western ridge gains a planned tonic run before the cold front",
        consequence_medium="Later Warden route talk can remember that you kept the patrol line alive with preparation instead of rescue",
    )

    area.quest("rf_q_foundation_survey",
        name="What the Mountain Was Built For",
        description="Halvek wants proof before he shuts a productive cut, and Renn wants proof before anyone digs farther. Compare the hidden alcove, the ancient foundation, and the old nest in the deep caverns to learn whether the miners broke into a structure instead of a vein.",
        quest_type="investigation",
        quest_giver="npc_foreman_halvek",
        prerequisite_quests=["rf_q_lost_miners"],
        objectives=[
            {"type": "investigate", "target": "gm_hidden_alcove", "count": 1,
             "description": "Examine the hidden alcove cut into the mine wall"},
            {"type": "investigate", "target": "mo_foundation", "count": 1,
             "description": "Survey the exposed foundation on the mountain ridge"},
            {"type": "investigate", "target": "dc_old_nest", "count": 1,
             "description": "Compare the symbols hidden behind the old nest in the deep caverns"},
        ],
        rewards=[
            {"action_type": "give_scales", "amount": 100},
            {"action_type": "modify_standing", "faction_id": "consortium", "delta": 150},
            {"action_type": "give_skill_xp", "skill_id": "investigation", "count": 4},
            {"action_type": "echo", "message": "|gHalvek studies the copied marks in silence before handing them to Renn. \"That is not mine work,\" he mutters. \"That means the mountain owed us warning before it owed us ore.\"|n"},
        ],
        one_chance=True,
        objective_type="investigate",
        objective_target="gm_hidden_alcove",
        objective_count=1,
        consequence_small="Halvek files the hidden alcove, foundation, and old nest under one red cord instead of three unrelated hazards",
        consequence_medium="Reth's mine story can shift from reopening a vein toward proving what older structure the miners disturbed",
    )

    area.lore_fragment(
        "lore_reth_patrol_cairn", ls_miners_rest,
        discovery_method="search",
        text=(
            "The stacked stones at Miner's Rest hide an older marker at their "
            "center: a carved wedge aligned with the pass, the western ridge, "
            "and the summit pillar. The Wardens keep a camp here because the "
            "older road planners already decided this was the mountain's hinge."
        ),
        insight_gain=4,
    )

    area.lore_fragment(
        "lore_reth_herb_terrace", ls_herb_ledge,
        discovery_method="search",
        text=(
            "The ledge wall is too even to be natural. Someone cut shallow "
            "planting shelves into the stone long before the current herb "
            "growth took hold. The alpine remedies survive here because this "
            "ledge was cultivated on purpose."
        ),
        insight_gain=5,
    )

    area.trigger(
        ls_herb_ledge, "on_examine",
        actions=[{"action_type": "give_item", "item_id": "rare_alpine_ingredient"}],
        trigger_id="rf_alpine_ingredient_herb_ledge",
    )
    area.trigger(
        mo_high_meadow, "on_examine",
        actions=[{"action_type": "give_item", "item_id": "rare_alpine_ingredient"}],
        trigger_id="rf_alpine_ingredient_high_meadow",
    )
    area.trigger(
        ed_lower_meadow, "on_examine",
        actions=[{"action_type": "give_item", "item_id": "rare_alpine_ingredient"}],
        trigger_id="rf_alpine_ingredient_lower_meadow",
    )
    area.trigger(
        ra_spring, "on_examine",
        actions=[{"action_type": "give_item", "item_id": "rare_alpine_ingredient"}],
        trigger_id="rf_alpine_ingredient_spring",
    )

    # ==================================================================
    #  MATERIALS (D-24: zone-level harvestable materials)
    # ==================================================================

    area.material("iron_ore", tier=1, terrain="underground",
                  profession_bonus={"smithing": 0.1})
    area.material("copper_ore", tier=1, terrain="underground",
                  profession_bonus={"smithing": 0.08})
    area.material("mountain_herb", tier=1, terrain="clearing",
                  profession_bonus={"herbalism": 0.08, "alchemy": 0.05})

    # ==================================================================
    #  TRAINER NPCs (09-02: wilderness trainers)
    # ==================================================================

    # Climbing trainer at cliff face
    area.npc(
        wr_cliff_face, "npc_trainer_climbing_reth",
        name="Grenn",
        title="Mountain Guide",
        desc="A wiry man with scarred hands and a coil of rope over one shoulder. He leans against the rock face, testing handholds with casual expertise.",
        faction=None,
        trainer_id="npc_trainer_climbing_reth",
        dialogue={"greeting": "Grenn looks you up and down. 'The foothills are gentle enough, but the real peaks will kill you if you do not know what you are doing. I can teach you to read the rock. It is not cheap, but it is cheaper than a funeral.'", "topics": {"climbing": "'Three rules: test every hold twice, never look down when you are committed, and always know your escape route before you start. The mountain does not forgive mistakes.'"}},
    )

    # ==================================================================
    #  PRACTICE OPPORTUNITIES (one-shot journey-start mountaincraft)
    # ==================================================================

    area.practice_opportunity(
        "reth_road_test_old_camp_ashes",
        ra_old_camp,
        verb="test",
        target="old camp ashes",
        skill_awards={"survival": 3, "tracking": 1},
        domain_awards={"naturalism": 75},
        success_text="You sift the ash without scattering it and spot the difference between a cold camp, a rushed camp, and a camp abandoned under pressure.",
        once_per_character=True,
        visible_in_exits=True,
        desc="test old camp ashes",
    )
    area.practice_opportunity(
        "reth_ridge_climb_lookout_rock",
        ra_lookout_rock,
        verb="climb",
        target="lookout rock",
        skill_awards={"climbing": 3, "navigation": 1},
        domain_awards={"combat": 60},
        success_text="You climb with three points of contact and learn why the easiest-looking handhold is not always the safest one.",
        once_per_character=True,
        visible_in_exits=True,
        desc="climb lookout rock",
    )
    area.practice_opportunity(
        "reth_ledge_follow_goat_trail",
        ls_goat_trail,
        verb="track",
        target="goat trail",
        skill_awards={"tracking": 3, "climbing": 1},
        domain_awards={"naturalism": 75},
        success_text="You follow the goat trail by scuffs and droppings, finding the line that hooves trust and boots usually miss.",
        once_per_character=True,
        visible_in_exits=True,
        desc="track goat trail",
    )
    area.practice_opportunity(
        "reth_mine_brace_ore_cart",
        gm_ore_cart_bay,
        verb="brace",
        target="ore cart",
        skill_awards={"engineering": 3, "mining": 1},
        domain_awards={"engineering": 75},
        success_text="You chock the ore cart before testing the brake, turning a dangerous roll into a controlled repair lesson.",
        once_per_character=True,
        visible_in_exits=True,
        desc="brace ore cart",
    )
    area.practice_opportunity(
        "reth_mine_read_ventilation_flow",
        gm_ventilation_shaft,
        verb="read",
        target="ventilation flow",
        skill_awards={"engineering": 2, "survival": 1},
        domain_awards={"engineering": 60},
        success_text="You hold a dust thread in the draft and trace how stale air moves through the shaft before the bad pockets become obvious.",
        once_per_character=True,
        visible_in_exits=True,
        desc="read ventilation flow",
    )
    area.practice_opportunity(
        "reth_cavern_study_fossil_wall",
        cn_fossil_wall,
        verb="study",
        target="fossil wall",
        skill_awards={"scholarship": 3, "investigation": 1},
        domain_awards={"resonance": 60},
        success_text="You compare shell layers and tool scratches until the wall reads less like decoration and more like a record of old water and older hands.",
        once_per_character=True,
        visible_in_exits=True,
        desc="study fossil wall",
    )
    area.practice_opportunity(
        "reth_crystal_read_pulse",
        cn_crystal_alcove,
        verb="read",
        target="crystal pulse",
        skill_awards={"node_reading": 3},
        domain_awards={"resonance": 75},
        success_text="You listen with your fingertips near the crystal, catching the uneven pulse that warns where the old stone is still under strain.",
        once_per_character=True,
        visible_in_exits=True,
        desc="read crystal pulse",
    )
    area.practice_opportunity(
        "reth_windgap_evade_crossgust",
        ls_wind_gap,
        verb="evade",
        target="crossgust",
        skill_awards={"reflexes": 3},
        domain_awards={"combat": 60},
        success_text="You wait for the gust to twist before stepping, learning to react to the mountain's rhythm instead of your own impatience.",
        once_per_character=True,
        visible_in_exits=True,
        desc="evade crossgust",
    )

    # ==================================================================
    #  TRIGGERS (09-02: zone entry, recipe learning)
    # ==================================================================

    # Zone entry — first visit atmospheric welcome
    area.trigger(
        ra_road_south, "on_first_visit",
        [{"action_type": "echo", "message": "|yThe air thins as the road climbs into the Reth Foothills. Jagged peaks loom above, their faces scarred with old mine shafts. The wind carries the distant ring of hammers on stone.|n"}],
        trigger_id="reth_first_entry",
        once_per_character=True,
    )

    # Recipe: steel sword from Foreman Halvek
    area.trigger(
        gm_foreman_office, "on_first_visit",
        [{"action_type": "learn_recipe", "recipe_id": "steel_sword", "learned_from": "Foreman Halvek", "message": "|gHalvek sketches a blade design on scrap parchment. 'Mountain steel holds an edge longer than city iron.' You have learned to forge |wSteel Sword|g.|n"}],
        trigger_id="reth_learn_steel_sword",
        once_per_character=True,
    )

    # Recipe: iron breastplate from Foreman Halvek
    area.trigger(
        gm_foreman_office, "on_first_visit",
        [{"action_type": "learn_recipe", "recipe_id": "iron_breastplate", "learned_from": "Foreman Halvek", "message": "|gHalvek shows you a breastplate mold. 'Five ingots, two straps. Simple, if your arm is strong enough.' You have learned to forge |wIron Breastplate|g.|n"}],
        trigger_id="reth_learn_iron_breastplate",
        once_per_character=True,
    )

    # ==================================================================
    #  GATHERING POOLS
    # ==================================================================

    area.gathering_pool(
        "ore",
        rooms=["gm_iron_face", "gm_copper_chamber", "gm_deep_crosscut", "gm_north_drift", "cn_crystal_alcove"],
        materials=["copper_ore", "iron_ore"],
        max_active=3, respawn_minutes=12, respawn_variance=4,
    )
    area.gathering_pool(
        "herb",
        rooms=["ls_herb_ledge", "ra_spring", "ra_scrub_flat", "ed_lower_meadow", "mo_high_meadow"],
        materials=["mountain_herb"],
        max_active=3, respawn_minutes=10, respawn_variance=3,
    )
    area.gathering_pool(
        "fish",
        rooms=["ra_spring", "cn_stream_passage", "cn_underground_pool", "dc_deep_pool"],
        materials=["river_trout", "cave_eel"],
        max_active=2, respawn_minutes=14, respawn_variance=4,
    )

    # ==================================================================
    #  BUILD
    # ==================================================================

    return area.build()
