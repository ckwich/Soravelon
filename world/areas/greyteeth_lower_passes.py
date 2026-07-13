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
    ra_rethward_arrival = area.room('ra_rethward_arrival', name='Rethward Arrival', desc='Rethward Arrival belongs to the Rethward Arrival Track, where travelers learn to count food, weather, and companions. The arrival cairn is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    ra_pack_count_slab = area.room('ra_pack_count_slab', name='Pack Count Slab', desc='Pack Count Slab belongs to the Rethward Arrival Track, where travelers learn to count food, weather, and companions. The road chalk is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    ra_snowmelt_runnel_03 = area.room('ra_snowmelt_runnel_03', name='Snowmelt Runnel 03', desc='Snowmelt Runnel 03 belongs to the Rethward Arrival Track, where travelers learn to count food, weather, and companions. The snowmelt runnel is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    ra_pack_count_04 = area.room('ra_pack_count_04', name='Pack Count 04', desc='Pack Count 04 belongs to the Rethward Arrival Track, where travelers learn to count food, weather, and companions. The pack count is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    ra_low_bell_05 = area.room('ra_low_bell_05', name='Low Bell 05', desc='Low Bell 05 belongs to the Rethward Arrival Track, where travelers learn to count food, weather, and companions. The low bell is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    ra_arrival_cairn_06 = area.room('ra_arrival_cairn_06', name='Arrival Cairn 06', desc='Arrival Cairn 06 belongs to the Rethward Arrival Track, where travelers learn to count food, weather, and companions. The arrival cairn is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    ra_road_chalk_07 = area.room('ra_road_chalk_07', name='Road Chalk 07', desc='Road Chalk 07 belongs to the Rethward Arrival Track, where travelers learn to count food, weather, and companions. The road chalk is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    ra_snowmelt_runnel_08 = area.room('ra_snowmelt_runnel_08', name='Snowmelt Runnel 08', desc='Snowmelt Runnel 08 belongs to the Rethward Arrival Track, where travelers learn to count food, weather, and companions. The snowmelt runnel is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    ra_pack_count_09 = area.room('ra_pack_count_09', name='Pack Count 09', desc='Pack Count 09 belongs to the Rethward Arrival Track, where travelers learn to count food, weather, and companions. The pack count is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    ra_low_bell_10 = area.room('ra_low_bell_10', name='Low Bell 10', desc='Low Bell 10 belongs to the Rethward Arrival Track, where travelers learn to count food, weather, and companions. The low bell is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    ra_arrival_cairn_11 = area.room('ra_arrival_cairn_11', name='Arrival Cairn 11', desc='Arrival Cairn 11 belongs to the Rethward Arrival Track, where travelers learn to count food, weather, and companions. The arrival cairn is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    ra_road_chalk_12 = area.room('ra_road_chalk_12', name='Road Chalk 12', desc='Road Chalk 12 belongs to the Rethward Arrival Track, where travelers learn to count food, weather, and companions. The road chalk is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    ra_snowmelt_runnel_13 = area.room('ra_snowmelt_runnel_13', name='Snowmelt Runnel 13', desc='Snowmelt Runnel 13 belongs to the Rethward Arrival Track, where travelers learn to count food, weather, and companions. The snowmelt runnel is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    ra_pack_count_14 = area.room('ra_pack_count_14', name='Pack Count 14', desc='Pack Count 14 belongs to the Rethward Arrival Track, where travelers learn to count food, weather, and companions. The pack count is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    lm_first_marker = area.room('lm_first_marker', name='First Marker', desc='First Marker belongs to the Lower Marker Road, where marker craft saves strangers before bravery has a chance to fail. The first marker is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    lm_chalked_switchback = area.room('lm_chalked_switchback', name='Chalked Switchback', desc='Chalked Switchback belongs to the Lower Marker Road, where marker craft saves strangers before bravery has a chance to fail. The chalk notch is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    lm_mended_rail_03 = area.room('lm_mended_rail_03', name='Mended Rail 03', desc='Mended Rail 03 belongs to the Lower Marker Road, where marker craft saves strangers before bravery has a chance to fail. The mended rail is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    lm_loose_scree_04 = area.room('lm_loose_scree_04', name='Loose Scree 04', desc='Loose Scree 04 belongs to the Lower Marker Road, where marker craft saves strangers before bravery has a chance to fail. The loose scree is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    lm_route_lesson_05 = area.room('lm_route_lesson_05', name='Route Lesson 05', desc='Route Lesson 05 belongs to the Lower Marker Road, where marker craft saves strangers before bravery has a chance to fail. The route lesson is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    lm_first_marker_06 = area.room('lm_first_marker_06', name='First Marker 06', desc='First Marker 06 belongs to the Lower Marker Road, where marker craft saves strangers before bravery has a chance to fail. The first marker is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    lm_chalk_notch_07 = area.room('lm_chalk_notch_07', name='Chalk Notch 07', desc='Chalk Notch 07 belongs to the Lower Marker Road, where marker craft saves strangers before bravery has a chance to fail. The chalk notch is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    lm_mended_rail_08 = area.room('lm_mended_rail_08', name='Mended Rail 08', desc='Mended Rail 08 belongs to the Lower Marker Road, where marker craft saves strangers before bravery has a chance to fail. The mended rail is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    lm_loose_scree_09 = area.room('lm_loose_scree_09', name='Loose Scree 09', desc='Loose Scree 09 belongs to the Lower Marker Road, where marker craft saves strangers before bravery has a chance to fail. The loose scree is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    lm_route_lesson_10 = area.room('lm_route_lesson_10', name='Route Lesson 10', desc='Route Lesson 10 belongs to the Lower Marker Road, where marker craft saves strangers before bravery has a chance to fail. The route lesson is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    lm_first_marker_11 = area.room('lm_first_marker_11', name='First Marker 11', desc='First Marker 11 belongs to the Lower Marker Road, where marker craft saves strangers before bravery has a chance to fail. The first marker is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    lm_chalk_notch_12 = area.room('lm_chalk_notch_12', name='Chalk Notch 12', desc='Chalk Notch 12 belongs to the Lower Marker Road, where marker craft saves strangers before bravery has a chance to fail. The chalk notch is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    lm_mended_rail_13 = area.room('lm_mended_rail_13', name='Mended Rail 13', desc='Mended Rail 13 belongs to the Lower Marker Road, where marker craft saves strangers before bravery has a chance to fail. The mended rail is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    lm_loose_scree_14 = area.room('lm_loose_scree_14', name='Loose Scree 14', desc='Loose Scree 14 belongs to the Lower Marker Road, where marker craft saves strangers before bravery has a chance to fail. The loose scree is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    bw_bellpost_waystation = area.room('bw_bellpost_waystation', name='Bellpost Waystation', desc='Bellpost Waystation belongs to the Bellpost Waystations, where warmth, soup, and public signs turn the climb into community work. The bellpost is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    bw_soup_hook = area.room('bw_soup_hook', name='Soup Hook', desc='Soup Hook belongs to the Bellpost Waystations, where warmth, soup, and public signs turn the climb into community work. The shelter stew is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    bw_boot_nail_03 = area.room('bw_boot_nail_03', name='Boot Nail 03', desc='Boot Nail 03 belongs to the Bellpost Waystations, where warmth, soup, and public signs turn the climb into community work. The boot nail is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    bw_traveler_name_04 = area.room('bw_traveler_name_04', name='Traveler Name 04', desc='Traveler Name 04 belongs to the Bellpost Waystations, where warmth, soup, and public signs turn the climb into community work. The traveler name is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    bw_night_rope_05 = area.room('bw_night_rope_05', name='Night Rope 05', desc='Night Rope 05 belongs to the Bellpost Waystations, where warmth, soup, and public signs turn the climb into community work. The night rope is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    bw_bellpost_06 = area.room('bw_bellpost_06', name='Bellpost 06', desc='Bellpost 06 belongs to the Bellpost Waystations, where warmth, soup, and public signs turn the climb into community work. The bellpost is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    bw_shelter_stew_07 = area.room('bw_shelter_stew_07', name='Shelter Stew 07', desc='Shelter Stew 07 belongs to the Bellpost Waystations, where warmth, soup, and public signs turn the climb into community work. The shelter stew is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    bw_boot_nail_08 = area.room('bw_boot_nail_08', name='Boot Nail 08', desc='Boot Nail 08 belongs to the Bellpost Waystations, where warmth, soup, and public signs turn the climb into community work. The boot nail is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    bw_traveler_name_09 = area.room('bw_traveler_name_09', name='Traveler Name 09', desc='Traveler Name 09 belongs to the Bellpost Waystations, where warmth, soup, and public signs turn the climb into community work. The traveler name is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    bw_night_rope_10 = area.room('bw_night_rope_10', name='Night Rope 10', desc='Night Rope 10 belongs to the Bellpost Waystations, where warmth, soup, and public signs turn the climb into community work. The night rope is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    bw_bellpost_11 = area.room('bw_bellpost_11', name='Bellpost 11', desc='Bellpost 11 belongs to the Bellpost Waystations, where warmth, soup, and public signs turn the climb into community work. The bellpost is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    bw_shelter_stew_12 = area.room('bw_shelter_stew_12', name='Shelter Stew 12', desc='Shelter Stew 12 belongs to the Bellpost Waystations, where warmth, soup, and public signs turn the climb into community work. The shelter stew is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    bw_boot_nail_13 = area.room('bw_boot_nail_13', name='Boot Nail 13', desc='Boot Nail 13 belongs to the Bellpost Waystations, where warmth, soup, and public signs turn the climb into community work. The boot nail is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    bw_traveler_name_14 = area.room('bw_traveler_name_14', name='Traveler Name 14', desc='Traveler Name 14 belongs to the Bellpost Waystations, where warmth, soup, and public signs turn the climb into community work. The traveler name is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    as_avalanche_shelter = area.room('as_avalanche_shelter', name='Avalanche Shelter', desc='Avalanche Shelter belongs to the Avalanche Shelters, where rescue supplies teach patience where speed gets people buried. The avalanche shutter is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    as_red_rope_cache = area.room('as_red_rope_cache', name='Red Rope Cache', desc='Red Rope Cache belongs to the Avalanche Shelters, where rescue supplies teach patience where speed gets people buried. The red rope is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    as_snow_shelf_03 = area.room('as_snow_shelf_03', name='Snow Shelf 03', desc='Snow Shelf 03 belongs to the Avalanche Shelters, where rescue supplies teach patience where speed gets people buried. The snow shelf is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    as_rescue_tally_04 = area.room('as_rescue_tally_04', name='Rescue Tally 04', desc='Rescue Tally 04 belongs to the Avalanche Shelters, where rescue supplies teach patience where speed gets people buried. The rescue tally is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    as_quiet_shovel_05 = area.room('as_quiet_shovel_05', name='Quiet Shovel 05', desc='Quiet Shovel 05 belongs to the Avalanche Shelters, where rescue supplies teach patience where speed gets people buried. The quiet shovel is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    as_avalanche_shutter_06 = area.room('as_avalanche_shutter_06', name='Avalanche Shutter 06', desc='Avalanche Shutter 06 belongs to the Avalanche Shelters, where rescue supplies teach patience where speed gets people buried. The avalanche shutter is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    as_red_rope_07 = area.room('as_red_rope_07', name='Red Rope 07', desc='Red Rope 07 belongs to the Avalanche Shelters, where rescue supplies teach patience where speed gets people buried. The red rope is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    as_snow_shelf_08 = area.room('as_snow_shelf_08', name='Snow Shelf 08', desc='Snow Shelf 08 belongs to the Avalanche Shelters, where rescue supplies teach patience where speed gets people buried. The snow shelf is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    as_rescue_tally_09 = area.room('as_rescue_tally_09', name='Rescue Tally 09', desc='Rescue Tally 09 belongs to the Avalanche Shelters, where rescue supplies teach patience where speed gets people buried. The rescue tally is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    as_quiet_shovel_10 = area.room('as_quiet_shovel_10', name='Quiet Shovel 10', desc='Quiet Shovel 10 belongs to the Avalanche Shelters, where rescue supplies teach patience where speed gets people buried. The quiet shovel is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    as_avalanche_shutter_11 = area.room('as_avalanche_shutter_11', name='Avalanche Shutter 11', desc='Avalanche Shutter 11 belongs to the Avalanche Shelters, where rescue supplies teach patience where speed gets people buried. The avalanche shutter is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    as_red_rope_12 = area.room('as_red_rope_12', name='Red Rope 12', desc='Red Rope 12 belongs to the Avalanche Shelters, where rescue supplies teach patience where speed gets people buried. The red rope is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    as_snow_shelf_13 = area.room('as_snow_shelf_13', name='Snow Shelf 13', desc='Snow Shelf 13 belongs to the Avalanche Shelters, where rescue supplies teach patience where speed gets people buried. The snow shelf is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    as_rescue_tally_14 = area.room('as_rescue_tally_14', name='Rescue Tally 14', desc='Rescue Tally 14 belongs to the Avalanche Shelters, where rescue supplies teach patience where speed gets people buried. The rescue tally is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    gl_goat_ledge = area.room('gl_goat_ledge', name='Goat Ledge', desc='Goat Ledge belongs to the Goat Ledges, where combat comes from territory, hunger, and bad footing. The goat trail is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    gl_ridgecat_shadow = area.room('gl_ridgecat_shadow', name='Ridgecat Shadow', desc='Ridgecat Shadow belongs to the Goat Ledges, where combat comes from territory, hunger, and bad footing. The ridgecat mark is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    gl_wind_tooth_03 = area.room('gl_wind_tooth_03', name='Wind Tooth 03', desc='Wind Tooth 03 belongs to the Goat Ledges, where combat comes from territory, hunger, and bad footing. The wind tooth is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    gl_lichen_shelf_04 = area.room('gl_lichen_shelf_04', name='Lichen Shelf 04', desc='Lichen Shelf 04 belongs to the Goat Ledges, where combat comes from territory, hunger, and bad footing. The lichen shelf is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    gl_bone_charm_05 = area.room('gl_bone_charm_05', name='Bone Charm 05', desc='Bone Charm 05 belongs to the Goat Ledges, where combat comes from territory, hunger, and bad footing. The bone charm is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    gl_goat_trail_06 = area.room('gl_goat_trail_06', name='Goat Trail 06', desc='Goat Trail 06 belongs to the Goat Ledges, where combat comes from territory, hunger, and bad footing. The goat trail is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    gl_ridgecat_mark_07 = area.room('gl_ridgecat_mark_07', name='Ridgecat Mark 07', desc='Ridgecat Mark 07 belongs to the Goat Ledges, where combat comes from territory, hunger, and bad footing. The ridgecat mark is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    gl_wind_tooth_08 = area.room('gl_wind_tooth_08', name='Wind Tooth 08', desc='Wind Tooth 08 belongs to the Goat Ledges, where combat comes from territory, hunger, and bad footing. The wind tooth is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    gl_lichen_shelf_09 = area.room('gl_lichen_shelf_09', name='Lichen Shelf 09', desc='Lichen Shelf 09 belongs to the Goat Ledges, where combat comes from territory, hunger, and bad footing. The lichen shelf is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    gl_bone_charm_10 = area.room('gl_bone_charm_10', name='Bone Charm 10', desc='Bone Charm 10 belongs to the Goat Ledges, where combat comes from territory, hunger, and bad footing. The bone charm is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    gl_goat_trail_11 = area.room('gl_goat_trail_11', name='Goat Trail 11', desc='Goat Trail 11 belongs to the Goat Ledges, where combat comes from territory, hunger, and bad footing. The goat trail is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    gl_ridgecat_mark_12 = area.room('gl_ridgecat_mark_12', name='Ridgecat Mark 12', desc='Ridgecat Mark 12 belongs to the Goat Ledges, where combat comes from territory, hunger, and bad footing. The ridgecat mark is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    gl_wind_tooth_13 = area.room('gl_wind_tooth_13', name='Wind Tooth 13', desc='Wind Tooth 13 belongs to the Goat Ledges, where combat comes from territory, hunger, and bad footing. The wind tooth is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    gl_lichen_shelf_14 = area.room('gl_lichen_shelf_14', name='Lichen Shelf 14', desc='Lichen Shelf 14 belongs to the Goat Ledges, where combat comes from territory, hunger, and bad footing. The lichen shelf is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    sp_survey_pull_off = area.room('sp_survey_pull_off', name='Survey Pull Off', desc='Survey Pull Off belongs to the Survey Pull-Offs, where old survey marks expose both civic care and Imperial appetite. The survey notch is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    sp_old_chain_pin = area.room('sp_old_chain_pin', name='Old Chain Pin', desc='Old Chain Pin belongs to the Survey Pull-Offs, where old survey marks expose both civic care and Imperial appetite. The old chain is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    sp_viewing_slit_03 = area.room('sp_viewing_slit_03', name='Viewing Slit 03', desc='Viewing Slit 03 belongs to the Survey Pull-Offs, where old survey marks expose both civic care and Imperial appetite. The viewing slit is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    sp_hammer_tap_04 = area.room('sp_hammer_tap_04', name='Hammer Tap 04', desc='Hammer Tap 04 belongs to the Survey Pull-Offs, where old survey marks expose both civic care and Imperial appetite. The hammer tap is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    sp_map_scratch_05 = area.room('sp_map_scratch_05', name='Map Scratch 05', desc='Map Scratch 05 belongs to the Survey Pull-Offs, where old survey marks expose both civic care and Imperial appetite. The map scratch is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    sp_survey_notch_06 = area.room('sp_survey_notch_06', name='Survey Notch 06', desc='Survey Notch 06 belongs to the Survey Pull-Offs, where old survey marks expose both civic care and Imperial appetite. The survey notch is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    sp_old_chain_07 = area.room('sp_old_chain_07', name='Old Chain 07', desc='Old Chain 07 belongs to the Survey Pull-Offs, where old survey marks expose both civic care and Imperial appetite. The old chain is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    sp_viewing_slit_08 = area.room('sp_viewing_slit_08', name='Viewing Slit 08', desc='Viewing Slit 08 belongs to the Survey Pull-Offs, where old survey marks expose both civic care and Imperial appetite. The viewing slit is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    sp_hammer_tap_09 = area.room('sp_hammer_tap_09', name='Hammer Tap 09', desc='Hammer Tap 09 belongs to the Survey Pull-Offs, where old survey marks expose both civic care and Imperial appetite. The hammer tap is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    sp_map_scratch_10 = area.room('sp_map_scratch_10', name='Map Scratch 10', desc='Map Scratch 10 belongs to the Survey Pull-Offs, where old survey marks expose both civic care and Imperial appetite. The map scratch is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    sp_survey_notch_11 = area.room('sp_survey_notch_11', name='Survey Notch 11', desc='Survey Notch 11 belongs to the Survey Pull-Offs, where old survey marks expose both civic care and Imperial appetite. The survey notch is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    sp_old_chain_12 = area.room('sp_old_chain_12', name='Old Chain 12', desc='Old Chain 12 belongs to the Survey Pull-Offs, where old survey marks expose both civic care and Imperial appetite. The old chain is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    sp_viewing_slit_13 = area.room('sp_viewing_slit_13', name='Viewing Slit 13', desc='Viewing Slit 13 belongs to the Survey Pull-Offs, where old survey marks expose both civic care and Imperial appetite. The viewing slit is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    sp_hammer_tap_14 = area.room('sp_hammer_tap_14', name='Hammer Tap 14', desc='Hammer Tap 14 belongs to the Survey Pull-Offs, where old survey marks expose both civic care and Imperial appetite. The hammer tap is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    wt_windcut_turn = area.room('wt_windcut_turn', name='Windcut Turn', desc='Windcut Turn belongs to the Windcut Traverse, where false signs and hard weather make the road dangerous for believable reasons. The windcut turn is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    wt_broken_banner = area.room('wt_broken_banner', name='Broken Banner', desc='Broken Banner belongs to the Windcut Traverse, where false signs and hard weather make the road dangerous for believable reasons. The false tab is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    wt_eagle_shadow_03 = area.room('wt_eagle_shadow_03', name='Eagle Shadow 03', desc='Eagle Shadow 03 belongs to the Windcut Traverse, where false signs and hard weather make the road dangerous for believable reasons. The eagle shadow is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    wt_sleet_bite_04 = area.room('wt_sleet_bite_04', name='Sleet Bite 04', desc='Sleet Bite 04 belongs to the Windcut Traverse, where false signs and hard weather make the road dangerous for believable reasons. The sleet bite is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    wt_thin_rope_05 = area.room('wt_thin_rope_05', name='Thin Rope 05', desc='Thin Rope 05 belongs to the Windcut Traverse, where false signs and hard weather make the road dangerous for believable reasons. The thin rope is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    wt_windcut_turn_06 = area.room('wt_windcut_turn_06', name='Windcut Turn 06', desc='Windcut Turn 06 belongs to the Windcut Traverse, where false signs and hard weather make the road dangerous for believable reasons. The windcut turn is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    wt_false_tab_07 = area.room('wt_false_tab_07', name='False Tab 07', desc='False Tab 07 belongs to the Windcut Traverse, where false signs and hard weather make the road dangerous for believable reasons. The false tab is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    wt_eagle_shadow_08 = area.room('wt_eagle_shadow_08', name='Eagle Shadow 08', desc='Eagle Shadow 08 belongs to the Windcut Traverse, where false signs and hard weather make the road dangerous for believable reasons. The eagle shadow is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    wt_sleet_bite_09 = area.room('wt_sleet_bite_09', name='Sleet Bite 09', desc='Sleet Bite 09 belongs to the Windcut Traverse, where false signs and hard weather make the road dangerous for believable reasons. The sleet bite is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    wt_thin_rope_10 = area.room('wt_thin_rope_10', name='Thin Rope 10', desc='Thin Rope 10 belongs to the Windcut Traverse, where false signs and hard weather make the road dangerous for believable reasons. The thin rope is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    wt_windcut_turn_11 = area.room('wt_windcut_turn_11', name='Windcut Turn 11', desc='Windcut Turn 11 belongs to the Windcut Traverse, where false signs and hard weather make the road dangerous for believable reasons. The windcut turn is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    wt_false_tab_12 = area.room('wt_false_tab_12', name='False Tab 12', desc='False Tab 12 belongs to the Windcut Traverse, where false signs and hard weather make the road dangerous for believable reasons. The false tab is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    wt_eagle_shadow_13 = area.room('wt_eagle_shadow_13', name='Eagle Shadow 13', desc='Eagle Shadow 13 belongs to the Windcut Traverse, where false signs and hard weather make the road dangerous for believable reasons. The eagle shadow is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    wt_sleet_bite_14 = area.room('wt_sleet_bite_14', name='Sleet Bite 14', desc='Sleet Bite 14 belongs to the Windcut Traverse, where false signs and hard weather make the road dangerous for believable reasons. The sleet bite is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    tg_tremen_gate = area.room('tg_tremen_gate', name='Tremen Gate', desc='Tremen Gate belongs to the Tremen Gate Approach, where arrival feels earned because the road has taught its habits. The final bell is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    tg_final_bell = area.room('tg_final_bell', name='Final Bell', desc='Final Bell belongs to the Tremen Gate Approach, where arrival feels earned because the road has taught its habits. The gate sightline is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    tg_warm_stone_03 = area.room('tg_warm_stone_03', name='Warm Stone 03', desc='Warm Stone 03 belongs to the Tremen Gate Approach, where arrival feels earned because the road has taught its habits. The warm stone is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    tg_last_marker_04 = area.room('tg_last_marker_04', name='Last Marker 04', desc='Last Marker 04 belongs to the Tremen Gate Approach, where arrival feels earned because the road has taught its habits. The last marker is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    tg_road_gratitude_05 = area.room('tg_road_gratitude_05', name='Road Gratitude 05', desc='Road Gratitude 05 belongs to the Tremen Gate Approach, where arrival feels earned because the road has taught its habits. The road gratitude is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    tg_final_bell_06 = area.room('tg_final_bell_06', name='Final Bell 06', desc='Final Bell 06 belongs to the Tremen Gate Approach, where arrival feels earned because the road has taught its habits. The final bell is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    tg_gate_sightline_07 = area.room('tg_gate_sightline_07', name='Gate Sightline 07', desc='Gate Sightline 07 belongs to the Tremen Gate Approach, where arrival feels earned because the road has taught its habits. The gate sightline is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    tg_warm_stone_08 = area.room('tg_warm_stone_08', name='Warm Stone 08', desc='Warm Stone 08 belongs to the Tremen Gate Approach, where arrival feels earned because the road has taught its habits. The warm stone is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    tg_last_marker_09 = area.room('tg_last_marker_09', name='Last Marker 09', desc='Last Marker 09 belongs to the Tremen Gate Approach, where arrival feels earned because the road has taught its habits. The last marker is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    tg_road_gratitude_10 = area.room('tg_road_gratitude_10', name='Road Gratitude 10', desc='Road Gratitude 10 belongs to the Tremen Gate Approach, where arrival feels earned because the road has taught its habits. The road gratitude is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    tg_final_bell_11 = area.room('tg_final_bell_11', name='Final Bell 11', desc='Final Bell 11 belongs to the Tremen Gate Approach, where arrival feels earned because the road has taught its habits. The final bell is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    tg_gate_sightline_12 = area.room('tg_gate_sightline_12', name='Gate Sightline 12', desc='Gate Sightline 12 belongs to the Tremen Gate Approach, where arrival feels earned because the road has taught its habits. The gate sightline is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    tg_warm_stone_13 = area.room('tg_warm_stone_13', name='Warm Stone 13', desc='Warm Stone 13 belongs to the Tremen Gate Approach, where arrival feels earned because the road has taught its habits. The warm stone is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)
    tg_last_marker_14 = area.room('tg_last_marker_14', name='Last Marker 14', desc='Last Marker 14 belongs to the Tremen Gate Approach, where arrival feels earned because the road has taught its habits. The last marker is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='path', indoor=False)

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
    _route_warden = area.npc(ra_rethward_arrival, 'npc_route_warden_mirren', name='Route Warden Mirren', faction='wardens', dialogue={'greeting': 'Mirren counts your party twice and your rope three times.', 'topics': {'route': 'The road is generous if you respect its bookkeeping.'}, 'base_hints': []})
    _bellpost_keeper = area.npc(bw_bellpost_waystation, 'npc_bellpost_keeper_roven', name='Bellpost Keeper Roven', faction='wardens', dialogue={'greeting': 'Roven has soup on the hook and chalk dust on both thumbs.', 'topics': {'markers': 'A mark that only locals understand is a vanity, not a rescue tool.'}, 'base_hints': []})
    _shelter_medic = area.npc(as_avalanche_shelter, 'npc_shelter_medic_essa', name='Shelter Medic Essa', faction='verdance', dialogue={'greeting': 'Essa checks ears, fingers, and courage in that order.', 'topics': {'rescue': 'Fast help matters, but careful help keeps the helpers alive.'}, 'base_hints': []})
    _surveyor = area.npc(sp_survey_pull_off, 'npc_surveyor_pel', name='Surveyor Pel', faction='western_arcana', dialogue={'greeting': 'Pel keeps a map pinned with spoon handles and old chain links.', 'topics': {'survey': 'The old chain pins were accurate. That does not mean they were kind.'}, 'base_hints': []})

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
