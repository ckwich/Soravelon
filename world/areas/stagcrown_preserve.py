"""
Stagcrown Preserve -- Hub 4 exterior zone

The noble preserve outside Varath Prime. Managed game trails, lodge grounds,
poacher blinds, reservoir edges, and stone-ring woods reveal how elite leisure
rests on enclosure, paperwork, hidden violence, and older boundaries pressed
into decorative service.
"""

from world.area_builder import AreaBuilder


def build():
    area = AreaBuilder("stagcrown_preserve")

    # ------------------------------------------------------------------
    # Zone setup
    # ------------------------------------------------------------------
    area.zone(
        name="Stagcrown Preserve",
        zone_type="frontier",
        continent="varath",
        tier=4,
        region="crownlands",
        hub_city="varath_prime",
        faction_territory="imperial",
        faction_presence=["empire", "consortium", "circle"],
        world_x=244,
        world_y=78,
        world_radius=126,
    )

    # ------------------------------------------------------------------
    # Materials
    # ------------------------------------------------------------------
    area.material("horncap_moss", tier=1, terrain="forest", absorbed_property="clarity", profession_bonus={"alchemy": 0.1, "scholarship": 0.05})
    area.material("charter_bark", tier=1, terrain="forest", absorbed_property="precision", profession_bonus={"scholarship": 0.1})
    area.material("stagcrown_hide", tier=1, terrain="forest", absorbed_property="tenacity", profession_bonus={"leatherworking": 0.1})
    area.material("silverfin_trout", tier=1, terrain="water", absorbed_property=None, profession_bonus={"cooking": 0.1})
    area.material("keeper_reed", tier=1, terrain="water", absorbed_property=None, profession_bonus={"cooking": 0.05, "alchemy": 0.05})
    area.material("bone_lure", tier=1, terrain="path", absorbed_property="durability", profession_bonus={"leatherworking": 0.05, "cooking": 0.05})

    # ==================================================================
    #  FORMAL HUNTING GATES
    # ==================================================================
    fg_charter_gate = area.room("fg_charter_gate", name="Charter Gate", desc="A dressed-stone gate and iron grill mark the gentle road out of Noble Heights, where smiling keepers inspect preserve writs with a courtesy reserved for the well-born.", room_type="path")
    fg_brass_check = area.room("fg_brass_check", name="Brass Check", desc="Polished scale arms, tally slates, and a tray for invitation seals turn this checkpoint into a ritual of class performed as hospitality.", room_type="path")
    fg_entry_lawn = area.room("fg_entry_lawn", name="Entry Lawn", desc="Clipped grass and pale gravel soften the road just enough to make the move from city street to private hunting ground feel deliberate.", room_type="clearing")
    fg_writ_arch = area.room("fg_writ_arch", name="Writ Arch", desc="The arch overhead bears the Stagcrown Revision of 728 in fresh script above older stone cuts that were merely boxed in and renamed.", room_type="path")
    fg_hound_racks = area.room("fg_hound_racks", name="Hound Racks", desc="Leash posts, horn pegs, and brushed kennels wait under striped canvas for hunts that begin with paperwork long before blood.", room_type="clearing")
    fg_keeper_steps = area.room("fg_keeper_steps", name="Keeper Steps", desc="Broad stone steps climb beside a retaining wall engraved with permit classes, guest privileges, and fines for unlicensed taking.", room_type="path")
    fg_tally_green = area.room("fg_tally_green", name="Tally Green", desc="This tidy green gives visiting stewards room to sort mounts, servants, and game tags without dirtying noble boots.", room_type="clearing")
    fg_guest_shed = area.room("fg_guest_shed", name="Guest Shed", desc="A trimmed timber shed stores spare cloaks, folding blinds, and lacquered cases for parties dressed more for display than weather.", room_type="building", indoor=True)
    fg_servant_lane = area.room("fg_servant_lane", name="Servants' Lane", desc="A narrower lane skirts the formal approach, carrying tack, cooking gear, and the labor that makes leisure seem effortless.", room_type="path")
    fg_quarry_marker = area.room("fg_quarry_marker", name="Quarry Marker", desc="An old milestone reused as a boundary stone still carries deeper numbering beneath the preserve's elegant antler seal.", room_type="path")
    fg_outer_paddock = area.room("fg_outer_paddock", name="Outer Paddock", desc="Leased horses crop clipped grass behind a low rail while grooms exchange gossip about who is allowed through today.", room_type="clearing")
    fg_horn_post = area.room("fg_horn_post", name="Horn Post", desc="A weather-dark post bears polished hunting horns whose calls organize privilege into neat departures and returns.", room_type="path")
    fg_ranger_turn = area.room("fg_ranger_turn", name="Ranger Turn", desc="The formal road bends here toward keeper trails, and the brush begins to press close enough to hide what the gate pretends to regulate.", room_type="path")
    fg_reed_verge = area.room("fg_reed_verge", name="Reed Verge", desc="A damp verge of reeds and flattened sedge catches dropped wax, split tags, and the quiet refuse of preserve administration.", room_type="clearing")
    fg_courtesy_stall = area.room("fg_courtesy_stall", name="Courtesy Stall", desc="A small awning offers watered wine, clean gloves, and the kind of assistance that is really another inspection.", room_type="building")
    fg_old_boundary = area.room("fg_old_boundary", name="Old Boundary", desc="Beneath the new charter post, older stone sockets mark a line that belonged to witness and custom long before noble enclosure.", room_type="ruins")
    fg_groom_yard = area.room("fg_groom_yard", name="Groom Yard", desc="Brush racks, curry combs, and lather troughs fill a yard where the animals look better rested than many of the staff.", room_type="clearing")
    fg_trail_split = area.room("fg_trail_split", name="Trail Split", desc="Formal gravel narrows into keeper tracks here, one route tending the managed runs and another circling toward the lodge.", room_type="path")

    # ==================================================================
    #  MANAGED GAME TRAILS
    # ==================================================================
    mt_trail_split = area.room("mt_trail_split", name="Trail Split", desc="Markers divide the preserve into managed runs, with color-coded tags sending paying hunters one way and working keepers another.", room_type="path")
    mt_marker_oak = area.room("mt_marker_oak", name="Marker Oak", desc="An old oak holds iron route plaques nailed over earlier cuts, the bark slowly swallowing the newer law.", room_type="path")
    mt_feed_scatter = area.room("mt_feed_scatter", name="Feed Scatter", desc="Grain, salt, and bruised apples have been cast across this shallow run to keep deer moving where noble bows can predict them.", room_type="clearing")
    mt_north_run = area.room("mt_north_run", name="North Run", desc="Packed hoofprints and boot marks show how often the game is turned through this straightened strip of wood.", room_type="path")
    mt_hind_path = area.room("mt_hind_path", name="Hind Path", desc="A softer trail slips beneath alder and thorn where smaller deer and patient trackers move with equal care.", room_type="path")
    mt_salt_lick = area.room("mt_salt_lick", name="Salt Lick", desc="A block of mineral salt sits beside a tally stake marked with guest initials and yesterday's observed herd counts.", room_type="clearing")
    mt_hound_cut = area.room("mt_hound_cut", name="Hound Cut", desc="The brush has been clipped into a narrow chase lane meant to give hounds speed and anything hunted through it less choice.", room_type="path")
    mt_low_hide = area.room("mt_low_hide", name="Low Hide", desc="A half-buried blind looks out across a lane of deliberate browse, more shooting gallery than wilderness.", room_type="building", indoor=True)
    mt_briar_turn = area.room("mt_briar_turn", name="Briar Turn", desc="The trail kinks through briar where keepers let the cover grow thick enough to make a clean shot feel earned.", room_type="path")
    mt_game_bridge = area.room("mt_game_bridge", name="Game Bridge", desc="A stout timber bridge spans a gully crossed more often by driven animals than by comfortable guests.", room_type="path")
    mt_track_bowl = area.room("mt_track_bowl", name="Track Bowl", desc="Mud and leaf litter collect in a shallow bowl where prints layer over one another like repeated entries in a hunting ledger.", room_type="clearing")
    mt_keeper_ladder = area.room("mt_keeper_ladder", name="Keeper Ladder", desc="A laddered stand rises above the run so rangers can watch the drives, the camps, and the guests all at once.", room_type="building")
    mt_broken_blind = area.room("mt_broken_blind", name="Broken Blind", desc="One blind has been smashed from within, its lacquered rail gouged by antler and hurried boot heels alike.", room_type="ruins")
    mt_hunter_loop = area.room("mt_hunter_loop", name="Hunter Loop", desc="The path curves through planted brush and staggered sightlines, turning pursuit into a carefully arranged leisure.", room_type="path")
    mt_fallen_post = area.room("mt_fallen_post", name="Fallen Post", desc="A snapped boundary post lies mossy at the trail edge, exposing an older socket beneath the newer peg.", room_type="path")
    mt_shed_bank = area.room("mt_shed_bank", name="Shed Bank", desc="A low bank hides a toolshed sunk into the slope where seed sacks, scent cloths, and spare nets are kept from public view.", room_type="building", indoor=True)
    mt_red_clay_run = area.room("mt_red_clay_run", name="Red Clay Run", desc="Hooves have churned the clay into a red slick where the managed trail dips toward water and less controlled ground.", room_type="path")
    mt_outer_track = area.room("mt_outer_track", name="Outer Track", desc="This outer run receives fewer guests and more honest weather, though tally stakes still measure it like a private corridor.", room_type="path")
    mt_wind_lane = area.room("mt_wind_lane", name="Wind Lane", desc="A breezy strip between pines carries scent cleanly, making it prized by trackers and resented by those who prefer easy drives.", room_type="path")
    mt_deer_wall = area.room("mt_deer_wall", name="Deer Wall", desc="A waist-high stone wall guides the herds around a bend that conveniently lines up with several noble stations.", room_type="ruins")
    mt_far_walk = area.room("mt_far_walk", name="Far Walk", desc="The managed trail grows quieter here, the polish of the gate giving way to leaf mold, water smell, and the patience of watchful ground.", room_type="path")
    mt_rut_hollow = area.room("mt_rut_hollow", name="Rut Hollow", desc="The hollow is scored by rut trenches and bark scars where stags have been harried through season after season.", room_type="clearing")
    mt_charter_stone = area.room("mt_charter_stone", name="Charter Stone", desc="A smooth standing stone quotes the preserve revision in legal language that never admits the woods were shared before they were licensed.", room_type="path")
    mt_lodge_approach = area.room("mt_lodge_approach", name="Lodge Approach", desc="Flags, smoke, and clipped hedges ahead announce the lodge grounds long before the first roof comes into view.", room_type="path")

    # ==================================================================
    #  LODGE GROUNDS AND NOBLE CAMPS
    # ==================================================================
    lg_lodge_approach = area.room("lg_lodge_approach", name="Lodge Approach", desc="The managed trail opens onto trimmed ground where servants erase mud before guests can track it indoors.", room_type="path")
    lg_hunt_lawn = area.room("lg_hunt_lawn", name="Hunt Lawn", desc="A broad lawn holds mounting blocks, parasols, and the quiet theater of nobles pretending the day's kill will be chance.", room_type="clearing")
    lg_trophy_portico = area.room("lg_trophy_portico", name="Trophy Portico", desc="Antlers, polished plaques, and old horn mounts decorate the lodge front, each kill rendered cleaner in display than it was in the field.", room_type="building")
    lg_keeper_store = area.room("lg_keeper_store", name="Keeper Store", desc="Shelves of salt, tallow, rope, and field tags reveal the preserve as a working machine beneath the velvet.", room_type="building", indoor=True)
    lg_quartermaster_tent = area.room("lg_quartermaster_tent", name="Quartermaster Tent", desc="Canvas walls snap over crates of rations, bait, hooks, and tools sold at polite markup to anyone allowed near them.", room_type="building", indoor=True)
    lg_guest_pavilions = area.room("lg_guest_pavilions", name="Guest Pavilions", desc="Striped pavilions shelter camp chairs, wine cases, and the sort of comforts that make the woods feel owned.", room_type="building")
    lg_steward_hall = area.room("lg_steward_hall", name="Steward Hall", desc="Ledgers, invitation rolls, and disputed privilege forms crowd a hall where leisure is balanced by signature and seal.", room_type="building", indoor=True)
    lg_licensed_fire = area.room("lg_licensed_fire", name="Licensed Fire", desc="A ring of dressed stone keeps a sanctioned campfire burning for approved parties and pointedly no one else.", room_type="clearing")
    lg_meat_shed = area.room("lg_meat_shed", name="Meat Shed", desc="Hooks, salt bins, and clean blocks line a shed where lawful harvest is weighed, stamped, and separated from what will go missing.", room_type="building", indoor=True)
    lg_pantry_yard = area.room("lg_pantry_yard", name="Pantry Yard", desc="Kitchen boys and field hands hurry between casks, produce baskets, and cold boxes under the eye of a steward's bell.", room_type="clearing")
    lg_hound_meadow = area.room("lg_hound_meadow", name="Hound Meadow", desc="A fenced meadow gives kennel hounds room to stretch, snarl, and practice the chase before guests arrive.", room_type="clearing")
    lg_wash_line = area.room("lg_wash_line", name="Wash Line", desc="Aprons, game cloths, and bloody towels snap on a line behind the lodge where the preserve's cleaner fictions are laundered.", room_type="clearing")
    lg_ledger_desk = area.room("lg_ledger_desk", name="Ledger Desk", desc="An outdoor desk beneath an awning handles licenses, camp tallies, and quiet amendments that never seem to reach the city copy.", room_type="building")
    lg_hidden_postern = area.room("lg_hidden_postern", name="Hidden Postern", desc="A stone postern behind stacked feed crates drops toward a keeper path the formal maps omit on purpose.", room_type="building", indoor=True)
    lg_noble_veranda = area.room("lg_noble_veranda", name="Noble Veranda", desc="From this shaded veranda the hunt can be watched at a distance gentle enough to feel refined.", room_type="building")
    lg_lake_walk = area.room("lg_lake_walk", name="Lake Walk", desc="A flagged walk curves away from the lodge toward the reservoir edge, ornamental near the lawn and practical farther on.", room_type="path")
    lg_camp_edge = area.room("lg_camp_edge", name="Camp Edge", desc="The clipped grounds fray into rough grass and tarped supply pits where staff, not guests, spend the night.", room_type="clearing")
    lg_outer_kennel = area.room("lg_outer_kennel", name="Outer Kennel", desc="Wire runs and low stone pens hold the less presentable dogs out of sight until violence is required.", room_type="building", indoor=True)

    # ==================================================================
    #  POACHER BLINDS AND HIDDEN MEAT LINES
    # ==================================================================
    pb_camp_edge = area.room("pb_camp_edge", name="Camp Edge", desc="A ragged trace branches off the service camps toward scrub where legal hunts become stories and stories become cover.", room_type="path")
    pb_torn_fence = area.room("pb_torn_fence", name="Torn Fence", desc="Sections of noble fence have been cut and retied here often enough to make damage part of the route.", room_type="path")
    pb_snare_run = area.room("pb_snare_run", name="Snare Run", desc="Fine wire loops hide among fern and thorn where poachers take what the charter claims to regulate.", room_type="path")
    pb_smoke_hollow = area.room("pb_smoke_hollow", name="Smoke Hollow", desc="Low smoke clings to this hollow from cooking fires kept small enough to deny but hot enough to cure meat.", room_type="clearing")
    pb_net_stand = area.room("pb_net_stand", name="Net Stand", desc="Hooks in the trees hold folded nets for flushing birds and tangling panicked deer in one ugly motion.", room_type="clearing")
    pb_hook_tree = area.room("pb_hook_tree", name="Hook Tree", desc="Iron meat hooks hang from a leaning tree above churned earth and old blood worked deep into the roots.", room_type="ruins")
    pb_blood_fern = area.room("pb_blood_fern", name="Blood Fern", desc="Red-stained ferns crowd a damp patch where carcasses are dressed faster than any lawful tally can follow.", room_type="clearing")
    pb_sunken_blind = area.room("pb_sunken_blind", name="Sunken Blind", desc="A dug-in blind roofed with brush looks toward the managed runs through slits cut for illegal certainty.", room_type="building", indoor=True)
    pb_hidden_rill = area.room("pb_hidden_rill", name="Hidden Rill", desc="Cold water threads through reeds here, washing scent, blood, and boot prints toward the lake.", room_type="clearing")
    pb_meat_line = area.room("pb_meat_line", name="Meat Line", desc="A line of pegged cords lets carcasses hang beneath burlap where they can be sorted into tribute, sale, or silence.", room_type="clearing")
    pb_ash_cover = area.room("pb_ash_cover", name="Ash Cover", desc="Cold ash has been scattered over the ground to mute tracks and keep the camps looking older than they are.", room_type="path")
    pb_watch_perch = area.room("pb_watch_perch", name="Watch Perch", desc="A rough platform overlooks both lodge service lanes and the game trails, proving the poachers know the preserve's rhythms intimately.", room_type="building")
    pb_dead_drop = area.room("pb_dead_drop", name="Dead Drop", desc="A hollow stump hides wrapped notes, copied licenses, and coin packets that move without admitting to trade.", room_type="clearing")
    pb_mud_hush = area.room("pb_mud_hush", name="Mud Hush", desc="Black mud swallows footsteps along this low strip, making it the safest path for anything that should not be seen leaving.", room_type="path")
    pb_poacher_den = area.room("pb_poacher_den", name="Poacher Den", desc="Canvas, stolen lanterns, drying hides, and a table of forged tags turn this dugout into the preserve's ugliest mirror.", room_type="building", indoor=True)
    pb_bone_ditch = area.room("pb_bone_ditch", name="Bone Ditch", desc="A shallow ditch choked with cracked rib, antler offcuts, and fish spine proves how much of the preserve dies off the ledger.", room_type="ruins")
    pb_wired_pass = area.room("pb_wired_pass", name="Wired Pass", desc="Trip wires and bent bells protect this narrow pass between thorn thickets and stacked hides.", room_type="path")
    pb_cold_rack = area.room("pb_cold_rack", name="Cold Rack", desc="A shaded rack of netting and wet cloth keeps choice cuts cool until a buyer from the city can fetch them.", room_type="clearing")
    pb_lake_cut = area.room("pb_lake_cut", name="Lake Cut", desc="The poacher trail drops toward the reservoir through willow and trampled sedge, carrying blood to cleaner water.", room_type="path")
    pb_stone_cut = area.room("pb_stone_cut", name="Stone Cut", desc="A stony break through the woods leads toward older ring stones where preserve law grows thin and older witness survives.", room_type="path")

    # ==================================================================
    #  LAKE BASIN / RESERVOIR EDGE
    # ==================================================================
    lb_lake_walk = area.room("lb_lake_walk", name="Lake Walk", desc="The lodge path reaches the reservoir in a sweep of gravel and reed beds arranged to look natural from a noble distance.", room_type="path")
    lb_reed_bank = area.room("lb_reed_bank", name="Reed Bank", desc="Tall reeds hiss in the wind along a bank stitched with boot cuts, bait scraps, and half-sunk tally pegs.", room_type="clearing")
    lb_tally_dock = area.room("lb_tally_dock", name="Tally Dock", desc="A small dock holds weighing boards for fish, reed bundles, and whatever else the steward decides to count today.", room_type="path")
    lb_fishing_steps = area.room("lb_fishing_steps", name="Fishing Steps", desc="Worn stone steps descend to quiet water where even approved leisure still smells like bait and silt.", room_type="path")
    lb_boathouse = area.room("lb_boathouse", name="Boathouse", desc="Flat skiffs, pole racks, and a locked chest of nets fill a boathouse reserved for licensed guests and their staff.", room_type="building", indoor=True)
    lb_silt_curve = area.room("lb_silt_curve", name="Silt Curve", desc="The bank curves through soft silt where water birds, fishers, and poachers all leave different stories in the same mud.", room_type="clearing")
    lb_reservoir_mark = area.room("lb_reservoir_mark", name="Reservoir Mark", desc="A carved post tracks the lake's level against dates of charter revision, drought, and improvement.", room_type="path")
    lb_wet_meadow = area.room("lb_wet_meadow", name="Wet Meadow", desc="Rushes, insect song, and bright marsh flowers soften the ground here until each step becomes a measured choice.", room_type="clearing")
    lb_narrow_cove = area.room("lb_narrow_cove", name="Narrow Cove", desc="The water pinches into a cove shadowed by willow roots and the quiet patience of fish below them.", room_type="clearing")
    lb_ripple_shelf = area.room("lb_ripple_shelf", name="Ripple Shelf", desc="Flat stone shelves just above the water make an easy casting perch and an even easier place to overhear confidential talk.", room_type="path")
    lb_keeper_weir = area.room("lb_keeper_weir", name="Keeper Weir", desc="A low timber weir turns water and fish alike according to keeper preference rather than the lake's own habit.", room_type="path")
    lb_weed_bar = area.room("lb_weed_bar", name="Weed Bar", desc="A bar of thick silverweed and drifting pollen marks the shallowest part of the basin.", room_type="clearing")
    lb_south_bank = area.room("lb_south_bank", name="South Bank", desc="The southern bank is less ornamental and more honest, lined with repair stakes, coiled rope, and damp boot marks.", room_type="path")
    lb_hidden_cove = area.room("lb_hidden_cove", name="Hidden Cove", desc="Brush and leaning stone hide a cove used for private casts, quiet exchanges, and departures nobody wants noticed.", room_type="clearing")
    lb_noble_jetty = area.room("lb_noble_jetty", name="Noble Jetty", desc="A narrow jetty reaches into deeper water where guests can fish without ever standing in mud.", room_type="path")
    lb_mist_bank = area.room("lb_mist_bank", name="Mist Bank", desc="Morning mist lingers between reeds and old posts here long after the sun has brightened the lodge lawns.", room_type="clearing")
    lb_charter_spill = area.room("lb_charter_spill", name="Charter Spill", desc="A retaining wall has slumped just enough to expose older dressed stone beneath the reservoir's later charter facing.", room_type="ruins")
    lb_stone_rim = area.room("lb_stone_rim", name="Stone Rim", desc="The basin ends at a rocky rim where the water gives way to root, lichen, and the first standing stones of the woods.", room_type="path")

    # ==================================================================
    #  STONE-CIRCLE WOODS
    # ==================================================================
    sw_stone_cut = area.room("sw_stone_cut", name="Stone Cut", desc="The poacher and lake paths meet at a cut between old standing stones whose older faces were never fully erased.", room_type="path")
    sw_outer_circle = area.room("sw_outer_circle", name="Outer Circle", desc="Weathered uprights form the first ring under pine and ash, their bases older than the preserve's gentler lies.", room_type="clearing")
    sw_ring_path = area.room("sw_ring_path", name="Ring Path", desc="A leaf-soft path curves along the outer stones where pilgrims once walked and keepers now pretend only hunters belong.", room_type="path")
    sw_carved_oak = area.room("sw_carved_oak", name="Carved Oak", desc="An oak at the ring edge carries witness cuts beneath newer antler marks and polite hunting blessings.", room_type="path")
    sw_witness_stone = area.room("sw_witness_stone", name="Witness Stone", desc="One tall stone bears layered rubbings, chalk notes, and the stubborn memory of boundaries that used to require consent.", room_type="ruins")
    sw_ash_fork = area.room("sw_ash_fork", name="Ash Fork", desc="Twin ash trunks divide the woods into a quiet pilgrim line and a rougher hunter's shortcut.", room_type="path")
    sw_old_altar = area.room("sw_old_altar", name="Old Altar", desc="A flat altar stone survives under moss, its older channels still aligned for offering rather than trophy display.", room_type="ruins")
    sw_fern_pocket = area.room("sw_fern_pocket", name="Fern Pocket", desc="A cool pocket of fern and shade muffles the woods enough to make every snapped twig feel witnessed.", room_type="clearing")
    sw_hart_run = area.room("sw_hart_run", name="Hart Run", desc="Deep slots in the earth show where driven stags have taken the same desperate line again and again.", room_type="path")
    sw_watch_stump = area.room("sw_watch_stump", name="Watch Stump", desc="A broad cut stump offers a view over ring stone, run, and the far shimmer of the lake.", room_type="clearing")
    sw_inner_ring = area.room("sw_inner_ring", name="Inner Ring", desc="The inner stones stand closer together, their tops chipped where later survey marks were hammered in.", room_type="clearing")
    sw_charter_marker = area.room("sw_charter_marker", name="Charter Marker", desc="A freestanding marker claims the woods were regularized by preserve law, but its footing plainly reuses an older socket.", room_type="path")
    sw_rootshelf = area.room("sw_rootshelf", name="Root Shelf", desc="Thick roots and stone ledges make this shelf difficult going, as if the grove itself resists straightening.", room_type="path")
    sw_prayer_break = area.room("sw_prayer_break", name="Prayer Break", desc="Reed ties, wax crumbs, and hushed footprints gather in a niche the official maps call only a rest point.", room_type="clearing")
    sw_north_spinney = area.room("sw_north_spinney", name="North Spinney", desc="The pine close grows dark and close-set here, hiding both frightened game and people who do not wish to be counted.", room_type="path")
    sw_hollow_ring = area.room("sw_hollow_ring", name="Hollow Ring", desc="A partial circle of half-sunk stones surrounds a shallow hollow where sound returns strangely even in calm air.", room_type="clearing")
    sw_hidden_spring = area.room("sw_hidden_spring", name="Hidden Spring", desc="Cold water seeps from under one tilted stone into a basin kept clean by careful, secret hands.", room_type="clearing")
    sw_ranger_stand = area.room("sw_ranger_stand", name="Ranger Stand", desc="A weathered stand lets keepers watch the heartward trails and the illicit routes that feed them.", room_type="building")
    sw_far_marker = area.room("sw_far_marker", name="Far Marker", desc="The farthest marker bears both House Rhest antlers and older witness notches cut too deep to plane away.", room_type="path")
    sw_heart_glade = area.room("sw_heart_glade", name="Heart Glade", desc="A quiet glade ringed by stone and torn bark holds the preserve's most dangerous beauty, where the greatest hart has been driven too many seasons.", room_type="clearing")

    # ==================================================================
    #  EXITS
    # ==================================================================
    area.exit(fg_charter_gate, "varath_prime:nh_preserve_gate", "south")
    area.exit(fg_charter_gate, fg_brass_check, "north")
    area.exit(fg_brass_check, fg_charter_gate, "south")
    area.exit(fg_brass_check, fg_entry_lawn, "north")
    area.exit(fg_entry_lawn, fg_brass_check, "south")
    area.exit(fg_entry_lawn, fg_writ_arch, "north")
    area.exit(fg_writ_arch, fg_entry_lawn, "south")
    area.exit(fg_writ_arch, fg_hound_racks, "north")
    area.exit(fg_hound_racks, fg_writ_arch, "south")
    area.exit(fg_hound_racks, fg_keeper_steps, "north")
    area.exit(fg_keeper_steps, fg_hound_racks, "south")
    area.exit(fg_keeper_steps, fg_tally_green, "north")
    area.exit(fg_tally_green, fg_keeper_steps, "south")
    area.exit(fg_tally_green, fg_guest_shed, "north")
    area.exit(fg_guest_shed, fg_tally_green, "south")
    area.exit(fg_guest_shed, fg_servant_lane, "north")
    area.exit(fg_servant_lane, fg_guest_shed, "south")
    area.exit(fg_servant_lane, fg_quarry_marker, "north")
    area.exit(fg_quarry_marker, fg_servant_lane, "south")
    area.exit(fg_quarry_marker, fg_outer_paddock, "north")
    area.exit(fg_outer_paddock, fg_quarry_marker, "south")
    area.exit(fg_outer_paddock, fg_horn_post, "north")
    area.exit(fg_horn_post, fg_outer_paddock, "south")
    area.exit(fg_horn_post, fg_ranger_turn, "north")
    area.exit(fg_ranger_turn, fg_horn_post, "south")
    area.exit(fg_ranger_turn, fg_reed_verge, "north")
    area.exit(fg_reed_verge, fg_ranger_turn, "south")
    area.exit(fg_reed_verge, fg_courtesy_stall, "north")
    area.exit(fg_courtesy_stall, fg_reed_verge, "south")
    area.exit(fg_courtesy_stall, fg_old_boundary, "north")
    area.exit(fg_old_boundary, fg_courtesy_stall, "south")
    area.exit(fg_old_boundary, fg_groom_yard, "north")
    area.exit(fg_groom_yard, fg_old_boundary, "south")
    area.exit(fg_groom_yard, fg_trail_split, "north")
    area.exit(fg_trail_split, fg_groom_yard, "south")

    area.exit(mt_trail_split, mt_marker_oak, "east")
    area.exit(mt_marker_oak, mt_trail_split, "west")
    area.exit(mt_marker_oak, mt_feed_scatter, "east")
    area.exit(mt_feed_scatter, mt_marker_oak, "west")
    area.exit(mt_feed_scatter, mt_north_run, "east")
    area.exit(mt_north_run, mt_feed_scatter, "west")
    area.exit(mt_north_run, mt_hind_path, "east")
    area.exit(mt_hind_path, mt_north_run, "west")
    area.exit(mt_hind_path, mt_salt_lick, "east")
    area.exit(mt_salt_lick, mt_hind_path, "west")
    area.exit(mt_salt_lick, mt_hound_cut, "east")
    area.exit(mt_hound_cut, mt_salt_lick, "west")
    area.exit(mt_hound_cut, mt_low_hide, "east")
    area.exit(mt_low_hide, mt_hound_cut, "west")
    area.exit(mt_low_hide, mt_briar_turn, "east")
    area.exit(mt_briar_turn, mt_low_hide, "west")
    area.exit(mt_briar_turn, mt_game_bridge, "east")
    area.exit(mt_game_bridge, mt_briar_turn, "west")
    area.exit(mt_game_bridge, mt_track_bowl, "east")
    area.exit(mt_track_bowl, mt_game_bridge, "west")
    area.exit(mt_track_bowl, mt_keeper_ladder, "east")
    area.exit(mt_keeper_ladder, mt_track_bowl, "west")
    area.exit(mt_keeper_ladder, mt_broken_blind, "east")
    area.exit(mt_broken_blind, mt_keeper_ladder, "west")
    area.exit(mt_broken_blind, mt_hunter_loop, "east")
    area.exit(mt_hunter_loop, mt_broken_blind, "west")
    area.exit(mt_hunter_loop, mt_fallen_post, "east")
    area.exit(mt_fallen_post, mt_hunter_loop, "west")
    area.exit(mt_fallen_post, mt_shed_bank, "east")
    area.exit(mt_shed_bank, mt_fallen_post, "west")
    area.exit(mt_shed_bank, mt_red_clay_run, "east")
    area.exit(mt_red_clay_run, mt_shed_bank, "west")
    area.exit(mt_red_clay_run, mt_outer_track, "east")
    area.exit(mt_outer_track, mt_red_clay_run, "west")
    area.exit(mt_outer_track, mt_wind_lane, "east")
    area.exit(mt_wind_lane, mt_outer_track, "west")
    area.exit(mt_wind_lane, mt_deer_wall, "east")
    area.exit(mt_deer_wall, mt_wind_lane, "west")
    area.exit(mt_deer_wall, mt_far_walk, "east")
    area.exit(mt_far_walk, mt_deer_wall, "west")
    area.exit(mt_far_walk, mt_rut_hollow, "east")
    area.exit(mt_rut_hollow, mt_far_walk, "west")
    area.exit(mt_rut_hollow, mt_charter_stone, "east")
    area.exit(mt_charter_stone, mt_rut_hollow, "west")
    area.exit(mt_charter_stone, mt_lodge_approach, "east")
    area.exit(mt_lodge_approach, mt_charter_stone, "west")

    area.exit(lg_lodge_approach, lg_hunt_lawn, "east")
    area.exit(lg_hunt_lawn, lg_lodge_approach, "west")
    area.exit(lg_hunt_lawn, lg_trophy_portico, "east")
    area.exit(lg_trophy_portico, lg_hunt_lawn, "west")
    area.exit(lg_trophy_portico, lg_keeper_store, "east")
    area.exit(lg_keeper_store, lg_trophy_portico, "west")
    area.exit(lg_keeper_store, lg_quartermaster_tent, "east")
    area.exit(lg_quartermaster_tent, lg_keeper_store, "west")
    area.exit(lg_quartermaster_tent, lg_guest_pavilions, "east")
    area.exit(lg_guest_pavilions, lg_quartermaster_tent, "west")
    area.exit(lg_guest_pavilions, lg_steward_hall, "east")
    area.exit(lg_steward_hall, lg_guest_pavilions, "west")
    area.exit(lg_steward_hall, lg_licensed_fire, "east")
    area.exit(lg_licensed_fire, lg_steward_hall, "west")
    area.exit(lg_licensed_fire, lg_meat_shed, "east")
    area.exit(lg_meat_shed, lg_licensed_fire, "west")
    area.exit(lg_meat_shed, lg_pantry_yard, "east")
    area.exit(lg_pantry_yard, lg_meat_shed, "west")
    area.exit(lg_pantry_yard, lg_hound_meadow, "east")
    area.exit(lg_hound_meadow, lg_pantry_yard, "west")
    area.exit(lg_hound_meadow, lg_wash_line, "east")
    area.exit(lg_wash_line, lg_hound_meadow, "west")
    area.exit(lg_wash_line, lg_ledger_desk, "east")
    area.exit(lg_ledger_desk, lg_wash_line, "west")
    area.exit(lg_ledger_desk, lg_hidden_postern, "east")
    area.exit(lg_hidden_postern, lg_ledger_desk, "west")
    area.exit(lg_hidden_postern, lg_noble_veranda, "east")
    area.exit(lg_noble_veranda, lg_hidden_postern, "west")
    area.exit(lg_noble_veranda, lg_lake_walk, "east")
    area.exit(lg_lake_walk, lg_noble_veranda, "west")
    area.exit(lg_lake_walk, lg_camp_edge, "east")
    area.exit(lg_camp_edge, lg_lake_walk, "west")
    area.exit(lg_camp_edge, lg_outer_kennel, "east")
    area.exit(lg_outer_kennel, lg_camp_edge, "west")

    area.exit(pb_camp_edge, pb_torn_fence, "north")
    area.exit(pb_torn_fence, pb_camp_edge, "south")
    area.exit(pb_torn_fence, pb_snare_run, "north")
    area.exit(pb_snare_run, pb_torn_fence, "south")
    area.exit(pb_snare_run, pb_smoke_hollow, "north")
    area.exit(pb_smoke_hollow, pb_snare_run, "south")
    area.exit(pb_smoke_hollow, pb_net_stand, "north")
    area.exit(pb_net_stand, pb_smoke_hollow, "south")
    area.exit(pb_net_stand, pb_hook_tree, "north")
    area.exit(pb_hook_tree, pb_net_stand, "south")
    area.exit(pb_hook_tree, pb_blood_fern, "north")
    area.exit(pb_blood_fern, pb_hook_tree, "south")
    area.exit(pb_blood_fern, pb_sunken_blind, "north")
    area.exit(pb_sunken_blind, pb_blood_fern, "south")
    area.exit(pb_sunken_blind, pb_hidden_rill, "north")
    area.exit(pb_hidden_rill, pb_sunken_blind, "south")
    area.exit(pb_hidden_rill, pb_meat_line, "north")
    area.exit(pb_meat_line, pb_hidden_rill, "south")
    area.exit(pb_meat_line, pb_ash_cover, "north")
    area.exit(pb_ash_cover, pb_meat_line, "south")
    area.exit(pb_ash_cover, pb_watch_perch, "north")
    area.exit(pb_watch_perch, pb_ash_cover, "south")
    area.exit(pb_watch_perch, pb_dead_drop, "north")
    area.exit(pb_dead_drop, pb_watch_perch, "south")
    area.exit(pb_dead_drop, pb_mud_hush, "north")
    area.exit(pb_mud_hush, pb_dead_drop, "south")
    area.exit(pb_mud_hush, pb_poacher_den, "north")
    area.exit(pb_poacher_den, pb_mud_hush, "south")
    area.exit(pb_poacher_den, pb_bone_ditch, "north")
    area.exit(pb_bone_ditch, pb_poacher_den, "south")
    area.exit(pb_bone_ditch, pb_wired_pass, "north")
    area.exit(pb_wired_pass, pb_bone_ditch, "south")
    area.exit(pb_wired_pass, pb_cold_rack, "north")
    area.exit(pb_cold_rack, pb_wired_pass, "south")
    area.exit(pb_cold_rack, pb_lake_cut, "north")
    area.exit(pb_lake_cut, pb_cold_rack, "south")
    area.exit(pb_lake_cut, pb_stone_cut, "north")
    area.exit(pb_stone_cut, pb_lake_cut, "south")

    area.exit(lb_lake_walk, lb_reed_bank, "north")
    area.exit(lb_reed_bank, lb_lake_walk, "south")
    area.exit(lb_reed_bank, lb_tally_dock, "north")
    area.exit(lb_tally_dock, lb_reed_bank, "south")
    area.exit(lb_tally_dock, lb_fishing_steps, "north")
    area.exit(lb_fishing_steps, lb_tally_dock, "south")
    area.exit(lb_fishing_steps, lb_boathouse, "north")
    area.exit(lb_boathouse, lb_fishing_steps, "south")
    area.exit(lb_boathouse, lb_silt_curve, "north")
    area.exit(lb_silt_curve, lb_boathouse, "south")
    area.exit(lb_silt_curve, lb_reservoir_mark, "north")
    area.exit(lb_reservoir_mark, lb_silt_curve, "south")
    area.exit(lb_reservoir_mark, lb_wet_meadow, "north")
    area.exit(lb_wet_meadow, lb_reservoir_mark, "south")
    area.exit(lb_wet_meadow, lb_narrow_cove, "north")
    area.exit(lb_narrow_cove, lb_wet_meadow, "south")
    area.exit(lb_narrow_cove, lb_ripple_shelf, "north")
    area.exit(lb_ripple_shelf, lb_narrow_cove, "south")
    area.exit(lb_ripple_shelf, lb_keeper_weir, "north")
    area.exit(lb_keeper_weir, lb_ripple_shelf, "south")
    area.exit(lb_keeper_weir, lb_weed_bar, "north")
    area.exit(lb_weed_bar, lb_keeper_weir, "south")
    area.exit(lb_weed_bar, lb_south_bank, "north")
    area.exit(lb_south_bank, lb_weed_bar, "south")
    area.exit(lb_south_bank, lb_hidden_cove, "north")
    area.exit(lb_hidden_cove, lb_south_bank, "south")
    area.exit(lb_hidden_cove, lb_noble_jetty, "north")
    area.exit(lb_noble_jetty, lb_hidden_cove, "south")
    area.exit(lb_noble_jetty, lb_mist_bank, "north")
    area.exit(lb_mist_bank, lb_noble_jetty, "south")
    area.exit(lb_mist_bank, lb_charter_spill, "north")
    area.exit(lb_charter_spill, lb_mist_bank, "south")
    area.exit(lb_charter_spill, lb_stone_rim, "north")
    area.exit(lb_stone_rim, lb_charter_spill, "south")

    area.exit(sw_stone_cut, sw_outer_circle, "east")
    area.exit(sw_outer_circle, sw_stone_cut, "west")
    area.exit(sw_outer_circle, sw_ring_path, "east")
    area.exit(sw_ring_path, sw_outer_circle, "west")
    area.exit(sw_ring_path, sw_carved_oak, "east")
    area.exit(sw_carved_oak, sw_ring_path, "west")
    area.exit(sw_carved_oak, sw_witness_stone, "east")
    area.exit(sw_witness_stone, sw_carved_oak, "west")
    area.exit(sw_witness_stone, sw_ash_fork, "east")
    area.exit(sw_ash_fork, sw_witness_stone, "west")
    area.exit(sw_ash_fork, sw_old_altar, "east")
    area.exit(sw_old_altar, sw_ash_fork, "west")
    area.exit(sw_old_altar, sw_fern_pocket, "east")
    area.exit(sw_fern_pocket, sw_old_altar, "west")
    area.exit(sw_fern_pocket, sw_hart_run, "east")
    area.exit(sw_hart_run, sw_fern_pocket, "west")
    area.exit(sw_hart_run, sw_watch_stump, "east")
    area.exit(sw_watch_stump, sw_hart_run, "west")
    area.exit(sw_watch_stump, sw_inner_ring, "east")
    area.exit(sw_inner_ring, sw_watch_stump, "west")
    area.exit(sw_inner_ring, sw_charter_marker, "east")
    area.exit(sw_charter_marker, sw_inner_ring, "west")
    area.exit(sw_charter_marker, sw_rootshelf, "east")
    area.exit(sw_rootshelf, sw_charter_marker, "west")
    area.exit(sw_rootshelf, sw_prayer_break, "east")
    area.exit(sw_prayer_break, sw_rootshelf, "west")
    area.exit(sw_prayer_break, sw_north_spinney, "east")
    area.exit(sw_north_spinney, sw_prayer_break, "west")
    area.exit(sw_north_spinney, sw_hollow_ring, "east")
    area.exit(sw_hollow_ring, sw_north_spinney, "west")
    area.exit(sw_hollow_ring, sw_hidden_spring, "east")
    area.exit(sw_hidden_spring, sw_hollow_ring, "west")
    area.exit(sw_hidden_spring, sw_ranger_stand, "east")
    area.exit(sw_ranger_stand, sw_hidden_spring, "west")
    area.exit(sw_ranger_stand, sw_far_marker, "east")
    area.exit(sw_far_marker, sw_ranger_stand, "west")
    area.exit(sw_far_marker, sw_heart_glade, "east")
    area.exit(sw_heart_glade, sw_far_marker, "west")

    area.exit(fg_trail_split, mt_trail_split, "north")
    area.exit(mt_trail_split, fg_trail_split, "south")
    area.exit(mt_lodge_approach, lg_lodge_approach, "east")
    area.exit(lg_lodge_approach, mt_lodge_approach, "west")
    area.exit(lg_lake_walk, lb_lake_walk, "north")
    area.exit(lb_lake_walk, lg_lake_walk, "south")
    area.exit(lg_camp_edge, pb_camp_edge, "north")
    area.exit(pb_camp_edge, lg_camp_edge, "south")
    area.exit(pb_stone_cut, sw_stone_cut, "east")
    area.exit(sw_stone_cut, pb_stone_cut, "west")
    area.exit(lb_stone_rim, sw_outer_circle, "northeast")
    area.exit(sw_outer_circle, lb_stone_rim, "southwest")

    area.exit(fg_keeper_steps, fg_servant_lane, "east")
    area.exit(fg_servant_lane, fg_keeper_steps, "west")
    area.exit(fg_tally_green, fg_courtesy_stall, "east")
    area.exit(fg_courtesy_stall, fg_tally_green, "west")
    area.exit(mt_hind_path, mt_low_hide, "south")
    area.exit(mt_low_hide, mt_hind_path, "north")
    area.exit(mt_briar_turn, mt_track_bowl, "north")
    area.exit(mt_track_bowl, mt_briar_turn, "south")
    area.exit(mt_broken_blind, mt_red_clay_run, "south")
    area.exit(mt_red_clay_run, mt_broken_blind, "north")
    area.exit(mt_outer_track, mt_rut_hollow, "north")
    area.exit(mt_rut_hollow, mt_outer_track, "south")
    area.exit(lg_keeper_store, lg_guest_pavilions, "south")
    area.exit(lg_guest_pavilions, lg_keeper_store, "north")
    area.exit(lg_steward_hall, lg_pantry_yard, "south")
    area.exit(lg_pantry_yard, lg_steward_hall, "north")
    area.exit(lg_licensed_fire, lg_wash_line, "north")
    area.exit(lg_wash_line, lg_licensed_fire, "south")
    area.exit(lg_noble_veranda, lg_outer_kennel, "south")
    area.exit(lg_outer_kennel, lg_noble_veranda, "north")
    area.exit(pb_snare_run, pb_hidden_rill, "east")
    area.exit(pb_hidden_rill, pb_snare_run, "west")
    area.exit(pb_smoke_hollow, pb_meat_line, "east")
    area.exit(pb_meat_line, pb_smoke_hollow, "west")
    area.exit(pb_blood_fern, pb_dead_drop, "east")
    area.exit(pb_dead_drop, pb_blood_fern, "west")
    area.exit(pb_sunken_blind, pb_watch_perch, "east")
    area.exit(pb_watch_perch, pb_sunken_blind, "west")
    area.exit(pb_poacher_den, pb_cold_rack, "east")
    area.exit(pb_cold_rack, pb_poacher_den, "west")
    area.exit(lb_tally_dock, lb_boathouse, "east")
    area.exit(lb_boathouse, lb_tally_dock, "west")
    area.exit(lb_fishing_steps, lb_narrow_cove, "east")
    area.exit(lb_narrow_cove, lb_fishing_steps, "west")
    area.exit(lb_silt_curve, lb_wet_meadow, "west")
    area.exit(lb_wet_meadow, lb_silt_curve, "east")
    area.exit(lb_keeper_weir, lb_hidden_cove, "east")
    area.exit(lb_hidden_cove, lb_keeper_weir, "west")
    area.exit(lb_noble_jetty, lb_charter_spill, "east")
    area.exit(lb_charter_spill, lb_noble_jetty, "west")
    area.exit(sw_ring_path, sw_witness_stone, "north")
    area.exit(sw_witness_stone, sw_ring_path, "south")
    area.exit(sw_ash_fork, sw_fern_pocket, "south")
    area.exit(sw_fern_pocket, sw_ash_fork, "north")
    area.exit(sw_hart_run, sw_inner_ring, "north")
    area.exit(sw_inner_ring, sw_hart_run, "south")
    area.exit(sw_charter_marker, sw_prayer_break, "south")
    area.exit(sw_prayer_break, sw_charter_marker, "north")
    area.exit(sw_hollow_ring, sw_ranger_stand, "north")
    area.exit(sw_ranger_stand, sw_hollow_ring, "south")
    area.exit(lg_hidden_postern, pb_snare_run, "down", hidden=True)
    area.exit(pb_snare_run, lg_hidden_postern, "up", hidden=True)
    area.exit(lb_hidden_cove, sw_hidden_spring, "down", hidden=True)
    area.exit(sw_hidden_spring, lb_hidden_cove, "up", hidden=True)

    # ==================================================================
    #  SPAWNS
    # ==================================================================
    area.spawn(fg_outer_paddock, "trophy_hound", count_min=1, count_max=1, respawn_minutes=24, respawn_variance=6)
    area.spawn(fg_reed_verge, "plains_viper", count_min=1, count_max=1, respawn_minutes=20, respawn_variance=5)
    area.spawn(mt_hound_cut, "wolf", count_min=1, count_max=2, respawn_minutes=24, respawn_variance=6)
    area.spawn(mt_low_hide, "poacher_trapper", count_min=0, count_max=1, respawn_minutes=26, respawn_variance=7)
    area.spawn(mt_broken_blind, "wild_boar", count_min=1, count_max=1, respawn_minutes=26, respawn_variance=7)
    area.spawn(mt_rut_hollow, "trophy_hound", count_min=1, count_max=1, respawn_minutes=24, respawn_variance=6)
    area.spawn(lg_outer_kennel, "trophy_hound", count_min=1, count_max=1, respawn_minutes=25, respawn_variance=6)
    area.spawn(lg_camp_edge, "poacher_trapper", count_min=0, count_max=1, respawn_minutes=27, respawn_variance=7)
    area.spawn(pb_snare_run, "poacher_trapper", count_min=1, count_max=1, respawn_minutes=25, respawn_variance=6)
    area.spawn(pb_blood_fern, "wild_boar", count_min=1, count_max=1, respawn_minutes=26, respawn_variance=7)
    area.spawn(pb_sunken_blind, "poacher_trapper", count_min=1, count_max=1, respawn_minutes=25, respawn_variance=6)
    area.spawn(pb_watch_perch, "poacher_trapper", count_min=0, count_max=1, respawn_minutes=27, respawn_variance=7)
    area.spawn(pb_bone_ditch, "wolf", count_min=1, count_max=1, respawn_minutes=24, respawn_variance=6)
    area.spawn(lb_reed_bank, "plains_viper", count_min=1, count_max=1, respawn_minutes=20, respawn_variance=5)
    area.spawn(lb_narrow_cove, "wild_boar", count_min=0, count_max=1, respawn_minutes=25, respawn_variance=6)
    area.spawn(lb_keeper_weir, "wolf", count_min=1, count_max=1, respawn_minutes=24, respawn_variance=6)
    area.spawn(lb_hidden_cove, "poacher_trapper", count_min=0, count_max=1, respawn_minutes=27, respawn_variance=7)
    area.spawn(sw_fern_pocket, "wolf", count_min=1, count_max=1, respawn_minutes=24, respawn_variance=6)
    area.spawn(sw_hart_run, "wild_boar", count_min=1, count_max=1, respawn_minutes=26, respawn_variance=7)
    area.spawn(sw_hollow_ring, "trophy_hound", count_min=0, count_max=1, respawn_minutes=24, respawn_variance=6)
    area.spawn(sw_hidden_spring, "plains_viper", count_min=1, count_max=1, respawn_minutes=20, respawn_variance=5)

    # ==================================================================
    #  NAMED MOBS
    # ==================================================================
    area.named_mob(
        "poachmaster_hadrik_vey",
        pb_poacher_den,
        respawn_minutes=190,
        respawn_variance=40,
        prestige_modifier=2.2,
        behavior=["territorial"],
        base_disposition=-0.95,
        flee_threshold=5,
        tome_drop="stagcrown_poacher_tome",
    )
    area.named_mob(
        "twelve_tine_hart",
        sw_heart_glade,
        respawn_minutes=220,
        respawn_variance=45,
        prestige_modifier=2.3,
        behavior=["guardian"],
        base_disposition=-1.0,
        flee_threshold=0,
        tome_drop="stagcrown_witness_tome",
    )

    # ==================================================================
    #  NPCS
    # ==================================================================
    area.npc(fg_charter_gate, "npc_gate_warden_imrel", faction="empire")
    area.npc(fg_hound_racks, "npc_houndmaster_pevra", faction="empire")
    area.npc(mt_charter_stone, "npc_trail_keeper_odan", faction="empire")
    area.npc(mt_keeper_ladder, "npc_game_scout_vesh", faction="empire")
    area.npc(lg_steward_hall, "npc_lodge_steward_halric", faction="empire")
    _quartermaster = area.npc(lg_quartermaster_tent, "npc_keeper_quartermaster_tovin", faction="consortium")
    area.vendor(
        _quartermaster,
        accepts=["consumable", "tool"],
        item_ids=[
            "trail_rations",
            "bandage",
            "minor_healing_potion",
            "minor_stamina_potion",
            "antidote_potion",
            "sickle",
            "skinning_knife",
            "fishing_rod",
            "bait",
        ],
        faction="consortium",
    )
    area.npc(lg_ledger_desk, "npc_registry_clerk_vestri", faction="empire")
    area.npc(lb_fishing_steps, "npc_netter_mira")
    area.npc(lb_weed_bar, "npc_herbalist_renna", faction="circle")
    area.npc(pb_dead_drop, "npc_turncoat_ivar")
    area.npc(sw_witness_stone, "npc_stone_reader_alwen", faction="circle")
    area.npc(sw_prayer_break, "npc_witness_nara")

    # ==================================================================
    #  ITEMS
    # ==================================================================
    area.item(
        "sealed_keeper_billet",
        key="Sealed Keeper Billet",
        item_type="item",
        weight=0.2,
        rarity="normal",
        value=0,
        is_quest_item=True,
        desc="A folded courtesy billet carrying preserve run assignments, guest seals, and the quiet proof that someone was admitted at the gate.",
    )
    area.item(
        "charter_rubbing_case",
        key="Charter Rubbing Case",
        item_type="item",
        weight=0.2,
        rarity="normal",
        value=0,
        is_quest_item=True,
        desc="A waxed case holding a fresh rubbing from the lodge charter desk, prepared for comparison against older witness cuts in the woods.",
    )

    # ==================================================================
    #  LORE FRAGMENTS
    # ==================================================================
    area.lore_fragment(
        "sp_lore_revision_post",
        fg_writ_arch,
        discovery_method="search",
        scholar_path="arcana",
        text="The Stagcrown Revision of 728 frames enclosure as refinement, yet the scraped margin beneath it notes common passage curtailed by courtesy rather than law.",
        insight_gain=2,
    )
    area.lore_fragment(
        "sp_lore_hound_ledger",
        fg_hound_racks,
        discovery_method="search",
        scholar_path="remnance",
        text="A kennel ledger counts House Rhest hounds, guest kills, and culled village dogs on the same page, then bills the losses to orderly management.",
        insight_gain=2,
    )
    area.lore_fragment(
        "sp_lore_tally_green",
        fg_tally_green,
        discovery_method="search",
        scholar_path="arcana",
        text="A guest roll marks licensed arrivals in gold ink while local petitioners are noted only as denied at gate, copy sufficient, no witness retained.",
        insight_gain=3,
    )
    area.lore_fragment(
        "sp_lore_drive_notes",
        mt_feed_scatter,
        discovery_method="search",
        scholar_path="resonance",
        text="Keeper notes on the feed scatter treat deer movement like road traffic, assigning timed drives, horn calls, and acceptable panic lanes for noble convenience.",
        insight_gain=2,
    )
    area.lore_fragment(
        "sp_lore_broken_blind",
        mt_broken_blind,
        discovery_method="search",
        scholar_path="remnance",
        text="A pasted repair order for the shattered blind omits the wounded stag that broke it, but not the guest whose shot must never be recorded as clumsy.",
        insight_gain=2,
    )
    area.lore_fragment(
        "sp_lore_steward_copy",
        lg_ledger_desk,
        discovery_method="search",
        scholar_path="arcana",
        text="Steward copies amend kill tallies after the hunt, shifting choice carcasses between House Talvere guests, lodge kitchens, and the private preserve reserve.",
        insight_gain=3,
    )
    area.lore_fragment(
        "sp_lore_poacher_letters",
        pb_dead_drop,
        discovery_method="search",
        scholar_path="arcana",
        text="Wrapped notes in the dead drop promise off-ledger venison to city buyers with instructions to mention House Rhest kitchens only in person, never in ink.",
        insight_gain=3,
    )
    area.lore_fragment(
        "sp_lore_bone_ditch",
        pb_bone_ditch,
        discovery_method="search",
        scholar_path="remnance",
        text="The bone ditch preserves seasons of discarded trophy cuts and stripped fish, proof that the preserve wastes openly while nearby wards are taught to starve politely.",
        insight_gain=2,
    )
    area.lore_fragment(
        "sp_lore_reservoir_face",
        lb_charter_spill,
        discovery_method="search",
        scholar_path="resonance",
        text="The slipped retaining face shows the reservoir edge was not founded for the preserve at all; later stone merely wrapped an older witness line in aristocratic masonry.",
        insight_gain=2,
    )
    area.lore_fragment(
        "sp_lore_witness_ring",
        sw_witness_stone,
        discovery_method="search",
        scholar_path="arcana",
        text="A rubbing pressed deep into the witness stone records that the ring once marked shared seasonal use. The preserve charter claims restoration while admitting no prior consent.",
        insight_gain=3,
    )

    # ==================================================================
    #  QUESTS
    # ==================================================================
    area.quest(
        "sp_q_courtesy_billet",
        name="Courtesy Billet",
        description="Gate Warden Imrel needs a sealed keeper billet carried from the preserve gate to Game Scout Vesh before another visiting party claims the managed runs without leaving a written trace.",
        quest_type="delivery",
        quest_giver="npc_gate_warden_imrel",
        objectives=[
            {
                "type": "deliver",
                "target": "npc_game_scout_vesh",
                "count": 1,
                "description": "Deliver the sealed keeper billet to Game Scout Vesh",
            },
        ],
        flagged_drop="sealed_keeper_billet",
        rewards=[
            {"action_type": "give_scales", "amount": 75},
            {"action_type": "modify_standing", "faction_id": "empire", "delta": 70},
            {
                "action_type": "echo",
                "message": "|gImrel inclines his head. \"Good. If the run is being stolen, I'd rather the proof arrive before the excuses do.\"|n",
            },
        ],
        next_quest_id="sp_q_meat_line",
        objective_type="deliver",
        objective_target="npc_game_scout_vesh",
        objective_count=1,
    )
    area.quest(
        "sp_q_meat_line",
        name="Meat Line",
        description="Game Scout Vesh says the drives are being bled through hidden meat lines in the brush. Break the poacher trappers working the preserve's blind routes.",
        quest_type="kill",
        quest_giver="npc_game_scout_vesh",
        prerequisite_quests=["sp_q_courtesy_billet"],
        objectives=[
            {
                "type": "kill",
                "target": "poacher_trapper",
                "count": 3,
                "description": "Defeat poacher trappers running the hidden meat lines",
            },
        ],
        rewards=[
            {"action_type": "give_scales", "amount": 95},
            {"action_type": "modify_standing", "faction_id": "empire", "delta": 60},
            {
                "action_type": "echo",
                "message": "|gVesh checks the torn wires in grim silence. \"Good. Every blind route they lose makes the next lie harder to stage.\"|n",
            },
        ],
        next_quest_id="sp_q_poachmaster_due",
        objective_type="kill",
        objective_target="poacher_trapper",
        objective_count=3,
    )
    area.quest(
        "sp_q_poachmaster_due",
        name="Poachmaster Due",
        description="Vesh has tracked the forged tags and hidden ledgers back to one dugout. Find Poachmaster Hadrik Vey and end the preserve racket he runs with noble protection.",
        quest_type="kill",
        quest_giver="npc_game_scout_vesh",
        prerequisite_quests=["sp_q_meat_line"],
        objectives=[
            {
                "type": "kill",
                "target": "poachmaster_hadrik_vey",
                "count": 1,
                "description": "Defeat Poachmaster Hadrik Vey in the poacher den",
            },
        ],
        rewards=[
            {"action_type": "give_scales", "amount": 130},
            {"action_type": "modify_standing", "faction_id": "empire", "delta": 105},
            {
                "action_type": "echo",
                "message": "|gVesh folds the recovered forged tags into his palm. \"There. Now the preserve will have to lie louder if it wants this buried again.\"|n",
            },
        ],
        objective_type="kill",
        objective_target="poachmaster_hadrik_vey",
        objective_count=1,
    )
    area.quest(
        "sp_q_charter_rubbing",
        name="Charter Rubbing",
        description="Registry Clerk Vestri wants a fresh charter rubbing carried from the lodge desk to Stone Reader Alwen in the woods before the steward amends the hunting copy again.",
        quest_type="delivery",
        quest_giver="npc_registry_clerk_vestri",
        objectives=[
            {
                "type": "deliver",
                "target": "npc_stone_reader_alwen",
                "count": 1,
                "description": "Deliver the charter rubbing case to Stone Reader Alwen",
            },
        ],
        flagged_drop="charter_rubbing_case",
        rewards=[
            {"action_type": "give_scales", "amount": 80},
            {"action_type": "modify_standing", "faction_id": "empire", "delta": 80},
            {
                "action_type": "echo",
                "message": "|gVestri presses ink from his fingertips. \"Good. If the lodge copy changes again, at least one comparison will survive it.\"|n",
            },
        ],
        next_quest_id="sp_q_stone_witness",
        objective_type="deliver",
        objective_target="npc_stone_reader_alwen",
        objective_count=1,
    )
    area.quest(
        "sp_q_stone_witness",
        name="Stone Witness",
        description="Alwen wants proof that the preserve charter was laid across older witness boundaries from gate, lake, and ring alike. Read the seams before they are boxed in again.",
        quest_type="investigation",
        quest_giver="npc_stone_reader_alwen",
        prerequisite_quests=["sp_q_charter_rubbing"],
        objectives=[
            {
                "type": "investigate",
                "target": "fg_old_boundary",
                "count": 1,
                "description": "Inspect the old boundary stones near the gate",
            },
            {
                "type": "investigate",
                "target": "lb_charter_spill",
                "count": 1,
                "description": "Inspect the slipped charter face at the reservoir",
            },
            {
                "type": "investigate",
                "target": "sw_old_altar",
                "count": 1,
                "description": "Read the older offering stone in the woods",
            },
        ],
        rewards=[
            {"action_type": "give_scales", "amount": 90},
            {"action_type": "modify_standing", "faction_id": "circle", "delta": 85},
            {
                "action_type": "echo",
                "message": "|gAlwen lays the rubbings side by side. \"There it is. Enclosure dressed as stewardship, cut onto older consent like it was always theirs.\"|n",
            },
        ],
        next_quest_id="sp_q_twelve_tines",
        objective_type="investigate",
        objective_target="fg_old_boundary",
        objective_count=3,
    )
    area.quest(
        "sp_q_twelve_tines",
        name="Twelve Tines",
        description="Alwen says the great hart haunting the heart glade has been driven, wounded, and claimed by too many hunting parties to leave the ring in peace. Bring the brutal pageant to an end.",
        quest_type="kill",
        quest_giver="npc_stone_reader_alwen",
        prerequisite_quests=["sp_q_stone_witness"],
        objectives=[
            {
                "type": "kill",
                "target": "twelve_tine_hart",
                "count": 1,
                "description": "Defeat the Twelve-Tine Hart in the heart glade",
            },
        ],
        rewards=[
            {"action_type": "give_scales", "amount": 125},
            {"action_type": "modify_standing", "faction_id": "circle", "delta": 100},
            {
                "action_type": "echo",
                "message": "|gAlwen bows his head toward the glade. \"Better witness than spectacle. Better an ending than another season of applause.\"|n",
            },
        ],
        objective_type="kill",
        objective_target="twelve_tine_hart",
        objective_count=1,
    )

    # ==================================================================
    #  GATHERING POOLS
    # ==================================================================
    area.gathering_pool(
        "herb",
        rooms=["fg_reed_verge", "mt_feed_scatter", "lb_weed_bar", "sw_fern_pocket"],
        materials=["horncap_moss", "charter_bark"],
        max_active=4,
        respawn_minutes=10,
        respawn_variance=3,
    )
    area.gathering_pool(
        "hide",
        rooms=["mt_rut_hollow", "pb_blood_fern", "sw_hart_run", "sw_heart_glade"],
        materials=["stagcrown_hide"],
        max_active=3,
        respawn_minutes=16,
        respawn_variance=5,
    )
    area.gathering_pool(
        "forage",
        rooms=["fg_reed_verge", "pb_bone_ditch", "lb_reed_bank", "lb_hidden_cove"],
        materials=["keeper_reed", "bone_lure"],
        max_active=3,
        respawn_minutes=9,
        respawn_variance=3,
    )
    area.gathering_pool(
        "fish",
        rooms=["lb_tally_dock", "lb_fishing_steps", "lb_narrow_cove", "lb_hidden_cove", "lb_noble_jetty"],
        materials=["silverfin_trout"],
        max_active=3,
        respawn_minutes=10,
        respawn_variance=4,
    )

    return area.build()
