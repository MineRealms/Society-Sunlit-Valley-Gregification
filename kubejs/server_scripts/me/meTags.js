// priority: 0
// ============================================================
// Middle-earth（me）接入 Sunlit Valley 农业标签。
//
// Item tags：供农场/配方/营养系统识别作物产物与种子。
// Block tag quality_food:quality_blocks：Quality Food 的品质方块标签，registry 类型是 BLOCK。
// 依据本机 Middle-earth 1.4.2-port.0 的 tags、loot tables 与 Block/BlockItem 注册。
// 该标签接入本身不保证每种作物一定产出品质物品；运行时效果仍需游戏内验收。
// ============================================================
console.info("[ME-INTEGRATION] meTags.js loaded");

if (Platform.isLoaded("me")) {
  ServerEvents.tags("item", (e) => {
    // 可食用蔬菜；亚麻是纤维作物，不放入 forge:vegetables。
    const VEGETABLES = ["leek", "cucumber", "lettuce", "garlic", "tomato", "bell_pepper", "onion"];
    VEGETABLES.forEach((crop) => e.add("forge:crops/" + crop, "me:" + crop));
    e.add("forge:vegetables", VEGETABLES.map((crop) => "me:" + crop));
    e.add("forge:fruits", ["me:strawberry", "me:strawberries"]);
    e.add("forge:crops/strawberry", "me:strawberry");
    e.add("forge:crops/flax", "me:flax");

    // 中州模组定义的可播种物；同时接入 Forge 与 Common Tags 种子分类。
    const SEEDS = ["bell_pepper", "cucumber", "flax", "lettuce", "pipeweed", "tomato"]
      .map((name) => "me:" + name + "_seeds");
    e.add("forge:seeds", SEEDS);
    e.add("c:seeds", SEEDS);
  });

  // quality_food:quality_blocks 在 Quality Food 中是 BLOCK tag，不是 ITEM tag。
  ServerEvents.tags("block", (e) => {
    e.add("quality_food:quality_blocks", [
      "me:bell_pepper_crop",
      "me:cucumber_crop",
      "me:flax_crop",
      "me:garlic_crop",
      "me:leek_crop",
      "me:lettuce_crop",
      "me:onion_crop",
      "me:pipeweed_crop",
      "me:tomato_crop",
      "me:strawberry_bush",
    ]);
  });
}

