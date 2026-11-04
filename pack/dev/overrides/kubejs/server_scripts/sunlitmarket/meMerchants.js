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
if (typeof SunlitMarket !== 'undefined' && Platform.isLoaded('me')) {
  SunlitMarket.clear()
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
    offers: [
      { item: 'me:leek', count: 1, buy: 14, sell: 8, stock: 16 },
      { item: 'me:cucumber', count: 1, buy: 16, sell: 10 },
      { item: 'me:lettuce', count: 1, buy: 14, sell: 8 },
      { item: 'me:tomato', count: 1, buy: 16, sell: 10, stock: 16 },
      { item: 'me:strawberry', count: 1, buy: 18, sell: 12 },
      { item: 'me:white_mushroom', count: 1, buy: 12, sell: 7 },
      { item: 'me:vegetable_soup', count: 1, buy: 80, sell: 55 }
    ]
  })

  SunlitMarket.merchant({
    id: 'me_gondor_quartermaster',
    name: '刚铎军需官',
    faction: 'me:gondor',
    tag: 'sunlitmarket.me.gondor_quartermaster',
    offers: [
      { item: 'minecraft:bread', count: 1, buy: 8, sell: 4 },
      { item: 'me:meat_bowl', count: 1, buy: 96, sell: 72, reputation: 5 },
      { item: 'me:cooked_meat_skewer', count: 1, buy: 55, sell: 42 },
      { item: 'me:meat_egg_meal', count: 1, buy: 90, sell: 70 }
    ]
  })

  SunlitMarket.merchant({
    id: 'me_rohan_hunter',
    name: '洛汗猎手',
    faction: 'me:rohan',
    tag: 'sunlitmarket.me.rohan_hunter',
    offers: [
      { item: 'me:cooked_goose', count: 1, buy: 40, sell: 28 },
      { item: 'me:cooked_duck', count: 1, buy: 40, sell: 28 },
      { item: 'me:cooked_swan', count: 1, buy: 44, sell: 30 },
      { item: 'me:cooked_rat', count: 1, buy: 16, sell: 10 },
      { item: 'me:sack_of_horsefeed', count: 1, buy: 30, sell: 18 }
    ]
  })

  SunlitMarket.merchant({
    id: 'me_lothlorien_herbalist',
    name: '萝林草药师',
    faction: 'me:lothlorien',
    tag: 'sunlitmarket.me.lothlorien_herbalist',
    offers: [
      { item: 'me:strawberries', count: 1, buy: 22, sell: 15 },
      { item: 'me:ghostshroom', count: 1, buy: 20, sell: 12 },
      { item: 'me:yellow_amanita', count: 1, buy: 20, sell: 12 },
      { item: 'me:trumpet_shroom', count: 1, buy: 18, sell: 11 },
      { item: 'me:pipeweed', count: 1, buy: 32, sell: 22, reputation: 5 }
    ]
  })

  SunlitMarket.merchant({
    id: 'me_erebor_smith',
    name: '孤山矿商',
    faction: 'me:longbeards',
    tag: 'sunlitmarket.me.erebor_smith',
    offers: [
      { item: 'me:flax', count: 1, buy: 24, sell: 16 },
      { item: 'minecraft:string', count: 1, buy: 8, sell: 4 },
      { item: 'me:copper_coin', count: 1, buy: 2, sell: 1 },
      { item: 'me:silver_coin', count: 1, buy: 16, sell: 8 },
      { item: 'me:gold_coin', count: 1, buy: 128, sell: 64, reputation: 10 }
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
