"""Korahei -- Hub 5 city zone

A circular Kau'roran island city of first bites, guest names, listening terraces, and careful welcome. The city teaches custom through play and service while routing players outward into reef, kiai, central-isle, and ruin stories."""

from world.area_builder import AreaBuilder


def build():
    area = AreaBuilder('korahei')

    area.zone(
        name='Korahei',
        zone_type='coastal',
        continent='veluana',
        tier=5,
        region='veluana_archipelago',
        hub_city='korahei',
        faction_territory='kauroran',
        faction_presence=['kauroran', 'wardens', 'consortium'],
        world_x=72,
        world_y=-6,
        world_radius=150,
    )

    area.material('reef_silverjack', tier=1, terrain='water', absorbed_property='finesse', profession_bonus={'cooking': 0.1, 'fishing': 0.05})
    area.material('saltfruit', tier=1, terrain='coastal', absorbed_property='endurance', profession_bonus={'cooking': 0.1})
    area.material('hearthroot', tier=2, terrain='garden', absorbed_property='warmth', profession_bonus={'cooking': 0.1, 'alchemy': 0.05})
    area.material('sunleaf', tier=1, terrain='garden', absorbed_property='clarity', profession_bonus={'alchemy': 0.1})
    area.material('reefstone', tier=1, terrain='reef', absorbed_property='durability', profession_bonus={'smithing': 0.1, 'engineering': 0.05})
    area.material('reefcrawler_shell', tier=1, terrain='reef', absorbed_property='protection', profession_bonus={'smithing': 0.1})
    area.material('saltpalm_wood', tier=1, terrain='coastal', absorbed_property='flexibility', profession_bonus={'engineering': 0.1})

    # Rooms
    ac_arrival_circle = area.room('ac_arrival_circle', name='Arrival Circle', desc="Korahei's first circle is open sky, woven shade, and benches sized for bodies far larger than most mainland guests. No gate bars the way, but every mat and water stone teaches the same rule: welcome begins with attention.", room_type='clearing')
    ac_first_bite_mat = area.room('ac_first_bite_mat', name='First-Bite Mat', desc='A round mat receives each fresh plate or cut fruit before anyone at its edge eats. The best first pieces pass to the people seated on either side, and a covered portion remains for the cook or courier who made the circle possible but cannot yet sit.', room_type='clearing')
    ac_guest_water_stone = area.room('ac_guest_water_stone', name='Guest Water Stone', desc='Cool jars occupy a waist-high stone beside cups of several shapes and grips. Fill and cleaning marks show which arrival crew tends them today, while an empty hook invites a guest to offer the next carried jar instead of mistaking welcome for limitless service.', room_type='clearing')
    ac_palm_welcome_shade = area.room('ac_palm_welcome_shade', name='Palm Welcome Shade', desc='Layered saltpalm panels shelter the broadest arrival benches from sun and sudden rain. Harvest and repair tags remain tied to every panel; mature replacement wood is marked on the work rack while living shade palms and fresh shoots stay outside the gathering cut.', room_type='clearing')
    ac_shell_chime_walk = area.room('ac_shell_chime_walk', name='Shell-Chime Walk', desc='Wave-worn shells sound softly along a curved walk whenever sea wind reaches the circle. Each chime bears its maker and home shore, and cracked pieces move to an inlay basket rather than being replaced with unmarked souvenirs from someone else’s beach.', room_type='clearing')
    ac_round_bench_of_names = area.room('ac_round_bench_of_names', name='Round Bench of Names', desc='New arrivals exchange names around a bench with no head and enough open places for companions still unloading. Pronunciation tiles can be corrected, withdrawn, or left blank, allowing welcome to remember a person without treating introduction as surrender of privacy.', room_type='clearing')
    ac_traveler_sandal_rack = area.room('ac_traveler_sandal_rack', name='Traveler Sandal Rack', desc='Salt-stiff sandals, wet boots, and bare-foot washing cloths occupy separate levels of an airy rack. Borrowed pairs carry return cords and repair tags, so the city’s comfort reaches a traveler without making the item—or the labor behind it—ownerless.', room_type='clearing')
    ac_woven_shade_rise = area.room('ac_woven_shade_rise', name='Woven Shade Rise', desc='A gentle ramp climbs through alternating panels of sun and saltpalm shade toward the courier posts. Route colors woven into the rail match reef, market, kiai, central-isle, and southern-boat notices, providing direction through city work instead of a list of attractions.', room_type='clearing')
    ac_low_tide_notice = area.room('ac_low_tide_notice', name='Living Tide Notice', desc='Painted stones show predicted low water beside shells placed at the actual reach of the most recent tide. Couriers add wind, current, and crossing reports throughout the day, and older mismatches remain visible so a guest learns quickly that the sea outranks the schedule.', room_type='clearing')
    ac_salt_washed_steps = area.room('ac_salt_washed_steps', name='Salt-Washed Steps', desc='Broad reefstone steps descend to a landing rinsed by spray at high water. Repair offcuts are sorted for useful gathering by quarry reach and failure mark, while load-bearing stones remain numbered in place for the masons tracking salt damage.', room_type='clearing')
    ac_runners_rest_mat = area.room('ac_runners_rest_mat', name="Runners' Rest Mat", desc='A shaded mat holds water, fruit, message tubes, and a board of routes waiting for rested carriers. Arrival and return times sit beside declined assignments, making fatigue and refusal part of safe scheduling rather than a private failure runners must hide.', room_type='clearing')
    ac_courier_ledger_post = area.room('ac_courier_ledger_post', name='Courier Ledger Post', desc='Runner Lani’s ledger tracks sender, recipient, route, tide window, carried supplies, and the person expected to confirm arrival. Corrections and missed handoffs stay attached to the route record, turning every delivery into safer knowledge for the next runner.', room_type='clearing')
    ac_courier_platform = area.room('ac_courier_platform', name='Courier Platform', desc='The courier platform rises above the arrival circle on saltpalm braces polished by bare hands. Handlers check tack, weather, and guest names here before any beast takes wing, making travel feel ceremonial without becoming spectacle.', room_type='clearing')
    ac_harbor_listening_rail = area.room('ac_harbor_listening_rail', name='Harbor Listening Rail', desc='A low rail overlooks the sheltered water where reef silverjack turn beneath arriving hulls. Catch marks track kept, released, and unusually absent fish beside boat traffic and tide, letting a meal gatherer add to harbor knowledge instead of taking from an invisible stock.', room_type='clearing')
    ac_guest_oath_bowl = area.room('ac_guest_oath_bowl', name='Guest Courtesy Bowl', desc='Guests choose a shell token naming one practical courtesy they can keep: ask names, share food, heed tide markers, return borrowed gear, or honor a closed path. The tokens are washed and reused on departure; the city judges conduct, not a vow made while everyone is watching.', room_type='clearing')
    ac_market_bend = area.room('ac_market_bend', name='Market Bend', desc='Smoke, fruit, fish, tool-song, and overlapping conversation reach the path before the Beach Market itself. A chalk board lists today’s shared hearths, repair circles, shortages, and people seeking help, so lingering begins with real needs and names.', room_type='clearing')
    ac_outer_mat_circle = area.room('ac_outer_mat_circle', name='Outfitter Mat Circle', desc='Reef Outfitter Pao arranges modest gear around an open mat with room to test fit, ask use, and return what is wrong. Route cards pair each tool with weather, care, and likely work rather than selling equipment as permission to ignore local warning.', room_type='clearing')
    ac_reef_warning_post = area.room('ac_reef_warning_post', name='Reef Warning Post', desc='Fresh cords mark current surge, damaged paths, reefcrawler activity, and crossings awaiting confirmation. Naturally shed and salvageable reefcrawler shell is sorted beneath the board by find-place and condition, while uncertain fragments stay out of trade until a keeper checks them.', room_type='clearing')
    ac_gate_of_shared_bread = area.room('ac_gate_of_shared_bread', name='Gate of Shared Bread', desc='A bread shelf stands where market, arrival, and reef paths divide, stocked by households and hearth crews throughout the day. Each loaf’s first pieces travel outward with the next runner, while a return ledger names which distant crew, guest, or watch still needs feeding.', room_type='clearing')
    ac_reef_gate = area.room('ac_reef_gate', name='Reef Gate', desc='Beyond this low gate the city paths loosen into reef stone and tide markers. Fresh warning cords hang beside baskets for shared food, a reminder that leaving Korahei means carrying its manners outward.', room_type='clearing')
    bm_beach_market_mouth = area.room('bm_beach_market_mouth', name='Beach Market Mouth', desc='Market stalls stand around communal hearths instead of in hard rows, so trade smells of smoke, fish, fruit, and argument. This part of the Beach Markets and Open Hearths centers on beach market mouth, where fish are portioned with the best bites set aside first. The market rewards players who linger: every stall points to a craft, a route, or a person worth knowing.', room_type='clearing')
    bm_saltfruit_awning = area.room('bm_saltfruit_awning', name='Saltfruit Awning', desc='Market stalls stand around communal hearths instead of in hard rows, so trade smells of smoke, fish, fruit, and argument. This part of the Beach Markets and Open Hearths centers on saltfruit awning, where shellbean baskets sit beside honest chalk prices. The market rewards players who linger: every stall points to a craft, a route, or a person worth knowing.', room_type='clearing')
    bm_silverjack_stall = area.room('bm_silverjack_stall', name='Silverjack Stall', desc='Market stalls stand around communal hearths instead of in hard rows, so trade smells of smoke, fish, fruit, and argument. This part of the Beach Markets and Open Hearths centers on silverjack stall, where net menders turn repairs into patient public lessons. The market rewards players who linger: every stall points to a craft, a route, or a person worth knowing.', room_type='clearing')
    bm_first_bite_hearth = area.room('bm_first_bite_hearth', name='First Bite Hearth', desc='Market stalls stand around communal hearths instead of in hard rows, so trade smells of smoke, fish, fruit, and argument. This part of the Beach Markets and Open Hearths centers on first bite hearth, where cooks call out who has eaten and who still needs a bowl. The market rewards players who linger: every stall points to a craft, a route, or a person worth knowing.', room_type='clearing')
    bm_open_smoke_pit = area.room('bm_open_smoke_pit', name='Open Smoke Pit', desc='Market stalls stand around communal hearths instead of in hard rows, so trade smells of smoke, fish, fruit, and argument. This part of the Beach Markets and Open Hearths centers on open smoke pit, where craft rings leave enough room for onlookers to learn. The market rewards players who linger: every stall points to a craft, a route, or a person worth knowing.', room_type='clearing')
    bm_shellbean_table = area.room('bm_shellbean_table', name='Shellbean Table', desc='Market stalls stand around communal hearths instead of in hard rows, so trade smells of smoke, fish, fruit, and argument. This part of the Beach Markets and Open Hearths centers on shellbean table, where fish are portioned with the best bites set aside first. The market rewards players who linger: every stall points to a craft, a route, or a person worth knowing.', room_type='clearing')
    bm_net_mender_circle = area.room('bm_net_mender_circle', name='Net-Mender Circle', desc='Market stalls stand around communal hearths instead of in hard rows, so trade smells of smoke, fish, fruit, and argument. This part of the Beach Markets and Open Hearths centers on net-mender circle, where shellbean baskets sit beside honest chalk prices. The market rewards players who linger: every stall points to a craft, a route, or a person worth knowing.', room_type='clearing')
    bm_reefstone_weighing_mat = area.room('bm_reefstone_weighing_mat', name='Reefstone Weighing Mat', desc='Market stalls stand around communal hearths instead of in hard rows, so trade smells of smoke, fish, fruit, and argument. This part of the Beach Markets and Open Hearths centers on reefstone weighing mat, where net menders turn repairs into patient public lessons. The market rewards players who linger: every stall points to a craft, a route, or a person worth knowing.', room_type='clearing')
    bm_bright_paddle_rack = area.room('bm_bright_paddle_rack', name='Bright Paddle Rack', desc='Market stalls stand around communal hearths instead of in hard rows, so trade smells of smoke, fish, fruit, and argument. This part of the Beach Markets and Open Hearths centers on bright paddle rack, where cooks call out who has eaten and who still needs a bowl. The market rewards players who linger: every stall points to a craft, a route, or a person worth knowing.', room_type='clearing')
    bm_hearthroot_basket = area.room('bm_hearthroot_basket', name='Hearthroot Basket', desc='Market stalls stand around communal hearths instead of in hard rows, so trade smells of smoke, fish, fruit, and argument. This part of the Beach Markets and Open Hearths centers on hearthroot basket, where craft rings leave enough room for onlookers to learn. The market rewards players who linger: every stall points to a craft, a route, or a person worth knowing.', room_type='clearing')
    bm_tide_mint_mortar = area.room('bm_tide_mint_mortar', name='Tide Mint Mortar', desc='Market stalls stand around communal hearths instead of in hard rows, so trade smells of smoke, fish, fruit, and argument. This part of the Beach Markets and Open Hearths centers on tide mint mortar, where fish are portioned with the best bites set aside first. The market rewards players who linger: every stall points to a craft, a route, or a person worth knowing.', room_type='clearing')
    bm_shared_bowl_bench = area.room('bm_shared_bowl_bench', name='Shared Bowl Bench', desc='Market stalls stand around communal hearths instead of in hard rows, so trade smells of smoke, fish, fruit, and argument. This part of the Beach Markets and Open Hearths centers on shared bowl bench, where shellbean baskets sit beside honest chalk prices. The market rewards players who linger: every stall points to a craft, a route, or a person worth knowing.', room_type='clearing')
    bm_laughing_cookfire = area.room('bm_laughing_cookfire', name='Laughing Cookfire', desc='Market stalls stand around communal hearths instead of in hard rows, so trade smells of smoke, fish, fruit, and argument. This part of the Beach Markets and Open Hearths centers on laughing cookfire, where net menders turn repairs into patient public lessons. The market rewards players who linger: every stall points to a craft, a route, or a person worth knowing.', room_type='clearing')
    bm_visitor_portion_line = area.room('bm_visitor_portion_line', name='Visitor Portion Line', desc='Market stalls stand around communal hearths instead of in hard rows, so trade smells of smoke, fish, fruit, and argument. This part of the Beach Markets and Open Hearths centers on visitor portion line, where cooks call out who has eaten and who still needs a bowl. The market rewards players who linger: every stall points to a craft, a route, or a person worth knowing.', room_type='clearing')
    bm_tool_menders_shade = area.room('bm_tool_menders_shade', name="Tool Mender's Shade", desc="Market stalls stand around communal hearths instead of in hard rows, so trade smells of smoke, fish, fruit, and argument. This part of the Beach Markets and Open Hearths centers on tool mender's shade, where craft rings leave enough room for onlookers to learn. The market rewards players who linger: every stall points to a craft, a route, or a person worth knowing.", room_type='clearing')
    bm_fish_salt_barrel = area.room('bm_fish_salt_barrel', name='Fish-Salt Barrel', desc='Market stalls stand around communal hearths instead of in hard rows, so trade smells of smoke, fish, fruit, and argument. This part of the Beach Markets and Open Hearths centers on fish-salt barrel, where fish are portioned with the best bites set aside first. The market rewards players who linger: every stall points to a craft, a route, or a person worth knowing.', room_type='clearing')
    bm_kelp_press_stand = area.room('bm_kelp_press_stand', name='Kelp Press Stand', desc='Market stalls stand around communal hearths instead of in hard rows, so trade smells of smoke, fish, fruit, and argument. This part of the Beach Markets and Open Hearths centers on kelp press stand, where shellbean baskets sit beside honest chalk prices. The market rewards players who linger: every stall points to a craft, a route, or a person worth knowing.', room_type='clearing')
    bm_market_story_post = area.room('bm_market_story_post', name='Market Story Post', desc='Market stalls stand around communal hearths instead of in hard rows, so trade smells of smoke, fish, fruit, and argument. This part of the Beach Markets and Open Hearths centers on market story post, where net menders turn repairs into patient public lessons. The market rewards players who linger: every stall points to a craft, a route, or a person worth knowing.', room_type='clearing')
    bm_long_spoon_hearth = area.room('bm_long_spoon_hearth', name='Long Spoon Hearth', desc='Market stalls stand around communal hearths instead of in hard rows, so trade smells of smoke, fish, fruit, and argument. This part of the Beach Markets and Open Hearths centers on long spoon hearth, where cooks call out who has eaten and who still needs a bowl. The market rewards players who linger: every stall points to a craft, a route, or a person worth knowing.', room_type='clearing')
    bm_evening_ember_ring = area.room('bm_evening_ember_ring', name='Evening Ember Ring', desc='Market stalls stand around communal hearths instead of in hard rows, so trade smells of smoke, fish, fruit, and argument. This part of the Beach Markets and Open Hearths centers on evening ember ring, where craft rings leave enough room for onlookers to learn. The market rewards players who linger: every stall points to a craft, a route, or a person worth knowing.', room_type='clearing')
    kg_kiai_gate = area.room('kg_kiai_gate', name='Kiai Gate', desc='The northern gate is less an entrance than a pause. Braided witness cords, covered drums, and plain water jars make it clear that the kiai road is not a shortcut to glory; it is a place to arrive correctly.', room_type='path')
    kg_witness_cord_post = area.room('kg_witness_cord_post', name='Witness Cord Post', desc='Plain cords identify the work someone is doing today—guest, witness, caretaker, runner, or council listener—without granting rank over the road. Each cord is returned, washed, and reassigned at departure, keeping a useful role from hardening into identity or permanent authority.', room_type='path')
    kg_council_shell_ring = area.room('kg_council_shell_ring', name='Council Shell Ring', desc='Shell markers circle a mat with no head seat, each representing a household, care crew, route, or open concern. Speakers move their marker inward when heard and outward when new evidence changes their position, leaving disagreement visible without demanding a winner before the tide turns.', room_type='path')
    kg_tide_law_bench = area.room('kg_tide_law_bench', name='Tide-Law Bench', desc='Public rulings on crossings, gathering limits, guest access, and storm closure are copied onto replaceable slats. Each names the observed tide or harm that prompted it and the date for review, treating law as accountable stewardship rather than custom beyond question.', room_type='path')
    kg_caretaker_ledger = area.room('kg_caretaker_ledger', name='Caretaker Route Ledger', desc='Care crews record people, supplies, privacy requests, repairs, and weather moving between Korahei and the Kiai Grounds. A returned mark closes each responsibility; overdue entries summon a conversation or search, not an assumption that sacred work excuses poor handoff.', room_type='path')
    kg_unlit_drum_porch = area.room('kg_unlit_drum_porch', name='Covered Drum Porch', desc='Ceremonial drums rest under fitted covers with tension, humidity, and repair dates posted beside them. Practice pads occupy a separate rack, allowing drummers to remain ready through ordinary seasons without making every rehearsal sound like an invitation.', room_type='path')
    kg_young_candidate_shade = area.room('kg_young_candidate_shade', name='Young Candidate Shade', desc='A shaded circle gives younger candidates, families, and chosen companions room to discuss readiness away from the gate. Boards name rights to pause, leave, return, change one’s mind, and remain fully part of Korahei whether or not any choosing ever occurs.', room_type='path')
    kg_guest_boundary_stone = area.room('kg_guest_boundary_stone', name='Guest Boundary Stone', desc='Moveable inlays show which parts of the road are open, quiet, working, private, or closed today. Guests are asked to confirm the current pattern with a keeper rather than treating an earlier invitation as lasting access to every gathering.', room_type='path')
    kg_braid_makers_nook = area.room('kg_braid_makers_nook', name="Braid-Makers' Nook", desc='Braid-makers weave role cords, boundary line, drum ties, and repair lashings from fibers labeled by source and strength. Old cords are unpicked in public, revealing which colors faded or knots slipped so ceremony materials remain as accountable as working rope.', room_type='path')
    kg_north_wind_steps = area.room('kg_north_wind_steps', name='North-Wind Steps', desc='Crosswind reaches these steps before the sheltered city path, carrying grass scent and hints of rain from the grounds. Streamers at several heights feed the caretaker route board, while a ramp behind the wall offers a steadier approach without being treated as a lesser arrival.', room_type='path')
    kg_quiet_hoof_sand = area.room('kg_quiet_hoof_sand', name='Quiet Hoof Sand', desc='Deep sand softens the passage of pack animals carrying water, mats, and repair supplies north. Handlers record load, gait, rest, and any rubbed tack at the exit, making the quiet road gentler through attention rather than demanding silence from working bodies.', room_type='path')
    kg_ceremony_water_jar = area.room('kg_ceremony_water_jar', name='Road Water Circle', desc='Covered jars serve candidates, witnesses, guests, caretakers, and pack handlers from the same ring. Fill and cleaning counts remain useful on days without ceremony, and a reserved jug is labeled for the return journey so anticipation cannot consume every supply.', room_type='path')
    kg_warden_courtesy_mat = area.room('kg_warden_courtesy_mat', name='Warden Courtesy Mat', desc='Warden Iren receives local route, privacy, and authority limits on a blue-edged guest mat. Courtesy notes request an introduction rather than command access; accepted, changed, and declined requests all remain in the handoff record.', room_type='path')
    kg_old_promise_stone = area.room('kg_old_promise_stone', name='Promises We Can Keep', desc='An old stone lists promises witnesses and caretakers can make: prepare honestly, protect choice, share food, keep names, admit uncertainty, and return what was entrusted. No line promises a dragon, a bond, or a result, because those are not human gifts to offer.', room_type='path')
    kg_listening_guardrail = area.room('kg_listening_guardrail', name='Listening Guardrail', desc='A smooth rail overlooks the grass without exposing the waiting rings beyond the bend. Listening marks distinguish weather, animals, drums, calls for aid, and sounds left uncertain, training attention for safety without turning private quiet into public evidence.', room_type='path')
    kg_pale_garland_wall = area.room('kg_pale_garland_wall', name='Garland Return Wall', desc='Pale garlands hang by source garden, use, and return date along a cool wall. Wilted flowers move to seed or compost baskets, reusable ties go to washing, and untouched garlands remain available for another gathering instead of becoming proof that an event must occur.', room_type='path')
    kg_gatekeepers_rest = area.room('kg_gatekeepers_rest', name="Gatekeepers' Rest", desc='Two shaded benches let outgoing and incoming keepers overlap long enough to exchange current names, boundaries, weather, supplies, and expected returns. Food and water are counted into the watch, recognizing that patient judgment depends on rested people rather than endless vigilance.', room_type='path')
    kg_high_grass_turn = area.room('kg_high_grass_turn', name='High-Grass Turn', desc='Tall grass closes around the city path, crossed by narrow animal tracks and the wider maintenance road. Fresh flags show where caretakers recently moved foot traffic to protect nesting or wet ground, making the route responsive to life outside the ceremony calendar.', room_type='path')
    kg_distant_ring_view = area.room('kg_distant_ring_view', name='Distant Ring View', desc='Care roofs and outer waiting circles appear through breaks in the grass, with inner spaces hidden by distance and screens. The view helps keepers judge smoke, crowding, and weather only; no observer here can declare what a dragon or candidate intends.', room_type='path')
    kg_witness_road_bend = area.room('kg_witness_road_bend', name='Witness Road Bend', desc='The city’s tide-council slats, guest cords, and courtesy notes pass into the Kiai Grounds handoff at this final bend. A return rack waits beside the northward path, making every arrival incomplete until names, tools, and responsibilities come back or are deliberately transferred.', room_type='path')
    lt_lower_listening_step = area.room('lt_lower_listening_step', name='Lower Listening Step', desc='Wide steps climb between open craft circles where work remains visible from the street. A daily board lists who is teaching, who wants another pair of hands, and who is available only to listen, allowing skill and attention to circulate without turning every elder into public property.', room_type='building')
    lt_carvers_quiet_rail = area.room('lt_carvers_quiet_rail', name="Carvers' Quiet Rail", desc='Carvers work beside a padded rail that catches chips before they tumble onto the terraces below. Scraps are sorted by wood, shell, stone, owner, and next use, while a quiet marker gives delicate cuts protection from well-meaning conversation.', room_type='building')
    lt_saltpalm_work_circle = area.room('lt_saltpalm_work_circle', name='Saltpalm Work Circle', desc='Fresh saltpalm lengths lie around a circular bench with grove, harvest, cure, and intended-load marks intact. Split or flawed pieces become teaching stock and small repairs, leaving sound lengths traceable to the living stand that must replace them.', room_type='building')
    lt_shell_inlay_bench = area.room('lt_shell_inlay_bench', name='Shell Inlay Bench', desc='Wave-broken shell and market offcuts are fitted into bowls, paddles, and name plaques at a low bench. Family patterns are copied only with a permission token beside the design, distinguishing shared technique from a guest’s casual claim on someone else’s history.', room_type='building')
    lt_cordage_lesson_mat = area.room('lt_cordage_lesson_mat', name='Cordage Lesson Mat', desc='Fibers at every stage—from cleaned leaf to retired line—are arranged around a woven teaching mat. Learners test knots under wet, dry, and angled loads, then label the failed pieces so a pretty braid cannot drift back into safety work.', room_type='building')
    lt_name_practice_terrace = area.room('lt_name_practice_terrace', name='Name-Practice Terrace', desc='Shell tiles carry guest-approved syllable breaks, stress marks, and corrections in the speaker’s own hand. Practice happens face to face, with room to ask again or admit a forgotten sound; accuracy is treated as care, not a performance of effortless belonging.', room_type='building')
    lt_listening_step = area.room('lt_listening_step', name='Listening Step', desc='Name-Keeper Haoa sits where market, craft, and guest paths meet, introducing people alongside the obligations that make their names matter today. Pronunciation marks, requested boundaries, and promised errands remain revisable, so trust grows from remembered conduct rather than a frozen label.', room_type='building')
    lt_tide_scratch_wall = area.room('lt_tide_scratch_wall', name='Tide-Scratch Wall', desc='Lines cut into a low wall record exceptional tides beside family observations of wind, moon, current, and damage. Conflicting marks share the same dated span, giving boat crews a history to test instead of a single inherited rule that the sea may already have disproved.', room_type='building')
    lt_open_palm_archive = area.room('lt_open_palm_archive', name='Open-Palm Archive', desc='Open shelves hold copied route notes, repair patterns, introductions, and public agreements within reach of the terrace. Private names and sensitive histories are represented by request tokens pointing to their keepers, making access a conversation rather than either secrecy or entitlement.', room_type='building')
    lt_scholars_woven_seat = area.room('lt_scholars_woven_seat', name="Scholars' Woven Circle", desc='Woven seats form a circle around a table scarred by revisions, spilled tea, and weighted charts. No chair faces the others as authority; speakers cite who taught them, listeners mark uncertainty, and corrections stay attached to the account they changed.', room_type='building')
    lt_round_loom_platform = area.room('lt_round_loom_platform', name='Round Loom Platform', desc='A circular loom lets several weavers share one growing shade panel without surrendering individual tension lines. Color tags identify each repair and material source, while open sections reserve space for the household that will install and later maintain the finished work.', room_type='building')
    lt_paddle_pattern_rack = area.room('lt_paddle_pattern_rack', name='Paddle Pattern Rack', desc='Practice paddles hang by size and weight, each one marked with cuts that teach grip before force. Students work the rack in measured turns, learning that a clean strike begins with a clean approach.', room_type='building')
    lt_guest_story_mat = area.room('lt_guest_story_mat', name='Guest Story Mat', desc='Guests may offer route news or personal accounts from a mat marked with pause, correction, private, and share signs. A listener repeats what may travel beyond the terrace before recording anything, letting a story enter Korahei’s memory without ceasing to belong to its teller.', room_type='building')
    lt_high_terrace_well = area.room('lt_high_terrace_well', name='High Terrace Well', desc='A deep, cool well serves craft rinsing, drinking jars, and the upper shade gardens through separately marked buckets. Draw counts and salt tests hang beside the crank, linking every lesson and gathering to the shared water that makes the terraces possible.', room_type='building')
    lt_soft_hammer_ring = area.room('lt_soft_hammer_ring', name='Soft Hammer Ring', desc='Soft hammers circle a sanded practice ring where counterweighted frames swing back just hard enough to teach caution. Elders watch for control, not victory, and the benches make room for advice after every exchange.', room_type='building')
    lt_shared_tool_shelf = area.room('lt_shared_tool_shelf', name='Shared Tool Shelf', desc='The shared shelf carries soft hammers, chalked hand wraps, and little tags naming who repaired what. Sparring frames stand nearby so practice feels tied to stewardship instead of a private contest.', room_type='building')
    lt_repair_song_niche = area.room('lt_repair_song_niche', name='Repair Song Niche', desc='A small niche holds padded dummies, mended frames, and the low repair songs used to keep rhythm steady. Nothing here rewards bravado; the lesson is to strike, reset, and leave the tools ready for the next learner.', room_type='building')
    lt_sunleaf_drying_rail = area.room('lt_sunleaf_drying_rail', name='Sunleaf Drying Rail', desc='Sunleaf bundles hang by garden plot, cutting date, wash, and intended preparation along a rail open to the sea breeze. Mature leaves occupy the gathering section while seed stalks and stressed plants remain marked for return, keeping clarity tied to renewable care.', room_type='building')
    lt_central_isle_lookout = area.room('lt_central_isle_lookout', name='Central Isle Lookout', desc='The eastern water path and Central Isle appear between carved route paddles at the terrace edge. Pathfinder notes describe currents, landings, and observations that changed on a second loop, but refuse to turn the island’s unsettling shapes into a solved map from this distance.', room_type='building')
    lt_central_path = area.room('lt_central_path', name='Central Path', desc='The eastern terrace path points toward the central isle through carved paddles and shell-cairn route marks. Listeners leave chalk notes here for travelers: walk the loop twice, trust the second silence, return with what you noticed.', room_type='building')
    qh_quiet_house_porch = area.room('qh_quiet_house_porch', name='Quiet House Porch', desc='The market road softens into a porch of plain bowls, shaded mats, and seats that can face together or apart. Mareva greets people without asking them to explain their grief, and a small board offers food, water, names, company, silence, or the southern boat path without ranking those needs.', room_type='building')
    qh_sunleaf_water_basin = area.room('qh_sunleaf_water_basin', name='Sunleaf Water Basin', desc='Clean water and floating sunleaf cool a stone basin used for hands, cloths, and quiet-house cups. Harvest ties identify garden and cutting date, while mature leaves occupy the gathering edge and seed stalks remain reserved for the next planting.', room_type='building')
    qh_plain_bowl_shelf = area.room('qh_plain_bowl_shelf', name='Plain Bowl Shelf', desc='Unadorned bowls wait in open rows beside wash, dry, repair, and return marks. Some travel south carrying food or a name; others remain empty because offering a vessel does not oblige anyone to fill it with a story.', room_type='building')
    qh_grief_mat_circle = area.room('qh_grief_mat_circle', name='Grief Mat Circle', desc='Mats form an incomplete circle with easy paths out and no seat reserved for a speaker. People may share memory, food, anger, uncertainty, or nothing at all, and witness cords state clearly what may be repeated beyond the room.', room_type='building')
    qh_low_voice_hall = area.room('qh_low_voice_hall', name='Low-Voice Hall', desc='Layered reed walls soften market and surf noise without demanding perfect silence from children, pain, or work. Hand signs and writing boards support conversation at different volumes, keeping quiet available as care rather than enforced solemnity.', room_type='building')
    qh_name_cloth_alcove = area.room('qh_name_cloth_alcove', name='Name-Cloth Alcove', desc='Cloths carry names offered by families and listeners, with pronunciation, privacy, and remembrance marks stitched beside them. Blank cloths stand for people not yet named or not given to public memory, preserving absence without inviting a visitor to invent an identity.', room_type='building')
    qh_ash_washed_threshold = area.room('qh_ash_washed_threshold', name='Ash-Washed Threshold', desc='Fine wood ash and water keep this threshold pale beneath generations of passing feet. Cleaning dates sit beside older scorch discoloration whose story is not posted for guests, distinguishing visible evidence from a community’s obligation to explain it.', room_type='building')
    qh_caretakers_small_table = area.room('qh_caretakers_small_table', name="Caretakers' Small Table", desc='Mareva’s care table tracks meals, wash, requested listeners, boat weather, private rooms, and names awaiting confirmation. Every task has an owner and return check, while declined help stays recorded only long enough to prevent the same intrusive offer from circling back.', room_type='building')
    qh_southern_shell_window = area.room('qh_southern_shell_window', name='Southern Shell Window', desc='A shell-latticed window admits salt air and a narrow view of the southern water without framing the distant ruins as scenery. Tide and boat lights can be checked through marked openings; the rest remains screened for people who came here to remember rather than look outward.', room_type='building')
    qh_visitor_pause_stone = area.room('qh_visitor_pause_stone', name='Visitor Pause Stone', desc='A stone beside the southern door asks visitors what they carry toward the ruins and for whom. Route help, listening, care, and accountable research are named; collecting proof, taking keepsakes, and demanding private history are not softened into curiosity.', room_type='building')
    qh_tide_silence_bench = area.room('qh_tide_silence_bench', name='Tide-Silence Bench', desc='The surf briefly quiets behind the breakwater at certain tides, though wind and passing boats often interrupt the interval. Listeners record when the hush actually occurred and let missed silence remain missed, refusing to manufacture a solemn moment for an impatient schedule.', room_type='building')
    qh_offering_basket_niche = area.room('qh_offering_basket_niche', name='Useful-Offering Niche', desc='Baskets request food, clean cloth, lamp oil, repair fiber, copied route notes, and other needs chosen by the Quiet House. Decorative or anonymous offerings wait for review rather than entering memory by default, keeping generosity answerable to the people meant to receive it.', room_type='building')
    qh_mended_paddle_rack = area.room('qh_mended_paddle_rack', name='Mended Paddle Rack', desc='Paddles bound for the southern crossing bear repair, flex, water-test, and assigned-boat marks along their shafts. Retired paddles remain split open beside the rack so future crews can see whether salt, impact, grain, or poor mending ended their service.', room_type='building')
    qh_ruins_warning_board = area.room('qh_ruins_warning_board', name='Ruins Passage Board', desc='Current tide, fire damage, unstable walls, private remembrance areas, listener contacts, and strict no-salvage boundaries cover a public board. Updates name their Kau’roran authority and review date; an open route grants passage, never ownership of what survived there.', room_type='building')
    qh_boat_hook_wall = area.room('qh_boat_hook_wall', name='Boat Hook Wall', desc='Hooks, lines, fenders, bailers, and covered bowl crates hang by boat and inspection date. Equipment returned wet or damaged moves to a bright repair row, making a respectful voyage include the uncelebrated work of leaving the next crew safe.', room_type='building')
    qh_south_sand_stair = area.room('qh_south_sand_stair', name='South Sand Stair', desc='Wide steps descend through drifting sand toward the low landing, with raised tide marks readable by hand along the rail. Sweep crews record buried edges and changed footing each day, and a higher switchback remains open when water or mobility makes the direct stair unsafe.', room_type='building')
    qh_breakwater_shrine = area.room('qh_breakwater_shrine', name='Breakwater Garden Shrine', desc='Hearthroot grows in sheltered beds among stones naming boat crews, listeners, and families who maintain the southern passage. Harvest markers permit mature roots from replenished rows, while remembrance plantings and new divisions remain untouched until their keepers open them.', room_type='building')
    qh_low_boat_landing = area.room('qh_low_boat_landing', name='Low Boat Landing', desc='The landing serves fishing skiffs, listener boats, and the narrow ruins craft without giving any one voyage priority over weather. Reef silverjack gather beneath its shadow; catch tallies sit beside passenger, tide, and return records so taking food remains part of harbor stewardship.', room_type='building')
    qh_quiet_oar_stand = area.room('qh_quiet_oar_stand', name='Quiet Oar Stand', desc='Matched oars rest in padded slots where their blades cannot knock together in the Quiet House lee. Weight, balance, repair, and boat assignments are checked before departure, allowing a restrained launch to come from preparation rather than ritualized secrecy.', room_type='building')
    qh_ruins_boat = area.room('qh_ruins_boat', name='Ruins Boat', desc='A narrow boat waits below the Quiet House with plain oars, a covered bowl shelf, and warning knots tied into the painter. The craft is ready for the ruins, but nothing about it invites sightseeing.', room_type='building')

    # Local exits
    area.exit(ac_arrival_circle, ac_first_bite_mat, 'east')
    area.exit(ac_first_bite_mat, ac_arrival_circle, 'west')
    area.exit(ac_first_bite_mat, ac_guest_water_stone, 'east')
    area.exit(ac_guest_water_stone, ac_first_bite_mat, 'west')
    area.exit(ac_guest_water_stone, ac_palm_welcome_shade, 'east')
    area.exit(ac_palm_welcome_shade, ac_guest_water_stone, 'west')
    area.exit(ac_palm_welcome_shade, ac_shell_chime_walk, 'east')
    area.exit(ac_shell_chime_walk, ac_palm_welcome_shade, 'west')
    area.exit(ac_shell_chime_walk, ac_round_bench_of_names, 'east')
    area.exit(ac_round_bench_of_names, ac_shell_chime_walk, 'west')
    area.exit(ac_round_bench_of_names, ac_traveler_sandal_rack, 'east')
    area.exit(ac_traveler_sandal_rack, ac_round_bench_of_names, 'west')
    area.exit(ac_traveler_sandal_rack, ac_woven_shade_rise, 'east')
    area.exit(ac_woven_shade_rise, ac_traveler_sandal_rack, 'west')
    area.exit(ac_woven_shade_rise, ac_low_tide_notice, 'east')
    area.exit(ac_low_tide_notice, ac_woven_shade_rise, 'west')
    area.exit(ac_low_tide_notice, ac_salt_washed_steps, 'east')
    area.exit(ac_salt_washed_steps, ac_low_tide_notice, 'west')
    area.exit(ac_salt_washed_steps, ac_runners_rest_mat, 'east')
    area.exit(ac_runners_rest_mat, ac_salt_washed_steps, 'west')
    area.exit(ac_runners_rest_mat, ac_courier_ledger_post, 'east')
    area.exit(ac_courier_ledger_post, ac_runners_rest_mat, 'west')
    area.exit(ac_courier_ledger_post, ac_courier_platform, 'east')
    area.exit(ac_courier_platform, ac_courier_ledger_post, 'west')
    area.exit(ac_courier_platform, ac_harbor_listening_rail, 'east')
    area.exit(ac_harbor_listening_rail, ac_courier_platform, 'west')
    area.exit(ac_harbor_listening_rail, ac_guest_oath_bowl, 'east')
    area.exit(ac_guest_oath_bowl, ac_harbor_listening_rail, 'west')
    area.exit(ac_guest_oath_bowl, ac_market_bend, 'east')
    area.exit(ac_market_bend, ac_guest_oath_bowl, 'west')
    area.exit(ac_market_bend, ac_outer_mat_circle, 'east')
    area.exit(ac_outer_mat_circle, ac_market_bend, 'west')
    area.exit(ac_outer_mat_circle, ac_reef_warning_post, 'east')
    area.exit(ac_reef_warning_post, ac_outer_mat_circle, 'west')
    area.exit(ac_reef_warning_post, ac_gate_of_shared_bread, 'east')
    area.exit(ac_gate_of_shared_bread, ac_reef_warning_post, 'west')
    area.exit(ac_gate_of_shared_bread, ac_reef_gate, 'east')
    area.exit(ac_reef_gate, ac_gate_of_shared_bread, 'west')
    area.exit(bm_beach_market_mouth, bm_saltfruit_awning, 'east')
    area.exit(bm_saltfruit_awning, bm_beach_market_mouth, 'west')
    area.exit(bm_saltfruit_awning, bm_silverjack_stall, 'east')
    area.exit(bm_silverjack_stall, bm_saltfruit_awning, 'west')
    area.exit(bm_silverjack_stall, bm_first_bite_hearth, 'east')
    area.exit(bm_first_bite_hearth, bm_silverjack_stall, 'west')
    area.exit(bm_first_bite_hearth, bm_open_smoke_pit, 'east')
    area.exit(bm_open_smoke_pit, bm_first_bite_hearth, 'west')
    area.exit(bm_open_smoke_pit, bm_shellbean_table, 'east')
    area.exit(bm_shellbean_table, bm_open_smoke_pit, 'west')
    area.exit(bm_shellbean_table, bm_net_mender_circle, 'east')
    area.exit(bm_net_mender_circle, bm_shellbean_table, 'west')
    area.exit(bm_net_mender_circle, bm_reefstone_weighing_mat, 'east')
    area.exit(bm_reefstone_weighing_mat, bm_net_mender_circle, 'west')
    area.exit(bm_reefstone_weighing_mat, bm_bright_paddle_rack, 'east')
    area.exit(bm_bright_paddle_rack, bm_reefstone_weighing_mat, 'west')
    area.exit(bm_bright_paddle_rack, bm_hearthroot_basket, 'east')
    area.exit(bm_hearthroot_basket, bm_bright_paddle_rack, 'west')
    area.exit(bm_hearthroot_basket, bm_tide_mint_mortar, 'east')
    area.exit(bm_tide_mint_mortar, bm_hearthroot_basket, 'west')
    area.exit(bm_tide_mint_mortar, bm_shared_bowl_bench, 'east')
    area.exit(bm_shared_bowl_bench, bm_tide_mint_mortar, 'west')
    area.exit(bm_shared_bowl_bench, bm_laughing_cookfire, 'east')
    area.exit(bm_laughing_cookfire, bm_shared_bowl_bench, 'west')
    area.exit(bm_laughing_cookfire, bm_visitor_portion_line, 'east')
    area.exit(bm_visitor_portion_line, bm_laughing_cookfire, 'west')
    area.exit(bm_visitor_portion_line, bm_tool_menders_shade, 'east')
    area.exit(bm_tool_menders_shade, bm_visitor_portion_line, 'west')
    area.exit(bm_tool_menders_shade, bm_fish_salt_barrel, 'east')
    area.exit(bm_fish_salt_barrel, bm_tool_menders_shade, 'west')
    area.exit(bm_fish_salt_barrel, bm_kelp_press_stand, 'east')
    area.exit(bm_kelp_press_stand, bm_fish_salt_barrel, 'west')
    area.exit(bm_kelp_press_stand, bm_market_story_post, 'east')
    area.exit(bm_market_story_post, bm_kelp_press_stand, 'west')
    area.exit(bm_market_story_post, bm_long_spoon_hearth, 'east')
    area.exit(bm_long_spoon_hearth, bm_market_story_post, 'west')
    area.exit(bm_long_spoon_hearth, bm_evening_ember_ring, 'east')
    area.exit(bm_evening_ember_ring, bm_long_spoon_hearth, 'west')
    area.exit(kg_kiai_gate, kg_witness_cord_post, 'east')
    area.exit(kg_witness_cord_post, kg_kiai_gate, 'west')
    area.exit(kg_witness_cord_post, kg_council_shell_ring, 'east')
    area.exit(kg_council_shell_ring, kg_witness_cord_post, 'west')
    area.exit(kg_council_shell_ring, kg_tide_law_bench, 'east')
    area.exit(kg_tide_law_bench, kg_council_shell_ring, 'west')
    area.exit(kg_tide_law_bench, kg_caretaker_ledger, 'east')
    area.exit(kg_caretaker_ledger, kg_tide_law_bench, 'west')
    area.exit(kg_caretaker_ledger, kg_unlit_drum_porch, 'east')
    area.exit(kg_unlit_drum_porch, kg_caretaker_ledger, 'west')
    area.exit(kg_unlit_drum_porch, kg_young_candidate_shade, 'east')
    area.exit(kg_young_candidate_shade, kg_unlit_drum_porch, 'west')
    area.exit(kg_young_candidate_shade, kg_guest_boundary_stone, 'east')
    area.exit(kg_guest_boundary_stone, kg_young_candidate_shade, 'west')
    area.exit(kg_guest_boundary_stone, kg_braid_makers_nook, 'east')
    area.exit(kg_braid_makers_nook, kg_guest_boundary_stone, 'west')
    area.exit(kg_braid_makers_nook, kg_north_wind_steps, 'east')
    area.exit(kg_north_wind_steps, kg_braid_makers_nook, 'west')
    area.exit(kg_north_wind_steps, kg_quiet_hoof_sand, 'east')
    area.exit(kg_quiet_hoof_sand, kg_north_wind_steps, 'west')
    area.exit(kg_quiet_hoof_sand, kg_ceremony_water_jar, 'east')
    area.exit(kg_ceremony_water_jar, kg_quiet_hoof_sand, 'west')
    area.exit(kg_ceremony_water_jar, kg_warden_courtesy_mat, 'east')
    area.exit(kg_warden_courtesy_mat, kg_ceremony_water_jar, 'west')
    area.exit(kg_warden_courtesy_mat, kg_old_promise_stone, 'east')
    area.exit(kg_old_promise_stone, kg_warden_courtesy_mat, 'west')
    area.exit(kg_old_promise_stone, kg_listening_guardrail, 'east')
    area.exit(kg_listening_guardrail, kg_old_promise_stone, 'west')
    area.exit(kg_listening_guardrail, kg_pale_garland_wall, 'east')
    area.exit(kg_pale_garland_wall, kg_listening_guardrail, 'west')
    area.exit(kg_pale_garland_wall, kg_gatekeepers_rest, 'east')
    area.exit(kg_gatekeepers_rest, kg_pale_garland_wall, 'west')
    area.exit(kg_gatekeepers_rest, kg_high_grass_turn, 'east')
    area.exit(kg_high_grass_turn, kg_gatekeepers_rest, 'west')
    area.exit(kg_high_grass_turn, kg_distant_ring_view, 'east')
    area.exit(kg_distant_ring_view, kg_high_grass_turn, 'west')
    area.exit(kg_distant_ring_view, kg_witness_road_bend, 'east')
    area.exit(kg_witness_road_bend, kg_distant_ring_view, 'west')
    area.exit(lt_lower_listening_step, lt_carvers_quiet_rail, 'east')
    area.exit(lt_carvers_quiet_rail, lt_lower_listening_step, 'west')
    area.exit(lt_carvers_quiet_rail, lt_saltpalm_work_circle, 'east')
    area.exit(lt_saltpalm_work_circle, lt_carvers_quiet_rail, 'west')
    area.exit(lt_saltpalm_work_circle, lt_shell_inlay_bench, 'east')
    area.exit(lt_shell_inlay_bench, lt_saltpalm_work_circle, 'west')
    area.exit(lt_shell_inlay_bench, lt_cordage_lesson_mat, 'east')
    area.exit(lt_cordage_lesson_mat, lt_shell_inlay_bench, 'west')
    area.exit(lt_cordage_lesson_mat, lt_name_practice_terrace, 'east')
    area.exit(lt_name_practice_terrace, lt_cordage_lesson_mat, 'west')
    area.exit(lt_name_practice_terrace, lt_listening_step, 'east')
    area.exit(lt_listening_step, lt_name_practice_terrace, 'west')
    area.exit(lt_listening_step, lt_tide_scratch_wall, 'east')
    area.exit(lt_tide_scratch_wall, lt_listening_step, 'west')
    area.exit(lt_tide_scratch_wall, lt_open_palm_archive, 'east')
    area.exit(lt_open_palm_archive, lt_tide_scratch_wall, 'west')
    area.exit(lt_open_palm_archive, lt_scholars_woven_seat, 'east')
    area.exit(lt_scholars_woven_seat, lt_open_palm_archive, 'west')
    area.exit(lt_scholars_woven_seat, lt_round_loom_platform, 'east')
    area.exit(lt_round_loom_platform, lt_scholars_woven_seat, 'west')
    area.exit(lt_round_loom_platform, lt_paddle_pattern_rack, 'east')
    area.exit(lt_paddle_pattern_rack, lt_round_loom_platform, 'west')
    area.exit(lt_paddle_pattern_rack, lt_guest_story_mat, 'east')
    area.exit(lt_guest_story_mat, lt_paddle_pattern_rack, 'west')
    area.exit(lt_guest_story_mat, lt_high_terrace_well, 'east')
    area.exit(lt_high_terrace_well, lt_guest_story_mat, 'west')
    area.exit(lt_high_terrace_well, lt_soft_hammer_ring, 'east')
    area.exit(lt_soft_hammer_ring, lt_high_terrace_well, 'west')
    area.exit(lt_soft_hammer_ring, lt_shared_tool_shelf, 'east')
    area.exit(lt_shared_tool_shelf, lt_soft_hammer_ring, 'west')
    area.exit(lt_shared_tool_shelf, lt_repair_song_niche, 'east')
    area.exit(lt_repair_song_niche, lt_shared_tool_shelf, 'west')
    area.exit(lt_repair_song_niche, lt_sunleaf_drying_rail, 'east')
    area.exit(lt_sunleaf_drying_rail, lt_repair_song_niche, 'west')
    area.exit(lt_sunleaf_drying_rail, lt_central_isle_lookout, 'east')
    area.exit(lt_central_isle_lookout, lt_sunleaf_drying_rail, 'west')
    area.exit(lt_central_isle_lookout, lt_central_path, 'east')
    area.exit(lt_central_path, lt_central_isle_lookout, 'west')
    area.exit(qh_quiet_house_porch, qh_sunleaf_water_basin, 'east')
    area.exit(qh_sunleaf_water_basin, qh_quiet_house_porch, 'west')
    area.exit(qh_sunleaf_water_basin, qh_plain_bowl_shelf, 'east')
    area.exit(qh_plain_bowl_shelf, qh_sunleaf_water_basin, 'west')
    area.exit(qh_plain_bowl_shelf, qh_grief_mat_circle, 'east')
    area.exit(qh_grief_mat_circle, qh_plain_bowl_shelf, 'west')
    area.exit(qh_grief_mat_circle, qh_low_voice_hall, 'east')
    area.exit(qh_low_voice_hall, qh_grief_mat_circle, 'west')
    area.exit(qh_low_voice_hall, qh_name_cloth_alcove, 'east')
    area.exit(qh_name_cloth_alcove, qh_low_voice_hall, 'west')
    area.exit(qh_name_cloth_alcove, qh_ash_washed_threshold, 'east')
    area.exit(qh_ash_washed_threshold, qh_name_cloth_alcove, 'west')
    area.exit(qh_ash_washed_threshold, qh_caretakers_small_table, 'east')
    area.exit(qh_caretakers_small_table, qh_ash_washed_threshold, 'west')
    area.exit(qh_caretakers_small_table, qh_southern_shell_window, 'east')
    area.exit(qh_southern_shell_window, qh_caretakers_small_table, 'west')
    area.exit(qh_southern_shell_window, qh_visitor_pause_stone, 'east')
    area.exit(qh_visitor_pause_stone, qh_southern_shell_window, 'west')
    area.exit(qh_visitor_pause_stone, qh_tide_silence_bench, 'east')
    area.exit(qh_tide_silence_bench, qh_visitor_pause_stone, 'west')
    area.exit(qh_tide_silence_bench, qh_offering_basket_niche, 'east')
    area.exit(qh_offering_basket_niche, qh_tide_silence_bench, 'west')
    area.exit(qh_offering_basket_niche, qh_mended_paddle_rack, 'east')
    area.exit(qh_mended_paddle_rack, qh_offering_basket_niche, 'west')
    area.exit(qh_mended_paddle_rack, qh_ruins_warning_board, 'east')
    area.exit(qh_ruins_warning_board, qh_mended_paddle_rack, 'west')
    area.exit(qh_ruins_warning_board, qh_boat_hook_wall, 'east')
    area.exit(qh_boat_hook_wall, qh_ruins_warning_board, 'west')
    area.exit(qh_boat_hook_wall, qh_south_sand_stair, 'east')
    area.exit(qh_south_sand_stair, qh_boat_hook_wall, 'west')
    area.exit(qh_south_sand_stair, qh_breakwater_shrine, 'east')
    area.exit(qh_breakwater_shrine, qh_south_sand_stair, 'west')
    area.exit(qh_breakwater_shrine, qh_low_boat_landing, 'east')
    area.exit(qh_low_boat_landing, qh_breakwater_shrine, 'west')
    area.exit(qh_low_boat_landing, qh_quiet_oar_stand, 'east')
    area.exit(qh_quiet_oar_stand, qh_low_boat_landing, 'west')
    area.exit(qh_quiet_oar_stand, qh_ruins_boat, 'east')
    area.exit(qh_ruins_boat, qh_quiet_oar_stand, 'west')
    area.exit(ac_reef_gate, bm_beach_market_mouth, 'north')
    area.exit(bm_beach_market_mouth, ac_reef_gate, 'south')
    area.exit(bm_evening_ember_ring, kg_kiai_gate, 'north')
    area.exit(kg_kiai_gate, bm_evening_ember_ring, 'south')
    area.exit(kg_witness_road_bend, lt_lower_listening_step, 'north')
    area.exit(lt_lower_listening_step, kg_witness_road_bend, 'south')
    area.exit(lt_central_path, qh_quiet_house_porch, 'north')
    area.exit(qh_quiet_house_porch, lt_central_path, 'south')
    area.exit(ac_reef_gate, 'veluana_outer_reefs:rl_korahei_landing', 'east')
    area.exit(kg_kiai_gate, 'kiai_grounds:wr_witness_gate', 'north')
    area.exit(lt_central_path, 'veluana_central_isle:gc_korahei_track', 'east')
    area.exit(qh_ruins_boat, 'colonist_ruins:ld_quiet_landing', 'south')

    # NPCs
    _hearth_mother = area.npc(bm_first_bite_hearth, 'npc_hearth_mother_pelani', faction='kauroran', dialogue={'greeting_tiers': {"neutral": 'Hearth Mother Pelani studies you with open attention.'}, 'topics': {'help': 'Teaches first bites, shared bowls, and the difference between welcome and entitlement.', 'custom': 'Korahei expects guests to learn by helping, listening, and returning what they carry.'}, 'base_hints': ['help', 'custom']}, ambient={'idle_echoes': ['Hearth Mother Pelani adjusts a small detail, making the place easier for the next person.'], 'idle_interval': 90, 'idle_variance': 30})
    _runner_lani = area.npc(ac_courier_platform, 'npc_runner_lani', faction='kauroran', dialogue={'greeting_tiers': {"neutral": 'Runner Lani studies you with open attention.'}, 'topics': {'help': 'Routes messages and small responsibilities to the reefs.', 'custom': 'Korahei expects guests to learn by helping, listening, and returning what they carry.'}, 'base_hints': ['help', 'custom']}, ambient={'idle_echoes': ['Runner Lani adjusts a small detail, making the place easier for the next person.'], 'idle_interval': 90, 'idle_variance': 30})
    _name_keeper = area.npc(lt_listening_step, 'npc_name_keeper_haoa', faction='kauroran', trust_sensitive=True, dialogue={'greeting_tiers': {"neutral": 'Name-Keeper Haoa studies you with open attention.'}, 'topics': {'help': 'Helps guests learn names before asking favors.', 'custom': 'Korahei expects guests to learn by helping, listening, and returning what they carry.'}, 'base_hints': ['help', 'custom']}, ambient={'idle_echoes': ['Name-Keeper Haoa adjusts a small detail, making the place easier for the next person.'], 'idle_interval': 90, 'idle_variance': 30})
    _warden_guest = area.npc(kg_warden_courtesy_mat, 'npc_warden_guest_iren', faction='wardens', dialogue={'greeting_tiers': {"neutral": 'Warden Iren studies you with open attention.'}, 'topics': {'help': 'A guest ally careful not to mistake invitation for ownership.', 'custom': 'Korahei expects guests to learn by helping, listening, and returning what they carry.'}, 'base_hints': ['help', 'custom']}, ambient={'idle_echoes': ['Warden Iren adjusts a small detail, making the place easier for the next person.'], 'idle_interval': 90, 'idle_variance': 30})
    _quiet_mareva = area.npc(qh_quiet_house_porch, 'npc_quiet_house_mareva', faction='kauroran', dialogue={'greeting_tiers': {"neutral": 'Quiet House Mareva studies you with open attention.'}, 'topics': {'help': 'Keeps bowls, names, and the southern boat path.', 'custom': 'Korahei expects guests to learn by helping, listening, and returning what they carry.'}, 'base_hints': ['help', 'custom']}, ambient={'idle_echoes': ['Quiet House Mareva adjusts a small detail, making the place easier for the next person.'], 'idle_interval': 90, 'idle_variance': 30})
    _market_auntie = area.npc(bm_saltfruit_awning, 'npc_market_auntie_sola', faction='kauroran', dialogue={'greeting_tiers': {"neutral": 'Auntie Sola studies you with open attention.'}, 'topics': {'help': 'Sells food while making sure new guests eat and listen.', 'custom': 'Korahei expects guests to learn by helping, listening, and returning what they carry.'}, 'base_hints': ['help', 'custom']}, ambient={'idle_echoes': ['Auntie Sola adjusts a small detail, making the place easier for the next person.'], 'idle_interval': 90, 'idle_variance': 30})
    _first_bite_child = area.npc(bm_shared_bowl_bench, 'npc_first_bite_child_makoa', faction='kauroran', dialogue={'greeting_tiers': {"neutral": 'Makoa of the First Bite studies you with open attention.'}, 'topics': {'help': 'A child taking the custom very seriously.', 'custom': 'Korahei expects guests to learn by helping, listening, and returning what they carry.'}, 'base_hints': ['help', 'custom']}, ambient={'idle_echoes': ['Makoa of the First Bite adjusts a small detail, making the place easier for the next person.'], 'idle_interval': 90, 'idle_variance': 30})
    area.vendor(_market_auntie, accepts=['consumable'], item_ids=['trail_rations', 'spiced_fish', 'hearty_stew', 'minor_stamina_potion', 'bandage'])
    _tool_mender = area.npc(bm_tool_menders_shade, 'npc_tool_mender_koa', faction='kauroran', dialogue={'greeting_tiers': {"neutral": 'The vendor nods toward practical island supplies.'}, 'topics': {'trade': 'Tools, food, and modest gear keep a guest useful without making them reckless.'}})
    area.vendor(_tool_mender, accepts=['tool', 'consumable'], item_ids=['fishing_rod', 'bait', 'sickle', 'hatchet', 'skinning_knife', 'pickaxe', 'bandage'])
    _reef_outfitter = area.npc(ac_outer_mat_circle, 'npc_reef_outfitter_pao', faction='kauroran', dialogue={'greeting_tiers': {"neutral": 'The vendor nods toward practical island supplies.'}, 'topics': {'trade': 'Tools, food, and modest gear keep a guest useful without making them reckless.'}})
    area.vendor(_reef_outfitter, accepts=['equipment', 'consumable', 'tool'], item_ids=['iron_dagger', 'iron_staff', 'leather_vest', 'leather_boots', 'travelers_cloak', 'fishing_rod', 'bait', 'minor_healing_potion'])

    # Quest and delivery item templates
    area.item('kor_first_bite_basket', key='first-bite basket', item_type='item', weight=0.4, rarity='normal', desc='A woven basket holding the best first pieces from the hearth.', value=0, is_quest_item=True)
    area.item('kor_reef_tally', key='reef tally bundle', item_type='item', weight=0.1, rarity='normal', desc='A palm-leaf tally of who still needs fish, rope, and medicine on the outer reef.', value=0, is_quest_item=True)
    area.item('kor_warden_courtesy_note', key='warden courtesy note', item_type='item', weight=0.1, rarity='normal', desc='A careful note asking the kiai caretakers to receive an allied guest properly.', value=0, is_quest_item=True)
    area.item('kor_quiet_bowl', key='quiet bowl', item_type='item', weight=0.5, rarity='normal', desc='A plain bowl wrapped for the ruin listeners, meant for names rather than display.', value=0, is_quest_item=True)
    area.quest(
        'kor_q_first_bite',
        name='The First Bite',
        description="Pelani asks you to learn Korahei's first-bite custom by serving before eating, turning hospitality into a playable social lesson.",
        quest_type='social',
        quest_giver='npc_hearth_mother_pelani',
        objectives=[{'type': 'talk_to', 'target': 'npc_first_bite_child_makoa', 'count': 1}, {'type': 'investigate', 'target': 'bm_first_bite_hearth', 'count': 1}, {'type': 'deliver', 'target': 'npc_market_auntie_sola', 'count': 1, 'item_tag': 'kor_first_bite_basket'}],
        rewards=[{'action_type': 'give_scales', 'amount': 18}, {'action_type': 'modify_standing', 'faction_id': 'kauroran', 'delta': 2500}],
        next_quest_id='kor_q_guest_names',
        prerequisite_quests=[],
        can_share=True,
        consequence_small='Pelani sets aside your own portion only after the market line is fed, and children repeat your name as someone who learned the first bite properly.',
    )
    area.quest(
        'kor_q_guest_names',
        name='Guest Names',
        description='Haoa teaches that names are not flavor text in Korahei; learning them is how a guest becomes safe to trust with errands.',
        quest_type='social',
        quest_giver='npc_name_keeper_haoa',
        objectives=[{'type': 'talk_to', 'target': 'npc_warden_guest_iren', 'count': 1}, {'type': 'talk_to', 'target': 'npc_market_auntie_sola', 'count': 1}, {'type': 'investigate', 'target': 'lt_listening_step', 'count': 1}],
        rewards=[{'action_type': 'give_scales', 'amount': 20}, {'action_type': 'give_skill_xp', 'skill_id': 'scholarship', 'count': 8}, {'action_type': 'modify_dimension', 'dimension': 'network', 'delta': 8, 'effect_id': 'kor_q_guest_names:network', 'message': '|cThe names and obligations of Korahei begin to form a living web around you.|n'}, {'action_type': 'modify_trust', 'faction_id': 'kauroran', 'delta': 30, 'effect_id': 'kor_q_guest_names:kauroran_trust', 'message': '|cHaoa now trusts you with more than a visitor\'s introduction.|n'}],
        next_quest_id=None,
        prerequisite_quests=['kor_q_first_bite'],
        can_share=True,
        consequence_small='Haoa adds your pronunciation marks to the guest bench so future introductions begin with a little less friction.',
    )
    area.quest(
        'kor_q_reef_runner',
        name="Reef Runner's Tally",
        description='Lani sends you with a tally that matters to real reef work, guiding you through the reef gate toward Tavake instead of creating a dead-end delivery.',
        quest_type='delivery',
        quest_giver='npc_runner_lani',
        objectives=[{'type': 'investigate', 'target': 'ac_reef_gate', 'count': 1}, {'type': 'deliver', 'target': 'npc_reef_keeper_tavake', 'count': 1, 'item_tag': 'kor_reef_tally'}],
        rewards=[{'action_type': 'give_scales', 'amount': 24}, {'action_type': 'give_skill_xp', 'skill_id': 'fishing', 'count': 8}],
        next_quest_id='reef_q_tide_marks',
        prerequisite_quests=[],
        can_share=True,
        consequence_small='Lani marks your tally route on the reef board, giving new runners a safer first line toward Tavake.',
    )
    area.quest(
        'kor_q_warden_guest',
        name='A Guest, Not a Claim',
        description='Iren asks you to carry a courtesy note to the kiai caretakers, framing Warden presence as relationship work rather than authority.',
        quest_type='delivery',
        quest_giver='npc_warden_guest_iren',
        objectives=[{'type': 'investigate', 'target': 'kg_kiai_gate', 'count': 1}, {'type': 'deliver', 'target': 'npc_kiai_caretaker_maluhia', 'count': 1, 'item_tag': 'kor_warden_courtesy_note'}],
        rewards=[{'action_type': 'give_scales', 'amount': 24}, {'action_type': 'modify_standing', 'faction_id': 'wardens', 'delta': 2500}],
        next_quest_id='kiai_q_witness_silence',
        prerequisite_quests=['kor_q_guest_names'],
        can_share=True,
        consequence_small='Iren records that your courtesy carried farther than Warden authority, making later kiai conversations easier to begin.',
    )
    area.quest(
        'kor_q_quiet_bowl',
        name='The Quiet Bowl',
        description='Mareva asks you to bring a plain bowl to the ruin listeners, making the southern route an act of respect before investigation.',
        quest_type='delivery',
        quest_giver='npc_quiet_house_mareva',
        objectives=[{'type': 'investigate', 'target': 'qh_ruins_boat', 'count': 1}, {'type': 'deliver', 'target': 'npc_ruin_listener_ao', 'count': 1, 'item_tag': 'kor_quiet_bowl'}],
        rewards=[{'action_type': 'give_scales', 'amount': 24}, {'action_type': 'give_skill_xp', 'skill_id': 'scholarship', 'count': 8}],
        next_quest_id='ruins_q_names_in_salt',
        prerequisite_quests=['kor_q_guest_names'],
        can_share=True,
        consequence_small='Mareva leaves a plain bowl ready for your next ruin crossing, trusting you to approach grief before curiosity.',
    )

    # Spawns
    area.spawn(lt_soft_hammer_ring, 'weighted_sparring_frame', count_min=1, count_max=2, respawn_minutes=10)
    area.spawn(lt_shared_tool_shelf, 'weighted_sparring_frame', count_min=1, count_max=2, respawn_minutes=10)
    area.spawn(lt_repair_song_niche, 'padded_practice_dummy', count_min=1, count_max=2, respawn_minutes=10)
    area.spawn(lt_paddle_pattern_rack, 'padded_practice_dummy', count_min=1, count_max=2, respawn_minutes=10)

    # Gathering pools
    area.gathering_pool('fish', ['ac_harbor_listening_rail', 'qh_low_boat_landing'], ['reef_silverjack'], max_active=3, respawn_minutes=12)
    area.gathering_pool('forage', ['bm_saltfruit_awning', 'bm_hearthroot_basket', 'qh_breakwater_shrine'], ['saltfruit', 'hearthroot'], max_active=3, respawn_minutes=12)
    area.gathering_pool('herb', ['lt_sunleaf_drying_rail', 'qh_sunleaf_water_basin'], ['sunleaf'], max_active=3, respawn_minutes=12)
    area.gathering_pool('ore', ['bm_reefstone_weighing_mat', 'ac_salt_washed_steps'], ['reefstone'], max_active=3, respawn_minutes=12)
    area.gathering_pool('hide', ['bm_net_mender_circle', 'ac_reef_warning_post'], ['reefcrawler_shell'], max_active=3, respawn_minutes=12)
    area.gathering_pool('wood', ['lt_saltpalm_work_circle', 'ac_palm_welcome_shade'], ['saltpalm_wood'], max_active=3, respawn_minutes=12)

    area.flight_point(ac_courier_platform, 'korahei_courier', name='Korahei Courier Platform')
    area.flight_route(
        'korahei_courier',
        'varath_prime_courier',
        220,
        leg_duration=120,
        echoes=[
            {'delay': 30, 'message': 'Wind hardens over open water. The courier beast settles into a long, practiced rhythm while mainland and islands trade places on the horizon.'},
            {'delay': 80, 'message': 'Far below, reef rings catch the sun around dark water, and working boats leave brief white seams between them.'},
        ],
    )

    return area.build()
