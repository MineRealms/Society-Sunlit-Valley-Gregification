// priority: 23
// ============================================================
// 寄售行的手续费。
//
// 玩家之间直接成交：买家付的钱进当铺现金，卖家立刻拿 98%（在线就当场到账，
// 离线就先记账，上线后 /sunlitmarket consign claim 领取），
// 剩下 2% 从现金挪进发行准备金 R —— 不销毁，用来做日常补款。
//
// 改这里就是改抽成，reload 立刻生效，不用动 mod。
// 上限 2000 bps（20%），下限 0。
// ============================================================
if (typeof SunlitMarket !== 'undefined' && SunlitMarket.consignmentFee) {
  SunlitMarket.consignmentFee(200)   // 200 bps = 2%
  console.info('[SV-INTEGRATION] consignment fee set to 2% (200 bps)')
}
