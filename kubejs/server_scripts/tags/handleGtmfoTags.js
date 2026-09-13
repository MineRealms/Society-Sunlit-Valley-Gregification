// priority: 0
// ============================================================
// GTMFO × Sunlit Valley — R1: 标签合并（只加标签，不改配方/物品）
// 进度文档：GTMFO_INTEGRATION.md
// 物品来源：GTMFO（gtmfo:*），共 381 物品 / 31 作物方块
// ============================================================
console.info("[GTMFO-INTEGRATION] handleGtmfoTags.js loaded (R1 tags)");

const GTMFO = "gtmfo:";
const g = (id) => GTMFO + id;

// ===== 种子（来自 GTMFO 作物注册表）=====
const seeds = [
  "seed_artichoke", "seed_basil", "seed_bean", "seed_coffee", "seed_cotton", "seed_cucumber",
  "seed_eggplant", "seed_garlic_purple", "seed_garlic_white", "seed_grape", "seed_horseradish",
  "seed_onion", "seed_oregano", "seed_pea", "seed_soy", "seed_tomato", "seed_white_grape",
  "corn_kernel", // 玉米种子
].map(g);

// ===== 蔬菜 =====
const vegetables = {
  onion: ["onion"],
  tomato: ["tomato"],
  cucumber: ["cucumber"],
  eggplant: ["eggplant"],
  garlic: ["garlic_purple", "garlic_white"],
  artichoke: ["artichoke"],
  lettuce: ["lettuce"],
  horseradish: ["horseradish"],
};

// ===== 水果 =====
const fruits = [
  "banana", "apricot", "lemon", "lime", "mango", "orange", "olive", "coconut",
  "grapes", "white_grapes",
];

// ===== 浆果（浆果丛直接种植，无种子物品）=====
const berries = [
  "blackberry", "blueberry", "raspberry", "strawberry",
  "black_currant", "red_currant", "white_currant",
  "lingonberry", "elderberry", "cranberry",
];

// ===== 作物产物（forge:crops 用，含香料/经济作物）=====
const crops = [
  "onion", "tomato", "cucumber", "eggplant", "garlic_purple", "garlic_white", "artichoke",
  "lettuce", "horseradish", "basil", "oregano", "black_pepper",
  "coffee_cherry", "corn_ear", "rice", "soybean", "pea_pod", "hop", "cotton",
];

// ===== 肉 =====
const rawMeats = [
  "bacon_raw", "sausage_raw", "sausage_roll_raw", "beef_slice", "seasoned_pork",
  "barg_meat", "scrap_meat",
];
const cookedMeats = [
  "bacon", "sausage", "sausage_roll", "beef_slice_roasted", "mince_meat_cooked",
  "meat_ingot_cooked", "porchetta",
];

// ===== 奶酪 =====
const cheeses = [
  "mozzarella_ball", "mozzarella_slice", "cheddar_slice", "cheddar_block",
  "gorgonzola_triangular_slice", "gorgonzola_wheel", "gorgonzola_wheel_fully_cured",
  "parmigiano_aged_roll", "parmigiano_brined_roll", "ricotta_piece",
];

// ===== 面团 / 未烤面点 =====
const doughs = [
  "dough", "flat_dough", "sugary_dough", "pasta_dough", "pasta_dough_egg",
  "pasta_dough_premixed", "graham_cracker_dough",
  "bread_unbaked", "baguette_unbaked", "bun_unbaked",
];

// ===== 甜点 =====
const sweets = [
  "apple_candy", "milk_chocolate", "marshmallow", "graham_cracker",
  "ice_cream", "ice_cream_bacon", "ice_cream_banana", "ice_cream_bear", "ice_cream_chip",
  "ice_cream_chocolate", "ice_cream_chorus", "ice_cream_chum", "ice_cream_lemon",
  "ice_cream_melon", "ice_cream_rainbow", "ice_cream_vanilla",
  "sorbet", "sorbet_apple", "sorbet_apricot", "sorbet_chorus", "sorbet_grape",
  "sorbet_lime", "sorbet_vibrant",
];

// ===== society:need_seeds（由种子种植的产物，Society 语义）=====
const needSeeds = [
  "onion", "tomato", "cucumber", "eggplant", "garlic_purple", "garlic_white", "artichoke",
  "horseradish", "basil", "oregano", "black_pepper", "coffee_cherry", "corn_ear",
  "soybean", "pea_pod", "cotton", "grapes", "white_grapes",
];

