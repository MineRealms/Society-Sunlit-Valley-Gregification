// priority: 0
// ============================================================
// GT × Create 轻量联动（R2）：Create 机器处理 GT 前期材料（ULV~LV）
// 进度文档：GT_INTEGRATION.md「5. Create × GT 轻量联动」
//
// 只加配方，不动物品/标签；所有数值镜像 GTCEu 7.5.x 官方配方
//
// 数值/结构出处（逐条核对，非推测）：
//  - 板材（Create 压床/压合）：
//      弯曲机 1 锭 → 1 板（EUt24）/ 锻造锤 3 锭 → 2 板（EUt16）
//      → data/recipe/generated/MaterialRecipeHandler.java:390-401
//  - 覆膜电路板：2×粘性树脂 + 1×木板 → 1×resin_circuit_board（无序合成 1x 版）
//      → data/recipe/misc/CircuitRecipes.java:770-778（COATED_BOARD）
//  - 原矿→碎矿：研磨机 raw→crushed ×2（+14% 副产）/ 锻造锤 ×1
//      → data/recipe/generated/OreRecipeHandler.java:180-203
//  - 合金（Create 混合 = GT 混合器 ULV）：
//      红合金 1铜粉+4红石粉→1 / 黄铜 3铜粉+1锌粉→4 / 青铜 3铜粉+1锡粉→4
//      金银合金 1金粉+1银粉→2 / 殷钢 2铁粉+1镍粉→3
//      → data/recipe/serialized/chemistry/MixerRecipes.java:143-206,223-228
//  - 橡胶（Create 混合 · 加热 = GT 合金炉 vulcanize）：
//      1 硫粉 + 3 生橡胶粉 → 1 橡胶锭（MachineRecipeLoader.java:423-424）
//      → 用 Society 已加工橡胶 1:1 替代 3 生橡胶粉
//  - 物品 ID：GT 侧全部来自包内 JEI 导出 H:\tools\jei_names.json；
//      Society 侧 society:rubber 来自包内 KubeJS 注册物品（quests/机器定义均引用）
//  - 配方 schema：create:compacting/milling/crushing/mixing
//      见 create-1.20.1-6.0.8.jar 自带 data/create/recipes/* 与包内
//      kubejs/server_scripts/recipes/addGtmfoRecipes.js、addPressingRecipes.js
// ============================================================
console.info("[GT-CREATE-BRIDGE] createBridges.js loaded");

ServerEvents.recipes((e) => {
  // ---------- 1) Create 压合（压床+盆）：GT 锭 → GT 板 ----------
  // 名单刻意避开 Create 自带压片（铁/铜/金/黄铜 → create:*_sheet）防止配方冲突
  const plates = [
    ["minecraft:iron_ingot", "gtceu:iron_plate"],
    ["minecraft:copper_ingot", "gtceu:copper_plate"],
    ["minecraft:gold_ingot", "gtceu:gold_plate"],
    ["gtceu:tin_ingot", "gtceu:tin_plate"],
    ["gtceu:steel_ingot", "gtceu:steel_plate"],
    ["gtceu:bronze_ingot", "gtceu:bronze_plate"],
    ["gtceu:brass_ingot", "gtceu:brass_plate"],
    ["gtceu:lead_ingot", "gtceu:lead_plate"],
    ["gtceu:silver_ingot", "gtceu:silver_plate"],
    ["gtceu:zinc_ingot", "gtceu:zinc_plate"],
    ["gtceu:nickel_ingot", "gtceu:nickel_plate"],
    ["gtceu:electrum_ingot", "gtceu:electrum_plate"],
    ["gtceu:wrought_iron_ingot", "gtceu:wrought_iron_plate"],
  ];
  plates.forEach(([input, output]) => {
    e.custom({
      type: "create:compacting",
      ingredients: [{ item: input }],
      results: [{ item: output }],
    });
  });

  // ---------- 2) Create 压合：粘性树脂 + 木板 → GT 覆膜电路板 ----------
  // 镜像无序合成 1x：2 树脂 + 1 木板 → 1
  e.custom({
    type: "create:compacting",
    ingredients: [{ item: "gtceu:wood_plate" }, { item: "gtceu:sticky_resin" }, { item: "gtceu:sticky_resin" }],
    results: [{ item: "gtceu:resin_circuit_board" }],
  });

  // ---------- 3) Create 粉碎轮：GT 原矿 → GT 碎矿（×2，镜像研磨机）----------
  // 输入用 forge 标签以兼容任意模组的同类原矿；锌无 GT 碎矿（JEI 核对）故不含
  const ores = ["tin", "iron", "copper", "gold", "coal", "nickel", "lead", "silver", "redstone"];
  ores.forEach((m) => {
    e.custom({
      type: "create:crushing",
      ingredients: [{ tag: "forge:raw_materials/" + m }],
      processingTime: 200,
      results: [{ count: 2, item: "gtceu:crushed_" + m + "_ore" }],
    });
  });

  // ---------- 4) Create 混合：GT 合金粉尘（镜像 GT 混合器 ULV）----------
  // 备注：GT 原本就有无序合成（3铜+1锌→3黄铜粉），此处为动力批量版（同 GT 混合器 4 粉）
  const alloy = (inputs, output, count) => {
    e.custom({
      type: "create:mixing",
      ingredients: inputs.map((t) => ({ tag: t })),
      results: [{ count: count, item: output }],
    });
  };
  alloy(["forge:dusts/copper", "forge:dusts/redstone", "forge:dusts/redstone", "forge:dusts/redstone", "forge:dusts/redstone"], "gtceu:red_alloy_dust", 1);
  alloy(["forge:dusts/copper", "forge:dusts/copper", "forge:dusts/copper", "forge:dusts/zinc"], "gtceu:brass_dust", 4);
  alloy(["forge:dusts/copper", "forge:dusts/copper", "forge:dusts/copper", "forge:dusts/tin"], "gtceu:bronze_dust", 4);
  alloy(["forge:dusts/gold", "forge:dusts/silver"], "gtceu:electrum_dust", 2);
  alloy(["forge:dusts/iron", "forge:dusts/iron", "forge:dusts/nickel"], "gtceu:invar_dust", 3);

  // ---------- 5) Create 混合（加热）：Society 橡胶 → GT 橡胶锭 ----------
  // 镜像 GT 合金炉：1 硫粉 + 3 生橡胶粉 → 1 橡胶锭
  e.custom({
    type: "create:mixing",
    heatRequirement: "heated",
    ingredients: [{ item: "society:rubber" }, { tag: "forge:dusts/sulfur" }],
    results: [{ item: "gtceu:rubber_ingot" }],
  });
});
