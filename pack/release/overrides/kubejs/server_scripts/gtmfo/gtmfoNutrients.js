// GTMFO x Sunlit Valley: balanced-diet integration.
// The mod is optional for pack tooling, so every GTMFO-facing path is guarded.
const GTMFO_NUTRIENT_MOD = Platform.isLoaded("gtmfo");
const GTMFO_NUTRIENT_NAMES = ["dairy", "fruit", "grain", "protein", "vegetable"];

if (!GTMFO_NUTRIENT_MOD) {
  console.info("[GTMFO-INTEGRATION] gtmfoNutrients.js skipped: GTMFO is not installed");
}

// Tags cover newly added foods and raw ingredients. A food can match more than one
// tag; composite meals below use explicit values and therefore override those categories.
ServerEvents.tags("item", (event) => {
  if (!GTMFO_NUTRIENT_MOD) return;

  event.add("gtmfo:nutrient/dairy", [
    "#c:cheeses",
    "#forge:cheeses",
    "farmersdelight:milk_bottle",
    "farm_and_charm:butter",
    "isorropia:chocolate_cream",
    "isorropia:chocolate_milk_bucket",
  ]);
  event.add("gtmfo:nutrient/fruit", [
    "#forge:fruits",
    "#diet:fruits",
    "minecraft:apple",
    "minecraft:melon_slice",
    "minecraft:sweet_berries",
    "minecraft:glow_berries",
  ]);
  event.add("gtmfo:nutrient/grain", [
    "#c:grain",
    "#forge:grain",
    "#diet:grains",
    "minecraft:wheat",
    "minecraft:bread",
  ]);
  event.add("gtmfo:nutrient/protein", [
    "#forge:raw_meat",
    "#forge:cooked_meat",
    "#c:raw_fishes",
    "#c:cooked_fishes",
    "#crabbersdelight:cooked_seafood",
    "me:cooked_goose",
    "me:cooked_duck",
    "me:cooked_swan",
    "me:cooked_horse",
    "me:cooked_rat",
    "me:cooked_crab_claw",
    "me:raw_goose",
    "me:raw_duck",
    "me:raw_swan",
    "me:raw_horse",
    "me:raw_rat",
    "me:raw_crab_claw",
  ]);
  event.add("gtmfo:nutrient/vegetable", [
    "#c:vegetables",
    "#forge:vegetables",
    "#diet:vegetables",
    "minecraft:carrot",
    "minecraft:potato",
    "minecraft:baked_potato",
    "minecraft:beetroot",
  ]);
});

