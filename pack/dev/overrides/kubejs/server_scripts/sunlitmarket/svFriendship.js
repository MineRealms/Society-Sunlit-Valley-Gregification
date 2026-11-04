// priority: 9
// ============================================================
// 好感度 -> 结盟值
//
// 整合包把 NPC 好感度存在 player.persistentData.npcData[<id>].friendship：
// 100 点一颗心、上限 500、-1 表示还没见过。SunlitMarket 的派系 id 是 society:<id>。
//
// 好感度是唯一真相，结盟值只是它的投影：每次同步算出目标值，只补差额、从不往下调。
// 这样柜台成交、还价、走私带来的额外结盟值不会被覆盖；每天 1 点的自然衰减也会在
// 下一次同步时被好感度补回来（送礼本身不走成交事件，所以另加 30 秒轮询）。
// 映射：friendship * 2，落在 -1000..3000，正好对上默认价目表
//   （100 好感 = 常客，250 = 盟友，500 = 挚友）。
// ============================================================
if (typeof SunlitMarket !== 'undefined' && typeof global !== 'undefined' && Platform.isLoaded('society')) {
  let NPC_IDS = ['banker', 'blacksmith', 'carpenter', 'fisher', 'librarian', 'market', 'shepherd', 'trader', 'witch', 'wise_oak']

  let target = (friendship) => {
    let value = Math.round(Number(friendship) * 2)
    if (!isFinite(value)) return 0
    return Math.max(-1000, Math.min(3000, value))
  }

  let sync = (player) => {
    try {
      let data = player.persistentData.npcData
      if (!data) return
      for (let i = 0; i < NPC_IDS.length; i++) {
        let row = data[NPC_IDS[i]]
        if (!row) continue
        let friendship = Number(row.friendship)
        if (!isFinite(friendship) || friendship === -1) continue
        let faction = 'society:' + NPC_IDS[i]
        let want = target(friendship)
        let have = SunlitMarket.alignment(player, faction)
        // 只补不扣：成交赚到的结盟值高于好感度时应保留。
        if (want > have) SunlitMarket.addAlignment(player, faction, want - have)
      }
    } catch (err) {
      console.warn('[SV-INTEGRATION] friendship sync failed: ' + err)
    }
  }

  PlayerEvents.loggedIn((event) => sync(event.player))
  PlayerEvents.tick((event) => { if (event.player.age % 600 === 0) sync(event.player) })
  SunlitMarketEvents.afterTrade((event) => { if (event.player) sync(event.player) })
  console.info('[SV-INTEGRATION] friendship -> alignment bridge installed')
}
