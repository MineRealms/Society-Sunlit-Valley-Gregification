// priority: 0
// ============================================================
// GTMFO × Sunlit Valley — R4: GT 配方（GTMFO 机器加工整合包物品）
// 进度文档：GTMFO_INTEGRATION.md
//
// 事实依据（均为源码/导出核对，非推测）：
//  - GTCEu 7.5.2 源码 integration/kjs/GregTechKubeJSPlugin.registerRecipeSchemas：
//      每个 GT 配方类型注册为 event.recipes.<namespace>.<path>
//  - GTMFO 自定义配方类型经 GTRecipeTypes.register("slicer"/"extractor", ...) 注册，
//      该方法内部用 GTCEu.id(name) → 命名空间是 gtceu:（证据：JEI 导出分类 gtceu:slicer / gtceu:baking_oven）
//  - 方法来自 integration/kjs/recipe/GTRecipeSchema.java 的 GTRecipeJS：
//      itemInputs / itemOutputs("Nx id") / notConsumable / outputFluids / duration / EUt
//  - id 会自动加 "<类型路径>/" 前缀（GTRecipeJS.id() 源码）
//  - Fluid.of("id", mB) 写法与包内 startup 脚本一致（KubeJS 自动把字符串转为 FluidStackJS，
//      证据：globalBlockEntityHandlers.js:806 `Fluid.of("minecraft:water", 0)`）
// 数值镜像 GTMFO 自身配方（CoreChain / 见每条的注释）
// ============================================================
console.info("[GTMFO-INTEGRATION] addGtmfoGtRecipes.js loaded (R4 gt recipes)");

ServerEvents.recipes((e) => {
  // ===== 切片机（gtceu:slicer）：整合包蔬菜 → GTMFO 切片 =====
  // 镜像 CoreChain.slice_*：平板刀片，1 → 8，EUt 18 / 30t
  const slicer = (id, input, output) => {
    e.recipes.gtceu.slicer(id)
      .itemInputs(input)
      .notConsumable("gtmfo:slicer_blade_flat")
      .itemOutputs("8x " + output)
      .duration(30)
      .EUt(18);
  };
  slicer("gtmfo:compat/slice_onion", "farm_and_charm:onion", "gtmfo:onion_slice");
  slicer("gtmfo:compat/slice_tomato", "farmersdelight:tomato", "gtmfo:tomato_slice");
  slicer("gtmfo:compat/slice_cucumber", "vintagedelight:cucumber", "gtmfo:cucumber_slice");
  slicer("gtmfo:compat/slice_eggplant", "society:eggplant", "gtmfo:eggplant_slice");

  // ===== 提取机（gtceu:extractor）：整合包柑橘 → GTMFO 提取液 =====
  // 镜像 CoreChain.lemon_zest / lime_zest / orange_zest：EUt 5 / 100t，碎皮粉 + 100mB
  const zest = (id, input, fluid) => {
    e.recipes.gtceu.extractor(id)
      .itemInputs(input)
      .itemOutputs("gtceu:zest_dust")
      .outputFluids(Fluid.of(fluid, 100))
      .duration(100)
      .EUt(5);
  };
  zest("gtmfo:compat/zest_orange_pam", "pamhc2trees:orangeitem", "gtceu:orange_extract");
  zest("gtmfo:compat/zest_orange_atmospheric", "atmospheric:orange", "gtceu:orange_extract");
  zest("gtmfo:compat/zest_lemon", "pamhc2trees:lemonitem", "gtceu:lemon_extract");

  // 番茄酱：镜像 CoreChain.tomato_sauce（EUt 2 / 10t，100mB；GTFO 用番茄片，这里直接用整番茄）
  e.recipes.gtceu.extractor("gtmfo:compat/tomato_sauce")
    .itemInputs("farmersdelight:tomato")
    .outputFluids(Fluid.of("gtceu:tomato_sauce", 100))
    .duration(10)
    .EUt(2);
});
