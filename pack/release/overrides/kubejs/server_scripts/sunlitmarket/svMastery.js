// priority: 8
// ============================================================
// Bridge the pack's FTBQ/game stages to SunlitMarket unlock ids.
// Quest stages remain the source of truth; SunlitMarket.unlock only mirrors
// them into its per-player SavedData so offer.unlock can use stable ids.
// ============================================================
if (typeof SunlitMarket !== 'undefined' && typeof global !== 'undefined' && !global.SV_MASTERY_INSTALLED) {
  global.SV_MASTERY_INSTALLED = true
  let STAGES = [
    ['mastery_unlocked', 'sv.mastery'],
    ['farming_mastery', 'sv.farming.master'],
    ['fishing_mastery', 'sv.fishing.master'],
    ['husbandry_mastery', 'sv.husbandry.master'],
    ['mining_mastery', 'sv.mining.master'],
    ['adventuring_mastery', 'sv.adventure.master'],
    ['invited_market', 'sv.shop.market'],
    ['invited_blacksmith', 'sv.shop.blacksmith'],
    ['invited_fisher', 'sv.shop.fisher'],
    ['invited_shepherd', 'sv.shop.shepherd'],
    ['invited_librarian', 'sv.shop.librarian'],
    ['invited_trader', 'sv.shop.trader'],
    ['invited_witch', 'sv.shop.witch'],
    ['invited_banker', 'sv.shop.banker']
  ]
  let sync = (player) => {
    for (let i = 0; i < STAGES.length; i++) {
      let stage = STAGES[i]
      if (player.stages.has(stage[0]) && !SunlitMarket.isUnlocked(player, stage[1])) {
        SunlitMarket.unlock(player, stage[1])
      }
    }
  }
  PlayerEvents.loggedIn((event) => sync(event.player))
  PlayerEvents.tick((event) => {
    if (event.player.age % 100 !== 0) return
    sync(event.player)
  })
  console.info('[SV-INTEGRATION] mastery stage bridge installed')
}
