// priority: 20
// ============================================================
// Acceptance bin boundary.
//
// The bin must never outbid the Shipping Bin. Everything the pack already
// prices in global.trades is refused outright (-1), so the bin stays a sink
// for the streams the Shipping Bin does not handle: fluids, FE, essentia,
// mana, and items the pack never priced.
//
// Without this the bin fell back to the pawnshop buyback price, and the
// Sunlit produce buyback is 1.02x the shipping value - a free 2% over the
// pack's own money channel, paid instantly and without touching debt.
// ============================================================
if (typeof SunlitMarket !== 'undefined' && SunlitMarket.depositBlock
    && typeof global !== 'undefined' && global.trades) {
  let blocked = 0
  Array.from(global.trades.keys()).forEach((id) => {
    let row = global.trades.get(id)
    if (id && row && row.value > 0) {
      SunlitMarket.depositBlock(id)
      blocked++
    }
  })
  console.info('[SM-INTEGRATION] acceptance bin refuses ' + blocked + ' shipping-bin items')
} else {
  console.info('[SM-INTEGRATION] acceptance bin boundary skipped: depositBlock='
    + (typeof SunlitMarket === 'undefined' ? 'no-binding' : typeof SunlitMarket.depositBlock)
    + ' trades=' + (typeof global === 'undefined' || !global.trades ? 'missing' : 'ok'))
}
