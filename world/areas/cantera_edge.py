"""
Cantera Edge -- Ancient Forest Starter Zone

Dense, ancient forest west of Vael's Crossing at the base of The Reth.
Northwestern Varath. "Cantera" means quarry -- a place where things are
extracted. The world's most important secret was first extracted from
this forest.

This is the NODE ZONE. An active resonance node sits deep in the forest's
heart, its ancient magic humming through root systems and standing stones.
When the node fails, ~20 rooms near the center transform into Layer 1
corrupted versions -- twisted, alien, almost unrecognizable.

100+ rooms across 5 regions, 5 base mob types, 3 corrupted L1 variants,
1 named mob, 3 field NPCs, harvestable materials, lore fragments.
No levels -- zone scaling makes all content universal.

Regions:
    1. Forest Edge       (~20 rooms) -- Cantera Trail approach, lighter woods
    2. Deep Cantera      (~25 rooms) -- Dense old-growth, spider territory
    3. The Bone Hollows  (~20 rooms) -- Pala tree groves, eerie atmosphere
    4. Root Caves        (~15 rooms) -- Underground passages beneath ancient trees
    5. The Resonance     (~25 rooms) -- Node center, standing stones, corruption
"""

from world.area_builder import AreaBuilder


def build():
    area = AreaBuilder("cantera_edge")

    # ------------------------------------------------------------------
    # Zone setup
    # ------------------------------------------------------------------
    area.zone(
        name="The Cantera Edge",
        zone_type="ancient_forest",
        continent="varath",
        faction_territory="contested",
        has_node=True,
        node_type="resonance",
        node_failure_start=0,
        world_x=-60,
        world_y=0,
        world_radius=60,
    )

    # ==================================================================
    #  REGION 1: FOREST EDGE (~20 rooms)
    #  Transition from plains to forest. Cantera Trail from Vael's
    #  Crossing enters here. Lighter canopy, wider paths, some wildlife.
    # ==================================================================

    fe_trailhead = area.room(
        "fe_trailhead",
        name="Cantera Trail - Forest Approach",
        desc=(
            "The narrow trail from Vael's Crossing ends at a wall of "
            "ancient trees. The canopy closes overhead like a vault door, "
            "cutting the Ashreach sunlight to a green-gold twilight. Roots "
            "thick as a man's torso arch across the path. The air changes "
            "here -- heavier, older, carrying the scent of wet bark and "
            "something faintly metallic. A weathered trail marker leans "
            "drunkenly against a moss-covered boulder."
        ),
        room_type="path",
        indoor=False,
        ambient_echoes=[
            "Something rustles in the underbrush just out of sight.",
            "A Pala tree's bone-white branches click overhead like distant wind chimes.",
            "The metallic scent grows stronger for a moment, then fades.",
        ],
    )

    fe_wide_path = area.room(
        "fe_wide_path",
        name="Wide Forest Path",
        desc=(
            "An old wagon track cuts through the forest, wide enough for "
            "two carts abreast. Deep ruts filled with dark water suggest "
            "it once saw heavy traffic -- timber wagons, perhaps, or "
            "quarry carts. Now the forest is reclaiming it, saplings "
            "pushing through the packed earth. Ferns crowd the margins."
        ),
        room_type="path",
        indoor=False,
    )

    fe_fern_glade = area.room(
        "fe_fern_glade",
        name="Fern Glade",
        desc=(
            "A natural clearing where the canopy thins enough for sunlight "
            "to reach the forest floor. Waist-high ferns blanket the ground "
            "in cascading green waves. Small blue flowers dot the fern "
            "fronds -- nightcaps, the herbalists call them, which bloom "
            "even in deep shade. A fallen log spans the clearing, its bark "
            "peeled away to reveal pale, fibrous wood underneath."
        ),
        room_type="clearing",
        indoor=False,
        ambient_echoes=[
            "A woodpecker hammers at a distant trunk -- rapid, insistent.",
            "The ferns rustle as something small moves through them.",
        ],
    )

    fe_mossy_bend = area.room(
        "fe_mossy_bend",
        name="Mossy Bend",
        desc=(
            "The path curves around an enormous boulder draped in thick "
            "moss. Water seeps from a crack in the stone, tracing dark "
            "lines down to a muddy puddle below. Boot prints in the mud "
            "suggest others pass this way, though the prints look days old. "
            "The trees press close on all sides."
        ),
        room_type="path",
        indoor=False,
    )

    fe_hunter_blind = area.room(
        "fe_hunter_blind",
        name="Hunter's Blind",
        desc=(
            "A crude platform of lashed branches sits wedged between three "
            "trees, about ten feet off the ground. A knotted rope dangles "
            "from the edge. Below, scattered bones and old fire rings mark "
            "this as a regular camp for forest hunters. A wooden rack holds "
            "strips of dried meat -- some fresh, some blackened with age."
        ),
        room_type="clearing",
        indoor=False,
        crafting_stations=["campfire"],
    )

    fe_split_oak = area.room(
        "fe_split_oak",
        name="The Split Oak",
        desc=(
            "A massive oak tree stands at a fork in the path, its trunk "
            "split cleanly down the middle by some ancient force -- "
            "lightning, perhaps, or something stranger. Both halves still "
            "live, reaching skyward in a V shape that frames a patch of "
            "grey sky. Travelers have hammered iron nails into the exposed "
            "heartwood for luck. Hundreds of them, rusted to orange stubs."
        ),
        room_type="path",
        indoor=False,
        ambient_echoes=[
            "Wind whistles through the split trunk, an eerie two-toned note.",
            "A nail falls from the oak and plinks against a root.",
        ],
    )

    fe_bramble_path = area.room(
        "fe_bramble_path",
        name="Bramble Path",
        desc=(
            "Thorny brambles crowd the narrow path from both sides, their "
            "barbed runners snagging at clothes and skin. Dark berries "
            "cluster among the thorns -- edible but bitter, the kind "
            "that stain fingers for days. The air is thick with insects "
            "that hover in shafts of green-filtered light."
        ),
        room_type="path",
        indoor=False,
    )

    fe_old_bridge = area.room(
        "fe_old_bridge",
        name="Old Stone Bridge",
        desc=(
            "A single-arch stone bridge spans a shallow creek that cuts "
            "through the forest floor. The stonework is old -- Imperial "
            "by design but predating any settlement in this region by "
            "centuries. The creek runs brown and sluggish beneath, its "
            "bed littered with fallen leaves turned to dark silt. Carved "
            "marks on the bridge rail might be tally marks or something "
            "older."
        ),
        room_type="path",
        indoor=False,
    )

    fe_creek_bank = area.room(
        "fe_creek_bank",
        name="Creek Bank",
        desc=(
            "The creek widens here into a shallow pool where the water "
            "slows and clears. Smooth stones line the bottom, visible "
            "through the amber-tinted water. Dragonflies skim the surface. "
            "The bank is muddy and tracked with animal prints -- deer, "
            "boar, and something larger with clawed toes."
        ),
        room_type="clearing",
        indoor=False,
    )

    fe_birch_stand = area.room(
        "fe_birch_stand",
        name="Birch Stand",
        desc=(
            "A grove of silver birch trees stands apart from the darker "
            "oaks and pines, their white bark peeling in papery curls. "
            "The light is brighter here, the canopy thinner. The ground "
            "is carpeted with small yellow leaves that crunch underfoot. "
            "Someone has carved initials into one trunk -- old enough "
            "that the bark has nearly grown over them."
        ),
        room_type="clearing",
        indoor=False,
    )

    fe_thicket = area.room(
        "fe_thicket",
        name="Dense Thicket",
        desc=(
            "The undergrowth becomes nearly impassable here, a wall of "
            "young growth fighting for light beneath the old canopy. "
            "Thin paths wind through where animals have forced passage. "
            "Visibility drops to a few yards in any direction. The sound "
            "of the forest seems amplified -- every snap and rustle "
            "magnified by the closeness."
        ),
        room_type="path",
        indoor=False,
    )

    fe_woodcutter_camp = area.room(
        "fe_woodcutter_camp",
        name="Abandoned Woodcutter's Camp",
        desc=(
            "A cleared patch of forest where stumps and wood chips testify "
            "to old logging operations. A canvas shelter, half-collapsed "
            "and green with mildew, leans against a stack of rotting "
            "timber. Rusted saw blades and a broken axe head lie in the "
            "weeds. Whatever drove the woodcutters away, they left in "
            "a hurry -- personal effects still scatter the ground."
        ),
        room_type="clearing",
        indoor=False,
    )

    fe_south_ridge = area.room(
        "fe_south_ridge",
        name="Southern Ridge",
        desc=(
            "The ground rises along a low ridge that runs roughly east-west, "
            "offering glimpses through gaps in the canopy. To the south, "
            "the brown expanse of the Ashreach plains shimmers in heat "
            "haze. To the north, the forest darkens as the canopy thickens "
            "into the Deep Cantera. Exposed roots crisscross the ridge "
            "trail like tripwires."
        ),
        room_type="path",
        indoor=False,
    )

    fe_mushroom_hollow = area.room(
        "fe_mushroom_hollow",
        name="Mushroom Hollow",
        desc=(
            "A dip in the terrain collects moisture and dead leaves into "
            "a natural hollow where mushrooms thrive. Shelf fungi bracket "
            "the trunks of dead trees in ascending tiers. Toadstools "
            "with mottled caps push through the leaf litter in clusters. "
            "The air smells of rich decay -- not unpleasant but heavy, "
            "the smell of the forest recycling itself."
        ),
        room_type="clearing",
        indoor=False,
    )

    fe_deer_trail = area.room(
        "fe_deer_trail",
        name="Deer Trail",
        desc=(
            "A narrow track beaten into the forest floor by generations "
            "of deer. It winds between trees with the logic of animals -- "
            "avoiding thorns, following contours, skirting wet ground. "
            "Fresh droppings and a scuffed patch where a deer bedded "
            "down mark recent passage."
        ),
        room_type="path",
        indoor=False,
    )

    fe_warden_post = area.room(
        "fe_warden_post",
        name="Warden's Watch Post",
        desc=(
            "A small wooden platform built around the trunk of a tall "
            "pine, with a canvas awning and a rope ladder. Warden "
            "markings -- the green-and-brown chevron -- are carved into "
            "the railing. A battered journal hangs from a string, its "
            "pages warped by rain, recording wildlife sightings and "
            "patrol notes in cramped handwriting."
        ),
        room_type="clearing",
        indoor=False,
    )

    fe_tangle_roots = area.room(
        "fe_tangle_roots",
        name="Tangled Roots",
        desc=(
            "The roots of several ancient trees have grown together above "
            "ground, creating a knee-high maze of woody tendrils. Passage "
            "requires careful stepping and occasional climbing. Dark "
            "spaces between the roots harbor small creatures -- the "
            "skittering of insects and the gleam of tiny eyes are constant."
        ),
        room_type="path",
        indoor=False,
    )

    fe_owl_tree = area.room(
        "fe_owl_tree",
        name="The Owl Tree",
        desc=(
            "An enormous dead oak still stands, its hollow trunk home to "
            "generations of owls. Pellets and feathers litter the ground "
            "at its base. Despite being dead, the tree has a presence -- "
            "it towers above its living neighbors, branches spread like "
            "the fingers of a skeletal hand against the sky. At dusk, "
            "the owls emerge in silent pairs."
        ),
        room_type="clearing",
        indoor=False,
        ambient_echoes=[
            "An owl hoots from somewhere inside the hollow trunk.",
            "A pellet drops from above and lands with a soft thud.",
        ],
    )

    fe_south_plains_exit = area.room(
        "fe_south_plains_exit",
        name="Forest Edge - Plains Overlook",
        desc=(
            "The trees thin here at the southern boundary of the Cantera, "
            "giving way to scrub and then the open Ashreach. The transition "
            "is abrupt -- dense green canopy to brown dust in fifty paces. "
            "A game trail leads south toward the plains. The wind changes "
            "character at the tree line, carrying dry heat instead of the "
            "forest's perpetual dampness."
        ),
        room_type="path",
        indoor=False,
    )

    fe_north_descent = area.room(
        "fe_north_descent",
        name="Northward Descent",
        desc=(
            "The ridge drops away to the north into deeper forest. The "
            "trees here are older, their trunks wider, their canopy so "
            "thick that the forest floor lies in permanent twilight. A "
            "path -- more suggestion than track -- descends through a "
            "gap in the ridge. The air rising from below is noticeably "
            "cooler and carries a faint hum at the edge of hearing."
        ),
        room_type="path",
        indoor=False,
    )

    fe_vine_bridge = area.room(
        "fe_vine_bridge",
        name="Vine Bridge",
        desc=(
            "A natural bridge of woven vines and fallen branches spans "
            "a shallow ravine. The vines creak underfoot but hold firm. "
            "Below, a trickle of water runs between mossy stones. The "
            "bridge connects two ridgelines, offering passage deeper "
            "into the forest."
        ),
        room_type="path",
        indoor=False,
    )

    fe_fox_den = area.room(
        "fe_fox_den",
        name="Fox Den",
        desc=(
            "A sandy hollow beneath the exposed roots of an ancient oak "
            "serves as a den for forest foxes. Tufts of reddish fur "
            "cling to the root edges. Scattered bones from small prey "
            "litter the entrance. The den smells of musk and earth, "
            "warm and surprisingly pleasant."
        ),
        room_type="clearing",
        indoor=False,
    )

    fe_old_quarry = area.room(
        "fe_old_quarry",
        name="Old Quarry Pit",
        desc=(
            "A shallow depression where stone was once extracted from "
            "the earth. The quarry walls are overgrown with ivy and "
            "ferns, but tool marks are still visible on the exposed "
            "rock faces. The name Cantera -- quarry -- is literal here. "
            "Something was extracted from this forest long before timber."
        ),
        room_type="ruins",
        indoor=False,
    )

    # Region 1 Exits
    area.exit(fe_trailhead, fe_wide_path, "west")
    area.exit(fe_wide_path, fe_trailhead, "east")
    area.exit(fe_wide_path, fe_fern_glade, "north")
    area.exit(fe_fern_glade, fe_wide_path, "south")
    area.exit(fe_wide_path, fe_mossy_bend, "west")
    area.exit(fe_mossy_bend, fe_wide_path, "east")
    area.exit(fe_mossy_bend, fe_hunter_blind, "north")
    area.exit(fe_hunter_blind, fe_mossy_bend, "south")
    area.exit(fe_fern_glade, fe_split_oak, "north")
    area.exit(fe_split_oak, fe_fern_glade, "south")
    area.exit(fe_split_oak, fe_bramble_path, "west")
    area.exit(fe_bramble_path, fe_split_oak, "east")
    area.exit(fe_split_oak, fe_old_bridge, "north")
    area.exit(fe_old_bridge, fe_split_oak, "south")
    area.exit(fe_old_bridge, fe_creek_bank, "east")
    area.exit(fe_creek_bank, fe_old_bridge, "west")
    area.exit(fe_bramble_path, fe_birch_stand, "west")
    area.exit(fe_birch_stand, fe_bramble_path, "east")
    area.exit(fe_birch_stand, fe_thicket, "north")
    area.exit(fe_thicket, fe_birch_stand, "south")
    area.exit(fe_hunter_blind, fe_woodcutter_camp, "west")
    area.exit(fe_woodcutter_camp, fe_hunter_blind, "east")
    area.exit(fe_creek_bank, fe_south_ridge, "north")
    area.exit(fe_south_ridge, fe_creek_bank, "south")
    area.exit(fe_south_ridge, fe_mushroom_hollow, "west")
    area.exit(fe_mushroom_hollow, fe_south_ridge, "east")
    area.exit(fe_south_ridge, fe_deer_trail, "east")
    area.exit(fe_deer_trail, fe_south_ridge, "west")
    area.exit(fe_deer_trail, fe_warden_post, "north")
    area.exit(fe_warden_post, fe_deer_trail, "south")
    area.exit(fe_thicket, fe_tangle_roots, "north")
    area.exit(fe_tangle_roots, fe_thicket, "south")
    area.exit(fe_woodcutter_camp, fe_owl_tree, "north")
    area.exit(fe_owl_tree, fe_woodcutter_camp, "south")
    area.exit(fe_fern_glade, fe_south_plains_exit, "southeast")
    area.exit(fe_south_plains_exit, fe_fern_glade, "northwest")
    area.exit(fe_old_bridge, fe_north_descent, "north")
    area.exit(fe_north_descent, fe_old_bridge, "south")
    area.exit(fe_owl_tree, fe_vine_bridge, "west")
    area.exit(fe_vine_bridge, fe_owl_tree, "east")
    area.exit(fe_vine_bridge, fe_fox_den, "north")
    area.exit(fe_fox_den, fe_vine_bridge, "south")
    area.exit(fe_mushroom_hollow, fe_old_quarry, "north")
    area.exit(fe_old_quarry, fe_mushroom_hollow, "south")

    # Cross-zone exits from forest edge
    area.exit(fe_trailhead, "vaels_crossing:hg_west_road", "east",
              desc="The Cantera Trail leads east toward Vael's Crossing.")
    area.exit(fe_south_plains_exit, "ashreach_plains:ash_road_01", "south",
              desc="A game trail descends south into the Ashreach plains.")

    # Region 1 spawns
    area.spawn(fe_fern_glade, "wild_boar", count_min=1, count_max=1,
               respawn_minutes=15)
    area.spawn(fe_thicket, "vine_creeper", count_min=1, count_max=2,
               respawn_minutes=12, base_disposition=-0.3)
    area.spawn(fe_deer_trail, "wild_boar", count_min=1, count_max=1,
               respawn_minutes=15)
    area.spawn(fe_tangle_roots, "forest_spider", count_min=1, count_max=1,
               respawn_minutes=12)
    area.spawn(fe_bramble_path, "cantera_wolf", count_min=1, count_max=1,
               respawn_minutes=15)
    area.spawn(fe_woodcutter_camp, "forest_bandit", count_min=1, count_max=2,
               respawn_minutes=20, respawn_variance=5)
    area.spawn(fe_owl_tree, "cantera_wolf", count_min=1, count_max=1,
               respawn_minutes=15, wander=True)
    area.spawn(fe_mossy_bend, "wild_boar", count_min=1, count_max=1,
               respawn_minutes=15, wander=True)

    # Region 1 lore + materials
    area.lore_fragment("cantera_history_001", fe_woodcutter_camp,
        text=(
            "A woodcutter's journal, water-damaged but legible: "
            "'Third week. The saws dull faster here than anywhere else on the "
            "contract. Foreman says it is the sap -- amber-colored, thick as "
            "honey. It gums the blades. The trees do not want to be cut. I am "
            "starting to think he is right about that in ways he does not mean.'"
        ),
        discovery_method="search",
        insight_gain=5,
    )
    area.lore_fragment("cantera_history_002", fe_old_bridge,
        text=(
            "Carved into the bridge rail in blocky Imperial script: 'SURVEY "
            "MARKER XII-IV. CANTERA QUARRY ROAD. BY ORDER OF THE THIRD "
            "SURVEY COMMISSION.' Below it, scratched in a different hand: "
            "'They were not quarrying stone.'"
        ),
        discovery_method="search",
        insight_gain=5,
    )

    area.material("cantera_timber", tier=1, terrain="forest",
                  absorbed_property="resonance")
    area.material("nightcap_mushroom", tier=1, terrain="forest")
    area.material("bramble_berry", tier=1, terrain="forest")

    # ==================================================================
    #  REGION 2: DEEP CANTERA (~25 rooms)
    #  Dense old-growth forest. Spider territory. Darker, quieter.
    #  The trees are enormous and ancient.
    # ==================================================================

    dc_canopy_tunnel = area.room(
        "dc_canopy_tunnel",
        name="Canopy Tunnel",
        desc=(
            "The canopy closes completely overhead, the interlocking "
            "branches of ancient oaks forming a green tunnel that blocks "
            "all direct sunlight. The air is still and cool. Moss hangs "
            "from every surface in pale curtains. The path narrows to "
            "single file, hemmed in by buttress roots taller than a man."
        ),
        room_type="path",
        indoor=False,
    )

    dc_webbed_clearing = area.room(
        "dc_webbed_clearing",
        name="Webbed Clearing",
        desc=(
            "Thick ropes of spider silk stretch between the trees in "
            "overlapping sheets, turning this clearing into a silk-walled "
            "chamber. Dew drops catch what little light filters through, "
            "making the webs glitter. Wrapped bundles hang from the higher "
            "strands -- deer, birds, things too decomposed to identify. "
            "The ground is littered with old silk and small bones."
        ),
        room_type="clearing",
        indoor=False,
        ambient_echoes=[
            "Something large moves in the web overhead -- a vibration more felt than heard.",
            "A wrapped bundle shifts, settling under its own weight.",
        ],
    )

    dc_fallen_giant = area.room(
        "dc_fallen_giant",
        name="The Fallen Giant",
        desc=(
            "A tree of staggering size has fallen across the forest floor, "
            "its trunk easily fifteen feet in diameter. The root ball, torn "
            "from the earth, stands like a wall of dirt and stone twice "
            "a man's height. The gap in the canopy left by its fall has "
            "created a pocket of light where ferns and young trees compete "
            "furiously for the sun. The fallen trunk is slowly being "
            "consumed by bracket fungi and moss."
        ),
        room_type="clearing",
        indoor=False,
    )

    dc_spider_nest = area.room(
        "dc_spider_nest",
        name="Spider's Nest",
        desc=(
            "The webs here are older and thicker, layered over years into "
            "a solid silk canopy beneath the tree canopy. The ground is "
            "carpeted with shed exoskeletons and the desiccated husks of "
            "prey. Multiple tunnels of webbing lead deeper into the nest "
            "complex. The silk has a faintly sweet, sickly smell."
        ),
        room_type="clearing",
        indoor=False,
    )

    dc_ancient_stump = area.room(
        "dc_ancient_stump",
        name="Ancient Stump",
        desc=(
            "The stump of some impossibly ancient tree remains here, "
            "easily twenty feet across. Whatever felled it did so long "
            "ago that the stump has become its own ecosystem -- ferns "
            "grow from its center, mushrooms ring its base, and small "
            "trees have taken root in the rotting wood. The rings visible "
            "on the cut face number in the thousands."
        ),
        room_type="clearing",
        indoor=False,
    )

    dc_dark_hollow = area.room(
        "dc_dark_hollow",
        name="Dark Hollow",
        desc=(
            "The terrain dips into a shallow depression where the darkness "
            "is almost absolute. The leaf litter is deep and soft here, "
            "swallowing footfalls. Pale fungus grows on every surface, "
            "providing the faintest phosphorescent glow -- not enough to "
            "see by, just enough to make the darkness feel alive."
        ),
        room_type="path",
        indoor=False,
    )

    dc_root_arch = area.room(
        "dc_root_arch",
        name="Root Arch",
        desc=(
            "Two ancient trees have grown so close together that their "
            "roots have fused above ground, creating a natural archway "
            "tall enough to walk through. The inner surface of the arch "
            "is smooth and dark with age. Beyond it, the forest floor "
            "drops away into deeper terrain. There is something almost "
            "intentional about the arch's shape -- too regular for nature."
        ),
        room_type="path",
        indoor=False,
    )

    dc_moss_cathedral = area.room(
        "dc_moss_cathedral",
        name="Moss Cathedral",
        desc=(
            "The trees here are spaced like pillars in a vast hall, their "
            "trunks rising straight and branchless for sixty feet before "
            "the canopy begins. Moss covers everything in thick green "
            "velvet. Sound is absorbed by the moss -- footsteps vanish, "
            "voices carry strangely. The effect is of standing inside "
            "a living building that was never designed but grew into "
            "its purpose."
        ),
        room_type="clearing",
        indoor=False,
        ambient_echoes=[
            "A distant bird call arrives muffled and directionless.",
            "Water drips somewhere, each drop amplified by the silence.",
        ],
    )

    dc_boar_wallow = area.room(
        "dc_boar_wallow",
        name="Boar Wallow",
        desc=(
            "A muddy depression churned into chaos by wild boars. Tusk "
            "marks scar the bark of surrounding trees at knee height. "
            "The mud is black and deep, reeking of animal musk. Tracks "
            "radiate outward in all directions, and tufts of coarse "
            "bristle cling to rough bark where boars have scratched."
        ),
        room_type="clearing",
        indoor=False,
    )

    dc_vine_curtain = area.room(
        "dc_vine_curtain",
        name="Vine Curtain",
        desc=(
            "Thick vines hang from the canopy in dense curtains, some "
            "as thick as a wrist. They sway gently despite the lack "
            "of wind, as if responding to some subterranean rhythm. "
            "Pushing through them reveals narrow passages between the "
            "hanging green walls. Some vines have thorns; others are "
            "smooth and slick with sap."
        ),
        room_type="path",
        indoor=False,
    )

    dc_lichen_rocks = area.room(
        "dc_lichen_rocks",
        name="Lichen-Covered Rocks",
        desc=(
            "A tumble of large boulders protrudes from the forest floor, "
            "each one covered in crusty orange and grey lichen. The rocks "
            "are not native to this geology -- they were carried here by "
            "some ancient force, possibly glacial, possibly not. Between "
            "the rocks, narrow gaps lead to shadowy spaces underneath."
        ),
        room_type="path",
        indoor=False,
    )

    dc_fungal_garden = area.room(
        "dc_fungal_garden",
        name="Fungal Garden",
        desc=(
            "Every surface in this small clearing is colonized by fungi. "
            "Shelf brackets in brilliant orange and purple tier up tree "
            "trunks. Puffballs the size of skulls dot the ground. Tiny "
            "white mushrooms push through the bark of fallen logs in "
            "dense clusters. The air is thick with spores -- a golden "
            "haze visible in what little light penetrates."
        ),
        room_type="clearing",
        indoor=False,
    )

    dc_wolf_run = area.room(
        "dc_wolf_run",
        name="Wolf Run",
        desc=(
            "A narrow track beaten smooth by predators runs between dense "
            "underbrush. Fresh paw prints mark the soft earth -- large "
            "ones, bigger than a spread hand. The track runs straight "
            "and purposeful, connecting hunting grounds. Tufts of grey "
            "fur cling to thorny bushes at flank height."
        ),
        room_type="path",
        indoor=False,
    )

    dc_silent_pool = area.room(
        "dc_silent_pool",
        name="Silent Pool",
        desc=(
            "A perfectly still pool of dark water fills a shallow basin "
            "between tree roots. No insects skim its surface. No frogs "
            "call from its edges. The water reflects the canopy above "
            "with mirror clarity -- and in the reflection, the trees "
            "seem to have more branches than the real ones. The silence "
            "here is oppressive, unnatural."
        ),
        room_type="clearing",
        indoor=False,
        ambient_echoes=[
            "The water's surface ripples once, from the center outward, though nothing broke it.",
        ],
    )

    dc_thorn_maze = area.room(
        "dc_thorn_maze",
        name="Thorn Maze",
        desc=(
            "Hawthorn and blackthorn have woven themselves into an almost "
            "impenetrable barrier. Narrow passages barely wide enough to "
            "squeeze through wind between the thorny walls. Shredded "
            "cloth and animal hide on the thorns mark previous passages. "
            "The paths fork and dead-end unpredictably."
        ),
        room_type="path",
        indoor=False,
    )

    dc_charcoal_clearing = area.room(
        "dc_charcoal_clearing",
        name="Charcoal Clearing",
        desc=(
            "An old charcoal-burning site. The ground is still black "
            "underfoot, stained by years of slow fires. A collapsed "
            "earth kiln -- a mound of packed dirt with a chimney hole -- "
            "sits at the center. The trees around the clearing grew back "
            "smaller and denser than their neighbors, a ring of second "
            "growth surrounding the old wound."
        ),
        room_type="clearing",
        indoor=False,
    )

    dc_druid_marker = area.room(
        "dc_druid_marker",
        name="Druid's Marker Stone",
        desc=(
            "A standing stone, waist-high and rough-hewn, juts from the "
            "earth at the intersection of two game trails. Spiraling "
            "grooves have been carved into its surface -- druidic "
            "waymarks, old enough that lichen fills the deepest cuts. "
            "Someone has placed fresh wildflowers at its base. The stone "
            "feels warm to the touch, even in shade."
        ),
        room_type="clearing",
        indoor=False,
    )

    dc_canopy_break = area.room(
        "dc_canopy_break",
        name="Canopy Break",
        desc=(
            "A gap in the canopy allows a column of light to strike "
            "the forest floor, illuminating a circle of brilliant green "
            "growth surrounded by the usual twilight. The contrast is "
            "almost painful. Butterflies cluster in the light column, "
            "hundreds of them spiraling upward in a living helix."
        ),
        room_type="clearing",
        indoor=False,
    )

    dc_twisted_path = area.room(
        "dc_twisted_path",
        name="Twisted Path",
        desc=(
            "The path here twists between trees that have grown at strange "
            "angles, their trunks curved and spiraling as if warped by "
            "some invisible force. The effect is disorienting -- distances "
            "seem wrong, perspectives skewed. The trees are healthy "
            "despite their deformity, leaves green and bark intact."
        ),
        room_type="path",
        indoor=False,
    )

    dc_amber_seep = area.room(
        "dc_amber_seep",
        name="Amber Seep",
        desc=(
            "Thick amber-colored sap oozes from cuts in several nearby "
            "trees, pooling in hollows and hardening into glossy lumps. "
            "This is the famous Cantera amber -- prized by alchemists "
            "and reviled by woodcutters. The smell is resinous and sharp, "
            "almost medicinal. Insects trapped in the hardened pools "
            "are preserved in perfect detail."
        ),
        room_type="clearing",
        indoor=False,
    )

    dc_bandit_lookout = area.room(
        "dc_bandit_lookout",
        name="Bandit's Lookout",
        desc=(
            "A crude camp tucked between boulders and screened by dense "
            "brush. Bedrolls, a cold fire pit, and a rack of weapons "
            "mark it as a staging point for forest bandits. A rope ladder "
            "leads up to a platform in the trees above -- a lookout "
            "position with clear sightlines along the main path. Empty "
            "bottles and gnawed bones litter the ground."
        ),
        room_type="clearing",
        indoor=False,
    )

    dc_hollow_log = area.room(
        "dc_hollow_log",
        name="Hollow Log Passage",
        desc=(
            "A massive fallen tree lies across the path, but its center "
            "has rotted away, creating a tunnel large enough to walk "
            "through upright. The interior is smooth and dark, smelling "
            "of wet wood and earth. Faint scratch marks on the walls "
            "suggest animals use it as a den. Light glows at both ends."
        ),
        room_type="path",
        indoor=True,
    )

    dc_overgrown_ruin = area.room(
        "dc_overgrown_ruin",
        name="Overgrown Ruin",
        desc=(
            "Stone walls, barely knee-high, trace the outline of a "
            "structure long reclaimed by the forest. Trees grow through "
            "what was once a floor. Vines have pulled apart the masonry "
            "stone by stone. The building's purpose is unguessable -- "
            "too small for a house, wrong shape for a shrine. A rusted "
            "iron ring juts from one wall, still firmly set."
        ),
        room_type="ruins",
        indoor=False,
    )

    dc_south_approach = area.room(
        "dc_south_approach",
        name="Southern Approach",
        desc=(
            "The forest deepens perceptibly here. The trees are older, "
            "wider, their bark darker. The undergrowth thins as the "
            "canopy blocks more light -- less competition at ground "
            "level. The air carries a faint vibration, like standing "
            "near a bell that was struck minutes ago. Not sound exactly. "
            "Something felt in the bones."
        ),
        room_type="path",
        indoor=False,
    )

    # Region 2 Exits
    area.exit(fe_north_descent, dc_canopy_tunnel, "north")
    area.exit(dc_canopy_tunnel, fe_north_descent, "south")
    area.exit(dc_canopy_tunnel, dc_webbed_clearing, "west")
    area.exit(dc_webbed_clearing, dc_canopy_tunnel, "east")
    area.exit(dc_canopy_tunnel, dc_fallen_giant, "north")
    area.exit(dc_fallen_giant, dc_canopy_tunnel, "south")
    area.exit(dc_webbed_clearing, dc_spider_nest, "west")
    area.exit(dc_spider_nest, dc_webbed_clearing, "east")
    area.exit(dc_fallen_giant, dc_ancient_stump, "west")
    area.exit(dc_ancient_stump, dc_fallen_giant, "east")
    area.exit(dc_fallen_giant, dc_dark_hollow, "north")
    area.exit(dc_dark_hollow, dc_fallen_giant, "south")
    area.exit(dc_dark_hollow, dc_root_arch, "north")
    area.exit(dc_root_arch, dc_dark_hollow, "south")
    area.exit(dc_root_arch, dc_moss_cathedral, "west")
    area.exit(dc_moss_cathedral, dc_root_arch, "east")
    area.exit(dc_ancient_stump, dc_boar_wallow, "north")
    area.exit(dc_boar_wallow, dc_ancient_stump, "south")
    area.exit(dc_spider_nest, dc_vine_curtain, "north")
    area.exit(dc_vine_curtain, dc_spider_nest, "south")
    area.exit(dc_vine_curtain, dc_lichen_rocks, "west")
    area.exit(dc_lichen_rocks, dc_vine_curtain, "east")
    area.exit(dc_lichen_rocks, dc_fungal_garden, "north")
    area.exit(dc_fungal_garden, dc_lichen_rocks, "south")
    area.exit(dc_moss_cathedral, dc_wolf_run, "north")
    area.exit(dc_wolf_run, dc_moss_cathedral, "south")
    area.exit(dc_wolf_run, dc_silent_pool, "west")
    area.exit(dc_silent_pool, dc_wolf_run, "east")
    area.exit(dc_boar_wallow, dc_thorn_maze, "west")
    area.exit(dc_thorn_maze, dc_boar_wallow, "east")
    area.exit(dc_thorn_maze, dc_charcoal_clearing, "north")
    area.exit(dc_charcoal_clearing, dc_thorn_maze, "south")
    area.exit(dc_charcoal_clearing, dc_druid_marker, "west")
    area.exit(dc_druid_marker, dc_charcoal_clearing, "east")
    area.exit(dc_fungal_garden, dc_canopy_break, "west")
    area.exit(dc_canopy_break, dc_fungal_garden, "east")
    area.exit(dc_canopy_break, dc_twisted_path, "north")
    area.exit(dc_twisted_path, dc_canopy_break, "south")
    area.exit(dc_twisted_path, dc_amber_seep, "west")
    area.exit(dc_amber_seep, dc_twisted_path, "east")
    area.exit(dc_wolf_run, dc_bandit_lookout, "east")
    area.exit(dc_bandit_lookout, dc_wolf_run, "west")
    area.exit(dc_druid_marker, dc_hollow_log, "north")
    area.exit(dc_hollow_log, dc_druid_marker, "south")
    area.exit(dc_hollow_log, dc_overgrown_ruin, "north")
    area.exit(dc_overgrown_ruin, dc_hollow_log, "south")
    area.exit(dc_amber_seep, dc_south_approach, "north")
    area.exit(dc_south_approach, dc_amber_seep, "south")

    # Connect regions
    area.exit(fe_tangle_roots, dc_canopy_tunnel, "west")
    area.exit(dc_canopy_tunnel, fe_tangle_roots, "east")

    # Region 2 spawns
    area.spawn(dc_webbed_clearing, "forest_spider", count_min=1, count_max=2,
               respawn_minutes=12)
    area.spawn(dc_spider_nest, "forest_spider", count_min=2, count_max=3,
               respawn_minutes=10, respawn_variance=3)
    area.spawn(dc_dark_hollow, "vine_creeper", count_min=1, count_max=2,
               respawn_minutes=12, base_disposition=-0.3)
    area.spawn(dc_boar_wallow, "wild_boar", count_min=1, count_max=2,
               respawn_minutes=15)
    area.spawn(dc_wolf_run, "cantera_wolf", count_min=1, count_max=2,
               respawn_minutes=15)
    area.spawn(dc_vine_curtain, "vine_creeper", count_min=1, count_max=1,
               respawn_minutes=12, base_disposition=-0.3)
    area.spawn(dc_bandit_lookout, "forest_bandit", count_min=2, count_max=3,
               respawn_minutes=20, respawn_variance=5)
    area.spawn(dc_thorn_maze, "forest_spider", count_min=1, count_max=1,
               respawn_minutes=12, is_hunter=True, detection_range=3)
    area.spawn(dc_moss_cathedral, "cantera_wolf", count_min=1, count_max=1,
               respawn_minutes=15, wander=True)
    area.spawn(dc_charcoal_clearing, "wild_boar", count_min=1, count_max=1,
               respawn_minutes=15, wander=True)
    area.spawn(dc_silent_pool, "vine_creeper", count_min=1, count_max=1,
               respawn_minutes=12, base_disposition=-0.3)

    # Region 2 lore
    area.lore_fragment("cantera_druid_001", dc_druid_marker,
        text=(
            "The spiraling grooves on the marker stone are not decorative. "
            "Traced with a fingertip, they form a pattern that repeats "
            "every eight turns -- a mathematical relationship. Druids "
            "carved these, but the pattern predates druidic tradition "
            "by millennia. Someone taught it to them."
        ),
        discovery_method="search",
        scholar_path="remnance",
        insight_gain=10,
    )
    area.lore_fragment("cantera_amber_001", dc_amber_seep,
        text=(
            "The amber sap is warm. Not sun-warm -- warm from within, "
            "as if the tree's blood carries heat from deep underground. "
            "Alchemists prize it because it holds enchantment better "
            "than any mineral substrate. The trees are pulling something "
            "up from the earth. Something old."
        ),
        discovery_method="search",
        insight_gain=5,
    )

    area.material("cantera_amber", tier=2, terrain="forest",
                  absorbed_property="resonance")
    area.material("shelf_fungus", tier=1, terrain="forest")
    area.material("spider_silk", tier=2, terrain="forest")

    # ==================================================================
    #  REGION 3: THE BONE HOLLOWS (~20 rooms)
    #  Pala tree groves. Eerie atmosphere. Bone-white branches that
    #  click in the wind. Amber heartwood. Orange sap.
    # ==================================================================

    bh_pala_grove = area.room(
        "bh_pala_grove",
        name="Pala Grove - Outer Ring",
        desc=(
            "The first Pala trees appear here, unmistakable with their "
            "bone-white bark and branches that fork at sharp angles. "
            "The branches are bare of leaves, clicking against each other "
            "in a breeze that does not seem to touch the ground. Where "
            "the bark has been stripped, amber-gold heartwood shows "
            "beneath. Orange sap beads at every wound."
        ),
        room_type="clearing",
        indoor=False,
        ambient_echoes=[
            "The Pala branches click and rattle -- a sound like distant wind chimes made of bone.",
            "Orange sap drips from a branch and sizzles faintly when it hits the ground.",
        ],
    )

    bh_pala_heart = area.room(
        "bh_pala_heart",
        name="Heart of the Pala Grove",
        desc=(
            "The Pala trees grow thick here, their white trunks so close "
            "together that the grove feels like standing inside the ribcage "
            "of some enormous creature. The clicking of branches is "
            "constant, rhythmic, almost musical. The ground between "
            "the roots is carpeted with shards of shed bark, white and "
            "brittle as old paper. Orange sap pools in hollows and runs "
            "in thin streams between the roots."
        ),
        room_type="clearing",
        indoor=False,
    )

    bh_bone_arch = area.room(
        "bh_bone_arch",
        name="Bone Arch",
        desc=(
            "Two Pala trees have grown together overhead, their branches "
            "interlocking to form an arch of white wood. The effect is "
            "skeletal -- like walking through the jaws of a beast. "
            "Beyond the arch, the atmosphere shifts. The clicking stops "
            "for a heartbeat, then resumes in a different rhythm."
        ),
        room_type="path",
        indoor=False,
    )

    bh_sap_pool = area.room(
        "bh_sap_pool",
        name="Sap Pool",
        desc=(
            "A depression between Pala roots has filled with orange sap "
            "to form a shallow, viscous pool. The surface shimmers with "
            "an oily iridescence. Small insects are trapped at the edges, "
            "preserved in amber as they struggle. The sap is warm -- "
            "not hot, but blood-warm. It pulses. Slowly. Rhythmically."
        ),
        room_type="clearing",
        indoor=False,
        ambient_echoes=[
            "The sap pool pulses -- the surface rising and falling by a fraction.",
            "An insect lands on the sap and is pulled under without a sound.",
        ],
    )

    bh_white_path = area.room(
        "bh_white_path",
        name="White Path",
        desc=(
            "Shed Pala bark has accumulated so thickly on this path that "
            "the ground is entirely white, crunching underfoot like "
            "dried leaves. The effect is of walking through snow in a "
            "forest that has never seen winter. The bone-white trees "
            "and white ground create an achromatic landscape. Only the "
            "orange sap provides color."
        ),
        room_type="path",
        indoor=False,
    )

    bh_hollow_trunk = area.room(
        "bh_hollow_trunk",
        name="Hollow Pala Trunk",
        desc=(
            "The largest Pala tree in the grove has hollowed with age, "
            "its interior wide enough for two people to stand. The inner "
            "walls gleam with exposed heartwood -- amber-gold, faintly "
            "warm. Carved marks on the interior walls are very old. "
            "Not druidic. Not Imperial. The writing system is unknown."
        ),
        room_type="cave",
        indoor=True,
    )

    bh_clicking_ridge = area.room(
        "bh_clicking_ridge",
        name="Clicking Ridge",
        desc=(
            "The ridge here is crowned with Pala trees whose branches "
            "extend horizontally, creating a canopy of white lattice "
            "that clicks endlessly. The sound is layered -- deep knocks "
            "from the thick branches, lighter taps from the thin ones, "
            "and an occasional hollow boom when two trunks rub together. "
            "The ridge offers a view north into deeper, darker forest."
        ),
        room_type="path",
        indoor=False,
    )

    bh_root_tangle = area.room(
        "bh_root_tangle",
        name="Pala Root Tangle",
        desc=(
            "Pala roots have grown above ground in a complex lattice, "
            "white and smooth like bleached bone. Walking requires "
            "careful placement of each foot. Between the roots, small "
            "pools of orange sap collect. The sap glows faintly in "
            "shadow -- or seems to. It might be a trick of the light."
        ),
        room_type="path",
        indoor=False,
    )

    bh_wind_gap = area.room(
        "bh_wind_gap",
        name="Wind Gap",
        desc=(
            "A natural gap in the terrain funnels wind through the Pala "
            "grove, setting every branch in violent motion. The clicking "
            "becomes a roar here -- a cacophony of bone-white wood "
            "percussing against itself. The wind carries Pala bark "
            "fragments that sting exposed skin."
        ),
        room_type="path",
        indoor=False,
    )

    bh_fallen_pala = area.room(
        "bh_fallen_pala",
        name="Fallen Pala",
        desc=(
            "A Pala tree has fallen recently, its root ball still trailing "
            "dirt and orange sap. The heartwood exposed by the break is "
            "vivid amber, almost luminous. The surrounding trees seem to "
            "have leaned away from the gap, as if recoiling. The fallen "
            "trunk still seeps sap from the break point -- a slow, "
            "steady flow like a wound that will not close."
        ),
        room_type="clearing",
        indoor=False,
    )

    bh_shrine_stones = area.room(
        "bh_shrine_stones",
        name="Shrine Stones",
        desc=(
            "Eight flat stones, roughly equal in size, are arranged in "
            "a circle in a clearing between Pala trees. The arrangement "
            "is too regular to be natural. Each stone bears a single "
            "carved mark -- not letters, but abstract symbols. Eight "
            "stones, eight symbols. The Pala trees around the clearing "
            "grow in a ring that matches the stones' spacing exactly."
        ),
        room_type="ruins",
        indoor=False,
    )

    bh_sap_stream = area.room(
        "bh_sap_stream",
        name="Sap Stream",
        desc=(
            "A thin stream of orange sap flows along a channel between "
            "Pala roots, running downhill toward the deeper forest. The "
            "stream is only a few inches wide but perfectly defined, "
            "as if cut into the earth. It flows with the consistency of "
            "warm honey. Where it passes between two roots, it "
            "accelerates briefly and makes a sound like a whispered word."
        ),
        room_type="path",
        indoor=False,
    )

    bh_bark_cave = area.room(
        "bh_bark_cave",
        name="Bark Cave",
        desc=(
            "Accumulated shed Pala bark has formed a canopy over a "
            "depression, creating a natural cave of white bark plates "
            "layered like scales. The interior is dry and surprisingly "
            "warm. The bark walls flex slightly when touched. Animal "
            "droppings and a nest of dried grass suggest foxes or "
            "badgers shelter here."
        ),
        room_type="cave",
        indoor=True,
    )

    bh_cantera_overlook = area.room(
        "bh_cantera_overlook",
        name="Cantera Overlook",
        desc=(
            "The ridge reaches its highest point here, offering a rare "
            "view over the forest canopy. To the north, the trees darken "
            "and thicken toward the center of the Cantera. Somewhere in "
            "that darkness, faint points of light pulse irregularly -- "
            "not fireflies. Wrong color. Wrong rhythm. The Pala branches "
            "click softly, and the orange sap glows in the setting light."
        ),
        room_type="clearing",
        indoor=False,
    )

    bh_hermit_clearing = area.room(
        "bh_hermit_clearing",
        name="Hermit's Clearing",
        desc=(
            "A small clearing where a rough-hewn shelter of Pala wood "
            "and canvas leans against a living tree. A fire ring of "
            "blackened stones sits before the entrance, cold but recently "
            "used. Drying racks hold bundles of herbs. A circle of "
            "carved stones surrounds the camp -- druidic ward markers. "
            "Whoever lives here has been here a long time."
        ),
        room_type="clearing",
        indoor=False,
    )

    bh_north_descent = area.room(
        "bh_north_descent",
        name="Descent to the Resonance",
        desc=(
            "The Pala grove gives way to older, darker trees as the "
            "terrain drops north. The clicking of Pala branches fades, "
            "replaced by a deeper vibration that seems to come from the "
            "ground itself. The air is warmer here, and carries a faint "
            "metallic taste. The path leads down into the heart of the "
            "Cantera -- toward the source of the forest's strangeness."
        ),
        room_type="path",
        indoor=False,
    )

    # Region 3 Exits
    area.exit(dc_overgrown_ruin, bh_pala_grove, "west")
    area.exit(bh_pala_grove, dc_overgrown_ruin, "east")
    area.exit(bh_pala_grove, bh_pala_heart, "north")
    area.exit(bh_pala_heart, bh_pala_grove, "south")
    area.exit(bh_pala_heart, bh_bone_arch, "west")
    area.exit(bh_bone_arch, bh_pala_heart, "east")
    area.exit(bh_pala_heart, bh_sap_pool, "north")
    area.exit(bh_sap_pool, bh_pala_heart, "south")
    area.exit(bh_bone_arch, bh_white_path, "north")
    area.exit(bh_white_path, bh_bone_arch, "south")
    area.exit(bh_white_path, bh_hollow_trunk, "west")
    area.exit(bh_hollow_trunk, bh_white_path, "east")
    area.exit(bh_sap_pool, bh_clicking_ridge, "east")
    area.exit(bh_clicking_ridge, bh_sap_pool, "west")
    area.exit(bh_clicking_ridge, bh_root_tangle, "north")
    area.exit(bh_root_tangle, bh_clicking_ridge, "south")
    area.exit(bh_root_tangle, bh_wind_gap, "east")
    area.exit(bh_wind_gap, bh_root_tangle, "west")
    area.exit(bh_white_path, bh_fallen_pala, "north")
    area.exit(bh_fallen_pala, bh_white_path, "south")
    area.exit(bh_fallen_pala, bh_shrine_stones, "west")
    area.exit(bh_shrine_stones, bh_fallen_pala, "east")
    area.exit(bh_sap_pool, bh_sap_stream, "west")
    area.exit(bh_sap_stream, bh_sap_pool, "east")
    area.exit(bh_sap_stream, bh_bark_cave, "north")
    area.exit(bh_bark_cave, bh_sap_stream, "south")
    area.exit(bh_wind_gap, bh_cantera_overlook, "north")
    area.exit(bh_cantera_overlook, bh_wind_gap, "south")
    area.exit(bh_shrine_stones, bh_hermit_clearing, "north")
    area.exit(bh_hermit_clearing, bh_shrine_stones, "south")
    area.exit(bh_hermit_clearing, bh_north_descent, "north")
    area.exit(bh_north_descent, bh_hermit_clearing, "south")

    # Region 3 spawns
    area.spawn(bh_pala_grove, "cantera_wolf", count_min=1, count_max=1,
               respawn_minutes=15)
    area.spawn(bh_white_path, "wild_boar", count_min=1, count_max=1,
               respawn_minutes=15, wander=True)
    area.spawn(bh_root_tangle, "vine_creeper", count_min=1, count_max=2,
               respawn_minutes=12, base_disposition=-0.3)
    area.spawn(bh_wind_gap, "cantera_wolf", count_min=1, count_max=2,
               respawn_minutes=15)
    area.spawn(bh_bark_cave, "forest_spider", count_min=1, count_max=1,
               respawn_minutes=12)
    area.spawn(bh_sap_stream, "wild_boar", count_min=1, count_max=1,
               respawn_minutes=15)

    # Region 3 lore
    area.lore_fragment("cantera_pala_001", bh_hollow_trunk,
        text=(
            "The marks on the interior walls are not carved -- they are "
            "grown. The heartwood formed around shapes that were placed "
            "inside the tree centuries ago and absorbed. The symbols are "
            "three-dimensional, embedded in the wood at different depths. "
            "Eight distinct symbols. Always eight."
        ),
        discovery_method="search",
        scholar_path="remnance",
        insight_gain=15,
    )
    area.lore_fragment("cantera_shrine_001", bh_shrine_stones,
        text=(
            "The eight stones are carved from a material not found "
            "anywhere in the Cantera. Basalt, perhaps, from the coastal "
            "cliffs far to the northeast. Someone carried them here. "
            "The symbols on each are different but share a common "
            "structural element -- four strokes each, intersecting "
            "at a central point."
        ),
        discovery_method="search",
        scholar_path="remnance",
        insight_gain=10,
    )

    area.material("pala_bark", tier=2, terrain="forest",
                  absorbed_property="resonance")
    area.material("pala_sap", tier=3, terrain="forest",
                  absorbed_property="resonance")

    # ==================================================================
    #  REGION 4: ROOT CAVES (~15 rooms)
    #  Underground passages beneath ancient trees. Dark, damp,
    #  claustrophobic. Connects to the Resonance from below.
    # ==================================================================

    rc_entrance = area.room(
        "rc_entrance",
        name="Root Cave Entrance",
        desc=(
            "A gap between massive tree roots opens into darkness below. "
            "The opening is wide enough to squeeze through but not "
            "comfortably. Roots frame the entrance like ribs, and a "
            "musty exhalation of warm air rises from the depths. The "
            "tree above is enormous -- possibly the oldest in the "
            "forest. Its roots must extend for hundreds of feet."
        ),
        room_type="cave",
        indoor=True,
    )

    rc_root_passage = area.room(
        "rc_root_passage",
        name="Root Passage",
        desc=(
            "A narrow tunnel carved not by tools but by root growth and "
            "water. The ceiling is a lattice of thick roots, the walls "
            "packed earth veined with white rootlets. The floor is soft "
            "with accumulated humus and drips. The passage curves "
            "organically, following paths of least resistance."
        ),
        room_type="cave",
        indoor=True,
    )

    rc_drip_chamber = area.room(
        "rc_drip_chamber",
        name="Drip Chamber",
        desc=(
            "The passage opens into a small natural chamber where water "
            "drips steadily from root tips above. The drips echo in the "
            "enclosed space. Mineral deposits have built up beneath each "
            "drip point into small stalagmites of orange-tinted calcium. "
            "The orange color is unmistakable -- the same hue as Pala sap."
        ),
        room_type="cave",
        indoor=True,
    )

    rc_fungal_cavern = area.room(
        "rc_fungal_cavern",
        name="Fungal Cavern",
        desc=(
            "The tunnel widens into a cavern dominated by enormous "
            "mushrooms -- some taller than a man, their caps wide as "
            "shields. Bioluminescent species provide an eerie blue-green "
            "glow that makes shadows dance. The air is thick with spores "
            "and the sweet smell of decay. The mushrooms grow from root "
            "matter, feeding on the ancient trees above."
        ),
        room_type="cave",
        indoor=True,
        ambient_echoes=[
            "A mushroom cap releases a puff of spores that glow briefly in the dark.",
            "Water trickles somewhere deeper, the sound distorted by echoes.",
        ],
    )

    rc_root_nexus = area.room(
        "rc_root_nexus",
        name="Root Nexus",
        desc=(
            "Multiple root systems converge here from different trees "
            "above, their roots intertwining in a massive knot of wood "
            "and earth. The root knot pulses -- slowly, almost "
            "imperceptibly, but it pulses. The wood is warm to the touch. "
            "Sap seeps from fissures in the root mass, glowing faintly "
            "orange in the darkness."
        ),
        room_type="cave",
        indoor=True,
    )

    rc_narrow_squeeze = area.room(
        "rc_narrow_squeeze",
        name="Narrow Squeeze",
        desc=(
            "The passage narrows to a gap barely wide enough for a person "
            "to push through sideways. Roots press from above, earth "
            "from below. Claustrophobia is immediate and intense. Beyond "
            "the squeeze, the passage opens again, but the air is "
            "different -- warmer, charged with something like static."
        ),
        room_type="cave",
        indoor=True,
    )

    rc_bone_chamber = area.room(
        "rc_bone_chamber",
        name="Bone Chamber",
        desc=(
            "A small chamber where the walls are studded with bones -- "
            "animal bones, pushed into the earth by root growth over "
            "centuries. Skulls of deer and boar stare from the walls "
            "at odd angles. The forest buries its dead this way, "
            "pulling remains underground through root action. The "
            "effect is macabre but natural."
        ),
        room_type="cave",
        indoor=True,
    )

    rc_sap_river = area.room(
        "rc_sap_river",
        name="Underground Sap Flow",
        desc=(
            "A channel of liquid amber sap flows through a groove in "
            "the cave floor, moving steadily in one direction -- deeper. "
            "The sap glows with its own light here, casting everything "
            "in warm orange. The flow is not fast but relentless. The "
            "channel is worn smooth, suggesting this flow has run for "
            "a very long time. The air above it shimmers with heat."
        ),
        room_type="cave",
        indoor=True,
    )

    rc_echo_gallery = area.room(
        "rc_echo_gallery",
        name="Echo Gallery",
        desc=(
            "A long, narrow cavern where every sound echoes and re-echoes "
            "from wall to wall, multiplying into a chorus. A whisper "
            "becomes a conversation. A footstep becomes a march. The "
            "roots along the ceiling vibrate in sympathy, adding their "
            "own resonance to the echoes. The combined effect is "
            "unsettling -- the sound of an empty room that is not empty."
        ),
        room_type="cave",
        indoor=True,
    )

    rc_spider_den = area.room(
        "rc_spider_den",
        name="Spider Den",
        desc=(
            "A wide chamber coated in thick spider silk, glowing faintly "
            "in the bioluminescent light. Egg sacs hang from the ceiling "
            "in clusters. The silk underfoot is springy and treacherous. "
            "Dark shapes move at the edges of vision -- large ones, "
            "barely distinguishable from the shadows."
        ),
        room_type="cave",
        indoor=True,
    )

    rc_crystal_vein = area.room(
        "rc_crystal_vein",
        name="Crystal Vein",
        desc=(
            "A seam of pale crystals runs through the cave wall, exposed "
            "by a collapse that left rubble on the floor. The crystals "
            "are translucent, with an amber core that catches and holds "
            "the faint light. They vibrate when touched -- a barely "
            "perceptible buzz that travels up through the fingers. "
            "The crystal vein runs deeper, disappearing into solid rock."
        ),
        room_type="cave",
        indoor=True,
    )

    rc_deep_pool = area.room(
        "rc_deep_pool",
        name="Deep Pool",
        desc=(
            "A subterranean pool of still, dark water fills a natural "
            "basin. The water is cold and clear, reflecting the cave "
            "ceiling with unsettling fidelity. The pool has no visible "
            "source or outlet. Its surface is perfectly still. At certain "
            "angles, the reflection shows roots that are not on the "
            "ceiling above."
        ),
        room_type="cave",
        indoor=True,
    )

    rc_collapsed_tunnel = area.room(
        "rc_collapsed_tunnel",
        name="Collapsed Tunnel",
        desc=(
            "The passage here has partially collapsed, rubble and dirt "
            "reducing the ceiling to waist height. Crawling is necessary. "
            "The roots above are broken and bleeding sap that drips onto "
            "the crawling traveler. Beyond the collapse, the tunnel "
            "opens into something larger."
        ),
        room_type="cave",
        indoor=True,
    )

    rc_ascending_shaft = area.room(
        "rc_ascending_shaft",
        name="Ascending Shaft",
        desc=(
            "A vertical shaft rises through the earth, its walls "
            "spiraling with thick roots that serve as a natural ladder. "
            "Light -- faint, strange, pulsing -- filters down from "
            "above. The air rising through the shaft is warm and "
            "carries the resonance that pervades everything this deep "
            "in the Cantera. The roots vibrate gently, like guitar "
            "strings that were plucked hours ago."
        ),
        room_type="cave",
        indoor=True,
    )

    rc_reth_exit = area.room(
        "rc_reth_exit",
        name="Root Cave - Northern Opening",
        desc=(
            "The cave system opens through a crack in a rocky hillside, "
            "revealing the grey slopes of The Reth's foothills. Cold "
            "mountain air mixes with the warm cave exhalation. The "
            "terrain transitions rapidly from forest to rocky scree. "
            "A narrow path leads north into the foothills."
        ),
        room_type="cave",
        indoor=False,
    )

    # Region 4 Exits
    area.exit(dc_lichen_rocks, rc_entrance, "down")
    area.exit(rc_entrance, dc_lichen_rocks, "up")
    area.exit(rc_entrance, rc_root_passage, "north")
    area.exit(rc_root_passage, rc_entrance, "south")
    area.exit(rc_root_passage, rc_drip_chamber, "west")
    area.exit(rc_drip_chamber, rc_root_passage, "east")
    area.exit(rc_root_passage, rc_fungal_cavern, "north")
    area.exit(rc_fungal_cavern, rc_root_passage, "south")
    area.exit(rc_fungal_cavern, rc_root_nexus, "west")
    area.exit(rc_root_nexus, rc_fungal_cavern, "east")
    area.exit(rc_drip_chamber, rc_narrow_squeeze, "north")
    area.exit(rc_narrow_squeeze, rc_drip_chamber, "south")
    area.exit(rc_narrow_squeeze, rc_bone_chamber, "west")
    area.exit(rc_bone_chamber, rc_narrow_squeeze, "east")
    area.exit(rc_root_nexus, rc_sap_river, "north")
    area.exit(rc_sap_river, rc_root_nexus, "south")
    area.exit(rc_sap_river, rc_echo_gallery, "west")
    area.exit(rc_echo_gallery, rc_sap_river, "east")
    area.exit(rc_fungal_cavern, rc_spider_den, "east")
    area.exit(rc_spider_den, rc_fungal_cavern, "west")
    area.exit(rc_echo_gallery, rc_crystal_vein, "north")
    area.exit(rc_crystal_vein, rc_echo_gallery, "south")
    area.exit(rc_bone_chamber, rc_deep_pool, "north")
    area.exit(rc_deep_pool, rc_bone_chamber, "south")
    area.exit(rc_deep_pool, rc_collapsed_tunnel, "west")
    area.exit(rc_collapsed_tunnel, rc_deep_pool, "east")
    area.exit(rc_crystal_vein, rc_ascending_shaft, "up")
    area.exit(rc_ascending_shaft, rc_crystal_vein, "down")
    area.exit(rc_collapsed_tunnel, rc_reth_exit, "north")
    area.exit(rc_reth_exit, rc_collapsed_tunnel, "south")

    # Cross-zone exit to Reth foothills
    area.exit(rc_reth_exit, "reth_foothills:cn_mouth", "north",
              desc="A narrow path climbs north into the foothills of The Reth.")

    # Region 4 spawns
    area.spawn(rc_spider_den, "forest_spider", count_min=2, count_max=3,
               respawn_minutes=10, respawn_variance=3)
    area.spawn(rc_fungal_cavern, "vine_creeper", count_min=1, count_max=1,
               respawn_minutes=12, base_disposition=-0.3)
    area.spawn(rc_bone_chamber, "forest_spider", count_min=1, count_max=1,
               respawn_minutes=12)
    area.spawn(rc_echo_gallery, "vine_creeper", count_min=1, count_max=1,
               respawn_minutes=12, base_disposition=-0.3)

    # Region 4 lore
    area.lore_fragment("cantera_crystal_001", rc_crystal_vein,
        text=(
            "The crystals vibrate at a frequency that changes throughout "
            "the day -- faster at dawn and dusk, slower at noon and "
            "midnight. The cycle is not solar. It is a harmonic of "
            "something deeper. An alchemist with resonance-tuned "
            "instruments could map it. The pattern would have eight "
            "nodes."
        ),
        discovery_method="search",
        scholar_path="remnance",
        insight_gain=15,
    )

    area.material("cave_mushroom", tier=1, terrain="cave")
    area.material("resonance_crystal", tier=3, terrain="cave",
                  absorbed_property="resonance")

    # ==================================================================
    #  REGION 5: THE RESONANCE (~25 rooms)
    #  Node center. Standing stones. Ancient magic. The heart of the
    #  forest's strangeness. ~20 rooms here get Layer 1 overrides.
    # ==================================================================

    rs_outer_ring = area.room(
        "rs_outer_ring",
        name="Resonance - Outer Ring",
        desc=(
            "The trees thin here, not from logging but from an unseen "
            "force that stunts growth. They are shorter, gnarled, their "
            "bark cracked and weeping sap. The ground vibrates constantly -- "
            "not enough to stumble, but enough to feel in the teeth. "
            "Patches of moss glow faintly in no particular pattern."
        ),
        room_type="clearing",
        indoor=False,
    )

    rs_humming_path = area.room(
        "rs_humming_path",
        name="Humming Path",
        desc=(
            "The path thrums underfoot with a deep vibration that rises "
            "and falls in slow waves. The trees here lean away from the "
            "center as if pushed by a constant wind, though the air is "
            "still. Small stones on the path rattle and shift. Leaves "
            "that fall from the canopy spiral in ways that defy the "
            "expected physics."
        ),
        room_type="path",
        indoor=False,
    )

    rs_warped_grove = area.room(
        "rs_warped_grove",
        name="Warped Grove",
        desc=(
            "The trees here have grown into impossible shapes -- spirals, "
            "right angles, perfect arcs. One trunk bends into a complete "
            "loop before continuing upward. The branches reach inward "
            "instead of outward, forming a canopy that funnels toward "
            "the center rather than spreading to catch light. The wood "
            "is alive but transformed."
        ),
        room_type="clearing",
        indoor=False,
    )

    rs_standing_stones = area.room(
        "rs_standing_stones",
        name="Standing Stones",
        desc=(
            "Eight tall stones stand in a circle, each roughly twelve "
            "feet high and carved from different materials. Granite, "
            "basalt, marble, sandstone -- no two alike. Each stone bears "
            "deeply carved symbols in the same unknown script found in "
            "the Pala trunk. The stones hum. Not metaphorically. They "
            "produce a bass note at the threshold of hearing, felt more "
            "than heard, and the note changes when you move between them."
        ),
        room_type="ruins",
        indoor=False,
        ambient_echoes=[
            "The standing stones shift pitch -- the hum deepens, then rises.",
            "Dust motes between the stones move in geometric patterns.",
            "The air between two stones shimmers briefly, like heat haze.",
        ],
    )

    rs_node_center = area.room(
        "rs_node_center",
        name="The Resonance Heart",
        desc=(
            "The center of the stone circle. The ground here is bare "
            "earth, hard-packed and warm. Nothing grows. A flat stone "
            "disc is set flush with the ground, its surface covered in "
            "concentric rings of carved symbols. The disc is warm -- "
            "almost hot. The vibration is strongest here, a bone-deep "
            "thrumming that makes vision blur at the edges. The air "
            "tastes of copper and ozone. This is the heart of the "
            "Cantera's ancient power, and it is not stable."
        ),
        room_type="node_center",
        indoor=False,
        ambient_echoes=[
            "The stone disc pulses with heat -- the rings seem to shift.",
            "Reality stutters -- for a heartbeat, the forest is different. Then it is not.",
            "The copper taste intensifies and the stones' hum rises to an audible note.",
        ],
    )

    rs_crystal_garden = area.room(
        "rs_crystal_garden",
        name="Crystal Garden",
        desc=(
            "Crystals push through the earth like plants in this small "
            "clearing. They range from finger-sized to arm-length, "
            "translucent amber shot through with veins of darker material. "
            "The crystals sing -- a chorus of high, thin notes that "
            "harmonize with the deeper vibration of the node. Touch one "
            "and the note changes. Touch another and the harmony shifts."
        ),
        room_type="clearing",
        indoor=False,
    )

    rs_sap_convergence = area.room(
        "rs_sap_convergence",
        name="Sap Convergence",
        desc=(
            "Multiple streams of orange sap converge here from different "
            "directions, joining into a single flow that sinks into the "
            "earth through a natural drain. The combined sap glows "
            "brightly -- bright enough to read by. The heat it generates "
            "makes the surrounding air shimmer. The flow pattern is "
            "complex, almost mathematical."
        ),
        room_type="clearing",
        indoor=False,
    )

    rs_echo_stones = area.room(
        "rs_echo_stones",
        name="Echo Stones",
        desc=(
            "Smaller stones, knee-high, are scattered in no apparent "
            "pattern around the periphery of the node. Each one echoes "
            "sounds differently -- speak near one and it returns your "
            "words in a lower register. Speak near another and the echo "
            "arrives before the original word finishes. The stones are "
            "carved with single symbols. Eight different symbols."
        ),
        room_type="clearing",
        indoor=False,
    )

    rs_twisted_approach = area.room(
        "rs_twisted_approach",
        name="Twisted Approach",
        desc=(
            "The path to the node center passes through an area where "
            "spatial relationships have become unreliable. Distances seem "
            "to change. A tree that was three steps away is suddenly ten. "
            "The ground rises and falls in waves that are not visible -- "
            "only felt. The effect intensifies closer to the center."
        ),
        room_type="path",
        indoor=False,
    )

    rs_amber_pool = area.room(
        "rs_amber_pool",
        name="Amber Pool",
        desc=(
            "A wide, shallow pool of liquid amber fills a depression. "
            "The amber is clear and warm, glowing from within. Objects "
            "beneath its surface are visible -- roots, stones, and "
            "something deeper that might be carved stone. The pool "
            "does not ripple. Its surface is glass-smooth. The heat "
            "rising from it is substantial."
        ),
        room_type="clearing",
        indoor=False,
    )

    rs_broken_pillar = area.room(
        "rs_broken_pillar",
        name="Broken Pillar",
        desc=(
            "The stump of a stone pillar protrudes from the earth, "
            "broken off about four feet up. The stone matches none "
            "of the standing stones but shares their carved symbols. "
            "The break is old -- centuries, maybe longer. Whatever "
            "shattered it left scorch marks on the remaining stump "
            "that glow faintly in dim light."
        ),
        room_type="ruins",
        indoor=False,
    )

    rs_moss_terrace = area.room(
        "rs_moss_terrace",
        name="Moss Terrace",
        desc=(
            "A series of natural terraces, each a few feet higher than "
            "the last, carpeted in thick, luminous moss. The moss glows "
            "a pale blue-green, intensifying near the node center. The "
            "terraces might be natural or might be eroded steps -- "
            "impossible to tell after so many centuries of growth. The "
            "vibration here causes the moss to pulse rhythmically."
        ),
        room_type="clearing",
        indoor=False,
    )

    rs_singing_trees = area.room(
        "rs_singing_trees",
        name="Singing Trees",
        desc=(
            "Three trees stand in a tight triangle, their trunks "
            "perfectly equidistant. The trees produce sound -- a "
            "continuous, modulating tone that changes pitch as the "
            "wind shifts. But there is no wind. The sound comes from "
            "the wood itself, vibrating in resonance with the node. "
            "Each tree sings a different note. Together they form "
            "a chord that is nearly, but not quite, harmonious."
        ),
        room_type="clearing",
        indoor=False,
    )

    rs_collapsed_arch = area.room(
        "rs_collapsed_arch",
        name="Collapsed Arch",
        desc=(
            "A stone archway has partially collapsed, its keystone "
            "fallen and split. The arch was carved from a single block "
            "of dark stone, its inner surface inscribed with symbols "
            "that match the standing stones. The collapse exposed "
            "the interior -- hollow, with channels cut into the stone "
            "that once carried something. Sap fills them now."
        ),
        room_type="ruins",
        indoor=False,
    )

    rs_vine_hollow = area.room(
        "rs_vine_hollow",
        name="Vine Hollow",
        desc=(
            "A hollow in the earth, perhaps ten feet deep, carpeted with "
            "vines that pulse with a faint inner light. The vines are "
            "thick and warm, covered in fine hairs that cling to skin. "
            "At the bottom of the hollow, the vines converge on a point "
            "directly above a buried stone. The vines grow from the "
            "stone, feeding on whatever it contains."
        ),
        room_type="clearing",
        indoor=False,
    )

    rs_thermal_vent = area.room(
        "rs_thermal_vent",
        name="Thermal Vent",
        desc=(
            "A crack in the earth vents warm, mineral-laden air from "
            "below. The temperature near the vent is noticeably higher "
            "than the surrounding forest. The air shimmers and carries "
            "the smell of hot stone and copper. Plants near the vent "
            "are lush and overgrown -- ferns twice normal size, flowers "
            "with colors too vivid."
        ),
        room_type="clearing",
        indoor=False,
    )

    rs_north_approach = area.room(
        "rs_north_approach",
        name="Northern Approach",
        desc=(
            "The northern edge of the Resonance zone, where the warped "
            "trees transition back to normal growth. The boundary is "
            "surprisingly sharp -- three steps and the vibration drops "
            "by half. Five more and it is barely perceptible. The trees "
            "on the normal side lean slightly toward the node, as if "
            "drawn by gravity."
        ),
        room_type="path",
        indoor=False,
    )

    rs_east_border = area.room(
        "rs_east_border",
        name="Eastern Border",
        desc=(
            "The eastern edge of the node's influence. The forest here "
            "is a battleground between normal growth and the node's "
            "distortion. Some trees grow straight, others are warped. "
            "Some moss glows, some does not. The boundary shifts -- "
            "trees that were normal last season show early signs of "
            "the spiral growth pattern."
        ),
        room_type="path",
        indoor=False,
    )

    rs_south_approach = area.room(
        "rs_south_approach",
        name="Southern Approach",
        desc=(
            "The southern path into the Resonance, where the Deep "
            "Cantera's normal darkness gives way to the node's strange "
            "twilight. The transition is gradual -- first the vibration, "
            "then the warped trees, then the glowing moss. A carved "
            "warning post, ancient and barely legible, stands at the "
            "boundary. Its message in druidic script: 'The earth "
            "remembers.'"
        ),
        room_type="path",
        indoor=False,
    )

    rs_west_clearing = area.room(
        "rs_west_clearing",
        name="Western Clearing",
        desc=(
            "A wide clearing on the western edge of the Resonance where "
            "no trees grow. The ground is bare and cracked, as if baked "
            "by heat from below. Stones arranged in a circle mark what "
            "might have been a meeting place. The vibration is strong "
            "here, and the air has a quality of expectation -- like "
            "the moment before a thunderclap that never comes."
        ),
        room_type="clearing",
        indoor=False,
    )

    rs_watcher_ridge = area.room(
        "rs_watcher_ridge",
        name="Watcher's Ridge",
        desc=(
            "A rocky outcropping that overlooks the node center from "
            "above. The view is remarkable -- the eight standing stones "
            "are visible below, the warped trees radiating outward from "
            "them like ripples frozen in wood. From this height, the "
            "pattern is obvious. The stones are not randomly placed. "
            "They are precisely positioned, forming an octagonal "
            "configuration that mirrors something."
        ),
        room_type="path",
        indoor=False,
    )

    rs_stabilization_ring = area.room(
        "rs_stabilization_ring",
        name="Stabilization Ring",
        desc=(
            "A ring of carved stone channels surrounds a section of the "
            "node, forming a pattern on the ground. The channels are "
            "old but functional -- sap flows through them in a precise "
            "circuit. Where the sap flows freely, the vibration is "
            "calmer. Where channels are blocked by debris or root growth, "
            "the vibration intensifies. Someone designed this to regulate "
            "the node. It needs maintenance."
        ),
        room_type="ruins",
        indoor=False,
    )

    rs_root_throne = area.room(
        "rs_root_throne",
        name="Root Throne",
        desc=(
            "An ancient tree's exposed root system has formed what can "
            "only be described as a seat -- curved, supported, almost "
            "comfortable. Before it, the ground is worn smooth by what "
            "must have been generations of feet. Someone sat here. "
            "Regularly. Watching the node. The tree is dead but its "
            "roots still pulse with warmth."
        ),
        room_type="clearing",
        indoor=False,
    )

    # Region 5 Exits
    area.exit(dc_south_approach, rs_south_approach, "north")
    area.exit(rs_south_approach, dc_south_approach, "south")
    area.exit(bh_north_descent, rs_west_clearing, "north")
    area.exit(rs_west_clearing, bh_north_descent, "south")
    area.exit(rc_ascending_shaft, rs_vine_hollow, "up")
    area.exit(rs_vine_hollow, rc_ascending_shaft, "down")

    area.exit(rs_south_approach, rs_outer_ring, "north")
    area.exit(rs_outer_ring, rs_south_approach, "south")
    area.exit(rs_outer_ring, rs_humming_path, "north")
    area.exit(rs_humming_path, rs_outer_ring, "south")
    area.exit(rs_humming_path, rs_warped_grove, "west")
    area.exit(rs_warped_grove, rs_humming_path, "east")
    area.exit(rs_humming_path, rs_twisted_approach, "north")
    area.exit(rs_twisted_approach, rs_humming_path, "south")
    area.exit(rs_twisted_approach, rs_standing_stones, "north")
    area.exit(rs_standing_stones, rs_twisted_approach, "south")
    area.exit(rs_standing_stones, rs_node_center, "in")
    area.exit(rs_node_center, rs_standing_stones, "out")
    area.exit(rs_warped_grove, rs_crystal_garden, "north")
    area.exit(rs_crystal_garden, rs_warped_grove, "south")
    area.exit(rs_crystal_garden, rs_sap_convergence, "west")
    area.exit(rs_sap_convergence, rs_crystal_garden, "east")
    area.exit(rs_standing_stones, rs_echo_stones, "east")
    area.exit(rs_echo_stones, rs_standing_stones, "west")
    area.exit(rs_standing_stones, rs_amber_pool, "west")
    area.exit(rs_amber_pool, rs_standing_stones, "east")
    area.exit(rs_echo_stones, rs_broken_pillar, "north")
    area.exit(rs_broken_pillar, rs_echo_stones, "south")
    area.exit(rs_amber_pool, rs_moss_terrace, "north")
    area.exit(rs_moss_terrace, rs_amber_pool, "south")
    area.exit(rs_moss_terrace, rs_singing_trees, "west")
    area.exit(rs_singing_trees, rs_moss_terrace, "east")
    area.exit(rs_broken_pillar, rs_collapsed_arch, "east")
    area.exit(rs_collapsed_arch, rs_broken_pillar, "west")
    area.exit(rs_sap_convergence, rs_thermal_vent, "north")
    area.exit(rs_thermal_vent, rs_sap_convergence, "south")
    area.exit(rs_thermal_vent, rs_north_approach, "north")
    area.exit(rs_north_approach, rs_thermal_vent, "south")
    area.exit(rs_collapsed_arch, rs_east_border, "east")
    area.exit(rs_east_border, rs_collapsed_arch, "west")
    area.exit(rs_west_clearing, rs_warped_grove, "east")
    area.exit(rs_warped_grove, rs_west_clearing, "west")
    area.exit(rs_singing_trees, rs_watcher_ridge, "north")
    area.exit(rs_watcher_ridge, rs_singing_trees, "south")
    area.exit(rs_vine_hollow, rs_outer_ring, "east")
    area.exit(rs_outer_ring, rs_vine_hollow, "west")
    area.exit(rs_watcher_ridge, rs_stabilization_ring, "east")
    area.exit(rs_stabilization_ring, rs_watcher_ridge, "west")
    area.exit(rs_stabilization_ring, rs_root_throne, "north")
    area.exit(rs_root_throne, rs_stabilization_ring, "south")

    # Region 5 spawns (normal L0 mobs)
    area.spawn(rs_outer_ring, "cantera_wolf", count_min=1, count_max=2,
               respawn_minutes=15)
    area.spawn(rs_warped_grove, "vine_creeper", count_min=1, count_max=2,
               respawn_minutes=12, base_disposition=-0.3)
    area.spawn(rs_east_border, "forest_spider", count_min=1, count_max=1,
               respawn_minutes=12)
    area.spawn(rs_west_clearing, "wild_boar", count_min=1, count_max=1,
               respawn_minutes=15)

    # L1 corrupted mob spawns (only active during node collapse)
    area.spawn(rs_node_center, "corrupted_treant", count_min=1, count_max=1,
               respawn_minutes=20, spawn_condition="node_active")
    area.spawn(rs_standing_stones, "void_wisp", count_min=2, count_max=3,
               respawn_minutes=15, spawn_condition="node_active")
    area.spawn(rs_crystal_garden, "void_wisp", count_min=1, count_max=2,
               respawn_minutes=15, spawn_condition="node_active")
    area.spawn(rs_warped_grove, "blighted_stag", count_min=1, count_max=2,
               respawn_minutes=18, spawn_condition="node_active")
    area.spawn(rs_amber_pool, "corrupted_treant", count_min=1, count_max=1,
               respawn_minutes=20, spawn_condition="node_active")
    area.spawn(rs_sap_convergence, "blighted_stag", count_min=1, count_max=1,
               respawn_minutes=18, spawn_condition="node_active")
    area.spawn(rs_echo_stones, "void_wisp", count_min=1, count_max=2,
               respawn_minutes=15, spawn_condition="node_active")
    area.spawn(rs_vine_hollow, "corrupted_treant", count_min=1, count_max=1,
               respawn_minutes=20, spawn_condition="node_active")
    area.spawn(rs_moss_terrace, "blighted_stag", count_min=1, count_max=1,
               respawn_minutes=18, spawn_condition="node_active")
    area.spawn(rs_thermal_vent, "void_wisp", count_min=1, count_max=1,
               respawn_minutes=15, spawn_condition="node_active")

    # Region 5 lore (normal/L0)
    area.lore_fragment("cantera_node_lore_001", rs_standing_stones,
        text=(
            "The eight standing stones are not merely placed -- they are "
            "anchored. Each one extends deep into the earth, far deeper "
            "than its visible height. They are keystones in a structure "
            "that continues underground. The symbols on each stone are "
            "different, but together they form a complete statement in "
            "a language that predates all known writing systems. "
            "Four strokes per symbol. Eight symbols total. Thirty-two "
            "strokes. A base-eight expression."
        ),
        discovery_method="search",
        scholar_path="remnance",
        insight_gain=20,
    )
    area.lore_fragment("cantera_node_lore_002", rs_node_center,
        text=(
            "The stone disc at the center is not a lid or a marker. It "
            "is a lens. The concentric rings focus something -- not "
            "light, but the resonance itself. The disc amplifies the "
            "vibration from below and distributes it through the stone "
            "circle. This was designed. Engineered. By something that "
            "understood mathematics and resonance frequencies at a "
            "level no current civilization possesses."
        ),
        discovery_method="search",
        scholar_path="remnance",
        insight_gain=25,
    )
    area.lore_fragment("cantera_stabilization_001", rs_stabilization_ring,
        text=(
            "The channel system is a regulator. When sap flows through "
            "all channels unobstructed, the node operates at a stable "
            "baseline. Blockages cause feedback -- resonance that "
            "amplifies instead of dispersing. The system was designed "
            "to be maintained. Whoever built it expected someone to "
            "keep the channels clear. That maintenance stopped long ago."
        ),
        discovery_method="search",
        scholar_path="remnance",
        insight_gain=15,
    )

    # L1 exclusive lore (only discoverable during node collapse)
    area.lore_fragment("cantera_l1_lore_001", rs_node_center,
        text=(
            "When the node is active, the stone disc becomes translucent. "
            "Through it, shapes are visible -- structures beneath the "
            "earth, extending far deeper than any root system. Corridors "
            "of shaped stone. Chambers with geometric precision. This "
            "is not a natural formation. Something was built here, and "
            "the forest grew over it."
        ),
        discovery_method="search",
        scholar_path="remnance",
        insight_gain=30,
    )
    area.lore_fragment("cantera_l1_lore_002", rs_standing_stones,
        text=(
            "In the node's active state, the standing stones sing in "
            "harmony. The eight notes form an octave -- but not a human "
            "octave. The intervals are different. Base-eight. The melody "
            "repeats every eight measures, each repetition introducing "
            "a variation so subtle it takes hours to detect. This is "
            "not music. It is communication. Something is speaking."
        ),
        discovery_method="search",
        scholar_path="remnance",
        insight_gain=30,
    )
    area.lore_fragment("cantera_l1_lore_003", rs_crystal_garden,
        text=(
            "The crystals in the garden rearrange themselves during "
            "node activation. Their positions shift -- slowly, over "
            "hours -- into a configuration that mirrors the standing "
            "stones above. An octagonal pattern. The crystals ARE the "
            "same material as the standing stones, just younger. The "
            "node is growing its own infrastructure. Or trying to."
        ),
        discovery_method="search",
        scholar_path="remnance",
        insight_gain=30,
    )

    # ------------------------------------------------------------------
    # Named mob: The Heartwood Ancient
    # ------------------------------------------------------------------
    area.named_mob(
        "heartwood_ancient",
        rs_root_throne,
        respawn_minutes=120,
        respawn_variance=30,
        prestige_modifier=2.0,
        tome_drop="heartwood_tome",
        behavior=["root_slam", "bark_shield", "sap_spray"],
        base_disposition=-0.8,
    )

    # ------------------------------------------------------------------
    # Field NPCs
    # ------------------------------------------------------------------

    # 1. Druid hermit studying node instability
    area.npc(
        bh_hermit_clearing,
        "npc_druid_thaelen",
        name="Thaelen",
        title="Druid Hermit",
        desc=(
            "An elderly man with a long grey beard woven with twigs and "
            "dried flowers. His robes are patched and stained with "
            "orange sap. His eyes are sharp and restless, constantly "
            "scanning the forest. He mutters to himself, making notes "
            "on strips of bark with charcoal."
        ),
        faction="wardens",
        trainer_id="npc_trainer_foraging_cantera",
        dialogue={
            "greeting": (
                "Thaelen looks up from his bark notes. 'Another one drawn "
                "to the pulse? I cannot blame you. I have studied it for "
                "thirty years and still do not understand what is happening "
                "down there. But I can tell you this -- it is getting worse.'"
            ),
            "topics": {
                "node": (
                    "'The resonance is not natural. Oh, the forest is natural "
                    "enough -- but what lies beneath predates the trees by "
                    "millennia. Something was built here, and the forest grew "
                    "to protect it. Or contain it. I am no longer certain "
                    "which.'"
                ),
                "corruption": (
                    "'When the resonance spikes, the forest changes. Trees "
                    "twist. The sap runs hot. Creatures appear that have no "
                    "business existing. I call it corruption because I lack "
                    "a better word. But corruption implies something is wrong. "
                    "What if this is what the forest is supposed to do?'"
                ),
                "stabilization": (
                    "'There are channels -- carved stone channels around the "
                    "node center. They regulate the resonance when they flow "
                    "freely. Clear the blockages and the node calms. But it "
                    "is a temporary measure. Like draining a wound that will "
                    "not heal. Someone needs to understand why it is failing.'"
                ),
                "pala": (
                    "'The Pala trees are sentinels. Their sap carries the "
                    "resonance from the node outward through the forest. They "
                    "are not trees in the way you understand trees. They are "
                    "conduits. Infrastructure. Built by something that saw "
                    "no distinction between the living and the mechanical.'"
                ),
            },
        },
    )

    # 2. Warden ranger tracking corruption spread
    area.npc(
        fe_warden_post,
        "npc_warden_kaelen",
        name="Kaelen",
        title="Warden Ranger",
        desc=(
            "A lean woman in worn green leathers, her dark hair pulled "
            "back tight. A longbow rests across her knees as she studies "
            "a map pinned to the post's railing. Red marks cluster near "
            "the center of the forest. Her expression is grim."
        ),
        faction="wardens",
        trainer_id="npc_trainer_tracking_cantera",
        dialogue={
            "greeting": (
                "Kaelen glances up briefly. 'You heading deeper? Watch "
                "yourself. The wildlife has been aggressive lately -- worse "
                "than usual. Something in the center is stirring them up. "
                "I have been tracking it for weeks.'"
            ),
            "topics": {
                "corruption": (
                    "'The red marks on this map? Each one is a sighting of "
                    "aberrant behavior -- wolves that do not flee, spiders "
                    "building webs where they never did before, trees growing "
                    "wrong. The pattern is expanding outward from the center. "
                    "Slowly, but steadily.'"
                ),
                "forest": (
                    "'The Cantera has always been strange. The Wardens have "
                    "monitored it for generations. But this -- this is new. "
                    "The forest is not just strange anymore. It is unstable. "
                    "And the Empire does not care because the instability "
                    "has not reached anything they value yet.'"
                ),
                "supplies": (
                    "'I could use help resupplying the watch posts deeper in. "
                    "The last runner did not come back. Probably just got "
                    "lost -- the paths shift when the resonance spikes -- but "
                    "I cannot leave this post unmanned.'"
                ),
            },
        },
    )

    # 3. Lost traveler (quest hook)
    area.npc(
        dc_charcoal_clearing,
        "npc_traveler_mirren",
        name="Mirren",
        title="Lost Traveler",
        desc=(
            "A young man sitting on the remains of the collapsed kiln, "
            "looking bewildered and frightened. His pack is open beside "
            "him, half its contents spilled. He keeps glancing at the "
            "trees as if expecting them to move."
        ),
        dialogue={
            "greeting": (
                "Mirren startles at your approach. 'Thank the Crown -- a "
                "person! I have been walking in circles for two days. My "
                "wagon train was heading to Vael's Crossing but I went to "
                "gather firewood and... the forest moved. I swear it moved. "
                "The path I came in on was not there when I turned around.'"
            ),
            "topics": {
                "supplies": (
                    "'My pack had three days of food. Most of it spilled when "
                    "I ran from -- I do not know what it was. Something big. "
                    "In the trees. Could you spare anything? Or at least "
                    "point me toward the trail east?'"
                ),
                "wagon": (
                    "'The wagon train was carrying timber orders for the "
                    "market in Vael's Crossing. Foreman Dask will not wait "
                    "long. If I do not catch up, I lose my pay for the "
                    "whole season.'"
                ),
            },
        },
    )

    # 4. Warden supply sergeant (delivery target for cantera_resupply)
    area.npc(
        bh_cantera_overlook, "npc_warden_supply_sergeant",
        name="Sergeant Voss",
        title="Warden Supply Sergeant",
        desc=(
            "A stocky woman in reinforced Warden leathers, her sleeves "
            "rolled past thick forearms. Crates and canvas bundles are "
            "stacked in neat rows behind her -- the product of a mind "
            "that treats logistics like a battlefield. She checks a "
            "manifest against a dwindling pile of supplies, frowning over "
            "the overlook where the deeper watch line should be visible."
        ),
        faction="wardens",
        dialogue={
            "greeting": (
                "Voss barely glances up from her manifest. 'If you are "
                "carrying supply crates, stack them there. If you are not, "
                "stay out of the way -- I have three outposts running on "
                "fumes and the last resupply runner never came back.'"
            ),
            "topics": {
                "supplies": (
                    "'We need rations, binding salve, and fire oil. In that "
                    "order. The corruption makes everything spoil faster -- "
                    "half what we requisition goes bad before it arrives.'"
                ),
                "corruption": (
                    "'The forest eats supply lines. Paths shift, landmarks "
                    "move. I have started marking trees with iron nails -- "
                    "the corruption does not seem to touch iron. Yet.'"
                ),
            },
        },
    )

    # 5. Ranger at forest edge (talk_to target for cantera_lost_traveler)
    area.npc(
        fe_trailhead, "npc_ranger_forest_edge",
        name="Ranger Taen",
        title="Forest Edge Ranger",
        desc=(
            "A lean figure in mottled green and brown, so still against "
            "the treeline that you almost miss him. His eyes track the "
            "canopy with the patience of someone who has learned that "
            "the forest rewards silence. A short bow and a coil of rope "
            "hang from his belt."
        ),
        faction="wardens",
        dialogue={
            "greeting": (
                "Taen nods once, barely moving. 'Heading in? Stay on the "
                "marked trail and do not follow sounds off the path. The "
                "forest plays tricks when the resonance is high.'"
            ),
            "topics": {
                "trail": (
                    "'I keep the first mile of trail clear and marked. Beyond "
                    "that, you are on your own. The corruption has not reached "
                    "this far yet, but the wildlife is restless.'"
                ),
                "traveler": (
                    "'We get lost ones stumbling out every few days. Most are "
                    "just disoriented. Some... are not the same when they come "
                    "back. If you find someone in there, get them to the trail "
                    "and head east. Do not linger.'"
                ),
            },
        },
    )

    # ------------------------------------------------------------------
    # Quests (enriched specs -- D-21/D-22)
    # ------------------------------------------------------------------
    area.quest("cantera_resupply",
        name="Warden Resupply",
        description="Kaelen needs a fresh supply crate carried from the forest edge to Sergeant Voss at the forward overlook. The path is usable again only in brief windows, and if the watch line goes hungry the whole west route starts guessing instead of reporting.",
        quest_type="delivery",
        quest_giver="npc_warden_kaelen",
        prerequisite_quests=["cantera_bandit_lookout"],
        objectives=[
            {"type": "deliver", "target": "npc_warden_supply_sergeant", "count": 1,
             "description": "Carry a Warden supply crate to Sergeant Voss at the forward overlook"},
        ],
        flagged_drop="warden_supplies",
        rewards=[
            {"action_type": "give_scales", "amount": 80},
            {"action_type": "modify_standing", "faction_id": "wardens", "delta": 200},
            {"action_type": "echo", "message": "|gVoss checks the crate seal, then the trail behind you. \"Good. One clean run means the line eats tonight and reports tomorrow. Tell Kaelen her route still breathes.\"|n"},
        ],
        # Legacy fields (backward compat)
        objective_type="deliver",
        objective_target="npc_warden_supply_sergeant",
        objective_count=1,
    )

    area.quest("cantera_lost_traveler",
        name="The Lost Traveler",
        description="Mirren is lost and frightened in the twisted forest paths near the cantera. The node corruption has warped the landmarks beyond recognition. Find the ranger at the forest edge who knows the safe routes out.",
        quest_type="escort",
        quest_giver="npc_traveler_mirren",
        objectives=[
            {"type": "talk_to", "target": "npc_ranger_forest_edge", "count": 1,
             "description": "Speak with the ranger about safe passage for Mirren"},
        ],
        rewards=[
            {"action_type": "give_scales", "amount": 60},
            {"action_type": "echo", "message": "|gMirren's shoulders sag with relief. \"A way out. Thank you -- I thought I'd wander these twisted paths forever. Take this, it's all I can offer.\"|n"},
        ],
        # Legacy fields (backward compat)
        objective_type="escort",
        objective_target="fe_trailhead",
        objective_count=1,
    )

    area.quest("cantera_bandit_lookout",
        name="Watchline Cutters",
        description="Kaelen has tracked a bandit knot using the charcoal clearings and old lookouts to cut runners off before they can reach the forward watch. Clear them out and the resupply line can move without every crate turning into a fight.",
        quest_type="kill",
        quest_giver="npc_warden_kaelen",
        prerequisite_quests=["ashreach_forest_relay"],
        objectives=[
            {"type": "kill", "target": "forest_bandit", "count": 6,
             "description": "Break the bandit hold on the charcoal clearings and lookout trail"},
        ],
        rewards=[
            {"action_type": "give_scales", "amount": 90},
            {"action_type": "modify_standing", "faction_id": "wardens", "delta": 175},
            {"action_type": "give_skill_xp", "skill_id": "reflexes", "count": 3},
            {"action_type": "echo", "message": "|gKaelen moves the bandit markers off her map one by one. \"That opens the trail. Good. Now we can carry food instead of bodies.\"|n"},
        ],
        next_quest_id="cantera_resupply",
        objective_type="kill",
        objective_target="forest_bandit",
        objective_count=6,
    )

    area.quest("cantera_node_study",
        name="Node Resonance Survey",
        description="Thaelen no longer wants guesses about the node. He wants observations from the standing stones, the crystal garden, and the stabilization ring -- the three places where the forest still shows what the buried machine is trying to do.",
        quest_type="investigation",
        quest_giver="npc_druid_thaelen",
        objectives=[
            {"type": "investigate", "target": "rs_standing_stones", "count": 1,
             "description": "Record what the standing stones are doing at the node edge"},
            {"type": "investigate", "target": "rs_crystal_garden", "count": 1,
             "description": "Survey how the crystal growth changes near the heart"},
            {"type": "investigate", "target": "rs_stabilization_ring", "count": 1,
             "description": "Inspect the stabilization ring where the old channels converge"},
        ],
        rewards=[
            {"action_type": "give_scales", "amount": 100},
            {"action_type": "modify_node_failure", "zone_id": "cantera_edge", "delta": -5.0},
            {"action_type": "give_skill_xp", "skill_id": "investigation", "count": 3},
            {"action_type": "echo", "message": "|gThaelen compares your notes against his bark strips and goes very still. \"Good. Now it begins to look like a system instead of a wound. That is worse in one way, and much better in another.\"|n"},
        ],
        next_quest_id="cantera_channel_survey",
        # Legacy fields (backward compat)
        objective_type="investigate",
        objective_target="rs_standing_stones",
        objective_count=1,
    )

    area.quest("cantera_channel_survey",
        name="Where the Forest Carries It",
        description="With the first survey complete, Thaelen wants the carrying lines traced beyond the heart itself. Follow the resonance from the shrine stones, through the sap convergence, and down into the root nexus where stone and living growth stop pretending they are separate things.",
        quest_type="investigation",
        quest_giver="npc_druid_thaelen",
        prerequisite_quests=["cantera_node_study"],
        objectives=[
            {"type": "investigate", "target": "bh_shrine_stones", "count": 1,
             "description": "Inspect the shrine stones where the outer channel still shows through"},
            {"type": "investigate", "target": "rs_sap_convergence", "count": 1,
             "description": "Trace the resonance where sap and carved channels meet"},
            {"type": "investigate", "target": "rc_root_nexus", "count": 1,
             "description": "Survey the root nexus beneath the forest"},
        ],
        rewards=[
            {"action_type": "give_scales", "amount": 95},
            {"action_type": "modify_node_failure", "zone_id": "cantera_edge", "delta": -3.0},
            {"action_type": "give_skill_xp", "skill_id": "investigation", "count": 4},
            {"action_type": "echo", "message": "|gThaelen presses bark charcoal into the grooves of your sketch and exhales slowly. \"There. A channel map. Not complete, but enough to prove the forest is carrying a design, not merely surviving a storm.\"|n"},
        ],
        objective_type="investigate",
        objective_target="bh_shrine_stones",
        objective_count=1,
    )

    area.lore_fragment("cantera_watchline_001", bh_cantera_overlook,
        discovery_method="search",
        text=(
            "The overlook's oldest marker stones do not face the node. They "
            "face east toward Ashreach and south toward the city road, as if "
            "this ridge was always meant to watch routes as much as forest. "
            "The Wardens inherited a watchline someone else first laid out."
        ),
        insight_gain=4,
    )

    area.lore_fragment("cantera_runner_markers_001", dc_bandit_lookout,
        discovery_method="search",
        text=(
            "Under the bandits' boot scrapes are older cut marks spaced at "
            "runner height along the rock. This lookout was not first built "
            "for ambush. It was a relay stop, then a warning point, and only "
            "much later a place where desperate people learned to steal."
        ),
        insight_gain=5,
    )

    # ------------------------------------------------------------------
    # Node configuration
    # ------------------------------------------------------------------
    # Layer 1 overrides: ~20 rooms near node center get corrupted versions.
    # Per D-46: Complete transformation. Almost unrecognizable from L0.
    # Per D-47: Partial overlay -- only rooms within radius 5 of center.
    # Per D-51: Stabilization mechanic via the stabilization_ring room.

    area.node(
        rs_node_center,
        radius=5,
        lore_fragments=[
            "cantera_node_lore_001",
            "cantera_node_lore_002",
            "cantera_l1_lore_001",
            "cantera_l1_lore_002",
            "cantera_l1_lore_003",
        ],
        layer_1_overrides={
            "rs_node_center": {
                "name": "The Shattered Lens",
                "desc": (
                    "The stone disc has cracked open. Raw energy pours upward "
                    "through the fractures in a column of white-gold light "
                    "that reaches the canopy and beyond. The concentric rings "
                    "spin freely, no longer anchored to the stone -- floating "
                    "discs of carved rock orbiting the light column. The heat "
                    "is intense. The sound is a single sustained note that "
                    "vibrates everything. Reality is thinner here. Through "
                    "the cracks, shapes move in a space that should not exist."
                ),
            },
            "rs_standing_stones": {
                "name": "The Singing Pillars",
                "desc": (
                    "The eight standing stones blaze with inner light, their "
                    "carved symbols burning white against the dark stone. "
                    "Each pillar produces a different note -- together they "
                    "create a chord that is physically painful. The air "
                    "between the pillars shimmers and tears, revealing "
                    "glimpses of underground chambers that should not be "
                    "visible from above. The grass is dead. The earth is "
                    "cracked. Something beneath is pushing upward."
                ),
            },
            "rs_crystal_garden": {
                "name": "Crystal Eruption",
                "desc": (
                    "The crystals have exploded from the earth in jagged "
                    "formations twice their normal size, their amber cores "
                    "burning with white fire. The ground is shattered where "
                    "they pushed through. Each crystal vibrates with "
                    "enough force to shatter glass. The chorus of notes "
                    "is deafening -- a harmony of frequencies that exist "
                    "at the edge of what the ear can process."
                ),
            },
            "rs_warped_grove": {
                "name": "The Petrified Spiral",
                "desc": (
                    "The warped trees have frozen mid-growth, their bark "
                    "turned to grey stone. They spiral inward like a "
                    "whirlpool frozen in wood-turned-rock. The leaves are "
                    "crystal -- delicate, translucent, chiming against each "
                    "other. Walking between them is like navigating a "
                    "sculpture of a forest rather than a forest itself. "
                    "Nothing lives here. Everything is preserved."
                ),
            },
            "rs_sap_convergence": {
                "name": "The Burning Rivers",
                "desc": (
                    "The sap streams have become rivers of liquid fire, "
                    "flowing in channels that cut through the earth with "
                    "the heat of molten metal. The air above shimmers "
                    "violently. Where the streams converge, a vortex of "
                    "burning amber spirals downward into a hole that was "
                    "not there before -- a drain that leads to impossible "
                    "depths. The heat is blistering."
                ),
            },
            "rs_echo_stones": {
                "name": "The Screaming Stones",
                "desc": (
                    "The echo stones have risen from the ground, floating "
                    "at waist height, spinning slowly. Each one emits a "
                    "continuous sound -- not an echo but a scream of "
                    "compressed noise that contains layers of information. "
                    "The symbols on their surfaces glow and shift, cycling "
                    "through configurations too fast to read. The stones "
                    "are broadcasting."
                ),
            },
            "rs_twisted_approach": {
                "name": "Fractured Path",
                "desc": (
                    "Spatial distortion has become visible. The path splits "
                    "into overlapping versions of itself -- three, four, "
                    "five copies occupying the same space at different "
                    "angles. Walking requires choosing which version is "
                    "real. The trees exist in multiple positions "
                    "simultaneously. Shadows fall in wrong directions. "
                    "Distance is meaningless."
                ),
            },
            "rs_amber_pool": {
                "name": "The Mirror of Depths",
                "desc": (
                    "The amber pool has become a window. Its surface is "
                    "glass-clear and shows not the sky above but chambers "
                    "below -- vast, carved, lit by sources that cast no "
                    "shadow. Structures of worked stone extend downward "
                    "for what might be miles. The pool's warmth has become "
                    "heat. The amber glows white at its center."
                ),
            },
            "rs_broken_pillar": {
                "name": "The Regrown Pillar",
                "desc": (
                    "The broken pillar has regenerated. New stone has grown "
                    "from the stump, raw and rough, not matching the "
                    "original's craftsmanship but unmistakably the same "
                    "material. The new growth pulses with light. The scorch "
                    "marks are gone, replaced by fresh-carved symbols that "
                    "glow and fade in a slow cycle. The node is repairing "
                    "its own infrastructure."
                ),
            },
            "rs_moss_terrace": {
                "name": "The Luminous Steps",
                "desc": (
                    "The moss terraces blaze with bioluminescent light -- "
                    "blue, green, and a color that has no name, cycling "
                    "through patterns that pulse in time with the node's "
                    "heartbeat. The terraces have become geometric, their "
                    "edges sharp and regular. They are not natural formations. "
                    "They are steps -- leading down into the earth where "
                    "the moss has peeled back to reveal carved stone beneath."
                ),
            },
            "rs_singing_trees": {
                "name": "The Crystallized Choir",
                "desc": (
                    "The three singing trees have transformed. Their bark "
                    "is crystal, their branches glass, their leaves prisms "
                    "that split the node's light into spectra that include "
                    "colors beyond normal vision. The song they produce is "
                    "not three notes but a full octave -- the missing five "
                    "notes supplied by resonance with the standing stones. "
                    "The harmony is perfect and terrible."
                ),
            },
            "rs_collapsed_arch": {
                "name": "The Restored Gate",
                "desc": (
                    "The archway has rebuilt itself. The keystone floats in "
                    "place, not resting on the arch but hovering a fraction "
                    "above it, held by force. The channels in the inner "
                    "surface flow with liquid light instead of sap. Through "
                    "the arch, the view is wrong -- not the forest beyond "
                    "but a corridor of dark stone extending into distance. "
                    "A gate. Not a ruin."
                ),
            },
            "rs_vine_hollow": {
                "name": "The Exposed Foundation",
                "desc": (
                    "The vines have pulled back from the buried stone, "
                    "revealing a carved surface larger than expected -- "
                    "not a single stone but the corner of a structure. "
                    "Walls. A corner of a room, buried under centuries "
                    "of growth. The stone is warm and covered in the same "
                    "symbols as the standing stones. Through gaps in the "
                    "exposed masonry, empty chambers are visible below."
                ),
            },
            "rs_thermal_vent": {
                "name": "The Exhaust Port",
                "desc": (
                    "The crack in the earth has widened into a shaft that "
                    "glows from deep within. The heat is furnace-like. "
                    "The air that rises carries not just minerals but light -- "
                    "particles of luminescence that drift upward like "
                    "inverted snow. The shaft is not natural. Its walls "
                    "are smooth and carved with channels. This is a vent "
                    "for something engineered."
                ),
            },
            "rs_outer_ring": {
                "name": "The Distortion Boundary",
                "desc": (
                    "The boundary between normal forest and the node's "
                    "influence has become a visible wall of shimmering air. "
                    "Trees on the node side are translucent, their internal "
                    "structures visible -- sap channels, root networks, the "
                    "resonance pathways that connect everything. The ground "
                    "glows. The boundary pulses outward in waves, each one "
                    "extending the node's reach by inches."
                ),
            },
            "rs_humming_path": {
                "name": "The Vibration Corridor",
                "desc": (
                    "The path has become a corridor of pure vibration. The "
                    "ground undulates in slow waves. The trees on either "
                    "side have merged into walls of wood and crystal, their "
                    "bark transparent, their cores glowing. Walking here "
                    "feels like walking through deep water -- resistance, "
                    "pressure, the sense that the medium itself is alive "
                    "and aware of your passage."
                ),
            },
            "rs_north_approach": {
                "name": "The Spreading Edge",
                "desc": (
                    "The northern boundary of the node has pushed outward. "
                    "Trees that were normal are now warped. Ground that was "
                    "stable now vibrates. The boundary is no longer sharp -- "
                    "it bleeds into the normal forest like ink in water. "
                    "Each pulse pushes it further. The node is growing."
                ),
            },
            "rs_east_border": {
                "name": "The Crystalline Front",
                "desc": (
                    "The eastern boundary has crystallized. A wall of amber "
                    "crystal stands where the tree line was, growing from "
                    "the ground in jagged formations. Trees caught in the "
                    "crystallization are preserved inside -- frozen mid-growth, "
                    "their details perfect. The crystal wall creaks and "
                    "groans as it expands, adding new layers."
                ),
            },
            "rs_west_clearing": {
                "name": "The Scorched Circle",
                "desc": (
                    "The clearing has become a blast zone. The meeting stones "
                    "are shattered. The ground is fused into dark glass that "
                    "reflects the node's light. Cracks in the glass reveal "
                    "the carved stone beneath -- more of the buried structure, "
                    "here exposed by whatever force sterilized the surface. "
                    "The heat rising from the glass is intense."
                ),
            },
            "rs_stabilization_ring": {
                "name": "The Overloaded Circuit",
                "desc": (
                    "The channel system has filled beyond capacity. Sap -- "
                    "now liquid light -- overflows the channels and pools "
                    "on the ground. The carved stone is hot enough to burn. "
                    "The channels themselves glow with patterns that race "
                    "through the circuit too fast to follow. The system is "
                    "trying to regulate but cannot keep up. Clearing the "
                    "channels might slow the process. Might."
                ),
            },
            "rs_watcher_ridge": {
                "name": "The Observation Point",
                "desc": (
                    "From the ridge, the full scope of the node activation "
                    "is visible. The octagonal pattern of the standing stones "
                    "is mirrored in the landscape itself -- eight radial "
                    "lines of distortion extending outward from the center, "
                    "each one a different manifestation. Crystal. Petrification. "
                    "Fire. Spatial distortion. The pattern is mathematical. "
                    "Precise. Designed."
                ),
            },
            "rs_root_throne": {
                "name": "The Awakened Seat",
                "desc": (
                    "The dead tree has reanimated. Its roots pulse with "
                    "light, its trunk groans and shifts. The seat-shaped "
                    "root formation has become a throne of living wood "
                    "that reshapes itself slowly, as if accommodating an "
                    "invisible occupant. The worn ground before it glows "
                    "with footprint-shaped impressions that appear and fade "
                    "in a pattern. Someone walked here. Is walking here. "
                    "In a time that is not now."
                ),
            },
        },
    )

    # ------------------------------------------------------------------
    # Triggers (09-02: zone entry)
    # ------------------------------------------------------------------

    # Zone entry — first visit atmospheric welcome
    area.trigger(
        fe_trailhead, "on_first_visit",
        [{"action_type": "echo", "message": "|yThe canopy closes overhead as you enter the Cantera. Pale orange sap weeps from the bark of towering Pala trees. The air is heavy, warm, and thrums with a low vibration you feel more than hear.|n"}],
        trigger_id="cantera_first_entry",
        once_per_character=True,
    )

    # ------------------------------------------------------------------
    # Gathering Pools
    # ------------------------------------------------------------------

    # Forest timber and pala wood
    area.gathering_pool(
        "wood",
        rooms=["fe_split_oak", "dc_fallen_giant", "dc_canopy_tunnel", "bh_pala_heart", "bh_fallen_pala"],
        materials=["cantera_timber", "pala_bark"],
        max_active=3, respawn_minutes=12, respawn_variance=4,
        tier_floor=1, tier_ceiling=2,
    )
    # Forest floor forage (mushrooms, berries, shelf fungus, pala sap)
    area.gathering_pool(
        "forage",
        rooms=["fe_fern_glade", "fe_mushroom_hollow", "dc_fungal_garden", "dc_druid_marker",
               "dc_charcoal_clearing", "bh_sap_pool", "rs_sap_convergence"],
        materials=["nightcap_mushroom", "bramble_berry", "shelf_fungus", "cave_mushroom", "pala_sap"],
        max_active=4, respawn_minutes=10, respawn_variance=3,
        tier_floor=1, tier_ceiling=3,
    )
    # Cave ores and crystals
    area.gathering_pool(
        "ore",
        rooms=["rc_drip_chamber", "rc_crystal_vein", "rc_root_nexus", "rc_deep_pool", "dc_amber_seep"],
        materials=["cantera_amber", "resonance_crystal"],
        max_active=2, respawn_minutes=18, respawn_variance=5,
        tier_floor=2, tier_ceiling=3,
    )
    # Spider silk from web-heavy areas
    area.gathering_pool(
        "hide",
        rooms=["dc_webbed_clearing", "dc_spider_nest", "rc_spider_den"],
        materials=["spider_silk"],
        max_active=2, respawn_minutes=15, respawn_variance=5,
    )
    area.gathering_pool(
        "fish",
        rooms=["fe_creek_bank", "dc_silent_pool", "rc_deep_pool"],
        materials=["river_trout", "shadow_bass"],
        max_active=2, respawn_minutes=13, respawn_variance=4,
    )

    # ------------------------------------------------------------------
    # Build
    # ------------------------------------------------------------------
    return area.build()
