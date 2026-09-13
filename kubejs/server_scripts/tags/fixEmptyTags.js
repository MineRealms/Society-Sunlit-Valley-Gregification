// fixEmptyTags.js — 修复"整合包移除物品后遗留的空标签"（2026-09-14）
// 背景：globalRemovedItems.js + handleItemBlockFluidTags.js 用 removeAllTagsFrom 把物品从所有标签移除，
// 有些标签因此变空，但引用它的配方仍在 → 配方失效（JEI 显示 Empty Tag）。
// 这里只把"整合包实际在用的替代品"加回对应标签，不添加任何新物品。
// 判定依据与完整清单见 GTMFO_INTEGRATION.md 第 13 节。

ServerEvents.tags("item", (e) => {
  // 1) forge:flour/wheat
  // 原唯一成员 create:wheat_flour 被移除；整合包替代品是 farm_and_charm:flour（addMillingRecipes.js 研磨可得）。
  // 仍在生效的消费方：
  //   create_central_kitchen:compacting/cookie（8 个曲奇）
  //   create_central_kitchen:compacting/cake（createaddition 未装 → 条件通过、生效）
  // Create 自家的 dough 配方因 removeByOutput("create:dough") 已移除，不受影响。
  if (Item.exists("farm_and_charm:flour")) {
    e.add("forge:flour/wheat", "farm_and_charm:flour");
  }

  // 2) forge:pasta/raw_pasta
  // 原唯一成员 farmersdelight:raw_pasta 被移除；整合包替代品是 farm_and_charm:raw_pasta
  //（handleItemBlockFluidTags.js 只把它加到了 forge:food/raw_pasta）。
  // 当前消费方（VeggiesDelight 的 2 条 moredelight 兼容配方）因 moredelight 未安装而不加载，
  // 加回仅为语义正确，避免后续 mod 加进来时再次踩坑。
  if (Item.exists("farm_and_charm:raw_pasta")) {
    e.add("forge:pasta/raw_pasta", "farm_and_charm:raw_pasta");
  }
});
