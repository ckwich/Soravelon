"""
Crownroad North -- Hub 4 exterior zone

The capital's overland artery outside Varath Prime. Checkpoints, relay yards,
shrine pull-offs, dead camps, caravan sidings, and survey strips show how the
Empire turns movement into paperwork, delay, and selective disappearance.
"""

from world.area_builder import AreaBuilder


def build():
    area = AreaBuilder("crownroad_north")

    # ------------------------------------------------------------------
    # Zone setup
    # ------------------------------------------------------------------
    area.zone(
        name="Crownroad North",
        zone_type="frontier",
        continent="varath",
        tier=4,
        region="crownlands",
        hub_city="varath_prime",
        faction_territory="imperial",
        faction_presence=["empire", "consortium", "circle"],
        world_x=180,
        world_y=-88,
        world_radius=120,
    )

    # ------------------------------------------------------------------
    # Materials
    # ------------------------------------------------------------------
    area.material(
        "roadsage",
        tier=1,
        terrain="roadside",
        absorbed_property="clarity",
        profession_bonus={"alchemy": 0.1},
    )
    area.material(
        "mileglass_lichen",
        tier=1,
        terrain="masonry",
        absorbed_property="precision",
        profession_bonus={"alchemy": 0.05, "scholarship": 0.05},
    )
    area.material(
        "milestone_iron",
        tier=1,
        terrain="stone",
        absorbed_property="hardite",
        profession_bonus={"smithing": 0.1},
    )
    area.material(
        "relay_scrap",
        tier=1,
        terrain="yard",
        absorbed_property="durability",
        profession_bonus={"smithing": 0.05},
    )
    area.material(
        "charter_reed",
        tier=1,
        terrain="ditch",
        absorbed_property=None,
        profession_bonus={"cooking": 0.05},
    )
    area.material(
        "dust_hound_hide",
        tier=1,
        terrain="roadside",
        absorbed_property="tenacity",
        profession_bonus={"leatherworking": 0.1},
    )

    # ==================================================================
    #  OUTER MILESTONES
    # ==================================================================
    om_gate_verge = area.room(
        "om_gate_verge",
        name="Gate Verge",
        desc=(
            "Beyond the measured arch of Varath Prime, the Crownroad widens "
            "into a stony verge scored by wagon ruts and hoofprints. Milebars "
            "and levy posts crowd the shoulder, reminding travelers that the "
            "road is watched before it is welcomed."
        ),
        room_type="path",
        indoor=False,
        ambient_echoes=[
            "A clerk's bell rings behind the gate, followed by the scrape of a copied seal.",
            "Wagons clatter over the first run of paving outside the capital.",
        ],
    )
    om_first_milestone = area.room(
        "om_first_milestone",
        name="First Milestone",
        desc=(
            "A waist-high road stone marks the first counted stretch beyond "
            "the capital. The face now bearing the measured rod seal was "
            "flattened and recut; older chisel lines still catch dust below "
            "the official wording."
        ),
        room_type="path",
        indoor=False,
    )
    om_kingbar_ditch = area.room(
        "om_kingbar_ditch",
        name="Kingbar Ditch",
        desc=(
            "Drainage ditches lined with old brick hold a trickle of brown "
            "water and a scatter of broken tally sticks. Cart wheels have "
            "chewed the shoulder down to stone and clay."
        ),
        room_type="path",
        indoor=False,
    )
    om_measure_bank = area.room(
        "om_measure_bank",
        name="Measure Bank",
        desc=(
            "A raised bank on the roadside gives clerks a clear line of sight "
            "over incoming caravans. Survey rods rest in iron cradles beside "
            "boards quoting the Edict of Measured Passage in careful, bloodless "
            "phrasing."
        ),
        room_type="path",
        indoor=False,
    )
    om_culvert_bridge = area.room(
        "om_culvert_bridge",
        name="Culvert Bridge",
        desc=(
            "The road crosses a narrow culvert of fitted stone older than the "
            "current paving above it. Moss clings in the joints where the newer "
            "mortar never quite took."
        ),
        room_type="path",
        indoor=False,
    )
    om_wayline_rise = area.room(
        "om_wayline_rise",
        name="Wayline Rise",
        desc=(
            "The Crownroad climbs a low rise from which the capital's outer "
            "walls and towers remain visible behind you. Ahead, the road is "
            "less a path than a ruled line drawn through field, ditch, and camp."
        ),
        room_type="path",
        indoor=False,
    )
    om_talon_post = area.room(
        "om_talon_post",
        name="Talon Post",
        desc=(
            "A relay post bearing the talon-and-bar seal stands beside the road, "
            "its message board crowded with notices, delays, and corrected run "
            "times. Most are copied in the same steady ministry hand."
        ),
        room_type="path",
        indoor=False,
    )
    om_stonebench_pull = area.room(
        "om_stonebench_pull",
        name="Stonebench Pull-Off",
        desc=(
            "Travelers pause here beneath a pair of stone benches set into the "
            "road shoulder. The benches face a view of ditch, marker, and wall "
            "rather than any pleasant prospect."
        ),
        room_type="clearing",
        indoor=False,
    )
    om_reed_swale = area.room(
        "om_reed_swale",
        name="Reed Swale",
        desc=(
            "A wet swale sags away from the road, thick with pale reeds and "
            "lichen-spotted marker stones. Bits of wax and twine wash down here "
            "from opened packets and broken travel seals."
        ),
        room_type="clearing",
        indoor=False,
    )
    om_marker_fence = area.room(
        "om_marker_fence",
        name="Marker Fence",
        desc=(
            "A line of repaired post markers hems the wet ground, each head "
            "painted with measured numbers and route warnings. The newest posts "
            "lean because their holes were cut in older stone fill."
        ),
        room_type="path",
        indoor=False,
    )
    om_old_shed = area.room(
        "om_old_shed",
        name="Old Measure Shed",
        desc=(
            "This small roadside shed once held field tools and tarps. Now its "
            "door hangs crooked, and the floor is a mat of straw, old papers, "
            "and animal hair."
        ),
        room_type="building",
        indoor=True,
    )
    om_teamster_fire = area.room(
        "om_teamster_fire",
        name="Teamster Fire",
        desc=(
            "A blackened fire ring sits in a wind-cut hollow just off the road. "
            "The ash is mixed with boot nails, cracked wax, and scraps from "
            "copied manifests burned after use."
        ),
        room_type="clearing",
        indoor=False,
    )
    om_dry_rut = area.room(
        "om_dry_rut",
        name="Dry Rut",
        desc=(
            "Parallel wagon ruts harden here into shallow troughs packed with "
            "powdered stone. The roadside grass is trampled low by animals led "
            "off the road to wait out inspections."
        ),
        room_type="path",
        indoor=False,
    )
    om_copy_stone = area.room(
        "om_copy_stone",
        name="Copy Stone",
        desc=(
            "A broad slab lies beside the road where official texts are copied "
            "before being posted farther out. Thin scratches beneath the current "
            "charter lines show older wording pared away and replaced."
        ),
        room_type="ruins",
        indoor=False,
    )
    om_roadside_well = area.room(
        "om_roadside_well",
        name="Roadside Well",
        desc=(
            "A capped stone well offers brackish water to caravans and clerks "
            "alike. The curb is worn smooth by bucket ropes and the resting "
            "weight of sealed dispatch satchels."
        ),
        room_type="clearing",
        indoor=False,
    )
    om_tally_hollow = area.room(
        "om_tally_hollow",
        name="Tally Hollow",
        desc=(
            "A shallow depression off the road is littered with snapped tally "
            "slats and discarded permit ties. Travelers step around it as if "
            "whatever happened here were still official business."
        ),
        room_type="clearing",
        indoor=False,
    )
    om_checkpoint_approach = area.room(
        "om_checkpoint_approach",
        name="Checkpoint Approach",
        desc=(
            "The road narrows toward a chained barrier ahead where the first "
            "full checkpoint breaks the flow of traffic into ordered lanes. "
            "Warning boards promise fairness and delay in the same breath."
        ),
        room_type="path",
        indoor=False,
    )

    # ==================================================================
    #  CHECKPOINT CHAIN
    # ==================================================================
    cc_south_bar = area.room(
        "cc_south_bar",
        name="South Chain Bar",
        desc=(
            "A timber boom and chain force travelers into file beneath the eyes "
            "of spear-bearing road guards. Splintered side rails show how often "
            "frustrated teamsters test the edges."
        ),
        room_type="path",
        indoor=False,
    )
    cc_permit_lane = area.room(
        "cc_permit_lane",
        name="Permit Lane",
        desc=(
            "Painted stones divide the checkpoint into permit, levy, and impound "
            "lanes. The permit line is longest, slowest, and watched by the "
            "quietest clerks."
        ),
        room_type="path",
        indoor=False,
    )
    cc_scriber_steps = area.room(
        "cc_scriber_steps",
        name="Scriber Steps",
        desc=(
            "A short stair climbs to a narrow desk platform where names, routes, "
            "and cargo tallies are copied into damp books. Ink stains blacken the "
            "stone underfoot."
        ),
        room_type="building",
        indoor=True,
    )
    cc_inspection_yard = area.room(
        "cc_inspection_yard",
        name="Inspection Yard",
        desc=(
            "Wagons stand open here while guards probe under tarps and between "
            "crates. The whole yard smells of lamp oil, damp rope, and the fear "
            "of having the wrong paper at the wrong hour."
        ),
        room_type="clearing",
        indoor=False,
    )
    cc_watch_berm = area.room(
        "cc_watch_berm",
        name="Watch Berm",
        desc=(
            "A compacted earthen berm lifts the road above the surrounding lanes. "
            "From here a sergeant can watch both the approach and the cages without "
            "raising their voice."
        ),
        room_type="path",
        indoor=False,
    )
    cc_barrack_walk = area.room(
        "cc_barrack_walk",
        name="Barrack Walk",
        desc=(
            "A plank walk runs along the outside of the checkpoint barracks. Wet "
            "boots, ration crates, and practice staves crowd the boards."
        ),
        room_type="path",
        indoor=False,
    )
    cc_bunkroom = area.room(
        "cc_bunkroom",
        name="Checkpoint Bunkroom",
        desc=(
            "Triple bunks fill this long room, each footlocker marked with chalked "
            "initials and shift numbers. The air is stale with sweat, polish, and "
            "old resentment."
        ),
        room_type="building",
        indoor=True,
    )
    cc_ration_shed = area.room(
        "cc_ration_shed",
        name="Ration Shed",
        desc=(
            "Salt meat casks, biscuit sacks, and water crocks are stacked in strict "
            "rows beneath a roof patched with tarred canvas. A clipped ledger notes "
            "every missing ladle and cracked cup."
        ),
        room_type="building",
        indoor=True,
    )
    cc_impound_pens = area.room(
        "cc_impound_pens",
        name="Impound Pens",
        desc=(
            "Fenced pens hold seized wagons, draft animals, and goods awaiting "
            "correction or disappearance. Tags tied to the rails bear the split "
            "roadwheel stamp of the High Registry."
        ),
        room_type="clearing",
        indoor=False,
    )
    cc_confiscation_cage = area.room(
        "cc_confiscation_cage",
        name="Confiscation Cage",
        desc=(
            "A barred cage of iron and heavy timber stores seized satchels, sealed "
            "rolls, and bound travel trunks. The labels are precise, the reasons "
            "for seizure less so."
        ),
        room_type="building",
        indoor=True,
    )
    cc_levy_booth = area.room(
        "cc_levy_booth",
        name="Levy Booth",
        desc=(
            "A narrow booth with shuttered windows collects scales for passage, delay, "
            "storage, and whatever fee the clerk can plausibly fit beneath the decree."
        ),
        room_type="building",
        indoor=True,
    )
    cc_side_ditch = area.room(
        "cc_side_ditch",
        name="Side Ditch",
        desc=(
            "The checkpoint's runoff empties into a shallow ditch thick with torn "
            "paper, lye ash, and the smell of wet leather. Footprints suggest more "
            "traffic here than any maintenance route should see."
        ),
        room_type="path",
        indoor=False,
    )
    cc_broken_culvert = area.room(
        "cc_broken_culvert",
        name="Broken Culvert",
        desc=(
            "A cracked culvert mouth opens under the checkpoint edge where older "
            "stonework meets newer fill. Water taps quietly through the break, and "
            "someone has scraped fresh mud away from a narrow crawl."
        ),
        room_type="underground",
        indoor=True,
    )
    cc_signal_walk = area.room(
        "cc_signal_walk",
        name="Signal Walk",
        desc=(
            "A raised walk connects the checkpoint proper to a signal mast and relay "
            "frame. Lantern hooks and shutter arms let officers mark delay, seizure, "
            "or privileged passage at a distance."
        ),
        room_type="path",
        indoor=False,
    )
    cc_captains_office = area.room(
        "cc_captains_office",
        name="Captain's Office",
        desc=(
            "Maps, levy slates, and impound ledgers cover every flat surface in this "
            "office. The walls display no honors, only route timings and lists of "
            "corrected names."
        ),
        room_type="building",
        indoor=True,
    )
    cc_archive_rack = area.room(
        "cc_archive_rack",
        name="Archive Rack",
        desc=(
            "Shelves of tied permit bundles climb to the rafters. Some bundles are "
            "fresh and orderly, others bound with replacement twine after earlier "
            "contents were removed by instruction."
        ),
        room_type="building",
        indoor=True,
    )
    cc_far_bar = area.room(
        "cc_far_bar",
        name="Far Chain Bar",
        desc=(
            "The northern face of the checkpoint sends traffic back into open road by "
            "means of another boom and chain. Travelers leaving the barrier do so more "
            "slowly than they arrived."
        ),
        room_type="path",
        indoor=False,
    )

    # ==================================================================
    #  RELAY HOSTEL YARDS
    # ==================================================================
    ry_road_gate = area.room(
        "ry_road_gate",
        name="Relay Road Gate",
        desc=(
            "A low gate of iron-banded timber opens from the checkpoint road into the "
            "relay enclosure. Posted rules limit fires, shouting, and the handling of "
            "sealed traffic outside assigned tables."
        ),
        room_type="path",
        indoor=False,
    )
    ry_courier_lane = area.room(
        "ry_courier_lane",
        name="Courier Lane",
        desc=(
            "Packed earth and stable grit mark the lane reserved for courier teams, "
            "registry runners, and favored wagons. The lane is swept more often than "
            "the public road."
        ),
        room_type="path",
        indoor=False,
    )
    ry_hostel_court = area.room(
        "ry_hostel_court",
        name="Hostel Court",
        desc=(
            "A square of trampled yard sits between the relay hostel, the cookhouse, "
            "and the stable ring. Travelers with honest papers rest here beneath the "
            "eyes of staff who remember everything."
        ),
        room_type="clearing",
        indoor=False,
    )
    ry_common_room = area.room(
        "ry_common_room",
        name="Hostel Common Room",
        desc=(
            "Long benches and scarred tables fill the hostel common room. Most talk "
            "drops when a clerk or courier comes in carrying sealed work."
        ),
        room_type="building",
        indoor=True,
    )
    ry_loft_bunks = area.room(
        "ry_loft_bunks",
        name="Loft Bunks",
        desc=(
            "The loft holds stacked bunks for drovers, runners, and those waiting for "
            "morning release from the checkpoint. Sleep is thin here; the yard noise "
            "never truly stops."
        ),
        room_type="building",
        indoor=True,
    )
    ry_ledger_desk = area.room(
        "ry_ledger_desk",
        name="Guest Ledger Desk",
        desc=(
            "A small desk under a shuttered window records arrivals, rooms, feed, and "
            "sealed packet transfers. Several leaves have been cut out cleanly with a "
            "knife."
        ),
        room_type="building",
        indoor=True,
    )
    ry_stable_ring = area.room(
        "ry_stable_ring",
        name="Stable Ring",
        desc=(
            "Feed troughs, hitch posts, and tack rails ring this broad stable court. "
            "Animals breathe steam into the air while hostlers argue over assignments "
            "and delays."
        ),
        room_type="clearing",
        indoor=False,
    )
    ry_fodder_shed = area.room(
        "ry_fodder_shed",
        name="Fodder Shed",
        desc=(
            "Hay bales and grain sacks are stacked beneath a low roof blackened by old "
            "smoke. A chalk board tracks shortages against caravan declarations."
        ),
        room_type="building",
        indoor=True,
    )
    ry_post_kitchen = area.room(
        "ry_post_kitchen",
        name="Post Kitchen",
        desc=(
            "The relay kitchen runs on stewpots, black bread, and whatever can be fed "
            "quickly to people who cannot afford to linger. Steam beads on every beam."
        ),
        room_type="building",
        indoor=True,
    )
    ry_back_paddock = area.room(
        "ry_back_paddock",
        name="Back Paddock",
        desc=(
            "A rough paddock behind the hostel holds overworked teams and overflow stock. "
            "Broken traces and chewed tether posts lie half-buried in the mud."
        ),
        room_type="clearing",
        indoor=False,
    )
    ry_wash_line = area.room(
        "ry_wash_line",
        name="Wash Line",
        desc=(
            "Sheets, saddle cloths, and stable rags hang between poles beside a runnel "
            "of grey water. The wind carries soap, dung, and boiled starch in equal parts."
        ),
        room_type="clearing",
        indoor=False,
    )
    ry_dispatch_board = area.room(
        "ry_dispatch_board",
        name="Dispatch Board",
        desc=(
            "A sheltered board lists relay times, courier transfers, and approved holds "
            "under the talon-and-bar seal of Thirteenth Talon Command. Several routes are "
            "crossed out and recopied beneath."
        ),
        room_type="path",
        indoor=False,
    )
    ry_farrier_nook = area.room(
        "ry_farrier_nook",
        name="Farrier Nook",
        desc=(
            "A compact work space holds hoof knives, spare shoes, and a brazier kept at a "
            "constant red glow. Hammer marks have dented the wall planks smooth."
        ),
        room_type="building",
        indoor=True,
    )
    ry_wagon_shelter = area.room(
        "ry_wagon_shelter",
        name="Wagon Shelter",
        desc=(
            "A roofed lean-to shelters relay carts and a few private wagons whose owners "
            "paid for quicker service. The wheels nearest the post are always the cleanest."
        ),
        room_type="building",
        indoor=False,
    )
    ry_team_dormer = area.room(
        "ry_team_dormer",
        name="Team Dormer",
        desc=(
            "This narrow dormer room gives relay drivers a few hours of privacy from the "
            "yard. Boots, bedrolls, and patched cloaks hang from every peg."
        ),
        room_type="building",
        indoor=True,
    )
    ry_far_yard = area.room(
        "ry_far_yard",
        name="Far Yard",
        desc=(
            "The relay enclosure thins here into hitch posts, wheel tracks, and stacks of "
            "emptied feed sacks. Beyond it the road takes on the tired feel of distance again."
        ),
        room_type="clearing",
        indoor=False,
    )
    ry_relay_verge = area.room(
        "ry_relay_verge",
        name="Relay Verge",
        desc=(
            "A low verge edged with broken paving marks the point where relay order gives way "
            "to chapel lay-bys and abandoned campfires. Dispatch slates nailed to a post rattle "
            "in the wind."
        ),
        room_type="path",
        indoor=False,
    )

    # ==================================================================
    #  SHRINE PULL-OFFS AND DEAD CAMPS
    # ==================================================================
    sd_layby_turn = area.room(
        "sd_layby_turn",
        name="Lay-By Turn",
        desc=(
            "The road broadens around an old pull-off once meant for pilgrims and state messengers. "
            "Its paving is broken by newer patchwork and the ash from too many roadside fires."
        ),
        room_type="path",
        indoor=False,
    )
    sd_waychapel_steps = area.room(
        "sd_waychapel_steps",
        name="Waychapel Steps",
        desc=(
            "Stone steps climb to a roadside chapel built into the slope beside the Crownroad. "
            "Official plaques speak of safe passage, but the candle niches are almost all empty."
        ),
        room_type="ruins",
        indoor=False,
    )
    sd_ash_bell = area.room(
        "sd_ash_bell",
        name="Ash Bell",
        desc=(
            "A cracked bell hangs in a soot-streaked frame over the chapel yard. Wind passing the "
            "fracture makes a small, unhappy note instead of a proper call."
        ),
        room_type="ruins",
        indoor=False,
    )
    sd_offertory_wall = area.room(
        "sd_offertory_wall",
        name="Offertory Wall",
        desc=(
            "A low wall holds bowls for wax, coin, and written petitions. The petitions left here "
            "are folded with care, as if order in the hand might persuade order in the state."
        ),
        room_type="ruins",
        indoor=False,
    )
    sd_prayer_shelf = area.room(
        "sd_prayer_shelf",
        name="Prayer Shelf",
        desc=(
            "A rock-cut shelf in the chapel side bears guttered candles, reed charms, and copied route "
            "blessings. The newest blessings are ministry copies, not older local verse."
        ),
        room_type="ruins",
        indoor=False,
    )
    sd_pilgrim_ditch = area.room(
        "sd_pilgrim_ditch",
        name="Pilgrim Ditch",
        desc=(
            "A shallow ditch runs behind the chapel where travelers once camped for the night. Wet grass "
            "and flattened reed mats show that some still do, though not comfortably."
        ),
        room_type="clearing",
        indoor=False,
    )
    sd_deadcamp_edge = area.room(
        "sd_deadcamp_edge",
        name="Dead Camp Edge",
        desc=(
            "Past the chapel the road skirts a field of old and recent campsites left to rot where they "
            "stood. Rings of stone, broken carts, and collapsed tarps mark each halted attempt at passage."
        ),
        room_type="clearing",
        indoor=False,
    )
    sd_cold_cookfire = area.room(
        "sd_cold_cookfire",
        name="Cold Cookfire",
        desc=(
            "A cookfire long gone cold sits surrounded by blackened kettles and split spoon handles. No one "
            "bothered to carry anything away after the camp emptied."
        ),
        room_type="clearing",
        indoor=False,
    )
    sd_burial_row = area.room(
        "sd_burial_row",
        name="Burial Row",
        desc=(
            "Thin mounds lined by river stones run beside the road where unclaimed travelers were buried in "
            "orderly sequence. Some markers bear names; many were left blank for later correction."
        ),
        room_type="clearing",
        indoor=False,
    )
    sd_tally_pyre = area.room(
        "sd_tally_pyre",
        name="Tally Pyre",
        desc=(
            "A pyre pit filled with ash, nails, and half-burned tally boards marks the place where camp records "
            "were destroyed after each sweep. Charred parchment still curls in the wind."
        ),
        room_type="clearing",
        indoor=False,
    )
    sd_pickline = area.room(
        "sd_pickline",
        name="Pickline",
        desc=(
            "A line of rough stakes once held draft animals beside the dead camps. The ropes are gone, but the "
            "ground remains cut by hooves and restless pacing."
        ),
        room_type="clearing",
        indoor=False,
    )
    sd_chapel_cut = area.room(
        "sd_chapel_cut",
        name="Chapel Cut",
        desc=(
            "A narrow cut behind the chapel lets water and furtive feet pass between slope and road. Broken "
            "tiles from the chapel roof crunch underfoot."
        ),
        room_type="path",
        indoor=False,
    )
    sd_rag_hedge = area.room(
        "sd_rag_hedge",
        name="Rag Hedge",
        desc=(
            "A hedge of thorn and scrub catches strips of cloth torn from cloaks, bedrolls, and burial wraps. "
            "Some are marked with route numbers or hostel tallies."
        ),
        room_type="clearing",
        indoor=False,
    )
    sd_witness_nook = area.room(
        "sd_witness_nook",
        name="Witness Nook",
        desc=(
            "A sheltered recess in the slope holds a low stool, a board, and a view over the burial row. Someone "
            "used this place to copy names before the official count changed."
        ),
        room_type="building",
        indoor=True,
    )
    sd_gutter_altar = area.room(
        "sd_gutter_altar",
        name="Gutter Altar",
        desc=(
            "A broken roadside altar has been reset in a drainage gutter and used anyway. Wax trails mix with mud "
            "and the grease from camp kettles."
        ),
        room_type="ruins",
        indoor=False,
    )
    sd_broken_oxpen = area.room(
        "sd_broken_oxpen",
        name="Broken Oxpen",
        desc=(
            "An old pen of warped rails leans over a trampled patch of weeds. Whatever beasts were held here pulled "
            "loose hard enough to drag whole posts sideways."
        ),
        room_type="clearing",
        indoor=False,
    )
    sd_far_track = area.room(
        "sd_far_track",
        name="Far Track",
        desc=(
            "The road narrows to a worn track between dead camps on one side and caravan sidings on the other. A "
            "traveler can smell tar, smoke, and old ash before seeing the next turn."
        ),
        room_type="path",
        indoor=False,
    )

    # ==================================================================
    #  CARAVAN SIDINGS
    # ==================================================================
    cs_siding_fork = area.room(
        "cs_siding_fork",
        name="Siding Fork",
        desc=(
            "The Crownroad splits around a spread of parked wagons, loading ramps, and temporary sheds. The main line "
            "is still clear enough for officials; everyone else is expected to wait or pay."
        ),
        room_type="path",
        indoor=False,
    )
    cs_wagon_park = area.room(
        "cs_wagon_park",
        name="Wagon Park",
        desc=(
            "Dozens of wheel tracks overlap in this broad holding ground where caravans are staged, delayed, or quietly "
            "reassigned. Teamsters camp in the lee of their own cargo."
        ),
        room_type="clearing",
        indoor=False,
    )
    cs_weighbridge = area.room(
        "cs_weighbridge",
        name="Weighbridge",
        desc=(
            "A timber weighing frame straddles the road while clerks compare load marks to declared figures. The bridge "
            "groans under even modest cargo, as if tired of telling the truth."
        ),
        room_type="path",
        indoor=False,
    )
    cs_tar_shed = area.room(
        "cs_tar_shed",
        name="Tar Shed",
        desc=(
            "Barrels of tar, pitch cloth, and repair pegs fill this hot little shed. A handbill on the wall warns that "
            "state-sealed cargo must be patched before public cargo."
        ),
        room_type="building",
        indoor=True,
    )
    cs_rope_walk = area.room(
        "cs_rope_walk",
        name="Rope Walk",
        desc=(
            "Lengths of rope hang from poles to dry above a path slick with hemp fibers and tar drips. Workers stride the "
            "walk as if delay itself were something they could twist tighter."
        ),
        room_type="path",
        indoor=False,
    )
    cs_axle_yard = area.room(
        "cs_axle_yard",
        name="Axle Yard",
        desc=(
            "Broken axles, spare spokes, and bent iron tires are piled in sorted heaps. Useful failures remain here; the "
            "rest is sold off as salvage or forgotten under newer orders."
        ),
        room_type="clearing",
        indoor=False,
    )
    cs_drover_hill = area.room(
        "cs_drover_hill",
        name="Drover Hill",
        desc=(
            "A low hill gives drovers a view over the wagon park and the queue for the weighbridge. Fires, curses, and "
            "bell calls drift together in the air."
        ),
        room_type="clearing",
        indoor=False,
    )
    cs_packing_floor = area.room(
        "cs_packing_floor",
        name="Packing Floor",
        desc=(
            "Crates, wrapped loads, and open manifests cover a broad timber floor raised above the mud. Men with sealing "
            "wax and cargo hooks move in quick practiced lines."
        ),
        room_type="building",
        indoor=False,
    )
    cs_broker_cab = area.room(
        "cs_broker_cab",
        name="Broker Cab",
        desc=(
            "A curtained wagon body serves as a broker's office for rushed loads and inconvenient delays. Its ledgers are "
            "locked, but the prices are spoken loudly enough."
        ),
        room_type="building",
        indoor=True,
    )
    cs_storage_bay = area.room(
        "cs_storage_bay",
        name="Storage Bay",
        desc=(
            "This covered bay holds cargo that officially remains in transit while unofficially going nowhere. Dust lies "
            "thick on some crates and fresh chalk on others."
        ),
        room_type="building",
        indoor=True,
    )
    cs_mule_lines = area.room(
        "cs_mule_lines",
        name="Mule Lines",
        desc=(
            "A long run of tether posts holds pack mules with frayed tack and patient eyes. Feed buckets are numbered to "
            "match route slips nailed overhead."
        ),
        room_type="clearing",
        indoor=False,
    )
    cs_cargo_ramp = area.room(
        "cs_cargo_ramp",
        name="Cargo Ramp",
        desc=(
            "A broad ramp leads from the packing floor back onto the road. Wheel grooves in the planks show how heavily "
            "the sidings favor certain routes over others."
        ),
        room_type="path",
        indoor=False,
    )
    cs_salvage_heap = area.room(
        "cs_salvage_heap",
        name="Salvage Heap",
        desc=(
            "Broken hoops, split boxes, rusted fasteners, and warped signboards mound here in a deliberate disorder. "
            "Useful pieces disappear from the pile at night."
        ),
        room_type="clearing",
        indoor=False,
    )
    cs_guard_lean = area.room(
        "cs_guard_lean",
        name="Guard Lean-To",
        desc=(
            "A lean-to of patched boards gives sidings guards a dry place to watch the ramp and the broker cab. Their table "
            "holds dice, bad tea, and a carefully hidden fee slate."
        ),
        room_type="building",
        indoor=True,
    )
    cs_waybill_table = area.room(
        "cs_waybill_table",
        name="Waybill Table",
        desc=(
            "A heavy table under a hanging lamp supports route slips, copied seals, and stacks of tied waybills. Every sheet "
            "promises orderly passage; very few look honest."
        ),
        room_type="building",
        indoor=True,
    )
    cs_far_sidings = area.room(
        "cs_far_sidings",
        name="Far Sidings",
        desc=(
            "The last of the parked wagons thin out into a stretch of hard ground where the Crownroad meets the survey fields. "
            "Old wheel ruts survive here beneath newer measured cuts."
        ),
        room_type="path",
        indoor=False,
    )

    # ==================================================================
    #  SURVEY FIELDS
    # ==================================================================
    sf_survey_gate = area.room(
        "sf_survey_gate",
        name="Survey Gate",
        desc=(
            "A simple gate of posts and chain opens onto the measured strips beyond the sidings. Marker boards cite the Office "
            "of Seals and Civic Measure and forbid the removal of stakes."
        ),
        room_type="path",
        indoor=False,
    )
    sf_rod_field = area.room(
        "sf_rod_field",
        name="Rod Field",
        desc=(
            "Rods laid end to end across this field show where a new survey was begun and then revised in place. The soil is cut "
            "by precise lines and careless boots."
        ),
        room_type="path",
        indoor=False,
    )
    sf_cut_line = area.room(
        "sf_cut_line",
        name="Cut Line",
        desc=(
            "A straight trench slices the ground where old boundary stones were lifted and reset. Chips of pale rock glint in the "
            "loose dirt beside bundled stakes."
        ),
        room_type="path",
        indoor=False,
    )
    sf_boundary_strip = area.room(
        "sf_boundary_strip",
        name="Boundary Strip",
        desc=(
            "The road shoulder gives way to a long strip of pegged turf where competing copies of the boundary have been measured, "
            "argued, and measured again. Every revision claims finality."
        ),
        room_type="path",
        indoor=False,
    )
    sf_marker_knoll = area.room(
        "sf_marker_knoll",
        name="Marker Knoll",
        desc=(
            "A low knoll studded with numbered stakes rises above the strip. Some are painted fresh, while others carry scraped "
            "surfaces where older marks were removed."
        ),
        room_type="clearing",
        indoor=False,
    )
    sf_stake_rows = area.room(
        "sf_stake_rows",
        name="Stake Rows",
        desc=(
            "Rows of survey stakes march through thin grass toward the horizon. Twine lines between them hum softly when the wind "
            "turns against the road."
        ),
        room_type="clearing",
        indoor=False,
    )
    sf_remeasure_ditch = area.room(
        "sf_remeasure_ditch",
        name="Remeasure Ditch",
        desc=(
            "A drainage ditch beside the survey strip is choked with reed cuttings, snapped pegs, and wax droppings from broken "
            "seal cords. Revisions wash downhill here."
        ),
        room_type="clearing",
        indoor=False,
    )
    sf_copy_trench = area.room(
        "sf_copy_trench",
        name="Copy Trench",
        desc=(
            "Survey assistants have scraped a shallow trench to brace boards and stones while copying inscriptions. The trench walls "
            "show where older fragments were stacked, examined, and discarded."
        ),
        room_type="path",
        indoor=False,
    )
    sf_old_charter_stone = area.room(
        "sf_old_charter_stone",
        name="Old Charter Stone",
        desc=(
            "A massive boundary stone lies half-exposed here, its older surface cut with deeper, broader lines than the newer script "
            "framed beside it. The Crown Restoration Charter of 711 sits on top of a prior history it does not fully hide."
        ),
        room_type="ruins",
        indoor=False,
    )
    sf_skewed_marker = area.room(
        "sf_skewed_marker",
        name="Skewed Marker",
        desc=(
            "A marker stone has been reset at a slight angle, enough to bend the measured strip by a handspan over distance. The "
            "change is too clean to be an accident."
        ),
        room_type="ruins",
        indoor=False,
    )
    sf_field_hut = area.room(
        "sf_field_hut",
        name="Field Hut",
        desc=(
            "A squat hut of planks and patched felt gives survey clerks a place to dry papers and sleep beside their work. The table "
            "inside is burned by lamp bases and sealing irons."
        ),
        room_type="building",
        indoor=True,
    )
    sf_chain_post = area.room(
        "sf_chain_post",
        name="Chain Post",
        desc=(
            "Lengths of measuring chain hang from this post like dull iron vines. Each link carries a little rust from field use and "
            "a great deal of argument."
        ),
        room_type="path",
        indoor=False,
    )
    sf_ledger_shelter = area.room(
        "sf_ledger_shelter",
        name="Ledger Shelter",
        desc=(
            "A shelter of slanted boards protects route books and boundary ledgers from the weather. More than one ledger has been "
            "cut open and stitched closed again."
        ),
        room_type="building",
        indoor=True,
    )
    sf_charred_scrip = area.room(
        "sf_charred_scrip",
        name="Charred Scrip Pit",
        desc=(
            "A shallow pit of blackened paper and wax clumps marks where unwanted survey copies were burned. The edges still hide "
            "bits of half-legible witness text."
        ),
        room_type="clearing",
        indoor=False,
    )
    sf_far_mark = area.room(
        "sf_far_mark",
        name="Far Mark",
        desc=(
            "The last standing marker in this strip overlooks open land and a road that will eventually need to decide what story it "
            "serves. The newest seal sits a fraction off center."
        ),
        room_type="path",
        indoor=False,
    )
    sf_far_road = area.room(
        "sf_far_road",
        name="Far Road",
        desc=(
            "Beyond the survey strip the Crownroad narrows and runs on toward territory not yet fully measured by capital hands. The "
            "air here feels wider, though the stakes behind you insist otherwise."
        ),
        room_type="path",
        indoor=False,
    )

    # ==================================================================
    #  EXITS
    # ==================================================================
    area.exit(om_gate_verge, "varath_prime:ca_crownroad_gate", "north")
    area.exit(om_gate_verge, om_first_milestone, "south")
    area.exit(om_first_milestone, om_gate_verge, "north")
    area.exit(om_first_milestone, om_kingbar_ditch, "south")
    area.exit(om_kingbar_ditch, om_first_milestone, "north")
    area.exit(om_kingbar_ditch, om_measure_bank, "south")
    area.exit(om_measure_bank, om_kingbar_ditch, "north")
    area.exit(om_measure_bank, om_culvert_bridge, "south")
    area.exit(om_culvert_bridge, om_measure_bank, "north")
    area.exit(om_culvert_bridge, om_wayline_rise, "south")
    area.exit(om_wayline_rise, om_culvert_bridge, "north")
    area.exit(om_wayline_rise, om_talon_post, "south")
    area.exit(om_talon_post, om_wayline_rise, "north")
    area.exit(om_talon_post, om_stonebench_pull, "south")
    area.exit(om_stonebench_pull, om_talon_post, "north")
    area.exit(om_stonebench_pull, om_checkpoint_approach, "south")
    area.exit(om_checkpoint_approach, om_stonebench_pull, "north")
    area.exit(om_measure_bank, om_reed_swale, "east")
    area.exit(om_reed_swale, om_measure_bank, "west")
    area.exit(om_reed_swale, om_marker_fence, "south")
    area.exit(om_marker_fence, om_reed_swale, "north")
    area.exit(om_marker_fence, om_old_shed, "west")
    area.exit(om_old_shed, om_marker_fence, "east")
    area.exit(om_old_shed, om_measure_bank, "southeast")
    area.exit(om_measure_bank, om_old_shed, "northwest")
    area.exit(om_culvert_bridge, om_teamster_fire, "southwest")
    area.exit(om_teamster_fire, om_culvert_bridge, "northeast")
    area.exit(om_teamster_fire, om_dry_rut, "east")
    area.exit(om_dry_rut, om_teamster_fire, "west")
    area.exit(om_teamster_fire, om_tally_hollow, "south")
    area.exit(om_tally_hollow, om_teamster_fire, "north")
    area.exit(om_tally_hollow, om_copy_stone, "east")
    area.exit(om_copy_stone, om_tally_hollow, "west")
    area.exit(om_dry_rut, om_roadside_well, "north")
    area.exit(om_roadside_well, om_dry_rut, "south")
    area.exit(om_roadside_well, om_culvert_bridge, "west")
    area.exit(om_culvert_bridge, om_roadside_well, "east")
    area.exit(om_roadside_well, om_copy_stone, "north")
    area.exit(om_copy_stone, om_roadside_well, "south")

    area.exit(om_checkpoint_approach, cc_south_bar, "south")
    area.exit(cc_south_bar, om_checkpoint_approach, "north")
    area.exit(cc_south_bar, cc_permit_lane, "south")
    area.exit(cc_permit_lane, cc_south_bar, "north")
    area.exit(cc_permit_lane, cc_inspection_yard, "south")
    area.exit(cc_inspection_yard, cc_permit_lane, "north")
    area.exit(cc_inspection_yard, cc_watch_berm, "south")
    area.exit(cc_watch_berm, cc_inspection_yard, "north")
    area.exit(cc_watch_berm, cc_signal_walk, "south")
    area.exit(cc_signal_walk, cc_watch_berm, "north")
    area.exit(cc_signal_walk, cc_far_bar, "south")
    area.exit(cc_far_bar, cc_signal_walk, "north")
    area.exit(cc_permit_lane, cc_scriber_steps, "east")
    area.exit(cc_scriber_steps, cc_permit_lane, "west")
    area.exit(cc_scriber_steps, cc_archive_rack, "south")
    area.exit(cc_archive_rack, cc_scriber_steps, "north")
    area.exit(cc_archive_rack, cc_levy_booth, "west")
    area.exit(cc_levy_booth, cc_archive_rack, "east")
    area.exit(cc_levy_booth, cc_permit_lane, "northeast")
    area.exit(cc_permit_lane, cc_levy_booth, "southwest")
    area.exit(cc_inspection_yard, cc_impound_pens, "east")
    area.exit(cc_impound_pens, cc_inspection_yard, "west")
    area.exit(cc_impound_pens, cc_confiscation_cage, "north")
    area.exit(cc_confiscation_cage, cc_impound_pens, "south")
    area.exit(cc_confiscation_cage, cc_ration_shed, "west")
    area.exit(cc_ration_shed, cc_confiscation_cage, "east")
    area.exit(cc_ration_shed, cc_barrack_walk, "south")
    area.exit(cc_barrack_walk, cc_ration_shed, "north")
    area.exit(cc_barrack_walk, cc_watch_berm, "east")
    area.exit(cc_watch_berm, cc_barrack_walk, "west")
    area.exit(cc_barrack_walk, cc_bunkroom, "south")
    area.exit(cc_bunkroom, cc_barrack_walk, "north")
    area.exit(cc_inspection_yard, cc_side_ditch, "west")
    area.exit(cc_side_ditch, cc_inspection_yard, "east")
    area.exit(cc_side_ditch, cc_broken_culvert, "south")
    area.exit(cc_broken_culvert, cc_side_ditch, "north")
    area.exit(cc_broken_culvert, cc_bunkroom, "east")
    area.exit(cc_bunkroom, cc_broken_culvert, "west")
    area.exit(cc_signal_walk, cc_captains_office, "east")
    area.exit(cc_captains_office, cc_signal_walk, "west")

    area.exit(cc_far_bar, ry_road_gate, "south")
    area.exit(ry_road_gate, cc_far_bar, "north")
    area.exit(ry_road_gate, ry_courier_lane, "south")
    area.exit(ry_courier_lane, ry_road_gate, "north")
    area.exit(ry_courier_lane, ry_hostel_court, "south")
    area.exit(ry_hostel_court, ry_courier_lane, "north")
    area.exit(ry_hostel_court, ry_stable_ring, "south")
    area.exit(ry_stable_ring, ry_hostel_court, "north")
    area.exit(ry_stable_ring, ry_dispatch_board, "south")
    area.exit(ry_dispatch_board, ry_stable_ring, "north")
    area.exit(ry_dispatch_board, ry_far_yard, "south")
    area.exit(ry_far_yard, ry_dispatch_board, "north")
    area.exit(ry_far_yard, ry_relay_verge, "south")
    area.exit(ry_relay_verge, ry_far_yard, "north")
    area.exit(ry_hostel_court, ry_common_room, "east")
    area.exit(ry_common_room, ry_hostel_court, "west")
    area.exit(ry_common_room, ry_loft_bunks, "south")
    area.exit(ry_loft_bunks, ry_common_room, "north")
    area.exit(ry_loft_bunks, ry_ledger_desk, "west")
    area.exit(ry_ledger_desk, ry_loft_bunks, "east")
    area.exit(ry_ledger_desk, ry_hostel_court, "northeast")
    area.exit(ry_hostel_court, ry_ledger_desk, "southwest")
    area.exit(ry_stable_ring, ry_fodder_shed, "east")
    area.exit(ry_fodder_shed, ry_stable_ring, "west")
    area.exit(ry_fodder_shed, ry_post_kitchen, "south")
    area.exit(ry_post_kitchen, ry_fodder_shed, "north")
    area.exit(ry_post_kitchen, ry_back_paddock, "west")
    area.exit(ry_back_paddock, ry_post_kitchen, "east")
    area.exit(ry_back_paddock, ry_stable_ring, "northeast")
    area.exit(ry_stable_ring, ry_back_paddock, "southwest")
    area.exit(ry_stable_ring, ry_wash_line, "west")
    area.exit(ry_wash_line, ry_stable_ring, "east")
    area.exit(ry_dispatch_board, ry_farrier_nook, "east")
    area.exit(ry_farrier_nook, ry_dispatch_board, "west")
    area.exit(ry_farrier_nook, ry_wagon_shelter, "south")
    area.exit(ry_wagon_shelter, ry_farrier_nook, "north")
    area.exit(ry_wagon_shelter, ry_team_dormer, "west")
    area.exit(ry_team_dormer, ry_wagon_shelter, "east")
    area.exit(ry_team_dormer, ry_dispatch_board, "northeast")
    area.exit(ry_dispatch_board, ry_team_dormer, "southwest")

    area.exit(ry_relay_verge, sd_layby_turn, "south")
    area.exit(sd_layby_turn, ry_relay_verge, "north")
    area.exit(sd_layby_turn, sd_waychapel_steps, "south")
    area.exit(sd_waychapel_steps, sd_layby_turn, "north")
    area.exit(sd_waychapel_steps, sd_deadcamp_edge, "south")
    area.exit(sd_deadcamp_edge, sd_waychapel_steps, "north")
    area.exit(sd_deadcamp_edge, sd_burial_row, "south")
    area.exit(sd_burial_row, sd_deadcamp_edge, "north")
    area.exit(sd_burial_row, sd_tally_pyre, "south")
    area.exit(sd_tally_pyre, sd_burial_row, "north")
    area.exit(sd_tally_pyre, sd_far_track, "south")
    area.exit(sd_far_track, sd_tally_pyre, "north")
    area.exit(sd_waychapel_steps, sd_ash_bell, "east")
    area.exit(sd_ash_bell, sd_waychapel_steps, "west")
    area.exit(sd_ash_bell, sd_offertory_wall, "south")
    area.exit(sd_offertory_wall, sd_ash_bell, "north")
    area.exit(sd_offertory_wall, sd_prayer_shelf, "west")
    area.exit(sd_prayer_shelf, sd_offertory_wall, "east")
    area.exit(sd_prayer_shelf, sd_waychapel_steps, "northeast")
    area.exit(sd_waychapel_steps, sd_prayer_shelf, "southwest")
    area.exit(sd_deadcamp_edge, sd_cold_cookfire, "east")
    area.exit(sd_cold_cookfire, sd_deadcamp_edge, "west")
    area.exit(sd_cold_cookfire, sd_pickline, "south")
    area.exit(sd_pickline, sd_cold_cookfire, "north")
    area.exit(sd_pickline, sd_chapel_cut, "west")
    area.exit(sd_chapel_cut, sd_pickline, "east")
    area.exit(sd_chapel_cut, sd_deadcamp_edge, "northeast")
    area.exit(sd_deadcamp_edge, sd_chapel_cut, "southwest")
    area.exit(sd_burial_row, sd_rag_hedge, "east")
    area.exit(sd_rag_hedge, sd_burial_row, "west")
    area.exit(sd_rag_hedge, sd_witness_nook, "south")
    area.exit(sd_witness_nook, sd_rag_hedge, "north")
    area.exit(sd_witness_nook, sd_gutter_altar, "west")
    area.exit(sd_gutter_altar, sd_witness_nook, "east")
    area.exit(sd_gutter_altar, sd_burial_row, "northeast")
    area.exit(sd_burial_row, sd_gutter_altar, "southwest")
    area.exit(sd_layby_turn, sd_pilgrim_ditch, "west")
    area.exit(sd_pilgrim_ditch, sd_layby_turn, "east")
    area.exit(sd_pilgrim_ditch, sd_broken_oxpen, "south")
    area.exit(sd_broken_oxpen, sd_pilgrim_ditch, "north")
    area.exit(sd_broken_oxpen, sd_far_track, "east")
    area.exit(sd_far_track, sd_broken_oxpen, "west")

    area.exit(sd_far_track, cs_siding_fork, "south")
    area.exit(cs_siding_fork, sd_far_track, "north")
    area.exit(cs_siding_fork, cs_wagon_park, "south")
    area.exit(cs_wagon_park, cs_siding_fork, "north")
    area.exit(cs_wagon_park, cs_weighbridge, "south")
    area.exit(cs_weighbridge, cs_wagon_park, "north")
    area.exit(cs_weighbridge, cs_packing_floor, "south")
    area.exit(cs_packing_floor, cs_weighbridge, "north")
    area.exit(cs_packing_floor, cs_cargo_ramp, "south")
    area.exit(cs_cargo_ramp, cs_packing_floor, "north")
    area.exit(cs_cargo_ramp, cs_far_sidings, "south")
    area.exit(cs_far_sidings, cs_cargo_ramp, "north")
    area.exit(cs_wagon_park, cs_tar_shed, "east")
    area.exit(cs_tar_shed, cs_wagon_park, "west")
    area.exit(cs_tar_shed, cs_rope_walk, "south")
    area.exit(cs_rope_walk, cs_tar_shed, "north")
    area.exit(cs_rope_walk, cs_axle_yard, "west")
    area.exit(cs_axle_yard, cs_rope_walk, "east")
    area.exit(cs_axle_yard, cs_wagon_park, "northeast")
    area.exit(cs_wagon_park, cs_axle_yard, "southwest")
    area.exit(cs_weighbridge, cs_drover_hill, "east")
    area.exit(cs_drover_hill, cs_weighbridge, "west")
    area.exit(cs_drover_hill, cs_broker_cab, "south")
    area.exit(cs_broker_cab, cs_drover_hill, "north")
    area.exit(cs_broker_cab, cs_storage_bay, "west")
    area.exit(cs_storage_bay, cs_broker_cab, "east")
    area.exit(cs_storage_bay, cs_weighbridge, "northeast")
    area.exit(cs_weighbridge, cs_storage_bay, "southwest")
    area.exit(cs_packing_floor, cs_mule_lines, "east")
    area.exit(cs_mule_lines, cs_packing_floor, "west")
    area.exit(cs_mule_lines, cs_salvage_heap, "south")
    area.exit(cs_salvage_heap, cs_mule_lines, "north")
    area.exit(cs_salvage_heap, cs_guard_lean, "west")
    area.exit(cs_guard_lean, cs_salvage_heap, "east")
    area.exit(cs_guard_lean, cs_waybill_table, "north")
    area.exit(cs_waybill_table, cs_guard_lean, "south")
    area.exit(cs_waybill_table, cs_cargo_ramp, "west")
    area.exit(cs_cargo_ramp, cs_waybill_table, "east")

    area.exit(cs_far_sidings, sf_survey_gate, "south")
    area.exit(sf_survey_gate, cs_far_sidings, "north")
    area.exit(sf_survey_gate, sf_rod_field, "south")
    area.exit(sf_rod_field, sf_survey_gate, "north")
    area.exit(sf_rod_field, sf_cut_line, "south")
    area.exit(sf_cut_line, sf_rod_field, "north")
    area.exit(sf_cut_line, sf_boundary_strip, "south")
    area.exit(sf_boundary_strip, sf_cut_line, "north")
    area.exit(sf_boundary_strip, sf_old_charter_stone, "south")
    area.exit(sf_old_charter_stone, sf_boundary_strip, "north")
    area.exit(sf_old_charter_stone, sf_far_mark, "south")
    area.exit(sf_far_mark, sf_old_charter_stone, "north")
    area.exit(sf_far_mark, sf_far_road, "south")
    area.exit(sf_far_road, sf_far_mark, "north")
    area.exit(sf_rod_field, sf_marker_knoll, "east")
    area.exit(sf_marker_knoll, sf_rod_field, "west")
    area.exit(sf_marker_knoll, sf_stake_rows, "south")
    area.exit(sf_stake_rows, sf_marker_knoll, "north")
    area.exit(sf_stake_rows, sf_remeasure_ditch, "west")
    area.exit(sf_remeasure_ditch, sf_stake_rows, "east")
    area.exit(sf_remeasure_ditch, sf_rod_field, "northeast")
    area.exit(sf_rod_field, sf_remeasure_ditch, "southwest")
    area.exit(sf_boundary_strip, sf_copy_trench, "east")
    area.exit(sf_copy_trench, sf_boundary_strip, "west")
    area.exit(sf_copy_trench, sf_skewed_marker, "south")
    area.exit(sf_skewed_marker, sf_copy_trench, "north")
    area.exit(sf_skewed_marker, sf_field_hut, "west")
    area.exit(sf_field_hut, sf_skewed_marker, "east")
    area.exit(sf_field_hut, sf_boundary_strip, "northeast")
    area.exit(sf_boundary_strip, sf_field_hut, "southwest")
    area.exit(sf_old_charter_stone, sf_chain_post, "east")
    area.exit(sf_chain_post, sf_old_charter_stone, "west")
    area.exit(sf_chain_post, sf_ledger_shelter, "south")
    area.exit(sf_ledger_shelter, sf_chain_post, "north")
    area.exit(sf_ledger_shelter, sf_charred_scrip, "west")
    area.exit(sf_charred_scrip, sf_ledger_shelter, "east")
    area.exit(sf_charred_scrip, sf_old_charter_stone, "northeast")
    area.exit(sf_old_charter_stone, sf_charred_scrip, "southwest")

    # ==================================================================
    #  SPAWNS
    # ==================================================================
    area.spawn(om_old_shed, "dust_hound", count_min=1, count_max=1, respawn_minutes=22, respawn_variance=6)
    area.spawn(om_tally_hollow, "bandit", count_min=1, count_max=1, respawn_minutes=24, respawn_variance=7)
    area.spawn(om_reed_swale, "plains_viper", count_min=1, count_max=1, respawn_minutes=20, respawn_variance=5)
    area.spawn(cc_side_ditch, "thug", count_min=1, count_max=2, respawn_minutes=20, respawn_variance=5)
    area.spawn(cc_broken_culvert, "plains_viper", count_min=1, count_max=1, respawn_minutes=22, respawn_variance=6)
    area.spawn(cc_impound_pens, "checkpoint_enforcer", count_min=1, count_max=1, respawn_minutes=28, respawn_variance=8)
    area.spawn(cc_signal_walk, "checkpoint_enforcer", count_min=0, count_max=1, respawn_minutes=30, respawn_variance=8)
    area.spawn(ry_back_paddock, "dust_hound", count_min=1, count_max=2, respawn_minutes=24, respawn_variance=6)
    area.spawn(ry_wagon_shelter, "bandit", count_min=0, count_max=1, respawn_minutes=26, respawn_variance=7)
    area.spawn(sd_pilgrim_ditch, "plains_viper", count_min=1, count_max=1, respawn_minutes=20, respawn_variance=5)
    area.spawn(sd_deadcamp_edge, "bandit", count_min=1, count_max=2, respawn_minutes=22, respawn_variance=6)
    area.spawn(sd_tally_pyre, "deadcamp_raider", count_min=1, count_max=1, respawn_minutes=30, respawn_variance=10)
    area.spawn(sd_gutter_altar, "deadcamp_raider", count_min=0, count_max=1, respawn_minutes=32, respawn_variance=10)
    area.spawn(sd_broken_oxpen, "dust_hound", count_min=1, count_max=1, respawn_minutes=24, respawn_variance=6)
    area.spawn(cs_wagon_park, "bandit", count_min=1, count_max=1, respawn_minutes=24, respawn_variance=6)
    area.spawn(cs_salvage_heap, "thug", count_min=1, count_max=2, respawn_minutes=22, respawn_variance=6)
    area.spawn(cs_guard_lean, "checkpoint_enforcer", count_min=0, count_max=1, respawn_minutes=28, respawn_variance=8)
    area.spawn(sf_remeasure_ditch, "ashreach_bandit", count_min=1, count_max=1, respawn_minutes=24, respawn_variance=6)
    area.spawn(sf_charred_scrip, "ashreach_bandit", count_min=1, count_max=2, respawn_minutes=26, respawn_variance=7)
    area.spawn(sf_skewed_marker, "steppe_hawk", count_min=1, count_max=1, respawn_minutes=18, respawn_variance=4)
    area.spawn(sf_far_road, "dust_hound", count_min=1, count_max=1, respawn_minutes=24, respawn_variance=6)

    area.named_mob(
        "captain_helvik_drenn",
        cc_captains_office,
        respawn_minutes=150,
        respawn_variance=30,
        prestige_modifier=2.0,
        behavior=["territorial"],
        base_disposition=-0.8,
        flee_threshold=10,
        tome_drop="crownroad_extortion_tome",
    )
    area.named_mob(
        "registrar_oric_vane",
        sf_ledger_shelter,
        respawn_minutes=180,
        respawn_variance=40,
        prestige_modifier=2.1,
        behavior=["desperate"],
        base_disposition=-0.9,
        flee_threshold=5,
        tome_drop="crownroad_registry_tome",
    )

    # ==================================================================
    #  NPCS
    # ==================================================================
    area.npc(om_gate_verge, "npc_roadward_sable", faction="empire")
    area.npc(cc_scriber_steps, "npc_checkpoint_scrivener_ysolde", faction="empire")
    area.npc(cc_watch_berm, "npc_sergeant_vek_moren", faction="empire")
    area.npc(cc_impound_pens, "npc_impound_keeper_ressa", faction="empire")
    area.npc(cc_levy_booth, "npc_permit_runner_hale", faction="empire")
    _hostel_keeper = area.npc(ry_hostel_court, "npc_hostel_keeper_marro", faction="consortium")
    area.vendor(
        _hostel_keeper,
        accepts=["consumable"],
        item_ids=[
            "trail_rations",
            "bandage",
            "minor_healing_potion",
            "antidote_potion",
        ],
        faction="consortium",
    )
    area.npc(ry_stable_ring, "npc_hostler_denn", faction="consortium")
    area.npc(ry_post_kitchen, "npc_waycook_fela", faction=None)
    area.npc(sd_waychapel_steps, "npc_waychapel_caretaker_iben", faction=None)
    area.npc(sd_witness_nook, "npc_witness_selk", faction=None)
    area.npc(cs_broker_cab, "npc_caravan_factor_rhune", faction="consortium")
    area.npc(cs_wagon_park, "npc_wagoner_pev", faction="consortium")
    area.npc(sf_ledger_shelter, "npc_surveyor_calm_trest", faction="circle")
    area.npc(sf_field_hut, "npc_marker_clerk_elsin", faction="empire")

    # ==================================================================
    #  ITEMS
    # ==================================================================
    area.item(
        "relay_waybill_roll",
        key="Sealed Waybill Roll",
        item_type="item",
        weight=0.1,
        rarity="normal",
        value=0,
        is_quest_item=True,
        desc=(
            "A tight roll of relay waybills sealed for internal transfer between "
            "the hostel court and the sidings broker."
        ),
    )
    area.item(
        "copied_boundary_slip",
        key="Copied Boundary Slip",
        item_type="item",
        weight=0.1,
        rarity="normal",
        value=0,
        is_quest_item=True,
        desc=(
            "A folded survey slip bearing fresh civic measure marks over older, "
            "partially erased witness notes."
        ),
    )

    # ==================================================================
    #  LORE FRAGMENTS
    # ==================================================================
    area.lore_fragment(
        "crn_lore_measured_passage",
        om_copy_stone,
        discovery_method="search",
        scholar_path="arcana",
        text=(
            "An older cutting beneath the current copy of the Edict of Measured Passage "
            "treats detained travelers as held in custody, not delayed for correction. "
            "The newer wording smooths force into procedure."
        ),
        insight_gain=2,
    )
    area.lore_fragment(
        "crn_lore_talon_posting",
        om_talon_post,
        discovery_method="search",
        scholar_path="resonance",
        text=(
            "A relay posting under the talon-and-bar seal notes Thirteenth Talon Command "
            "runs delayed by road seizures, then adds in a smaller hand that copied manifests "
            "must stand in place of missing originals."
        ),
        insight_gain=2,
    )
    area.lore_fragment(
        "crn_lore_impound_notice",
        cc_confiscation_cage,
        discovery_method="search",
        scholar_path="remnance",
        text=(
            "An impound notice lists trunks, satchels, and draft animals held under the split "
            "roadwheel stamp. One column for disposition has been left blank so often that the "
            "paper creases before the clerk reaches it."
        ),
        insight_gain=2,
    )
    area.lore_fragment(
        "crn_lore_private_levy",
        cc_captains_office,
        discovery_method="search",
        scholar_path="arcana",
        text=(
            "A slate hidden beneath routine levy figures tracks 'private correction fees' paid "
            "in addition to lawful tolls. House Talvere route marks appear beside the highest "
            "totals, but only where the chalk was not fully wiped clean."
        ),
        insight_gain=3,
    )
    area.lore_fragment(
        "crn_lore_relay_guestlist",
        ry_ledger_desk,
        discovery_method="search",
        scholar_path="remnance",
        text=(
            "The relay guest list records rooms, animals, and packet transfers with obsessive care, "
            "yet a whole run of traveler names has been cut from the book. In the margin: 'copy accepted "
            "in place of witness.'"
        ),
        insight_gain=2,
    )
    area.lore_fragment(
        "crn_lore_waychapel_omission",
        sd_offertory_wall,
        discovery_method="search",
        scholar_path="arcana",
        text=(
            "A prayer slip tucked behind the offertory bowls asks that those halted on the Crownroad be "
            "returned to lawful passage. Another hand below it adds: 'disposition omitted by instruction.'"
        ),
        insight_gain=2,
    )
    area.lore_fragment(
        "crn_lore_deadcamp_roll",
        sd_tally_pyre,
        discovery_method="search",
        scholar_path="remnance",
        text=(
            "Half-burned camp rolls name drovers, clerks, and family retainers lost to delay at the road. "
            "Three lines are marked for House Rhest preserve access, then blackened out with lamp soot."
        ),
        insight_gain=3,
    )
    area.lore_fragment(
        "crn_lore_waybill_slate",
        cs_waybill_table,
        discovery_method="search",
        scholar_path="arcana",
        text=(
            "A sidings slate gives Stonewake Contracting haul priority under the Iron Vein Requisition of 734, "
            "placing quarry loads ahead of food wagons and burial carts. Someone has scratched 'defensive necessity' "
            "into the wood with obvious contempt."
        ),
        insight_gain=2,
    )
    area.lore_fragment(
        "crn_lore_charter_stone",
        sf_old_charter_stone,
        discovery_method="search",
        scholar_path="remnance",
        text=(
            "The old charter stone shows one boundary line cut deeper than the Crown Restoration Charter of 711 now "
            "laid over it. The newer copy claims restoration; the older stone suggests seizure followed by renaming."
        ),
        insight_gain=3,
    )
    area.lore_fragment(
        "crn_lore_charred_revision",
        sf_charred_scrip,
        discovery_method="search",
        scholar_path="resonance",
        text=(
            "A charred survey slip preserves witness text omitted from the official revision: a copied boundary accepted "
            "without stone, without second measure, and without the named registrar present."
        ),
        insight_gain=2,
    )

    # ==================================================================
    #  QUESTS
    # ==================================================================
    area.quest(
        "crn_q_waybill_run",
        name="Waybill Run",
        description=(
            "Hostel Keeper Marro needs a sealed waybill carried from the relay court to Caravan "
            "Factor Rhune before another sidings fee is invented around it."
        ),
        quest_type="delivery",
        quest_giver="npc_hostel_keeper_marro",
        objectives=[
            {
                "type": "deliver",
                "target": "npc_caravan_factor_rhune",
                "count": 1,
                "description": "Deliver the sealed waybill roll to Caravan Factor Rhune",
            },
        ],
        flagged_drop="relay_waybill_roll",
        rewards=[
            {"action_type": "give_scales", "amount": 70},
            {"action_type": "modify_standing", "faction_id": "consortium", "delta": 80},
            {
                "action_type": "echo",
                "message": "|gMarro exhales through his nose. \"Good. One less excuse for them to squeeze the yard.\"|n",
            },
        ],
        next_quest_id="crn_q_private_levy",
        objective_type="deliver",
        objective_target="npc_caravan_factor_rhune",
        objective_count=1,
    )
    area.quest(
        "crn_q_private_levy",
        name="Private Levy",
        description=(
            "Caravan Factor Rhune wants proof that the checkpoint's 'extra handling fees' are "
            "being enforced with cudgels instead of charters. Thin the enforcers leaning on the yards."
        ),
        quest_type="kill",
        quest_giver="npc_caravan_factor_rhune",
        prerequisite_quests=["crn_q_waybill_run"],
        objectives=[
            {
                "type": "kill",
                "target": "checkpoint_enforcer",
                "count": 3,
                "description": "Defeat checkpoint enforcers collecting private levies",
            },
        ],
        rewards=[
            {"action_type": "give_scales", "amount": 95},
            {"action_type": "modify_standing", "faction_id": "consortium", "delta": 100},
            {
                "action_type": "echo",
                "message": "|gRhune taps the ruined fee slate. \"They call it order when they can write it down. Keep pushing.\"|n",
            },
        ],
        objective_type="kill",
        objective_target="checkpoint_enforcer",
        objective_count=3,
    )
    area.quest(
        "crn_q_deadcamp_names",
        name="Deadcamp Names",
        description=(
            "Caretaker Iben tends the road chapel and wants the dead camps searched for names the sweepers "
            "missed or removed. He is tired of burying blanks."
        ),
        quest_type="investigation",
        quest_giver="npc_waychapel_caretaker_iben",
        objectives=[
            {
                "type": "investigate",
                "target": "sd_burial_row",
                "count": 1,
                "description": "Investigate the burial row",
            },
            {
                "type": "investigate",
                "target": "sd_tally_pyre",
                "count": 1,
                "description": "Search the tally pyre for surviving names",
            },
            {
                "type": "investigate",
                "target": "sd_witness_nook",
                "count": 1,
                "description": "Inspect the witness nook for copied rolls",
            },
        ],
        rewards=[
            {"action_type": "give_scales", "amount": 85},
            {"action_type": "modify_standing", "faction_id": "empire", "delta": 40},
            {
                "action_type": "echo",
                "message": "|gIben bows his head. \"A named dead soul weighs differently than an omitted one.\"|n",
            },
        ],
        objective_type="investigate",
        objective_target="sd_burial_row",
        objective_count=3,
    )
    area.quest(
        "crn_q_remeasure_strip",
        name="Remeasure Strip",
        description=(
            "Surveyor Calm Trest has prepared a copied boundary slip that needs to reach Scrivener Ysolde "
            "before the next revision closes over it."
        ),
        quest_type="delivery",
        quest_giver="npc_surveyor_calm_trest",
        objectives=[
            {
                "type": "deliver",
                "target": "npc_checkpoint_scrivener_ysolde",
                "count": 1,
                "description": "Deliver the copied boundary slip to Scrivener Ysolde",
            },
        ],
        flagged_drop="copied_boundary_slip",
        rewards=[
            {"action_type": "give_scales", "amount": 80},
            {"action_type": "modify_standing", "faction_id": "circle", "delta": 85},
            {
                "action_type": "echo",
                "message": "|gTrest folds his measuring chain away. \"Thank you. Accuracy is often just speed before interference arrives.\"|n",
            },
        ],
        next_quest_id="crn_q_missing_registrar",
        objective_type="deliver",
        objective_target="npc_checkpoint_scrivener_ysolde",
        objective_count=1,
    )
    area.quest(
        "crn_q_missing_registrar",
        name="Missing Registrar",
        description=(
            "Scrivener Ysolde says Registrar Oric Vane vanished from the rolls months ago, yet boundary copies "
            "in the field still carry his hand. Find him where the survey books went to burn."
        ),
        quest_type="kill",
        quest_giver="npc_checkpoint_scrivener_ysolde",
        prerequisite_quests=["crn_q_remeasure_strip"],
        objectives=[
            {
                "type": "kill",
                "target": "registrar_oric_vane",
                "count": 1,
                "description": "Defeat Registrar Oric Vane in the survey fields",
            },
        ],
        rewards=[
            {"action_type": "give_scales", "amount": 130},
            {"action_type": "modify_standing", "faction_id": "empire", "delta": 120},
            {
                "action_type": "echo",
                "message": "|gYsolde reads the returned notes twice. \"So he was not lost to delay after all. That explains far too much.\"|n",
            },
        ],
        objective_type="kill",
        objective_target="registrar_oric_vane",
        objective_count=1,
    )

    # ==================================================================
    #  GATHERING POOLS
    # ==================================================================
    area.gathering_pool(
        "ore",
        rooms=["om_copy_stone", "cc_broken_culvert", "cs_salvage_heap", "sf_copy_trench"],
        materials=["milestone_iron", "relay_scrap"],
        max_active=3,
        respawn_minutes=14,
        respawn_variance=4,
    )
    area.gathering_pool(
        "herb",
        rooms=["om_reed_swale", "sd_prayer_shelf", "sf_remeasure_ditch", "sf_stake_rows"],
        materials=["roadsage", "mileglass_lichen"],
        max_active=3,
        respawn_minutes=10,
        respawn_variance=3,
    )
    area.gathering_pool(
        "forage",
        rooms=["om_marker_fence", "ry_back_paddock", "sd_pilgrim_ditch", "cs_tar_shed"],
        materials=["charter_reed"],
        max_active=3,
        respawn_minutes=9,
        respawn_variance=3,
    )
    area.gathering_pool(
        "hide",
        rooms=["om_old_shed", "sd_broken_oxpen", "sf_far_road"],
        materials=["dust_hound_hide"],
        max_active=2,
        respawn_minutes=16,
        respawn_variance=5,
    )

    return area.build()
