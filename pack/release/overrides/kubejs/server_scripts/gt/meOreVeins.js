// priority: 10
// ============================================================
// GregTech 矿脉改道：EV 阶段的矿只在中洲（Middle-earth）生成
//
// 来源 → 群系：
//   末地来源（pitchblende / scheelite / sheldonite）→ #me:is_mordor（魔多/阴影）
//   下界来源（molybdenum）→ #me:is_cave
//
// 说明：
//   - 只影响新生成区块；已探索区块不会补矿
//   - 被移走的矿脉不再在末地/下界生成
//   - IV 阶段及之后的矿（naquadah / monazite）已改去亚尔夫海姆，见 alfheimOreVeins.js
//   - 高度范围沿用原矿脉（ME 世界 min_y=-4，表面 ~66+）
//   - 岩层：startup_scripts/gt/worldGenLayers.js 的 middle_earth 层
// ============================================================
console.info("[GT-ORES] meOreVeins.js loaded")

const ME_VEINS = [
  // ---- 末地来源 → 魔多/阴影群系 ----
  { id: "gtceu:pitchblende_vein_end", biomes: "#me:is_mordor" },
  { id: "gtceu:scheelite_vein", biomes: "#me:is_mordor" },
  { id: "gtceu:sheldonite_vein", biomes: "#me:is_mordor" },
  // ---- 下界来源 → 洞穴群系 ----
  { id: "gtceu:molybdenum_vein", biomes: "#me:is_cave" },
]

GTCEuServerEvents.oreVeins(event => {
  ME_VEINS.forEach(v => {
    event.modify(v.id, vein => {
      vein.layer("middle_earth")
      vein.dimensions("me:middle-earth")
      vein.biomes(v.biomes)
    })
  })
  console.info(`[GT-ORES] moved ${ME_VEINS.length} veins to Middle-earth`)
})
