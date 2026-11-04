// priority: 21
// ============================================================
// 接受仓的"收什么"和"怎么定价"全在这里。
//
// mod 侧只保留通用默认值（流体 1、FE 50000、魔力 2000、源质 1:1），
// 具体哪种流体、哪个要素值多少，是整合包数据，写在脚本里。
// 脚本每次加载都会写一遍，tick 保存点回写到
// config/sunlitmarket/deposit_values.json，所以脚本就是唯一真相。
//
// 另一条边界在 svAcceptBoundary.js：出货箱能卖的东西一律 -1 拒收。
// ============================================================
if (typeof SunlitMarket !== 'undefined' && SunlitMarket.depositFluidRate) {
  // ---- 流体：spur / 每单位 ----
  SunlitMarket.depositFluidRate('default', 1)
  SunlitMarket.depositFluidRate('gtceu:diesel', 8)
  SunlitMarket.depositFluidRate('gtceu:gasoline', 10)
  SunlitMarket.depositFluidRate('gtceu:oil', 6)
  SunlitMarket.depositFluidRate('gtceu:sulfuric_acid', 3)
  SunlitMarket.depositFluidRate('gtceu:creosote', 2)
  SunlitMarket.depositFluidRate('gtceu:heavy_fuel', 7)
  SunlitMarket.depositFluidRate('gtceu:light_fuel', 7)
  SunlitMarket.depositFluidRate('gtceu:naphtha', 6)
  SunlitMarket.depositFluidRate('gtceu:refinery_gas', 4)

  // ---- FE / 魔力 ----
  SunlitMarket.depositEnergyRate(50000)   // 50000 FE = 1 spur
  SunlitMarket.depositManaRate(2000)      // 2000 mana = 1 spur

  // ---- 源质：默认 1 点 = 1 spur，按稀有度分档 ----
  // 数值 = 多少点换 1 spur。数字越小越值钱。
  SunlitMarket.depositEssentiaRate(4)     // 兜底：4 点 = 1 spur
  let common = ['aer', 'terra', 'ignis', 'aqua', 'ordo', 'perditio',
                'herba', 'arbor', 'victus', 'messis', 'meto', 'perfodio',
                'pannus', 'instrumentum', 'telum', 'fames', 'limus',
                'metallum', 'lucrum', 'corpus']
  common.forEach((a) => SunlitMarket.depositAspectRate(a, 4))
  let uncommon = ['gelum', 'lux', 'motus', 'permutatio', 'potentia', 'praecantatio',
                  'vitreus', 'sano', 'sensus', 'bestia', 'humanus', 'exanimis',
                  'mortuus', 'spiritus', 'machina', 'iter', 'volatus', 'tutamen',
                  'vinculum', 'fabrico', 'venenum']
  uncommon.forEach((a) => SunlitMarket.depositAspectRate(a, 2))
  let rare = ['auram', 'alienis', 'cognitio', 'vitium', 'tempestas', 'vacuos', 'tenebrae']
  rare.forEach((a) => SunlitMarket.depositAspectRate(a, 1))

  console.info('[SV-INTEGRATION] deposit rates: fluid default=' + 1
    + ' energy=50000:1 mana=2000:1 essentia 4/2/1 by tier')
}
