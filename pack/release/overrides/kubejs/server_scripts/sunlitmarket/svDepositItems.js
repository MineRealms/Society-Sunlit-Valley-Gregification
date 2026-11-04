// priority: 22
// ============================================================
// 接受仓的物品通道：只收"采石场/挖矿废料"。
//
// 背景：svAcceptBoundary.js 把 global.trades 里出货箱能卖的 2337 项全部设成 -1，
// 所以接受仓原本什么都收不了。这里给石头类废料一个最低价，让"挖矿副产物"有出口。
//
// 注意两点：
//  1. mod 的价格是"每件多少 spur"，最小 1，所以这里只能是 1 spur/件；
//     真正限制产量的是 buyback 每日上限（默认全服 10 万、每人 2 万），
//     也就是说这个通道每天最多换 2 万 spur，和别的通道共用同一个额度。
//  2. 只列真正没有别的用途的方块。带合成用途的（线、骨头、皮革）不要加进来；
//     出货箱已经给价的物品一律跳过，绝不能把 -1 覆盖回来。
// ============================================================
if (typeof SunlitMarket !== 'undefined' && SunlitMarket.depositPrice) {
  let junk = [
    'minecraft:cobblestone', 'minecraft:deepslate', 'minecraft:netherrack',
    'minecraft:tuff', 'minecraft:calcite', 'minecraft:gravel',
    'minecraft:andesite', 'minecraft:diorite', 'minecraft:granite',
    'minecraft:basalt', 'minecraft:blackstone', 'minecraft:end_stone',
    'minecraft:sand', 'minecraft:red_sand', 'minecraft:dirt', 'minecraft:flint'
  ]
  let priced = 0
  let skipped = 0
  junk.forEach((id) => {
    let row = typeof global !== 'undefined' && global.trades ? global.trades.get(id) : null
    if (row && row.value > 0) { skipped++; return }
    SunlitMarket.depositPrice(id, 1)
    priced++
  })
  console.info('[SV-INTEGRATION] deposit item channel: ' + priced + ' quarry-waste items at 1 spur each'
    + (skipped > 0 ? ' (' + skipped + ' skipped: shipping bin already prices them)' : ''))
}
