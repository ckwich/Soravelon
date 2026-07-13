"""Tremeneth High Passes -- Hub 3 exterior zone

Wind-shorn patrol stairs, storm bells, guarded cairns, and high ridges where Warden duty and Druid caution meet."""

from world.area_builder import AreaBuilder


def build():
    area = AreaBuilder('tremeneth_high_passes')

    area.zone(
        name='Tremeneth High Passes',
        zone_type='mountain',
        continent='varath',
        tier=3,
        region='tremeneth_mountains',
        faction_territory='warden',
        faction_presence=['wardens', 'ironblood', 'resonance', 'verdance', 'western_arcana'],
        world_x=35,
        world_y=50,
        world_radius=165,
    )

    # Materials
    area.material('coldvein_stone', tier=2, terrain='stone', absorbed_property='endurance', profession_bonus={'engineering': 0.1, 'mining': 0.05})
    area.material('resonance_shard', tier=3, terrain='deep stone', absorbed_property='attunement', profession_bonus={'alchemy': 0.1, 'scholarship': 0.05})
    area.material('windroot', tier=2, terrain='alpine', absorbed_property='breath', profession_bonus={'alchemy': 0.1, 'herbalism': 0.05})
    area.material('bellcap_mushroom', tier=2, terrain='cavern', absorbed_property='focus', profession_bonus={'cooking': 0.1, 'foraging': 0.05})
    area.material('snowmelt_trout', tier=2, terrain='water', absorbed_property='clarity', profession_bonus={'cooking': 0.1, 'fishing': 0.05})
    area.material('ridgecat_pelt', tier=2, terrain='ridge', absorbed_property='warmth', profession_bonus={'smithing': 0.1, 'skinning': 0.05})

    # Rooms
    ps_patrol_stair = area.room('ps_patrol_stair', name='Patrol Stair', desc='The lift from Tremen opens onto broad half-dwarf steps polished by generations of laden boots. High Warden Thessa keeps two slate columns beside the first rise—one for patrols climbing and one for those expected home—while fresh chalk records wind, visibility, and the hour of the last bell.', room_type='path', indoor=False)
    ps_breathing_niche = area.room('ps_breathing_niche', name='Breathing Niche', desc='A shoulder-deep recess breaks the first hard climb, its back wall warmed faintly by stone from the city below. Notches at hand height mark the slow count taught to new climbers, and a row of pegs holds packs set down by people wise enough to turn back before pride became a rescue.', room_type='path', indoor=False)
    ps_rope_bell_03 = area.room('ps_rope_bell_03', name='Lower Warning Bell', desc='A tarred rope follows the stair to a bronze bell housed beneath a shallow stone hood. Patrol knots tied below the handle identify who tested the line today; an older red cord remains until its frayed section farther uphill has been replaced.', room_type='path', indoor=False)
    ps_old_boot_04 = area.room('ps_old_boot_04', name="Dori's Boot", desc="One iron-shod boot is fixed heel-first into a crack beside the path, filled with hardy white flowers. A small plate names Dori Venn, who carried three strangers down through a sleetfall and complained afterward only that they had packed poor socks; passing patrols leave fresh laces around the ankle.", room_type='path', indoor=False)
    ps_thin_air_05 = area.room('ps_thin_air_05', name='First Windbreak', desc='The stair turns out of the mountain shadow and the air becomes suddenly cold, bright, and spare. A waist-high wall gives climbers somewhere to crouch while wind drives loose frost over it, and scuffed arcs in the snow show where Wardens have checked one another for shaking hands before continuing.', room_type='path', indoor=False)
    ps_patrol_stair_06 = area.room('ps_patrol_stair_06', name='Switchback Muster', desc='Three switchbacks meet on a landing wide enough for a patrol to count heads without blocking the descent. Colored stone chips in a covered tray match the day’s posted routes, so a missing climber leaves a visible gap long before the weather closes over their tracks.', room_type='path', indoor=False)
    ps_breath_niche_07 = area.room('ps_breath_niche_07', name="Medic's Niche", desc='Wool blankets, splints, and sealed warming bricks occupy a dry recess cut behind a thick stone lip. Each bundle bears the name of the household that supplied it and a return tally, making neglect as public as generosity when the stores are inspected.', room_type='path', indoor=False)
    ps_rope_bell_08 = area.room('ps_rope_bell_08', name='Middle Warning Bell', desc='A squat bell hangs where the stair crosses a bare rib of mountain, its tone carrying both down toward Tremen and up toward the storm line. The clapper has been wrapped for repair, and a slate directs patrols to relay warnings by the paired rope pulls recorded beneath it.', room_type='path', indoor=False)
    ps_old_boot_09 = area.room('ps_old_boot_09', name="Tammel's Last", desc="A child-sized climbing boot rests inside a glazed wall box with its worn sole turned outward. The accompanying card explains that Tammel outgrew it on his first full patrol and now repairs the city lift; new climbers tuck written promises behind the frame, then collect them on the way home.", room_type='path', indoor=False)
    ps_thin_air_10 = area.room('ps_thin_air_10', name='Cloudbreak Step', desc='Clouds stream below the outer edge of this narrow step, opening brief views of Tremen’s roofs and the lower road beyond. Patrol marks point not toward the view but toward three gathering banks of weather, their dates and initials allowing the next watch to compare what has changed.', room_type='path', indoor=False)
    ps_patrol_stair_11 = area.room('ps_patrol_stair_11', name='Relief Turn', desc='A sheltered turn serves as the handoff point between city watch and high-pass patrols. Waxed tablets list blocked steps, animal sign, and travelers still abroad; yesterday’s entries remain beneath today’s so a recurring hazard cannot be dismissed as a single bad crossing.', room_type='path', indoor=False)
    ps_breath_niche_12 = area.room('ps_breath_niche_12', name='Shared-Flask Niche', desc='A long stone bench faces inward from the drop, forcing resting climbers to look at one another instead of the height. Empty flask hooks are tagged by patrol and date, while a copper basin catches clean snow for the next descent crew to melt and replenish.', room_type='path', indoor=False)
    ps_rope_bell_13 = area.room('ps_rope_bell_13', name='Upper Muster Bell', desc='The upper bell stands within a cage of black iron that keeps wind-thrown debris from striking it by accident. A board of carved call patterns distinguishes storm, injury, lost traveler, and clear passage; fresh practice scores show which patrol must repeat the drill tomorrow.', room_type='path', indoor=False)
    ps_old_boot_14 = area.room('ps_old_boot_14', name='Last-Boot Cairn', desc='Boot buckles, sole nails, and smooth stones surround the final cairn before the exposed storm-bell route. Each token carries an initial for someone who turned back or was brought home, and a clear strip is deliberately left for names the next patrol hopes it will not need.', room_type='path', indoor=False)
    sb_storm_bells = area.room('sb_storm_bells', name='Storm Bells', desc='Five bronze bells face different reaches of the sky from a half-circle of stone cradles. Storm Listener Ava has chalked the morning’s pitch beneath each one, leaving room for travelers to add the hour when wind, ice, or distant thunder changed what they heard.', room_type='path', indoor=False)
    sb_frosted_clapper = area.room('sb_frosted_clapper', name='Frosted Clapper', desc='Rime thickens one bell’s clapper until every gust produces a dull, late note. A ladder, scraper, and safety line lie secured nearby, and the maintenance slate names both the listener who reported the lag and the patrol assigned to clear it.', room_type='path', indoor=False)
    sb_weather_oath_03 = area.room('sb_weather_oath_03', name='Weather Oath Slate', desc='A black slate carries the listener’s oath: report what the mountain says, admit what you could not hear, and let each traveler choose with honest warning. Older signatures have been preserved around its edge, including several crossed out by the people themselves after they mistook certainty for skill.', room_type='path', indoor=False)
    sb_ringing_ice_04 = area.room('sb_ringing_ice_04', name='Ice Chime Rack', desc='Thin bars of gathered ice hang from a cedar frame, each cut from a different exposed ledge. Their changing notes give Ava a rough comparison of temperature and wind, while a bucket catches the meltwater so no one pretends yesterday’s chimes can describe today.', room_type='path', indoor=False)
    sb_low_thunder_05 = area.room('sb_low_thunder_05', name='Thunder Notch', desc='The path narrows between two leaning slabs where thunder arrives through the stone before it reaches the ear. Pebbles sorted into shallow cups record the gaps between tremors, a simple ledger that lets one watch compare a growing storm with those survived in earlier seasons.', room_type='path', indoor=False)
    sb_storm_bell_06 = area.room('sb_storm_bell_06', name='South-Reach Bell', desc='A greened bell points toward Tremen and the lower roads, carrying warnings to people who cannot yet see the high weather. Wax plugs and a padded mallet hang in a dry case, evidence that the listener protects nearby ears as carefully as the settlements below.', room_type='path', indoor=False)
    sb_frosted_clapper_07 = area.room('sb_frosted_clapper_07', name='Clapper Hearth', desc='A hooded charcoal basin gives just enough heat to thaw bell fittings without weakening the bronze. Each replaced pin is wired to a board with its date and failure mark, turning small repairs into a history that the next craftsperson can challenge or improve.', room_type='path', indoor=False)
    sb_weather_oath_08 = area.room('sb_weather_oath_08', name='Relief Listener Post', desc='Two stone seats face opposite horizons so an arriving listener can compare observations before the tired watch descends. Half-finished tea and a disputed cloud sketch occupy the shared ledge; both names remain on the page until later weather settles which reading was useful.', room_type='path', indoor=False)
    sb_ringing_ice_09 = area.room('sb_ringing_ice_09', name='Melt Ledger', desc='Channels cut in the rock guide thaw from the bell ropes into marked copper cups. Ava’s notes compare how quickly each cup fills under sun, cloud, and crosswind, with blank rows waiting for the next shift rather than presenting any pattern as permanent.', room_type='path', indoor=False)
    sb_low_thunder_10 = area.room('sb_low_thunder_10', name='Ground-Hum Step', desc='A broad step rests on a seam that hums when distant weather presses against the range. Listeners kneel here with fingertips to stone, but a painted warning reminds them that mine blasts, hooves, and shifting ice can imitate a storm and must be checked against other signs.', room_type='path', indoor=False)
    sb_storm_bell_11 = area.room('sb_storm_bell_11', name='North-Reach Bell', desc='The northern bell is smaller and sharper, aimed along ridges where wind can swallow a lower tone. Colored streamers tied below it show which valleys can currently hear the signal, and a bundle of replacements waits for patrol reports to move those claims.', room_type='path', indoor=False)
    sb_frosted_clapper_12 = area.room('sb_frosted_clapper_12', name='Spare Clapper Rack', desc='Clappers of bronze, stone, and iron hang from a sheltered rack, each labeled with the bell and weather it best serves. Several empty hooks bear promised delivery dates from Tremen smiths, making the warning line visibly dependent on work performed far below.', room_type='path', indoor=False)
    sb_weather_oath_13 = area.room('sb_weather_oath_13', name='Traveler Choice Board', desc='Three movable markers indicate which routes listeners judge clear, uncertain, or closing, with the observation time carved beside every judgment. Beneath them, a permanent inscription states that the bells warn rather than command; those who proceed are asked to leave a route token for the patrol that may follow.', room_type='path', indoor=False)
    sb_ringing_ice_14 = area.room('sb_ringing_ice_14', name='Last Ice Tongue', desc='Wind draws a clear, uneasy note from a blade of ice overhanging the final bell cradle. Broken fragments have been arranged by date instead of swept away, showing how often the pitch changes before the path reaches the animal-cut ridges ahead.', room_type='path', indoor=False)
    ir_ice_shear_ridge = area.room('ir_ice_shear_ridge', name='Ice-Shear Ridge', desc='Wind has peeled the snow from one side of this ridge and packed it into a blue-white cornice on the other. Stormgoat tracks cross the boot path without following it, while Warden tally marks distinguish the herd seen at dawn from animals driven uphill by later bells.', room_type='path', indoor=False)
    ir_goat_break = area.room('ir_goat_break', name='Goat Break', desc='Broken horn sheaths and coarse gray hair cling to stones rubbed smooth by stormgoats squeezing through the gap. A patrol post bears two route arrows—one for giving a settled herd room and another for crossing when fresh ridgecat scent turns the animals restless.', room_type='path', indoor=False)
    ir_knife_wind_03 = area.room('ir_knife_wind_03', name='Knife-Wind Shelf', desc='Crosswind scours a shelf barely wide enough for two careful travelers, exposing prints that drifting snow would hide elsewhere. Rounded goat tracks bunch near the inner wall, but broad clawed pads keep to the higher lip; a recently replaced warning pennant confirms the predator sign is current.', room_type='path', indoor=False)
    ir_blue_crack_04 = area.room('ir_blue_crack_04', name='Coldvein Fissure', desc='A narrow blue fissure reveals coldvein stone beneath the ice, its workable edges marked in charcoal by Tremen surveyors. Chisel dates and filled-in scars show where earlier cuts were closed before the shelf weakened, leaving today’s gathering boundary smaller than last season’s.', room_type='path', indoor=False)
    ir_snow_glare_05 = area.room('ir_snow_glare_05', name='Glare Screen', desc='Sunlight rebounds between snowfield and pale cliff until depth becomes difficult to judge. Strips of dark wool have been threaded through a low rope at boot height, giving travelers a line to follow without raising a barrier that would trap the animals using this crossing.', room_type='path', indoor=False)
    ir_ice_shear_06 = area.room('ir_ice_shear_06', name='Sheared Shelf', desc='A recent slab break has left raw stone beside older ice rounded by many winters. Patrol stakes track the crack’s retreat in dated spans, and hoofprints detour above the newest marker as if the stormgoats noticed the change before the survey crew did.', room_type='path', indoor=False)
    ir_goat_break_07 = area.room('ir_goat_break_07', name='Mineral Lick', desc='Rust-red mineral stains draw stormgoats to a sheltered wall where countless tongues have polished the stone. Wardens have moved the footpath downslope and hung a quiet-route sign, preserving access while leaving the feeding place enough distance to settle.', room_type='path', indoor=False)
    ir_knife_wind_08 = area.room('ir_knife_wind_08', name='Claw-Scrape Bend', desc='Four fresh scratches score a leaning marker above a bend littered with tufts of ridgecat fur. A patrol has turned the marker sideways rather than erasing the sign, warning later travelers that the animal now crosses here while preserving the evidence for the next count.', room_type='path', indoor=False)
    ir_blue_crack_09 = area.room('ir_blue_crack_09', name='Mended Crevasse', desc='A half-dwarf stone bridge spans a crack glowing blue through deep ice. Its newest blocks carry mason names and quarry marks, while a basket below catches chips for inspection so frost damage can be traced to a repair instead of blamed on the mountain in general.', room_type='path', indoor=False)
    ir_snow_glare_10 = area.room('ir_snow_glare_10', name='Whiteout Stakes', desc='Tall stakes disappear one after another into the bright slope, each painted with a different raised pattern for hands numbed by cold. A sliding ring on the nearest stake records how high the last patrol found the snow, making the route’s worsening burden visible before the next bell sounds.', room_type='path', indoor=False)
    ir_ice_shear_11 = area.room('ir_ice_shear_11', name='Molt Shelf', desc='Wind has gathered pale underfur in the lee of a rock spur, along with the smaller pawprints of a young ridgecat. A Warden tag dates the finding and redirects routine patrols below the shelf, leaving any decision to intervene for evidence of hunger, injury, or danger to travelers.', room_type='path', indoor=False)
    ir_goat_break_12 = area.room('ir_goat_break_12', name='Kidding Ledge', desc='Small hoofprints circle a patch of trampled alpine grass beneath an overhang darkened by old shelter fires. Seasonal markers ask hunters to pass the ledge without pursuit, and crossed-out dates preserve how long each restriction actually lasted rather than making caution permanent by habit.', room_type='path', indoor=False)
    ir_knife_wind_13 = area.room('ir_knife_wind_13', name='Carrion Wind', desc='The wind carries the iron smell of an old stormgoat kill from somewhere above the path. Fur caught in thorny windroot and drag marks toward the rocks place a ridgecat’s feeding ground uphill, while bootprints below show recent travelers gave it the wider claim.', room_type='path', indoor=False)
    ir_blue_crack_14 = area.room('ir_blue_crack_14', name='Coldvein Threshold', desc='Blue-veined stone breaks through the last icy rise before the Warden cairns. Numbered sample hollows match sealed packets in a weather box, and an untouched band between them is marked for comparison after the next thaw rather than offered for immediate cutting.', room_type='path', indoor=False)
    wc_warden_cairn = area.room('wc_warden_cairn', name='Warden Cairn', desc='Flat stones form a shoulder-high cairn beneath the circling route of windcut eagles. Every visible face carries the name of someone brought home from the pass; loose stones wait in a covered box, but no rescuer’s name is carved larger than the person they returned.', room_type='path', indoor=False)
    wc_counting_slate = area.room('wc_counting_slate', name='Outbound Slate', desc='A roofed slate lists travelers, patrols, pack animals, and the routes they intended to take. Return marks are cut deeply enough to survive sleet, while uncertain sightings remain in chalk until a named witness or a recovered route token confirms them.', room_type='path', indoor=False)
    wc_signal_notch_03 = area.room('wc_signal_notch_03', name='Red Signal Notch', desc='A cleft in the ridge frames the Storm Bells behind and the next cairn ahead. Red cloth tied across the opening warns of fresh ridgecat sign nearby, and bite marks on the signal case explain why patrols now sheath spare flags in tin rather than leather.', room_type='path', indoor=False)
    wc_lost_glove_04 = area.room('wc_lost_glove_04', name='The Unmatched Glove', desc='A heavy left glove hangs beneath glass with its find-place and weather written on the frame. No name has been assigned to it; the Warden record preserves several rejected guesses so a familiar stitching pattern cannot become false certainty through repetition.', room_type='path', indoor=False)
    wc_patrol_debt_05 = area.room('wc_patrol_debt_05', name='Rescue-Debt Board', desc='Wooden tags record blankets, rope, food, and watch hours spent bringing people safely down. Those rescued repay the pass by replacing supplies or serving a later watch when able, and open debts are grouped by need rather than by shame or coin.', room_type='path', indoor=False)
    wc_warden_cairn_06 = area.room('wc_warden_cairn_06', name='Returned-Names Cairn', desc='This low cairn is rebuilt after every successful search, one temporary marker exchanged for a stone bearing the traveler’s own account of the return. Several inscriptions credit cooks, bell listeners, and lift crews alongside the patrol, making rescue a chain of work rather than a single heroic moment.', room_type='path', indoor=False)
    wc_counting_slate_07 = area.room('wc_counting_slate_07', name='Rescue Stores Count', desc='Rope coils, canvas litters, heat bricks, and hooded lamps occupy numbered stone lockers. A tally beside each latch records what left, what came back damaged, and who promised repair, allowing the next search party to see the real cost of readiness.', room_type='path', indoor=False)
    wc_signal_notch_08 = area.room('wc_signal_notch_08', name='Mirror Notch', desc='A polished metal plate can flash the city, Storm Bells, or higher cairns when the sky is clear. Practice times cover the adjacent slate, including failed replies, so line-of-sight claims are renewed by actual watches instead of inherited from an old map.', room_type='path', indoor=False)
    wc_lost_glove_09 = area.room('wc_lost_glove_09', name='Matched-Pair Shelf', desc='Recovered gloves, scarves, buckles, and route tokens rest in labeled cubbies awaiting a claimant or a patrol homeward. Empty spaces bear small return notes with dates and destinations, turning ordinary belongings into proof that many searches end with someone known again.', room_type='path', indoor=False)
    wc_patrol_debt_10 = area.room('wc_patrol_debt_10', name='Promise Hooks', desc='Iron hooks hold wooden promises from climbers who accepted food, shelter, or escort on this route. Completed tags are not discarded; they hang reversed to show the later patrol, meal, repair, or warning that paid the help forward.', room_type='path', indoor=False)
    wc_warden_cairn_11 = area.room('wc_warden_cairn_11', name='Open-Search Cairn', desc='Seven uncarved stones stand apart from the named cairns, each paired with the last reliable route and weather report for a missing traveler. Patrols move a stone only when new evidence changes the search, preventing hope, fear, or rumor from quietly rewriting where attention is owed.', room_type='path', indoor=False)
    wc_counting_slate_12 = area.room('wc_counting_slate_12', name='Search Ledger', desc='Waxed pages compare tracks, witness statements, bell times, and supplies committed to active searches. Contradictions are boxed instead of erased, giving the relief patrol a place to begin testing accounts rather than rewarding whichever story arrived first.', room_type='path', indoor=False)
    wc_signal_notch_13 = area.room('wc_signal_notch_13', name='Green Signal Notch', desc='The next notch opens toward the Druid-guarded route, where a green cord marks the limit of routine Warden signaling. A second hook remains empty for messages accepted by both watches, acknowledging that urgency does not erase another steward’s boundary.', room_type='path', indoor=False)
    wc_lost_glove_14 = area.room('wc_lost_glove_14', name='Boundary Mittens', desc='Two patched mittens share a weather box at the last cairn, one Warden blue and one tied with Verdance green. Their repair log passes back and forth between patrols, a modest record that cooperation here is maintained through repeated work rather than assumed agreement.', room_type='path', indoor=False)
    dg_guarded_stone = area.room('dg_guarded_stone', name='Guarded Stone', desc='A broad dark stone rises through the path without tool marks, warm enough to keep a narrow ring of frost at bay. Druid Guard Elun has placed a listening frame outside a green cord, while a Warden slate records the safe width left for patrols; neither record claims to know why the stone differs from its neighbors.', room_type='path', indoor=False)
    dg_green_thread = area.room('dg_green_thread', name='Green Thread', desc='A thread of moss follows a hairline seam away from the guarded stone, bright against the winter-gray rock. Tiny loose orelings have disturbed several observation pegs, and Elun’s corrected sketch preserves both their movement and the earlier mistaken boundary.', room_type='path', indoor=False)
    dg_druid_hush_03 = area.room('dg_druid_hush_03', name='Listening Hush', desc='A curve of stacked stone screens the worst wind without enclosing the path. Visitors are asked to cross quietly because seed fall, animal steps, and cracks in thawing rock are being counted here; wax tablets list what was actually heard alongside long intervals when nothing answered.', room_type='path', indoor=False)
    dg_root_in_frost_04 = area.room('dg_root_in_frost_04', name='Windroot Nursery', desc='Windroot grips a frost-split shelf with pale stems flattened by the prevailing gusts. Harvest tags mark mature clusters and newly divided crowns, leaving roots and seed heads in place so today’s useful cutting can be compared with next season’s return.', room_type='path', indoor=False)
    dg_careful_boundary_05 = area.room('dg_careful_boundary_05', name='Two-Cord Boundary', desc='A green cord protects a recovering seam while a blue Warden cord preserves enough width for litters and pack animals. The space between them has been adjusted several times, with both sets of initials retained wherever snow creep or new growth forced the compromise to move.', room_type='path', indoor=False)
    dg_guarded_stone_06 = area.room('dg_guarded_stone_06', name='Listening Frame Yard', desc='Wooden frames of different sizes stand on bare patches around an otherwise ordinary stone outcrop. Notes compare wind vibration, oreling contact, and frost without declaring one cause, and every frame can be lifted away without drilling into the rock beneath it.', room_type='path', indoor=False)
    dg_green_thread_07 = area.room('dg_green_thread_07', name='Lichen Return', desc='Squares once scraped for an old survey are filling slowly with silver and green lichen. Elun’s dated tracings show which patches recovered and which remained bare, making the cost of a small sample visible years after the answer it sought was forgotten.', room_type='path', indoor=False)
    dg_druid_hush_08 = area.room('dg_druid_hush_08', name='Quiet Watch', desc='A low blind faces a crossing used by orelings, goats, and patrols moving between exposed ridges. Separate tally strings keep each kind of passage distinct, and a basket of discarded guesses shows how often prints seen at dusk were corrected in morning light.', room_type='path', indoor=False)
    dg_root_in_frost_09 = area.room('dg_root_in_frost_09', name='Root-Bound Shelf', desc='Living roots lace a cracked shelf tightly enough to hold loose gravel above the route. Small woven guards keep boots off the newest growth, while gaps deliberately remain for meltwater and animals rather than turning preservation into a wall across the pass.', room_type='path', indoor=False)
    dg_careful_boundary_10 = area.room('dg_careful_boundary_10', name='Shared Survey Line', desc='Verdance stakes measure plant recovery on one side of the path and Warden stakes measure stone movement on the other. A joint slate records where those observations disagree, giving each watch a reason to return after weather changes instead of winning the argument once.', room_type='path', indoor=False)
    dg_guarded_stone_11 = area.room('dg_guarded_stone_11', name='Uncut Face', desc='Old rectangular scars stop abruptly at a dark, uncut face of mountain. Surviving marks identify the abandoned work as an Imperial survey but give no reason for its end; newer stewards monitor frost around the scars without reopening the unanswered excavation.', room_type='path', indoor=False)
    dg_green_thread_12 = area.room('dg_green_thread_12', name='Seed-Cord Crossing', desc='Braided green cords carry tiny paper sleeves of windroot and alpine-grass seed across a scraped slope. Each sleeve names its source patch and sowing date, allowing failures to be replanted from appropriate stock instead of hiding them beneath whatever grows fastest.', room_type='path', indoor=False)
    dg_druid_hush_13 = area.room('dg_druid_hush_13', name='Recovery Hush', desc='A shallow hollow shelters young growth where a fallen signal frame once tore through the soil. The broken fittings remain tagged beside the repair log, and the quiet watch records new insects and shoots as signs of recovery rather than proof that the damage never mattered.', room_type='path', indoor=False)
    dg_root_in_frost_14 = area.room('dg_root_in_frost_14', name='Skyward Root', desc='A thick windroot descends from a crack above the path, its exposed fibers twisting toward the first sky-bridge anchorage. Green and blue inspection tags share the same support peg but measure different concerns—new growth for Elun, stone strain for the runners who must cross ahead.', room_type='path', indoor=False)
    sk_sky_bridge = area.room('sk_sky_bridge', name='First Sky Bridge', desc='A narrow deck of linked stone slats crosses open air between two ironbound anchor towers. Skybridge Runner Maro checks the streamers before each crossing and records both the gusts he judged safe and the ones that made him wait; windcut eagles circle below the span.', room_type='path', indoor=False)
    sk_chain_shadow = area.room('sk_chain_shadow', name='Anchor Shadow', desc='The bridge’s main chain disappears into a cool recess where every link can be inspected out of the glare. Fresh ridgecat prints overlap the runner’s chalk marks near the outer anchor, and a caged lamp keeps the animal sign visible without claiming the recess from it.', room_type='path', indoor=False)
    sk_eagle_lane_03 = area.room('sk_eagle_lane_03', name='Eagle Lane', desc='Updrafts beside the bridge carry windcut eagles past at eye level, close enough for wingbeats to shake loose frost from the rail. Painted perch marks leave the favored stones clear, while dated notes track when nesting birds forced runners to shift their crossing rhythm.', room_type='path', indoor=False)
    sk_wind_rung_04 = area.room('sk_wind_rung_04', name='Wind-Vote Rung', desc='One bridge rung is fitted with ribbons at ankle, waist, and shoulder height. Their disagreement matters more than any single gust: Maro’s slate lists crossings delayed when upper air pulled one way and the deck-height current pulled another.', room_type='path', indoor=False)
    sk_wide_fall_05 = area.room('sk_wide_fall_05', name='Rescue Drop', desc='The chasm opens beneath a reinforced gap in the railing where a litter or safety line can be lowered without snagging on the deck. Rope lengths are marked by destination ledges, and a recent inspection note rejects one old anchor despite the reassuring paint still on it.', room_type='path', indoor=False)
    sk_sky_bridge_06 = area.room('sk_sky_bridge_06', name='Midspan Rest Cage', desc='A waist-high cage of woven chain gives stalled travelers a place to brace without turning around on the moving span. Scratched initials are paired with later crossing dates, showing that many frightened climbers returned by choice and crossed successfully with better weather or company.', room_type='path', indoor=False)
    sk_chain_shadow_07 = area.room('sk_chain_shadow_07', name='Sounding Chain', desc='Half-dwarf inspectors have hung small numbered hammers beside the suspension chain. Marks on the adjacent chart compare each link’s tone across cold, thaw, and heavy load, making a changed note grounds for inspection rather than an omen dressed up as certainty.', room_type='path', indoor=False)
    sk_eagle_lane_08 = area.room('sk_eagle_lane_08', name='Feather Gate', desc='Molted flight feathers gather in a mesh screen where the bridge passes between two rising drafts. Runners sort damaged feathers from clean seasonal molt before changing route warnings, and the discarded guesses remain tied below the current conclusion.', room_type='path', indoor=False)
    sk_wind_rung_09 = area.room('sk_wind_rung_09', name='Crosswind Rail', desc='The handrail bends inward at a place where side gusts strike without warning from the ravine. Repair plates bear the smiths’ names and load dates, while a runner’s tally records which pack shapes caught the wind so future crossings can redistribute cargo before committing.', room_type='path', indoor=False)
    sk_wide_fall_10 = area.room('sk_wide_fall_10', name='Litter Turn', desc='A stone platform interrupts the bridge long enough for a rescue litter to change bearers. Hooks are spaced for hands of different reach, and the duty board credits every carrier in a recent pack-animal recovery instead of only the runner who first spotted trouble.', room_type='path', indoor=False)
    sk_sky_bridge_11 = area.room('sk_sky_bridge_11', name='Second Span', desc='The second span climbs toward thinner air on shorter, stiffer chains. Its maintenance board tracks deck slats by quarry batch and replacement date, exposing whether repeated cracks come from stone, fitting, weather, or the loads the route is asked to bear.', room_type='path', indoor=False)
    sk_chain_shadow_12 = area.room('sk_chain_shadow_12', name='Claw-Shadow Anchorage', desc='A sheltered anchorage smells faintly of ridgecat musk, with tawny hair caught where the chain enters stone. Runners leave the inner route open and record each sighting, recognizing the animal’s established passage while keeping evidence ready if encounters begin threatening travelers.', room_type='path', indoor=False)
    sk_eagle_lane_13 = area.room('sk_eagle_lane_13', name="Runner's Pause", desc='A shallow bay lets runners watch the final eagle lane before stepping into it. Water, message tubes, and a slate of changing nest locations share the bench, giving speed a place to yield to observation without making hesitation a source of ridicule.', room_type='path', indoor=False)
    sk_wind_rung_14 = area.room('sk_wind_rung_14', name='Last Wind Rung', desc='The final stone rung reaches solid mountain beside three frayed streamers saved from previous seasons. Each is tagged with the gust pattern that ended its service, and a fresh line points toward the thin-air shelters where crossing reports, food, and recovery wait.', room_type='path', indoor=False)
    ts_thin_air_shelter = area.room('ts_thin_air_shelter', name='Thin-Air Shelter', desc='A roofed stone alcove holds a patrol pot, drying hooks, and shallow trays where bellcap mushrooms are checked before cooking. The supply board names who carried food up and who used it, with tomorrow’s shortages written larger than anyone’s claim to generosity.', room_type='path', indoor=False)
    ts_basin_pool = area.room('ts_basin_pool', name='Snowmelt Basin', desc='Clear meltwater gathers behind a low half-dwarf weir where snowmelt trout hold in the slower current. Catch marks distinguish kept fish from small or spawning fish returned, giving the supper tally a record of what the pool can continue to provide.', room_type='path', indoor=False)
    ts_warm_stone_03 = area.room('ts_warm_stone_03', name='Sun-Warm Bench', desc='A slab of dark stone captures afternoon sun beside a wall that blocks the prevailing wind. Bedroll outlines and a basket of windroot wraps show how patrols warm stiff hands here, while a dated temperature slate warns that cloud can take the comfort away quickly.', room_type='path', indoor=False)
    ts_breath_mark_04 = area.room('ts_breath_mark_04', name='Four-Breath Post', desc='Four carved rings guide resting climbers through a slow breathing count without turning discomfort into a contest. Chalk beside them records headache, nausea, shaking, and recovery times, so a companion can compare changing symptoms and choose descent before silence becomes danger.', room_type='path', indoor=False)
    ts_snowmelt_cup_05 = area.room('ts_snowmelt_cup_05', name='Trout Cup', desc='A round rock pool catches fish moving between two narrow snowmelt channels. Barbless hooks dry above a measuring board, and old catch notches have been planed away where heavy use once outpaced the returning trout.', room_type='path', indoor=False)
    ts_thin_shelter_06 = area.room('ts_thin_shelter_06', name='Blanket Loft', desc='Dry wool blankets fill a raised rack above a shelter narrow enough to hold warmth between a few bodies. Mending colors identify the Tremen households that repaired each tear, and damp bundles hang separately with the patrol expected to carry them down for washing.', room_type='path', indoor=False)
    ts_basin_pool_07 = area.room('ts_basin_pool_07', name='Nursery Basin', desc='Finger-length trout shelter among pebbles in a shallow side pool protected from the fastest meltwater. A low marker asks fishers to leave this basin alone, and seasonal counts remain posted so the request can expand or end with evidence rather than custom alone.', room_type='path', indoor=False)
    ts_warm_stone_08 = area.room('ts_warm_stone_08', name='Cookstone', desc='A broad sun-warmed stone supports a lidded patrol pot without open flame on the exposed shelf. Meal tallies pair servings with the route and weather faced next, letting cooks learn whether broth, trout, mushroom, or carried grain best sustained different crossings.', room_type='path', indoor=False)
    ts_breath_mark_09 = area.room('ts_breath_mark_09', name='Acclimation Board', desc='A sheltered board records arrival time, resting breath, and the point when each traveler felt ready to move. Some names reappear across many climbs with different waits, a public reminder that experience does not make the mountain or the body behave the same way twice.', room_type='path', indoor=False)
    ts_snowmelt_cup_10 = area.room('ts_snowmelt_cup_10', name='Clean-Water Cup', desc='Snowmelt runs through gravel and charcoal into a stone cup beneath a fitted cover. Test strips, boil notices, and replacement dates for the filter layers hang nearby, making safe water a maintained process rather than a gift assumed from clear ice.', room_type='path', indoor=False)
    ts_thin_shelter_11 = area.room('ts_thin_shelter_11', name='Boot-Repair Shelter', desc='Awls, waxed thread, sole nails, and drying forms line a small shelter whose floor is scarred by impatient repairs. A ledger matches borrowed tools to later replacements and records which fixes survived the descent, turning every damaged boot into instruction for the next pair.', room_type='path', indoor=False)
    ts_basin_pool_12 = area.room('ts_basin_pool_12', name='Overflow Pool', desc='Excess water from the upper basins settles here before spilling beneath the path. Covered jugs are rotated by date between shelter and patrol use, while a marked reserve remains untouched unless a storm or failed filter closes the ordinary supply.', room_type='path', indoor=False)
    ts_warm_stone_13 = area.room('ts_warm_stone_13', name='Night-Watch Bench', desc='A heat-darkened bench faces the shelter lamps and the high route beyond. Watch notes mix weather with meal counts, sleeping places, and quiet observations about who struggled or helped, giving the relief patrol a humane picture instead of a bare headcount.', room_type='path', indoor=False)
    ts_breath_mark_14 = area.room('ts_breath_mark_14', name='High-Route Decision', desc='The last shelter post compares the climb to the overlook with the long return toward Tremen. Tokens left by recent travelers record direction, departure time, and remaining supplies, while an open column invites those who changed their mind to make that choice useful to whoever follows.', room_type='path', indoor=False)
    ho_high_overlook = area.room('ho_high_overlook', name='High Overlook', desc='The route rises above the shelters onto a broad shelf where the Sky Bridges, bell line, cairns, and Tremen road can be seen as one worked passage. A half-dwarf orientation table names maintained places and travel times but leaves distant ridges unclaimed, inviting observation without pretending height supplies every answer.', room_type='path', indoor=False)
    ho_last_cairn = area.room('ho_last_cairn', name='Coldvein Cairn', desc='A cairn of ordinary gray stones surrounds a narrow coldvein exposure used for supervised samples. Cut faces are numbered against sealed comparison pieces, and the cairn’s rebuild log shows exactly what each gathering changed before the next survey permits more.', room_type='path', indoor=False)
    ho_far_bell_03 = area.room('ho_far_bell_03', name='Far-Bell Bench', desc='A stone bench faces the Storm Bells far below, where their motion can sometimes be seen before their notes arrive. Listeners record the gap beside wind direction and cloud cover, turning the delayed sound into another changing route observation rather than a fixed measure of distance.', room_type='path', indoor=False)
    ho_cloud_cut_04 = area.room('ho_cloud_cut_04', name='Cloud Window', desc='Two dark pinnacles divide the moving cloud into brief windows over separate valleys. Waxed sketch cards hang beneath a hood, each dated and corrected where a ridge, road, or settlement looked different after snow or shifting light.', room_type='path', indoor=False)
    ho_return_sight_05 = area.room('ho_return_sight_05', name='Tremen Sight', desc='The mountain city appears below as smoke threads, lift roofs, and warm points behind stone rather than a single distant landmark. Route markers align those signs with the safest descent, and messages tucked beneath them name meals, repairs, and people expected when travelers return.', room_type='path', indoor=False)
    ho_high_overlook_06 = area.room('ho_high_overlook_06', name='Passwork Panorama', desc='From this ledge, patrol stairs, bridge anchors, shelter roofs, and signal notches reveal the labor connecting one high place to another. An inspection map is layered by season, showing closed spans and moved boundaries alongside the current route instead of erasing the work that failed.', room_type='path', indoor=False)
    ho_last_cairn_07 = area.room('ho_last_cairn_07', name="Carriers' Cairn", desc='Small tokens honor the people who hauled bell bronze, bridge chain, blankets, seed, and clean water into the pass. New supply requests are wedged among the older names, keeping gratitude tied to unfinished work rather than sealing it safely in the past.', room_type='path', indoor=False)
    ho_far_bell_08 = area.room('ho_far_bell_08', name='Range-Bell Listening Post', desc='A cupped stone wall gathers faint bells from several directions when the wind allows. Their known call patterns are carved at the base, while blank grooves wait for signals that can be corroborated later instead of naming every distant sound too soon.', room_type='path', indoor=False)
    ho_cloud_cut_09 = area.room('ho_cloud_cut_09', name='Weather Table', desc='A flat slab carries movable markers for cloud banks, snow curtains, and visible sunbreaks across the known pass. Earlier arrangements have been copied onto thin slates below it, giving returning travelers a way to compare the present sky with storms that changed direction before.', room_type='path', indoor=False)
    ho_return_sight_10 = area.room('ho_return_sight_10', name='Homefire Count', desc='At dusk, sheltered lights appear one by one along Tremen’s upper face and the lower watch road. Patrol notes distinguish expected lamps from a missing or newly lit point, allowing the overlook to carry useful concern home without turning every darkness into alarm.', room_type='path', indoor=False)
    ho_high_overlook_11 = area.room('ho_high_overlook_11', name='Route Atlas Ledge', desc='Stone reliefs map the maintained high-pass route through texture: steps, chain, water, cairn, and shelter can be read by gloved hands. Replaceable clay inserts mark recent closures and repairs, so the atlas remains an accountable tool rather than an ancient object travelers are expected to trust.', room_type='path', indoor=False)
    ho_last_cairn_12 = area.room('ho_last_cairn_12', name='Last Survey Cairn', desc='The highest maintained survey cairn holds sighting tubes aimed at named landmarks within the traveled range. A sealed tube pointing beyond them is labeled unresolved after conflicting observations, preserving the question without converting uncertainty into secret proof.', room_type='path', indoor=False)
    ho_far_bell_13 = area.room('ho_far_bell_13', name='Distant Warning Line', desc='Thin air carries an occasional bell note from somewhere beyond the charted patrol circuit. Listeners log direction, pitch, weather, and whether anyone else heard it; the growing pages contain disagreements as often as matches and authorize no route into the unknown.', room_type='path', indoor=False)
    ho_cloud_cut_14 = area.room('ho_cloud_cut_14', name='Turning Sky', desc='The maintained path ends at a safe stone turn beneath a sky that opens toward unnamed mountains and moving cloud. No cairn or bridge claims a way onward; a return board instead asks what changed since the climb began, making the long view useful when carried back through the living pass.', room_type='path', indoor=False)

    # Local exits
    area.exit(ps_patrol_stair, ps_breathing_niche, 'east')
    area.exit(ps_breathing_niche, ps_patrol_stair, 'west')
    area.exit(ps_breathing_niche, ps_rope_bell_03, 'east')
    area.exit(ps_rope_bell_03, ps_breathing_niche, 'west')
    area.exit(ps_rope_bell_03, ps_old_boot_04, 'east')
    area.exit(ps_old_boot_04, ps_rope_bell_03, 'west')
    area.exit(ps_old_boot_04, ps_thin_air_05, 'east')
    area.exit(ps_thin_air_05, ps_old_boot_04, 'west')
    area.exit(ps_thin_air_05, ps_patrol_stair_06, 'east')
    area.exit(ps_patrol_stair_06, ps_thin_air_05, 'west')
    area.exit(ps_patrol_stair_06, ps_breath_niche_07, 'east')
    area.exit(ps_breath_niche_07, ps_patrol_stair_06, 'west')
    area.exit(ps_breath_niche_07, ps_rope_bell_08, 'east')
    area.exit(ps_rope_bell_08, ps_breath_niche_07, 'west')
    area.exit(ps_rope_bell_08, ps_old_boot_09, 'east')
    area.exit(ps_old_boot_09, ps_rope_bell_08, 'west')
    area.exit(ps_old_boot_09, ps_thin_air_10, 'east')
    area.exit(ps_thin_air_10, ps_old_boot_09, 'west')
    area.exit(ps_thin_air_10, ps_patrol_stair_11, 'east')
    area.exit(ps_patrol_stair_11, ps_thin_air_10, 'west')
    area.exit(ps_patrol_stair_11, ps_breath_niche_12, 'east')
    area.exit(ps_breath_niche_12, ps_patrol_stair_11, 'west')
    area.exit(ps_breath_niche_12, ps_rope_bell_13, 'east')
    area.exit(ps_rope_bell_13, ps_breath_niche_12, 'west')
    area.exit(ps_rope_bell_13, ps_old_boot_14, 'east')
    area.exit(ps_old_boot_14, ps_rope_bell_13, 'west')
    area.exit(sb_storm_bells, sb_frosted_clapper, 'east')
    area.exit(sb_frosted_clapper, sb_storm_bells, 'west')
    area.exit(sb_frosted_clapper, sb_weather_oath_03, 'east')
    area.exit(sb_weather_oath_03, sb_frosted_clapper, 'west')
    area.exit(sb_weather_oath_03, sb_ringing_ice_04, 'east')
    area.exit(sb_ringing_ice_04, sb_weather_oath_03, 'west')
    area.exit(sb_ringing_ice_04, sb_low_thunder_05, 'east')
    area.exit(sb_low_thunder_05, sb_ringing_ice_04, 'west')
    area.exit(sb_low_thunder_05, sb_storm_bell_06, 'east')
    area.exit(sb_storm_bell_06, sb_low_thunder_05, 'west')
    area.exit(sb_storm_bell_06, sb_frosted_clapper_07, 'east')
    area.exit(sb_frosted_clapper_07, sb_storm_bell_06, 'west')
    area.exit(sb_frosted_clapper_07, sb_weather_oath_08, 'east')
    area.exit(sb_weather_oath_08, sb_frosted_clapper_07, 'west')
    area.exit(sb_weather_oath_08, sb_ringing_ice_09, 'east')
    area.exit(sb_ringing_ice_09, sb_weather_oath_08, 'west')
    area.exit(sb_ringing_ice_09, sb_low_thunder_10, 'east')
    area.exit(sb_low_thunder_10, sb_ringing_ice_09, 'west')
    area.exit(sb_low_thunder_10, sb_storm_bell_11, 'east')
    area.exit(sb_storm_bell_11, sb_low_thunder_10, 'west')
    area.exit(sb_storm_bell_11, sb_frosted_clapper_12, 'east')
    area.exit(sb_frosted_clapper_12, sb_storm_bell_11, 'west')
    area.exit(sb_frosted_clapper_12, sb_weather_oath_13, 'east')
    area.exit(sb_weather_oath_13, sb_frosted_clapper_12, 'west')
    area.exit(sb_weather_oath_13, sb_ringing_ice_14, 'east')
    area.exit(sb_ringing_ice_14, sb_weather_oath_13, 'west')
    area.exit(ir_ice_shear_ridge, ir_goat_break, 'east')
    area.exit(ir_goat_break, ir_ice_shear_ridge, 'west')
    area.exit(ir_goat_break, ir_knife_wind_03, 'east')
    area.exit(ir_knife_wind_03, ir_goat_break, 'west')
    area.exit(ir_knife_wind_03, ir_blue_crack_04, 'east')
    area.exit(ir_blue_crack_04, ir_knife_wind_03, 'west')
    area.exit(ir_blue_crack_04, ir_snow_glare_05, 'east')
    area.exit(ir_snow_glare_05, ir_blue_crack_04, 'west')
    area.exit(ir_snow_glare_05, ir_ice_shear_06, 'east')
    area.exit(ir_ice_shear_06, ir_snow_glare_05, 'west')
    area.exit(ir_ice_shear_06, ir_goat_break_07, 'east')
    area.exit(ir_goat_break_07, ir_ice_shear_06, 'west')
    area.exit(ir_goat_break_07, ir_knife_wind_08, 'east')
    area.exit(ir_knife_wind_08, ir_goat_break_07, 'west')
    area.exit(ir_knife_wind_08, ir_blue_crack_09, 'east')
    area.exit(ir_blue_crack_09, ir_knife_wind_08, 'west')
    area.exit(ir_blue_crack_09, ir_snow_glare_10, 'east')
    area.exit(ir_snow_glare_10, ir_blue_crack_09, 'west')
    area.exit(ir_snow_glare_10, ir_ice_shear_11, 'east')
    area.exit(ir_ice_shear_11, ir_snow_glare_10, 'west')
    area.exit(ir_ice_shear_11, ir_goat_break_12, 'east')
    area.exit(ir_goat_break_12, ir_ice_shear_11, 'west')
    area.exit(ir_goat_break_12, ir_knife_wind_13, 'east')
    area.exit(ir_knife_wind_13, ir_goat_break_12, 'west')
    area.exit(ir_knife_wind_13, ir_blue_crack_14, 'east')
    area.exit(ir_blue_crack_14, ir_knife_wind_13, 'west')
    area.exit(wc_warden_cairn, wc_counting_slate, 'east')
    area.exit(wc_counting_slate, wc_warden_cairn, 'west')
    area.exit(wc_counting_slate, wc_signal_notch_03, 'east')
    area.exit(wc_signal_notch_03, wc_counting_slate, 'west')
    area.exit(wc_signal_notch_03, wc_lost_glove_04, 'east')
    area.exit(wc_lost_glove_04, wc_signal_notch_03, 'west')
    area.exit(wc_lost_glove_04, wc_patrol_debt_05, 'east')
    area.exit(wc_patrol_debt_05, wc_lost_glove_04, 'west')
    area.exit(wc_patrol_debt_05, wc_warden_cairn_06, 'east')
    area.exit(wc_warden_cairn_06, wc_patrol_debt_05, 'west')
    area.exit(wc_warden_cairn_06, wc_counting_slate_07, 'east')
    area.exit(wc_counting_slate_07, wc_warden_cairn_06, 'west')
    area.exit(wc_counting_slate_07, wc_signal_notch_08, 'east')
    area.exit(wc_signal_notch_08, wc_counting_slate_07, 'west')
    area.exit(wc_signal_notch_08, wc_lost_glove_09, 'east')
    area.exit(wc_lost_glove_09, wc_signal_notch_08, 'west')
    area.exit(wc_lost_glove_09, wc_patrol_debt_10, 'east')
    area.exit(wc_patrol_debt_10, wc_lost_glove_09, 'west')
    area.exit(wc_patrol_debt_10, wc_warden_cairn_11, 'east')
    area.exit(wc_warden_cairn_11, wc_patrol_debt_10, 'west')
    area.exit(wc_warden_cairn_11, wc_counting_slate_12, 'east')
    area.exit(wc_counting_slate_12, wc_warden_cairn_11, 'west')
    area.exit(wc_counting_slate_12, wc_signal_notch_13, 'east')
    area.exit(wc_signal_notch_13, wc_counting_slate_12, 'west')
    area.exit(wc_signal_notch_13, wc_lost_glove_14, 'east')
    area.exit(wc_lost_glove_14, wc_signal_notch_13, 'west')
    area.exit(dg_guarded_stone, dg_green_thread, 'east')
    area.exit(dg_green_thread, dg_guarded_stone, 'west')
    area.exit(dg_green_thread, dg_druid_hush_03, 'east')
    area.exit(dg_druid_hush_03, dg_green_thread, 'west')
    area.exit(dg_druid_hush_03, dg_root_in_frost_04, 'east')
    area.exit(dg_root_in_frost_04, dg_druid_hush_03, 'west')
    area.exit(dg_root_in_frost_04, dg_careful_boundary_05, 'east')
    area.exit(dg_careful_boundary_05, dg_root_in_frost_04, 'west')
    area.exit(dg_careful_boundary_05, dg_guarded_stone_06, 'east')
    area.exit(dg_guarded_stone_06, dg_careful_boundary_05, 'west')
    area.exit(dg_guarded_stone_06, dg_green_thread_07, 'east')
    area.exit(dg_green_thread_07, dg_guarded_stone_06, 'west')
    area.exit(dg_green_thread_07, dg_druid_hush_08, 'east')
    area.exit(dg_druid_hush_08, dg_green_thread_07, 'west')
    area.exit(dg_druid_hush_08, dg_root_in_frost_09, 'east')
    area.exit(dg_root_in_frost_09, dg_druid_hush_08, 'west')
    area.exit(dg_root_in_frost_09, dg_careful_boundary_10, 'east')
    area.exit(dg_careful_boundary_10, dg_root_in_frost_09, 'west')
    area.exit(dg_careful_boundary_10, dg_guarded_stone_11, 'east')
    area.exit(dg_guarded_stone_11, dg_careful_boundary_10, 'west')
    area.exit(dg_guarded_stone_11, dg_green_thread_12, 'east')
    area.exit(dg_green_thread_12, dg_guarded_stone_11, 'west')
    area.exit(dg_green_thread_12, dg_druid_hush_13, 'east')
    area.exit(dg_druid_hush_13, dg_green_thread_12, 'west')
    area.exit(dg_druid_hush_13, dg_root_in_frost_14, 'east')
    area.exit(dg_root_in_frost_14, dg_druid_hush_13, 'west')
    area.exit(sk_sky_bridge, sk_chain_shadow, 'east')
    area.exit(sk_chain_shadow, sk_sky_bridge, 'west')
    area.exit(sk_chain_shadow, sk_eagle_lane_03, 'east')
    area.exit(sk_eagle_lane_03, sk_chain_shadow, 'west')
    area.exit(sk_eagle_lane_03, sk_wind_rung_04, 'east')
    area.exit(sk_wind_rung_04, sk_eagle_lane_03, 'west')
    area.exit(sk_wind_rung_04, sk_wide_fall_05, 'east')
    area.exit(sk_wide_fall_05, sk_wind_rung_04, 'west')
    area.exit(sk_wide_fall_05, sk_sky_bridge_06, 'east')
    area.exit(sk_sky_bridge_06, sk_wide_fall_05, 'west')
    area.exit(sk_sky_bridge_06, sk_chain_shadow_07, 'east')
    area.exit(sk_chain_shadow_07, sk_sky_bridge_06, 'west')
    area.exit(sk_chain_shadow_07, sk_eagle_lane_08, 'east')
    area.exit(sk_eagle_lane_08, sk_chain_shadow_07, 'west')
    area.exit(sk_eagle_lane_08, sk_wind_rung_09, 'east')
    area.exit(sk_wind_rung_09, sk_eagle_lane_08, 'west')
    area.exit(sk_wind_rung_09, sk_wide_fall_10, 'east')
    area.exit(sk_wide_fall_10, sk_wind_rung_09, 'west')
    area.exit(sk_wide_fall_10, sk_sky_bridge_11, 'east')
    area.exit(sk_sky_bridge_11, sk_wide_fall_10, 'west')
    area.exit(sk_sky_bridge_11, sk_chain_shadow_12, 'east')
    area.exit(sk_chain_shadow_12, sk_sky_bridge_11, 'west')
    area.exit(sk_chain_shadow_12, sk_eagle_lane_13, 'east')
    area.exit(sk_eagle_lane_13, sk_chain_shadow_12, 'west')
    area.exit(sk_eagle_lane_13, sk_wind_rung_14, 'east')
    area.exit(sk_wind_rung_14, sk_eagle_lane_13, 'west')
    area.exit(ts_thin_air_shelter, ts_basin_pool, 'east')
    area.exit(ts_basin_pool, ts_thin_air_shelter, 'west')
    area.exit(ts_basin_pool, ts_warm_stone_03, 'east')
    area.exit(ts_warm_stone_03, ts_basin_pool, 'west')
    area.exit(ts_warm_stone_03, ts_breath_mark_04, 'east')
    area.exit(ts_breath_mark_04, ts_warm_stone_03, 'west')
    area.exit(ts_breath_mark_04, ts_snowmelt_cup_05, 'east')
    area.exit(ts_snowmelt_cup_05, ts_breath_mark_04, 'west')
    area.exit(ts_snowmelt_cup_05, ts_thin_shelter_06, 'east')
    area.exit(ts_thin_shelter_06, ts_snowmelt_cup_05, 'west')
    area.exit(ts_thin_shelter_06, ts_basin_pool_07, 'east')
    area.exit(ts_basin_pool_07, ts_thin_shelter_06, 'west')
    area.exit(ts_basin_pool_07, ts_warm_stone_08, 'east')
    area.exit(ts_warm_stone_08, ts_basin_pool_07, 'west')
    area.exit(ts_warm_stone_08, ts_breath_mark_09, 'east')
    area.exit(ts_breath_mark_09, ts_warm_stone_08, 'west')
    area.exit(ts_breath_mark_09, ts_snowmelt_cup_10, 'east')
    area.exit(ts_snowmelt_cup_10, ts_breath_mark_09, 'west')
    area.exit(ts_snowmelt_cup_10, ts_thin_shelter_11, 'east')
    area.exit(ts_thin_shelter_11, ts_snowmelt_cup_10, 'west')
    area.exit(ts_thin_shelter_11, ts_basin_pool_12, 'east')
    area.exit(ts_basin_pool_12, ts_thin_shelter_11, 'west')
    area.exit(ts_basin_pool_12, ts_warm_stone_13, 'east')
    area.exit(ts_warm_stone_13, ts_basin_pool_12, 'west')
    area.exit(ts_warm_stone_13, ts_breath_mark_14, 'east')
    area.exit(ts_breath_mark_14, ts_warm_stone_13, 'west')
    area.exit(ho_high_overlook, ho_last_cairn, 'east')
    area.exit(ho_last_cairn, ho_high_overlook, 'west')
    area.exit(ho_last_cairn, ho_far_bell_03, 'east')
    area.exit(ho_far_bell_03, ho_last_cairn, 'west')
    area.exit(ho_far_bell_03, ho_cloud_cut_04, 'east')
    area.exit(ho_cloud_cut_04, ho_far_bell_03, 'west')
    area.exit(ho_cloud_cut_04, ho_return_sight_05, 'east')
    area.exit(ho_return_sight_05, ho_cloud_cut_04, 'west')
    area.exit(ho_return_sight_05, ho_high_overlook_06, 'east')
    area.exit(ho_high_overlook_06, ho_return_sight_05, 'west')
    area.exit(ho_high_overlook_06, ho_last_cairn_07, 'east')
    area.exit(ho_last_cairn_07, ho_high_overlook_06, 'west')
    area.exit(ho_last_cairn_07, ho_far_bell_08, 'east')
    area.exit(ho_far_bell_08, ho_last_cairn_07, 'west')
    area.exit(ho_far_bell_08, ho_cloud_cut_09, 'east')
    area.exit(ho_cloud_cut_09, ho_far_bell_08, 'west')
    area.exit(ho_cloud_cut_09, ho_return_sight_10, 'east')
    area.exit(ho_return_sight_10, ho_cloud_cut_09, 'west')
    area.exit(ho_return_sight_10, ho_high_overlook_11, 'east')
    area.exit(ho_high_overlook_11, ho_return_sight_10, 'west')
    area.exit(ho_high_overlook_11, ho_last_cairn_12, 'east')
    area.exit(ho_last_cairn_12, ho_high_overlook_11, 'west')
    area.exit(ho_last_cairn_12, ho_far_bell_13, 'east')
    area.exit(ho_far_bell_13, ho_last_cairn_12, 'west')
    area.exit(ho_far_bell_13, ho_cloud_cut_14, 'east')
    area.exit(ho_cloud_cut_14, ho_far_bell_13, 'west')
    area.exit(ps_old_boot_14, sb_storm_bells, 'north')
    area.exit(sb_storm_bells, ps_old_boot_14, 'south')
    area.exit(sb_ringing_ice_14, ir_ice_shear_ridge, 'north')
    area.exit(ir_ice_shear_ridge, sb_ringing_ice_14, 'south')
    area.exit(ir_blue_crack_14, wc_warden_cairn, 'north')
    area.exit(wc_warden_cairn, ir_blue_crack_14, 'south')
    area.exit(wc_lost_glove_14, dg_guarded_stone, 'north')
    area.exit(dg_guarded_stone, wc_lost_glove_14, 'south')
    area.exit(dg_root_in_frost_14, sk_sky_bridge, 'north')
    area.exit(sk_sky_bridge, dg_root_in_frost_14, 'south')
    area.exit(sk_wind_rung_14, ts_thin_air_shelter, 'north')
    area.exit(ts_thin_air_shelter, sk_wind_rung_14, 'south')
    area.exit(ts_breath_mark_14, ho_high_overlook, 'north')
    area.exit(ho_high_overlook, ts_breath_mark_14, 'south')
    area.exit(ps_patrol_stair, 'tremen:hl_high_lift', 'down')

    # NPCs
    _high_warden = area.npc(ps_patrol_stair, 'npc_high_warden_thessa', name='High Warden Thessa', faction='wardens', dialogue={'greeting_tiers': {"neutral": 'Thessa checks your breathing before she asks why you came up.'}, 'topics': {'patrol': 'Count what moved, what changed, and what you were tempted to ignore.'}, 'base_hints': []})
    _storm_listener = area.npc(sb_storm_bells, 'npc_storm_listener_ava', name='Storm Listener Ava', faction='resonance', dialogue={'greeting_tiers': {"neutral": 'Ava times speech between bell notes and thunder mutters.'}, 'topics': {'bells': 'The bells warn. They do not command. People still choose.'}, 'base_hints': []})
    _druid_guard = area.npc(dg_guarded_stone, 'npc_druid_guard_elun', name='Druid Guard Elun', faction='verdance', dialogue={'greeting_tiers': {"neutral": 'Elun stands where root meets frost, polite enough to be heard and firm enough to be believed.'}, 'topics': {'stone': 'Some places are studied best by not stepping on them first.'}, 'base_hints': []})
    _sky_runner = area.npc(sk_sky_bridge, 'npc_skybridge_runner_maro', name='Skybridge Runner Maro', faction='wardens', dialogue={'greeting_tiers': {"neutral": 'Maro grins like fear is a tool he keeps sharp but sheathed.'}, 'topics': {'bridge': 'The trick is not bravery. The trick is knowing which gusts get a vote.'}, 'base_hints': []})

    # Quest item templates
    area.item('thp_patrol_count', key='high-pass patrol count', item_type='item', weight=0.5, rarity='normal', desc='A slate of tracks, bell timings, and stormgoat movements gathered from the high pass.', value=0, is_quest_item=True)
    area.item('thp_druid_note', key='guarded-stone note', item_type='item', weight=0.5, rarity='normal', desc='A folded note asking for restraint around a stone that too many factions want to measure first.', value=0, is_quest_item=True)

    # Quests
    area.quest(
        'thp_q_patrol_count',
        name='Count The Moving Weather',
        description='Thessa sends you along the patrol stair and cairns, making the high pass a lesson in observation before fighting becomes necessary.',
        quest_type='patrol',
        quest_giver='npc_high_warden_thessa',
        objectives=[{'type': 'visit', 'target': 'wc_warden_cairn', 'count': 1}, {'type': 'investigate', 'target': 'ir_ice_shear_ridge', 'count': 1}, {'type': 'deliver', 'target': 'npc_watch_captain_maela', 'count': 1, 'item_tag': 'thp_patrol_count'}],
        rewards=[{'action_type': 'give_scales', 'amount': 38}, {'action_type': 'modify_standing', 'faction_id': 'wardens', 'delta': 1800}],
        next_quest_id=None,
        prerequisite_quests=['tre_q_bell_weather'],
        can_share=True,
        consequence_small='Thessa moves your count into the city weather board, where it can warn the next patrol before they climb.',
    )
    area.quest(
        'thp_q_storm_bells',
        name='When Bells Disagree',
        description='Ava asks you to compare storm bells across exposed ridges, turning dangerous travel into a puzzle of timing and sound.',
        quest_type='investigation',
        quest_giver='npc_storm_listener_ava',
        objectives=[{'type': 'investigate', 'target': 'sb_storm_bells', 'count': 1}, {'type': 'investigate', 'target': 'sk_sky_bridge', 'count': 1}, {'type': 'talk_to', 'target': 'npc_storm_listener_ava', 'count': 1}],
        rewards=[{'action_type': 'give_scales', 'amount': 34}, {'action_type': 'give_skill_xp', 'skill_id': 'scholarship', 'count': 12}],
        next_quest_id=None,
        prerequisite_quests=[],
        can_share=True,
        consequence_small='Ava retunes one clapper by a finger width and credits your walk for catching the disagreement before the next storm.',
    )
    area.quest(
        'thp_q_guarded_stone',
        name='A Boundary Kept',
        description='Elun asks you to carry a restraint note to the Warden cairn and back, making faction tension playable as respect instead of a shouting match.',
        quest_type='delivery',
        quest_giver='npc_druid_guard_elun',
        objectives=[{'type': 'visit', 'target': 'dg_guarded_stone', 'count': 1}, {'type': 'deliver', 'target': 'wc_warden_cairn', 'count': 1, 'item_tag': 'thp_druid_note'}, {'type': 'talk_to', 'target': 'npc_high_warden_thessa', 'count': 1}],
        rewards=[{'action_type': 'give_scales', 'amount': 36}, {'action_type': 'modify_standing', 'faction_id': 'verdance', 'delta': 1800}],
        next_quest_id=None,
        prerequisite_quests=[],
        can_share=True,
        consequence_small='Elun leaves a visible cord boundary beside the guarded stone, trusting future visitors to see restraint before curiosity.',
    )
    area.quest(
        'thp_q_ridge_rescue',
        name='Hooves On The Wrong Side',
        description='Maro spots a stranded pack animal beyond ridgecat territory, giving the combat loop a rescue reason and a route across the sky bridge.',
        quest_type='rescue',
        quest_giver='npc_skybridge_runner_maro',
        objectives=[{'type': 'visit', 'target': 'sk_sky_bridge', 'count': 1}, {'type': 'kill', 'target': 'ridgecat', 'count': 3}, {'type': 'kill', 'target': 'stormgoat', 'count': 2}],
        rewards=[{'action_type': 'give_scales', 'amount': 42}, {'action_type': 'give_skill_xp', 'skill_id': 'survival', 'count': 12}],
        next_quest_id=None,
        prerequisite_quests=[],
        can_share=True,
        consequence_small='Maro ties a bright cloth at the bridge turn where the rescue began, turning a scary crossing into a story runners will retell usefully.',
    )
    area.quest(
        'thp_q_snowmelt_supper',
        name='Snowmelt Supper',
        description='Thessa points you to basin pools where fishing supports patrols, proving high-pass survival is not only blades and boots.',
        quest_type='gather',
        quest_giver='npc_high_warden_thessa',
        objectives=[{'type': 'visit', 'target': 'ts_basin_pool', 'count': 1}, {'type': 'gather', 'target': 'snowmelt_trout', 'count': 3}, {'type': 'deliver', 'target': 'npc_skybridge_runner_maro', 'count': 1, 'item_tag': 'snowmelt_trout'}],
        rewards=[{'action_type': 'give_scales', 'amount': 28}, {'action_type': 'give_skill_xp', 'skill_id': 'fishing', 'count': 12}],
        next_quest_id=None,
        prerequisite_quests=[],
        can_share=True,
        consequence_small='A patrol pot hangs at the thin-air shelter with your catch named as the reason no one skipped supper before the descent.',
    )

    # Spawns
    area.spawn(ir_ice_shear_ridge, 'stormgoat', count_min=1, count_max=2, respawn_minutes=14, respawn_variance=4)
    area.spawn(ir_goat_break, 'stormgoat', count_min=1, count_max=2, respawn_minutes=14, respawn_variance=4)
    area.spawn(ir_knife_wind_03, 'ridgecat', count_min=1, count_max=2, respawn_minutes=14, respawn_variance=4)
    area.spawn(wc_warden_cairn, 'windcut_eagle', count_min=1, count_max=2, respawn_minutes=14, respawn_variance=4)
    area.spawn(wc_signal_notch_03, 'ridgecat', count_min=1, count_max=2, respawn_minutes=14, respawn_variance=4)
    area.spawn(wc_patrol_debt_05, 'stormgoat', count_min=1, count_max=1, respawn_minutes=14, respawn_variance=4)
    area.spawn(dg_guarded_stone, 'stone_listening_frame', count_min=1, count_max=1, respawn_minutes=14, respawn_variance=4)
    area.spawn(dg_green_thread, 'loose_oreling', count_min=1, count_max=2, respawn_minutes=14, respawn_variance=4)
    area.spawn(dg_root_in_frost_04, 'loose_oreling', count_min=1, count_max=1, respawn_minutes=14, respawn_variance=4)
    area.spawn(sk_sky_bridge, 'windcut_eagle', count_min=1, count_max=2, respawn_minutes=14, respawn_variance=4)
    area.spawn(sk_eagle_lane_03, 'windcut_eagle', count_min=1, count_max=2, respawn_minutes=14, respawn_variance=4)
    area.spawn(sk_chain_shadow, 'ridgecat', count_min=1, count_max=1, respawn_minutes=14, respawn_variance=4)
    area.spawn(sb_storm_bells, 'stone_listening_frame', count_min=1, count_max=1, respawn_minutes=14, respawn_variance=4)

    # Gathering pools
    area.gathering_pool('ore', ['ir_blue_crack_04', 'dg_guarded_stone', 'ho_last_cairn'], ['coldvein_stone', 'resonance_shard'], max_active=3, respawn_minutes=12, respawn_variance=4, tier_floor=2, tier_ceiling=3)
    area.gathering_pool('herb', ['dg_root_in_frost_04', 'ts_warm_stone_03'], ['windroot'], max_active=3, respawn_minutes=12, respawn_variance=4, tier_floor=2, tier_ceiling=2)
    area.gathering_pool('forage', ['ts_thin_air_shelter', 'dg_green_thread'], ['bellcap_mushroom'], max_active=3, respawn_minutes=12, respawn_variance=4, tier_floor=2, tier_ceiling=2)
    area.gathering_pool('hide', ['ir_goat_break', 'sk_chain_shadow'], ['ridgecat_pelt'], max_active=3, respawn_minutes=12, respawn_variance=4, tier_floor=2, tier_ceiling=2)
    area.gathering_pool('fish', ['ts_basin_pool', 'ts_snowmelt_cup_05'], ['snowmelt_trout'], max_active=3, respawn_minutes=12, respawn_variance=4, tier_floor=2, tier_ceiling=2)

    # Lore fragments
    area.lore_fragment(
        'thp_lore_cairn_rescue',
        wc_warden_cairn,
        discovery_method='search',
        scholar_path='architecture',
        text='The cairn stones are arranged by rescues completed, not enemies slain, making Warden honor in the high pass quieter and more demanding than a banner.',
        insight_gain=1,
    )

    return area.build()
