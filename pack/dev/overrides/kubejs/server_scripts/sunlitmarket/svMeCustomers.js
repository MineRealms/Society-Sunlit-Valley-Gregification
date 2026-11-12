// priority: 9
// ============================================================
// Middle-earth faction customers for the pawn counter.
// Native NpcData.Type already supplies faction + rank; this file only adds
// faction-specific request pools. Prices use Shipping Bin values as the floor.
// Tagged shopkeepers are overridden to MERCHANT by the priority-0 merchant
// scripts; untagged civilians keep these customer identities.
// ============================================================
if (typeof SunlitMarket !== 'undefined' && typeof global !== 'undefined' && global.trades && Platform.isLoaded('me')) {
  let valueOf = (id, fallback) => {
    let row = global.trades.get(id)
    return row && row.value > 0 ? row.value : fallback
  }
  let slug = (id) => String(id).replace(/[^a-z0-9_]+/g, '_')
  let addPool = (faction, key, item, count, ratio, fallback, extra) => {
    let total = Math.max(1, Math.round(valueOf(item, fallback) * count))
    let rule = {
      type: 'pool',
      id: 'sv.me.' + slug(faction) + '.' + key,
      faction: faction,
      item: item,
      count: count,
      baseValue: Math.max(1, Math.round(total * 0.60)),
      marketValue: total,
      askPrice: Math.max(1, Math.round(total * ratio)),
      repGain: extra && extra.repGain !== undefined ? extra.repGain : 1
    }
    if (extra && extra.heat !== undefined) {
      rule.heat = extra.heat
      rule.wanted = extra.wanted || 0
    }
    SunlitMarket.rule(rule)
  }
  let addNpc = (key, faction, type) => {
    SunlitMarket.rule({ type: 'npc', id: 'sv.me.npc.' + key, faction: faction, npcType: type, rank: 'CIVILIAN' })
  }
  let addMany = (faction, rows) => {
    for (let i = 0; i < rows.length; i++) {
      let row = rows[i]
      addPool(faction, row[0], row[1], row[2], row[3], row[4], row[5])
    }
  }

  // Explicit, non-conflicting CIVILIAN types make the customer rule independent
  // of a future faction-table rank change. The shipped ME jar is authoritative:
  // rohan.militia, brigand.thug, wild_goblins.gatherer and woodland_realm.ranger
  // also occur in combat pools, so they are deliberately NOT forced into CIVILIAN.
  addNpc('shire_peasant', 'me:shire', 'me:shire.peasant')
  addNpc('gondor_peasant', 'me:gondor', 'me:gondor.peasant')
  addNpc('dale_peasant', 'me:dale', 'me:dale.peasant')
  addNpc('lothlorien_sentinel', 'me:lothlorien', 'me:lothlorien.sentinel')
  addNpc('erebor_peasant', 'me:longbeards.erebor', 'me:longbeards.erebor.peasant')
  addNpc('erebor_miner', 'me:longbeards.erebor', 'me:longbeards.erebor.miner')
  addNpc('goblin_town_goblin', 'me:goblin_town', 'me:goblin_town.goblin')
  addNpc('gundabad_goblin', 'me:hobgoblin_tribes.gundabad', 'me:hobgoblin_tribes.gundabad.goblin')
  addNpc('isengard_snaga', 'me:isengard', 'me:isengard.snaga')
  addNpc('mordor_snaga', 'me:mordor', 'me:mordor.snaga')
  addNpc('moria_goblin', 'me:moria', 'me:moria.goblin')

  // Shire: garden produce and simple cooked food.
  addMany('me:shire', [
    ['leek', 'me:leek', 4, 0.92, 10],
    ['cucumber', 'me:cucumber', 4, 0.92, 12],
    ['lettuce', 'me:lettuce', 4, 0.92, 10],
    ['tomato', 'me:tomato', 4, 0.92, 12],
    ['strawberry', 'me:strawberry', 4, 0.92, 12],
    ['mushroom', 'me:white_mushroom', 6, 0.92, 8],
    ['soup', 'me:vegetable_soup', 1, 0.92, 55],
    ['bell_pepper', 'me:bell_pepper', 4, 0.92, 14],
    ['garlic', 'me:garlic', 4, 0.92, 14],
    ['onion', 'me:onion', 4, 0.92, 10]
  ])

  // Gondor: field rations and metal for the quartermaster.
  addMany('me:gondor', [
    ['bread', 'minecraft:bread', 2, 0.92, 16],
    ['meat_bowl', 'me:meat_bowl', 1, 0.92, 72],
    ['meat_skewer', 'me:cooked_meat_skewer', 2, 0.92, 42],
    ['egg_meal', 'me:meat_egg_meal', 1, 0.92, 70],
    ['iron', 'minecraft:iron_ingot', 4, 0.90, 32],
    ['berry_pie', 'me:berry_pie', 1, 0.90, 48]
  ])

  // Rohan: hunt, fowl and horse feed.
  addMany('me:rohan', [
    ['goose', 'me:cooked_goose', 1, 0.92, 40],
    ['duck', 'me:cooked_duck', 1, 0.92, 40],
    ['swan', 'me:cooked_swan', 1, 0.90, 44],
    ['rat', 'me:cooked_rat', 2, 0.92, 16],
    ['horsefeed', 'me:sack_of_horsefeed', 1, 0.92, 30],
    ['beef', 'minecraft:beef', 4, 0.92, 16],
    ['fish_stew', 'me:fish_stew', 1, 0.90, 65]
  ])

  // Lothlorien: herbs, mushrooms and pipeweed.
  addMany('me:lothlorien', [
    ['strawberries', 'me:strawberries', 4, 0.92, 22],
    ['ghostshroom', 'me:ghostshroom', 2, 0.90, 20],
    ['amanita', 'me:yellow_amanita', 2, 0.90, 20],
    ['trumpet', 'me:trumpet_shroom', 2, 0.85, 18],
    ['pipeweed', 'me:pipeweed', 1, 0.90, 32]
  ])

  // Erebor: ore and smithing stock.
  addMany('me:longbeards.erebor', [
    ['flax', 'me:flax', 4, 0.92, 16],
    ['iron', 'minecraft:raw_iron', 8, 0.90, 8],
    ['coal', 'minecraft:coal', 16, 0.92, 8],
    ['lead', 'oreganized:raw_lead', 4, 0.90, 48],
    ['silver', 'oreganized:raw_silver', 2, 0.90, 64]
  ])

  // Dale: trade goods and prepared food.
  addMany('me:dale', [
    ['bread', 'minecraft:bread', 2, 0.92, 16],
    ['string', 'minecraft:string', 8, 0.92, 4],
    ['cabbage', 'farmersdelight:cabbage', 2, 0.92, 70],
    ['berry', 'society:blueberry', 4, 0.92, 24]
  ])

  // Hostile / outlaw factions: cheap stolen stock with real consequences.
  addMany('me:brigand', [
    ['stolen_diamond', 'minecraft:diamond', 1, 0.55, 256, { repGain: 0, heat: 35, wanted: 12 }],
    ['stolen_gold', 'minecraft:gold_ingot', 2, 0.58, 64, { repGain: 0, heat: 20, wanted: 7 }],
    ['stolen_scrap', 'minecraft:netherite_scrap', 1, 0.52, 1024, { repGain: 0, heat: 60, wanted: 20 }]
  ])
  addMany('me:isengard', [
    ['stolen_iron', 'minecraft:iron_ingot', 8, 0.55, 32, { repGain: 0, heat: 25, wanted: 9 }],
    ['stolen_gold', 'minecraft:gold_ingot', 2, 0.55, 64, { repGain: 0, heat: 20, wanted: 7 }],
    ['gunpowder', 'minecraft:gunpowder', 8, 0.60, 8, { repGain: 0, heat: 15, wanted: 5 }]
  ])
  addMany('me:mordor', [
    ['stolen_scrap', 'minecraft:netherite_scrap', 1, 0.50, 1024, { repGain: 0, heat: 60, wanted: 20 }],
    ['stolen_diamond', 'minecraft:diamond', 1, 0.52, 256, { repGain: 0, heat: 35, wanted: 12 }],
    ['gunpowder', 'minecraft:gunpowder', 16, 0.58, 8, { repGain: 0, heat: 15, wanted: 5 }]
  ])
  addMany('me:moria', [
    ['iron', 'minecraft:raw_iron', 8, 0.90, 8],
    ['gold', 'minecraft:raw_gold', 4, 0.90, 16],
    ['redstone', 'minecraft:redstone', 12, 0.92, 8]
  ])
  addMany('me:goblin_town', [
    ['stolen_gold', 'minecraft:gold_ingot', 2, 0.55, 64, { repGain: 0, heat: 20, wanted: 7 }],
    ['coal', 'minecraft:coal', 16, 0.92, 8],
    ['iron', 'minecraft:raw_iron', 8, 0.92, 8]
  ])
  addMany('me:hobgoblin_tribes.gundabad', [
    ['stolen_iron', 'minecraft:iron_ingot', 8, 0.58, 32, { repGain: 0, heat: 25, wanted: 9 }],
    ['coal', 'minecraft:coal', 16, 0.92, 8]
  ])
  addMany('me:wild_goblins', [
    ['stolen_gold', 'minecraft:gold_ingot', 2, 0.56, 64, { repGain: 0, heat: 20, wanted: 7 }],
    ['coal', 'minecraft:coal', 12, 0.92, 8]
  ])

  console.info('[SV-INTEGRATION] Middle-earth customer pools registered')
}
