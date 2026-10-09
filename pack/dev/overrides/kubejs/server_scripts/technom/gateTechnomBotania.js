// priority: 0
// ============================================================
// 神秘科技（Technomancy）· Botania 选装模块门控
// 设计：把 Technomancy 的 4 台 Botania 机器卡在植物魔法后期（对齐 gateBotania.js）。
//
// 目标：flower_dynamo / mana_fabricator / mana_exchanger / processor_bo 都吃
//       植物魔法材料；把 manasteel_ingot 换成 terrasteel_ingot（泰拉钢 = 植物魔法
//       中期门槛），使其只能在该章节推进后制造。
//
// 依据（源码核对）：
//   - 四台机器配方均含 botania:manasteel_ingot
//     源码：data/technom/recipes/{flower_dynamo,mana_fabricator,
//           mana_exchanger,processor_bo}.json
//   - 缺席安全：无 Botania 时不改写（Platform.isLoaded 门控）。
// ============================================================
console.info("[TECHNOM] gateTechnomBotania.js loaded");

ServerEvents.recipes((e) => {
  if (!Platform.isLoaded("technom") || !Platform.isLoaded("botania")) return;

  ["flower_dynamo", "mana_fabricator", "mana_exchanger", "processor_bo"].forEach((name) => {
    e.replaceInput({ output: "technom:" + name }, "botania:manasteel_ingot", "botania:terrasteel_ingot");
  });
});
