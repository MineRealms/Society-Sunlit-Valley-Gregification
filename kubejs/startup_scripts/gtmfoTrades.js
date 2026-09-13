// priority: -30
// ============================================================
// GTMFO × Sunlit Valley — R2: 经济数据（定价 + 可售）
// 进度文档：GTMFO_INTEGRATION.md
// 依赖：globalRegistry.js 先执行（它是 priority -20），本脚本用 -30 保证在其之后
// （KubeJS 规则：priority 数值越大越先加载；实测 -10 会比 -20 早加载导致 global.crops 未定义）
// 效果：自动获得 society:sellable / farmer_product 等标签（由 handleItemBlockFluidTags.js 遍历 global.trades 生成）
//       + 价格 tooltip（addPriceTooltips.js）+ Shipping Bin 售价 + 村民礼物
// 定价参考：包内同类物品（见 GTMFO_INTEGRATION.md R2 明细）
// ============================================================
console.info("[GTMFO-INTEGRATION] gtmfoTrades.js loaded (R2 trades)");

const GTMFO = "gtmfo:";
const CROP_MULT = "shippingbin:crop_sell_multiplier";
const WOOD_MULT = "shippingbin:wood_sell_multiplier";

const addTrades = (list, kind, entries, multiplier) => {
  entries.forEach(([id, value]) => {
    const item = GTMFO + id;
    list.push({ item: item, value: value });
    global.trades.set(item, {
      value: global.getConfiguredValue(value, kind),
      multiplier: multiplier,
    });
  });
};

// ===== 作物 / 水果 / 浆果（global.crops，参考包内：洋葱12 番茄24 玉米28 茄子42 蒜27 生菜24 黄瓜72 草莓18 蓝莓24 蔓越莓18 大米16 葡萄20 香蕉16 芒果64 橙96 柠檬160 咖啡豆8 可可豆4）=====
addTrades(global.crops, "crop", [
  ["onion", 12],
  ["tomato", 24],
  ["cucumber", 30],
  ["eggplant", 42],
  ["garlic_purple", 27],
  ["garlic_white", 27],
  ["artichoke", 30],
  ["lettuce", 24],
  ["horseradish", 20],
  ["basil", 12],
  ["oregano", 12],
  ["black_pepper", 24],
  ["coffee_cherry", 12],
  ["corn_ear", 28],
  ["rice", 16],
  ["soybean", 14],
  ["pea_pod", 10],
  ["hop", 12],
  ["cotton", 16],
  ["grapes", 20],
  ["white_grapes", 20],
  ["banana", 16],
  ["apricot", 24],
  ["lemon", 40],
  ["lime", 32],
  ["mango", 48],
  ["orange", 48],
  ["coconut", 32],
  ["olive", 24],
  ["blackberry", 20],
  ["blueberry", 24],
  ["raspberry", 20],
  ["strawberry", 18],
  ["black_currant", 16],
  ["red_currant", 16],
  ["white_currant", 16],
  ["lingonberry", 20],
  ["elderberry", 20],
  ["cranberry", 18],
], CROP_MULT);

// ===== 生肉 / 肉制品原料（global.animalProducts，参考包内：牛肉16 猪肉32 鸡肉8 生水牛肉32）=====
addTrades(global.animalProducts, "crop", [
  ["beef_slice", 16],
  ["bacon_raw", 20],
  ["sausage_raw", 24],
  ["sausage_roll_raw", 32],
  ["seasoned_pork", 36],
  ["barg_meat", 48],
  ["scrap_meat", 3],
], CROP_MULT);

// ===== 料理 / 饮品（global.cooking，参考包内：面包16 三明治114-171 巧克力派切片165 苹果派切片150 芝士蛋糕35 巧克力棒30）=====
addTrades(global.cooking, "crop", [
  // 面包类
  ["bun", 12],
  ["baguette", 20],
  ["bread_slice", 4],
  ["toast", 8],
  // 三明治 / 汉堡
  ["sandwich_toast", 40],
  ["sandwich_veggie", 90],
  ["sandwich_cheese", 100],
  ["sandwich_steak", 140],
  ["sandwich_bacon", 170],
  ["sandwich_vibrant", 200],
  ["burger_veggie", 110],
  ["burger_cheese", 120],
  ["burger_steak", 160],
  ["burger_bacon", 190],
  ["burger_chum", 60],
  // 披萨切片
  ["pizza_cheese_slice", 90],
  ["pizza_veggie_slice", 100],
  ["pizza_meat_slice", 110],
  // 意面 / 主食
  ["pasta_al_pomodoro", 120],
  ["pasta_alla_norma", 140],
  ["pasta_e_fagioli", 130],
  ["pasta_all_amogus", 160],
  ["carbonara", 180],
  ["fettuccine_alfredo", 200],
  ["tagliatelle_al_ragu", 220],
  ["lasagna_napoletana", 300],
  ["risotto", 200],
  ["tortellini_in_brodo", 180],
  ["jiaozi", 120],
  ["pelmeni", 140],
  // 英式 / 意式菜
  ["beans_on_toast", 90],
  ["full_breakfast", 250],
  ["shepherds_pie", 220],
  ["porchetta", 200],
  ["vitello_tonnato", 260],
  ["bruschetta", 90],
  ["caponata", 110],
  ["parmigiana", 180],
  ["polenta", 80],
  ["rafanata", 120],
  // 炸物 / 小食
  ["fish_and_chips", 160],
  ["fried_fish", 80],
  ["french_fries", 60],
  ["potato_stick", 20],
  ["chips_kettle", 30],
  ["chips_reduced_fat", 30],
  ["chips_syals", 30],
  ["chips_bag", 60],
  // 奶酪
  ["mozzarella_slice", 15],
  ["mozzarella_ball", 60],
  ["cheddar_slice", 20],
  ["cheddar_block", 160],
  ["gorgonzola_triangular_slice", 25],
  ["gorgonzola_wheel", 400],
  ["parmigiano_aged_roll", 500],
  ["ricotta_piece", 40],
  // 甜点
  ["apple_candy", 20],
  ["milk_chocolate", 30],
  ["marshmallow", 12],
  ["graham_cracker", 16],
  ["ice_cream", 60],
  ["sorbet", 55],
  // 饮品
  ["coffee", 30],
  ["coffee_energized", 60],
  ["juice_apple", 60],
  ["juice_orange", 60],
  ["etirps", 40],
  ["etirps_cranberry", 50],
  ["mineral_water", 20],
  ["sparkling_water", 25],
], CROP_MULT);

// ===== 酒 / 酿造（global.wines / global.brews，参考包内：vinery 葡萄酒 336-6048，用 wood 乘数）=====
addTrades(global.wines, "wood", [
  ["red_wine", 400],
  ["white_wine", 400],
], WOOD_MULT);

addTrades(global.brews, "wood", [
  ["beer", 80],
  ["vodka", 120],
  ["leninade", 90],
], WOOD_MULT);
