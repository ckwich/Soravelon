"""
Vael's Crossing -- Hub City Zone Spec

Soravelon's first hub city. A dark frontier outpost on Sorath's eastern edge
where old roads, river traffic, and the rough country beyond the walls meet.
Gritty, worn, practical -- a crossroads town built by the Empire but shaped
by everyone who washes through it.

100+ rooms across 7 districts, 50+ NPCs, all city services.
No levels -- zone scaling makes all content universal.

Districts:
    1. Harbor Gate District  (~15 rooms) -- Main entrance, greeter, zone exits
    2. Market District       (~20 rooms) -- Vendors, forge, bustling trade
    3. Guild Quarter         (~20 rooms) -- All 10 guild halls
    4. Consortium Quarter    (~15 rooms) -- Bank, trading houses
    5. Imperial Quarter      (~15 rooms) -- Garrison, medic, courier platform
    6. Residential District  (~15 rooms) -- Inns, tavern, homes, crafting
    7. The Warrens           (~15 rooms) -- Hidden underworld, mob spawns
"""

from world.area_builder import AreaBuilder


def build():
    area = AreaBuilder("vaels_crossing")

    # ------------------------------------------------------------------
    # Zone setup
    # ------------------------------------------------------------------
    area.zone(
        name="Vael's Crossing",
        zone_type="frontier",
        continent="sorath",
        faction_territory="imperial",
        faction_presence=["empire", "consortium", "wardens"],
        world_x=0,
        world_y=0,
        world_radius=100,
    )

    # ==================================================================
    #  DISTRICT 1: HARBOR GATE (~15 rooms)
    #  Main entrance, arrival point, Imperial checkpoint, greeter NPC.
    #  Thematic paths lead outward to starter zones.
    # ==================================================================

    hg_arrival = area.room(
        "hg_arrival",
        name="Harbor Gate - Arrival Square",
        desc=(
            "Dust and grit swirl through a broad square paved with cracked "
            "flagstones. A weathered gatehouse looms to the south, its iron "
            "portcullis raised and rust-streaked. Imperial banners -- faded "
            "red and gold -- hang limp from poles flanking the entrance. "
            "Wagons queue at the checkpoint while harried merchants argue "
            "with guards over manifest tallies. A greeter in worn city livery "
            "stands near a notice board, waving newcomers forward."
        ),
        room_type="building",
        indoor=False,
        ambient_echoes=[
            "A wagon rattles through the gate, its axle squealing.",
            "An Imperial guard shouts for the next traveler in line.",
            "Dust blows in from the plains beyond the gatehouse.",
            "A merchant curses as a crate slips from a cart.",
        ],
    )
    # D-11: Tag arrival square as new character spawn point
    hg_arrival.tags.add("greeter_room", category="spawn_point")

    hg_gatehouse = area.room(
        "hg_gatehouse",
        name="Harbor Gate - Gatehouse",
        desc=(
            "The gatehouse is a squat, functional structure of grey stone "
            "and riveted iron. Murder holes line the ceiling and arrow slits "
            "pierce the walls -- though the guards stationed here look more "
            "bored than vigilant. A ledger desk sits near the inner arch "
            "where a clerk records the names of everyone who enters. The "
            "smell of old stone and oiled leather fills the narrow passage."
        ),
        room_type="building",
        indoor=True,
    )

    hg_south_road = area.room(
        "hg_south_road",
        name="The Ashway - City Approach",
        desc=(
            "A wide dirt road stretches south across the Ashreach plains, "
            "the horizon a brown line broken only by scraggly thornbush. "
            "Deep wagon ruts carve the road into muddy channels after rain. "
            "Ash-grey dust coats everything -- boots, clothes, lungs. The "
            "road is named for the ancient fires that scorched these plains "
            "in a forgotten age. To the north, Vael's Crossing hunkers "
            "behind its walls."
        ),
        room_type="path",
        indoor=False,
        ambient_echoes=[
            "Wind sweeps ash-colored dust across the road.",
            "A courier dragon passes high overhead, shadow racing across the plains.",
            "Something howls far out on the Ashreach -- too distant to identify.",
        ],
    )

    hg_east_road = area.room(
        "hg_east_road",
        name="Harbor Road - Eastward",
        desc=(
            "The Harbor Road runs east toward the jagged northeastern "
            "coastline of Varath. Salt air mixes with dust from the plains. "
            "Imperial mile markers -- stone pillars carved with distances "
            "in the old system -- line the route at irregular intervals. "
            "The road is well-maintained here but narrows to a track "
            "beyond the next ridge."
        ),
        room_type="path",
        indoor=False,
    )

    hg_west_road = area.room(
        "hg_west_road",
        name="Cantera Trail - Westward",
        desc=(
            "A narrower trail winds west toward the dark tree line of "
            "the Cantera Forest. The air feels different here -- heavier, "
            "older. Pala trees are visible at the forest's edge, their "
            "bone-pale branches clicking in the wind like distant chimes. "
            "Few wagons take this route. The forest has a reputation."
        ),
        room_type="path",
        indoor=False,
        ambient_echoes=[
            "The pale branches of distant Pala trees click and rattle.",
            "A bird calls from the forest edge -- an unfamiliar song.",
        ],
    )

    hg_north_road = area.room(
        "hg_north_road",
        name="Rethward Pass - Northward",
        desc=(
            "The road climbs north toward the foothills of The Reth, "
            "the mountain spine of Varath. Rocky outcroppings replace "
            "the flat plains within a few miles. The pass is named for "
            "the mountains it approaches -- their grey teeth visible "
            "on clear days. Miners and prospectors use this route, "
            "their pack animals laden with ore."
        ),
        room_type="path",
        indoor=False,
    )

    hg_guard_post = area.room(
        "hg_guard_post",
        name="Harbor Gate - Guard Post",
        desc=(
            "A small stone building beside the gate houses the watch "
            "rotation. Bunks line one wall, a weapon rack the other. "
            "A duty roster is pinned to a board near the door, names "
            "crossed off and rewritten in different hands. The guards "
            "here work twelve-hour shifts and complain about all of them."
        ),
        room_type="building",
        indoor=True,
    )

    hg_stable = area.room(
        "hg_stable",
        name="Harbor Gate - City Stables",
        desc=(
            "The city stables smell of hay, manure, and leather. Stalls "
            "line both sides of a long, low building. A Kau'roran stable "
            "hand moves between the animals with surprising gentleness "
            "for someone of his size. Saddles and tack hang from pegs "
            "along the walls. A water trough near the entrance is "
            "perpetually half-empty."
        ),
        room_type="building",
        indoor=True,
        ambient_echoes=[
            "A horse stamps and snorts in its stall.",
            "The stable hand murmurs to a nervous mare.",
        ],
    )

    hg_plaza_north = area.room(
        "hg_plaza_north",
        name="Harbor Gate - Northern Plaza",
        desc=(
            "The northern edge of the arrival plaza opens onto a wider "
            "avenue leading deeper into the city. A weathered stone "
            "fountain -- long dry -- stands at the center, its basin "
            "used as a message drop by locals. The avenue splits: east "
            "toward the Market District, west toward the Guild Quarter."
        ),
        room_type="path",
        indoor=False,
    )

    hg_notice_wall = area.room(
        "hg_notice_wall",
        name="Harbor Gate - Notice Wall",
        desc=(
            "An entire section of the gatehouse wall has been given "
            "over to public notices. Bounties, wanted posters, work "
            "offers, and missing-person notices layer over each other "
            "in a palimpsest of desperation and commerce. Some notices "
            "are years old, their ink faded to ghost-writing."
        ),
        room_type="building",
        indoor=False,
    )

    hg_customs_office = area.room(
        "hg_customs_office",
        name="Harbor Gate - Customs Office",
        desc=(
            "A cramped room behind the gatehouse where Imperial customs "
            "officials process trade goods. Ledgers are stacked on every "
            "surface. A scale for weighing goods sits on the counter, its "
            "brass pans tarnished green. The clerk behind the desk has "
            "the thousand-yard stare of someone who has stamped too many "
            "forms in one lifetime."
        ),
        room_type="building",
        indoor=True,
    )

    hg_wagon_yard = area.room(
        "hg_wagon_yard",
        name="Harbor Gate - Wagon Yard",
        desc=(
            "An open yard where merchants park their wagons while goods "
            "clear customs. Broken wheels lean against the fence. A "
            "wheelwright's workshop occupies the far corner, the sound "
            "of hammering echoing off the walls. Children dart between "
            "the wagons, playing games with stolen fruit."
        ),
        room_type="path",
        indoor=False,
        ambient_echoes=[
            "A wheelwright hammers a rim onto a new wheel.",
            "Children shriek with laughter between the parked wagons.",
        ],
    )

    hg_watchtower_base = area.room(
        "hg_watchtower_base",
        name="Ashwatch Tower - Base",
        desc=(
            "The base of an old watchtower built from darker stone than "
            "the rest of the city. The Ashwatch Tower predates Vael's "
            "Crossing by centuries -- nobody is sure who built it or why. "
            "Its stones are fitted without mortar in a style that matches "
            "no known Imperial technique. A narrow spiral staircase winds "
            "upward into shadow."
        ),
        room_type="building",
        indoor=True,
    )

    hg_watchtower_top = area.room(
        "hg_watchtower_top",
        name="Ashwatch Tower - Summit",
        desc=(
            "From the top of the Ashwatch Tower the entire Ashreach is "
            "visible -- a brown sea of grass and dust stretching to the "
            "horizon. To the north, The Reth's grey peaks. To the west, "
            "the dark smudge of the Cantera Forest. To the east, a "
            "distant glitter that might be the coast. The wind up here "
            "is constant and cold. Carved into the parapet stones are "
            "symbols that match nothing in any Imperial record."
        ),
        room_type="building",
        indoor=False,
        ambient_echoes=[
            "Wind keens through the ancient stonework of the tower.",
            "A courier dragon circles lazily in the distance.",
            "You can see the entire Ashreach from up here -- vast and empty.",
        ],
    )

    hg_alley = area.room(
        "hg_alley",
        name="Harbor Gate - Narrow Alley",
        desc=(
            "A cramped alley between the gatehouse wall and a row of "
            "squat buildings. Rainwater collects in puddles that never "
            "fully dry. The alley smells of mildew and something sour. "
            "A half-hidden doorway at the far end leads somewhere "
            "the guards pretend not to know about."
        ),
        room_type="path",
        indoor=False,
    )

    # Harbor Gate exits
    area.exit(hg_arrival, hg_gatehouse, "south")
    area.exit(hg_gatehouse, hg_arrival, "north")
    area.exit(hg_gatehouse, hg_south_road, "south")
    area.exit(hg_south_road, hg_gatehouse, "north")
    area.exit(hg_arrival, hg_plaza_north, "north")
    area.exit(hg_plaza_north, hg_arrival, "south")
    area.exit(hg_arrival, hg_guard_post, "east")
    area.exit(hg_guard_post, hg_arrival, "west")
    area.exit(hg_arrival, hg_stable, "west")
    area.exit(hg_stable, hg_arrival, "east")
    area.exit(hg_arrival, hg_notice_wall, "northeast")
    area.exit(hg_notice_wall, hg_arrival, "southwest")
    area.exit(hg_guard_post, hg_customs_office, "north")
    area.exit(hg_customs_office, hg_guard_post, "south")
    area.exit(hg_stable, hg_wagon_yard, "north")
    area.exit(hg_wagon_yard, hg_stable, "south")
    area.exit(hg_watchtower_base, hg_watchtower_top, "up")
    area.exit(hg_watchtower_top, hg_watchtower_base, "down")
    area.exit(hg_plaza_north, hg_watchtower_base, "west")
    area.exit(hg_watchtower_base, hg_plaza_north, "east")
    area.exit(hg_gatehouse, hg_alley, "east")
    area.exit(hg_alley, hg_gatehouse, "west")

    # Thematic zone exit stubs (will be cross-zone exits when zones load)
    area.exit(hg_south_road, hg_arrival, "north")
    area.exit(hg_arrival, hg_south_road, "south")
    area.exit(hg_south_road, "ashreach_plains:ash_road_01", "south")
    area.exit(hg_east_road, hg_plaza_north, "west")
    area.exit(hg_plaza_north, hg_east_road, "east")
    area.exit(hg_west_road, hg_plaza_north, "west")
    area.exit(hg_plaza_north, hg_west_road, "east")
    area.exit(hg_wagon_yard, hg_west_road, "west")
    area.exit(hg_west_road, hg_wagon_yard, "east")
    area.exit(hg_north_road, hg_plaza_north, "south")
    area.exit(hg_plaza_north, hg_north_road, "north")

    ashwatch_tower_ruins = area.room(
        "ashwatch_tower_ruins",
        name="Ashwatch Tower Ruins",
        desc=(
            "The crumbling base of a tower far older than Vael's Crossing "
            "itself. Blackened stone rises two stories before ending in a "
            "jagged break where the upper floors collapsed long ago. Faded "
            "ward-glyphs are carved into the foundation stones, their edges "
            "still faintly warm to the touch. The air hums with residual "
            "node-wrought heat -- whatever protections were laid here are "
            "failing."
        ),
        room_type="ruins",
    )
    area.exit(hg_south_road, ashwatch_tower_ruins, "west")
    area.exit(ashwatch_tower_ruins, hg_south_road, "east")

    # Harbor Gate NPCs

    # 1. Greeter NPC (D-11 onboarding)
    area.npc(
        hg_arrival,
        "npc_greeter_maren",
        faction="empire",
        dialogue={
            "greeting_tiers": {
                "neutral": (
                    "Maren squares her ledger against one hip and gives you a "
                    "practiced once-over. 'First time through Vael's Crossing? "
                    "Keep the harbor at your back and you'll find food, work, "
                    "and trouble in that order.'"
                ),
                "friendly": (
                    "Maren lifts two fingers in a small salute. 'Back again? "
                    "Good. The city makes more sense once you know which doors "
                    "lead to work and which only lead to speeches.'"
                ),
            },
            "topics": {
                "work": {
                    "default": (
                        "'If you want honest coin, start with the tavern, the "
                        "trading house, or the Warden office. Marta hears half "
                        "the city's small troubles, Broker Carston pays for eyes "
                        "that notice details, and Agent Calloway needs people "
                        "who can carry a sealed report without losing it.'"
                    ),
                },
                "guilds": {
                    "default": (
                        "'The guild halls are open to visitors, not promises. "
                        "You earn a place there by proving what you can do, not "
                        "by walking in fresh off the road. Learn the city, take "
                        "some work, and let people remember your name for the "
                        "right reasons.'"
                    ),
                },
                "rumors": {
                    "default": (
                        "'River traffic is jumpier than it should be, Warden "
                        "riders have been coming and going at odd hours, and the "
                        "market keeps whispering about cargo that vanishes on "
                        "paper before it ever vanishes in the street. That's "
                        "enough rumor for one arrival.'"
                    ),
                },
            },
            "base_hints": ["work", "guilds", "rumors"],
        },
    )

    # 2. Gate guard captain
    area.npc(hg_gatehouse, "npc_gate_captain_voss", faction="empire")

    # 3. Customs clerk
    area.npc(hg_customs_office, "npc_customs_clerk_pellam", faction="empire")

    # 4. Stable hand
    area.npc(hg_stable, "npc_stablehand_korua", faction="kauroran", trainer_id="npc_stablehand_korua")

    # 5. Wheelwright
    area.npc(hg_wagon_yard, "npc_wheelwright_tomas", faction=None)

    # ==================================================================
    #  DISTRICT 2: MARKET DISTRICT (~20 rooms)
    #  Vendors, smithing forge, bustling trade atmosphere.
    # ==================================================================

    mk_square = area.room(
        "mk_square",
        name="Market Square",
        desc=(
            "The heart of Vael's Crossing commerce. Stalls crowd the "
            "square in haphazard rows, their canopies patched and "
            "re-patched in every color. Voices compete -- hawkers "
            "shouting prices, buyers haggling, a Veth merchant singing "
            "the virtues of his wares in a high, carrying voice. The "
            "cobblestones are stained with spilled dye, crushed fruit, "
            "and things best not examined closely."
        ),
        room_type="path",
        indoor=False,
        ambient_echoes=[
            "A merchant shouts: 'Fresh iron! Straight from the Reth mines!'",
            "Two buyers argue over the price of a bolt of cloth.",
            "A pickpocket bumps into someone and vanishes into the crowd.",
            "The smell of grilled meat from a nearby stall makes your stomach growl.",
            "A Selvar merchant flashes a grin at a passing guard who pretends not to see her.",
        ],
    )

    mk_weapon_shop = area.room(
        "mk_weapon_shop",
        name="Ironhand Arms",
        desc=(
            "A weapon shop occupying the ground floor of a sturdy stone "
            "building. Swords, axes, maces, and daggers hang from wall "
            "racks in ordered rows. A practice dummy in the corner shows "
            "the marks of many test swings. The proprietor -- a broad "
            "woman with scarred forearms -- watches browsers with the "
            "flat attention of someone who has caught too many shoplifters."
        ),
        room_type="building",
        indoor=True,
    )

    mk_armor_shop = area.room(
        "mk_armor_shop",
        name="Thornguard Outfitters",
        desc=(
            "Leather and plate hang from wooden mannequins arranged like "
            "a silent army. The shop smells of tanning oil and brass "
            "polish. Helmets line a shelf above the counter. Shields "
            "lean against every wall. A sign reads: 'ALL SALES FINAL. "
            "YOUR HEAD, YOUR PROBLEM.'"
        ),
        room_type="building",
        indoor=True,
    )

    mk_potion_shop = area.room(
        "mk_potion_shop",
        name="Vael's Remedies",
        desc=(
            "Glass bottles of every size and color crowd the shelves "
            "of this small apothecary. The air is thick with the smell "
            "of herbs, alcohol, and something vaguely sulfurous. Labels "
            "in cramped handwriting identify each preparation. A mortar "
            "and pestle sits on the counter, stained deep green."
        ),
        room_type="building",
        indoor=True,
    )

    mk_general_store = area.room(
        "mk_general_store",
        name="Crossroads General Goods",
        desc=(
            "If Vael's Crossing needs it, this shop probably has it -- "
            "buried somewhere in the towering stacks of crates, barrels, "
            "and burlap sacks that fill every available surface. Rope, "
            "lanterns, bedrolls, tinderboxes, and a hundred other "
            "necessities compete for shelf space. The proprietor navigates "
            "the chaos with practiced ease."
        ),
        room_type="building",
        indoor=True,
    )

    mk_forge = area.room(
        "mk_forge",
        name="The Anvil - City Forge",
        desc=(
            "Heat rolls from the open doorway of the city forge. Inside, "
            "a massive stone hearth holds a coal fire that never fully "
            "dies. Anvils of various sizes sit on scarred wooden blocks. "
            "The smith -- a heavyset man glistening with sweat -- works "
            "a piece of iron with rhythmic, practiced blows. Sparks "
            "scatter across the flagstone floor."
        ),
        room_type="building",
        indoor=True,
        crafting_stations=["forge"],
        ambient_echoes=[
            "The ring of hammer on anvil echoes through the forge.",
            "Sparks shower from hot iron as the smith works.",
            "The forge fire roars as bellows pump air into the coals.",
        ],
    )

    mk_food_stalls = area.room(
        "mk_food_stalls",
        name="Market Square - Food Row",
        desc=(
            "A line of food stalls runs along the eastern edge of the "
            "market. Grilled meat on skewers, flatbread with drippings, "
            "boiled roots, and dubious pastries are on offer. A Kau'roran "
            "woman serves enormous portions from a pot that seems "
            "bottomless. The line at her stall is always the longest."
        ),
        room_type="path",
        indoor=False,
        ambient_echoes=[
            "The sizzle of meat hitting a hot grill fills the air.",
            "A vendor shouts: 'Three for a scale! Can't beat that!'",
        ],
    )

    mk_cloth_row = area.room(
        "mk_cloth_row",
        name="Market Square - Cloth Row",
        desc=(
            "Bolts of fabric hang from poles and drape over stall frames "
            "like flags of a dozen nations. Linen, wool, imported silk "
            "from the western continent, and rough canvas for workwear. "
            "A tailor works at a portable table, hemming a cloak while "
            "its owner shifts impatiently from foot to foot."
        ),
        room_type="path",
        indoor=False,
    )

    mk_north_lane = area.room(
        "mk_north_lane",
        name="Trader's Lane - North",
        desc=(
            "A busy lane connecting the Market Square to the Guild "
            "Quarter. Shops and stalls thin out here, replaced by the "
            "workshops of craftspeople. A leatherworker cuts patterns "
            "in the doorway of her shop. The sound of the market fades "
            "to a background murmur."
        ),
        room_type="path",
        indoor=False,
    )

    mk_south_lane = area.room(
        "mk_south_lane",
        name="Trader's Lane - South",
        desc=(
            "The southern stretch of Trader's Lane runs toward the "
            "Consortium Quarter. Merchant houses line both sides -- "
            "their stone facades nicer than the rest of the district, "
            "their doors heavier, their windows smaller. Money lives "
            "here but doesn't like to be seen."
        ),
        room_type="path",
        indoor=False,
    )

    mk_jeweler = area.room(
        "mk_jeweler",
        name="Seld's Fine Trinkets",
        desc=(
            "A tiny shop with iron bars on the windows and a reinforced "
            "door. Inside, glass cases display rings, amulets, bracelets, "
            "and brooches of varying quality. A Veth proprietor perches "
            "on a high stool behind the counter, a jeweler's loupe "
            "permanently affixed to one eye. He appraises you as quickly "
            "as he would a gemstone."
        ),
        room_type="building",
        indoor=True,
    )

    mk_tanner = area.room(
        "mk_tanner",
        name="Blackhide Tannery",
        desc=(
            "The tannery sits downwind of the market for obvious reasons. "
            "Hides stretch on frames in the yard while chemical baths "
            "cure leather in stone vats. The smell is extraordinary and "
            "unpleasant. Workers move through the space with rags tied "
            "over their noses."
        ),
        room_type="building",
        indoor=False,
    )

    mk_auction_corner = area.room(
        "mk_auction_corner",
        name="Auction Corner",
        desc=(
            "A raised wooden platform in the corner of the market where "
            "a fast-talking auctioneer runs sales every afternoon. Today "
            "the platform sits empty, but chalk marks on the boards "
            "record recent winning bids. A notice promises a rare "
            "mineral shipment from The Reth at tomorrow's sale."
        ),
        room_type="path",
        indoor=False,
    )

    mk_back_alley = area.room(
        "mk_back_alley",
        name="Market Back Alley",
        desc=(
            "A narrow passage behind the market stalls where deliveries "
            "are made and garbage accumulates. Crates are stacked high "
            "against the walls. A door in the back of the Ironhand Arms "
            "shop is propped open for ventilation. Rats scuttle between "
            "the refuse piles."
        ),
        room_type="path",
        indoor=False,
    )

    mk_tea_house = area.room(
        "mk_tea_house",
        name="The Bitter Cup",
        desc=(
            "A small tea house wedged between larger buildings. Low "
            "tables and cushions replace the chairs found in most "
            "establishments. A Selvar woman with a winter coat the color "
            "of fresh snow serves dark, bitter tea with unexpected "
            "grace. The clientele is quiet -- merchants resting between "
            "deals, travelers gathering their thoughts."
        ),
        room_type="building",
        indoor=True,
    )

    mk_chandler = area.room(
        "mk_chandler",
        name="Wickman's Chandlery",
        desc=(
            "Candles, lanterns, oil flasks, and torches fill this shop "
            "with a warm glow and the smell of beeswax. Wicks hang "
            "drying from the ceiling like pale vines. The chandler is "
            "an old human man who speaks mostly in grunts and points."
        ),
        room_type="building",
        indoor=True,
    )

    mk_scribe = area.room(
        "mk_scribe",
        name="Pellam's Letters & Seals",
        desc=(
            "A scribe's office where documents are drafted, copied, and "
            "sealed for a fee. Ink stains cover the desk, the floor, and "
            "the scribe's hands. Wax seals of various factions and "
            "merchant houses hang on display pegs. The scribe charges "
            "by the word and counts every one."
        ),
        room_type="building",
        indoor=True,
    )

    mk_well = area.room(
        "mk_well",
        name="Market Well",
        desc=(
            "A stone well at the intersection of two market lanes. A "
            "bucket on a rope sits on the rim, water sloshing. Locals "
            "gather here to fill jugs, gossip, and watch the crowd. "
            "The well is said to be old -- older than the city -- but "
            "nobody knows who dug it. The water tastes of iron."
        ),
        room_type="path",
        indoor=False,
    )

    mk_spice_stall = area.room(
        "mk_spice_stall",
        name="Market Square - Spice Merchants",
        desc=(
            "Barrels and baskets of dried spices, herbs, and salt line "
            "the front of a colorful stall. The air burns with the "
            "intensity of ground pepper and dried chili. A dark-skinned "
            "human woman weighs portions on a hand-held scale, her "
            "fingers stained orange with turmeric."
        ),
        room_type="path",
        indoor=False,
    )

    # Market District exits
    area.exit(mk_square, hg_plaza_north, "south")
    area.exit(hg_plaza_north, mk_square, "north")
    area.exit(mk_square, mk_weapon_shop, "east")
    area.exit(mk_weapon_shop, mk_square, "west")
    area.exit(mk_square, mk_armor_shop, "northeast")
    area.exit(mk_armor_shop, mk_square, "southwest")
    area.exit(mk_square, mk_potion_shop, "northwest")
    area.exit(mk_potion_shop, mk_square, "southeast")
    area.exit(mk_square, mk_general_store, "west")
    area.exit(mk_general_store, mk_square, "east")
    area.exit(mk_square, mk_food_stalls, "north")
    area.exit(mk_food_stalls, mk_square, "south")
    area.exit(mk_food_stalls, mk_cloth_row, "east")
    area.exit(mk_cloth_row, mk_food_stalls, "west")
    area.exit(mk_square, mk_north_lane, "north")
    area.exit(mk_north_lane, mk_square, "south")
    area.exit(mk_square, mk_south_lane, "south")
    area.exit(mk_south_lane, mk_square, "north")
    area.exit(mk_weapon_shop, mk_forge, "east")
    area.exit(mk_forge, mk_weapon_shop, "west")
    area.exit(mk_square, mk_jeweler, "southeast")
    area.exit(mk_jeweler, mk_square, "northwest")
    area.exit(mk_forge, mk_tanner, "north")
    area.exit(mk_tanner, mk_forge, "south")
    area.exit(mk_cloth_row, mk_auction_corner, "north")
    area.exit(mk_auction_corner, mk_cloth_row, "south")
    area.exit(mk_armor_shop, mk_back_alley, "east")
    area.exit(mk_back_alley, mk_armor_shop, "west")
    area.exit(mk_food_stalls, mk_tea_house, "northeast")
    area.exit(mk_tea_house, mk_food_stalls, "southwest")
    area.exit(mk_general_store, mk_chandler, "north")
    area.exit(mk_chandler, mk_general_store, "south")
    area.exit(mk_scribe, mk_south_lane, "east")
    area.exit(mk_south_lane, mk_scribe, "west")
    area.exit(mk_square, mk_well, "west")
    area.exit(mk_well, mk_square, "east")
    area.exit(mk_well, mk_spice_stall, "north")
    area.exit(mk_spice_stall, mk_well, "south")

    # Market District NPCs

    # 6. Weapon vendor
    _brenna = area.npc(mk_weapon_shop, "npc_weaponsmith_brenna", faction=None)
    _brenna.db.is_vendor = True
    _brenna.db.vendor_accepts = ["equipment"]
    _brenna.db.vendor_faction = None
    _brenna.db.player_stock = {}

    # 7. Armor vendor
    _derik = area.npc(mk_armor_shop, "npc_armorsmith_derik", faction=None)
    _derik.db.is_vendor = True
    _derik.db.vendor_accepts = ["equipment"]
    _derik.db.vendor_faction = None
    _derik.db.player_stock = {}

    # 8. Potion vendor
    _ystra = area.npc(mk_potion_shop, "npc_apothecary_ystra", faction=None)
    _ystra.db.is_vendor = True
    _ystra.db.vendor_accepts = ["consumable", "ingredient"]
    _ystra.db.vendor_faction = None
    _ystra.db.player_stock = {}

    # 9. General goods vendor
    _haldric = area.npc(mk_general_store, "npc_shopkeep_haldric", faction=None)
    _haldric.db.is_vendor = True
    _haldric.db.vendor_accepts = ["item", "material"]
    _haldric.db.vendor_faction = None
    _haldric.db.player_stock = {}

    # 10. Smith (forge master)
    area.npc(mk_forge, "npc_smith_goram", faction=None)

    # 11. Jeweler
    area.npc(mk_jeweler, "npc_jeweler_seld", faction=None)

    # 12. Food stall vendor
    area.npc(mk_food_stalls, "npc_cook_malani", faction=None)

    # 13. Tea house owner
    area.npc(mk_tea_house, "npc_tea_owner_silka", faction=None)

    # 14. Auctioneer
    area.npc(mk_auction_corner, "npc_auctioneer_bale", faction="consortium")

    # 15. Spice merchant
    area.npc(mk_spice_stall, "npc_spice_merchant_zara", faction=None)

    # 16b. Tanner vendor
    _tanner = area.npc(mk_tanner, "npc_tanner_blackhide", faction=None)
    _tanner.db.is_vendor = True
    _tanner.db.vendor_accepts = ["hide"]
    _tanner.db.vendor_faction = None
    _tanner.db.player_stock = {}

    # ==================================================================
    #  DISTRICT 3: GUILD QUARTER (~20 rooms)
    #  All 10 guild halls, training yard, arcane library.
    # ==================================================================

    gq_entrance = area.room(
        "gq_entrance",
        name="Guild Quarter - Main Avenue",
        desc=(
            "A wide stone avenue flanked by guild hall entrances, each "
            "marked with its domain's emblem carved into the lintel. "
            "The avenue is quieter than the market -- purposeful rather "
            "than chaotic. Apprentices hurry between halls carrying "
            "bundles and scrolls. The air smells of chalk dust and "
            "old parchment."
        ),
        room_type="path",
        indoor=False,
    )

    gq_combat_hall = area.room(
        "gq_combat_hall",
        name="Steelward Hall - Combat Guild",
        desc=(
            "The Combat Guild hall is a functional space of scarred wood "
            "and stone. Weapon racks line the walls. A sand-covered "
            "sparring ring dominates the center. Battle standards hang "
            "from the rafters -- each one commemorating a guild member "
            "who distinguished themselves in service. The guild master's "
            "office is behind a heavy oak door at the back."
        ),
        room_type="building",
        indoor=True,
    )

    gq_subterfuge_den = area.room(
        "gq_subterfuge_den",
        name="The Blind Eye - Subterfuge Guild",
        desc=(
            "There is no sign above this door. The entrance is an "
            "unmarked archway between two larger buildings. Inside, "
            "the space is dim, intimate, and smells of candle wax and "
            "damp stone. Alcoves with heavy curtains provide private "
            "meeting spaces. A woman behind a narrow desk nods once "
            "and waits for you to state your business."
        ),
        room_type="building",
        indoor=True,
    )

    gq_naturalism_hall = area.room(
        "gq_naturalism_hall",
        name="The Green Bower - Naturalism Guild",
        desc=(
            "This hall is half building, half garden. Vines climb the "
            "interior walls. Potted plants sit on every surface. A "
            "skylight lets in natural light. The air is thick with the "
            "smell of earth and growing things -- a strange contrast "
            "to the dusty city outside. A druid in worn leather tends "
            "a planter of unfamiliar herbs."
        ),
        room_type="building",
        indoor=True,
    )

    gq_resonance_hall = area.room(
        "gq_resonance_hall",
        name="The Tuning Chamber - Resonance Guild",
        desc=(
            "The Resonance Guild occupies a building with unusually thick "
            "walls. Inside, the acoustics are strange -- voices carry "
            "in unexpected directions. Crystal formations sit in wall "
            "niches, some faintly humming at frequencies just below "
            "hearing. A scholar studies a node fragment under a magnifying "
            "apparatus, muttering about harmonics."
        ),
        room_type="building",
        indoor=True,
    )

    gq_arcana_hall = area.room(
        "gq_arcana_hall",
        name="The Crucible - Arcana Guild",
        desc=(
            "Bookshelves reach the ceiling. Arcane diagrams cover a "
            "slate board on the far wall. The smell of ink, old paper, "
            "and something faintly metallic pervades the space. Glyphs "
            "are carved into the door frame -- purely decorative, the "
            "guild master insists, though they seem to shift when viewed "
            "from the corner of your eye."
        ),
        room_type="building",
        indoor=True,
    )

    gq_diplomacy_hall = area.room(
        "gq_diplomacy_hall",
        name="The Open Hand - Diplomacy Guild",
        desc=(
            "An airy hall with a large round table at its center, "
            "designed so no seat holds precedence. Maps of Varath and "
            "the known world cover the walls. Faction banners hang "
            "from the ceiling -- every major faction represented, "
            "including some whose relations with the Empire are "
            "decidedly frosty. The guild master believes in talking "
            "to everyone."
        ),
        room_type="building",
        indoor=True,
    )

    gq_alchemy_lab = area.room(
        "gq_alchemy_lab",
        name="The Retort - Alchemy Guild",
        desc=(
            "Glass apparatus covers every workbench -- tubes, flasks, "
            "condensers, and devices whose purpose is unclear. Colored "
            "liquids bubble in beakers over low flames. A ventilation "
            "shaft in the ceiling draws away fumes that would otherwise "
            "be lethal. The alchemist in charge has stained fingers "
            "and slightly unfocused eyes."
        ),
        room_type="building",
        indoor=True,
    )

    gq_tactics_hall = area.room(
        "gq_tactics_hall",
        name="The War Table - Tactics Guild",
        desc=(
            "Sand tables and tactical maps dominate this hall. Miniature "
            "figurines representing troops, siege engines, and terrain "
            "features are arranged in various scenarios. A retired "
            "Imperial officer runs the guild with military precision. "
            "Chairs are arranged in rows facing a lectern -- this is "
            "a classroom as much as a guild hall."
        ),
        room_type="building",
        indoor=True,
    )

    gq_engineering_hall = area.room(
        "gq_engineering_hall",
        name="The Gearworks - Engineering Guild",
        desc=(
            "Mechanical devices in various states of assembly clutter "
            "the workbenches. Gears, springs, cables, and structural "
            "members hang from hooks on the ceiling. A Gnome engineer "
            "stands on a stepladder, tightening something that clicks "
            "and whirs. Blueprints are pinned to every vertical surface. "
            "The guild smells of machine oil and copper."
        ),
        room_type="building",
        indoor=True,
        crafting_stations=["workbench"],
    )

    gq_remnance_hall = area.room(
        "gq_remnance_hall",
        name="The Old Echo Archive",
        desc=(
            "The oldest building in the Quarter keeps its public face "
            "quiet: dark foundation stones, narrow windows, and display "
            "cases full of pre-Imperial artifacts nobody has managed to "
            "catalog with confidence. Archivists speak softly here, as if "
            "the past is easier to handle when no one shouts claims over it."
        ),
        room_type="building",
        indoor=True,
    )

    gq_training_yard = area.room(
        "gq_training_yard",
        name="Guild Quarter - Training Yard",
        desc=(
            "An open practice yard shared by the guild halls. Target "
            "dummies, archery butts, and sparring circles are laid out "
            "across packed earth. Apprentices from different guilds "
            "train side by side -- a Combat student drilling forms "
            "next to a Naturalism student sketching plants. The yard "
            "is the one place where guild rivalries dissolve into "
            "shared effort."
        ),
        room_type="path",
        indoor=False,
        ambient_echoes=[
            "The crack of a practice sword on a training dummy echoes across the yard.",
            "An apprentice curses as she fumbles a technique for the third time.",
            "A Tactics student calls out corrections to a sparring pair.",
        ],
    )

    gq_library = area.room(
        "gq_library",
        name="Guild Quarter - Shared Library",
        desc=(
            "A two-story library shared by all ten guilds. Shelves "
            "reach to the ceiling on both floors, connected by narrow "
            "spiral staircases. Reading desks with oil lamps sit in "
            "alcoves along the walls. The library is run by a fiercely "
            "protective Veth librarian who treats every book as a "
            "personal friend."
        ),
        room_type="building",
        indoor=True,
    )

    gq_courtyard = area.room(
        "gq_courtyard",
        name="Guild Quarter - Inner Courtyard",
        desc=(
            "A quiet courtyard at the center of the Guild Quarter. A "
            "single, ancient tree grows here -- its species unknown, "
            "its bark marked with the same unfamiliar symbols found on "
            "the Ashwatch Tower. Benches circle the tree. Guild masters "
            "sometimes meet here when formal council chambers feel "
            "too confining."
        ),
        room_type="path",
        indoor=False,
    )

    gq_north_passage = area.room(
        "gq_north_passage",
        name="Guild Quarter - North Passage",
        desc=(
            "A covered passage connecting the Guild Quarter to the "
            "Imperial Quarter. The architecture changes visibly here -- "
            "the practical stone of the guilds giving way to the "
            "deliberately imposing style of Imperial construction. "
            "Guards are posted at the far end."
        ),
        room_type="path",
        indoor=False,
    )

    # Guild Quarter exits
    area.exit(gq_entrance, mk_north_lane, "south")
    area.exit(mk_north_lane, gq_entrance, "north")
    area.exit(gq_entrance, gq_combat_hall, "east")
    area.exit(gq_combat_hall, gq_entrance, "west")
    area.exit(gq_entrance, gq_subterfuge_den, "west")
    area.exit(gq_subterfuge_den, gq_entrance, "east")
    area.exit(gq_entrance, gq_courtyard, "north")
    area.exit(gq_courtyard, gq_entrance, "south")
    area.exit(gq_courtyard, gq_naturalism_hall, "east")
    area.exit(gq_naturalism_hall, gq_courtyard, "west")
    area.exit(gq_courtyard, gq_resonance_hall, "west")
    area.exit(gq_resonance_hall, gq_courtyard, "east")
    area.exit(gq_courtyard, gq_arcana_hall, "northeast")
    area.exit(gq_arcana_hall, gq_courtyard, "southwest")
    area.exit(gq_courtyard, gq_diplomacy_hall, "northwest")
    area.exit(gq_diplomacy_hall, gq_courtyard, "southeast")
    area.exit(gq_courtyard, gq_alchemy_lab, "north")
    area.exit(gq_alchemy_lab, gq_courtyard, "south")
    area.exit(gq_combat_hall, gq_tactics_hall, "north")
    area.exit(gq_tactics_hall, gq_combat_hall, "south")
    area.exit(gq_subterfuge_den, gq_engineering_hall, "north")
    area.exit(gq_engineering_hall, gq_subterfuge_den, "south")
    area.exit(gq_alchemy_lab, gq_remnance_hall, "east")
    area.exit(gq_remnance_hall, gq_alchemy_lab, "west")
    area.exit(gq_combat_hall, gq_training_yard, "east")
    area.exit(gq_training_yard, gq_combat_hall, "west")
    area.exit(gq_entrance, gq_library, "southeast")
    area.exit(gq_library, gq_entrance, "northwest")
    area.exit(gq_courtyard, gq_north_passage, "north")
    area.exit(gq_north_passage, gq_courtyard, "south")

    # Guild Quarter NPCs

    # 16. Combat guild master
    area.npc(gq_combat_hall, "npc_guildmaster_combat_haren", faction="empire")

    # 17. Subterfuge guild master
    area.npc(gq_subterfuge_den, "npc_guildmaster_subterfuge_dessa", faction=None, trainer_id="npc_guildmaster_subterfuge_dessa")

    # 18. Naturalism guild master
    area.npc(gq_naturalism_hall, "npc_guildmaster_naturalism_elwen", faction="wardens", trainer_id="npc_guildmaster_naturalism_elwen")

    # 19. Resonance guild master
    area.npc(gq_resonance_hall, "npc_guildmaster_resonance_kael", faction=None, trainer_id="npc_guildmaster_resonance_kael")

    # 20. Arcana guild master
    area.npc(gq_arcana_hall, "npc_guildmaster_arcana_thessa", faction=None)

    # 21. Diplomacy guild master
    area.npc(gq_diplomacy_hall, "npc_guildmaster_diplomacy_aldric", faction="empire", trainer_id="npc_guildmaster_diplomacy_aldric")

    # 22. Alchemy guild master
    area.npc(gq_alchemy_lab, "npc_guildmaster_alchemy_mirelle", faction=None, trainer_id="npc_guildmaster_alchemy_mirelle")

    # 23. Tactics guild master
    area.npc(gq_tactics_hall, "npc_guildmaster_tactics_brennus", faction="empire", trainer_id="npc_guildmaster_tactics_brennus")

    # 24. Engineering guild master
    area.npc(gq_engineering_hall, "npc_guildmaster_engineering_pren", faction="consortium", trainer_id="npc_guildmaster_engineering_pren")

    # 25. Old archive keeper
    area.npc(gq_remnance_hall, "npc_guildmaster_remnance_morwen", name="Archivist Morwen", faction=None)

    # 26. Librarian
    area.npc(gq_library, "npc_librarian_whisp", faction=None)

    # 27. Training instructor
    area.npc(gq_training_yard, "npc_trainer_combat_sergeant_vale", faction="empire", trainer_id="npc_trainer_combat_sergeant_vale")

    # ==================================================================
    #  DISTRICT 4: CONSORTIUM QUARTER (~15 rooms)
    #  Bank branch, trading houses, merchant residences.
    # ==================================================================

    cq_entrance = area.room(
        "cq_entrance",
        name="Consortium Quarter - Main Gate",
        desc=(
            "Iron gates stand permanently open but pointedly present. "
            "The cobblestones here are cleaner, the buildings better "
            "maintained. Consortium guards -- Gnomes in polished leather "
            "and brass-buttoned coats -- patrol the entrance. A sign "
            "reads: 'Consortium Quarter. All visitors welcome. "
            "All debts remembered.'"
        ),
        room_type="building",
        indoor=False,
    )

    cq_bank = area.room(
        "cq_bank",
        name="Consortium Bank - Vael's Crossing Branch",
        desc=(
            "The bank is the most imposing building in the quarter -- "
            "marble columns framing a brass-fitted door. Inside, "
            "counting tables sit behind iron grilles. The vault door "
            "is visible at the back of the hall, its surface engraved "
            "with the Consortium's merchant seal. The silence here is "
            "deliberate and enforced. A sign warns: 'SILENCE. YOUR "
            "MONEY DESERVES RESPECT.'"
        ),
        room_type="building",
        indoor=True,
    )

    cq_trading_house = area.room(
        "cq_trading_house",
        name="Vael's Trading House",
        desc=(
            "A large building where bulk goods change hands. Sample "
            "crates sit on display tables -- ore, timber, grain, cloth. "
            "Consortium agents negotiate prices with a ruthless "
            "politeness that leaves sellers feeling robbed and grateful "
            "simultaneously. A chalkboard lists today's commodity prices."
        ),
        room_type="building",
        indoor=True,
    )

    cq_exchange = area.room(
        "cq_exchange",
        name="Currency Exchange",
        desc=(
            "A small office where foreign currencies are exchanged for "
            "Imperial Scales at rates that favor the Consortium. An "
            "abacus clicks rhythmically as the clerk calculates "
            "conversion fees. A chart on the wall lists exchange rates "
            "for currencies from both continents and the archipelago."
        ),
        room_type="building",
        indoor=True,
    )

    cq_merchant_row = area.room(
        "cq_merchant_row",
        name="Merchant Row",
        desc=(
            "A row of merchant residences -- larger and sturdier than "
            "homes in the residential district. Each has a workshop or "
            "office on the ground floor and living quarters above. "
            "Brass nameplates identify the residents: importers, "
            "exporters, factors, and agents of distant trading houses."
        ),
        room_type="path",
        indoor=False,
    )

    cq_warehouse = area.room(
        "cq_warehouse",
        name="Consortium Warehouse",
        desc=(
            "A massive stone warehouse where goods are stored between "
            "transactions. Crates are stacked to the ceiling, each "
            "marked with Consortium shipping codes. A foreman with a "
            "clipboard directs workers with brusque efficiency. The "
            "smell of sawdust and packing straw fills the air."
        ),
        room_type="building",
        indoor=True,
    )

    cq_gnome_club = area.room(
        "cq_gnome_club",
        name="The Cogwheel Club",
        desc=(
            "A private social club for Consortium members and associates. "
            "The furnishings are surprisingly comfortable -- cushioned "
            "chairs, warm lighting, a small bar serving imported spirits. "
            "Gnome-sized furniture is mixed with standard pieces. "
            "Business is discussed here over drinks, away from the "
            "formality of the trading house."
        ),
        room_type="building",
        indoor=True,
    )

    cq_records_office = area.room(
        "cq_records_office",
        name="Consortium Records Office",
        desc=(
            "Filing cabinets fill this room from floor to ceiling. Every "
            "transaction in Vael's Crossing involving Consortium trade "
            "is recorded here in triplicate. A clerk with ink-stained "
            "fingers manages the archive with obsessive precision."
        ),
        room_type="building",
        indoor=True,
    )

    cq_courtyard = area.room(
        "cq_courtyard",
        name="Consortium Quarter - Courtyard",
        desc=(
            "A tidy courtyard with a working fountain -- one of the few "
            "in the city that still runs. Consortium employees take "
            "their meals here on benches arranged around the fountain. "
            "The water is clean and tastes faintly of minerals."
        ),
        room_type="path",
        indoor=False,
    )

    cq_golem_shed = area.room(
        "cq_golem_shed",
        name="Golem Maintenance Shed",
        desc=(
            "A large shed where Consortium golems are serviced and "
            "repaired. A golem stands motionless in the center -- its "
            "chest plate open, gears exposed. A Gnome mechanic works "
            "inside the cavity, humming tunelessly. Tools of unfamiliar "
            "design hang from wall hooks."
        ),
        room_type="building",
        indoor=True,
        ambient_echoes=[
            "Metal clicks and whirs from inside the golem's chest cavity.",
            "The mechanic mutters something about 'base-eight calibration.'",
        ],
    )

    cq_guild_liaison = area.room(
        "cq_guild_liaison",
        name="Faction Liaison Office - Consortium",
        desc=(
            "An office where Consortium representatives handle faction "
            "business. Contracts, trade agreements, and diplomatic "
            "correspondence are managed here. The Consortium liaison "
            "is a Gnome of impeccable dress and ruthless pragmatism."
        ),
        room_type="building",
        indoor=True,
    )

    cq_south_passage = area.room(
        "cq_south_passage",
        name="Consortium Quarter - South Passage",
        desc=(
            "A passage connecting the Consortium Quarter to the "
            "southern part of the city. The clean cobblestones of the "
            "quarter give way to rougher ground. A Consortium guard "
            "watches the passage from a sentry box."
        ),
        room_type="path",
        indoor=False,
    )

    cq_import_dock = area.room(
        "cq_import_dock",
        name="Import Receiving Dock",
        desc=(
            "A loading area where wagon shipments are received and "
            "catalogued. Gnome inspectors check each delivery against "
            "manifests. Rejected goods are piled in a 'returns' area "
            "that nobody ever seems to collect from."
        ),
        room_type="building",
        indoor=False,
    )

    cq_private_garden = area.room(
        "cq_private_garden",
        name="Merchant's Private Garden",
        desc=(
            "A small walled garden behind one of the larger merchant "
            "residences. Ornamental plants from the western continent "
            "grow in raised beds. A bench sits under a trellis heavy "
            "with flowering vines. It is quiet here -- deliberately so."
        ),
        room_type="path",
        indoor=False,
    )

    # Consortium Quarter exits
    area.exit(cq_entrance, mk_south_lane, "south")
    area.exit(mk_south_lane, cq_entrance, "north")
    area.exit(cq_entrance, cq_bank, "north")
    area.exit(cq_bank, cq_entrance, "south")
    area.exit(cq_entrance, cq_trading_house, "east")
    area.exit(cq_trading_house, cq_entrance, "west")
    area.exit(cq_bank, cq_exchange, "east")
    area.exit(cq_exchange, cq_bank, "west")
    area.exit(cq_entrance, cq_merchant_row, "west")
    area.exit(cq_merchant_row, cq_entrance, "east")
    area.exit(cq_trading_house, cq_warehouse, "north")
    area.exit(cq_warehouse, cq_trading_house, "south")
    area.exit(cq_merchant_row, cq_gnome_club, "north")
    area.exit(cq_gnome_club, cq_merchant_row, "south")
    area.exit(cq_bank, cq_records_office, "west")
    area.exit(cq_records_office, cq_bank, "east")
    area.exit(cq_entrance, cq_courtyard, "northeast")
    area.exit(cq_courtyard, cq_entrance, "southwest")
    area.exit(cq_courtyard, cq_golem_shed, "east")
    area.exit(cq_golem_shed, cq_courtyard, "west")
    area.exit(cq_courtyard, cq_guild_liaison, "north")
    area.exit(cq_guild_liaison, cq_courtyard, "south")
    area.exit(cq_entrance, cq_south_passage, "southeast")
    area.exit(cq_south_passage, cq_entrance, "northwest")
    area.exit(cq_warehouse, cq_import_dock, "east")
    area.exit(cq_import_dock, cq_warehouse, "west")
    area.exit(cq_merchant_row, cq_private_garden, "west")
    area.exit(cq_private_garden, cq_merchant_row, "east")

    vc_warehouse_district = area.room(
        "vc_warehouse_district",
        name="Warehouse Loading Bay",
        desc=(
            "A cavernous loading bay behind the main warehouse, open to the "
            "sky on one side where cargo wagons back in for unloading. Crates "
            "are stacked high along the walls, many bearing Consortium seals. "
            "One section has been roped off -- recently disturbed crates, a "
            "broken seal, and fresh boot prints in the dust suggest someone "
            "has been here who shouldn't have been."
        ),
        room_type="building",
    )
    area.exit(cq_warehouse, vc_warehouse_district, "south")
    area.exit(vc_warehouse_district, cq_warehouse, "north")

    # Consortium Quarter NPCs

    # 28. Bank teller
    area.npc(cq_bank, "npc_bank_teller_fenwick", faction="consortium")

    # 29. Bank manager
    area.npc(cq_bank, "npc_bank_manager_giselle", faction="consortium")

    # 30. Trading house broker
    area.npc(
        cq_trading_house,
        "npc_broker_carston",
        faction="consortium",
        dialogue={
            "greeting_tiers": {
                "neutral": (
                    "Carston closes a ledger with one finger still marking the "
                    "page. 'If you are here to waste my afternoon, queue behind "
                    "the auditors. If you are here to be useful, say so quickly.'"
                ),
                "friendly": (
                    "Carston's eyes sharpen with recognition. 'Good. Someone "
                    "who can tell the difference between a missing crate and a "
                    "missing story. I can use that.'"
                ),
            },
            "topics": {
                "work": {
                    "default": (
                        "'Most of my work begins when a manifest stops matching "
                        "the dock, the wagon yard, or the men swearing they saw "
                        "nothing. I pay for steady hands, sharp memory, and "
                        "people willing to walk a trail all the way to the end.'"
                    ),
                },
                "trade": {
                    "default": (
                        "'Vael's Crossing survives on movement. Ore from the "
                        "foothills, timber from Cantera, fish and salt from the "
                        "coast, and enough paperwork to choke a horse. Break the "
                        "flow anywhere and everyone in the quarter feels it.'"
                    ),
                },
                "rumors": {
                    "default": (
                        "'Rumor says smugglers are getting bolder. My ledgers say "
                        "someone higher up the line is teaching them where to be "
                        "bold. I trust ledgers more than rumor, but I listen to "
                        "both.'"
                    ),
                },
            },
            "base_hints": ["work", "trade", "rumors"],
        },
    )

    # 31. Consortium liaison
    area.npc(cq_guild_liaison, "npc_liaison_twick", faction="consortium")

    # 32. Golem mechanic
    area.npc(cq_golem_shed, "npc_mechanic_gidgit", faction="consortium")

    # 33. Exchange clerk
    area.npc(cq_exchange, "npc_exchange_clerk_bynn", faction="consortium")

    # ==================================================================
    #  DISTRICT 5: IMPERIAL QUARTER (~15 rooms)
    #  Garrison, barracks, medic building (respawn), courier platform.
    # ==================================================================

    iq_entrance = area.room(
        "iq_entrance",
        name="Imperial Quarter - Garrison Gate",
        desc=(
            "A fortified gate marks the entrance to the Imperial "
            "Quarter. The walls here are taller, the stones newer. "
            "Guards in Imperial uniform stand at attention -- or at "
            "least a close approximation of it. The Imperial standard "
            "flies from a pole above the gate: red field, gold eagle, "
            "crown and sword."
        ),
        room_type="building",
        indoor=False,
    )

    iq_parade_ground = area.room(
        "iq_parade_ground",
        name="Imperial Parade Ground",
        desc=(
            "A large open area where Imperial troops drill and "
            "assemble. The ground is packed earth, flattened by "
            "thousands of marching boots. A flagpole at the center "
            "flies the Imperial standard. Wooden barricades mark out "
            "training lanes. A sergeant bellows at recruits with the "
            "enthusiasm of someone who genuinely enjoys yelling."
        ),
        room_type="path",
        indoor=False,
        ambient_echoes=[
            "A drill sergeant roars: 'LEFT! RIGHT! LEFT! You call that marching?!'",
            "Boots stamp in ragged unison across the parade ground.",
            "An officer mutters something about budget cuts.",
        ],
    )

    iq_barracks = area.room(
        "iq_barracks",
        name="Imperial Barracks",
        desc=(
            "Rows of bunks fill a long, low building. Personal effects "
            "are stored in footlockers chained to bed frames. The "
            "barracks smell of boot polish, sweat, and the vague "
            "sourness of communal living. Off-duty soldiers play cards "
            "on an upturned crate."
        ),
        room_type="building",
        indoor=True,
    )

    iq_officers_quarters = area.room(
        "iq_officers_quarters",
        name="Officers' Quarters",
        desc=(
            "Private rooms for garrison officers. The furnishings are "
            "better than the barracks but not by much -- a desk, a "
            "proper bed, a wardrobe. Maps and duty rosters cover the "
            "wall of the senior officer's room."
        ),
        room_type="building",
        indoor=True,
    )

    iq_armory = area.room(
        "iq_armory",
        name="Imperial Armory",
        desc=(
            "Weapons and armor for the garrison are stored here under "
            "lock and key. A quartermaster manages the inventory with "
            "military precision. Every blade is counted, every "
            "breastplate numbered. Requisition forms are required in "
            "triplicate."
        ),
        room_type="building",
        indoor=True,
    )

    iq_medic_building = area.room(
        "iq_medic_building",
        name="Imperial Medic Station",
        desc=(
            "The medic station is a clean, whitewashed building with "
            "cots arranged along the walls. A surgeon-barber runs the "
            "facility with brisk competence. Bandages, splints, and "
            "herbal poultices are organized on shelves. The air smells "
            "of carbolic and dried mint. This is where the wounded "
            "are brought and where the fallen return to consciousness."
        ),
        room_type="building",
        indoor=True,
    )
    # D-14: Tag medic building as death respawn point
    iq_medic_building.tags.add("respawn_point", category="spawn_point")

    iq_courier_platform = area.room(
        "iq_courier_platform",
        name="The Courier's Roost - Dragon Platform",
        desc=(
            "An elevated stone platform built on the highest point in "
            "the Imperial Quarter. Scorch marks darken the landing "
            "surface where dragon claws have gripped. A Courier Service "
            "agent manages departures from a small booth at the base "
            "of the stairs. The view from the platform edge is "
            "commanding -- the entire city and the plains beyond. "
            "The wind smells of ozone and scale-musk."
        ),
        room_type="building",
        indoor=False,
        ambient_echoes=[
            "A courier dragon launches from the platform with a thunderous beat of wings.",
            "Wind howls across the exposed platform.",
            "The Courier agent checks the next departure schedule.",
        ],
    )

    iq_war_memorial = area.room(
        "iq_war_memorial",
        name="Memorial of the Fallen",
        desc=(
            "A solemn stone monument listing the names of soldiers who "
            "died defending this frontier. The list is long. Fresh "
            "wildflowers sit at the base -- someone tends this memorial "
            "daily. The names are carved in order of death, not rank. "
            "The newest names are at the bottom, the letters still "
            "sharp-edged. It is quiet here in a way that the rest of "
            "the city is not."
        ),
        room_type="building",
        indoor=False,
    )

    iq_command_office = area.room(
        "iq_command_office",
        name="Garrison Commander's Office",
        desc=(
            "A functional office with a large desk, a map of the region "
            "pinned to the wall, and a locked cabinet that presumably "
            "contains sensitive documents. The garrison commander is "
            "rarely here -- she prefers to be on the parade ground or "
            "walking the walls. Her adjutant manages affairs in her "
            "absence."
        ),
        room_type="building",
        indoor=True,
    )

    iq_faction_office = area.room(
        "iq_faction_office",
        name="Imperial Faction Office",
        desc=(
            "The Empire's official presence in Vael's Crossing. An "
            "administrator handles citizen records, land claims, tax "
            "collection, and the endless paperwork of governance. "
            "Imperial law is posted on the wall in small print that "
            "nobody reads. A portrait of the current Emperor hangs "
            "behind the desk."
        ),
        room_type="building",
        indoor=True,
    )

    iq_chapel = area.room(
        "iq_chapel",
        name="Imperial Chapel",
        desc=(
            "A small chapel where soldiers and citizens gather for "
            "contemplation. The faith practiced here is vague and "
            "syncretic -- there are no gods in Soravelon, but the "
            "human need for ritual persists. Candles burn in wall "
            "niches. A meditation bench faces a window that overlooks "
            "the parade ground."
        ),
        room_type="building",
        indoor=True,
    )

    iq_warden_office = area.room(
        "iq_warden_office",
        name="Dragon Warden Outpost",
        desc=(
            "A small, underfunded office tucked into the corner of the "
            "Imperial Quarter. The Dragon Wardens maintain a presence "
            "here despite the Empire's indifference. Posters about "
            "dragon protection and anti-poaching laws cover the walls. "
            "A lone Warden agent works at a cluttered desk, looking "
            "overworked and underslept."
        ),
        room_type="building",
        indoor=True,
    )

    iq_stockade = area.room(
        "iq_stockade",
        name="Imperial Stockade",
        desc=(
            "A row of heavy iron doors mark the garrison's holding "
            "cells. The stockade is small -- Vael's Crossing isn't "
            "large enough for a proper prison. Most offenders are "
            "fined, flogged, or expelled. The cells are for those "
            "awaiting transport to larger Imperial facilities."
        ),
        room_type="building",
        indoor=True,
    )

    iq_wall_walk = area.room(
        "iq_wall_walk",
        name="City Wall - Walkway",
        desc=(
            "A walkway atop the city's northern wall. The view extends "
            "across the foothills toward The Reth. Guards patrol here "
            "in pairs. The wall is old but well-maintained -- the "
            "Empire takes fortification seriously, even on the frontier."
        ),
        room_type="path",
        indoor=False,
    )

    # Imperial Quarter exits
    area.exit(iq_entrance, gq_north_passage, "south")
    area.exit(gq_north_passage, iq_entrance, "north")
    area.exit(iq_entrance, iq_parade_ground, "north")
    area.exit(iq_parade_ground, iq_entrance, "south")
    area.exit(iq_parade_ground, iq_barracks, "east")
    area.exit(iq_barracks, iq_parade_ground, "west")
    area.exit(iq_barracks, iq_officers_quarters, "north")
    area.exit(iq_officers_quarters, iq_barracks, "south")
    area.exit(iq_parade_ground, iq_armory, "west")
    area.exit(iq_armory, iq_parade_ground, "east")
    area.exit(iq_parade_ground, iq_medic_building, "northeast")
    area.exit(iq_medic_building, iq_parade_ground, "southwest")
    area.exit(iq_entrance, iq_courier_platform, "east")
    area.exit(iq_courier_platform, iq_entrance, "west")
    area.exit(iq_parade_ground, iq_war_memorial, "north")
    area.exit(iq_war_memorial, iq_parade_ground, "south")
    area.exit(iq_officers_quarters, iq_command_office, "east")
    area.exit(iq_command_office, iq_officers_quarters, "west")
    area.exit(iq_entrance, iq_faction_office, "west")
    area.exit(iq_faction_office, iq_entrance, "east")
    area.exit(iq_war_memorial, iq_chapel, "east")
    area.exit(iq_chapel, iq_war_memorial, "west")
    area.exit(iq_faction_office, iq_warden_office, "north")
    area.exit(iq_warden_office, iq_faction_office, "south")
    area.exit(iq_barracks, iq_stockade, "south")
    area.exit(iq_stockade, iq_barracks, "north")
    area.exit(iq_war_memorial, iq_wall_walk, "north")
    area.exit(iq_wall_walk, iq_war_memorial, "south")

    # Imperial Quarter NPCs

    # 34. Medic (is_medic flag enables CmdBlessing interaction)
    _medic = area.npc(iq_medic_building, "npc_medic_surgeon_adela", faction="empire")
    _medic.db.is_medic = True

    # 35. Courier agent
    area.npc(
        iq_courier_platform,
        "npc_courier_agent_renn",
        faction="consortium",
        social_profile={
            "social_role": "broker",
            "public_trait": "route-minded courier agent",
            "memory_style": "remembers which names make routes arrive intact",
            "worldview": {
                "admires": ["route", "trade", "reliable", "report"],
                "skeptical_of": ["delay", "reckless", "rumor"],
                "uses": ["market_gossip", "official_report", "guild_record"],
            },
            "templates": {
                "supported": "Renn reads this as route reliability. A name attached to a clean delivery changes who he trusts with a satchel.",
                "rumor": "Renn hears the rumor as route weather: useful to watch, too thin to schedule around.",
                "empty": "Renn has no route note about you yet.",
            },
        },
    )

    # 36. Garrison commander
    area.npc(iq_command_office, "npc_commander_vareth", faction="empire")

    # 37. Imperial administrator
    area.npc(iq_faction_office, "npc_admin_clerk_pellith", faction="empire")

    # 38. Dragon Warden agent
    area.npc(
        iq_warden_office,
        "npc_warden_agent_calloway",
        faction="wardens",
        social_profile={
            "social_role": "gatekeeper",
            "public_trait": "careful Warden contact",
            "memory_style": "files supported reports before rumor",
            "worldview": {
                "admires": ["reliable", "warden", "report", "supported"],
                "skeptical_of": ["rumor", "boast", "reckless"],
                "uses": ["official_report", "warden_report"],
            },
            "templates": {
                "supported": "Calloway treats this as a supported report, not tavern color. He weighs the official report first and lets it decide how much road business to put in your hands.",
                "rumor": "Calloway notes the rumor but does not file it as confirmed. He will ask for a report before he changes Warden posture.",
                "empty": "Calloway has nothing specific enough to file about you.",
            },
        },
        dialogue={
            "greeting_tiers": {
                "neutral": (
                    "Calloway keeps one hand on a stack of sealed packets. "
                    "'Speak clearly. If you need the Wardens, I assume it "
                    "matters. If you want work, I assume you can travel.'"
                ),
                "friendly": (
                    "Calloway gives a curt nod. 'You're still standing, which "
                    "puts you ahead of some couriers I've had. What do you need?'"
                ),
            },
            "topics": {
                "work": {
                    "default": (
                        "'Road work, dispatches, field checks. The Ashway and "
                        "the outposts stay alive because someone carries orders, "
                        "counts trouble, and comes back with the truth instead of "
                        "a good story.'"
                    ),
                },
                "wardens": {
                    "default": (
                        "'The Wardens keep routes open, track threats before they "
                        "reach the walls, and answer when the rest of the city "
                        "would rather let a problem stay distant. There is always "
                        "more road than there are Wardens.'"
                    ),
                },
                "rumors": {
                    "default": (
                        "'Rumor says the plains are restless, patrol gaps are "
                        "widening, and too many reports are arriving late. I do "
                        "not work in rumor. I work in confirmation. That is why "
                        "I send people out.'"
                    ),
                },
                "report": {
                    "social_claim_type:report": (
                        "'Your name is attached to a report I can stand behind. "
                        "That matters more to the Wardens than a brave story told "
                        "after the road goes quiet.'"
                    ),
                    "default": (
                        "'If you are asking about reports, keep them sealed, keep "
                        "them moving, and do not improve the truth to make it sound "
                        "cleaner than it was.'"
                    ),
                },
                "testimony": {
                    "default": (
                        "'Put Whistle's testimony in the record. I will keep "
                        "the source and the seal together.'"
                    ),
                },
            },
            "base_hints": ["work", "wardens", "rumors"],
        },
    )

    # 39. Drill sergeant
    area.npc(iq_parade_ground, "npc_drill_sergeant_krath", faction="empire")

    # 40. Quartermaster
    area.npc(iq_armory, "npc_quartermaster_stubb", faction="empire")

    # Flight point (D-07)
    area.flight_point(iq_courier_platform, "vaels_crossing_courier",
                      name="Vael's Crossing Courier Platform")

    # ==================================================================
    #  DISTRICT 6: RESIDENTIAL DISTRICT (~15 rooms)
    #  Inns, tavern, homes, crafting stations (cooking, alchemy).
    # ==================================================================

    rd_main_street = area.room(
        "rd_main_street",
        name="Hearthstone Lane",
        desc=(
            "The main street of the residential district. Houses of "
            "wood and stone line both sides, their windows glowing "
            "with lamplight. Laundry hangs between buildings on lines "
            "stretched across the narrow street. Children play in the "
            "doorways while their parents work. The smell of cooking "
            "drifts from open windows."
        ),
        room_type="path",
        indoor=False,
        ambient_echoes=[
            "A child laughs somewhere down the lane.",
            "The smell of baking bread wafts from a nearby window.",
            "A dog barks at a passing cart.",
        ],
    )

    rd_tavern = area.room(
        "rd_tavern",
        name="The Broken Antler Tavern",
        desc=(
            "The city's main tavern occupies a large building with a "
            "cracked antler mounted above the door -- the trophy of "
            "some forgotten hunt. Inside, long tables fill a common "
            "room warmed by a stone hearth. The bar is a slab of "
            "scarred oak. The barkeep is a heavyset human woman who "
            "can carry four tankards in each hand and broker peace "
            "between brawlers with a look."
        ),
        room_type="building",
        indoor=True,
        ambient_echoes=[
            "Someone starts a drinking song. It's terrible.",
            "Dice rattle on a back table.",
            "The hearth fire crackles and pops.",
            "A patron snores loudly in the corner.",
        ],
    )

    rd_tavern_kitchen = area.room(
        "rd_tavern_kitchen",
        name="The Broken Antler - Kitchen",
        desc=(
            "The tavern kitchen is a hot, chaotic workspace. A massive "
            "cooking fire dominates one wall, iron pots hanging from "
            "hooks above it. A cook hacks at a joint of meat with "
            "more enthusiasm than precision. Bundles of herbs hang "
            "from the ceiling beams."
        ),
        room_type="building",
        indoor=True,
        crafting_stations=["campfire"],
    )

    rd_inn = area.room(
        "rd_inn",
        name="The Dustwalker's Rest",
        desc=(
            "An inn offering beds for the night. The rooms are small "
            "but clean -- a step up from the tavern floor. A ledger "
            "on the front desk records guests. The innkeeper is a "
            "quiet Veth woman who remembers every face that has ever "
            "slept under her roof."
        ),
        room_type="building",
        indoor=True,
    )

    rd_herbalist = area.room(
        "rd_herbalist",
        name="Ystra's Herb Garden & Workshop",
        desc=(
            "A cottage with an overgrown herb garden in front and an "
            "alchemy workspace in back. Dried plants hang from every "
            "rafter. Jars of prepared remedies line the shelves. An "
            "alchemy bench sits under the window, its surface stained "
            "with the residue of a hundred preparations."
        ),
        room_type="building",
        indoor=True,
        crafting_stations=["alchemy_bench"],
    )

    rd_sunken_temple = area.room(
        "rd_sunken_temple",
        name="The Sunken Temple",
        desc=(
            "The remains of a pre-Imperial temple, half-collapsed into "
            "the earth. Only the upper walls and a portion of the roof "
            "remain visible. Stone carvings on the exposed walls show "
            "symbols that match no known alphabet -- the same mysterious "
            "writing found on the Ashwatch Tower. Locals avoid the "
            "place after dark. The ground around it feels faintly "
            "warm, even in winter."
        ),
        room_type="ruins",
        indoor=False,
        ambient_echoes=[
            "The stones of the sunken temple hum faintly -- or is that the wind?",
            "A draft rises from somewhere beneath the collapsed floor.",
        ],
    )

    rd_well_square = area.room(
        "rd_well_square",
        name="Well Square",
        desc=(
            "A small residential square with a communal well at its "
            "center. Women gather here in the morning to draw water "
            "and exchange news. In the evening, old men sit on the "
            "well rim and argue about weather, politics, and the price "
            "of grain -- in that order."
        ),
        room_type="path",
        indoor=False,
    )

    rd_bakery = area.room(
        "rd_bakery",
        name="Marta's Bakery",
        desc=(
            "The bakery opens before dawn and the smell of fresh bread "
            "fills the street. Loaves, rolls, and heavy grain cakes "
            "fill racks behind the counter. The baker is a flour-dusted "
            "woman who never stops working and never stops talking."
        ),
        room_type="building",
        indoor=True,
    )

    rd_boarding_house = area.room(
        "rd_boarding_house",
        name="Rendell's Boarding House",
        desc=(
            "A large, run-down house divided into rental rooms. The "
            "tenants are a mix of laborers, traveling merchants, and "
            "people who prefer not to answer questions. The landlord "
            "collects rent weekly and asks nothing else."
        ),
        room_type="building",
        indoor=True,
    )

    rd_carpenter = area.room(
        "rd_carpenter",
        name="Carpenter's Workshop",
        desc=(
            "Wood shavings cover the floor of this open-fronted workshop. "
            "A carpenter shapes timber with practiced strokes. Finished "
            "furniture -- chairs, tables, bed frames -- sits along the "
            "walls waiting for buyers. The air smells of fresh-cut pine."
        ),
        room_type="building",
        indoor=True,
    )

    rd_shrine = area.room(
        "rd_shrine",
        name="Roadside Shrine",
        desc=(
            "A small stone shrine at a crossroads in the residential "
            "district. Offerings of coins, flowers, and small carved "
            "figures are left here by residents seeking good fortune. "
            "The shrine is old -- its stone worn smooth by centuries "
            "of touching hands. Nobody remembers what it was originally "
            "dedicated to."
        ),
        room_type="path",
        indoor=False,
    )

    rd_laundry = area.room(
        "rd_laundry",
        name="Communal Laundry",
        desc=(
            "A public area where residents wash clothes in stone "
            "basins fed by a small aqueduct. The water is cold but "
            "clean. Wet clothes hang on lines strung between posts. "
            "Two women scrub linens with lye soap while discussing "
            "the garrison commander's latest announcement."
        ),
        room_type="building",
        indoor=False,
    )

    rd_garden_plot = area.room(
        "rd_garden_plot",
        name="Community Garden",
        desc=(
            "A patch of ground behind the residential buildings given "
            "over to vegetable gardens. Neat rows of root vegetables, "
            "beans, and herbs grow in dark soil. A scarecrow made from "
            "an old Imperial uniform watches over the plot with empty "
            "sleeves."
        ),
        room_type="path",
        indoor=False,
    )

    rd_back_lane = area.room(
        "rd_back_lane",
        name="Hearthstone Lane - Back Way",
        desc=(
            "A narrow lane running behind the houses. Back doors, "
            "rubbish bins, and woodpiles line the passage. This is "
            "where deliveries are made and cats hunt rats. A half-open "
            "cellar door leads down into shadow."
        ),
        room_type="path",
        indoor=False,
    )

    # Residential District exits
    area.exit(rd_main_street, mk_square, "east")
    area.exit(mk_square, rd_main_street, "west")
    area.exit(rd_main_street, rd_tavern, "north")
    area.exit(rd_tavern, rd_main_street, "south")
    area.exit(rd_tavern, rd_tavern_kitchen, "west")
    area.exit(rd_tavern_kitchen, rd_tavern, "east")
    area.exit(rd_main_street, rd_inn, "east")
    area.exit(rd_inn, rd_main_street, "west")
    area.exit(rd_main_street, rd_herbalist, "west")
    area.exit(rd_herbalist, rd_main_street, "east")
    area.exit(rd_main_street, rd_well_square, "south")
    area.exit(rd_well_square, rd_main_street, "north")
    area.exit(rd_well_square, rd_bakery, "east")
    area.exit(rd_bakery, rd_well_square, "west")
    area.exit(rd_well_square, rd_boarding_house, "west")
    area.exit(rd_boarding_house, rd_well_square, "east")
    area.exit(rd_well_square, rd_sunken_temple, "south")
    area.exit(rd_sunken_temple, rd_well_square, "north")
    area.exit(rd_main_street, rd_carpenter, "northeast")
    area.exit(rd_carpenter, rd_main_street, "southwest")
    area.exit(rd_well_square, rd_shrine, "southeast")
    area.exit(rd_shrine, rd_well_square, "northwest")
    area.exit(rd_main_street, rd_laundry, "northwest")
    area.exit(rd_laundry, rd_main_street, "southeast")
    area.exit(rd_boarding_house, rd_garden_plot, "south")
    area.exit(rd_garden_plot, rd_boarding_house, "north")
    area.exit(rd_main_street, rd_back_lane, "south")
    area.exit(rd_back_lane, rd_main_street, "north")

    # Residential District NPCs

    # 41. Tavern keeper
    area.npc(
        rd_tavern,
        "npc_barkeep_marta_voss",
        faction=None,
        dialogue={
            "greeting_tiers": {
                "neutral": (
                    "Marta wipes the bar with a cloth that has given up on ever "
                    "being clean. 'If you need a drink, a room, or the kind of "
                    "work polite people call a favor, you're in the right place.'"
                ),
                "friendly": (
                    "Marta leans on the bar and smirks. 'Back already? Good. "
                    "The city always sounds clearer after one hot meal and two "
                    "solid rumors.'"
                ),
            },
            "topics": {
                "work": {
                    "default": (
                        "'I hear what breaks first in this city: cellars, tempers, "
                        "supply lines, and sometimes people's nerve. If you want "
                        "small work that leads to bigger trouble, ask me before "
                        "you ask anyone in a uniform.'"
                    ),
                },
                "rumors": {
                    "default": (
                        "'Tonight's rumor says rats are getting bold below the "
                        "taproom, caravans are arriving light, and someone down "
                        "by the river keeps paying in fresh coin for old silence. "
                        "Take whichever piece sounds like your sort of evening.'"
                    ),
                },
                "trade": {
                    "default": (
                        "'A tavern measures trade better than a counting house. "
                        "When teamsters eat well, the roads are good. When "
                        "couriers drink fast and leave faster, trouble is "
                        "moving.'"
                    ),
                },
            },
            "base_hints": ["work", "rumors", "trade"],
        },
    )

    # 42. Innkeeper
    area.npc(
        rd_inn,
        "npc_innkeeper_whistle",
        faction=None,
        social_profile={
            "social_role": "gossip",
            "public_trait": "innkeeper with a long ear",
            "memory_style": "remembers who makes trouble expensive in the taproom",
            "worldview": {
                "admires": ["tavern", "road_rumor", "discreet", "reliable"],
                "skeptical_of": ["official_report", "warden", "sealed"],
                "uses": ["tavern_rumor", "inn_traveler"],
            },
            "templates": {
                "supported": "Whistle heard it as road talk, not a sworn ledger. He keeps sealed details at arm's length, but he remembers that your name travels cleanly through the inn.",
                "rumor": "Whistle heard it as road talk and keeps sealed details at arm's length. He remembers the shape of the story, not the Warden business inside it.",
                "empty": "Whistle has no fair story about you yet.",
            },
        },
        dialogue={
            "topics": {
                "pressure": {
                    "default": (
                        "'Someone pressed me about Warden packet seals. I gave "
                        "them no sealed detail, but I remember the pressure.'"
                    ),
                },
                "testimony": {
                    "default": (
                        "'If the pressure is answered, I can put what I saw into "
                        "a statement for the Wardens.'"
                    ),
                },
            },
            "base_hints": ["pressure", "testimony"],
        },
    )

    # 43. Herbalist
    area.npc(rd_herbalist, "npc_herbalist_old_ystra", faction=None, trainer_id="npc_herbalist_old_ystra")

    # 44. Baker
    area.npc(rd_bakery, "npc_baker_marta_hawe", faction=None)

    # 45. Carpenter
    area.npc(rd_carpenter, "npc_carpenter_jorin", faction=None)

    # 46. Tavern bard
    area.npc(rd_tavern, "npc_bard_liriel", faction=None)

    # ==================================================================
    #  DISTRICT 7: THE WARRENS (Underworld) (~15 rooms)
    #  Hidden district, shady NPCs, mob spawns, unsafe.
    # ==================================================================

    wn_entrance = area.room(
        "wn_entrance",
        name="The Warrens - Cellar Stairs",
        desc=(
            "Cracked stone steps descend into a cellar that opens into "
            "something larger and older than any building above. The "
            "air is damp and smells of mildew, old stone, and unwashed "
            "bodies. Torches in rusted sconces provide flickering, "
            "unreliable light. A Selvar with a knife-scarred face "
            "watches the entrance from the shadows."
        ),
        room_type="underground",
        indoor=True,
    )

    wn_black_market = area.room(
        "wn_black_market",
        name="The Gutter Market",
        desc=(
            "An underground market carved from old cellars and forgotten "
            "tunnels. Goods of questionable provenance spread on blankets "
            "and crates. Prices are not posted. Everything is negotiable. "
            "Stolen weapons, smuggled luxuries, and substances the Empire "
            "has banned -- all available if you know how to ask and who "
            "to trust."
        ),
        room_type="underground",
        indoor=True,
        ambient_echoes=[
            "A whispered offer: 'Finest lockpicks. Imperial make. Don't ask how.'",
            "Someone coughs in the shadows. It sounds unhealthy.",
            "The clink of illicit coins changing hands.",
        ],
    )

    wn_den_of_knives = area.room(
        "wn_den_of_knives",
        name="The Den of Knives",
        desc=(
            "A cramped drinking hole lit by a single oil lamp. The "
            "patrons here do not make eye contact and do not give "
            "names. The bartender -- a massive human with a broken "
            "nose -- serves drinks in dirty cups and asks no questions. "
            "This is where debts are discussed, jobs are posted, and "
            "vendettas are born."
        ),
        room_type="underground",
        indoor=True,
    )

    wn_debt_collector = area.room(
        "wn_debt_collector",
        name="The Counting Room",
        desc=(
            "A room behind a reinforced door where a thin man in "
            "expensive clothes manages the underworld's financial "
            "operations. Ledgers sit on a desk beside a set of brass "
            "scales. Two enforcers flank the door -- they are very "
            "large and very still. The thin man smiles too much."
        ),
        room_type="underground",
        indoor=True,
    )

    wn_smuggler_dock = area.room(
        "wn_smuggler_dock",
        name="Smuggler's Dock",
        desc=(
            "A hidden loading area where goods enter the Warrens from "
            "tunnels connecting to the world outside the city walls. "
            "Crates stamped with Consortium shipping marks -- clearly "
            "redirected -- sit in stacks. A smuggler oversees the "
            "operation with the calm efficiency of a legitimate "
            "businesswoman."
        ),
        room_type="underground",
        indoor=True,
    )

    wn_sewer_junction = area.room(
        "wn_sewer_junction",
        name="Sewer Junction",
        desc=(
            "Where several old sewer lines meet, the tunnel opens into "
            "a vaulted chamber. The stench is powerful. Water -- or "
            "something worse -- flows through channels cut into the "
            "floor. Rats the size of cats watch from ledges. This is "
            "not a place people come voluntarily."
        ),
        room_type="underground",
        indoor=True,
    )

    wn_rat_tunnel = area.room(
        "wn_rat_tunnel",
        name="Rat-infested Tunnel",
        desc=(
            "A narrow tunnel where the ceiling is low enough to force "
            "a crouch. Rat droppings cover the ground. Something "
            "scrabbles in the darkness ahead. The tunnel walls are "
            "slick with moisture and an unidentifiable film."
        ),
        room_type="underground",
        indoor=True,
    )

    wn_thug_alley = area.room(
        "wn_thug_alley",
        name="Deadend Alley",
        desc=(
            "A dead-end passage where the desperate and the dangerous "
            "congregate. Debris and broken furniture create improvised "
            "barricades. Graffiti covers the walls -- territorial marks, "
            "threats, and crude drawings. The air is thick with tension."
        ),
        room_type="underground",
        indoor=True,
    )

    wn_resistance_contact = area.room(
        "wn_resistance_contact",
        name="Unmarked Alcove",
        desc=(
            "A small alcove hidden behind a loose stone panel. It looks "
            "like just another dead-end until the panel slides aside. "
            "Inside, the space is clean and organized -- at odds with "
            "the rest of the Warrens. A hooded figure sits at a small "
            "table, hands folded, waiting."
        ),
        room_type="underground",
        indoor=True,
    )

    wn_fighting_pit = area.room(
        "wn_fighting_pit",
        name="The Pit",
        desc=(
            "A sunken area ringed by wooden benches where illegal "
            "fighting matches are held. The pit floor is hard-packed "
            "earth stained dark with old blood. Spectators place bets "
            "with a bookmaker who records everything in a small "
            "notebook. The matches are brutal, the rules minimal."
        ),
        room_type="underground",
        indoor=True,
        ambient_echoes=[
            "The crowd roars as a fighter lands a vicious blow.",
            "A bookmaker shouts odds over the noise of the crowd.",
        ],
    )

    wn_collapsed_chamber = area.room(
        "wn_collapsed_chamber",
        name="Collapsed Chamber",
        desc=(
            "Part of the tunnel system that partially collapsed long "
            "ago. Broken stone and timber block most of the passage. "
            "A narrow gap at the top allows a small person -- or a "
            "brave one -- to squeeze through. Beyond, older stonework "
            "is visible -- the same dark stone as the Ashwatch Tower."
        ),
        room_type="underground",
        indoor=True,
    )

    wn_back_passage = area.room(
        "wn_back_passage",
        name="Narrow Back Passage",
        desc=(
            "A twisting passage between rough-hewn walls. Water drips "
            "from somewhere above. The passage connects several of "
            "the Warrens' spaces and serves as an escape route for "
            "those who know it well."
        ),
        room_type="underground",
        indoor=True,
    )

    wn_poison_shop = area.room(
        "wn_poison_shop",
        name="The Apothecary Below",
        desc=(
            "A clandestine shop selling substances not found at the "
            "legitimate apothecary above. Vials of poisons, paralytic "
            "agents, and hallucinogens are displayed without labels "
            "for those who know what they're looking at. The proprietor "
            "is an old Veth woman with steady hands and no conscience."
        ),
        room_type="underground",
        indoor=True,
    )

    wn_safehouse = area.room(
        "wn_safehouse",
        name="Unmarked Safehouse",
        desc=(
            "A room with a heavy door that can be barred from inside. "
            "A cot, a water barrel, and a sealed chest -- nothing else. "
            "This is where people hide when they need to disappear for "
            "a while. The walls are thick enough to muffle screams."
        ),
        room_type="underground",
        indoor=True,
    )

    wn_old_cistern = area.room(
        "wn_old_cistern",
        name="Old Cistern",
        desc=(
            "An ancient water cistern long since drained. The circular "
            "chamber is large enough to echo. The walls bear the marks "
            "of pre-Imperial construction -- fitted stones, unfamiliar "
            "symbols, no mortar. A faint warmth emanates from the "
            "floor -- the same unexplained heat found near the Sunken "
            "Temple above."
        ),
        room_type="underground",
        indoor=True,
    )

    # Warrens exits
    area.exit(wn_entrance, rd_back_lane, "up", hidden=True)
    area.exit(rd_back_lane, wn_entrance, "down", hidden=True)
    area.exit(hg_alley, wn_entrance, "down", hidden=True)
    area.exit(wn_entrance, hg_alley, "up")
    area.exit(wn_entrance, wn_black_market, "north")
    area.exit(wn_black_market, wn_entrance, "south")
    area.exit(wn_black_market, wn_den_of_knives, "east")
    area.exit(wn_den_of_knives, wn_black_market, "west")
    area.exit(wn_den_of_knives, wn_debt_collector, "north")
    area.exit(wn_debt_collector, wn_den_of_knives, "south")
    area.exit(wn_black_market, wn_smuggler_dock, "west")
    area.exit(wn_smuggler_dock, wn_black_market, "east")
    area.exit(wn_entrance, wn_sewer_junction, "south")
    area.exit(wn_sewer_junction, wn_entrance, "north")
    area.exit(wn_sewer_junction, wn_rat_tunnel, "east")
    area.exit(wn_rat_tunnel, wn_sewer_junction, "west")
    area.exit(wn_sewer_junction, wn_thug_alley, "south")
    area.exit(wn_thug_alley, wn_sewer_junction, "north")
    area.exit(wn_den_of_knives, wn_resistance_contact, "east", hidden=True)
    area.exit(wn_resistance_contact, wn_den_of_knives, "west")
    area.exit(wn_thug_alley, wn_fighting_pit, "west")
    area.exit(wn_fighting_pit, wn_thug_alley, "east")
    area.exit(wn_rat_tunnel, wn_collapsed_chamber, "east")
    area.exit(wn_collapsed_chamber, wn_rat_tunnel, "west")
    area.exit(wn_den_of_knives, wn_back_passage, "south")
    area.exit(wn_back_passage, wn_den_of_knives, "north")
    area.exit(wn_black_market, wn_poison_shop, "north")
    area.exit(wn_poison_shop, wn_black_market, "south")
    area.exit(wn_back_passage, wn_safehouse, "east")
    area.exit(wn_safehouse, wn_back_passage, "west")
    area.exit(wn_collapsed_chamber, wn_old_cistern, "east")
    area.exit(wn_old_cistern, wn_collapsed_chamber, "west")

    # Warrens NPCs

    # 47. Black market fence
    area.npc(wn_black_market, "npc_fence_shadow_mekk", faction=None)

    # 48. Den bartender
    area.npc(wn_den_of_knives, "npc_barkeep_broken_nose", faction=None)

    # 49. Debt collector
    area.npc(
        wn_debt_collector,
        "npc_debt_collector_raith",
        faction=None,
        social_profile={
            "social_role": "creditor",
            "public_trait": "obligation broker",
            "memory_style": "remembers leverage, debt, and who follows through",
            "worldview": {
                "admires": ["obligation", "leverage", "useful", "reliable"],
                "skeptical_of": ["charity", "official_report"],
                "uses": ["criminal_whisper", "tavern_rumor", "direct_witness"],
            },
            "templates": {
                "supported": "Raith reads the report as leverage: a useful person who finishes sealed work may also finish uncomfortable work.",
                "rumor": "Raith treats the rumor as possible leverage, useful enough to watch but not clean enough to spend yet.",
                "empty": "Raith has not found a useful angle on you yet.",
            },
        },
        dialogue={
            "topics": {
                "pressure": {
                    "default": (
                        "'You came a long way to say pressure. Make the "
                        "accusation you mean, or leave the word alone.'"
                    ),
                },
            },
            "base_hints": ["pressure"],
        },
    )

    # 50. Smuggler boss
    area.npc(wn_smuggler_dock, "npc_smuggler_kessa", faction=None)

    # 51. Resistance contact (hidden faction)
    area.npc(wn_resistance_contact, "npc_resistance_contact_shadow", faction=None)

    # 52. Pit bookmaker
    area.npc(wn_fighting_pit, "npc_bookmaker_odds", faction=None)

    # 53. Poison vendor
    area.npc(wn_poison_shop, "npc_poison_vendor_nightshade", faction=None)

    # 54. Warren lookout
    area.npc(wn_entrance, "npc_lookout_scar", faction=None)

    # ==================================================================
    #  MOB SPAWNS — Warrens only (D-05: unsafe edges)
    # ==================================================================

    # Sewer rats — passive, wander
    area.spawn(wn_sewer_junction, "sewer_rat", count_min=1, count_max=2,
               respawn_minutes=10, respawn_variance=3)
    area.spawn(wn_rat_tunnel, "sewer_rat", count_min=2, count_max=3,
               respawn_minutes=10, respawn_variance=3)

    # Thugs — cautious, won't chase
    area.spawn(wn_thug_alley, "thug", count_min=1, count_max=2,
               respawn_minutes=15, respawn_variance=5,
               base_disposition=-0.3)
    area.spawn(wn_back_passage, "thug", count_min=1, count_max=1,
               respawn_minutes=15, respawn_variance=5,
               base_disposition=-0.3)

    # Smugglers — aggressive when cornered
    area.spawn(wn_smuggler_dock, "smuggler", count_min=1, count_max=2,
               respawn_minutes=20, respawn_variance=5,
               base_disposition=-0.2)

    # Pickpocket — rare, wanders
    area.spawn(wn_black_market, "pickpocket", count_min=0, count_max=1,
               respawn_minutes=30, respawn_variance=10,
               base_disposition=-0.1)

    # ==================================================================
    #  ITEMS — Vendor equipment and consumables (D-15)
    # ==================================================================

    # --- Starter Weapons (Iron tier) ---
    area.item("iron_sword", key="iron sword", item_type="equipment",
              equip_slot="main_hand", damage_min=8, damage_max=14,
              stat_scaling="strength", value=50,
              desc="A standard-issue iron sword. Functional, unremarkable, dependable.")
    area.item("iron_dagger", key="iron dagger", item_type="equipment",
              equip_slot="main_hand", damage_min=5, damage_max=10,
              stat_scaling="agility", value=35,
              desc="A short iron dagger. Quick in the hand, light on the belt.")
    area.item("iron_mace", key="iron mace", item_type="equipment",
              equip_slot="main_hand", damage_min=10, damage_max=16,
              stat_scaling="strength", value=55,
              desc="A heavy iron mace. What it lacks in finesse it makes up for in impact.")
    area.item("iron_staff", key="iron-shod staff", item_type="equipment",
              equip_slot="main_hand", damage_min=6, damage_max=12,
              stat_scaling="intellect", value=40,
              desc="A wooden staff capped with iron. Favored by those who prefer magic to muscle.")
    area.item("iron_axe", key="iron axe", item_type="equipment",
              equip_slot="main_hand", damage_min=9, damage_max=15,
              stat_scaling="strength", value=50,
              desc="An iron-headed axe. Splits wood and skulls with equal efficiency.")
    area.item("iron_greatsword", key="iron greatsword", item_type="equipment",
              equip_slot="main_hand", two_handed=True, damage_min=14, damage_max=22,
              stat_scaling="strength", value=80,
              desc="A massive two-handed iron blade. Requires both hands and considerable resolve.")
    area.item("iron_greataxe", key="iron greataxe", item_type="equipment",
              equip_slot="main_hand", two_handed=True, damage_min=16, damage_max=24,
              stat_scaling="strength", value=85,
              desc="A two-handed axe of raw iron. Slow, devastating, unsubtle.")

    # --- Starter Armor (Leather tier) ---
    area.item("leather_cap", key="leather cap", item_type="equipment",
              equip_slot="head", armor=3, stat_bonus={"endurance": 1},
              value=25,
              desc="A hard leather cap. Keeps the rain off and the blows slightly less fatal.")
    area.item("leather_vest", key="leather vest", item_type="equipment",
              equip_slot="chest", armor=8, stat_bonus={"endurance": 2},
              value=60,
              desc="A sturdy leather vest. Standard protection for the practical adventurer.")
    area.item("leather_gloves", key="leather gloves", item_type="equipment",
              equip_slot="hands", armor=2, stat_bonus={"agility": 1},
              value=20,
              desc="Supple leather gloves. Good grip, decent protection.")
    area.item("leather_boots", key="leather boots", item_type="equipment",
              equip_slot="feet", armor=3, stat_bonus={"agility": 1},
              value=30,
              desc="Worn leather boots. They've walked a lot of roads.")
    area.item("leather_leggings", key="leather leggings", item_type="equipment",
              equip_slot="legs", armor=5, stat_bonus={"endurance": 1},
              value=40,
              desc="Leather leggings. Flexible enough to run in, tough enough to matter.")
    area.item("leather_bracers", key="leather bracers", item_type="equipment",
              equip_slot="wrists", armor=2, stat_bonus={"strength": 1},
              value=20,
              desc="Stiff leather bracers. Protect the forearms from blade and bramble.")
    area.item("iron_buckler", key="iron buckler", item_type="equipment",
              equip_slot="off_hand", armor=5, stat_bonus={"endurance": 1},
              value=35,
              desc="A small round shield of battered iron. Passive defense for the off hand.")
    area.item("traveler_cloak", key="traveler's cloak", item_type="equipment",
              equip_slot="back", armor=1, stat_bonus={"perception": 1},
              value=15,
              desc="A dusty wool cloak. Keeps the wind and the worst of the weather at bay.")

    # --- Consumables ---
    area.item("minor_healing_potion", key="minor healing potion",
              item_type="consumable", effect="heal", magnitude=30,
              value=15,
              desc="A small glass vial of reddish liquid. Tastes like copper and hope.")
    area.item("healing_potion", key="healing potion",
              item_type="consumable", effect="heal", magnitude=60,
              value=35,
              desc="A standard healing potion. The apothecary's most reliable seller.")
    area.item("stamina_draught", key="stamina draught",
              item_type="consumable", effect="restore_stamina", magnitude=40,
              value=20,
              desc="A bitter green draught that restores flagging energy.")
    area.item("antidote", key="antidote",
              item_type="consumable", effect="cure_poison", magnitude=1,
              value=25,
              desc="A cloudy liquid that neutralizes most common poisons.")

    # --- Quest Items ---
    area.item("warden_field_report", key="warden field report",
              item_type="item", weight=0.2, rarity="normal", value=0,
              is_quest_item=True,
              desc="A wax-sealed dispatch tube packed with patrol reports and route warnings from Vael's Crossing.")

    # ==================================================================
    #  LORE FRAGMENTS (D-10 landmarks, atmospheric discoveries)
    # ==================================================================

    area.lore_fragment(
        "lore_ashwatch_symbols", hg_watchtower_top,
        discovery_method="search",
        text=(
            "The symbols carved into the Ashwatch Tower parapet are "
            "arranged in groups of eight. Each group follows a pattern -- "
            "four primary symbols, four modifiers. The notation system "
            "is mathematical, not linguistic. It predates every known "
            "human writing system by at least two thousand years."
        ),
        insight_gain=5,
    )

    area.lore_fragment(
        "lore_sunken_temple_warmth", rd_sunken_temple,
        discovery_method="search",
        scholar_path="remnance",
        text=(
            "The warmth emanating from beneath the Sunken Temple has "
            "no natural source. It is consistent, never varying. A "
            "careful comparison against old survey notes identifies it "
            "as the thermal signature of an intact sub-surface node -- "
            "dormant but not dead. The temple was built directly over it. "
            "Not coincidentally."
        ),
        insight_gain=8,
    )

    area.lore_fragment(
        "lore_old_cistern_stones", wn_old_cistern,
        discovery_method="search",
        scholar_path="remnance",
        text=(
            "The stones of the old cistern are fitted with older-than-Imperial "
            "precision. No mortar, no gaps. The symbols carved into "
            "the walls match those on the Ashwatch Tower and the "
            "Sunken Temple. Three locations in one city, all built in "
            "the same older design tradition."
        ),
        insight_gain=10,
    )

    area.lore_fragment(
        "lore_guild_tree", gq_courtyard,
        discovery_method="search",
        text=(
            "The ancient tree in the Guild Quarter courtyard is of no "
            "known species. Its bark bears the same unfamiliar symbols. "
            "It has stood here longer than the city. The guilds built "
            "around it -- not the other way around."
        ),
        insight_gain=3,
    )

    area.lore_fragment(
        "lore_customs_weights", hg_customs_office,
        discovery_method="search",
        text=(
            "The oldest customs weights are cut with eight equal notches "
            "instead of the modern trade marks used by the Consortium. "
            "They measure volume and burden according to a system older "
            "than the city, suggesting the gate inherited its duties "
            "from an earlier road station."
        ),
        insight_gain=4,
    )

    area.lore_fragment(
        "lore_market_well_shaft", mk_well,
        discovery_method="search",
        scholar_path="remnance",
        text=(
            "The market well descends through newer brick before meeting "
            "a ring of fitted dark stone identical to the old cistern. "
            "The shaft was not first dug to serve the square. The square "
            "was laid over a much older water system already waiting here."
        ),
        insight_gain=6,
    )

    area.lore_fragment(
        "lore_library_survey_roll", gq_library,
        discovery_method="search",
        text=(
            "A brittle survey roll in the shared library places Ashwatch, "
            "the Sunken Temple, and the old road markers of Ashreach on "
            "one uninterrupted line. The early city planners did not pick "
            "their landmarks at random. They built around a preexisting "
            "network they only partly understood."
        ),
        insight_gain=7,
    )

    area.lore_fragment(
        "lore_courier_marker", iq_courier_platform,
        discovery_method="search",
        text=(
            "Under the courier roost's newest flagstones lies a much older "
            "sighting mark cut into the parapet itself. The angle lines do "
            "not point at city walls or roads. They point toward the plains, "
            "the coast, and the mountain pass with mathematical precision."
        ),
        insight_gain=5,
    )

    area.lore_fragment(
        "lore_river_pilings", wn_smuggler_dock,
        discovery_method="search",
        text=(
            "The smugglers lash boats to timber, but the lower pilings are "
            "stone. Those blocks are older than the riverfront above them "
            "and fitted with the same pressure-tight joints seen in the "
            "Sunken Temple and the old cistern. Someone engineered this "
            "landing for heavier use than smugglers and ferrymen manage now."
        ),
        insight_gain=6,
    )

    # ==================================================================
    #  QUESTS (enriched specs — D-21/D-22)
    # ==================================================================

    area.quest("vc_q_missing_shipment",
        name="The Missing Shipment",
        description="Broker Carston has a shipment of survey brass and dried stores vanish between the loading bay, the records office, and the river line. Follow the paper trail and the river trail before the loss disappears into the Warrens for good.",
        quest_type="investigation",
        quest_giver="npc_broker_carston",
        objectives=[
            {"type": "investigate", "target": "vc_warehouse_district", "count": 1,
             "description": "Inspect the warehouse loading bay where the shipment was last seen"},
            {"type": "investigate", "target": "cq_records_office", "count": 1,
             "description": "Check the Consortium records office for altered manifests"},
            {"type": "investigate", "target": "wn_smuggler_dock", "count": 1,
             "description": "Trace the shipment to the hidden river docks below the city"},
        ],
        rewards=[
            {"action_type": "give_scales", "amount": 80},
            {"action_type": "modify_standing", "faction_id": "consortium", "delta": 150},
            {"action_type": "echo", "message": "|gCarston folds the corrected manifest into his ledger. \"So that is how it walked. Quiet work, and useful work. I can use people who notice the seams in a city.\"|n"},
        ],
        next_quest_id="vc_q_stolen_goods",
        # Legacy fields (backward compat)
        objective_type="investigate",
        objective_target="vc_warehouse_district",
        objective_count=1,
    )

    area.quest("vc_q_rat_problem",
        name="Cellar Menace",
        description="Marta Voss needs someone to clear the sewer rats that have been ruining her ale stores. They've gotten bolder since the last cold snap drove them up from the undercity.",
        quest_type="combat",
        quest_giver="npc_barkeep_marta_voss",
        objectives=[
            {"type": "kill", "target": "sewer_rat", "count": 10,
             "description": "Kill sewer rats in the cellar"},
        ],
        rewards=[
            {"action_type": "give_scales", "amount": 50},
            {"action_type": "modify_standing", "faction_id": "consortium", "delta": 100},
            {"action_type": "echo", "message": "|gMarta slides a pouch of coins across the bar. \"That should keep them out for a while. Drink's on me.\"|n"},
        ],
        # Legacy fields (backward compat)
        objective_type="kill",
        objective_target="sewer_rat",
        objective_count=10,
    )

    area.quest("vc_q_warden_report",
        name="Ashway Dispatch",
        description="Agent Calloway needs a sealed field report carried to Commander Harven at the Ashreach outpost. The roads are still thinly patrolled, and the Wardens trust a traveler who can actually reach the line more than any stamped order left sitting in a tray.",
        quest_type="delivery",
        quest_giver="npc_warden_agent_calloway",
        objectives=[
            {"type": "deliver", "target": "npc_warden_outpost_commander", "count": 1,
             "description": "Deliver the field report to the outpost commander"},
        ],
        flagged_drop="warden_field_report",
        rewards=[
            {"action_type": "give_scales", "amount": 60},
            {"action_type": "modify_standing", "faction_id": "wardens", "delta": 200},
            {
                "action_type": "record_social_event",
                "nodes": [
                    {
                        "ref": "player",
                        "node_type": "player",
                        "identifier_template": "{character_id}",
                        "display_name_template": "{character_key}",
                        "zone_id": "vaels_crossing",
                        "settlement_id": "vaels_crossing",
                    },
                    {
                        "ref": "calloway",
                        "node_type": "npc",
                        "identifier": "npc_warden_agent_calloway",
                        "display_name": "Agent Calloway",
                        "zone_id": "vaels_crossing",
                        "settlement_id": "vaels_crossing",
                        "faction_id": "wardens",
                    },
                    {
                        "ref": "harven",
                        "node_type": "npc",
                        "identifier": "npc_warden_outpost_commander",
                        "display_name": "Commander Harven",
                        "zone_id": "ashreach_plains",
                        "settlement_id": "ashreach_outpost",
                        "faction_id": "wardens",
                    },
                ],
                "edges": [
                    {
                        "source": "calloway",
                        "target": "harven",
                        "edge_type": "warden_report",
                        "directionality": "one_way",
                        "trust": 0.95,
                        "latency_seconds": 0,
                        "scope_tags": ["warden", "report", "quest"],
                    },
                ],
                "fact": {
                    "fact_key_template": "fact:{character_id}:vc_q_warden_report:delivered",
                    "subject": "player",
                    "actor": "player",
                    "scope": "calloway",
                    "event_type": "quest_completed",
                    "summary": "The player delivered Calloway's sealed field report.",
                    "tags": ["reliable", "warden", "report", "quest"],
                    "visibility": "institutional",
                    "evidence": {
                        "quest_id": "vc_q_warden_report",
                        "source": "quest_reward",
                    },
                },
                "claim": {
                    "claim_key_template": "claim:calloway:{character_id}:vc_q_warden_report:delivered",
                    "speaker": "calloway",
                    "subject": "player",
                    "claim_type": "report",
                    "summary": "Calloway reports that the player carried Warden business cleanly.",
                    "status": "supported",
                    "confidence": 1.0,
                    "bias_tags": ["warden", "report", "quest"],
                },
                "knowledge": [
                    {
                        "node": "calloway",
                        "fact_key_template": "fact:{character_id}:vc_q_warden_report:delivered",
                        "channel": "official_report",
                        "confidence": 1.0,
                        "spreading": False,
                    },
                    {
                        "node": "calloway",
                        "claim_key_template": "claim:calloway:{character_id}:vc_q_warden_report:delivered",
                        "channel": "official_report",
                        "confidence": 1.0,
                        "spreading": True,
                    },
                ],
                "propagate": {
                    "source": "calloway",
                    "claim_key_template": "claim:calloway:{character_id}:vc_q_warden_report:delivered",
                    "required": True,
                },
            },
            {
                "action_type": "record_social_event",
                "nodes": [
                    {
                        "ref": "player",
                        "node_type": "player",
                        "identifier_template": "{character_id}",
                        "display_name_template": "{character_key}",
                        "zone_id": "vaels_crossing",
                        "settlement_id": "vaels_crossing",
                    },
                    {
                        "ref": "travelers",
                        "node_type": "gathering",
                        "identifier": "vc_inn_travelers",
                        "display_name": "Dustwalker's Rest travelers",
                        "zone_id": "vaels_crossing",
                        "settlement_id": "vaels_crossing",
                    },
                ],
                "fact": {
                    "fact_key_template": "fact:{character_id}:vc_q_warden_report:road_conduct",
                    "subject": "player",
                    "actor": "player",
                    "scope": "travelers",
                    "event_type": "road_conduct",
                    "summary": "The player carried road business cleanly.",
                    "tags": ["public", "road_conduct", "traveler", "quest"],
                    "visibility": "route",
                    "evidence": {
                        "quest_id": "vc_q_warden_report",
                        "source": "quest_reward",
                    },
                },
                "claim": {
                    "claim_key_template": "claim:gathering:vc_inn_travelers:{character_id}:vc_q_warden_report:road_conduct",
                    "speaker": "travelers",
                    "subject": "player",
                    "claim_type": "rumor",
                    "summary": "Travelers say the player carried road business cleanly.",
                    "status": "supported",
                    "confidence": 0.75,
                    "bias_tags": ["public", "road_conduct", "traveler", "quest"],
                },
                "knowledge": [
                    {
                        "node": "travelers",
                        "claim_key_template": "claim:gathering:vc_inn_travelers:{character_id}:vc_q_warden_report:road_conduct",
                        "channel": "tavern_rumor",
                        "confidence": 0.75,
                        "spreading": True,
                    },
                ],
            },
            {"action_type": "echo", "message": "|gCalloway checks the returned seal and gives a rare approving nod. \"Good. That road stays alive because someone walks it on purpose. The Wardens remember that.\"|n"},
        ],
        next_quest_id="ashreach_wolf_overpopulation",
        one_chance=True,
        # Legacy fields (backward compat)
        objective_type="deliver",
        objective_target="npc_warden_outpost_commander",
        objective_count=1,
    )

    area.quest("vc_q_debt_collection",
        name="Quiet Collections",
        description="Raith has decided broken noses are bad for business and wants signatures instead of bruises. Track down three debtors across the city and make certain they remember whose coin kept them open through lean months.",
        quest_type="social",
        quest_giver="npc_debt_collector_raith",
        objectives=[
            {"type": "talk_to", "target": "npc_exchange_clerk_bynn", "count": 1,
             "description": "Remind Bynn at the exchange what he still owes"},
            {"type": "talk_to", "target": "npc_innkeeper_whistle", "count": 1,
             "description": "Collect Whistle's promise of payment at the Dustwalker's Rest"},
            {"type": "talk_to", "target": "npc_wheelwright_tomas", "count": 1,
             "description": "Get Tomas to acknowledge the overdue wheel order in the wagon yard"},
        ],
        rewards=[
            {"action_type": "give_scales", "amount": 90},
            {"action_type": "modify_standing", "faction_id": "consortium", "delta": 100},
            {"action_type": "echo", "message": "|gRaith skims the signed pledges and tucks them away. \"Better. Fear spends once. Obligation spends for years. You did this the useful way.\"|n"},
        ],
        # Legacy fields (backward compat)
        objective_type="talk_to",
        objective_target="npc_exchange_clerk_bynn",
        objective_count=1,
    )

    area.quest("vc_q_forging_commission",
        name="Goram's Temper",
        description="Goram refuses to ruin a commission on suspect ore. Inspect the import dock, the wagon yard, and the forge itself so he can work out where bad metal entered the city's supply before he wastes heat and reputation on it.",
        quest_type="crafting",
        quest_giver="npc_smith_goram",
        objectives=[
            {"type": "investigate", "target": "cq_import_dock", "count": 1,
             "description": "Inspect the import dock for signs of tampered ore shipments"},
            {"type": "investigate", "target": "hg_wagon_yard", "count": 1,
             "description": "Check the wagon yard where the mountain loads are broken down"},
            {"type": "investigate", "target": "mk_forge", "count": 1,
             "description": "Compare the suspect ore against Goram's current stock at the forge"},
        ],
        rewards=[
            {"action_type": "give_scales", "amount": 85},
            {"action_type": "give_skill_xp", "skill_id": "smithing", "count": 4},
            {"action_type": "modify_standing", "faction_id": "consortium", "delta": 100},
            {"action_type": "echo", "message": "|gGoram grunts over the slag streaks you found in the shipment notes. \"There. That is the lie in the metal. A forge is honest if the hands feeding it are. You just saved me a bad commission.\"|n"},
        ],
        next_quest_id="rf_q_lost_miners",
        # Legacy fields (backward compat)
        objective_type="investigate",
        objective_target="cq_import_dock",
        objective_count=1,
    )

    area.quest("vc_q_stolen_goods",
        name="Shadow Market Recovery",
        description="Shadow Mekk knows where the warehouse relics passed after last month's heists. He wants proof of the route more than the cargo itself: loading bay, black market, and the safehouse where the real buyers wait for the city to stop looking.",
        quest_type="investigation",
        quest_giver="npc_fence_shadow_mekk",
        prerequisite_quests=["vc_q_missing_shipment"],
        objectives=[
            {"type": "investigate", "target": "vc_warehouse_district", "count": 1,
             "description": "Revisit the loading bay where the theft route began"},
            {"type": "investigate", "target": "wn_black_market", "count": 1,
             "description": "Work through the black market stalls where the relics were fenced"},
            {"type": "investigate", "target": "wn_safehouse", "count": 1,
             "description": "Confirm where the heist goods are being held after sale"},
        ],
        rewards=[
            {"action_type": "give_scales", "amount": 110},
            {"action_type": "give_skill_xp", "skill_id": "investigation", "count": 3},
            {"action_type": "echo", "message": "|gMekk studies the route you traced and smiles without warmth. \"That is what I needed. Goods come and go. Knowing who moved them and where they vanish is what keeps a person alive down here.\"|n"},
        ],
        # Legacy fields (backward compat)
        objective_type="investigate",
        objective_target="wn_black_market",
        objective_count=1,
    )

    area.quest("vc_q_tower_mystery",
        name="Echoes of the Tower",
        description="Archivist Morwen wants a clean survey of the three oldest intact sites in the city: the Ashwatch ruins, the Sunken Temple, and the old cistern. The same buried geometry runs through all of them, and she needs more than rumor before she asks the guilds to treat the pattern seriously.",
        quest_type="exploration",
        quest_giver="npc_guildmaster_remnance_morwen",
        objectives=[
            {"type": "investigate", "target": "ashwatch_tower_ruins", "count": 1,
             "description": "Survey the old Ashwatch ruins for surviving ward geometry"},
            {"type": "investigate", "target": "rd_sunken_temple", "count": 1,
             "description": "Compare the Sunken Temple's buried stonework against Ashwatch"},
            {"type": "investigate", "target": "wn_old_cistern", "count": 1,
             "description": "Trace the shared markings down into the old cistern"},
        ],
        rewards=[
            {"action_type": "give_scales", "amount": 100},
            {"action_type": "give_skill_xp", "skill_id": "investigation", "count": 4},
            {"action_type": "echo", "message": "|gMorwen lays your notes beside older sketches from the library. \"Good. Not ghosts, then. Structure. Repetition. Someone laid this city over a much older thought, and now we can start proving it without making fools of ourselves.\"|n"},
        ],
        # Legacy fields (backward compat)
        objective_type="investigate",
        objective_target="ashwatch_tower_ruins",
        objective_count=1,
    )

    area.quest("vc_q_herbalist_gathering",
        name="Ystra's Remedy",
        description="Old Ystra's strongest remedies depend on herbs that only survive beyond the city walls -- in the ash-choked plains and on the cooler ledges of the Reth. Bring her enough bundles to restock before the next caravan season turns every scraped knee into a fever.",
        quest_type="gathering",
        quest_giver="npc_herbalist_old_ystra",
        objectives=[
            {"type": "collect", "target": "rare_herb_bundle", "count": 5,
             "description": "Gather rare herb bundles from Ashreach and the lower Reth"},
        ],
        rewards=[
            {"action_type": "give_scales", "amount": 70},
            {"action_type": "give_skill_xp", "skill_id": "herbalism", "count": 3},
            {"action_type": "learn_recipe", "recipe_id": "healing_draught"},
            {"action_type": "echo", "message": "|gYstra's weathered hands sort through the herbs with practiced care. \"Good quality. Here -- let me show you how I make my draughts. You've earned the knowledge.\"|n"},
        ],
        next_quest_id="rf_q_rare_ingredients",
        # Legacy fields (backward compat)
        objective_type="gather",
        objective_target="rare_herb_bundle",
        objective_count=5,
    )

    # ==================================================================
    #  PRACTICE OPPORTUNITIES (one-shot journey-start skill contact)
    # ==================================================================

    area.practice_opportunity(
        "vc_stable_calm_nervous_mare",
        hg_stable,
        verb="calm",
        target="nervous mare",
        skill_awards={"animal_handling": 3},
        domain_awards={"naturalism": 75},
        success_text="You lower your voice, keep your hands open, and wait until the mare stops fighting the halter. The stablehand notices the patience more than the speed.",
        once_per_character=True,
        visible_in_exits=True,
        desc="calm nervous mare",
        aliases=["soothe"],
    )
    area.practice_opportunity(
        "vc_notice_wall_compare_routes",
        hg_notice_wall,
        verb="compare",
        target="road notices",
        skill_awards={"navigation": 2, "scholarship": 1},
        domain_awards={"tactics": 60},
        success_text="You compare old road notices against the fresher Warden marks and pick out which warnings still matter beyond the gate.",
        once_per_character=True,
        visible_in_exits=True,
        desc="compare road notices",
    )
    area.practice_opportunity(
        "vc_customs_pick_jammed_lockbox",
        hg_customs_office,
        verb="pick",
        target="jammed lockbox",
        skill_awards={"lockpicking": 3},
        domain_awards={"subterfuge": 75},
        success_text="You work the bent lockbox carefully enough to free the clasp without snapping the clerk's only key inside it.",
        once_per_character=True,
        visible_in_exits=True,
        desc="pick jammed lockbox",
    )
    area.practice_opportunity(
        "vc_tanner_cut_repair_strap",
        mk_tanner,
        verb="cut",
        target="repair strap",
        skill_awards={"leatherworking": 3},
        domain_awards={"naturalism": 60},
        success_text="You cut the strap along the grain instead of across it, then stitch the stress point where the tanner taps the bench.",
        once_per_character=True,
        visible_in_exits=True,
        desc="cut repair strap",
    )
    area.practice_opportunity(
        "vc_records_study_tariff_ledger",
        cq_records_office,
        verb="study",
        target="tariff ledger",
        skill_awards={"scholarship": 3, "appraisal": 1},
        domain_awards={"diplomacy": 60},
        success_text="You trace three columns of tariffs until a smuggling pattern becomes visible in the spaces between legitimate fees.",
        once_per_character=True,
        visible_in_exits=True,
        desc="study tariff ledger",
    )
    area.practice_opportunity(
        "vc_medic_tend_field_dressing",
        iq_medic_building,
        verb="tend",
        target="field dressing",
        skill_awards={"first_aid": 3},
        domain_awards={"alchemy": 75},
        success_text="You clean the wound before binding it, and the medic nods once when the cloth holds without cutting off circulation.",
        once_per_character=True,
        visible_in_exits=True,
        desc="tend field dressing",
    )
    area.practice_opportunity(
        "vc_training_yard_evade_padded_strike",
        gq_training_yard,
        verb="evade",
        target="padded strike",
        skill_awards={"reflexes": 3},
        domain_awards={"combat": 75},
        success_text="You move on the trainer's shoulder twitch instead of the padded blade, learning the warning before the blow.",
        once_per_character=True,
        visible_in_exits=True,
        desc="evade padded strike",
    )
    area.practice_opportunity(
        "vc_wagon_yard_brace_axle_strap",
        hg_wagon_yard,
        verb="brace",
        target="axle strap",
        skill_awards={"engineering": 3},
        domain_awards={"engineering": 75},
        success_text="You brace the cracked axle strap with a wedge and wire wrap, buying the driver enough miles to reach a proper shop.",
        once_per_character=True,
        visible_in_exits=True,
        desc="brace axle strap",
    )

    # ==================================================================
    #  TRIGGERS (zone entry, recipe learning, atmospheric)
    # ==================================================================

    # Zone entry — first visit atmospheric welcome
    area.trigger(
        hg_arrival, "on_first_visit",
        [{"action_type": "echo", "message": "|yThe gates of Vael's Crossing stand open before you. The smell of woodsmoke and spiced meat drifts from somewhere deeper in the city. A guard gives you an appraising look but waves you through.|n"}],
        trigger_id="vc_first_arrival",
        once_per_character=True,
    )

    # Forge — learn iron chainmail recipe from Goram
    area.trigger(
        mk_forge, "on_first_visit",
        [{"action_type": "learn_recipe", "recipe_id": "iron_chainmail", "learned_from": "Goram the Smith", "message": "|gGoram demonstrates a basic chainmail weave. You have learned to craft |wIron Chainmail|g.|n"}],
        trigger_id="vc_forge_learn_chainmail",
        once_per_character=True,
    )

    # Alchemy lab — learn antidote recipe from Mirelle
    area.trigger(
        gq_alchemy_lab, "on_first_visit",
        [{"action_type": "learn_recipe", "recipe_id": "antidote", "learned_from": "Mirelle", "message": "|gMirelle shows you how to distill a basic antidote. You have learned to brew |wAntidote|g.|n"}],
        trigger_id="vc_alchemy_learn_antidote",
        once_per_character=True,
    )

    # Alchemy lab — learn stamina tonic recipe from Mirelle
    area.trigger(
        gq_alchemy_lab, "on_first_visit",
        [{"action_type": "learn_recipe", "recipe_id": "stamina_tonic", "learned_from": "Mirelle", "message": "|gMirelle demonstrates the stamina tonic formula. You have learned to brew |wStamina Tonic|g.|n"}],
        trigger_id="vc_alchemy_learn_stamina",
        once_per_character=True,
    )

    # Food stalls — learn spiced fish recipe from Malani
    area.trigger(
        mk_food_stalls, "on_first_visit",
        [{"action_type": "learn_recipe", "recipe_id": "spiced_fish", "learned_from": "Malani", "message": "|gMalani shares her spiced fish recipe with a knowing grin. You have learned to cook |wSpiced Fish|g.|n"}],
        trigger_id="vc_food_learn_spiced_fish",
        once_per_character=True,
    )

    # ==================================================================
    #  MATERIALS (zone-level harvestable materials)
    # ==================================================================

    area.material("iron_ore", tier=1, terrain="underground",
                  profession_bonus={"smithing": 0.1})
    area.material("common_herb", tier=1, terrain="garden",
                  profession_bonus={"herbalism": 0.05, "alchemy": 0.05})
    area.material("rough_leather", tier=1, terrain="building",
                  profession_bonus={"smithing": 0.05})

    # ==================================================================
    #  GATHERING POOLS
    # ==================================================================

    area.gathering_pool(
        "herb",
        rooms=["rd_garden_plot", "rd_herbalist", "gq_alchemy_lab"],
        materials=["common_herb"],
        max_active=2, respawn_minutes=8, respawn_variance=3,
    )
    area.gathering_pool(
        "hide",
        rooms=["mk_tanner", "mk_cloth_row"],
        materials=["rough_leather"],
        max_active=2, respawn_minutes=12, respawn_variance=4,
    )
    area.gathering_pool(
        "fish",
        rooms=["cq_import_dock", "wn_smuggler_dock"],
        materials=["river_trout"],
        max_active=2, respawn_minutes=12, respawn_variance=4,
    )

    # Social Web topology — literal graph data, not quest reward side effects.
    area.social_node(
        "npc", "npc_courier_agent_renn", display_name="Renn",
        settlement_id="vaels_crossing", faction_id="consortium",
    )
    area.social_node(
        "npc", "npc_warden_agent_calloway", display_name="Agent Calloway",
        settlement_id="vaels_crossing", faction_id="wardens",
    )
    area.social_node(
        "npc", "npc_innkeeper_whistle", display_name="Whistle",
        settlement_id="vaels_crossing",
    )
    area.social_node(
        "gathering", "vc_inn_travelers",
        display_name="Dustwalker's Rest travelers",
        settlement_id="vaels_crossing",
    )
    area.social_node(
        "npc", "npc_debt_collector_raith", display_name="Raith",
        settlement_id="vaels_crossing",
    )
    area.social_edge(
        "npc:npc_warden_agent_calloway",
        "npc:npc_warden_outpost_commander",
        edge_type="warden_report",
        directionality="one_way",
        trust=0.95,
        latency_seconds=0,
        scope_tags=["warden", "report", "quest"],
    )
    area.social_edge(
        "gathering:vc_inn_travelers",
        "npc:npc_innkeeper_whistle",
        edge_type="inn_traveler",
        directionality="one_way",
        trust=0.75,
        latency_seconds=60,
        scope_tags=["public", "road_conduct", "traveler", "quest"],
    )

    # ==================================================================
    #  BUILD
    # ==================================================================

    return area.build()
