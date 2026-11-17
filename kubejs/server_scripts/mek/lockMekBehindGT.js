// priority: 0
// ============================================================
// GT × MEK 科技锁（MEK 基础机器）
// 进度文档：GT_INTEGRATION.md 第 6.4 节 / STATUS.md 3.1
//
// 目标：
//   1) MEK 基础机器使用 #gtceu:circuits/lv，接受该等级标签内的任意电路
//   2) 4 台基础机器同时需要 Create 精密构件（create:precision_mechanism）
//   3) 电路阶段锁（2026-09-22）：高级电路=GT MV 电路、精英电路=GT HV 电路、
//      终极电路=GT EV 电路（基础=LV，见 1））
//
// 事实依据（源码 / JAR 核对，非推测）：
//  - 配方来源：mods/Mekanism-1.20.1-10.4.16.80.jar
//      data/mekanism/recipes/metallurgic_infuser.json   （熔炉×2）
//      data/mekanism/recipes/enrichment_chamber.json    （#forge:circuits/basic×2 + 铁锭×2）
//      data/mekanism/recipes/crusher.json               （#forge:circuits/basic×2 + 熔岩桶×2）
//      data/mekanism/recipes/energized_smelter.json     （#forge:circuits/basic×2 + 硅玻璃×2）
//      data/mekanism/recipes/precision_sawmill.json     （#forge:circuits/basic×2 + 灌注合金×2）
//  - 电路等级：GTCEu 7.5.3 的 gtceu:circuits/<tier> 标签；不限定技术路线
//  - 进阶机器（锇压缩机等）经灌注机链（合金/高级电路）与钢外壳自然被门槛住
// ============================================================
console.info("[GT-MEK-LOCK] lockMekBehindGT.js loaded");

