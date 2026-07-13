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
    cg_claim_gate = area.room('cg_claim_gate', name='Claim Gate', desc='The mine lift opens beside a gate covered in current crew names, routes, claim limits, and expected return times. Mine Steward Bran checks every lamp before acknowledging the ore a party hopes to bring back.', room_type='underground', indoor=True)
    cg_lamp_check = area.room('cg_lamp_check', name='Lamp Check', desc='A dark testing hood reveals weak flames, cracked glass, and leaking seals before descent. Fuel measures are recorded beside route length and spare count, treating light as shared survival equipment rather than personal decoration.', room_type='underground', indoor=True)
    cg_helmet_tally_03 = area.room('cg_helmet_tally_03', name='Crew Helmets', desc='Numbered helmet hooks align with names on the active-crew board. Empty hooks show who is below, while damaged helmets remain beside incident notes until the person and equipment have both been accounted for.', room_type='underground', indoor=True)
    cg_fresh_brace_04 = area.room('cg_fresh_brace_04', name='Witness Brace', desc='A newly set timber brace carries the source mark of its wood, the crew that fitted it, and two inspection dates. Small witness wedges reveal any shift before fresh paint or pride can hide the load.', room_type='underground', indoor=True)
    cg_ore_oath_05 = area.room('cg_ore_oath_05', name='Claim Oath', desc='A claim tablet binds ore removed to braces maintained, hazards reported, and every crew member returned. Old tablets with broken promises hang face-out, making failure part of the mine’s working law.', room_type='underground', indoor=True)
    cg_claim_gate_06 = area.room('cg_claim_gate_06', name='Living Claim', desc='Movable claim markers show active, paused, disputed, and closed workings rather than permanent ownership. Each includes a review date and safety contact so an absent crew cannot quietly hold dangerous ground forever.', room_type='underground', indoor=True)
    cg_lamp_check_07 = area.room('cg_lamp_check_07', name='Returned Lamps', desc='Lamps coming up from the mine cool on a soot-stained shelf before cleaning. Remaining fuel, glass damage, and unusual residue are logged because a lamp can report bad air or hard travel before its bearer finds the words.', room_type='underground', indoor=True)
    cg_helmet_tally_08 = area.room('cg_helmet_tally_08', name='Impact Shelf', desc='Dented helmets are grouped by falling stone, machinery, cramped clearance, and unknown cause. Repairs are dated beside medical follow-up, keeping protective gear from turning an injured worker into an anonymous statistic.', room_type='underground', indoor=True)
    cg_fresh_brace_09 = area.room('cg_fresh_brace_09', name='Load Brace', desc='A laminated brace spans a ceiling seam under numbered pressure pins. The newest pin sits slightly proud, enough for Bran to mark the route conditional while another crew verifies whether the movement continues.', room_type='underground', indoor=True)
    cg_ore_oath_10 = area.room('cg_ore_oath_10', name='Ore and Exit', desc='Two tally columns pair every loaded cart with a cleared return path. A crossed-out shipment shows ore left below when a brace report changed, demonstrating that the mine’s current oath can overrule its appetite.', room_type='underground', indoor=True)
    cg_claim_gate_11 = area.room('cg_claim_gate_11', name='Closure Board', desc='Red tags list flooded, unstable, contested, and unverified claims with the evidence required before review. Returned tags remain archived by date, making a reopened route a traceable decision rather than an erased warning.', room_type='underground', indoor=True)
    cg_lamp_check_12 = area.room('cg_lamp_check_12', name='Quarantine Light', desc='A sealed lamp cabinet holds equipment exposed to unknown fumes or residue. Observation cards track odor, flame color, and cleaning attempts while spare lamps remain available outside the cabinet.', room_type='underground', indoor=True)
    cg_helmet_tally_13 = area.room('cg_helmet_tally_13', name='Open Hook', desc='One helmet hook remains empty beside a crew name and overdue route. Search assignments, last contact, and family notice share the same slate, ensuring the mine cannot balance its count by quietly removing the person.', room_type='underground', indoor=True)
    cg_fresh_brace_14 = area.room('cg_fresh_brace_14', name='Paper Brace', desc='A final support carries copies of the claim, inspection, wage, and requisition numbers tied to its construction. The physical timber points onward to the old offices, where paper can either support a crew or expose how it failed them.', room_type='underground', indoor=True)
    ro_requisition_office = area.room('ro_requisition_office', name='Requisition Office', desc='Old Imperial counters divide a cramped office where Requisitioner Sava sorts ore orders, wage rolls, injury marks, and current claim records into linked piles. Clear weights hold matched evidence where crews can inspect it.', room_type='building', indoor=True)
    ro_stamped_shelf = area.room('ro_stamped_shelf', name='Stamped Shelf', desc='Shelves are arranged by authorization stamp rather than worker or crew. Sava’s colored cords reconnect scattered requests, deliveries, and payroll entries, exposing how an orderly archive can conceal a person by design.', room_type='building', indoor=True)
    ro_old_seal_03 = area.room('ro_old_seal_03', name='Quota Seal', desc='A heavy seal stamps ore category, demanded weight, and deadline into wax with no space for brace condition or injury. Test impressions beside it show how much authority fit into one small mark and how little context survived.', room_type='building', indoor=True)
    ro_missing_wage_04 = area.room('ro_missing_wage_04', name='Unpaid Line', desc='One payroll row names a full shift and then leaves the wage column blank beneath an injury stamp. Later notes follow the worker across three ledgers, keeping the omission specific enough to pursue.', room_type='building', indoor=True)
    ro_ledger_bruise_05 = area.room('ro_ledger_bruise_05', name='Buried Entry', desc='Deep pen pressure from a removed page has bruised names and numbers into the sheet below. Side-light and a non-contact tracing recover part of the entry without pretending the missing document has been restored.', room_type='building', indoor=True)
    ro_requisition_desk_06 = area.room('ro_requisition_desk_06', name='Matching Desk', desc='Sliding frames align requisition, hoist, injury, and wage columns from different books. Open disagreements receive question tags and responsible names, turning archival work into a current civic case rather than passive lore.', room_type='building', indoor=True)
    ro_stamped_shelf_07 = area.room('ro_stamped_shelf_07', name='Equipment Refusals', desc='Stamped denials for lamps, rope, braces, and helmets fill a low shelf beside the incidents that followed. Current crews add claim numbers where the same equipment is now mandatory, making policy change traceable.', room_type='building', indoor=True)
    ro_old_seal_08 = area.room('ro_old_seal_08', name='Broken Authority', desc='A cracked office seal rests in a locked display beside every known impression it made after the break. Mismatched wax edges help distinguish a late order from a forged one without granting the old order moral weight.', room_type='building', indoor=True)
    ro_missing_wage_09 = area.room('ro_missing_wage_09', name='Absent but Charged', desc='Workers marked absent still appear beside deductions for food, lamp oil, and bunk space. Sava has tied each charge to a separate incident report, building proof from the bureaucracy’s own contradictions.', room_type='building', indoor=True)
    ro_ledger_bruise_10 = area.room('ro_ledger_bruise_10', name='Counted Injury', desc='A thumb-worn page converts injuries into lost shifts while the margin preserves names added by another hand. Modern annotations restore the medical reports and crew testimony that the central totals excluded.', room_type='building', indoor=True)
    ro_requisition_desk_11 = area.room('ro_requisition_desk_11', name='Crew Claims Desk', desc='Current claim packets begin with crew names, safety conditions, and review dates before listing desired ore. Copies travel to Bran and the hoist, ensuring no single office can revise the promise invisibly.', room_type='building', indoor=True)
    ro_stamped_shelf_12 = area.room('ro_stamped_shelf_12', name='Matched Evidence', desc='Completed matches rest beneath clear stone weights with the source pages still visible. Visitors can follow wage, injury, shipment, and location cords themselves instead of accepting Sava’s conclusion as a hidden verdict.', room_type='building', indoor=True)
    ro_old_seal_13 = area.room('ro_old_seal_13', name='Retired Seals', desc='Imperial stamps are stored with retirement dates, known users, and sample impressions. None remains in active drawers, but preserving them lets later cases prove which authority once made an extraction demand look routine.', room_type='building', indoor=True)
    ro_missing_wage_14 = area.room('ro_missing_wage_14', name='Open Wage Cases', desc='A board facing the lower hoist lists unresolved wages beside worker names, last known crews, and evidence still needed. Empty resolution boxes refuse both easy closure and the older habit of treating silence as payment.', room_type='building', indoor=True)
    lh_lower_hoist = area.room('lh_lower_hoist', name='Lower Hoist', desc='A reinforced cage hangs over the deeper shaft beside load, route, and crew boards. Safety Captain Rill marks unsafe braces before accepting any descent schedule, letting the mine wait when its stone will not.', room_type='underground', indoor=True)
    lh_chain_tender_post = area.room('lh_chain_tender_post', name='Chain Tender Post', desc='Chain gauges, grease tins, haul-rope fiber, and bellcap provisions share a stocked work post. Minimum lines and harvest dates keep both machinery and its tenders supplied without treating either as inexhaustible.', room_type='underground', indoor=True)
    lh_brake_wheel_03 = area.room('lh_brake_wheel_03', name='Brake Test Wheel', desc='A scarred wheel engages the hoist brake against numbered test loads. The current stopping distance is chalked beside older values, making gradual wear visible before an operator mistakes familiarity for safety.', room_type='underground', indoor=True)
    lh_echo_count_04 = area.room('lh_echo_count_04', name='Shaft Count', desc='Measured hammer taps return from platforms, braces, and the shaft bottom in a learned sequence. Missing or delayed answers are logged with cage position, giving crews a second check when sight and shouted words fail.', room_type='underground', indoor=True)
    lh_drop_warning_05 = area.room('lh_drop_warning_05', name='Falling-Line Board', desc='A red boundary encloses the space beneath suspended loads. Warning boards name the last dropped object, cause, and repair instead of reducing every fall to a generic reminder to be careful.', room_type='underground', indoor=True)
    lh_lower_hoist_06 = area.room('lh_lower_hoist_06', name='Load Platform', desc='Balance marks divide the cage floor for people, tools, braces, and ore. A crossed-out capacity shows where an old Imperial load was replaced by the lower limit the current chain can safely carry.', room_type='underground', indoor=True)
    lh_chain_tender_07 = area.room('lh_chain_tender_07', name='Witness Links', desc='Selected chain links hang beside magnifying lenses and wear templates. Cracks, stretch, and repairs are tagged to the position they came from, allowing the hoist’s hidden fatigue to become shared evidence.', room_type='underground', indoor=True)
    lh_brake_wheel_08 = area.room('lh_brake_wheel_08', name='Second Brake', desc='A separate wheel operates the emergency brake through a distinct linkage. Shift drills are dated beside the names of both operators, ensuring redundancy exists in practiced people as well as machinery.', room_type='underground', indoor=True)
    lh_echo_count_09 = area.room('lh_echo_count_09', name='Platform Replies', desc='Each lower landing answers with its own bell-and-tap count before the cage moves. The latest board leaves one platform closed after an uncertain reply, preserving doubt as a reason to investigate on foot.', room_type='underground', indoor=True)
    lh_drop_warning_10 = area.room('lh_drop_warning_10', name='Secured Tools', desc='Tethers, covered buckets, and locking cart pins line a rack beside examples of failed knots. The damaged gear keeps its incident tag so replacing it does not erase how it entered the shaft.', room_type='underground', indoor=True)
    lh_lower_hoist_11 = area.room('lh_lower_hoist_11', name='Lower Landing', desc='The cage meets a broad landing where crews recount names, lamps, and equipment before entering the pressure galleries. Return loads wait behind a separate line, keeping valuable ore from crowding people at the shaft.', room_type='underground', indoor=True)
    lh_chain_tender_12 = area.room('lh_chain_tender_12', name='Grease Record', desc='Different greases are tested on marked lengths of chain under the mine’s damp and dust. Tendril-shaped wear around one pin is copied into the maintenance book without turning an unfamiliar pattern into folklore.', room_type='underground', indoor=True)
    lh_brake_wheel_13 = area.room('lh_brake_wheel_13', name='Handoff Wheel', desc='Outgoing and incoming operators test the brake together before exchanging its handle. Both sign the result and unresolved faults stay on the wheel’s tag, preventing a shift change from resetting responsibility.', room_type='underground', indoor=True)
    lh_echo_count_14 = area.room('lh_echo_count_14', name='Gallery Echo', desc='A final call-and-response reaches from the hoist to the first pressure gallery. Changes in the returning tone are paired with brace inspections and crew reports, carrying machinery discipline into valuable ground.', room_type='underground', indoor=True)
    pg_pressure_gallery = area.room('pg_pressure_gallery', name='Pressure Gallery', desc='Brace pins, crack gauges, and sample permits frame a gallery rich in greyteeth iron and pressure quartz. Loose orelings disturb fragments near the marked collection line, making supervised value and immediate hazard part of the same room.', room_type='underground', indoor=True)
    pg_quartz_bloom = area.room('pg_quartz_bloom', name='Quartz Bloom', desc='Blue-white quartz fans across a loaded seam beneath numbered extraction pockets. Sample tags name brace condition, tool, and surrounding fractures, while untouched pockets preserve both stability and future study.', room_type='underground', indoor=True)
    pg_brace_groan_03 = area.room('pg_brace_groan_03', name='Speaking Brace', desc='A timber brace releases a low groan when a haul construct shifts nearby stone. Witness wedges and a load chart distinguish ordinary settling from new movement, and the work line remains narrowed pending review.', room_type='underground', indoor=True)
    pg_blue_spark_04 = area.room('pg_blue_spark_04', name='Impact Spark', desc='Brief blue sparks appear where a test pick meets a quartz-bearing edge. The strike force, tool head, damp, and result are recorded together, keeping a striking effect attached to reproducible conditions.', room_type='underground', indoor=True)
    pg_safety_chalk_05 = area.room('pg_safety_chalk_05', name='Sample Boundary', desc='Layered chalk defines observation, tool, catch-cloth, and retreat zones around a prospective sample. Erased lines remain dated in the log so a safer boundary does not conceal how close earlier work came.', room_type='underground', indoor=True)
    pg_pressure_seam_06 = area.room('pg_pressure_seam_06', name='Witnessed Seam', desc='Pairs of brass points measure a seam crossing ore and barren stone. The ore-rich side has moved more since the last cut, and Bran’s red notation limits collection until the difference is understood.', room_type='underground', indoor=True)
    pg_quartz_bloom_07 = area.room('pg_quartz_bloom_07', name='Resting Bloom', desc='A harvested quartz fan sits behind a pause marker with fragments sorted by where they detached. Small crystals remain in place around the cut, preserving a reference for regrowth, stress, and future provenance.', room_type='underground', indoor=True)
    pg_brace_groan_08 = area.room('pg_brace_groan_08', name='Changed Note', desc='One brace now answers cart vibration at a higher pitch than its neighboring supports. Crews have added a temporary sister beam and left both old and new sound counts open for the next shift.', room_type='underground', indoor=True)
    pg_blue_spark_09 = area.room('pg_blue_spark_09', name='Cartlight Seam', desc='Loaded cart wheels sometimes draw a blue flicker from dust along this seam. A stop mark precedes the effect, requiring the cart to be checked and the gallery cleared before anyone repeats the passage.', room_type='underground', indoor=True)
    pg_safety_chalk_10 = area.room('pg_safety_chalk_10', name='Crew Exclusion', desc='Different chalk colors reserve space for the sampler, brace watcher, catcher, and clear retreat. Names and times beside each role make supervision an active crew arrangement rather than a word on a permit.', room_type='underground', indoor=True)
    pg_pressure_seam_11 = area.room('pg_pressure_seam_11', name='Requisition Seam', desc='Old order numbers are chiseled beside extraction scars that match Sava’s requisitions. Current measurements show where demanded weight exceeded the support plan, turning archival contradiction into physical evidence.', room_type='underground', indoor=True)
    pg_quartz_bloom_12 = area.room('pg_quartz_bloom_12', name='Forge Samples', desc='Wrapped quartz and resonance-shard samples rest in fitted trays with source pocket, fracture direction, and brace state. The labels let advanced craft value the method and place, not merely the rare material.', room_type='underground', indoor=True)
    pg_brace_groan_13 = area.room('pg_brace_groan_13', name='Construct Load', desc='A reinforced brace bay bears impact marks at the height of old haul constructs. New sacrificial blocks take that contact and show fresh damage plainly, protecting the main support without disguising ongoing strain.', room_type='underground', indoor=True)
    pg_blue_spark_14 = area.room('pg_blue_spark_14', name='Damp Spark Line', desc='Blue flickers diminish where sump damp darkens the gallery wall, but mineral flakes have increased around the same edge. Separate logs track both changes before the route turns toward blackwater.', room_type='underground', indoor=True)
    bs_blackwater_sump = area.room('bs_blackwater_sump', name='Blackwater Sump', desc='Dark water fills an old drainage basin beneath hooks, catch tallies, and lamp marks. Blackwater Cook Doma sorts char and whitefish for household pots while broad eel ripples keep every fisher aware that the sump also bites.', room_type='cave', indoor=True)
    bs_lamp_reflection = area.room('bs_lamp_reflection', name='Lamp Reflection', desc='Shielded lamps cast paired marks across a fishable pool, revealing current, floating debris, and sudden movement without blinding the water. Catch and eel sightings share the same slate so food gathering updates route safety.', room_type='cave', indoor=True)
    bs_eel_ripple_03 = area.room('bs_eel_ripple_03', name='Crossing Ripple', desc='A blackwater eel’s wake cuts against the sump’s ordinary current near a narrow crossing. Scraped scales on the stone lip and a recently replaced tether show where the animal’s territory meets mine traffic.', room_type='cave', indoor=True)
    bs_slick_rail_04 = area.room('bs_slick_rail_04', name='Scrubbed Rail', desc='Oil, mineral slime, and fish residue make different stains along the handrail. Cleaning tags name which treatment removed each without weakening the grip, while an unsolved dark patch remains cordoned.', room_type='cave', indoor=True)
    bs_sump_hook_05 = area.room('bs_sump_hook_05', name='Catch Hooks', desc='Barbed eel hooks, gentle fish hooks, rescue crooks, and kettle hangers occupy separate numbered racks. Bent examples remain beside repair notes, preventing one useful tool from being mistaken for another in poor light.', room_type='cave', indoor=True)
    bs_blackwater_sump_06 = area.room('bs_blackwater_sump_06', name='Level Basin', desc='Water marks and dated boards track the sump’s rise after gallery runoff and its fall during dry shifts. Doma’s food count sits beside the route closure line, making abundance and access two readings of the same water.', room_type='cave', indoor=True)
    bs_lamp_reflection_07 = area.room('bs_lamp_reflection_07', name='Broken Reflection', desc='A surface film fractures the guide lamp into scattered points near an inflow. Sample jars, source guesses, and a no-fishing tag remain open until crews determine whether the sheen came from hoist grease or deeper water.', room_type='cave', indoor=True)
    bs_eel_ripple_08 = area.room('bs_eel_ripple_08', name='Feeding Edge', desc='Eel tracks and discarded shells collect beneath an overhung bank. Catch records distinguish animals removed near the walking line from those left deeper in the sump, managing danger without declaring the ecology an enemy.', room_type='cave', indoor=True)
    bs_slick_rail_09 = area.room('bs_slick_rail_09', name='Rope-Grip Rail', desc='Haul-rope wraps add grip where constant mist defeats bare metal. Replacement dates and drying hooks keep the fibers from rotting unseen, and each worn wrap becomes evidence for the next material choice.', room_type='cave', indoor=True)
    bs_sump_hook_10 = area.room('bs_sump_hook_10', name='Reach Hook', desc='A long rescue hook rests above a diagram of the ledges it can reach from stable footing. Practice times and one real recovery are recorded separately, preserving both readiness and the cost of using it.', room_type='cave', indoor=True)
    bs_blackwater_sump_11 = area.room('bs_blackwater_sump_11', name='Household Catch', desc='A catch board assigns char and whitefish to kitchens, infirmary broth, and shift meals before surplus. Small-fish counts and resting intervals remain visible, tying the next stew to the sump’s ability to replenish.', room_type='cave', indoor=True)
    bs_lamp_reflection_12 = area.room('bs_lamp_reflection_12', name='Safer Lamp Marks', desc='Fresh paint fixes lamp positions above stable ledges and away from eel cover. Doma has dated the change and left the former marks visible beneath a strike, so safer practice preserves what prompted it.', room_type='cave', indoor=True)
    bs_eel_ripple_13 = area.room('bs_eel_ripple_13', name='Deep Wake', desc='A heavy wake moves beneath water too dark for a lamp to penetrate. The warning board records direction, size estimate, and time while resisting the urge to turn one unseen animal into a legend.', room_type='cave', indoor=True)
    bs_slick_rail_14 = area.room('bs_slick_rail_14', name='Cartward Drip', desc='Sump water follows wheels and boots onto the rail line ahead. Drainage mats, scrub tools, and a wet-track arrow prepare travelers for broken carts and disputed salvage before the route leaves the water.', room_type='cave', indoor=True)
    bc_broken_cart_run = area.room('bc_broken_cart_run', name='Broken Cart Run', desc='An ore cart lies across the rails amid drag marks, boot scuffs, and improvised claim signs. Warden evidence tags preserve where claim jumpers confronted the crew, keeping the violence tied to a place and disputed salvage.', room_type='underground', indoor=True)
    bc_split_axle = area.room('bc_split_axle', name='Split Axle', desc='The cart axle has split along an old flaw widened by a fresh side impact. Haul-rope fiber and bellcaps grow among stored repair scraps, while witness notes distinguish mechanical failure from the fight that followed.', room_type='underground', indoor=True)
    bc_stolen_rail_03 = area.room('bc_stolen_rail_03', name='Missing Rail', desc='A length of rail has been pried from its chairs and dragged toward a side cut. Minevermin nest in the exposed bed, leaving useful hide and gnawed packing that complicate the original theft evidence.', room_type='underground', indoor=True)
    bc_claim_scar_04 = area.room('bc_claim_scar_04', name='Overcut Claim', desc='Three claim symbols have been carved over one another beside an extraction scar outside every current permit. Tracings preserve the sequence of cuts so the dispute can be judged without granting the deepest mark ownership.', room_type='underground', indoor=True)
    bc_dropped_boot_05 = area.room('bc_dropped_boot_05', name='Evidence Boot', desc='A torn work boot remains where the cart blocked the passage, protected by a chalk outline and incident tag. Size, repair pattern, and bloodless wear are recorded without declaring who wore it before testimony returns.', room_type='underground', indoor=True)
    bc_broken_cart_06 = area.room('bc_broken_cart_06', name='Cargo Count', desc='The cart’s surviving compartments hold ore dust from two registered claims and one unidentified seam. Sava’s seals and Bran’s load marks share the evidence board, linking physical cargo to records that can be challenged.', room_type='underground', indoor=True)
    bc_split_axle_07 = area.room('bc_split_axle_07', name='Tool-Scored Axle', desc='Saw starts and chisel slips cross the axle near its break, unlike the long grain split elsewhere. Casts of the marks sit beside repair tools for comparison, turning suspicion into a testable question.', room_type='underground', indoor=True)
    bc_stolen_rail_08 = area.room('bc_stolen_rail_08', name='Unsafe Gap', desc='Painted sleepers mark where the missing rail made the cart line unusable. A temporary walking bridge keeps crews moving while material requests and the theft case remain open instead of disguising the loss.', room_type='underground', indoor=True)
    bc_claim_scar_09 = area.room('bc_claim_scar_09', name='Crew Boundary', desc='A current claim line circles braces, drainage, and retreat space as well as ore. Claim-jumper cuts ignore all three, visually separating a crew’s safety promise from a mark made only to seize value.', room_type='underground', indoor=True)
    bc_dropped_boot_10 = area.room('bc_dropped_boot_10', name='Returned Pair', desc='A second boot has been matched to the first and returned by its owner after treatment. Their signed account remains copied beside the empty evidence hooks, preserving the person beyond the objects used in the case.', room_type='underground', indoor=True)
    bc_broken_cart_11 = area.room('bc_broken_cart_11', name='Salvage Ledger', desc='Cart parts are divided into repairable, reusable, evidentiary, and unsafe bins. Each transfer needs a name and destination, preventing civic salvage from becoming a quieter version of claim jumping.', room_type='underground', indoor=True)
    bc_split_axle_12 = area.room('bc_split_axle_12', name='Sleeved Axle', desc='A repaired axle section demonstrates a bolted sleeve sized for mine carts. Test loads and failure limits sit beside it, turning the broken run into training material without erasing the original incident.', room_type='underground', indoor=True)
    bc_stolen_rail_13 = area.room('bc_stolen_rail_13', name='Recovered Rail', desc='A recovered rail bears old Imperial numbers, fresh pry marks, and a Warden case tag. It remains off the track until ownership, structural condition, and evidentiary use are settled in the open.', room_type='underground', indoor=True)
    bc_claim_scar_14 = area.room('bc_claim_scar_14', name='Posted Case', desc='Rill’s case board names the endangered crew, witness statements, recovered parts, and unresolved claims. Beyond it, red wax seals mark an Imperial cut where old authority and present trespass demand different kinds of restraint.', room_type='underground', indoor=True)
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
