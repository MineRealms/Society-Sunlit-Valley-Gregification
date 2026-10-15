// priority: 0
// ============================================================
// 神秘时代 × 农业稀有物 —— 坩埚田园琥珀
//
// 目标：长翼蝴蝶养殖的 society:butterfly_amber 投坩埚，
//       炼出 2× thaumcraft:amber（神秘琥珀）
//
// 事实依据（JAR / 包内先例核对，非推测）：
//  - thaumcraft-forge-4.2.3.5-1.20.1-port 配方结构：
//      data/thaumcraft/recipes/crucible/minecraft/*.json
//      type=thaumcraft:crucible，result 支持 count（bone_meal=4）
//  - 包内自定义坩埚先例：tcRecipes.js
//      quicksilver_from_cinnabar_dust（research 字段可省略）
//  - 蝴蝶琥珀来源：长翼蝴蝶好感互动
//      （kubejs/server_scripts/entities/checkAnimal.js）
//  - 任务标注：thaumcraft.snbt「田园琥珀」
// ============================================================
console.info("[TC-FARM-BRIDGE] tcFarmBridge.js loaded");

ServerEvents.recipes((e) => {
  if (!Platform.isLoaded("thaumcraft")) return;

  e.custom({
    type: "thaumcraft:crucible",
    catalyst: { item: "society:butterfly_amber" },
    result: { item: "thaumcraft:amber", count: 2 },
    aspects: { terra: 2, ignis: 1 },
  }).id("tc4:compat/amber_from_butterfly_amber");
});