ServerEvents.recipes((e) => {
  // ---- 入门机器：冶金灌注机（熔炉 ×2 → LV 电路 ×2）----
  e.replaceInput({ output: "mekanism:metallurgic_infuser" }, "minecraft:furnace", "#gtceu:circuits/lv");

  // ---- 4 台基础机器：MEK 基础控制电路 → LV 电路 ×2 ----
  const BASIC_MACHINES = [
    "mekanism:enrichment_chamber",
    "mekanism:crusher",
    "mekanism:energized_smelter",
    "mekanism:precision_sawmill",
  ];
  BASIC_MACHINES.forEach((id) => {
    e.replaceInput({ output: id }, "#forge:circuits/basic", "#gtceu:circuits/lv");
  });

  // ---- Create 精密构件（每台 ×2）----
  e.replaceInput({ output: "mekanism:enrichment_chamber" }, "#forge:ingots/iron", "create:precision_mechanism");
  e.replaceInput({ output: "mekanism:crusher" }, "minecraft:lava_bucket", "create:precision_mechanism");
  e.replaceInput({ output: "mekanism:energized_smelter" }, "#forge:glass/silica", "create:precision_mechanism");
  e.replaceInput({ output: "mekanism:precision_sawmill" }, "#mekanism:alloys/infused", "create:precision_mechanism");

  // ============================================================
  // 电路阶段锁（2026-09-22 用户指定）：
  //   MEK 基础电路 = LV（已由上面的灌注机锁实现）
  //   → 高级电路 = MV → 精英电路 = HV → 终极电路 = EV
  //
  // 事实依据（mods/Mekanism-1.20.1-10.4.16.80.jar
  //          data/mekanism/recipes/control_circuit/{advanced,elite,ultimate}.json）：
  //   advanced: crafting_shaped ["ACA"]  A=#mekanism:alloys/infused     C=#forge:circuits/basic
  //   elite   : crafting_shaped ["ACA"]  A=#mekanism:alloys/reinforced  C=#forge:circuits/advanced
  //   ultimate: crafting_shaped ["ACA"]  A=#mekanism:alloys/atomic      C=#forge:circuits/elite
  // 把配方内的“电路”输入替换为对应阶段的标签，允许同档电子、集成与魔法电路互换。
  //（三个电路均为原版合成台配方，replaceInput 有效；
  //  合金/富集材料为灌注机内部配方（自定义类型），无法用 replaceInput 限制）
  // 配套任务书双锁：GT 章「首个中压电路!」0DBC148D92A9F69F /
  //   「首批高压电路!」26394C1290D70AB6 / 「首款极端电压电路!」4AFD3073C731A1E4
  // ============================================================
  e.replaceInput({ output: "mekanism:advanced_control_circuit" }, "#forge:circuits/basic", "#gtceu:circuits/mv");
  e.replaceInput({ output: "mekanism:elite_control_circuit" }, "#forge:circuits/advanced", "#gtceu:circuits/hv");
  e.replaceInput({ output: "mekanism:ultimate_control_circuit" }, "#forge:circuits/elite", "#gtceu:circuits/ev");

  // ============================================================
  // 深度融合补锁（2026-11-03，方案 A–D，经配方逐条核对）
  // ============================================================

  // ---- A. 数字矿机：GT EV + Create 精密构件 ----
  // 原配方 ["ACA","SRS","TXT"] 只用 1 个 #forge:circuits/basic（LV 档），
  // LV 一过就能掏整块区块，绕过 GT 矿脉与矿石处理线。重做配方：
  // 电路升为 EV 标签；撤掉便宜的物流分拣器，换入 2 个精密构件。
  e.remove({ output: "mekanism:digital_miner" });
  e.recipes.minecraft.crafting_shaped("mekanism:digital_miner",
    ["ACA", "MRM", "TXT"],
    { A: "#mekanism:alloys/atomic",
      C: "#gtceu:circuits/ev",
      M: "create:precision_mechanism",
      R: "mekanism:robit",
      T: "mekanism:teleportation_core",
      X: "mekanism:steel_casing" });

  // ---- B1. 钢外壳：居中锇锭 → GT MV 电路 ----
  // 6.4 节推荐方案第 1 处（此前未实施）：钢外壳是所有中后期 MEK 机器的底盘。
  e.replaceInput({ output: "mekanism:steel_casing" }, "#forge:ingots/osmium", "#gtceu:circuits/mv");

  // ---- B2. MEK 钢锭必须走 GT 电力高炉 ----
  // MEK 钢尘 = 铁尘+碳（灌注机）本来普通熔炉就能烧成钢锭，绕过 GT EBF。
  // 撤掉熔炉/高炉两条路（输入是 #forge:dusts/steel 标签，只影响产出 mekanism:ingot_steel 的两条），
  // 另给 EBF 加专属配方。GT 自己的 gtceu:steel_ingot 不受影响。
  e.remove({ output: "mekanism:ingot_steel", type: "minecraft:smelting" });
  e.remove({ output: "mekanism:ingot_steel", type: "minecraft:blasting" });
  e.recipes.gtceu.electric_blast_furnace("kubejs:mek_steel_ingot_ebf")
    .itemInputs("mekanism:dust_steel")
    .itemOutputs("mekanism:ingot_steel")
    .blastFurnaceTemp(1000)
    .duration(800)
    .EUt(120);

  // ---- C. 工厂税：四级工厂的金属锭位 → Create 精密构件（各 ×2）----
  // 36 台工厂配方核对：basic I=铁锭 / advanced I=锇锭 / elite I=金锭 / ultimate I=钻石，均出现 2 次。
  const FACTORY_TIERS = [
    ["basic", "#forge:ingots/iron"],
    ["advanced", "#forge:ingots/osmium"],
    ["elite", "#forge:ingots/gold"],
    ["ultimate", "#forge:gems/diamond"],
  ];
  const FACTORY_KINDS = [
    "combining", "compressing", "crushing", "enriching", "infusing",
    "injecting", "purifying", "sawing", "smelting",
  ];
  FACTORY_TIERS.forEach(([tier, ing]) => {
    FACTORY_KINDS.forEach((kind) => {
      const recipeId = "mekanism:factory/" + tier + "/" + kind;
      e.forEachRecipe({ id: recipeId }, (recipe) => {
        const factory = JSON.parse(recipe.json.toString());
        factory.key.I = { item: "create:precision_mechanism" };
        e.remove({ id: recipeId });
        e.custom(factory).id(recipeId);
      });
    });
    e.replaceInput({ output: "mekanism:" + tier + "_tier_installer" }, ing, "create:precision_mechanism");
  });

  // ---- D. 发电税 ----
  // 燃气发电机：灌注合金×4 → GT MV 电路×4（原配方无电路）
  e.replaceInput({ output: "mekanismgenerators:gas_burning_generator" }, "#mekanism:alloys/infused", "#gtceu:circuits/mv");
  // 风力的 mek_data 不响应 replaceInput；保留原 serializer 和电量继承。
  e.forEachRecipe({ id: "mekanismgenerators:generator/wind" }, (recipe) => {
    const wind = JSON.parse(recipe.json.toString());
    wind.key.C = { tag: "gtceu:circuits/mv" };
    e.remove({ id: "mekanismgenerators:generator/wind" });
    e.custom(wind).id("mekanismgenerators:generator/wind");
  });
  // 生物发电机：基础电路 → GT MV 电路
  e.replaceInput({ output: "mekanismgenerators:bio_generator" }, "#forge:circuits/basic", "#gtceu:circuits/mv");
  // 太阳能 / 高级太阳能：灌注合金×2 → GT MV 电路×2
  e.replaceInput({ output: "mekanismgenerators:solar_generator" }, "#mekanism:alloys/infused", "#gtceu:circuits/mv");
  e.replaceInput({ output: "mekanismgenerators:advanced_solar_generator" }, "#mekanism:alloys/infused", "#gtceu:circuits/mv");
  // 加热发电机：熔炉 → GT LV 电路（镜像灌注机锁）
  e.replaceInput({ output: "mekanismgenerators:heat_generator" }, "minecraft:furnace", "#gtceu:circuits/lv");
  // 电解分离器：铁锭×4 → Create 精密构件×4（水电解开局税）
  e.replaceInput({ output: "mekanism:electrolytic_separator" }, "#forge:ingots/iron", "create:precision_mechanism");

  // ---- E. 核能阶段 ----
  // EV: all four reactor parts require a circuit in the EV tier tag.
  e.replaceInput({ output: "mekanismgenerators:fission_reactor_casing" }, "mekanism:steel_casing", "#gtceu:circuits/ev");
  e.replaceInput({ output: "mekanismgenerators:fission_fuel_assembly" }, "mekanism:basic_chemical_tank", "#gtceu:circuits/ev");
  e.replaceInput({ output: "mekanismgenerators:control_rod_assembly" }, "#forge:circuits/elite", "#gtceu:circuits/ev");
  e.replaceInput({ output: "mekanismgenerators:fission_reactor_port" }, "#forge:circuits/elite", "#gtceu:circuits/ev");

  // UF6 keeps its 1:1 gas/fluid ratio. One fragment oxidizes into 2000 mB
  // fissile gas, so the EV centrifuge preserves the original fuel yield.
  e.remove({ id: "mekanism:processing/uranium/fissile_fuel" });
  // Unified UF6 tags match both recipes. Explicit modes keep GT separation
  // and Mekanism fuel production selectable in the same centrifuge.
  e.remove({ id: "gtceu:centrifuge/uranium_hexafluoride_separation" });
  e.recipes.gtceu.centrifuge("gtceu:uranium_hexafluoride_separation")
    .circuit(1)
    .inputFluids("#forge:uranium_hexafluoride 1000")
    .outputFluids(
      Fluid.of("gtceu:enriched_uranium_hexafluoride", 100),
      Fluid.of("gtceu:depleted_uranium_hexafluoride", 900)
    )
    .duration(160)
    .EUt(480);
  e.recipes.gtceu.centrifuge("society:mek/fissile_fuel_feedstock")
    .circuit(2)
    .inputFluids("#forge:uranium_hexafluoride 2000")
    .itemOutputs("mekanism:reprocessed_fissile_fragment")
    .duration(2000)
    .EUt(2048);

  // LuV: the reactor controller and ports are the construction gate. The
  // existing Mekanism injection route remains useful at the low capped rate.
  e.replaceInput({ output: "mekanismgenerators:fusion_reactor_controller" }, "#forge:circuits/ultimate", "#gtceu:circuits/luv");
  e.replaceInput({ output: "mekanismgenerators:fusion_reactor_port" }, "#forge:circuits/ultimate", "#gtceu:circuits/luv");

  // LuV ignition needs one full Hohlraum before separate D/T injection works.
  // Fill the item instead of unlocking the cheap bulk gas-mixing recipe.
  e.recipes.gtceu.chemical_reactor("society:mek/hohlraum_ignition")
    .itemInputs("mekanismgenerators:hohlraum")
    .inputFluids(
      Fluid.of("mekanismgenerators:deuterium", 5),
      Fluid.of("mekanismgenerators:tritium", 5)
    )
    .itemOutputs(Item.of("mekanismgenerators:hohlraum",
      '{mekData:{GasTanks:[{Tank:0b,stored:{amount:10L,gasName:"mekanismgenerators:fusion_fuel"}}]}}'))
    .duration(2000)
    .EUt(32768);

  // ZPM: remove the free chemical-infusion route. GT converts liquid D and T
  // into liquid fusion fuel; Mekanism's Rotary Condensentrator turns it back
  // into gas for the reactor.
  e.remove({ id: "mekanismgenerators:chemical_infusing/fusion_fuel" });
  e.recipes.gtceu.chemical_reactor("society:mek/fusion_fuel_direct_dt")
    .inputFluids(
      Fluid.of("mekanismgenerators:deuterium", 1000),
      Fluid.of("mekanismgenerators:tritium", 1000)
    )
    .outputFluids(Fluid.of("mekanismgenerators:fusion_fuel", 2000))
    .duration(1000)
    .EUt(131072);

  // SPS now uses the researched assembly-line routes in industry/gtTiangongProgression.js.

  // ---- F. HXTG machine recipes retain their parts and Thaumcraft research,
  // with a GT circuit tier tag as a real recipe input at each voltage step. ----
  // HXTG controller recipes are overridden by their stable data-pack IDs in
  // kubejs/data/zmod/recipes; the Tian Gong serializer retains these IDs.
});
