"""
Equipment Catalog — master item definitions for Soravelon M1.

Defines 69+ equipment items across 3 material tiers (iron/steel/mithril)
covering all 13 equipment slots, plus basic consumable potions.

This is a utility zone spec — no rooms, just item definitions registered
via area.item() for use by vendors, loot tables, and crafting outputs.

Per CON-04: No procedural affixes. All items are static definitions.
Per D-41: No durability system.
Per D-36: Weight values are cosmetic (no encumbrance enforcement).
Per D-33: Soft stat requirements via scaling_stat (no hard checks).
Per D-42: Weapons have damage_min/damage_max + stat scaling.
Per D-39: Shields are passive off_hand armor.
Per D-38: Two-handed weapons use both hand slots.
"""

from world.area_builder import AreaBuilder


def build():
    area = AreaBuilder("equipment_catalog")
    area.zone(
        "equipment_catalog",
        "Equipment Catalog",
        zone_type="frontier",
        continent="varath",
    )

    # ==================================================================
    # WEAPONS — main_hand (21 items: 7 types x 3 tiers)
    # ==================================================================

    # --- Swords (balanced, strength scaling) ---
    area.item("iron_sword", key="Iron Sword", item_type="equipment",
              equip_slot="main_hand", damage_min=8, damage_max=14,
              stat_bonuses={"strength": 1}, material_tier=1,
              scaling_stat="strength",
              weight=3.0, rarity="normal", value=25,
              desc="A sturdy iron longsword with a simple crossguard.")
    area.item("steel_sword", key="Steel Sword", item_type="equipment",
              equip_slot="main_hand", damage_min=12, damage_max=20,
              stat_bonuses={"strength": 2}, material_tier=2,
              scaling_stat="strength",
              weight=3.0, rarity="normal", value=60,
              desc="A well-forged steel blade with a leather-wrapped grip.")
    area.item("mithril_sword", key="Mithril Sword", item_type="equipment",
              equip_slot="main_hand", damage_min=16, damage_max=28,
              stat_bonuses={"strength": 3}, material_tier=3,
              scaling_stat="strength",
              weight=2.5, rarity="rare", value=200,
              desc="A gleaming mithril blade, impossibly light and razor-sharp.")

    # --- Daggers (fast, agility scaling) ---
    area.item("iron_dagger", key="Iron Dagger", item_type="equipment",
              equip_slot="main_hand", damage_min=4, damage_max=10,
              stat_bonuses={"agility": 1}, material_tier=1,
              scaling_stat="agility",
              weight=1.0, rarity="normal", value=15,
              desc="A simple iron dagger with a tapered blade.")
    area.item("steel_dagger", key="Steel Dagger", item_type="equipment",
              equip_slot="main_hand", damage_min=6, damage_max=14,
              stat_bonuses={"agility": 2}, material_tier=2,
              scaling_stat="agility",
              weight=1.0, rarity="normal", value=40,
              desc="A keen steel dagger balanced for quick strikes.")
    area.item("mithril_dagger", key="Mithril Dagger", item_type="equipment",
              equip_slot="main_hand", damage_min=8, damage_max=20,
              stat_bonuses={"agility": 3}, material_tier=3,
              scaling_stat="agility",
              weight=0.5, rarity="rare", value=160,
              desc="A whisper-thin mithril stiletto that seems to find gaps in armor.")

    # --- Maces (slow, strength scaling, high damage) ---
    area.item("iron_mace", key="Iron Mace", item_type="equipment",
              equip_slot="main_hand", damage_min=10, damage_max=16,
              stat_bonuses={"strength": 1}, material_tier=1,
              scaling_stat="strength",
              weight=4.0, rarity="normal", value=30,
              desc="A heavy iron mace with a flanged head.")
    area.item("steel_mace", key="Steel Mace", item_type="equipment",
              equip_slot="main_hand", damage_min=14, damage_max=22,
              stat_bonuses={"strength": 2}, material_tier=2,
              scaling_stat="strength",
              weight=4.0, rarity="normal", value=70,
              desc="A steel warhammer with a reinforced striking face.")
    area.item("mithril_mace", key="Mithril Mace", item_type="equipment",
              equip_slot="main_hand", damage_min=18, damage_max=30,
              stat_bonuses={"strength": 3}, material_tier=3,
              scaling_stat="strength",
              weight=3.5, rarity="rare", value=220,
              desc="A mithril morningstar that rings with a clear tone on impact.")

    # --- Staves (two-handed, willpower/mana scaling) ---
    area.item("iron_staff", key="Iron-Shod Staff", item_type="equipment",
              equip_slot="main_hand", damage_min=6, damage_max=12,
              stat_bonuses={"mana": 2}, material_tier=1,
              scaling_stat="mana", two_handed=True,
              weight=3.5, rarity="normal", value=30,
              desc="A gnarled wooden staff capped with iron at both ends.")
    area.item("steel_staff", key="Steel-Bound Staff", item_type="equipment",
              equip_slot="main_hand", damage_min=10, damage_max=18,
              stat_bonuses={"mana": 3}, material_tier=2,
              scaling_stat="mana", two_handed=True,
              weight=3.5, rarity="normal", value=75,
              desc="A polished staff reinforced with steel bands etched with faint runes.")
    area.item("mithril_staff", key="Mithril Staff", item_type="equipment",
              equip_slot="main_hand", damage_min=14, damage_max=24,
              stat_bonuses={"mana": 5}, material_tier=3,
              scaling_stat="mana", two_handed=True,
              weight=2.0, rarity="rare", value=250,
              desc="A slender mithril staff that hums with barely contained arcane resonance.")

    # --- Greatswords (two-handed, strength scaling) ---
    area.item("iron_greatsword", key="Iron Greatsword", item_type="equipment",
              equip_slot="main_hand", damage_min=12, damage_max=20,
              stat_bonuses={"strength": 2}, material_tier=1,
              scaling_stat="strength", two_handed=True,
              weight=6.0, rarity="normal", value=40,
              desc="A broad iron blade requiring two hands to wield effectively.")
    area.item("steel_greatsword", key="Steel Greatsword", item_type="equipment",
              equip_slot="main_hand", damage_min=18, damage_max=30,
              stat_bonuses={"strength": 3}, material_tier=2,
              scaling_stat="strength", two_handed=True,
              weight=6.0, rarity="normal", value=90,
              desc="A massive steel claymore with a wire-wrapped hilt.")
    area.item("mithril_greatsword", key="Mithril Greatsword", item_type="equipment",
              equip_slot="main_hand", damage_min=24, damage_max=40,
              stat_bonuses={"strength": 5}, material_tier=3,
              scaling_stat="strength", two_handed=True,
              weight=4.5, rarity="rare", value=300,
              desc="A mithril greatsword that moves like a feather despite its size.")

    # --- Greataxes (two-handed, highest damage, strength scaling) ---
    area.item("iron_greataxe", key="Iron Greataxe", item_type="equipment",
              equip_slot="main_hand", damage_min=14, damage_max=22,
              stat_bonuses={"strength": 2}, material_tier=1,
              scaling_stat="strength", two_handed=True,
              weight=7.0, rarity="normal", value=45,
              desc="A heavy iron axe with a crescent blade on a long haft.")
    area.item("steel_greataxe", key="Steel Greataxe", item_type="equipment",
              equip_slot="main_hand", damage_min=20, damage_max=34,
              stat_bonuses={"strength": 3}, material_tier=2,
              scaling_stat="strength", two_handed=True,
              weight=7.0, rarity="normal", value=100,
              desc="A brutal steel battleaxe with a bearded cutting edge.")
    area.item("mithril_greataxe", key="Mithril Greataxe", item_type="equipment",
              equip_slot="main_hand", damage_min=28, damage_max=44,
              stat_bonuses={"strength": 5}, material_tier=3,
              scaling_stat="strength", two_handed=True,
              weight=5.0, rarity="rare", value=320,
              desc="A mithril greataxe whose edge never dulls, inscribed with dwarven runes.")

    # --- Bows (ranged flavor only per D-32, agility scaling) ---
    area.item("iron_bow", key="Short Bow", item_type="equipment",
              equip_slot="main_hand", damage_min=6, damage_max=12,
              stat_bonuses={"agility": 1}, material_tier=1,
              scaling_stat="agility", two_handed=True,
              weight=2.0, rarity="normal", value=20,
              desc="A simple short bow of yew, tipped with iron nocks.")
    area.item("steel_bow", key="Composite Bow", item_type="equipment",
              equip_slot="main_hand", damage_min=10, damage_max=18,
              stat_bonuses={"agility": 2}, material_tier=2,
              scaling_stat="agility", two_handed=True,
              weight=2.5, rarity="normal", value=55,
              desc="A composite bow reinforced with steel laminate for greater draw.")
    area.item("mithril_bow", key="Mithril Longbow", item_type="equipment",
              equip_slot="main_hand", damage_min=14, damage_max=24,
              stat_bonuses={"agility": 3}, material_tier=3,
              scaling_stat="agility", two_handed=True,
              weight=1.5, rarity="rare", value=200,
              desc="An elegant mithril-reinforced longbow with uncanny accuracy.")

    # ==================================================================
    # SHIELDS — off_hand (6 items: 2 types x 3 tiers)
    # ==================================================================

    # --- Bucklers (light shield, small armor_value) ---
    area.item("iron_buckler", key="Iron Buckler", item_type="equipment",
              equip_slot="off_hand", armor_value=3,
              stat_bonuses={"endurance": 1}, material_tier=1,
              weight=2.0, rarity="normal", value=20,
              desc="A small round iron shield strapped to the forearm.")
    area.item("steel_buckler", key="Steel Buckler", item_type="equipment",
              equip_slot="off_hand", armor_value=5,
              stat_bonuses={"endurance": 1}, material_tier=2,
              weight=2.0, rarity="normal", value=50,
              desc="A polished steel buckler with a reinforced boss.")
    area.item("mithril_buckler", key="Mithril Buckler", item_type="equipment",
              equip_slot="off_hand", armor_value=7,
              stat_bonuses={"endurance": 2}, material_tier=3,
              weight=1.0, rarity="rare", value=180,
              desc="A featherlight mithril buckler that turns blades effortlessly.")

    # --- Kite Shields (heavy shield, larger armor_value) ---
    area.item("iron_kite_shield", key="Iron Kite Shield", item_type="equipment",
              equip_slot="off_hand", armor_value=5,
              stat_bonuses={"endurance": 1, "strength": 1}, material_tier=1,
              weight=5.0, rarity="normal", value=35,
              desc="A tall iron kite shield bearing no heraldry.")
    area.item("steel_kite_shield", key="Steel Kite Shield", item_type="equipment",
              equip_slot="off_hand", armor_value=8,
              stat_bonuses={"endurance": 2, "strength": 1}, material_tier=2,
              weight=5.0, rarity="normal", value=80,
              desc="A heavy steel kite shield with a riveted border.")
    area.item("mithril_kite_shield", key="Mithril Kite Shield", item_type="equipment",
              equip_slot="off_hand", armor_value=11,
              stat_bonuses={"endurance": 3, "strength": 2}, material_tier=3,
              weight=3.0, rarity="rare", value=280,
              desc="A mithril tower shield, impossibly light for its coverage.")

    # ==================================================================
    # ARMOR — LIGHT SET (leather, agility-friendly)
    # 5 slots x 3 tiers = 15 items
    # ==================================================================

    # --- Head ---
    area.item("leather_cap", key="Leather Cap", item_type="equipment",
              equip_slot="head", armor_value=1,
              stat_bonuses={"agility": 1}, material_tier=1,
              weight=0.5, rarity="normal", value=10,
              desc="A fitted leather cap that covers the crown.")
    area.item("hardened_leather_cap", key="Hardened Leather Cap", item_type="equipment",
              equip_slot="head", armor_value=2,
              stat_bonuses={"agility": 1}, material_tier=2,
              weight=0.5, rarity="normal", value=25,
              desc="A boiled leather cap reinforced with brass studs.")
    area.item("shadowsilk_hood", key="Shadowsilk Hood", item_type="equipment",
              equip_slot="head", armor_value=3,
              stat_bonuses={"agility": 2}, material_tier=3,
              weight=0.3, rarity="rare", value=120,
              desc="A hood woven from shadowsilk, dark as a moonless night.")

    # --- Chest ---
    area.item("leather_vest", key="Leather Vest", item_type="equipment",
              equip_slot="chest", armor_value=3,
              stat_bonuses={"agility": 1}, material_tier=1,
              weight=3.0, rarity="normal", value=30,
              desc="A sleeveless leather vest, supple and easy to move in.")
    area.item("hardened_leather_vest", key="Hardened Leather Cuirass", item_type="equipment",
              equip_slot="chest", armor_value=5,
              stat_bonuses={"agility": 2}, material_tier=2,
              weight=3.5, rarity="normal", value=70,
              desc="A cuirass of boiled leather layered with metal rivets.")
    area.item("shadowsilk_tunic", key="Shadowsilk Tunic", item_type="equipment",
              equip_slot="chest", armor_value=7,
              stat_bonuses={"agility": 3}, material_tier=3,
              weight=1.5, rarity="rare", value=200,
              desc="A form-fitting tunic that seems to absorb light around it.")

    # --- Hands ---
    area.item("leather_gloves", key="Leather Gloves", item_type="equipment",
              equip_slot="hands", armor_value=1,
              stat_bonuses={"agility": 1}, material_tier=1,
              weight=0.3, rarity="normal", value=8,
              desc="Thin leather gloves that preserve dexterity.")
    area.item("hardened_leather_gloves", key="Hardened Leather Gauntlets", item_type="equipment",
              equip_slot="hands", armor_value=2,
              stat_bonuses={"agility": 1}, material_tier=2,
              weight=0.5, rarity="normal", value=20,
              desc="Gauntlets of hardened leather with reinforced knuckles.")
    area.item("shadowsilk_gloves", key="Shadowsilk Gloves", item_type="equipment",
              equip_slot="hands", armor_value=3,
              stat_bonuses={"agility": 2}, material_tier=3,
              weight=0.2, rarity="rare", value=90,
              desc="Gossamer-thin gloves that enhance grip and nimbleness.")

    # --- Legs ---
    area.item("leather_leggings", key="Leather Leggings", item_type="equipment",
              equip_slot="legs", armor_value=2,
              stat_bonuses={"agility": 1}, material_tier=1,
              weight=2.0, rarity="normal", value=18,
              desc="Fitted leather leggings with cord lacing.")
    area.item("hardened_leather_leggings", key="Hardened Leather Greaves", item_type="equipment",
              equip_slot="legs", armor_value=3,
              stat_bonuses={"agility": 1}, material_tier=2,
              weight=2.5, rarity="normal", value=40,
              desc="Greaves of stiffened leather with articulated knee guards.")
    area.item("shadowsilk_leggings", key="Shadowsilk Leggings", item_type="equipment",
              equip_slot="legs", armor_value=5,
              stat_bonuses={"agility": 2}, material_tier=3,
              weight=1.0, rarity="rare", value=140,
              desc="Leggings that seem to meld with shadow, muffling every step.")

    # --- Feet ---
    area.item("leather_boots", key="Leather Boots", item_type="equipment",
              equip_slot="feet", armor_value=1,
              stat_bonuses={"agility": 1}, material_tier=1,
              weight=1.0, rarity="normal", value=12,
              desc="Worn leather boots with a soft sole.")
    area.item("hardened_leather_boots", key="Hardened Leather Boots", item_type="equipment",
              equip_slot="feet", armor_value=2,
              stat_bonuses={"agility": 1}, material_tier=2,
              weight=1.5, rarity="normal", value=30,
              desc="Sturdy boots with hardened leather shin guards.")
    area.item("shadowsilk_boots", key="Shadowsilk Boots", item_type="equipment",
              equip_slot="feet", armor_value=3,
              stat_bonuses={"agility": 2}, material_tier=3,
              weight=0.5, rarity="rare", value=110,
              desc="Near-silent boots that leave no tracks on stone.")

    # ==================================================================
    # ARMOR — HEAVY SET (plate, strength-friendly)
    # 5 slots x 3 tiers = 15 items
    # ==================================================================

    # --- Head ---
    area.item("iron_helm", key="Iron Helm", item_type="equipment",
              equip_slot="head", armor_value=2,
              stat_bonuses={"strength": 1}, material_tier=1,
              weight=2.0, rarity="normal", value=18,
              desc="An open-faced iron helm with a nose guard.")
    area.item("steel_helm", key="Steel Helm", item_type="equipment",
              equip_slot="head", armor_value=4,
              stat_bonuses={"strength": 1, "endurance": 1}, material_tier=2,
              weight=2.5, rarity="normal", value=45,
              desc="A full steel helm with cheek plates and a visor slot.")
    area.item("mithril_helm", key="Mithril Helm", item_type="equipment",
              equip_slot="head", armor_value=6,
              stat_bonuses={"strength": 2, "endurance": 1}, material_tier=3,
              weight=1.5, rarity="rare", value=180,
              desc="A mithril helm that gleams like starlight, light as a circlet.")

    # --- Chest ---
    area.item("iron_breastplate", key="Iron Breastplate", item_type="equipment",
              equip_slot="chest", armor_value=5,
              stat_bonuses={"strength": 1, "endurance": 1}, material_tier=1,
              weight=8.0, rarity="normal", value=50,
              desc="A hammered iron breastplate with leather strapping.")
    area.item("steel_breastplate", key="Steel Breastplate", item_type="equipment",
              equip_slot="chest", armor_value=8,
              stat_bonuses={"strength": 2, "endurance": 1}, material_tier=2,
              weight=8.0, rarity="normal", value=120,
              desc="A well-crafted steel cuirass with articulated shoulder guards.")
    area.item("mithril_breastplate", key="Mithril Breastplate", item_type="equipment",
              equip_slot="chest", armor_value=12,
              stat_bonuses={"strength": 3, "endurance": 2}, material_tier=3,
              weight=4.0, rarity="rare", value=350,
              desc="A mithril breastplate that fits like a second skin, utterly impenetrable.")

    # --- Hands ---
    area.item("iron_gauntlets", key="Iron Gauntlets", item_type="equipment",
              equip_slot="hands", armor_value=2,
              stat_bonuses={"strength": 1}, material_tier=1,
              weight=1.5, rarity="normal", value=15,
              desc="Heavy iron gauntlets with articulated fingers.")
    area.item("steel_gauntlets", key="Steel Gauntlets", item_type="equipment",
              equip_slot="hands", armor_value=3,
              stat_bonuses={"strength": 1, "endurance": 1}, material_tier=2,
              weight=1.5, rarity="normal", value=35,
              desc="Reinforced steel gauntlets with knuckle ridges.")
    area.item("mithril_gauntlets", key="Mithril Gauntlets", item_type="equipment",
              equip_slot="hands", armor_value=5,
              stat_bonuses={"strength": 2, "endurance": 1}, material_tier=3,
              weight=0.8, rarity="rare", value=150,
              desc="Mithril gauntlets so responsive they feel like bare hands.")

    # --- Legs ---
    area.item("iron_greaves", key="Iron Greaves", item_type="equipment",
              equip_slot="legs", armor_value=3,
              stat_bonuses={"strength": 1, "endurance": 1}, material_tier=1,
              weight=3.0, rarity="normal", value=25,
              desc="Iron leg plates with leather backing.")
    area.item("steel_greaves", key="Steel Greaves", item_type="equipment",
              equip_slot="legs", armor_value=5,
              stat_bonuses={"strength": 1, "endurance": 1}, material_tier=2,
              weight=3.5, rarity="normal", value=55,
              desc="Articulated steel greaves covering shin to thigh.")
    area.item("mithril_greaves", key="Mithril Greaves", item_type="equipment",
              equip_slot="legs", armor_value=7,
              stat_bonuses={"strength": 2, "endurance": 2}, material_tier=3,
              weight=2.0, rarity="rare", value=200,
              desc="Mithril leg armor that bends and flexes like liquid metal.")

    # --- Feet ---
    area.item("iron_sabatons", key="Iron Sabatons", item_type="equipment",
              equip_slot="feet", armor_value=2,
              stat_bonuses={"strength": 1}, material_tier=1,
              weight=2.0, rarity="normal", value=18,
              desc="Heavy iron boots that clank with each step.")
    area.item("steel_sabatons", key="Steel Sabatons", item_type="equipment",
              equip_slot="feet", armor_value=3,
              stat_bonuses={"strength": 1, "endurance": 1}, material_tier=2,
              weight=2.5, rarity="normal", value=40,
              desc="Steel-plated boots with reinforced soles.")
    area.item("mithril_sabatons", key="Mithril Sabatons", item_type="equipment",
              equip_slot="feet", armor_value=5,
              stat_bonuses={"strength": 2, "endurance": 1}, material_tier=3,
              weight=1.0, rarity="rare", value=160,
              desc="Mithril boots that ring like bells on stone floors.")

    # ==================================================================
    # ACCESSORIES (12 items)
    # ==================================================================

    # --- Cloaks (back slot) ---
    area.item("travelers_cloak", key="Traveler's Cloak", item_type="equipment",
              equip_slot="back", armor_value=1,
              stat_bonuses={"endurance": 1}, material_tier=1,
              weight=1.0, rarity="normal", value=15,
              desc="A weathered wool cloak that keeps the rain off.")
    area.item("rangers_cloak", key="Ranger's Cloak", item_type="equipment",
              equip_slot="back", armor_value=2,
              stat_bonuses={"agility": 1, "acuity": 1}, material_tier=2,
              weight=1.0, rarity="normal", value=45,
              desc="A mottled green cloak that helps the wearer blend into foliage.")
    area.item("cloak_of_shadows", key="Cloak of Shadows", item_type="equipment",
              equip_slot="back", armor_value=3,
              stat_bonuses={"agility": 2, "acuity": 2}, material_tier=3,
              weight=0.5, rarity="rare", value=200,
              desc="A cloak of shifting darkness that writhes at the edges of vision.")

    # --- Bracers (wrists slot) ---
    area.item("leather_bracers", key="Leather Bracers", item_type="equipment",
              equip_slot="wrists", armor_value=1,
              stat_bonuses={"strength": 1}, material_tier=1,
              weight=0.5, rarity="normal", value=10,
              desc="Simple leather bracers laced tight around the forearms.")
    area.item("steel_bracers", key="Steel Vambraces", item_type="equipment",
              equip_slot="wrists", armor_value=2,
              stat_bonuses={"strength": 1, "endurance": 1}, material_tier=2,
              weight=1.0, rarity="normal", value=30,
              desc="Polished steel vambraces engraved with geometric patterns.")

    # --- Rings (ring1/ring2 slots) ---
    area.item("iron_band", key="Iron Band", item_type="equipment",
              equip_slot="ring1", armor_value=0,
              stat_bonuses={"endurance": 1}, material_tier=1,
              weight=0.1, rarity="normal", value=8,
              desc="A plain iron ring, cold to the touch.")
    area.item("signet_ring", key="Signet Ring", item_type="equipment",
              equip_slot="ring1", armor_value=0,
              stat_bonuses={"presence": 1}, material_tier=1,
              weight=0.1, rarity="normal", value=20,
              desc="A silver signet ring bearing an unrecognizable crest.")
    area.item("ring_of_acuity", key="Ring of Acuity", item_type="equipment",
              equip_slot="ring1", armor_value=0,
              stat_bonuses={"acuity": 2}, material_tier=2,
              weight=0.1, rarity="normal", value=60,
              desc="A thin gold ring set with a tiny sapphire that sharpens the mind.")
    area.item("mithril_ring", key="Mithril Ring", item_type="equipment",
              equip_slot="ring1", armor_value=0,
              stat_bonuses={"resonance": 2, "mana": 1}, material_tier=3,
              weight=0.1, rarity="rare", value=150,
              desc="A mithril ring that vibrates faintly near sources of magical power.")

    # --- Amulets (amulet slot) ---
    area.item("bone_talisman", key="Bone Talisman", item_type="equipment",
              equip_slot="amulet", armor_value=0,
              stat_bonuses={"resonance": 1}, material_tier=1,
              weight=0.2, rarity="normal", value=12,
              desc="A crude talisman carved from animal bone, strung on sinew.")
    area.item("silver_pendant", key="Silver Pendant", item_type="equipment",
              equip_slot="amulet", armor_value=0,
              stat_bonuses={"mana": 2}, material_tier=2,
              weight=0.2, rarity="normal", value=50,
              desc="A silver pendant shaped like a crescent moon.")
    area.item("amulet_of_warding", key="Amulet of Warding", item_type="equipment",
              equip_slot="amulet", armor_value=0,
              stat_bonuses={"mana": 2, "endurance": 2}, material_tier=3,
              weight=0.2, rarity="rare", value=180,
              desc="An ancient amulet inscribed with protective glyphs that pulse faintly.")

    # --- Face (face slot) ---
    area.item("leather_mask", key="Leather Mask", item_type="equipment",
              equip_slot="face", armor_value=1,
              stat_bonuses={"acuity": 1}, material_tier=1,
              weight=0.3, rarity="normal", value=10,
              desc="A half-mask of cured leather that covers nose and cheeks.")
    area.item("steel_visor", key="Steel Visor", item_type="equipment",
              equip_slot="face", armor_value=2,
              stat_bonuses={"acuity": 1, "endurance": 1}, material_tier=2,
              weight=0.5, rarity="normal", value=35,
              desc="A hinged steel visor attached to a leather headband.")

    # ==================================================================
    # CONSUMABLES (4 items per D-44)
    # ==================================================================

    area.item("minor_healing_potion", key="Minor Healing Potion",
              item_type="consumable",
              use_effect={"type": "heal_hp", "amount": 30},
              weight=0.5, rarity="normal", value=10,
              desc="A small vial of ruddy liquid that mends minor wounds.")
    area.item("minor_stamina_potion", key="Minor Stamina Potion",
              item_type="consumable",
              use_effect={"type": "restore_stamina", "amount": 20},
              weight=0.5, rarity="normal", value=10,
              desc="A fizzing green tonic that restores flagging stamina.")
    area.item("antidote_potion", key="Antidote", item_type="consumable",
              use_effect={"type": "cure_poison"},
              weight=0.3, rarity="normal", value=15,
              desc="A bitter white draught that neutralizes most common poisons.")
    area.item("bandage", key="Linen Bandage", item_type="consumable",
              use_effect={"type": "heal_over_time", "amount": 5, "ticks": 6},
              weight=0.2, rarity="normal", value=5,
              desc="A roll of clean linen for binding wounds. Heals slowly over time.")

    return area.build()
