// priority: 0
// ============================================================
// GCYR × GT--（gtnn）燃料互通
//
// 事实依据（反编译核对，非推测）：
//   - GTNN 火箭引擎配方类型注册于 gtceu:rocket_engine（GTNNRecipeTypes 调用 GTRecipeTypes.register）
//     原配方：rp_1(4mB/3t) / dense_hydrazine(2mB/3t) / MHN(1mB/3t) / UDMH(1mB/6t)，EUt = -V[4]（-2048，发电）
//   - GTNN 燃料为 GT 材料（lang material.gtceu.rp_1_rocket_fuel 等）→ 流体 id：gtceu:rp_1_rocket_fuel 等
//   - GCYR 火箭燃料配方（RocketFuelRecipes.java）：
//       汽油25t/柴油18t/火箭燃料75t/氢10t/氢等离子18t（每 mB 燃烧时长，duration 字段）
//       EUt 字段 = 所需发动机等级（1=基础 2=先进 3=精英）
//
// 本脚本：
//   B1 让 GTNN 引擎燃烧 GCYR 燃料（发电）
//   B2 让 GTNN 高级燃料驱动 GCYR 火箭（燃烧时长更长，但需要更高级发动机）
// ============================================================
console.info("[GCYR-GTNN] gtnnLinks.js loaded");

ServerEvents.recipes((e) => {
  if (!Platform.isLoaded("gcyr") || !Platform.isLoaded("gtnn")) return;

  // ---- B1：GTNN 火箭引擎接受 GCYR 燃料（发电，EUt 负值）----
  const engineFuels = [
    ["gtceu:rocket_fuel", 1, 4],      // 精炼火箭燃料：1mB / 4t
    ["gtceu:gasoline", 4, 3],         // 汽油（≈RP-1）：4mB / 3t
    ["gtceu:diesel", 3, 3],           // 柴油：3mB / 3t
    ["mekanism:hydrogen", 8, 3],      // Mek 氢（低密度）：8mB / 3t
  ];
  engineFuels.forEach(([fluid, amount, duration]) => {
    e.recipes.gtceu.rocket_engine("kubejs:rocket_engine_" + fluid.split(":")[1])
      .inputFluids(Fluid.of(fluid, amount))
      .duration(duration)
      .EUt(-2048, 1);
  });

  // ---- B2：GTNN 高级燃料驱动 GCYR 火箭 ----
  // duration = 每 mB 燃烧时长（越高越省燃料）；EUt = 最低发动机等级
  const rocketFuels = [
    ["gtceu:rp_1_rocket_fuel", 50, 1],                     // RP-1（煤油系）
    ["gtceu:dense_hydrazine_mixed_fuel", 60, 2],           // 稠密肼混合燃料
    ["gtceu:udmh_rocket_fuel", 90, 2],                     // UDMH
    ["gtceu:methylhydrazine_nitrate_rocket_fuel", 100, 3], // MHN（最强）
  ];
  rocketFuels.forEach(([fluid, duration, tier]) => {
    e.recipes.gcyr.rocket_fuel("kubejs:rocket_fuel_" + fluid.split(":")[1])
      .inputFluids(Fluid.of(fluid, 1))
      .duration(duration)
      .EUt(tier, 1);
  });
});