// Explicit values are based on ingredients and keep individual categories below
// the built-in GTMFO meal scale. They also make the common pack dishes readable.
const GTMFO_NUTRIENT_DEFINITIONS = {
  "minecraft:apple": { fruit: 1.0 },
  "minecraft:bread": { grain: 1.0 },
  "minecraft:cookie": { grain: 0.75 },
  "minecraft:melon_slice": { fruit: 0.75 },
  "minecraft:sweet_berries": { fruit: 0.75 },
  "minecraft:glow_berries": { fruit: 0.75 },
  "minecraft:carrot": { vegetable: 1.0 },
  "minecraft:potato": { vegetable: 1.0 },
  "minecraft:baked_potato": { vegetable: 1.25 },
  "minecraft:beetroot": { vegetable: 1.0 },
  "minecraft:cooked_beef": { protein: 1.5 },
  "minecraft:cooked_porkchop": { protein: 1.5 },
  "minecraft:cooked_chicken": { protein: 1.5 },
  "minecraft:cooked_mutton": { protein: 1.5 },
  "minecraft:cooked_rabbit": { protein: 1.5 },
  "minecraft:cooked_cod": { protein: 1.25 },
  "minecraft:cooked_salmon": { protein: 1.25 },

  "farmersdelight:milk_bottle": { dairy: 1.0 },
  "farmersdelight:cabbage": { vegetable: 1.0 },
  "farmersdelight:onion": { vegetable: 1.0 },
  "farmersdelight:tomato": { vegetable: 1.0 },
  "farmersdelight:rice": { grain: 1.0 },
  "farmersdelight:cooked_rice": { grain: 1.25 },
  "farmersdelight:fried_egg": { protein: 1.0 },
  "farmersdelight:beef_patty": { protein: 1.5 },
  "farmersdelight:cooked_bacon": { protein: 1.25 },
  "farmersdelight:cooked_chicken_cuts": { protein: 1.25 },
  "farmersdelight:cooked_cod_slice": { protein: 1.0 },
  "farmersdelight:cooked_mutton_chops": { protein: 1.25 },
  "farmersdelight:cooked_salmon_slice": { protein: 1.0 },
  "farmersdelight:fruit_salad": { fruit: 1.5 },
  "farmersdelight:mixed_salad": { vegetable: 1.25, fruit: 0.5 },
  "farmersdelight:vegetable_soup": { vegetable: 1.5 },
  "farmersdelight:fish_stew": { protein: 1.25, vegetable: 0.5 },
  "farmersdelight:steak_and_potatoes": { protein: 1.5, vegetable: 0.75 },
  "farmersdelight:pasta_with_meatballs": { grain: 1.0, protein: 1.25 },
  "farmersdelight:chicken_sandwich": { grain: 0.75, protein: 1.25 },
  "farmersdelight:hamburger": { grain: 0.75, protein: 1.5 },
  "farmersdelight:bacon_and_eggs": { protein: 1.5 },
  "farmersdelight:mutton_wrap": { grain: 0.75, protein: 1.25, vegetable: 0.5 },
  "farmersdelight:stuffed_potato": { vegetable: 1.25, protein: 0.75 },
  "farmersdelight:sweet_berry_cheesecake": { dairy: 1.0, fruit: 1.0, grain: 0.5 },
  "farmersdelight:apple_pie": { fruit: 1.0, grain: 0.75 },
  "farmersdelight:chocolate_pie": { grain: 0.75, dairy: 0.5 },

  "farm_and_charm:butter": { dairy: 1.0 },
  "farm_and_charm:lettuce": { vegetable: 1.0 },
  "farm_and_charm:tomato": { vegetable: 1.0 },
  "farm_and_charm:strawberry": { fruit: 1.0 },
  "farm_and_charm:oatmeal_with_strawberries": { grain: 1.0, fruit: 1.0 },
  "farm_and_charm:farmer_salad": { vegetable: 1.25, fruit: 0.25 },
  "farm_and_charm:farmers_bread": { grain: 1.25 },
  "farm_and_charm:bacon_with_eggs": { protein: 1.5 },
  "farm_and_charm:beef_patty_with_vegetables": { protein: 1.5, vegetable: 0.75 },
  "farm_and_charm:chicken_wrapped_in_bacon": { protein: 1.75 },
  "farm_and_charm:lamb_with_corn": { protein: 1.5, grain: 0.5 },
  "farm_and_charm:oat_pancake": { grain: 1.25 },
  "farm_and_charm:potato_with_roast_meat": { vegetable: 1.0, protein: 1.5 },
  "farm_and_charm:roasted_chicken": { protein: 1.5 },
  "farm_and_charm:stuffed_chicken": { protein: 1.5, vegetable: 0.75 },
  "farm_and_charm:stuffed_rabbit": { protein: 1.5, vegetable: 0.5 },

  "bakery:bread": { grain: 1.0 },
  "bakery:baguette": { grain: 1.25 },
  "bakery:braided_bread": { grain: 1.25 },
  "bakery:bun": { grain: 0.75 },
  "bakery:crusty_bread": { grain: 1.25 },
  "bakery:grilled_bacon_sandwich": { grain: 0.75, protein: 1.25 },
  "bakery:grilled_salmon_sandwich": { grain: 0.75, protein: 1.25 },
  "bakery:toast": { grain: 0.75 },
  "bakery:waffle": { grain: 1.0, dairy: 0.25 },
  "bakery:apple_pie": { fruit: 1.0, grain: 0.75 },
  "bakery:vegetable_sandwich": { grain: 0.75, vegetable: 1.0 },

  "candlelight:beef_tartare": { protein: 1.5 },
  "candlelight:beetroot_salad": { vegetable: 1.25 },
  "candlelight:fresh_garden_salad": { vegetable: 1.5, fruit: 0.25 },
  "candlelight:harvest_plate": { vegetable: 1.0, fruit: 0.75, grain: 0.5 },
  "candlelight:tomato_mozzarella_salad": { vegetable: 1.0, dairy: 1.0 },
  "candlelight:bolognese": { grain: 0.75, protein: 1.25 },
  "candlelight:fillet_steak": { protein: 1.75 },
  "candlelight:omelet": { protein: 1.25 },
  "candlelight:pasta_with_bolognese": { grain: 1.0, protein: 1.25 },
  "candlelight:beef_wellington": { grain: 0.75, protein: 1.75 },
  "candlelight:chicken_alfredo": { grain: 0.75, protein: 1.25, dairy: 0.75 },
  "candlelight:chicken_with_vegetables": { protein: 1.25, vegetable: 1.0 },
  "candlelight:lasagne": { grain: 1.0, protein: 1.25, dairy: 0.5 },
  "candlelight:pork_ribs": { protein: 1.75 },
  "candlelight:roastbeef_with_glazed_carrots": { protein: 1.5, vegetable: 0.75 },
  "candlelight:tropical_fish_supreme": { protein: 1.5, vegetable: 0.5 },

  "meadow:piece_of_cheese": { dairy: 1.0 },
  "meadow:piece_of_buffalo_cheese": { dairy: 1.25 },
  "meadow:piece_of_goat_cheese": { dairy: 1.25 },
  "meadow:piece_of_sheep_cheese": { dairy: 1.25 },
  "meadow:cheese_sandwich": { dairy: 1.0, grain: 0.75 },
  "meadow:cheese_tart": { dairy: 1.0, grain: 0.75 },
  "meadow:cheesecake": { dairy: 1.0, grain: 0.5 },
  "meadow:fondue": { dairy: 1.5 },
  "meadow:cooked_buffalo_meat": { protein: 1.5 },

  "crabbersdelight:cooked_clam_meat": { protein: 1.25 },
  "crabbersdelight:cooked_clawster": { protein: 1.25 },
  "crabbersdelight:cooked_crab": { protein: 1.25 },
  "crabbersdelight:cooked_frog_leg": { protein: 1.25 },
  "crabbersdelight:cooked_glow_squid_tentacles": { protein: 1.0 },
  "crabbersdelight:cooked_pufferfish_slice": { protein: 1.0 },
  "crabbersdelight:cooked_shrimp": { protein: 1.25 },
  "crabbersdelight:cooked_squid_tentacles": { protein: 1.0 },
  "crabbersdelight:cooked_tropical_fish": { protein: 1.25 },
  "crabbersdelight:cooked_tropical_fish_slice": { protein: 1.0 },
  "crabbersdelight:fish_stick": { grain: 0.5, protein: 1.0 },
  "crabbersdelight:frog_leg_kebob": { protein: 1.25 },
  "crabbersdelight:seafood_gumbo": { protein: 1.25, vegetable: 0.75 },
  "crabbersdelight:shrimp_fried_rice": { grain: 1.0, protein: 1.0 },
  "crabbersdelight:shrimp_skewer": { protein: 1.25 },
  "crabbersdelight:squid_kebob": { protein: 1.25 },
  "crabbersdelight:stuffed_nautilus_shell": { protein: 1.0, vegetable: 0.5 },
  "crabbersdelight:surf_and_turf": { protein: 1.75, vegetable: 0.5 },

  "vinery:apple_cider": { fruit: 0.75 },
  "vinery:apple_juice": { fruit: 1.0 },
  "vintagedelight:apple_sauce_bottle": { fruit: 1.0 },
  "vinery:red_grapejuice": { fruit: 1.0 },

  "isorropia:chocolate_cream": { dairy: 1.0 },
  "isorropia:chocolate_milk_bucket": { dairy: 1.0 },

  // Middle-earth (中州) crops, ingredients, and complete meals.
  // Values are explicit because these composite foods should reflect their recipe inputs,
  // not inherit a single category from the item tag.
  "me:leek": { vegetable: 1.0 },
  "me:cucumber": { vegetable: 1.0 },
  "me:lettuce": { vegetable: 1.0 },
  "me:garlic": { vegetable: 1.0 },
  "me:tomato": { vegetable: 1.0 },
  "me:bell_pepper": { vegetable: 1.0 },
  "me:onion": { vegetable: 1.0 },
  "me:strawberry": { fruit: 0.75 },
  "me:strawberries": { fruit: 0.75 },
  "me:white_mushroom": { vegetable: 0.5 },
  "me:ghostshroom": { vegetable: 0.5 },
  "me:cave_amanita": { vegetable: 0.5 },
  "me:yellow_amanita": { vegetable: 0.5 },
  "me:deep_firecap": { vegetable: 0.5 },
  "me:sky_firecap": { vegetable: 0.5 },
  "me:violet_caps": { vegetable: 0.5 },
  "me:brown_bolete": { vegetable: 0.5 },
  "me:trumpet_shroom": { vegetable: 0.5 },
  "me:tubeshroom": { vegetable: 0.5 },
  "me:lembas": { grain: 2.0 },
  "me:cram": { grain: 0.5 },
  "me:maggoty_bread": { grain: 0.75 },
  "me:boiled_egg": { protein: 1.0 },
  "me:vegetable_soup": { vegetable: 1.5 },
  "me:berry_pie": { fruit: 1.0, grain: 0.75 },
  "me:fish_stew": { protein: 1.25, vegetable: 0.5 },
  "me:crab_soup": { protein: 1.25, vegetable: 0.5 },
  "me:poultry_meal": { protein: 1.25, vegetable: 0.5 },
  "me:meat_bowl": { protein: 1.5 },
  "me:meat_egg_meal": { protein: 1.5 },
  "me:meat_skewer": { protein: 0.75, vegetable: 0.25 },
  "me:cooked_meat_skewer": { protein: 1.5, vegetable: 0.5 },
  "me:rat_skewer": { protein: 0.5 },
  "me:cooked_rat_skewer": { protein: 1.0 },
  "me:vegetable_skewer": { vegetable: 0.75 },
  "me:cooked_vegetable_skewer": { vegetable: 1.25 },
  "me:sack_of_horsefeed": { grain: 0.75, vegetable: 0.5 },
  "me:cooked_goose": { protein: 1.25 },
  "me:cooked_duck": { protein: 1.25 },
  "me:cooked_swan": { protein: 1.25 },
  "me:cooked_horse": { protein: 1.5 },
  "me:cooked_rat": { protein: 0.75 },
  "me:cooked_crab_claw": { protein: 1.0 },
  "me:raw_goose": { protein: 0.75 },
  "me:raw_duck": { protein: 0.75 },
  "me:raw_swan": { protein: 0.75 },
  "me:raw_horse": { protein: 1.0 },
  "me:raw_rat": { protein: 0.5 },
  "me:raw_crab_claw": { protein: 0.75 },
  "me:pterosaur_nugget": { protein: 0.75 },
  "me:therapod_nugget": { protein: 0.75 },
  "me:ceratopsian_nugget": { protein: 0.75 },
  "me:thyreophoran_nugget": { protein: 0.75 },
  "me:sauropod_nugget": { protein: 0.75 },
};

