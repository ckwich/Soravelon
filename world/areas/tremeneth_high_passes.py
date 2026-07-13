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
    ir_ice_shear_ridge = area.room('ir_ice_shear_ridge', name='Ice Shear Ridge', desc='Ice Shear Ridge belongs to the Ice-Shear Ridges, where hooves, claws, and boots all make territorial claims. The ice shear is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    ir_goat_break = area.room('ir_goat_break', name='Goat Break', desc='Goat Break belongs to the Ice-Shear Ridges, where hooves, claws, and boots all make territorial claims. The goat break is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    ir_knife_wind_03 = area.room('ir_knife_wind_03', name='Knife Wind 03', desc='Knife Wind 03 belongs to the Ice-Shear Ridges, where hooves, claws, and boots all make territorial claims. The knife wind is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    ir_blue_crack_04 = area.room('ir_blue_crack_04', name='Blue Crack 04', desc='Blue Crack 04 belongs to the Ice-Shear Ridges, where hooves, claws, and boots all make territorial claims. The blue crack is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    ir_snow_glare_05 = area.room('ir_snow_glare_05', name='Snow Glare 05', desc='Snow Glare 05 belongs to the Ice-Shear Ridges, where hooves, claws, and boots all make territorial claims. The snow glare is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    ir_ice_shear_06 = area.room('ir_ice_shear_06', name='Ice Shear 06', desc='Ice Shear 06 belongs to the Ice-Shear Ridges, where hooves, claws, and boots all make territorial claims. The ice shear is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    ir_goat_break_07 = area.room('ir_goat_break_07', name='Goat Break 07', desc='Goat Break 07 belongs to the Ice-Shear Ridges, where hooves, claws, and boots all make territorial claims. The goat break is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    ir_knife_wind_08 = area.room('ir_knife_wind_08', name='Knife Wind 08', desc='Knife Wind 08 belongs to the Ice-Shear Ridges, where hooves, claws, and boots all make territorial claims. The knife wind is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    ir_blue_crack_09 = area.room('ir_blue_crack_09', name='Blue Crack 09', desc='Blue Crack 09 belongs to the Ice-Shear Ridges, where hooves, claws, and boots all make territorial claims. The blue crack is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    ir_snow_glare_10 = area.room('ir_snow_glare_10', name='Snow Glare 10', desc='Snow Glare 10 belongs to the Ice-Shear Ridges, where hooves, claws, and boots all make territorial claims. The snow glare is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    ir_ice_shear_11 = area.room('ir_ice_shear_11', name='Ice Shear 11', desc='Ice Shear 11 belongs to the Ice-Shear Ridges, where hooves, claws, and boots all make territorial claims. The ice shear is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    ir_goat_break_12 = area.room('ir_goat_break_12', name='Goat Break 12', desc='Goat Break 12 belongs to the Ice-Shear Ridges, where hooves, claws, and boots all make territorial claims. The goat break is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    ir_knife_wind_13 = area.room('ir_knife_wind_13', name='Knife Wind 13', desc='Knife Wind 13 belongs to the Ice-Shear Ridges, where hooves, claws, and boots all make territorial claims. The knife wind is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    ir_blue_crack_14 = area.room('ir_blue_crack_14', name='Blue Crack 14', desc='Blue Crack 14 belongs to the Ice-Shear Ridges, where hooves, claws, and boots all make territorial claims. The blue crack is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    wc_warden_cairn = area.room('wc_warden_cairn', name='Warden Cairn', desc='Warden Cairn belongs to the Warden Cairns, where honor is measured in rescues and returned names. The warden cairn is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    wc_counting_slate = area.room('wc_counting_slate', name='Counting Slate', desc='Counting Slate belongs to the Warden Cairns, where honor is measured in rescues and returned names. The counting slate is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    wc_signal_notch_03 = area.room('wc_signal_notch_03', name='Signal Notch 03', desc='Signal Notch 03 belongs to the Warden Cairns, where honor is measured in rescues and returned names. The signal notch is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    wc_lost_glove_04 = area.room('wc_lost_glove_04', name='Lost Glove 04', desc='Lost Glove 04 belongs to the Warden Cairns, where honor is measured in rescues and returned names. The lost glove is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    wc_patrol_debt_05 = area.room('wc_patrol_debt_05', name='Patrol Debt 05', desc='Patrol Debt 05 belongs to the Warden Cairns, where honor is measured in rescues and returned names. The patrol debt is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    wc_warden_cairn_06 = area.room('wc_warden_cairn_06', name='Warden Cairn 06', desc='Warden Cairn 06 belongs to the Warden Cairns, where honor is measured in rescues and returned names. The warden cairn is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    wc_counting_slate_07 = area.room('wc_counting_slate_07', name='Counting Slate 07', desc='Counting Slate 07 belongs to the Warden Cairns, where honor is measured in rescues and returned names. The counting slate is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    wc_signal_notch_08 = area.room('wc_signal_notch_08', name='Signal Notch 08', desc='Signal Notch 08 belongs to the Warden Cairns, where honor is measured in rescues and returned names. The signal notch is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    wc_lost_glove_09 = area.room('wc_lost_glove_09', name='Lost Glove 09', desc='Lost Glove 09 belongs to the Warden Cairns, where honor is measured in rescues and returned names. The lost glove is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    wc_patrol_debt_10 = area.room('wc_patrol_debt_10', name='Patrol Debt 10', desc='Patrol Debt 10 belongs to the Warden Cairns, where honor is measured in rescues and returned names. The patrol debt is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    wc_warden_cairn_11 = area.room('wc_warden_cairn_11', name='Warden Cairn 11', desc='Warden Cairn 11 belongs to the Warden Cairns, where honor is measured in rescues and returned names. The warden cairn is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    wc_counting_slate_12 = area.room('wc_counting_slate_12', name='Counting Slate 12', desc='Counting Slate 12 belongs to the Warden Cairns, where honor is measured in rescues and returned names. The counting slate is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    wc_signal_notch_13 = area.room('wc_signal_notch_13', name='Signal Notch 13', desc='Signal Notch 13 belongs to the Warden Cairns, where honor is measured in rescues and returned names. The signal notch is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    wc_lost_glove_14 = area.room('wc_lost_glove_14', name='Lost Glove 14', desc='Lost Glove 14 belongs to the Warden Cairns, where honor is measured in rescues and returned names. The lost glove is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    dg_guarded_stone = area.room('dg_guarded_stone', name='Guarded Stone', desc='Guarded Stone belongs to the Druid-Guarded Stone, where Druid caution and Warden duty both have understandable stakes. The guarded stone is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    dg_green_thread = area.room('dg_green_thread', name='Green Thread', desc='Green Thread belongs to the Druid-Guarded Stone, where Druid caution and Warden duty both have understandable stakes. The green thread is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    dg_druid_hush_03 = area.room('dg_druid_hush_03', name='Druid Hush 03', desc='Druid Hush 03 belongs to the Druid-Guarded Stone, where Druid caution and Warden duty both have understandable stakes. The Druid hush is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    dg_root_in_frost_04 = area.room('dg_root_in_frost_04', name='Root In Frost 04', desc='Root In Frost 04 belongs to the Druid-Guarded Stone, where Druid caution and Warden duty both have understandable stakes. The root in frost is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    dg_careful_boundary_05 = area.room('dg_careful_boundary_05', name='Careful Boundary 05', desc='Careful Boundary 05 belongs to the Druid-Guarded Stone, where Druid caution and Warden duty both have understandable stakes. The careful boundary is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    dg_guarded_stone_06 = area.room('dg_guarded_stone_06', name='Guarded Stone 06', desc='Guarded Stone 06 belongs to the Druid-Guarded Stone, where Druid caution and Warden duty both have understandable stakes. The guarded stone is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    dg_green_thread_07 = area.room('dg_green_thread_07', name='Green Thread 07', desc='Green Thread 07 belongs to the Druid-Guarded Stone, where Druid caution and Warden duty both have understandable stakes. The green thread is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    dg_druid_hush_08 = area.room('dg_druid_hush_08', name='Druid Hush 08', desc='Druid Hush 08 belongs to the Druid-Guarded Stone, where Druid caution and Warden duty both have understandable stakes. The Druid hush is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    dg_root_in_frost_09 = area.room('dg_root_in_frost_09', name='Root In Frost 09', desc='Root In Frost 09 belongs to the Druid-Guarded Stone, where Druid caution and Warden duty both have understandable stakes. The root in frost is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    dg_careful_boundary_10 = area.room('dg_careful_boundary_10', name='Careful Boundary 10', desc='Careful Boundary 10 belongs to the Druid-Guarded Stone, where Druid caution and Warden duty both have understandable stakes. The careful boundary is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    dg_guarded_stone_11 = area.room('dg_guarded_stone_11', name='Guarded Stone 11', desc='Guarded Stone 11 belongs to the Druid-Guarded Stone, where Druid caution and Warden duty both have understandable stakes. The guarded stone is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    dg_green_thread_12 = area.room('dg_green_thread_12', name='Green Thread 12', desc='Green Thread 12 belongs to the Druid-Guarded Stone, where Druid caution and Warden duty both have understandable stakes. The green thread is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    dg_druid_hush_13 = area.room('dg_druid_hush_13', name='Druid Hush 13', desc='Druid Hush 13 belongs to the Druid-Guarded Stone, where Druid caution and Warden duty both have understandable stakes. The Druid hush is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    dg_root_in_frost_14 = area.room('dg_root_in_frost_14', name='Root In Frost 14', desc='Root In Frost 14 belongs to the Druid-Guarded Stone, where Druid caution and Warden duty both have understandable stakes. The root in frost is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    sk_sky_bridge = area.room('sk_sky_bridge', name='Sky Bridge', desc='Sky Bridge belongs to the Sky Bridges, where crossing open air is thrilling because it is useful and dangerous. The sky bridge is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    sk_chain_shadow = area.room('sk_chain_shadow', name='Chain Shadow', desc='Chain Shadow belongs to the Sky Bridges, where crossing open air is thrilling because it is useful and dangerous. The chain shadow is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    sk_eagle_lane_03 = area.room('sk_eagle_lane_03', name='Eagle Lane 03', desc='Eagle Lane 03 belongs to the Sky Bridges, where crossing open air is thrilling because it is useful and dangerous. The eagle lane is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    sk_wind_rung_04 = area.room('sk_wind_rung_04', name='Wind Rung 04', desc='Wind Rung 04 belongs to the Sky Bridges, where crossing open air is thrilling because it is useful and dangerous. The wind rung is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    sk_wide_fall_05 = area.room('sk_wide_fall_05', name='Wide Fall 05', desc='Wide Fall 05 belongs to the Sky Bridges, where crossing open air is thrilling because it is useful and dangerous. The wide fall is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    sk_sky_bridge_06 = area.room('sk_sky_bridge_06', name='Sky Bridge 06', desc='Sky Bridge 06 belongs to the Sky Bridges, where crossing open air is thrilling because it is useful and dangerous. The sky bridge is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    sk_chain_shadow_07 = area.room('sk_chain_shadow_07', name='Chain Shadow 07', desc='Chain Shadow 07 belongs to the Sky Bridges, where crossing open air is thrilling because it is useful and dangerous. The chain shadow is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    sk_eagle_lane_08 = area.room('sk_eagle_lane_08', name='Eagle Lane 08', desc='Eagle Lane 08 belongs to the Sky Bridges, where crossing open air is thrilling because it is useful and dangerous. The eagle lane is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    sk_wind_rung_09 = area.room('sk_wind_rung_09', name='Wind Rung 09', desc='Wind Rung 09 belongs to the Sky Bridges, where crossing open air is thrilling because it is useful and dangerous. The wind rung is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    sk_wide_fall_10 = area.room('sk_wide_fall_10', name='Wide Fall 10', desc='Wide Fall 10 belongs to the Sky Bridges, where crossing open air is thrilling because it is useful and dangerous. The wide fall is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    sk_sky_bridge_11 = area.room('sk_sky_bridge_11', name='Sky Bridge 11', desc='Sky Bridge 11 belongs to the Sky Bridges, where crossing open air is thrilling because it is useful and dangerous. The sky bridge is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    sk_chain_shadow_12 = area.room('sk_chain_shadow_12', name='Chain Shadow 12', desc='Chain Shadow 12 belongs to the Sky Bridges, where crossing open air is thrilling because it is useful and dangerous. The chain shadow is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    sk_eagle_lane_13 = area.room('sk_eagle_lane_13', name='Eagle Lane 13', desc='Eagle Lane 13 belongs to the Sky Bridges, where crossing open air is thrilling because it is useful and dangerous. The eagle lane is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    sk_wind_rung_14 = area.room('sk_wind_rung_14', name='Wind Rung 14', desc='Wind Rung 14 belongs to the Sky Bridges, where crossing open air is thrilling because it is useful and dangerous. The wind rung is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    ts_thin_air_shelter = area.room('ts_thin_air_shelter', name='Thin Air Shelter', desc='Thin Air Shelter belongs to the Thin-Air Shelters, where rest, food, and fishing are part of survival play. The thin shelter is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    ts_basin_pool = area.room('ts_basin_pool', name='Basin Pool', desc='Basin Pool belongs to the Thin-Air Shelters, where rest, food, and fishing are part of survival play. The basin pool is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    ts_warm_stone_03 = area.room('ts_warm_stone_03', name='Warm Stone 03', desc='Warm Stone 03 belongs to the Thin-Air Shelters, where rest, food, and fishing are part of survival play. The warm stone is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    ts_breath_mark_04 = area.room('ts_breath_mark_04', name='Breath Mark 04', desc='Breath Mark 04 belongs to the Thin-Air Shelters, where rest, food, and fishing are part of survival play. The breath mark is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    ts_snowmelt_cup_05 = area.room('ts_snowmelt_cup_05', name='Snowmelt Cup 05', desc='Snowmelt Cup 05 belongs to the Thin-Air Shelters, where rest, food, and fishing are part of survival play. The snowmelt cup is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    ts_thin_shelter_06 = area.room('ts_thin_shelter_06', name='Thin Shelter 06', desc='Thin Shelter 06 belongs to the Thin-Air Shelters, where rest, food, and fishing are part of survival play. The thin shelter is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    ts_basin_pool_07 = area.room('ts_basin_pool_07', name='Basin Pool 07', desc='Basin Pool 07 belongs to the Thin-Air Shelters, where rest, food, and fishing are part of survival play. The basin pool is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    ts_warm_stone_08 = area.room('ts_warm_stone_08', name='Warm Stone 08', desc='Warm Stone 08 belongs to the Thin-Air Shelters, where rest, food, and fishing are part of survival play. The warm stone is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    ts_breath_mark_09 = area.room('ts_breath_mark_09', name='Breath Mark 09', desc='Breath Mark 09 belongs to the Thin-Air Shelters, where rest, food, and fishing are part of survival play. The breath mark is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    ts_snowmelt_cup_10 = area.room('ts_snowmelt_cup_10', name='Snowmelt Cup 10', desc='Snowmelt Cup 10 belongs to the Thin-Air Shelters, where rest, food, and fishing are part of survival play. The snowmelt cup is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    ts_thin_shelter_11 = area.room('ts_thin_shelter_11', name='Thin Shelter 11', desc='Thin Shelter 11 belongs to the Thin-Air Shelters, where rest, food, and fishing are part of survival play. The thin shelter is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    ts_basin_pool_12 = area.room('ts_basin_pool_12', name='Basin Pool 12', desc='Basin Pool 12 belongs to the Thin-Air Shelters, where rest, food, and fishing are part of survival play. The basin pool is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    ts_warm_stone_13 = area.room('ts_warm_stone_13', name='Warm Stone 13', desc='Warm Stone 13 belongs to the Thin-Air Shelters, where rest, food, and fishing are part of survival play. The warm stone is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    ts_breath_mark_14 = area.room('ts_breath_mark_14', name='Breath Mark 14', desc='Breath Mark 14 belongs to the Thin-Air Shelters, where rest, food, and fishing are part of survival play. The breath mark is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    ho_high_overlook = area.room('ho_high_overlook', name='High Overlook', desc='High Overlook belongs to the High Overlook, where exploration rewards players with context for the whole pack. The high overlook is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    ho_last_cairn = area.room('ho_last_cairn', name='Last Cairn', desc='Last Cairn belongs to the High Overlook, where exploration rewards players with context for the whole pack. The last cairn is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    ho_far_bell_03 = area.room('ho_far_bell_03', name='Far Bell 03', desc='Far Bell 03 belongs to the High Overlook, where exploration rewards players with context for the whole pack. The far bell is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    ho_cloud_cut_04 = area.room('ho_cloud_cut_04', name='Cloud Cut 04', desc='Cloud Cut 04 belongs to the High Overlook, where exploration rewards players with context for the whole pack. The cloud cut is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    ho_return_sight_05 = area.room('ho_return_sight_05', name='Return Sight 05', desc='Return Sight 05 belongs to the High Overlook, where exploration rewards players with context for the whole pack. The return sight is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    ho_high_overlook_06 = area.room('ho_high_overlook_06', name='High Overlook 06', desc='High Overlook 06 belongs to the High Overlook, where exploration rewards players with context for the whole pack. The high overlook is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    ho_last_cairn_07 = area.room('ho_last_cairn_07', name='Last Cairn 07', desc='Last Cairn 07 belongs to the High Overlook, where exploration rewards players with context for the whole pack. The last cairn is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    ho_far_bell_08 = area.room('ho_far_bell_08', name='Far Bell 08', desc='Far Bell 08 belongs to the High Overlook, where exploration rewards players with context for the whole pack. The far bell is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    ho_cloud_cut_09 = area.room('ho_cloud_cut_09', name='Cloud Cut 09', desc='Cloud Cut 09 belongs to the High Overlook, where exploration rewards players with context for the whole pack. The cloud cut is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    ho_return_sight_10 = area.room('ho_return_sight_10', name='Return Sight 10', desc='Return Sight 10 belongs to the High Overlook, where exploration rewards players with context for the whole pack. The return sight is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    ho_high_overlook_11 = area.room('ho_high_overlook_11', name='High Overlook 11', desc='High Overlook 11 belongs to the High Overlook, where exploration rewards players with context for the whole pack. The high overlook is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    ho_last_cairn_12 = area.room('ho_last_cairn_12', name='Last Cairn 12', desc='Last Cairn 12 belongs to the High Overlook, where exploration rewards players with context for the whole pack. The last cairn is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    ho_far_bell_13 = area.room('ho_far_bell_13', name='Far Bell 13', desc='Far Bell 13 belongs to the High Overlook, where exploration rewards players with context for the whole pack. The far bell is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    ho_cloud_cut_14 = area.room('ho_cloud_cut_14', name='Cloud Cut 14', desc='Cloud Cut 14 belongs to the High Overlook, where exploration rewards players with context for the whole pack. The cloud cut is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)

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
