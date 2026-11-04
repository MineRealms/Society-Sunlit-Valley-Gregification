// priority: 0
// ============================================================
// 魔法材料 × GT — 研磨/预处理联动（2026-11-03）
//
// 设计原则（对齐 gateBotania.js / tcGtCompat.js）：GT 做物理预处理，
// 魔法核心循环（魔力/星光/源质）不被绕过。
//
// 事实依据（JAR 核对，非推测）：
//  - gtceu:wood_dust（lang: Wood Pulp）/ gtceu:talc_dust（lang: Talc）存在
//    （gtceu-1.20.1-7.5.3.jar assets/gtceu/lang/en_us.json 逐 key 核对；
//      GTCEu 无 stone_dust / marble_dust，GT 化学里大理石=滑石 talc）
//  - botania:livingrock / livingwood：纯华蓑菊（pure_daisy）可再生，
//    gateBotania.js 已把魔力体系锁在暮色火把浆果之后
//  - astralsorcery:marble_raw：AS 自带 data/forge/tags/blocks/marble.json，
//    大理石生成已在包内（forge/biome_modifier/marble.json）
//  - 数值沿用包内先例 tcGtCompat.js（macerator 矿石级 EUt 2 / duration 400）
// ============================================================
console.info("[MAGIC-GT] gtMagicBridge.js loaded");

ServerEvents.recipes((e) => {
  if (!Platform.isLoaded("gtceu")) return;

  // ---- 活石 → 滑石粉（纯华蓑菊可再生的 GT 滑石来源，化学/脱硫用）----
  e.recipes.gtceu.macerator("magic:compat/livingrock_to_talc")
    .itemInputs("botania:livingrock")
    .itemOutputs("gtceu:talc_dust")
    .duration(400)
    .EUt(2, 1);

  // ---- 活木 → 木浆（可再生的造纸/化学木浆来源）----
  e.recipes.gtceu.macerator("magic:compat/livingwood_to_pulp")
    .itemInputs("botania:livingwood")
    .itemOutputs("2x gtceu:wood_dust")
    .duration(200)
    .EUt(2, 1);

  // ---- 星辉大理石 → 滑石粉 ×2（大理石在 GT 化学里就是滑石）----
  e.recipes.gtceu.macerator("magic:compat/as_marble_to_talc")
    .itemInputs("astralsorcery:marble_raw")
    .itemOutputs("2x gtceu:talc_dust")
    .duration(400)
    .EUt(2, 1);

  // ---- 星辉金属锭回收：碎成铁粉 ×1 ----
  // 产量核对：starmetal_ore 熔炉/高炉 → 1 锭（astralsorcery smelting/blasting）。
  // 回收只给 1 铁粉（=1 锭当量再亏掉星光投入），绝不能给 2，否则成了刷铁机。
  e.recipes.gtceu.macerator("magic:compat/starmetal_recycle")
    .itemInputs("astralsorcery:starmetal_ingot")
    .itemOutputs("1x gtceu:iron_dust")
    .duration(400)
    .EUt(2, 1);
});
