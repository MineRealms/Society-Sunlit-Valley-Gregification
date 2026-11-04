// priority: 0
// ============================================================
// 神秘附属（ThaumicAdditions）× 农业桥 —— 品质糖 → 坩埚 → 魔力盐
//
// 目标：枫糖浆农业线（品质糖）接进 TC 坩埚，产出 thaumadds 魔力盐，
//       供灵气扩散器给农田/牲畜施加要素食效（1.12 原版机制）。
//
// 事实依据（JAR / 源码核对，非推测）：
//  - 坩埚 catalyst 为 Forge Ingredient，支持精确 NBT：
//    {"item":"minecraft:sugar","nbt":"{quality_food:{quality:3}}"}
//    （CrucibleRecipe$Serializer → RecipeValuePlatform.INGREDIENT_NONEMPTY
//      → Ingredient.fromJson → CraftingHelper.getItemStack，原生读 nbt 字段）
//  - 品质 3 糖来源：addMiscRecipes.js 枫糖浆 → 8× 糖（精确 NBT，无 effects 键）
//  - thaumadds:salt_essence（魔力盐）= 灵气扩散器燃料（TileAuraDisperser）
// ============================================================
console.info("[TC-FARM-BRIDGE] thaumaddsFarmBridge.js loaded");

ServerEvents.recipes((e) => {
  if (!Platform.isLoaded("thaumadds")) return;

  e.custom({
    type: "thaumcraft:crucible",
    catalyst: { item: "minecraft:sugar", nbt: "{quality_food:{quality:3}}" },
    result: { item: "thaumadds:salt_essence", count: 2 },
    aspects: { herba: 2, ignis: 1 },
  }).id("thaumadds:compat/salt_essence_from_quality_sugar");
});
