// priority: 0
// ============================================================
// Seasonal price curve for Middle-earth produce merchants.
//
// Reads the real SereneSeasons season (no pack-specific global helper) and
// drives SunlitMarket's runtime price multipliers. Reputation discount/bonus
// is applied by the mod on top of these multipliers.
//
// Each item has a factor per season; the value is interpolated across the
// season boundary with a smoothstep so prices glide instead of snapping.
//
// NOTE: KubeJS/Rhino rejects array destructuring in arrow parameters, so this
// file uses plain index access everywhere.
// ============================================================
// KubeJS evaluates server scripts more than once per boot, and it hoists every
// top-level "const" into the shared script scope, so the second evaluation dies
// with "redeclaration of var X". Use "let" (not hoisted) and keep the global
// guard so tick handlers are only registered once.
if (typeof SunlitMarket !== 'undefined' && Platform.isLoaded('sereneseasons') && !global.SM_SEASON_INSTALLED) {
  global.SM_SEASON_INSTALLED = true
  {
    // KubeJS also declares a var named after the class, so do not reuse the simple name.
  let SM_SEASON_API = Java.loadClass('sereneseasons.api.season.SeasonHelper')
    let ORDER = ['spring', 'summer', 'autumn', 'winter']

    // [merchant, item, spring, summer, autumn, winter]
    let TABLE = [
      // Shire farmer: field crops peak in summer/autumn, scarce in winter.
      ['me_shire_farmer', 'me:leek', 0.90, 0.95, 1.10, 1.40],
      ['me_shire_farmer', 'me:cucumber', 1.00, 0.90, 1.05, 1.35],
      ['me_shire_farmer', 'me:lettuce', 0.90, 1.00, 1.05, 1.30],
      ['me_shire_farmer', 'me:tomato', 1.05, 0.90, 1.05, 1.35],
      ['me_shire_farmer', 'me:strawberry', 0.85, 1.00, 1.10, 1.45],
      // Forage: mushrooms are cheapest in autumn, available all year.
      ['me_shire_farmer', 'me:white_mushroom', 1.00, 1.05, 0.90, 1.10],
      // Hearty stews cost more when ingredients are scarce.
      ['me_shire_farmer', 'me:vegetable_soup', 0.95, 0.95, 1.00, 1.20],
      // Lothlorien herbalist: spring foraging, winter scarcity.
      ['me_lothlorien_herbalist', 'me:strawberries', 0.85, 1.00, 1.10, 1.40],
      ['me_lothlorien_herbalist', 'me:ghostshroom', 1.00, 1.05, 0.90, 1.15],
      ['me_lothlorien_herbalist', 'me:yellow_amanita', 1.00, 1.05, 0.90, 1.15],
      ['me_lothlorien_herbalist', 'me:trumpet_shroom', 1.00, 1.05, 0.90, 1.15],
      ['me_lothlorien_herbalist', 'me:pipeweed', 0.95, 0.90, 1.00, 1.25],
    ]

    let smoothstep = (t) => t * t * (3 - 2 * t)

    let multipliers = (season, progress) => {
      let index = Math.max(0, ORDER.indexOf(season))
      let next = (index + 1) % ORDER.length
      let blend = smoothstep(Math.min(1, Math.max(0, progress)))
      let result = []
      for (let i = 0; i < TABLE.length; i++) {
        let row = TABLE[i]
        let current = row[2 + index]
        let following = row[2 + next]
        let value = current + (following - current) * blend
        result.push([row[0], row[1], Math.round(value * 100) / 100])
      }
      return result
    }

    let apply = (server) => {
      let season = 'spring'
      let progress = 0
      try {
        let state = SM_SEASON_API.getSeasonState(server.overworld())
        season = String(state.getSeason()).toLowerCase()
        let duration = state.getSeasonDuration()
        if (duration > 0) progress = (state.getSeasonCycleTicks() % duration) / duration
      } catch (error) {
        console.warn('[SunlitMarket] season lookup failed: ' + error)
        return null
      }
      let values = multipliers(season, progress)
      let sample = ''
      for (let i = 0; i < values.length; i++) {
        let entry = values[i]
        SunlitMarket.priceMultiplier(entry[0], entry[1], entry[2])
        if (entry[1] === 'me:leek' || entry[1] === 'me:white_mushroom') {
          sample = sample + entry[1].replace('me:', '') + '=' + entry[2] + ' '
        }
      }
      let key = season + '@' + Math.round(progress * 100) + '% ' + sample
    global.SM_LAST_SEASON = key
    return key
    }

    let lastKey = ''
    ServerEvents.tick((event) => {
      if (event.server.getTickCount() % 200 !== 0) return
      let key = apply(event.server)
      if (key && key !== lastKey) {
        lastKey = key
        console.info('[SunlitMarket] seasonal multipliers applied: ' + key)
      }
    })

    // Reapply immediately after /reload so an open shop keeps the right prices.
    ServerEvents.loaded((event) => {
      let key = apply(event.server)
      if (key) console.info('[SunlitMarket] seasonal multipliers (load): ' + key)
    })
  }

}
