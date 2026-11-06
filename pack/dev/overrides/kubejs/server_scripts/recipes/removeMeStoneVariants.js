// 中洲 (Middle-earth) 为每种石头批量生成 17 个 2x2 单材料配方，
// 输入全是 minecraft:stone、输出却各不相同 -> 互相冲突，JEI 里刷出 26 页。
// 这里只清掉 minecraft:stone 这一族；10 个 me: 变体都有 stonecutting 替代，删掉不卡进度。
// 顺带补回被 ME 的 data/minecraft/recipes/ 顶掉的两个原版熔炼配方。
console.info("[SOCIETY] removeMeStoneVariants.js loaded");

ServerEvents.recipes((e) => {
  let ids = [
    "minecraft:stone",
    "minecraft:cobblestone",
    "minecraft:mossy_cobblestone",
    "minecraft:smooth_stone",
    "minecraft:mossy_stone_bricks",
    "minecraft:cracked_stone_bricks",
    "me:polished_stone",
    "me:cracked_polished_stone",
    "me:mossy_polished_stone",
    "me:cracked_smooth_stone",
    "me:mossy_smooth_stone",
    "me:stone_tiles",
    "me:cracked_stone_tiles",
    "me:mossy_stone_tiles",
    "me:old_stone",
    "me:stone_brickwork"
  ];
  ids.forEach((id) => e.remove({ id: id }));

  e.smelting("minecraft:smooth_stone", "minecraft:stone")
    .xp(0.1)
    .id("minecraft:smooth_stone");
  e.smelting("minecraft:cracked_stone_bricks", "minecraft:stone_bricks")
    .xp(0.1)
    .id("minecraft:cracked_stone_bricks");
});
