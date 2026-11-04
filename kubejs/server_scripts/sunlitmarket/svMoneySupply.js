// priority: 9
// ============================================================
// M0 / 债务 -> 审计
//
// SunlitMarket 不自己算货币总量：银行和债务账本都属于整合包。这里按
// updateCoinLeaderboard.js 的口径遍历 global.GLOBAL_BANK.accounts 求和，
// 再把 server.persistentData.debts 的未偿总额一起报给审计。
// 报上去之后 /sunlitmarket 的审计状态里 M0 不再是 UNKNOWN，
// 当铺现金 C 和发行准备金 R 才有校准依据（见 docs/SUNLIT_INTEGRATION_PLAN.md 的 S0）。
// ============================================================
if (typeof SunlitMarket !== 'undefined' && typeof global !== 'undefined' && Platform.isLoaded('society')) {
  let bankTotal = () => {
    try {
      if (!global.GLOBAL_BANK || !global.GLOBAL_BANK.accounts) return -1
      let total = 0
      global.GLOBAL_BANK.accounts.forEach((uuid, account) => {
        let balance = Number(account.getBalance())
        if (isFinite(balance)) total += balance
      })
      return Math.round(total)
    } catch (err) {
      console.warn('[SV-INTEGRATION] GLOBAL_BANK scan failed: ' + err)
      return -1
    }
  }

  let debtTotal = (server) => {
    let total = 0
    let rows = server.persistentData.debts
    if (rows) {
      for (let i = 0; i < rows.length; i++) {
        let amount = Number(rows[i].amount)
        if (isFinite(amount) && amount > 0) total += amount
      }
    }
    return Math.round(total)
  }

  let lastLogged = -1
  let report = (server) => {
    let total = bankTotal()
    if (total < 0) return
    let debts = debtTotal(server)
    SunlitMarket.auditSupply(total, debts)
    if (total !== lastLogged) {
      lastLogged = total
      console.info('[SV-INTEGRATION] M0=' + total + ' debts=' + debts)
    }
  }

  ServerEvents.loaded((event) => report(event.server))
  ServerEvents.tick((event) => { if (event.server.getTickCount() % 1200 === 0) report(event.server) })
  PlayerEvents.loggedIn((event) => { if (event.player.getServer()) report(event.player.getServer()) })
  console.info('[SV-INTEGRATION] money supply reporter installed')
}
