"""Tremeneth Underhalls -- Hub 3 exterior zone

Family vault walks, bell-tuned corridors, cisterns, and deep pattern rooms under Tremen where old stone refuses simple answers."""

from world.area_builder import AreaBuilder


def build():
    area = AreaBuilder('tremeneth_underhalls')

    area.zone(
        name='Tremeneth Underhalls',
        zone_type='underground',
        continent='varath',
        tier=3,
        region='tremeneth_mountains',
        faction_territory='warden',
        faction_presence=['resonance', 'wardens', 'western_arcana', 'verdance'],
        world_x=34,
        world_y=48,
        world_radius=145,
    )

    # Materials
    area.material('coldvein_stone', tier=2, terrain='stone', absorbed_property='endurance', profession_bonus={'engineering': 0.1, 'mining': 0.05})
    area.material('resonance_shard', tier=3, terrain='deep stone', absorbed_property='attunement', profession_bonus={'alchemy': 0.1, 'scholarship': 0.05})
    area.material('windroot', tier=2, terrain='alpine', absorbed_property='breath', profession_bonus={'alchemy': 0.1, 'herbalism': 0.05})
    area.material('bellcap_mushroom', tier=2, terrain='cavern', absorbed_property='focus', profession_bonus={'cooking': 0.1, 'foraging': 0.05})
    area.material('cavern_whitefish', tier=2, terrain='water', absorbed_property='quiet', profession_bonus={'cooking': 0.1, 'fishing': 0.05})
    area.material('minevermin_hide', tier=1, terrain='mine', absorbed_property='utility', profession_bonus={'smithing': 0.1, 'skinning': 0.05})

    # Rooms
    ug_underhall_gate = area.room('ug_underhall_gate', name='Underhall Gate', desc='Underhall Gate belongs to the Underhall Gate, where descent is witness work rather than adventure tourism. The underhall gate is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    ug_lantern_count = area.room('ug_lantern_count', name='Lantern Count', desc='Lantern Count belongs to the Underhall Gate, where descent is witness work rather than adventure tourism. The lantern count is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    ug_name_cord_03 = area.room('ug_name_cord_03', name='Name Cord 03', desc='Name Cord 03 belongs to the Underhall Gate, where descent is witness work rather than adventure tourism. The name cord is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    ug_cool_draft_04 = area.room('ug_cool_draft_04', name='Cool Draft 04', desc='Cool Draft 04 belongs to the Underhall Gate, where descent is witness work rather than adventure tourism. The cool draft is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    ug_guest_warning_05 = area.room('ug_guest_warning_05', name='Guest Warning 05', desc='Guest Warning 05 belongs to the Underhall Gate, where descent is witness work rather than adventure tourism. The guest warning is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    ug_underhall_gate_06 = area.room('ug_underhall_gate_06', name='Underhall Gate 06', desc='Underhall Gate 06 belongs to the Underhall Gate, where descent is witness work rather than adventure tourism. The underhall gate is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    ug_lantern_count_07 = area.room('ug_lantern_count_07', name='Lantern Count 07', desc='Lantern Count 07 belongs to the Underhall Gate, where descent is witness work rather than adventure tourism. The lantern count is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    ug_name_cord_08 = area.room('ug_name_cord_08', name='Name Cord 08', desc='Name Cord 08 belongs to the Underhall Gate, where descent is witness work rather than adventure tourism. The name cord is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    ug_cool_draft_09 = area.room('ug_cool_draft_09', name='Cool Draft 09', desc='Cool Draft 09 belongs to the Underhall Gate, where descent is witness work rather than adventure tourism. The cool draft is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    ug_guest_warning_10 = area.room('ug_guest_warning_10', name='Guest Warning 10', desc='Guest Warning 10 belongs to the Underhall Gate, where descent is witness work rather than adventure tourism. The guest warning is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    ug_underhall_gate_11 = area.room('ug_underhall_gate_11', name='Underhall Gate 11', desc='Underhall Gate 11 belongs to the Underhall Gate, where descent is witness work rather than adventure tourism. The underhall gate is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    ug_lantern_count_12 = area.room('ug_lantern_count_12', name='Lantern Count 12', desc='Lantern Count 12 belongs to the Underhall Gate, where descent is witness work rather than adventure tourism. The lantern count is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    ug_name_cord_13 = area.room('ug_name_cord_13', name='Name Cord 13', desc='Name Cord 13 belongs to the Underhall Gate, where descent is witness work rather than adventure tourism. The name cord is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    ug_cool_draft_14 = area.room('ug_cool_draft_14', name='Cool Draft 14', desc='Cool Draft 14 belongs to the Underhall Gate, where descent is witness work rather than adventure tourism. The cool draft is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    fv_family_vault_walk = area.room('fv_family_vault_walk', name='Family Vault Walk', desc='Family Vault Walk belongs to the Family Vault Walks, where history is personal, named, and resistant to treasure-room thinking. The family vault is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    fv_low_name_shelf = area.room('fv_low_name_shelf', name='Low Name Shelf', desc='Low Name Shelf belongs to the Family Vault Walks, where history is personal, named, and resistant to treasure-room thinking. The low name shelf is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    fv_quiet_bowl_03 = area.room('fv_quiet_bowl_03', name='Quiet Bowl 03', desc='Quiet Bowl 03 belongs to the Family Vault Walks, where history is personal, named, and resistant to treasure-room thinking. The quiet bowl is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    fv_kept_tool_04 = area.room('fv_kept_tool_04', name='Kept Tool 04', desc='Kept Tool 04 belongs to the Family Vault Walks, where history is personal, named, and resistant to treasure-room thinking. The kept tool is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    fv_mourning_bench_05 = area.room('fv_mourning_bench_05', name='Mourning Bench 05', desc='Mourning Bench 05 belongs to the Family Vault Walks, where history is personal, named, and resistant to treasure-room thinking. The mourning bench is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    fv_family_vault_06 = area.room('fv_family_vault_06', name='Family Vault 06', desc='Family Vault 06 belongs to the Family Vault Walks, where history is personal, named, and resistant to treasure-room thinking. The family vault is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    fv_low_name_shelf_07 = area.room('fv_low_name_shelf_07', name='Low Name Shelf 07', desc='Low Name Shelf 07 belongs to the Family Vault Walks, where history is personal, named, and resistant to treasure-room thinking. The low name shelf is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    fv_quiet_bowl_08 = area.room('fv_quiet_bowl_08', name='Quiet Bowl 08', desc='Quiet Bowl 08 belongs to the Family Vault Walks, where history is personal, named, and resistant to treasure-room thinking. The quiet bowl is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    fv_kept_tool_09 = area.room('fv_kept_tool_09', name='Kept Tool 09', desc='Kept Tool 09 belongs to the Family Vault Walks, where history is personal, named, and resistant to treasure-room thinking. The kept tool is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    fv_mourning_bench_10 = area.room('fv_mourning_bench_10', name='Mourning Bench 10', desc='Mourning Bench 10 belongs to the Family Vault Walks, where history is personal, named, and resistant to treasure-room thinking. The mourning bench is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    fv_family_vault_11 = area.room('fv_family_vault_11', name='Family Vault 11', desc='Family Vault 11 belongs to the Family Vault Walks, where history is personal, named, and resistant to treasure-room thinking. The family vault is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    fv_low_name_shelf_12 = area.room('fv_low_name_shelf_12', name='Low Name Shelf 12', desc='Low Name Shelf 12 belongs to the Family Vault Walks, where history is personal, named, and resistant to treasure-room thinking. The low name shelf is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    fv_quiet_bowl_13 = area.room('fv_quiet_bowl_13', name='Quiet Bowl 13', desc='Quiet Bowl 13 belongs to the Family Vault Walks, where history is personal, named, and resistant to treasure-room thinking. The quiet bowl is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    fv_kept_tool_14 = area.room('fv_kept_tool_14', name='Kept Tool 14', desc='Kept Tool 14 belongs to the Family Vault Walks, where history is personal, named, and resistant to treasure-room thinking. The kept tool is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    bc_bell_tuned_corridor = area.room('bc_bell_tuned_corridor', name='Bell Tuned Corridor', desc='Bell Tuned Corridor belongs to the Bell-Tuned Corridors, where resonance is listening and consequence, not a simple ghost story. The bell corridor is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    bc_soft_clapper = area.room('bc_soft_clapper', name='Soft Clapper', desc='Soft Clapper belongs to the Bell-Tuned Corridors, where resonance is listening and consequence, not a simple ghost story. The soft clapper is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    bc_tuned_niche_03 = area.room('bc_tuned_niche_03', name='Tuned Niche 03', desc='Tuned Niche 03 belongs to the Bell-Tuned Corridors, where resonance is listening and consequence, not a simple ghost story. The tuned niche is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    bc_dust_tone_04 = area.room('bc_dust_tone_04', name='Dust Tone 04', desc='Dust Tone 04 belongs to the Bell-Tuned Corridors, where resonance is listening and consequence, not a simple ghost story. The dust tone is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    bc_measured_foot_05 = area.room('bc_measured_foot_05', name='Measured Foot 05', desc='Measured Foot 05 belongs to the Bell-Tuned Corridors, where resonance is listening and consequence, not a simple ghost story. The measured foot is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    bc_bell_corridor_06 = area.room('bc_bell_corridor_06', name='Bell Corridor 06', desc='Bell Corridor 06 belongs to the Bell-Tuned Corridors, where resonance is listening and consequence, not a simple ghost story. The bell corridor is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    bc_soft_clapper_07 = area.room('bc_soft_clapper_07', name='Soft Clapper 07', desc='Soft Clapper 07 belongs to the Bell-Tuned Corridors, where resonance is listening and consequence, not a simple ghost story. The soft clapper is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    bc_tuned_niche_08 = area.room('bc_tuned_niche_08', name='Tuned Niche 08', desc='Tuned Niche 08 belongs to the Bell-Tuned Corridors, where resonance is listening and consequence, not a simple ghost story. The tuned niche is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    bc_dust_tone_09 = area.room('bc_dust_tone_09', name='Dust Tone 09', desc='Dust Tone 09 belongs to the Bell-Tuned Corridors, where resonance is listening and consequence, not a simple ghost story. The dust tone is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    bc_measured_foot_10 = area.room('bc_measured_foot_10', name='Measured Foot 10', desc='Measured Foot 10 belongs to the Bell-Tuned Corridors, where resonance is listening and consequence, not a simple ghost story. The measured foot is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    bc_bell_corridor_11 = area.room('bc_bell_corridor_11', name='Bell Corridor 11', desc='Bell Corridor 11 belongs to the Bell-Tuned Corridors, where resonance is listening and consequence, not a simple ghost story. The bell corridor is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    bc_soft_clapper_12 = area.room('bc_soft_clapper_12', name='Soft Clapper 12', desc='Soft Clapper 12 belongs to the Bell-Tuned Corridors, where resonance is listening and consequence, not a simple ghost story. The soft clapper is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    bc_tuned_niche_13 = area.room('bc_tuned_niche_13', name='Tuned Niche 13', desc='Tuned Niche 13 belongs to the Bell-Tuned Corridors, where resonance is listening and consequence, not a simple ghost story. The tuned niche is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    bc_dust_tone_14 = area.room('bc_dust_tone_14', name='Dust Tone 14', desc='Dust Tone 14 belongs to the Bell-Tuned Corridors, where resonance is listening and consequence, not a simple ghost story. The dust tone is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    dc_dry_cistern = area.room('dc_dry_cistern', name='Dry Cistern', desc='Dry Cistern belongs to the Dry Cisterns, where water, food, and repair make underground life practical. The dry cistern is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    dc_whitefish_rill = area.room('dc_whitefish_rill', name='Whitefish Rill', desc='Whitefish Rill belongs to the Dry Cisterns, where water, food, and repair make underground life practical. The whitefish rill is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    dc_water_mark_03 = area.room('dc_water_mark_03', name='Water Mark 03', desc='Water Mark 03 belongs to the Dry Cisterns, where water, food, and repair make underground life practical. The water mark is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    dc_old_bucket_04 = area.room('dc_old_bucket_04', name='Old Bucket 04', desc='Old Bucket 04 belongs to the Dry Cisterns, where water, food, and repair make underground life practical. The old bucket is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    dc_cool_moss_05 = area.room('dc_cool_moss_05', name='Cool Moss 05', desc='Cool Moss 05 belongs to the Dry Cisterns, where water, food, and repair make underground life practical. The cool moss is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    dc_dry_cistern_06 = area.room('dc_dry_cistern_06', name='Dry Cistern 06', desc='Dry Cistern 06 belongs to the Dry Cisterns, where water, food, and repair make underground life practical. The dry cistern is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    dc_whitefish_rill_07 = area.room('dc_whitefish_rill_07', name='Whitefish Rill 07', desc='Whitefish Rill 07 belongs to the Dry Cisterns, where water, food, and repair make underground life practical. The whitefish rill is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    dc_water_mark_08 = area.room('dc_water_mark_08', name='Water Mark 08', desc='Water Mark 08 belongs to the Dry Cisterns, where water, food, and repair make underground life practical. The water mark is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    dc_old_bucket_09 = area.room('dc_old_bucket_09', name='Old Bucket 09', desc='Old Bucket 09 belongs to the Dry Cisterns, where water, food, and repair make underground life practical. The old bucket is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    dc_cool_moss_10 = area.room('dc_cool_moss_10', name='Cool Moss 10', desc='Cool Moss 10 belongs to the Dry Cisterns, where water, food, and repair make underground life practical. The cool moss is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    dc_dry_cistern_11 = area.room('dc_dry_cistern_11', name='Dry Cistern 11', desc='Dry Cistern 11 belongs to the Dry Cisterns, where water, food, and repair make underground life practical. The dry cistern is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    dc_whitefish_rill_12 = area.room('dc_whitefish_rill_12', name='Whitefish Rill 12', desc='Whitefish Rill 12 belongs to the Dry Cisterns, where water, food, and repair make underground life practical. The whitefish rill is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    dc_water_mark_13 = area.room('dc_water_mark_13', name='Water Mark 13', desc='Water Mark 13 belongs to the Dry Cisterns, where water, food, and repair make underground life practical. The water mark is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    dc_old_bucket_14 = area.room('dc_old_bucket_14', name='Old Bucket 14', desc='Old Bucket 14 belongs to the Dry Cisterns, where water, food, and repair make underground life practical. The old bucket is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    ej_eightfold_junction = area.room('ej_eightfold_junction', name='Eightfold Junction', desc='Eightfold Junction belongs to Eightfold Junction, where navigation is learned culture instead of maze punishment. The eightfold junction is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    ej_wrong_turn_bell = area.room('ej_wrong_turn_bell', name='Wrong Turn Bell', desc='Wrong Turn Bell belongs to Eightfold Junction, where navigation is learned culture instead of maze punishment. The wrong-turn bell is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    ej_chalk_braid_03 = area.room('ej_chalk_braid_03', name='Chalk Braid 03', desc='Chalk Braid 03 belongs to Eightfold Junction, where navigation is learned culture instead of maze punishment. The chalk braid is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    ej_return_arrow_04 = area.room('ej_return_arrow_04', name='Return Arrow 04', desc='Return Arrow 04 belongs to Eightfold Junction, where navigation is learned culture instead of maze punishment. The return arrow is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    ej_listening_dust_05 = area.room('ej_listening_dust_05', name='Listening Dust 05', desc='Listening Dust 05 belongs to Eightfold Junction, where navigation is learned culture instead of maze punishment. The listening dust is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    ej_eightfold_junction_06 = area.room('ej_eightfold_junction_06', name='Eightfold Junction 06', desc='Eightfold Junction 06 belongs to Eightfold Junction, where navigation is learned culture instead of maze punishment. The eightfold junction is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    ej_wrong_turn_bell_07 = area.room('ej_wrong_turn_bell_07', name='Wrong Turn Bell 07', desc='Wrong Turn Bell 07 belongs to Eightfold Junction, where navigation is learned culture instead of maze punishment. The wrong-turn bell is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    ej_chalk_braid_08 = area.room('ej_chalk_braid_08', name='Chalk Braid 08', desc='Chalk Braid 08 belongs to Eightfold Junction, where navigation is learned culture instead of maze punishment. The chalk braid is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    ej_return_arrow_09 = area.room('ej_return_arrow_09', name='Return Arrow 09', desc='Return Arrow 09 belongs to Eightfold Junction, where navigation is learned culture instead of maze punishment. The return arrow is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    ej_listening_dust_10 = area.room('ej_listening_dust_10', name='Listening Dust 10', desc='Listening Dust 10 belongs to Eightfold Junction, where navigation is learned culture instead of maze punishment. The listening dust is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    ej_eightfold_junction_11 = area.room('ej_eightfold_junction_11', name='Eightfold Junction 11', desc='Eightfold Junction 11 belongs to Eightfold Junction, where navigation is learned culture instead of maze punishment. The eightfold junction is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    ej_wrong_turn_bell_12 = area.room('ej_wrong_turn_bell_12', name='Wrong Turn Bell 12', desc='Wrong Turn Bell 12 belongs to Eightfold Junction, where navigation is learned culture instead of maze punishment. The wrong-turn bell is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    ej_chalk_braid_13 = area.room('ej_chalk_braid_13', name='Chalk Braid 13', desc='Chalk Braid 13 belongs to Eightfold Junction, where navigation is learned culture instead of maze punishment. The chalk braid is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    ej_return_arrow_14 = area.room('ej_return_arrow_14', name='Return Arrow 14', desc='Return Arrow 14 belongs to Eightfold Junction, where navigation is learned culture instead of maze punishment. The return arrow is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    qc_quiet_chasm = area.room('qc_quiet_chasm', name='Quiet Chasm', desc='Quiet Chasm belongs to the Quiet Chasms, where sound and caution matter more than swagger. The quiet chasm is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='cave', indoor=True)
    qc_chain_whisper = area.room('qc_chain_whisper', name='Chain Whisper', desc='Chain Whisper belongs to the Quiet Chasms, where sound and caution matter more than swagger. The chain whisper is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='cave', indoor=True)
    qc_dark_rail_03 = area.room('qc_dark_rail_03', name='Dark Rail 03', desc='Dark Rail 03 belongs to the Quiet Chasms, where sound and caution matter more than swagger. The dark rail is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='cave', indoor=True)
    qc_fall_bell_04 = area.room('qc_fall_bell_04', name='Fall Bell 04', desc='Fall Bell 04 belongs to the Quiet Chasms, where sound and caution matter more than swagger. The fall bell is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='cave', indoor=True)
    qc_breath_pause_05 = area.room('qc_breath_pause_05', name='Breath Pause 05', desc='Breath Pause 05 belongs to the Quiet Chasms, where sound and caution matter more than swagger. The breath pause is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='cave', indoor=True)
    qc_quiet_chasm_06 = area.room('qc_quiet_chasm_06', name='Quiet Chasm 06', desc='Quiet Chasm 06 belongs to the Quiet Chasms, where sound and caution matter more than swagger. The quiet chasm is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='cave', indoor=True)
    qc_chain_whisper_07 = area.room('qc_chain_whisper_07', name='Chain Whisper 07', desc='Chain Whisper 07 belongs to the Quiet Chasms, where sound and caution matter more than swagger. The chain whisper is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='cave', indoor=True)
    qc_dark_rail_08 = area.room('qc_dark_rail_08', name='Dark Rail 08', desc='Dark Rail 08 belongs to the Quiet Chasms, where sound and caution matter more than swagger. The dark rail is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='cave', indoor=True)
    qc_fall_bell_09 = area.room('qc_fall_bell_09', name='Fall Bell 09', desc='Fall Bell 09 belongs to the Quiet Chasms, where sound and caution matter more than swagger. The fall bell is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='cave', indoor=True)
    qc_breath_pause_10 = area.room('qc_breath_pause_10', name='Breath Pause 10', desc='Breath Pause 10 belongs to the Quiet Chasms, where sound and caution matter more than swagger. The breath pause is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='cave', indoor=True)
    qc_quiet_chasm_11 = area.room('qc_quiet_chasm_11', name='Quiet Chasm 11', desc='Quiet Chasm 11 belongs to the Quiet Chasms, where sound and caution matter more than swagger. The quiet chasm is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='cave', indoor=True)
    qc_chain_whisper_12 = area.room('qc_chain_whisper_12', name='Chain Whisper 12', desc='Chain Whisper 12 belongs to the Quiet Chasms, where sound and caution matter more than swagger. The chain whisper is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='cave', indoor=True)
    qc_dark_rail_13 = area.room('qc_dark_rail_13', name='Dark Rail 13', desc='Dark Rail 13 belongs to the Quiet Chasms, where sound and caution matter more than swagger. The dark rail is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='cave', indoor=True)
    qc_fall_bell_14 = area.room('qc_fall_bell_14', name='Fall Bell 14', desc='Fall Bell 14 belongs to the Quiet Chasms, where sound and caution matter more than swagger. The fall bell is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='cave', indoor=True)
    sp_sealed_pattern_room = area.room('sp_sealed_pattern_room', name='Sealed Pattern Room', desc='Sealed Pattern Room belongs to the Sealed Pattern Rooms, where curiosity is welcome only when it keeps restraint close. The sealed pattern is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    sp_pattern_threshold = area.room('sp_pattern_threshold', name='Pattern Threshold', desc='Pattern Threshold belongs to the Sealed Pattern Rooms, where curiosity is welcome only when it keeps restraint close. The threshold line is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    sp_old_inlay_03 = area.room('sp_old_inlay_03', name='Old Inlay 03', desc='Old Inlay 03 belongs to the Sealed Pattern Rooms, where curiosity is welcome only when it keeps restraint close. The old inlay is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    sp_silent_frame_04 = area.room('sp_silent_frame_04', name='Silent Frame 04', desc='Silent Frame 04 belongs to the Sealed Pattern Rooms, where curiosity is welcome only when it keeps restraint close. The silent frame is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    sp_pressure_mark_05 = area.room('sp_pressure_mark_05', name='Pressure Mark 05', desc='Pressure Mark 05 belongs to the Sealed Pattern Rooms, where curiosity is welcome only when it keeps restraint close. The pressure mark is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    sp_sealed_pattern_06 = area.room('sp_sealed_pattern_06', name='Sealed Pattern 06', desc='Sealed Pattern 06 belongs to the Sealed Pattern Rooms, where curiosity is welcome only when it keeps restraint close. The sealed pattern is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    sp_threshold_line_07 = area.room('sp_threshold_line_07', name='Threshold Line 07', desc='Threshold Line 07 belongs to the Sealed Pattern Rooms, where curiosity is welcome only when it keeps restraint close. The threshold line is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    sp_old_inlay_08 = area.room('sp_old_inlay_08', name='Old Inlay 08', desc='Old Inlay 08 belongs to the Sealed Pattern Rooms, where curiosity is welcome only when it keeps restraint close. The old inlay is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    sp_silent_frame_09 = area.room('sp_silent_frame_09', name='Silent Frame 09', desc='Silent Frame 09 belongs to the Sealed Pattern Rooms, where curiosity is welcome only when it keeps restraint close. The silent frame is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    sp_pressure_mark_10 = area.room('sp_pressure_mark_10', name='Pressure Mark 10', desc='Pressure Mark 10 belongs to the Sealed Pattern Rooms, where curiosity is welcome only when it keeps restraint close. The pressure mark is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    sp_sealed_pattern_11 = area.room('sp_sealed_pattern_11', name='Sealed Pattern 11', desc='Sealed Pattern 11 belongs to the Sealed Pattern Rooms, where curiosity is welcome only when it keeps restraint close. The sealed pattern is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    sp_threshold_line_12 = area.room('sp_threshold_line_12', name='Threshold Line 12', desc='Threshold Line 12 belongs to the Sealed Pattern Rooms, where curiosity is welcome only when it keeps restraint close. The threshold line is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    sp_old_inlay_13 = area.room('sp_old_inlay_13', name='Old Inlay 13', desc='Old Inlay 13 belongs to the Sealed Pattern Rooms, where curiosity is welcome only when it keeps restraint close. The old inlay is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    sp_silent_frame_14 = area.room('sp_silent_frame_14', name='Silent Frame 14', desc='Silent Frame 14 belongs to the Sealed Pattern Rooms, where curiosity is welcome only when it keeps restraint close. The silent frame is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    dl_deep_listening_chamber = area.room('dl_deep_listening_chamber', name='Deep Listening Chamber', desc='Deep Listening Chamber belongs to the Deep Listening Chamber, where some questions are important before they are answerable. The deep chamber is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    dl_last_measure = area.room('dl_last_measure', name='Last Measure', desc='Last Measure belongs to the Deep Listening Chamber, where some questions are important before they are answerable. The last measure is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    dl_slow_bell_03 = area.room('dl_slow_bell_03', name='Slow Bell 03', desc='Slow Bell 03 belongs to the Deep Listening Chamber, where some questions are important before they are answerable. The slow bell is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    dl_stone_breath_04 = area.room('dl_stone_breath_04', name='Stone Breath 04', desc='Stone Breath 04 belongs to the Deep Listening Chamber, where some questions are important before they are answerable. The stone breath is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    dl_kept_question_05 = area.room('dl_kept_question_05', name='Kept Question 05', desc='Kept Question 05 belongs to the Deep Listening Chamber, where some questions are important before they are answerable. The kept question is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    dl_deep_chamber_06 = area.room('dl_deep_chamber_06', name='Deep Chamber 06', desc='Deep Chamber 06 belongs to the Deep Listening Chamber, where some questions are important before they are answerable. The deep chamber is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    dl_last_measure_07 = area.room('dl_last_measure_07', name='Last Measure 07', desc='Last Measure 07 belongs to the Deep Listening Chamber, where some questions are important before they are answerable. The last measure is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    dl_slow_bell_08 = area.room('dl_slow_bell_08', name='Slow Bell 08', desc='Slow Bell 08 belongs to the Deep Listening Chamber, where some questions are important before they are answerable. The slow bell is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    dl_stone_breath_09 = area.room('dl_stone_breath_09', name='Stone Breath 09', desc='Stone Breath 09 belongs to the Deep Listening Chamber, where some questions are important before they are answerable. The stone breath is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    dl_kept_question_10 = area.room('dl_kept_question_10', name='Kept Question 10', desc='Kept Question 10 belongs to the Deep Listening Chamber, where some questions are important before they are answerable. The kept question is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    dl_deep_chamber_11 = area.room('dl_deep_chamber_11', name='Deep Chamber 11', desc='Deep Chamber 11 belongs to the Deep Listening Chamber, where some questions are important before they are answerable. The deep chamber is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    dl_last_measure_12 = area.room('dl_last_measure_12', name='Last Measure 12', desc='Last Measure 12 belongs to the Deep Listening Chamber, where some questions are important before they are answerable. The last measure is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    dl_slow_bell_13 = area.room('dl_slow_bell_13', name='Slow Bell 13', desc='Slow Bell 13 belongs to the Deep Listening Chamber, where some questions are important before they are answerable. The slow bell is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    dl_stone_breath_14 = area.room('dl_stone_breath_14', name='Stone Breath 14', desc='Stone Breath 14 belongs to the Deep Listening Chamber, where some questions are important before they are answerable. The stone breath is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)

    # Local exits
    area.exit(ug_underhall_gate, ug_lantern_count, 'east')
    area.exit(ug_lantern_count, ug_underhall_gate, 'west')
    area.exit(ug_lantern_count, ug_name_cord_03, 'east')
    area.exit(ug_name_cord_03, ug_lantern_count, 'west')
    area.exit(ug_name_cord_03, ug_cool_draft_04, 'east')
    area.exit(ug_cool_draft_04, ug_name_cord_03, 'west')
    area.exit(ug_cool_draft_04, ug_guest_warning_05, 'east')
    area.exit(ug_guest_warning_05, ug_cool_draft_04, 'west')
    area.exit(ug_guest_warning_05, ug_underhall_gate_06, 'east')
    area.exit(ug_underhall_gate_06, ug_guest_warning_05, 'west')
    area.exit(ug_underhall_gate_06, ug_lantern_count_07, 'east')
    area.exit(ug_lantern_count_07, ug_underhall_gate_06, 'west')
    area.exit(ug_lantern_count_07, ug_name_cord_08, 'east')
    area.exit(ug_name_cord_08, ug_lantern_count_07, 'west')
    area.exit(ug_name_cord_08, ug_cool_draft_09, 'east')
    area.exit(ug_cool_draft_09, ug_name_cord_08, 'west')
    area.exit(ug_cool_draft_09, ug_guest_warning_10, 'east')
    area.exit(ug_guest_warning_10, ug_cool_draft_09, 'west')
    area.exit(ug_guest_warning_10, ug_underhall_gate_11, 'east')
    area.exit(ug_underhall_gate_11, ug_guest_warning_10, 'west')
    area.exit(ug_underhall_gate_11, ug_lantern_count_12, 'east')
    area.exit(ug_lantern_count_12, ug_underhall_gate_11, 'west')
    area.exit(ug_lantern_count_12, ug_name_cord_13, 'east')
    area.exit(ug_name_cord_13, ug_lantern_count_12, 'west')
    area.exit(ug_name_cord_13, ug_cool_draft_14, 'east')
    area.exit(ug_cool_draft_14, ug_name_cord_13, 'west')
    area.exit(fv_family_vault_walk, fv_low_name_shelf, 'east')
    area.exit(fv_low_name_shelf, fv_family_vault_walk, 'west')
    area.exit(fv_low_name_shelf, fv_quiet_bowl_03, 'east')
    area.exit(fv_quiet_bowl_03, fv_low_name_shelf, 'west')
    area.exit(fv_quiet_bowl_03, fv_kept_tool_04, 'east')
    area.exit(fv_kept_tool_04, fv_quiet_bowl_03, 'west')
    area.exit(fv_kept_tool_04, fv_mourning_bench_05, 'east')
    area.exit(fv_mourning_bench_05, fv_kept_tool_04, 'west')
    area.exit(fv_mourning_bench_05, fv_family_vault_06, 'east')
    area.exit(fv_family_vault_06, fv_mourning_bench_05, 'west')
    area.exit(fv_family_vault_06, fv_low_name_shelf_07, 'east')
    area.exit(fv_low_name_shelf_07, fv_family_vault_06, 'west')
    area.exit(fv_low_name_shelf_07, fv_quiet_bowl_08, 'east')
    area.exit(fv_quiet_bowl_08, fv_low_name_shelf_07, 'west')
    area.exit(fv_quiet_bowl_08, fv_kept_tool_09, 'east')
    area.exit(fv_kept_tool_09, fv_quiet_bowl_08, 'west')
    area.exit(fv_kept_tool_09, fv_mourning_bench_10, 'east')
    area.exit(fv_mourning_bench_10, fv_kept_tool_09, 'west')
    area.exit(fv_mourning_bench_10, fv_family_vault_11, 'east')
    area.exit(fv_family_vault_11, fv_mourning_bench_10, 'west')
    area.exit(fv_family_vault_11, fv_low_name_shelf_12, 'east')
    area.exit(fv_low_name_shelf_12, fv_family_vault_11, 'west')
    area.exit(fv_low_name_shelf_12, fv_quiet_bowl_13, 'east')
    area.exit(fv_quiet_bowl_13, fv_low_name_shelf_12, 'west')
    area.exit(fv_quiet_bowl_13, fv_kept_tool_14, 'east')
    area.exit(fv_kept_tool_14, fv_quiet_bowl_13, 'west')
    area.exit(bc_bell_tuned_corridor, bc_soft_clapper, 'east')
    area.exit(bc_soft_clapper, bc_bell_tuned_corridor, 'west')
    area.exit(bc_soft_clapper, bc_tuned_niche_03, 'east')
    area.exit(bc_tuned_niche_03, bc_soft_clapper, 'west')
    area.exit(bc_tuned_niche_03, bc_dust_tone_04, 'east')
    area.exit(bc_dust_tone_04, bc_tuned_niche_03, 'west')
    area.exit(bc_dust_tone_04, bc_measured_foot_05, 'east')
    area.exit(bc_measured_foot_05, bc_dust_tone_04, 'west')
    area.exit(bc_measured_foot_05, bc_bell_corridor_06, 'east')
    area.exit(bc_bell_corridor_06, bc_measured_foot_05, 'west')
    area.exit(bc_bell_corridor_06, bc_soft_clapper_07, 'east')
    area.exit(bc_soft_clapper_07, bc_bell_corridor_06, 'west')
    area.exit(bc_soft_clapper_07, bc_tuned_niche_08, 'east')
    area.exit(bc_tuned_niche_08, bc_soft_clapper_07, 'west')
    area.exit(bc_tuned_niche_08, bc_dust_tone_09, 'east')
    area.exit(bc_dust_tone_09, bc_tuned_niche_08, 'west')
    area.exit(bc_dust_tone_09, bc_measured_foot_10, 'east')
    area.exit(bc_measured_foot_10, bc_dust_tone_09, 'west')
    area.exit(bc_measured_foot_10, bc_bell_corridor_11, 'east')
    area.exit(bc_bell_corridor_11, bc_measured_foot_10, 'west')
    area.exit(bc_bell_corridor_11, bc_soft_clapper_12, 'east')
    area.exit(bc_soft_clapper_12, bc_bell_corridor_11, 'west')
    area.exit(bc_soft_clapper_12, bc_tuned_niche_13, 'east')
    area.exit(bc_tuned_niche_13, bc_soft_clapper_12, 'west')
    area.exit(bc_tuned_niche_13, bc_dust_tone_14, 'east')
    area.exit(bc_dust_tone_14, bc_tuned_niche_13, 'west')
    area.exit(dc_dry_cistern, dc_whitefish_rill, 'east')
    area.exit(dc_whitefish_rill, dc_dry_cistern, 'west')
    area.exit(dc_whitefish_rill, dc_water_mark_03, 'east')
    area.exit(dc_water_mark_03, dc_whitefish_rill, 'west')
    area.exit(dc_water_mark_03, dc_old_bucket_04, 'east')
    area.exit(dc_old_bucket_04, dc_water_mark_03, 'west')
    area.exit(dc_old_bucket_04, dc_cool_moss_05, 'east')
    area.exit(dc_cool_moss_05, dc_old_bucket_04, 'west')
    area.exit(dc_cool_moss_05, dc_dry_cistern_06, 'east')
    area.exit(dc_dry_cistern_06, dc_cool_moss_05, 'west')
    area.exit(dc_dry_cistern_06, dc_whitefish_rill_07, 'east')
    area.exit(dc_whitefish_rill_07, dc_dry_cistern_06, 'west')
    area.exit(dc_whitefish_rill_07, dc_water_mark_08, 'east')
    area.exit(dc_water_mark_08, dc_whitefish_rill_07, 'west')
    area.exit(dc_water_mark_08, dc_old_bucket_09, 'east')
    area.exit(dc_old_bucket_09, dc_water_mark_08, 'west')
    area.exit(dc_old_bucket_09, dc_cool_moss_10, 'east')
    area.exit(dc_cool_moss_10, dc_old_bucket_09, 'west')
    area.exit(dc_cool_moss_10, dc_dry_cistern_11, 'east')
    area.exit(dc_dry_cistern_11, dc_cool_moss_10, 'west')
    area.exit(dc_dry_cistern_11, dc_whitefish_rill_12, 'east')
    area.exit(dc_whitefish_rill_12, dc_dry_cistern_11, 'west')
    area.exit(dc_whitefish_rill_12, dc_water_mark_13, 'east')
    area.exit(dc_water_mark_13, dc_whitefish_rill_12, 'west')
    area.exit(dc_water_mark_13, dc_old_bucket_14, 'east')
    area.exit(dc_old_bucket_14, dc_water_mark_13, 'west')
    area.exit(ej_eightfold_junction, ej_wrong_turn_bell, 'east')
    area.exit(ej_wrong_turn_bell, ej_eightfold_junction, 'west')
    area.exit(ej_wrong_turn_bell, ej_chalk_braid_03, 'east')
    area.exit(ej_chalk_braid_03, ej_wrong_turn_bell, 'west')
    area.exit(ej_chalk_braid_03, ej_return_arrow_04, 'east')
    area.exit(ej_return_arrow_04, ej_chalk_braid_03, 'west')
    area.exit(ej_return_arrow_04, ej_listening_dust_05, 'east')
    area.exit(ej_listening_dust_05, ej_return_arrow_04, 'west')
    area.exit(ej_listening_dust_05, ej_eightfold_junction_06, 'east')
    area.exit(ej_eightfold_junction_06, ej_listening_dust_05, 'west')
    area.exit(ej_eightfold_junction_06, ej_wrong_turn_bell_07, 'east')
    area.exit(ej_wrong_turn_bell_07, ej_eightfold_junction_06, 'west')
    area.exit(ej_wrong_turn_bell_07, ej_chalk_braid_08, 'east')
    area.exit(ej_chalk_braid_08, ej_wrong_turn_bell_07, 'west')
    area.exit(ej_chalk_braid_08, ej_return_arrow_09, 'east')
    area.exit(ej_return_arrow_09, ej_chalk_braid_08, 'west')
    area.exit(ej_return_arrow_09, ej_listening_dust_10, 'east')
    area.exit(ej_listening_dust_10, ej_return_arrow_09, 'west')
    area.exit(ej_listening_dust_10, ej_eightfold_junction_11, 'east')
    area.exit(ej_eightfold_junction_11, ej_listening_dust_10, 'west')
    area.exit(ej_eightfold_junction_11, ej_wrong_turn_bell_12, 'east')
    area.exit(ej_wrong_turn_bell_12, ej_eightfold_junction_11, 'west')
    area.exit(ej_wrong_turn_bell_12, ej_chalk_braid_13, 'east')
    area.exit(ej_chalk_braid_13, ej_wrong_turn_bell_12, 'west')
    area.exit(ej_chalk_braid_13, ej_return_arrow_14, 'east')
    area.exit(ej_return_arrow_14, ej_chalk_braid_13, 'west')
    area.exit(qc_quiet_chasm, qc_chain_whisper, 'east')
    area.exit(qc_chain_whisper, qc_quiet_chasm, 'west')
    area.exit(qc_chain_whisper, qc_dark_rail_03, 'east')
    area.exit(qc_dark_rail_03, qc_chain_whisper, 'west')
    area.exit(qc_dark_rail_03, qc_fall_bell_04, 'east')
    area.exit(qc_fall_bell_04, qc_dark_rail_03, 'west')
    area.exit(qc_fall_bell_04, qc_breath_pause_05, 'east')
    area.exit(qc_breath_pause_05, qc_fall_bell_04, 'west')
    area.exit(qc_breath_pause_05, qc_quiet_chasm_06, 'east')
    area.exit(qc_quiet_chasm_06, qc_breath_pause_05, 'west')
    area.exit(qc_quiet_chasm_06, qc_chain_whisper_07, 'east')
    area.exit(qc_chain_whisper_07, qc_quiet_chasm_06, 'west')
    area.exit(qc_chain_whisper_07, qc_dark_rail_08, 'east')
    area.exit(qc_dark_rail_08, qc_chain_whisper_07, 'west')
    area.exit(qc_dark_rail_08, qc_fall_bell_09, 'east')
    area.exit(qc_fall_bell_09, qc_dark_rail_08, 'west')
    area.exit(qc_fall_bell_09, qc_breath_pause_10, 'east')
    area.exit(qc_breath_pause_10, qc_fall_bell_09, 'west')
    area.exit(qc_breath_pause_10, qc_quiet_chasm_11, 'east')
    area.exit(qc_quiet_chasm_11, qc_breath_pause_10, 'west')
    area.exit(qc_quiet_chasm_11, qc_chain_whisper_12, 'east')
    area.exit(qc_chain_whisper_12, qc_quiet_chasm_11, 'west')
    area.exit(qc_chain_whisper_12, qc_dark_rail_13, 'east')
    area.exit(qc_dark_rail_13, qc_chain_whisper_12, 'west')
    area.exit(qc_dark_rail_13, qc_fall_bell_14, 'east')
    area.exit(qc_fall_bell_14, qc_dark_rail_13, 'west')
    area.exit(sp_sealed_pattern_room, sp_pattern_threshold, 'east')
    area.exit(sp_pattern_threshold, sp_sealed_pattern_room, 'west')
    area.exit(sp_pattern_threshold, sp_old_inlay_03, 'east')
    area.exit(sp_old_inlay_03, sp_pattern_threshold, 'west')
    area.exit(sp_old_inlay_03, sp_silent_frame_04, 'east')
    area.exit(sp_silent_frame_04, sp_old_inlay_03, 'west')
    area.exit(sp_silent_frame_04, sp_pressure_mark_05, 'east')
    area.exit(sp_pressure_mark_05, sp_silent_frame_04, 'west')
    area.exit(sp_pressure_mark_05, sp_sealed_pattern_06, 'east')
    area.exit(sp_sealed_pattern_06, sp_pressure_mark_05, 'west')
    area.exit(sp_sealed_pattern_06, sp_threshold_line_07, 'east')
    area.exit(sp_threshold_line_07, sp_sealed_pattern_06, 'west')
    area.exit(sp_threshold_line_07, sp_old_inlay_08, 'east')
    area.exit(sp_old_inlay_08, sp_threshold_line_07, 'west')
    area.exit(sp_old_inlay_08, sp_silent_frame_09, 'east')
    area.exit(sp_silent_frame_09, sp_old_inlay_08, 'west')
    area.exit(sp_silent_frame_09, sp_pressure_mark_10, 'east')
    area.exit(sp_pressure_mark_10, sp_silent_frame_09, 'west')
    area.exit(sp_pressure_mark_10, sp_sealed_pattern_11, 'east')
    area.exit(sp_sealed_pattern_11, sp_pressure_mark_10, 'west')
    area.exit(sp_sealed_pattern_11, sp_threshold_line_12, 'east')
    area.exit(sp_threshold_line_12, sp_sealed_pattern_11, 'west')
    area.exit(sp_threshold_line_12, sp_old_inlay_13, 'east')
    area.exit(sp_old_inlay_13, sp_threshold_line_12, 'west')
    area.exit(sp_old_inlay_13, sp_silent_frame_14, 'east')
    area.exit(sp_silent_frame_14, sp_old_inlay_13, 'west')
    area.exit(dl_deep_listening_chamber, dl_last_measure, 'east')
    area.exit(dl_last_measure, dl_deep_listening_chamber, 'west')
    area.exit(dl_last_measure, dl_slow_bell_03, 'east')
    area.exit(dl_slow_bell_03, dl_last_measure, 'west')
    area.exit(dl_slow_bell_03, dl_stone_breath_04, 'east')
    area.exit(dl_stone_breath_04, dl_slow_bell_03, 'west')
    area.exit(dl_stone_breath_04, dl_kept_question_05, 'east')
    area.exit(dl_kept_question_05, dl_stone_breath_04, 'west')
    area.exit(dl_kept_question_05, dl_deep_chamber_06, 'east')
    area.exit(dl_deep_chamber_06, dl_kept_question_05, 'west')
    area.exit(dl_deep_chamber_06, dl_last_measure_07, 'east')
    area.exit(dl_last_measure_07, dl_deep_chamber_06, 'west')
    area.exit(dl_last_measure_07, dl_slow_bell_08, 'east')
    area.exit(dl_slow_bell_08, dl_last_measure_07, 'west')
    area.exit(dl_slow_bell_08, dl_stone_breath_09, 'east')
    area.exit(dl_stone_breath_09, dl_slow_bell_08, 'west')
    area.exit(dl_stone_breath_09, dl_kept_question_10, 'east')
    area.exit(dl_kept_question_10, dl_stone_breath_09, 'west')
    area.exit(dl_kept_question_10, dl_deep_chamber_11, 'east')
    area.exit(dl_deep_chamber_11, dl_kept_question_10, 'west')
    area.exit(dl_deep_chamber_11, dl_last_measure_12, 'east')
    area.exit(dl_last_measure_12, dl_deep_chamber_11, 'west')
    area.exit(dl_last_measure_12, dl_slow_bell_13, 'east')
    area.exit(dl_slow_bell_13, dl_last_measure_12, 'west')
    area.exit(dl_slow_bell_13, dl_stone_breath_14, 'east')
    area.exit(dl_stone_breath_14, dl_slow_bell_13, 'west')
    area.exit(ug_cool_draft_14, fv_family_vault_walk, 'north')
    area.exit(fv_family_vault_walk, ug_cool_draft_14, 'south')
    area.exit(fv_kept_tool_14, bc_bell_tuned_corridor, 'north')
    area.exit(bc_bell_tuned_corridor, fv_kept_tool_14, 'south')
    area.exit(bc_dust_tone_14, dc_dry_cistern, 'north')
    area.exit(dc_dry_cistern, bc_dust_tone_14, 'south')
    area.exit(dc_old_bucket_14, ej_eightfold_junction, 'north')
    area.exit(ej_eightfold_junction, dc_old_bucket_14, 'south')
    area.exit(ej_return_arrow_14, qc_quiet_chasm, 'north')
    area.exit(qc_quiet_chasm, ej_return_arrow_14, 'south')
    area.exit(qc_fall_bell_14, sp_sealed_pattern_room, 'north')
    area.exit(sp_sealed_pattern_room, qc_fall_bell_14, 'south')
    area.exit(sp_silent_frame_14, dl_deep_listening_chamber, 'north')
    area.exit(dl_deep_listening_chamber, sp_silent_frame_14, 'south')
    area.exit(ug_underhall_gate, 'tremen:ug_underhall_gate', 'up')

    # NPCs
    _underhall_archivist = area.npc(ug_underhall_gate, 'npc_underhall_archivist_nelli', name='Underhall Archivist Nelli', faction='resonance', dialogue={'greeting_tiers': {"neutral": 'Nelli waits until your lantern is steady before she hands you any history.'}, 'topics': {'measure': 'A careful measure is a promise to return the name with the number.'}, 'base_hints': []})
    _vault_grandson = area.npc(fv_family_vault_walk, 'npc_vault_grandson_porr', name='Porr Of The Low Shelf', faction=None, dialogue={'greeting_tiers': {"neutral": 'Porr has a water cup in both hands and a stubborn set to his jaw.'}, 'topics': {'names': 'Grandmother said a name is thirsty if no one speaks it kindly.'}, 'base_hints': []})
    _cistern_fisher = area.npc(dc_dry_cistern, 'npc_cistern_fisher_ren', name='Cistern Fisher Ren', faction=None, dialogue={'greeting_tiers': {"neutral": 'Ren fishes by sound and claims surface anglers are too loud to learn anything.'}, 'topics': {'fish': 'Whitefish feed families. That makes them more important than rumors.'}, 'base_hints': []})
    _pattern_listener = area.npc(sp_pattern_threshold, 'npc_pattern_listener_ysol', name='Pattern Listener Ysol', faction='western_arcana', dialogue={'greeting_tiers': {"neutral": 'Ysol keeps ink off the old inlay and her curiosity on a short leash.'}, 'topics': {'pattern': 'The first duty is not making the room answer. The first duty is not damaging the question.'}, 'base_hints': []})
    _quiet_guard = area.npc(ej_eightfold_junction, 'npc_quiet_guard_vedra', name='Quiet Guard Vedra', faction='wardens', dialogue={'greeting_tiers': {"neutral": 'Vedra points with two fingers and never raises her voice in the junction.'}, 'topics': {'junction': 'If you get lost here, stop moving. The wrong turn is louder than waiting.'}, 'base_hints': []})

    # Quest item templates
    area.item('thu_name_cord', key='name cord', item_type='item', weight=0.5, rarity='normal', desc='A soft cord knotted with family marks, meant to be carried through vault rooms without touching the shelves.', value=0, is_quest_item=True)
    area.item('thu_pattern_note', key='pattern note', item_type='item', weight=0.5, rarity='normal', desc='A cautious note about a sealed pattern, written with more questions than conclusions.', value=0, is_quest_item=True)

    # Quests
    area.quest(
        'thu_q_first_measure',
        name='The First Measure Below',
        description="Nelli turns Belru's cord into a careful walk through the first gate, making the underhall chain begin with respect and route learning.",
        quest_type='investigation',
        quest_giver='npc_underhall_archivist_nelli',
        objectives=[{'type': 'investigate', 'target': 'ug_underhall_gate', 'count': 1}, {'type': 'visit', 'target': 'bc_bell_tuned_corridor', 'count': 1}, {'type': 'talk_to', 'target': 'npc_quiet_guard_vedra', 'count': 1}],
        rewards=[{'action_type': 'give_scales', 'amount': 34}, {'action_type': 'give_skill_xp', 'skill_id': 'scholarship', 'count': 12}],
        next_quest_id='thu_q_family_names',
        prerequisite_quests=['tre_q_underhall_measure'],
        can_share=True,
        consequence_small='Nelli adds your first measurements to the descent ledger and leaves room for corrections, not boasts.',
    )
    area.quest(
        'thu_q_family_names',
        name='Water For Low Names',
        description='Porr asks you to carry a name cord and water through the vault walk, making emotional continuity part of exploration rather than optional flavor.',
        quest_type='social',
        quest_giver='npc_vault_grandson_porr',
        objectives=[{'type': 'visit', 'target': 'fv_family_vault_walk', 'count': 1}, {'type': 'deliver', 'target': 'fv_low_name_shelf', 'count': 1, 'item_tag': 'thu_name_cord'}, {'type': 'talk_to', 'target': 'npc_vault_grandson_porr', 'count': 1}],
        rewards=[{'action_type': 'give_scales', 'amount': 30}, {'action_type': 'modify_standing', 'faction_id': 'resonance', 'delta': 1800}],
        next_quest_id=None,
        prerequisite_quests=['thu_q_first_measure'],
        can_share=True,
        consequence_small='Porr places the empty cup upside down, a small sign that the name was visited properly and not merely checked off.',
    )
    area.quest(
        'thu_q_dry_cistern',
        name='Whitefish In The Dark',
        description='Ren teaches underhall fishing as household logistics, routing players into cistern rooms where practical life continues below the city.',
        quest_type='gather',
        quest_giver='npc_cistern_fisher_ren',
        objectives=[{'type': 'visit', 'target': 'dc_dry_cistern', 'count': 1}, {'type': 'gather', 'target': 'cavern_whitefish', 'count': 3}, {'type': 'deliver', 'target': 'npc_cistern_fisher_ren', 'count': 1, 'item_tag': 'cavern_whitefish'}],
        rewards=[{'action_type': 'give_scales', 'amount': 28}, {'action_type': 'give_skill_xp', 'skill_id': 'fishing', 'count': 12}],
        next_quest_id=None,
        prerequisite_quests=[],
        can_share=True,
        consequence_small='Ren chalks the quietest fishing posture on the cistern wall, which is exactly as smug and useful as promised.',
    )
    area.quest(
        'thu_q_eightfold_count',
        name='Count Eight, Return Once',
        description='Vedra asks you to map the junction by sound and return, making navigation a learned underhall practice instead of punishment for being new.',
        quest_type='exploration',
        quest_giver='npc_quiet_guard_vedra',
        objectives=[{'type': 'investigate', 'target': 'ej_eightfold_junction', 'count': 1}, {'type': 'visit', 'target': 'qc_quiet_chasm', 'count': 1}, {'type': 'talk_to', 'target': 'npc_quiet_guard_vedra', 'count': 1}],
        rewards=[{'action_type': 'give_scales', 'amount': 32}, {'action_type': 'give_skill_xp', 'skill_id': 'survival', 'count': 12}],
        next_quest_id=None,
        prerequisite_quests=[],
        can_share=True,
        consequence_small='Vedra adds your sound count to a public chalk braid, helping later visitors learn where silence bends.',
    )
    area.quest(
        'thu_q_pattern_debt',
        name='The Pattern Debt',
        description='Ysol receives the mine seam tracing and asks you to compare it with sealed pattern rooms, seeding a longer mystery without changing the shared world yet.',
        quest_type='investigation',
        quest_giver='npc_pattern_listener_ysol',
        objectives=[{'type': 'deliver', 'target': 'npc_pattern_listener_ysol', 'count': 1, 'item_tag': 'tdm_seam_tracing'}, {'type': 'investigate', 'target': 'sp_sealed_pattern_room', 'count': 1}, {'type': 'visit', 'target': 'dl_deep_listening_chamber', 'count': 1}],
        rewards=[{'action_type': 'give_scales', 'amount': 44}, {'action_type': 'give_skill_xp', 'skill_id': 'scholarship', 'count': 12}],
        next_quest_id=None,
        prerequisite_quests=['tdm_q_underhall_seam'],
        can_share=True,
        consequence_small='Ysol files your comparison under unresolved but witnessed, which in Tremen is a serious category rather than a shrug.',
    )

    # Spawns
    area.spawn(dc_dry_cistern, 'underhall_skitter', count_min=1, count_max=2, respawn_minutes=14, respawn_variance=4)
    area.spawn(dc_whitefish_rill, 'underhall_skitter', count_min=1, count_max=2, respawn_minutes=14, respawn_variance=4)
    area.spawn(dc_water_mark_03, 'minevermin', count_min=1, count_max=2, respawn_minutes=14, respawn_variance=4)
    area.spawn(ej_eightfold_junction, 'bell_echo', count_min=1, count_max=1, respawn_minutes=14, respawn_variance=4)
    area.spawn(ej_wrong_turn_bell, 'underhall_skitter', count_min=1, count_max=2, respawn_minutes=14, respawn_variance=4)
    area.spawn(ej_listening_dust_05, 'bell_echo', count_min=1, count_max=1, respawn_minutes=14, respawn_variance=4)
    area.spawn(qc_quiet_chasm, 'underhall_skitter', count_min=1, count_max=2, respawn_minutes=14, respawn_variance=4)
    area.spawn(qc_chain_whisper, 'loose_oreling', count_min=1, count_max=2, respawn_minutes=14, respawn_variance=4)
    area.spawn(qc_dark_rail_03, 'bell_echo', count_min=1, count_max=1, respawn_minutes=14, respawn_variance=4)
    area.spawn(sp_sealed_pattern_room, 'pattern_guardian', count_min=1, count_max=1, respawn_minutes=14, respawn_variance=4)
    area.spawn(sp_pattern_threshold, 'stone_listening_frame', count_min=1, count_max=1, respawn_minutes=14, respawn_variance=4)
    area.spawn(sp_silent_frame_04, 'pattern_guardian', count_min=1, count_max=1, respawn_minutes=14, respawn_variance=4)
    area.spawn(dl_deep_listening_chamber, 'bell_echo', count_min=1, count_max=1, respawn_minutes=14, respawn_variance=4)
    area.spawn(dl_last_measure, 'stone_listening_frame', count_min=1, count_max=1, respawn_minutes=14, respawn_variance=4)
    area.spawn(dl_stone_breath_04, 'loose_oreling', count_min=1, count_max=2, respawn_minutes=14, respawn_variance=4)

    # Gathering pools
    area.gathering_pool('ore', ['sp_sealed_pattern_room', 'dl_deep_listening_chamber'], ['coldvein_stone', 'resonance_shard'], max_active=3, respawn_minutes=12, respawn_variance=4, tier_floor=2, tier_ceiling=3)
    area.gathering_pool('herb', ['dc_cool_moss_05', 'fv_mourning_bench_05'], ['windroot'], max_active=3, respawn_minutes=12, respawn_variance=4, tier_floor=2, tier_ceiling=2)
    area.gathering_pool('forage', ['bc_tuned_niche_03', 'dc_old_bucket_04'], ['bellcap_mushroom'], max_active=3, respawn_minutes=12, respawn_variance=4, tier_floor=2, tier_ceiling=2)
    area.gathering_pool('hide', ['dc_water_mark_03', 'ej_wrong_turn_bell'], ['minevermin_hide'], max_active=3, respawn_minutes=12, respawn_variance=4, tier_floor=1, tier_ceiling=1)
    area.gathering_pool('fish', ['dc_whitefish_rill', 'dc_dry_cistern'], ['cavern_whitefish'], max_active=3, respawn_minutes=12, respawn_variance=4, tier_floor=2, tier_ceiling=2)

    # Lore fragments
    area.lore_fragment(
        'thu_lore_names_before_patterns',
        fv_family_vault_walk,
        discovery_method='search',
        scholar_path='architecture',
        text='A family shelf has been repaired around an older pattern instead of over it, as if the current city learned to live beside mystery before trying to master it.',
        insight_gain=1,
    )
    area.lore_fragment(
        'thu_lore_deep_listening',
        dl_deep_listening_chamber,
        discovery_method='search',
        scholar_path='architecture',
        text='The deepest bell notation includes blank spaces preserved as carefully as notes, proof that Tremen sometimes records uncertainty as a civic duty.',
        insight_gain=1,
    )

    return area.build()