// ===== 季节分配（种子 + 产物 + 作物方块）=====
const seasons = {
  spring: {
    items: [
      "seed_artichoke", "seed_basil", "seed_bean", "seed_cucumber", "seed_garlic_purple",
      "seed_garlic_white", "seed_horseradish", "seed_onion", "seed_oregano", "seed_pea",
      "seed_soy",
      "artichoke", "basil", "cucumber", "garlic_purple", "garlic_white", "horseradish",
      "lettuce", "onion", "oregano", "pea_pod", "soybean", "strawberry",
    ],
    blocks: [
      "crop_artichoke", "crop_basil", "crop_bean", "crop_cucumber", "crop_garlic",
      "crop_horseradish", "crop_onion", "crop_oregano", "crop_pea", "crop_soy",
      "crop_strawberry",
    ],
  },
  summer: {
    items: [
      "seed_basil", "seed_bean", "seed_coffee", "seed_cotton", "seed_cucumber", "seed_grape",
      "seed_oregano", "seed_pea", "seed_soy", "seed_tomato", "seed_white_grape", "corn_kernel",
      "basil", "black_currant", "black_pepper", "blackberry", "blueberry", "coffee_cherry",
      "corn_ear", "cotton", "cucumber", "grapes", "hop", "onion", "oregano", "pea_pod",
      "raspberry", "red_currant", "rice", "soybean", "strawberry", "tomato", "white_currant",
      "white_grapes",
    ],
    blocks: [
      "crop_basil", "crop_bean", "crop_black_currant", "crop_black_pepper", "crop_blackberry",
      "crop_blueberry", "crop_coffee", "crop_corn", "crop_cotton", "crop_cucumber",
      "crop_grape", "crop_hops", "crop_onion", "crop_oregano", "crop_pea", "crop_raspberry",
      "crop_red_currant", "crop_rice", "crop_soy", "crop_strawberry", "crop_tomato",
      "crop_white_currant", "crop_white_grape",
    ],
  },
  autumn: {
    items: [
      "seed_bean", "seed_grape", "seed_horseradish", "seed_onion", "seed_white_grape",
      "black_currant", "black_pepper", "corn_ear", "cranberry", "elderberry", "eggplant",
      "grapes", "horseradish", "lingonberry", "onion", "red_currant", "rice", "tomato",
      "white_currant", "white_grapes",
    ],
    blocks: [
      "crop_aubergine", "crop_bean", "crop_black_currant", "crop_black_pepper", "crop_corn",
      "crop_cranberry", "crop_elderberry", "crop_grape", "crop_horseradish",
      "crop_lingonberry", "crop_onion", "crop_red_currant", "crop_rice", "crop_tomato",
      "crop_white_currant", "crop_white_grape",
    ],
  },
  winter: {
    items: ["seed_garlic_purple", "seed_garlic_white", "garlic_purple", "garlic_white"],
    blocks: ["crop_garlic"],
  },
};

ServerEvents.tags("item", (e) => {
  // ---- forge 标准标签 ----
  seeds.forEach((id) => e.add("forge:seeds", id));
  crops.forEach((id) => e.add("forge:crops", g(id)));
  fruits.forEach((id) => e.add("forge:fruits", g(id)));
  berries.forEach((id) => {
    e.add("forge:berries", g(id));
    e.add("forge:fruits", g(id));
  });
  rawMeats.forEach((id) => e.add("forge:raw_meat", g(id)));
  cookedMeats.forEach((id) => e.add("forge:cooked_meat", g(id)));
  cheeses.forEach((id) => {
    e.add("forge:cheeses", g(id));
    e.add("c:cheeses", g(id));
  });
  doughs.forEach((id) => e.add("forge:dough", g(id)));
  sweets.forEach((id) => e.add("farmersdelight:sweets", g(id)));

  // 蔬菜 + 子标签（forge:vegetables/<name>）
  // 注意：KubeJS 的 Rhino 不支持 Array.prototype.flat()，这里逐项循环
  Object.entries(vegetables).forEach((entry) => {
    entry[1].forEach((id) => {
      e.add("forge:vegetables", g(id));
      e.add("forge:vegetables/" + entry[0], g(id));
    });
  });

  // 作物子标签（forge:crops/<name>）
  crops.forEach((id) => e.add("forge:crops/" + id, g(id)));

  // Society：需要种子种植的产物
  needSeeds.forEach((id) => e.add("society:need_seeds", g(id)));

  // ---- 季节标签（item）----
  Object.entries(seasons).forEach((entry) => {
    entry[1].items.forEach((id) => e.add("sereneseasons:" + entry[0] + "_crops", g(id)));
  });
});

ServerEvents.tags("block", (e) => {
  // ---- 季节标签（block，Serene Seasons 生长判定）----
  Object.entries(seasons).forEach((entry) => {
    entry[1].blocks.forEach((id) => e.add("sereneseasons:" + entry[0] + "_crops", g(id)));
  });
});
