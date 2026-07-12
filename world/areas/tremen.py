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
        faction_presence=['warden', 'ironblood', 'resonance', 'verdance', 'western_arcana'],
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
    gt_gate_teeth = area.room('gt_gate_teeth', name='Gate Teeth', desc='Gate Teeth belongs to the Gate Teeth, where arrival bells teach guests to pause before taking shelter. The arrival bell is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    gt_guest_bell_arch = area.room('gt_guest_bell_arch', name='Guest Bell Arch', desc='Guest Bell Arch belongs to the Gate Teeth, where arrival bells teach guests to pause before taking shelter. The guest chalk is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    gt_lantern_registry = area.room('gt_lantern_registry', name='Lantern Registry', desc='Lantern Registry belongs to the Gate Teeth, where arrival bells teach guests to pause before taking shelter. The warden eye is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    gt_lower_gate = area.room('gt_lower_gate', name='Lower Gate', desc='Lower Gate belongs to the Gate Teeth, where arrival bells teach guests to pause before taking shelter. The road debt is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    gt_old_teeth_05 = area.room('gt_old_teeth_05', name='Old Teeth 05', desc='Old Teeth 05 belongs to the Gate Teeth, where arrival bells teach guests to pause before taking shelter. The old teeth is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    gt_arrival_bell_06 = area.room('gt_arrival_bell_06', name='Arrival Bell 06', desc='Arrival Bell 06 belongs to the Gate Teeth, where arrival bells teach guests to pause before taking shelter. The arrival bell is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    gt_guest_chalk_07 = area.room('gt_guest_chalk_07', name='Guest Chalk 07', desc='Guest Chalk 07 belongs to the Gate Teeth, where arrival bells teach guests to pause before taking shelter. The guest chalk is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    gt_warden_eye_08 = area.room('gt_warden_eye_08', name='Warden Eye 08', desc='Warden Eye 08 belongs to the Gate Teeth, where arrival bells teach guests to pause before taking shelter. The warden eye is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    gt_road_debt_09 = area.room('gt_road_debt_09', name='Road Debt 09', desc='Road Debt 09 belongs to the Gate Teeth, where arrival bells teach guests to pause before taking shelter. The road debt is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    gt_old_teeth_10 = area.room('gt_old_teeth_10', name='Old Teeth 10', desc='Old Teeth 10 belongs to the Gate Teeth, where arrival bells teach guests to pause before taking shelter. The old teeth is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    gt_arrival_bell_11 = area.room('gt_arrival_bell_11', name='Arrival Bell 11', desc='Arrival Bell 11 belongs to the Gate Teeth, where arrival bells teach guests to pause before taking shelter. The arrival bell is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    gt_guest_chalk_12 = area.room('gt_guest_chalk_12', name='Guest Chalk 12', desc='Guest Chalk 12 belongs to the Gate Teeth, where arrival bells teach guests to pause before taking shelter. The guest chalk is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    gt_warden_eye_13 = area.room('gt_warden_eye_13', name='Warden Eye 13', desc='Warden Eye 13 belongs to the Gate Teeth, where arrival bells teach guests to pause before taking shelter. The warden eye is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    gt_road_debt_14 = area.room('gt_road_debt_14', name='Road Debt 14', desc='Road Debt 14 belongs to the Gate Teeth, where arrival bells teach guests to pause before taking shelter. The road debt is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    bm_bellcut_market = area.room('bm_bellcut_market', name='Bellcut Market', desc='Bellcut Market belongs to Bellcut Market, where trade is measured against weather, roads, and responsibility. The bellcut stall is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    bm_scale_weighing_arch = area.room('bm_scale_weighing_arch', name='Scale Weighing Arch', desc='Scale Weighing Arch belongs to Bellcut Market, where trade is measured against weather, roads, and responsibility. The weighted scale is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    bm_rope_bazaar = area.room('bm_rope_bazaar', name='Rope Bazaar', desc='Rope Bazaar belongs to Bellcut Market, where trade is measured against weather, roads, and responsibility. The route gossip is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    bm_warm_bread_04 = area.room('bm_warm_bread_04', name='Warm Bread 04', desc='Warm Bread 04 belongs to Bellcut Market, where trade is measured against weather, roads, and responsibility. The warm bread is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    bm_repair_cord_05 = area.room('bm_repair_cord_05', name='Repair Cord 05', desc='Repair Cord 05 belongs to Bellcut Market, where trade is measured against weather, roads, and responsibility. The repair cord is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    bm_bellcut_stall_06 = area.room('bm_bellcut_stall_06', name='Bellcut Stall 06', desc='Bellcut Stall 06 belongs to Bellcut Market, where trade is measured against weather, roads, and responsibility. The bellcut stall is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    bm_weighted_scale_07 = area.room('bm_weighted_scale_07', name='Weighted Scale 07', desc='Weighted Scale 07 belongs to Bellcut Market, where trade is measured against weather, roads, and responsibility. The weighted scale is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    bm_route_gossip_08 = area.room('bm_route_gossip_08', name='Route Gossip 08', desc='Route Gossip 08 belongs to Bellcut Market, where trade is measured against weather, roads, and responsibility. The route gossip is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    bm_warm_bread_09 = area.room('bm_warm_bread_09', name='Warm Bread 09', desc='Warm Bread 09 belongs to Bellcut Market, where trade is measured against weather, roads, and responsibility. The warm bread is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    bm_repair_cord_10 = area.room('bm_repair_cord_10', name='Repair Cord 10', desc='Repair Cord 10 belongs to Bellcut Market, where trade is measured against weather, roads, and responsibility. The repair cord is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    bm_bellcut_stall_11 = area.room('bm_bellcut_stall_11', name='Bellcut Stall 11', desc='Bellcut Stall 11 belongs to Bellcut Market, where trade is measured against weather, roads, and responsibility. The bellcut stall is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    bm_weighted_scale_12 = area.room('bm_weighted_scale_12', name='Weighted Scale 12', desc='Weighted Scale 12 belongs to Bellcut Market, where trade is measured against weather, roads, and responsibility. The weighted scale is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    bm_route_gossip_13 = area.room('bm_route_gossip_13', name='Route Gossip 13', desc='Route Gossip 13 belongs to Bellcut Market, where trade is measured against weather, roads, and responsibility. The route gossip is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    bm_warm_bread_14 = area.room('bm_warm_bread_14', name='Warm Bread 14', desc='Warm Bread 14 belongs to Bellcut Market, where trade is measured against weather, roads, and responsibility. The warm bread is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    fh_advanced_forge = area.room('fh_advanced_forge', name='Advanced Forge', desc='Advanced Forge belongs to Forgeheart, where advanced craft is treated as civic discipline rather than vanity. The blue coals is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='building', indoor=True)
    fh_mine_lift = area.room('fh_mine_lift', name='Mine Lift', desc='Mine Lift belongs to Forgeheart, where advanced craft is treated as civic discipline rather than vanity. The pressure gauge is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='building', indoor=True)
    fh_bellows_walk = area.room('fh_bellows_walk', name='Bellows Walk', desc='Bellows Walk belongs to Forgeheart, where advanced craft is treated as civic discipline rather than vanity. The annealed rail is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='building', indoor=True)
    fh_apprentice_rhythm_04 = area.room('fh_apprentice_rhythm_04', name='Apprentice Rhythm 04', desc='Apprentice Rhythm 04 belongs to Forgeheart, where advanced craft is treated as civic discipline rather than vanity. The apprentice rhythm is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='building', indoor=True)
    fh_ore_tithe_05 = area.room('fh_ore_tithe_05', name='Ore Tithe 05', desc='Ore Tithe 05 belongs to Forgeheart, where advanced craft is treated as civic discipline rather than vanity. The ore tithe is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='building', indoor=True)
    fh_blue_coals_06 = area.room('fh_blue_coals_06', name='Blue Coals 06', desc='Blue Coals 06 belongs to Forgeheart, where advanced craft is treated as civic discipline rather than vanity. The blue coals is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='building', indoor=True)
    fh_pressure_gauge_07 = area.room('fh_pressure_gauge_07', name='Pressure Gauge 07', desc='Pressure Gauge 07 belongs to Forgeheart, where advanced craft is treated as civic discipline rather than vanity. The pressure gauge is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='building', indoor=True)
    fh_annealed_rail_08 = area.room('fh_annealed_rail_08', name='Annealed Rail 08', desc='Annealed Rail 08 belongs to Forgeheart, where advanced craft is treated as civic discipline rather than vanity. The annealed rail is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='building', indoor=True)
    fh_apprentice_rhythm_09 = area.room('fh_apprentice_rhythm_09', name='Apprentice Rhythm 09', desc='Apprentice Rhythm 09 belongs to Forgeheart, where advanced craft is treated as civic discipline rather than vanity. The apprentice rhythm is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='building', indoor=True)
    fh_ore_tithe_10 = area.room('fh_ore_tithe_10', name='Ore Tithe 10', desc='Ore Tithe 10 belongs to Forgeheart, where advanced craft is treated as civic discipline rather than vanity. The ore tithe is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='building', indoor=True)
    fh_blue_coals_11 = area.room('fh_blue_coals_11', name='Blue Coals 11', desc='Blue Coals 11 belongs to Forgeheart, where advanced craft is treated as civic discipline rather than vanity. The blue coals is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='building', indoor=True)
    fh_pressure_gauge_12 = area.room('fh_pressure_gauge_12', name='Pressure Gauge 12', desc='Pressure Gauge 12 belongs to Forgeheart, where advanced craft is treated as civic discipline rather than vanity. The pressure gauge is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='building', indoor=True)
    fh_annealed_rail_13 = area.room('fh_annealed_rail_13', name='Annealed Rail 13', desc='Annealed Rail 13 belongs to Forgeheart, where advanced craft is treated as civic discipline rather than vanity. The annealed rail is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='building', indoor=True)
    fh_apprentice_rhythm_14 = area.room('fh_apprentice_rhythm_14', name='Apprentice Rhythm 14', desc='Apprentice Rhythm 14 belongs to Forgeheart, where advanced craft is treated as civic discipline rather than vanity. The apprentice rhythm is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='building', indoor=True)
    wh_watch_muster = area.room('wh_watch_muster', name='Watch Muster', desc='Watch Muster belongs to the Watch Houses, where combat practice supports rescue, patrols, and accurate reports. The patrol slate is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='building', indoor=True)
    wh_sparring_ring = area.room('wh_sparring_ring', name='Sparring Ring', desc='Sparring Ring belongs to the Watch Houses, where combat practice supports rescue, patrols, and accurate reports. The safe practice is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='building', indoor=True)
    wh_weather_board = area.room('wh_weather_board', name='Weather Board', desc='Weather Board belongs to the Watch Houses, where combat practice supports rescue, patrols, and accurate reports. The bell rope is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='building', indoor=True)
    wh_snow_tally_04 = area.room('wh_snow_tally_04', name='Snow Tally 04', desc='Snow Tally 04 belongs to the Watch Houses, where combat practice supports rescue, patrols, and accurate reports. The snow tally is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='building', indoor=True)
    wh_ridge_lesson_05 = area.room('wh_ridge_lesson_05', name='Ridge Lesson 05', desc='Ridge Lesson 05 belongs to the Watch Houses, where combat practice supports rescue, patrols, and accurate reports. The ridge lesson is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='building', indoor=True)
    wh_patrol_slate_06 = area.room('wh_patrol_slate_06', name='Patrol Slate 06', desc='Patrol Slate 06 belongs to the Watch Houses, where combat practice supports rescue, patrols, and accurate reports. The patrol slate is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='building', indoor=True)
    wh_safe_practice_07 = area.room('wh_safe_practice_07', name='Safe Practice 07', desc='Safe Practice 07 belongs to the Watch Houses, where combat practice supports rescue, patrols, and accurate reports. The safe practice is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='building', indoor=True)
    wh_bell_rope_08 = area.room('wh_bell_rope_08', name='Bell Rope 08', desc='Bell Rope 08 belongs to the Watch Houses, where combat practice supports rescue, patrols, and accurate reports. The bell rope is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='building', indoor=True)
    wh_snow_tally_09 = area.room('wh_snow_tally_09', name='Snow Tally 09', desc='Snow Tally 09 belongs to the Watch Houses, where combat practice supports rescue, patrols, and accurate reports. The snow tally is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='building', indoor=True)
    wh_ridge_lesson_10 = area.room('wh_ridge_lesson_10', name='Ridge Lesson 10', desc='Ridge Lesson 10 belongs to the Watch Houses, where combat practice supports rescue, patrols, and accurate reports. The ridge lesson is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='building', indoor=True)
    wh_patrol_slate_11 = area.room('wh_patrol_slate_11', name='Patrol Slate 11', desc='Patrol Slate 11 belongs to the Watch Houses, where combat practice supports rescue, patrols, and accurate reports. The patrol slate is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='building', indoor=True)
    wh_safe_practice_12 = area.room('wh_safe_practice_12', name='Safe Practice 12', desc='Safe Practice 12 belongs to the Watch Houses, where combat practice supports rescue, patrols, and accurate reports. The safe practice is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='building', indoor=True)
    wh_bell_rope_13 = area.room('wh_bell_rope_13', name='Bell Rope 13', desc='Bell Rope 13 belongs to the Watch Houses, where combat practice supports rescue, patrols, and accurate reports. The bell rope is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='building', indoor=True)
    wh_snow_tally_14 = area.room('wh_snow_tally_14', name='Snow Tally 14', desc='Snow Tally 14 belongs to the Watch Houses, where combat practice supports rescue, patrols, and accurate reports. The snow tally is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='building', indoor=True)
    rh_listening_bells = area.room('rh_listening_bells', name='Listening Bells', desc='Listening Bells belongs to the Resonance Halls, where listeners record node-adjacent motion without pretending they can mend it. The listening bell is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='building', indoor=True)
    rh_measurement_table = area.room('rh_measurement_table', name='Measurement Table', desc='Measurement Table belongs to the Resonance Halls, where listeners record node-adjacent motion without pretending they can mend it. The stone hum is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='building', indoor=True)
    rh_quiet_gallery = area.room('rh_quiet_gallery', name='Quiet Gallery', desc='Quiet Gallery belongs to the Resonance Halls, where listeners record node-adjacent motion without pretending they can mend it. The careful chalk is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='building', indoor=True)
    rh_Arcana_lens_04 = area.room('rh_Arcana_lens_04', name='Arcana Lens 04', desc='Arcana Lens 04 belongs to the Resonance Halls, where listeners record node-adjacent motion without pretending they can mend it. The Arcana lens is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='building', indoor=True)
    rh_Resonance_ledger_05 = area.room('rh_Resonance_ledger_05', name='Resonance Ledger 05', desc='Resonance Ledger 05 belongs to the Resonance Halls, where listeners record node-adjacent motion without pretending they can mend it. The Resonance ledger is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='building', indoor=True)
    rh_listening_bell_06 = area.room('rh_listening_bell_06', name='Listening Bell 06', desc='Listening Bell 06 belongs to the Resonance Halls, where listeners record node-adjacent motion without pretending they can mend it. The listening bell is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='building', indoor=True)
    rh_stone_hum_07 = area.room('rh_stone_hum_07', name='Stone Hum 07', desc='Stone Hum 07 belongs to the Resonance Halls, where listeners record node-adjacent motion without pretending they can mend it. The stone hum is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='building', indoor=True)
    rh_careful_chalk_08 = area.room('rh_careful_chalk_08', name='Careful Chalk 08', desc='Careful Chalk 08 belongs to the Resonance Halls, where listeners record node-adjacent motion without pretending they can mend it. The careful chalk is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='building', indoor=True)
    rh_Arcana_lens_09 = area.room('rh_Arcana_lens_09', name='Arcana Lens 09', desc='Arcana Lens 09 belongs to the Resonance Halls, where listeners record node-adjacent motion without pretending they can mend it. The Arcana lens is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='building', indoor=True)
    rh_Resonance_ledger_10 = area.room('rh_Resonance_ledger_10', name='Resonance Ledger 10', desc='Resonance Ledger 10 belongs to the Resonance Halls, where listeners record node-adjacent motion without pretending they can mend it. The Resonance ledger is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='building', indoor=True)
    rh_listening_bell_11 = area.room('rh_listening_bell_11', name='Listening Bell 11', desc='Listening Bell 11 belongs to the Resonance Halls, where listeners record node-adjacent motion without pretending they can mend it. The listening bell is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='building', indoor=True)
    rh_stone_hum_12 = area.room('rh_stone_hum_12', name='Stone Hum 12', desc='Stone Hum 12 belongs to the Resonance Halls, where listeners record node-adjacent motion without pretending they can mend it. The stone hum is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='building', indoor=True)
    rh_careful_chalk_13 = area.room('rh_careful_chalk_13', name='Careful Chalk 13', desc='Careful Chalk 13 belongs to the Resonance Halls, where listeners record node-adjacent motion without pretending they can mend it. The careful chalk is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='building', indoor=True)
    rh_Arcana_lens_14 = area.room('rh_Arcana_lens_14', name='Arcana Lens 14', desc='Arcana Lens 14 belongs to the Resonance Halls, where listeners record node-adjacent motion without pretending they can mend it. The Arcana lens is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='building', indoor=True)
    sc_stone_commons = area.room('sc_stone_commons', name='Stone Commons', desc='Stone Commons belongs to Stone Commons, where ordinary civic life makes trust visible one task at a time. The hearth queue is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    sc_guest_hearth = area.room('sc_guest_hearth', name='Guest Hearth', desc='Guest Hearth belongs to Stone Commons, where ordinary civic life makes trust visible one task at a time. The family slate is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    sc_family_step = area.room('sc_family_step', name='Family Step', desc='Family Step belongs to Stone Commons, where ordinary civic life makes trust visible one task at a time. The shared bench is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    sc_rain_trough_04 = area.room('sc_rain_trough_04', name='Rain Trough 04', desc='Rain Trough 04 belongs to Stone Commons, where ordinary civic life makes trust visible one task at a time. The rain trough is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    sc_civic_tale_05 = area.room('sc_civic_tale_05', name='Civic Tale 05', desc='Civic Tale 05 belongs to Stone Commons, where ordinary civic life makes trust visible one task at a time. The civic tale is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    sc_hearth_queue_06 = area.room('sc_hearth_queue_06', name='Hearth Queue 06', desc='Hearth Queue 06 belongs to Stone Commons, where ordinary civic life makes trust visible one task at a time. The hearth queue is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    sc_family_slate_07 = area.room('sc_family_slate_07', name='Family Slate 07', desc='Family Slate 07 belongs to Stone Commons, where ordinary civic life makes trust visible one task at a time. The family slate is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    sc_shared_bench_08 = area.room('sc_shared_bench_08', name='Shared Bench 08', desc='Shared Bench 08 belongs to Stone Commons, where ordinary civic life makes trust visible one task at a time. The shared bench is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    sc_rain_trough_09 = area.room('sc_rain_trough_09', name='Rain Trough 09', desc='Rain Trough 09 belongs to Stone Commons, where ordinary civic life makes trust visible one task at a time. The rain trough is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    sc_civic_tale_10 = area.room('sc_civic_tale_10', name='Civic Tale 10', desc='Civic Tale 10 belongs to Stone Commons, where ordinary civic life makes trust visible one task at a time. The civic tale is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    sc_hearth_queue_11 = area.room('sc_hearth_queue_11', name='Hearth Queue 11', desc='Hearth Queue 11 belongs to Stone Commons, where ordinary civic life makes trust visible one task at a time. The hearth queue is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    sc_family_slate_12 = area.room('sc_family_slate_12', name='Family Slate 12', desc='Family Slate 12 belongs to Stone Commons, where ordinary civic life makes trust visible one task at a time. The family slate is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    sc_shared_bench_13 = area.room('sc_shared_bench_13', name='Shared Bench 13', desc='Shared Bench 13 belongs to Stone Commons, where ordinary civic life makes trust visible one task at a time. The shared bench is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    sc_rain_trough_14 = area.room('sc_rain_trough_14', name='Rain Trough 14', desc='Rain Trough 14 belongs to Stone Commons, where ordinary civic life makes trust visible one task at a time. The rain trough is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
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
    area.exit(rh_quiet_gallery, rh_Arcana_lens_04, 'east')
    area.exit(rh_Arcana_lens_04, rh_quiet_gallery, 'west')
    area.exit(rh_Arcana_lens_04, rh_Resonance_ledger_05, 'east')
    area.exit(rh_Resonance_ledger_05, rh_Arcana_lens_04, 'west')
    area.exit(rh_Resonance_ledger_05, rh_listening_bell_06, 'east')
    area.exit(rh_listening_bell_06, rh_Resonance_ledger_05, 'west')
    area.exit(rh_listening_bell_06, rh_stone_hum_07, 'east')
    area.exit(rh_stone_hum_07, rh_listening_bell_06, 'west')
    area.exit(rh_stone_hum_07, rh_careful_chalk_08, 'east')
    area.exit(rh_careful_chalk_08, rh_stone_hum_07, 'west')
    area.exit(rh_careful_chalk_08, rh_Arcana_lens_09, 'east')
    area.exit(rh_Arcana_lens_09, rh_careful_chalk_08, 'west')
    area.exit(rh_Arcana_lens_09, rh_Resonance_ledger_10, 'east')
    area.exit(rh_Resonance_ledger_10, rh_Arcana_lens_09, 'west')
    area.exit(rh_Resonance_ledger_10, rh_listening_bell_11, 'east')
    area.exit(rh_listening_bell_11, rh_Resonance_ledger_10, 'west')
    area.exit(rh_listening_bell_11, rh_stone_hum_12, 'east')
    area.exit(rh_stone_hum_12, rh_listening_bell_11, 'west')
    area.exit(rh_stone_hum_12, rh_careful_chalk_13, 'east')
    area.exit(rh_careful_chalk_13, rh_stone_hum_12, 'west')
    area.exit(rh_careful_chalk_13, rh_Arcana_lens_14, 'east')
    area.exit(rh_Arcana_lens_14, rh_careful_chalk_13, 'west')
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
    area.exit(rh_Arcana_lens_14, sc_stone_commons, 'north')
    area.exit(sc_stone_commons, rh_Arcana_lens_14, 'south')
    area.exit(sc_rain_trough_14, ug_underhall_gate, 'north')
    area.exit(ug_underhall_gate, sc_rain_trough_14, 'south')
    area.exit(ug_stone_witness_14, hl_high_lift, 'north')
    area.exit(hl_high_lift, ug_stone_witness_14, 'south')
    area.exit(gt_lower_gate, 'greyteeth_lower_passes:ra_rethward_arrival', 'south')
    area.exit(hl_high_lift, 'tremeneth_high_passes:ps_patrol_stair', 'up')
    area.exit(fh_mine_lift, 'tremeneth_deep_mines:cg_claim_gate', 'down')
    area.exit(ug_underhall_gate, 'tremeneth_underhalls:ug_underhall_gate', 'down')

    # NPCs
    _arrival_captain = area.npc(gt_gate_teeth, 'npc_arrival_captain_hadrim', name='Arrival Captain Hadrim', faction='warden', dialogue={'greeting': 'Hadrim listens for the guest bell before he asks your name.', 'topics': {'guest bell': 'Ring once for arrival, twice for need, and never for impatience.'}, 'base_hints': []})
    _quartermaster = area.npc(bm_bellcut_market, 'npc_quartermaster_vessa', name='Quartermaster Vessa', faction='warden', dialogue={'greeting': 'Vessa measures your pack by weight and weather, not by bravado.', 'topics': {'trade': 'Road gear is cheap compared with a bad ridge decision.'}, 'base_hints': []})
    area.vendor(_quartermaster, item_ids=['trail_rations', 'hearty_stew', 'travelers_cloak', 'leather_boots', 'bandage'])
    _forgemaster = area.npc(fh_advanced_forge, 'npc_forgemaster_orruk', name='Forgemaster Orruk Bellhand', faction='ironblood', dialogue={'greeting': 'Orruk watches the color of the metal before he watches the visitor.', 'topics': {'forge': 'A fine edge remembers the person who kept the fire honest.'}, 'base_hints': []})
    area.vendor(_forgemaster, item_ids=['iron_dagger', 'iron_staff', 'pickaxe', 'hatchet', 'skinning_knife'])
    _watch_captain = area.npc(wh_watch_muster, 'npc_watch_captain_maela', name='Watch Captain Maela', faction='warden', dialogue={'greeting': 'Maela reads weather boards the way other captains read warrants.', 'topics': {'patrol': 'A patrol that returns with numbers saves more lives than one that returns with trophies.'}, 'base_hints': []})
    _listener = area.npc(rh_listening_bells, 'npc_listener_senna', name='Listener Senna', faction='resonance', dialogue={'greeting': 'Senna raises a finger until the bell tremor finishes its thought.', 'topics': {'listening': 'We record what the stone does. We do not promise what we cannot do.'}, 'base_hints': []})
    _archivist = area.npc(ug_oath_lintel, 'npc_archivist_belru', name='Archivist Belru Stonekin', faction='resonance', dialogue={'greeting': 'Belru keeps one palm on the underhall ledger as if it might walk away.', 'topics': {'underhalls': 'Family stone deserves witnesses, not looters with cleaner boots.'}, 'base_hints': []})
    _lift_forewoman = area.npc(hl_high_lift, 'npc_lift_forewoman_kelda', name='Lift Forewoman Kelda', faction='ironblood', dialogue={'greeting': 'Kelda tests every cable with the suspicion of someone who likes living.', 'topics': {'lift': 'The high pass does not care who is in a hurry.'}, 'base_hints': []})
    _healer = area.npc(sc_guest_hearth, 'npc_healer_arin', name='Healer Arin Coldhand', faction='verdance', dialogue={'greeting': 'Arin has warm broth ready and no patience for untreated frostbite.', 'topics': {'care': 'A bandage used early is cheaper than pride used late.'}, 'base_hints': []})
    area.vendor(_healer, item_ids=['minor_healing_potion', 'minor_stamina_potion', 'bandage', 'trail_rations'])
    _innkeeper = area.npc(sc_stone_commons, 'npc_innkeeper_tolma', name='Innkeeper Tolma', faction=None, dialogue={'greeting': 'Tolma points out boot hooks, water, and the quiet corner before asking for coin.', 'topics': {'rest': 'Sleep below the bells before you try to answer the heights.'}, 'base_hints': []})
    area.vendor(_innkeeper, item_ids=['trail_rations', 'spiced_fish', 'hearty_stew', 'minor_stamina_potion'])
    _bank_clerk = area.npc(bm_scale_weighing_arch, 'npc_bank_clerk_pellen', name='Bank Clerk Pellen', faction=None, dialogue={'greeting': 'Pellen seals ledgers with a hammer tap that sounds like a tiny verdict.', 'topics': {'coin': 'Stone keeps records better than memory when weather gets involved.'}, 'base_hints': []})
    _arcana_scholar = area.npc(rh_measurement_table, 'npc_arcana_scholar_ileth', name='Scholar Ileth of Western Arcana', faction='western_arcana', dialogue={'greeting': 'Ileth has three lenses, four notebooks, and the manners to admit when none are enough.', 'topics': {'measurements': 'The honest phrase is not yet understood.'}, 'base_hints': []})
    _warden_scout = area.npc(gt_lower_gate, 'npc_warden_scout_rusk', name='Warden Scout Rusk', faction='warden', dialogue={'greeting': 'Rusk smells of road chalk and snowmelt, with marker dust under every nail.', 'topics': {'marks': 'A good marker sends strangers toward help before danger gets a vote.'}, 'base_hints': []})
    _tool_mender = area.npc(bm_rope_bazaar, 'npc_tool_mender_bressa', name='Tool Mender Bressa', faction='ironblood', dialogue={'greeting': 'Bressa tests tool hafts by ear and refuses to sell pretty nonsense.', 'topics': {'tools': 'If it cannot survive a wet climb, it belongs on a wall, not your belt.'}, 'base_hints': []})
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
        rewards=[{'action_type': 'give_scales', 'amount': 28}, {'action_type': 'modify_standing', 'faction_id': 'warden', 'delta': 18}],
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
        rewards=[{'action_type': 'give_scales', 'amount': 36}, {'action_type': 'modify_standing', 'faction_id': 'ironblood', 'delta': 18}],
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
