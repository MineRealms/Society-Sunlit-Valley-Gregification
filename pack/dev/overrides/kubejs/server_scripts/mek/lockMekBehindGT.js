// priority: 0
// ============================================================
// GT × MEK 科技锁（MEK 基础机器）
// 进度文档：GT_INTEGRATION.md 第 6.4 节 / STATUS.md 3.1
//
// 目标：
//   1) MEK 基础机器必须用 GT LV 电路（微处理器）合成
//      —— gtceu:microchip_processor 只有「电路组装机」配方
//         （GTCEu 源码 CircuitRecipes.java:1095，无工作台版）
//      → 玩家必须先完成 LV 电路组装机阶段才能入门 MEK
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
//  - 物品 ID：gtceu:microchip_processor（GTItems.java:1688，MICROPROCESSOR_LV）
//    / create:precision_mechanism（Create）
//  - 进阶机器（锇压缩机等）经灌注机链（合金/高级电路）与钢外壳自然被门槛住
// ============================================================
console.info("[GT-MEK-LOCK] lockMekBehindGT.js loaded");

ServerEvents.recipes((e) => {
  // ---- 入门机器：冶金灌注机（熔炉 ×2 → LV 微处理器 ×2）----
  e.replaceInput({ output: "mekanism:metallurgic_infuser" }, "minecraft:furnace", "gtceu:microchip_processor");

  // ---- 4 台基础机器：MEK 基础控制电路 → LV 微处理器 ×2 ----
  const BASIC_MACHINES = [
    "mekanism:enrichment_chamber",
    "mekanism:crusher",
    "mekanism:energized_smelter",
    "mekanism:precision_sawmill",
  ];
  BASIC_MACHINES.forEach((id) => {
    e.replaceInput({ output: id }, "#forge:circuits/basic", "gtceu:microchip_processor");
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
  // GT 电路阶段（gtceu-1.20.1-7.5.3.jar lang tooltip 逐条核对）：
  //   microchip_processor=LV / good_electronic_circuit=MV /
  //   advanced_integrated_circuit=HV / micro_processor_computer=EV
  // 方法：把配方内的“电路”输入替换为对应阶段的 GT 电路
  //（三个电路均为原版合成台配方，replaceInput 有效；
  //  合金/富集材料为灌注机内部配方（自定义类型），无法用 replaceInput 限制）
  // 配套任务书双锁：GT 章「首个中压电路!」0DBC148D92A9F69F /
  //   「首批高压电路!」26394C1290D70AB6 / 「首款极端电压电路!」4AFD3073C731A1E4
  // ============================================================
  e.replaceInput({ output: "mekanism:advanced_control_circuit" }, "#forge:circuits/basic", "gtceu:good_electronic_circuit");
  e.replaceInput({ output: "mekanism:elite_control_circuit" }, "#forge:circuits/advanced", "gtceu:advanced_integrated_circuit");
  e.replaceInput({ output: "mekanism:ultimate_control_circuit" }, "#forge:circuits/elite", "gtceu:micro_processor_computer");
});
