// priority: 0
// ============================================================
// 植物魔法（Botania）× 暮色森林 / 神秘时代 阶段锁
//
// 手册流程依据（Botania 内置 Patchouli 手册 Lexicon 的 advancement 解锁链，
// 证据：assets/botania/patchouli_books/lexicon/en_us/entries/**）：
//   白雏菊 pure_daisy → mana（魔力散布器/魔力池）→ runic_altar（符文祭坛）
//   → terrasteel（泰拉钢）→ alfhomancy（精灵门）→ gaia_ritual（盖亚仪式）
//
// 阶段锁设计：
//   ① 进入暮色森林 → 魔力散布器 / 魔力池 需要 twilightforest:torchberries
//      （火把浆果：暮色森林火把浆果植株掉落，无剪刀也可获得）
//   ② 击败巫妖王   → 符文祭坛 需要 twilightforest:lich_trophy
//      （泰拉钢 / 精灵门 / 盖亚仪式由符文祭坛 + 泰拉钢自然卡住，无需额外锁）
//   ③ 神秘出虚空锭 → 泰拉钢锭 需要 thaumcraft:void_ingot
//      （TC4 研究 VOIDMETAL：parents = THAUMIUM + ELDRITCHMINOR，属中后期；
//        虚空锭坩埚配方 = 虚空种子 + metallum 8，虚空种子可再生）
// ============================================================
console.info("[SOCIETY] gateBotania.js loaded");

ServerEvents.recipes((e) => {
  if (!Platform.isLoaded("botania")) return;

  const TF_BERRY = "twilightforest:torchberries";
  const LICH_TROPHY = "twilightforest:lich_trophy";
  const VOID_INGOT = "thaumcraft:void_ingot";

  // ---------- ① 进入暮色森林：解锁魔力体系 ----------
  // 原配方为 botania:gog_alternation 类型（含 Garden of Glass 变体），移除后重写
  e.remove({ id: "botania:mana_spreader" });
  e.shaped("botania:mana_spreader", ["WWW", "CPB", "WWW"], {
    W: "#botania:livingwood_logs",
    C: "minecraft:copper_ingot",
    P: "#botania:petals",
    B: TF_BERRY,
  });

  e.remove({ id: "botania:mana_pool" });
  e.shaped("botania:mana_pool", ["R R", "RRR", " B "], {
    R: "botania:livingrock",
    B: TF_BERRY,
  });

  // ---------- ② 击败巫妖王：解锁符文祭坛（后续泰拉钢/精灵门/盖亚随之解锁） ----------
  e.remove({ id: "botania:runic_altar" });
  e.shaped("botania:runic_altar", ["SSS", "SPS", " T "], {
    S: "botania:livingrock",
    P: "botania:mana_pearl",
    T: LICH_TROPHY,
  });

  // ---------- ③ 神秘时代虚空锭：泰拉钢锭 ----------
  e.remove({ id: "botania:terra_plate/terrasteel_ingot" });
  e.custom({
    type: "botania:terra_plate",
    ingredients: [
      { item: "botania:manasteel_ingot" },
      { item: "botania:mana_pearl" },
      { item: "botania:mana_diamond" },
      { item: VOID_INGOT },
    ],
    mana: 500000,
    result: { item: "botania:terrasteel_ingot" },
  });
});
