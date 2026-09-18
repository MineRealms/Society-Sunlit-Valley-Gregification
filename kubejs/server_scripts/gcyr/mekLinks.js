// priority: 0
// ============================================================
// GCYR × Mekanism 联动（氧气 / 氢气）
//
// 事实依据（源码/数据核对，非推测）：
//   - GCYR 宇航服灌装检查流体标签 forge:oxygen
//     （SpaceSuitArmorItem.canFillFluidType → GCYRTags.OXYGEN = forge:oxygen）
//   - Mekanism 液态氧/液氢已挂 forge:oxygen / forge:hydrogen 标签
//     （mekanism-10.4.16.80.jar: data/forge/tags/fluids/oxygen.json / hydrogen.json）
//     → 宇航服可直接灌 Mek 氧气，无需任何转换（本脚本不含此部分）
//   - GCYR 氧扩散器配方写死 gtceu:oxygen；火箭氢燃料写死 gtceu:hydrogen
//     → 本脚本为两者补 Mek 流体配方（GCYR 自定义 GT 配方类型经 KubeJS 注册）
//   - 参数镜像 GCYR 原配方：
//       氧扩散器：750mB 氧气/10L 档（circuit 1），同理 1500/3750/7500/75000/750000
//       氢燃料：1mB / 燃烧时长 10t / EUt 1
// ============================================================
console.info("[GCYR-MEK] mekLinks.js loaded");

ServerEvents.recipes((e) => {
  if (!Platform.isLoaded("gcyr") || !Platform.isLoaded("mekanism")) return;

  // ---- 火箭燃料：Mek 液态氢（镜像 gtceu:hydrogen：1mB / 10t / EUt 1）----
  e.recipes.gcyr.rocket_fuel("kubejs:rocket_fuel_mek_hydrogen")
    .inputFluids(Fluid.of("mekanism:hydrogen", 1))
    .duration(10)
    .EUt(1, 1);

  // ---- 氧扩散器：Mek 液态氧（镜像 GCYR 氧气档位）----
  const sizes = [
    [1, 750],      // 10L
    [2, 1500],     // 20L
    [3, 3750],     // 50L
    [4, 7500],     // 100L
    [5, 75000],    // 1000L
    [6, 750000],   // 10000L
  ];
  sizes.forEach(([circuit, amount]) => {
    e.recipes.gcyr.oxygen_spreader("kubejs:oxygen_spreader_mek_oxygen_" + amount)
      .circuit(circuit)
      .inputFluids(Fluid.of("mekanism:oxygen", amount))
      .duration(20)
      .EUt(30, 1);
  });
});
