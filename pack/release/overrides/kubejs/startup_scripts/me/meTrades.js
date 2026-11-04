// priority: -30
// ============================================================
// Middle-earth crops and meals in the shipping bin price table.
// Runs after globalRegistry.js (-20) so global.trades/getConfiguredValue exist.
// ============================================================
console.info("[ME-INTEGRATION] meTrades.js loaded (shipping bin)");

const ME_LOADED = Platform.isLoaded("me");
if (!ME_LOADED) {
  console.info("[ME-INTEGRATION] meTrades.js skipped: Middle-earth not installed");
}

const CROP = "shippingbin:crop_sell_multiplier";
const ARTISAN = "shippingbin:crop_sell_multiplier";

const addMeTrades = (kind, multiplier, entries) => {
  if (!ME_LOADED) return;
  entries.forEach(([id, value]) => {
    global.trades.set("me:" + id, {
      value: global.getConfiguredValue(value, kind),
      multiplier: multiplier,
    });
  });
};

// Raw produce. Kept below the pack's expensive specialty crops; quality
// bonuses are applied by the shipping bin and merchant GUI separately.
addMeTrades("crop", CROP, [
  ["leek", 10], ["cucumber", 12], ["lettuce", 10], ["garlic", 14],
  ["tomato", 12], ["bell_pepper", 14], ["onion", 10],
  ["strawberry", 12], ["strawberries", 12],
  ["flax", 16], ["pipeweed", 24],
  ["white_mushroom", 8], ["brown_bolete", 10], ["trumpet_shroom", 12],
]);

// Prepared dishes; the recipe and GTMFO values live in meCooking.js and
// gtmfoNutrients.js. These are shipping-bin values only.
addMeTrades("artisan", ARTISAN, [
  ["vegetable_soup", 55], ["berry_pie", 48], ["fish_stew", 65],
  ["crab_soup", 65], ["poultry_meal", 60], ["meat_bowl", 72],
  ["meat_egg_meal", 70], ["vegetable_skewer", 18], ["cooked_vegetable_skewer", 36],
  ["meat_skewer", 20], ["cooked_meat_skewer", 42],
  ["rat_skewer", 10], ["cooked_rat_skewer", 20],
]);

console.info("[ME-INTEGRATION] meTrades.js done");
