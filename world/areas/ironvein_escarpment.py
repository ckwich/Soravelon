"""
Ironvein Escarpment -- Hub 4 exterior zone

The capital's nearest quarry front. Switchbacks, blasted terraces, lift towers,
spoil runoff, labor camps, and a stripped shrine belt reveal how Varath Prime's
order is built out of counted stone, erased memorials, and forced obedience.
"""

from world.area_builder import AreaBuilder


def build():
    area = AreaBuilder("ironvein_escarpment")

    # ------------------------------------------------------------------
    # Zone setup
    # ------------------------------------------------------------------
    area.zone(
        name="Ironvein Escarpment",
        zone_type="frontier",
        continent="varath",
        tier=4,
        region="crownlands",
        hub_city="varath_prime",
        faction_territory="imperial",
        faction_presence=["empire", "consortium", "circle"],
        world_x=108,
        world_y=44,
        world_radius=128,
    )

    # ------------------------------------------------------------------
    # Materials
    # ------------------------------------------------------------------
    area.material(
        "ironvein_ore",
        tier=1,
        terrain="stone",
        absorbed_property="hardite",
        profession_bonus={"smithing": 0.1},
    )
    area.material(
        "bench_slate",
        tier=1,
        terrain="stone",
        absorbed_property="precision",
        profession_bonus={"smithing": 0.05, "scholarship": 0.05},
    )
    area.material(
        "haul_chain_link",
        tier=1,
        terrain="yard",
        absorbed_property="durability",
        profession_bonus={"smithing": 0.1},
    )
    area.material(
        "runoff_cress",
        tier=1,
        terrain="water",
        absorbed_property="clarity",
        profession_bonus={"alchemy": 0.1},
    )
    area.material(
        "memorial_chalk",
        tier=1,
        terrain="ruins",
        absorbed_property="resonance",
        profession_bonus={"scholarship": 0.1},
    )
    area.material(
        "slag_hound_hide",
        tier=1,
        terrain="path",
        absorbed_property="tenacity",
        profession_bonus={"leatherworking": 0.1},
    )

    # ==================================================================
    #  SWITCHBACK APPROACH ROAD
    # ==================================================================
    sr_gate_grade = area.room(
        "sr_gate_grade",
        name="Gate Grade",
        desc=(
            "The road north from the Martial Quarter steepens into a chalky grade lined "
            "with tally posts, hammer marks, and warning boards quoting the Iron Vein "
            "Requisition of 734 as if stone itself had asked for more cutting."
        ),
        room_type="path",
    )
    sr_first_switch = area.room(
        "sr_first_switch",
        name="First Switch",
        desc="The first turn of the escarpment road curls around pale spoil and old wheel scars where supply carts grind uphill under shouted counts.",
        room_type="path",
    )
    sr_talon_barricade = area.room(
        "sr_talon_barricade",
        name="Talon Barricade",
        desc="A low barricade of quarry block and old tack crates narrows the road beneath a weathered talon-and-bar posting about controlled haul traffic.",
        room_type="path",
    )
    sr_milestone_cut = area.room(
        "sr_milestone_cut",
        name="Milestone Cut",
        desc="An older roadside stone was split and reset into the slope, its deeper numbering buried beneath a measured rod seal and fresh lime wash.",
        room_type="path",
    )
    sr_guard_shelf = area.room(
        "sr_guard_shelf",
        name="Guard Shelf",
        desc="A widened shelf gives road guards clear sightlines over the climb and the lower city roofs now paling behind dust.",
        room_type="clearing",
    )
    sr_dust_turn = area.room(
        "sr_dust_turn",
        name="Dust Turn",
        desc="The road bends through grit fine enough to gray every boot and glove, making rank and labor look briefly alike.",
        room_type="path",
    )
    sr_chain_berm = area.room(
        "sr_chain_berm",
        name="Chain Berm",
        desc="Broken haul chains, bent hooks, and snapped bracing pins have been shoveled into a roadside berm beside the climb.",
        room_type="path",
    )
    sr_ration_nook = area.room(
        "sr_ration_nook",
        name="Ration Nook",
        desc="A shallow cut in the slope holds cracked ration bins, tin cups, and the grease-dark shadows of short sanctioned meal stops.",
        room_type="clearing",
    )
    sr_quarry_view = area.room(
        "sr_quarry_view",
        name="Quarry View",
        desc="The escarpment opens enough here to show the first broad shelves of the works above, pale cuts stacked like stripped pages.",
        room_type="path",
    )
    sr_ash_slope = area.room(
        "sr_ash_slope",
        name="Ash Slope",
        desc="Black powder dust and pale quarry chalk mix underfoot into a caked film that grips wheels and lungs alike.",
        room_type="path",
    )
    sr_marker_post = area.room(
        "sr_marker_post",
        name="Marker Post",
        desc="A tall post lists load priorities, shift bells, and sanctioned losses in a hand so neat it feels like another instrument of force.",
        room_type="path",
    )
    sr_ledge_turn = area.room(
        "sr_ledge_turn",
        name="Ledge Turn",
        desc="The road narrows against a drop where every wagon must slow, exposing the hauled stone to every eye on the slope.",
        room_type="path",
    )
    sr_watch_cradle = area.room(
        "sr_watch_cradle",
        name="Watch Cradle",
        desc="A braced timber cradle hangs over the road shoulder for spotters and tally clerks who watch the climb more than they help it.",
        room_type="building",
        indoor=True,
    )
    sr_broken_cart = area.room(
        "sr_broken_cart",
        name="Broken Cart",
        desc="A shattered ore cart lies against the retaining wall, its split boards still chalked with Stonewake pickmarks and docked labor counts.",
        room_type="ruins",
    )
    sr_upper_switch = area.room(
        "sr_upper_switch",
        name="Upper Switch",
        desc="The climb turns back on itself again beneath hanging chain and chalk arrows pointing toward terraces, haul towers, and camp rows.",
        room_type="path",
    )
    sr_powder_lean = area.room(
        "sr_powder_lean",
        name="Powder Lean",
        desc="A roofed lean-to of patched canvas and stone keeps blasting casks dry under Ministry warnings copied one more time than the wood needed.",
        room_type="building",
        indoor=True,
    )
    sr_narrow_shelf = area.room(
        "sr_narrow_shelf",
        name="Narrow Shelf",
        desc="The road thins to a stony shelf worn smooth by wagon wheels leaning outward toward the drop.",
        room_type="path",
    )
    sr_shock_gully = area.room(
        "sr_shock_gully",
        name="Shock Gully",
        desc="A scarred gully beside the road carries rain, grit, and the echo of blasting charges down toward the city wall.",
        room_type="ruins",
    )
    sr_last_bend = area.room(
        "sr_last_bend",
        name="Last Bend",
        desc="The final curve below the terraces is cut broad and clean, as if the escarpment were being taught to obey survey lines.",
        room_type="path",
    )
    sr_lower_bench = area.room(
        "sr_lower_bench",
        name="Lower Bench",
        desc="The road finally levels into the first broad bench of the quarry, where hauled stone gives way to raw cut-face and hammered commands.",
        room_type="clearing",
    )

    # ==================================================================
    #  LOWER CUT TERRACES
    # ==================================================================
    lt_lower_bench = area.room(
        "lt_lower_bench",
        name="Lower Bench",
        desc="Fresh tool marks and older fracture lines share the same terrace wall, proving the quarry has been widened by many hands but claimed by one office.",
        room_type="clearing",
    )
    lt_cut_entry = area.room(
        "lt_cut_entry",
        name="Cut Entry",
        desc="Rutted tracks and sled grooves lead into the first active cut where teams pry slate and ore from the bench face.",
        room_type="path",
    )
    lt_first_terrace = area.room(
        "lt_first_terrace",
        name="First Terrace",
        desc="Laborers once stood here in even lines; now only bracing slots and half-buried wedges keep the pattern visible.",
        room_type="clearing",
    )
    lt_powder_lane = area.room(
        "lt_powder_lane",
        name="Powder Lane",
        desc="Black streaks in the chalk mark where blasting powder is dragged from dry store to drilled seam.",
        room_type="path",
    )
    lt_split_ramp = area.room(
        "lt_split_ramp",
        name="Split Ramp",
        desc="One ramp climbs toward higher benches while another falls toward runoff, both carved through older fracture planes the survey did not make.",
        room_type="path",
    )
    lt_drill_shed = area.room(
        "lt_drill_shed",
        name="Drill Shed",
        desc="Hand drills, mallets, and dull augers hang in careful rows under a shed wall scored with shift tallies and injury marks.",
        room_type="building",
        indoor=True,
    )
    lt_blast_lip = area.room(
        "lt_blast_lip",
        name="Blast Lip",
        desc="The terrace edge falls away in a jagged bite where repeated charges have taught the stone to fail along profitable lines.",
        room_type="clearing",
    )
    lt_chain_posts = area.room(
        "lt_chain_posts",
        name="Chain Posts",
        desc="Iron posts sunk deep into the bench hold drag chains and brake ropes for lowering dressed blocks toward the haul line.",
        room_type="clearing",
    )
    lt_ore_screen = area.room(
        "lt_ore_screen",
        name="Ore Screen",
        desc="Rattle screens and chipped bins divide richer iron-bearing stone from the rest while dust hangs in the air like old witness ash.",
        room_type="clearing",
    )
    lt_water_break = area.room(
        "lt_water_break",
        name="Water Break",
        desc="A shaded notch in the bench holds cracked jars and a trough of chalky water where crews pause under watch instead of privacy.",
        room_type="clearing",
    )
    lt_broken_dolly = area.room(
        "lt_broken_dolly",
        name="Broken Dolly",
        desc="A shattered hauling dolly sprawls on its side with one wheel still grinding slowly whenever the haul line takes load above.",
        room_type="ruins",
    )
    lt_red_chute = area.room(
        "lt_red_chute",
        name="Red Chute",
        desc="A steep chute stained by iron dust funnels better ore toward sorted bins and worse bodies toward the runoff below.",
        room_type="path",
    )
    lt_tool_house = area.room(
        "lt_tool_house",
        name="Tool House",
        desc="The lockbox room for chisels, wedges, and measure rods smells of old oil, wet slate, and too many signed receipts.",
        room_type="building",
        indoor=True,
    )
    lt_shiver_cut = area.room(
        "lt_shiver_cut",
        name="Shiver Cut",
        desc="Hairline fractures web the cut face so densely that each hammer tap seems to answer from a dozen hidden seams.",
        room_type="path",
    )
    lt_blast_cleft = area.room(
        "lt_blast_cleft",
        name="Blast Cleft",
        desc="A torn cleft splits the bench where an overcharge opened a crawlspace into the drainage bed below and the office pretended it was planned.",
        room_type="cave",
        indoor=True,
    )
    lt_second_terrace = area.room(
        "lt_second_terrace",
        name="Second Terrace",
        desc="The second bench carries deeper extraction scars, thicker haul grooves, and more memorial scratches than the lower shelf ever admitted.",
        room_type="clearing",
    )
    lt_marker_wall = area.room(
        "lt_marker_wall",
        name="Marker Wall",
        desc="A retaining wall of numbered cut blocks bears Ministry revision paint over older count marks that never fully disappear.",
        room_type="ruins",
    )
    lt_bone_heap = area.room(
        "lt_bone_heap",
        name="Bone Heap",
        desc="Discarded splints, snapped handles, and blasted stone pile together in a heap that workers pretend is only debris.",
        room_type="ruins",
    )
    lt_sump_steps = area.room(
        "lt_sump_steps",
        name="Sump Steps",
        desc="Shallow steps drop toward a drainage sump where red water and powdered chalk swirl together in sluggish loops.",
        room_type="path",
    )
    lt_memorial_slab = area.room(
        "lt_memorial_slab",
        name="Memorial Slab",
        desc="A broad slab against the cut face carries names scratched, scraped off, and scratched again beneath the same civic measure seal.",
        room_type="ruins",
    )
    lt_upper_terrace = area.room(
        "lt_upper_terrace",
        name="Upper Terrace",
        desc="The highest active bench opens onto the liftworks above, where every loaded stone becomes a counted obligation before it ever reaches the city.",
        room_type="clearing",
    )
    lt_haul_link = area.room(
        "lt_haul_link",
        name="Haul Link",
        desc="Heavy ruts and chain scars draw the quarry bench toward the lift towers, trading chisels and dust for hooks and ledgers.",
        room_type="path",
    )

    # ==================================================================
    #  LIFT TOWERS AND HAUL LINES
    # ==================================================================
    hl_haul_link = area.room(
        "hl_haul_link",
        name="Haul Link",
        desc="The terrace road narrows into a packed line of rollers and chain guides where cut stone begins its climb out of the pit.",
        room_type="path",
    )
    hl_main_lift = area.room(
        "hl_main_lift",
        name="Main Lift",
        desc="The main lift frame towers overhead in timber, iron, and civic paint, turning brute force into orderly transport by decree.",
        room_type="building",
        indoor=True,
    )
    hl_chain_gantry = area.room(
        "hl_chain_gantry",
        name="Chain Gantry",
        desc="Great chain loops travel through the gantry teeth with a grinding rhythm that feels older than any shouted shift order.",
        room_type="building",
        indoor=True,
    )
    hl_counterweight_pit = area.room(
        "hl_counterweight_pit",
        name="Counterweight Pit",
        desc="A deep pit drops under the gantry where stone weights travel in darkness slick with grease and powdered metal.",
        room_type="underground",
        indoor=True,
    )
    hl_signal_post = area.room(
        "hl_signal_post",
        name="Signal Post",
        desc="Flags, bells, and chalk slates crowd this post so thoroughly that the lift seems to move on paperwork as much as weight.",
        room_type="clearing",
    )
    hl_slung_bridge = area.room(
        "hl_slung_bridge",
        name="Slung Bridge",
        desc="A swaying bridge of plank and chain spans one open cut, forcing handlers and loads into the same exposed line.",
        room_type="path",
    )
    hl_cradle_platform = area.room(
        "hl_cradle_platform",
        name="Cradle Platform",
        desc="Loaded cradles pause here before rising, each one marked in chalk with lot numbers, contractor cuts, and deducted deadweight.",
        room_type="clearing",
    )
    hl_tower_stairs = area.room(
        "hl_tower_stairs",
        name="Tower Stairs",
        desc="Steep timber stairs climb the lift tower interior, their rails worn by hands that worked long before this paint job.",
        room_type="building",
        indoor=True,
    )
    hl_lift_cab = area.room(
        "hl_lift_cab",
        name="Lift Cab",
        desc="A cramped operator cab overlooks the quarry through dust-frosted shutters and a grid of signal cords.",
        room_type="building",
        indoor=True,
    )
    hl_bell_frame = area.room(
        "hl_bell_frame",
        name="Bell Frame",
        desc="Shift bells and warning hammers hang from an iron frame where the day is cut into profitable noise.",
        room_type="clearing",
    )
    hl_tarp_walk = area.room(
        "hl_tarp_walk",
        name="Tarp Walk",
        desc="Canvas screens snap in the wind along this narrow walk, hiding ledger tables from weather but not from suspicion.",
        room_type="path",
    )
    hl_upper_hook = area.room(
        "hl_upper_hook",
        name="Upper Hook",
        desc="Massive hooks wait here for the heaviest lifted loads, each one bright at the wear points and red with dust elsewhere.",
        room_type="clearing",
    )
    hl_maintenance_bay = area.room(
        "hl_maintenance_bay",
        name="Maintenance Bay",
        desc="Split rollers, spare pins, and dragged chain lengths fill a repair bay where nothing is ever fully replaced, only made passable.",
        room_type="building",
        indoor=True,
    )
    hl_grease_shed = area.room(
        "hl_grease_shed",
        name="Grease Shed",
        desc="Buckets of black grease and grit line the shed wall beside invoices stamped for Stonewake use and nobody else's.",
        room_type="building",
        indoor=True,
    )
    hl_slack_line = area.room(
        "hl_slack_line",
        name="Slack Line",
        desc="A side run of chain sags over an older cut where the lift path was moved but never truly rebuilt.",
        room_type="path",
    )
    hl_drop_stage = area.room(
        "hl_drop_stage",
        name="Drop Stage",
        desc="Loads coming off the higher lift slam onto this stage before teams roll them toward camp stores or city carts.",
        room_type="clearing",
    )
    hl_ledger_catwalk = area.room(
        "hl_ledger_catwalk",
        name="Ledger Catwalk",
        desc="A catwalk above the loading floor gives clerks room to watch weights, names, and deductions from a safe remove.",
        room_type="path",
    )
    hl_spoil_overlook = area.room(
        "hl_spoil_overlook",
        name="Spoil Overlook",
        desc="From this high edge the spoil fields look like a second quarry made only of what the first one judged unworthy.",
        room_type="clearing",
    )

    # ==================================================================
    #  SPOIL FIELDS AND RUNOFF
    # ==================================================================
    sp_black_run = area.room(
        "sp_black_run",
        name="Black Run",
        desc="Dark runoff from powder ash and iron dust cuts a shallow line through the spoil below the haul towers.",
        room_type="path",
    )
    sp_drain_slot = area.room(
        "sp_drain_slot",
        name="Drain Slot",
        desc="A cut drain carries red-brown slurry between broken retaining stones and the remains of hurried repairs.",
        room_type="cave",
        indoor=True,
    )
    sp_spoil_mound = area.room(
        "sp_spoil_mound",
        name="Spoil Mound",
        desc="A steep mound of rejected stone, shattered wedges, and useless dust leans against the runoff trench.",
        room_type="clearing",
    )
    sp_ash_pit = area.room(
        "sp_ash_pit",
        name="Ash Pit",
        desc="Powder ash and charcoal fines gather in a pit where anything black enough can be called disposable.",
        room_type="ruins",
    )
    sp_tin_shack = area.room(
        "sp_tin_shack",
        name="Tin Shack",
        desc="A rattling shack of patched tin and quarry board shelters pumps, shovels, and an old roster no one admits keeping.",
        room_type="building",
        indoor=True,
    )
    sp_slurry_bank = area.room(
        "sp_slurry_bank",
        name="Slurry Bank",
        desc="The bank beside the trench is slick with clay, ore grit, and clotted runoff that refuses to settle clear.",
        room_type="path",
    )
    sp_chain_dump = area.room(
        "sp_chain_dump",
        name="Chain Dump",
        desc="Snapped links and rusted hooks lie in a dump heap waiting to be weighed, salvaged, or forgotten under new loads.",
        room_type="ruins",
    )
    sp_runoff_trench = area.room(
        "sp_runoff_trench",
        name="Runoff Trench",
        desc="A hand-cut trench channels sour water away from the camp, though the smell says it only moves the harm around.",
        room_type="path",
    )
    sp_weed_gutter = area.room(
        "sp_weed_gutter",
        name="Weed Gutter",
        desc="Thin green growth clings to the gutter where poisoned water slows enough for desperate herbs to risk it.",
        room_type="clearing",
    )
    sp_burnt_heap = area.room(
        "sp_burnt_heap",
        name="Burnt Heap",
        desc="A heap of tarps, broken handles, and old clothing has been burned down to clinker and nail heads beside the trench.",
        room_type="ruins",
    )
    sp_cracked_pipe = area.room(
        "sp_cracked_pipe",
        name="Cracked Pipe",
        desc="A clay pipe split by pressure leaks a steady ribbon of red water that stains the spoil in branching fans.",
        room_type="ruins",
    )
    sp_buzzard_post = area.room(
        "sp_buzzard_post",
        name="Buzzard Post",
        desc="A lone post above the runoff gives scavenger birds a perfect watchpoint over the ditch and the camp edge.",
        room_type="clearing",
    )
    sp_mud_step = area.room(
        "sp_mud_step",
        name="Mud Step",
        desc="Bootsteps and drag marks have hardened into a low stair of clay where crews cross the spreading runoff by habit.",
        room_type="path",
    )
    sp_sink_hollow = area.room(
        "sp_sink_hollow",
        name="Sink Hollow",
        desc="One hollowed patch of spoil has sunk into itself, leaving a bowl of damp grit, weed stalks, and lost tools.",
        room_type="clearing",
    )
    sp_stake_channel = area.room(
        "sp_stake_channel",
        name="Stake Channel",
        desc="Survey stakes line a narrow channel whose measured edges fail every time the runoff rises.",
        room_type="path",
    )
    sp_broken_weir = area.room(
        "sp_broken_weir",
        name="Broken Weir",
        desc="A failed weir of quarried block tries and fails to make a pond out of poison and rejected stone.",
        room_type="ruins",
    )
    sp_red_sluice = area.room(
        "sp_red_sluice",
        name="Red Sluice",
        desc="The sluice gate is permanently stained the color of old blood and iron filings, though the books call it routine runoff.",
        room_type="ruins",
    )
    sp_camp_backwash = area.room(
        "sp_camp_backwash",
        name="Camp Backwash",
        desc="The last spill of the runoff slows behind the labor camp where the ground remembers every overflow longer than the office does.",
        room_type="clearing",
    )

    # ==================================================================
    #  LABOR ENCAMPMENTS
    # ==================================================================
    lc_muster_square = area.room(
        "lc_muster_square",
        name="Muster Square",
        desc="Packed earth and chalk lines mark the square where crews are counted, reassigned, and reminded which losses will be written down.",
        room_type="clearing",
    )
    lc_payline = area.room(
        "lc_payline",
        name="Payline",
        desc="A roped corridor and tally board turn wages into a process of waiting under eyes and deductions.",
        room_type="path",
    )
    lc_sleep_rows = area.room(
        "lc_sleep_rows",
        name="Sleep Rows",
        desc="Canvas rows sag under quarry dust and damp where the camp holds bodies between one bell and the next.",
        room_type="clearing",
    )
    lc_quiet_roll = area.room(
        "lc_quiet_roll",
        name="Quiet Roll",
        desc="A narrow strip behind the sleeping rows is where the missing are whispered into memory after the official count closes.",
        room_type="path",
    )
    lc_tool_lot = area.room(
        "lc_tool_lot",
        name="Tool Lot",
        desc="Loaned picks, shovels, and drag hooks stand in ordered racks that make debt look organized.",
        room_type="clearing",
    )
    lc_chain_patch = area.room(
        "lc_chain_patch",
        name="Chain Patch",
        desc="Teams patch haul chain and cart braces in the open because the lift will never wait for comfort.",
        room_type="clearing",
    )
    lc_shift_bell = area.room(
        "lc_shift_bell",
        name="Shift Bell",
        desc="A cracked bell hangs above the camp spine, ringing start, stop, injury, and shortage in the same harsh tone.",
        room_type="clearing",
    )
    lc_dust_court = area.room(
        "lc_dust_court",
        name="Dust Court",
        desc="This open patch of camp is wide enough for arguments, punishments, and quick public corrections before the next load moves.",
        room_type="clearing",
    )
    lc_water_cart = area.room(
        "lc_water_cart",
        name="Water Cart",
        desc="A heavy cart of chalky water stands under guard because relief is counted here like every other ration.",
        room_type="clearing",
    )
    lc_wage_desk = area.room(
        "lc_wage_desk",
        name="Wage Desk",
        desc="Scratched tables and weight stones form a makeshift office where pay is issued, docked, and justified under copied seals.",
        room_type="building",
        indoor=True,
    )
    lc_camp_rim = area.room(
        "lc_camp_rim",
        name="Camp Rim",
        desc="The back edge of the camp overlooks the runoff field and the lifted stone above, trapping every worker between them.",
        room_type="clearing",
    )
    lc_shrine_track = area.room(
        "lc_shrine_track",
        name="Shrine Track",
        desc="A beaten track leaves the camp toward stripped prayer stones and a belt of sanctuaries the quarry could not quite grind flat.",
        room_type="path",
    )
    lc_sutler_tent = area.room(
        "lc_sutler_tent",
        name="Sutler Tent",
        desc="A broad service tent sells worn tools, bitter tonics, and enough dry food to keep a shift standing another day.",
        room_type="building",
        indoor=True,
    )
    lc_cookfires = area.room(
        "lc_cookfires",
        name="Cookfires",
        desc="Shallow cook pits smoke beside dented pots where stew is stretched as far as the payline will allow.",
        room_type="clearing",
    )
    lc_nurse_tent = area.room(
        "lc_nurse_tent",
        name="Nurse Tent",
        desc="Bandages, splints, and a copper basin fill a tent where the injured are patched just enough to stand again.",
        room_type="building",
        indoor=True,
    )
    lc_bucket_rack = area.room(
        "lc_bucket_rack",
        name="Bucket Rack",
        desc="Buckets for water, slurry, and lime hang from a rack blackened by years of handling and no real cleaning.",
        room_type="clearing",
    )
    lc_guard_lane = area.room(
        "lc_guard_lane",
        name="Guard Lane",
        desc="A narrow lane between tents gives overseers a straight path through the camp and everyone else a reason to go still.",
        room_type="path",
    )
    lc_barricade_end = area.room(
        "lc_barricade_end",
        name="Barricade End",
        desc="A rough barricade of stone blocks and snapped shafts marks where the camp can be closed faster than it can be protected.",
        room_type="ruins",
    )
    lc_overseer_step = area.room(
        "lc_overseer_step",
        name="Overseer Step",
        desc="A raised stone step beside the pay boards gives foremen and bailiffs a clear place to stand above every grievance.",
        room_type="clearing",
    )
    lc_latrine_edge = area.room(
        "lc_latrine_edge",
        name="Latrine Edge",
        desc="The far edge of camp smells of lime, waste, and runoff where privacy ends and negligence begins.",
        room_type="clearing",
    )

    # ==================================================================
    #  STRIPPED SHRINE BELT
    # ==================================================================
    sb_outer_shrine = area.room(
        "sb_outer_shrine",
        name="Outer Shrine",
        desc="The first shrine on the ridge still holds its old shape, but the niche faces are shaved flat for revised notices and work warnings.",
        room_type="ruins",
    )
    sb_prayer_steps = area.room(
        "sb_prayer_steps",
        name="Prayer Steps",
        desc="Shallow stone steps lead upward past soot-dark wax and chisel scars where offerings once stood openly.",
        room_type="path",
    )
    sb_stripped_porch = area.room(
        "sb_stripped_porch",
        name="Stripped Porch",
        desc="Columns and roofline survive here, but every carved face has been stripped for new text or salvage.",
        room_type="ruins",
    )
    sb_offering_gut = area.room(
        "sb_offering_gut",
        name="Offering Gut",
        desc="A trough where offerings once washed clean is now full of quarry dust, broken bowls, and rusted nails from posted decrees.",
        room_type="ruins",
    )
    sb_scar_wall = area.room(
        "sb_scar_wall",
        name="Scar Wall",
        desc="The shrine wall bears long deliberate scars where names, prayers, and boundary signs were removed under civic authority.",
        room_type="ruins",
    )
    sb_bell_court = area.room(
        "sb_bell_court",
        name="Bell Court",
        desc="This court still centers on a cracked bell frame, though the bell now rings more often for quarry shifts than rites.",
        room_type="clearing",
    )
    sb_ash_apse = area.room(
        "sb_ash_apse",
        name="Ash Apse",
        desc="An inner apse is layered in cold ash from burned slips and old candle offerings swept into the same curve.",
        room_type="cave",
        indoor=True,
    )
    sb_relic_rack = area.room(
        "sb_relic_rack",
        name="Relic Rack",
        desc="Salvaged fragments, bowls, and broken figures have been stacked in a rack like inventory waiting for a better buyer.",
        room_type="building",
        indoor=True,
    )
    sb_witness_stones = area.room(
        "sb_witness_stones",
        name="Witness Stones",
        desc="A cluster of old standing stones watches the stripped belt with the stubbornness of things too heavy to confiscate quietly.",
        room_type="ruins",
    )
    sb_back_steps = area.room(
        "sb_back_steps",
        name="Back Steps",
        desc="Hidden steps behind the witness stones descend toward the camp on a line omitted from the public quarry maps.",
        room_type="path",
    )
    sb_marrow_path = area.room(
        "sb_marrow_path",
        name="Marrow Path",
        desc="A narrow ridge path runs between broken shrines and exposed bedrock where the quarry has cut the hill to its harder center.",
        room_type="path",
    )
    sb_split_idol = area.room(
        "sb_split_idol",
        name="Split Idol",
        desc="A once-towering idol lies split along an ancient seam, its pieces numbered for removal but never fully carried off.",
        room_type="ruins",
    )
    sb_inner_ring = area.room(
        "sb_inner_ring",
        name="Inner Ring",
        desc="A half-buried ring of shrine stones survives deeper in the belt, too aligned to be random and too damaged to be denied.",
        room_type="ruins",
    )
    sb_charred_cells = area.room(
        "sb_charred_cells",
        name="Charred Cells",
        desc="Small prayer cells blackened by deliberate fire line the inner ring like a lesson in sanctioned forgetting.",
        room_type="ruins",
    )
    sb_hush_chamber = area.room(
        "sb_hush_chamber",
        name="Hush Chamber",
        desc="A chamber behind the ring swallows echoes beneath soot and cut marks, as if even sound had been revised here.",
        room_type="underground",
        indoor=True,
    )
    sb_cinder_font = area.room(
        "sb_cinder_font",
        name="Cinder Font",
        desc="The old font holds only cinder, grit, and folded slips too singed to read at a glance.",
        room_type="underground",
        indoor=True,
    )
    sb_broken_sanctum = area.room(
        "sb_broken_sanctum",
        name="Broken Sanctum",
        desc="The sanctum roof is gone, leaving prayer walls open to ash, weather, and the gaze of quarry guards on the ridge.",
        room_type="ruins",
    )
    sb_silent_walk = area.room(
        "sb_silent_walk",
        name="Silent Walk",
        desc="A stone walk circles the deepest part of the belt where even scavengers lower their voices without knowing why.",
        room_type="path",
    )
    sb_scarred_sanctum = area.room(
        "sb_scarred_sanctum",
        name="Scarred Sanctum",
        desc="At the heart of the shrine belt stands a sanctum carved, scraped, and claimed so many times that every surface feels contested.",
        room_type="ruins",
    )
    sb_memorial_cleft = area.room(
        "sb_memorial_cleft",
        name="Memorial Cleft",
        desc="A cleft in the ridge is filled with chalk names, prayer ties, and hidden rubbings left where the quarry cannot easily sweep them away.",
        room_type="cave",
        indoor=True,
    )
    sb_ridge_lookout = area.room(
        "sb_ridge_lookout",
        name="Ridge Lookout",
        desc="From this lookout the whole escarpment unfolds: city, road, lift, spoil, camp, and shrine all stacked into one visible account.",
        room_type="clearing",
    )
    sb_far_ridge = area.room(
        "sb_far_ridge",
        name="Far Ridge",
        desc="The far ridge trails away from the quarry into rough country, but even here the stone bears quarry marks and revised boundaries.",
        room_type="path",
    )

    # ==================================================================
    #  EXITS
    # ==================================================================
    area.exit(sr_gate_grade, "varath_prime:mq_escarpment_road", "south")
    area.exit(sr_gate_grade, sr_first_switch, "north")
    area.exit(sr_first_switch, sr_gate_grade, "south")
    area.exit(sr_first_switch, sr_talon_barricade, "north")
    area.exit(sr_talon_barricade, sr_first_switch, "south")
    area.exit(sr_talon_barricade, sr_milestone_cut, "north")
    area.exit(sr_milestone_cut, sr_talon_barricade, "south")
    area.exit(sr_milestone_cut, sr_guard_shelf, "north")
    area.exit(sr_guard_shelf, sr_milestone_cut, "south")
    area.exit(sr_guard_shelf, sr_dust_turn, "north")
    area.exit(sr_dust_turn, sr_guard_shelf, "south")
    area.exit(sr_dust_turn, sr_chain_berm, "north")
    area.exit(sr_chain_berm, sr_dust_turn, "south")
    area.exit(sr_chain_berm, sr_ration_nook, "north")
    area.exit(sr_ration_nook, sr_chain_berm, "south")
    area.exit(sr_ration_nook, sr_quarry_view, "north")
    area.exit(sr_quarry_view, sr_ration_nook, "south")
    area.exit(sr_quarry_view, sr_ash_slope, "north")
    area.exit(sr_ash_slope, sr_quarry_view, "south")
    area.exit(sr_ash_slope, sr_marker_post, "north")
    area.exit(sr_marker_post, sr_ash_slope, "south")
    area.exit(sr_marker_post, sr_ledge_turn, "north")
    area.exit(sr_ledge_turn, sr_marker_post, "south")
    area.exit(sr_ledge_turn, sr_watch_cradle, "north")
    area.exit(sr_watch_cradle, sr_ledge_turn, "south")
    area.exit(sr_watch_cradle, sr_broken_cart, "north")
    area.exit(sr_broken_cart, sr_watch_cradle, "south")
    area.exit(sr_broken_cart, sr_upper_switch, "north")
    area.exit(sr_upper_switch, sr_broken_cart, "south")
    area.exit(sr_upper_switch, sr_powder_lean, "north")
    area.exit(sr_powder_lean, sr_upper_switch, "south")
    area.exit(sr_powder_lean, sr_narrow_shelf, "north")
    area.exit(sr_narrow_shelf, sr_powder_lean, "south")
    area.exit(sr_narrow_shelf, sr_shock_gully, "north")
    area.exit(sr_shock_gully, sr_narrow_shelf, "south")
    area.exit(sr_shock_gully, sr_last_bend, "north")
    area.exit(sr_last_bend, sr_shock_gully, "south")
    area.exit(sr_last_bend, sr_lower_bench, "north")
    area.exit(sr_lower_bench, sr_last_bend, "south")
    area.exit(sr_lower_bench, lt_lower_bench, "north")
    area.exit(lt_lower_bench, sr_lower_bench, "south")
    area.exit(sr_milestone_cut, sr_ration_nook, "east")
    area.exit(sr_ration_nook, sr_milestone_cut, "west")
    area.exit(sr_guard_shelf, sr_quarry_view, "east")
    area.exit(sr_quarry_view, sr_guard_shelf, "west")
    area.exit(sr_dust_turn, sr_broken_cart, "east")
    area.exit(sr_broken_cart, sr_dust_turn, "west")
    area.exit(sr_chain_berm, sr_upper_switch, "east")
    area.exit(sr_upper_switch, sr_chain_berm, "west")
    area.exit(sr_ash_slope, sr_watch_cradle, "east")
    area.exit(sr_watch_cradle, sr_ash_slope, "west")
    area.exit(sr_marker_post, sr_shock_gully, "east")
    area.exit(sr_shock_gully, sr_marker_post, "west")
    area.exit(sr_quarry_view, sr_powder_lean, "east")
    area.exit(sr_powder_lean, sr_quarry_view, "west")

    area.exit(lt_lower_bench, lt_cut_entry, "north")
    area.exit(lt_cut_entry, lt_lower_bench, "south")
    area.exit(lt_cut_entry, lt_first_terrace, "north")
    area.exit(lt_first_terrace, lt_cut_entry, "south")
    area.exit(lt_first_terrace, lt_powder_lane, "north")
    area.exit(lt_powder_lane, lt_first_terrace, "south")
    area.exit(lt_powder_lane, lt_split_ramp, "north")
    area.exit(lt_split_ramp, lt_powder_lane, "south")
    area.exit(lt_split_ramp, lt_drill_shed, "north")
    area.exit(lt_drill_shed, lt_split_ramp, "south")
    area.exit(lt_drill_shed, lt_blast_lip, "north")
    area.exit(lt_blast_lip, lt_drill_shed, "south")
    area.exit(lt_blast_lip, lt_chain_posts, "north")
    area.exit(lt_chain_posts, lt_blast_lip, "south")
    area.exit(lt_chain_posts, lt_ore_screen, "north")
    area.exit(lt_ore_screen, lt_chain_posts, "south")
    area.exit(lt_ore_screen, lt_water_break, "north")
    area.exit(lt_water_break, lt_ore_screen, "south")
    area.exit(lt_water_break, lt_broken_dolly, "north")
    area.exit(lt_broken_dolly, lt_water_break, "south")
    area.exit(lt_broken_dolly, lt_red_chute, "north")
    area.exit(lt_red_chute, lt_broken_dolly, "south")
    area.exit(lt_red_chute, lt_tool_house, "north")
    area.exit(lt_tool_house, lt_red_chute, "south")
    area.exit(lt_tool_house, lt_shiver_cut, "north")
    area.exit(lt_shiver_cut, lt_tool_house, "south")
    area.exit(lt_shiver_cut, lt_blast_cleft, "north")
    area.exit(lt_blast_cleft, lt_shiver_cut, "south")
    area.exit(lt_blast_cleft, lt_second_terrace, "north")
    area.exit(lt_second_terrace, lt_blast_cleft, "south")
    area.exit(lt_second_terrace, lt_marker_wall, "north")
    area.exit(lt_marker_wall, lt_second_terrace, "south")
    area.exit(lt_marker_wall, lt_bone_heap, "north")
    area.exit(lt_bone_heap, lt_marker_wall, "south")
    area.exit(lt_bone_heap, lt_sump_steps, "north")
    area.exit(lt_sump_steps, lt_bone_heap, "south")
    area.exit(lt_sump_steps, lt_memorial_slab, "north")
    area.exit(lt_memorial_slab, lt_sump_steps, "south")
    area.exit(lt_memorial_slab, lt_upper_terrace, "north")
    area.exit(lt_upper_terrace, lt_memorial_slab, "south")
    area.exit(lt_upper_terrace, lt_haul_link, "north")
    area.exit(lt_haul_link, lt_upper_terrace, "south")
    area.exit(lt_haul_link, hl_haul_link, "east")
    area.exit(hl_haul_link, lt_haul_link, "west")
    area.exit(lt_first_terrace, lt_drill_shed, "east")
    area.exit(lt_drill_shed, lt_first_terrace, "west")
    area.exit(lt_powder_lane, lt_water_break, "east")
    area.exit(lt_water_break, lt_powder_lane, "west")
    area.exit(lt_split_ramp, lt_tool_house, "east")
    area.exit(lt_tool_house, lt_split_ramp, "west")
    area.exit(lt_blast_lip, lt_red_chute, "east")
    area.exit(lt_red_chute, lt_blast_lip, "west")
    area.exit(lt_chain_posts, lt_shiver_cut, "east")
    area.exit(lt_shiver_cut, lt_chain_posts, "west")
    area.exit(lt_ore_screen, lt_marker_wall, "east")
    area.exit(lt_marker_wall, lt_ore_screen, "west")
    area.exit(lt_broken_dolly, lt_bone_heap, "east")
    area.exit(lt_bone_heap, lt_broken_dolly, "west")
    area.exit(lt_blast_cleft, sp_drain_slot, "down", hidden=True)
    area.exit(sp_drain_slot, lt_blast_cleft, "up", hidden=True)

    area.exit(hl_haul_link, hl_main_lift, "east")
    area.exit(hl_main_lift, hl_haul_link, "west")
    area.exit(hl_main_lift, hl_chain_gantry, "east")
    area.exit(hl_chain_gantry, hl_main_lift, "west")
    area.exit(hl_chain_gantry, hl_signal_post, "east")
    area.exit(hl_signal_post, hl_chain_gantry, "west")
    area.exit(hl_signal_post, hl_slung_bridge, "east")
    area.exit(hl_slung_bridge, hl_signal_post, "west")
    area.exit(hl_slung_bridge, hl_cradle_platform, "east")
    area.exit(hl_cradle_platform, hl_slung_bridge, "west")
    area.exit(hl_cradle_platform, hl_bell_frame, "east")
    area.exit(hl_bell_frame, hl_cradle_platform, "west")
    area.exit(hl_bell_frame, hl_tarp_walk, "east")
    area.exit(hl_tarp_walk, hl_bell_frame, "west")
    area.exit(hl_tarp_walk, hl_upper_hook, "east")
    area.exit(hl_upper_hook, hl_tarp_walk, "west")
    area.exit(hl_upper_hook, hl_drop_stage, "east")
    area.exit(hl_drop_stage, hl_upper_hook, "west")
    area.exit(hl_drop_stage, hl_ledger_catwalk, "east")
    area.exit(hl_ledger_catwalk, hl_drop_stage, "west")
    area.exit(hl_ledger_catwalk, hl_spoil_overlook, "east")
    area.exit(hl_spoil_overlook, hl_ledger_catwalk, "west")
    area.exit(hl_main_lift, hl_tower_stairs, "north")
    area.exit(hl_tower_stairs, hl_main_lift, "south")
    area.exit(hl_tower_stairs, hl_lift_cab, "up")
    area.exit(hl_lift_cab, hl_tower_stairs, "down")
    area.exit(hl_lift_cab, hl_counterweight_pit, "east")
    area.exit(hl_counterweight_pit, hl_lift_cab, "west")
    area.exit(hl_signal_post, hl_maintenance_bay, "north")
    area.exit(hl_maintenance_bay, hl_signal_post, "south")
    area.exit(hl_maintenance_bay, hl_grease_shed, "east")
    area.exit(hl_grease_shed, hl_maintenance_bay, "west")
    area.exit(hl_bell_frame, hl_slack_line, "north")
    area.exit(hl_slack_line, hl_bell_frame, "south")
    area.exit(hl_slack_line, hl_ledger_catwalk, "northeast")
    area.exit(hl_ledger_catwalk, hl_slack_line, "southwest")
    area.exit(hl_drop_stage, lc_chain_patch, "southeast")
    area.exit(lc_chain_patch, hl_drop_stage, "northwest")
    area.exit(hl_spoil_overlook, sp_black_run, "south")
    area.exit(sp_black_run, hl_spoil_overlook, "north")

    area.exit(sp_black_run, sp_drain_slot, "east")
    area.exit(sp_drain_slot, sp_black_run, "west")
    area.exit(sp_drain_slot, sp_spoil_mound, "east")
    area.exit(sp_spoil_mound, sp_drain_slot, "west")
    area.exit(sp_spoil_mound, sp_ash_pit, "east")
    area.exit(sp_ash_pit, sp_spoil_mound, "west")
    area.exit(sp_ash_pit, sp_tin_shack, "east")
    area.exit(sp_tin_shack, sp_ash_pit, "west")
    area.exit(sp_tin_shack, sp_slurry_bank, "east")
    area.exit(sp_slurry_bank, sp_tin_shack, "west")
    area.exit(sp_slurry_bank, sp_chain_dump, "east")
    area.exit(sp_chain_dump, sp_slurry_bank, "west")
    area.exit(sp_chain_dump, sp_runoff_trench, "east")
    area.exit(sp_runoff_trench, sp_chain_dump, "west")
    area.exit(sp_runoff_trench, sp_weed_gutter, "east")
    area.exit(sp_weed_gutter, sp_runoff_trench, "west")
    area.exit(sp_weed_gutter, sp_burnt_heap, "east")
    area.exit(sp_burnt_heap, sp_weed_gutter, "west")
    area.exit(sp_burnt_heap, sp_cracked_pipe, "east")
    area.exit(sp_cracked_pipe, sp_burnt_heap, "west")
    area.exit(sp_cracked_pipe, sp_buzzard_post, "east")
    area.exit(sp_buzzard_post, sp_cracked_pipe, "west")
    area.exit(sp_buzzard_post, sp_mud_step, "east")
    area.exit(sp_mud_step, sp_buzzard_post, "west")
    area.exit(sp_mud_step, sp_sink_hollow, "east")
    area.exit(sp_sink_hollow, sp_mud_step, "west")
    area.exit(sp_sink_hollow, sp_stake_channel, "east")
    area.exit(sp_stake_channel, sp_sink_hollow, "west")
    area.exit(sp_stake_channel, sp_broken_weir, "east")
    area.exit(sp_broken_weir, sp_stake_channel, "west")
    area.exit(sp_broken_weir, sp_red_sluice, "east")
    area.exit(sp_red_sluice, sp_broken_weir, "west")
    area.exit(sp_red_sluice, sp_camp_backwash, "east")
    area.exit(sp_camp_backwash, sp_red_sluice, "west")
    area.exit(sp_camp_backwash, lc_camp_rim, "east")
    area.exit(lc_camp_rim, sp_camp_backwash, "west")
    area.exit(sp_spoil_mound, sp_slurry_bank, "south")
    area.exit(sp_slurry_bank, sp_spoil_mound, "north")
    area.exit(sp_chain_dump, sp_burnt_heap, "south")
    area.exit(sp_burnt_heap, sp_chain_dump, "north")
    area.exit(sp_runoff_trench, sp_sink_hollow, "south")
    area.exit(sp_sink_hollow, sp_runoff_trench, "north")
    area.exit(sp_buzzard_post, sp_broken_weir, "south")
    area.exit(sp_broken_weir, sp_buzzard_post, "north")
    area.exit(sp_cracked_pipe, sp_red_sluice, "south")
    area.exit(sp_red_sluice, sp_cracked_pipe, "north")

    area.exit(lc_muster_square, lc_payline, "north")
    area.exit(lc_payline, lc_muster_square, "south")
    area.exit(lc_payline, lc_sleep_rows, "north")
    area.exit(lc_sleep_rows, lc_payline, "south")
    area.exit(lc_sleep_rows, lc_quiet_roll, "north")
    area.exit(lc_quiet_roll, lc_sleep_rows, "south")
    area.exit(lc_quiet_roll, lc_tool_lot, "north")
    area.exit(lc_tool_lot, lc_quiet_roll, "south")
    area.exit(lc_tool_lot, lc_chain_patch, "north")
    area.exit(lc_chain_patch, lc_tool_lot, "south")
    area.exit(lc_chain_patch, lc_shift_bell, "north")
    area.exit(lc_shift_bell, lc_chain_patch, "south")
    area.exit(lc_shift_bell, lc_dust_court, "north")
    area.exit(lc_dust_court, lc_shift_bell, "south")
    area.exit(lc_dust_court, lc_water_cart, "north")
    area.exit(lc_water_cart, lc_dust_court, "south")
    area.exit(lc_water_cart, lc_wage_desk, "north")
    area.exit(lc_wage_desk, lc_water_cart, "south")
    area.exit(lc_wage_desk, lc_camp_rim, "north")
    area.exit(lc_camp_rim, lc_wage_desk, "south")
    area.exit(lc_camp_rim, lc_shrine_track, "north")
    area.exit(lc_shrine_track, lc_camp_rim, "south")
    area.exit(lc_muster_square, lc_sutler_tent, "east")
    area.exit(lc_sutler_tent, lc_muster_square, "west")
    area.exit(lc_payline, lc_cookfires, "east")
    area.exit(lc_cookfires, lc_payline, "west")
    area.exit(lc_sleep_rows, lc_nurse_tent, "east")
    area.exit(lc_nurse_tent, lc_sleep_rows, "west")
    area.exit(lc_quiet_roll, lc_bucket_rack, "east")
    area.exit(lc_bucket_rack, lc_quiet_roll, "west")
    area.exit(lc_tool_lot, lc_guard_lane, "east")
    area.exit(lc_guard_lane, lc_tool_lot, "west")
    area.exit(lc_chain_patch, lc_barricade_end, "east")
    area.exit(lc_barricade_end, lc_chain_patch, "west")
    area.exit(lc_water_cart, lc_overseer_step, "east")
    area.exit(lc_overseer_step, lc_water_cart, "west")
    area.exit(lc_wage_desk, lc_latrine_edge, "east")
    area.exit(lc_latrine_edge, lc_wage_desk, "west")
    area.exit(lc_sutler_tent, lc_cookfires, "north")
    area.exit(lc_cookfires, lc_sutler_tent, "south")
    area.exit(lc_cookfires, lc_nurse_tent, "north")
    area.exit(lc_nurse_tent, lc_cookfires, "south")
    area.exit(lc_nurse_tent, lc_bucket_rack, "north")
    area.exit(lc_bucket_rack, lc_nurse_tent, "south")
    area.exit(lc_bucket_rack, lc_guard_lane, "north")
    area.exit(lc_guard_lane, lc_bucket_rack, "south")
    area.exit(lc_guard_lane, lc_barricade_end, "north")
    area.exit(lc_barricade_end, lc_guard_lane, "south")
    area.exit(lc_overseer_step, lc_latrine_edge, "north")
    area.exit(lc_latrine_edge, lc_overseer_step, "south")
    area.exit(lc_shrine_track, sb_outer_shrine, "east")
    area.exit(sb_outer_shrine, lc_shrine_track, "west")
    area.exit(lc_quiet_roll, sb_back_steps, "northeast", hidden=True)
    area.exit(sb_back_steps, lc_quiet_roll, "southwest", hidden=True)

    area.exit(sb_outer_shrine, sb_prayer_steps, "north")
    area.exit(sb_prayer_steps, sb_outer_shrine, "south")
    area.exit(sb_prayer_steps, sb_stripped_porch, "north")
    area.exit(sb_stripped_porch, sb_prayer_steps, "south")
    area.exit(sb_stripped_porch, sb_offering_gut, "north")
    area.exit(sb_offering_gut, sb_stripped_porch, "south")
    area.exit(sb_offering_gut, sb_scar_wall, "north")
    area.exit(sb_scar_wall, sb_offering_gut, "south")
    area.exit(sb_scar_wall, sb_bell_court, "north")
    area.exit(sb_bell_court, sb_scar_wall, "south")
    area.exit(sb_bell_court, sb_ash_apse, "north")
    area.exit(sb_ash_apse, sb_bell_court, "south")
    area.exit(sb_ash_apse, sb_relic_rack, "north")
    area.exit(sb_relic_rack, sb_ash_apse, "south")
    area.exit(sb_relic_rack, sb_witness_stones, "north")
    area.exit(sb_witness_stones, sb_relic_rack, "south")
    area.exit(sb_witness_stones, sb_back_steps, "north")
    area.exit(sb_back_steps, sb_witness_stones, "south")
    area.exit(sb_back_steps, sb_marrow_path, "north")
    area.exit(sb_marrow_path, sb_back_steps, "south")
    area.exit(sb_marrow_path, sb_split_idol, "north")
    area.exit(sb_split_idol, sb_marrow_path, "south")
    area.exit(sb_split_idol, sb_inner_ring, "east")
    area.exit(sb_inner_ring, sb_split_idol, "west")
    area.exit(sb_inner_ring, sb_charred_cells, "east")
    area.exit(sb_charred_cells, sb_inner_ring, "west")
    area.exit(sb_charred_cells, sb_hush_chamber, "east")
    area.exit(sb_hush_chamber, sb_charred_cells, "west")
    area.exit(sb_hush_chamber, sb_cinder_font, "east")
    area.exit(sb_cinder_font, sb_hush_chamber, "west")
    area.exit(sb_cinder_font, sb_broken_sanctum, "east")
    area.exit(sb_broken_sanctum, sb_cinder_font, "west")
    area.exit(sb_broken_sanctum, sb_silent_walk, "east")
    area.exit(sb_silent_walk, sb_broken_sanctum, "west")
    area.exit(sb_silent_walk, sb_scarred_sanctum, "east")
    area.exit(sb_scarred_sanctum, sb_silent_walk, "west")
    area.exit(sb_scarred_sanctum, sb_memorial_cleft, "east")
    area.exit(sb_memorial_cleft, sb_scarred_sanctum, "west")
    area.exit(sb_memorial_cleft, sb_ridge_lookout, "east")
    area.exit(sb_ridge_lookout, sb_memorial_cleft, "west")
    area.exit(sb_ridge_lookout, sb_far_ridge, "east")
    area.exit(sb_far_ridge, sb_ridge_lookout, "west")
    area.exit(sb_scar_wall, sb_inner_ring, "northeast")
    area.exit(sb_inner_ring, sb_scar_wall, "southwest")
    area.exit(sb_bell_court, sb_charred_cells, "northeast")
    area.exit(sb_charred_cells, sb_bell_court, "southwest")
    area.exit(sb_ash_apse, sb_hush_chamber, "northeast")
    area.exit(sb_hush_chamber, sb_ash_apse, "southwest")
    area.exit(sb_relic_rack, sb_cinder_font, "northeast")
    area.exit(sb_cinder_font, sb_relic_rack, "southwest")
    area.exit(sb_witness_stones, sb_broken_sanctum, "southeast")
    area.exit(sb_broken_sanctum, sb_witness_stones, "northwest")
    area.exit(sb_back_steps, sb_silent_walk, "southeast")
    area.exit(sb_silent_walk, sb_back_steps, "northwest")
    area.exit(sb_marrow_path, sb_scarred_sanctum, "northeast")
    area.exit(sb_scarred_sanctum, sb_marrow_path, "southwest")
    area.exit(sb_split_idol, sb_memorial_cleft, "southeast")
    area.exit(sb_memorial_cleft, sb_split_idol, "northwest")

    # ==================================================================
    #  SPAWNS
    # ==================================================================
    area.spawn(sr_guard_shelf, "quarry_thug", count_min=1, count_max=1, respawn_minutes=24, respawn_variance=6)
    area.spawn(sr_broken_cart, "slag_hound", count_min=1, count_max=1, respawn_minutes=22, respawn_variance=6)
    area.spawn(sr_shock_gully, "scree_harrier", count_min=1, count_max=1, respawn_minutes=18, respawn_variance=4)
    area.spawn(lt_first_terrace, "quarry_thug", count_min=1, count_max=2, respawn_minutes=24, respawn_variance=6)
    area.spawn(lt_red_chute, "camp_overseer", count_min=1, count_max=1, respawn_minutes=28, respawn_variance=8)
    area.spawn(lt_shiver_cut, "cutface_burrower", count_min=1, count_max=1, respawn_minutes=22, respawn_variance=5)
    area.spawn(lt_blast_cleft, "cutface_burrower", count_min=0, count_max=1, respawn_minutes=23, respawn_variance=5)
    area.spawn(lt_memorial_slab, "slag_hound", count_min=0, count_max=1, respawn_minutes=24, respawn_variance=6)
    area.spawn(hl_signal_post, "camp_overseer", count_min=1, count_max=1, respawn_minutes=27, respawn_variance=7)
    area.spawn(hl_counterweight_pit, "cutface_burrower", count_min=1, count_max=1, respawn_minutes=22, respawn_variance=5)
    area.spawn(hl_slack_line, "scree_harrier", count_min=1, count_max=1, respawn_minutes=18, respawn_variance=4)
    area.spawn(sp_ash_pit, "slag_hound", count_min=1, count_max=2, respawn_minutes=24, respawn_variance=6)
    area.spawn(sp_runoff_trench, "cutface_burrower", count_min=1, count_max=1, respawn_minutes=21, respawn_variance=5)
    area.spawn(sp_buzzard_post, "scree_harrier", count_min=1, count_max=1, respawn_minutes=18, respawn_variance=4)
    area.spawn(sp_red_sluice, "relic_raider", count_min=1, count_max=1, respawn_minutes=25, respawn_variance=6)
    area.spawn(lc_guard_lane, "camp_overseer", count_min=1, count_max=1, respawn_minutes=28, respawn_variance=8)
    area.spawn(lc_barricade_end, "quarry_thug", count_min=1, count_max=2, respawn_minutes=24, respawn_variance=6)
    area.spawn(lc_latrine_edge, "slag_hound", count_min=1, count_max=1, respawn_minutes=23, respawn_variance=6)
    area.spawn(sb_stripped_porch, "relic_raider", count_min=1, count_max=1, respawn_minutes=25, respawn_variance=6)
    area.spawn(sb_hush_chamber, "cutface_burrower", count_min=1, count_max=1, respawn_minutes=22, respawn_variance=5)
    area.spawn(sb_memorial_cleft, "stone_golem_fragment", count_min=0, count_max=1, respawn_minutes=40, respawn_variance=10)

    # ==================================================================
    #  NAMED MOBS
    # ==================================================================
    area.named_mob(
        "stonewake_bailiff_torren",
        hl_ledger_catwalk,
        respawn_minutes=180,
        respawn_variance=40,
        prestige_modifier=2.2,
        behavior=["territorial"],
        base_disposition=-0.9,
        flee_threshold=5,
        tome_drop="ironvein_requisition_tome",
    )
    area.named_mob(
        "scarwarden_saelen_dross",
        sb_scarred_sanctum,
        respawn_minutes=220,
        respawn_variance=45,
        prestige_modifier=2.3,
        behavior=["guardian"],
        base_disposition=-1.0,
        flee_threshold=0,
        tome_drop="ironvein_shrine_tome",
    )

    # ==================================================================
    #  NPCS
    # ==================================================================
    area.npc(sr_gate_grade, "npc_gate_sergeant_dar", faction="empire")
    area.npc(hl_signal_post, "npc_haul_clerk_siven", faction="empire")
    area.npc(hl_maintenance_bay, "npc_chainwright_pela", faction="consortium")
    area.npc(lt_marker_wall, "npc_blast_scout_orme", faction="circle")
    area.npc(sp_runoff_trench, "npc_runoff_picker_nella")
    _sutler = area.npc(lc_sutler_tent, "npc_sutler_dera", faction="consortium")
    area.vendor(
        _sutler,
        accepts=["consumable", "tool"],
        item_ids=[
            "pickaxe",
            "trail_rations",
            "bandage",
            "minor_healing_potion",
            "minor_stamina_potion",
            "antidote_potion",
        ],
        faction="consortium",
    )
    area.npc(lt_memorial_slab, "npc_memorial_reader_cast")
    area.npc(lc_nurse_tent, "npc_shift_nurse_verin")
    area.npc(hl_main_lift, "npc_lift_tender_jorad", faction="consortium")
    area.npc(lt_tool_house, "npc_quarry_copyist_mael", faction="empire")
    area.npc(sb_witness_stones, "npc_shrine_witness_esa")
    area.npc(lc_wage_desk, "npc_payclerk_rull", faction="consortium")

    # ==================================================================
    #  ITEMS
    # ==================================================================
    area.item(
        "stamped_requisition_copy",
        key="Stamped Requisition Copy",
        item_type="item",
        weight=0.2,
        rarity="normal",
        value=0,
        is_quest_item=True,
        desc="A copied requisition leaf showing memorial stone, chain iron, and labor deductions quietly folded into the same Stonewake order.",
    )
    area.item(
        "runoff_sample_satchel",
        key="Runoff Sample Satchel",
        item_type="item",
        weight=0.2,
        rarity="normal",
        value=0,
        is_quest_item=True,
        desc="A sealed satchel of red slurry, weed growth, and chalk sediment gathered from the spoil runoff for Circle review.",
    )

    # ==================================================================
    #  LORE FRAGMENTS
    # ==================================================================
    area.lore_fragment(
        "ie_lore_requisition_board",
        sr_marker_post,
        discovery_method="search",
        scholar_path="arcana",
        text="The load board cites the Iron Vein Requisition of 734 as emergency necessity, then quietly assigns House Talvere paving priority over burial stone and camp timber.",
        insight_gain=2,
    )
    area.lore_fragment(
        "ie_lore_memorial_dust",
        lt_memorial_slab,
        discovery_method="search",
        scholar_path="remnance",
        text="Dust caught in the slab's cuts preserves names erased beneath civic lime. A smaller note beside them reads: copy accepted in place of stone, memorial charge reassigned without witness.",
        insight_gain=3,
    )
    area.lore_fragment(
        "ie_lore_cutface_marks",
        lt_marker_wall,
        discovery_method="search",
        scholar_path="resonance",
        text="Older cut-face numbers run on a rhythm the present wall only imitates. The newer measured rod seals mark ownership, not authorship.",
        insight_gain=2,
    )
    area.lore_fragment(
        "ie_lore_chain_manifest",
        hl_ledger_catwalk,
        discovery_method="search",
        scholar_path="arcana",
        text="A haul manifest stamped with the split roadwheel and stonewake pickmark counts chains, lift teeth, and missing crew in the same column of replaceable losses.",
        insight_gain=2,
    )
    area.lore_fragment(
        "ie_lore_shift_bell",
        hl_bell_frame,
        discovery_method="search",
        scholar_path="remnance",
        text="The bell roster records stoppages for weather, chain failure, and death. Names are given for broken lift parts more consistently than for broken workers.",
        insight_gain=2,
    )
    area.lore_fragment(
        "ie_lore_spoil_count",
        sp_red_sluice,
        discovery_method="search",
        scholar_path="arcana",
        text="A sluice slate orders runoff diverted around the lower camp during inspections so the labor rows appear cleaner than the trench remembers.",
        insight_gain=2,
    )
    area.lore_fragment(
        "ie_lore_labor_roll",
        lc_quiet_roll,
        discovery_method="search",
        scholar_path="remnance",
        text="A hidden camp roll lists the same absent workers across three shifts with the note disposition omitted by instruction. The official bell sheets simply close the space.",
        insight_gain=3,
    )
    area.lore_fragment(
        "ie_lore_pay_deduction",
        lc_wage_desk,
        discovery_method="search",
        scholar_path="arcana",
        text="Pay tallies dock workers for damaged tools, memorial chalk, and ration overages while Stonewake haul bonuses pass upward untouched.",
        insight_gain=2,
    )
    area.lore_fragment(
        "ie_lore_shrine_scar",
        sb_scar_wall,
        discovery_method="search",
        scholar_path="resonance",
        text="The scar wall still holds prayer grooves beneath the revised charter cuts. Someone removed devotion here by chisel, not by forgetting.",
        insight_gain=2,
    )
    area.lore_fragment(
        "ie_lore_removed_prayer",
        sb_cinder_font,
        discovery_method="search",
        scholar_path="arcana",
        text="A half-burned slip in the font asks that the hill be returned to witness rather than measure. Below it, a later office hand writes: prior text removed.",
        insight_gain=3,
    )

    # ==================================================================
    #  QUESTS
    # ==================================================================
    area.quest(
        "ie_q_requisition_copy",
        name="Requisition Copy",
        description="Quarry Copyist Mael wants a copied requisition page delivered up the haul line before the memorial charges are folded back into acceptable totals.",
        quest_type="delivery",
        quest_giver="npc_quarry_copyist_mael",
        objectives=[
            {
                "type": "deliver",
                "target": "npc_haul_clerk_siven",
                "count": 1,
                "description": "Deliver the stamped requisition copy to Haul Clerk Siven",
            },
        ],
        flagged_drop="stamped_requisition_copy",
        rewards=[
            {"action_type": "give_scales", "amount": 80},
            {"action_type": "modify_standing", "faction_id": "empire", "delta": 80},
            {"action_type": "echo", "message": "|gMael lowers his voice. \"Good. Numbers rot faster when nobody carries them between offices.\"|n"},
        ],
        next_quest_id="ie_q_stonewake_due",
        objective_type="deliver",
        objective_target="npc_haul_clerk_siven",
        objective_count=1,
    )
    area.quest(
        "ie_q_cutline_discipline",
        name="Cutline Discipline",
        description="Shift Nurse Verin wants the overseers bloodied enough to stop driving injured crews back onto the red chutes before the splints are tied.",
        quest_type="kill",
        quest_giver="npc_shift_nurse_verin",
        objectives=[
            {
                "type": "kill",
                "target": "camp_overseer",
                "count": 3,
                "description": "Defeat camp overseers beating crews back to work",
            },
        ],
        rewards=[
            {"action_type": "give_scales", "amount": 95},
            {"action_type": "modify_standing", "faction_id": "consortium", "delta": 55},
            {"action_type": "echo", "message": "|gVerin ties off a bandage with brutal care. \"Pain teaches fast when orders finally answer to it.\"|n"},
        ],
        objective_type="kill",
        objective_target="camp_overseer",
        objective_count=3,
    )
    area.quest(
        "ie_q_tally_the_dead",
        name="Tally the Dead",
        description="Memorial Reader Cast needs proof that the quarry keeps erasing the same names from slab, camp, and shrine alike. Trace the pattern before it is cleaned again.",
        quest_type="investigation",
        quest_giver="npc_memorial_reader_cast",
        objectives=[
            {
                "type": "investigate",
                "target": "lt_memorial_slab",
                "count": 1,
                "description": "Inspect the memorial slab on the upper terrace",
            },
            {
                "type": "investigate",
                "target": "lc_quiet_roll",
                "count": 1,
                "description": "Search the quiet roll behind the labor rows",
            },
            {
                "type": "investigate",
                "target": "sb_memorial_cleft",
                "count": 1,
                "description": "Find the hidden memorial cleft in the shrine belt",
            },
        ],
        rewards=[
            {"action_type": "give_scales", "amount": 90},
            {"action_type": "modify_standing", "faction_id": "circle", "delta": 65},
            {"action_type": "echo", "message": "|gCast brushes chalk from his fingers. \"A buried name is still a line in the ledger, if someone keeps reading.\"|n"},
        ],
        objective_type="investigate",
        objective_target="lt_memorial_slab",
        objective_count=3,
    )
    area.quest(
        "ie_q_runoff_sample",
        name="Runoff Sample",
        description="Runoff Picker Nella has scraped together a slurry sample that needs to reach Blast Scout Orme before the ditch is drained and the evidence goes with it.",
        quest_type="delivery",
        quest_giver="npc_runoff_picker_nella",
        objectives=[
            {
                "type": "deliver",
                "target": "npc_blast_scout_orme",
                "count": 1,
                "description": "Deliver the runoff sample satchel to Blast Scout Orme",
            },
        ],
        flagged_drop="runoff_sample_satchel",
        rewards=[
            {"action_type": "give_scales", "amount": 85},
            {"action_type": "modify_standing", "faction_id": "circle", "delta": 85},
            {"action_type": "echo", "message": "|gNella wipes red water from her wrists. \"Good. Let them test what the camp has been drinking for years.\"|n"},
        ],
        next_quest_id="ie_q_scarred_sanctum",
        objective_type="deliver",
        objective_target="npc_blast_scout_orme",
        objective_count=1,
    )
    area.quest(
        "ie_q_stonewake_due",
        name="Stonewake Due",
        description="Haul Clerk Siven says Bailiff Torren keeps the real deductions on the catwalk above the lift. Put him down before another shift is balanced against the dead.",
        quest_type="kill",
        quest_giver="npc_haul_clerk_siven",
        prerequisite_quests=["ie_q_requisition_copy"],
        objectives=[
            {
                "type": "kill",
                "target": "stonewake_bailiff_torren",
                "count": 1,
                "description": "Defeat Stonewake Bailiff Torren on the lift catwalk",
            },
        ],
        rewards=[
            {"action_type": "give_scales", "amount": 135},
            {"action_type": "modify_standing", "faction_id": "empire", "delta": 110},
            {"action_type": "echo", "message": "|gSiven studies the recovered tally slips. \"There it is. The city asked for stone, and he turned people into part of the freight.\"|n"},
        ],
        objective_type="kill",
        objective_target="stonewake_bailiff_torren",
        objective_count=1,
    )
    area.quest(
        "ie_q_scarred_sanctum",
        name="Scarred Sanctum",
        description="Shrine Witness Esa believes the deepest sanctum will stay under quarry claim until its chosen warden is broken. Go to the heart of the stripped belt and end the watch.",
        quest_type="kill",
        quest_giver="npc_shrine_witness_esa",
        prerequisite_quests=["ie_q_runoff_sample"],
        objectives=[
            {
                "type": "kill",
                "target": "scarwarden_saelen_dross",
                "count": 1,
                "description": "Defeat Scarwarden Saelen Dross in the scarred sanctum",
            },
        ],
        rewards=[
            {"action_type": "give_scales", "amount": 125},
            {"action_type": "modify_standing", "faction_id": "circle", "delta": 95},
            {"action_type": "echo", "message": "|gEsa presses a chalk-marked palm to the stone. \"That is better. Witness can breathe again, even here.\"|n"},
        ],
        objective_type="kill",
        objective_target="scarwarden_saelen_dross",
        objective_count=1,
    )

    # ==================================================================
    #  GATHERING POOLS
    # ==================================================================
    area.gathering_pool(
        "ore",
        rooms=["lt_red_chute", "lt_upper_terrace", "hl_counterweight_pit", "sp_ash_pit"],
        materials=["ironvein_ore", "bench_slate"],
        max_active=4,
        respawn_minutes=14,
        respawn_variance=4,
    )
    area.gathering_pool(
        "forage",
        rooms=["sr_chain_berm", "hl_maintenance_bay", "sp_chain_dump", "sb_memorial_cleft"],
        materials=["haul_chain_link", "memorial_chalk"],
        max_active=4,
        respawn_minutes=12,
        respawn_variance=3,
    )
    area.gathering_pool(
        "herb",
        rooms=["sp_runoff_trench", "sp_weed_gutter", "sp_sink_hollow", "sb_cinder_font"],
        materials=["runoff_cress"],
        max_active=3,
        respawn_minutes=10,
        respawn_variance=3,
    )
    area.gathering_pool(
        "hide",
        rooms=["sr_broken_cart", "lt_memorial_slab", "sp_ash_pit", "lc_latrine_edge"],
        materials=["slag_hound_hide"],
        max_active=3,
        respawn_minutes=16,
        respawn_variance=5,
    )

    return area.build()
