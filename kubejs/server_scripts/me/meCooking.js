// priority: 0
// ============================================================
// Middle-earth × Farmer's Delight：让中州作物进入现有厨房设施。
//
// 中州自带的合成配方保留；这里只增加农夫乐事炖锅（farmersdelight:cooking）
// 的等价做法，方便批量制作/接入厨房自动化。
// 配方原料与输出均取自 Middle-earth 1.4.2-port.0 的 data/me/recipes。
// ============================================================
console.info("[ME-INTEGRATION] meCooking.js loaded");

ServerEvents.recipes((e) => {
  if (!Platform.isLoaded("me") || !Platform.isLoaded("farmersdelight")) return;

  const bowl = { item: "minecraft:bowl" };

  e.custom({
    type: "farmersdelight:cooking",
    cookingtime: 200,
    experience: 1.0,
    container: bowl,
    ingredients: [
      { tag: "me:vegetable" },
      { tag: "me:vegetable" },
      { tag: "me:vegetable" },
    ],
    result: { item: "me:vegetable_soup" },
  }).id("society:me/vegetable_soup_cooking");

  e.custom({
    type: "farmersdelight:cooking",
    cookingtime: 200,
    experience: 1.0,
    container: bowl,
    ingredients: [
      { tag: "me:cooked_fish" },
      { tag: "me:vegetable" },
      { tag: "me:vegetable" },
    ],
    result: { item: "me:fish_stew" },
  }).id("society:me/fish_stew_cooking");

  e.custom({
    type: "farmersdelight:cooking",
    cookingtime: 200,
    experience: 1.0,
    container: bowl,
    ingredients: [
      { item: "me:cooked_crab_claw" },
      { tag: "me:vegetable" },
      { tag: "me:vegetable" },
    ],
    result: { item: "me:crab_soup" },
  }).id("society:me/crab_soup_cooking");

  e.custom({
    type: "farmersdelight:cooking",
    cookingtime: 200,
    experience: 1.0,
    container: bowl,
    ingredients: [
      { tag: "me:cooked_poultry" },
      { tag: "me:vegetable" },
      { tag: "me:vegetable" },
    ],
    result: { item: "me:poultry_meal" },
  }).id("society:me/poultry_meal_cooking");

  e.custom({
    type: "farmersdelight:cooking",
    cookingtime: 200,
    experience: 1.0,
    container: bowl,
    ingredients: [
      { tag: "me:cooked_meat" },
      { tag: "me:cooked_meat" },
    ],
    result: { item: "me:meat_bowl" },
  }).id("society:me/meat_bowl_cooking");

  e.custom({
    type: "farmersdelight:cooking",
    cookingtime: 200,
    experience: 1.0,
    container: bowl,
    ingredients: [
      { tag: "me:cooked_meat" },
      { item: "me:boiled_egg" },
    ],
    result: { item: "me:meat_egg_meal" },
  }).id("society:me/meat_egg_meal_cooking");
});
