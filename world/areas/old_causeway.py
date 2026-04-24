"""
Old Causeway -- Hub 4 exterior zone

An older corridor near Varath Prime that the Empire repurposed rather than
built. Repeating geometry, revised plaques, drained works, and hidden survey
routes make the causeway feel inherited, counted, and only partly understood.
"""

from world.area_builder import AreaBuilder


def build():
    area = AreaBuilder("old_causeway")

    # ------------------------------------------------------------------
    # Zone setup
    # ------------------------------------------------------------------
    area.zone(
        name="Old Causeway",
        zone_type="frontier",
        continent="varath",
        tier=4,
        region="crownlands",
        hub_city="varath_prime",
        faction_territory="imperial",
        faction_presence=["empire", "circle", "consortium"],
        world_x=44,
        world_y=-28,
        world_radius=125,
    )

    # ------------------------------------------------------------------
    # Materials
    # ------------------------------------------------------------------
    area.material(
        "causeway_shard",
        tier=1,
        terrain="stone",
        absorbed_property="durability",
        profession_bonus={"smithing": 0.1, "scholarship": 0.05},
    )
    area.material(
        "archmoss",
        tier=1,
        terrain="masonry",
        absorbed_property="clarity",
        profession_bonus={"alchemy": 0.1, "scholarship": 0.05},
    )
    area.material(
        "cistern_salt",
        tier=1,
        terrain="underground",
        absorbed_property="precision",
        profession_bonus={"alchemy": 0.05, "cooking": 0.05},
    )
    area.material(
        "survey_bronze",
        tier=1,
        terrain="ruins",
        absorbed_property="precision",
        profession_bonus={"smithing": 0.05, "scholarship": 0.1},
    )
    area.material(
        "reservoir_calcite",
        tier=1,
        terrain="underground",
        absorbed_property="hardite",
        profession_bonus={"smithing": 0.1},
    )
    area.material(
        "shrine_silt",
        tier=1,
        terrain="water",
        absorbed_property=None,
        profession_bonus={"alchemy": 0.05, "scholarship": 0.05},
    )

    # ==================================================================
    #  BROKEN CAUSEWAY SPINE
    # ==================================================================
    bs_postern_landing = area.room(
        "bs_postern_landing",
        name="Postern Landing",
        desc="A service lane spills out from the Ministry Ward onto paving older than the wall itself. Fresh Imperial patchstone ends after a few steps, leaving numbered blocks worn by traffic the postern only inherited.",
        room_type="path",
    )
    bs_numbered_span = area.room(
        "bs_numbered_span",
        name="Numbered Span",
        desc="Every fifth stone here bears a shallow numeral cut beneath later seal marks. The official paint is newer than the wear around it.",
        room_type="path",
    )
    bs_split_mile = area.room(
        "bs_split_mile",
        name="Split Mile",
        desc="A cracked milestone was cut in half and reset on either side of the road, as if the corridor had once been measured to a different center.",
        room_type="path",
    )
    bs_gap_brace = area.room(
        "bs_gap_brace",
        name="Gap Brace",
        desc="Iron braces stitch one sunken section of paving where the original roadbed dropped away. The repair is newer than the stone it grips.",
        room_type="path",
    )
    bs_echo_joint = area.room(
        "bs_echo_joint",
        name="Echo Joint",
        desc="Tight seams between the fitted blocks answer bootsteps with a delayed hum. The sound comes back too evenly to be a simple hollow below.",
        room_type="path",
    )
    bs_culvert_mouth = area.room(
        "bs_culvert_mouth",
        name="Culvert Mouth",
        desc="Black water slips under the causeway through an opening too round and too old for modern Imperial masonry. Salt bloom and soot share the same stone lip.",
        room_type="ruins",
    )
    bs_patchwork_ramp = area.room(
        "bs_patchwork_ramp",
        name="Patchwork Ramp",
        desc="The road tilts over a length of salvaged block and lime mortar where crews forced newer stone to obey the old rise.",
        room_type="path",
    )
    bs_recut_plate = area.room(
        "bs_recut_plate",
        name="Recut Plate",
        desc="A plaque slab has been shaved flat and recut with the Crown Restoration Charter of 711. Earlier lines still push through under the new text when the light catches sideways.",
        room_type="ruins",
    )
    bs_shiver_span = area.room(
        "bs_shiver_span",
        name="Shiver Span",
        desc="Thin paving slabs tremble above a long hidden cavity. Each wagon-rattle turns the surface into a measured shiver.",
        room_type="path",
    )
    bs_survey_notch = area.room(
        "bs_survey_notch",
        name="Survey Notch",
        desc="Brass pins and scored measure lines bite into the roadside stone. The newer survey marks never quite match the older geometry beneath them.",
        room_type="path",
    )
    bs_broken_guardrail = area.room(
        "bs_broken_guardrail",
        name="Broken Guardrail",
        desc="Rail sockets line the edge here, though the current iron is gone. The spacing suggests an older barrier built for something more formal than today's salvage traffic.",
        room_type="ruins",
    )
    bs_long_crack = area.room(
        "bs_long_crack",
        name="Long Crack",
        desc="One dark fissure runs across a dozen fitted stones without interrupting the repeated count marks cut into them. The road was measured through damage and then claimed anyway.",
        room_type="path",
    )
    bs_mended_cause = area.room(
        "bs_mended_cause",
        name="Mended Cause",
        desc="Lime mortar and scavenged blocks make an obvious Imperial patch across older seamless work. The repair reads like an apology written too late.",
        room_type="path",
    )
    bs_counting_stones = area.room(
        "bs_counting_stones",
        name="Counting Stones",
        desc="The blocks along this reach repeat in six-stone cycles broken only by later patchwork. Someone counted this place long before the Registry claimed it.",
        room_type="path",
    )
    bs_far_break = area.room(
        "bs_far_break",
        name="Far Break",
        desc="The roadway ends in a clean collapse that reveals the first ruin-shadow of the arches below. The break feels abrupt, almost chosen.",
        room_type="ruins",
    )
    bs_arch_threshold = area.room(
        "bs_arch_threshold",
        name="Arch Threshold",
        desc="Open causeway gives way to leaning vault stone ahead. A colder draft comes through the gap where the arches begin.",
        room_type="ruins",
    )
    bs_shorn_plaque = area.room(
        "bs_shorn_plaque",
        name="Shorn Plaque",
        desc="The face of this plaque was hacked smooth, leaving the tops of older letters at the border. The newer decree text is careful and defensive.",
        room_type="ruins",
    )
    bs_side_slab = area.room(
        "bs_side_slab",
        name="Side Slab",
        desc="A broad shoulder slab overlooks lower spoil and a ditch full of discarded wedges. Survey chalk still clings to one edge.",
        room_type="clearing",
    )
    bs_watch_niche = area.room(
        "bs_watch_niche",
        name="Watch Niche",
        desc="A narrow roadside recess offers sightlines down the causeway, though its angles do not favor the current postern approach. It watched some earlier traffic better than this one.",
        room_type="ruins",
    )
    bs_marker_hollow = area.room(
        "bs_marker_hollow",
        name="Marker Hollow",
        desc="Weeds crowd a shallow socket where a numbered marker once stood. The stone around it is polished by repeated removal and replacement.",
        room_type="clearing",
    )
    bs_third_marker = area.room(
        "bs_third_marker",
        name="Third Marker",
        desc="Another broken numeral stone repeats the same sequence as the first milestone nearer the city. Either the count was reused or the road was re-centered by force.",
        room_type="path",
    )
    bs_shrine_pull = area.room(
        "bs_shrine_pull",
        name="Shrine Pull",
        desc="Wax drips, ash, and reed ties gather beside a roadside block that was clearly once an altar before it became a stopping place.",
        room_type="clearing",
    )
    bs_seal_bench = area.room(
        "bs_seal_bench",
        name="Seal Bench",
        desc="A low bench bears charcoal smears, wax flakes, and rubbed copies of vanished text. Clerks and scavengers both use it, for different forms of extraction.",
        room_type="ruins",
    )
    bs_drop_sounding = area.room(
        "bs_drop_sounding",
        name="Drop Sounding",
        desc="A broken rail opens onto a maintenance shaft where stones and voices take too long to hit bottom. Damp air rises with the smell of mineral rot.",
        room_type="ruins",
    )

    # ==================================================================
    #  COLLAPSED ARCHES
    # ==================================================================
    ar_first_arch = area.room(
        "ar_first_arch",
        name="First Fallen Arch",
        desc="Great stones lean together overhead like ribs. The Empire shored the entrance, but the shape underneath belongs to an older maker.",
        room_type="ruins",
    )
    ar_shadow_underspan = area.room(
        "ar_shadow_underspan",
        name="Shadow Underspan",
        desc="Cool gloom pools beneath a surviving curve of masonry where the light thins and footsteps flatten into echoes.",
        room_type="underground",
        indoor=True,
    )
    ar_broken_pier = area.room(
        "ar_broken_pier",
        name="Broken Pier",
        desc="A support pier stands split and stitched with later iron clamps. The clamps are practical; the fracture is patient.",
        room_type="ruins",
    )
    ar_echo_chamber = area.room(
        "ar_echo_chamber",
        name="Echo Chamber",
        desc="Even a whisper returns in counted intervals from unseen cavities inside the arch body. The chamber seems to remember measurements better than voices.",
        room_type="underground",
        indoor=True,
    )
    ar_drip_gallery = area.room(
        "ar_drip_gallery",
        name="Drip Gallery",
        desc="Water slips through the vault in thin silver lines that never miss the same grooves. Wet stone shines where long use polished it smooth.",
        room_type="underground",
        indoor=True,
    )
    ar_fallen_bays = area.room(
        "ar_fallen_bays",
        name="Fallen Bays",
        desc="Three adjoining arch bays have collapsed into a maze of block, lintel, and dark pockets. The route through them feels recently used.",
        room_type="ruins",
    )
    ar_undercourt = area.room(
        "ar_undercourt",
        name="Undercourt",
        desc="A broad paved court sits beneath the surviving arches in precise squares older than any Ministry paving order.",
        room_type="underground",
        indoor=True,
    )
    ar_cracked_keystone = area.room(
        "ar_cracked_keystone",
        name="Cracked Keystone",
        desc="The exposed keystone above bears two layers of numbering, one cleanly recut over the other. Neither matches current road tallies.",
        room_type="ruins",
    )
    ar_second_underspan = area.room(
        "ar_second_underspan",
        name="Second Underspan",
        desc="Another low passage continues west through cool stone and dripping seams. The corridor is too regular to be a mere collapse path.",
        room_type="underground",
        indoor=True,
    )
    ar_far_arch = area.room(
        "ar_far_arch",
        name="Far Arch",
        desc="The last intact arch looms over a drift of shattered stone and scrub. Past it, the ruin eases into waystation ground.",
        room_type="ruins",
    )
    ar_waystation_turn = area.room(
        "ar_waystation_turn",
        name="Waystation Turn",
        desc="The corridor bends away from the arch complex toward a ruined stophouse. The paving broadens here as if traffic once pooled and sorted.",
        room_type="path",
    )
    ar_hook_ladder = area.room(
        "ar_hook_ladder",
        name="Hook Ladder",
        desc="Iron hooks and ladder pegs climb into the arch body where repair crews and scavengers both go looking for unreachable stone.",
        room_type="ruins",
    )
    ar_upper_rib = area.room(
        "ar_upper_rib",
        name="Upper Rib",
        desc="A narrow ledge runs along the upper curve of the vault, looking down over broken bays and old sightlines.",
        room_type="ruins",
    )
    ar_low_squeeze = area.room(
        "ar_low_squeeze",
        name="Low Squeeze",
        desc="This crawl-height passage was cleared by many shoulders and few official tools. Mud and scraped mortar tell the truth of hidden traffic.",
        room_type="underground",
        indoor=True,
    )
    ar_arch_roost = area.room(
        "ar_arch_roost",
        name="Arch Roost",
        desc="Feathers, husks, and old bones gather on a dry perch inside the vault ribs. Predators favor the same shelter surveyors once did.",
        room_type="ruins",
    )
    ar_collapse_nest = area.room(
        "ar_collapse_nest",
        name="Collapse Nest",
        desc="Broken mortar and gnawed bone have been dragged into one warm bowl of rubble. Something nests here and trusts the ruin to hide it.",
        room_type="cave",
        indoor=True,
    )
    ar_dust_landing = area.room(
        "ar_dust_landing",
        name="Dust Landing",
        desc="Fine grit lies here as if poured from above in regular sifted falls. Even the dust seems to follow a pattern.",
        room_type="ruins",
    )
    ar_repeater_stair = area.room(
        "ar_repeater_stair",
        name="Repeater Stair",
        desc="Short stair flights turn in identical lengths and rises, repeating too neatly to feel improvised. The shape suggests a plan still echoing through the ruin.",
        room_type="underground",
        indoor=True,
    )
    ar_hidden_apse = area.room(
        "ar_hidden_apse",
        name="Hidden Apse",
        desc="A blind chamber opens behind the low squeeze, its wall cut with copied marks and pried-out fixings. This room hid revisions before it hid people.",
        room_type="underground",
        indoor=True,
    )
    ar_shaft_pool = area.room(
        "ar_shaft_pool",
        name="Shaft Pool",
        desc="Rain and seep water collect in a black basin at the bottom of a narrow shaft. Bronze fragments glitter beneath the surface silt.",
        room_type="underground",
        indoor=True,
    )

    # ==================================================================
    #  RUINED WAYSTATIONS
    # ==================================================================
    ws_gatecourt = area.room(
        "ws_gatecourt",
        name="Waystation Gatecourt",
        desc="Worn threshold stones front a stophouse the Empire repaired only at the facade. Everything behind the gate still belongs to the older road.",
        room_type="path",
    )
    ws_broken_hostel = area.room(
        "ws_broken_hostel",
        name="Broken Hostel",
        desc="The main hall stands roofless except one patched corner where current traffic still shelters. Ledger nails line the walls in careful rows.",
        room_type="building",
        indoor=True,
    )
    ws_hearth_shell = area.room(
        "ws_hearth_shell",
        name="Hearth Shell",
        desc="A cold hearth sits under black rafters and faint tally scratches. Heat left this room long ago, but counting never did.",
        room_type="building",
        indoor=True,
    )
    ws_ledger_alcove = area.room(
        "ws_ledger_alcove",
        name="Ledger Alcove",
        desc="Shelves for guest ledgers survive behind a half-hanging shutter. Damp spared less paper than thieves did.",
        room_type="building",
        indoor=True,
    )
    ws_stable_ruin = area.room(
        "ws_stable_ruin",
        name="Stable Ruin",
        desc="Stone stalls remain while the timber roof has rotted away. Rings in the walls show this place served pack trains for a long time.",
        room_type="building",
        indoor=True,
    )
    ws_bucket_well = area.room(
        "ws_bucket_well",
        name="Bucket Well",
        desc="A ring well still draws sour water from under the station yard. The curb is polished by rope and impatient hands.",
        room_type="clearing",
    )
    ws_cart_shed = area.room(
        "ws_cart_shed",
        name="Cart Shed",
        desc="One lean-to shed still holds wheels, axles, pry bars, and sorted lengths of iron strap ready for salvage.",
        room_type="building",
        indoor=True,
    )
    ws_dormer_wall = area.room(
        "ws_dormer_wall",
        name="Dormer Wall",
        desc="A surviving upper wall walk offers a view over the station yard and the arch approach. The wall is safer than it looks and less safe than it promises.",
        room_type="ruins",
    )
    ws_salvage_square = area.room(
        "ws_salvage_square",
        name="Salvage Square",
        desc="Cut stone, bronze fittings, and sorted debris are stacked for resale in neat lots. The square smells of wet lime, dust, and profit.",
        room_type="clearing",
    )
    ws_waychapel = area.room(
        "ws_waychapel",
        name="Waychapel",
        desc="A small road chapel was fitted into one end of the station long before the current charter plates were nailed over it.",
        room_type="building",
        indoor=True,
    )
    ws_offering_step = area.room(
        "ws_offering_step",
        name="Offering Step",
        desc="Candle ends, reed ties, and copied prayers crowd a chipped step facing the waychapel door. The offerings ask for safe return more often than safe passage.",
        room_type="clearing",
    )
    ws_tack_room = area.room(
        "ws_tack_room",
        name="Tack Room",
        desc="Pegs, lockers, and patched harness straps line this tight chamber. Most good leather was taken years ago, but the smell lingers.",
        room_type="building",
        indoor=True,
    )
    ws_cellar_door = area.room(
        "ws_cellar_door",
        name="Cellar Door",
        desc="A thick trapdoor opens beneath an old ration room where flour dust and damp rope smell older than the rot around them.",
        room_type="building",
        indoor=True,
    )
    ws_cellar_run = area.room(
        "ws_cellar_run",
        name="Cellar Run",
        desc="A low cellar corridor extends under the station with scraped walls and footprints that do not belong to any official inventory.",
        room_type="underground",
        indoor=True,
    )
    ws_sidings_path = area.room(
        "ws_sidings_path",
        name="Sidings Path",
        desc="A narrow rear path runs behind the station toward older branch growth and spoil mounds. Traffic still favors it when the square grows crowded.",
        room_type="path",
    )
    ws_burned_loft = area.room(
        "ws_burned_loft",
        name="Burned Loft",
        desc="This upper room charred in neat lines that somehow spared the ledger alcove below. Someone burned selected memory here, not merely the building.",
        room_type="building",
        indoor=True,
    )
    ws_back_verge = area.room(
        "ws_back_verge",
        name="Back Verge",
        desc="Nettles and spoil heaps crowd the rear verge where broken crockery and axle pins vanish into the grass.",
        room_type="clearing",
    )
    ws_branch_west = area.room(
        "ws_branch_west",
        name="West Branch Gate",
        desc="Broken gateposts mark where the old branches peel away from the station lane. The main causeway wanted control; the branches kept options.",
        room_type="path",
    )

    # ==================================================================
    #  OVERGROWN BRANCH ROUTES
    # ==================================================================
    br_first_branch = area.room(
        "br_first_branch",
        name="First Branch",
        desc="Older paving peels away from the main route under creeping roots. The line is still deliberate even where the road is not.",
        room_type="path",
    )
    br_root_lane = area.room(
        "br_root_lane",
        name="Root Lane",
        desc="Tree roots lift whole blocks into a buckled lane. The road keeps its old width in spite of the trees trying to close it.",
        room_type="path",
    )
    br_half_buried_mark = area.room(
        "br_half_buried_mark",
        name="Half-Buried Mark",
        desc="Only the crown of a marker stone survives above moss and soil. Its number does not match the sequence cut on the main spine.",
        room_type="path",
    )
    br_green_cut = area.room(
        "br_green_cut",
        name="Green Cut",
        desc="Vegetation forms a corridor where survey crews keep chopping back growth just enough to prove continued claim.",
        room_type="path",
    )
    br_old_switch = area.room(
        "br_old_switch",
        name="Old Switch",
        desc="The route divides around a fallen lintel yet keeps the same measured spacing on both forks. The repetition is more unsettling than the ruin.",
        room_type="path",
    )
    br_stone_lattice = area.room(
        "br_stone_lattice",
        name="Stone Lattice",
        desc="Collapsed paving forms a patterned grid through moss and soil. The geometry survived even after the road lost its surface.",
        room_type="ruins",
    )
    br_lintel_grove = area.room(
        "br_lintel_grove",
        name="Lintel Grove",
        desc="Fallen lintels now serve as tree rings and shade frames. The grove grew through structure rather than over it.",
        room_type="clearing",
    )
    br_ivy_steps = area.room(
        "br_ivy_steps",
        name="Ivy Steps",
        desc="Narrow steps descend through ivy and broken capstone toward a route salvagers prefer not to announce.",
        room_type="ruins",
    )
    br_hidden_fork = area.room(
        "br_hidden_fork",
        name="Hidden Fork",
        desc="A half-concealed side route turns away beneath bramble and low stone. Foot traffic keeps it more open than the plants should allow.",
        room_type="path",
    )
    br_snare_walk = area.room(
        "br_snare_walk",
        name="Snare Walk",
        desc="Trip cords, hooks, and snapped loops hang among the shrubs. Whoever uses this branch plans for pursuit.",
        room_type="path",
    )
    br_waymarker_ring = area.room(
        "br_waymarker_ring",
        name="Waymarker Ring",
        desc="Six low markers encircle a cleared patch in stubborn symmetry. Later surveyors copied the spacing without ever explaining it.",
        room_type="clearing",
    )
    br_briar_gap = area.room(
        "br_briar_gap",
        name="Briar Gap",
        desc="A slit through the thorns opens onto a surprisingly straight run of old paving and scraped wheel lines.",
        room_type="path",
    )
    br_watcher_tree = area.room(
        "br_watcher_tree",
        name="Watcher Tree",
        desc="A bent tree grows through a socket clearly meant for stone or bronze. Whatever stood here first was removed with care.",
        room_type="clearing",
    )
    br_old_shrine = area.room(
        "br_old_shrine",
        name="Old Shrine",
        desc="Shrine stones sit beneath recent charter nails and a thin brass registry tab. Official custody did not make the place any newer.",
        room_type="ruins",
    )
    br_shrine_hollow = area.room(
        "br_shrine_hollow",
        name="Shrine Hollow",
        desc="A basin behind the shrine collects wax, rain, and the black grit of old incense. Small bones hide under the reeds.",
        room_type="clearing",
    )
    br_moss_bridge = area.room(
        "br_moss_bridge",
        name="Moss Bridge",
        desc="A narrow stone bridge crosses a shallow cut choked with green water and root-shadow.",
        room_type="ruins",
    )
    br_branch_pool = area.room(
        "br_branch_pool",
        name="Branch Pool",
        desc="Still water reflects paving blocks visible just under the surface. The branch road continues through memory better than through stone.",
        room_type="clearing",
    )
    br_return_grade = area.room(
        "br_return_grade",
        name="Return Grade",
        desc="The branch climbs again toward the drained reservoir works, dragging damp air uphill with it.",
        room_type="path",
    )
    br_far_branch = area.room(
        "br_far_branch",
        name="Far Branch",
        desc="The outer spur ends at broken survey stakes and a view over drainage lines that no current map bothers to show.",
        room_type="path",
    )
    br_reservoir_path = area.room(
        "br_reservoir_path",
        name="Reservoir Path",
        desc="Damp paving narrows toward the headworks ahead. Water once ruled this segment more than traffic did.",
        room_type="path",
    )

    # ==================================================================
    #  DRAINED RESERVOIR WORKS
    # ==================================================================
    rw_headworks = area.room(
        "rw_headworks",
        name="Headworks",
        desc="Cut stone gates and intake channels once regulated water feeding the corridor. Even dry, the place feels built for pressure.",
        room_type="ruins",
    )
    rw_dry_channel = area.room(
        "rw_dry_channel",
        name="Dry Channel",
        desc="An empty channel runs west with mineral lines far above your head. The water level was once much higher than comfort would suggest.",
        room_type="path",
    )
    rw_sluice_house = area.room(
        "rw_sluice_house",
        name="Sluice House",
        desc="Machinery housings and crank beds survive inside a damp stone shell. The Registry renamed this place, but the workings ignored the new title.",
        room_type="building",
        indoor=True,
    )
    rw_lower_stairs = area.room(
        "rw_lower_stairs",
        name="Lower Stairs",
        desc="Short stair flights descend toward the old basin in the same repeating run used elsewhere on the causeway.",
        room_type="underground",
        indoor=True,
    )
    rw_cistern_lip = area.room(
        "rw_cistern_lip",
        name="Cistern Lip",
        desc="The rim of a drained chamber glitters with salt, lime, and calcite where the water withdrew and left a hard memory behind.",
        room_type="underground",
        indoor=True,
    )
    rw_mineral_floor = area.room(
        "rw_mineral_floor",
        name="Mineral Floor",
        desc="Pale crust and broken fittings crack underfoot on the chamber floor. A careless step wakes sharp echoes.",
        room_type="underground",
        indoor=True,
    )
    rw_sump_bridge = area.room(
        "rw_sump_bridge",
        name="Sump Bridge",
        desc="A narrow bridge crosses the deepest sump of the drained works. The pit below still holds dark water and older things than water.",
        room_type="underground",
        indoor=True,
    )
    rw_drowned_records = area.room(
        "rw_drowned_records",
        name="Drowned Records",
        desc="Burst document boxes lie matted against the wall where floodwater once pinned them. Whole names survive only because the silt covered them.",
        room_type="underground",
        indoor=True,
    )
    rw_valve_walk = area.room(
        "rw_valve_walk",
        name="Valve Walk",
        desc="Iron valve posts march along a ledge beside the basin. Their spacing matches the counted stones up on the causeway.",
        room_type="underground",
        indoor=True,
    )
    rw_resonance_pit = area.room(
        "rw_resonance_pit",
        name="Resonance Pit",
        desc="The pit below answers footsteps with a delayed hum that climbs the walls in numbered pulses.",
        room_type="underground",
        indoor=True,
    )
    rw_gate_mechanism = area.room(
        "rw_gate_mechanism",
        name="Gate Mechanism",
        desc="Massive stone gears remain locked in place by bronze pins. They look built to outlast titles, charters, and the hands that named them.",
        room_type="underground",
        indoor=True,
    )
    rw_basin_floor = area.room(
        "rw_basin_floor",
        name="Basin Floor",
        desc="The main reservoir basin is now a silted bowl full of cracked plates, exposed channels, and stubborn damp.",
        room_type="underground",
        indoor=True,
    )
    rw_herb_ledge = area.room(
        "rw_herb_ledge",
        name="Herb Ledge",
        desc="A damp ledge supports pale herbs that thrive on mineral seep and old mortar dust.",
        room_type="underground",
        indoor=True,
    )
    rw_dark_siphon = area.room(
        "rw_dark_siphon",
        name="Dark Siphon",
        desc="A black tunnel mouth drinks the little water that remains. The channel beyond is too smooth and too deliberate to be a cave accident.",
        room_type="cave",
        indoor=True,
    )
    rw_hidden_conduit = area.room(
        "rw_hidden_conduit",
        name="Hidden Conduit",
        desc="A maintenance conduit cut with unnerving precision runs behind the basin wall. It links the works to spaces the current charts omit.",
        room_type="underground",
        indoor=True,
    )
    rw_shrine_niche = area.room(
        "rw_shrine_niche",
        name="Shrine Niche",
        desc="A recessed basin and soot-black wall survive here behind the official machinery. Someone kept a sacred corner inside the works themselves.",
        room_type="underground",
        indoor=True,
    )
    rw_ward_core = area.room(
        "rw_ward_core",
        name="Ward Core",
        desc="A ring of numbered stone posts guards the heart of the reservoir. The sequence cut into them is older than any Circle notation now in use.",
        room_type="underground",
        indoor=True,
    )
    rw_court_ascent = area.room(
        "rw_court_ascent",
        name="Court Ascent",
        desc="Steps climb from the drained works toward a paved survey court open to daylight. The transition feels ceremonial rather than practical.",
        room_type="path",
    )

    # ==================================================================
    #  SURVEY CIRCLE / OLD COURT
    # ==================================================================
    sc_outer_ring = area.room(
        "sc_outer_ring",
        name="Outer Ring",
        desc="Circular paving surrounds the old court in measured bands. The geometry here is still exact enough to make the eye uneasy.",
        room_type="clearing",
    )
    sc_numbered_dais = area.room(
        "sc_numbered_dais",
        name="Numbered Dais",
        desc="A raised dais bears repeating numeric sequences under later civic seals. The later text looks like a cover sheet pinned over stone.",
        room_type="ruins",
    )
    sc_broken_bench = area.room(
        "sc_broken_bench",
        name="Broken Bench",
        desc="Bench fragments lie arranged as if moved by rule rather than collapse. Nothing here feels purely accidental.",
        room_type="clearing",
    )
    sc_copy_stand = area.room(
        "sc_copy_stand",
        name="Copy Stand",
        desc="A sloped stone stand still bears charcoal smears from copied rubbings and hurried field notes.",
        room_type="ruins",
    )
    sc_measure_seat = area.room(
        "sc_measure_seat",
        name="Measure Seat",
        desc="A high-backed survey chair faces the ring center with faint grooves worn into both arms by repeated use.",
        room_type="ruins",
    )
    sc_charter_wall = area.room(
        "sc_charter_wall",
        name="Charter Wall",
        desc="Plaques from successive regimes cover this wall, each claiming the court as restoration rather than inheritance.",
        room_type="ruins",
    )
    sc_inner_circle = area.room(
        "sc_inner_circle",
        name="Inner Circle",
        desc="The tighter inner ring sits unnervingly true despite weather, theft, and revision. Standing here makes every other line feel like an imitation.",
        room_type="clearing",
    )
    sc_witness_step = area.room(
        "sc_witness_step",
        name="Witness Step",
        desc="A low step marks where observers once stood while measurements or judgments were taken.",
        room_type="ruins",
    )
    sc_removed_stone = area.room(
        "sc_removed_stone",
        name="Removed Stone",
        desc="One carefully extracted block leaves a raw absence in the ring. The surrounding cut marks are tidier than any collapse would be.",
        room_type="ruins",
    )
    sc_court_hollow = area.room(
        "sc_court_hollow",
        name="Court Hollow",
        desc="Ash, filings, and old wax gather in the hollow at the center of the court where records and verdicts once converged.",
        room_type="clearing",
    )
    sc_orbit_path = area.room(
        "sc_orbit_path",
        name="Orbit Path",
        desc="A narrow walking lane follows the perimeter of the old court in one exact curve after another.",
        room_type="path",
    )
    sc_reviser_niche = area.room(
        "sc_reviser_niche",
        name="Reviser Niche",
        desc="Snapped styluses, charcoal stubs, and ruined paper crowd this tucked niche where later officials worked over older text.",
        room_type="ruins",
    )
    sc_line_house = area.room(
        "sc_line_house",
        name="Line House",
        desc="A small office kept chains, rods, and rolled copies dry behind thick stone and a mean little door.",
        room_type="building",
        indoor=True,
    )
    sc_chain_hook = area.room(
        "sc_chain_hook",
        name="Chain Hook",
        desc="Bronze hooks line one wall in counted pairs, ready for measured chain and confiscated tools alike.",
        room_type="building",
        indoor=True,
    )
    sc_far_disc = area.room(
        "sc_far_disc",
        name="Far Disc",
        desc="An outer platform looks west across the older corridor and its broken claims. The view makes the city seem late to its own history.",
        room_type="clearing",
    )
    sc_old_verdict = area.room(
        "sc_old_verdict",
        name="Old Verdict",
        desc="An inscription slab gives procedural instructions that no current office repeats but no one has fully removed either.",
        room_type="ruins",
    )
    sc_survey_fire = area.room(
        "sc_survey_fire",
        name="Survey Fire",
        desc="A long-used field fire ring sits beside the court edge where later crews camped among older authorities.",
        room_type="clearing",
    )
    sc_west_edge = area.room(
        "sc_west_edge",
        name="West Edge",
        desc="The paved court ends at a ragged western drop where the old corridor finally loosens into open ruin and country.",
        room_type="clearing",
    )

    # ==================================================================
    #  EXITS
    # ==================================================================
    area.exit(bs_postern_landing, "varath_prime:mw_causeway_postern", "east")
    area.exit(bs_postern_landing, bs_numbered_span, "west")
    area.exit(bs_numbered_span, bs_postern_landing, "east")
    area.exit(bs_numbered_span, bs_split_mile, "west")
    area.exit(bs_split_mile, bs_numbered_span, "east")
    area.exit(bs_split_mile, bs_gap_brace, "west")
    area.exit(bs_gap_brace, bs_split_mile, "east")
    area.exit(bs_gap_brace, bs_echo_joint, "west")
    area.exit(bs_echo_joint, bs_gap_brace, "east")
    area.exit(bs_echo_joint, bs_culvert_mouth, "west")
    area.exit(bs_culvert_mouth, bs_echo_joint, "east")
    area.exit(bs_culvert_mouth, bs_patchwork_ramp, "west")
    area.exit(bs_patchwork_ramp, bs_culvert_mouth, "east")
    area.exit(bs_patchwork_ramp, bs_recut_plate, "west")
    area.exit(bs_recut_plate, bs_patchwork_ramp, "east")
    area.exit(bs_recut_plate, bs_shiver_span, "west")
    area.exit(bs_shiver_span, bs_recut_plate, "east")
    area.exit(bs_shiver_span, bs_survey_notch, "west")
    area.exit(bs_survey_notch, bs_shiver_span, "east")
    area.exit(bs_survey_notch, bs_broken_guardrail, "west")
    area.exit(bs_broken_guardrail, bs_survey_notch, "east")
    area.exit(bs_broken_guardrail, bs_long_crack, "west")
    area.exit(bs_long_crack, bs_broken_guardrail, "east")
    area.exit(bs_long_crack, bs_mended_cause, "west")
    area.exit(bs_mended_cause, bs_long_crack, "east")
    area.exit(bs_mended_cause, bs_counting_stones, "west")
    area.exit(bs_counting_stones, bs_mended_cause, "east")
    area.exit(bs_counting_stones, bs_far_break, "west")
    area.exit(bs_far_break, bs_counting_stones, "east")
    area.exit(bs_far_break, bs_arch_threshold, "west")
    area.exit(bs_arch_threshold, bs_far_break, "east")
    area.exit(bs_split_mile, bs_shorn_plaque, "north")
    area.exit(bs_shorn_plaque, bs_split_mile, "south")
    area.exit(bs_numbered_span, bs_side_slab, "south")
    area.exit(bs_side_slab, bs_numbered_span, "north")
    area.exit(bs_echo_joint, bs_watch_niche, "north")
    area.exit(bs_watch_niche, bs_echo_joint, "south")
    area.exit(bs_echo_joint, bs_marker_hollow, "south")
    area.exit(bs_marker_hollow, bs_echo_joint, "north")
    area.exit(bs_culvert_mouth, bs_third_marker, "south")
    area.exit(bs_third_marker, bs_culvert_mouth, "north")
    area.exit(bs_shiver_span, bs_shrine_pull, "south")
    area.exit(bs_shrine_pull, bs_shiver_span, "north")
    area.exit(bs_recut_plate, bs_seal_bench, "north")
    area.exit(bs_seal_bench, bs_recut_plate, "south")
    area.exit(bs_broken_guardrail, bs_drop_sounding, "south")
    area.exit(bs_drop_sounding, bs_broken_guardrail, "north")

    area.exit(bs_arch_threshold, ar_first_arch, "west")
    area.exit(ar_first_arch, bs_arch_threshold, "east")
    area.exit(ar_first_arch, ar_shadow_underspan, "west")
    area.exit(ar_shadow_underspan, ar_first_arch, "east")
    area.exit(ar_shadow_underspan, ar_broken_pier, "west")
    area.exit(ar_broken_pier, ar_shadow_underspan, "east")
    area.exit(ar_broken_pier, ar_echo_chamber, "west")
    area.exit(ar_echo_chamber, ar_broken_pier, "east")
    area.exit(ar_echo_chamber, ar_drip_gallery, "west")
    area.exit(ar_drip_gallery, ar_echo_chamber, "east")
    area.exit(ar_drip_gallery, ar_fallen_bays, "west")
    area.exit(ar_fallen_bays, ar_drip_gallery, "east")
    area.exit(ar_fallen_bays, ar_undercourt, "west")
    area.exit(ar_undercourt, ar_fallen_bays, "east")
    area.exit(ar_undercourt, ar_cracked_keystone, "west")
    area.exit(ar_cracked_keystone, ar_undercourt, "east")
    area.exit(ar_cracked_keystone, ar_second_underspan, "west")
    area.exit(ar_second_underspan, ar_cracked_keystone, "east")
    area.exit(ar_second_underspan, ar_far_arch, "west")
    area.exit(ar_far_arch, ar_second_underspan, "east")
    area.exit(ar_far_arch, ar_waystation_turn, "west")
    area.exit(ar_waystation_turn, ar_far_arch, "east")
    area.exit(ar_shadow_underspan, ar_hook_ladder, "north")
    area.exit(ar_hook_ladder, ar_shadow_underspan, "south")
    area.exit(ar_hook_ladder, ar_upper_rib, "up")
    area.exit(ar_upper_rib, ar_hook_ladder, "down")
    area.exit(ar_broken_pier, ar_low_squeeze, "down")
    area.exit(ar_low_squeeze, ar_broken_pier, "up")
    area.exit(ar_low_squeeze, ar_hidden_apse, "west")
    area.exit(ar_hidden_apse, ar_low_squeeze, "east")
    area.exit(ar_drip_gallery, ar_arch_roost, "up")
    area.exit(ar_arch_roost, ar_drip_gallery, "down")
    area.exit(ar_fallen_bays, ar_collapse_nest, "south")
    area.exit(ar_collapse_nest, ar_fallen_bays, "north")
    area.exit(ar_cracked_keystone, ar_dust_landing, "north")
    area.exit(ar_dust_landing, ar_cracked_keystone, "south")
    area.exit(ar_second_underspan, ar_repeater_stair, "up")
    area.exit(ar_repeater_stair, ar_second_underspan, "down")
    area.exit(ar_repeater_stair, ar_shaft_pool, "west")
    area.exit(ar_shaft_pool, ar_repeater_stair, "east")

    area.exit(ar_waystation_turn, ws_gatecourt, "west")
    area.exit(ws_gatecourt, ar_waystation_turn, "east")
    area.exit(ws_gatecourt, ws_salvage_square, "west")
    area.exit(ws_salvage_square, ws_gatecourt, "east")
    area.exit(ws_salvage_square, ws_broken_hostel, "west")
    area.exit(ws_broken_hostel, ws_salvage_square, "east")
    area.exit(ws_broken_hostel, ws_hearth_shell, "west")
    area.exit(ws_hearth_shell, ws_broken_hostel, "east")
    area.exit(ws_hearth_shell, ws_ledger_alcove, "west")
    area.exit(ws_ledger_alcove, ws_hearth_shell, "east")
    area.exit(ws_ledger_alcove, ws_stable_ruin, "west")
    area.exit(ws_stable_ruin, ws_ledger_alcove, "east")
    area.exit(ws_stable_ruin, ws_bucket_well, "west")
    area.exit(ws_bucket_well, ws_stable_ruin, "east")
    area.exit(ws_bucket_well, ws_waychapel, "west")
    area.exit(ws_waychapel, ws_bucket_well, "east")
    area.exit(ws_waychapel, ws_offering_step, "west")
    area.exit(ws_offering_step, ws_waychapel, "east")
    area.exit(ws_offering_step, ws_sidings_path, "west")
    area.exit(ws_sidings_path, ws_offering_step, "east")
    area.exit(ws_sidings_path, ws_branch_west, "west")
    area.exit(ws_branch_west, ws_sidings_path, "east")
    area.exit(ws_salvage_square, ws_cart_shed, "south")
    area.exit(ws_cart_shed, ws_salvage_square, "north")
    area.exit(ws_broken_hostel, ws_dormer_wall, "up")
    area.exit(ws_dormer_wall, ws_broken_hostel, "down")
    area.exit(ws_ledger_alcove, ws_burned_loft, "up")
    area.exit(ws_burned_loft, ws_ledger_alcove, "down")
    area.exit(ws_stable_ruin, ws_tack_room, "south")
    area.exit(ws_tack_room, ws_stable_ruin, "north")
    area.exit(ws_hearth_shell, ws_cellar_door, "down")
    area.exit(ws_cellar_door, ws_hearth_shell, "up")
    area.exit(ws_cellar_door, ws_cellar_run, "west")
    area.exit(ws_cellar_run, ws_cellar_door, "east")
    area.exit(ws_sidings_path, ws_back_verge, "south")
    area.exit(ws_back_verge, ws_sidings_path, "north")

    area.exit(ws_branch_west, br_first_branch, "west")
    area.exit(br_first_branch, ws_branch_west, "east")
    area.exit(br_first_branch, br_root_lane, "west")
    area.exit(br_root_lane, br_first_branch, "east")
    area.exit(br_root_lane, br_half_buried_mark, "west")
    area.exit(br_half_buried_mark, br_root_lane, "east")
    area.exit(br_half_buried_mark, br_green_cut, "west")
    area.exit(br_green_cut, br_half_buried_mark, "east")
    area.exit(br_green_cut, br_old_switch, "west")
    area.exit(br_old_switch, br_green_cut, "east")
    area.exit(br_old_switch, br_stone_lattice, "west")
    area.exit(br_stone_lattice, br_old_switch, "east")
    area.exit(br_stone_lattice, br_waymarker_ring, "west")
    area.exit(br_waymarker_ring, br_stone_lattice, "east")
    area.exit(br_waymarker_ring, br_old_shrine, "west")
    area.exit(br_old_shrine, br_waymarker_ring, "east")
    area.exit(br_old_shrine, br_moss_bridge, "west")
    area.exit(br_moss_bridge, br_old_shrine, "east")
    area.exit(br_moss_bridge, br_return_grade, "west")
    area.exit(br_return_grade, br_moss_bridge, "east")
    area.exit(br_return_grade, br_reservoir_path, "west")
    area.exit(br_reservoir_path, br_return_grade, "east")
    area.exit(br_old_switch, br_lintel_grove, "north")
    area.exit(br_lintel_grove, br_old_switch, "south")
    area.exit(br_stone_lattice, br_ivy_steps, "south")
    area.exit(br_ivy_steps, br_stone_lattice, "north")
    area.exit(br_ivy_steps, br_hidden_fork, "west")
    area.exit(br_hidden_fork, br_ivy_steps, "east")
    area.exit(br_hidden_fork, br_snare_walk, "west")
    area.exit(br_snare_walk, br_hidden_fork, "east")
    area.exit(br_waymarker_ring, br_briar_gap, "south")
    area.exit(br_briar_gap, br_waymarker_ring, "north")
    area.exit(br_waymarker_ring, br_watcher_tree, "north")
    area.exit(br_watcher_tree, br_waymarker_ring, "south")
    area.exit(br_old_shrine, br_shrine_hollow, "south")
    area.exit(br_shrine_hollow, br_old_shrine, "north")
    area.exit(br_moss_bridge, br_branch_pool, "south")
    area.exit(br_branch_pool, br_moss_bridge, "north")
    area.exit(br_return_grade, br_far_branch, "south")
    area.exit(br_far_branch, br_return_grade, "north")

    area.exit(br_reservoir_path, rw_headworks, "west")
    area.exit(rw_headworks, br_reservoir_path, "east")
    area.exit(rw_headworks, rw_dry_channel, "west")
    area.exit(rw_dry_channel, rw_headworks, "east")
    area.exit(rw_dry_channel, rw_sluice_house, "west")
    area.exit(rw_sluice_house, rw_dry_channel, "east")
    area.exit(rw_sluice_house, rw_lower_stairs, "down")
    area.exit(rw_lower_stairs, rw_sluice_house, "up")
    area.exit(rw_lower_stairs, rw_cistern_lip, "west")
    area.exit(rw_cistern_lip, rw_lower_stairs, "east")
    area.exit(rw_cistern_lip, rw_sump_bridge, "west")
    area.exit(rw_sump_bridge, rw_cistern_lip, "east")
    area.exit(rw_sump_bridge, rw_valve_walk, "west")
    area.exit(rw_valve_walk, rw_sump_bridge, "east")
    area.exit(rw_valve_walk, rw_gate_mechanism, "west")
    area.exit(rw_gate_mechanism, rw_valve_walk, "east")
    area.exit(rw_gate_mechanism, rw_basin_floor, "west")
    area.exit(rw_basin_floor, rw_gate_mechanism, "east")
    area.exit(rw_basin_floor, rw_ward_core, "west")
    area.exit(rw_ward_core, rw_basin_floor, "east")
    area.exit(rw_ward_core, rw_court_ascent, "west")
    area.exit(rw_court_ascent, rw_ward_core, "east")
    area.exit(rw_cistern_lip, rw_mineral_floor, "down")
    area.exit(rw_mineral_floor, rw_cistern_lip, "up")
    area.exit(rw_sump_bridge, rw_drowned_records, "north")
    area.exit(rw_drowned_records, rw_sump_bridge, "south")
    area.exit(rw_valve_walk, rw_resonance_pit, "down")
    area.exit(rw_resonance_pit, rw_valve_walk, "up")
    area.exit(rw_basin_floor, rw_herb_ledge, "north")
    area.exit(rw_herb_ledge, rw_basin_floor, "south")
    area.exit(rw_basin_floor, rw_dark_siphon, "down")
    area.exit(rw_dark_siphon, rw_basin_floor, "up")
    area.exit(rw_dark_siphon, rw_hidden_conduit, "west")
    area.exit(rw_hidden_conduit, rw_dark_siphon, "east")
    area.exit(rw_ward_core, rw_shrine_niche, "south")
    area.exit(rw_shrine_niche, rw_ward_core, "north")

    area.exit(rw_court_ascent, sc_outer_ring, "up")
    area.exit(sc_outer_ring, rw_court_ascent, "down")
    area.exit(sc_outer_ring, sc_numbered_dais, "west")
    area.exit(sc_numbered_dais, sc_outer_ring, "east")
    area.exit(sc_numbered_dais, sc_measure_seat, "west")
    area.exit(sc_measure_seat, sc_numbered_dais, "east")
    area.exit(sc_measure_seat, sc_charter_wall, "west")
    area.exit(sc_charter_wall, sc_measure_seat, "east")
    area.exit(sc_charter_wall, sc_inner_circle, "west")
    area.exit(sc_inner_circle, sc_charter_wall, "east")
    area.exit(sc_inner_circle, sc_witness_step, "west")
    area.exit(sc_witness_step, sc_inner_circle, "east")
    area.exit(sc_witness_step, sc_court_hollow, "west")
    area.exit(sc_court_hollow, sc_witness_step, "east")
    area.exit(sc_court_hollow, sc_orbit_path, "west")
    area.exit(sc_orbit_path, sc_court_hollow, "east")
    area.exit(sc_orbit_path, sc_far_disc, "west")
    area.exit(sc_far_disc, sc_orbit_path, "east")
    area.exit(sc_far_disc, sc_west_edge, "west")
    area.exit(sc_west_edge, sc_far_disc, "east")
    area.exit(sc_numbered_dais, sc_broken_bench, "south")
    area.exit(sc_broken_bench, sc_numbered_dais, "north")
    area.exit(sc_measure_seat, sc_copy_stand, "north")
    area.exit(sc_copy_stand, sc_measure_seat, "south")
    area.exit(sc_charter_wall, sc_line_house, "south")
    area.exit(sc_line_house, sc_charter_wall, "north")
    area.exit(sc_line_house, sc_chain_hook, "south")
    area.exit(sc_chain_hook, sc_line_house, "north")
    area.exit(sc_inner_circle, sc_removed_stone, "south")
    area.exit(sc_removed_stone, sc_inner_circle, "north")
    area.exit(sc_orbit_path, sc_reviser_niche, "north")
    area.exit(sc_reviser_niche, sc_orbit_path, "south")
    area.exit(sc_far_disc, sc_old_verdict, "south")
    area.exit(sc_old_verdict, sc_far_disc, "north")
    area.exit(sc_west_edge, sc_survey_fire, "north")
    area.exit(sc_survey_fire, sc_west_edge, "south")

    area.exit(ws_cellar_run, br_hidden_fork, "south", hidden=True)
    area.exit(br_hidden_fork, ws_cellar_run, "north", hidden=True)
    area.exit(ar_hidden_apse, rw_hidden_conduit, "down", hidden=True)
    area.exit(rw_hidden_conduit, ar_hidden_apse, "up", hidden=True)

    # ==================================================================
    #  SPAWNS
    # ==================================================================
    area.spawn(bs_side_slab, "causeway_scavenger", count_min=1, count_max=1, respawn_minutes=24, respawn_variance=6)
    area.spawn(bs_marker_hollow, "dust_hound", count_min=1, count_max=2, respawn_minutes=25, respawn_variance=6)
    area.spawn(bs_shrine_pull, "causeway_scavenger", count_min=0, count_max=1, respawn_minutes=26, respawn_variance=7)
    area.spawn(bs_drop_sounding, "causeway_scavenger", count_min=1, count_max=2, respawn_minutes=28, respawn_variance=8)
    area.spawn(ar_low_squeeze, "culvert_lurker", count_min=1, count_max=1, respawn_minutes=30, respawn_variance=8)
    area.spawn(ar_collapse_nest, "shard_swarm", count_min=1, count_max=2, respawn_minutes=20, respawn_variance=5)
    area.spawn(ar_shaft_pool, "culvert_lurker", count_min=1, count_max=1, respawn_minutes=29, respawn_variance=7)
    area.spawn(ar_arch_roost, "cave_spider", count_min=0, count_max=1, respawn_minutes=22, respawn_variance=5)
    area.spawn(ws_salvage_square, "salvager_cutthroat", count_min=1, count_max=2, respawn_minutes=26, respawn_variance=7)
    area.spawn(ws_cellar_run, "cave_spider", count_min=1, count_max=1, respawn_minutes=21, respawn_variance=5)
    area.spawn(br_snare_walk, "salvager_cutthroat", count_min=1, count_max=1, respawn_minutes=25, respawn_variance=6)
    area.spawn(br_shrine_hollow, "causeway_scavenger", count_min=0, count_max=1, respawn_minutes=26, respawn_variance=7)
    area.spawn(br_branch_pool, "dust_hound", count_min=1, count_max=1, respawn_minutes=24, respawn_variance=6)
    area.spawn(rw_mineral_floor, "culvert_lurker", count_min=1, count_max=1, respawn_minutes=30, respawn_variance=8)
    area.spawn(rw_dark_siphon, "cave_spider", count_min=1, count_max=2, respawn_minutes=23, respawn_variance=5)
    area.spawn(rw_hidden_conduit, "shard_swarm", count_min=1, count_max=1, respawn_minutes=22, respawn_variance=5)
    area.spawn(rw_shrine_niche, "stone_golem_fragment", count_min=0, count_max=1, respawn_minutes=40, respawn_variance=10)
    area.spawn(sc_removed_stone, "causeway_scavenger", count_min=1, count_max=1, respawn_minutes=24, respawn_variance=6)
    area.spawn(sc_chain_hook, "salvager_cutthroat", count_min=0, count_max=1, respawn_minutes=27, respawn_variance=7)
    area.spawn(sc_old_verdict, "shard_swarm", count_min=1, count_max=2, respawn_minutes=20, respawn_variance=5)

    area.named_mob(
        "surveyor_maelik_dross",
        sc_inner_circle,
        respawn_minutes=190,
        respawn_variance=40,
        prestige_modifier=2.1,
        behavior=["erratic"],
        base_disposition=-0.9,
        flee_threshold=5,
        tome_drop="causeway_survey_tome",
    )
    area.named_mob(
        "ninth_reservoir_warden",
        rw_ward_core,
        respawn_minutes=240,
        respawn_variance=50,
        prestige_modifier=2.3,
        behavior=["guardian"],
        base_disposition=-1.0,
        flee_threshold=0,
        tome_drop="causeway_ward_tome",
    )

    # ==================================================================
    #  NPCS
    # ==================================================================
    area.npc(bs_postern_landing, "npc_postern_keeper_loras", faction="empire")
    area.npc(bs_seal_bench, "npc_stone_reader_miren", faction="empire")
    area.npc(ws_ledger_alcove, "npc_archivist_runner_pela", faction="empire")
    _waystation_host = area.npc(ws_gatecourt, "npc_waystation_host_tam", faction="consortium")
    _waystation_host.db.is_vendor = True
    _waystation_host.db.vendor_accepts = ["consumable"]
    _waystation_host.db.vendor_item_ids = [
        "trail_rations",
        "bandage",
        "minor_healing_potion",
        "minor_stamina_potion",
        "antidote_potion",
    ]
    area.npc(ws_salvage_square, "npc_salvage_factor_brel", faction="consortium")
    area.npc(br_hidden_fork, "npc_branch_guide_siven", faction="consortium")
    area.npc(br_old_shrine, "npc_shrine_keeper_odan")
    area.npc(rw_headworks, "npc_headworks_keeper_ulen", faction="circle")
    area.npc(rw_herb_ledge, "npc_cistern_herbalist_vela", faction="circle")
    area.npc(sc_copy_stand, "npc_circle_fieldreader_tern", faction="circle")
    area.npc(sc_charter_wall, "npc_court_copyist_ressa", faction="empire")

    # ==================================================================
    #  ITEMS
    # ==================================================================
    area.item(
        "sealed_revision_packet",
        key="Sealed Revision Packet",
        item_type="item",
        weight=0.2,
        rarity="normal",
        value=0,
        is_quest_item=True,
        desc="A wax-sealed packet of revised road text meant for the old court copy desk before someone strips another plaque bare.",
    )
    area.item(
        "mineral_residue_packet",
        key="Mineral Residue Packet",
        item_type="item",
        weight=0.2,
        rarity="normal",
        value=0,
        is_quest_item=True,
        desc="A wrapped paper packet of calcite dust, cistern salt, and scraped residue from the drained works, prepared for Circle review.",
    )

    # ==================================================================
    #  LORE FRAGMENTS
    # ==================================================================
    area.lore_fragment(
        "oc_lore_shorn_decree",
        bs_shorn_plaque,
        discovery_method="search",
        scholar_path="arcana",
        text="The shaved plaque still preserves part of an older line beneath the Crown Restoration Charter of 711: prior text removed, copy accepted in place of stone, corridor returned to lawful passage by declaration alone.",
        insight_gain=2,
    )
    area.lore_fragment(
        "oc_lore_count_cycle",
        bs_counting_stones,
        discovery_method="search",
        scholar_path="resonance",
        text="Each sixth stone along this stretch bears the same hidden cut, proving the count cycle predates both the Edict of Measured Passage and the current city wall alignment.",
        insight_gain=2,
    )
    area.lore_fragment(
        "oc_lore_arch_revision",
        ar_cracked_keystone,
        discovery_method="search",
        scholar_path="remnance",
        text="The keystone carries one number sequence recut over another. The measured rod seal sits on the newer face, but the deeper older count still controls the arch spacing around it.",
        insight_gain=3,
    )
    area.lore_fragment(
        "oc_lore_hidden_apse_copy",
        ar_hidden_apse,
        discovery_method="search",
        scholar_path="arcana",
        text="A copied survey leaf hidden in the apse notes that a prior chamber plan was withheld from the Registry and replaced by a cleaner drawing for capital review.",
        insight_gain=2,
    )
    area.lore_fragment(
        "oc_lore_waystation_roll",
        ws_ledger_alcove,
        discovery_method="search",
        scholar_path="remnance",
        text="The surviving guest roll lists teamsters, copy clerks, and shrine tenders delayed on the causeway. Several names end in the same notation: disposition omitted by instruction.",
        insight_gain=3,
    )
    area.lore_fragment(
        "oc_lore_branch_ring",
        br_waymarker_ring,
        discovery_method="search",
        scholar_path="resonance",
        text="One branch marker rubbing attributes the ring not to Imperial survey but to an older boundary court that later offices merely numbered and copied.",
        insight_gain=2,
    )
    area.lore_fragment(
        "oc_lore_shrine_reassignment",
        br_old_shrine,
        discovery_method="search",
        scholar_path="arcana",
        text="A brass tab nailed to the shrine grants the site to maintenance custody under revised charter, yet the backing stone names no Empire at all.",
        insight_gain=2,
    )
    area.lore_fragment(
        "oc_lore_drowned_registry",
        rw_drowned_records,
        discovery_method="search",
        scholar_path="remnance",
        text="Water-swollen registry leaves show route access reassigned without witness during one reservoir closure. Several corrected entries point back to the Ministry Ward postern.",
        insight_gain=3,
    )
    area.lore_fragment(
        "oc_lore_ward_sequence",
        rw_ward_core,
        discovery_method="search",
        scholar_path="resonance",
        text="The ward posts are cut with a nine-part sequence no current Circle notation explains. Later chalk labels merely copy the order and pretend authorship.",
        insight_gain=2,
    )
    area.lore_fragment(
        "oc_lore_charter_stack",
        sc_charter_wall,
        discovery_method="search",
        scholar_path="arcana",
        text="The charter wall frames each regime as restoration, but the oldest surviving slab calls the court assumed rather than founded. The Empire inherited authority here and then engraved over the admission.",
        insight_gain=3,
    )

    # ==================================================================
    #  QUESTS
    # ==================================================================
    area.quest(
        "oc_q_revision_packet",
        name="Revision Packet",
        description="Archivist Runner Pela needs a sealed revision packet carried across the old court before another plaque is stripped or copied over.",
        quest_type="delivery",
        quest_giver="npc_archivist_runner_pela",
        objectives=[
            {
                "type": "deliver",
                "target": "npc_court_copyist_ressa",
                "count": 1,
                "description": "Deliver the sealed revision packet to Court Copyist Ressa",
            },
        ],
        flagged_drop="sealed_revision_packet",
        rewards=[
            {"action_type": "give_scales", "amount": 75},
            {"action_type": "modify_standing", "faction_id": "empire", "delta": 70},
            {"action_type": "echo", "message": "|gPela exhales. \"Good. Let the court lose the truth on purpose, not by accident.\"|n"},
        ],
        next_quest_id="oc_q_removed_numbers",
        objective_type="deliver",
        objective_target="npc_court_copyist_ressa",
        objective_count=1,
    )
    area.quest(
        "oc_q_removed_numbers",
        name="Removed Numbers",
        description="Stone Reader Miren wants the causeway scavengers driven off before they pry out more numbered blocks and sell the corridor by the fragment.",
        quest_type="kill",
        quest_giver="npc_stone_reader_miren",
        prerequisite_quests=["oc_q_revision_packet"],
        objectives=[
            {
                "type": "kill",
                "target": "causeway_scavenger",
                "count": 4,
                "description": "Defeat causeway scavengers stripping numbered stone",
            },
        ],
        rewards=[
            {"action_type": "give_scales", "amount": 95},
            {"action_type": "modify_standing", "faction_id": "empire", "delta": 90},
            {"action_type": "echo", "message": "|gMiren runs his thumb over an old cut line. \"If they take enough numbers, the lie wins by vacancy.\"|n"},
        ],
        objective_type="kill",
        objective_target="causeway_scavenger",
        objective_count=4,
    )
    area.quest(
        "oc_q_hidden_ways",
        name="Hidden Ways",
        description="Branch Guide Siven wants the quiet routes checked before cutthroats or clerks close them for good.",
        quest_type="investigation",
        quest_giver="npc_branch_guide_siven",
        objectives=[
            {
                "type": "investigate",
                "target": "ws_cellar_run",
                "count": 1,
                "description": "Inspect the cellar run beneath the waystation",
            },
            {
                "type": "investigate",
                "target": "br_hidden_fork",
                "count": 1,
                "description": "Trace the hidden fork through the branch route",
            },
            {
                "type": "investigate",
                "target": "rw_hidden_conduit",
                "count": 1,
                "description": "Confirm the conduit path behind the reservoir wall",
            },
        ],
        rewards=[
            {"action_type": "give_scales", "amount": 90},
            {"action_type": "modify_standing", "faction_id": "consortium", "delta": 80},
            {"action_type": "echo", "message": "|gSiven nods once. \"A road stays alive by the paths officials cannot tidy.\"|n"},
        ],
        objective_type="investigate",
        objective_target="ws_cellar_run",
        objective_count=3,
    )
    area.quest(
        "oc_q_cistern_proof",
        name="Cistern Proof",
        description="Cistern Herbalist Vela has prepared a residue packet from the drained works and wants it in Circle hands before the headworks get closed again.",
        quest_type="delivery",
        quest_giver="npc_cistern_herbalist_vela",
        objectives=[
            {
                "type": "deliver",
                "target": "npc_circle_fieldreader_tern",
                "count": 1,
                "description": "Deliver the mineral residue packet to Fieldreader Tern",
            },
        ],
        flagged_drop="mineral_residue_packet",
        rewards=[
            {"action_type": "give_scales", "amount": 80},
            {"action_type": "modify_standing", "faction_id": "circle", "delta": 85},
            {"action_type": "echo", "message": "|gVela brushes white dust from her hands. \"If the residue matches the old sequence, the court was never what the wall says.\"|n"},
        ],
        next_quest_id="oc_q_missing_surveyor",
        objective_type="deliver",
        objective_target="npc_circle_fieldreader_tern",
        objective_count=1,
    )
    area.quest(
        "oc_q_missing_surveyor",
        name="Missing Surveyor",
        description="Fieldreader Tern says Surveyor Maelik Dross vanished from the court years ago, yet newer copy leaves still use his measurements. Find him where the rings stayed true.",
        quest_type="kill",
        quest_giver="npc_circle_fieldreader_tern",
        prerequisite_quests=["oc_q_cistern_proof"],
        objectives=[
            {
                "type": "kill",
                "target": "surveyor_maelik_dross",
                "count": 1,
                "description": "Defeat Surveyor Maelik Dross in the old court",
            },
        ],
        rewards=[
            {"action_type": "give_scales", "amount": 135},
            {"action_type": "modify_standing", "faction_id": "circle", "delta": 120},
            {"action_type": "echo", "message": "|gTern studies the returned notes in silence. \"So the court kept him better than the rolls did.\"|n"},
        ],
        objective_type="kill",
        objective_target="surveyor_maelik_dross",
        objective_count=1,
    )
    area.quest(
        "oc_q_ninth_ward",
        name="Ninth Ward",
        description="Shrine Keeper Odan believes the numbered ward at the reservoir was never properly laid to rest when the works were emptied. Break the guardian still holding the count.",
        quest_type="kill",
        quest_giver="npc_shrine_keeper_odan",
        objectives=[
            {
                "type": "kill",
                "target": "ninth_reservoir_warden",
                "count": 1,
                "description": "Defeat the Ninth Reservoir Warden",
            },
        ],
        rewards=[
            {"action_type": "give_scales", "amount": 120},
            {"action_type": "modify_standing", "faction_id": "circle", "delta": 95},
            {"action_type": "echo", "message": "|gOdan bows toward the dark works. \"Some counts should end with witness, not abandonment.\"|n"},
        ],
        objective_type="kill",
        objective_target="ninth_reservoir_warden",
        objective_count=1,
    )

    # ==================================================================
    #  GATHERING POOLS
    # ==================================================================
    area.gathering_pool(
        "ore",
        rooms=["bs_drop_sounding", "ar_broken_pier", "rw_mineral_floor", "sc_chain_hook"],
        materials=["causeway_shard", "survey_bronze", "reservoir_calcite"],
        max_active=3,
        respawn_minutes=15,
        respawn_variance=4,
    )
    area.gathering_pool(
        "herb",
        rooms=["ar_shaft_pool", "br_shrine_hollow", "rw_herb_ledge", "rw_shrine_niche"],
        materials=["archmoss", "shrine_silt"],
        max_active=3,
        respawn_minutes=11,
        respawn_variance=3,
    )
    area.gathering_pool(
        "forage",
        rooms=["bs_marker_hollow", "ws_back_verge", "br_branch_pool", "rw_dry_channel"],
        materials=["cistern_salt"],
        max_active=3,
        respawn_minutes=10,
        respawn_variance=3,
    )
    area.gathering_pool(
        "fish",
        rooms=["ar_shaft_pool", "br_branch_pool", "rw_cistern_lip", "rw_sump_bridge"],
        materials=["cave_eel"],
        max_active=2,
        respawn_minutes=14,
        respawn_variance=4,
    )

    return area.build()
