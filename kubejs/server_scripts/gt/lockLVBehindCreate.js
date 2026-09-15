// priority: 0
// ============================================================
// GT × Create 联动：LV 门槛（R1）
// 进度文档：GT_INTEGRATION.md「3. LV 门槛（Create × GT）」
//
// 目标：卡住 GT 的 LV 科技线 —— LV 电路不再用 GT 真空管，
//       改用 Create 的电子管（中期元件），必须先发展 Create
//
// 事实依据（源码 / 文档 / 包内先例核对，非推测）：
//  - GTCEu 7.5.2 源码 data/recipe/misc/CircuitRecipes.java:1007-1013
//      shaped electronic_circuit_lv: "RPR","VBV","CCC"
//      'V' = VACUUM_TUBE.asStack()（真空管，物品）
//    同文件 1015-1021 电路组装机版用 CustomTags.ULV_CIRCUITS（标签）——
//    该机器在 LV 门槛之后才能建造，故本次只改工作台版（一行生效）
//  - 物品 ID 以包内 7.5.3 注册名为准：gtceu:basic_electronic_circuit
//    （证据：gtceu-1.20.1-7.5.3.jar assets/gtceu/lang/en_us.json）
//  - KubeJS replaceInput 按 output 过滤：GTCEu 官方文档
//    docs/content/Modpacks/Recipes/Adding-and-Removing-Recipes.md
//    （event.replaceInput({ mod: 'gtceu' }, ...)）
//    包内已有用法：kubejs/server_scripts/recipes/removeRecipes.js:1086
// ============================================================
console.info("[GT-LV-GATE] lockLVBehindCreate.js loaded");

ServerEvents.recipes((e) => {
  // LV 电路（工作台）：真空管 → Create 电子管
  e.replaceInput({ output: "gtceu:basic_electronic_circuit" }, "gtceu:vacuum_tube", "create:electron_tube");
});
