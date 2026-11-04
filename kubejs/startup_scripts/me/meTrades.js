// priority: -30
// ============================================================
// Middle-earth crops and meals in the shipping bin price table.
// Runs after globalRegistry.js (-20) so global.trades/getConfiguredValue exist.
// ============================================================
console.info("[ME-INTEGRATION] meTrades.js loaded (shipping bin)");

let ME_LOADED = Platform.isLoaded("me");
let ME_TRADES_READY = typeof global.trades !== "undefined";
if (!ME_LOADED) {
  console.info("[ME-INTEGRATION] meTrades.js skipped: Middle-earth not installed");
} else if (!ME_TRADES_READY) {
  console.info("[ME-INTEGRATION] meTrades.js skipped: global.trades missing (globalRegistry.js not loaded)");
}

let ME_CROP = "shippingbin:crop_sell_multiplier";
let ME_ARTISAN = "shippingbin:crop_sell_multiplier";

let addMeTrades = (kind, multiplier, entries) => {
  if (!ME_LOADED || !ME_TRADES_READY) return;
  for (let i = 0; i < entries.length; i++) {
    let entry = entries[i];
    global.trades.set("me:" + entry[0], {
      value: global.getConfiguredValue(entry[1], kind),
      multiplier: multiplier,
    });
  }
};

// Raw produce. Kept below the pack's expensive specialty crops; quality
// bonuses are applied by the shipping bin and merchant GUI separately.
addMeTrades("crop", ME_CROP, [
  ["leek", 10], ["cucumber", 12], ["lettuce", 10], ["garlic", 14],
  ["tomato", 12], ["bell_pepper", 14], ["onion", 10],
  ["strawberry", 12], ["strawberries", 12],
  ["flax", 16], ["pipeweed", 24],
  ["white_mushroom", 8], ["brown_bolete", 10], ["trumpet_shroom", 12],
  ["ghostshroom", 12], ["yellow_amanita", 12],
]);

// Prepared dishes; the recipe and GTMFO values live in meCooking.js and
// gtmfoNutrients.js. These are shipping-bin values only.
addMeTrades("artisan", ME_ARTISAN, [
  ["vegetable_soup", 55], ["berry_pie", 48], ["fish_stew", 65],
  ["crab_soup", 65], ["poultry_meal", 60], ["meat_bowl", 72],
  ["meat_egg_meal", 70], ["vegetable_skewer", 18], ["cooked_vegetable_skewer", 36],
  ["meat_skewer", 20], ["cooked_meat_skewer", 42],
  ["rat_skewer", 10], ["cooked_rat_skewer", 20],
  ["cooked_goose", 36], ["cooked_duck", 36], ["cooked_swan", 40],
  ["cooked_rat", 14], ["sack_of_horsefeed", 26],
]);

console.info("[ME-INTEGRATION] meTrades.js done");
