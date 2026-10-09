// priority: 0
// ============================================================
// 神秘科技（Technomancy）· 阶段门控（轻量）
// 设计：Society Sunlit Valley 神秘科技支线（支线组 4A46A5E1358A80A6）
//
// 目标：Technomancy 是「TC4 精华 ↔ 科技能量」的桥梁，卡在 GT 与神秘时代之后。
//       只做入口与仪式材料的轻量门控；核心机器另有 TC4 研究门槛（data/technom/
//       thaumcraft/research、arcane_shaped 的 research 字段），不重复加固。
//
// 依据（源码 / JAR 核对，非推测）：
//   - Technomancy 配方均为标准数据包类型：minecraft:crafting_shaped /
//     thaumcraft:arcane_shaped / crucible / infusion / botania:mana_infusion
//     源码：H:\MinecraftMods\Technomancy-1.20.1\src\main\resources\data\technom\recipes
//   - 物品 ID 以 technom 0.1.0-20732 注册为准（assets/technom/lang/en_us.json）。
//   - 原仪式书 = 书 + 荧石粉 + 黑色染料；五色水晶 = 荧石粉×2 + 染料×2；五催化器
//     = 金块为中心 + 染料 + 材料；存在宝石 = 金粒 + 绿宝石。
//   - replaceInput 用法对齐 kubejs/server_scripts/mek/lockMekBehindGT.js。
// ============================================================
console.info("[TECHNOM] gateTechnom.js loaded");

ServerEvents.recipes((e) => {
  if (!Platform.isLoaded("technom")) return;

  // ---- 入口：仪式书追加 GT 真空管一行（进入神秘科技需要 GT 起步）----
  e.remove({ id: "technom:ritual_tome" });
  e.shaped("technom:ritual_tome", ["RI ", "IS ", " T "], {
    R: "minecraft:book",
    I: "minecraft:glowstone_dust",
    S: "forge:dyes/black",
    T: "gtceu:vacuum_tube",
  }).id("technom:ritual_tome");

  // ---- 五色水晶：荧石粉 -> 神秘锭（仪式材料卡在神秘时代之后）----
  ["light", "dark", "fire", "earth", "water"].forEach((c) => {
    e.replaceInput({ output: "technom:crystal_" + c }, "minecraft:glowstone_dust", "thaumcraft:thaumium_ingot");
  });

  // ---- 五催化器：金块 -> GT 基础电路（对齐 LV 阶段）----
  ["light", "dark", "fire", "earth", "water"].forEach((c) => {
    e.replaceInput({ output: "technom:catalyst_" + c }, "minecraft:gold_block", "gtceu:basic_electronic_circuit");
  });

  // ---- 存在宝石：S3 起点，追加 GT 基础电路 ---- 
  e.remove({ id: "technom:existence_gem" });
  e.shaped("technom:existence_gem", [" N ", "NEN", " C "], {
    N: "minecraft:gold_nugget",
    E: "minecraft:emerald",
    C: "gtceu:basic_electronic_circuit",
  }).id("technom:existence_gem");
});
