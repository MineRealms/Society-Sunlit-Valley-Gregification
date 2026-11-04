// priority: 7
// ============================================================
// Market-maker price indices for the pawnshop trading hall.
//
// Members bind to merchant shelves by (merchantId, item). An index only moves when a
// member actually trades: it is the geometric mean of each member's last traded
// (price modifier x shelf scarcity) ratio, starting at 1000. Prices here are feed stock
// into those shelves - see meMerchants.js. /sunlitmarket index prints the live values.
// Futures are opt-in per index (docs/ECONOMY_ACCOUNTS.md), e.g.:
//   SunlitMarket.futures({ index: 'sv.metal', tenorDays: 7, band: 0.2, maxLots: 20, minTraders: 2 })
// ============================================================
if (typeof SunlitMarket !== 'undefined' && Platform.isLoaded('me')) {
  SunlitMarket.index('sv.produce', '谷蔬指', [
    ['me_shire_farmer', 'me:leek'],
    ['me_shire_farmer', 'me:cucumber'],
    ['me_shire_farmer', 'me:lettuce'],
    ['me_shire_farmer', 'me:tomato'],
    ['me_shire_farmer', 'me:strawberry'],
    ['me_shire_farmer', 'me:white_mushroom'],
    ['me_shire_farmer', 'me:vegetable_soup']
  ])
  SunlitMarket.index('sv.metal', '金属指', [
    ['me_erebor_smith', 'minecraft:raw_iron'],
    ['me_erebor_smith', 'minecraft:coal'],
    ['me_erebor_smith', 'minecraft:iron_ingot'],
    ['me_erebor_smith', 'oreganized:raw_lead'],
    ['me_erebor_smith', 'oreganized:raw_silver']
  ])
  SunlitMarket.index('sv.delicacy', '料理指', [
    ['me_gondor_quartermaster', 'me:meat_bowl'],
    ['me_gondor_quartermaster', 'me:cooked_meat_skewer'],
    ['me_gondor_quartermaster', 'me:meat_egg_meal'],
    ['me_shire_farmer', 'me:vegetable_soup']
  ])
  console.info('[SV-INTEGRATION] price indices registered')
}
