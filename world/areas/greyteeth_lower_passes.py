"""Greyteeth Lower Passes -- Hub 3 exterior zone

The guarded road up from the Rethward approach into Tremen, shaped by waystation bells, marker craft, and weather scars."""

from world.area_builder import AreaBuilder


def build():
    area = AreaBuilder('greyteeth_lower_passes')

    area.zone(
        name='Greyteeth Lower Passes',
        zone_type='mountain',
        continent='varath',
        tier=3,
        region='tremeneth_mountains',
        faction_territory='warden',
        faction_presence=['wardens', 'ironblood', 'resonance', 'verdance', 'western_arcana'],
        world_x=33,
        world_y=43,
        world_radius=155,
    )

    # Materials
    area.material('greyteeth_iron', tier=2, terrain='stone', absorbed_property='stability', profession_bonus={'smithing': 0.1, 'mining': 0.05})
    area.material('coldvein_stone', tier=2, terrain='stone', absorbed_property='endurance', profession_bonus={'engineering': 0.1, 'mining': 0.05})
    area.material('windroot', tier=2, terrain='alpine', absorbed_property='breath', profession_bonus={'alchemy': 0.1, 'herbalism': 0.05})
    area.material('bellcap_mushroom', tier=2, terrain='cavern', absorbed_property='focus', profession_bonus={'cooking': 0.1, 'foraging': 0.05})
    area.material('haul_rope_fiber', tier=1, terrain='roadside', absorbed_property='flexibility', profession_bonus={'engineering': 0.1, 'foraging': 0.05})
    area.material('snowmelt_trout', tier=2, terrain='water', absorbed_property='clarity', profession_bonus={'cooking': 0.1, 'fishing': 0.05})
    area.material('ridgecat_pelt', tier=2, terrain='ridge', absorbed_property='warmth', profession_bonus={'smithing': 0.1, 'skinning': 0.05})

    # Rooms
    ra_rethward_arrival = area.room('ra_rethward_arrival', name='Rethward Arrival', desc='The southern road reaches its first mountain shelf beside a cairn faced with Tremen chalk. Route Warden Mirren counts every arriving companion twice and the rope coils three times before pointing uphill.', room_type='path', indoor=False)
    ra_pack_count_slab = area.room('ra_pack_count_slab', name='Pack Count Slab', desc='Carved columns divide a broad slab into food, water, warmth, cord, and names. Fresh chalk shows one group reducing its load and another turning back for boots suited to the wet stone ahead.', room_type='path', indoor=False)
    ra_snowmelt_runnel_03 = area.room('ra_snowmelt_runnel_03', name='First Snowmelt', desc='A clear runnel crosses the road from a shaded seam still crusted with old snow. Windroot clings to the bank above darting trout, and a painted cup mark identifies where the water is safely collected.', room_type='path', indoor=False)
    ra_pack_count_04 = area.room('ra_pack_count_04', name='Rope Count', desc='Iron pegs hold measuring loops for checking rope length, wear, and wet stretch. One rejected coil hangs apart with a red thread through its hidden fray, left as a warning rather than quietly sold onward.', room_type='path', indoor=False)
    ra_low_bell_05 = area.room('ra_low_bell_05', name='Valley Bell', desc='A low bronze bell carries down the Rethward road more readily than it carries uphill. Its post bears the times of recent rings, letting Mirren distinguish an overdue party from echoes wandering between stone faces.', room_type='path', indoor=False)
    ra_arrival_cairn_06 = area.room('ra_arrival_cairn_06', name='South Cairn', desc='Flat stones from roads farther south make this cairn a rough map of arriving places. Travelers add no stone until they have reported their route, keeping the marker tied to knowledge instead of vanity.', room_type='path', indoor=False)
    ra_road_chalk_07 = area.room('ra_road_chalk_07', name='Weather Chalk', desc='A sheltered wall holds symbols for rain, ice, wind, blocked trail, and safe shelter. The newest mark warns of meltwater above the next bend, signed by a hand expected back before dusk.', room_type='path', indoor=False)
    ra_snowmelt_runnel_08 = area.room('ra_snowmelt_runnel_08', name='Trout Runnel', desc='Cold water widens into a shallow pool where snowmelt trout hold behind dark stones. A fish-cleaning board sits well downstream from the drinking mark, preserving both supper and the next traveler’s water.', room_type='path', indoor=False)
    ra_pack_count_09 = area.room('ra_pack_count_09', name='Companion Count', desc='Paired footprints have been chiseled across the road beside a simple instruction to name who walks with you. Erased chalk beneath the words shows how often a party has stopped here and counted again.', room_type='path', indoor=False)
    ra_low_bell_10 = area.room('ra_low_bell_10', name='Fog Bell', desc='A squat iron bell stands where valley fog first swallows the road behind. Its wrapped striker gives a dull note at close intervals, guiding separated companions without drawing every echo in the pass.', room_type='path', indoor=False)
    ra_arrival_cairn_11 = area.room('ra_arrival_cairn_11', name='Return Cairn', desc='This cairn is built from stones removed after repairs rather than stones carried up for display. White circles mark crews that returned with everyone named on the slab, while an open ring waits beside today’s date.', room_type='path', indoor=False)
    ra_road_chalk_12 = area.room('ra_road_chalk_12', name='Pass Notes', desc='Short reports cover a dry rock face: scree movement, animal tracks, bell condition, and the hour shade reached the path. Mirren has crossed out one false shortcut and written the cost of that mistake beneath it.', room_type='path', indoor=False)
    ra_snowmelt_runnel_13 = area.room('ra_snowmelt_runnel_13', name='Coldwater Ford', desc='The runnel spreads over a broad section of road where boots can be tested before higher crossings. Stepping stones carry repair dates, and a loose one has been ringed in orange chalk for the next road crew.', room_type='path', indoor=False)
    ra_pack_count_14 = area.room('ra_pack_count_14', name='Last Count', desc='The arrival shelf narrows here into the true lower-pass climb. A final slate asks for people, rope, food, and return time; beyond it, no official mark assumes preparation can be repaired after the fact.', room_type='path', indoor=False)
    lm_first_marker = area.room('lm_first_marker', name='First Marker', desc='A shoulder-high marker begins the maintained road with arrows readable from either direction. Beneath later paint, rescuer initials crowd the stone where the first route builders recorded people rather than destinations.', room_type='path', indoor=False)
    lm_chalked_switchback = area.room('lm_chalked_switchback', name='Chalked Switchback', desc='White chevrons carry the road around a blind switchback where darker marks once pointed straight into scree. Scuffed bootprints and a snapped tab suggest someone has tested the false line again recently.', room_type='path', indoor=False)
    lm_mended_rail_03 = area.room('lm_mended_rail_03', name='Spliced Rail', desc='A wooden handrail changes grain halfway across the exposed turn, joined by an iron sleeve and fresh pins. The repair date faces the path so any loosening can be reported by name and place.', room_type='path', indoor=False)
    lm_loose_scree_04 = area.room('lm_loose_scree_04', name='Listening Scree', desc='Flat shards cover the uphill slope and click together before a larger slide begins. Greyteeth scavenger tracks weave between the quiet patches, making both stone and animal movement worth hearing before stepping on.', room_type='path', indoor=False)
    lm_route_lesson_05 = area.room('lm_route_lesson_05', name='Public Symbols', desc='A practice slab pairs each road symbol with a plain carved meaning: shelter, water, unstable stone, closed route, and bell. Private family shorthand has been struck through wherever a frightened stranger could mistake it.', room_type='path', indoor=False)
    lm_first_marker_06 = area.room('lm_first_marker_06', name='Rescue Initials', desc='The oldest marker on this stretch bears no directional arrow at all. Initials and dates fill its sheltered face, preserving the chain of people who came back for someone they did not know.', room_type='path', indoor=False)
    lm_chalk_notch_07 = area.room('lm_chalk_notch_07', name='Ice Notch', desc='A triangular notch holds chalk above the line reached by winter ice. Blue marks date the last freeze and orange marks show where meltwater now undermines the outer edge.', room_type='path', indoor=False)
    lm_mended_rail_08 = area.room('lm_mended_rail_08', name='Chain-Pin Rail', desc='Old survey chain pins anchor a newer rope rail along the cliff side. The iron is sound but Imperial claim numbers remain visible, an inherited tool repurposed without pretending its first use was generous.', room_type='path', indoor=False)
    lm_loose_scree_09 = area.room('lm_loose_scree_09', name='Slide Fan', desc='Fresh scree spreads across the road in a fan from a narrow chute overhead. A temporary marker line climbs inside the fall shadow, and small stones still arrive often enough to keep the detour provisional.', room_type='path', indoor=False)
    lm_route_lesson_10 = area.room('lm_route_lesson_10', name='False Shortcut', desc='Two paths appear to reunite beyond a stone shoulder, but only the marked one keeps stable footing. A recovered false tab has been nailed backward to the wall, exposing the private symbol used by route saboteurs.', room_type='path', indoor=False)
    lm_first_marker_11 = area.room('lm_first_marker_11', name="Stranger's Marker", desc='Words in several hands explain this marker without assuming local knowledge. An added sketch shows the next bellpost as it appears in fog, including the broken cap that distinguishes it from bare rock.', room_type='path', indoor=False)
    lm_chalk_notch_12 = area.room('lm_chalk_notch_12', name='Storm Correction', desc='An old arrow disappears beneath a broad grey strike where last season’s storm removed the path it named. The replacement route is dated, signed, and drawn with a dotted line until another crew verifies it.', room_type='path', indoor=False)
    lm_mended_rail_13 = area.room('lm_mended_rail_13', name='Shared Handrail', desc='Sections of wood, rope, and iron form a handrail repaired by whatever each returning crew could spare. Tags identify weak joins honestly, allowing the next hand to choose support without trusting appearance alone.', room_type='path', indoor=False)
    lm_loose_scree_14 = area.room('lm_loose_scree_14', name='Moving Slope', desc='The road crosses the toe of a slope that changes after every hard rain. Numbered stakes expose how far the stone has crept since yesterday, and the newest measurement leaves little room for complacency.', room_type='path', indoor=False)
    bw_bellpost_waystation = area.room('bw_bellpost_waystation', name='Bellpost Waystation', desc='A stone shelter and tall bellpost occupy the widest shelf on the lower road. Bellpost Keeper Roven keeps the fire breathing, the public marks legible, and a place on the bench for whoever weather sends through next.', room_type='path', indoor=False)
    bw_soup_hook = area.room('bw_soup_hook', name='Soup Hook', desc='An iron hook swings a lidded pot over the waystation fire. Snowmelt trout, roots, and whatever passing hands could spare simmer together, with a chalk line tracking how many bowls remain before resupply.', room_type='path', indoor=False)
    bw_boot_nail_03 = area.room('bw_boot_nail_03', name='Boot-Nail Tin', desc='Sorted boot nails fill a covered tin beside a small hammer and last. Bent nails lie in a second tray for reforging, ensuring a quick repair does not turn metal waste into the next traveler’s problem.', room_type='path', indoor=False)
    bw_traveler_name_04 = area.room('bw_traveler_name_04', name='Arrival Slate', desc='Names, directions, and arrival hours cover a slate mounted inside the shelter. Roven circles each name when its owner departs and adds the next expected bellpost, making silence easier to interpret.', room_type='path', indoor=False)
    bw_night_rope_05 = area.room('bw_night_rope_05', name='Night Guide', desc='A pale rope runs from the shelter door to the bellpost and water barrel. Knots mark each safe turn, allowing cold or smoke-blinded hands to find necessities without leaving the maintained line.', room_type='path', indoor=False)
    bw_bellpost_06 = area.room('bw_bellpost_06', name='Lower Bellpost', desc='The bellpost carries a bronze bell, a weather hood, and clear carved instructions for need, arrival, and road closure. Fresh grease darkens the pivot, while the striker cord bears Roven’s inspection knot.', room_type='path', indoor=False)
    bw_shelter_stew_07 = area.room('bw_shelter_stew_07', name='Storm Pot', desc='A larger pot waits empty beneath a slate marked for storm use only. Dried fish, barley, and salt are stored in sealed shares nearby, each dated so generosity does not become spoiled food.', room_type='path', indoor=False)
    bw_boot_nail_08 = area.room('bw_boot_nail_08', name='Cobbler Stone', desc='A flat work stone holds awls, waxed thread, leather patches, and a groove for bracing a boot. Repairs scratched into its edge range from loose soles to a split pack strap mended during last winter’s closure.', room_type='path', indoor=False)
    bw_traveler_name_09 = area.room('bw_traveler_name_09', name='Return Names', desc='A second slate records those who reached the waystation from higher roads. Several names repeat across seasons in different hands, turning routine travel into a history of who keeps coming back.', room_type='path', indoor=False)
    bw_night_rope_10 = area.room('bw_night_rope_10', name='Fog Line', desc='The guide rope continues beyond the bellpost between waist-high stakes painted with luminous mineral wash. One stake has shifted downhill and been tied off visibly until a road crew can reset it.', room_type='path', indoor=False)
    bw_bellpost_11 = area.room('bw_bellpost_11', name='Spare Clapper', desc='A spare bell clapper hangs under oilcloth beside templates for its leather and iron fittings. The old one rests below with a hairline crack dated and signed, evidence for the repair rather than a discarded mystery.', room_type='path', indoor=False)
    bw_shelter_stew_12 = area.room('bw_shelter_stew_12', name='Shared Stores', desc='Shelves hold dry kindling, broth packets, lamp oil, blankets, and a small reserve of haul rope. Every item has a minimum line and replacement note, making the shelter’s generosity measurable and renewable.', room_type='path', indoor=False)
    bw_boot_nail_13 = area.room('bw_boot_nail_13', name='Sole Bench', desc='A narrow bench near the fire lets wet boots dry while their soles are checked. A row of borrowed pairs in many sizes keeps an emergency repair from forcing bare feet onto the pass.', room_type='path', indoor=False)
    bw_traveler_name_14 = area.room('bw_traveler_name_14', name='Unclosed Names', desc='Names still awaiting a later bell occupy a protected corner of the ledger wall. Some carry notes from search parties or family, while blank space beside today’s entries waits without assuming the outcome.', room_type='path', indoor=False)
    as_avalanche_shelter = area.room('as_avalanche_shelter', name='Avalanche Shelter', desc='A low stone refuge faces away from the loaded slopes, its entrance framed by probe poles and red rescue rope. Shelter Medic Essa has hung an abandoned pack from an inspection peg, keeping its owner’s absence visible while she checks each arrival for cold injury.', room_type='path', indoor=False)
    as_red_rope_cache = area.room('as_red_rope_cache', name='Red Rope Cache', desc='Sealed wall boxes hold coils of red rope, spare webbing, bellcap poultices, and fibers for field repairs. Each seal bears a date and length count, so taking rescue gear creates a duty to report what remains.', room_type='path', indoor=False)
    as_snow_shelf_03 = area.room('as_snow_shelf_03', name='Clawprint Shelf', desc='Wind-packed snow spans a shallow shelf beneath overhanging stone. Probe flags mark a narrow tested line, while ridgecat tracks cross it toward a scrap of torn pack cloth snagged above the drop.', room_type='path', indoor=False)
    as_rescue_tally_04 = area.room('as_rescue_tally_04', name='Rescue Tally', desc='A weatherproof board records who was sought, who returned, hours spent, rope used, and injuries among the searchers. Blank columns are left open until every borrowed tool and every person is accounted for.', room_type='path', indoor=False)
    as_quiet_shovel_05 = area.room('as_quiet_shovel_05', name='Listening Shovels', desc='Short rescue shovels rest on felt-lined pegs beside a painted reminder to stop and listen between digging turns. Scratches on the blades are numbered to the maintenance ledger instead of being polished into false readiness.', room_type='path', indoor=False)
    as_avalanche_shutter_06 = area.room('as_avalanche_shutter_06', name='Tested Shutter', desc='A timber-and-iron shutter can seal the refuge’s exposed opening when snow begins to move. Fresh chalk around its hinges marks the last full closure test, and a warped lower brace has been tagged for replacement.', room_type='path', indoor=False)
    as_red_rope_07 = area.room('as_red_rope_07', name='Anchor Practice', desc='Red rope runs between waist-high iron anchors set into stable rock. Knot diagrams have been carved where sleet cannot erase them, and frayed practice ends let cold hands learn without risking a rescue coil.', room_type='path', indoor=False)
    as_snow_shelf_08 = area.room('as_snow_shelf_08', name='Snow Profile', desc='A square cut in the snow exposes alternating crust, powder, and wind slab. Dated wooden tabs show how the layers changed after each storm, giving travelers a reason to compare today’s slope with yesterday’s warning.', room_type='path', indoor=False)
    as_rescue_tally_09 = area.room('as_rescue_tally_09', name='Search Board', desc='Movable name tiles map active search groups, their assigned lines, and the hour they must report back. One faded tile has been retired beneath a note explaining the route knowledge that person left behind.', room_type='path', indoor=False)
    as_quiet_shovel_10 = area.room('as_quiet_shovel_10', name='Dig Order', desc='Shovels, probes, hauling cloths, and warming wraps are staged in the order a rescue team needs them. Mud from a recent return still marks the floor, but every tool has reached its counted place.', room_type='path', indoor=False)
    as_avalanche_shutter_11 = area.room('as_avalanche_shutter_11', name='Relief Door', desc='A second shutter protects a narrow air pocket on the lee side of the route. Its inward face carries height marks from old snow loads, including one season when the pass remained closed well into thaw.', room_type='path', indoor=False)
    as_red_rope_12 = area.room('as_red_rope_12', name='Retired Rope', desc='Cut lengths of rope hang with tags naming the strain, abrasion, or chemical stain that ended their service. Sound pieces have become pack ties and splints, while damaged fibers remain examples rather than hidden waste.', room_type='path', indoor=False)
    as_snow_shelf_13 = area.room('as_snow_shelf_13', name='Safe Interval', desc='Two red poles define a waiting place before the path crosses another exposed shelf. Notches count how many travelers may enter the traverse together, and fresh ridgecat prints explain why the rear guard keeps looking uphill.', room_type='path', indoor=False)
    as_rescue_tally_14 = area.room('as_rescue_tally_14', name='Relief Handoff', desc='The final shelter board passes responsibility toward the goat ledges with route notes, missing-person descriptions, and supply requests. Essa’s newest entry asks higher patrols to watch for the owner of the recovered pack rather than closing the story at the shelter.', room_type='path', indoor=False)
    gl_goat_ledge = area.room('gl_goat_ledge', name='Goat Ledge', desc='A hoof-wide route crosses a ledge scattered with clipped hair, droppings, and freshly dislodged stone. Deep pawprints overlap the goat tracks near the uphill wall, putting travelers inside a ridgecat’s hunting ground rather than on an empty road.', room_type='path', indoor=False)
    gl_ridgecat_shadow = area.room('gl_ridgecat_shadow', name='Ridgecat Shadow', desc='A shallow overhang darkens the path where a ridgecat has scraped the rock and left pale winter fur. Old skinning cuts on a nearby board show that useful pelts come from dangerous ground, not anonymous stock.', room_type='path', indoor=False)
    gl_wind_tooth_03 = area.room('gl_wind_tooth_03', name='Eagle Tooth', desc='A narrow stone tooth splits the crosswind into sudden rising currents. Windcut eagles circle close enough for their shadows to race over the path, watching the same exposed prey trail as everything below.', room_type='path', indoor=False)
    gl_lichen_shelf_04 = area.room('gl_lichen_shelf_04', name='Windroot Shelf', desc='Orange lichen and wiry windroot occupy cracks beyond the reach of grazing goats. Harvest marks stop short of the smallest crowns, evidence that gatherers leave enough rooted growth for the shelf to recover.', room_type='path', indoor=False)
    gl_bone_charm_05 = area.room('gl_bone_charm_05', name='Herd Warning', desc='Goat bones threaded on red cord turn in the wind beside three deliberate claw marks. A route note dates when the warning moved east, tracking a predator’s territory without pretending the boundary will hold.', room_type='path', indoor=False)
    gl_goat_trail_06 = area.room('gl_goat_trail_06', name='Passing Shelf', desc='The trail widens just enough for one party to brace while another passes. White handprints mark the stable wall, and loose stones have been swept to the outer edge where a careless heel cannot launch them downhill.', room_type='path', indoor=False)
    gl_ridgecat_mark_07 = area.room('gl_ridgecat_mark_07', name='Fresh Scrape', desc='Four parallel scratches expose bright stone beneath the weathered surface. Tufts of fur caught lower down and the absence of goat tracks make the mark current evidence, not an old story repeated for effect.', room_type='path', indoor=False)
    gl_wind_tooth_08 = area.room('gl_wind_tooth_08', name='Broken Updraft', desc='A fractured pinnacle makes the wind lift, drop, and twist without warning. Feathers collect in the lee beside a snapped pack buckle, showing where an eagle’s advantage and a traveler’s bad footing meet.', room_type='path', indoor=False)
    gl_lichen_shelf_09 = area.room('gl_lichen_shelf_09', name='Browsed Shelf', desc='Goats have cropped one side of this shelf to bare stone while the protected cracks remain thick with lichen. Small cairns keep boots off the recovering patches and reveal how slowly life returns at this height.', room_type='path', indoor=False)
    gl_bone_charm_10 = area.room('gl_bone_charm_10', name='Changed Range', desc='A bone marker has been retied beneath a slate naming two recent ridgecat sightings and one missing pack animal. The older position remains as a faded cord scar, preserving how the danger shifted instead of declaring it solved.', room_type='path', indoor=False)
    gl_goat_trail_11 = area.room('gl_goat_trail_11', name='Split Hoofpath', desc='The animal trail divides around a block of frost-cracked stone. One branch bears fresh hoofprints and the other ends in a small slide, while a rescuer’s arrow directs burdened travelers along the tested line.', room_type='path', indoor=False)
    gl_ridgecat_mark_12 = area.room('gl_ridgecat_mark_12', name='Scenting Stone', desc='A high boulder carries claw scoring, dark guard hairs, and the sharp scent of a territorial cat. Someone has tied a visibility streamer well below the mark so the warning can be seen without approaching it.', room_type='path', indoor=False)
    gl_wind_tooth_13 = area.room('gl_wind_tooth_13', name='Feather Current', desc='Crosswinds comb shed eagle feathers into a crack behind the pinnacle. A weighted ribbon on an iron pin shows the current’s direction, and its hard snapping warns when balance will matter more than speed.', room_type='path', indoor=False)
    gl_lichen_shelf_14 = area.room('gl_lichen_shelf_14', name='Patrol Rest', desc='A lichen-faced recess overlooks both the goat trail and the route toward the survey pull-offs. Patrol notes distinguish animals driven off, animals merely sighted, and travelers escorted through, leaving the next watch a truthful starting point.', room_type='path', indoor=False)
    sp_survey_pull_off = area.room('sp_survey_pull_off', name='Survey Pull-Off', desc='A broad shelf lets traffic clear the measuring lines stretched across the pass. Surveyor Pel pins current weather, road movement, and missing markers over an older map whose precise lines privilege ore seams over shelters.', room_type='path', indoor=False)
    sp_old_chain_pin = area.room('sp_old_chain_pin', name='Old Chain Pin', desc='A square iron pin driven deep into the rock once anchored a survey chain. Imperial distance marks march from it toward exposed greyteeth iron, while Pel’s newer chalk records the pin’s slow movement after frost.', room_type='path', indoor=False)
    sp_viewing_slit_03 = area.room('sp_viewing_slit_03', name='Ore-Line Slit', desc='A narrow cut in a stone screen frames three mineral scars across the valley and excludes most of the traveled road. Later hands have added sight lines to bellposts and shelters without erasing what the first survey valued.', room_type='path', indoor=False)
    sp_hammer_tap_04 = area.room('sp_hammer_tap_04', name='Sounding Face', desc='Small hammer dimples form dated rows across a dark rock face. Fresh marks stop around a widening fracture, while the oldest rows continue straight through as if measurement once mattered more than the shelf beneath it.', room_type='path', indoor=False)
    sp_map_scratch_05 = area.room('sp_map_scratch_05', name='Competing Maps', desc='Two maps share a flat slab: deep incisions count veins and haul distance, while removable chalk names water, shelter, unstable stone, and recent animal sign. Neither can hide what the other was built to notice.', room_type='path', indoor=False)
    sp_survey_notch_06 = area.room('sp_survey_notch_06', name='Frost Baseline', desc='Paired notches on opposite walls hold a measuring cord above the path. Pel has dated the newest offset in red, turning a tiny shift into public evidence that the roadbed is still moving.', room_type='path', indoor=False)
    sp_old_chain_07 = area.room('sp_old_chain_07', name='Chain Measure', desc='Several heavy survey links remain fused by rust beside their original length table. The table is exact to a finger’s width but has no column for weather delays, injured haulers, or the cost of keeping the line straight.', room_type='path', indoor=False)
    sp_viewing_slit_08 = area.room('sp_viewing_slit_08', name='Shelter Bearing', desc='This viewing slit once pointed only toward a cut in the opposite ridge. A second groove now aligns it with the nearest avalanche shelter, and a brass plate gives walking time in clear, fog, and ice.', room_type='path', indoor=False)
    sp_hammer_tap_09 = area.room('sp_hammer_tap_09', name='Loose-Stone Test', desc='A rack holds light sounding hammers beside a sequence of painted tap points. One point is crossed out above a basket of fresh fragments, showing where yesterday’s solid answer no longer applies.', room_type='path', indoor=False)
    sp_map_scratch_10 = area.room('sp_map_scratch_10', name='Haul Scar', desc='Parallel scratches descend from a worked seam toward the road, deep enough to outlast the sleds that made them. Current survey notes measure runoff through the grooves because old extraction still redirects today’s meltwater.', room_type='path', indoor=False)
    sp_survey_notch_11 = area.room('sp_survey_notch_11', name='Public Datum', desc='A new brass datum sits beside an older Imperial notch rather than covering it. Its ledger is open to road crews, gatherers, and patrols, allowing many hands to challenge a measurement before it becomes policy.', room_type='path', indoor=False)
    sp_old_chain_12 = area.room('sp_old_chain_12', name='Reused Links', desc='Retired survey links have become a handhold along the exposed edge. Each repaired join bears a maker’s stamp, converting an old instrument of possession into infrastructure that answers to its users.', room_type='path', indoor=False)
    sp_viewing_slit_13 = area.room('sp_viewing_slit_13', name='Weather Sight', desc='A widened slit frames cloud movement over the Windcut Traverse. Strings of dated tabs compare visibility with actual travel reports, so a clear-looking horizon cannot overrule conditions recorded farther ahead.', room_type='path', indoor=False)
    sp_hammer_tap_14 = area.room('sp_hammer_tap_14', name='Road Handoff', desc='A final sounding station marks the transition from measured shelf to wind-scoured traverse. Pel’s slate lists the last verified sign, the next expected report, and which old markers should never be trusted without fresh evidence.', room_type='path', indoor=False)
    wt_windcut_turn = area.room('wt_windcut_turn', name='Windcut Turn', desc='The road vanishes around a wind-carved shoulder beneath brackets for official route tabs. One tab points toward a mineral seam and fresh boot cover rather than the maintained turn, while iron fragments in the scree reward anyone willing to inspect the dangerous ground.', room_type='path', indoor=False)
    wt_broken_banner = area.room('wt_broken_banner', name='Broken Banner', desc='Half a Warden weather banner snaps from a pole scored by knife cuts instead of storm wear. Its missing lower color makes the road-status signal easy to misread, and a dated correction has already been wired below it.', room_type='path', indoor=False)
    wt_eagle_shadow_03 = area.room('wt_eagle_shadow_03', name='Hunting Shadow', desc='A windcut eagle rides the blind side of the ridge, its shadow appearing on the path before the bird clears the turn. Bones and torn food wrappings below its perch show that animal hunger and careless packs draw the same attention.', room_type='path', indoor=False)
    wt_sleet_bite_04 = area.room('wt_sleet_bite_04', name='Rime Face', desc='Sleet freezes against the windward wall in overlapping clear scales. Scraped footholds remain rough beneath the glaze, but a fresh warning stripe ends where runoff has iced over the next handhold.', room_type='path', indoor=False)
    wt_thin_rope_05 = area.room('wt_thin_rope_05', name='Questioned Line', desc='A thin guide rope follows the wall between two official red anchors. Its middle section has been replaced with a mismatched cord and flagged at both joins, warning travelers to use it for direction rather than trust it with weight.', room_type='path', indoor=False)
    wt_windcut_turn_06 = area.room('wt_windcut_turn_06', name='Blind Switch', desc='Crosswind drives dust and sleet around a switchback whose far landing cannot be seen from below. Paired whistle marks ask ascending and descending parties to announce themselves before both commit to the narrow corner.', room_type='path', indoor=False)
    wt_false_tab_07 = area.room('wt_false_tab_07', name='Counterfeit Tab', desc='A route tab bears the right shape but the wrong punch pattern and a layer of paint too fresh for its claimed date. Scrapes on the bracket show it has been reversed more than once, steering uncertain travelers toward a concealed shelf.', room_type='path', indoor=False)
    wt_eagle_shadow_08 = area.room('wt_eagle_shadow_08', name='Carrion Draft', desc='A rising draft carries feathers and the smell of a scavenged carcass from below the road. Eagles circle wider whenever voices approach, revealing a feeding site without making the birds responsible for the broken straps scattered there.', room_type='path', indoor=False)
    wt_sleet_bite_09 = area.room('wt_sleet_bite_09', name='Freezing Runoff', desc='Meltwater crosses the path and freezes again in the turn’s permanent shadow. Grit baskets stand on both sides with fill lines and dated contributions, making safe passage depend on repeated small acts rather than a single repair.', room_type='path', indoor=False)
    wt_thin_rope_10 = area.room('wt_thin_rope_10', name='Cut Guide', desc='The guide rope ends in a clean slice just before a misleading side trail. Someone has knotted the severed ends around separate anchors so the break remains obvious until a verified replacement can be carried up.', room_type='path', indoor=False)
    wt_windcut_turn_11 = area.room('wt_windcut_turn_11', name='Echo Turn', desc='Two rock faces return footsteps and voices from the wrong direction. Warden arrows are carved into the stable wall rather than hung from brackets, and fresh chalk adds the hour each direction was last walked.', room_type='path', indoor=False)
    wt_false_tab_12 = area.room('wt_false_tab_12', name='Bait Marker', desc='A convincing shelter tab points toward a recess littered with boot scuffs, spent cord, and four places where watchers could wait above. The genuine marker lies face-down nearby with its mounting bolts deliberately saved.', room_type='path', indoor=False)
    wt_eagle_shadow_13 = area.room('wt_eagle_shadow_13', name='Low-Wing Warning', desc='Eagles fly unusually low where the traverse narrows, using the wall’s sudden lift. A feather bundle tied beneath the handline shows the same turbulence, turning the animals’ movement into warning without promising safety.', room_type='path', indoor=False)
    wt_sleet_bite_14 = area.room('wt_sleet_bite_14', name='Gateward Rime', desc='The last exposed bend carries rime on every surface facing away from Tremen’s gate. A sheltered board lists false tabs recovered, travelers redirected, and the latest clear route ahead, ready for the next patrol to amend.', room_type='path', indoor=False)
    tg_tremen_gate = area.room('tg_tremen_gate', name='Tremen Gate', desc='The lower gate stands inside a deep-cut stone recess where the pass finally yields to Tremen. Arrival boards reconcile names from Rethward, Bellpost, and the upper patrols, making the city threshold the last link in the road’s chain of accountability.', room_type='path', indoor=False)
    tg_final_bell = area.room('tg_final_bell', name='Gate Bell', desc='A broad bronze bell carries both down the pass and into the gate works. Its posted signals distinguish arrival, missing companion, closed road, and requested aid, preserving the vocabulary learned at the lower bellposts.', room_type='path', indoor=False)
    tg_warm_stone_03 = area.room('tg_warm_stone_03', name='Warming Wall', desc='Dark masonry beside the approach holds a gentle warmth from the occupied city beyond. Hooks for wet gloves and narrow leaning rails let cold travelers recover without blocking the road or mistaking arrival for the end of care.', room_type='path', indoor=False)
    tg_last_marker_04 = area.room('tg_last_marker_04', name='Last Road Marker', desc='The final pass marker lists the distance back to every maintained shelter and the hour of its latest report. Corrections accumulate in chalk around the permanent carving, keeping old certainty subordinate to current conditions.', room_type='path', indoor=False)
    tg_road_gratitude_05 = area.room('tg_road_gratitude_05', name='Roadkeepers’ Wall', desc='Names of bell keepers, shovel crews, guides, cooks, surveyors, and search parties fill a sheltered wall. Each entry names the work and season rather than reducing the road’s survival to a single celebrated hero.', room_type='path', indoor=False)
    tg_final_bell_06 = area.room('tg_final_bell_06', name='Return Bell', desc='A smaller bell answers signals from the exposed turns below. A slate records which distant bell replied and which remained silent, turning the relief of arrival into information someone else can act upon.', room_type='path', indoor=False)
    tg_gate_sightline_07 = area.room('tg_gate_sightline_07', name='Watch Aperture', desc='A protected aperture overlooks the final bends without exposing the watcher to their full wind. Colored shutters repeat the pass signals, and scraped paint shows how often weather forces the system back to hand signs.', room_type='path', indoor=False)
    tg_warm_stone_08 = area.room('tg_warm_stone_08', name='Thaw Bench', desc='A stone bench warmed through the wall faces racks for damp rope and outer layers. Water channels carry the melt away from the walking surface, evidence that welcome here includes the unglamorous work after rescue.', room_type='path', indoor=False)
    tg_last_marker_09 = area.room('tg_last_marker_09', name='Patrol Closure', desc='This marker collects the final signatures for patrols returning from the pass. Open lines remain visible beside an expected time and route, so a party inside the gate can still be overdue to those keeping count.', room_type='path', indoor=False)
    tg_road_gratitude_10 = area.room('tg_road_gratitude_10', name='Supply Ledger', desc='A public ledger credits households and workshops for rope, broth, nails, blankets, and lamp oil sent downhill. Need columns sit beside the thanks, inviting the next contribution before scarcity becomes an emergency.', room_type='path', indoor=False)
    tg_final_bell_11 = area.room('tg_final_bell_11', name='Shift Bell', desc='A compact iron bell marks the handoff between gate watches rather than another victory over the climb. Beside it, outgoing and incoming reports share a board until both hands agree on unresolved names and road faults.', room_type='path', indoor=False)
    tg_gate_sightline_12 = area.room('tg_gate_sightline_12', name='Lower-Road View', desc='The approach opens to one last view across the traverse, survey shelves, and goat ledges. Signal posts remain visible in clear weather, but a rack of fog flags waits nearby for the common days when sight alone is useless.', room_type='path', indoor=False)
    tg_warm_stone_13 = area.room('tg_warm_stone_13', name='Shared Hearthstone', desc='A broad stone near the gate carries the warmth and soot of many small braziers set upon it over the years. Empty fuel baskets bear return tags, extending Bellpost’s reciprocal shelter habits all the way to the city.', room_type='path', indoor=False)
    tg_last_marker_14 = area.room('tg_last_marker_14', name='Next Departure', desc='The final board faces back toward the pass and lists the first checks for anyone leaving Tremen: weather, companions, rope, shelter stores, and known false signs. Arrival changes the traveler’s relationship to the road; it does not erase the road’s needs.', room_type='path', indoor=False)

    # Local exits
    area.exit(ra_rethward_arrival, ra_pack_count_slab, 'east')
    area.exit(ra_pack_count_slab, ra_rethward_arrival, 'west')
    area.exit(ra_pack_count_slab, ra_snowmelt_runnel_03, 'east')
    area.exit(ra_snowmelt_runnel_03, ra_pack_count_slab, 'west')
    area.exit(ra_snowmelt_runnel_03, ra_pack_count_04, 'east')
    area.exit(ra_pack_count_04, ra_snowmelt_runnel_03, 'west')
    area.exit(ra_pack_count_04, ra_low_bell_05, 'east')
    area.exit(ra_low_bell_05, ra_pack_count_04, 'west')
    area.exit(ra_low_bell_05, ra_arrival_cairn_06, 'east')
    area.exit(ra_arrival_cairn_06, ra_low_bell_05, 'west')
    area.exit(ra_arrival_cairn_06, ra_road_chalk_07, 'east')
    area.exit(ra_road_chalk_07, ra_arrival_cairn_06, 'west')
    area.exit(ra_road_chalk_07, ra_snowmelt_runnel_08, 'east')
    area.exit(ra_snowmelt_runnel_08, ra_road_chalk_07, 'west')
    area.exit(ra_snowmelt_runnel_08, ra_pack_count_09, 'east')
    area.exit(ra_pack_count_09, ra_snowmelt_runnel_08, 'west')
    area.exit(ra_pack_count_09, ra_low_bell_10, 'east')
    area.exit(ra_low_bell_10, ra_pack_count_09, 'west')
    area.exit(ra_low_bell_10, ra_arrival_cairn_11, 'east')
    area.exit(ra_arrival_cairn_11, ra_low_bell_10, 'west')
    area.exit(ra_arrival_cairn_11, ra_road_chalk_12, 'east')
    area.exit(ra_road_chalk_12, ra_arrival_cairn_11, 'west')
    area.exit(ra_road_chalk_12, ra_snowmelt_runnel_13, 'east')
    area.exit(ra_snowmelt_runnel_13, ra_road_chalk_12, 'west')
    area.exit(ra_snowmelt_runnel_13, ra_pack_count_14, 'east')
    area.exit(ra_pack_count_14, ra_snowmelt_runnel_13, 'west')
    area.exit(lm_first_marker, lm_chalked_switchback, 'east')
    area.exit(lm_chalked_switchback, lm_first_marker, 'west')
    area.exit(lm_chalked_switchback, lm_mended_rail_03, 'east')
    area.exit(lm_mended_rail_03, lm_chalked_switchback, 'west')
    area.exit(lm_mended_rail_03, lm_loose_scree_04, 'east')
    area.exit(lm_loose_scree_04, lm_mended_rail_03, 'west')
    area.exit(lm_loose_scree_04, lm_route_lesson_05, 'east')
    area.exit(lm_route_lesson_05, lm_loose_scree_04, 'west')
    area.exit(lm_route_lesson_05, lm_first_marker_06, 'east')
    area.exit(lm_first_marker_06, lm_route_lesson_05, 'west')
    area.exit(lm_first_marker_06, lm_chalk_notch_07, 'east')
    area.exit(lm_chalk_notch_07, lm_first_marker_06, 'west')
    area.exit(lm_chalk_notch_07, lm_mended_rail_08, 'east')
    area.exit(lm_mended_rail_08, lm_chalk_notch_07, 'west')
    area.exit(lm_mended_rail_08, lm_loose_scree_09, 'east')
    area.exit(lm_loose_scree_09, lm_mended_rail_08, 'west')
    area.exit(lm_loose_scree_09, lm_route_lesson_10, 'east')
    area.exit(lm_route_lesson_10, lm_loose_scree_09, 'west')
    area.exit(lm_route_lesson_10, lm_first_marker_11, 'east')
    area.exit(lm_first_marker_11, lm_route_lesson_10, 'west')
    area.exit(lm_first_marker_11, lm_chalk_notch_12, 'east')
    area.exit(lm_chalk_notch_12, lm_first_marker_11, 'west')
    area.exit(lm_chalk_notch_12, lm_mended_rail_13, 'east')
    area.exit(lm_mended_rail_13, lm_chalk_notch_12, 'west')
    area.exit(lm_mended_rail_13, lm_loose_scree_14, 'east')
    area.exit(lm_loose_scree_14, lm_mended_rail_13, 'west')
    area.exit(bw_bellpost_waystation, bw_soup_hook, 'east')
    area.exit(bw_soup_hook, bw_bellpost_waystation, 'west')
    area.exit(bw_soup_hook, bw_boot_nail_03, 'east')
    area.exit(bw_boot_nail_03, bw_soup_hook, 'west')
    area.exit(bw_boot_nail_03, bw_traveler_name_04, 'east')
    area.exit(bw_traveler_name_04, bw_boot_nail_03, 'west')
    area.exit(bw_traveler_name_04, bw_night_rope_05, 'east')
    area.exit(bw_night_rope_05, bw_traveler_name_04, 'west')
    area.exit(bw_night_rope_05, bw_bellpost_06, 'east')
    area.exit(bw_bellpost_06, bw_night_rope_05, 'west')
    area.exit(bw_bellpost_06, bw_shelter_stew_07, 'east')
    area.exit(bw_shelter_stew_07, bw_bellpost_06, 'west')
    area.exit(bw_shelter_stew_07, bw_boot_nail_08, 'east')
    area.exit(bw_boot_nail_08, bw_shelter_stew_07, 'west')
    area.exit(bw_boot_nail_08, bw_traveler_name_09, 'east')
    area.exit(bw_traveler_name_09, bw_boot_nail_08, 'west')
    area.exit(bw_traveler_name_09, bw_night_rope_10, 'east')
    area.exit(bw_night_rope_10, bw_traveler_name_09, 'west')
    area.exit(bw_night_rope_10, bw_bellpost_11, 'east')
    area.exit(bw_bellpost_11, bw_night_rope_10, 'west')
    area.exit(bw_bellpost_11, bw_shelter_stew_12, 'east')
    area.exit(bw_shelter_stew_12, bw_bellpost_11, 'west')
    area.exit(bw_shelter_stew_12, bw_boot_nail_13, 'east')
    area.exit(bw_boot_nail_13, bw_shelter_stew_12, 'west')
    area.exit(bw_boot_nail_13, bw_traveler_name_14, 'east')
    area.exit(bw_traveler_name_14, bw_boot_nail_13, 'west')
    area.exit(as_avalanche_shelter, as_red_rope_cache, 'east')
    area.exit(as_red_rope_cache, as_avalanche_shelter, 'west')
    area.exit(as_red_rope_cache, as_snow_shelf_03, 'east')
    area.exit(as_snow_shelf_03, as_red_rope_cache, 'west')
    area.exit(as_snow_shelf_03, as_rescue_tally_04, 'east')
    area.exit(as_rescue_tally_04, as_snow_shelf_03, 'west')
    area.exit(as_rescue_tally_04, as_quiet_shovel_05, 'east')
    area.exit(as_quiet_shovel_05, as_rescue_tally_04, 'west')
    area.exit(as_quiet_shovel_05, as_avalanche_shutter_06, 'east')
    area.exit(as_avalanche_shutter_06, as_quiet_shovel_05, 'west')
    area.exit(as_avalanche_shutter_06, as_red_rope_07, 'east')
    area.exit(as_red_rope_07, as_avalanche_shutter_06, 'west')
    area.exit(as_red_rope_07, as_snow_shelf_08, 'east')
    area.exit(as_snow_shelf_08, as_red_rope_07, 'west')
    area.exit(as_snow_shelf_08, as_rescue_tally_09, 'east')
    area.exit(as_rescue_tally_09, as_snow_shelf_08, 'west')
    area.exit(as_rescue_tally_09, as_quiet_shovel_10, 'east')
    area.exit(as_quiet_shovel_10, as_rescue_tally_09, 'west')
    area.exit(as_quiet_shovel_10, as_avalanche_shutter_11, 'east')
    area.exit(as_avalanche_shutter_11, as_quiet_shovel_10, 'west')
    area.exit(as_avalanche_shutter_11, as_red_rope_12, 'east')
    area.exit(as_red_rope_12, as_avalanche_shutter_11, 'west')
    area.exit(as_red_rope_12, as_snow_shelf_13, 'east')
    area.exit(as_snow_shelf_13, as_red_rope_12, 'west')
    area.exit(as_snow_shelf_13, as_rescue_tally_14, 'east')
    area.exit(as_rescue_tally_14, as_snow_shelf_13, 'west')
    area.exit(gl_goat_ledge, gl_ridgecat_shadow, 'east')
    area.exit(gl_ridgecat_shadow, gl_goat_ledge, 'west')
    area.exit(gl_ridgecat_shadow, gl_wind_tooth_03, 'east')
    area.exit(gl_wind_tooth_03, gl_ridgecat_shadow, 'west')
    area.exit(gl_wind_tooth_03, gl_lichen_shelf_04, 'east')
    area.exit(gl_lichen_shelf_04, gl_wind_tooth_03, 'west')
    area.exit(gl_lichen_shelf_04, gl_bone_charm_05, 'east')
    area.exit(gl_bone_charm_05, gl_lichen_shelf_04, 'west')
    area.exit(gl_bone_charm_05, gl_goat_trail_06, 'east')
    area.exit(gl_goat_trail_06, gl_bone_charm_05, 'west')
    area.exit(gl_goat_trail_06, gl_ridgecat_mark_07, 'east')
    area.exit(gl_ridgecat_mark_07, gl_goat_trail_06, 'west')
    area.exit(gl_ridgecat_mark_07, gl_wind_tooth_08, 'east')
    area.exit(gl_wind_tooth_08, gl_ridgecat_mark_07, 'west')
    area.exit(gl_wind_tooth_08, gl_lichen_shelf_09, 'east')
    area.exit(gl_lichen_shelf_09, gl_wind_tooth_08, 'west')
    area.exit(gl_lichen_shelf_09, gl_bone_charm_10, 'east')
    area.exit(gl_bone_charm_10, gl_lichen_shelf_09, 'west')
    area.exit(gl_bone_charm_10, gl_goat_trail_11, 'east')
    area.exit(gl_goat_trail_11, gl_bone_charm_10, 'west')
    area.exit(gl_goat_trail_11, gl_ridgecat_mark_12, 'east')
    area.exit(gl_ridgecat_mark_12, gl_goat_trail_11, 'west')
    area.exit(gl_ridgecat_mark_12, gl_wind_tooth_13, 'east')
    area.exit(gl_wind_tooth_13, gl_ridgecat_mark_12, 'west')
    area.exit(gl_wind_tooth_13, gl_lichen_shelf_14, 'east')
    area.exit(gl_lichen_shelf_14, gl_wind_tooth_13, 'west')
    area.exit(sp_survey_pull_off, sp_old_chain_pin, 'east')
    area.exit(sp_old_chain_pin, sp_survey_pull_off, 'west')
    area.exit(sp_old_chain_pin, sp_viewing_slit_03, 'east')
    area.exit(sp_viewing_slit_03, sp_old_chain_pin, 'west')
    area.exit(sp_viewing_slit_03, sp_hammer_tap_04, 'east')
    area.exit(sp_hammer_tap_04, sp_viewing_slit_03, 'west')
    area.exit(sp_hammer_tap_04, sp_map_scratch_05, 'east')
    area.exit(sp_map_scratch_05, sp_hammer_tap_04, 'west')
    area.exit(sp_map_scratch_05, sp_survey_notch_06, 'east')
    area.exit(sp_survey_notch_06, sp_map_scratch_05, 'west')
    area.exit(sp_survey_notch_06, sp_old_chain_07, 'east')
    area.exit(sp_old_chain_07, sp_survey_notch_06, 'west')
    area.exit(sp_old_chain_07, sp_viewing_slit_08, 'east')
    area.exit(sp_viewing_slit_08, sp_old_chain_07, 'west')
    area.exit(sp_viewing_slit_08, sp_hammer_tap_09, 'east')
    area.exit(sp_hammer_tap_09, sp_viewing_slit_08, 'west')
    area.exit(sp_hammer_tap_09, sp_map_scratch_10, 'east')
    area.exit(sp_map_scratch_10, sp_hammer_tap_09, 'west')
    area.exit(sp_map_scratch_10, sp_survey_notch_11, 'east')
    area.exit(sp_survey_notch_11, sp_map_scratch_10, 'west')
    area.exit(sp_survey_notch_11, sp_old_chain_12, 'east')
    area.exit(sp_old_chain_12, sp_survey_notch_11, 'west')
    area.exit(sp_old_chain_12, sp_viewing_slit_13, 'east')
    area.exit(sp_viewing_slit_13, sp_old_chain_12, 'west')
    area.exit(sp_viewing_slit_13, sp_hammer_tap_14, 'east')
    area.exit(sp_hammer_tap_14, sp_viewing_slit_13, 'west')
    area.exit(wt_windcut_turn, wt_broken_banner, 'east')
    area.exit(wt_broken_banner, wt_windcut_turn, 'west')
    area.exit(wt_broken_banner, wt_eagle_shadow_03, 'east')
    area.exit(wt_eagle_shadow_03, wt_broken_banner, 'west')
    area.exit(wt_eagle_shadow_03, wt_sleet_bite_04, 'east')
    area.exit(wt_sleet_bite_04, wt_eagle_shadow_03, 'west')
    area.exit(wt_sleet_bite_04, wt_thin_rope_05, 'east')
    area.exit(wt_thin_rope_05, wt_sleet_bite_04, 'west')
    area.exit(wt_thin_rope_05, wt_windcut_turn_06, 'east')
    area.exit(wt_windcut_turn_06, wt_thin_rope_05, 'west')
    area.exit(wt_windcut_turn_06, wt_false_tab_07, 'east')
    area.exit(wt_false_tab_07, wt_windcut_turn_06, 'west')
    area.exit(wt_false_tab_07, wt_eagle_shadow_08, 'east')
    area.exit(wt_eagle_shadow_08, wt_false_tab_07, 'west')
    area.exit(wt_eagle_shadow_08, wt_sleet_bite_09, 'east')
    area.exit(wt_sleet_bite_09, wt_eagle_shadow_08, 'west')
    area.exit(wt_sleet_bite_09, wt_thin_rope_10, 'east')
    area.exit(wt_thin_rope_10, wt_sleet_bite_09, 'west')
    area.exit(wt_thin_rope_10, wt_windcut_turn_11, 'east')
    area.exit(wt_windcut_turn_11, wt_thin_rope_10, 'west')
    area.exit(wt_windcut_turn_11, wt_false_tab_12, 'east')
    area.exit(wt_false_tab_12, wt_windcut_turn_11, 'west')
    area.exit(wt_false_tab_12, wt_eagle_shadow_13, 'east')
    area.exit(wt_eagle_shadow_13, wt_false_tab_12, 'west')
    area.exit(wt_eagle_shadow_13, wt_sleet_bite_14, 'east')
    area.exit(wt_sleet_bite_14, wt_eagle_shadow_13, 'west')
    area.exit(tg_tremen_gate, tg_final_bell, 'east')
    area.exit(tg_final_bell, tg_tremen_gate, 'west')
    area.exit(tg_final_bell, tg_warm_stone_03, 'east')
    area.exit(tg_warm_stone_03, tg_final_bell, 'west')
    area.exit(tg_warm_stone_03, tg_last_marker_04, 'east')
    area.exit(tg_last_marker_04, tg_warm_stone_03, 'west')
    area.exit(tg_last_marker_04, tg_road_gratitude_05, 'east')
    area.exit(tg_road_gratitude_05, tg_last_marker_04, 'west')
    area.exit(tg_road_gratitude_05, tg_final_bell_06, 'east')
    area.exit(tg_final_bell_06, tg_road_gratitude_05, 'west')
    area.exit(tg_final_bell_06, tg_gate_sightline_07, 'east')
    area.exit(tg_gate_sightline_07, tg_final_bell_06, 'west')
    area.exit(tg_gate_sightline_07, tg_warm_stone_08, 'east')
    area.exit(tg_warm_stone_08, tg_gate_sightline_07, 'west')
    area.exit(tg_warm_stone_08, tg_last_marker_09, 'east')
    area.exit(tg_last_marker_09, tg_warm_stone_08, 'west')
    area.exit(tg_last_marker_09, tg_road_gratitude_10, 'east')
    area.exit(tg_road_gratitude_10, tg_last_marker_09, 'west')
    area.exit(tg_road_gratitude_10, tg_final_bell_11, 'east')
    area.exit(tg_final_bell_11, tg_road_gratitude_10, 'west')
    area.exit(tg_final_bell_11, tg_gate_sightline_12, 'east')
    area.exit(tg_gate_sightline_12, tg_final_bell_11, 'west')
    area.exit(tg_gate_sightline_12, tg_warm_stone_13, 'east')
    area.exit(tg_warm_stone_13, tg_gate_sightline_12, 'west')
    area.exit(tg_warm_stone_13, tg_last_marker_14, 'east')
    area.exit(tg_last_marker_14, tg_warm_stone_13, 'west')
    area.exit(ra_pack_count_14, lm_first_marker, 'north')
    area.exit(lm_first_marker, ra_pack_count_14, 'south')
    area.exit(lm_loose_scree_14, bw_bellpost_waystation, 'north')
    area.exit(bw_bellpost_waystation, lm_loose_scree_14, 'south')
    area.exit(bw_traveler_name_14, as_avalanche_shelter, 'north')
    area.exit(as_avalanche_shelter, bw_traveler_name_14, 'south')
    area.exit(as_rescue_tally_14, gl_goat_ledge, 'north')
    area.exit(gl_goat_ledge, as_rescue_tally_14, 'south')
    area.exit(gl_lichen_shelf_14, sp_survey_pull_off, 'north')
    area.exit(sp_survey_pull_off, gl_lichen_shelf_14, 'south')
    area.exit(sp_hammer_tap_14, wt_windcut_turn, 'north')
    area.exit(wt_windcut_turn, sp_hammer_tap_14, 'south')
    area.exit(wt_sleet_bite_14, tg_tremen_gate, 'north')
    area.exit(tg_tremen_gate, wt_sleet_bite_14, 'south')
    area.exit(tg_tremen_gate, 'tremen:gt_lower_gate', 'north', one_way=True)

    # NPCs
    _route_warden = area.npc(ra_rethward_arrival, 'npc_route_warden_mirren', name='Route Warden Mirren', faction='wardens', dialogue={'greeting_tiers': {"neutral": 'Mirren counts your party twice and your rope three times.'}, 'topics': {'route': 'The road is generous if you respect its bookkeeping.'}, 'base_hints': []})
    _bellpost_keeper = area.npc(bw_bellpost_waystation, 'npc_bellpost_keeper_roven', name='Bellpost Keeper Roven', faction='wardens', dialogue={'greeting_tiers': {"neutral": 'Roven has soup on the hook and chalk dust on both thumbs.'}, 'topics': {'markers': 'A mark that only locals understand is a vanity, not a rescue tool.'}, 'base_hints': []})
    _shelter_medic = area.npc(as_avalanche_shelter, 'npc_shelter_medic_essa', name='Shelter Medic Essa', faction='verdance', dialogue={'greeting_tiers': {"neutral": 'Essa checks ears, fingers, and courage in that order.'}, 'topics': {'rescue': 'Fast help matters, but careful help keeps the helpers alive.'}, 'base_hints': []})
    _surveyor = area.npc(sp_survey_pull_off, 'npc_surveyor_pel', name='Surveyor Pel', faction='western_arcana', dialogue={'greeting_tiers': {"neutral": 'Pel keeps a map pinned with spoon handles and old chain links.'}, 'topics': {'survey': 'The old chain pins were accurate. That does not mean they were kind.'}, 'base_hints': []})

    # Quest item templates
    area.item('glp_marker_tally', key='marker tally', item_type='item', weight=0.5, rarity='normal', desc='A damp tally of repaired lower-pass markers, smudged by glove thumbs and snow.', value=0, is_quest_item=True)

    # Quests
    area.quest(
        'glp_q_marker_line',
        name='Line Of Bells',
        description='Roven turns the city marker kit into a route lesson, asking you to walk the line and repair what actually guides frightened travelers.',
        quest_type='delivery',
        quest_giver='npc_bellpost_keeper_roven',
        objectives=[{'type': 'visit', 'target': 'lm_first_marker', 'count': 1}, {'type': 'investigate', 'target': 'wt_windcut_turn', 'count': 1}, {'type': 'deliver', 'target': 'npc_route_warden_mirren', 'count': 1, 'item_tag': 'glp_marker_tally'}],
        rewards=[{'action_type': 'give_scales', 'amount': 32}, {'action_type': 'give_skill_xp', 'skill_id': 'survival', 'count': 12}],
        next_quest_id=None,
        prerequisite_quests=['tre_q_waystation_marks'],
        can_share=True,
        consequence_small='Roven replaces three private shorthand marks with clear public ones and writes your name beside the safer line.',
    )
    area.quest(
        'glp_q_missing_pack',
        name='Pack In The Shelter Snow',
        description='Essa asks you to find the owner of an abandoned pack, pushing you through avalanche shelter habits before combat becomes the loudest answer.',
        quest_type='rescue',
        quest_giver='npc_shelter_medic_essa',
        objectives=[{'type': 'investigate', 'target': 'as_avalanche_shelter', 'count': 1}, {'type': 'kill', 'target': 'ridgecat', 'count': 2}, {'type': 'talk_to', 'target': 'npc_shelter_medic_essa', 'count': 1}],
        rewards=[{'action_type': 'give_scales', 'amount': 34}, {'action_type': 'modify_standing', 'faction_id': 'verdance', 'delta': 1800}],
        next_quest_id=None,
        prerequisite_quests=[],
        can_share=True,
        consequence_small='Essa hangs the recovered pack where late travelers can see it and remember that a shelter is a promise, not a pantry.',
    )
    area.quest(
        'glp_q_false_tabs',
        name='False Tabs',
        description='Mirren has you hunt the people moving marker tabs, making the bandit loop about route sabotage rather than random roadside violence.',
        quest_type='combat',
        quest_giver='npc_route_warden_mirren',
        objectives=[{'type': 'investigate', 'target': 'wt_windcut_turn', 'count': 1}, {'type': 'kill', 'target': 'marker_bandit', 'count': 4}, {'type': 'deliver', 'target': 'npc_route_warden_mirren', 'count': 1, 'item_tag': 'glp_marker_tally'}],
        rewards=[{'action_type': 'give_scales', 'amount': 40}, {'action_type': 'modify_standing', 'faction_id': 'wardens', 'delta': 1800}],
        next_quest_id=None,
        prerequisite_quests=[],
        can_share=True,
        consequence_small='Mirren nails the false tabs above the arrival slab as a warning that clever cruelty is still cruelty.',
    )
    area.quest(
        'glp_q_bellpost_fish',
        name='Soup Beneath The Bell',
        description='Roven teaches that fishing is roadcraft here: a snowmelt pool can feed a stuck waystation when weather closes both directions.',
        quest_type='gather',
        quest_giver='npc_bellpost_keeper_roven',
        objectives=[{'type': 'visit', 'target': 'bw_bellpost_waystation', 'count': 1}, {'type': 'gather', 'target': 'snowmelt_trout', 'count': 3}, {'type': 'deliver', 'target': 'npc_shelter_medic_essa', 'count': 1, 'item_tag': 'snowmelt_trout'}],
        rewards=[{'action_type': 'give_scales', 'amount': 26}, {'action_type': 'give_skill_xp', 'skill_id': 'fishing', 'count': 12}],
        next_quest_id=None,
        prerequisite_quests=[],
        can_share=True,
        consequence_small='The bellpost soup hook carries your catch through the next storm, and Roven starts pointing new anglers toward useful water instead of easy water.',
    )

    # Spawns
    area.spawn(lm_first_marker, 'greyteeth_scavenger', count_min=1, count_max=2, respawn_minutes=14, respawn_variance=4)
    area.spawn(lm_chalked_switchback, 'marker_bandit', count_min=1, count_max=2, respawn_minutes=14, respawn_variance=4)
    area.spawn(lm_loose_scree_04, 'greyteeth_scavenger', count_min=1, count_max=2, respawn_minutes=14, respawn_variance=4)
    area.spawn(as_avalanche_shelter, 'ridgecat', count_min=1, count_max=2, respawn_minutes=14, respawn_variance=4)
    area.spawn(as_red_rope_cache, 'greyteeth_scavenger', count_min=1, count_max=1, respawn_minutes=14, respawn_variance=4)
    area.spawn(as_snow_shelf_03, 'ridgecat', count_min=1, count_max=2, respawn_minutes=14, respawn_variance=4)
    area.spawn(gl_goat_ledge, 'ridgecat', count_min=1, count_max=2, respawn_minutes=14, respawn_variance=4)
    area.spawn(gl_ridgecat_shadow, 'ridgecat', count_min=1, count_max=2, respawn_minutes=14, respawn_variance=4)
    area.spawn(gl_wind_tooth_03, 'windcut_eagle', count_min=1, count_max=2, respawn_minutes=14, respawn_variance=4)
    area.spawn(wt_windcut_turn, 'marker_bandit', count_min=1, count_max=2, respawn_minutes=14, respawn_variance=4)
    area.spawn(wt_false_tab_07, 'marker_bandit', count_min=1, count_max=2, respawn_minutes=14, respawn_variance=4)
    area.spawn(wt_eagle_shadow_03, 'windcut_eagle', count_min=1, count_max=2, respawn_minutes=14, respawn_variance=4)
    area.spawn(sp_survey_pull_off, 'greyteeth_scavenger', count_min=1, count_max=1, respawn_minutes=14, respawn_variance=4)

    # Gathering pools
    area.gathering_pool('ore', ['lm_chalked_switchback', 'sp_old_chain_pin', 'wt_windcut_turn'], ['greyteeth_iron', 'coldvein_stone'], max_active=3, respawn_minutes=12, respawn_variance=4, tier_floor=2, tier_ceiling=2)
    area.gathering_pool('herb', ['ra_snowmelt_runnel_03', 'gl_lichen_shelf_04'], ['windroot'], max_active=3, respawn_minutes=12, respawn_variance=4, tier_floor=2, tier_ceiling=2)
    area.gathering_pool('forage', ['bw_soup_hook', 'as_red_rope_cache'], ['haul_rope_fiber', 'bellcap_mushroom'], max_active=3, respawn_minutes=12, respawn_variance=4, tier_floor=1, tier_ceiling=2)
    area.gathering_pool('hide', ['gl_ridgecat_shadow', 'as_snow_shelf_03'], ['ridgecat_pelt'], max_active=3, respawn_minutes=12, respawn_variance=4, tier_floor=2, tier_ceiling=2)
    area.gathering_pool('fish', ['ra_snowmelt_runnel_03', 'bw_bellpost_waystation'], ['snowmelt_trout'], max_active=3, respawn_minutes=12, respawn_variance=4, tier_floor=2, tier_ceiling=2)

    # Lore fragments
    area.lore_fragment(
        'glp_lore_marker_names',
        lm_first_marker,
        discovery_method='search',
        scholar_path='architecture',
        text='The earliest marker marks are not directions but rescuer initials, as if the route first learned to speak through people who came back for strangers.',
        insight_gain=1,
    )

    return area.build()
