// priority: 0
// ============================================================
// Seasonal price texture for Middle-earth merchants.
//
// Uses the pack's existing SereneSeasons global helper and SunlitMarket's
// runtime price multipliers. Reputation discount/bonus is applied by the mod
// on top of these multipliers.
// ============================================================
if (typeof SunlitMarket !== 'undefined' && Platform.isLoaded('me') && Platform.isLoaded('sereneseasons')) {
  const PRODUCE = [
    ['me_shire_farmer', ['me:leek', 'me:cucumber', 'me:lettuce', 'me:tomato', 'me:strawberry', 'me:white_mushroom']],
    ['me_lothlorien_herbalist', ['me:strawberries', 'me:ghostshroom', 'me:yellow_amanita', 'me:trumpet_shroom', 'me:pipeweed']],
  ]

  const setPrices = (season) => {
    SunlitMarket.clearPriceMultipliers()
    const multiplier = season === 'winter' ? 1.25 : (season === 'autumn' ? 0.95 : 1.0)
    PRODUCE.forEach(([merchant, items]) => {
      items.forEach((item) => SunlitMarket.priceMultiplier(merchant, item, multiplier))
    })
    // Mushrooms keep a smaller seasonal swing; they are forage, not field crops.
    for (const item of ['me:white_mushroom', 'me:ghostshroom', 'me:yellow_amanita', 'me:trumpet_shroom']) {
      SunlitMarket.priceMultiplier('me_shire_farmer', item, season === 'winter' ? 1.1 : 1.0)
      SunlitMarket.priceMultiplier('me_lothlorien_herbalist', item, season === 'winter' ? 1.1 : 1.0)
    }
    console.info('[SunlitMarket] seasonal multipliers applied: ' + season)
  }

  let lastSeason = ''
  ServerEvents.tick((event) => {
    if (event.server.getTickCount() % 200 !== 0) return
    const season = global.getSeasonFromLevel(event.server.overworld())
    if (season === lastSeason) return
    lastSeason = season
    setPrices(season)
  })
}
