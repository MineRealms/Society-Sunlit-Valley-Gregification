// priority: -10
// ============================================================
// GregTech 矿脉深度规则：越深 = 电压越高
//
// 每个维度按自身可挖深度（表面 → min_y）分 4 档：
//   浅档  = LV/MV 材料
//   中档  = HV 材料
//   深档  = EV 材料
//   最深档 = IV 及之后材料
//
// 各维度深度档（按表面与 min_y 等分）：
//   主世界   (表面 64, min_y -64)：浅 32..64 / 中 0..32 / 深 -32..0 / 最深 -64..-32
//   暮色森林 (表面 64, min_y -32)：浅 40..64 / 中 16..40 / 深 -8..16 / 最深 -32..-8
//   中洲     (表面 66, min_y -4) ：浅 48..66 / 中 31..48 / 深 13..31 / 最深 -4..13
//   亚尔夫海姆(表面 64, min_y 0) ：浅 48..64 / 中 32..48 / 深 16..32 / 最深 0..16
//
// 说明：
//   - 只改高度范围，不改维度/群系（维度门槛见 tf/me/alfheim 脚本）
//   - 主世界深板岩层天然在深处，故深板岩矿脉落在深/最深档
//   - 只影响新生成区块
// ============================================================
console.info("[GT-ORES] depthOreVeins.js loaded")

const HEIGHT_BANDS = {
  // ---- 主世界：LV/MV 浅档，深板岩落深/最深档 ----
  // 浅档（石层 LV/MV）
  'gtceu:apatite_vein': [32, 64],
  'gtceu:cassiterite_vein': [32, 64],
  'gtceu:coal_vein': [32, 64],
  'gtceu:copper_tin_vein': [32, 64],
  'gtceu:galena_vein': [32, 64],
  'gtceu:garnet_tin_vein': [32, 64],
  'gtceu:iron_vein': [32, 64],
  'gtceu:lubricant_vein': [32, 64],
  'gtceu:mineral_sand_vein': [32, 64],
  'gtceu:salts_vein': [32, 64],
  'gtceu:oilsands_vein': [32, 64],
  // 中档
  'gtceu:garnet_vein': [0, 32],
  // 深档（深板岩）
  'gtceu:copper_vein': [-32, 0],
  'gtceu:diamond_vein': [-32, 0],
  'gtceu:lapis_vein': [-32, 0],
  'gtceu:redstone_vein_ow': [-32, 0],
  // 最深档（深板岩）
  'gtceu:mica_vein': [-64, -32],
  'gtceu:sapphire_vein': [-64, -32],

  // ---- 暮色森林：HV 中档 16..40 ----
  'kubejs:tf_bauxite_vein': [16, 40],
  'kubejs:tf_magnetite_end_vein': [16, 40],
  'kubejs:tf_magnetite_vein': [16, 40],
  'kubejs:tf_nickel_vein': [16, 40],
  'kubejs:tf_manganese_vein': [16, 40],
  'kubejs:tf_olivine_vein': [16, 40],

  // ---- 中洲：EV 深档 13..31 ----
  'gtceu:pitchblende_vein_end': [13, 31],
  'gtceu:scheelite_vein': [13, 31],
  'gtceu:sheldonite_vein': [13, 31],
  'gtceu:molybdenum_vein': [13, 31],

  // ---- 亚尔夫海姆：IV+ 最深档 0..16 ----
  'gtceu:naquadah_vein': [0, 16],
  'gtceu:monazite_vein': [0, 16],
}

GTCEuServerEvents.oreVeins(event => {
  Object.entries(HEIGHT_BANDS).forEach(([id, [min, max]]) => {
    event.modify(id, vein => vein.heightRangeUniform(min, max))
  })
  console.info(`[GT-ORES] applied depth bands to ${Object.keys(HEIGHT_BANDS).length} veins`)
})
