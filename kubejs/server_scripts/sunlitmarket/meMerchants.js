// priority: 0
// ============================================================
// SunlitMarket merchants for Middle-earth.
//
// Requires the optional SunlitMarket mod. If it is missing, this script is
// skipped and the pack keeps working unchanged.
//
// Natural Middle-earth NPCs are matched by their NpcData.Type in config JSON;
// for player-placed merchants use entity tags:
//   /summon me:npc ~ ~ ~ {Tags:["sunlitmarket.me.shire_farmer"],InitializationData:{Type:"me:shire.peasant"}}
//
// All prices are in "spur" (Numismatics base value). `buy` is what the player
// pays; `sell` is what the player receives. Values are intentionally modest;
// adjust per economy pass.
// ============================================================
// Script merchants are rebuilt from scratch on every /reload. clear() lives
// outside the ME gate so the themed merchants are not duplicated when ME is
// missing (this file sorts before themedMerchants.js).
if (typeof SunlitMarket !== 'undefined') {
  SunlitMarket.clear()
}

if (typeof SunlitMarket !== 'undefined' && Platform.isLoaded('me')) {
  // The Shipping Bin table is the pack-wide price anchor. These sell-only
  // offers pay 102% of that value, so a counter purchase has a small but
  // real margin without creating a buy-low/sell-high loop.
  let svValue = (id, fallback) => {
    let row = typeof global !== 'undefined' && global.trades ? global.trades.get(id) : null
    return row && row.value > 0 ? row.value : fallback
  }
  let svSell = (id, fallback) => Math.max(1, Math.ceil(svValue(id, fallback) * 1.02))

  // Exchange values for Middle-earth coin items. Override or remove if the
  // pack later unifies coins through a dedicated bank.
  SunlitMarket.coinValue('me:copper_coin', 1)
  SunlitMarket.coinValue('me:silver_coin', 8)
  SunlitMarket.coinValue('me:gold_coin', 64)

  SunlitMarket.merchant({
    id: 'me_shire_farmer',
    name: '夏尔农户',
    faction: 'me:shire',
    tag: 'sunlitmarket.me.shire_farmer',
    npcType: 'me:shire.peasant',
    offers: [
      { item: 'me:leek', count: 1, buy: 14, sell: 8, stock: 16 },
      { item: 'me:cucumber', count: 1, buy: 16, sell: 10, stock: 24 },
      { item: 'me:lettuce', count: 1, buy: 14, sell: 8, stock: 24 },
      { item: 'me:tomato', count: 1, buy: 16, sell: 10, stock: 16 },
      { item: 'me:strawberry', count: 1, buy: 18, sell: 12 },
      { item: 'me:white_mushroom', count: 1, buy: 12, sell: 7, stock: 24 },
      { item: 'me:vegetable_soup', count: 1, buy: 80, sell: 55, stock: 8 },
      { item: 'society:blueberry', count: 1, sell: svSell('society:blueberry', 24) },
      { item: 'society:cranberry', count: 1, sell: svSell('society:cranberry', 18) },
      { item: 'farmersdelight:tomato', count: 1, sell: svSell('farmersdelight:tomato', 24) },
      { item: 'farmersdelight:cabbage', count: 1, sell: svSell('farmersdelight:cabbage', 70) }
    ]
  })

  SunlitMarket.merchant({
    id: 'me_gondor_quartermaster',
    name: '刚铎军需官',
    faction: 'me:gondor',
    tag: 'sunlitmarket.me.gondor_quartermaster',
    npcType: 'me:gondor.peasant',
    offers: [
      // Shipping Bin value is 16; buying at 8 used to allow risk-free resale.
      { item: 'minecraft:bread', count: 1, buy: 22, sell: 14 },
      { item: 'society:aged_cheese_block', count: 1, sell: svSell('society:aged_cheese_block', 288) },
      { item: 'society:oil', count: 1, sell: svSell('society:oil', 112) },
      { item: 'society:maple_syrup', count: 1, sell: svSell('society:maple_syrup', 192) },
      { item: 'society:truffle_oil', count: 1, buy: Math.round(svValue('society:truffle_oil', 1536) * 1.24), sell: Math.round(svValue('society:truffle_oil', 1536) * 0.78), stock: 2, unlock: 'sv.farming.master', repGain: 2 },
      { item: 'me:meat_bowl', count: 1, buy: 96, sell: 72, reputation: 5, stock: 8 },
      { item: 'me:cooked_meat_skewer', count: 1, buy: 55, sell: 42, stock: 12 },
      { item: 'me:meat_egg_meal', count: 1, buy: 90, sell: 70, stock: 8 }
    ]
  })

  SunlitMarket.merchant({
    id: 'me_rohan_hunter',
    name: '洛汗猎手',
    faction: 'me:rohan',
    tag: 'sunlitmarket.me.rohan_hunter',
    // No unambiguous civilian type in this shipped ME build. Require the explicit
    // merchant tag; matching all rohan.militia would also make soldiers immune to AI targets.
    npcType: '',
    offers: [
      { item: 'me:cooked_goose', count: 1, buy: 40, sell: 28 },
      { item: 'me:cooked_duck', count: 1, buy: 40, sell: 28 },
      { item: 'me:cooked_swan', count: 1, buy: 44, sell: 30 },
      { item: 'me:cooked_rat', count: 1, buy: 16, sell: 10 },
      { item: 'me:sack_of_horsefeed', count: 1, buy: 30, sell: 18 },
      { item: 'minecraft:beef', count: 1, sell: svSell('minecraft:beef', 16) },
      { item: 'minecraft:porkchop', count: 1, sell: svSell('minecraft:porkchop', 32) },
      { item: 'farmersdelight:ham', count: 1, sell: svSell('farmersdelight:ham', 64) }
    ]
  })

  SunlitMarket.merchant({
    id: 'me_lothlorien_herbalist',
    name: '萝林草药师',
    faction: 'me:lothlorien',
    tag: 'sunlitmarket.me.lothlorien_herbalist',
    npcType: 'me:lothlorien.sentinel',
    offers: [
      { item: 'me:strawberries', count: 1, buy: 22, sell: 15, stock: 16 },
      { item: 'me:ghostshroom', count: 1, buy: 20, sell: 12, stock: 12 },
      { item: 'me:yellow_amanita', count: 1, buy: 20, sell: 12, stock: 12 },
      { item: 'me:trumpet_shroom', count: 1, buy: 18, sell: 11, stock: 12 },
      { item: 'me:pipeweed', count: 1, buy: 32, sell: 22, reputation: 5, stock: 8 },
      { item: 'society:crystalberry', count: 1, sell: svSell('society:crystalberry', 22) },
      { item: 'society:mana_fruit', count: 1, buy: Math.round(svValue('society:mana_fruit', 256) * 1.25), sell: Math.round(svValue('society:mana_fruit', 256) * 0.78), stock: 2, unlock: 'sv.farming.master', repGain: 2 }
    ]
  })

  SunlitMarket.merchant({
    id: 'me_erebor_smith',
    name: '孤山矿商',
    faction: 'me:longbeards',
    tag: 'sunlitmarket.me.erebor_smith',
    npcType: 'me:longbeards.erebor.miner',
    offers: [
      { item: 'me:flax', count: 1, buy: 24, sell: 16, stock: 16 },
      { item: 'minecraft:string', count: 1, buy: 8, sell: 4, stock: 32 },
      // Ore restock shelf: buy prices sit just above the Shipping Bin anchor so the
      // metal index has real, finite supply that player trading can move.
      { item: 'minecraft:raw_iron', count: 1, buy: 10, sell: 8, stock: 32 },
      { item: 'minecraft:coal', count: 1, buy: 10, sell: 8, stock: 48 },
      { item: 'minecraft:iron_ingot', count: 1, buy: 35, sell: 30, stock: 16 },
      { item: 'oreganized:raw_lead', count: 1, buy: 53, sell: 48, stock: 12 },
      { item: 'oreganized:raw_silver', count: 1, buy: 70, sell: 64, stock: 8 },
      { item: 'me:copper_coin', count: 1, buy: 2, sell: 1 },
      { item: 'me:silver_coin', count: 1, buy: 16, sell: 8 },
      { item: 'me:gold_coin', count: 1, buy: 128, sell: 64, reputation: 10 },
      { item: 'minecraft:raw_iron', count: 1, sell: svSell('minecraft:raw_iron', 8) },
      { item: 'minecraft:coal', count: 1, sell: svSell('minecraft:coal', 8) },
      { item: 'oreganized:raw_lead', count: 1, sell: svSell('oreganized:raw_lead', 48) },
      { item: 'society:prismatic_shard', count: 1, buy: Math.round(svValue('society:prismatic_shard', 2048) * 1.27), sell: Math.round(svValue('society:prismatic_shard', 2048) * 0.78), stock: 1, unlock: 'sv.mining.master', repGain: 2 }
    ]
  })

  SunlitMarket.merchant({
    id: 'me_moneychanger',
    name: '中州钱庄',
    faction: 'me:neutral',
    tag: 'sunlitmarket.me.moneychanger',
    offers: [
      { item: 'me:copper_coin', count: 1, buy: 1, sell: 1 },
      { item: 'me:silver_coin', count: 1, buy: 8, sell: 8 },
      { item: 'me:gold_coin', count: 1, buy: 64, sell: 64 }
    ]
  })

  console.info('[SunlitMarket] Middle-earth merchants registered')
}
