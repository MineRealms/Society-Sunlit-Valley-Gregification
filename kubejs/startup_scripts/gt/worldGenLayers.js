// priority: 0
// ============================================================
// GregTech 世界生成层（World Gen Layer）
// 为暮色森林 / 骷髅洞穴注册可被 GT 矿脉替换的岩层。
// 参考：GTCEu 官方文档 Modpacks/Ore-Generation/04-Layers-and-Dimensions
//   - 层名将在 oreVeins.js 中通过 vein.layer("...") 引用
//   - targets 支持标签 / 方块 / 方块状态
//   - dimensions 决定该层适用的维度
// ============================================================
console.info("[GT-ORES] worldGenLayers.js loaded")

GTCEuStartupEvents.registry("gtceu:world_gen_layer", event => {
  // 暮色森林：主世界式地形（石头 + 深板岩）
  // 维度 min_y=-32, height=288
  event.create("twilight_forest")
    .targets("#minecraft:stone_ore_replaceables", "#minecraft:deepslate_ore_replaceables")
    .dimensions("twilightforest:twilight_forest")

  // 骷髅洞穴：Society 自定义岩层（skull_cavern.json noise_settings）
  // 维度 min_y=0, height=512；岩层含主石与各群系表层岩
  event.create("skull_cavern")
    .targets(
      "#minecraft:stone_ore_replaceables",
      "#minecraft:deepslate_ore_replaceables",
      "society:skull_stone",
      "society:skull_blackstone",
      "society:skull_arid_sandstone",
      "society:skull_sandstone",
      "society:skull_end_stone",
      "society:skull_permafrost"
    )
    .dimensions("society:skull_cavern")
})
