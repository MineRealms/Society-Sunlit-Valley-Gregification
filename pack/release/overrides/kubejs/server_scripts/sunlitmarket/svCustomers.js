// priority: 10
// ============================================================
// Sunlit Valley professions as customer sources for the pawn counter.
//
// Customer identity is data-driven: vanilla professions and explicit entities
// are matched by MarketRules (entity / profession selectors), never by locale
// or custom name. Shipping Bin values from global.trades are the common price
// anchor, so a counter purchase can be compared with a real pack money sink.
//
// Price policy (see docs/SUNLIT_VALLEY_INTEGRATION.md):
//   market = shipping value (what the player could get at a Shipping Bin)
//   ask    = market * category ratio (below 1.0 = player has a margin)
//   base   = market * 0.60 (display/haggle reference, not a second price)
// ============================================================
if (typeof SunlitMarket !== 'undefined' && typeof global !== 'undefined' && global.trades && Platform.isLoaded('society')) {
  let svValue = (id, fallback) => {
    let row = global.trades.get(id)
    return row && row.value > 0 ? row.value : fallback
  }
  let svSlug = (id) => String(id).replace(/[^a-z0-9_]+/g, '_')
  let addNpc = (key, faction, entity, profession) => {
    let rule = { type: 'npc', id: 'sv.npc.' + key, faction: faction, rank: 'CIVILIAN' }
    if (entity) rule.entity = entity
    if (profession) rule.profession = profession
    SunlitMarket.rule(rule)
  }
  let seenPools = {}
  let addPool = (faction, key, item, count, ratio, fallback, extra) => {
    let poolKey = faction + '|' + item
    if (seenPools[poolKey]) return
    seenPools[poolKey] = true
    let total = Math.max(1, Math.round(svValue(item, fallback) * count))
    if (total < 2) return
    let ask = Math.round(total * ratio)
    if (ask >= total) ask = total - 1
    let rule = {
      type: 'pool',
      id: 'sv.' + svSlug(faction) + '.' + key,
      faction: faction,
      item: item,
      count: count,
      baseValue: Math.max(1, Math.round(total * 0.60)),
      marketValue: total,
      askPrice: Math.max(1, ask),
      repGain: extra && extra.repGain !== undefined ? extra.repGain : 1
    }
    if (extra && extra.heat !== undefined) {
      rule.heat = extra.heat
      rule.wanted = extra.wanted || 0
    }
    SunlitMarket.rule(rule)
  }

  // ---- named NPCs: dialog name key -------------------------------------------
  // The pack names its NPCs with a dialog key (dialog.npc.<id>.name). Profession
  // display names are rewritten per locale and disagree between zh_cn and en_us
  // (weaponsmith is "Librarian" in en_us and the storage keeper in zh_cn), so the
  // key is the only stable identity.
  let addNamed = (key, faction) => SunlitMarket.rule({
    type: 'npc', id: 'sv.npc.' + key, faction: faction, rank: 'CIVILIAN', npcKey: key
  })
  addNamed('banker', 'society:banker')
  addNamed('blacksmith', 'society:blacksmith')
  addNamed('carpenter', 'society:carpenter')
  addNamed('fisher', 'society:fisher')
  addNamed('librarian', 'society:librarian')
  addNamed('market', 'society:market')
  addNamed('shepherd', 'society:shepherd')
  addNamed('trader', 'society:trader')

  // ---- ambient villagers: profession id, as the pack maps it ------------------
  // mason is the pack's mechanic, not the carpenter; fletcher is the exotic trader.
  addNpc('farmer', 'society:farmer', 'minecraft:villager', 'farmer')
  addNpc('fisher_villager', 'society:fisher', 'minecraft:villager', 'fisherman')
  addNpc('shepherd_villager', 'society:shepherd', 'minecraft:villager', 'shepherd')
  addNpc('blacksmith_villager', 'society:blacksmith', 'minecraft:villager', 'toolsmith')
  addNpc('butcher', 'society:butcher', 'minecraft:villager', 'butcher')
  addNpc('librarian_villager', 'society:librarian', 'minecraft:villager', 'librarian')
  addNpc('librarian_weaponsmith', 'society:librarian', 'minecraft:villager', 'weaponsmith')
  addNpc('banker_villager', 'society:banker', 'minecraft:villager', 'cartographer')
  addNpc('trader_fletcher', 'society:trader', 'minecraft:villager', 'fletcher')
  addNpc('trader_wandering', 'society:trader', 'minecraft:wandering_trader', '')
  addNpc('market_block', 'society:market', 'farmingforblockheads:merchant', '')

  // ---- farm produce ----------------------------------------------------------
  // Raw crops only: crates/bags/blocks are intentionally excluded from counter
  // requests so one order cannot move an entire warehouse.
  if (typeof global.crops !== 'undefined') {
    for (let i = 0; i < global.crops.length; i++) {
      let row = global.crops[i]
      if (!row || !row.item || row.value < 4 || row.value > 512) continue
      if (/_(crate|bag|block|sack|basket|barrel|box|tray)(_|$)/.test(row.item)) continue
      let count = row.value <= 16 ? 6 : row.value <= 64 ? 4 : 2
      addPool('society:farmer', 'crop_' + svSlug(row.item), row.item, count, 0.92, row.value)
    }
  }

  // FTBQ crop entries that are not in global.crops' normal price list.
  addPool('society:farmer', 'crop_etcetera_cotton_flower', 'etcetera:cotton_flower', 4, 0.92, 24)

  // ---- fish ------------------------------------------------------------------
  if (typeof global.fish !== 'undefined') {
    for (let i = 0; i < global.fish.length; i++) {
      let row = global.fish[i]
      if (!row || !row.item || row.value < 4) continue
      if (/_barrel(_|$)/.test(row.item)) continue
      addPool('society:fisher', 'fish_' + svSlug(row.item), row.item, 1, 0.92, row.value)
    }
  }

  // FTBQ jelly fish are not in global.fish but have Shipping values.
  addPool('society:fisher', 'fish_society_river_jelly', 'society:river_jelly', 1, 0.90, 128)
  addPool('society:fisher', 'fish_society_ocean_jelly', 'society:ocean_jelly', 1, 0.90, 256)
  addPool('society:fisher', 'fish_society_nether_jelly', 'society:nether_jelly', 1, 0.90, 512)

  // ---- logs / carpenter ------------------------------------------------------
  if (typeof global.logs !== 'undefined') {
    for (let i = 0; i < global.logs.length; i++) {
      let row = global.logs[i]
      if (!row || !row.item || row.value < 2 || row.value > 16) continue
      addPool('society:carpenter', 'log_' + svSlug(row.item), row.item, 16, 0.90, row.value)
    }
  }

  // ---- animal products -------------------------------------------------------
  addPool('society:shepherd', 'milk', 'society:milk', 4, 0.92, 16)
  addPool('society:shepherd', 'goat_milk', 'society:goat_milk', 2, 0.90, 96)
  addPool('society:shepherd', 'egg', 'minecraft:egg', 8, 0.92, 4)
  addPool('society:shepherd', 'wool', 'minecraft:white_wool', 8, 0.92, 8)
  addPool('society:shepherd', 'beef', 'minecraft:beef', 4, 0.92, 16)
  addPool('society:shepherd', 'pork', 'minecraft:porkchop', 4, 0.90, 32)
  addPool('society:shepherd', 'mutton', 'minecraft:mutton', 4, 0.92, 16)
  addPool('society:shepherd', 'ham', 'farmersdelight:ham', 2, 0.90, 64)
  addPool('society:shepherd', 'sheep_cheese', 'society:aged_sheep_cheese_block', 1, 0.90, 144)

  // ---- ores / blacksmith -----------------------------------------------------
  addPool('society:blacksmith', 'raw_iron', 'minecraft:raw_iron', 8, 0.90, 8)
  addPool('society:blacksmith', 'raw_copper', 'minecraft:raw_copper', 16, 0.90, 4)
  addPool('society:blacksmith', 'raw_gold', 'minecraft:raw_gold', 4, 0.88, 16)
  addPool('society:blacksmith', 'coal', 'minecraft:coal', 16, 0.90, 8)
  addPool('society:blacksmith', 'redstone', 'minecraft:redstone', 12, 0.90, 8)
  addPool('society:blacksmith', 'lapis', 'minecraft:lapis_lazuli', 8, 0.90, 6)
  addPool('society:blacksmith', 'zinc', 'create:raw_zinc', 8, 0.90, 8)
  addPool('society:blacksmith', 'lead', 'oreganized:raw_lead', 4, 0.90, 48)
  addPool('society:blacksmith', 'silver', 'oreganized:raw_silver', 2, 0.88, 64)
  addPool('society:blacksmith', 'iron_ingot', 'minecraft:iron_ingot', 4, 0.90, 32)
  addPool('society:blacksmith', 'gold_ingot', 'minecraft:gold_ingot', 2, 0.88, 64)

  // ---- market / prepared goods ----------------------------------------------
  addPool('society:market', 'mayonnaise', 'society:mayonnaise', 4, 0.92, 16)
  addPool('society:market', 'canvas', 'society:canvas', 2, 0.90, 80)
  addPool('society:market', 'oil', 'society:oil', 1, 0.90, 112)
  addPool('society:market', 'maple_syrup', 'society:maple_syrup', 1, 0.90, 192)
  addPool('society:market', 'cheese', 'society:aged_cheese_block', 1, 0.90, 288)
  addPool('society:market', 'battery', 'society:battery', 1, 0.90, 400)
  addPool('society:market', 'truffle_oil', 'society:truffle_oil', 1, 0.88, 1536)
  addPool('society:market', 'wine', 'vinery:white_grape', 4, 0.92, 20)
  addPool('society:market', 'cooked_meal', 'farmersdelight:roast_chicken_block', 1, 0.90, 160)


  // ---- FTBQ drinks -----------------------------------------------------------
  // Brewery / herbalbrews / wine values are already Shipping Bin values.
  // Cheap drinks stay with the market; rare bottles go to the travelling trader.
  let addDrinkList = (list, prefix) => {
    if (typeof list === 'undefined' || !list) return
    for (let i = 0; i < list.length; i++) {
      let row = list[i]
      if (!row || !row.item || row.value < 8) continue
      if (row.value <= 512) addPool('society:market', prefix + '_' + svSlug(row.item), row.item, 1, 0.90, row.value)
      else if (row.value <= 8192) addPool('society:trader', 'luxury_' + prefix + '_' + svSlug(row.item), row.item, 1, 0.82, row.value)
    }
  }
  addDrinkList(global.wines, 'wine')
  addDrinkList(global.brews, 'brew')
  addDrinkList(global.cocktails, 'cocktail')
  addDrinkList(global.herbalBrews, 'tea')

  // ---- FTBQ minerals / geodes / artefacts -----------------------------------
  let addValueList = (list, faction, prefix, min, max, ratio, extra) => {
    if (typeof list === 'undefined' || !list) return
    for (let i = 0; i < list.length; i++) {
      let row = list[i]
      if (!row || !row.item || row.value < min || row.value > max) continue
      let count = row.value <= 12 ? 8 : row.value <= 64 ? 4 : 1
      addPool(faction, prefix + '_' + svSlug(row.item), row.item, count, ratio, row.value, extra)
    }
  }
  addValueList(global.ore, 'society:blacksmith', 'ore', 4, 2560, 0.88)
  addValueList(global.gems, 'society:trader', 'gem', 64, 2048, 0.80)
  addValueList(global.geodeList, 'society:trader', 'geode', 32, 1024, 0.78)
  addValueList(global.frozenGeodeList, 'society:trader', 'frozen_geode', 32, 1024, 0.78)
  addValueList(global.magmaGeodeList, 'society:trader', 'magma_geode', 32, 1024, 0.78)
  addValueList(global.miscGeologist, 'society:trader', 'curio', 16, 4096, 0.78)
  addPool('society:blacksmith', 'mineral_limestone_pebble', 'society:limestone_pebble', 8, 0.90, 15)
  addPool('society:blacksmith', 'mineral_mudstone', 'society:mudstone', 8, 0.90, 24)
  addPool('society:trader', 'gem_prismarine_crystals', 'minecraft:prismarine_crystals', 4, 0.90, 20)
  addValueList(global.artifacts, 'society:trader', 'artifact', 64, 4096, 0.78, { repGain: 2 })
  addValueList(global.relics, 'society:trader', 'relic', 64, 4096, 0.78, { repGain: 2 })

  // ---- librarian -------------------------------------------------------------
  addPool('society:librarian', 'paper', 'minecraft:paper', 16, 0.92, 4)
  addPool('society:librarian', 'book', 'minecraft:book', 4, 0.90, 16)
  addPool('society:librarian', 'bookshelf', 'minecraft:bookshelf', 2, 0.90, 48)
  addPool('society:librarian', 'name_tag', 'minecraft:name_tag', 1, 0.88, 64)
  addPool('society:librarian', 'star_book', 'society:book_of_stars', 1, 0.78, 2048)

  // ---- rare trader / magic ---------------------------------------------------
  addPool('society:trader', 'sparkstone', 'society:sparkstone', 4, 0.88, 16)
  addPool('society:trader', 'amethyst', 'minecraft:amethyst_shard', 8, 0.90, 8)
  addPool('society:trader', 'aquamarine', 'society:aquamarine', 2, 0.78, 184)
  addPool('society:trader', 'ruby', 'society:ruby', 1, 0.76, 256)
  addPool('society:trader', 'jade', 'society:jade', 1, 0.74, 512)
  addPool('society:trader', 'spinel', 'society:spinel', 1, 0.72, 1024)
  addPool('society:trader', 'prismatic', 'society:prismatic_shard', 1, 0.72, 2048)
  // Explicit stolen stock: buying it is cheap, but it carries provenance/heat.
  addPool('society:trader', 'stolen_diamond', 'minecraft:diamond', 1, 0.55, 256, { repGain: 0, heat: 35, wanted: 12 })

  console.info('[SV-INTEGRATION] Sunlit customer pools registered')
}
