// priority: 0
// ============================================================
// TC4（神秘时代）× Sunlit Valley — TC4 特色配方（KubeJS 自定义）
// 进度文档：TC4_INTEGRATION.md 第 7.4 节
//
// 目标：用 GT / Create 材料走 TC4 路线（坩埚 / 注魔）
//
// 事实依据（源码 / JAR 核对，非推测）：
//  - TC4 配方 JSON 结构：type=thaumcraft:crucible / thaumcraft:infusion
//    （证据：数据包 data/thaumcraft/recipes/*.json）
//  - 研究键：THAUMIUM（thaumium_ingot.json）/ ALUMENTUM（alumentum.json）/
//    GOGGLES（goggles_of_revealing.json）
//  - 要素名：metallum/permutatio/praecantatio/ignis/potentia/sensus/auram/machina
//    （证据：object_aspects/definitions.json 使用中的键）
//  - 物品 ID：create:precision_mechanism（Create）；gtceu:basic_electronic_circuit /
//    gtceu:coke_dust（jei_names.json）；thaumcraft:thaumometer /
//    thaumcraft:goggles_of_revealing / thaumcraft:balanced_shard（TC4 配方引用）
// ============================================================
console.info("[TC4-INTEGRATION] tcRecipes.js loaded (thaumcraft recipes)");

ServerEvents.recipes((e) => {
  if (!Platform.isLoaded("thaumcraft")) return;

  // 坩埚：GT 辰砂粉 → 神秘水银（GT 水银路线接入炼金）
  e.custom({
    type: "thaumcraft:crucible",
    catalyst: { item: "gtceu:cinnabar_dust" },
    result: { item: "thaumcraft:quicksilver" },
    aspects: { metallum: 2, permutatio: 2 },
  }).id("tc4:compat/quicksilver_from_cinnabar_dust");

  // 坩埚：GT 钢锭 → 神秘锭（镜像铁锭路线，研究 THAUMIUM）
  e.custom({
    type: "thaumcraft:crucible",
    research: "THAUMIUM",
    catalyst: { item: "gtceu:steel_ingot" },
    result: { item: "thaumcraft:thaumium_ingot" },
    aspects: { praecantatio: 4 },
  }).id("tc4:compat/thaumium_from_steel");

  // 坩埚：GT 焦炭粉 → 炼金煤（研究 ALUMENTUM）
  e.custom({
    type: "thaumcraft:crucible",
    research: "ALUMENTUM",
    catalyst: { item: "gtceu:coke_dust" },
    result: { item: "thaumcraft:alumentum" },
    aspects: { potentia: 2, ignis: 2 },
  }).id("tc4:compat/alumentum_from_coke_dust");

  // 注魔：机械魔法护目镜（Create 精密构件 + GT LV 电路 + 魔导透镜），研究 GOGGLES
  e.custom({
    type: "thaumcraft:infusion",
    research: "GOGGLES",
    central: { item: "thaumcraft:thaumometer" },
    components: [
      { item: "create:precision_mechanism" },
      { item: "gtceu:basic_electronic_circuit" },
      { item: "thaumcraft:balanced_shard" },
      { item: "minecraft:gold_ingot" },
    ],
    instability: 2,
    aspects: { sensus: 16, auram: 8, machina: 16 },
    result: { item: "thaumcraft:goggles_of_revealing" },
  }).id("tc4:compat/goggles_magitech");
});
