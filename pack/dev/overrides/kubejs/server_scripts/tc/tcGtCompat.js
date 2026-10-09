// priority: 0
// ============================================================
// TC4（神秘时代）× GT — 机器加工联动
// 进度文档：TC4_INTEGRATION.md 第 7.3 节
//
// 目标：GT 机器可以加工 TC4 材料（辰砂矿 / 琥珀矿石 / 水银）
//
// 事实依据（源码 / JAR 核对，非推测）：
//  - TC4 物品 ID：thaumcraft:cinnabar_ore / amber_bearing_stone / quicksilver
//    （证据：TC4 20711 源码包 data/thaumcraft/recipes/ 内的物品引用）
//  - GT 材料 ID：gtceu:cinnabar_dust；水银流体 gtceu:mercury
//    （证据：H:\tools\jei_names.json 存在 gtceu:cinnabar_dust / gtceu:mercury / gtceu:flowing_mercury）
//  - 数值镜像 GTCEu 源码 OreRecipeHandler.java:121-128：
//      矿石研磨 = EUt 2 / duration 400（2x 碎矿惯例）
//  - KubeJS 写法镜像包内先例 kubejs/server_scripts/recipes/addGtmfoGtRecipes.js
// ============================================================
console.info("[TC4-INTEGRATION] tcGtCompat.js loaded (gt recipes)");

ServerEvents.recipes((e) => {
  if (!Platform.isLoaded("thaumcraft")) return;

  // 辰砂矿 → 2x 辰砂粉（镜像 GT 矿石研磨数值）
  e.recipes.gtceu.macerator("tc4:compat/cinnabar_ore_to_dust")
    .itemInputs("thaumcraft:cinnabar_ore")
    .itemOutputs("2x gtceu:cinnabar_dust")
    .duration(400)
    .EUt(2, 1);

  // 琥珀矿石 → 2x 琥珀
  e.recipes.gtceu.macerator("tc4:compat/amber_bearing_stone_to_amber")
    .itemInputs("thaumcraft:amber_bearing_stone")
    .itemOutputs("2x thaumcraft:amber")
    .duration(400)
    .EUt(2, 1);

  // 神秘水银 → GT 水银（提取机，144mB = 1 锭当量）
  e.recipes.gtceu.extractor("tc4:compat/quicksilver_to_mercury")
    .itemInputs("thaumcraft:quicksilver")
    .outputFluids(Fluid.of("gtceu:mercury", 144))
    .duration(60)
    .EUt(30, 1);
});
