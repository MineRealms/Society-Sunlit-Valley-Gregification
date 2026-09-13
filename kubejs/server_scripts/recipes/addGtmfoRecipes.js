// priority: 0
// ============================================================
// GTMFO × Sunlit Valley — R3: 加工配方（整合包机器处理 GTMFO 物品）
// 进度文档：GTMFO_INTEGRATION.md
// 只加配方，不动物品/标签；给 GTMFO 内容提供非 GT 电力路径
//
// 配方 schema 来源（均为事实核对，非推测）：
//  - farmersdelight:cutting：包内 kubejs/server_scripts/recipes/addMillingRecipes.js 的 addKnifeRecipe
//    （另见 FarmersDelight-1.20.1-1.3.2.jar 的 data/farmersdelight/recipes/cutting/*.json）
//  - create:milling：包内 addMillingRecipes.js 的 addMillRecipe + create-1.20.1-6.0.8.jar
//    自带 data/create/recipes/milling/*.json（processingTime 为合法字段）
//  - create:compacting：包内 kubejs/server_scripts/recipes/addPressingRecipes.js +
//    create-1.20.1-6.0.8.jar 的 data/create/recipes/compacting/*.json（无 processingTime 字段）
// 数值来源：GTMFO 自己的配方（CheeseRecipes / BreadsRecipes / ChocolateRecipes / CoreChain）
// ============================================================
console.info("[GTMFO-INTEGRATION] addGtmfoRecipes.js loaded (R3 recipes)");

