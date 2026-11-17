// priority: 0
// ============================================================
// TC4（神秘时代）× 灾变（L_Enders_Cataclysm）— 纯 datapack/KubeJS 联动
//
// 目标：让灾变 Boss 掉落成为神秘学的可观测、可分解、可再利用的材料。
//  1) 坩埚：焚天锭 → 炼金煤（火/能量 → 炼金燃料）
//  2) 坩埚：虚空碎片 → 平衡碎片（异界/虚空 → 原质）
//  3) 注魔：虚空之眼 + 魔导透镜 → 揭示之护目镜（收容虚空的观测装置）
//
// 事实依据（源码 / JAR 核对，非推测）：
//  - 坩埚 schema：data/thaumcraft/.../recipes/crucible/*.json
//      { type, research?, catalyst, result, aspects }
//  - 注魔 schema：kubejs/server_scripts/tc/tcRecipes.js 内既有写法
//  - 要素键：assets/thaumcraft/textures/aspects/*.png（见同目录 cataclysm.json）
//  - 灾变物品 id：L_Enders_Cataclysm-2.39 jar 的 models/item/*.json 逐一核对
//  - 研究页 recipe_link_policy=COMPLETED_SINGLE 要求恰好 1 个 recipe_id
// ============================================================
console.info("[TC-CATACLYSM] tcCataclysm.js loaded");

ServerEvents.recipes((e) => {
  if (!Platform.isLoaded("thaumcraft") || !Platform.isLoaded("cataclysm")) return;

  // ---- 坩埚：焚天锭 → 炼金煤（研究 CATACLYSM_CRUCIBLE 页面引用此 id）----
  e.custom({
    type: "thaumcraft:crucible",
    research: "CATACLYSM_CRUCIBLE",
    catalyst: { item: "cataclysm:ignitium_ingot" },
    result: { item: "thaumcraft:alumentum", count: 2 },
    aspects: { ignis: 4, potentia: 4, permutatio: 2 },
  }).id("society:cataclysm/ignitium_to_alumentum");

  // ---- 坩埚：虚空碎片 → 平衡碎片 ----
  e.custom({
    type: "thaumcraft:crucible",
    research: "CATACLYSM_CRUCIBLE",
    catalyst: { item: "cataclysm:void_shard" },
    result: { item: "thaumcraft:balanced_shard", count: 2 },
    aspects: { alienis: 4, vacuos: 3, ordo: 2 },
  }).id("society:cataclysm/void_shard_to_balanced");

  // ---- 注魔：虚空之眼 + 魔导透镜 → 揭示之护目镜
  //      （研究 CATACLYSM_INFUSION 页面引用此 id）----
  e.custom({
    type: "thaumcraft:infusion",
    research: "CATACLYSM_INFUSION",
    central: { item: "cataclysm:void_eye" },
    components: [
      { item: "thaumcraft:thaumometer" },
      { item: "cataclysm:ancient_metal_ingot" },
      { item: "thaumcraft:balanced_shard" },
      { item: "minecraft:gold_ingot" },
    ],
    instability: 4,
    aspects: { alienis: 24, sensus: 16, praecantatio: 12, vitium: 8 },
    result: { item: "thaumcraft:goggles_of_revealing" },
  }).id("society:cataclysm/void_lens");
});
