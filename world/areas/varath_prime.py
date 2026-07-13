"""
Varath Prime -- Hub 4 Capital Zone Spec

First implementation slice for Soravelon's central imperial capital.
This pass establishes the builder-safe city skeleton, service anchors,
shared institutional vocabulary, courier platform, and the stable room ids
that later Hub 4 exterior zones will connect into.

Districts in this first slice:
    1. Crown Approach
    2. Outer Commons
    3. Ministry Ward
    4. Martial Quarter
    5. Dragon Corps Enclave
    6. Circle District
    7. Noble Heights
    8. Hidden Warrens
"""

from world.area_builder import AreaBuilder


def build():
    area = AreaBuilder("varath_prime")

    # ------------------------------------------------------------------
    # Zone setup
    # ------------------------------------------------------------------
    area.zone(
        name="Varath Prime",
        zone_type="imperial_city",
        continent="varath",
        tier=4,
        region="crownlands",
        faction_territory="imperial",
        faction_presence=["empire", "consortium", "circle"],
        world_x=180,
        world_y=24,
        world_radius=130,
    )

    # ==================================================================
    #  DISTRICT 1: CROWN APPROACH
    #  Main ceremonial and administrative entry corridor into the city.
    # ==================================================================

    ca_crownroad_gate = area.room(
        "ca_crownroad_gate",
        name="Crownroad Gate",
        desc=(
            "The main gate of Varath Prime rises in layered stone and iron, "
            "its arch lined with carved milebars and civic measures rather "
            "than heroic relief. Traffic enters beneath the watch of clerks, "
            "levy officers, and polished guards who care more for manifests "
            "than greetings. A bronze plaque names the Crown Restoration "
            "Charter of 711, though the paving beneath your feet is older "
            "than the inscription admitting to it."
        ),
        room_type="path",
        indoor=False,
        ambient_echoes=[
            "A clerk calls for the next manifest in a dry, carrying voice.",
            "Wagon axles groan as traffic inches through the crown gate.",
            "A bell rings once from somewhere deeper in the city.",
        ],
    )

    ca_gatehouse = area.room(
        "ca_gatehouse",
        name="Gatehouse of Measured Passage",
        desc=(
            "The gatehouse is fitted with brass counters, inspection rails, "
            "and narrow windows through which passing travelers are examined "
            "like parcels. Painted boards quote the Edict of Measured "
            "Passage, each line neat and stern. Ink, damp wool, and lamp "
            "smoke mingle in the guarded air."
        ),
        room_type="building",
        indoor=True,
    )

    ca_customs_hall = area.room(
        "ca_customs_hall",
        name="Customs Hall",
        desc=(
            "Long counting tables divide the customs hall into channels for "
            "merchants, petitioners, and military traffic. Bundles wait to "
            "be opened under seal while scribes scratch dispositions into "
            "ledgers bound in red leather. Above the desks, a fresh copy of "
            "the Edict of Measured Passage hangs over stonework whose joints "
            "do not match any recent restoration."
        ),
        room_type="building",
        indoor=True,
    )

    ca_arrival_court = area.room(
        "ca_arrival_court",
        name="Arrival Court",
        desc=(
            "Beyond customs, the capital opens into a broad court of dark "
            "stone striped by older pale bands that refuse to weather evenly. "
            "Processional banners hang from the upper walls, and runners "
            "cross the space carrying satchels, tablets, and stamped writs. "
            "Here the city makes its first promise: order, scale, and the "
            "sense that every step will be recorded by someone."
        ),
        room_type="path",
        indoor=False,
        ambient_echoes=[
            "Bootheels crack sharply against the court's layered stone.",
            "A messenger hurries past with a packet bound in green cord.",
            "Somewhere overhead, chains creak in the wind.",
        ],
    )
    area.room_role(ca_arrival_court, "greeter")

    ca_processional_way = area.room(
        "ca_processional_way",
        name="The Processional Way",
        desc=(
            "The avenue leading inward is unusually wide, laid with dark "
            "slabs edged in brighter stone that may once have framed another "
            "road entirely. Courtiers, levy officers, petitioners, and "
            "clerks all pass here under a forest of poles bearing civic "
            "measure-marks rather than heraldry. The city wants visitors to "
            "see itself first as a machine of lawful passage."
        ),
        room_type="path",
        indoor=False,
    )

    ca_watch_platform = area.room(
        "ca_watch_platform",
        name="Gate Watch Platform",
        desc=(
            "From the watch platform the geometry of the capital becomes more "
            "apparent: measured avenues, squared courts, and district walls "
            "laid atop lines that do not quite agree with each other. The "
            "gate crews below appear tiny beside the mass of stone and record "
            "keeping that keeps the city fed."
        ),
        room_type="building",
        indoor=False,
    )

    ca_manifest_yard = area.room(
        "ca_manifest_yard",
        name="Manifest Yard",
        desc=(
            "Impounded wagons and inspected carts stand in ordered rows behind "
            "painted guide lines while runners haul tablets between tally posts. "
            "Split roadwheel stamps mark the approved loads, and the rejected "
            "ones sit beneath canvas sheets until someone decides whether their "
            "errors are clerical or profitable."
        ),
        room_type="path",
        indoor=False,
    )

    ca_porters_shelter = area.room(
        "ca_porters_shelter",
        name="Porters' Shelter",
        desc=(
            "Benches, drying hooks, and a long iron stove make this shelter a "
            "brief mercy for those who drag the city's traffic into shape. Wet "
            "cloaks steam beside stacked handbarrows and coil baskets. Every "
            "conversation here eventually turns to delays, inspections, or who "
            "got left waiting at the gate."
        ),
        room_type="building",
        indoor=True,
    )

    ca_tally_steps = area.room(
        "ca_tally_steps",
        name="Tally Steps",
        desc=(
            "A narrow internal stair climbs past chalk boards crowded with load "
            "weights, wagon tallies, and abbreviated dispositions. The stone "
            "wear on the steps is older than the handrails fitted against it. "
            "Even here, the city has formalized something it inherited."
        ),
        room_type="building",
        indoor=True,
    )

    ca_assessor_gallery = area.room(
        "ca_assessor_gallery",
        name="Assessor Gallery",
        desc=(
            "High desks look down through slotted windows onto the traffic "
            "below. Here road assessors compare toll tables, seal rubbings, and "
            "manifest disputes with the cool patience of people who know delay "
            "is one of the tools of government."
        ),
        room_type="building",
        indoor=True,
    )

    ca_toll_archive = area.room(
        "ca_toll_archive",
        name="Old Toll Archive",
        desc=(
            "Shelves of waxed tablets and bound toll sheets fill this cramped "
            "archive, many scored with the split roadwheel stamp of the High "
            "Registry of Roads and Passage. New copies sit beside scraped older "
            "tables whose wording was changed just enough to look lawful."
        ),
        room_type="building",
        indoor=True,
    )

    ca_caravan_court = area.room(
        "ca_caravan_court",
        name="Caravan Court",
        desc=(
            "Licensed caravans wait here in measured rows between chalked curb "
            "marks and painted priority lines. Team leaders pace with tablets "
            "in hand while inspectors compare loads to declared manifests. Even "
            "resting traffic is expected to look orderly under the Crown's eye."
        ),
        room_type="path",
        indoor=False,
    )

    ca_levy_office = area.room(
        "ca_levy_office",
        name="Levy Office",
        desc=(
            "The levy office is a plain chamber of counters, rate boards, and "
            "argument benches where wagon masters dispute fees too late to avoid "
            "them. Split roadwheel stamps and measured rod seals share the wall "
            "space like allied blades."
        ),
        room_type="building",
        indoor=True,
    )

    ca_seized_goods_shed = area.room(
        "ca_seized_goods_shed",
        name="Seized Goods Shed",
        desc=(
            "Confiscated crates, impounded bundles, and disputed cargo wait in "
            "this locked shed beneath numbered tags and wax-sealed inventory "
            "strips. Nothing here belongs to itself anymore. It belongs to the "
            "next clerk willing to decide its disposition."
        ),
        room_type="building",
        indoor=True,
    )

    ca_milebar_balcony = area.room(
        "ca_milebar_balcony",
        name="Milebar Balcony",
        desc=(
            "A narrow upper balcony displays old milebars, route plates, and "
            "retired traffic markers whose measures do not all agree with the "
            "modern network below. Some were restored, some recopied, and some "
            "simply renamed into obedience."
        ),
        room_type="building",
        indoor=False,
    )

    ca_queue_lane = area.room(
        "ca_queue_lane",
        name="Queue Lane",
        desc=(
            "Rails and painted stones force arriving petitioners and merchants "
            "into lines that bend between the gatehouse and the levy counters. "
            "Patience is treated here as another toll owed to the capital."
        ),
        room_type="path",
        indoor=False,
    )

    ca_measure_house = area.room(
        "ca_measure_house",
        name="Measure House",
        desc=(
            "Stacks of standard weights, yard rods, capacity jars, and test "
            "scales fill the measure house with the heavy calm of official "
            "certainty. Anyone disputing a tally is eventually brought here."
        ),
        room_type="building",
        indoor=True,
    )

    ca_guard_colonnade = area.room(
        "ca_guard_colonnade",
        name="Guard Colonnade",
        desc=(
            "Spears stand in ordered racks beneath a long colonnade where gate "
            "guards wait between inspections, disputes, and brief calls to force. "
            "Their presence makes the arrival courts feel less civic than staged."
        ),
        room_type="building",
        indoor=False,
    )

    ca_waybill_office = area.room(
        "ca_waybill_office",
        name="Waybill Office",
        desc=(
            "Bundles of route slips, tariff copies, escort notices, and amended "
            "waybills cover the desks in this narrow office. The room reduces "
            "travel to a series of authorized lines, deletions, and seals."
        ),
        room_type="building",
        indoor=True,
    )

    ca_relief_yard = area.room(
        "ca_relief_yard",
        name="Relief Yard",
        desc=(
            "Overflow wagons, delayed patrols, and redirected teamsters are held "
            "in this side yard until the gate front can bear them. The city never "
            "stops; it merely stacks its waiting out of sight."
        ),
        room_type="path",
        indoor=False,
    )

    # ==================================================================
    #  DISTRICT 2: OUTER COMMONS
    #  Public trade, lodging, money, and everyday capital traffic.
    # ==================================================================

    oc_scale_square = area.room(
        "oc_scale_square",
        name="Scale Square",
        desc=(
            "The Outer Commons revolve around a large public square where "
            "scales, tally boards, message posts, and wagon lanes compete for "
            "space. Hawkers work the edges while porters weave through the "
            "crowd with practiced impatience. This is the face of the capital "
            "most common folk understand: expensive, crowded, efficient, and "
            "never entirely kind."
        ),
        room_type="path",
        indoor=False,
        ambient_echoes=[
            "A porter curses as a handcart clips a stone curb.",
            "Someone shouts today's grain rate from the far side of the square.",
            "Coins click over a counting board in a rapid metallic rhythm.",
        ],
    )

    oc_red_market = area.room(
        "oc_red_market",
        name="Red Market",
        desc=(
            "The Red Market is a tight lane of awnings, hanging lanterns, "
            "leather racks, and stacked crates of practical gear. Nothing "
            "sold here is ceremonial, only necessary. Travelers buy cloaks, "
            "boots, knives, packs, and whatever else might let them survive "
            "the roads just long enough to owe the city more money later."
        ),
        room_type="path",
        indoor=False,
    )

    oc_wayfarer_inn = area.room(
        "oc_wayfarer_inn",
        name="The Wayfarer's Burden",
        desc=(
            "The common inn is low-beamed, noisy, and perpetually warm from "
            "its kitchen hearth. Benches crowd around long tables scarred by "
            "knife points and tankard rings. Couriers, drovers, petitioners, "
            "and minor functionaries all pass through, leaving gossip in "
            "their wake like ash in a draft."
        ),
        room_type="building",
        indoor=True,
    )

    oc_exchange_hall = area.room(
        "oc_exchange_hall",
        name="Commons Exchange Hall",
        desc=(
            "Columns of dark stone hold up the exchange hall, where counting "
            "windows stand behind brass grilles and armed clerks keep their "
            "voices low. Notices warn against disorderly conduct, forged "
            "drafts, and unnecessary noise. Even in the Outer Commons, money "
            "is handled as if it were a sacred civic instrument."
        ),
        room_type="building",
        indoor=True,
    )

    oc_shrine_lane = area.room(
        "oc_shrine_lane",
        name="Shrine Lane",
        desc=(
            "Small shrines crowd the lane between trade fronts and older "
            "stone drains. Most are worn nearly smooth by touch, their icons "
            "half obscured by city soot and later civic paint. Petitioners "
            "leave wax, ribbon, and copied prayers between runoff grates that "
            "look older than the district around them."
        ),
        room_type="path",
        indoor=False,
    )

    oc_carter_row = area.room(
        "oc_carter_row",
        name="Carter Row",
        desc=(
            "Teamsters, wheelwrights, porters, and baggage clerks operate "
            "along Carter Row amid stacked harness, axle grease, feed bins, "
            "and repair benches. The traffic here never fully stops. Even at "
            "rest, the street feels like it is braced for movement."
        ),
        room_type="path",
        indoor=False,
    )

    oc_ragcourt = area.room(
        "oc_ragcourt",
        name="Ragcourt",
        desc=(
            "A crooked elbow off the Red Market serves secondhand dealers, "
            "patch merchants, and opportunists who buy what the road leaves "
            "behind. Cloaks, straps, traveling blankets, and dented cookware "
            "hang from lines overhead. The bargains here are real, though so is "
            "the likelihood someone checks your purse while you admire them."
        ),
        room_type="path",
        indoor=False,
    )

    oc_lodger_alley = area.room(
        "oc_lodger_alley",
        name="Lodger Alley",
        desc=(
            "This back lane behind the inn is lined with shutters, wash lines, "
            "cheap bunks, and hired cubbies for people too transient or too poor "
            "for proper rooms. Voices carry easily here through warped boards "
            "and thin curtains. Everyone knows a little about everyone else."
        ),
        room_type="path",
        indoor=False,
    )

    oc_coinstairs = area.room(
        "oc_coinstairs",
        name="Coinstairs Arcade",
        desc=(
            "A covered stair arcade climbs past licensed money desks and narrow "
            "account windows where consortium scribes sort drafts, wagers, and "
            "short-term notes. Brass plates warn against forged seals and noisy "
            "arguments. The arcade smells faintly of metal, wax, and anxiety."
        ),
        room_type="building",
        indoor=True,
    )

    oc_stewpot_arcade = area.room(
        "oc_stewpot_arcade",
        name="Stewpot Arcade",
        desc=(
            "Steam drifts through this covered row of cookstalls where drovers, "
            "messengers, and market hands buy quick bowls before getting back to "
            "someone else's timetable. It is one of the few corners of the "
            "capital where people still laugh without checking who heard them."
        ),
        room_type="building",
        indoor=True,
    )

    oc_teamyard = area.room(
        "oc_teamyard",
        name="Teamyard",
        desc=(
            "Draft teams are watered and re-hitched in a broad fenced yard "
            "ringed by feed troughs, repair racks, and shouted instructions. "
            "Registry chalk marks on the posts divide the space by route and "
            "priority, turning even tired animals into another ledger problem."
        ),
        room_type="path",
        indoor=False,
    )

    oc_tinkers_row = area.room(
        "oc_tinkers_row",
        name="Tinkers' Row",
        desc=(
            "A line of braziers, tool racks, solder stands, and patched canopies "
            "marks the practical heart of the commons. Travelers come here for "
            "buckles, rivets, hinges, lamp parts, and a hundred small repairs "
            "that keep larger disasters one road farther away."
        ),
        room_type="path",
        indoor=False,
    )

    oc_cloth_hall = area.room(
        "oc_cloth_hall",
        name="Cloth Hall",
        desc=(
            "Bolts of rough wool, travel wraps, gloves, patched cloaks, and "
            "weather capes hang from beams over a floor dusted with lint. The "
            "hall is not elegant, but it understands roads better than elegance "
            "ever will."
        ),
        room_type="building",
        indoor=True,
    )

    oc_broker_steps = area.room(
        "oc_broker_steps",
        name="Broker Steps",
        desc=(
            "Stone steps climb between message boards, day-rate slates, and "
            "licensed runner posts where work, risk, and urgency are priced in "
            "public. Porters, couriers, caravan hands, and opportunists gather "
            "here to sell time they do not really own."
        ),
        room_type="building",
        indoor=False,
    )

    oc_public_baths = area.room(
        "oc_public_baths",
        name="Commons Baths",
        desc=(
            "Steam curls up from tiled basins while attendants keep order with "
            "wooden ladles, quiet warnings, and an eye for cutpurses. The baths "
            "offer warmth, gossip, and a temporary sense that road grime and city "
            "pressure can be scrubbed off together."
        ),
        room_type="building",
        indoor=True,
    )

    oc_artisans_court = area.room(
        "oc_artisans_court",
        name="Artisans' Court",
        desc=(
            "A paved little court gathers practical craftsmen beneath shared "
            "awnings and public notice slates. Everyone here repairs what the "
            "city and the roads wear down faster than pride admits."
        ),
        room_type="path",
        indoor=False,
    )

    oc_scribes_corner = area.room(
        "oc_scribes_corner",
        name="Scribes' Corner",
        desc=(
            "Portable desks, ink trays, copied forms, and waiting stools line "
            "this narrow corner where letters, contracts, and petitions are put "
            "into the sort of language officials might accept."
        ),
        room_type="building",
        indoor=False,
    )

    oc_lantern_row = area.room(
        "oc_lantern_row",
        name="Lantern Row",
        desc=(
            "Rows of hanging lamps, spare chimneys, oil jars, and mirrored tins "
            "throw warm light across a lane dedicated to illumination and the "
            "business that follows after dusk."
        ),
        room_type="path",
        indoor=False,
    )

    oc_teamsters_hall = area.room(
        "oc_teamsters_hall",
        name="Teamsters' Hall",
        desc=(
            "Ledger boards, bench tables, and rough wall maps give the hall the "
            "feel of a workplace too busy to waste charm on visitors. Routes, "
            "rates, and grievances all pass through here sooner or later."
        ),
        room_type="building",
        indoor=True,
    )

    oc_hawkers_walk = area.room(
        "oc_hawkers_walk",
        name="Hawkers' Walk",
        desc=(
            "Street sellers cluster along this broad walk with trays, poles, and "
            "stacked baskets of every legal convenience the capital can tolerate. "
            "Nothing stays quiet here for long, especially not a bargain."
        ),
        room_type="path",
        indoor=False,
    )

    # ==================================================================
    #  DISTRICT 3: MINISTRY WARD
    #  Permits, seals, ledgers, record copies, and civic revisions.
    # ==================================================================

    mw_decree_wall = area.room(
        "mw_decree_wall",
        name="Decree Wall",
        desc=(
            "A long wall of fitted stone carries layers of civic text: fresh "
            "painted decrees, copied charter language, and bronze tablets "
            "mounted over rasped surfaces where earlier inscriptions were "
            "removed. Citizens stop here to read what the city currently "
            "admits about itself."
        ),
        room_type="building",
        indoor=False,
    )

    mw_permit_hall = area.room(
        "mw_permit_hall",
        name="Permit Hall",
        desc=(
            "Counters and partition rails split the permit hall into patient, "
            "sullen lines. Every desk has its own seal set, ink block, and "
            "bundle of copied forms. The clerks here are not cruel so much as "
            "precisely uninterested in anyone's urgency."
        ),
        room_type="building",
        indoor=True,
    )

    mw_records_arcade = area.room(
        "mw_records_arcade",
        name="Records Arcade",
        desc=(
            "Stone arches shelter a corridor of chained cabinets, hanging "
            "index boards, and pigeonholes stuffed with folded copies. Pages "
            "change hands here under supervision, and damaged entries are "
            "quietly replaced by newer, cleaner ones. It is a place where "
            "history survives by being recopied just enough times."
        ),
        room_type="building",
        indoor=True,
    )

    mw_registry_annex = area.room(
        "mw_registry_annex",
        name="Registry Annex",
        desc=(
            "The annex is more cramped than the formal arcade, with patched "
            "shelving and stacks of rejected copies waiting for review. Leaves "
            "marked with civic measure seals lie beside bundles tagged for "
            "correction, excision, or transfer. The room smells of damp paste "
            "and scraped vellum."
        ),
        room_type="building",
        indoor=True,
    )

    mw_causeway_postern = area.room(
        "mw_causeway_postern",
        name="Causeway Postern",
        desc=(
            "A narrow postern gate opens from the Ministry Ward onto a service "
            "lane used by survey crews, archive runners, and sealed carts. The "
            "stone threshold is worn in a way the surrounding walls are not, "
            "suggesting an older passage formalized into ministry use. This "
            "is the stable city-side boundary for the old causeway route."
        ),
        room_type="path",
        indoor=False,
    )

    mw_copyists_walk = area.room(
        "mw_copyists_walk",
        name="Copyists' Walk",
        desc=(
            "Long desks run beneath high lamps where professional copyists set "
            "down civic language in disciplined hands. Scraped leaves dry on "
            "lines beside clean replacements awaiting official seals. This is "
            "where the city decides which version of itself will survive."
        ),
        room_type="building",
        indoor=True,
    )

    mw_seal_chamber = area.room(
        "mw_seal_chamber",
        name="Seal Chamber",
        desc=(
            "Cabinets of stamp heads, wax bars, lead tags, and measured rods "
            "fill the seal chamber with the heavy smell of hot resin. Clerks "
            "enter only with logged purpose. The Office of Seals and Civic "
            "Measure treats symbols like weapons that must be accounted for."
        ),
        room_type="building",
        indoor=True,
    )

    mw_correction_office = area.room(
        "mw_correction_office",
        name="Correction Office",
        desc=(
            "Bundles marked for amendment, excision, and restatement wait on "
            "shelving racks beside iron braziers used to soften wax and destroy "
            "damaged copies. Every tray bears a neat disposition slip. The room "
            "feels calm in the way a blade edge feels calm."
        ),
        room_type="building",
        indoor=True,
    )

    mw_confiscation_room = area.room(
        "mw_confiscation_room",
        name="Confiscation Room",
        desc=(
            "Shelved behind a double lock, confiscated copies and seized private "
            "records sit in tied bundles under numbered tags. Some were taken "
            "for error, some for fraud, and some for reasons the ledger slips do "
            "not bother to explain. Dust gathers on truth and lie alike."
        ),
        room_type="building",
        indoor=True,
    )

    mw_charter_vault = area.room(
        "mw_charter_vault",
        name="Charter Vault",
        desc=(
            "The vault is colder than the rest of the ward, with thick walls "
            "and barred catalog bays holding formal charter copies. Private "
            "house exemptions, preserve rights, extraction licenses, and road "
            "easements are all reduced here to tied bundles and shelf markers."
        ),
        room_type="building",
        indoor=True,
    )

    mw_petition_cloister = area.room(
        "mw_petition_cloister",
        name="Petition Cloister",
        desc=(
            "Benched alcoves line this covered walk where petitioners rehearse "
            "their phrasing before stepping up to official desks. Draft requests, "
            "private pleas, and expensive legal advice all circulate here under "
            "the patient drip of institutional time."
        ),
        room_type="building",
        indoor=True,
    )

    mw_notary_room = area.room(
        "mw_notary_room",
        name="Notary Room",
        desc=(
            "Austere tables, witness stools, and seal trays fill the notary room "
            "with the smell of wax and wetted paper. Signatures are not trusted "
            "here without ceremony, and ceremony is never free."
        ),
        room_type="building",
        indoor=True,
    )

    mw_witness_chamber = area.room(
        "mw_witness_chamber",
        name="Witness Chamber",
        desc=(
            "The witness chamber is quieter than the public ward, fitted with "
            "narrow desks, recording slates, and benches placed to keep people "
            "from forgetting they are being observed. Statements made here take "
            "on a civic weight few speakers seem to enjoy."
        ),
        room_type="building",
        indoor=True,
    )

    mw_ink_store = area.room(
        "mw_ink_store",
        name="Ink Store",
        desc=(
            "Locked cupboards of ink cakes, scraping knives, ruled sheets, and "
            "copy cords give this store the feeling of a well-defended arsenal. "
            "In a city of records, the materials of revision are too important "
            "to leave unattended."
        ),
        room_type="building",
        indoor=True,
    )

    mw_review_court = area.room(
        "mw_review_court",
        name="Review Court",
        desc=(
            "A roofed court of benches and filing rails where disputed copies are "
            "read aloud, compared, and either affirmed or quietly replaced. The "
            "process is orderly enough to make erasure feel procedural."
        ),
        room_type="building",
        indoor=False,
    )

    mw_docket_room = area.room(
        "mw_docket_room",
        name="Docket Room",
        desc=(
            "Stacks of day dockets, transfer orders, and correction slips rise "
            "from every flat surface in the room. The capital's paperwork does "
            "not merely describe movement; it creates it."
        ),
        room_type="building",
        indoor=True,
    )

    mw_archive_stair = area.room(
        "mw_archive_stair",
        name="Archive Stair",
        desc=(
            "A tight spiral stair links upper storage, lower records, and side "
            "desks that were never meant to hold as much work as they now do. "
            "Every landing bears the scrape marks of cabinets hauled by hand."
        ),
        room_type="building",
        indoor=True,
    )

    mw_public_records = area.room(
        "mw_public_records",
        name="Public Records Hall",
        desc=(
            "Long reading tables and chained reference copies allow citizens to "
            "consult the versions of history and law the ward has chosen to make "
            "visible. Access is public, but never exactly welcoming."
        ),
        room_type="building",
        indoor=True,
    )

    mw_seal_brazier = area.room(
        "mw_seal_brazier",
        name="Seal Brazier",
        desc=(
            "A fixed brazier heats wax, resin, and metal stamps for urgent sealing "
            "work. The glow makes every nearby document look momentarily important, "
            "which is useful when importance is part of the ritual."
        ),
        room_type="building",
        indoor=True,
    )

    # ==================================================================
    #  DISTRICT 4: MARTIAL QUARTER
    #  Barracks, drill space, infirmary, and the quarry road out.
    # ==================================================================

    mq_barracks_yard = area.room(
        "mq_barracks_yard",
        name="Barracks Yard",
        desc=(
            "The yard is packed hard by years of drill and wagon passage. "
            "Weapon racks stand beneath awnings while runners move orders "
            "between adjoining offices with heads lowered against the wind. "
            "Nothing here is decorative, only maintained."
        ),
        room_type="path",
        indoor=False,
    )

    mq_drill_green = area.room(
        "mq_drill_green",
        name="Drill Green",
        desc=(
            "A broad training ground opens behind the barracks, its lanes "
            "marked with chalked distances and scarred practice dummies. "
            "Commands snap through the air in clipped rhythms. The ground has "
            "been turned, tamped, and turned again so many times that it looks "
            "more engineered than natural."
        ),
        room_type="path",
        indoor=False,
    )

    mq_armory_lane = area.room(
        "mq_armory_lane",
        name="Armory Lane",
        desc=(
            "The lane runs between storehouses, repair bays, and quartermaster "
            "windows where kit is issued by ledger line. Crates of spears, "
            "bundled shields, and tarred ration bins are stacked with "
            "military neatness. Painted arrows on the stone point toward "
            "both the Dragon Corps enclave and the quarry road."
        ),
        room_type="path",
        indoor=False,
    )

    mq_infirmary = area.room(
        "mq_infirmary",
        name="Quarter Infirmary",
        desc=(
            "Rows of whitewashed cots line the infirmary under shelves of "
            "bandages, poultices, splints, and boiled instruments. Orderlies "
            "move with restrained urgency while a chalk board tracks the fit, "
            "the wounded, and the dead. It is less comforting than efficient, "
            "but efficiency is sometimes enough."
        ),
        room_type="building",
        indoor=True,
    )
    area.room_role(mq_infirmary, "respawn")

    mq_escarpment_road = area.room(
        "mq_escarpment_road",
        name="Escarpment Road",
        desc=(
            "The road leaving the Martial Quarter slopes toward the haul lanes "
            "and quarry approaches beyond the city. Wagon grooves score the "
            "stone, and every few yards a lifting ring or hitch post has been "
            "set into the curb. This is the stable city-side boundary for the "
            "ironvein route."
        ),
        room_type="path",
        indoor=False,
    )

    mq_muster_hall = area.room(
        "mq_muster_hall",
        name="Muster Hall",
        desc=(
            "Roster boards, bench lines, and issue hooks dominate the long "
            "muster hall. Units are assembled here into something the quarter "
            "can count, move, and punish. Names are spoken aloud less often "
            "than duties, absences, and deficiencies."
        ),
        room_type="building",
        indoor=True,
    )

    mq_supply_depot = area.room(
        "mq_supply_depot",
        name="Supply Depot",
        desc=(
            "Crates of preserved rations, lamp oil, bandage rolls, spare nails, "
            "and stamped requisition packets sit in disciplined rows behind the "
            "depot grille. Stonewake pickmarks show up on lifted hardware and "
            "haul hooks meant for work beyond the city walls."
        ),
        room_type="building",
        indoor=True,
    )

    mq_signal_tower = area.room(
        "mq_signal_tower",
        name="Signal Tower",
        desc=(
            "From the tower platform the Martial Quarter opens into lines of "
            "drill ground, storehouse roofs, and ordered roads. Flag racks and "
            "shutter codes hang beside speaking tubes used for emergency relay. "
            "The city communicates with an efficiency that feels almost impersonal."
        ),
        room_type="building",
        indoor=False,
    )

    mq_detention_block = area.room(
        "mq_detention_block",
        name="Detention Block",
        desc=(
            "Iron-barred cells line a narrow corridor beneath whitewashed walls "
            "and heavily locked stores. Drunk troopers, deserters awaiting "
            "transfer, and unlucky civilians all pass through the same doors. "
            "Mercy exists here only as a change in paperwork."
        ),
        room_type="building",
        indoor=True,
    )

    mq_ordnance_shed = area.room(
        "mq_ordnance_shed",
        name="Ordnance Shed",
        desc=(
            "Bolted racks hold spare spear shafts, crossbow limbs, tool heads, "
            "and reinforced hauling gear marked for hard field use. Iron Vein "
            "requisition slips are pinned to half the crates, tying the quarter's "
            "orderly shelves to the extraction roads beyond."
        ),
        room_type="building",
        indoor=True,
    )

    mq_forge_bay = area.room(
        "mq_forge_bay",
        name="Forge Bay",
        desc=(
            "Bellows, quench troughs, and iron worktables fill the forge bay "
            "with hard light and harder labor. Armor fastenings, spear heads, "
            "haul hooks, and repair plates come off these benches in a constant "
            "flow toward the quarter's various appetites."
        ),
        room_type="building",
        indoor=True,
    )

    mq_fletcher_yard = area.room(
        "mq_fletcher_yard",
        name="Fletcher Yard",
        desc=(
            "Dry racks of shafts, bundled fletching, and sorting stands line a "
            "walled work yard where ammunition is built in quantities too large "
            "to feel personal. The wind carries feather dust and clipped orders "
            "in equal measure."
        ),
        room_type="path",
        indoor=False,
    )

    mq_pay_window = area.room(
        "mq_pay_window",
        name="Pay Window",
        desc=(
            "A barred payout window serves soldiers, labor details, and approved "
            "contract crews beneath slates listing deductions for kit loss, late "
            "reporting, and transport damage. Money moves here only after it has "
            "been made disciplinary."
        ),
        room_type="building",
        indoor=True,
    )

    mq_stables = area.room(
        "mq_stables",
        name="Quarter Stables",
        desc=(
            "Military mounts stamp and snort between feed bins, tack hooks, and "
            "well-scrubbed stalls lined with issue numbers. Stablehands move with "
            "brisk caution among animals expected to serve the same schedules and "
            "requisitions as the people around them."
        ),
        room_type="building",
        indoor=False,
    )

    mq_armorers_hall = area.room(
        "mq_armorers_hall",
        name="Armorers' Hall",
        desc=(
            "Riveted plates, leather harness, spare buckles, and repair forms "
            "cover the long benches of the hall. It is less a workshop than a "
            "machine for returning damaged gear to the field in acceptable shape."
        ),
        room_type="building",
        indoor=True,
    )

    mq_ration_house = area.room(
        "mq_ration_house",
        name="Ration House",
        desc=(
            "Salted meat, hard bread, dried legumes, and transport bins are stacked "
            "here under chalked issue boards and stern warnings about theft. Hunger "
            "is kept at bay in the quarter by count, not generosity."
        ),
        room_type="building",
        indoor=True,
    )

    mq_range_gallery = area.room(
        "mq_range_gallery",
        name="Range Gallery",
        desc=(
            "Marked lanes, bolt catchers, and patched target screens line the "
            "gallery where practice fire is measured by consistency rather than "
            "showmanship. Misses are treated as paperwork with splinters."
        ),
        room_type="building",
        indoor=False,
    )

    mq_farrier_row = area.room(
        "mq_farrier_row",
        name="Farrier Row",
        desc=(
            "Shoe racks, hoof stands, coal braziers, and tack hooks fill this "
            "short row where working animals are made serviceable again and again. "
            "The quarter's pace rests on more legs than its officers admit."
        ),
        room_type="path",
        indoor=False,
    )

    mq_orders_desk = area.room(
        "mq_orders_desk",
        name="Orders Desk",
        desc=(
            "Fresh orders, suspension notices, and escort assignments are pinned "
            "to thick boards behind a rail where runners queue for sealed copies. "
            "This is the quarter reduced to instructions and consequence."
        ),
        room_type="building",
        indoor=True,
    )

    # ==================================================================
    #  DISTRICT 5: DRAGON CORPS ENCLAVE
    #  Corps logistics, handler infrastructure, and the courier platform.
    # ==================================================================

    dc_outer_yard = area.room(
        "dc_outer_yard",
        name="Dragon Corps Outer Yard",
        desc=(
            "The outer yard of the enclave is kept unnervingly clear. Feed "
            "wagons, water cisterns, tack frames, and inspection posts all "
            "sit exactly where regulation says they should. Even the silence "
            "here feels disciplined."
        ),
        room_type="path",
        indoor=False,
    )

    dc_tack_hall = area.room(
        "dc_tack_hall",
        name="Tack Hall",
        desc=(
            "Leather harness, plated collars, travel crates, and brass-bound "
            "flight kit hang in regimented rows. Every strap bears a tag, and "
            "every tag bears a line of issue. The place smells of oil, hide, "
            "and the faint mineral bite of scale dust."
        ),
        room_type="building",
        indoor=True,
    )

    dc_handler_ring = area.room(
        "dc_handler_ring",
        name="Handler Ring",
        desc=(
            "A circular training ring lies at the core of the enclave, marked "
            "by heavy posts, sanded footing, and iron rails built more to "
            "shape movement than to invite spectators. Handler crews cross "
            "the ring with clipped precision, each motion observed and "
            "recorded by someone."
        ),
        room_type="path",
        indoor=False,
    )

    dc_courier_platform = area.room(
        "dc_courier_platform",
        name="Courier Platform of the Thirteenth Talon",
        desc=(
            "High above the enclave, the courier platform looks out across "
            "Varath Prime and the long roads that feed it. Launch markers, "
            "signal cages, and chained cargo frames line the stone deck. A "
            "board near the stairs lists departures, delays, and cancelled "
            "runs beneath the talon-and-bar seal of Thirteenth Talon Command."
        ),
        room_type="building",
        indoor=False,
    )

    dc_observation_walk = area.room(
        "dc_observation_walk",
        name="Observation Walk",
        desc=(
            "A narrow elevated walk runs beside the handler ring and courier "
            "stairs, used by officers, clerks, and select visitors with the "
            "right seals. From here one can study the routines of the enclave "
            "without interrupting them, which is exactly what the walk was "
            "built to permit."
        ),
        room_type="building",
        indoor=False,
    )

    dc_feed_court = area.room(
        "dc_feed_court",
        name="Feed Court",
        desc=(
            "Water troughs, feed bins, and inspection rails fill a stone court "
            "where handler crews prepare outbound loads and calm restless bodies "
            "before launch schedules tighten. The place is kept nearly spotless, "
            "which only makes its scale more unsettling."
        ),
        room_type="path",
        indoor=False,
    )

    dc_manifest_rail = area.room(
        "dc_manifest_rail",
        name="Manifest Rail",
        desc=(
            "A long brass rail holds clipped route manifests, rider clearances, "
            "tack issue sheets, and disciplinary notices for Thirteenth Talon "
            "Command. Some route boards have been re-cut so often the wood shows "
            "ghost lines beneath the current lettering."
        ),
        room_type="building",
        indoor=False,
    )

    dc_chain_lift = area.room(
        "dc_chain_lift",
        name="Chain Lift",
        desc=(
            "Heavy chains, counterweights, and pulley housings move cargo and "
            "secured equipment between the open yards above and the restricted "
            "maintenance passages below. Every crank stroke is logged on a slate "
            "board within arm's reach."
        ),
        room_type="building",
        indoor=False,
    )

    dc_restricted_tunnel = area.room(
        "dc_restricted_tunnel",
        name="Restricted Tunnel",
        desc=(
            "A low stone tunnel runs beneath the enclave, wide enough for carts "
            "but too narrow for comfort. Tool racks line the walls beside chained "
            "inspection lamps and old repair alcoves. The silence here is broken "
            "only by drip water and the distant clank of the chain lift."
        ),
        room_type="underground",
        indoor=True,
    )

    dc_quarantine_pens = area.room(
        "dc_quarantine_pens",
        name="Quarantine Pens",
        desc=(
            "Partitioned holding pens and fenced treatment lanes sit at the edge "
            "of the enclave for animals, tack, and cargo requiring inspection "
            "before release. The notices here are clinical, procedural, and full "
            "of penalties. Compassion appears nowhere on the posted rules."
        ),
        room_type="building",
        indoor=False,
    )

    dc_dispatch_office = area.room(
        "dc_dispatch_office",
        name="Dispatch Office",
        desc=(
            "Departure ledgers, route tables, suspension notices, and weather "
            "summaries cover the walls of this cramped office in layered civic "
            "order. Nothing leaves the platform network without being reduced to "
            "a line entry here first."
        ),
        room_type="building",
        indoor=True,
    )

    dc_weather_balcony = area.room(
        "dc_weather_balcony",
        name="Weather Balcony",
        desc=(
            "Wind vanes, storm plates, and calibrated signal ribbons line the "
            "balcony where dispatch crews track the capital's changing air. The "
            "view is broad enough to humble anyone still pretending routes are "
            "only about courage and not about conditions."
        ),
        room_type="building",
        indoor=False,
    )

    dc_scale_wash = area.room(
        "dc_scale_wash",
        name="Scale Wash",
        desc=(
            "Troughs, brushes, chain drains, and stacks of drying cloth make this "
            "a hard-working service room more than a ceremonial one. The enclave "
            "depends on places like this and rarely admits it."
        ),
        room_type="building",
        indoor=True,
    )

    dc_repair_bay = area.room(
        "dc_repair_bay",
        name="Repair Bay",
        desc=(
            "Harness frames, wheel stands, travel cages, and metal fittings are "
            "laid out for inspection and repair in a broad stone bay open to the "
            "yard. Every part here has failed once or is expected to soon."
        ),
        room_type="building",
        indoor=False,
    )

    dc_roster_hall = area.room(
        "dc_roster_hall",
        name="Roster Hall",
        desc=(
            "Duty boards, posted shifts, and clipped talon-and-bar tags line the "
            "walls of this narrow hall. Names mean less here than assignment, "
            "clearance, and whether someone is late."
        ),
        room_type="building",
        indoor=True,
    )

    dc_cargo_loft = area.room(
        "dc_cargo_loft",
        name="Cargo Loft",
        desc=(
            "Raised platforms and chain guides hold outbound satchels, secured "
            "crates, and strapped dispatch bundles awaiting the next legal moment "
            "to move. The loft feels built for weight and secrecy in equal measure."
        ),
        room_type="building",
        indoor=True,
    )

    dc_signal_cage = area.room(
        "dc_signal_cage",
        name="Signal Cage",
        desc=(
            "A latticed station of flags, lamp shutters, and weather boards gives "
            "the cage a view over the courtyards and roofs below. The city speaks "
            "to itself in signals here, and very little of that speech is public."
        ),
        room_type="building",
        indoor=False,
    )

    dc_harness_loft = area.room(
        "dc_harness_loft",
        name="Harness Loft",
        desc=(
            "Suspended racks of fitted harness, spare straps, buckle rolls, and "
            "travel nets sway gently in the loft above the tack lanes. Everything "
            "is labeled, counted, and one failure away from urgent use."
        ),
        room_type="building",
        indoor=True,
    )

    dc_officers_gallery = area.room(
        "dc_officers_gallery",
        name="Officers' Gallery",
        desc=(
            "A restrained gallery of route charts, older command rosters, and "
            "observation windows lets ranking officers study the enclave without "
            "joining its labor. Distance is part of authority here."
        ),
        room_type="building",
        indoor=False,
    )

    # ==================================================================
    #  DISTRICT 6: CIRCLE DISTRICT
    #  Survey work, sanctioned studies, and controlled magical trade.
    # ==================================================================

    cd_sealed_gate = area.room(
        "cd_sealed_gate",
        name="Sealed Gate",
        desc=(
            "The entrance to the Circle District is less ornate than expected, "
            "a severe wall and gate marked with survey sigils and civic seals "
            "rather than flourishes. Visitors are expected to understand that "
            "permission matters more than spectacle here."
        ),
        room_type="building",
        indoor=False,
    )

    cd_survey_cloister = area.room(
        "cd_survey_cloister",
        name="Survey Cloister",
        desc=(
            "Arcaded stone walks enclose tables of measured rods, wax tablets, "
            "inked rubbings, and pinned route diagrams. Apprentices carry "
            "copy bundles from desk to desk while senior surveyors debate "
            "angles, subsidence, and the wording of public reports."
        ),
        room_type="building",
        indoor=True,
    )

    cd_lens_court = area.room(
        "cd_lens_court",
        name="Lens Court",
        desc=(
            "A quiet court of polished stone lies beneath suspended brass "
            "frames and fixed viewing lenses used for sanctioned inspection. "
            "The place feels part laboratory, part legal chamber. Even the "
            "light seems sorted before it is allowed to touch the floor."
        ),
        room_type="building",
        indoor=False,
    )

    cd_attic_archive = area.room(
        "cd_attic_archive",
        name="Attic Archive",
        desc=(
            "The upper archive holds rolled survey copies, layered site "
            "sketches, and boxes of rejected calculations tied shut with "
            "fading cords. Marginal notes crowd the stored pages. Some look "
            "like corrections; some look like arguments nobody wished to have "
            "in public."
        ),
        room_type="building",
        indoor=True,
    )

    cd_apothecary = area.room(
        "cd_apothecary",
        name="Measured Apothecary",
        desc=(
            "Stoppered jars, dried herbs, powders, and distilled preparations "
            "line the walls of this regulated apothecary. Every shelf bears a "
            "copy mark and price slate. Nothing is sold casually, but almost "
            "everything has been priced, indexed, and labeled."
        ),
        room_type="building",
        indoor=True,
    )

    cd_copy_hall = area.room(
        "cd_copy_hall",
        name="Copy Hall",
        desc=(
            "This long chamber is given over to clean sanctioned copies of site "
            "notes, survey abstracts, and public-facing advisories. Racks of "
            "discarded draft language stand near the hearth, reminding everyone "
            "that truth is only one phase of publication."
        ),
        room_type="building",
        indoor=True,
    )

    cd_revision_gallery = area.room(
        "cd_revision_gallery",
        name="Revision Gallery",
        desc=(
            "Mounted drafts, correction slates, and revised notice boards line "
            "this internal gallery where Circle and civic language are brought "
            "into agreement. Many final public phrases look softer here than the "
            "versions pinned beneath them."
        ),
        room_type="building",
        indoor=True,
    )

    cd_calibration_cell = area.room(
        "cd_calibration_cell",
        name="Calibration Cell",
        desc=(
            "Balanced tables, nested measure rings, and marked lenses fill a "
            "sealed work cell used for fine instrument alignment. The room is "
            "quiet enough that the scratch of a quill sounds intrusive. Precision "
            "here is treated as both craft and authority."
        ),
        room_type="building",
        indoor=True,
    )

    cd_undercroft = area.room(
        "cd_undercroft",
        name="Survey Undercroft",
        desc=(
            "Below the formal district lies an undercroft of spare frames, "
            "retired lenses, broken markers, and bundled notes awaiting either "
            "reuse or destruction. The air is dry and mineral. One gets the "
            "sense that this is where inconvenient work waits to become invisible."
        ),
        room_type="underground",
        indoor=True,
    )

    cd_powder_store = area.room(
        "cd_powder_store",
        name="Powder Store",
        desc=(
            "Measured packets of survey chalk, alchemical powders, drying salts, "
            "and sealing compounds sit behind latticed cupboards in the powder "
            "store. Every shelf carries a quantity slate, and every slate carries "
            "a signature line beneath it."
        ),
        room_type="building",
        indoor=True,
    )

    cd_reagent_garden = area.room(
        "cd_reagent_garden",
        name="Reagent Garden",
        desc=(
            "Raised beds of bitter herbs, silverleaf cuttings, drying reeds, and "
            "marked roots fill a walled garden under strict copy boards listing "
            "yield, use, and disposal rules. Even living things are cataloged "
            "here as if they had filed for permission."
        ),
        room_type="path",
        indoor=False,
    )

    cd_glasshouse = area.room(
        "cd_glasshouse",
        name="Measured Glasshouse",
        desc=(
            "Warm panes and brass frames shelter trays of delicate growths used "
            "for reagents, tinctures, and sanctioned experiments. Moisture beads "
            "on the glass around clipped labels and correction notes written in a "
            "hand too neat to be accidental."
        ),
        room_type="building",
        indoor=True,
    )

    cd_quietium_chamber = area.room(
        "cd_quietium_chamber",
        name="Quietium Chamber",
        desc=(
            "Soft wall cloth, padded cabinets, and low benches make this chamber "
            "feel restrained to the point of suspicion. Delicate measurements and "
            "fragile discussions are both apparently expected to occur here."
        ),
        room_type="building",
        indoor=True,
    )

    cd_reference_vault = area.room(
        "cd_reference_vault",
        name="Reference Vault",
        desc=(
            "Bound abstracts, sealed field copies, and catalog rods fill a vault "
            "used for the sanctioned memory of the district. It is not the oldest "
            "material that matters here, but the version judged safe to consult."
        ),
        room_type="building",
        indoor=True,
    )

    cd_lecture_ambulatory = area.room(
        "cd_lecture_ambulatory",
        name="Lecture Ambulatory",
        desc=(
            "Tiered benches curve along a covered walk where lessons, briefings, "
            "and sanctioned interpretations are delivered to apprentices and visitors. "
            "Knowledge is organized here by permission before curiosity."
        ),
        room_type="building",
        indoor=False,
    )

    cd_binding_hall = area.room(
        "cd_binding_hall",
        name="Binding Hall",
        desc=(
            "Tables of waxed thread, press boards, cover plates, and trimming knives "
            "line the hall where loose survey work becomes durable official record. "
            "The district trusts a bound page more than a memory."
        ),
        room_type="building",
        indoor=True,
    )

    cd_specimen_archive = area.room(
        "cd_specimen_archive",
        name="Specimen Archive",
        desc=(
            "Shelved boxes, labeled jars, and wrapped samples rest in orderly rows "
            "behind copy marks and caution placards. The archive makes even oddities "
            "feel administrative."
        ),
        room_type="building",
        indoor=True,
    )

    cd_measure_tower = area.room(
        "cd_measure_tower",
        name="Measure Tower",
        desc=(
            "From the upper stage of the tower, the district's courts and the capital's "
            "ordered avenues seem to align into a single thesis about control. Rod marks "
            "cut into the parapet show this height has long been used to judge the world below."
        ),
        room_type="building",
        indoor=False,
    )

    cd_silent_cloister = area.room(
        "cd_silent_cloister",
        name="Silent Cloister",
        desc=(
            "A narrow cloister of shaded arches and quiet benches separates the more public "
            "rooms from the district's finer work. Even the wind seems to lower its voice here."
        ),
        room_type="building",
        indoor=False,
    )

    # ==================================================================
    #  DISTRICT 7: NOBLE HEIGHTS
    #  Patronage, preserve interests, and private archives.
    # ==================================================================

    nh_processional = area.room(
        "nh_processional",
        name="High Processional",
        desc=(
            "The street climbs above the common traffic into cleaner air and "
            "quieter stone. House walls rise on either side, broken by guarded "
            "arches, trimmed lanterns, and discreet family emblems. The city "
            "still governs here, but it governs with softer shoes."
        ),
        room_type="path",
        indoor=False,
    )

    nh_salon_steps = area.room(
        "nh_salon_steps",
        name="Salon Steps",
        desc=(
            "Wide steps lead to a terrace where invitations, influence, and "
            "careful rumor pass between polished hands. Servants move wine, "
            "documents, and sealed cases through the colonnade while petitioners "
            "wait below for the chance to matter to somebody important."
        ),
        room_type="building",
        indoor=False,
    )

    nh_garden_terrace = area.room(
        "nh_garden_terrace",
        name="Garden Terrace",
        desc=(
            "The terrace looks outward over clipped hedges, narrow water "
            "channels, and carefully placed stonework meant to suggest ease. "
            "Boundary markers from the Stagcrown Revision stand beside older "
            "stones whose original purpose has been buried under noble taste."
        ),
        room_type="path",
        indoor=False,
    )

    nh_private_archive = area.room(
        "nh_private_archive",
        name="Private Charter Archive",
        desc=(
            "Cabinets of copied charters, preserve rights, line maps, and "
            "sealed family records fill the private archive. Unlike the public "
            "records of the Ministry Ward, these copies are curated rather "
            "than comprehensive. What is omitted is as revealing as what is "
            "preserved."
        ),
        room_type="building",
        indoor=True,
    )

    nh_preserve_gate = area.room(
        "nh_preserve_gate",
        name="Preserve Gate",
        desc=(
            "An elegant gate of worked stone and iron screens the noble road "
            "leading toward the hunting grounds beyond the city. Guards posted "
            "here inspect writs with far more courtesy than the customs hall "
            "ever offers. This is the stable city-side boundary for the "
            "stagcrown route."
        ),
        room_type="path",
        indoor=False,
    )

    nh_house_talvere_portico = area.room(
        "nh_house_talvere_portico",
        name="House Talvere Portico",
        desc=(
            "The Talvere portico is all measured arches, dark lanterns, and the "
            "subtle suggestion that roads, gates, and order themselves are part "
            "of the family's inheritance. Retainers keep the approach clear while "
            "guests are evaluated long before anyone greets them."
        ),
        room_type="building",
        indoor=False,
    )

    nh_guest_loggia = area.room(
        "nh_guest_loggia",
        name="Guest Loggia",
        desc=(
            "A long covered gallery overlooks the lower city through carved "
            "screens while chamberlains sort callers by rank, urgency, and "
            "patron worth. Guest rolls, invitation boards, and quiet refusals "
            "all begin in the same courteous voice."
        ),
        room_type="building",
        indoor=False,
    )

    nh_rhest_colonnade = area.room(
        "nh_rhest_colonnade",
        name="House Rhest Colonnade",
        desc=(
            "The Rhest colonnade balances private elegance with public record. "
            "Plaques celebrating preserve reform stand beside locked cabinets of "
            "charter copies and hunting licenses. Wealth here prefers to dress "
            "itself as stewardship."
        ),
        room_type="building",
        indoor=False,
    )

    nh_mirror_green = area.room(
        "nh_mirror_green",
        name="Mirror Green",
        desc=(
            "A narrow green of clipped grass and reflecting basins lies between "
            "house walls, its symmetry broken only by old stones built into the "
            "garden edges. Their original cuts do not match the later noble work. "
            "Something older was made decorative here."
        ),
        room_type="path",
        indoor=False,
    )

    nh_servants_postern = area.room(
        "nh_servants_postern",
        name="Servants' Postern",
        desc=(
            "The service postern is plain compared to the district's formal "
            "facades, used by carriers, private guards, kitchen staff, and the "
            "people who make noble discretion function. Delivery crates and wax "
            "scrap show that influence requires an enormous amount of routine labor."
        ),
        room_type="building",
        indoor=True,
    )

    nh_patron_registry = area.room(
        "nh_patron_registry",
        name="Patron Registry",
        desc=(
            "A discreet office of guest rolls, invitation cards, and sponsor ledgers "
            "tracks who owes courtesy to whom in Noble Heights. Influence here is "
            "recorded with the same seriousness the lower city reserves for freight."
        ),
        room_type="building",
        indoor=True,
    )

    nh_hunt_map_gallery = area.room(
        "nh_hunt_map_gallery",
        name="Hunt Map Gallery",
        desc=(
            "Framed preserve charts, lodge routes, game counts, and boundary copies "
            "line a gallery meant to display stewardship as taste. Close study shows "
            "how often the maps have been redrafted to keep privilege looking natural."
        ),
        room_type="building",
        indoor=True,
    )

    nh_kitchen_court = area.room(
        "nh_kitchen_court",
        name="Kitchen Court",
        desc=(
            "Delivery carts, coal bins, cistern barrels, and servant benches crowd "
            "the service court behind the district's polished facades. The smells of "
            "bread, soap, and hot grease remind you how much labor props up refinement."
        ),
        room_type="path",
        indoor=False,
    )

    nh_garden_wall = area.room(
        "nh_garden_wall",
        name="Garden Wall Walk",
        desc=(
            "A narrow walk runs atop part of the old retaining wall, overlooking "
            "terraces that now pretend they were always gardens. Older stone courses "
            "show beneath the noble improvements like a history refusing full burial."
        ),
        room_type="path",
        indoor=False,
    )

    nh_talvere_gallery = area.room(
        "nh_talvere_gallery",
        name="Talvere Gallery",
        desc=(
            "Road charters, civic gifts, and measured ceremonial pieces are displayed "
            "here with the confidence of a house that expects infrastructure itself to "
            "read as pedigree."
        ),
        room_type="building",
        indoor=True,
    )

    nh_rhest_salon = area.room(
        "nh_rhest_salon",
        name="Rhest Salon",
        desc=(
            "Soft chairs, quiet decanters, preserve sketches, and invitation trays make "
            "the salon feel intimate until one notices how carefully every conversation "
            "can be managed from its corners."
        ),
        room_type="building",
        indoor=True,
    )

    nh_carriage_court = area.room(
        "nh_carriage_court",
        name="Carriage Court",
        desc=(
            "Private coaches, liveried attendants, and polished hitch rails occupy the "
            "court behind the district's formal entries. Here privilege looks less like "
            "inheritance and more like logistics with better polish."
        ),
        room_type="path",
        indoor=False,
    )

    nh_guest_garden = area.room(
        "nh_guest_garden",
        name="Guest Garden",
        desc=(
            "A carefully secluded garden offers benches, narrow water channels, and "
            "screened paths where important visitors can be courted away from public hearing. "
            "Its calm feels expensive because it is."
        ),
        room_type="path",
        indoor=False,
    )

    nh_lodge_office = area.room(
        "nh_lodge_office",
        name="Lodge Office",
        desc=(
            "Preserve bookings, hunting allotments, carriage schedules, and private "
            "guest notes are managed here with a courtesy sharpened by exclusivity. "
            "The office turns leisure into a chain of permissions."
        ),
        room_type="building",
        indoor=True,
    )

    # ==================================================================
    #  DISTRICT 8: HIDDEN WARRENS
    #  Drains, cellar routes, smuggling corners, and a print cellar.
    # ==================================================================

    hw_drain_steps = area.room(
        "hw_drain_steps",
        name="Drain Steps",
        desc=(
            "A narrow stair drops below Shrine Lane into damp masonry that "
            "smells of runoff, lamp oil, and old paper. The upper city is "
            "still audible above, but muffled now, as if respectability were "
            "only a ceiling away."
        ),
        room_type="underground",
        indoor=True,
    )

    hw_smuggler_lantern = area.room(
        "hw_smuggler_lantern",
        name="The Smuggler's Lantern",
        desc=(
            "A cellar room lit by hooded lamps and patience serves as a quiet "
            "exchange point for whatever the public city prices too highly or "
            "forbids too loudly. Nothing is displayed unless asked for. The "
            "walls remember older uses beneath the plaster."
        ),
        room_type="underground",
        indoor=True,
    )

    hw_print_cellar = area.room(
        "hw_print_cellar",
        name="Print Cellar",
        desc=(
            "Trays of type, ink blocks, drying sheets, and burnt candle ends "
            "crowd this cramped cellar. Handbills are stacked beneath false "
            "bottoms and wrapped in ordinary account paper. The work done here "
            "is less dramatic than rebellion songs and more dangerous than it "
            "sounds: careful copying, careful editing, careful circulation."
        ),
        room_type="underground",
        indoor=True,
    )

    hw_ratwalk = area.room(
        "hw_ratwalk",
        name="Ratwalk",
        desc=(
            "A narrow ledge and service path runs above a broad drain channel, "
            "its stones slick with age and patched mortar. Crates have been "
            "stored here before, and men have lain in wait here before that. "
            "The place invites crouched movement and bad decisions."
        ),
        room_type="underground",
        indoor=True,
    )

    hw_old_cistern = area.room(
        "hw_old_cistern",
        name="Old Cistern",
        desc=(
            "The cistern chamber is older than the warrens built around it, "
            "its fitted stones marked by channels and cut numbers no current "
            "city mason would choose. The water basin has long been drained, "
            "but the chamber still smells faintly mineral and cold. Someone "
            "has used the dry ledges for meetings, caches, and hurried exits."
        ),
        room_type="underground",
        indoor=True,
    )

    hw_burnt_store = area.room(
        "hw_burnt_store",
        name="Burnt Store",
        desc=(
            "Charred shelving and smoke-blackened stone mark a store room that "
            "once held more than anyone expected to lose. Bundles salvaged from "
            "the fire are hidden behind stacked jars and false boards. The room "
            "still smells of ash each time the air shifts."
        ),
        room_type="underground",
        indoor=True,
    )

    hw_cinder_loft = area.room(
        "hw_cinder_loft",
        name="Cinder Loft",
        desc=(
            "A cramped loft above the print cellar holds paper bundles wrapped "
            "in ordinary account sheets, coded drop lists, and handbills marked "
            "with the ash-cinder cipher. The loft is careful rather than dramatic. "
            "That is why it still functions."
        ),
        room_type="underground",
        indoor=True,
    )

    hw_dead_drop_drain = area.room(
        "hw_dead_drop_drain",
        name="Dead Drop Drain",
        desc=(
            "The drain narrows here around a dry shelf used for quiet exchanges "
            "and things meant to wait unseen. Pebbles have been arranged as markers "
            "more than once, then kicked aside again. The place is all temporary "
            "signals and permanent risk."
        ),
        room_type="underground",
        indoor=True,
    )

    hw_sump_bridge = area.room(
        "hw_sump_bridge",
        name="Sump Bridge",
        desc=(
            "A narrow stone bridge crosses a black water sump where runoff, lost "
            "objects, and city secrets gather together. Maintenance hooks line the "
            "walls, though some of the more recent scratches belong to smugglers "
            "and watchers rather than repair crews."
        ),
        room_type="underground",
        indoor=True,
    )

    hw_watch_niche = area.room(
        "hw_watch_niche",
        name="Watch Niche",
        desc=(
            "This cramped recess overlooks the sump bridge through a broken arch "
            "and gives just enough room for a lamp, a listener, and a knife. Marks "
            "in the stone show it has served as lookout, ambush point, and hurried "
            "meeting place in roughly equal measure."
        ),
        room_type="underground",
        indoor=True,
    )

    hw_ink_sink = area.room(
        "hw_ink_sink",
        name="Ink Sink",
        desc=(
            "A cracked work sink, pigment bowls, wet rags, and stripped type trays "
            "make this little chamber smell of oil, metal, and spoiled paper. Failed "
            "proofs are washed down here when they cannot safely be kept."
        ),
        room_type="underground",
        indoor=True,
    )

    hw_chain_cache = area.room(
        "hw_chain_cache",
        name="Chain Cache",
        desc=(
            "Hooks in the ceiling hold wrapped bundles of chain, lamp cages, and "
            "cargo fittings that never went through a proper registry. The cache is "
            "organized with a professionalism the city would call criminal and then use."
        ),
        room_type="underground",
        indoor=True,
    )

    hw_sluice_gate = area.room(
        "hw_sluice_gate",
        name="Sluice Gate",
        desc=(
            "A heavy iron gate controls old runoff channels that still connect parts "
            "of the capital more honestly than its streets do. Cut marks on the stone "
            "suggest repeated adjustment, older than the most recent hardware."
        ),
        room_type="underground",
        indoor=True,
    )

    hw_gutter_oratory = area.room(
        "hw_gutter_oratory",
        name="Gutter Oratory",
        desc=(
            "Someone once turned this alcove into a place for low-voiced meetings, "
            "warnings, and promises made without witnesses. Wax drips, charcoal marks, "
            "and hidden niches show how often the city drives its truths underground."
        ),
        room_type="underground",
        indoor=True,
    )

    hw_runner_dormer = area.room(
        "hw_runner_dormer",
        name="Runner Dormer",
        desc=(
            "Blankets, satchels, spare boots, and rolled handbills are packed into "
            "a cramped dormer where couriers too unofficial for the surface rest in "
            "short, uneasy shifts."
        ),
        room_type="underground",
        indoor=True,
    )

    hw_false_store = area.room(
        "hw_false_store",
        name="False Store",
        desc=(
            "Shelves of ordinary jars and spoiled grain conceal deeper compartments "
            "used to hide anything the warrens cannot afford to lose. The room succeeds "
            "by appearing not worth a second look."
        ),
        room_type="underground",
        indoor=True,
    )

    hw_culvert_crossing = area.room(
        "hw_culvert_crossing",
        name="Culvert Crossing",
        desc=(
            "Old culvert arches cross here beneath the city like bones beneath flesh. "
            "The route is inconvenient enough to discourage the curious and useful "
            "enough to reward the determined."
        ),
        room_type="underground",
        indoor=True,
    )

    hw_ash_nook = area.room(
        "hw_ash_nook",
        name="Ash Nook",
        desc=(
            "Burnt scraps, soot jars, and wrapped type blocks fill a little nook used "
            "for destroying the wrong copies and preserving the right ones. It smells "
            "like failure put to practical use."
        ),
        room_type="underground",
        indoor=True,
    )

    hw_grate_ladder = area.room(
        "hw_grate_ladder",
        name="Grate Ladder",
        desc=(
            "An iron ladder climbs to a maintenance grate beneath the city, giving the "
            "warrens another discreet way to breathe up toward the respectable world. "
            "The rungs shine where many hands have used them in haste."
        ),
        room_type="underground",
        indoor=True,
    )

    # ==================================================================
    #  EXITS
    # ==================================================================

    area.exit(ca_crownroad_gate, ca_gatehouse, "north")
    area.exit(ca_gatehouse, ca_crownroad_gate, "south")
    area.exit(ca_crownroad_gate, "crownroad_north:om_gate_verge", "south")
    area.exit(ca_gatehouse, ca_customs_hall, "north")
    area.exit(ca_customs_hall, ca_gatehouse, "south")
    area.exit(ca_customs_hall, ca_arrival_court, "north")
    area.exit(ca_arrival_court, ca_customs_hall, "south")
    area.exit(ca_arrival_court, ca_processional_way, "north")
    area.exit(ca_processional_way, ca_arrival_court, "south")
    area.exit(ca_arrival_court, ca_watch_platform, "up")
    area.exit(ca_watch_platform, ca_arrival_court, "down")
    area.exit(ca_crownroad_gate, ca_manifest_yard, "east")
    area.exit(ca_manifest_yard, ca_crownroad_gate, "west")
    area.exit(ca_manifest_yard, ca_porters_shelter, "south")
    area.exit(ca_porters_shelter, ca_manifest_yard, "north")
    area.exit(ca_gatehouse, ca_tally_steps, "east")
    area.exit(ca_tally_steps, ca_gatehouse, "west")
    area.exit(ca_tally_steps, ca_assessor_gallery, "up")
    area.exit(ca_assessor_gallery, ca_tally_steps, "down")
    area.exit(ca_assessor_gallery, ca_toll_archive, "east")
    area.exit(ca_toll_archive, ca_assessor_gallery, "west")
    area.exit(ca_manifest_yard, ca_caravan_court, "north")
    area.exit(ca_caravan_court, ca_manifest_yard, "south")
    area.exit(ca_caravan_court, ca_levy_office, "east")
    area.exit(ca_levy_office, ca_caravan_court, "west")
    area.exit(ca_manifest_yard, ca_seized_goods_shed, "east")
    area.exit(ca_seized_goods_shed, ca_manifest_yard, "west")
    area.exit(ca_watch_platform, ca_milebar_balcony, "east")
    area.exit(ca_milebar_balcony, ca_watch_platform, "west")
    area.exit(ca_milebar_balcony, ca_toll_archive, "south")
    area.exit(ca_toll_archive, ca_milebar_balcony, "north")
    area.exit(ca_gatehouse, ca_queue_lane, "west")
    area.exit(ca_queue_lane, ca_gatehouse, "east")
    area.exit(ca_queue_lane, ca_caravan_court, "northeast")
    area.exit(ca_caravan_court, ca_queue_lane, "southwest")
    area.exit(ca_queue_lane, ca_levy_office, "west")
    area.exit(ca_levy_office, ca_queue_lane, "east")
    area.exit(ca_levy_office, ca_measure_house, "north")
    area.exit(ca_measure_house, ca_levy_office, "south")
    area.exit(ca_caravan_court, ca_guard_colonnade, "west")
    area.exit(ca_guard_colonnade, ca_caravan_court, "east")
    area.exit(ca_guard_colonnade, ca_relief_yard, "north")
    area.exit(ca_relief_yard, ca_guard_colonnade, "south")
    area.exit(ca_relief_yard, ca_waybill_office, "east")
    area.exit(ca_waybill_office, ca_relief_yard, "west")
    area.exit(ca_waybill_office, ca_assessor_gallery, "south")
    area.exit(ca_assessor_gallery, ca_waybill_office, "north")

    area.exit(ca_processional_way, oc_scale_square, "north")
    area.exit(oc_scale_square, ca_processional_way, "south")
    area.exit(oc_scale_square, oc_red_market, "east")
    area.exit(oc_red_market, oc_scale_square, "west")
    area.exit(oc_scale_square, oc_wayfarer_inn, "west")
    area.exit(oc_wayfarer_inn, oc_scale_square, "east")
    area.exit(oc_scale_square, oc_exchange_hall, "north")
    area.exit(oc_exchange_hall, oc_scale_square, "south")
    area.exit(oc_scale_square, oc_shrine_lane, "northwest")
    area.exit(oc_shrine_lane, oc_scale_square, "southeast")
    area.exit(oc_scale_square, oc_carter_row, "northeast")
    area.exit(oc_carter_row, oc_scale_square, "southwest")
    area.exit(oc_red_market, oc_carter_row, "north")
    area.exit(oc_carter_row, oc_red_market, "south")
    area.exit(oc_red_market, oc_ragcourt, "east")
    area.exit(oc_ragcourt, oc_red_market, "west")
    area.exit(oc_wayfarer_inn, oc_lodger_alley, "west")
    area.exit(oc_lodger_alley, oc_wayfarer_inn, "east")
    area.exit(oc_exchange_hall, oc_coinstairs, "east")
    area.exit(oc_coinstairs, oc_exchange_hall, "west")
    area.exit(oc_shrine_lane, oc_stewpot_arcade, "north")
    area.exit(oc_stewpot_arcade, oc_shrine_lane, "south")
    area.exit(oc_carter_row, oc_teamyard, "north")
    area.exit(oc_teamyard, oc_carter_row, "south")
    area.exit(oc_ragcourt, oc_coinstairs, "north")
    area.exit(oc_coinstairs, oc_ragcourt, "south")
    area.exit(oc_red_market, oc_tinkers_row, "northwest")
    area.exit(oc_tinkers_row, oc_red_market, "southeast")
    area.exit(oc_tinkers_row, oc_cloth_hall, "east")
    area.exit(oc_cloth_hall, oc_tinkers_row, "west")
    area.exit(oc_coinstairs, oc_broker_steps, "north")
    area.exit(oc_broker_steps, oc_coinstairs, "south")
    area.exit(oc_lodger_alley, oc_public_baths, "north")
    area.exit(oc_public_baths, oc_lodger_alley, "south")
    area.exit(oc_public_baths, oc_stewpot_arcade, "east")
    area.exit(oc_stewpot_arcade, oc_public_baths, "west")
    area.exit(oc_tinkers_row, oc_artisans_court, "north")
    area.exit(oc_artisans_court, oc_tinkers_row, "south")
    area.exit(oc_artisans_court, oc_lantern_row, "east")
    area.exit(oc_lantern_row, oc_artisans_court, "west")
    area.exit(oc_lantern_row, oc_cloth_hall, "north")
    area.exit(oc_cloth_hall, oc_lantern_row, "south")
    area.exit(oc_broker_steps, oc_scribes_corner, "east")
    area.exit(oc_scribes_corner, oc_broker_steps, "west")
    area.exit(oc_scribes_corner, oc_hawkers_walk, "north")
    area.exit(oc_hawkers_walk, oc_scribes_corner, "south")
    area.exit(oc_teamyard, oc_teamsters_hall, "east")
    area.exit(oc_teamsters_hall, oc_teamyard, "west")
    area.exit(oc_teamsters_hall, oc_broker_steps, "northwest")
    area.exit(oc_broker_steps, oc_teamsters_hall, "southeast")
    area.exit(oc_hawkers_walk, oc_artisans_court, "southwest")
    area.exit(oc_artisans_court, oc_hawkers_walk, "northeast")

    area.exit(oc_scale_square, mw_decree_wall, "southwest")
    area.exit(mw_decree_wall, oc_scale_square, "northeast")
    area.exit(mw_decree_wall, mw_permit_hall, "east")
    area.exit(mw_permit_hall, mw_decree_wall, "west")
    area.exit(mw_decree_wall, mw_records_arcade, "west")
    area.exit(mw_records_arcade, mw_decree_wall, "east")
    area.exit(mw_records_arcade, mw_registry_annex, "north")
    area.exit(mw_registry_annex, mw_records_arcade, "south")
    area.exit(mw_records_arcade, mw_causeway_postern, "west")
    area.exit(mw_causeway_postern, mw_records_arcade, "east")
    area.exit(mw_causeway_postern, "old_causeway:bs_postern_landing", "west")
    area.exit(mw_permit_hall, mw_seal_chamber, "north")
    area.exit(mw_seal_chamber, mw_permit_hall, "south")
    area.exit(mw_seal_chamber, mw_copyists_walk, "west")
    area.exit(mw_copyists_walk, mw_seal_chamber, "east")
    area.exit(mw_copyists_walk, mw_correction_office, "north")
    area.exit(mw_correction_office, mw_copyists_walk, "south")
    area.exit(mw_correction_office, mw_confiscation_room, "east")
    area.exit(mw_confiscation_room, mw_correction_office, "west")
    area.exit(mw_registry_annex, mw_charter_vault, "east")
    area.exit(mw_charter_vault, mw_registry_annex, "west")
    area.exit(mw_charter_vault, mw_confiscation_room, "north")
    area.exit(mw_confiscation_room, mw_charter_vault, "south")
    area.exit(mw_permit_hall, mw_petition_cloister, "east")
    area.exit(mw_petition_cloister, mw_permit_hall, "west")
    area.exit(mw_petition_cloister, mw_notary_room, "north")
    area.exit(mw_notary_room, mw_petition_cloister, "south")
    area.exit(mw_notary_room, mw_witness_chamber, "east")
    area.exit(mw_witness_chamber, mw_notary_room, "west")
    area.exit(mw_copyists_walk, mw_ink_store, "south")
    area.exit(mw_ink_store, mw_copyists_walk, "north")
    area.exit(mw_ink_store, mw_petition_cloister, "northeast")
    area.exit(mw_petition_cloister, mw_ink_store, "southwest")
    area.exit(mw_petition_cloister, mw_review_court, "northeast")
    area.exit(mw_review_court, mw_petition_cloister, "southwest")
    area.exit(mw_review_court, mw_docket_room, "east")
    area.exit(mw_docket_room, mw_review_court, "west")
    area.exit(mw_docket_room, mw_archive_stair, "north")
    area.exit(mw_archive_stair, mw_docket_room, "south")
    area.exit(mw_archive_stair, mw_public_records, "east")
    area.exit(mw_public_records, mw_archive_stair, "west")
    area.exit(mw_review_court, mw_seal_brazier, "west")
    area.exit(mw_seal_brazier, mw_review_court, "east")
    area.exit(mw_seal_brazier, mw_notary_room, "south")
    area.exit(mw_notary_room, mw_seal_brazier, "north")
    area.exit(mw_public_records, mw_records_arcade, "southwest")
    area.exit(mw_records_arcade, mw_public_records, "northeast")

    area.exit(oc_scale_square, mq_barracks_yard, "southeast")
    area.exit(mq_barracks_yard, oc_scale_square, "northwest")
    area.exit(mq_barracks_yard, mq_drill_green, "north")
    area.exit(mq_drill_green, mq_barracks_yard, "south")
    area.exit(mq_barracks_yard, mq_armory_lane, "east")
    area.exit(mq_armory_lane, mq_barracks_yard, "west")
    area.exit(mq_drill_green, mq_infirmary, "east")
    area.exit(mq_infirmary, mq_drill_green, "west")
    area.exit(mq_armory_lane, mq_escarpment_road, "north")
    area.exit(mq_escarpment_road, mq_armory_lane, "south")
    area.exit(mq_escarpment_road, "ironvein_escarpment:sr_gate_grade", "north")
    area.exit(mq_barracks_yard, mq_muster_hall, "south")
    area.exit(mq_muster_hall, mq_barracks_yard, "north")
    area.exit(mq_muster_hall, mq_supply_depot, "east")
    area.exit(mq_supply_depot, mq_muster_hall, "west")
    area.exit(mq_supply_depot, mq_armory_lane, "north")
    area.exit(mq_armory_lane, mq_supply_depot, "south")
    area.exit(mq_drill_green, mq_signal_tower, "north")
    area.exit(mq_signal_tower, mq_drill_green, "south")
    area.exit(mq_infirmary, mq_detention_block, "south")
    area.exit(mq_detention_block, mq_infirmary, "north")
    area.exit(mq_supply_depot, mq_detention_block, "east")
    area.exit(mq_detention_block, mq_supply_depot, "west")
    area.exit(mq_armory_lane, mq_ordnance_shed, "east")
    area.exit(mq_ordnance_shed, mq_armory_lane, "west")
    area.exit(mq_ordnance_shed, mq_forge_bay, "north")
    area.exit(mq_forge_bay, mq_ordnance_shed, "south")
    area.exit(mq_forge_bay, mq_fletcher_yard, "east")
    area.exit(mq_fletcher_yard, mq_forge_bay, "west")
    area.exit(mq_muster_hall, mq_pay_window, "west")
    area.exit(mq_pay_window, mq_muster_hall, "east")
    area.exit(mq_muster_hall, mq_stables, "south")
    area.exit(mq_stables, mq_muster_hall, "north")
    area.exit(mq_ordnance_shed, mq_armorers_hall, "east")
    area.exit(mq_armorers_hall, mq_ordnance_shed, "west")
    area.exit(mq_armorers_hall, mq_forge_bay, "northwest")
    area.exit(mq_forge_bay, mq_armorers_hall, "southeast")
    area.exit(mq_supply_depot, mq_ration_house, "south")
    area.exit(mq_ration_house, mq_supply_depot, "north")
    area.exit(mq_ration_house, mq_pay_window, "southwest")
    area.exit(mq_pay_window, mq_ration_house, "northeast")
    area.exit(mq_drill_green, mq_range_gallery, "west")
    area.exit(mq_range_gallery, mq_drill_green, "east")
    area.exit(mq_range_gallery, mq_orders_desk, "north")
    area.exit(mq_orders_desk, mq_range_gallery, "south")
    area.exit(mq_stables, mq_farrier_row, "east")
    area.exit(mq_farrier_row, mq_stables, "west")
    area.exit(mq_farrier_row, mq_fletcher_yard, "north")
    area.exit(mq_fletcher_yard, mq_farrier_row, "south")
    area.exit(mq_signal_tower, mq_orders_desk, "east")
    area.exit(mq_orders_desk, mq_signal_tower, "west")
    area.exit(ca_relief_yard, mq_stables, "southeast")
    area.exit(mq_stables, ca_relief_yard, "northwest")

    area.exit(mq_barracks_yard, dc_outer_yard, "northeast")
    area.exit(dc_outer_yard, mq_barracks_yard, "southwest")
    area.exit(dc_outer_yard, dc_tack_hall, "east")
    area.exit(dc_tack_hall, dc_outer_yard, "west")
    area.exit(dc_outer_yard, dc_handler_ring, "north")
    area.exit(dc_handler_ring, dc_outer_yard, "south")
    area.exit(dc_handler_ring, dc_courier_platform, "up")
    area.exit(dc_courier_platform, dc_handler_ring, "down")
    area.exit(dc_handler_ring, dc_observation_walk, "west")
    area.exit(dc_observation_walk, dc_handler_ring, "east")
    area.exit(dc_outer_yard, dc_feed_court, "west")
    area.exit(dc_feed_court, dc_outer_yard, "east")
    area.exit(dc_feed_court, dc_quarantine_pens, "north")
    area.exit(dc_quarantine_pens, dc_feed_court, "south")
    area.exit(dc_quarantine_pens, dc_manifest_rail, "east")
    area.exit(dc_manifest_rail, dc_quarantine_pens, "west")
    area.exit(dc_observation_walk, dc_manifest_rail, "north")
    area.exit(dc_manifest_rail, dc_observation_walk, "south")
    area.exit(dc_handler_ring, dc_chain_lift, "east")
    area.exit(dc_chain_lift, dc_handler_ring, "west")
    area.exit(dc_chain_lift, dc_restricted_tunnel, "down")
    area.exit(dc_restricted_tunnel, dc_chain_lift, "up")
    area.exit(dc_manifest_rail, dc_dispatch_office, "east")
    area.exit(dc_dispatch_office, dc_manifest_rail, "west")
    area.exit(dc_dispatch_office, dc_weather_balcony, "north")
    area.exit(dc_weather_balcony, dc_dispatch_office, "south")
    area.exit(dc_tack_hall, dc_scale_wash, "north")
    area.exit(dc_scale_wash, dc_tack_hall, "south")
    area.exit(dc_quarantine_pens, dc_repair_bay, "northeast")
    area.exit(dc_repair_bay, dc_quarantine_pens, "southwest")
    area.exit(dc_repair_bay, dc_scale_wash, "south")
    area.exit(dc_scale_wash, dc_repair_bay, "north")
    area.exit(dc_dispatch_office, dc_roster_hall, "south")
    area.exit(dc_roster_hall, dc_dispatch_office, "north")
    area.exit(dc_roster_hall, dc_officers_gallery, "west")
    area.exit(dc_officers_gallery, dc_roster_hall, "east")
    area.exit(dc_dispatch_office, dc_signal_cage, "east")
    area.exit(dc_signal_cage, dc_dispatch_office, "west")
    area.exit(dc_signal_cage, dc_weather_balcony, "northwest")
    area.exit(dc_weather_balcony, dc_signal_cage, "southeast")
    area.exit(dc_tack_hall, dc_harness_loft, "up")
    area.exit(dc_harness_loft, dc_tack_hall, "down")
    area.exit(dc_harness_loft, dc_cargo_loft, "north")
    area.exit(dc_cargo_loft, dc_harness_loft, "south")
    area.exit(dc_cargo_loft, dc_repair_bay, "southeast")
    area.exit(dc_repair_bay, dc_cargo_loft, "northwest")
    area.exit(dc_officers_gallery, dc_observation_walk, "southwest")
    area.exit(dc_observation_walk, dc_officers_gallery, "northeast")
    area.exit(mq_orders_desk, dc_dispatch_office, "northwest")
    area.exit(dc_dispatch_office, mq_orders_desk, "southeast")

    area.exit(mw_decree_wall, cd_sealed_gate, "north")
    area.exit(cd_sealed_gate, mw_decree_wall, "south")
    area.exit(cd_sealed_gate, cd_survey_cloister, "east")
    area.exit(cd_survey_cloister, cd_sealed_gate, "west")
    area.exit(cd_survey_cloister, cd_lens_court, "north")
    area.exit(cd_lens_court, cd_survey_cloister, "south")
    area.exit(cd_survey_cloister, cd_attic_archive, "up")
    area.exit(cd_attic_archive, cd_survey_cloister, "down")
    area.exit(cd_lens_court, cd_apothecary, "west")
    area.exit(cd_apothecary, cd_lens_court, "east")
    area.exit(cd_sealed_gate, cd_copy_hall, "north")
    area.exit(cd_copy_hall, cd_sealed_gate, "south")
    area.exit(cd_copy_hall, cd_survey_cloister, "north")
    area.exit(cd_survey_cloister, cd_copy_hall, "south")
    area.exit(cd_lens_court, cd_revision_gallery, "east")
    area.exit(cd_revision_gallery, cd_lens_court, "west")
    area.exit(cd_revision_gallery, cd_calibration_cell, "north")
    area.exit(cd_calibration_cell, cd_revision_gallery, "south")
    area.exit(cd_calibration_cell, cd_undercroft, "down")
    area.exit(cd_undercroft, cd_calibration_cell, "up")
    area.exit(cd_apothecary, cd_powder_store, "north")
    area.exit(cd_powder_store, cd_apothecary, "south")
    area.exit(cd_apothecary, cd_reagent_garden, "south")
    area.exit(cd_reagent_garden, cd_apothecary, "north")
    area.exit(cd_reagent_garden, cd_glasshouse, "east")
    area.exit(cd_glasshouse, cd_reagent_garden, "west")
    area.exit(cd_revision_gallery, cd_quietium_chamber, "east")
    area.exit(cd_quietium_chamber, cd_revision_gallery, "west")
    area.exit(cd_attic_archive, cd_reference_vault, "north")
    area.exit(cd_reference_vault, cd_attic_archive, "south")
    area.exit(cd_survey_cloister, cd_lecture_ambulatory, "southwest")
    area.exit(cd_lecture_ambulatory, cd_survey_cloister, "northeast")
    area.exit(cd_copy_hall, cd_binding_hall, "west")
    area.exit(cd_binding_hall, cd_copy_hall, "east")
    area.exit(cd_binding_hall, cd_specimen_archive, "north")
    area.exit(cd_specimen_archive, cd_binding_hall, "south")
    area.exit(cd_specimen_archive, cd_reference_vault, "east")
    area.exit(cd_reference_vault, cd_specimen_archive, "west")
    area.exit(cd_lecture_ambulatory, cd_silent_cloister, "north")
    area.exit(cd_silent_cloister, cd_lecture_ambulatory, "south")
    area.exit(cd_silent_cloister, cd_reagent_garden, "east")
    area.exit(cd_reagent_garden, cd_silent_cloister, "west")
    area.exit(cd_calibration_cell, cd_measure_tower, "up")
    area.exit(cd_measure_tower, cd_calibration_cell, "down")

    area.exit(ca_processional_way, nh_processional, "east")
    area.exit(nh_processional, ca_processional_way, "west")
    area.exit(nh_processional, nh_salon_steps, "north")
    area.exit(nh_salon_steps, nh_processional, "south")
    area.exit(nh_salon_steps, nh_garden_terrace, "east")
    area.exit(nh_garden_terrace, nh_salon_steps, "west")
    area.exit(nh_salon_steps, nh_private_archive, "west")
    area.exit(nh_private_archive, nh_salon_steps, "east")
    area.exit(nh_garden_terrace, nh_preserve_gate, "north")
    area.exit(nh_preserve_gate, nh_garden_terrace, "south")
    area.exit(nh_preserve_gate, "stagcrown_preserve:fg_charter_gate", "north")
    area.exit(nh_processional, nh_house_talvere_portico, "east")
    area.exit(nh_house_talvere_portico, nh_processional, "west")
    area.exit(nh_salon_steps, nh_guest_loggia, "north")
    area.exit(nh_guest_loggia, nh_salon_steps, "south")
    area.exit(nh_guest_loggia, nh_rhest_colonnade, "east")
    area.exit(nh_rhest_colonnade, nh_guest_loggia, "west")
    area.exit(nh_private_archive, nh_rhest_colonnade, "north")
    area.exit(nh_rhest_colonnade, nh_private_archive, "south")
    area.exit(nh_rhest_colonnade, nh_mirror_green, "east")
    area.exit(nh_mirror_green, nh_rhest_colonnade, "west")
    area.exit(nh_mirror_green, nh_garden_terrace, "southwest")
    area.exit(nh_garden_terrace, nh_mirror_green, "northeast")
    area.exit(nh_mirror_green, nh_servants_postern, "east")
    area.exit(nh_servants_postern, nh_mirror_green, "west")
    area.exit(nh_guest_loggia, nh_patron_registry, "west")
    area.exit(nh_patron_registry, nh_guest_loggia, "east")
    area.exit(nh_patron_registry, nh_hunt_map_gallery, "north")
    area.exit(nh_hunt_map_gallery, nh_patron_registry, "south")
    area.exit(nh_servants_postern, nh_kitchen_court, "south")
    area.exit(nh_kitchen_court, nh_servants_postern, "north")
    area.exit(nh_mirror_green, nh_garden_wall, "north")
    area.exit(nh_garden_wall, nh_mirror_green, "south")
    area.exit(nh_kitchen_court, nh_garden_wall, "east")
    area.exit(nh_garden_wall, nh_kitchen_court, "west")
    area.exit(nh_house_talvere_portico, nh_talvere_gallery, "north")
    area.exit(nh_talvere_gallery, nh_house_talvere_portico, "south")
    area.exit(nh_rhest_colonnade, nh_rhest_salon, "north")
    area.exit(nh_rhest_salon, nh_rhest_colonnade, "south")
    area.exit(nh_patron_registry, nh_carriage_court, "northeast")
    area.exit(nh_carriage_court, nh_patron_registry, "southwest")
    area.exit(nh_carriage_court, nh_lodge_office, "east")
    area.exit(nh_lodge_office, nh_carriage_court, "west")
    area.exit(nh_guest_loggia, nh_guest_garden, "northeast")
    area.exit(nh_guest_garden, nh_guest_loggia, "southwest")
    area.exit(nh_guest_garden, nh_hunt_map_gallery, "east")
    area.exit(nh_hunt_map_gallery, nh_guest_garden, "west")
    area.exit(nh_hunt_map_gallery, nh_lodge_office, "northeast")
    area.exit(nh_lodge_office, nh_hunt_map_gallery, "southwest")
    area.exit(oc_hawkers_walk, nh_kitchen_court, "east")
    area.exit(nh_kitchen_court, oc_hawkers_walk, "west")
    area.exit(cd_reagent_garden, nh_guest_garden, "southeast")
    area.exit(nh_guest_garden, cd_reagent_garden, "northwest")

    area.exit(oc_shrine_lane, hw_drain_steps, "down")
    area.exit(hw_drain_steps, oc_shrine_lane, "up")
    area.exit(hw_drain_steps, hw_smuggler_lantern, "north")
    area.exit(hw_smuggler_lantern, hw_drain_steps, "south")
    area.exit(hw_drain_steps, hw_ratwalk, "west")
    area.exit(hw_ratwalk, hw_drain_steps, "east")
    area.exit(hw_smuggler_lantern, hw_print_cellar, "east")
    area.exit(hw_print_cellar, hw_smuggler_lantern, "west")
    area.exit(hw_smuggler_lantern, hw_old_cistern, "north")
    area.exit(hw_old_cistern, hw_smuggler_lantern, "south")
    area.exit(hw_smuggler_lantern, hw_burnt_store, "west")
    area.exit(hw_burnt_store, hw_smuggler_lantern, "east")
    area.exit(hw_print_cellar, hw_cinder_loft, "up")
    area.exit(hw_cinder_loft, hw_print_cellar, "down")
    area.exit(mw_registry_annex, hw_print_cellar, "out", hidden=True)
    area.exit(hw_print_cellar, mw_registry_annex, "in", hidden=True)
    area.exit(hw_ratwalk, hw_dead_drop_drain, "west")
    area.exit(hw_dead_drop_drain, hw_ratwalk, "east")
    area.exit(hw_old_cistern, mw_causeway_postern, "up", hidden=True)
    area.exit(mw_causeway_postern, hw_old_cistern, "down", hidden=True)
    area.exit(hw_old_cistern, hw_sump_bridge, "east")
    area.exit(hw_sump_bridge, hw_old_cistern, "west")
    area.exit(hw_sump_bridge, hw_watch_niche, "north")
    area.exit(hw_watch_niche, hw_sump_bridge, "south")
    area.exit(mw_confiscation_room, hw_burnt_store, "down", hidden=True)
    area.exit(hw_burnt_store, mw_confiscation_room, "up", hidden=True)
    area.exit(cd_undercroft, hw_watch_niche, "west", hidden=True)
    area.exit(hw_watch_niche, cd_undercroft, "east", hidden=True)
    area.exit(dc_restricted_tunnel, hw_sump_bridge, "out", hidden=True)
    area.exit(hw_sump_bridge, dc_restricted_tunnel, "in", hidden=True)
    area.exit(hw_print_cellar, hw_ink_sink, "south")
    area.exit(hw_ink_sink, hw_print_cellar, "north")
    area.exit(hw_ink_sink, hw_chain_cache, "east")
    area.exit(hw_chain_cache, hw_ink_sink, "west")
    area.exit(hw_sump_bridge, hw_sluice_gate, "east")
    area.exit(hw_sluice_gate, hw_sump_bridge, "west")
    area.exit(hw_chain_cache, hw_gutter_oratory, "north")
    area.exit(hw_gutter_oratory, hw_chain_cache, "south")
    area.exit(nh_kitchen_court, hw_gutter_oratory, "down", hidden=True)
    area.exit(hw_gutter_oratory, nh_kitchen_court, "up", hidden=True)
    area.exit(hw_cinder_loft, hw_runner_dormer, "east")
    area.exit(hw_runner_dormer, hw_cinder_loft, "west")
    area.exit(hw_runner_dormer, hw_false_store, "north")
    area.exit(hw_false_store, hw_runner_dormer, "south")
    area.exit(hw_false_store, hw_culvert_crossing, "east")
    area.exit(hw_culvert_crossing, hw_false_store, "west")
    area.exit(hw_culvert_crossing, hw_ash_nook, "north")
    area.exit(hw_ash_nook, hw_culvert_crossing, "south")
    area.exit(hw_ash_nook, hw_ink_sink, "east")
    area.exit(hw_ink_sink, hw_ash_nook, "west")
    area.exit(hw_culvert_crossing, hw_sluice_gate, "northeast")
    area.exit(hw_sluice_gate, hw_culvert_crossing, "southwest")
    area.exit(hw_dead_drop_drain, hw_grate_ladder, "up")
    area.exit(hw_grate_ladder, hw_dead_drop_drain, "down")
    area.exit(oc_lodger_alley, hw_grate_ladder, "down", hidden=True)
    area.exit(hw_grate_ladder, oc_lodger_alley, "up", hidden=True)

    # ==================================================================
    #  NPCS AND SERVICE ANCHORS
    # ==================================================================

    area.npc(ca_customs_hall, "npc_gate_clerk_sera_dain", faction="empire")
    area.npc(ca_arrival_court, "npc_greeter_olven_march", faction="empire")
    area.npc(ca_manifest_yard, "npc_manifest_runner_jor", faction="empire")
    area.npc(ca_assessor_gallery, "npc_roads_assessor_mirel", faction="empire")
    area.npc(ca_caravan_court, "npc_caravan_marshal_tev", faction="empire")
    area.npc(ca_levy_office, "npc_levy_clerk_hesra", faction="empire")
    area.npc(ca_measure_house, "npc_measure_inspector_avax", faction="empire")
    area.npc(ca_waybill_office, "npc_waybill_clerk_noren", faction="empire")

    _outfitter = area.npc(oc_red_market, "npc_outfitter_loric", faction=None)
    area.vendor(
        _outfitter,
        accepts=["equipment", "consumable"],
        item_ids=[
            "iron_sword", "iron_dagger", "iron_staff", "iron_bow",
            "iron_buckler", "leather_cap", "leather_vest", "leather_gloves",
            "leather_leggings", "leather_boots", "travelers_cloak",
            "leather_mask", "leather_bracers", "trail_rations", "bandage",
        ],
    )

    area.npc(oc_wayfarer_inn, "npc_innkeeper_brinn_hal", faction=None)
    area.npc(oc_exchange_hall, "npc_bank_teller_vestri", faction="consortium")
    area.npc(oc_exchange_hall, "npc_bank_manager_calis_urne", faction="consortium")
    area.npc(oc_coinstairs, "npc_moneychanger_sivek", faction="consortium")
    area.npc(oc_broker_steps, "npc_broker_yaran", faction="consortium")

    _stewpot = area.npc(oc_stewpot_arcade, "npc_stewpot_doria", faction=None)
    area.vendor(
        _stewpot,
        accepts=["consumable"],
        item_ids=["cooked_meat", "hearty_stew", "trail_rations", "minor_stamina_potion"],
    )

    _tinker = area.npc(oc_tinkers_row, "npc_tinker_solla", faction=None)
    area.vendor(
        _tinker,
        accepts=["tool", "consumable", "equipment", "material"],
        item_ids=["pickaxe", "sickle", "hatchet", "skinning_knife", "fishing_rod", "bait", "bandage"],
    )

    _clothier = area.npc(oc_cloth_hall, "npc_clothier_penric", faction=None)
    area.vendor(_clothier, accepts=["equipment"], item_ids=[
        "leather_cap",
        "hardened_leather_cap",
        "leather_vest",
        "hardened_leather_vest",
        "leather_gloves",
        "hardened_leather_gloves",
        "leather_leggings",
        "hardened_leather_leggings",
        "leather_boots",
        "hardened_leather_boots",
        "travelers_cloak",
        "rangers_cloak",
        "leather_mask",
    ])
    area.npc(oc_teamsters_hall, "npc_teamster_holl", faction=None)
    area.npc(oc_scribes_corner, "npc_scribe_galen", faction=None)

    _lanternwright = area.npc(oc_lantern_row, "npc_lanternwright_pes", faction=None)
    area.vendor(_lanternwright, accepts=["equipment", "consumable", "tool", "material"], item_ids=[
        "travelers_cloak",
        "leather_mask",
        "bandage",
        "trail_rations",
        "minor_stamina_potion",
        "antidote_potion",
    ])

    area.npc(mw_permit_hall, "npc_registrar_taveth", faction="empire")
    area.npc(mw_records_arcade, "npc_archivist_seln", faction="empire")
    area.npc(mw_seal_chamber, "npc_seal_keeper_jori", faction="empire")
    area.npc(mw_confiscation_room, "npc_confiscation_clerk_ollis", faction="empire")
    area.npc(mw_petition_cloister, "npc_petition_clerk_vessa", faction="empire")
    area.npc(mw_notary_room, "npc_notary_vesk", faction="empire")
    area.npc(mw_review_court, "npc_review_magistrate_ceren", faction="empire")
    area.npc(mw_public_records, "npc_records_keeper_ulis", faction="empire")

    _quartermaster = area.npc(mq_armory_lane, "npc_quartermaster_brenn", faction="empire")
    area.vendor(_quartermaster, accepts=["equipment"], item_ids=[
        "iron_sword",
        "steel_sword",
        "iron_mace",
        "steel_mace",
        "iron_greatsword",
        "steel_greatsword",
        "iron_greataxe",
        "steel_greataxe",
        "iron_buckler",
        "steel_buckler",
        "iron_kite_shield",
        "steel_kite_shield",
        "iron_helm",
        "steel_helm",
        "iron_chainmail",
        "iron_breastplate",
        "steel_breastplate",
        "iron_gauntlets",
        "steel_gauntlets",
        "iron_greaves",
        "steel_greaves",
        "iron_sabatons",
        "steel_sabatons",
    ], faction="empire")

    area.npc(mq_muster_hall, "npc_muster_captain_rheon", faction="empire")

    _supply_sergeant = area.npc(mq_supply_depot, "npc_supply_sergeant_hadrik", faction="empire")
    area.vendor(_supply_sergeant, accepts=["consumable"], item_ids=[
        "bandage",
        "minor_healing_potion",
        "minor_stamina_potion",
        "antidote_potion",
        "trail_rations",
        "cooked_meat",
        "hearty_stew",
        "healing_draught",
        "mountain_tonic",
        "stamina_tonic",
    ], faction="empire")
    area.npc(mq_pay_window, "npc_paymaster_lurex", faction="empire")

    _forge_sergeant = area.npc(mq_forge_bay, "npc_forge_sergeant_tomas", faction="empire")
    area.vendor(_forge_sergeant, accepts=["equipment", "tool", "material"], item_ids=[
        "steel_sword",
        "steel_dagger",
        "steel_mace",
        "steel_staff",
        "steel_greatsword",
        "steel_greataxe",
        "steel_buckler",
        "steel_kite_shield",
        "pickaxe",
        "hatchet",
    ], faction="empire")
    area.npc(mq_farrier_row, "npc_farrier_kerem", faction="empire")
    area.npc(mq_orders_desk, "npc_orders_lieutenant_serik", faction="empire")

    _medic = area.npc(mq_infirmary, "npc_medic_surgeon_halwen", faction="empire")
    area.medic(_medic)

    area.npc(dc_courier_platform, "npc_courier_factor_helian", faction="empire")
    area.npc(dc_handler_ring, "npc_handler_sergeant_vorun", faction="empire")
    area.npc(dc_manifest_rail, "npc_flight_ledger_iras", faction="empire")
    area.npc(dc_quarantine_pens, "npc_pen_keeper_cadra", faction="empire")
    area.npc(dc_dispatch_office, "npc_dispatch_officer_sevain", faction="empire")
    area.npc(dc_weather_balcony, "npc_weather_reader_pel", faction="empire")
    area.npc(dc_roster_hall, "npc_roster_officer_mav", faction="empire")

    _harness_master = area.npc(dc_harness_loft, "npc_harness_master_torin", faction="empire")
    area.vendor(_harness_master, accepts=["equipment", "consumable", "material"], item_ids=[
        "iron_bow",
        "steel_bow",
        "iron_dagger",
        "steel_dagger",
        "hardened_leather_boots",
        "travelers_cloak",
        "rangers_cloak",
        "trail_rations",
        "bandage",
    ], faction="empire")

    area.npc(cd_survey_cloister, "npc_surveyor_lyessa", faction=None)
    area.npc(cd_copy_hall, "npc_copymaster_meren", faction=None)
    area.npc(cd_revision_gallery, "npc_lens_custodian_seris", faction=None)
    area.npc(cd_reference_vault, "npc_circle_copyist_neme", faction=None)
    area.npc(cd_lecture_ambulatory, "npc_lectrix_sana", faction=None)
    area.npc(cd_binding_hall, "npc_binder_orel", faction=None)

    _apothecary = area.npc(cd_apothecary, "npc_apothecary_meret", faction=None)
    area.vendor(_apothecary, accepts=["consumable", "ingredient"], item_ids=[
        "minor_healing_potion",
        "minor_stamina_potion",
        "antidote_potion",
        "bandage",
        "herb_poultice",
        "healing_draught",
        "mountain_tonic",
        "stamina_tonic",
    ])

    _reagent_keeper = area.npc(cd_glasshouse, "npc_reagent_keeper_olian", faction=None)
    area.vendor(_reagent_keeper, accepts=["ingredient", "consumable", "equipment"], item_ids=[
        "iron_staff",
        "steel_staff",
        "bone_talisman",
        "silver_pendant",
        "ring_of_acuity",
        "minor_healing_potion",
        "antidote_potion",
    ])

    area.npc(nh_salon_steps, "npc_steward_maelin_rhest", faction="empire")
    area.npc(nh_private_archive, "npc_house_scholar_talvere", faction="empire")
    area.npc(nh_house_talvere_portico, "npc_house_guard_talvere", faction="empire")
    area.npc(nh_guest_loggia, "npc_guest_chamberlain_ost", faction="empire")
    area.npc(nh_patron_registry, "npc_patron_secretary_vael", faction="empire")
    area.npc(nh_hunt_map_gallery, "npc_hunt_curator_rhysa", faction="empire")
    area.npc(nh_carriage_court, "npc_carriage_master_sel", faction="empire")
    area.npc(nh_rhest_salon, "npc_guest_mistress_lura", faction="empire")

    _fence = area.npc(hw_smuggler_lantern, "npc_fence_ivera_coal", faction=None)
    area.vendor(_fence, accepts=["item", "material", "equipment", "consumable"], item_ids=[
        "steel_dagger",
        "rangers_cloak",
        "leather_mask",
        "signet_ring",
        "bone_talisman",
        "antidote_potion",
        "bandage",
    ])

    area.npc(hw_print_cellar, "npc_printkeeper_elais", faction=None)
    area.npc(hw_cinder_loft, "npc_cinder_runner_mara", faction=None)
    area.npc(hw_chain_cache, "npc_cache_keeper_dren", faction=None)
    area.npc(hw_runner_dormer, "npc_runner_tallis", faction=None)
    area.npc(hw_ash_nook, "npc_ash_scribe_rell", faction=None)

    # ==================================================================
    #  HOSTILE POCKETS
    # ==================================================================

    area.spawn(oc_ragcourt, "pickpocket", count_min=0, count_max=1, respawn_minutes=18, respawn_variance=5)
    area.spawn(oc_broker_steps, "pickpocket", count_min=0, count_max=1, respawn_minutes=20, respawn_variance=6)
    area.spawn(oc_public_baths, "pickpocket", count_min=0, count_max=1, respawn_minutes=24, respawn_variance=7)
    area.spawn(hw_ratwalk, "thug", count_min=1, count_max=2, respawn_minutes=20, respawn_variance=5)
    area.spawn(hw_dead_drop_drain, "sewer_rat", count_min=1, count_max=2, respawn_minutes=15, respawn_variance=4)
    area.spawn(hw_burnt_store, "pickpocket", count_min=0, count_max=1, respawn_minutes=24, respawn_variance=6)
    area.spawn(hw_old_cistern, "smuggler", count_min=1, count_max=1, respawn_minutes=25, respawn_variance=8)
    area.spawn(hw_sump_bridge, "thug", count_min=1, count_max=1, respawn_minutes=22, respawn_variance=5)
    area.spawn(hw_watch_niche, "smuggler", count_min=0, count_max=1, respawn_minutes=28, respawn_variance=8)
    area.spawn(hw_ink_sink, "sewer_rat", count_min=1, count_max=2, respawn_minutes=16, respawn_variance=4)
    area.spawn(hw_chain_cache, "thug", count_min=1, count_max=1, respawn_minutes=26, respawn_variance=7)
    area.spawn(hw_sluice_gate, "smuggler", count_min=0, count_max=1, respawn_minutes=30, respawn_variance=10)
    area.spawn(hw_gutter_oratory, "thug", count_min=0, count_max=1, respawn_minutes=28, respawn_variance=9)
    area.spawn(dc_restricted_tunnel, "bandit", count_min=1, count_max=1, respawn_minutes=30, respawn_variance=10)
    area.spawn(dc_quarantine_pens, "sewer_rat", count_min=1, count_max=2, respawn_minutes=16, respawn_variance=4)
    area.spawn(cd_undercroft, "sewer_rat", count_min=1, count_max=2, respawn_minutes=18, respawn_variance=5)

    # ==================================================================
    #  FLIGHT
    # ==================================================================

    area.flight_point(
        dc_courier_platform,
        "varath_prime_courier",
        name="Varath Prime Courier Platform",
    )
    area.flight_route(
        "varath_prime_courier",
        "vaels_crossing_courier",
        140,
        leg_duration=90,
        echoes=[
            {"delay": 25, "message": "Varath Prime falls away beneath the courier route, its measured avenues shrinking to dark lines."},
            {"delay": 60, "message": "Far below, the roads of Varath look less like conquest than inheritance pressed into service."},
        ],
    )

    # ==================================================================
    #  LORE FRAGMENTS
    # ==================================================================

    area.lore_fragment(
        "vp_lore_processional_stone",
        ca_processional_way,
        discovery_method="search",
        scholar_path="remnance",
        text=(
            "The paving bands beneath the Processional Way do not belong to a "
            "single project. New stone names the Crown Restoration Charter of "
            "711, but the older pale bands beneath it were cut to a different "
            "measure entirely. The city restored something it did not first lay."
        ),
        insight_gain=2,
    )

    area.lore_fragment(
        "vp_lore_decree_wall",
        mw_decree_wall,
        discovery_method="search",
        scholar_path="arcana",
        text=(
            "The decree wall carries three versions of the same boundary "
            "language beneath its current paint. One names public safety, one "
            "names lawful revision, and the oldest surviving lines name only "
            "measure, custody, and removal of prior text."
        ),
        insight_gain=2,
    )

    area.lore_fragment(
        "vp_lore_survey_margin",
        cd_attic_archive,
        discovery_method="search",
        scholar_path="remnance",
        text=(
            "A survey copy from the Collegium notes that several culvert lines "
            "and road angles 'do not originate in any current civic program.' "
            "The margin beside that sentence was trimmed by hand, but not "
            "carefully enough to remove it completely."
        ),
        insight_gain=2,
    )

    area.lore_fragment(
        "vp_lore_courier_board",
        dc_observation_walk,
        discovery_method="search",
        scholar_path="resonance",
        text=(
            "A weathered manifest board still bears the talon-and-bar seal of "
            "Thirteenth Talon Command. Several route names were scraped off and "
            "copied over, but the older indentations remain. The network has "
            "been revised more than once, and not all of those revisions were "
            "honest."
        ),
        insight_gain=2,
    )

    area.lore_fragment(
        "vp_lore_preserve_charter",
        nh_private_archive,
        discovery_method="search",
        scholar_path="arcana",
        text=(
            "A private copy of the Stagcrown Revision of 728 sits beside an "
            "older survey sketch with the same boundary line drawn under a "
            "different name. The preserve did not create the border it now "
            "claims; it inherited and renamed it."
        ),
        insight_gain=2,
    )

    area.lore_fragment(
        "vp_lore_cistern_marks",
        hw_old_cistern,
        discovery_method="search",
        scholar_path="remnance",
        text=(
            "The dry cistern walls are marked with cut numbers and channel "
            "notations that do not match current civic indexing. Someone later "
            "painted Office of Seals and Civic Measure marks over them, but the "
            "older work remains legible in the right light."
        ),
        insight_gain=3,
    )

    area.lore_fragment(
        "vp_lore_split_roadwheel",
        ca_toll_archive,
        discovery_method="search",
        scholar_path="arcana",
        text=(
            "One toll table preserves a prior wording of the Edict of Measured "
            "Passage beneath later copied lines. The older clause concerns "
            "custody of travelers held for irregular papers, while the later "
            "copy speaks only of delay, correction, and lawful review."
        ),
        insight_gain=2,
    )

    area.lore_fragment(
        "vp_lore_confiscation_ledger",
        mw_confiscation_room,
        discovery_method="search",
        scholar_path="remnance",
        text=(
            "A confiscation ledger notes three charter copies as 'accepted in "
            "place of stone' and one private register as 'entry reassigned "
            "without witness.' No explanation follows those phrases. None is "
            "apparently expected."
        ),
        insight_gain=3,
    )

    area.lore_fragment(
        "vp_lore_iron_vein_notice",
        mq_ordnance_shed,
        discovery_method="search",
        scholar_path="arcana",
        text=(
            "A stack of haul slips stamped with the stonewake pickmark cites "
            "the Iron Vein Requisition of 734 as authority for emergency "
            "movement of tools, chain, and labor allotments. The listed needs "
            "sound permanent for something framed as temporary."
        ),
        insight_gain=2,
    )

    area.lore_fragment(
        "vp_lore_pen_roster",
        dc_manifest_rail,
        discovery_method="search",
        scholar_path="resonance",
        text=(
            "A retired roster board tracks penalties for unlogged feed, broken "
            "tack seals, and unauthorized tunnel access beneath Thirteenth Talon "
            "Command. The route names change from column to column, but the "
            "punishments remain mechanically consistent."
        ),
        insight_gain=2,
    )

    area.lore_fragment(
        "vp_lore_revision_slate",
        cd_revision_gallery,
        discovery_method="search",
        scholar_path="arcana",
        text=(
            "Pinned beneath a polished public advisory is an earlier draft that "
            "uses harsher terms: seizure, custody, and removal of prior markers. "
            "The approved version replaces them with restoration, revision, and "
            "civic order. The policy appears unchanged. Only the language softened."
        ),
        insight_gain=2,
    )

    area.lore_fragment(
        "vp_lore_guest_roll",
        nh_guest_loggia,
        discovery_method="search",
        scholar_path="remnance",
        text=(
            "A partially burned guest roll places House Talvere, House Rhest, "
            "and registry officials at the same private supper the week after "
            "the Stagcrown Revision was copied into noble records. The preserve "
            "was negotiated as much over wine as over law."
        ),
        insight_gain=2,
    )

    area.lore_fragment(
        "vp_lore_cinder_proof",
        hw_cinder_loft,
        discovery_method="search",
        scholar_path="resonance",
        text=(
            "A half-corrected handbill in ash-cinder cipher accuses the city of "
            "using copied ledgers to disappear obligations, people, and boundaries "
            "alike. Whoever set the proof knew official language well enough to "
            "twist it back against itself."
        ),
        insight_gain=3,
    )

    area.lore_fragment(
        "vp_lore_levy_schedule",
        ca_levy_office,
        discovery_method="search",
        scholar_path="arcana",
        text=(
            "A levy schedule cross-references road fees with categories for "
            "detention, escort, and irregular passage under the Edict of Measured "
            "Passage. Movement in Varath Prime is not simply taxed. It is sorted."
        ),
        insight_gain=2,
    )

    area.lore_fragment(
        "vp_lore_broker_slate",
        oc_broker_steps,
        discovery_method="search",
        scholar_path="remnance",
        text=(
            "A cracked runner slate lists rush prices for sealed ministry packets, "
            "quarry orders, preserve permits, and courier corrections. Even access "
            "to official order has a public shadow market here."
        ),
        insight_gain=2,
    )

    area.lore_fragment(
        "vp_lore_witness_roll",
        mw_witness_chamber,
        discovery_method="search",
        scholar_path="arcana",
        text=(
            "A witness roll notes one testimony attached to a copied boundary revision "
            "and another marked 'prior text removed.' The legal process appears careful, "
            "yet its records still assume some histories deserve erasure."
        ),
        insight_gain=3,
    )

    area.lore_fragment(
        "vp_lore_pay_window_notice",
        mq_pay_window,
        discovery_method="search",
        scholar_path="remnance",
        text=(
            "A pay notice under the Iron Vein Requisition deducts gear loss, transport "
            "damage, and ration overruns from labor allotments before wages are even "
            "mentioned. The quarter calls this discipline; the numbers call it hunger."
        ),
        insight_gain=2,
    )

    area.lore_fragment(
        "vp_lore_dispatch_revision",
        dc_dispatch_office,
        discovery_method="search",
        scholar_path="resonance",
        text=(
            "A dispatch ledger preserves older route names beneath the current tables, "
            "each overwritten in the same tidy hand. The courier network grows by "
            "revision as much as by distance."
        ),
        insight_gain=2,
    )

    area.lore_fragment(
        "vp_lore_glasshouse_margin",
        cd_glasshouse,
        discovery_method="search",
        scholar_path="arcana",
        text=(
            "A clipped cultivation note from the Surveyor Collegium of Varath Prime "
            "changes 'containment by custody' into 'maintenance by measure' between "
            "drafts. The garden's labels are gentler than the policy beneath them."
        ),
        insight_gain=2,
    )

    area.lore_fragment(
        "vp_lore_hunt_map",
        nh_hunt_map_gallery,
        discovery_method="search",
        scholar_path="remnance",
        text=(
            "A framed hunt map gives the Stagcrown Revision pride of place, yet the "
            "under-drawing shows an older line copied almost exactly. House Rhest did "
            "not discover the preserve border. It inherited a claim and refined it."
        ),
        insight_gain=2,
    )

    area.lore_fragment(
        "vp_lore_sluice_marks",
        hw_sluice_gate,
        discovery_method="search",
        scholar_path="resonance",
        text=(
            "The sluice stone carries old cut numbers under newer chalk arrows used by "
            "the Cinder Ledger. Both systems guide movement through the city; one was "
            "made public, and one survived because it was not."
        ),
        insight_gain=3,
    )

    # ==================================================================
    #  QUEST DELIVERY ITEMS
    # ==================================================================

    area.item(
        "courier_manifest_packet",
        key="Sealed Courier Manifest",
        item_type="item",
        weight=0.1,
        rarity="normal",
        value=0,
        is_quest_item=True,
        desc=(
            "A folded routing manifest bound in twine and sealed with the "
            "Varath Prime permit office mark. The wax is still warm."
        ),
    )

    area.item(
        "stagcrown_petition",
        key="Stagcrown Access Petition",
        item_type="item",
        weight=0.1,
        rarity="normal",
        value=0,
        is_quest_item=True,
        desc=(
            "A carefully folded petition bearing House Rhest's preserve seal "
            "and several blank endorsement lines."
        ),
    )

    area.item(
        "dispatch_correction_note",
        key="Dispatch Correction Note",
        item_type="item",
        weight=0.1,
        rarity="normal",
        value=0,
        is_quest_item=True,
        desc=(
            "A revised courier note carrying dispatch marks, route tallies, and "
            "one hasty correction in a different hand."
        ),
    )

    # ==================================================================
    #  QUESTS
    # ==================================================================

    area.quest(
        "vp_q_registry_of_the_missing",
        name="Registry of the Missing",
        description=(
            "Archivist Seln has found evidence that names were removed from "
            "recent civic copies and quietly reassigned in the annex. Review "
            "the damaged registry work before the next correction sweep erases "
            "what remains."
        ),
        quest_type="investigation",
        quest_giver="npc_archivist_seln",
        objectives=[
            {
                "type": "investigate",
                "target": "mw_registry_annex",
                "count": 1,
                "description": "Investigate the damaged registry annex copies",
            },
        ],
        rewards=[
            {"action_type": "give_scales", "amount": 85},
            {"action_type": "modify_standing", "faction_id": "empire", "delta": 100},
            {"action_type": "give_skill_xp", "skill_id": "investigation", "count": 3},
            {
                "action_type": "echo",
                "message": "|gSeln presses the copied leaves flat with careful fingers. \"So it wasn't clerical error after all.\"|n",
            },
        ],
        objective_type="investigate",
        objective_target="mw_registry_annex",
        objective_count=1,
    )

    area.quest(
        "vp_q_courier_manifest",
        name="Courier Manifest",
        description=(
            "Registrar Taveth needs a sealed routing manifest carried from the "
            "Permit Hall to the Courier Platform without passing it through the "
            "usual desk chain. He claims it is an efficiency matter; his voice "
            "suggests otherwise."
        ),
        quest_type="delivery",
        quest_giver="npc_registrar_taveth",
        objectives=[
            {
                "type": "deliver",
                "target": "npc_courier_factor_helian",
                "count": 1,
                "description": "Deliver the sealed manifest to Courier Factor Helian",
            },
        ],
        flagged_drop="courier_manifest_packet",
        rewards=[
            {"action_type": "give_scales", "amount": 70},
            {"action_type": "modify_standing", "faction_id": "empire", "delta": 90},
            {
                "action_type": "discover_flight_point",
                "point_id": "tremen_courier",
                "message": "|gHelian copies the Tremen lift line onto your manifest slate. The destination is now available from any connected Courier platform.|n",
            },
            {
                "action_type": "discover_flight_point",
                "point_id": "korahei_courier",
                "message": "|gHelian adds the long-haul Korahei exchange marks to your route slate. Beside them he copies the island note exactly: arrival grants passage, not entitlement.|n",
            },
            {
                "action_type": "echo",
                "message": "|gHelian checks the seal twice before tucking the manifest away. \"Good. Better it came by hand.\"|n",
            },
        ],
        objective_type="deliver",
        objective_target="npc_courier_factor_helian",
        objective_count=1,
    )

    area.quest(
        "vp_q_stagcrown_petition",
        name="The Stagcrown Petition",
        description=(
            "Steward Maelin Rhest wants a petition for preserve access entered "
            "cleanly and quietly through the permit machinery before a rival "
            "house notices. Take the matter to Registrar Taveth and return with "
            "his answer."
        ),
        quest_type="social",
        quest_giver="npc_steward_maelin_rhest",
        objectives=[
            {
                "type": "deliver",
                "target": "npc_registrar_taveth",
                "count": 1,
                "description": "Carry House Rhest's petition to Registrar Taveth",
            },
        ],
        flagged_drop="stagcrown_petition",
        rewards=[
            {"action_type": "give_scales", "amount": 90},
            {"action_type": "modify_standing", "faction_id": "empire", "delta": 75},
            {
                "action_type": "echo",
                "message": "|gMaelin folds the reply into his sleeve without reading it in public. \"You understand discretion. That matters here.\"|n",
            },
        ],
        objective_type="deliver",
        objective_target="npc_registrar_taveth",
        objective_count=1,
    )

    area.quest(
        "vp_q_shuttered_press",
        name="Shuttered Press",
        description=(
            "Printkeeper Elais suspects the drains below the city are being "
            "watched again. Check the old cistern for fresh use and return with "
            "anything that proves the ward has not gone quiet by chance."
        ),
        quest_type="investigation",
        quest_giver="npc_printkeeper_elais",
        objectives=[
            {
                "type": "investigate",
                "target": "hw_old_cistern",
                "count": 1,
                "description": "Investigate the old cistern for signs of recent surveillance",
            },
        ],
        rewards=[
            {"action_type": "give_scales", "amount": 95},
            {"action_type": "give_skill_xp", "skill_id": "investigation", "count": 3},
            {
                "action_type": "echo",
                "message": "|gElais studies what you found, then feeds one scrap to the lamp flame. \"Good. Then we plan for watchers, not ghosts.\"|n",
            },
        ],
        objective_type="investigate",
        objective_target="hw_old_cistern",
        objective_count=1,
    )

    area.quest(
        "vp_q_split_roadwheel",
        name="Split Roadwheel",
        description=(
            "Roads Assessor Mirel believes one of the old toll tables still "
            "preserves an earlier wording of the Edict of Measured Passage. "
            "Search the toll archive and confirm what the newer copies tried "
            "to smooth away."
        ),
        quest_type="investigation",
        quest_giver="npc_roads_assessor_mirel",
        objectives=[
            {
                "type": "investigate",
                "target": "ca_toll_archive",
                "count": 1,
                "description": "Investigate the old toll archive",
            },
        ],
        rewards=[
            {"action_type": "give_scales", "amount": 80},
            {"action_type": "modify_standing", "faction_id": "empire", "delta": 60},
            {"action_type": "give_skill_xp", "skill_id": "investigation", "count": 2},
            {
                "action_type": "echo",
                "message": "|gMirel studies the wording in silence, then nods once. \"So the archive kept a spine after all.\"|n",
            },
        ],
        objective_type="investigate",
        objective_target="ca_toll_archive",
        objective_count=1,
    )

    area.quest(
        "vp_q_confiscated_measure",
        name="Confiscated Measure",
        description=(
            "Seal Keeper Jori needs an answer she cannot request through the "
            "proper desk chain. Search the confiscation room for the missing "
            "instruction packet before it is moved, altered, or officially lost."
        ),
        quest_type="investigation",
        quest_giver="npc_seal_keeper_jori",
        objectives=[
            {
                "type": "investigate",
                "target": "mw_confiscation_room",
                "count": 1,
                "description": "Investigate the confiscation room for the missing packet",
            },
        ],
        rewards=[
            {"action_type": "give_scales", "amount": 90},
            {"action_type": "modify_standing", "faction_id": "empire", "delta": 85},
            {"action_type": "give_skill_xp", "skill_id": "investigation", "count": 3},
            {
                "action_type": "echo",
                "message": "|gJori closes the packet without opening it. \"Good. Then I still have time to decide who is allowed to know this existed.\"|n",
            },
        ],
        objective_type="investigate",
        objective_target="mw_confiscation_room",
        objective_count=1,
    )

    area.quest(
        "vp_q_quiet_pen",
        name="Quiet Pen",
        description=(
            "Handler Sergeant Vorun has noticed unlogged movement beneath the "
            "enclave and wants it checked before it becomes a reportable failure. "
            "Search the restricted tunnel and determine whether the trouble is "
            "theft, vermin, or something more deliberate."
        ),
        quest_type="investigation",
        quest_giver="npc_handler_sergeant_vorun",
        objectives=[
            {
                "type": "investigate",
                "target": "dc_restricted_tunnel",
                "count": 1,
                "description": "Investigate the restricted tunnel",
            },
        ],
        rewards=[
            {"action_type": "give_scales", "amount": 100},
            {"action_type": "modify_standing", "faction_id": "empire", "delta": 95},
            {
                "action_type": "echo",
                "message": "|gVorun's expression does not change, but his shoulders ease a fraction. \"Good. Better a tunnel problem than a platform scandal.\"|n",
            },
        ],
        objective_type="investigate",
        objective_target="dc_restricted_tunnel",
        objective_count=1,
    )

    area.quest(
        "vp_q_cinder_proof",
        name="Cinder Proof",
        description=(
            "Cinder Runner Mara needs a half-burned proof recovered from the "
            "burnt store before another sweep claims it. Search the room and "
            "bring back whatever survived the fire and the panic after it."
        ),
        quest_type="investigation",
        quest_giver="npc_cinder_runner_mara",
        objectives=[
            {
                "type": "investigate",
                "target": "hw_burnt_store",
                "count": 1,
                "description": "Investigate the burnt store for the missing proof",
            },
        ],
        rewards=[
            {"action_type": "give_scales", "amount": 90},
            {"action_type": "give_skill_xp", "skill_id": "investigation", "count": 3},
            {
                "action_type": "echo",
                "message": "|gMara slides the singed proof into an oilskin sleeve. \"Ugly work, but useful. That's usually how truth survives down here.\"|n",
            },
        ],
        objective_type="investigate",
        objective_target="hw_burnt_store",
        objective_count=1,
    )

    area.quest(
        "vp_q_brokered_passage",
        name="Brokered Passage",
        description=(
            "Caravan Marshal Tev wants to know who is inflating rush prices for "
            "approved road work in the commons. Search Broker Steps and report what "
            "rates are being demanded for official movement."
        ),
        quest_type="investigation",
        quest_giver="npc_caravan_marshal_tev",
        objectives=[
            {
                "type": "investigate",
                "target": "oc_broker_steps",
                "count": 1,
                "description": "Investigate Broker Steps",
            },
        ],
        rewards=[
            {"action_type": "give_scales", "amount": 85},
            {"action_type": "modify_standing", "faction_id": "empire", "delta": 70},
            {
                "action_type": "echo",
                "message": "|gTev exhales through his teeth. \"Thought so. The city taxes the road once and the brokers tax it again.\"|n",
            },
        ],
        objective_type="investigate",
        objective_target="oc_broker_steps",
        objective_count=1,
    )

    area.quest(
        "vp_q_witness_copy",
        name="Witness Copy",
        description=(
            "Petition Clerk Vessa needs an older witness record checked before it "
            "is replaced by a cleaner copy. Search the witness chamber for the "
            "relevant roll and bring back what survives of the original wording."
        ),
        quest_type="investigation",
        quest_giver="npc_petition_clerk_vessa",
        objectives=[
            {
                "type": "investigate",
                "target": "mw_witness_chamber",
                "count": 1,
                "description": "Investigate the witness chamber",
            },
        ],
        rewards=[
            {"action_type": "give_scales", "amount": 95},
            {"action_type": "modify_standing", "faction_id": "empire", "delta": 90},
            {"action_type": "give_skill_xp", "skill_id": "investigation", "count": 3},
            {
                "action_type": "echo",
                "message": "|gVessa reads the line twice, then folds it flat. \"Good. Then I know what version they're trying to make disappear.\"|n",
            },
        ],
        objective_type="investigate",
        objective_target="mw_witness_chamber",
        objective_count=1,
    )

    area.quest(
        "vp_q_dispatch_delay",
        name="Dispatch Delay",
        description=(
            "Dispatch Officer Sevain needs a corrected routing note carried from "
            "the dispatch office to Courier Factor Helian before a delay becomes "
            "public embarrassment. Take the note up to the platform and return "
            "with Helian's answer."
        ),
        quest_type="delivery",
        quest_giver="npc_dispatch_officer_sevain",
        objectives=[
            {
                "type": "deliver",
                "target": "npc_courier_factor_helian",
                "count": 1,
                "description": "Deliver the corrected routing note to Courier Factor Helian",
            },
        ],
        flagged_drop="dispatch_correction_note",
        rewards=[
            {"action_type": "give_scales", "amount": 90},
            {"action_type": "modify_standing", "faction_id": "empire", "delta": 85},
            {
                "action_type": "echo",
                "message": "|gSevain scans Helian's reply and allows herself one tired nod. \"Good. Then the delay remains procedural instead of political.\"|n",
            },
        ],
        objective_type="deliver",
        objective_target="npc_courier_factor_helian",
        objective_count=1,
    )

    area.quest(
        "vp_q_sluice_cipher",
        name="Sluice Cipher",
        description=(
            "Cache Keeper Dren believes a dead route beneath the city has gone "
            "live again. Search the old sluice gate for fresh marks and bring "
            "back anything that proves the path is being used."
        ),
        quest_type="investigation",
        quest_giver="npc_cache_keeper_dren",
        objectives=[
            {
                "type": "investigate",
                "target": "hw_sluice_gate",
                "count": 1,
                "description": "Investigate the old sluice gate",
            },
        ],
        rewards=[
            {"action_type": "give_scales", "amount": 100},
            {"action_type": "give_skill_xp", "skill_id": "investigation", "count": 3},
            {
                "action_type": "echo",
                "message": "|gDren studies the marks, then tucks the proof into his coat. \"Then the route still breathes. Good. We'll need it.\"|n",
            },
        ],
        objective_type="investigate",
        objective_target="hw_sluice_gate",
        objective_count=1,
    )

    return area.build()
