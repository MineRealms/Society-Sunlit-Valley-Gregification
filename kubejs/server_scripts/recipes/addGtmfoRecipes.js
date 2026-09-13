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
});
