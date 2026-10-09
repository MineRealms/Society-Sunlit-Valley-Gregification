// priority: 0
// ============================================================
// GCYR 汽油/柴油火箭燃料修复
//
// 事实依据（反编译核对 + 服务器日志）：
//   - GCYR 0.2.9 RocketFuelRecipes.java 用 EUt(0) 注册燃料配方：
//       gasoline: 1mB / 25t   diesel: 1mB / 18t   （rocket_fuel/hydrogen 等用 EUt≥1，正常注册）
//   - GTCEu 7.5.x 拒绝 EUt=0 的配方（日志：EUt can't be explicitly set to 0, id: gcyr:gasoline / gcyr:diesel）
//     → 这两条配方未注册 → RocketEntity 的燃料检查（按 ROCKET_FUEL_RECIPES 匹配流体）
//       不接受汽油/柴油 → 火箭无法使用它们
//   - EUt 字段含义 = 所需发动机等级（见 gtnnLinks.js 的核对结论）
//
// 修复：以 EUt(1,1)（基础发动机级）重新注册，duration 与原值一致
// ============================================================
console.info("[GCYR-FUEL-FIX] fixRocketFuels.js loaded");

ServerEvents.recipes((e) => {
  if (!Platform.isLoaded("gcyr")) return;

  e.recipes.gcyr.rocket_fuel("kubejs:gcyr_fuel_gasoline")
    .inputFluids(Fluid.of("gtceu:gasoline", 1))
    .duration(25)
    .EUt(1, 1);

  e.recipes.gcyr.rocket_fuel("kubejs:gcyr_fuel_diesel")
    .inputFluids(Fluid.of("gtceu:diesel", 1))
    .duration(18)
    .EUt(1, 1);
});