if (GTMFO_NUTRIENT_MOD && typeof GTMFO !== "undefined") {
  var registered = GTMFO.nutrients.addMany(GTMFO_NUTRIENT_DEFINITIONS);
  console.info("[GTMFO-INTEGRATION] nutrient definitions registered: " + registered);
}

const updateNutrientStage = (player, stage, enabled) => {
  if (enabled && !player.stages.has(stage)) player.stages.add(stage);
  if (!enabled && player.stages.has(stage)) player.stages.remove(stage);
};

// FTB Quests consumes gamestages. Stages mirror the live values and are deliberately
// removed when a nutrient decays below a milestone, so the quest display stays honest.
PlayerEvents.tick((event) => {
  if (!GTMFO_NUTRIENT_MOD || event.player.age % 20 !== 0) return;

  const player = event.player;
  let balancedFive = true;
  let balancedTen = true;

  GTMFO_NUTRIENT_NAMES.forEach((name) => {
    const value = Number(player.persistentData.getFloat("gtmfo_nutrient_" + name));
    const safeValue = isFinite(value) ? value : 0;
    updateNutrientStage(player, "gtmfo_nutrient_" + name + "_5", safeValue >= 5.0);
    balancedFive = balancedFive && safeValue >= 5.0;
    balancedTen = balancedTen && safeValue >= 10.0;
  });

  updateNutrientStage(player, "gtmfo_nutrient_balanced_5", balancedFive);
  updateNutrientStage(player, "gtmfo_nutrient_balanced_10", balancedTen);
});

console.info("[GTMFO-INTEGRATION] gtmfoNutrients.js loaded (nutrients, stages, FTBQ bridge)");
