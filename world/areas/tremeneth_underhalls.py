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
    ug_underhall_gate = area.room('ug_underhall_gate', name='Underhall Gate', desc='A bronze-bound gate separates Tremen’s occupied halls from the older descent. Underhall Archivist Nelli keeps an open ledger of names, purposes, lanterns, and intended routes, asking every visitor to become a witness before becoming an explorer.', room_type='underground', indoor=True)
    ug_lantern_count = area.room('ug_lantern_count', name='Lantern Count', desc='Numbered lanterns hang above fuel measures, spare wicks, and polished reflectors. The issue slate records expected burn time beside each party’s route, making a late light meaningful before anyone calls it lost.', room_type='underground', indoor=True)
    ug_name_cord_03 = area.room('ug_name_cord_03', name='Name-Cord Rack', desc='Soft cords carry knots for each person descending and a separate pattern for the planned return. Some old cords remain open beside dated search notes, refusing to turn an absent name into a finished account.', room_type='underground', indoor=True)
    ug_cool_draft_04 = area.room('ug_cool_draft_04', name='Draft Ribbons', desc='Threads stretched across a carved frame reveal cool air moving upward from several unseen passages. Nelli’s dated tags compare strength and direction, preserving changes without claiming what lies at their source.', room_type='underground', indoor=True)
    ug_guest_warning_05 = area.room('ug_guest_warning_05', name='Guest Compact', desc='A low plaque asks guests to leave family objects in place, carry no unrecorded flame, and return every measurement with the name attached to it. Repairs around the plaque show the compact is maintained, not merely ceremonial.', room_type='underground', indoor=True)
    ug_underhall_gate_06 = area.room('ug_underhall_gate_06', name='First Descent Gate', desc='A second grille opens onto steeper, older steps. Inspection chalk circles a strained hinge and worn threshold, while the bars preserve a clear view of the route rather than dressing restraint as secrecy.', room_type='underground', indoor=True)
    ug_lantern_count_07 = area.room('ug_lantern_count_07', name='Returned Lights', desc='Extinguished lanterns cool on a stone shelf before cleaning and recounting. Soot patterns, cracked glass, and fuel remaining are copied into the ledger because the condition of a returned lamp describes the journey it survived.', room_type='underground', indoor=True)
    ug_name_cord_08 = area.room('ug_name_cord_08', name='Witness Braid', desc='Short name cords from completed descents have been braided into a thick guide beside the stairs. Each retains its original knots, allowing shared memory to strengthen the route without dissolving the people inside it.', room_type='underground', indoor=True)
    ug_cool_draft_09 = area.room('ug_cool_draft_09', name='Air Ledger', desc='A recessed desk holds wax tablets for temperature, damp, scent, and draft observations. Conflicting entries remain side by side until a later walk resolves them, treating uncertainty as work still owed.', room_type='underground', indoor=True)
    ug_guest_warning_10 = area.room('ug_guest_warning_10', name='Borrowed History', desc='A warning panel names tools, bowls, cords, and memorial objects that may look abandoned to an outsider. Beside each category is the person or family to ask, making curiosity possible without turning heritage into loot.', room_type='underground', indoor=True)
    ug_underhall_gate_11 = area.room('ug_underhall_gate_11', name='Old Lintel', desc='The fitted blocks of Tremen’s maintained passage meet a lintel cut with unfamiliar proportions and weathered tool marks. A modern brace supports it openly, while its survey label records dimensions and leaves the maker unanswered.', room_type='underground', indoor=True)
    ug_lantern_count_12 = area.room('ug_lantern_count_12', name='Wick Bench', desc='Trimmed wicks, clean oil cups, wire guards, and rejected glass are arranged by condition. A repair tally credits the hands that restored each light and identifies parts still unsafe for another descent.', room_type='underground', indoor=True)
    ug_name_cord_13 = area.room('ug_name_cord_13', name='Open Names', desc='The last registry before the vault walks repeats every descending name and leaves space for the returning hand. Several entries carry corrections to route or purpose, evidence that testimony matters more than an unchanging record.', room_type='underground', indoor=True)
    ug_cool_draft_14 = area.room('ug_cool_draft_14', name='Vaultward Air', desc='Cool air carries mineral damp, lamp smoke, and the faint trace of water from deeper halls. Direction cords point toward the family vault walk and back to the gate, keeping the next threshold connected to a witnessed return.', room_type='underground', indoor=True)
    fv_family_vault_walk = area.room('fv_family_vault_walk', name='Family Vault Walk', desc='Small family thresholds line a passage built for visiting rather than display. Porr waits with a cup of water and a name cord, watching that guests learn whose history they enter before they look at what was kept.', room_type='underground', indoor=True)
    fv_low_name_shelf = area.room('fv_low_name_shelf', name='Low Name Shelf', desc='Names are cut into a shelf near the floor beside thumb-sized cups and smooth hand stones. Fresh water darkens one cup without hiding the older mineral rings left by years of remembered visits.', room_type='underground', indoor=True)
    fv_quiet_bowl_03 = area.room('fv_quiet_bowl_03', name='Water-Worn Bowl', desc='A plain stone bowl rests beneath a family mark, its rim polished by refilling hands rather than precious metal. A folded cloth catches spills so the offered water never damages the names below.', room_type='underground', indoor=True)
    fv_kept_tool_04 = area.room('fv_kept_tool_04', name='Mended Chisel', desc='A narrow chisel bears two replaced handles, a reforged tip, and a tag naming the mason who used each repair. Its value lies in continued work and witnessed hands, not in being old enough to steal.', room_type='underground', indoor=True)
    fv_mourning_bench_05 = area.room('fv_mourning_bench_05', name='Windroot Bench', desc='A low mourning bench faces a damp seam where tended windroot grows between marked stones. Clipping dates leave the youngest crowns untouched, joining household medicine to remembrance without stripping the memorial bare.', room_type='underground', indoor=True)
    fv_family_vault_06 = area.room('fv_family_vault_06', name='Open Family Room', desc='A woven cord across the threshold has been lowered and its visit slate turned outward. Bowls, work aprons, letters, and repaired tools remain arranged for family stories, with no treasure pedestal to invite the wrong kind of attention.', room_type='underground', indoor=True)
    fv_low_name_shelf_07 = area.room('fv_low_name_shelf_07', name='Reachable Names', desc='This shelf keeps every inscription within reach of a seated visitor. Rubbed edges show where fingers return to the same names, while a recent correction preserves a changed family title instead of freezing the person in one role.', room_type='underground', indoor=True)
    fv_quiet_bowl_08 = area.room('fv_quiet_bowl_08', name='Shared Cup', desc='One broad cup serves several names carved along a joined shelf. Water marks connect them across different dates, and a small ledger records who carried the cup when relatives could not make the descent.', room_type='underground', indoor=True)
    fv_kept_tool_09 = area.room('fv_kept_tool_09', name='Bread Hammer', desc='A compact stone hammer sits beside a worn bread stamp and an account of kitchen repairs. The pairing remembers a life divided between feeding a household and keeping its ovens standing.', room_type='underground', indoor=True)
    fv_mourning_bench_10 = area.room('fv_mourning_bench_10', name='Unfinished Seat', desc='Tool marks stop halfway across one end of the bench, and a note asks visitors not to smooth them away. Small offerings identify several hands that resumed other work while choosing to leave this absence visible.', room_type='underground', indoor=True)
    fv_family_vault_11 = area.room('fv_family_vault_11', name='Closed Family Room', desc='The threshold cord remains raised and the visit slate names the family contact who may open it. A clear return date turns closure into consent and stewardship rather than an invitation to defeat a lock.', room_type='underground', indoor=True)
    fv_low_name_shelf_12 = area.room('fv_low_name_shelf_12', name='Newly Cut Name', desc='Pale stone dust surrounds a fresh inscription on the oldest shelf. The dates leave room for a life’s work, relationships, and later corrections, acknowledging that even a finished carving begins an ongoing memory.', room_type='underground', indoor=True)
    fv_quiet_bowl_13 = area.room('fv_quiet_bowl_13', name='Upside-Down Cup', desc='An empty cup rests inverted beside a damp ring and a neatly coiled name cord. The small sign records that a visit was completed properly, allowing absence, care, and return to be read without a posted explanation.', room_type='underground', indoor=True)
    fv_kept_tool_14 = area.room('fv_kept_tool_14', name='Listening Mallet', desc='A felt-headed mallet from a family bell workshop hangs beside its repair history and permission tag. Its worn face points onward to the tuned corridors, connecting personal craft to the sounds still maintained below Tremen.', room_type='underground', indoor=True)
    bc_bell_tuned_corridor = area.room('bc_bell_tuned_corridor', name='Bell-Tuned Corridor', desc='Small bronze bells hang at measured intervals beneath a ceiling shaped to carry their sound. A listening chart records expected decay, echoes, and changes after repairs, making the corridor an instrument people maintain rather than an unexplained haunting.', room_type='underground', indoor=True)
    bc_soft_clapper = area.room('bc_soft_clapper', name='Soft Clapper', desc='Felt, leather, wood, and wrapped metal clappers hang beside the first bell. Each produces a different strength of test tone, and a red tag reserves the hardest striker for supervised structural checks.', room_type='underground', indoor=True)
    bc_tuned_niche_03 = area.room('bc_tuned_niche_03', name='Bellcap Niche', desc='Bellcap mushrooms cluster in the damp curve of a listening niche. Harvest marks leave young caps and their substrate intact, while tone notes distinguish changes caused by moisture from changes deeper in the stone.', room_type='underground', indoor=True)
    bc_dust_tone_04 = area.room('bc_dust_tone_04', name='Dust Figure', desc='Fine pale dust rests on a taut dark membrane set into the wall. Recent bell tests have drawn branching lines through it, dated before anyone attempts to interpret whether the pattern reflects air, footing, or stone.', room_type='underground', indoor=True)
    bc_measured_foot_05 = area.room('bc_measured_foot_05', name='Walking Measure', desc='Brass inlays mark slow, ordinary, burdened, and hurried walking intervals along the floor. Test logs compare each pace with the bells’ response, allowing daily traffic to expose a change without demanding theatrical silence.', room_type='underground', indoor=True)
    bc_bell_corridor_06 = area.room('bc_bell_corridor_06', name='Mended Resonator', desc='A long wall recess ends at a bronze plate whose lower edge was reset after a crack opened nearby. The old pitch remains in the ledger beside the new one, preserving the repair’s consequence instead of pretending perfect restoration.', room_type='underground', indoor=True)
    bc_soft_clapper_07 = area.room('bc_soft_clapper_07', name='Mute Station', desc='Padded sleeves can quiet each test bell while crews move equipment through the passage. Counted ties and inspection dates keep the temporary silence reversible, preventing a convenience from erasing an alarm path.', room_type='underground', indoor=True)
    bc_tuned_niche_08 = area.room('bc_tuned_niche_08', name='Crossway Ear', desc='A rounded niche gathers sounds from two unseen corridors into separate stone cups. Chalk reports name footsteps, water, tool work, and uncertain tones by time and direction rather than assigning every sound a story.', room_type='underground', indoor=True)
    bc_dust_tone_09 = area.room('bc_dust_tone_09', name='Fracture Line', desc='Dark dust has settled into a hairline seam beneath one bell bracket. Three measurements show the seam unchanged, but the next check remains scheduled and the bell’s permitted force has been reduced.', room_type='underground', indoor=True)
    bc_measured_foot_10 = area.room('bc_measured_foot_10', name='Pause Marks', desc='Paired floor marks create places for groups to stop between resonant spans. Scratches cluster where impatient feet crossed early, while a maintenance note records the loosened fitting that habit helped reveal.', room_type='underground', indoor=True)
    bc_bell_corridor_11 = area.room('bc_bell_corridor_11', name='Paired Tones', desc='Two differently cast bells share one stone arch and answer each other with a slow beat. A public comparison ledger records temperature, damp, clapper, and listener, making disagreement part of the measurement.', room_type='underground', indoor=True)
    bc_soft_clapper_12 = area.room('bc_soft_clapper_12', name='Practice Strikers', desc='Worn felt strikers and replaceable pads let new listeners learn a repeatable touch. Failed pads remain tagged with the tones they distorted, turning mistakes into material knowledge instead of embarrassment.', room_type='underground', indoor=True)
    bc_tuned_niche_13 = area.room('bc_tuned_niche_13', name='Weighted Niche', desc='Movable bronze weights rest in numbered sockets around a shallow niche. Their current arrangement bears several signatures and an expiry date, marking it as a test configuration rather than a permanent answer.', room_type='underground', indoor=True)
    bc_dust_tone_14 = area.room('bc_dust_tone_14', name='Water Overtone', desc='The last bell’s note carries a faint wavering overtone from the cistern passages ahead. Damp readings and water levels share its slate, connecting a changed sound to the practical life below before reaching for stranger explanations.', room_type='underground', indoor=True)
    dc_dry_cistern = area.room('dc_dry_cistern', name='Dry Cistern', desc='An emptied storage basin exposes intake channels, patched seams, and ladders used for maintenance. Cistern Fisher Ren works beside the remaining rill while skitters nose through old sediment, keeping food, water, and pests in the same practical account.', room_type='underground', indoor=True)
    dc_whitefish_rill = area.room('dc_whitefish_rill', name='Whitefish Rill', desc='Cold water slips through a grated channel where pale whitefish hold against the current. Ren’s catch board lists household requests, fish taken, and quiet intervals that leave the rill time to settle.', room_type='underground', indoor=True)
    dc_water_mark_03 = area.room('dc_water_mark_03', name='Gnawed Gauge', desc='Layered water marks climb a measuring pillar beside fresh minevermin tooth scores. The gauge records both storage history and current damage, while a hide-scraping frame nearby makes clear that pest control still yields useful material.', room_type='underground', indoor=True)
    dc_old_bucket_04 = area.room('dc_old_bucket_04', name='Forager’s Bucket', desc='An old bucket patched with wire and pitch rests beneath a damp shelf of bellcap mushrooms. Collection dates and missing staves are marked on its side, joining careful foraging to the ordinary repair of its container.', room_type='underground', indoor=True)
    dc_cool_moss_05 = area.room('dc_cool_moss_05', name='Moss Filter', desc='Cool moss and windroot grow along a slow seep before it reaches the storage channels. Harvest bands protect the densest roots, and clear gaps show where crews inspect stone for contamination and cracks.', room_type='underground', indoor=True)
    dc_dry_cistern_06 = area.room('dc_dry_cistern_06', name='Cleaning Basin', desc='This basin remains dry while crews scrape mineral scale into labeled barrows. Sections already inspected bear dates and initials; dark untouched patches reveal how much work remains before the next filling cycle.', room_type='underground', indoor=True)
    dc_whitefish_rill_07 = area.room('dc_whitefish_rill_07', name='Nursery Run', desc='The rill widens into shallow cover where finger-length whitefish shelter among smooth stones. A fine-mesh marker and a no-take tally protect the smallest fish, tying today’s restraint to later household meals.', room_type='underground', indoor=True)
    dc_water_mark_08 = area.room('dc_water_mark_08', name='Drought Rings', desc='Closely spaced cuts record seasons when the cistern fell faster than expected. Later notes add population, repairs, and diverted flow, ensuring a low-water year remains a shared logistical memory instead of a vague hardship tale.', room_type='underground', indoor=True)
    dc_old_bucket_09 = area.room('dc_old_bucket_09', name='Cooper’s Stand', desc='Buckets awaiting hoops, handles, or pitch sit upside down on a draining rack. Repair tags sort those safe for drinking water from those restricted to cleaning, preventing thrift from becoming contamination.', room_type='underground', indoor=True)
    dc_cool_moss_10 = area.room('dc_cool_moss_10', name='Seep Garden', desc='A tended strip of moss slows runoff along the cistern wall and holds moisture for useful roots. Wooden dividers name resting, harvestable, and newly restored sections so the garden’s condition can change without losing its history.', room_type='underground', indoor=True)
    dc_dry_cistern_11 = area.room('dc_dry_cistern_11', name='Cracked Reserve', desc='A reserve basin stands empty around a long repaired crack crossed by numbered witness marks. The newest mark has shifted less than a finger width, enough to keep the basin out of service and the repair under observation.', room_type='underground', indoor=True)
    dc_whitefish_rill_12 = area.room('dc_whitefish_rill_12', name='Listening Pool', desc='The rill deepens beneath a stone lip where whitefish feed beyond lantern glare. Chalk silhouettes show Ren’s low casting posture, and the catch ledger credits patience alongside number and weight.', room_type='underground', indoor=True)
    dc_water_mark_13 = area.room('dc_water_mark_13', name='New Baseline', desc='A bright brass line establishes a new water baseline beside centuries of carved marks. Its installation note explains the changed channel rather than pretending measurements made before the repair mean the same thing.', room_type='underground', indoor=True)
    dc_old_bucket_14 = area.room('dc_old_bucket_14', name='Sounding Bucket', desc='A narrow bucket hangs from a measured cord for checking water in shafts beyond the cisterns. Knots record depth and the bucket’s returning sound, carrying a familiar household tool toward the confusing junction ahead.', room_type='underground', indoor=True)
    ej_eightfold_junction = area.room('ej_eightfold_junction', name='Eightfold Junction', desc='Eight corridor mouths divide a round chamber, though gates and service chains close those outside the maintained route. Quiet Guard Vedra points out each distinct echo, chalk braid, and return mark before asking a newcomer to move at all.', room_type='underground', indoor=True)
    ej_wrong_turn_bell = area.room('ej_wrong_turn_bell', name='Wrong-Turn Bell', desc='A low bell hangs where an old service passage resembles the traveled way. Its broad pull can be found in darkness, while skitter gnawing and scraps of minevermin hide show why waiting for an answer is safer than wandering.', room_type='underground', indoor=True)
    ej_chalk_braid_03 = area.room('ej_chalk_braid_03', name='Cistern Braid', desc='Blue, white, and grey chalk lines weave together along the wall from the cistern route. New sound counts are braided into the pattern with dates and initials, allowing later travelers to compare rather than simply obey.', room_type='underground', indoor=True)
    ej_return_arrow_04 = area.room('ej_return_arrow_04', name='Palm Arrow', desc='A return arrow is carved deep enough to read with a gloved hand when dust or darkness hides its paint. The tail carries a notch for every verified junction crossed back toward occupied halls.', room_type='underground', indoor=True)
    ej_listening_dust_05 = area.room('ej_listening_dust_05', name='Echo Dust', desc='Fine dust lies across a quiet bay marked for listening. Footprints stop behind its boundary while a bell-like echo repeats from changing directions, leaving observers room to distinguish the sound from the tracks it did not make.', room_type='underground', indoor=True)
    ej_eightfold_junction_06 = area.room('ej_eightfold_junction_06', name='Sound Count', desc='A radial floor diagram assigns each corridor a simple count, hand sign, and expected return tone. Several labels have been amended as gates closed or water changed, keeping the lesson current without changing the chamber’s old geometry.', room_type='underground', indoor=True)
    ej_wrong_turn_bell_07 = area.room('ej_wrong_turn_bell_07', name='Damped Bell', desc='Leather wraps mute all but the lowest note of this wrong-turn bell. A repair card explains that the higher tone became indistinguishable from cistern work, so the warning was changed instead of blaming confused travelers.', room_type='underground', indoor=True)
    ej_chalk_braid_08 = area.room('ej_chalk_braid_08', name='Public Braid', desc='Overlapping chalk strands record Vedra’s count beside additions from fishers, vault visitors, and repair crews. Crossed-out turns remain readable beneath corrections, teaching how the route changed and how errors were recovered.', room_type='underground', indoor=True)
    ej_return_arrow_09 = area.room('ej_return_arrow_09', name='Waiting Arrow', desc='A broad return arrow points back to a recessed waiting place instead of urging immediate travel. Tally scratches count parties guided out from here, making stopping a practiced navigation skill rather than a mark of failure.', room_type='underground', indoor=True)
    ej_listening_dust_10 = area.room('ej_listening_dust_10', name='Traffic Fan', desc='Dust has fanned into different shapes at the mouths of three passages. One bears boot traffic, one a steady water draft, and one only scattered skitter prints, providing clues that complement the bells without replacing them.', room_type='underground', indoor=True)
    ej_eightfold_junction_11 = area.room('ej_eightfold_junction_11', name='Closed Spokes', desc='Iron service gates reveal several branches while preventing casual entry. Each carries its closure reason, responsible crew, and next review, so inaccessible space reads as managed infrastructure rather than arbitrary denial.', room_type='underground', indoor=True)
    ej_wrong_turn_bell_12 = area.room('ej_wrong_turn_bell_12', name='Answer Bell', desc='Two pulls on this bell ask the junction watch for a confirming reply. The response chart includes delayed, muffled, and absent answers with clear instructions to remain in place when certainty does not return.', room_type='underground', indoor=True)
    ej_chalk_braid_13 = area.room('ej_chalk_braid_13', name='Learners’ Braid', desc='Fresh chalk counts from recent learners run beside the established route braid. Disagreements are circled rather than erased, giving Vedra and the next group evidence about where the chamber still misleads.', room_type='underground', indoor=True)
    ej_return_arrow_14 = area.room('ej_return_arrow_14', name='Chasm Return', desc='The last tactile arrow points back toward the junction from the mouth of the Quiet Chasms. A chain code and breath-pause mark introduce the next route’s discipline while preserving an unmistakable way home.', room_type='underground', indoor=True)
    qc_quiet_chasm = area.room('qc_quiet_chasm', name='Quiet Chasm', desc='A railed path enters a natural cleft whose bottom swallows ordinary lantern light. Skitters move among loose stones near the lip, and posted hand signs ask parties to listen for falls before adding their own noise.', room_type='cave', indoor=True)
    qc_chain_whisper = area.room('qc_chain_whisper', name='Chain Whisper', desc='A safety chain hums against iron eyes whenever the rock cools or the walkway shifts. Fresh scoring from a loose oreling interrupts the older wear pattern, giving the changed sound a visible source that still must be dealt with.', room_type='cave', indoor=True)
    qc_dark_rail_03 = area.room('qc_dark_rail_03', name='Echo Rail', desc='Blackened handrail disappears into the bend, its raised repair bands readable by touch. A bell-like echo answers contact from farther along the metal, but inspection tags separate expected resonance from knocks no crew recorded.', room_type='cave', indoor=True)
    qc_fall_bell_04 = area.room('qc_fall_bell_04', name='Loose-Stone Bell', desc='A shielded bell hangs beside a tray of stones recovered from the walking line. Its signal chart distinguishes falling debris, dropped gear, and a person over the rail, because rescue begins with an accurate warning.', room_type='cave', indoor=True)
    qc_breath_pause_05 = area.room('qc_breath_pause_05', name='First Breath Pause', desc='A recessed stance allows a whole party to stop clear of the exposed path. Finger counts mark slow breaths and listening intervals, while a return arrow remains within reach of anyone choosing not to continue.', room_type='cave', indoor=True)
    qc_quiet_chasm_06 = area.room('qc_quiet_chasm_06', name='Single-Foot Span', desc='The path narrows across a stone rib with room for only one careful line. White step marks show tested placements, and crossed-out marks preserve where a recent chip made the old cadence unsafe.', room_type='cave', indoor=True)
    qc_chain_whisper_07 = area.room('qc_chain_whisper_07', name='Tension Link', desc='One bright replacement link joins lengths of older chain on either side. A hanging gauge records load and temperature, helping travelers decide whether a new whisper belongs to metal under strain or movement below.', room_type='cave', indoor=True)
    qc_dark_rail_08 = area.room('qc_dark_rail_08', name='Three-Hand Rail', desc='Three different repairs meet along this section of rail: riveted iron, wrapped cable, and a stone socket reset around both. Each bears its safe-grip mark and inspection date instead of hiding the uneven history beneath paint.', room_type='cave', indoor=True)
    qc_fall_bell_09 = area.room('qc_fall_bell_09', name='Answering Bell', desc='A second fall bell is tuned to answer the first across the chasm. The response ledger lists clear, delayed, and failed tests, with the latest failed answer still open beside a scheduled chain inspection.', room_type='cave', indoor=True)
    qc_breath_pause_10 = area.room('qc_breath_pause_10', name='Shared Silence', desc='A broad alcove lets separated groups rejoin and count one another without crowding the rail. Chalk notes credit those who reported loose fittings, showing that listening here protects people the observer may never meet.', room_type='cave', indoor=True)
    qc_quiet_chasm_11 = area.room('qc_quiet_chasm_11', name='Recovery Ledge', desc='A netted shelf below the path catches some dropped tools and stones before the deeper fall. Its retrieval ledger names what returned, what broke, and what remains below, refusing to turn every loss into mystery.', room_type='cave', indoor=True)
    qc_chain_whisper_12 = area.room('qc_chain_whisper_12', name='Cooling Chain', desc='Condensation beads along a chain where colder air rises from the sealed-room side of the cleft. Rags beneath it collect mineral traces for comparison, while the route log treats the draft as an observation rather than an answer.', room_type='cave', indoor=True)
    qc_dark_rail_13 = area.room('qc_dark_rail_13', name='Threshold Rail', desc='The maintained rail ends at fitted stone whose proportions differ from the natural chasm path. A temporary extension is bolted only to newer masonry, preserving both safe passage and the older surface for study.', room_type='cave', indoor=True)
    qc_fall_bell_14 = area.room('qc_fall_bell_14', name='Patternward Bell', desc='The final warning bell stands where the chasm path meets the sealed pattern rooms. Its muffled pull reports a safe crossing back toward Vedra, while an unstruck witness tag marks who entered the next threshold and when.', room_type='cave', indoor=True)
    sp_sealed_pattern_room = area.room('sp_sealed_pattern_room', name='Sealed Pattern Room', desc='A jointed ward-frame occupies the wall beside an inlaid floor that disappears beneath later seals. Loose coldvein stone and resonance shards are catalogued outside the protected line, separating legitimate gathering from damage to the unanswered pattern.', room_type='underground', indoor=True)
    sp_pattern_threshold = area.room('sp_pattern_threshold', name='Pattern Threshold', desc='Pattern Listener Ysol keeps paper, lamps, and measuring cords behind a bright boundary stripe. A listening frame torn from its mount turns toward movement nearby, demonstrating why observation begins with distance and an exit path.', room_type='underground', indoor=True)
    sp_old_inlay_03 = area.room('sp_old_inlay_03', name='Raking-Light Inlay', desc='Shallow lines emerge only where a shielded lamp casts light nearly parallel to the floor. Tracing frames bridge above the stone without touching it, and every copy records lamp angle, observer, and missing sections.', room_type='underground', indoor=True)
    sp_silent_frame_04 = area.room('sp_silent_frame_04', name='Ward-Frame Bay', desc='Family tally cuts cross the outer plates of a folded ward-frame while older pattern-work continues beneath them. Clear floor marks preserve the corridors it blocks and those it ignores without claiming to know the distinction’s purpose.', room_type='underground', indoor=True)
    sp_pressure_mark_05 = area.room('sp_pressure_mark_05', name='Wax Witness', desc='Soft wax tiles surround a pressure mark without covering its center. Dated impressions reveal vibration, footsteps, and instrument weight, allowing Ysol to discard changes caused by the observers themselves.', room_type='underground', indoor=True)
    sp_sealed_pattern_06 = area.room('sp_sealed_pattern_06', name='Layered Seal', desc='Stone, clay, and metal closures from different periods overlap across part of the inlay. Each later inspection has opened only its own witness hatch, preserving older decisions while admitting that their reasons are incomplete.', room_type='underground', indoor=True)
    sp_threshold_line_07 = area.room('sp_threshold_line_07', name='Reversible Line', desc='Numbered brass feet hold a cord boundary without drilling into the old floor. Their ledger records every movement and the condition required to restore the previous layout, making even caution accountable.', room_type='underground', indoor=True)
    sp_old_inlay_08 = area.room('sp_old_inlay_08', name='Seam Comparison', desc='A fragment of the old inlay bends near a natural mineral seam but neither clearly follows nor crosses it. Ysol’s copies place the mine tracing beside several possible alignments and label every one unresolved.', room_type='underground', indoor=True)
    sp_silent_frame_09 = area.room('sp_silent_frame_09', name='Empty Mount', desc='Broken sockets and twitch-worn bell wires mark where a stone listening frame once stood. Its last stable measurements remain posted beside later motion reports, separating the instrument’s record from its current behavior.', room_type='underground', indoor=True)
    sp_pressure_mark_10 = area.room('sp_pressure_mark_10', name='Control Slab', desc='A plain slab of newer stone carries matching gauges for pressure, temperature, and sound. Differences between it and the patterned floor are logged before anyone attributes a change to the inlay itself.', room_type='underground', indoor=True)
    sp_sealed_pattern_11 = area.room('sp_sealed_pattern_11', name='Witnessed Closure', desc='A sealed recess bears intact wax from Resonance, Warden, and local family witnesses. The accompanying slate lists what was observed before closure and what nobody agreed upon, preserving uncertainty as part of the record.', room_type='underground', indoor=True)
    sp_threshold_line_12 = area.room('sp_threshold_line_12', name='Retreat Boundary', desc='A second threshold line faces back toward the chasm and carries hand signals for stop, withdraw, and account for everyone. Test notes emphasize how quickly the room can be left, not how boldly it can be entered.', room_type='underground', indoor=True)
    sp_old_inlay_13 = area.room('sp_old_inlay_13', name='Mineral Veil', desc='Natural mineral accretion hides much of an inlaid curve near the wall. Comparison sketches document the visible edges while a restraint notice forbids cleaning the veil until a non-damaging method is proven.', room_type='underground', indoor=True)
    sp_silent_frame_14 = area.room('sp_silent_frame_14', name='Deep Watch Frame', desc='An intact but silent measuring frame faces the passage into the Deep Listening Chamber. Removable gauges show no agreed response, and the handoff ledger carries observations forward without turning silence into proof.', room_type='underground', indoor=True)
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
