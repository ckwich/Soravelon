"""Velu'ana Central Isle -- Hub 5 exterior zone

A humid inner isle where circular paths, rain pools, basalt rings, and subtle node pressure create wonder without explaining the world's deeper secret."""

from world.area_builder import AreaBuilder


def build():
    area = AreaBuilder('veluana_central_isle')

    area.zone(
        name="Velu'ana Central Isle",
        zone_type='node_active',
        continent='veluana',
        tier=5,
        region='veluana_archipelago',
        hub_city='korahei',
        faction_territory='kauroran',
        faction_presence=['kauroran', 'wardens'],
        has_node=True,
        node_type='resonance',
        world_x=80,
        world_y=-1,
        world_radius=140,
    )

    area.material('reef_silverjack', tier=1, terrain='water', absorbed_property='finesse', profession_bonus={'cooking': 0.1, 'fishing': 0.05})
    area.material('tide_eel', tier=2, terrain='water', absorbed_property='timing', profession_bonus={'cooking': 0.1, 'alchemy': 0.05})
    area.material('saltfruit', tier=1, terrain='coastal', absorbed_property='endurance', profession_bonus={'cooking': 0.1})
    area.material('hearthroot', tier=2, terrain='garden', absorbed_property='warmth', profession_bonus={'cooking': 0.1, 'alchemy': 0.05})
    area.material('sunleaf', tier=1, terrain='garden', absorbed_property='clarity', profession_bonus={'alchemy': 0.1})
    area.material('old_ring_basalt', tier=2, terrain='ring', absorbed_property='resonance', profession_bonus={'smithing': 0.1, 'scholarship': 0.05})
    area.material('shore_drake_hide', tier=2, terrain='coastal', absorbed_property='resilience', profession_bonus={'smithing': 0.1})
    area.material('circle_bamboo', tier=2, terrain='ring', absorbed_property='balance', profession_bonus={'engineering': 0.1})

    # Rooms
    gc_korahei_track = area.room('gc_korahei_track', name='Korahei Track', desc='The green track leaves Korahei by crossing inner water and thick palms, then begins circling more than distance requires. Route charms, root arcs, and damp prints make orientation feel learned, not imposed.', room_type='path')
    gc_green_cause_start = area.room('gc_green_cause_start', name='Green Cause Start', desc='The Korahei track reaches a causeway where inward and outward route charms hang on separate rails despite sharing the same stone. Inoa’s board asks walkers to note weather, companions, and first impressions here, then compare them after completing the island loop.', room_type='path')
    gc_palm_root_arc = area.room('gc_palm_root_arc', name='Palm Root Arc', desc='Palm roots rise over the path in a broad arc reinforced by older stonework whose curve continues beneath the soil. Harvest bands mark mature circle-bamboo culms beyond the roots, leaving new shoots and the living support of the causeway outside the gathering cut.', room_type='path')
    gc_mist_pocket_step = area.room('gc_mist_pocket_step', name='Mist Pocket Step', desc='Cool mist gathers at ankle height on three steps while direct sun warms the rail above. Dated ribbons track how high and how long it lasted on earlier walks, with blank days preserved so the pocket remains an observation rather than a guaranteed trick.', room_type='path')
    gc_retied_route_charm = area.room('gc_retied_route_charm', name='Retied Route Charm', desc='A route charm has been repaired so often that five fibers and several hands share one small marker. Each knot records the direction its keeper believed useful that day; contradictory ties remain beside Inoa’s current mark instead of being cut away as embarrassment.', room_type='path')
    gc_repeating_bird_turn = area.room('gc_repeating_bird_turn', name='Repeating Bird Turn', desc='The same three-note bird call seems to answer from ahead, behind, and across the inner water. Sightings scratched onto a listening board identify several ordinary birds and many unheard sources, keeping sound-location errors separate from claims about what made them.', room_type='path')
    gc_loop_stone = area.room('gc_loop_stone', name='Loop Stone', desc="A loop stone rests where the path doubles back without quite admitting it. Inoa's scratches show how many travelers needed a second pass before the island's rhythm began to make sense.", room_type='path')
    gc_mossy_cause_rail = area.room('gc_mossy_cause_rail', name='Mossy Cause Rail', desc='Moss climbs the old cause rail where lizards slip between root shadows and pooled warmth. The rail turns the central loop into a living corridor, not an empty road between landmarks.', room_type='path')
    gc_inner_water_glance = area.room('gc_inner_water_glance', name='Inner Water Glance', desc='A narrow opening reveals the inner channel and a cause rail glimpsed through palms on the opposite side. Painted floats and tide times help walkers determine whether they are seeing a later part of their route, while moving reflections keep certainty usefully provisional.', room_type='path')
    gc_double_back_bend = area.room('gc_double_back_bend', name='Double-Back Bend', desc='The path turns around a fern-covered rise until the earlier causeway briefly appears ahead rather than behind. Inoa’s paired scratch marks distinguish compass bearing from felt direction, offering a tool for the second walk without naming the land’s deeper cause.', room_type='path')
    gc_kelp_scented_shade = area.room('gc_kelp_scented_shade', name='Kelp-Scented Shade', desc='Salt air settles beneath dense palms far from the visible shore, feeding a damp bed of naturalized saltfruit and hearthroot. Gathering tags identify replenished plants and compare their taste with coastal stock, while unmarked growth remains part of the ongoing survey.', room_type='path')
    gc_soft_mud_print = area.room('gc_soft_mud_print', name='Soft-Mud Record', desc='Soft mud preserves bird, lizard, and traveler tracks at a bend many walkers initially remember as new. A raised copy board lets Inoa trace prints before weather erases them, turning mistaken recognition into route evidence rather than ridicule.', room_type='path')
    gc_hidden_spring_sound = area.room('gc_hidden_spring_sound', name='Hidden Spring Sound', desc='Running water can be heard beneath root and basalt, though several marked searches found no safe opening to follow. Flow volume, recent rain, and tide are recorded at the rail, allowing the unseen spring to remain a changing question instead of an implied secret passage.', room_type='path')
    gc_warm_fern_run = area.room('gc_warm_fern_run', name='Warm Fern Run', desc='Warm ferns lean over the path where humid air holds moths in slow clouds. The run gives the central loop a breathing pressure, making every shortcut feel a little less certain.', room_type='path')
    gc_old_track_shoulder = area.room('gc_old_track_shoulder', name='Old Track Shoulder', desc='An older track runs beside the maintained path for a short span, narrowed by roots and marked closed where the ground has slumped. Former route charms remain dated along it, preserving how the loop changed without inviting travelers onto a line no longer inspected.', room_type='path')
    gc_round_stone_rest = area.room('gc_round_stone_rest', name='Round Stone Rest', desc='Six curved stones form a rest circle around a rain gauge and route-copy table. Walkers add what they now recognize from the first half of the loop, while erased guesses remain faintly visible beneath revised directions.', room_type='path')
    gc_unlost_turn = area.room('gc_unlost_turn', name='Unlost Turn', desc='Two familiar route charms appear at a turn that many walkers cannot place on their first pass. A sign avoids calling them lost and asks instead which observation would distinguish this bend tomorrow, making uncertainty a navigational skill rather than failure.', room_type='path')
    gc_green_cause_rise = area.room('gc_green_cause_rise', name='Green Cause Rise', desc='The causeway climbs above root level on stone darkened by constant humidity. Repair ledgers compare settling at matching points around the loop, and similar wear is recorded as a pattern to watch rather than proof that the sites are the same.', room_type='path')
    gc_central_light_gap = area.room('gc_central_light_gap', name='Central Light Gap', desc='A break in the canopy casts a bright oval across several paths that seem to approach it from too many angles. Shadow stakes record sun position and date, giving repeat walkers a stable comparison while the surrounding routes continue to feel less orderly than the light.', room_type='path')
    gc_humid_path_fork = area.room('gc_humid_path_fork', name='Humid Path Fork', desc='Two damp paths divide around a low ridge, both carrying route knots toward the rain pools ahead. Closure tags and return marks show which branch Inoa inspected today, and a blank comparison slate invites a later walk rather than promising either route is the definitive one.', room_type='path')
    rp_rain_pools = area.room('rp_rain_pools', name='Rain Pools', desc='Stone bowls hold rain-bright water under a clear sky, reflecting a shade of blue that never quite matches the air. The pools invite tracking and restraint without naming the deeper strangeness too early.', room_type='clearing')
    rp_clear_sky_ripple = area.room('rp_clear_sky_ripple', name='Clear-Sky Ripple', desc='Fresh rings cross a pool while unbroken blue sky shows between the palms. Toma’s suspended cloths, wind threads, insect counts, and timed sketches record what might have touched the surface, including intervals when every visible source failed to match the ripples.', room_type='clearing')
    rp_tide_mint_bowl = area.room('rp_tide_mint_bowl', name='Sunleaf-and-Mint Bowl', desc='Tide-scented mint and sunleaf share a damp stone bowl well inland from their expected gardens. Plot tags compare growth, water level, and flavor with coastal controls; mature sunleaf occupies the gathering band while roots, seed, and stressed plants remain in place.', room_type='clearing')
    rp_silent_frog_bank = area.room('rp_silent_frog_bank', name='Silent Frog Bank', desc="Frogs fall silent along this bank before footsteps arrive, and moths lift from the wet leaves in nervous sheets. The quiet turns combat into a clue about the pool's alert little ecosystem.", room_type='clearing')
    rp_bright_reflection_pool = area.room('rp_bright_reflection_pool', name='Bright Reflection Pool', desc='The reflected sky appears slightly brighter than the open air above this shallow pool. White, blue, and gray comparison tiles sit at fixed depths, with observations split by sun, cloud, viewer, and water clarity so perception remains part of the evidence.', room_type='clearing')
    rp_cupped_basalt_lip = area.room('rp_cupped_basalt_lip', name='Cupped Basalt Lip', desc='Basalt curves around the water like a worn basin, its inner edge banded by mineral deposits at several old levels. Toma measures water rise against rainfall and seepage while leaving the lip uncut, preserving the surface needed for future comparison.', room_type='clearing')
    rp_freshwater_thread = area.room('rp_freshwater_thread', name='Freshwater Thread', desc='A narrow thread leaves one pool, crosses bare stone, and disappears beneath a fern bank without reaching the lagoon in view. Flow markers compare rain, tide, heat, and neighboring pool levels, and no channel has been dug to force the water into a simpler answer.', room_type='clearing')
    rp_warm_rain_stone = area.room('rp_warm_rain_stone', name='Warm Rain Stone', desc='A dark stone beside the pool stays warmer than adjacent shade after sudden beads of moisture appear across it. Paired temperature slates follow stone, water, air, and a dry control, keeping warmth and wetness as separate observations until their timing actually agrees.', room_type='clearing')
    rp_round_pool_shelf = area.room('rp_round_pool_shelf', name='Round Pool Shelf', desc='A circular shelf holds sealed sample jars at equal distances from the water’s center. Color, scent, sediment, and collection time are recorded against blank control jars, giving later visits a repeatable comparison rather than a cabinet of mysterious water.', room_type='clearing')
    rp_unfallen_drop_ring = area.room('rp_unfallen_drop_ring', name='Unfallen-Drop Ring', desc='Concentric ripples begin near marked points even when no falling drop can be seen or heard. Overhead mesh, ground-vibration slates, and paired watches rule out some ordinary causes on some days, while the many inconclusive records remain filed beside the exceptions.', room_type='clearing')
    rp_moss_wet_seat = area.room('rp_moss_wet_seat', name='Moss-Wet Seat', desc='Moss keeps one stone seat damp through sunlit hours when nearby growth dries. Shade screens and weighed cloths test evaporation without scraping away the colony, allowing the living surface to remain both participant and protected subject.', room_type='clearing')
    rp_low_fern_mirror = area.room('rp_low_fern_mirror', name='Low Fern Mirror', desc='Low ferns lean over a pool that reflects their pale undersides more clearly than their green crowns. Leaf angles, wind, surface film, and viewing position fill Toma’s sketch frame, with changed fronds tagged instead of trimmed into a more convincing effect.', room_type='clearing')
    rp_singing_water_edge = area.room('rp_singing_water_edge', name='Singing Water Edge', desc='Water hums softly against the pool edge where fern roots drink from impossible freshness. Moths gather in the damp sound, making the place useful for practice and strange enough to remember.', room_type='clearing')
    rp_pale_fish_bowl = area.room('rp_pale_fish_bowl', name='Pale Fish Bowl', desc='Reef silverjack and tide eels occupy a deep bowl connected to other water by cracks too narrow to follow. Catch limits distinguish species, size, and season; marked releases and population counts protect the pool while samples compare how these fish differ from lagoon stock.', room_type='clearing')
    rp_green_light_basin = area.room('rp_green_light_basin', name='Green-Light Basin', desc='Green light gathers beneath the western lip after neighboring pools have entered shade. Removable screens, algae slides, depth markers, and timed drawings track what changes the color, with every instrument lifted away between observations rather than built into the basin.', room_type='clearing')
    rp_still_rain_cut = area.room('rp_still_rain_cut', name='Still-Rain Cut', desc='A narrow cut in the rock remains wet above the pool without a visible flow line. Threads placed across it register occasional droplets and long dry intervals, while a covered control cut nearby separates drifting mist from moisture emerging at the stone.', room_type='clearing')
    rp_pool_of_two_skies = area.room('rp_pool_of_two_skies', name='Pool of Two Skies', desc='One half of the pool reflects open blue while the other holds the green canopy even from a single viewing mark. Toma’s rotating shade frame tests light and angle, and the ledger records when the division blurs, reverses, or fails to appear at all.', room_type='clearing')
    rp_mist_breath_hollow = area.room('rp_mist_breath_hollow', name='Mist-Breath Hollow', desc='Mist breathes from a hollow even when the sky stays clear, beading on hair, leaves, and gear. Swarms coil in the vapor, giving the mystery teeth without turning it into exposition.', room_type='clearing')
    rp_last_rain_bowl = area.room('rp_last_rain_bowl', name='Last Rain Bowl', desc='The final pool carries dated level pins from years of clear mornings, sudden showers, drought, and unexplained refill. A closing ledger asks observers which patterns survived comparison and which need another season, making incomplete study the intended result rather than a failed revelation.', room_type='clearing')
    rp_pool_ridge_turn = area.room('rp_pool_ridge_turn', name='Pool Ridge Turn', desc='The wet ground rises toward old basalt rings where Safi maintains a separate listening record. Water samples and route notes can pass between the studies, but labels keep pool observation distinct from stone interpretation so proximity does not become a single convenient theory.', room_type='clearing')
    bs_basalt_ring = area.room('bs_basalt_ring', name='Basalt Ring', desc='Basalt stones spiral through the inner isle, warm on the edges and cool at the heart. Tool marks softened by age invite study, while the shape stays suggestive instead of explaining itself.', room_type='ruins')
    bs_warm_outer_spiral = area.room('bs_warm_outer_spiral', name='Warm Outer Spiral', desc='Sunlit basalt begins a curving walk whose outer stones stay warmer than shaded controls of similar size. Safi’s paired temperature slates record time, weather, moisture, surface, and observer, leaving the gradient measurable without declaring why this arrangement holds it.', room_type='ruins')
    bs_cool_center_stone = area.room('bs_cool_center_stone', name='Cool Center Stone', desc='The center stone stays cool under direct sun, ringed by tortoise grazes and old dust. Its refusal to behave normally makes investigation feel physical: touch, compare, and wonder carefully.', room_type='ruins')
    bs_crescent_moss_gap = area.room('bs_crescent_moss_gap', name='Crescent Moss Gap', desc='Moss fills a curved gap between stones but thins wherever tortoises, runoff, or direct sun cross it. Tracing frames compare the crescent over time without cutting it into a cleaner pattern, preserving irregular edges that may matter more than resemblance.', room_type='ruins')
    bs_tortoise_grazing_edge = area.room('bs_tortoise_grazing_edge', name='Tortoise Grazing Edge', desc='Basalt tortoises graze at the spiral edge where moss grows in crescent gaps. Their slow strength makes the ring feel inhabited by old habits instead of conveniently placed enemies.', room_type='ruins')
    bs_inland_shell_scatter = area.room('bs_inland_shell_scatter', name='Inland Shell Scatter', desc='Small sea shells lie among black stones beyond any visible high-water mark. Species, wear, soil depth, animal sign, and find position are mapped before a shell is moved, allowing storm, trade, wildlife, and deliberate placement to remain competing histories.', room_type='ruins')
    bs_tool_softened_mark = area.room('bs_tool_softened_mark', name='Tool-Softened Mark', desc='Parallel depressions cross one stone beneath weather polish and lichen. Raking-light sketches compare the marks with known quarry, repair, root, and erosion traces, while the stone stays in place and their maker—if there was one—remains unnamed.', room_type='ruins')
    bs_old_ring_notch = area.room('bs_old_ring_notch', name='Old Ring Notch', desc='A squared notch interrupts the curved stone line at knee height, worn more deeply on its seaward side. Insert gauges record dimensions without testing what might fit, and tortoise rubs are logged separately from older wear rather than used to explain it away.', room_type='ruins')
    bs_black_stone_step = area.room('bs_black_stone_step', name='Black Stone Step', desc='A single basalt block rises like a step where the walk tightens toward the inner stones. Edge wear, sediment, and comfortable foot placement are recorded alongside a bypass, since present use does not prove the block was built as a stair.', room_type='ruins')
    bs_narrow_spiral_walk = area.room('bs_narrow_spiral_walk', name='Narrow Spiral Walk', desc='The route narrows between stone and moss until walkers must pass one at a time or use the outer mat. Distance tags count turns from both directions, helping repeat visitors separate the spiral’s physical length from the longer journey they often remember.', room_type='ruins')
    bs_center_listening_seat = area.room('bs_center_listening_seat', name='Center Listening Seat', desc='Basalt Listener Safi keeps a movable seat near the ring’s cool interior, never fixed to the old stone. Listening cards separate wind, water, insects, tortoises, footfall, and unexplained vibration by time and witness, treating disagreement as part of the record.', room_type='ruins')
    bs_basalt_dust_pocket = area.room('bs_basalt_dust_pocket', name='Basalt Dust Pocket', desc='Dark grit gathers behind a low stone where runoff and tortoise movement naturally sort heavier fragments. Clearly shed material occupies a measured gathering tray; source, grain, moisture, and removed weight are logged so useful samples do not quietly excavate the ring.', room_type='ruins')
    bs_round_echo_wall = area.room('bs_round_echo_wall', name='Curved Echo Wall', desc='A curved wall returns claps, speech, and soft hammer taps at noticeably different strengths along its face. Safi’s test points include open-air controls and hearing positions, preventing an attractive echo from becoming evidence for a ceremonial purpose no one has established.', room_type='ruins')
    bs_stone_warm_hollow = area.room('bs_stone_warm_hollow', name='Stone-Warm Hollow', desc='A warm hollow between black stones gathers tortoises, shed grit, and the smell of wet mineral. The spiral offers combat practice through stubborn wildlife rather than staged guardians.', room_type='ruins')
    bs_half_buried_ring = area.room('bs_half_buried_ring', name='Half-Buried Ring', desc='A smaller curve of stones disappears beneath soil and roots before its full outline can be followed. Depth probes stop above resistance and a seasonal plant map covers the buried reach, preserving both structure and habitat instead of clearing one to reveal the other.', room_type='ruins')
    bs_spiral_return_turn = area.room('bs_spiral_return_turn', name='Spiral Return Turn', desc='The inner walk meets a marked return line that leads outward without retracing every curve. Direction, time, and recognition notes from both routes hang together, making safe exit part of Safi’s study and preventing confusion from being romanticized as revelation.', room_type='ruins')
    bs_marked_basalt_face = area.room('bs_marked_basalt_face', name='Marked Basalt Face', desc='A standing face carries softened grooves beside a naturally fractured edge. Only loose material from the labeled fall pocket may be gathered; sample number, exact find place, weight, and later analysis stay linked while the marked face remains uncut.', room_type='ruins')
    bs_moss_crescent_rise = area.room('bs_moss_crescent_rise', name='Moss Crescent Rise', desc='Several moss crescents climb a low rise at different moisture and sun exposures. Tortoise grazing exclusions cover only comparison patches and rotate by season, allowing Safi to distinguish animal influence without evicting the creatures that live among the stones.', room_type='ruins')
    bs_inner_ring_shelf = area.room('bs_inner_ring_shelf', name='Inner Ring Shelf', desc='A level shelf gives researchers room to compare samples and observations without setting equipment on the old ring. Separate trays hold pool water, lagoon sediment, ruin mineral, and basalt notes, keeping adjacency from turning distinct evidence into one sweeping explanation.', room_type='ruins')
    bs_quiet_black_center = area.room('bs_quiet_black_center', name='Quiet Black Center', desc='The spiral’s quiet center contains cool stone, scattered shell, tortoise tracks, and many seasons of contradictory listening records. A closing slate asks what repeated, what changed, and what remains unsupported; no inscription, map, or keeper claims the island has disclosed its shape or purpose.', room_type='ruins')
    hr_humid_ruin = area.room('hr_humid_ruin', name='Humid Ruin', desc='Low walls sleep under vines and shell-white fungus, suggesting old use without surrendering easy answers. The ruin is a breadcrumb: enough structure to invite questions, not enough to solve the island.', room_type='ruins')
    hr_vine_hidden_wall = area.room('hr_vine_hidden_wall', name='Vine-Hidden Wall', desc='Dense vines conceal a wall until rain darkens the mortar line beneath their leaves. Survey cords follow only exposed masonry, and dated sketches record sections revealed by natural dieback rather than cutting living cover to complete an imagined shape.', room_type='ruins')
    hr_shell_fungus_crack = area.room('hr_shell_fungus_crack', name='Shell-Fungus Crack', desc='Shell-white fungus beads along a shaded crack and bridges several tiny gaps in the stone. Spore, moisture, and widening marks are observed from either side, leaving the living colony intact while conservators learn whether it protects, damages, or merely occupies the wall.', room_type='ruins')
    hr_circle_facing_threshold = area.room('hr_circle_facing_threshold', name='Circle-Facing Threshold', desc='A broken threshold opens toward a roughly circular court rather than any surviving road. Compass marks and wall fragments establish the present alignment; missing foundations and displaced stones keep its original approach and use unresolved.', room_type='ruins')
    hr_sunset_plaster_niche = area.room('hr_sunset_plaster_niche', name='Sunset Plaster Niche', desc='A shallow niche preserves orange, rose, and smoke-gray plaster beneath an overhang. Color cards track fading across seasons, and no pigment is scraped for a definitive sample while light, mineral, and later repair remain plausible sources.', room_type='ruins')
    hr_rain_mineral_hall = area.room('hr_rain_mineral_hall', name='Rain-Mineral Hall', desc='Rain enters through an absent roof and leaves pale mineral fans down opposing walls. Catch jars compare fresh runoff with nearby pool water, while a clear path keeps boots from grinding the deposits into evidence that cannot be revisited.', room_type='ruins')
    hr_broken_palm_court = area.room('hr_broken_palm_court', name='Broken Palm Court', desc='A mature palm rises through a court of cracked paving, lifting some stones and shading others from rain. Growth rings, root movement, and older repair gaps are mapped separately, resisting the temptation to blame every break on either the tree or the builders.', room_type='ruins')
    hr_root_lifted_floor = area.room('hr_root_lifted_floor', name='Root-Lifted Floor', desc='Roots have raised the floor into ridges with hollow, unstable pockets between them. A narrow mat route crosses only tested stones, and movement stakes remain for later seasons instead of flattening the floor into easier passage.', room_type='ruins')
    hr_low_arch_moss = area.room('hr_low_arch_moss', name='Low Moss Arch', desc='A low arch survives under moss thick enough to hide joints and old chips. Height and stability marks are taken from freestanding frames, while the marked bypass avoids rubbing away growth merely to prove the opening can still be used.', room_type='ruins')
    hr_damp_color_room = area.room('hr_damp_color_room', name='Damp Color Room', desc='Faint wall color deepens after rain and recedes unevenly as the chamber dries. Humidity slates and photographs compare the change without wetting the plaster on purpose, preserving both the pigment and the uncertainty of what the stronger color once represented.', room_type='ruins')
    hr_fallen_lintel_seat = area.room('hr_fallen_lintel_seat', name='Fallen Lintel', desc='A carved lintel lies at bench height but remains corded against sitting or climbing. Its visible face is copied beside the route, and the buried face stays undisturbed until a supported lift has a conservation reason stronger than curiosity.', room_type='ruins')
    hr_old_door_without_road = area.room('hr_old_door_without_road', name='Door Without Road', desc='Two jambs and a worn sill stand where root, mud, and later wall fall leave no surviving approach. Survey layers show several possible paths without choosing one, and the opening leads only to the next inspected chamber rather than a hidden route.', room_type='ruins')
    hr_misty_wall_bend = area.room('hr_misty_wall_bend', name='Misty Wall Bend', desc='Mist from the lower pools gathers where two ruin walls make a blind bend. Visibility cords and edge markers shift with each watch, keeping the safe line honest while damp acoustics make distances beyond the turn difficult to judge.', room_type='ruins')
    hr_hidden_drain_stone = area.room('hr_hidden_drain_stone', name='Covered Drain Stone', desc='A slotted stone beneath vines admits rainwater into a channel that cannot be followed without dismantling the floor. Flow, sediment, and downstream seepage are recorded during storms, allowing drainage skill to be recognized without inventing the structure it once served.', room_type='ruins')
    hr_soft_fern_chamber = area.room('hr_soft_fern_chamber', name='Soft-Fern Chamber', desc='Ferns fill a roofless chamber whose walls create cool shade and constant leaf drip. Species and nesting signs are mapped around a narrow perimeter, treating the room’s present habitat as real history rather than clutter covering the preferred past.', room_type='ruins')
    hr_wet_plaster_shelf = area.room('hr_wet_plaster_shelf', name='Wet Plaster Shelf', desc='A sheltered shelf holds plaster fragments loosened by moisture from the wall above. Each piece is left where found under a raised screen with date and fall conditions, preserving context that a basket of attractive fragments would destroy.', room_type='ruins')
    hr_grey_vine_gallery = area.room('hr_grey_vine_gallery', name='Gray-Vine Gallery', desc='Gray vines cross a long wall in lines that resemble faded decoration until their new growth catches the light. Botanical tags and masonry tracings use different colors, keeping the living pattern from being mistaken for a recovered design.', room_type='ruins')
    hr_quiet_root_stair = area.room('hr_quiet_root_stair', name='Root-Broken Stair', desc='Roots interrupt a narrow stair after five tested steps, with loose stone and an unmeasured drop beyond. The upper flight is explicitly closed; survey mirrors provide a partial view without turning a dangerous gap into a promised destination.', room_type='ruins')
    hr_collapsed_shade_room = area.room('hr_collapsed_shade_room', name='Collapsed Shade Room', desc='A wall fall has roofed part of this chamber in unstable slabs and deep leaf shadow. Movement pins, rain dates, and a broad exclusion line document the collapse from safety, while no glint or gap is described as treasure access.', room_type='ruins')
    hr_last_humid_wall = area.room('hr_last_humid_wall', name='Last Humid Wall', desc='The inspected ruin route ends at a wall sweating mineral water beneath woven vines. A return board gathers structure, pigment, drainage, and habitat questions separately, and the unverified ground beyond remains unclaimed rather than shaped into an answer by the end of the path.', room_type='ruins')
    lc_lagoon_crown_mouth = area.room('lc_lagoon_crown_mouth', name='Lagoon Crown Mouth', desc='The circular island route opens onto a broad lagoon edged by fern, reed, saltfruit, and shifting sand bars. A habitat board separates current fishing reaches, drake crossings, nursery water, and the marked return path, making abundance legible before anyone enters it.', room_type='clearing')
    lc_green_blue_step = area.room('lc_green_blue_step', name='Green-Blue Step', desc='Lagoon water changes from leaf green to clear blue across a submerged shelf narrow enough to step over. Depth tiles, tide marks, algae samples, and sun position are logged on both sides, letting Toma compare the color boundary without presenting it as a permanent line.', room_type='clearing')
    lc_saltfruit_root_bank = area.room('lc_saltfruit_root_bank', name='Saltfruit Root Bank', desc='Saltfruit roots bind a wet bank where old tide scars show how much soil would otherwise leave each season. Fruit and mature hearthroot occupy marked gathering pockets, while seed stock, stabilizing roots, and storm-damaged recovery beds remain outside the cut.', room_type='clearing')
    lc_warm_belly_trail = area.room('lc_warm_belly_trail', name='Warm Belly Trail', desc='Wide belly trails cross sun-warmed sand between reed cover and deeper water. Track cards distinguish shore drake, tideback lizard, and boat drag by width, scale print, and timing, giving travelers a fair warning without promising the animal has already moved on.', room_type='clearing')
    lc_hanging_fern_fish = area.room('lc_hanging_fern_fish', name='Hanging-Fern Fishery', desc='Fern shade cools a channel where reef silverjack and tide eels feed along submerged roots. Species, size, season, and released catch are tallied separately, and a closed nursery pocket keeps the useful fishing site capable of replenishing itself.', room_type='clearing')
    lc_shell_cairn_return = area.room('lc_shell_cairn_return', name='Shell Cairn Return', desc='Low cairns use wave-broken shell and plain stone to mark the route back without stripping living reef. Every marker has a matching sightline on the next bend and a repair date, making return navigation a maintained chain rather than faith in one picturesque pile.', room_type='clearing')
    lc_quiet_lagoon_seat = area.room('lc_quiet_lagoon_seat', name='Quiet Lagoon Seat', desc='A driftwood seat faces bird shallows and the green-blue shelf from behind a reed screen. Observation slates ask for time, tide, weather, and disturbance, allowing a patient visitor to add habitat knowledge without approaching nests or feeding animals.', room_type='clearing')
    lc_reed_warm_edge = area.room('lc_reed_warm_edge', name='Reed-Warm Edge', desc='Reeds trap heat along the lagoon edge, and shore drakes nose through them after small fish. The line is beautiful, useful, and sharp enough to keep gathering from becoming sleepwalking.', room_type='clearing')
    lc_deep_color_cut = area.room('lc_deep_color_cut', name='Deep-Color Cut', desc='A narrow cut drops abruptly from pale sand into water too dark to judge by color alone. Sounding knots and current ribbons mark the safe edge, while repeated measurements remain posted where depth and apparent shade disagreed.', room_type='clearing')
    lc_small_fish_shade = area.room('lc_small_fish_shade', name='Small-Fish Shade', desc='Palm and fern roots create a crowded refuge for young fish beside the walking line. A no-catch marker shifts with water level and spawning counts, protecting the nursery without closing neighboring adult-fish reaches by habit.', room_type='clearing')
    lc_palm_loop_bank = area.room('lc_palm_loop_bank', name='Palm-Loop Bank', desc='Palms and circle bamboo follow the lagoon in a curve that resembles the inland causeway from certain angles. Harvest bands identify mature bamboo useful for cairn and rail repair; roots, new culms, and bank-stabilizing growth remain visibly protected.', room_type='clearing')
    lc_shore_track_bar = area.room('lc_shore_track_bar', name='Shore-Drake Crossing', desc='Shore drake tracks braid across a sand bar between saltfruit roots and clear water, refreshed often enough to establish a living route. Track direction, tide, feeding sign, and old hide provenance are posted before the crossing, making any encounter or gathering accountable to territory and evidence.', room_type='clearing')
    lc_clear_water_turn = area.room('lc_clear_water_turn', name='Clear-Water Turn', desc='Clear water wraps around a low bank where submerged tracks can be followed farther than those on sand. Viewing stones keep observers off the route itself, and clouded patches are dated rather than swept clean when drakes, fish, or a changed current disturb the bottom.', room_type='clearing')
    lc_lagoon_bird_stone = area.room('lc_lagoon_bird_stone', name='Lagoon Bird Stone', desc='A flat stone overlooks feeding shallows used by long-legged birds at falling tide. Nest distance, flock count, alarm behavior, and fishing activity share one slate, linking a quiet watch to decisions about when nearby gathering should pause.', room_type='clearing')
    lc_low_return_cairn = area.room('lc_low_return_cairn', name='Low Return Cairn', desc='This cairn sits below the usual sightline and appears only after the path descends around a fern bank. A raised companion mark on the rail prevents it from becoming a trap for shorter travelers or high water, and both markers share the same inspection tag.', room_type='clearing')
    lc_fern_dark_pool = area.room('lc_fern_dark_pool', name='Fern-Dark Pool', desc='Overlapping ferns shade a pool whose surface hides root snags and tide-eel burrows. A perimeter cord marks the measured footing, while a sampling gap remains open for Toma’s water comparisons without implying the dark center should be entered.', room_type='clearing')
    lc_long_sand_tongue = area.room('lc_long_sand_tongue', name='Long Sand Tongue', desc='A sand tongue reaches into the lagoon and changes length with every tide and storm. Dated stakes trace its recent edges, and temporary route knots move with them so an inviting strip of dry ground never masquerades as permanent passage.', room_type='clearing')
    lc_inner_lagoon_shelf = area.room('lc_inner_lagoon_shelf', name='Inner Lagoon Shelf', desc="The inner shelf slopes from reed shade into blue-green water where belly trails cross warm sand. Lizards hunt fish here, tying danger to the lagoon's abundance instead of random aggression.", room_type='clearing')
    lc_blue_crown_bend = area.room('lc_blue_crown_bend', name='Blue-Lagoon Bend', desc='Blue water, reed green, and pale sand meet at a bend where three habitat boundaries change with the tide. Route notes compare the lagoon circuit with earlier pool observations without suggesting their similar curves share a known origin.', room_type='clearing')
    lc_last_lagoon_cairn = area.room('lc_last_lagoon_cairn', name='Last Lagoon Cairn', desc='The final shell-and-stone marker points back through every verified return cairn and inland toward the high ring path. Catch, track, weather, and route notes have separate return pockets here, ensuring lagoon evidence can travel without collapsing distinct observations into one theory.', room_type='clearing')

    # Local exits
    area.exit(gc_korahei_track, gc_green_cause_start, 'east')
    area.exit(gc_green_cause_start, gc_korahei_track, 'west')
    area.exit(gc_green_cause_start, gc_palm_root_arc, 'east')
    area.exit(gc_palm_root_arc, gc_green_cause_start, 'west')
    area.exit(gc_palm_root_arc, gc_mist_pocket_step, 'east')
    area.exit(gc_mist_pocket_step, gc_palm_root_arc, 'west')
    area.exit(gc_mist_pocket_step, gc_retied_route_charm, 'east')
    area.exit(gc_retied_route_charm, gc_mist_pocket_step, 'west')
    area.exit(gc_retied_route_charm, gc_repeating_bird_turn, 'east')
    area.exit(gc_repeating_bird_turn, gc_retied_route_charm, 'west')
    area.exit(gc_repeating_bird_turn, gc_loop_stone, 'east')
    area.exit(gc_loop_stone, gc_repeating_bird_turn, 'west')
    area.exit(gc_loop_stone, gc_mossy_cause_rail, 'east')
    area.exit(gc_mossy_cause_rail, gc_loop_stone, 'west')
    area.exit(gc_mossy_cause_rail, gc_inner_water_glance, 'east')
    area.exit(gc_inner_water_glance, gc_mossy_cause_rail, 'west')
    area.exit(gc_inner_water_glance, gc_double_back_bend, 'east')
    area.exit(gc_double_back_bend, gc_inner_water_glance, 'west')
    area.exit(gc_double_back_bend, gc_kelp_scented_shade, 'east')
    area.exit(gc_kelp_scented_shade, gc_double_back_bend, 'west')
    area.exit(gc_kelp_scented_shade, gc_soft_mud_print, 'east')
    area.exit(gc_soft_mud_print, gc_kelp_scented_shade, 'west')
    area.exit(gc_soft_mud_print, gc_hidden_spring_sound, 'east')
    area.exit(gc_hidden_spring_sound, gc_soft_mud_print, 'west')
    area.exit(gc_hidden_spring_sound, gc_warm_fern_run, 'east')
    area.exit(gc_warm_fern_run, gc_hidden_spring_sound, 'west')
    area.exit(gc_warm_fern_run, gc_old_track_shoulder, 'east')
    area.exit(gc_old_track_shoulder, gc_warm_fern_run, 'west')
    area.exit(gc_old_track_shoulder, gc_round_stone_rest, 'east')
    area.exit(gc_round_stone_rest, gc_old_track_shoulder, 'west')
    area.exit(gc_round_stone_rest, gc_unlost_turn, 'east')
    area.exit(gc_unlost_turn, gc_round_stone_rest, 'west')
    area.exit(gc_unlost_turn, gc_green_cause_rise, 'east')
    area.exit(gc_green_cause_rise, gc_unlost_turn, 'west')
    area.exit(gc_green_cause_rise, gc_central_light_gap, 'east')
    area.exit(gc_central_light_gap, gc_green_cause_rise, 'west')
    area.exit(gc_central_light_gap, gc_humid_path_fork, 'east')
    area.exit(gc_humid_path_fork, gc_central_light_gap, 'west')
    area.exit(rp_rain_pools, rp_clear_sky_ripple, 'east')
    area.exit(rp_clear_sky_ripple, rp_rain_pools, 'west')
    area.exit(rp_clear_sky_ripple, rp_tide_mint_bowl, 'east')
    area.exit(rp_tide_mint_bowl, rp_clear_sky_ripple, 'west')
    area.exit(rp_tide_mint_bowl, rp_silent_frog_bank, 'east')
    area.exit(rp_silent_frog_bank, rp_tide_mint_bowl, 'west')
    area.exit(rp_silent_frog_bank, rp_bright_reflection_pool, 'east')
    area.exit(rp_bright_reflection_pool, rp_silent_frog_bank, 'west')
    area.exit(rp_bright_reflection_pool, rp_cupped_basalt_lip, 'east')
    area.exit(rp_cupped_basalt_lip, rp_bright_reflection_pool, 'west')
    area.exit(rp_cupped_basalt_lip, rp_freshwater_thread, 'east')
    area.exit(rp_freshwater_thread, rp_cupped_basalt_lip, 'west')
    area.exit(rp_freshwater_thread, rp_warm_rain_stone, 'east')
    area.exit(rp_warm_rain_stone, rp_freshwater_thread, 'west')
    area.exit(rp_warm_rain_stone, rp_round_pool_shelf, 'east')
    area.exit(rp_round_pool_shelf, rp_warm_rain_stone, 'west')
    area.exit(rp_round_pool_shelf, rp_unfallen_drop_ring, 'east')
    area.exit(rp_unfallen_drop_ring, rp_round_pool_shelf, 'west')
    area.exit(rp_unfallen_drop_ring, rp_moss_wet_seat, 'east')
    area.exit(rp_moss_wet_seat, rp_unfallen_drop_ring, 'west')
    area.exit(rp_moss_wet_seat, rp_low_fern_mirror, 'east')
    area.exit(rp_low_fern_mirror, rp_moss_wet_seat, 'west')
    area.exit(rp_low_fern_mirror, rp_singing_water_edge, 'east')
    area.exit(rp_singing_water_edge, rp_low_fern_mirror, 'west')
    area.exit(rp_singing_water_edge, rp_pale_fish_bowl, 'east')
    area.exit(rp_pale_fish_bowl, rp_singing_water_edge, 'west')
    area.exit(rp_pale_fish_bowl, rp_green_light_basin, 'east')
    area.exit(rp_green_light_basin, rp_pale_fish_bowl, 'west')
    area.exit(rp_green_light_basin, rp_still_rain_cut, 'east')
    area.exit(rp_still_rain_cut, rp_green_light_basin, 'west')
    area.exit(rp_still_rain_cut, rp_pool_of_two_skies, 'east')
    area.exit(rp_pool_of_two_skies, rp_still_rain_cut, 'west')
    area.exit(rp_pool_of_two_skies, rp_mist_breath_hollow, 'east')
    area.exit(rp_mist_breath_hollow, rp_pool_of_two_skies, 'west')
    area.exit(rp_mist_breath_hollow, rp_last_rain_bowl, 'east')
    area.exit(rp_last_rain_bowl, rp_mist_breath_hollow, 'west')
    area.exit(rp_last_rain_bowl, rp_pool_ridge_turn, 'east')
    area.exit(rp_pool_ridge_turn, rp_last_rain_bowl, 'west')
    area.exit(bs_basalt_ring, bs_warm_outer_spiral, 'east')
    area.exit(bs_warm_outer_spiral, bs_basalt_ring, 'west')
    area.exit(bs_warm_outer_spiral, bs_cool_center_stone, 'east')
    area.exit(bs_cool_center_stone, bs_warm_outer_spiral, 'west')
    area.exit(bs_cool_center_stone, bs_crescent_moss_gap, 'east')
    area.exit(bs_crescent_moss_gap, bs_cool_center_stone, 'west')
    area.exit(bs_crescent_moss_gap, bs_tortoise_grazing_edge, 'east')
    area.exit(bs_tortoise_grazing_edge, bs_crescent_moss_gap, 'west')
    area.exit(bs_tortoise_grazing_edge, bs_inland_shell_scatter, 'east')
    area.exit(bs_inland_shell_scatter, bs_tortoise_grazing_edge, 'west')
    area.exit(bs_inland_shell_scatter, bs_tool_softened_mark, 'east')
    area.exit(bs_tool_softened_mark, bs_inland_shell_scatter, 'west')
    area.exit(bs_tool_softened_mark, bs_old_ring_notch, 'east')
    area.exit(bs_old_ring_notch, bs_tool_softened_mark, 'west')
    area.exit(bs_old_ring_notch, bs_black_stone_step, 'east')
    area.exit(bs_black_stone_step, bs_old_ring_notch, 'west')
    area.exit(bs_black_stone_step, bs_narrow_spiral_walk, 'east')
    area.exit(bs_narrow_spiral_walk, bs_black_stone_step, 'west')
    area.exit(bs_narrow_spiral_walk, bs_center_listening_seat, 'east')
    area.exit(bs_center_listening_seat, bs_narrow_spiral_walk, 'west')
    area.exit(bs_center_listening_seat, bs_basalt_dust_pocket, 'east')
    area.exit(bs_basalt_dust_pocket, bs_center_listening_seat, 'west')
    area.exit(bs_basalt_dust_pocket, bs_round_echo_wall, 'east')
    area.exit(bs_round_echo_wall, bs_basalt_dust_pocket, 'west')
    area.exit(bs_round_echo_wall, bs_stone_warm_hollow, 'east')
    area.exit(bs_stone_warm_hollow, bs_round_echo_wall, 'west')
    area.exit(bs_stone_warm_hollow, bs_half_buried_ring, 'east')
    area.exit(bs_half_buried_ring, bs_stone_warm_hollow, 'west')
    area.exit(bs_half_buried_ring, bs_spiral_return_turn, 'east')
    area.exit(bs_spiral_return_turn, bs_half_buried_ring, 'west')
    area.exit(bs_spiral_return_turn, bs_marked_basalt_face, 'east')
    area.exit(bs_marked_basalt_face, bs_spiral_return_turn, 'west')
    area.exit(bs_marked_basalt_face, bs_moss_crescent_rise, 'east')
    area.exit(bs_moss_crescent_rise, bs_marked_basalt_face, 'west')
    area.exit(bs_moss_crescent_rise, bs_inner_ring_shelf, 'east')
    area.exit(bs_inner_ring_shelf, bs_moss_crescent_rise, 'west')
    area.exit(bs_inner_ring_shelf, bs_quiet_black_center, 'east')
    area.exit(bs_quiet_black_center, bs_inner_ring_shelf, 'west')
    area.exit(hr_humid_ruin, hr_vine_hidden_wall, 'east')
    area.exit(hr_vine_hidden_wall, hr_humid_ruin, 'west')
    area.exit(hr_vine_hidden_wall, hr_shell_fungus_crack, 'east')
    area.exit(hr_shell_fungus_crack, hr_vine_hidden_wall, 'west')
    area.exit(hr_shell_fungus_crack, hr_circle_facing_threshold, 'east')
    area.exit(hr_circle_facing_threshold, hr_shell_fungus_crack, 'west')
    area.exit(hr_circle_facing_threshold, hr_sunset_plaster_niche, 'east')
    area.exit(hr_sunset_plaster_niche, hr_circle_facing_threshold, 'west')
    area.exit(hr_sunset_plaster_niche, hr_rain_mineral_hall, 'east')
    area.exit(hr_rain_mineral_hall, hr_sunset_plaster_niche, 'west')
    area.exit(hr_rain_mineral_hall, hr_broken_palm_court, 'east')
    area.exit(hr_broken_palm_court, hr_rain_mineral_hall, 'west')
    area.exit(hr_broken_palm_court, hr_root_lifted_floor, 'east')
    area.exit(hr_root_lifted_floor, hr_broken_palm_court, 'west')
    area.exit(hr_root_lifted_floor, hr_low_arch_moss, 'east')
    area.exit(hr_low_arch_moss, hr_root_lifted_floor, 'west')
    area.exit(hr_low_arch_moss, hr_damp_color_room, 'east')
    area.exit(hr_damp_color_room, hr_low_arch_moss, 'west')
    area.exit(hr_damp_color_room, hr_fallen_lintel_seat, 'east')
    area.exit(hr_fallen_lintel_seat, hr_damp_color_room, 'west')
    area.exit(hr_fallen_lintel_seat, hr_old_door_without_road, 'east')
    area.exit(hr_old_door_without_road, hr_fallen_lintel_seat, 'west')
    area.exit(hr_old_door_without_road, hr_misty_wall_bend, 'east')
    area.exit(hr_misty_wall_bend, hr_old_door_without_road, 'west')
    area.exit(hr_misty_wall_bend, hr_hidden_drain_stone, 'east')
    area.exit(hr_hidden_drain_stone, hr_misty_wall_bend, 'west')
    area.exit(hr_hidden_drain_stone, hr_soft_fern_chamber, 'east')
    area.exit(hr_soft_fern_chamber, hr_hidden_drain_stone, 'west')
    area.exit(hr_soft_fern_chamber, hr_wet_plaster_shelf, 'east')
    area.exit(hr_wet_plaster_shelf, hr_soft_fern_chamber, 'west')
    area.exit(hr_wet_plaster_shelf, hr_grey_vine_gallery, 'east')
    area.exit(hr_grey_vine_gallery, hr_wet_plaster_shelf, 'west')
    area.exit(hr_grey_vine_gallery, hr_quiet_root_stair, 'east')
    area.exit(hr_quiet_root_stair, hr_grey_vine_gallery, 'west')
    area.exit(hr_quiet_root_stair, hr_collapsed_shade_room, 'east')
    area.exit(hr_collapsed_shade_room, hr_quiet_root_stair, 'west')
    area.exit(hr_collapsed_shade_room, hr_last_humid_wall, 'east')
    area.exit(hr_last_humid_wall, hr_collapsed_shade_room, 'west')
    area.exit(lc_lagoon_crown_mouth, lc_green_blue_step, 'east')
    area.exit(lc_green_blue_step, lc_lagoon_crown_mouth, 'west')
    area.exit(lc_green_blue_step, lc_saltfruit_root_bank, 'east')
    area.exit(lc_saltfruit_root_bank, lc_green_blue_step, 'west')
    area.exit(lc_saltfruit_root_bank, lc_warm_belly_trail, 'east')
    area.exit(lc_warm_belly_trail, lc_saltfruit_root_bank, 'west')
    area.exit(lc_warm_belly_trail, lc_hanging_fern_fish, 'east')
    area.exit(lc_hanging_fern_fish, lc_warm_belly_trail, 'west')
    area.exit(lc_hanging_fern_fish, lc_shell_cairn_return, 'east')
    area.exit(lc_shell_cairn_return, lc_hanging_fern_fish, 'west')
    area.exit(lc_shell_cairn_return, lc_quiet_lagoon_seat, 'east')
    area.exit(lc_quiet_lagoon_seat, lc_shell_cairn_return, 'west')
    area.exit(lc_quiet_lagoon_seat, lc_reed_warm_edge, 'east')
    area.exit(lc_reed_warm_edge, lc_quiet_lagoon_seat, 'west')
    area.exit(lc_reed_warm_edge, lc_deep_color_cut, 'east')
    area.exit(lc_deep_color_cut, lc_reed_warm_edge, 'west')
    area.exit(lc_deep_color_cut, lc_small_fish_shade, 'east')
    area.exit(lc_small_fish_shade, lc_deep_color_cut, 'west')
    area.exit(lc_small_fish_shade, lc_palm_loop_bank, 'east')
    area.exit(lc_palm_loop_bank, lc_small_fish_shade, 'west')
    area.exit(lc_palm_loop_bank, lc_shore_track_bar, 'east')
    area.exit(lc_shore_track_bar, lc_palm_loop_bank, 'west')
    area.exit(lc_shore_track_bar, lc_clear_water_turn, 'east')
    area.exit(lc_clear_water_turn, lc_shore_track_bar, 'west')
    area.exit(lc_clear_water_turn, lc_lagoon_bird_stone, 'east')
    area.exit(lc_lagoon_bird_stone, lc_clear_water_turn, 'west')
    area.exit(lc_lagoon_bird_stone, lc_low_return_cairn, 'east')
    area.exit(lc_low_return_cairn, lc_lagoon_bird_stone, 'west')
    area.exit(lc_low_return_cairn, lc_fern_dark_pool, 'east')
    area.exit(lc_fern_dark_pool, lc_low_return_cairn, 'west')
    area.exit(lc_fern_dark_pool, lc_long_sand_tongue, 'east')
    area.exit(lc_long_sand_tongue, lc_fern_dark_pool, 'west')
    area.exit(lc_long_sand_tongue, lc_inner_lagoon_shelf, 'east')
    area.exit(lc_inner_lagoon_shelf, lc_long_sand_tongue, 'west')
    area.exit(lc_inner_lagoon_shelf, lc_blue_crown_bend, 'east')
    area.exit(lc_blue_crown_bend, lc_inner_lagoon_shelf, 'west')
    area.exit(lc_blue_crown_bend, lc_last_lagoon_cairn, 'east')
    area.exit(lc_last_lagoon_cairn, lc_blue_crown_bend, 'west')
    area.exit(gc_humid_path_fork, rp_rain_pools, 'north')
    area.exit(rp_rain_pools, gc_humid_path_fork, 'south')
    area.exit(rp_pool_ridge_turn, bs_basalt_ring, 'north')
    area.exit(bs_basalt_ring, rp_pool_ridge_turn, 'south')
    area.exit(bs_quiet_black_center, hr_humid_ruin, 'north')
    area.exit(hr_humid_ruin, bs_quiet_black_center, 'south')
    area.exit(hr_last_humid_wall, lc_lagoon_crown_mouth, 'north')
    area.exit(lc_lagoon_crown_mouth, hr_last_humid_wall, 'south')
    area.exit(gc_korahei_track, 'korahei:lt_central_path', 'west')

    # NPCs
    _pathfinder = area.npc(gc_loop_stone, 'npc_central_pathfinder_inoa', faction='kauroran', dialogue={'greeting_tiers': {"neutral": 'Pathfinder Inoa studies you with open attention.'}, 'topics': {'help': 'Keeps routes honest where the isle repeats itself.', 'custom': 'Korahei expects guests to learn by helping, listening, and returning what they carry.'}, 'base_hints': ['help', 'custom']}, ambient={'idle_echoes': ['Pathfinder Inoa adjusts a small detail, making the place easier for the next person.'], 'idle_interval': 90, 'idle_variance': 30})
    _basalt_listener = area.npc(bs_center_listening_seat, 'npc_basalt_listener_safi', faction='kauroran', dialogue={'greeting_tiers': {"neutral": 'Basalt Listener Safi studies you with open attention.'}, 'topics': {'help': 'Studies old rings through practice, not revelation.', 'custom': 'Korahei expects guests to learn by helping, listening, and returning what they carry.'}, 'base_hints': ['help', 'custom']}, ambient={'idle_echoes': ['Basalt Listener Safi adjusts a small detail, making the place easier for the next person.'], 'idle_interval': 90, 'idle_variance': 30})
    _rain_keeper = area.npc(rp_rain_pools, 'npc_rain_pool_keeper_toma', faction='kauroran', dialogue={'greeting_tiers': {"neutral": 'Rain-Pool Keeper Toma studies you with open attention.'}, 'topics': {'help': 'Records water that arrives at inconvenient times.', 'custom': 'Korahei expects guests to learn by helping, listening, and returning what they carry.'}, 'base_hints': ['help', 'custom']}, ambient={'idle_echoes': ['Rain-Pool Keeper Toma adjusts a small detail, making the place easier for the next person.'], 'idle_interval': 90, 'idle_variance': 30})

    # Quest and delivery item templates
    area.quest(
        'central_q_loop_walk',
        name='Walk the Loop Twice',
        description='Inoa asks you to walk the central loop deliberately, turning odd terrain into learned orientation rather than random maze friction.',
        quest_type='exploration',
        quest_giver='npc_central_pathfinder_inoa',
        objectives=[{'type': 'investigate', 'target': 'gc_loop_stone', 'count': 1}, {'type': 'investigate', 'target': 'rp_rain_pools', 'count': 1}, {'type': 'investigate', 'target': 'bs_basalt_ring', 'count': 1}],
        rewards=[{'action_type': 'give_scales', 'amount': 32}, {'action_type': 'give_skill_xp', 'skill_id': 'scholarship', 'count': 10}],
        next_quest_id='central_q_basalt_listening',
        prerequisite_quests=['kiai_q_patient_steps'],
        can_share=True,
        consequence_small='Inoa scratches your double-walk marks beside the loop stone, turning confusion into a route lesson for later travelers.',
    )
    area.quest(
        'central_q_basalt_listening',
        name='Basalt Listening',
        description='Safi asks for basalt samples and careful observation, giving players node-adjacent mystery without explaining the impossible too early.',
        quest_type='gathering',
        quest_giver='npc_basalt_listener_safi',
        objectives=[{'type': 'collect', 'target': 'old_ring_basalt', 'count': 3}, {'type': 'investigate', 'target': 'bs_basalt_ring', 'count': 1}, {'type': 'talk_to', 'target': 'npc_rain_pool_keeper_toma', 'count': 1}],
        rewards=[{'action_type': 'give_scales', 'amount': 34}, {'action_type': 'give_skill_xp', 'skill_id': 'mining', 'count': 10}],
        next_quest_id=None,
        prerequisite_quests=['central_q_loop_walk'],
        can_share=True,
        consequence_small='Safi shelves your basalt notes with the samples, preserving mystery while making the old ring easier to study responsibly.',
    )
    area.quest(
        'central_q_rain_without_clouds',
        name='Rain Without Clouds',
        description="Toma has you compare rain pools and lagoon water so the isle's strangeness feels trackable, not decorative.",
        quest_type='exploration',
        quest_giver='npc_rain_pool_keeper_toma',
        objectives=[{'type': 'investigate', 'target': 'rp_clear_sky_ripple', 'count': 1}, {'type': 'investigate', 'target': 'lc_green_blue_step', 'count': 1}, {'type': 'collect', 'target': 'sunleaf', 'count': 2}],
        rewards=[{'action_type': 'give_scales', 'amount': 30}, {'action_type': 'give_skill_xp', 'skill_id': 'herbalism', 'count': 8}],
        next_quest_id=None,
        prerequisite_quests=[],
        can_share=True,
        consequence_small='Toma labels the cloudless-rain comparison in the pool ledger, giving the isle one more honest pattern to watch.',
    )

    # Spawns
    area.spawn(bs_tortoise_grazing_edge, 'basalt_tortoise', count_min=1, count_max=2, respawn_minutes=18)
    area.spawn(bs_cool_center_stone, 'basalt_tortoise', count_min=1, count_max=2, respawn_minutes=18)
    area.spawn(bs_stone_warm_hollow, 'basalt_tortoise', count_min=1, count_max=2, respawn_minutes=18)
    area.spawn(lc_shore_track_bar, 'shore_drake', count_min=1, count_max=1, respawn_minutes=18)
    area.spawn(lc_reed_warm_edge, 'shore_drake', count_min=1, count_max=1, respawn_minutes=18)
    area.spawn(lc_inner_lagoon_shelf, 'tideback_lizard', count_min=1, count_max=2, respawn_minutes=18)
    area.spawn(rp_silent_frog_bank, 'ring_moth_swarm', count_min=1, count_max=2, respawn_minutes=18)
    area.spawn(rp_singing_water_edge, 'ring_moth_swarm', count_min=1, count_max=2, respawn_minutes=18)
    area.spawn(rp_mist_breath_hollow, 'ring_moth_swarm', count_min=1, count_max=2, respawn_minutes=18)
    area.spawn(gc_soft_mud_print, 'tideback_lizard', count_min=1, count_max=2, respawn_minutes=18)
    area.spawn(gc_mossy_cause_rail, 'tideback_lizard', count_min=1, count_max=2, respawn_minutes=18)
    area.spawn(gc_warm_fern_run, 'ring_moth_swarm', count_min=1, count_max=2, respawn_minutes=18)

    # Gathering pools
    area.gathering_pool('fish', ['lc_hanging_fern_fish', 'rp_pale_fish_bowl'], ['reef_silverjack', 'tide_eel'], max_active=3, respawn_minutes=12)
    area.gathering_pool('forage', ['lc_saltfruit_root_bank', 'gc_kelp_scented_shade'], ['saltfruit', 'hearthroot'], max_active=3, respawn_minutes=12)
    area.gathering_pool('herb', ['rp_tide_mint_bowl', 'gc_warm_fern_run'], ['sunleaf'], max_active=3, respawn_minutes=12)
    area.gathering_pool('ore', ['bs_marked_basalt_face', 'bs_basalt_dust_pocket'], ['old_ring_basalt'], max_active=3, respawn_minutes=12)
    area.gathering_pool('hide', ['lc_shore_track_bar', 'bs_tortoise_grazing_edge'], ['shore_drake_hide'], max_active=3, respawn_minutes=12)
    area.gathering_pool('wood', ['gc_palm_root_arc', 'lc_palm_loop_bank'], ['circle_bamboo'], max_active=3, respawn_minutes=12)

    area.node(
        bs_basalt_ring,
        radius=6,
        lore_fragments=['central_isle_lore_001', 'central_isle_lore_002'],
        layer_1_overrides={
            'bs_basalt_ring': {
                'name': 'Basalt Ring Under Sudden Rain',
                'desc': 'Rain beads on the basalt while the sky remains bright. The ring feels carefully measured, but it explains nothing by itself.',
            },
        },
    )

    return area.build()
