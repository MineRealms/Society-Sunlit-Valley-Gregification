// priority: 10
// ============================================================
// GregTech 矿脉改道：IV 阶段及之后的矿只去亚尔夫海姆（Pollution）
//
// 亚尔夫海姆维度：pollution:alfheim，地形为 Botania livingrock
// 岩层：Pollution 已注册的 pollution_alfheim 层（stone / livingrock）
//
// 说明：
//   - 只影响新生成区块；已探索区块不会补矿
//   - 被移走的矿脉不再在末地/下界生成
//   - 高度范围沿用原矿脉（Alfheim 世界 0..255）
// ============================================================
console.info("[GT-ORES] alfheimOreVeins.js loaded")

// IV 阶段及之后的矿脉 → 亚尔夫海姆
const ALFHEIM_VEINS = [
  "gtceu:naquadah_vein",
  "gtceu:monazite_vein",
]

GTCEuServerEvents.oreVeins(event => {
  ALFHEIM_VEINS.forEach(id => {
    event.modify(id, vein => {
      vein.layer("pollution_alfheim")
      vein.dimensions("pollution:alfheim")
      vein.biomes(
        "pollution:alfheim_field",
        "pollution:alfheim_giant_flower_field",
        "pollution:alfheim_beach",
        "pollution:alfheim_sandbank",
        "pollution:alfheim_river",
        "pollution:alfheim_low_plateau",
        "pollution:alfheim_mid_plateau",
        "pollution:alfheim_high_plateau",
        "pollution:alfheim_high_plateau_forest",
        "pollution:alfheim_high_plateau_field",
        "pollution:alfheim_island_forest",
        "pollution:alfheim_pit_forest"
      )
    })
  })
  console.info(`[GT-ORES] moved ${ALFHEIM_VEINS.length} veins to Alfheim`)
})
