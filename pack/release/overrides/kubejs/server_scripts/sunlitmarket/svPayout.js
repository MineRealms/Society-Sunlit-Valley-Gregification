// priority: 12
// ============================================================
// 付款先还医院债务
//
// 出货箱（globalShippingBinHandlers.js#handleShippingBinDebt）在给钱之前先把
// server.persistentData.debts 里的欠款扣掉。SunlitMarket 的三条付款路径
// （柜台收购、顾客采购、接受仓结算）也走同一个 Currency.settle，所以在这里
// 注册一个 payout sink，把同样的顺序补上——否则玩家可以靠当铺绕开医院债务。
//
// divert 返回"不要发给玩家的部分"，失败时 mod 会回调 rollback 把这笔钱加回债务。
// ============================================================
if (typeof SunlitMarket !== 'undefined' && typeof global !== 'undefined' && Platform.isLoaded('society')) {
  let debtRow = (server, uuid) => {
    let rows = server.persistentData.debts
    if (!rows) return null
    for (let i = 0; i < rows.length; i++) {
      if (String(rows[i].uuid) === String(uuid)) return rows[i]
    }
    return null
  }

  let amountOf = (row) => {
    let value = Math.round(Number(row.amount))
    return isFinite(value) && value > 0 ? value : 0
  }

  let notify = (player, paid) => {
    try {
      let text = typeof global.formatPrice === 'function' ? global.formatPrice(String(paid)) : String(paid)
      player.tell(Text.translatable('society.shipping_bin.debt_paid', text).gold())
    } catch (err) {
      // 提示失败不影响付款
    }
  }

  SunlitMarket.payoutSink(
    (player, amount, reason) => {
      try {
        let server = player.getServer()
        if (!server) return 0
        let row = debtRow(server, player.getUuid())
        if (!row) return 0
        let debt = amountOf(row)
        if (debt <= 0) return 0
        let paid = Math.min(debt, Math.round(Number(amount)))
        if (paid <= 0) return 0
        row.amount = debt - paid
        notify(player, paid)
        return paid
      } catch (err) {
        console.warn('[SV-INTEGRATION] debt-first payout skipped: ' + err)
        return 0
      }
    },
    (player, diverted, reason) => {
      try {
        let server = player.getServer()
        if (!server) return
        let row = debtRow(server, player.getUuid())
        if (row) {
          row.amount = amountOf(row) + Math.round(Number(diverted))
          return
        }
        if (!server.persistentData.debts) server.persistentData.debts = []
        server.persistentData.debts.push({ uuid: String(player.getUuid()), amount: Math.round(Number(diverted)) })
      } catch (err) {
        console.warn('[SV-INTEGRATION] debt rollback failed: ' + err)
      }
    }
  )
  console.info('[SV-INTEGRATION] debt-first payout sink installed')
}
