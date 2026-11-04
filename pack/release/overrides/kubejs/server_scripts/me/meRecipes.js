// priority: 0
// ============================================================
// 内容：Middle-earth / me（中州）星辉 & 联动
//
// 1) 星光水晶瓶：原为工作台无序配方（#me:glowy + 装水水瓶）。
//    现在改为星辉祭坛合成，材料是暮色森林的冰雪女王战利品。
//    祭坛配方本体在：kubejs/data/society/recipes/altar/starlight_phial.json
//    （altar_type 0 = 发现祭坛；数据包配方保证 JEI / 服务端都能读到）
// 2) 中州的工匠台、合金炉改用 GT LV 电路锁
//    参考 mek/lockMekBehindGT.js，把原输入替换为 LV 电路
// ============================================================
console.info("[ME-INTEGRATION] meRecipes.js loaded");

ServerEvents.recipes((e) => {
  if (!Platform.isLoaded("me")) return;

  // ---- 星光水晶瓶：移除旧的工作台配方，祭坛配方由数据包提供 ----
  if (Platform.isLoaded("astralsorcery")) {
    e.remove({ id: "me:starlight_phial" });
  }

  // ---- 中州工匠台 / 合金炉：GT LV 电路锁 ----
  if (Platform.isLoaded("gtceu")) {
    e.replaceInput({ output: "me:artisan_table" }, "me:tin_ingot", "gtceu:basic_electronic_circuit");
    e.replaceInput({ output: "me:alloy_furnace" }, "minecraft:furnace", "gtceu:basic_electronic_circuit");
  }
});