ServerEvents.recipes((e) => {
  // Farmer's Delight 切菜板（工具：#forge:tools/knives）
  const knife = (input, output, count) => {
    e.custom({
      type: "farmersdelight:cutting",
      ingredients: [{ item: input }],
      tool: { tag: "forge:tools/knives" },
      result: [{ item: output, count: count }],
    });
  };

  // Create 研磨
  const mill = (input, output, count, time) => {
    e.custom({
      type: "create:milling",
      ingredients: [{ item: input }],
      processingTime: time,
      results: [{ count: count, item: output }],
    });
  };

  // Create 压块
  const compact = (input, output, count) => {
    e.custom({
      type: "create:compacting",
      ingredients: [{ item: input }],
      results: [{ count: count, item: output }],
    });
  };

  // ===== Farmer's Delight 切菜板 =====
  // 数值镜像 GTMFO 自身配方：
  //  cheddar_slice: 切片机 1 → 9（CheeseRecipes.cheddar_slice）
  //  gorgonzola_triangular_slice: 切片机 1 → 16（CheeseRecipes.gorgonzola_triangular_slice）
  //  bread_slice: 手搓（刀）1 → 4（BreadsRecipes.bread_slice_by_hand）
  //  bun_sliced / baguette_sliced: 手搓（刀）1 → 1（BreadsRecipes）
  knife("gtmfo:cheddar_block", "gtmfo:cheddar_slice", 9);
  knife("gtmfo:gorgonzola_wheel_fully_cured", "gtmfo:gorgonzola_triangular_slice", 16);
  knife("minecraft:bread", "gtmfo:bread_slice", 4);
  knife("gtmfo:bun", "gtmfo:bun_sliced", 1);
  knife("gtmfo:baguette", "gtmfo:baguette_sliced", 1);

  // ===== Create 研磨 =====
  // 数值镜像 GTMFO 研磨机（ChocolateRecipes / CoreChain）：
  //  cocoa_beans_hulled → cocoa_nibs 1 → 1
  //  potato → potato_mashed 1 → 1
  //  apple_candy → apple_candy_crushed 1 → 2
  mill("gtmfo:cocoa_beans_hulled", "gtmfo:cocoa_nibs", 1, 200);
  mill("minecraft:potato", "gtmfo:potato_mashed", 1, 200);
  mill("gtmfo:apple_candy", "gtmfo:apple_candy_crushed", 2, 400);

  // ===== Create 压块 =====
  // 数值镜像 GTMFO 压缩机（CheeseRecipes.aged_cheddar_mold：cheddar_curd_mold → cheddar_aged_mold）
  compact("gtmfo:cheddar_curd_mold", "gtmfo:cheddar_aged_mold", 1);

  // ===== Create 混合（R3 第二批）=====
  // schema 核对：包内 recipes/addMixerRecipes.js + create-1.20.1-6.0.8.jar 自带
  //   data/create/recipes/mixing/chocolate.json（支持 fluid / fluidTag 输入、fluid 输出、heatRequirement）
  // 流体 ID 核对：GTMFO 材料用 GTCEu.id() 注册，故为 gtceu: 命名空间
  //   （证据：开发实例 JEI 导出 H:\tools\jei_names.json 中 gtceu:apple_extract / gtceu:molten_dark_chocolate）
  const mix = (ingredients, results, heated) => {
    const recipe = {
      type: "create:mixing",
      ingredients: ingredients,
      results: results,
    };
    if (heated) recipe.heatRequirement = "heated";
    e.custom(recipe);
  };

  // 面团：镜像 GTCEu 混合器（MiscRecipeLoader.flour_to_dough：2×forge:grain/wheat + 250mB 水 → 3×面团）
  mix(
    [{ tag: "forge:grain/wheat" }, { tag: "forge:grain/wheat" }, { amount: 250, fluid: "minecraft:water" }],
    [{ item: "gtceu:dough", count: 3 }],
    false
  );

  // 苹果汁 / 橙汁：镜像 CoreChain 罐装机（玻璃瓶 + 100mB 提取液 → 果汁）
  mix(
    [{ item: "minecraft:glass_bottle" }, { amount: 100, fluid: "gtceu:apple_extract" }],
    [{ item: "gtmfo:juice_apple", count: 1 }],
    false
  );
  mix(
    [{ item: "minecraft:glass_bottle" }, { amount: 100, fluid: "gtceu:orange_extract" }],
    [{ item: "gtmfo:juice_orange", count: 1 }],
    false
  );

  // 熔融黑巧克力：镜像 ChocolateRecipes.molten_dark_chocolate（糖 + 144mB 可可脂 + 1008mB 无糖巧克力 → 1152mB）
  mix(
    [
      { item: "minecraft:sugar" },
      { amount: 144, fluid: "gtceu:cocoa_butter" },
      { amount: 1008, fluid: "gtceu:molten_unsweetened_chocolate" },
    ],
    [{ amount: 1152, fluid: "gtceu:molten_dark_chocolate" }],
    true
  );

  // 熔融牛奶巧克力：镜像 ChocolateRecipes.molten_milk_chocolate（864mB 黑巧 + 288mB 奶 → 1152mB）
  mix(
    [
      { amount: 864, fluid: "gtceu:molten_dark_chocolate" },
      { amount: 288, fluidTag: "forge:milk" },
    ],
    [{ amount: 1152, fluid: "gtceu:molten_milk_chocolate" }],
    true
  );

  // ===== R3 第三批：Create 压制 + Farm & Charm 绞肉机 =====
  // create:pressing schema 核对：包内 recipes/addPressingRecipes.js（createPressingRecipe）
  const press = (input, output, count) => {
    e.custom({
      type: "create:pressing",
      ingredients: [{ item: input }],
      results: [{ count: count, item: output }],
    });
  };

  // farm_and_charm:mincer schema 核对：包内 addMillingRecipes.js +
  //   letsdo-farm_and_charm-forge-1.0.4.jar 的 data/farm_and_charm/recipes/mincer/*.json
  //   （recipe_type 合法值：MEAT / STONE / METAL / WOOD）
  const mincer = (input, output, count, type) => {
    e.custom({
      type: "farm_and_charm:mincer",
      ingredient: { item: input },
      recipe_type: type,
      result: { count: count, item: output },
    });
  };

  // 平摊面团：镜像 GTMFORecipes.dough_flat（锻锤：GTCEu 面团 → 平摊面团 1→1）
  press("gtceu:dough", "gtmfo:flat_dough", 1);

  // 绞肉：镜像 GTFO 手搓肉末（臼+肉 → 肉末 1→1；肉末即 gtceu:meat_dust，
  //   证据：开发实例 JEI 导出 gtceu:meat_dust = "Mince Meat"）
  mincer("minecraft:beef", "gtceu:meat_dust", 1, "MEAT");
  mincer("minecraft:porkchop", "gtceu:meat_dust", 1, "MEAT");
  mincer("minecraft:chicken", "gtceu:meat_dust", 1, "MEAT");
  mincer("minecraft:mutton", "gtceu:meat_dust", 1, "MEAT");
  mincer("minecraft:rabbit", "gtceu:meat_dust", 1, "MEAT");
  mincer("meadow:raw_buffalo_meat", "gtceu:meat_dust", 1, "MEAT");
});
