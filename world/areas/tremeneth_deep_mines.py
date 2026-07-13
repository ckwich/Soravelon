"""Tremeneth Deep Mines -- Hub 3 exterior zone

Old Imperial mineworks beneath Tremen, now a dangerous mix of civic salvage, pressure seams, and unresolved extraction debts."""

from world.area_builder import AreaBuilder


def build():
    area = AreaBuilder('tremeneth_deep_mines')

    area.zone(
        name='Tremeneth Deep Mines',
        zone_type='underground',
        continent='varath',
        tier=3,
        region='tremeneth_mountains',
        faction_territory='warden',
        faction_presence=['ironblood', 'wardens', 'resonance', 'western_arcana'],
        world_x=34,
        world_y=45,
        world_radius=150,
    )

    # Materials
    area.material('greyteeth_iron', tier=2, terrain='stone', absorbed_property='stability', profession_bonus={'smithing': 0.1, 'mining': 0.05})
    area.material('pressure_quartz', tier=3, terrain='mine', absorbed_property='precision', profession_bonus={'alchemy': 0.1, 'mining': 0.05})
    area.material('resonance_shard', tier=3, terrain='deep stone', absorbed_property='attunement', profession_bonus={'alchemy': 0.1, 'scholarship': 0.05})
    area.material('bellcap_mushroom', tier=2, terrain='cavern', absorbed_property='focus', profession_bonus={'cooking': 0.1, 'foraging': 0.05})
    area.material('haul_rope_fiber', tier=1, terrain='roadside', absorbed_property='flexibility', profession_bonus={'engineering': 0.1, 'foraging': 0.05})
    area.material('blackwater_char', tier=3, terrain='water', absorbed_property='resilience', profession_bonus={'cooking': 0.1, 'fishing': 0.05})
    area.material('cavern_whitefish', tier=2, terrain='water', absorbed_property='quiet', profession_bonus={'cooking': 0.1, 'fishing': 0.05})
    area.material('minevermin_hide', tier=1, terrain='mine', absorbed_property='utility', profession_bonus={'smithing': 0.1, 'skinning': 0.05})

    # Rooms
    cg_claim_gate = area.room('cg_claim_gate', name='Claim Gate', desc='Claim Gate belongs to the Claim Gate, where crews count lamps and exits before they count ore. The claim gate is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    cg_lamp_check = area.room('cg_lamp_check', name='Lamp Check', desc='Lamp Check belongs to the Claim Gate, where crews count lamps and exits before they count ore. The lamp check is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    cg_helmet_tally_03 = area.room('cg_helmet_tally_03', name='Helmet Tally 03', desc='Helmet Tally 03 belongs to the Claim Gate, where crews count lamps and exits before they count ore. The helmet tally is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    cg_fresh_brace_04 = area.room('cg_fresh_brace_04', name='Fresh Brace 04', desc='Fresh Brace 04 belongs to the Claim Gate, where crews count lamps and exits before they count ore. The fresh brace is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    cg_ore_oath_05 = area.room('cg_ore_oath_05', name='Ore Oath 05', desc='Ore Oath 05 belongs to the Claim Gate, where crews count lamps and exits before they count ore. The ore oath is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    cg_claim_gate_06 = area.room('cg_claim_gate_06', name='Claim Gate 06', desc='Claim Gate 06 belongs to the Claim Gate, where crews count lamps and exits before they count ore. The claim gate is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    cg_lamp_check_07 = area.room('cg_lamp_check_07', name='Lamp Check 07', desc='Lamp Check 07 belongs to the Claim Gate, where crews count lamps and exits before they count ore. The lamp check is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    cg_helmet_tally_08 = area.room('cg_helmet_tally_08', name='Helmet Tally 08', desc='Helmet Tally 08 belongs to the Claim Gate, where crews count lamps and exits before they count ore. The helmet tally is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    cg_fresh_brace_09 = area.room('cg_fresh_brace_09', name='Fresh Brace 09', desc='Fresh Brace 09 belongs to the Claim Gate, where crews count lamps and exits before they count ore. The fresh brace is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    cg_ore_oath_10 = area.room('cg_ore_oath_10', name='Ore Oath 10', desc='Ore Oath 10 belongs to the Claim Gate, where crews count lamps and exits before they count ore. The ore oath is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    cg_claim_gate_11 = area.room('cg_claim_gate_11', name='Claim Gate 11', desc='Claim Gate 11 belongs to the Claim Gate, where crews count lamps and exits before they count ore. The claim gate is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    cg_lamp_check_12 = area.room('cg_lamp_check_12', name='Lamp Check 12', desc='Lamp Check 12 belongs to the Claim Gate, where crews count lamps and exits before they count ore. The lamp check is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    cg_helmet_tally_13 = area.room('cg_helmet_tally_13', name='Helmet Tally 13', desc='Helmet Tally 13 belongs to the Claim Gate, where crews count lamps and exits before they count ore. The helmet tally is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    cg_fresh_brace_14 = area.room('cg_fresh_brace_14', name='Fresh Brace 14', desc='Fresh Brace 14 belongs to the Claim Gate, where crews count lamps and exits before they count ore. The fresh brace is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    ro_requisition_office = area.room('ro_requisition_office', name='Requisition Office', desc='Requisition Office belongs to the Requisition Offices, where paper evidence makes Imperial extraction concrete and playable. The requisition desk is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='building', indoor=True)
    ro_stamped_shelf = area.room('ro_stamped_shelf', name='Stamped Shelf', desc='Stamped Shelf belongs to the Requisition Offices, where paper evidence makes Imperial extraction concrete and playable. The stamped shelf is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='building', indoor=True)
    ro_old_seal_03 = area.room('ro_old_seal_03', name='Old Seal 03', desc='Old Seal 03 belongs to the Requisition Offices, where paper evidence makes Imperial extraction concrete and playable. The old seal is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='building', indoor=True)
    ro_missing_wage_04 = area.room('ro_missing_wage_04', name='Missing Wage 04', desc='Missing Wage 04 belongs to the Requisition Offices, where paper evidence makes Imperial extraction concrete and playable. The missing wage is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='building', indoor=True)
    ro_ledger_bruise_05 = area.room('ro_ledger_bruise_05', name='Ledger Bruise 05', desc='Ledger Bruise 05 belongs to the Requisition Offices, where paper evidence makes Imperial extraction concrete and playable. The ledger bruise is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='building', indoor=True)
    ro_requisition_desk_06 = area.room('ro_requisition_desk_06', name='Requisition Desk 06', desc='Requisition Desk 06 belongs to the Requisition Offices, where paper evidence makes Imperial extraction concrete and playable. The requisition desk is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='building', indoor=True)
    ro_stamped_shelf_07 = area.room('ro_stamped_shelf_07', name='Stamped Shelf 07', desc='Stamped Shelf 07 belongs to the Requisition Offices, where paper evidence makes Imperial extraction concrete and playable. The stamped shelf is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='building', indoor=True)
    ro_old_seal_08 = area.room('ro_old_seal_08', name='Old Seal 08', desc='Old Seal 08 belongs to the Requisition Offices, where paper evidence makes Imperial extraction concrete and playable. The old seal is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='building', indoor=True)
    ro_missing_wage_09 = area.room('ro_missing_wage_09', name='Missing Wage 09', desc='Missing Wage 09 belongs to the Requisition Offices, where paper evidence makes Imperial extraction concrete and playable. The missing wage is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='building', indoor=True)
    ro_ledger_bruise_10 = area.room('ro_ledger_bruise_10', name='Ledger Bruise 10', desc='Ledger Bruise 10 belongs to the Requisition Offices, where paper evidence makes Imperial extraction concrete and playable. The ledger bruise is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='building', indoor=True)
    ro_requisition_desk_11 = area.room('ro_requisition_desk_11', name='Requisition Desk 11', desc='Requisition Desk 11 belongs to the Requisition Offices, where paper evidence makes Imperial extraction concrete and playable. The requisition desk is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='building', indoor=True)
    ro_stamped_shelf_12 = area.room('ro_stamped_shelf_12', name='Stamped Shelf 12', desc='Stamped Shelf 12 belongs to the Requisition Offices, where paper evidence makes Imperial extraction concrete and playable. The stamped shelf is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='building', indoor=True)
    ro_old_seal_13 = area.room('ro_old_seal_13', name='Old Seal 13', desc='Old Seal 13 belongs to the Requisition Offices, where paper evidence makes Imperial extraction concrete and playable. The old seal is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='building', indoor=True)
    ro_missing_wage_14 = area.room('ro_missing_wage_14', name='Missing Wage 14', desc='Missing Wage 14 belongs to the Requisition Offices, where paper evidence makes Imperial extraction concrete and playable. The missing wage is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='building', indoor=True)
    lh_lower_hoist = area.room('lh_lower_hoist', name='Lower Hoist', desc='Lower Hoist belongs to the Lower Hoist, where descent is negotiated with tools, crews, and stone. The lower hoist is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    lh_chain_tender_post = area.room('lh_chain_tender_post', name='Chain Tender Post', desc='Chain Tender Post belongs to the Lower Hoist, where descent is negotiated with tools, crews, and stone. The chain tender is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    lh_brake_wheel_03 = area.room('lh_brake_wheel_03', name='Brake Wheel 03', desc='Brake Wheel 03 belongs to the Lower Hoist, where descent is negotiated with tools, crews, and stone. The brake wheel is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    lh_echo_count_04 = area.room('lh_echo_count_04', name='Echo Count 04', desc='Echo Count 04 belongs to the Lower Hoist, where descent is negotiated with tools, crews, and stone. The echo count is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    lh_drop_warning_05 = area.room('lh_drop_warning_05', name='Drop Warning 05', desc='Drop Warning 05 belongs to the Lower Hoist, where descent is negotiated with tools, crews, and stone. The drop warning is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    lh_lower_hoist_06 = area.room('lh_lower_hoist_06', name='Lower Hoist 06', desc='Lower Hoist 06 belongs to the Lower Hoist, where descent is negotiated with tools, crews, and stone. The lower hoist is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    lh_chain_tender_07 = area.room('lh_chain_tender_07', name='Chain Tender 07', desc='Chain Tender 07 belongs to the Lower Hoist, where descent is negotiated with tools, crews, and stone. The chain tender is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    lh_brake_wheel_08 = area.room('lh_brake_wheel_08', name='Brake Wheel 08', desc='Brake Wheel 08 belongs to the Lower Hoist, where descent is negotiated with tools, crews, and stone. The brake wheel is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    lh_echo_count_09 = area.room('lh_echo_count_09', name='Echo Count 09', desc='Echo Count 09 belongs to the Lower Hoist, where descent is negotiated with tools, crews, and stone. The echo count is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    lh_drop_warning_10 = area.room('lh_drop_warning_10', name='Drop Warning 10', desc='Drop Warning 10 belongs to the Lower Hoist, where descent is negotiated with tools, crews, and stone. The drop warning is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    lh_lower_hoist_11 = area.room('lh_lower_hoist_11', name='Lower Hoist 11', desc='Lower Hoist 11 belongs to the Lower Hoist, where descent is negotiated with tools, crews, and stone. The lower hoist is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    lh_chain_tender_12 = area.room('lh_chain_tender_12', name='Chain Tender 12', desc='Chain Tender 12 belongs to the Lower Hoist, where descent is negotiated with tools, crews, and stone. The chain tender is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    lh_brake_wheel_13 = area.room('lh_brake_wheel_13', name='Brake Wheel 13', desc='Brake Wheel 13 belongs to the Lower Hoist, where descent is negotiated with tools, crews, and stone. The brake wheel is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    lh_echo_count_14 = area.room('lh_echo_count_14', name='Echo Count 14', desc='Echo Count 14 belongs to the Lower Hoist, where descent is negotiated with tools, crews, and stone. The echo count is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    pg_pressure_gallery = area.room('pg_pressure_gallery', name='Pressure Gallery', desc='Pressure Gallery belongs to the Pressure Galleries, where valuable materials demand careful methods. The pressure seam is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    pg_quartz_bloom = area.room('pg_quartz_bloom', name='Quartz Bloom', desc='Quartz Bloom belongs to the Pressure Galleries, where valuable materials demand careful methods. The quartz bloom is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    pg_brace_groan_03 = area.room('pg_brace_groan_03', name='Brace Groan 03', desc='Brace Groan 03 belongs to the Pressure Galleries, where valuable materials demand careful methods. The brace groan is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    pg_blue_spark_04 = area.room('pg_blue_spark_04', name='Blue Spark 04', desc='Blue Spark 04 belongs to the Pressure Galleries, where valuable materials demand careful methods. The blue spark is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    pg_safety_chalk_05 = area.room('pg_safety_chalk_05', name='Safety Chalk 05', desc='Safety Chalk 05 belongs to the Pressure Galleries, where valuable materials demand careful methods. The safety chalk is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    pg_pressure_seam_06 = area.room('pg_pressure_seam_06', name='Pressure Seam 06', desc='Pressure Seam 06 belongs to the Pressure Galleries, where valuable materials demand careful methods. The pressure seam is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    pg_quartz_bloom_07 = area.room('pg_quartz_bloom_07', name='Quartz Bloom 07', desc='Quartz Bloom 07 belongs to the Pressure Galleries, where valuable materials demand careful methods. The quartz bloom is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    pg_brace_groan_08 = area.room('pg_brace_groan_08', name='Brace Groan 08', desc='Brace Groan 08 belongs to the Pressure Galleries, where valuable materials demand careful methods. The brace groan is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    pg_blue_spark_09 = area.room('pg_blue_spark_09', name='Blue Spark 09', desc='Blue Spark 09 belongs to the Pressure Galleries, where valuable materials demand careful methods. The blue spark is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    pg_safety_chalk_10 = area.room('pg_safety_chalk_10', name='Safety Chalk 10', desc='Safety Chalk 10 belongs to the Pressure Galleries, where valuable materials demand careful methods. The safety chalk is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    pg_pressure_seam_11 = area.room('pg_pressure_seam_11', name='Pressure Seam 11', desc='Pressure Seam 11 belongs to the Pressure Galleries, where valuable materials demand careful methods. The pressure seam is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    pg_quartz_bloom_12 = area.room('pg_quartz_bloom_12', name='Quartz Bloom 12', desc='Quartz Bloom 12 belongs to the Pressure Galleries, where valuable materials demand careful methods. The quartz bloom is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    pg_brace_groan_13 = area.room('pg_brace_groan_13', name='Brace Groan 13', desc='Brace Groan 13 belongs to the Pressure Galleries, where valuable materials demand careful methods. The brace groan is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    pg_blue_spark_14 = area.room('pg_blue_spark_14', name='Blue Spark 14', desc='Blue Spark 14 belongs to the Pressure Galleries, where valuable materials demand careful methods. The blue spark is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    bs_blackwater_sump = area.room('bs_blackwater_sump', name='Blackwater Sump', desc='Blackwater Sump belongs to the Blackwater Sumps, where water is food source, hazard, and route clue at once. The blackwater sump is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='cave', indoor=True)
    bs_lamp_reflection = area.room('bs_lamp_reflection', name='Lamp Reflection', desc='Lamp Reflection belongs to the Blackwater Sumps, where water is food source, hazard, and route clue at once. The lamp reflection is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='cave', indoor=True)
    bs_eel_ripple_03 = area.room('bs_eel_ripple_03', name='Eel Ripple 03', desc='Eel Ripple 03 belongs to the Blackwater Sumps, where water is food source, hazard, and route clue at once. The eel ripple is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='cave', indoor=True)
    bs_slick_rail_04 = area.room('bs_slick_rail_04', name='Slick Rail 04', desc='Slick Rail 04 belongs to the Blackwater Sumps, where water is food source, hazard, and route clue at once. The slick rail is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='cave', indoor=True)
    bs_sump_hook_05 = area.room('bs_sump_hook_05', name='Sump Hook 05', desc='Sump Hook 05 belongs to the Blackwater Sumps, where water is food source, hazard, and route clue at once. The sump hook is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='cave', indoor=True)
    bs_blackwater_sump_06 = area.room('bs_blackwater_sump_06', name='Blackwater Sump 06', desc='Blackwater Sump 06 belongs to the Blackwater Sumps, where water is food source, hazard, and route clue at once. The blackwater sump is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='cave', indoor=True)
    bs_lamp_reflection_07 = area.room('bs_lamp_reflection_07', name='Lamp Reflection 07', desc='Lamp Reflection 07 belongs to the Blackwater Sumps, where water is food source, hazard, and route clue at once. The lamp reflection is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='cave', indoor=True)
    bs_eel_ripple_08 = area.room('bs_eel_ripple_08', name='Eel Ripple 08', desc='Eel Ripple 08 belongs to the Blackwater Sumps, where water is food source, hazard, and route clue at once. The eel ripple is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='cave', indoor=True)
    bs_slick_rail_09 = area.room('bs_slick_rail_09', name='Slick Rail 09', desc='Slick Rail 09 belongs to the Blackwater Sumps, where water is food source, hazard, and route clue at once. The slick rail is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='cave', indoor=True)
    bs_sump_hook_10 = area.room('bs_sump_hook_10', name='Sump Hook 10', desc='Sump Hook 10 belongs to the Blackwater Sumps, where water is food source, hazard, and route clue at once. The sump hook is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='cave', indoor=True)
    bs_blackwater_sump_11 = area.room('bs_blackwater_sump_11', name='Blackwater Sump 11', desc='Blackwater Sump 11 belongs to the Blackwater Sumps, where water is food source, hazard, and route clue at once. The blackwater sump is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='cave', indoor=True)
    bs_lamp_reflection_12 = area.room('bs_lamp_reflection_12', name='Lamp Reflection 12', desc='Lamp Reflection 12 belongs to the Blackwater Sumps, where water is food source, hazard, and route clue at once. The lamp reflection is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='cave', indoor=True)
    bs_eel_ripple_13 = area.room('bs_eel_ripple_13', name='Eel Ripple 13', desc='Eel Ripple 13 belongs to the Blackwater Sumps, where water is food source, hazard, and route clue at once. The eel ripple is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='cave', indoor=True)
    bs_slick_rail_14 = area.room('bs_slick_rail_14', name='Slick Rail 14', desc='Slick Rail 14 belongs to the Blackwater Sumps, where water is food source, hazard, and route clue at once. The slick rail is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='cave', indoor=True)
    bc_broken_cart_run = area.room('bc_broken_cart_run', name='Broken Cart Run', desc='Broken Cart Run belongs to the Broken Cart Runs, where salvage disputes have rails, injuries, and witnesses. The broken cart is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    bc_split_axle = area.room('bc_split_axle', name='Split Axle', desc='Split Axle belongs to the Broken Cart Runs, where salvage disputes have rails, injuries, and witnesses. The split axle is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    bc_stolen_rail_03 = area.room('bc_stolen_rail_03', name='Stolen Rail 03', desc='Stolen Rail 03 belongs to the Broken Cart Runs, where salvage disputes have rails, injuries, and witnesses. The stolen rail is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    bc_claim_scar_04 = area.room('bc_claim_scar_04', name='Claim Scar 04', desc='Claim Scar 04 belongs to the Broken Cart Runs, where salvage disputes have rails, injuries, and witnesses. The claim scar is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    bc_dropped_boot_05 = area.room('bc_dropped_boot_05', name='Dropped Boot 05', desc='Dropped Boot 05 belongs to the Broken Cart Runs, where salvage disputes have rails, injuries, and witnesses. The dropped boot is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    bc_broken_cart_06 = area.room('bc_broken_cart_06', name='Broken Cart 06', desc='Broken Cart 06 belongs to the Broken Cart Runs, where salvage disputes have rails, injuries, and witnesses. The broken cart is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    bc_split_axle_07 = area.room('bc_split_axle_07', name='Split Axle 07', desc='Split Axle 07 belongs to the Broken Cart Runs, where salvage disputes have rails, injuries, and witnesses. The split axle is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    bc_stolen_rail_08 = area.room('bc_stolen_rail_08', name='Stolen Rail 08', desc='Stolen Rail 08 belongs to the Broken Cart Runs, where salvage disputes have rails, injuries, and witnesses. The stolen rail is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    bc_claim_scar_09 = area.room('bc_claim_scar_09', name='Claim Scar 09', desc='Claim Scar 09 belongs to the Broken Cart Runs, where salvage disputes have rails, injuries, and witnesses. The claim scar is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    bc_dropped_boot_10 = area.room('bc_dropped_boot_10', name='Dropped Boot 10', desc='Dropped Boot 10 belongs to the Broken Cart Runs, where salvage disputes have rails, injuries, and witnesses. The dropped boot is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    bc_broken_cart_11 = area.room('bc_broken_cart_11', name='Broken Cart 11', desc='Broken Cart 11 belongs to the Broken Cart Runs, where salvage disputes have rails, injuries, and witnesses. The broken cart is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    bc_split_axle_12 = area.room('bc_split_axle_12', name='Split Axle 12', desc='Split Axle 12 belongs to the Broken Cart Runs, where salvage disputes have rails, injuries, and witnesses. The split axle is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    bc_stolen_rail_13 = area.room('bc_stolen_rail_13', name='Stolen Rail 13', desc='Stolen Rail 13 belongs to the Broken Cart Runs, where salvage disputes have rails, injuries, and witnesses. The stolen rail is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    bc_claim_scar_14 = area.room('bc_claim_scar_14', name='Claim Scar 14', desc='Claim Scar 14 belongs to the Broken Cart Runs, where salvage disputes have rails, injuries, and witnesses. The claim scar is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    si_sealed_imperial_cut = area.room('si_sealed_imperial_cut', name='Sealed Imperial Cut', desc='Sealed Imperial Cut belongs to the Sealed Imperial Cut, where old extraction is visible without becoming an instant unlock. The sealed cut is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    si_red_wax_mark = area.room('si_red_wax_mark', name='Red Wax Mark', desc='Red Wax Mark belongs to the Sealed Imperial Cut, where old extraction is visible without becoming an instant unlock. The red wax is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    si_old_order_03 = area.room('si_old_order_03', name='Old Order 03', desc='Old Order 03 belongs to the Sealed Imperial Cut, where old extraction is visible without becoming an instant unlock. The old order is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    si_blocked_shaft_04 = area.room('si_blocked_shaft_04', name='Blocked Shaft 04', desc='Blocked Shaft 04 belongs to the Sealed Imperial Cut, where old extraction is visible without becoming an instant unlock. The blocked shaft is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    si_quiet_pick_05 = area.room('si_quiet_pick_05', name='Quiet Pick 05', desc='Quiet Pick 05 belongs to the Sealed Imperial Cut, where old extraction is visible without becoming an instant unlock. The quiet pick is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    si_sealed_cut_06 = area.room('si_sealed_cut_06', name='Sealed Cut 06', desc='Sealed Cut 06 belongs to the Sealed Imperial Cut, where old extraction is visible without becoming an instant unlock. The sealed cut is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    si_red_wax_07 = area.room('si_red_wax_07', name='Red Wax 07', desc='Red Wax 07 belongs to the Sealed Imperial Cut, where old extraction is visible without becoming an instant unlock. The red wax is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    si_old_order_08 = area.room('si_old_order_08', name='Old Order 08', desc='Old Order 08 belongs to the Sealed Imperial Cut, where old extraction is visible without becoming an instant unlock. The old order is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    si_blocked_shaft_09 = area.room('si_blocked_shaft_09', name='Blocked Shaft 09', desc='Blocked Shaft 09 belongs to the Sealed Imperial Cut, where old extraction is visible without becoming an instant unlock. The blocked shaft is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    si_quiet_pick_10 = area.room('si_quiet_pick_10', name='Quiet Pick 10', desc='Quiet Pick 10 belongs to the Sealed Imperial Cut, where old extraction is visible without becoming an instant unlock. The quiet pick is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    si_sealed_cut_11 = area.room('si_sealed_cut_11', name='Sealed Cut 11', desc='Sealed Cut 11 belongs to the Sealed Imperial Cut, where old extraction is visible without becoming an instant unlock. The sealed cut is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    si_red_wax_12 = area.room('si_red_wax_12', name='Red Wax 12', desc='Red Wax 12 belongs to the Sealed Imperial Cut, where old extraction is visible without becoming an instant unlock. The red wax is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    si_old_order_13 = area.room('si_old_order_13', name='Old Order 13', desc='Old Order 13 belongs to the Sealed Imperial Cut, where old extraction is visible without becoming an instant unlock. The old order is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    si_blocked_shaft_14 = area.room('si_blocked_shaft_14', name='Blocked Shaft 14', desc='Blocked Shaft 14 belongs to the Sealed Imperial Cut, where old extraction is visible without becoming an instant unlock. The blocked shaft is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    rs_resonance_seam = area.room('rs_resonance_seam', name='Resonance Seam', desc='Resonance Seam belongs to the Old Resonance Seam, where node-adjacent mystery invites restraint before theory. The resonance seam is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    rs_listening_pin = area.room('rs_listening_pin', name='Listening Pin', desc='Listening Pin belongs to the Old Resonance Seam, where node-adjacent mystery invites restraint before theory. The listening pin is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    rs_hummed_dust_03 = area.room('rs_hummed_dust_03', name='Hummed Dust 03', desc='Hummed Dust 03 belongs to the Old Resonance Seam, where node-adjacent mystery invites restraint before theory. The hummed dust is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    rs_careful_sample_04 = area.room('rs_careful_sample_04', name='Careful Sample 04', desc='Careful Sample 04 belongs to the Old Resonance Seam, where node-adjacent mystery invites restraint before theory. The careful sample is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    rs_unsteady_note_05 = area.room('rs_unsteady_note_05', name='Unsteady Note 05', desc='Unsteady Note 05 belongs to the Old Resonance Seam, where node-adjacent mystery invites restraint before theory. The unsteady note is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    rs_resonance_seam_06 = area.room('rs_resonance_seam_06', name='Resonance Seam 06', desc='Resonance Seam 06 belongs to the Old Resonance Seam, where node-adjacent mystery invites restraint before theory. The resonance seam is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    rs_listening_pin_07 = area.room('rs_listening_pin_07', name='Listening Pin 07', desc='Listening Pin 07 belongs to the Old Resonance Seam, where node-adjacent mystery invites restraint before theory. The listening pin is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    rs_hummed_dust_08 = area.room('rs_hummed_dust_08', name='Hummed Dust 08', desc='Hummed Dust 08 belongs to the Old Resonance Seam, where node-adjacent mystery invites restraint before theory. The hummed dust is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    rs_careful_sample_09 = area.room('rs_careful_sample_09', name='Careful Sample 09', desc='Careful Sample 09 belongs to the Old Resonance Seam, where node-adjacent mystery invites restraint before theory. The careful sample is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    rs_unsteady_note_10 = area.room('rs_unsteady_note_10', name='Unsteady Note 10', desc='Unsteady Note 10 belongs to the Old Resonance Seam, where node-adjacent mystery invites restraint before theory. The unsteady note is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    rs_resonance_seam_11 = area.room('rs_resonance_seam_11', name='Resonance Seam 11', desc='Resonance Seam 11 belongs to the Old Resonance Seam, where node-adjacent mystery invites restraint before theory. The resonance seam is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    rs_listening_pin_12 = area.room('rs_listening_pin_12', name='Listening Pin 12', desc='Listening Pin 12 belongs to the Old Resonance Seam, where node-adjacent mystery invites restraint before theory. The listening pin is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    rs_hummed_dust_13 = area.room('rs_hummed_dust_13', name='Hummed Dust 13', desc='Hummed Dust 13 belongs to the Old Resonance Seam, where node-adjacent mystery invites restraint before theory. The hummed dust is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)
    rs_careful_sample_14 = area.room('rs_careful_sample_14', name='Careful Sample 14', desc='Careful Sample 14 belongs to the Old Resonance Seam, where node-adjacent mystery invites restraint before theory. The careful sample is not decoration; it teaches route sense, local memory, and the practical caution that keeps Tremeneth stories grounded in play. Old stone, half-dwarf stewardship, and signs of Imperial extraction all remain visible here without turning mystery into an answer key.', room_type='underground', indoor=True)

    # Local exits
    area.exit(cg_claim_gate, cg_lamp_check, 'east')
    area.exit(cg_lamp_check, cg_claim_gate, 'west')
    area.exit(cg_lamp_check, cg_helmet_tally_03, 'east')
    area.exit(cg_helmet_tally_03, cg_lamp_check, 'west')
    area.exit(cg_helmet_tally_03, cg_fresh_brace_04, 'east')
    area.exit(cg_fresh_brace_04, cg_helmet_tally_03, 'west')
    area.exit(cg_fresh_brace_04, cg_ore_oath_05, 'east')
    area.exit(cg_ore_oath_05, cg_fresh_brace_04, 'west')
    area.exit(cg_ore_oath_05, cg_claim_gate_06, 'east')
    area.exit(cg_claim_gate_06, cg_ore_oath_05, 'west')
    area.exit(cg_claim_gate_06, cg_lamp_check_07, 'east')
    area.exit(cg_lamp_check_07, cg_claim_gate_06, 'west')
    area.exit(cg_lamp_check_07, cg_helmet_tally_08, 'east')
    area.exit(cg_helmet_tally_08, cg_lamp_check_07, 'west')
    area.exit(cg_helmet_tally_08, cg_fresh_brace_09, 'east')
    area.exit(cg_fresh_brace_09, cg_helmet_tally_08, 'west')
    area.exit(cg_fresh_brace_09, cg_ore_oath_10, 'east')
    area.exit(cg_ore_oath_10, cg_fresh_brace_09, 'west')
    area.exit(cg_ore_oath_10, cg_claim_gate_11, 'east')
    area.exit(cg_claim_gate_11, cg_ore_oath_10, 'west')
    area.exit(cg_claim_gate_11, cg_lamp_check_12, 'east')
    area.exit(cg_lamp_check_12, cg_claim_gate_11, 'west')
    area.exit(cg_lamp_check_12, cg_helmet_tally_13, 'east')
    area.exit(cg_helmet_tally_13, cg_lamp_check_12, 'west')
    area.exit(cg_helmet_tally_13, cg_fresh_brace_14, 'east')
    area.exit(cg_fresh_brace_14, cg_helmet_tally_13, 'west')
    area.exit(ro_requisition_office, ro_stamped_shelf, 'east')
    area.exit(ro_stamped_shelf, ro_requisition_office, 'west')
    area.exit(ro_stamped_shelf, ro_old_seal_03, 'east')
    area.exit(ro_old_seal_03, ro_stamped_shelf, 'west')
    area.exit(ro_old_seal_03, ro_missing_wage_04, 'east')
    area.exit(ro_missing_wage_04, ro_old_seal_03, 'west')
    area.exit(ro_missing_wage_04, ro_ledger_bruise_05, 'east')
    area.exit(ro_ledger_bruise_05, ro_missing_wage_04, 'west')
    area.exit(ro_ledger_bruise_05, ro_requisition_desk_06, 'east')
    area.exit(ro_requisition_desk_06, ro_ledger_bruise_05, 'west')
    area.exit(ro_requisition_desk_06, ro_stamped_shelf_07, 'east')
    area.exit(ro_stamped_shelf_07, ro_requisition_desk_06, 'west')
    area.exit(ro_stamped_shelf_07, ro_old_seal_08, 'east')
    area.exit(ro_old_seal_08, ro_stamped_shelf_07, 'west')
    area.exit(ro_old_seal_08, ro_missing_wage_09, 'east')
    area.exit(ro_missing_wage_09, ro_old_seal_08, 'west')
    area.exit(ro_missing_wage_09, ro_ledger_bruise_10, 'east')
    area.exit(ro_ledger_bruise_10, ro_missing_wage_09, 'west')
    area.exit(ro_ledger_bruise_10, ro_requisition_desk_11, 'east')
    area.exit(ro_requisition_desk_11, ro_ledger_bruise_10, 'west')
    area.exit(ro_requisition_desk_11, ro_stamped_shelf_12, 'east')
    area.exit(ro_stamped_shelf_12, ro_requisition_desk_11, 'west')
    area.exit(ro_stamped_shelf_12, ro_old_seal_13, 'east')
    area.exit(ro_old_seal_13, ro_stamped_shelf_12, 'west')
    area.exit(ro_old_seal_13, ro_missing_wage_14, 'east')
    area.exit(ro_missing_wage_14, ro_old_seal_13, 'west')
    area.exit(lh_lower_hoist, lh_chain_tender_post, 'east')
    area.exit(lh_chain_tender_post, lh_lower_hoist, 'west')
    area.exit(lh_chain_tender_post, lh_brake_wheel_03, 'east')
    area.exit(lh_brake_wheel_03, lh_chain_tender_post, 'west')
    area.exit(lh_brake_wheel_03, lh_echo_count_04, 'east')
    area.exit(lh_echo_count_04, lh_brake_wheel_03, 'west')
    area.exit(lh_echo_count_04, lh_drop_warning_05, 'east')
    area.exit(lh_drop_warning_05, lh_echo_count_04, 'west')
    area.exit(lh_drop_warning_05, lh_lower_hoist_06, 'east')
    area.exit(lh_lower_hoist_06, lh_drop_warning_05, 'west')
    area.exit(lh_lower_hoist_06, lh_chain_tender_07, 'east')
    area.exit(lh_chain_tender_07, lh_lower_hoist_06, 'west')
    area.exit(lh_chain_tender_07, lh_brake_wheel_08, 'east')
    area.exit(lh_brake_wheel_08, lh_chain_tender_07, 'west')
    area.exit(lh_brake_wheel_08, lh_echo_count_09, 'east')
    area.exit(lh_echo_count_09, lh_brake_wheel_08, 'west')
    area.exit(lh_echo_count_09, lh_drop_warning_10, 'east')
    area.exit(lh_drop_warning_10, lh_echo_count_09, 'west')
    area.exit(lh_drop_warning_10, lh_lower_hoist_11, 'east')
    area.exit(lh_lower_hoist_11, lh_drop_warning_10, 'west')
    area.exit(lh_lower_hoist_11, lh_chain_tender_12, 'east')
    area.exit(lh_chain_tender_12, lh_lower_hoist_11, 'west')
    area.exit(lh_chain_tender_12, lh_brake_wheel_13, 'east')
    area.exit(lh_brake_wheel_13, lh_chain_tender_12, 'west')
    area.exit(lh_brake_wheel_13, lh_echo_count_14, 'east')
    area.exit(lh_echo_count_14, lh_brake_wheel_13, 'west')
    area.exit(pg_pressure_gallery, pg_quartz_bloom, 'east')
    area.exit(pg_quartz_bloom, pg_pressure_gallery, 'west')
    area.exit(pg_quartz_bloom, pg_brace_groan_03, 'east')
    area.exit(pg_brace_groan_03, pg_quartz_bloom, 'west')
    area.exit(pg_brace_groan_03, pg_blue_spark_04, 'east')
    area.exit(pg_blue_spark_04, pg_brace_groan_03, 'west')
    area.exit(pg_blue_spark_04, pg_safety_chalk_05, 'east')
    area.exit(pg_safety_chalk_05, pg_blue_spark_04, 'west')
    area.exit(pg_safety_chalk_05, pg_pressure_seam_06, 'east')
    area.exit(pg_pressure_seam_06, pg_safety_chalk_05, 'west')
    area.exit(pg_pressure_seam_06, pg_quartz_bloom_07, 'east')
    area.exit(pg_quartz_bloom_07, pg_pressure_seam_06, 'west')
    area.exit(pg_quartz_bloom_07, pg_brace_groan_08, 'east')
    area.exit(pg_brace_groan_08, pg_quartz_bloom_07, 'west')
    area.exit(pg_brace_groan_08, pg_blue_spark_09, 'east')
    area.exit(pg_blue_spark_09, pg_brace_groan_08, 'west')
    area.exit(pg_blue_spark_09, pg_safety_chalk_10, 'east')
    area.exit(pg_safety_chalk_10, pg_blue_spark_09, 'west')
    area.exit(pg_safety_chalk_10, pg_pressure_seam_11, 'east')
    area.exit(pg_pressure_seam_11, pg_safety_chalk_10, 'west')
    area.exit(pg_pressure_seam_11, pg_quartz_bloom_12, 'east')
    area.exit(pg_quartz_bloom_12, pg_pressure_seam_11, 'west')
    area.exit(pg_quartz_bloom_12, pg_brace_groan_13, 'east')
    area.exit(pg_brace_groan_13, pg_quartz_bloom_12, 'west')
    area.exit(pg_brace_groan_13, pg_blue_spark_14, 'east')
    area.exit(pg_blue_spark_14, pg_brace_groan_13, 'west')
    area.exit(bs_blackwater_sump, bs_lamp_reflection, 'east')
    area.exit(bs_lamp_reflection, bs_blackwater_sump, 'west')
    area.exit(bs_lamp_reflection, bs_eel_ripple_03, 'east')
    area.exit(bs_eel_ripple_03, bs_lamp_reflection, 'west')
    area.exit(bs_eel_ripple_03, bs_slick_rail_04, 'east')
    area.exit(bs_slick_rail_04, bs_eel_ripple_03, 'west')
    area.exit(bs_slick_rail_04, bs_sump_hook_05, 'east')
    area.exit(bs_sump_hook_05, bs_slick_rail_04, 'west')
    area.exit(bs_sump_hook_05, bs_blackwater_sump_06, 'east')
    area.exit(bs_blackwater_sump_06, bs_sump_hook_05, 'west')
    area.exit(bs_blackwater_sump_06, bs_lamp_reflection_07, 'east')
    area.exit(bs_lamp_reflection_07, bs_blackwater_sump_06, 'west')
    area.exit(bs_lamp_reflection_07, bs_eel_ripple_08, 'east')
    area.exit(bs_eel_ripple_08, bs_lamp_reflection_07, 'west')
    area.exit(bs_eel_ripple_08, bs_slick_rail_09, 'east')
    area.exit(bs_slick_rail_09, bs_eel_ripple_08, 'west')
    area.exit(bs_slick_rail_09, bs_sump_hook_10, 'east')
    area.exit(bs_sump_hook_10, bs_slick_rail_09, 'west')
    area.exit(bs_sump_hook_10, bs_blackwater_sump_11, 'east')
    area.exit(bs_blackwater_sump_11, bs_sump_hook_10, 'west')
    area.exit(bs_blackwater_sump_11, bs_lamp_reflection_12, 'east')
    area.exit(bs_lamp_reflection_12, bs_blackwater_sump_11, 'west')
    area.exit(bs_lamp_reflection_12, bs_eel_ripple_13, 'east')
    area.exit(bs_eel_ripple_13, bs_lamp_reflection_12, 'west')
    area.exit(bs_eel_ripple_13, bs_slick_rail_14, 'east')
    area.exit(bs_slick_rail_14, bs_eel_ripple_13, 'west')
    area.exit(bc_broken_cart_run, bc_split_axle, 'east')
    area.exit(bc_split_axle, bc_broken_cart_run, 'west')
    area.exit(bc_split_axle, bc_stolen_rail_03, 'east')
    area.exit(bc_stolen_rail_03, bc_split_axle, 'west')
    area.exit(bc_stolen_rail_03, bc_claim_scar_04, 'east')
    area.exit(bc_claim_scar_04, bc_stolen_rail_03, 'west')
    area.exit(bc_claim_scar_04, bc_dropped_boot_05, 'east')
    area.exit(bc_dropped_boot_05, bc_claim_scar_04, 'west')
    area.exit(bc_dropped_boot_05, bc_broken_cart_06, 'east')
    area.exit(bc_broken_cart_06, bc_dropped_boot_05, 'west')
    area.exit(bc_broken_cart_06, bc_split_axle_07, 'east')
    area.exit(bc_split_axle_07, bc_broken_cart_06, 'west')
    area.exit(bc_split_axle_07, bc_stolen_rail_08, 'east')
    area.exit(bc_stolen_rail_08, bc_split_axle_07, 'west')
    area.exit(bc_stolen_rail_08, bc_claim_scar_09, 'east')
    area.exit(bc_claim_scar_09, bc_stolen_rail_08, 'west')
    area.exit(bc_claim_scar_09, bc_dropped_boot_10, 'east')
    area.exit(bc_dropped_boot_10, bc_claim_scar_09, 'west')
    area.exit(bc_dropped_boot_10, bc_broken_cart_11, 'east')
    area.exit(bc_broken_cart_11, bc_dropped_boot_10, 'west')
    area.exit(bc_broken_cart_11, bc_split_axle_12, 'east')
    area.exit(bc_split_axle_12, bc_broken_cart_11, 'west')
    area.exit(bc_split_axle_12, bc_stolen_rail_13, 'east')
    area.exit(bc_stolen_rail_13, bc_split_axle_12, 'west')
    area.exit(bc_stolen_rail_13, bc_claim_scar_14, 'east')
    area.exit(bc_claim_scar_14, bc_stolen_rail_13, 'west')
    area.exit(si_sealed_imperial_cut, si_red_wax_mark, 'east')
    area.exit(si_red_wax_mark, si_sealed_imperial_cut, 'west')
    area.exit(si_red_wax_mark, si_old_order_03, 'east')
    area.exit(si_old_order_03, si_red_wax_mark, 'west')
    area.exit(si_old_order_03, si_blocked_shaft_04, 'east')
    area.exit(si_blocked_shaft_04, si_old_order_03, 'west')
    area.exit(si_blocked_shaft_04, si_quiet_pick_05, 'east')
    area.exit(si_quiet_pick_05, si_blocked_shaft_04, 'west')
    area.exit(si_quiet_pick_05, si_sealed_cut_06, 'east')
    area.exit(si_sealed_cut_06, si_quiet_pick_05, 'west')
    area.exit(si_sealed_cut_06, si_red_wax_07, 'east')
    area.exit(si_red_wax_07, si_sealed_cut_06, 'west')
    area.exit(si_red_wax_07, si_old_order_08, 'east')
    area.exit(si_old_order_08, si_red_wax_07, 'west')
    area.exit(si_old_order_08, si_blocked_shaft_09, 'east')
    area.exit(si_blocked_shaft_09, si_old_order_08, 'west')
    area.exit(si_blocked_shaft_09, si_quiet_pick_10, 'east')
    area.exit(si_quiet_pick_10, si_blocked_shaft_09, 'west')
    area.exit(si_quiet_pick_10, si_sealed_cut_11, 'east')
    area.exit(si_sealed_cut_11, si_quiet_pick_10, 'west')
    area.exit(si_sealed_cut_11, si_red_wax_12, 'east')
    area.exit(si_red_wax_12, si_sealed_cut_11, 'west')
    area.exit(si_red_wax_12, si_old_order_13, 'east')
    area.exit(si_old_order_13, si_red_wax_12, 'west')
    area.exit(si_old_order_13, si_blocked_shaft_14, 'east')
    area.exit(si_blocked_shaft_14, si_old_order_13, 'west')
    area.exit(rs_resonance_seam, rs_listening_pin, 'east')
    area.exit(rs_listening_pin, rs_resonance_seam, 'west')
    area.exit(rs_listening_pin, rs_hummed_dust_03, 'east')
    area.exit(rs_hummed_dust_03, rs_listening_pin, 'west')
    area.exit(rs_hummed_dust_03, rs_careful_sample_04, 'east')
    area.exit(rs_careful_sample_04, rs_hummed_dust_03, 'west')
    area.exit(rs_careful_sample_04, rs_unsteady_note_05, 'east')
    area.exit(rs_unsteady_note_05, rs_careful_sample_04, 'west')
    area.exit(rs_unsteady_note_05, rs_resonance_seam_06, 'east')
    area.exit(rs_resonance_seam_06, rs_unsteady_note_05, 'west')
    area.exit(rs_resonance_seam_06, rs_listening_pin_07, 'east')
    area.exit(rs_listening_pin_07, rs_resonance_seam_06, 'west')
    area.exit(rs_listening_pin_07, rs_hummed_dust_08, 'east')
    area.exit(rs_hummed_dust_08, rs_listening_pin_07, 'west')
    area.exit(rs_hummed_dust_08, rs_careful_sample_09, 'east')
    area.exit(rs_careful_sample_09, rs_hummed_dust_08, 'west')
    area.exit(rs_careful_sample_09, rs_unsteady_note_10, 'east')
    area.exit(rs_unsteady_note_10, rs_careful_sample_09, 'west')
    area.exit(rs_unsteady_note_10, rs_resonance_seam_11, 'east')
    area.exit(rs_resonance_seam_11, rs_unsteady_note_10, 'west')
    area.exit(rs_resonance_seam_11, rs_listening_pin_12, 'east')
    area.exit(rs_listening_pin_12, rs_resonance_seam_11, 'west')
    area.exit(rs_listening_pin_12, rs_hummed_dust_13, 'east')
    area.exit(rs_hummed_dust_13, rs_listening_pin_12, 'west')
    area.exit(rs_hummed_dust_13, rs_careful_sample_14, 'east')
    area.exit(rs_careful_sample_14, rs_hummed_dust_13, 'west')
    area.exit(cg_fresh_brace_14, ro_requisition_office, 'north')
    area.exit(ro_requisition_office, cg_fresh_brace_14, 'south')
    area.exit(ro_missing_wage_14, lh_lower_hoist, 'north')
    area.exit(lh_lower_hoist, ro_missing_wage_14, 'south')
    area.exit(lh_echo_count_14, pg_pressure_gallery, 'north')
    area.exit(pg_pressure_gallery, lh_echo_count_14, 'south')
    area.exit(pg_blue_spark_14, bs_blackwater_sump, 'north')
    area.exit(bs_blackwater_sump, pg_blue_spark_14, 'south')
    area.exit(bs_slick_rail_14, bc_broken_cart_run, 'north')
    area.exit(bc_broken_cart_run, bs_slick_rail_14, 'south')
    area.exit(bc_claim_scar_14, si_sealed_imperial_cut, 'north')
    area.exit(si_sealed_imperial_cut, bc_claim_scar_14, 'south')
    area.exit(si_blocked_shaft_14, rs_resonance_seam, 'north')
    area.exit(rs_resonance_seam, si_blocked_shaft_14, 'south')
    area.exit(cg_claim_gate, 'tremen:fh_mine_lift', 'up')

    # NPCs
    _mine_steward = area.npc(cg_claim_gate, 'npc_mine_steward_bran', name='Mine Steward Bran', faction='ironblood', dialogue={'greeting_tiers': {"neutral": 'Bran checks lamps with a tenderness he does not show people until later.'}, 'topics': {'claims': 'A claim is a promise to leave a crew alive after the ore is gone.'}, 'base_hints': []})
    _requisitioner = area.npc(ro_requisition_office, 'npc_requisitioner_sava', name='Requisitioner Sava', faction='ironblood', dialogue={'greeting_tiers': {"neutral": 'Sava has dust on her sleeves and fury arranged into neat piles.'}, 'topics': {'records': 'Every missing wage had a stamp. That is what makes it useful now.'}, 'base_hints': []})
    _blackwater_cook = area.npc(bs_blackwater_sump, 'npc_blackwater_cook_doma', name='Blackwater Cook Doma', faction=None, dialogue={'greeting_tiers': {"neutral": 'Doma keeps a hook, a kettle, and a sharp opinion about sump fish.'}, 'topics': {'sump': 'If the water feeds us, we respect it. If it bites us, we respect it more.'}, 'base_hints': []})
    _safety_captain = area.npc(lh_lower_hoist, 'npc_safety_captain_rill', name='Safety Captain Rill', faction='wardens', dialogue={'greeting_tiers': {"neutral": 'Rill marks unsafe braces with a calm that makes everyone else quieter.'}, 'topics': {'safety': 'The mine can be brave after it is braced.'}, 'base_hints': []})
    _mapper = area.npc(rs_resonance_seam, 'npc_underhall_mapper_vaun', name='Underhall Mapper Vaun', faction='resonance', dialogue={'greeting_tiers': {"neutral": 'Vaun keeps his maps rolled in different directions so the newest one never lies flat.'}, 'topics': {'seam': 'This line points toward the underhalls, which is not the same as permission.'}, 'base_hints': []})

    # Quest item templates
    area.item('tdm_requisition_bundle', key='requisition bundle', item_type='item', weight=0.5, rarity='normal', desc='A bundle of old requisition slips that show ore, wages, and injuries refusing to add up.', value=0, is_quest_item=True)
    area.item('tdm_seam_tracing', key='resonance seam tracing', item_type='item', weight=0.5, rarity='normal', desc='A soot tracing of a seam pattern that seems to continue toward older underhall stone.', value=0, is_quest_item=True)

    # Quests
    area.quest(
        'tdm_q_requisition_echo',
        name='Requisition Echo',
        description='Sava asks you to match old requisitions with current mine rooms, making paper evidence lead you through the working mine instead of sitting in a lore corner.',
        quest_type='investigation',
        quest_giver='npc_requisitioner_sava',
        objectives=[{'type': 'investigate', 'target': 'ro_requisition_office', 'count': 1}, {'type': 'visit', 'target': 'pg_pressure_gallery', 'count': 1}, {'type': 'deliver', 'target': 'npc_mine_steward_bran', 'count': 1, 'item_tag': 'tdm_requisition_bundle'}],
        rewards=[{'action_type': 'give_scales', 'amount': 42}, {'action_type': 'give_skill_xp', 'skill_id': 'scholarship', 'count': 12}],
        next_quest_id=None,
        prerequisite_quests=['tre_q_mine_reckoning'],
        can_share=True,
        consequence_small='Sava pins the matched requisitions under a clear weight so crews can point to proof instead of rumor.',
    )
    area.quest(
        'tdm_q_sump_lamps',
        name='Lamps In Blackwater',
        description='Doma needs food and safer lamp marks around the sump, turning fishing into mine logistics with teeth nearby.',
        quest_type='gather',
        quest_giver='npc_blackwater_cook_doma',
        objectives=[{'type': 'visit', 'target': 'bs_blackwater_sump', 'count': 1}, {'type': 'gather', 'target': 'blackwater_char', 'count': 3}, {'type': 'kill', 'target': 'blackwater_eel', 'count': 2}],
        rewards=[{'action_type': 'give_scales', 'amount': 36}, {'action_type': 'give_skill_xp', 'skill_id': 'fishing', 'count': 12}],
        next_quest_id=None,
        prerequisite_quests=[],
        can_share=True,
        consequence_small='Doma paints safer lamp marks above the sump and names the next stew after the catch that proved the water useful.',
    )
    area.quest(
        'tdm_q_claim_jumper_case',
        name='The Case For The Crew',
        description='Rill asks you to stop claim jumpers near broken cart runs and collect the evidence that lets Tremen treat violence as a civic problem.',
        quest_type='combat',
        quest_giver='npc_safety_captain_rill',
        objectives=[{'type': 'investigate', 'target': 'bc_broken_cart_run', 'count': 1}, {'type': 'kill', 'target': 'claim_jumper', 'count': 4}, {'type': 'talk_to', 'target': 'npc_safety_captain_rill', 'count': 1}],
        rewards=[{'action_type': 'give_scales', 'amount': 44}, {'action_type': 'modify_standing', 'faction_id': 'wardens', 'delta': 1800}],
        next_quest_id=None,
        prerequisite_quests=[],
        can_share=True,
        consequence_small='Rill posts the case at the hoist, naming the endangered crew instead of letting the mine reduce them to an incident number.',
    )
    area.quest(
        'tdm_q_pressure_sample',
        name='Pressure Sample',
        description='Bran wants pressure quartz gathered under supervision, showing why valuable materials should create careful play rather than a rush for rare nodes.',
        quest_type='gather',
        quest_giver='npc_mine_steward_bran',
        objectives=[{'type': 'visit', 'target': 'pg_pressure_gallery', 'count': 1}, {'type': 'gather', 'target': 'pressure_quartz', 'count': 2}, {'type': 'gather', 'target': 'resonance_shard', 'count': 1}],
        rewards=[{'action_type': 'give_scales', 'amount': 46}, {'action_type': 'give_skill_xp', 'skill_id': 'mining', 'count': 12}],
        next_quest_id=None,
        prerequisite_quests=[],
        can_share=True,
        consequence_small='Bran labels your samples with brace conditions, making the advanced forge value the method as much as the material.',
    )
    area.quest(
        'tdm_q_underhall_seam',
        name='A Seam Toward Names',
        description='Vaun finds a seam tracing that points toward the underhalls, asking you to carry evidence forward without pretending it unlocks a public miracle.',
        quest_type='delivery',
        quest_giver='npc_underhall_mapper_vaun',
        objectives=[{'type': 'investigate', 'target': 'rs_resonance_seam', 'count': 1}, {'type': 'deliver', 'target': 'npc_underhall_archivist_nelli', 'count': 1, 'item_tag': 'tdm_seam_tracing'}, {'type': 'visit', 'target': 'ug_underhall_gate', 'count': 1}],
        rewards=[{'action_type': 'give_scales', 'amount': 38}, {'action_type': 'give_skill_xp', 'skill_id': 'scholarship', 'count': 12}],
        next_quest_id='thu_q_pattern_debt',
        prerequisite_quests=[],
        can_share=True,
        consequence_small='Vaun redraws the seam in red instead of black, a visible reminder that evidence can ask for care before it asks for action.',
    )

    # Spawns
    area.spawn(pg_pressure_gallery, 'loose_oreling', count_min=1, count_max=2, respawn_minutes=14, respawn_variance=4)
    area.spawn(pg_quartz_bloom, 'loose_oreling', count_min=1, count_max=2, respawn_minutes=14, respawn_variance=4)
    area.spawn(pg_brace_groan_03, 'haul_construct', count_min=1, count_max=1, respawn_minutes=14, respawn_variance=4)
    area.spawn(bs_blackwater_sump, 'blackwater_eel', count_min=1, count_max=2, respawn_minutes=14, respawn_variance=4)
    area.spawn(bs_lamp_reflection, 'blackwater_eel', count_min=1, count_max=2, respawn_minutes=14, respawn_variance=4)
    area.spawn(bs_eel_ripple_03, 'blackwater_eel', count_min=1, count_max=2, respawn_minutes=14, respawn_variance=4)
    area.spawn(bc_broken_cart_run, 'claim_jumper', count_min=1, count_max=2, respawn_minutes=14, respawn_variance=4)
    area.spawn(bc_split_axle, 'claim_jumper', count_min=1, count_max=2, respawn_minutes=14, respawn_variance=4)
    area.spawn(bc_stolen_rail_03, 'minevermin', count_min=1, count_max=2, respawn_minutes=14, respawn_variance=4)
    area.spawn(si_sealed_imperial_cut, 'haul_construct', count_min=1, count_max=1, respawn_minutes=14, respawn_variance=4)
    area.spawn(si_red_wax_mark, 'claim_jumper', count_min=1, count_max=2, respawn_minutes=14, respawn_variance=4)
    area.spawn(si_quiet_pick_05, 'minevermin', count_min=1, count_max=2, respawn_minutes=14, respawn_variance=4)
    area.spawn(rs_resonance_seam, 'stone_listening_frame', count_min=1, count_max=1, respawn_minutes=14, respawn_variance=4)
    area.spawn(rs_listening_pin, 'loose_oreling', count_min=1, count_max=2, respawn_minutes=14, respawn_variance=4)
    area.spawn(rs_hummed_dust_03, 'bell_echo', count_min=1, count_max=1, respawn_minutes=14, respawn_variance=4)

    # Gathering pools
    area.gathering_pool('ore', ['pg_pressure_gallery', 'pg_quartz_bloom', 'rs_resonance_seam'], ['greyteeth_iron', 'pressure_quartz', 'resonance_shard'], max_active=3, respawn_minutes=12, respawn_variance=4, tier_floor=2, tier_ceiling=3)
    area.gathering_pool('forage', ['lh_chain_tender_post', 'bc_split_axle'], ['haul_rope_fiber', 'bellcap_mushroom'], max_active=3, respawn_minutes=12, respawn_variance=4, tier_floor=1, tier_ceiling=2)
    area.gathering_pool('hide', ['bc_stolen_rail_03', 'si_quiet_pick_05'], ['minevermin_hide'], max_active=3, respawn_minutes=12, respawn_variance=4, tier_floor=1, tier_ceiling=1)
    area.gathering_pool('fish', ['bs_blackwater_sump', 'bs_lamp_reflection'], ['blackwater_char', 'cavern_whitefish'], max_active=3, respawn_minutes=12, respawn_variance=4, tier_floor=2, tier_ceiling=3)

    # Lore fragments
    area.lore_fragment(
        'tdm_lore_wage_stamp',
        ro_requisition_office,
        discovery_method='search',
        scholar_path='architecture',
        text='A payroll stamp repeats beside injury marks for workers listed as absent, a tiny bureaucratic cruelty that makes the old occupation feel colder than any monster.',
        insight_gain=1,
    )

    return area.build()
