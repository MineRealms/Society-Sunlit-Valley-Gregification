// priority: 0
// ============================================================
// 神秘科技（Technomancy）· 标签统一
// 设计：把 Technomancy 的材料并入通用 forge 标签，便于 GT/Mek/自动化配方通用化。
//
// 依据（源码核对）：
//   - 它自带的 processable/tools 标签见 data/technom/tags/items/**，已含
//     #forge:ores/* 与 #forge:raw_materials/*，无需重复。
//   - 这里只补它未提供、但其它模组常按标签查找的齿轮/锭标签。
// ============================================================
console.info("[TECHNOM] technomTags.js loaded");

ServerEvents.tags("item", (e) => {
  if (!Platform.isLoaded("technom")) return;

  // 中子化金属 / 齿轮：给自动化与通用齿轮配方一个稳定标签
  e.add("forge:ingots/neutronized", "technom:neutronized_metal");
  e.add("forge:gears/neutronized", "technom:neutronized_gear");

  // 植物魔法钢齿轮（选装，缺席安全由 Botania 物品存在与否决定）
  e.add("forge:gears/manasteel", "technom:manasteel_gear");
});
