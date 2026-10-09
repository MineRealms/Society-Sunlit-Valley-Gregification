// priority: 0
// ============================================================
// 神秘科技（Technomancy）· GT 联动桥
// 设计：以 GT ↔ 源质/能量为主线（对齐 tcGtCompat.js 的写法）。
//
// 目标：
//   1) GT 组装机量产 Technomancy 的核心组件（附魔线圈 / 中子化齿轮 / 量化玻璃），
//      让工厂化生产取代工作台手搓。
//   2) 记录能量语义边界：源质发电机 / 节点发电机输出 FE（可接 GT EU），
//      本文件不伪造 TC4 源质与 GT 流体之间的转换（源质是罐/管道概念）。
//
// 依据（源码 / JAR 核对）：
//   - 附魔线圈 = 红石×2 + 神秘锭；中子化齿轮 = 中子化金属 + 铁锭；量化玻璃 = 玻璃×4
//     源码：data/technom/recipes/enchanted_coil.json / neutronized_gear.json /
//           quantized_glass.json
//   - GT 配方写法对齐 kubejs/server_scripts/tc/tcGtCompat.js（macerator/extractor）。
//   - 能源：essentia_dynamo / node_dynamo 产出 FE；GTCEu 联调见 TC4_INTEGRATION。
// ============================================================
console.info("[TECHNOM] bridgeTechnomGt.js loaded (gt recipes)");

ServerEvents.recipes((e) => {
  if (!Platform.isLoaded("technom") || !Platform.isLoaded("gtceu")) return;

  // ---- 附魔线圈：红石×2 + 神秘锭 ----
  e.recipes.gtceu.assembler("technom:compat/enchanted_coil")
    .itemInputs("2x minecraft:redstone", "#forge:ingots/thaumium")
    .itemOutputs("technom:enchanted_coil")
    .duration(100)
    .EUt(30);

  // ---- 中子化齿轮：中子化金属 + 铁锭 ----
  e.recipes.gtceu.assembler("technom:compat/neutronized_gear")
    .itemInputs("technom:neutronized_metal", "minecraft:iron_ingot")
    .itemOutputs("technom:neutronized_gear")
    .duration(100)
    .EUt(120);

  // ---- 量化玻璃：玻璃×4（对标原奥术配方的 4 出）----
  e.recipes.gtceu.assembler("technom:compat/quantized_glass")
    .itemInputs("4x minecraft:glass")
    .itemOutputs("4x technom:quantized_glass")
    .duration(100)
    .EUt(30);

  // ---- 神秘术士芯（终局）：GT 次世代电路组装（把终局机卡在 GT HV 之后）----
  e.recipes.gtceu.assembler("technom:compat/technoturge_core")
    .itemInputs("technom:energized_wand_core", "gtceu:advanced_electronic_circuit", "#forge:ingots/thaumium")
    .itemOutputs("technom:technoturge_core")
    .duration(200)
    .EUt(480);

  // ---- 反向桥：GT 电解/离心让 Technomancy 纯金属进入 GT 材料体系 ----
  // 纯铜/金/铁的最终中间品（pure_*_5）可被 GT 离心回收为对应粉尘。
  const PURE = [
    ["technom:pure_copper_5", "gtceu:copper_dust"],
    ["technom:pure_gold_5", "gtceu:gold_dust"],
    ["technom:pure_iron_5", "gtceu:iron_dust"],
  ];
  PURE.forEach(([input, dust]) => {
    e.recipes.gtceu.centrifuge("technom:compat/" + input.split(":")[1])
      .itemInputs(input)
      .itemOutputs(dust)
      .duration(200)
      .EUt(30);
  });
});
