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
        faction_presence=['kauroran', 'warden', 'consortium'],
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
    ac_first_bite_mat = area.room('ac_first_bite_mat', name='First Bite Mat', desc='Korahei opens in circles rather than gates, with palms, woven shade, and benches placed so strangers meet faces before rules. This part of the Arrival Circle centers on first bite mat, where shell chimes move softly in the sea wind. Every path bends back toward welcome, but the welcome asks guests to notice what they take and what they owe.', room_type='clearing')
    ac_guest_water_stone = area.room('ac_guest_water_stone', name='Guest Water Stone', desc='Korahei opens in circles rather than gates, with palms, woven shade, and benches placed so strangers meet faces before rules. This part of the Arrival Circle centers on guest water stone, where couriers compare tide routes beside painted stones. Every path bends back toward welcome, but the welcome asks guests to notice what they take and what they owe.', room_type='clearing')
    ac_palm_welcome_shade = area.room('ac_palm_welcome_shade', name='Palm Welcome Shade', desc='Korahei opens in circles rather than gates, with palms, woven shade, and benches placed so strangers meet faces before rules. This part of the Arrival Circle centers on palm welcome shade, where children practice the first-bite custom with solemn delight. Every path bends back toward welcome, but the welcome asks guests to notice what they take and what they owe.', room_type='clearing')
    ac_shell_chime_walk = area.room('ac_shell_chime_walk', name='Shell Chime Walk', desc='Korahei opens in circles rather than gates, with palms, woven shade, and benches placed so strangers meet faces before rules. This part of the Arrival Circle centers on shell chime walk, where elders watch arrivals without making a spectacle of caution. Every path bends back toward welcome, but the welcome asks guests to notice what they take and what they owe.', room_type='clearing')
    ac_round_bench_of_names = area.room('ac_round_bench_of_names', name='Round Bench of Names', desc='Korahei opens in circles rather than gates, with palms, woven shade, and benches placed so strangers meet faces before rules. This part of the Arrival Circle centers on round bench of names, where woven mats mark where first greetings are offered. Every path bends back toward welcome, but the welcome asks guests to notice what they take and what they owe.', room_type='clearing')
    ac_traveler_sandal_rack = area.room('ac_traveler_sandal_rack', name='Traveler Sandal Rack', desc='Korahei opens in circles rather than gates, with palms, woven shade, and benches placed so strangers meet faces before rules. This part of the Arrival Circle centers on traveler sandal rack, where shell chimes move softly in the sea wind. Every path bends back toward welcome, but the welcome asks guests to notice what they take and what they owe.', room_type='clearing')
    ac_woven_shade_rise = area.room('ac_woven_shade_rise', name='Woven Shade Rise', desc='Korahei opens in circles rather than gates, with palms, woven shade, and benches placed so strangers meet faces before rules. This part of the Arrival Circle centers on woven shade rise, where couriers compare tide routes beside painted stones. Every path bends back toward welcome, but the welcome asks guests to notice what they take and what they owe.', room_type='clearing')
    ac_low_tide_notice = area.room('ac_low_tide_notice', name='Low Tide Notice', desc='Korahei opens in circles rather than gates, with palms, woven shade, and benches placed so strangers meet faces before rules. This part of the Arrival Circle centers on low tide notice, where children practice the first-bite custom with solemn delight. Every path bends back toward welcome, but the welcome asks guests to notice what they take and what they owe.', room_type='clearing')
    ac_salt_washed_steps = area.room('ac_salt_washed_steps', name='Salt-Washed Steps', desc='Korahei opens in circles rather than gates, with palms, woven shade, and benches placed so strangers meet faces before rules. This part of the Arrival Circle centers on salt-washed steps, where elders watch arrivals without making a spectacle of caution. Every path bends back toward welcome, but the welcome asks guests to notice what they take and what they owe.', room_type='clearing')
    ac_runners_rest_mat = area.room('ac_runners_rest_mat', name="Runner's Rest Mat", desc="Korahei opens in circles rather than gates, with palms, woven shade, and benches placed so strangers meet faces before rules. This part of the Arrival Circle centers on runner's rest mat, where woven mats mark where first greetings are offered. Every path bends back toward welcome, but the welcome asks guests to notice what they take and what they owe.", room_type='clearing')
    ac_courier_ledger_post = area.room('ac_courier_ledger_post', name='Courier Ledger Post', desc='Korahei opens in circles rather than gates, with palms, woven shade, and benches placed so strangers meet faces before rules. This part of the Arrival Circle centers on courier ledger post, where shell chimes move softly in the sea wind. Every path bends back toward welcome, but the welcome asks guests to notice what they take and what they owe.', room_type='clearing')
    ac_courier_platform = area.room('ac_courier_platform', name='Courier Platform', desc='The courier platform rises above the arrival circle on saltpalm braces polished by bare hands. Handlers check tack, weather, and guest names here before any beast takes wing, making travel feel ceremonial without becoming spectacle.', room_type='clearing')
    ac_harbor_listening_rail = area.room('ac_harbor_listening_rail', name='Harbor Listening Rail', desc='Korahei opens in circles rather than gates, with palms, woven shade, and benches placed so strangers meet faces before rules. This part of the Arrival Circle centers on harbor listening rail, where children practice the first-bite custom with solemn delight. Every path bends back toward welcome, but the welcome asks guests to notice what they take and what they owe.', room_type='clearing')
    ac_guest_oath_bowl = area.room('ac_guest_oath_bowl', name='Guest Oath Bowl', desc='Korahei opens in circles rather than gates, with palms, woven shade, and benches placed so strangers meet faces before rules. This part of the Arrival Circle centers on guest oath bowl, where elders watch arrivals without making a spectacle of caution. Every path bends back toward welcome, but the welcome asks guests to notice what they take and what they owe.', room_type='clearing')
    ac_market_bend = area.room('ac_market_bend', name='Market Bend', desc='Korahei opens in circles rather than gates, with palms, woven shade, and benches placed so strangers meet faces before rules. This part of the Arrival Circle centers on market bend, where woven mats mark where first greetings are offered. Every path bends back toward welcome, but the welcome asks guests to notice what they take and what they owe.', room_type='clearing')
    ac_outer_mat_circle = area.room('ac_outer_mat_circle', name='Outer Mat Circle', desc='Korahei opens in circles rather than gates, with palms, woven shade, and benches placed so strangers meet faces before rules. This part of the Arrival Circle centers on outer mat circle, where shell chimes move softly in the sea wind. Every path bends back toward welcome, but the welcome asks guests to notice what they take and what they owe.', room_type='clearing')
    ac_reef_warning_post = area.room('ac_reef_warning_post', name='Reef Warning Post', desc='Korahei opens in circles rather than gates, with palms, woven shade, and benches placed so strangers meet faces before rules. This part of the Arrival Circle centers on reef warning post, where couriers compare tide routes beside painted stones. Every path bends back toward welcome, but the welcome asks guests to notice what they take and what they owe.', room_type='clearing')
    ac_gate_of_shared_bread = area.room('ac_gate_of_shared_bread', name='Gate of Shared Bread', desc='Korahei opens in circles rather than gates, with palms, woven shade, and benches placed so strangers meet faces before rules. This part of the Arrival Circle centers on gate of shared bread, where children practice the first-bite custom with solemn delight. Every path bends back toward welcome, but the welcome asks guests to notice what they take and what they owe.', room_type='clearing')
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
    kg_witness_cord_post = area.room('kg_witness_cord_post', name='Witness Cord Post', desc='The northern city path grows quieter as council circles give way to the road used by caretakers, witnesses, and candidates. This part of the Kiai Gate and Tide Council Walk centers on witness cord post, where council mats are set in rings with no single head seat. Nothing here sells the kiai as a prize; the city treats preparation as responsibility before wonder.', room_type='path')
    kg_council_shell_ring = area.room('kg_council_shell_ring', name='Council Shell Ring', desc='The northern city path grows quieter as council circles give way to the road used by caretakers, witnesses, and candidates. This part of the Kiai Gate and Tide Council Walk centers on council shell ring, where handlers speak in low tones about weather and safety. Nothing here sells the kiai as a prize; the city treats preparation as responsibility before wonder.', room_type='path')
    kg_tide_law_bench = area.room('kg_tide_law_bench', name='Tide Law Bench', desc='The northern city path grows quieter as council circles give way to the road used by caretakers, witnesses, and candidates. This part of the Kiai Gate and Tide Council Walk centers on tide law bench, where braided cords mark who is a guest, a witness, or a caretaker. Nothing here sells the kiai as a prize; the city treats preparation as responsibility before wonder.', room_type='path')
    kg_caretaker_ledger = area.room('kg_caretaker_ledger', name='Caretaker Ledger', desc='The northern city path grows quieter as council circles give way to the road used by caretakers, witnesses, and candidates. This part of the Kiai Gate and Tide Council Walk centers on caretaker ledger, where old drums are covered until ceremony calls for them. Nothing here sells the kiai as a prize; the city treats preparation as responsibility before wonder.', room_type='path')
    kg_unlit_drum_porch = area.room('kg_unlit_drum_porch', name='Unlit Drum Porch', desc='The northern city path grows quieter as council circles give way to the road used by caretakers, witnesses, and candidates. This part of the Kiai Gate and Tide Council Walk centers on unlit drum porch, where polished stones carry marks from many patient feet. Nothing here sells the kiai as a prize; the city treats preparation as responsibility before wonder.', room_type='path')
    kg_young_candidate_shade = area.room('kg_young_candidate_shade', name='Young Candidate Shade', desc='The northern city path grows quieter as council circles give way to the road used by caretakers, witnesses, and candidates. This part of the Kiai Gate and Tide Council Walk centers on young candidate shade, where council mats are set in rings with no single head seat. Nothing here sells the kiai as a prize; the city treats preparation as responsibility before wonder.', room_type='path')
    kg_guest_boundary_stone = area.room('kg_guest_boundary_stone', name='Guest Boundary Stone', desc='The northern city path grows quieter as council circles give way to the road used by caretakers, witnesses, and candidates. This part of the Kiai Gate and Tide Council Walk centers on guest boundary stone, where handlers speak in low tones about weather and safety. Nothing here sells the kiai as a prize; the city treats preparation as responsibility before wonder.', room_type='path')
    kg_braid_makers_nook = area.room('kg_braid_makers_nook', name="Braid-Maker's Nook", desc="The northern city path grows quieter as council circles give way to the road used by caretakers, witnesses, and candidates. This part of the Kiai Gate and Tide Council Walk centers on braid-maker's nook, where braided cords mark who is a guest, a witness, or a caretaker. Nothing here sells the kiai as a prize; the city treats preparation as responsibility before wonder.", room_type='path')
    kg_north_wind_steps = area.room('kg_north_wind_steps', name='North Wind Steps', desc='The northern city path grows quieter as council circles give way to the road used by caretakers, witnesses, and candidates. This part of the Kiai Gate and Tide Council Walk centers on north wind steps, where old drums are covered until ceremony calls for them. Nothing here sells the kiai as a prize; the city treats preparation as responsibility before wonder.', room_type='path')
    kg_quiet_hoof_sand = area.room('kg_quiet_hoof_sand', name='Quiet Hoof Sand', desc='The northern city path grows quieter as council circles give way to the road used by caretakers, witnesses, and candidates. This part of the Kiai Gate and Tide Council Walk centers on quiet hoof sand, where polished stones carry marks from many patient feet. Nothing here sells the kiai as a prize; the city treats preparation as responsibility before wonder.', room_type='path')
    kg_ceremony_water_jar = area.room('kg_ceremony_water_jar', name='Ceremony Water Jar', desc='The northern city path grows quieter as council circles give way to the road used by caretakers, witnesses, and candidates. This part of the Kiai Gate and Tide Council Walk centers on ceremony water jar, where council mats are set in rings with no single head seat. Nothing here sells the kiai as a prize; the city treats preparation as responsibility before wonder.', room_type='path')
    kg_warden_courtesy_mat = area.room('kg_warden_courtesy_mat', name='Warden Courtesy Mat', desc='The northern city path grows quieter as council circles give way to the road used by caretakers, witnesses, and candidates. This part of the Kiai Gate and Tide Council Walk centers on warden courtesy mat, where handlers speak in low tones about weather and safety. Nothing here sells the kiai as a prize; the city treats preparation as responsibility before wonder.', room_type='path')
    kg_old_promise_stone = area.room('kg_old_promise_stone', name='Old Promise Stone', desc='The northern city path grows quieter as council circles give way to the road used by caretakers, witnesses, and candidates. This part of the Kiai Gate and Tide Council Walk centers on old promise stone, where braided cords mark who is a guest, a witness, or a caretaker. Nothing here sells the kiai as a prize; the city treats preparation as responsibility before wonder.', room_type='path')
    kg_listening_guardrail = area.room('kg_listening_guardrail', name='Listening Guardrail', desc='The northern city path grows quieter as council circles give way to the road used by caretakers, witnesses, and candidates. This part of the Kiai Gate and Tide Council Walk centers on listening guardrail, where old drums are covered until ceremony calls for them. Nothing here sells the kiai as a prize; the city treats preparation as responsibility before wonder.', room_type='path')
    kg_pale_garland_wall = area.room('kg_pale_garland_wall', name='Pale Garland Wall', desc='The northern city path grows quieter as council circles give way to the road used by caretakers, witnesses, and candidates. This part of the Kiai Gate and Tide Council Walk centers on pale garland wall, where polished stones carry marks from many patient feet. Nothing here sells the kiai as a prize; the city treats preparation as responsibility before wonder.', room_type='path')
    kg_gatekeepers_rest = area.room('kg_gatekeepers_rest', name="Gatekeeper's Rest", desc="The northern city path grows quieter as council circles give way to the road used by caretakers, witnesses, and candidates. This part of the Kiai Gate and Tide Council Walk centers on gatekeeper's rest, where council mats are set in rings with no single head seat. Nothing here sells the kiai as a prize; the city treats preparation as responsibility before wonder.", room_type='path')
    kg_high_grass_turn = area.room('kg_high_grass_turn', name='High Grass Turn', desc='The northern city path grows quieter as council circles give way to the road used by caretakers, witnesses, and candidates. This part of the Kiai Gate and Tide Council Walk centers on high grass turn, where handlers speak in low tones about weather and safety. Nothing here sells the kiai as a prize; the city treats preparation as responsibility before wonder.', room_type='path')
    kg_distant_ring_view = area.room('kg_distant_ring_view', name='Distant Ring View', desc='The northern city path grows quieter as council circles give way to the road used by caretakers, witnesses, and candidates. This part of the Kiai Gate and Tide Council Walk centers on distant ring view, where braided cords mark who is a guest, a witness, or a caretaker. Nothing here sells the kiai as a prize; the city treats preparation as responsibility before wonder.', room_type='path')
    kg_witness_road_bend = area.room('kg_witness_road_bend', name='Witness Road Bend', desc='The northern city path grows quieter as council circles give way to the road used by caretakers, witnesses, and candidates. This part of the Kiai Gate and Tide Council Walk centers on witness road bend, where old drums are covered until ceremony calls for them. Nothing here sells the kiai as a prize; the city treats preparation as responsibility before wonder.', room_type='path')
    lt_lower_listening_step = area.room('lt_lower_listening_step', name='Lower Listening Step', desc='Terraces climb toward work circles where carving, mending, and quiet listening are treated as civic skills. This part of the Listening Terraces and Craft Rings centers on lower listening step, where students leave room for elders to correct their hands. The terraces make the city feel learned without becoming a schoolhouse; knowledge is shared by sitting close and doing the work.', room_type='building')
    lt_carvers_quiet_rail = area.room('lt_carvers_quiet_rail', name="Carver's Quiet Rail", desc="Terraces climb toward work circles where carving, mending, and quiet listening are treated as civic skills. This part of the Listening Terraces and Craft Rings centers on carver's quiet rail, where craft scraps are sorted instead of wasted. The terraces make the city feel learned without becoming a schoolhouse; knowledge is shared by sitting close and doing the work.", room_type='building')
    lt_saltpalm_work_circle = area.room('lt_saltpalm_work_circle', name='Saltpalm Work Circle', desc='Terraces climb toward work circles where carving, mending, and quiet listening are treated as civic skills. This part of the Listening Terraces and Craft Rings centers on saltpalm work circle, where low walls carry tide scratches and family marks. The terraces make the city feel learned without becoming a schoolhouse; knowledge is shared by sitting close and doing the work.', room_type='building')
    lt_shell_inlay_bench = area.room('lt_shell_inlay_bench', name='Shell Inlay Bench', desc='Terraces climb toward work circles where carving, mending, and quiet listening are treated as civic skills. This part of the Listening Terraces and Craft Rings centers on shell inlay bench, where listeners repeat names until pronunciation becomes care. The terraces make the city feel learned without becoming a schoolhouse; knowledge is shared by sitting close and doing the work.', room_type='building')
    lt_cordage_lesson_mat = area.room('lt_cordage_lesson_mat', name='Cordage Lesson Mat', desc='Terraces climb toward work circles where carving, mending, and quiet listening are treated as civic skills. This part of the Listening Terraces and Craft Rings centers on cordage lesson mat, where shade sails turn the sun into warm moving patterns. The terraces make the city feel learned without becoming a schoolhouse; knowledge is shared by sitting close and doing the work.', room_type='building')
    lt_name_practice_terrace = area.room('lt_name_practice_terrace', name='Name-Practice Terrace', desc='Terraces climb toward work circles where carving, mending, and quiet listening are treated as civic skills. This part of the Listening Terraces and Craft Rings centers on name-practice terrace, where students leave room for elders to correct their hands. The terraces make the city feel learned without becoming a schoolhouse; knowledge is shared by sitting close and doing the work.', room_type='building')
    lt_listening_step = area.room('lt_listening_step', name='Listening Step', desc='Terraces climb toward work circles where carving, mending, and quiet listening are treated as civic skills. This part of the Listening Terraces and Craft Rings centers on listening step, where craft scraps are sorted instead of wasted. The terraces make the city feel learned without becoming a schoolhouse; knowledge is shared by sitting close and doing the work.', room_type='building')
    lt_tide_scratch_wall = area.room('lt_tide_scratch_wall', name='Tide-Scratch Wall', desc='Terraces climb toward work circles where carving, mending, and quiet listening are treated as civic skills. This part of the Listening Terraces and Craft Rings centers on tide-scratch wall, where low walls carry tide scratches and family marks. The terraces make the city feel learned without becoming a schoolhouse; knowledge is shared by sitting close and doing the work.', room_type='building')
    lt_open_palm_archive = area.room('lt_open_palm_archive', name='Open Palm Archive', desc='Terraces climb toward work circles where carving, mending, and quiet listening are treated as civic skills. This part of the Listening Terraces and Craft Rings centers on open palm archive, where listeners repeat names until pronunciation becomes care. The terraces make the city feel learned without becoming a schoolhouse; knowledge is shared by sitting close and doing the work.', room_type='building')
    lt_scholars_woven_seat = area.room('lt_scholars_woven_seat', name="Scholar's Woven Seat", desc="Terraces climb toward work circles where carving, mending, and quiet listening are treated as civic skills. This part of the Listening Terraces and Craft Rings centers on scholar's woven seat, where shade sails turn the sun into warm moving patterns. The terraces make the city feel learned without becoming a schoolhouse; knowledge is shared by sitting close and doing the work.", room_type='building')
    lt_round_loom_platform = area.room('lt_round_loom_platform', name='Round Loom Platform', desc='Terraces climb toward work circles where carving, mending, and quiet listening are treated as civic skills. This part of the Listening Terraces and Craft Rings centers on round loom platform, where students leave room for elders to correct their hands. The terraces make the city feel learned without becoming a schoolhouse; knowledge is shared by sitting close and doing the work.', room_type='building')
    lt_paddle_pattern_rack = area.room('lt_paddle_pattern_rack', name='Paddle Pattern Rack', desc='Practice paddles hang by size and weight, each one marked with cuts that teach grip before force. Students work the rack in measured turns, learning that a clean strike begins with a clean approach.', room_type='building')
    lt_guest_story_mat = area.room('lt_guest_story_mat', name='Guest Story Mat', desc='Terraces climb toward work circles where carving, mending, and quiet listening are treated as civic skills. This part of the Listening Terraces and Craft Rings centers on guest story mat, where low walls carry tide scratches and family marks. The terraces make the city feel learned without becoming a schoolhouse; knowledge is shared by sitting close and doing the work.', room_type='building')
    lt_high_terrace_well = area.room('lt_high_terrace_well', name='High Terrace Well', desc='Terraces climb toward work circles where carving, mending, and quiet listening are treated as civic skills. This part of the Listening Terraces and Craft Rings centers on high terrace well, where listeners repeat names until pronunciation becomes care. The terraces make the city feel learned without becoming a schoolhouse; knowledge is shared by sitting close and doing the work.', room_type='building')
    lt_soft_hammer_ring = area.room('lt_soft_hammer_ring', name='Soft Hammer Ring', desc='Soft hammers circle a sanded practice ring where counterweighted frames swing back just hard enough to teach caution. Elders watch for control, not victory, and the benches make room for advice after every exchange.', room_type='building')
    lt_shared_tool_shelf = area.room('lt_shared_tool_shelf', name='Shared Tool Shelf', desc='The shared shelf carries soft hammers, chalked hand wraps, and little tags naming who repaired what. Sparring frames stand nearby so practice feels tied to stewardship instead of a private contest.', room_type='building')
    lt_repair_song_niche = area.room('lt_repair_song_niche', name='Repair Song Niche', desc='A small niche holds padded dummies, mended frames, and the low repair songs used to keep rhythm steady. Nothing here rewards bravado; the lesson is to strike, reset, and leave the tools ready for the next learner.', room_type='building')
    lt_sunleaf_drying_rail = area.room('lt_sunleaf_drying_rail', name='Sunleaf Drying Rail', desc='Terraces climb toward work circles where carving, mending, and quiet listening are treated as civic skills. This part of the Listening Terraces and Craft Rings centers on sunleaf drying rail, where low walls carry tide scratches and family marks. The terraces make the city feel learned without becoming a schoolhouse; knowledge is shared by sitting close and doing the work.', room_type='building')
    lt_central_isle_lookout = area.room('lt_central_isle_lookout', name='Central Isle Lookout', desc='Terraces climb toward work circles where carving, mending, and quiet listening are treated as civic skills. This part of the Listening Terraces and Craft Rings centers on central isle lookout, where listeners repeat names until pronunciation becomes care. The terraces make the city feel learned without becoming a schoolhouse; knowledge is shared by sitting close and doing the work.', room_type='building')
    lt_central_path = area.room('lt_central_path', name='Central Path', desc='The eastern terrace path points toward the central isle through carved paddles and shell-cairn route marks. Listeners leave chalk notes here for travelers: walk the loop twice, trust the second silence, return with what you noticed.', room_type='building')
    qh_quiet_house_porch = area.room('qh_quiet_house_porch', name='Quiet House Porch', desc='The south of Korahei lowers its voice around the Quiet House, where grief, remembrance, and hospitality share the same bowls. This part of the Quiet House and Southern Boat Path centers on quiet house porch, where plain bowls are set out for visitors who do not know what to say. The path toward the ruins is not hidden, but the city expects players to approach it with humility instead of treasure fever.', room_type='building')
    qh_sunleaf_water_basin = area.room('qh_sunleaf_water_basin', name='Sunleaf Water Basin', desc='The south of Korahei lowers its voice around the Quiet House, where grief, remembrance, and hospitality share the same bowls. This part of the Quiet House and Southern Boat Path centers on sunleaf water basin, where names are spoken softly before any story is told. The path toward the ruins is not hidden, but the city expects players to approach it with humility instead of treasure fever.', room_type='building')
    qh_plain_bowl_shelf = area.room('qh_plain_bowl_shelf', name='Plain Bowl Shelf', desc='The south of Korahei lowers its voice around the Quiet House, where grief, remembrance, and hospitality share the same bowls. This part of the Quiet House and Southern Boat Path centers on plain bowl shelf, where stone basins hold clean water and floating sunleaf. The path toward the ruins is not hidden, but the city expects players to approach it with humility instead of treasure fever.', room_type='building')
    qh_grief_mat_circle = area.room('qh_grief_mat_circle', name='Grief Mat Circle', desc='The south of Korahei lowers its voice around the Quiet House, where grief, remembrance, and hospitality share the same bowls. This part of the Quiet House and Southern Boat Path centers on grief mat circle, where boat hooks hang beside warnings against careless salvage. The path toward the ruins is not hidden, but the city expects players to approach it with humility instead of treasure fever.', room_type='building')
    qh_low_voice_hall = area.room('qh_low_voice_hall', name='Low Voice Hall', desc='The south of Korahei lowers its voice around the Quiet House, where grief, remembrance, and hospitality share the same bowls. This part of the Quiet House and Southern Boat Path centers on low voice hall, where the surf below carries a hush different from the market. The path toward the ruins is not hidden, but the city expects players to approach it with humility instead of treasure fever.', room_type='building')
    qh_name_cloth_alcove = area.room('qh_name_cloth_alcove', name='Name Cloth Alcove', desc='The south of Korahei lowers its voice around the Quiet House, where grief, remembrance, and hospitality share the same bowls. This part of the Quiet House and Southern Boat Path centers on name cloth alcove, where plain bowls are set out for visitors who do not know what to say. The path toward the ruins is not hidden, but the city expects players to approach it with humility instead of treasure fever.', room_type='building')
    qh_ash_washed_threshold = area.room('qh_ash_washed_threshold', name='Ash-Washed Threshold', desc='The south of Korahei lowers its voice around the Quiet House, where grief, remembrance, and hospitality share the same bowls. This part of the Quiet House and Southern Boat Path centers on ash-washed threshold, where names are spoken softly before any story is told. The path toward the ruins is not hidden, but the city expects players to approach it with humility instead of treasure fever.', room_type='building')
    qh_caretakers_small_table = area.room('qh_caretakers_small_table', name="Caretaker's Small Table", desc="The south of Korahei lowers its voice around the Quiet House, where grief, remembrance, and hospitality share the same bowls. This part of the Quiet House and Southern Boat Path centers on caretaker's small table, where stone basins hold clean water and floating sunleaf. The path toward the ruins is not hidden, but the city expects players to approach it with humility instead of treasure fever.", room_type='building')
    qh_southern_shell_window = area.room('qh_southern_shell_window', name='Southern Shell Window', desc='The south of Korahei lowers its voice around the Quiet House, where grief, remembrance, and hospitality share the same bowls. This part of the Quiet House and Southern Boat Path centers on southern shell window, where boat hooks hang beside warnings against careless salvage. The path toward the ruins is not hidden, but the city expects players to approach it with humility instead of treasure fever.', room_type='building')
    qh_visitor_pause_stone = area.room('qh_visitor_pause_stone', name='Visitor Pause Stone', desc='The south of Korahei lowers its voice around the Quiet House, where grief, remembrance, and hospitality share the same bowls. This part of the Quiet House and Southern Boat Path centers on visitor pause stone, where the surf below carries a hush different from the market. The path toward the ruins is not hidden, but the city expects players to approach it with humility instead of treasure fever.', room_type='building')
    qh_tide_silence_bench = area.room('qh_tide_silence_bench', name='Tide-Silence Bench', desc='The south of Korahei lowers its voice around the Quiet House, where grief, remembrance, and hospitality share the same bowls. This part of the Quiet House and Southern Boat Path centers on tide-silence bench, where plain bowls are set out for visitors who do not know what to say. The path toward the ruins is not hidden, but the city expects players to approach it with humility instead of treasure fever.', room_type='building')
    qh_offering_basket_niche = area.room('qh_offering_basket_niche', name='Offering Basket Niche', desc='The south of Korahei lowers its voice around the Quiet House, where grief, remembrance, and hospitality share the same bowls. This part of the Quiet House and Southern Boat Path centers on offering basket niche, where names are spoken softly before any story is told. The path toward the ruins is not hidden, but the city expects players to approach it with humility instead of treasure fever.', room_type='building')
    qh_mended_paddle_rack = area.room('qh_mended_paddle_rack', name='Mended Paddle Rack', desc='The south of Korahei lowers its voice around the Quiet House, where grief, remembrance, and hospitality share the same bowls. This part of the Quiet House and Southern Boat Path centers on mended paddle rack, where stone basins hold clean water and floating sunleaf. The path toward the ruins is not hidden, but the city expects players to approach it with humility instead of treasure fever.', room_type='building')
    qh_ruins_warning_board = area.room('qh_ruins_warning_board', name='Ruins Warning Board', desc='The south of Korahei lowers its voice around the Quiet House, where grief, remembrance, and hospitality share the same bowls. This part of the Quiet House and Southern Boat Path centers on ruins warning board, where boat hooks hang beside warnings against careless salvage. The path toward the ruins is not hidden, but the city expects players to approach it with humility instead of treasure fever.', room_type='building')
    qh_boat_hook_wall = area.room('qh_boat_hook_wall', name='Boat Hook Wall', desc='The south of Korahei lowers its voice around the Quiet House, where grief, remembrance, and hospitality share the same bowls. This part of the Quiet House and Southern Boat Path centers on boat hook wall, where the surf below carries a hush different from the market. The path toward the ruins is not hidden, but the city expects players to approach it with humility instead of treasure fever.', room_type='building')
    qh_south_sand_stair = area.room('qh_south_sand_stair', name='South Sand Stair', desc='The south of Korahei lowers its voice around the Quiet House, where grief, remembrance, and hospitality share the same bowls. This part of the Quiet House and Southern Boat Path centers on south sand stair, where plain bowls are set out for visitors who do not know what to say. The path toward the ruins is not hidden, but the city expects players to approach it with humility instead of treasure fever.', room_type='building')
    qh_breakwater_shrine = area.room('qh_breakwater_shrine', name='Breakwater Shrine', desc='The south of Korahei lowers its voice around the Quiet House, where grief, remembrance, and hospitality share the same bowls. This part of the Quiet House and Southern Boat Path centers on breakwater shrine, where names are spoken softly before any story is told. The path toward the ruins is not hidden, but the city expects players to approach it with humility instead of treasure fever.', room_type='building')
    qh_low_boat_landing = area.room('qh_low_boat_landing', name='Low Boat Landing', desc='The south of Korahei lowers its voice around the Quiet House, where grief, remembrance, and hospitality share the same bowls. This part of the Quiet House and Southern Boat Path centers on low boat landing, where stone basins hold clean water and floating sunleaf. The path toward the ruins is not hidden, but the city expects players to approach it with humility instead of treasure fever.', room_type='building')
    qh_quiet_oar_stand = area.room('qh_quiet_oar_stand', name='Quiet Oar Stand', desc='The south of Korahei lowers its voice around the Quiet House, where grief, remembrance, and hospitality share the same bowls. This part of the Quiet House and Southern Boat Path centers on quiet oar stand, where boat hooks hang beside warnings against careless salvage. The path toward the ruins is not hidden, but the city expects players to approach it with humility instead of treasure fever.', room_type='building')
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
    _hearth_mother = area.npc(bm_first_bite_hearth, 'npc_hearth_mother_pelani', faction='kauroran', dialogue={'greeting': 'Hearth Mother Pelani studies you with open attention.', 'topics': {'help': 'Teaches first bites, shared bowls, and the difference between welcome and entitlement.', 'custom': 'Korahei expects guests to learn by helping, listening, and returning what they carry.'}, 'hints': ['Use talk and ask to learn why the errand matters before you run it.']}, ambient={'idle_echoes': ['Hearth Mother Pelani adjusts a small detail, making the place easier for the next person.'], 'idle_interval': 90, 'idle_variance': 30})
    _runner_lani = area.npc(ac_courier_platform, 'npc_runner_lani', faction='kauroran', dialogue={'greeting': 'Runner Lani studies you with open attention.', 'topics': {'help': 'Routes messages and small responsibilities to the reefs.', 'custom': 'Korahei expects guests to learn by helping, listening, and returning what they carry.'}, 'hints': ['Use talk and ask to learn why the errand matters before you run it.']}, ambient={'idle_echoes': ['Runner Lani adjusts a small detail, making the place easier for the next person.'], 'idle_interval': 90, 'idle_variance': 30})
    _name_keeper = area.npc(lt_listening_step, 'npc_name_keeper_haoa', faction='kauroran', dialogue={'greeting': 'Name-Keeper Haoa studies you with open attention.', 'topics': {'help': 'Helps guests learn names before asking favors.', 'custom': 'Korahei expects guests to learn by helping, listening, and returning what they carry.'}, 'hints': ['Use talk and ask to learn why the errand matters before you run it.']}, ambient={'idle_echoes': ['Name-Keeper Haoa adjusts a small detail, making the place easier for the next person.'], 'idle_interval': 90, 'idle_variance': 30})
    _warden_guest = area.npc(kg_warden_courtesy_mat, 'npc_warden_guest_iren', faction='warden', dialogue={'greeting': 'Warden Iren studies you with open attention.', 'topics': {'help': 'A guest ally careful not to mistake invitation for ownership.', 'custom': 'Korahei expects guests to learn by helping, listening, and returning what they carry.'}, 'hints': ['Use talk and ask to learn why the errand matters before you run it.']}, ambient={'idle_echoes': ['Warden Iren adjusts a small detail, making the place easier for the next person.'], 'idle_interval': 90, 'idle_variance': 30})
    _quiet_mareva = area.npc(qh_quiet_house_porch, 'npc_quiet_house_mareva', faction='kauroran', dialogue={'greeting': 'Quiet House Mareva studies you with open attention.', 'topics': {'help': 'Keeps bowls, names, and the southern boat path.', 'custom': 'Korahei expects guests to learn by helping, listening, and returning what they carry.'}, 'hints': ['Use talk and ask to learn why the errand matters before you run it.']}, ambient={'idle_echoes': ['Quiet House Mareva adjusts a small detail, making the place easier for the next person.'], 'idle_interval': 90, 'idle_variance': 30})
    _market_auntie = area.npc(bm_saltfruit_awning, 'npc_market_auntie_sola', faction='kauroran', dialogue={'greeting': 'Auntie Sola studies you with open attention.', 'topics': {'help': 'Sells food while making sure new guests eat and listen.', 'custom': 'Korahei expects guests to learn by helping, listening, and returning what they carry.'}, 'hints': ['Use talk and ask to learn why the errand matters before you run it.']}, ambient={'idle_echoes': ['Auntie Sola adjusts a small detail, making the place easier for the next person.'], 'idle_interval': 90, 'idle_variance': 30})
    _first_bite_child = area.npc(bm_shared_bowl_bench, 'npc_first_bite_child_makoa', faction='kauroran', dialogue={'greeting': 'Makoa of the First Bite studies you with open attention.', 'topics': {'help': 'A child taking the custom very seriously.', 'custom': 'Korahei expects guests to learn by helping, listening, and returning what they carry.'}, 'hints': ['Use talk and ask to learn why the errand matters before you run it.']}, ambient={'idle_echoes': ['Makoa of the First Bite adjusts a small detail, making the place easier for the next person.'], 'idle_interval': 90, 'idle_variance': 30})
    _market_auntie.db.is_vendor = True
    _market_auntie.db.vendor_accepts = ['consumable']
    _market_auntie.db.vendor_item_ids = ['trail_rations', 'spiced_fish', 'hearty_stew', 'minor_stamina_potion', 'bandage']
    _market_auntie.db.vendor_faction = None
    _market_auntie.db.player_stock = {}
    _tool_mender = area.npc(bm_tool_menders_shade, 'npc_tool_mender_koa', faction='kauroran', dialogue={'greeting': 'The vendor nods toward practical island supplies.', 'topics': {'trade': 'Tools, food, and modest gear keep a guest useful without making them reckless.'}})
    _tool_mender.db.is_vendor = True
    _tool_mender.db.vendor_accepts = ['tool', 'consumable']
    _tool_mender.db.vendor_item_ids = ['fishing_rod', 'bait', 'sickle', 'hatchet', 'skinning_knife', 'pickaxe', 'bandage']
    _tool_mender.db.vendor_faction = None
    _tool_mender.db.player_stock = {}
    _reef_outfitter = area.npc(ac_outer_mat_circle, 'npc_reef_outfitter_pao', faction='kauroran', dialogue={'greeting': 'The vendor nods toward practical island supplies.', 'topics': {'trade': 'Tools, food, and modest gear keep a guest useful without making them reckless.'}})
    _reef_outfitter.db.is_vendor = True
    _reef_outfitter.db.vendor_accepts = ['equipment', 'consumable', 'tool']
    _reef_outfitter.db.vendor_item_ids = ['iron_dagger', 'iron_staff', 'leather_vest', 'leather_boots', 'travelers_cloak', 'fishing_rod', 'bait', 'minor_healing_potion']
    _reef_outfitter.db.vendor_faction = None
    _reef_outfitter.db.player_stock = {}

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
        rewards=[{'action_type': 'give_scales', 'amount': 18}, {'action_type': 'modify_standing', 'faction_id': 'kauroran', 'delta': 25}],
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
        rewards=[{'action_type': 'give_scales', 'amount': 20}, {'action_type': 'give_skill_xp', 'skill_id': 'scholarship', 'count': 8}],
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
        rewards=[{'action_type': 'give_scales', 'amount': 24}, {'action_type': 'modify_standing', 'faction_id': 'warden', 'delta': 25}],
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

    return area.build()
