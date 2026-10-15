// priority: 0
// ============================================================
// 星辉魔法 × 农业/采矿稀有物 —— 唤醒祭坛门槛
//
// 目标：唤醒祭坛（attunement_altar，共鸣阶段入口）配方右上角
//       由海蓝宝石换成 society:star_shards（星尘碎片）
//
// 事实依据（JAR 核对，非推测）：
//  - AstralSorcery-1.20.1.0.jar
//      data/astralsorcery/recipes/altar/attunement_altar.json
//      pattern 首行 "A___A"，A = aquamarine（共 2 格）
//      本脚本改为 "A___F"，F = star_shards，保留海蓝宝石 1 格
//  - 星尘碎片来源：矿脉稀有掉落 / 万能晶洞
//      （kubejs/server_scripts/loot/miningLoot.js 2%~6%）
//  - 原配方其余键位（B 大理石/D 水晶/E 星辉金属/C 转继器）
//    与 altar_type/duration/starlight/effects 原样保留
// ============================================================
console.info("[ASTRAL-FARM-GATE] gateAstralFarmBridge.js loaded");

ServerEvents.recipes((e) => {
  if (!Platform.isLoaded("astralsorcery")) return;

  e.remove({ id: "astralsorcery:attunement_altar" });
  e.custom({
    type: "astralsorcery:altar",
    altar_type: 1,
    duration: 200,
    starlight: 1600,
    pattern: [
      "A___F",
      "__D__",
      "_E_E_",
      "_BCB_",
      "B___B",
    ],
    key: {
      A: { item: "astralsorcery:aquamarine" },
      F: { item: "society:star_shards" },
      B: { item: "astralsorcery:marble_runed" },
      C: { item: "astralsorcery:spectral_relay" },
      D: {
        type: "astralsorcery:crystal",
        hasToBeAttuned: false,
        hasToBeCelestial: false,
        canBeAttuned: true,
        canBeCelestialCrystal: true,
      },
      E: { tag: "astralsorcery:starmetal" },
    },
    output: [
      {
        item: "astralsorcery:attunement_altar",
        count: 1,
      },
    ],
    effects: [
      "astralsorcery:pillar_sparkle",
      "astralsorcery:built_in_effect_discovery_central_beam",
      "astralsorcery:altar_default_lightbeams",
      "astralsorcery:altar_default_sparkle",
      "astralsorcery:built_in_effect_attunement_sparkle",
    ],
  }).id("society:astral/attunement_altar_star_shards");
});
