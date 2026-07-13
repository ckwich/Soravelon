"""Tremen -- Hub 3 city zone

A half-dwarf mountain city of bell roads, worked stone, advanced forges, and careful listening in the Tremeneth Mountains."""

from world.area_builder import AreaBuilder


def build():
    area = AreaBuilder('tremen')

    area.zone(
        name='Tremen',
        zone_type='mountain',
        continent='varath',
        tier=3,
        region='tremeneth_mountains',
        faction_territory='warden',
        faction_presence=['wardens', 'ironblood', 'resonance', 'verdance', 'western_arcana'],
        hub_city='tremen',
        world_x=34,
        world_y=47,
        world_radius=140,
    )

    # Materials
    area.material('greyteeth_iron', tier=2, terrain='stone', absorbed_property='stability', profession_bonus={'smithing': 0.1, 'mining': 0.05})
    area.material('coldvein_stone', tier=2, terrain='stone', absorbed_property='endurance', profession_bonus={'engineering': 0.1, 'mining': 0.05})
    area.material('windroot', tier=2, terrain='alpine', absorbed_property='breath', profession_bonus={'alchemy': 0.1, 'herbalism': 0.05})
    area.material('bellcap_mushroom', tier=2, terrain='cavern', absorbed_property='focus', profession_bonus={'cooking': 0.1, 'foraging': 0.05})
    area.material('haul_rope_fiber', tier=1, terrain='roadside', absorbed_property='flexibility', profession_bonus={'engineering': 0.1, 'foraging': 0.05})
    area.material('ridgecat_pelt', tier=2, terrain='ridge', absorbed_property='warmth', profession_bonus={'smithing': 0.1, 'skinning': 0.05})

    # Rooms
    gt_gate_teeth = area.room('gt_gate_teeth', name='Gate Teeth', desc='Two towers of weathered stone bite into the road, their inner faces crowded with rescue names and craft marks. Arrival Captain Hadrim waits beneath the first bell, listening for its note before he asks who has come in from the mountain.', room_type='path', indoor=False)
    gt_guest_bell_arch = area.room('gt_guest_bell_arch', name='Guest Bell Arch', desc='A low brass bell hangs beneath an arch blackened by generations of gloved hands. One ring announces an arrival and two ask for aid; a polished striker rests where even a freezing traveler can reach it.', room_type='path', indoor=False)
    gt_lantern_registry = area.room('gt_lantern_registry', name='Lantern Registry', desc='Rows of hooded lanterns occupy numbered niches beside a slate of outbound names. Empty hooks identify parties still beyond the gate, while returned lamps carry fresh chalk notes about snow, rockfall, and damaged markers.', room_type='path', indoor=False)
    gt_lower_gate = area.room('gt_lower_gate', name='Lower Gate', desc='The southern gate opens onto the lower-pass road and its first hard climb. Warden Scout Rusk keeps marker cord, chalk tabs, and a current route board here, each item arranged for use rather than ceremony.', room_type='path', indoor=False)
    gt_old_teeth_05 = area.room('gt_old_teeth_05', name='Rescue Tooth', desc='A broken gate merlon has been rebuilt with stones carried home from rescue sites. Each bears a date, a weather mark, and the names of those who returned together rather than the name of any commander.', room_type='path', indoor=False)
    gt_arrival_bell_06 = area.room('gt_arrival_bell_06', name='Snowline Bell', desc='A narrow bell tuned for thin mountain air hangs above the turn where snow first lingers. Its rope ends in a heavy knot, easy to find with numb hands, and yesterday’s ice has been chipped clear from the step below.', room_type='path', indoor=False)
    gt_guest_chalk_07 = area.room('gt_guest_chalk_07', name='Guestboard Turn', desc='The wall widens into a chalkboard of guest names, destinations, and expected returns. New arrivals write beneath older smudges, making every journey part of a public promise to notice who has not come back.', room_type='path', indoor=False)
    gt_warden_eye_08 = area.room('gt_warden_eye_08', name='Watch Slit', desc='A deep slit in the gatework frames the lower road without exposing the watcher to its wind. Small mirrors carry daylight into the recess, and a speaking tube connects the post to the bell arch behind.', room_type='path', indoor=False)
    gt_road_debt_09 = area.room('gt_road_debt_09', name='Marker Tithe', desc='Bundles of cut stakes, chalk, and braided cord fill a public rack beside the road. Travelers who used a waystation leave something for the next crossing, paying the mountain back in preparation rather than coin.', room_type='path', indoor=False)
    gt_old_teeth_10 = area.room('gt_old_teeth_10', name='Weathered Tooth', desc='Wind has rounded this outer stone until only the deepest oath marks remain. Imperial tally cuts survive lower down, crossed through where Tremen later turned an extraction count into a record of repairs.', room_type='path', indoor=False)
    gt_arrival_bell_11 = area.room('gt_arrival_bell_11', name='Returning Bell', desc='This smaller bell faces inward and is rung by crews coming home. Fresh sprigs of windroot hang from its bracket, one for each party that returned before the weather board closed the road.', room_type='path', indoor=False)
    gt_guest_chalk_12 = area.room('gt_guest_chalk_12', name='Namewall', desc='Chalked names cover the sheltered wall in layers of white, ochre, and blue. Some are circled to mark safe return; others remain untouched beside dates old enough to quiet passing conversation.', room_type='path', indoor=False)
    gt_warden_eye_13 = area.room('gt_warden_eye_13', name='Lower Watch', desc='A heated watch niche overlooks the final approach, stocked with blankets and a kettle as carefully as signal horns. The current sentry has pinned a sketch of a damaged cairn beside the shift roster.', room_type='path', indoor=False)
    gt_road_debt_14 = area.room('gt_road_debt_14', name='Road Ledger', desc='A stone ledger records blocked routes, repaired bellposts, and supplies carried to isolated waystations. Blank lines remain beneath every entry, leaving the work visibly unfinished for whoever takes the road next.', room_type='path', indoor=False)
    bm_bellcut_market = area.room('bm_bellcut_market', name='Bellcut Market', desc='Brass stall bells divide the market into provisions, repair work, and loads waiting for the road. Quartermaster Vessa moves between them with a weather slate, asking where each pack is going before she names a price.', room_type='path', indoor=False)
    bm_scale_weighing_arch = area.room('bm_scale_weighing_arch', name='Scale Weighing Arch', desc='A beam scale hangs beneath the arch beside carved tables for steep, wet, and high routes. Bank Clerk Pellen records sealed loads with a hammer tap, preserving weight and obligation in the same stone ledger.', room_type='path', indoor=False)
    bm_rope_bazaar = area.room('bm_rope_bazaar', name='Rope Bazaar', desc='Coils of haul rope hang by thickness, stretch, and last known weather rather than color. Tool Mender Bressa tests every splice by ear while climbers trade reports over the rasp of fiber on stone.', room_type='path', indoor=False)
    bm_warm_bread_04 = area.room('bm_warm_bread_04', name='Bakehouse Queue', desc='A narrow bakehouse window passes out dark loaves wrapped for mountain travel. The queue moves slowly because each first loaf is cut open, checked for a raw center, and shared among those waiting.', room_type='path', indoor=False)
    bm_repair_cord_05 = area.room('bm_repair_cord_05', name='Cordwright Bench', desc='A long bench is scarred by awls, wax pots, and the weighted blocks used to test repaired cord. Failed pieces hang overhead with notes naming the weather that broke them, so no mistake leaves the market without a lesson.', room_type='path', indoor=False)
    bm_bellcut_stall_06 = area.room('bm_bellcut_stall_06', name='Bellcut Stall', desc='Small bells shaped for packs, doors, and waystations fill a stall cut into the stone wall. Every one is sounded before sale, and their different notes carry through the market without becoming noise.', room_type='path', indoor=False)
    bm_weighted_scale_07 = area.room('bm_weighted_scale_07', name='Weather Scale', desc='Sliding brass weights marked with rain, snow, and altitude modify the load scale here. A pack that balances in the city can fail the mountain measure, a fact Vessa demonstrates without entertaining argument.', room_type='path', indoor=False)
    bm_route_gossip_08 = area.room('bm_route_gossip_08', name='Passboard', desc='Fresh route reports crowd a slate organized by bellpost and hour. Travelers add rockfall sketches, snow depth, and patrol sightings, while a clerk strikes through rumors that returned crews have disproved.', room_type='path', indoor=False)
    bm_warm_bread_09 = area.room('bm_warm_bread_09', name='Hearth Loaves', desc='Round loaves cool on stone racks above a communal oven vent. Families stamp their crusts with different marks, then leave every eighth loaf unclaimed for late patrols and stranded guests.', room_type='path', indoor=False)
    bm_repair_cord_10 = area.room('bm_repair_cord_10', name='Splice Table', desc='Two vise posts hold damaged rope while apprentices work new fiber into the old lay. Finished splices are chalked with the name of the mender, making every repair both useful and answerable.', room_type='path', indoor=False)
    bm_bellcut_stall_11 = area.room('bm_bellcut_stall_11', name='Warden Supply Stall', desc='Bandages, trail rations, boot nails, and lamp oil are packed in reach of the roadward aisle. Empty bins carry expected restock times instead of promises, and returned gear waits to be repaired rather than hidden.', room_type='path', indoor=False)
    bm_weighted_scale_12 = area.room('bm_weighted_scale_12', name='Loadstone Scales', desc='Stone counterweights from several passes line a massive balance, each density telling its own mountain story. Porters compare pack weight against body, route, and forecast before accepting work.', room_type='path', indoor=False)
    bm_route_gossip_13 = area.room('bm_route_gossip_13', name='Courier Chalkboard', desc='Courier times and missed arrivals are chalked beside quick maps of the high roads. A red circle marks one delayed run, drawing quiet offers of spare fuel and blankets from nearby stalls.', room_type='path', indoor=False)
    bm_warm_bread_14 = area.room('bm_warm_bread_14', name='Last Oven', desc='The market passage ends beside an oven kept hot after the other stalls close. A shelf of yesterday’s bread waits to become stew, while fresh travel loaves are counted against the dawn departure slate.', room_type='path', indoor=False)
    fh_advanced_forge = area.room('fh_advanced_forge', name='Advanced Forge', desc='Four hearths share a single stone hood blackened by decades of disciplined heat. Forgemaster Orruk Bellhand watches metal color, material labels, and the hands holding the tongs before he offers any judgment on the work.', room_type='building', indoor=True)
    fh_mine_lift = area.room('fh_mine_lift', name='Mine Lift', desc='A caged platform descends toward the deep claims on paired chains thick as a wrist. Old Imperial capacity plates remain bolted beside a newer Tremen ledger of inspections, injuries, and loads refused for safety.', room_type='building', indoor=True)
    fh_bellows_walk = area.room('fh_bellows_walk', name='Bellows Walk', desc='Leather bellows line a raised walk where teams feed air to the hearths in measured turns. Chalk marks on the floor keep hot traffic separated from ore carts and the apprentices carrying quench water.', room_type='building', indoor=True)
    fh_apprentice_rhythm_04 = area.room('fh_apprentice_rhythm_04', name='Hammer Cadence', desc='Practice hammers rise and fall along six small anvils, each apprentice keeping a slower shared cadence. Orruk stops the line whenever one strike wanders, treating a bad rhythm as a warning before it becomes ruined metal.', room_type='building', indoor=True)
    fh_ore_tithe_05 = area.room('fh_ore_tithe_05', name='Provenance Bench', desc='Ore samples rest in divided trays beside the names of mine, finder, and claim. Coldvein stone from different depths carries different grain, and no piece reaches a hearth until its origin is recorded.', room_type='building', indoor=True)
    fh_blue_coals_06 = area.room('fh_blue_coals_06', name='Blue-Coal Hearth', desc='A carefully banked hearth burns blue beneath a narrow crucible stand. The fuel bins are sealed between uses, and a slate lists which alloys tolerate this heat and which fail before their color gives warning.', room_type='building', indoor=True)
    fh_pressure_gauge_07 = area.room('fh_pressure_gauge_07', name='Lift Pressure Board', desc='Needles linked to the mine lift track chain strain, brake heat, and air returning from below. A sudden tremor has left the newest line jagged, with the next descent held in red chalk pending inspection.', room_type='building', indoor=True)
    fh_annealed_rail_08 = area.room('fh_annealed_rail_08', name='Quench Rail', desc='Blades, tools, and structural pins cool along an iron rail between oil and water troughs. Each piece carries a stamped tag for material and intended use, preventing a fine edge from being mistaken for a mine brace.', room_type='building', indoor=True)
    fh_apprentice_rhythm_09 = area.room('fh_apprentice_rhythm_09', name='Practice Anvil', desc='Flawed hooks and uneven knife blanks surround a scarred apprentice anvil. None are discarded: each has been marked at the bad balance point, ready to be studied and broken down for another attempt.', room_type='building', indoor=True)
    fh_ore_tithe_10 = area.room('fh_ore_tithe_10', name='Claim Ledger', desc='Stone shelves hold ore tallies beside reports of water, cracking supports, and exhausted crews. Recent pages give injuries the same dark ink as yield, refusing the old Imperial habit of counting only what came up.', room_type='building', indoor=True)
    fh_blue_coals_11 = area.room('fh_blue_coals_11', name='Tempering Hearth', desc='A low hearth holds steady heat for long tempering work rather than spectacle. Finished tools hang nearby with repair dates and owner marks, their worn handles valued as evidence that the craft survived use.', room_type='building', indoor=True)
    fh_pressure_gauge_12 = area.room('fh_pressure_gauge_12', name='Vent Gauge', desc='Glass tubes measure the draw through Forgeheart’s buried vents, their soot lines read at every shift. One channel runs cooler than the others, and a maintenance crew has already laid out brushes and joint seals.', room_type='building', indoor=True)
    fh_annealed_rail_13 = area.room('fh_annealed_rail_13', name='Repair Rail', desc='Bent buckles, chipped picks, and split cooking knives wait along a rail organized by urgency. Rescue gear takes the first hooks, household work the next, and ornament only the space left after both.', room_type='building', indoor=True)
    fh_apprentice_rhythm_14 = area.room('fh_apprentice_rhythm_14', name='Quiet Hammer', desc='A single small anvil occupies the coolest corner of Forgeheart for precision finishing. Its hammer is wrapped at the grip, and the surrounding hush lets a smith hear a hidden crack before polish conceals it.', room_type='building', indoor=True)
    wh_watch_muster = area.room('wh_watch_muster', name='Watch Muster', desc='Patrol pairs assemble beneath a board of open roads, overdue crews, and rescue stores. Watch Captain Maela checks every name against a route and return hour, sending no one out merely because they look eager.', room_type='building', indoor=True)
    wh_sparring_ring = area.room('wh_sparring_ring', name='Sparring Ring', desc='A stone ring holds padded frames weighted to shove back like an off-balance climber. Chalk boundaries leave room for a rescuer, a casualty, and the rope team that must move both without losing the ledge.', room_type='building', indoor=True)
    wh_weather_board = area.room('wh_weather_board', name='Weather Board', desc='Slates from city bells, lift cables, and high-pass observers meet on one wall. Maela’s current reading closes two ridges, narrows a third to paired travel, and leaves space for the next report to change the decision.', room_type='building', indoor=True)
    wh_snow_tally_04 = area.room('wh_snow_tally_04', name='Snow Tally', desc='Wooden measures stained at finger widths stand beside jars of snow from different exposures. Patrols record depth, crust, and melt rather than writing only that the road is bad.', room_type='building', indoor=True)
    wh_ridge_lesson_05 = area.room('wh_ridge_lesson_05', name='Ridge Classroom', desc='A carved model of the nearby ridges fills a waist-high table. Loose white sand demonstrates drifting snow, and red cord shows how a straight route can become the deadliest choice once wind shifts.', room_type='building', indoor=True)
    wh_patrol_slate_06 = area.room('wh_patrol_slate_06', name='Patrol Slate', desc='Each outbound patrol has a row for route, bell checks, supplies, and names encountered. Trophy counts are absent; the widest column is reserved for changes that the next crew must know.', room_type='building', indoor=True)
    wh_safe_practice_07 = area.room('wh_safe_practice_07', name='Rescue Drill', desc='A padded figure hangs halfway over a mock ledge while trainees anchor, communicate, and haul. The exercise stops at every missed call, because speed learned without shared timing is treated as another hazard.', room_type='building', indoor=True)
    wh_bell_rope_08 = area.room('wh_bell_rope_08', name='Alarm Rope', desc='A red rope descends from the watch bell through a guide worn smooth by drills and emergencies. Knotted patterns on the wall distinguish lost traveler, blocked road, mine trouble, and a call for every available hand.', room_type='building', indoor=True)
    wh_snow_tally_09 = area.room('wh_snow_tally_09', name='Drift Measure', desc='A full-height frame holds layered samples from the season’s largest drifts. Dark grit between storms makes each fall distinct and shows exactly where a buried path can shear under added weight.', room_type='building', indoor=True)
    wh_ridge_lesson_10 = area.room('wh_ridge_lesson_10', name='Wind Stair', desc='Open steps climb through slots that reproduce crosswinds from several passes. Trainees carry water, blankets, and one another upward, learning where a body must lean before weather supplies the consequence.', room_type='building', indoor=True)
    wh_patrol_slate_11 = area.room('wh_patrol_slate_11', name='Missing Names', desc='A narrow slate holds names that remained overdue after a route reopened. Some have dates of return written later in a second hand; others still face an empty space and a lamp kept burning below.', room_type='building', indoor=True)
    wh_safe_practice_12 = area.room('wh_safe_practice_12', name='Load Carry', desc='Weighted packs mimic wet rope, injured bodies, and the gear a rescue acquires on its way home. The route through the room forces teams to trade loads before exhaustion turns private pride into public danger.', room_type='building', indoor=True)
    wh_bell_rope_13 = area.room('wh_bell_rope_13', name='Muster Bell', desc='The muster bell hangs low enough to be heard through every watch room without carrying panic into the city. Its rope is inspected at each change of shift, with the checker’s mark tied visibly into the end.', room_type='building', indoor=True)
    wh_snow_tally_14 = area.room('wh_snow_tally_14', name='Melt Ledger', desc='Water from measured snow samples drains into marked copper cups along the wall. The ledger compares depth with actual melt, correcting old assumptions before they become bad estimates of flood or drinking water.', room_type='building', indoor=True)
    rh_listening_bells = area.room('rh_listening_bells', name='Listening Bells', desc='Bells of stone, brass, and coldvein iron hang without clappers above a quiet floor. Listener Senna waits for each tremor to finish before she records its direction, duration, and the weather beyond the walls.', room_type='building', indoor=True)
    rh_measurement_table = area.room('rh_measurement_table', name='Measurement Table', desc='Weights, tuning forks, water cups, and three arcane lenses occupy a table ruled with fine lines. Scholar Ileth keeps contradictory readings side by side, refusing to make agreement by erasing the difficult result.', room_type='building', indoor=True)
    rh_quiet_gallery = area.room('rh_quiet_gallery', name='Quiet Gallery', desc='Thick felt and offset stone doors shelter a gallery where the city’s forge noise fades to a distant pulse. Benches face several bare wall sections, each watched for dust movement when the mountain begins to hum.', room_type='building', indoor=True)
    rh_arcana_lens_04 = area.room('rh_arcana_lens_04', name='Split-Light Lens', desc='A mounted lens divides lamplight into narrow bands across a slate target. One band bends whenever the north wall vibrates, but a note beneath it states plainly that correlation is not cause.', room_type='building', indoor=True)
    rh_resonance_ledger_05 = area.room('rh_resonance_ledger_05', name='Baseline Ledger', desc='Years of ordinary bell readings fill this ledger before any unusual entry appears. Senna uses those quiet pages as the standard, treating a calm day as evidence rather than empty space between events.', room_type='building', indoor=True)
    rh_listening_bell_06 = area.room('rh_listening_bell_06', name='North Bell', desc='A broad stone bell hangs from leather straps aligned toward the high passes. Frost forms along one edge before certain weather changes, a useful pattern recorded without any claim that the bell creates it.', room_type='building', indoor=True)
    rh_stone_hum_07 = area.room('rh_stone_hum_07', name='Hum Chamber', desc='The floor carries a low vibration too steady to be forge work and too faint to hear while standing. Cushions and handrails let listeners kneel safely, compare the sensation, and leave before certainty outruns endurance.', room_type='building', indoor=True)
    rh_careful_chalk_08 = area.room('rh_careful_chalk_08', name='Uncertainty Board', desc='Observations cover a black wall in white chalk, while guesses appear in yellow and disproven ideas in red. Nothing is scrubbed away until the reason for rejection has been copied into the ledger.', room_type='building', indoor=True)
    rh_arcana_lens_09 = area.room('rh_arcana_lens_09', name='Refraction Stand', desc='Three lenses can be rotated toward the same hair-thin beam crossing the room. Their readings agree today except at the final mark, where Ileth has drawn a question instead of rounding the difference away.', room_type='building', indoor=True)
    rh_resonance_ledger_10 = area.room('rh_resonance_ledger_10', name='Cross-Check Ledger', desc='Bell times are compared here with lift strain, mine reports, snowfall, and city repairs. Marginal notes name the person who supplied each observation, leaving every conclusion traceable to a witness.', room_type='building', indoor=True)
    rh_listening_bell_11 = area.room('rh_listening_bell_11', name='Weather Bell', desc='A thin bronze bell responds readily to pressure changes and distant thunder. A sealed slip from the high lift hangs beside its latest timing, ready to be compared rather than treated as confirmation.', room_type='building', indoor=True)
    rh_stone_hum_12 = area.room('rh_stone_hum_12', name='Foundation Note', desc='A single foundation block resonates at a pitch absent from the stones around it. Tool marks show repeated examinations by careful hands, yet the adjoining slate still reads not understood.', room_type='building', indoor=True)
    rh_careful_chalk_13 = area.room('rh_careful_chalk_13', name='Correction Wall', desc='Revised measurements are written directly beneath their earlier values instead of over them. The wall turns changing judgment into a visible history, including several confident mistakes preserved for apprentices.', room_type='building', indoor=True)
    rh_arcana_lens_14 = area.room('rh_arcana_lens_14', name='Unanswered Lens', desc='The final lens remains covered except during paired observations, its glass expensive and its behavior unreliable. A blank book waits beside it, titled only with the date of the next scheduled reading.', room_type='building', indoor=True)
    sc_stone_commons = area.room('sc_stone_commons', name='Stone Commons', desc='Homes, workshops, and public hearths open onto a broad terrace worn smooth by ordinary traffic. Innkeeper Tolma points out water, boot hooks, and the quiet corner before asking any guest for coin.', room_type='path', indoor=False)
    sc_guest_hearth = area.room('sc_guest_hearth', name='Guest Hearth', desc='A sheltered hearth keeps broth warm beside blankets, bandages, and drying racks for wet gear. Healer Arin Coldhand treats early frostbite without ceremony and leaves windroot steeping where anyone can smell when a fresh pot is ready.', room_type='path', indoor=False)
    sc_family_step = area.room('sc_family_step', name='Family Step', desc='A wide step links several adjoining households whose craft marks overlap on the lintel. Children carry messages between doors while elders sort shared tools into baskets labeled by who needs them next.', room_type='path', indoor=False)
    sc_rain_trough_04 = area.room('sc_rain_trough_04', name='Rain Trough', desc='Roof channels feed a covered stone trough divided into drinking, washing, and forge-water basins. Floating markers show the current reserve, and a fresh repair keeps mountain grit out of the clean side.', room_type='path', indoor=False)
    sc_civic_tale_05 = area.room('sc_civic_tale_05', name='Story Bench', desc='A curved bench faces a wall carved with names added after rescues, inventions, and long service. New chalk beneath one carving disputes an old version of the tale, waiting for evening witnesses to settle the detail.', room_type='path', indoor=False)
    sc_hearth_queue_06 = area.room('sc_hearth_queue_06', name='Broth Queue', desc='Workers and travelers queue with mismatched bowls beside a pot that never quite empties. Those returning from the heights are served first, not as honor, but because cold hands spill hot broth.', room_type='path', indoor=False)
    sc_family_slate_07 = area.room('sc_family_slate_07', name='Family Slate', desc='Births, departures, apprenticeships, and expected returns share one large household slate. Several entries have been corrected in different hands, making the record feel maintained rather than monumental.', room_type='path', indoor=False)
    sc_shared_bench_08 = area.room('sc_shared_bench_08', name='Shared Bench', desc='The longest bench in the commons carries baskets of mending, vegetables, letters, and half-finished toys. Anyone who sits finds work within reach and conversation already moving around it.', room_type='path', indoor=False)
    sc_rain_trough_09 = area.room('sc_rain_trough_09', name='Wash Channel', desc='Warm runoff from the public kitchens passes through a washing channel before reaching the lower drains. Scrub boards stand beside boot brushes, with clean rinse water protected upstream under a fitted lid.', room_type='path', indoor=False)
    sc_civic_tale_10 = area.room('sc_civic_tale_10', name='Rescue Stories', desc='Painted stones map rescues from different winters, each route beginning with a bell and ending with a counted return. One stone has been turned over for revision after a survivor objected to being described as helpless.', room_type='path', indoor=False)
    sc_hearth_queue_11 = area.room('sc_hearth_queue_11', name='Guest Pots', desc='Small covered pots ring a low guest fire, marked with common ingredients and the hands that prepared them. Empty hooks invite another contribution, while Arin’s warning slate lists herbs that should never share a broth.', room_type='path', indoor=False)
    sc_family_slate_12 = area.room('sc_family_slate_12', name='Work Roster', desc='Households post tasks they can offer and needs they cannot meet alone. A collapsed chimney, two night watches, and a newborn’s meal schedule have already gathered overlapping names.', room_type='path', indoor=False)
    sc_shared_bench_13 = area.room('sc_shared_bench_13', name='Mending Bench', desc='Coats, packs, and blankets move across this bench with repair tags pinned to every tear. Finished pieces wait without charge beside a box for spare thread, leather, or time.', room_type='path', indoor=False)
    sc_rain_trough_14 = area.room('sc_rain_trough_14', name='Overflow Garden', desc='Excess trough water feeds a stepped garden of windroot, onions, and hardy greens. Melt has exposed new soil along the lowest bed, and neighbors are already arguing cheerfully over what should be planted there.', room_type='path', indoor=False)
    ug_underhall_gate = area.room('ug_underhall_gate', name='Underhall Gate', desc='Underhall Gate belongs to the Underhall Gates, where descent is framed as witness work, not treasure hunting. The locked descent is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=True)
    ug_oath_lintel = area.room('ug_oath_lintel', name='Oath Lintel', desc='Oath Lintel belongs to the Underhall Gates, where descent is framed as witness work, not treasure hunting. The family mark is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=True)
    ug_cistern_key_post = area.room('ug_cistern_key_post', name='Cistern Key Post', desc='Cistern Key Post belongs to the Underhall Gates, where descent is framed as witness work, not treasure hunting. The old air is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=True)
    ug_stone_witness_04 = area.room('ug_stone_witness_04', name='Stone Witness 04', desc='Stone Witness 04 belongs to the Underhall Gates, where descent is framed as witness work, not treasure hunting. The stone witness is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=True)
    ug_underhall_warning_05 = area.room('ug_underhall_warning_05', name='Underhall Warning 05', desc='Underhall Warning 05 belongs to the Underhall Gates, where descent is framed as witness work, not treasure hunting. The underhall warning is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=True)
    ug_locked_descent_06 = area.room('ug_locked_descent_06', name='Locked Descent 06', desc='Locked Descent 06 belongs to the Underhall Gates, where descent is framed as witness work, not treasure hunting. The locked descent is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=True)
    ug_family_mark_07 = area.room('ug_family_mark_07', name='Family Mark 07', desc='Family Mark 07 belongs to the Underhall Gates, where descent is framed as witness work, not treasure hunting. The family mark is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=True)
    ug_old_air_08 = area.room('ug_old_air_08', name='Old Air 08', desc='Old Air 08 belongs to the Underhall Gates, where descent is framed as witness work, not treasure hunting. The old air is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=True)
    ug_stone_witness_09 = area.room('ug_stone_witness_09', name='Stone Witness 09', desc='Stone Witness 09 belongs to the Underhall Gates, where descent is framed as witness work, not treasure hunting. The stone witness is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=True)
    ug_underhall_warning_10 = area.room('ug_underhall_warning_10', name='Underhall Warning 10', desc='Underhall Warning 10 belongs to the Underhall Gates, where descent is framed as witness work, not treasure hunting. The underhall warning is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=True)
    ug_locked_descent_11 = area.room('ug_locked_descent_11', name='Locked Descent 11', desc='Locked Descent 11 belongs to the Underhall Gates, where descent is framed as witness work, not treasure hunting. The locked descent is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=True)
    ug_family_mark_12 = area.room('ug_family_mark_12', name='Family Mark 12', desc='Family Mark 12 belongs to the Underhall Gates, where descent is framed as witness work, not treasure hunting. The family mark is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=True)
    ug_old_air_13 = area.room('ug_old_air_13', name='Old Air 13', desc='Old Air 13 belongs to the Underhall Gates, where descent is framed as witness work, not treasure hunting. The old air is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=True)
    ug_stone_witness_14 = area.room('ug_stone_witness_14', name='Stone Witness 14', desc='Stone Witness 14 belongs to the Underhall Gates, where descent is framed as witness work, not treasure hunting. The stone witness is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=True)
    hl_high_lift = area.room('hl_high_lift', name='High Lift', desc='High Lift belongs to High Lift Courts, where the city sends people upward only after weather and cable agree. The high cable is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    hl_cable_house = area.room('hl_cable_house', name='Cable House', desc='Cable House belongs to High Lift Courts, where the city sends people upward only after weather and cable agree. The weather pause is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    hl_sky_waiting_bench = area.room('hl_sky_waiting_bench', name='Sky Waiting Bench', desc='Sky Waiting Bench belongs to High Lift Courts, where the city sends people upward only after weather and cable agree. The lift chant is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    hl_thin_air_token_04 = area.room('hl_thin_air_token_04', name='Thin Air Token 04', desc='Thin Air Token 04 belongs to High Lift Courts, where the city sends people upward only after weather and cable agree. The thin-air token is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    hl_ridge_report_05 = area.room('hl_ridge_report_05', name='Ridge Report 05', desc='Ridge Report 05 belongs to High Lift Courts, where the city sends people upward only after weather and cable agree. The ridge report is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    hl_high_cable_06 = area.room('hl_high_cable_06', name='High Cable 06', desc='High Cable 06 belongs to High Lift Courts, where the city sends people upward only after weather and cable agree. The high cable is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    hl_weather_pause_07 = area.room('hl_weather_pause_07', name='Weather Pause 07', desc='Weather Pause 07 belongs to High Lift Courts, where the city sends people upward only after weather and cable agree. The weather pause is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    hl_lift_chant_08 = area.room('hl_lift_chant_08', name='Lift Chant 08', desc='Lift Chant 08 belongs to High Lift Courts, where the city sends people upward only after weather and cable agree. The lift chant is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    hl_thin_air_token_09 = area.room('hl_thin_air_token_09', name='Thin Air Token 09', desc='Thin Air Token 09 belongs to High Lift Courts, where the city sends people upward only after weather and cable agree. The thin-air token is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    hl_ridge_report_10 = area.room('hl_ridge_report_10', name='Ridge Report 10', desc='Ridge Report 10 belongs to High Lift Courts, where the city sends people upward only after weather and cable agree. The ridge report is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    hl_high_cable_11 = area.room('hl_high_cable_11', name='High Cable 11', desc='High Cable 11 belongs to High Lift Courts, where the city sends people upward only after weather and cable agree. The high cable is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    hl_weather_pause_12 = area.room('hl_weather_pause_12', name='Weather Pause 12', desc='Weather Pause 12 belongs to High Lift Courts, where the city sends people upward only after weather and cable agree. The weather pause is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    hl_lift_chant_13 = area.room('hl_lift_chant_13', name='Lift Chant 13', desc='Lift Chant 13 belongs to High Lift Courts, where the city sends people upward only after weather and cable agree. The lift chant is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    hl_thin_air_token_14 = area.room('hl_thin_air_token_14', name='Thin Air Token 14', desc='Thin Air Token 14 belongs to High Lift Courts, where the city sends people upward only after weather and cable agree. The thin-air token is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)

    # Local exits
    area.exit(gt_gate_teeth, gt_guest_bell_arch, 'east')
    area.exit(gt_guest_bell_arch, gt_gate_teeth, 'west')
    area.exit(gt_guest_bell_arch, gt_lantern_registry, 'east')
    area.exit(gt_lantern_registry, gt_guest_bell_arch, 'west')
    area.exit(gt_lantern_registry, gt_lower_gate, 'east')
    area.exit(gt_lower_gate, gt_lantern_registry, 'west')
    area.exit(gt_lower_gate, gt_old_teeth_05, 'east')
    area.exit(gt_old_teeth_05, gt_lower_gate, 'west')
    area.exit(gt_old_teeth_05, gt_arrival_bell_06, 'east')
    area.exit(gt_arrival_bell_06, gt_old_teeth_05, 'west')
    area.exit(gt_arrival_bell_06, gt_guest_chalk_07, 'east')
    area.exit(gt_guest_chalk_07, gt_arrival_bell_06, 'west')
    area.exit(gt_guest_chalk_07, gt_warden_eye_08, 'east')
    area.exit(gt_warden_eye_08, gt_guest_chalk_07, 'west')
    area.exit(gt_warden_eye_08, gt_road_debt_09, 'east')
    area.exit(gt_road_debt_09, gt_warden_eye_08, 'west')
    area.exit(gt_road_debt_09, gt_old_teeth_10, 'east')
    area.exit(gt_old_teeth_10, gt_road_debt_09, 'west')
    area.exit(gt_old_teeth_10, gt_arrival_bell_11, 'east')
    area.exit(gt_arrival_bell_11, gt_old_teeth_10, 'west')
    area.exit(gt_arrival_bell_11, gt_guest_chalk_12, 'east')
    area.exit(gt_guest_chalk_12, gt_arrival_bell_11, 'west')
    area.exit(gt_guest_chalk_12, gt_warden_eye_13, 'east')
    area.exit(gt_warden_eye_13, gt_guest_chalk_12, 'west')
    area.exit(gt_warden_eye_13, gt_road_debt_14, 'east')
    area.exit(gt_road_debt_14, gt_warden_eye_13, 'west')
    area.exit(bm_bellcut_market, bm_scale_weighing_arch, 'east')
    area.exit(bm_scale_weighing_arch, bm_bellcut_market, 'west')
    area.exit(bm_scale_weighing_arch, bm_rope_bazaar, 'east')
    area.exit(bm_rope_bazaar, bm_scale_weighing_arch, 'west')
    area.exit(bm_rope_bazaar, bm_warm_bread_04, 'east')
    area.exit(bm_warm_bread_04, bm_rope_bazaar, 'west')
    area.exit(bm_warm_bread_04, bm_repair_cord_05, 'east')
    area.exit(bm_repair_cord_05, bm_warm_bread_04, 'west')
    area.exit(bm_repair_cord_05, bm_bellcut_stall_06, 'east')
    area.exit(bm_bellcut_stall_06, bm_repair_cord_05, 'west')
    area.exit(bm_bellcut_stall_06, bm_weighted_scale_07, 'east')
    area.exit(bm_weighted_scale_07, bm_bellcut_stall_06, 'west')
    area.exit(bm_weighted_scale_07, bm_route_gossip_08, 'east')
    area.exit(bm_route_gossip_08, bm_weighted_scale_07, 'west')
    area.exit(bm_route_gossip_08, bm_warm_bread_09, 'east')
    area.exit(bm_warm_bread_09, bm_route_gossip_08, 'west')
    area.exit(bm_warm_bread_09, bm_repair_cord_10, 'east')
    area.exit(bm_repair_cord_10, bm_warm_bread_09, 'west')
    area.exit(bm_repair_cord_10, bm_bellcut_stall_11, 'east')
    area.exit(bm_bellcut_stall_11, bm_repair_cord_10, 'west')
    area.exit(bm_bellcut_stall_11, bm_weighted_scale_12, 'east')
    area.exit(bm_weighted_scale_12, bm_bellcut_stall_11, 'west')
    area.exit(bm_weighted_scale_12, bm_route_gossip_13, 'east')
    area.exit(bm_route_gossip_13, bm_weighted_scale_12, 'west')
    area.exit(bm_route_gossip_13, bm_warm_bread_14, 'east')
    area.exit(bm_warm_bread_14, bm_route_gossip_13, 'west')
    area.exit(fh_advanced_forge, fh_mine_lift, 'east')
    area.exit(fh_mine_lift, fh_advanced_forge, 'west')
    area.exit(fh_mine_lift, fh_bellows_walk, 'east')
    area.exit(fh_bellows_walk, fh_mine_lift, 'west')
    area.exit(fh_bellows_walk, fh_apprentice_rhythm_04, 'east')
    area.exit(fh_apprentice_rhythm_04, fh_bellows_walk, 'west')
    area.exit(fh_apprentice_rhythm_04, fh_ore_tithe_05, 'east')
    area.exit(fh_ore_tithe_05, fh_apprentice_rhythm_04, 'west')
    area.exit(fh_ore_tithe_05, fh_blue_coals_06, 'east')
    area.exit(fh_blue_coals_06, fh_ore_tithe_05, 'west')
    area.exit(fh_blue_coals_06, fh_pressure_gauge_07, 'east')
    area.exit(fh_pressure_gauge_07, fh_blue_coals_06, 'west')
    area.exit(fh_pressure_gauge_07, fh_annealed_rail_08, 'east')
    area.exit(fh_annealed_rail_08, fh_pressure_gauge_07, 'west')
    area.exit(fh_annealed_rail_08, fh_apprentice_rhythm_09, 'east')
    area.exit(fh_apprentice_rhythm_09, fh_annealed_rail_08, 'west')
    area.exit(fh_apprentice_rhythm_09, fh_ore_tithe_10, 'east')
    area.exit(fh_ore_tithe_10, fh_apprentice_rhythm_09, 'west')
    area.exit(fh_ore_tithe_10, fh_blue_coals_11, 'east')
    area.exit(fh_blue_coals_11, fh_ore_tithe_10, 'west')
    area.exit(fh_blue_coals_11, fh_pressure_gauge_12, 'east')
    area.exit(fh_pressure_gauge_12, fh_blue_coals_11, 'west')
    area.exit(fh_pressure_gauge_12, fh_annealed_rail_13, 'east')
    area.exit(fh_annealed_rail_13, fh_pressure_gauge_12, 'west')
    area.exit(fh_annealed_rail_13, fh_apprentice_rhythm_14, 'east')
    area.exit(fh_apprentice_rhythm_14, fh_annealed_rail_13, 'west')
    area.exit(wh_watch_muster, wh_sparring_ring, 'east')
    area.exit(wh_sparring_ring, wh_watch_muster, 'west')
    area.exit(wh_sparring_ring, wh_weather_board, 'east')
    area.exit(wh_weather_board, wh_sparring_ring, 'west')
    area.exit(wh_weather_board, wh_snow_tally_04, 'east')
    area.exit(wh_snow_tally_04, wh_weather_board, 'west')
    area.exit(wh_snow_tally_04, wh_ridge_lesson_05, 'east')
    area.exit(wh_ridge_lesson_05, wh_snow_tally_04, 'west')
    area.exit(wh_ridge_lesson_05, wh_patrol_slate_06, 'east')
    area.exit(wh_patrol_slate_06, wh_ridge_lesson_05, 'west')
    area.exit(wh_patrol_slate_06, wh_safe_practice_07, 'east')
    area.exit(wh_safe_practice_07, wh_patrol_slate_06, 'west')
    area.exit(wh_safe_practice_07, wh_bell_rope_08, 'east')
    area.exit(wh_bell_rope_08, wh_safe_practice_07, 'west')
    area.exit(wh_bell_rope_08, wh_snow_tally_09, 'east')
    area.exit(wh_snow_tally_09, wh_bell_rope_08, 'west')
    area.exit(wh_snow_tally_09, wh_ridge_lesson_10, 'east')
    area.exit(wh_ridge_lesson_10, wh_snow_tally_09, 'west')
    area.exit(wh_ridge_lesson_10, wh_patrol_slate_11, 'east')
    area.exit(wh_patrol_slate_11, wh_ridge_lesson_10, 'west')
    area.exit(wh_patrol_slate_11, wh_safe_practice_12, 'east')
    area.exit(wh_safe_practice_12, wh_patrol_slate_11, 'west')
    area.exit(wh_safe_practice_12, wh_bell_rope_13, 'east')
    area.exit(wh_bell_rope_13, wh_safe_practice_12, 'west')
    area.exit(wh_bell_rope_13, wh_snow_tally_14, 'east')
    area.exit(wh_snow_tally_14, wh_bell_rope_13, 'west')
    area.exit(rh_listening_bells, rh_measurement_table, 'east')
    area.exit(rh_measurement_table, rh_listening_bells, 'west')
    area.exit(rh_measurement_table, rh_quiet_gallery, 'east')
    area.exit(rh_quiet_gallery, rh_measurement_table, 'west')
    area.exit(rh_quiet_gallery, rh_arcana_lens_04, 'east')
    area.exit(rh_arcana_lens_04, rh_quiet_gallery, 'west')
    area.exit(rh_arcana_lens_04, rh_resonance_ledger_05, 'east')
    area.exit(rh_resonance_ledger_05, rh_arcana_lens_04, 'west')
    area.exit(rh_resonance_ledger_05, rh_listening_bell_06, 'east')
    area.exit(rh_listening_bell_06, rh_resonance_ledger_05, 'west')
    area.exit(rh_listening_bell_06, rh_stone_hum_07, 'east')
    area.exit(rh_stone_hum_07, rh_listening_bell_06, 'west')
    area.exit(rh_stone_hum_07, rh_careful_chalk_08, 'east')
    area.exit(rh_careful_chalk_08, rh_stone_hum_07, 'west')
    area.exit(rh_careful_chalk_08, rh_arcana_lens_09, 'east')
    area.exit(rh_arcana_lens_09, rh_careful_chalk_08, 'west')
    area.exit(rh_arcana_lens_09, rh_resonance_ledger_10, 'east')
    area.exit(rh_resonance_ledger_10, rh_arcana_lens_09, 'west')
    area.exit(rh_resonance_ledger_10, rh_listening_bell_11, 'east')
    area.exit(rh_listening_bell_11, rh_resonance_ledger_10, 'west')
    area.exit(rh_listening_bell_11, rh_stone_hum_12, 'east')
    area.exit(rh_stone_hum_12, rh_listening_bell_11, 'west')
    area.exit(rh_stone_hum_12, rh_careful_chalk_13, 'east')
    area.exit(rh_careful_chalk_13, rh_stone_hum_12, 'west')
    area.exit(rh_careful_chalk_13, rh_arcana_lens_14, 'east')
    area.exit(rh_arcana_lens_14, rh_careful_chalk_13, 'west')
    area.exit(sc_stone_commons, sc_guest_hearth, 'east')
    area.exit(sc_guest_hearth, sc_stone_commons, 'west')
    area.exit(sc_guest_hearth, sc_family_step, 'east')
    area.exit(sc_family_step, sc_guest_hearth, 'west')
    area.exit(sc_family_step, sc_rain_trough_04, 'east')
    area.exit(sc_rain_trough_04, sc_family_step, 'west')
    area.exit(sc_rain_trough_04, sc_civic_tale_05, 'east')
    area.exit(sc_civic_tale_05, sc_rain_trough_04, 'west')
    area.exit(sc_civic_tale_05, sc_hearth_queue_06, 'east')
    area.exit(sc_hearth_queue_06, sc_civic_tale_05, 'west')
    area.exit(sc_hearth_queue_06, sc_family_slate_07, 'east')
    area.exit(sc_family_slate_07, sc_hearth_queue_06, 'west')
    area.exit(sc_family_slate_07, sc_shared_bench_08, 'east')
    area.exit(sc_shared_bench_08, sc_family_slate_07, 'west')
    area.exit(sc_shared_bench_08, sc_rain_trough_09, 'east')
    area.exit(sc_rain_trough_09, sc_shared_bench_08, 'west')
    area.exit(sc_rain_trough_09, sc_civic_tale_10, 'east')
    area.exit(sc_civic_tale_10, sc_rain_trough_09, 'west')
    area.exit(sc_civic_tale_10, sc_hearth_queue_11, 'east')
    area.exit(sc_hearth_queue_11, sc_civic_tale_10, 'west')
    area.exit(sc_hearth_queue_11, sc_family_slate_12, 'east')
    area.exit(sc_family_slate_12, sc_hearth_queue_11, 'west')
    area.exit(sc_family_slate_12, sc_shared_bench_13, 'east')
    area.exit(sc_shared_bench_13, sc_family_slate_12, 'west')
    area.exit(sc_shared_bench_13, sc_rain_trough_14, 'east')
    area.exit(sc_rain_trough_14, sc_shared_bench_13, 'west')
    area.exit(ug_underhall_gate, ug_oath_lintel, 'east')
    area.exit(ug_oath_lintel, ug_underhall_gate, 'west')
    area.exit(ug_oath_lintel, ug_cistern_key_post, 'east')
    area.exit(ug_cistern_key_post, ug_oath_lintel, 'west')
    area.exit(ug_cistern_key_post, ug_stone_witness_04, 'east')
    area.exit(ug_stone_witness_04, ug_cistern_key_post, 'west')
    area.exit(ug_stone_witness_04, ug_underhall_warning_05, 'east')
    area.exit(ug_underhall_warning_05, ug_stone_witness_04, 'west')
    area.exit(ug_underhall_warning_05, ug_locked_descent_06, 'east')
    area.exit(ug_locked_descent_06, ug_underhall_warning_05, 'west')
    area.exit(ug_locked_descent_06, ug_family_mark_07, 'east')
    area.exit(ug_family_mark_07, ug_locked_descent_06, 'west')
    area.exit(ug_family_mark_07, ug_old_air_08, 'east')
    area.exit(ug_old_air_08, ug_family_mark_07, 'west')
    area.exit(ug_old_air_08, ug_stone_witness_09, 'east')
    area.exit(ug_stone_witness_09, ug_old_air_08, 'west')
    area.exit(ug_stone_witness_09, ug_underhall_warning_10, 'east')
    area.exit(ug_underhall_warning_10, ug_stone_witness_09, 'west')
    area.exit(ug_underhall_warning_10, ug_locked_descent_11, 'east')
    area.exit(ug_locked_descent_11, ug_underhall_warning_10, 'west')
    area.exit(ug_locked_descent_11, ug_family_mark_12, 'east')
    area.exit(ug_family_mark_12, ug_locked_descent_11, 'west')
    area.exit(ug_family_mark_12, ug_old_air_13, 'east')
    area.exit(ug_old_air_13, ug_family_mark_12, 'west')
    area.exit(ug_old_air_13, ug_stone_witness_14, 'east')
    area.exit(ug_stone_witness_14, ug_old_air_13, 'west')
    area.exit(hl_high_lift, hl_cable_house, 'east')
    area.exit(hl_cable_house, hl_high_lift, 'west')
    area.exit(hl_cable_house, hl_sky_waiting_bench, 'east')
    area.exit(hl_sky_waiting_bench, hl_cable_house, 'west')
    area.exit(hl_sky_waiting_bench, hl_thin_air_token_04, 'east')
    area.exit(hl_thin_air_token_04, hl_sky_waiting_bench, 'west')
    area.exit(hl_thin_air_token_04, hl_ridge_report_05, 'east')
    area.exit(hl_ridge_report_05, hl_thin_air_token_04, 'west')
    area.exit(hl_ridge_report_05, hl_high_cable_06, 'east')
    area.exit(hl_high_cable_06, hl_ridge_report_05, 'west')
    area.exit(hl_high_cable_06, hl_weather_pause_07, 'east')
    area.exit(hl_weather_pause_07, hl_high_cable_06, 'west')
    area.exit(hl_weather_pause_07, hl_lift_chant_08, 'east')
    area.exit(hl_lift_chant_08, hl_weather_pause_07, 'west')
    area.exit(hl_lift_chant_08, hl_thin_air_token_09, 'east')
    area.exit(hl_thin_air_token_09, hl_lift_chant_08, 'west')
    area.exit(hl_thin_air_token_09, hl_ridge_report_10, 'east')
    area.exit(hl_ridge_report_10, hl_thin_air_token_09, 'west')
    area.exit(hl_ridge_report_10, hl_high_cable_11, 'east')
    area.exit(hl_high_cable_11, hl_ridge_report_10, 'west')
    area.exit(hl_high_cable_11, hl_weather_pause_12, 'east')
    area.exit(hl_weather_pause_12, hl_high_cable_11, 'west')
    area.exit(hl_weather_pause_12, hl_lift_chant_13, 'east')
    area.exit(hl_lift_chant_13, hl_weather_pause_12, 'west')
    area.exit(hl_lift_chant_13, hl_thin_air_token_14, 'east')
    area.exit(hl_thin_air_token_14, hl_lift_chant_13, 'west')
    area.exit(gt_road_debt_14, bm_bellcut_market, 'north')
    area.exit(bm_bellcut_market, gt_road_debt_14, 'south')
    area.exit(bm_warm_bread_14, fh_advanced_forge, 'north')
    area.exit(fh_advanced_forge, bm_warm_bread_14, 'south')
    area.exit(fh_apprentice_rhythm_14, wh_watch_muster, 'north')
    area.exit(wh_watch_muster, fh_apprentice_rhythm_14, 'south')
    area.exit(wh_snow_tally_14, rh_listening_bells, 'north')
    area.exit(rh_listening_bells, wh_snow_tally_14, 'south')
    area.exit(rh_arcana_lens_14, sc_stone_commons, 'north')
    area.exit(sc_stone_commons, rh_arcana_lens_14, 'south')
    area.exit(sc_rain_trough_14, ug_underhall_gate, 'north')
    area.exit(ug_underhall_gate, sc_rain_trough_14, 'south')
    area.exit(ug_stone_witness_14, hl_high_lift, 'north')
    area.exit(hl_high_lift, ug_stone_witness_14, 'south')
    area.exit(gt_lower_gate, 'greyteeth_lower_passes:ra_rethward_arrival', 'south', one_way=True)
    area.exit(hl_high_lift, 'tremeneth_high_passes:ps_patrol_stair', 'up')
    area.exit(fh_mine_lift, 'tremeneth_deep_mines:cg_claim_gate', 'down')
    area.exit(ug_underhall_gate, 'tremeneth_underhalls:ug_underhall_gate', 'down')

    # NPCs
    _arrival_captain = area.npc(gt_gate_teeth, 'npc_arrival_captain_hadrim', name='Arrival Captain Hadrim', faction='wardens', dialogue={'greeting_tiers': {"neutral": 'Hadrim listens for the guest bell before he asks your name.'}, 'topics': {'guest bell': 'Ring once for arrival, twice for need, and never for impatience.'}, 'base_hints': []})
    _quartermaster = area.npc(bm_bellcut_market, 'npc_quartermaster_vessa', name='Quartermaster Vessa', faction='wardens', dialogue={'greeting_tiers': {"neutral": 'Vessa measures your pack by weight and weather, not by bravado.'}, 'topics': {'trade': 'Road gear is cheap compared with a bad ridge decision.'}, 'base_hints': []})
    area.vendor(_quartermaster, item_ids=['trail_rations', 'hearty_stew', 'travelers_cloak', 'leather_boots', 'bandage'])
    _forgemaster = area.npc(fh_advanced_forge, 'npc_forgemaster_orruk', name='Forgemaster Orruk Bellhand', faction='ironblood', dialogue={'greeting_tiers': {"neutral": 'Orruk watches the color of the metal before he watches the visitor.'}, 'topics': {'forge': 'A fine edge remembers the person who kept the fire honest.'}, 'base_hints': []})
    area.vendor(_forgemaster, item_ids=['iron_dagger', 'iron_staff', 'pickaxe', 'hatchet', 'skinning_knife'])
    _watch_captain = area.npc(wh_watch_muster, 'npc_watch_captain_maela', name='Watch Captain Maela', faction='wardens', dialogue={'greeting_tiers': {"neutral": 'Maela reads weather boards the way other captains read warrants.'}, 'topics': {'patrol': 'A patrol that returns with numbers saves more lives than one that returns with trophies.'}, 'base_hints': []})
    _listener = area.npc(rh_listening_bells, 'npc_listener_senna', name='Listener Senna', faction='resonance', dialogue={'greeting_tiers': {"neutral": 'Senna raises a finger until the bell tremor finishes its thought.'}, 'topics': {'listening': 'We record what the stone does. We do not promise what we cannot do.'}, 'base_hints': []})
    _archivist = area.npc(ug_oath_lintel, 'npc_archivist_belru', name='Archivist Belru Stonekin', faction='resonance', dialogue={'greeting_tiers': {"neutral": 'Belru keeps one palm on the underhall ledger as if it might walk away.'}, 'topics': {'underhalls': 'Family stone deserves witnesses, not looters with cleaner boots.'}, 'base_hints': []})
    _lift_forewoman = area.npc(hl_high_lift, 'npc_lift_forewoman_kelda', name='Lift Forewoman Kelda', faction='ironblood', dialogue={'greeting_tiers': {"neutral": 'Kelda tests every cable with the suspicion of someone who likes living.'}, 'topics': {'lift': 'The high pass does not care who is in a hurry.'}, 'base_hints': []})
    _healer = area.npc(sc_guest_hearth, 'npc_healer_arin', name='Healer Arin Coldhand', faction='verdance', dialogue={'greeting_tiers': {"neutral": 'Arin has warm broth ready and no patience for untreated frostbite.'}, 'topics': {'care': 'A bandage used early is cheaper than pride used late.'}, 'base_hints': []})
    area.vendor(_healer, item_ids=['minor_healing_potion', 'minor_stamina_potion', 'bandage', 'trail_rations'])
    _innkeeper = area.npc(sc_stone_commons, 'npc_innkeeper_tolma', name='Innkeeper Tolma', faction=None, dialogue={'greeting_tiers': {"neutral": 'Tolma points out boot hooks, water, and the quiet corner before asking for coin.'}, 'topics': {'rest': 'Sleep below the bells before you try to answer the heights.'}, 'base_hints': []})
    area.vendor(_innkeeper, item_ids=['trail_rations', 'spiced_fish', 'hearty_stew', 'minor_stamina_potion'])
    _bank_clerk = area.npc(bm_scale_weighing_arch, 'npc_bank_clerk_pellen', name='Bank Clerk Pellen', faction=None, dialogue={'greeting_tiers': {"neutral": 'Pellen seals ledgers with a hammer tap that sounds like a tiny verdict.'}, 'topics': {'coin': 'Stone keeps records better than memory when weather gets involved.'}, 'base_hints': []})
    _arcana_scholar = area.npc(rh_measurement_table, 'npc_arcana_scholar_ileth', name='Scholar Ileth of Western Arcana', faction='western_arcana', dialogue={'greeting_tiers': {"neutral": 'Ileth has three lenses, four notebooks, and the manners to admit when none are enough.'}, 'topics': {'measurements': 'The honest phrase is not yet understood.'}, 'base_hints': []})
    _warden_scout = area.npc(gt_lower_gate, 'npc_warden_scout_rusk', name='Warden Scout Rusk', faction='wardens', dialogue={'greeting_tiers': {"neutral": 'Rusk smells of road chalk and snowmelt, with marker dust under every nail.'}, 'topics': {'marks': 'A good marker sends strangers toward help before danger gets a vote.'}, 'base_hints': []})
    _tool_mender = area.npc(bm_rope_bazaar, 'npc_tool_mender_bressa', name='Tool Mender Bressa', faction='ironblood', dialogue={'greeting_tiers': {"neutral": 'Bressa tests tool hafts by ear and refuses to sell pretty nonsense.'}, 'topics': {'tools': 'If it cannot survive a wet climb, it belongs on a wall, not your belt.'}, 'base_hints': []})
    area.vendor(_tool_mender, item_ids=['fishing_rod', 'bait', 'sickle', 'hatchet', 'skinning_knife', 'pickaxe', 'bandage'])

    # Quest item templates
    area.item('tre_waystation_marker_kit', key='waystation marker kit', item_type='item', weight=0.5, rarity='normal', desc='A packet of chalk tabs, cord, and bell-post nails meant for the first lower-pass waystation.', value=0, is_quest_item=True)
    area.item('tre_weather_slip', key='weather slip', item_type='item', weight=0.5, rarity='normal', desc='A narrow slate slip marked with storm-bell timing and lift-house cautions.', value=0, is_quest_item=True)
    area.item('tre_underhall_measure', key='underhall measure', item_type='item', weight=0.5, rarity='normal', desc='A weighted cord and listening tab sealed by Archivist Belru for careful underhall work.', value=0, is_quest_item=True)
    area.item('tre_mine_reckoning', key='mine reckoning slate', item_type='item', weight=0.5, rarity='normal', desc='A slate of old claim numbers, new injuries, and questions the mine office would rather not answer.', value=0, is_quest_item=True)

    # Quests
    area.quest(
        'tre_q_guest_bell',
        name='Guest Bell, Guest Name',
        description="Arrival Captain Hadrim asks you to learn Tremen's guest-bell custom before you treat the city like a marketplace with walls.",
        quest_type='social',
        quest_giver='npc_arrival_captain_hadrim',
        objectives=[{'type': 'investigate', 'target': 'gt_guest_bell_arch', 'count': 1}, {'type': 'visit', 'target': 'rh_listening_bells', 'count': 1}, {'type': 'talk_to', 'target': 'npc_listener_senna', 'count': 1}],
        rewards=[{'action_type': 'give_scales', 'amount': 28}, {'action_type': 'modify_standing', 'faction_id': 'wardens', 'delta': 1800}],
        next_quest_id='tre_q_waystation_marks',
        prerequisite_quests=[],
        can_share=True,
        consequence_small='Hadrim chalks your guest name beside the bell arch, so later gate questions begin with recognition instead of suspicion.',
    )
    area.quest(
        'tre_q_waystation_marks',
        name='Waystation Marks',
        description='Rusk sends you toward the lower road with a marker kit, turning a delivery into a lesson in how Tremen keeps strangers from dying between bells.',
        quest_type='delivery',
        quest_giver='npc_warden_scout_rusk',
        objectives=[{'type': 'investigate', 'target': 'gt_lower_gate', 'count': 1}, {'type': 'visit', 'target': 'bw_bellpost_waystation', 'count': 1}, {'type': 'deliver', 'target': 'npc_bellpost_keeper_roven', 'count': 1, 'item_tag': 'tre_waystation_marker_kit'}],
        rewards=[{'action_type': 'give_scales', 'amount': 34}, {'action_type': 'give_skill_xp', 'skill_id': 'survival', 'count': 12}],
        next_quest_id='glp_q_marker_line',
        prerequisite_quests=['tre_q_guest_bell'],
        can_share=True,
        consequence_small='Rusk adds your hand to the lower-road chalkboard, noting that you learned the route by improving it rather than merely crossing it.',
    )
    area.quest(
        'tre_q_stone_debt',
        name='Stone Debt',
        description='Forgemaster Orruk wants a useful coldvein sample and the story of where you found it, because Tremen treats material value as history in your hand.',
        quest_type='gather',
        quest_giver='npc_forgemaster_orruk',
        objectives=[{'type': 'investigate', 'target': 'fh_advanced_forge', 'count': 1}, {'type': 'gather', 'target': 'coldvein_stone', 'count': 2}, {'type': 'deliver', 'target': 'npc_forgemaster_orruk', 'count': 1, 'item_tag': 'coldvein_stone'}],
        rewards=[{'action_type': 'give_scales', 'amount': 32}, {'action_type': 'give_skill_xp', 'skill_id': 'smithing', 'count': 12}],
        next_quest_id=None,
        prerequisite_quests=[],
        can_share=True,
        consequence_small='Orruk sets your sample beside the apprentice rail with a note about where it came from, making the lesson local instead of abstract.',
    )
    area.quest(
        'tre_q_bell_weather',
        name='Bell Weather',
        description='Listener Senna asks you to compare city bell readings against the high-lift board, making weather a playable clue rather than background flavor.',
        quest_type='investigation',
        quest_giver='npc_listener_senna',
        objectives=[{'type': 'investigate', 'target': 'rh_listening_bells', 'count': 1}, {'type': 'visit', 'target': 'hl_high_lift', 'count': 1}, {'type': 'deliver', 'target': 'npc_lift_forewoman_kelda', 'count': 1, 'item_tag': 'tre_weather_slip'}],
        rewards=[{'action_type': 'give_scales', 'amount': 30}, {'action_type': 'give_skill_xp', 'skill_id': 'scholarship', 'count': 12}],
        next_quest_id='thp_q_patrol_count',
        prerequisite_quests=[],
        can_share=True,
        consequence_small='Senna keeps your timing slip on the measurement table, a small proof that listening and travel belong in the same story.',
    )
    area.quest(
        'tre_q_underhall_measure',
        name='Measure Before Descent',
        description='Archivist Belru refuses to send you below as a tourist; he makes you carry a measure so the first underhall step becomes care, not trespass.',
        quest_type='investigation',
        quest_giver='npc_archivist_belru',
        objectives=[{'type': 'investigate', 'target': 'ug_underhall_gate', 'count': 1}, {'type': 'talk_to', 'target': 'npc_arcana_scholar_ileth', 'count': 1}, {'type': 'deliver', 'target': 'ug_underhall_gate', 'count': 1, 'item_tag': 'tre_underhall_measure'}],
        rewards=[{'action_type': 'give_scales', 'amount': 30}, {'action_type': 'give_skill_xp', 'skill_id': 'scholarship', 'count': 12}],
        next_quest_id='thu_q_first_measure',
        prerequisite_quests=[],
        can_share=True,
        consequence_small='Belru ties a small witness knot on your measure cord, marking you as someone expected to return with names intact.',
    )
    area.quest(
        'tre_q_mine_reckoning',
        name='Mine Reckoning',
        description='Maela sends you to the claim gate with old numbers and fresh injuries, asking you to see whether the mine is teaching caution or repeating extraction.',
        quest_type='investigation',
        quest_giver='npc_watch_captain_maela',
        objectives=[{'type': 'visit', 'target': 'fh_mine_lift', 'count': 1}, {'type': 'investigate', 'target': 'ro_requisition_office', 'count': 1}, {'type': 'deliver', 'target': 'npc_mine_steward_bran', 'count': 1, 'item_tag': 'tre_mine_reckoning'}],
        rewards=[{'action_type': 'give_scales', 'amount': 36}, {'action_type': 'modify_standing', 'faction_id': 'ironblood', 'delta': 1800}],
        next_quest_id='tdm_q_requisition_echo',
        prerequisite_quests=[],
        can_share=True,
        consequence_small='Maela copies your route into the watch ledger, treating mine safety as a public duty rather than a private accident.',
    )

    # Spawns
    area.spawn(wh_sparring_ring, 'weighted_sparring_frame', count_min=1, count_max=2, respawn_minutes=10, respawn_variance=4)
    area.spawn(wh_weather_board, 'padded_practice_dummy', count_min=1, count_max=2, respawn_minutes=10, respawn_variance=4)
    area.spawn(fh_bellows_walk, 'weighted_sparring_frame', count_min=1, count_max=1, respawn_minutes=10, respawn_variance=4)
    area.spawn(sc_guest_hearth, 'padded_practice_dummy', count_min=1, count_max=1, respawn_minutes=10, respawn_variance=4)

    # Gathering pools
    area.gathering_pool('ore', ['fh_advanced_forge', 'bm_scale_weighing_arch'], ['greyteeth_iron', 'coldvein_stone'], max_active=3, respawn_minutes=12, respawn_variance=4, tier_floor=2, tier_ceiling=2)
    area.gathering_pool('herb', ['sc_guest_hearth', 'rh_quiet_gallery'], ['windroot'], max_active=3, respawn_minutes=12, respawn_variance=4, tier_floor=2, tier_ceiling=2)
    area.gathering_pool('forage', ['bm_rope_bazaar', 'ug_cistern_key_post'], ['haul_rope_fiber', 'bellcap_mushroom'], max_active=3, respawn_minutes=12, respawn_variance=4, tier_floor=1, tier_ceiling=2)
    area.gathering_pool('hide', ['wh_sparring_ring', 'bm_bellcut_market'], ['ridgecat_pelt'], max_active=3, respawn_minutes=12, respawn_variance=4, tier_floor=2, tier_ceiling=2)

    # Lore fragments
    area.lore_fragment(
        'tre_lore_half_dwarf_oath',
        gt_gate_teeth,
        discovery_method='search',
        scholar_path='architecture',
        text='The gate oath lists families by craft and rescue, not by blood purity, which is why Tremen citizenship reads like a record of who kept the road open.',
        insight_gain=1,
    )
    area.lore_fragment(
        'tre_lore_imperial_tally',
        fh_advanced_forge,
        discovery_method='search',
        scholar_path='architecture',
        text='An Imperial tally stone has been turned face down under the forge rail. Its old numbers remain legible if you kneel, but the working surface now belongs to repairs.',
        insight_gain=1,
    )

    # Flight
    area.flight_point(hl_sky_waiting_bench, 'tremen_courier', name='Tremen Courier Lift')
    area.flight_route(
        'tremen_courier',
        'varath_prime_courier',
        125,
        leg_duration=90,
        echoes=[{'delay': 25, 'message': 'Tremen drops into grey terraces beneath the courier line, its bells shrinking to points of brass.'}, {'delay': 60, 'message': 'The Rethward roads below look less like borders than old promises being tested by weather.'}],
    )

    return area.build()
