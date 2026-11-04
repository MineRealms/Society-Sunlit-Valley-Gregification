// priority: 9
// ============================================================
// 成交 -> 任务阶段
//
// 柜台成交后给玩家加阶段，供 FTB Quests 直接当任务条件用；
// 同时镜像成 SunlitMarket 的 unlock id，商店 offer 的 unlock 字段可以引用。
// 阶段名：sm_pawn_first / sm_pawn_ten / sm_pawn_fifty
// 解锁 id：sv.pawn.sm_pawn_first 等（一一对应）。
// ============================================================
if (typeof SunlitMarket !== 'undefined' && typeof SunlitMarketEvents !== 'undefined') {
  let MILESTONES = [[1, 'sm_pawn_first'], [10, 'sm_pawn_ten'], [50, 'sm_pawn_fifty']]

  SunlitMarketEvents.afterTrade((event) => {
    try {
      let player = event.player
      if (!player) return
      let count = Math.round(Number(player.persistentData.smPawnTrades) || 0) + 1
      player.persistentData.smPawnTrades = count
      for (let i = 0; i < MILESTONES.length; i++) {
        let at = MILESTONES[i][0]
        let stage = MILESTONES[i][1]
        if (count !== at) continue
        player.stages.add(stage)
        SunlitMarket.unlock(player, 'sv.pawn.' + stage)
        player.tell(Text.of('当铺成交 ' + count + ' 次').gold())
      }
    } catch (err) {
      console.warn('[SV-INTEGRATION] trade stage hook failed: ' + err)
    }
  })
  console.info('[SV-INTEGRATION] trade stage hook installed')
}
