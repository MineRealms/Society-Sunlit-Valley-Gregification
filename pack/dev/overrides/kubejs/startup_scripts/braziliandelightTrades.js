// priority: -30
// ============================================================
// 巴西乐事（Brazilian Delight）× Sunlit Valley — 经济数据（定价 + 可售）
// 文档：本会话设计（Delight 系联动）
//
// 依赖：globalRegistry.js（priority -20）先执行；本脚本 -30 保证其后。
// 效果：society:sellable 标签 + 价格 tooltip + Shipping Bin 售价 + 村民礼物。
// 定价参考（包内同类）：蔬菜 10-42 / 生肉 12-16 / 熟肉 16-24 / 冰淇淋 60 /
//                       小吃 40-90 / 大菜 160-300 / 甜点 60-100 / 饮料 25-60。
// ============================================================
console.info("[BRAZILIANDELIGHT-INTEGRATION] braziliandelightTrades.js loaded");

const BD_LOADED = Platform.isLoaded("braziliandelight");
if (!BD_LOADED) {
  console.info("[BRAZILIANDELIGHT-INTEGRATION] braziliandelight not installed, skipping trades");
}

const BD_CROP = "shippingbin:crop_sell_multiplier";
const bd = (id) => "braziliandelight:" + id;

const addBd = (list, entries) => {
  if (!BD_LOADED) return;
  entries.forEach(([id, value]) => {
    const item = bd(id);
    list.push({ item: item, value: value });
    global.trades.set(item, {
      value: global.getConfiguredValue(value, "crop"),
      multiplier: BD_CROP,
    });
  });
};

// ===== 作物 / 果实 / 原料（global.crops）=====
addBd(global.crops, [
  ["acai_berries", 24],
  ["guarana_fruit", 32],
  ["lemon", 24],
  ["lemon_slice", 6],
  ["sweet_love_apple", 18],
  ["corn", 16],
  ["cooked_corn", 22],
  ["buttered_corn", 30],
  ["roasted_garlic", 24],
  ["garlic_bulb", 12],
  ["garlic_clove", 4],
  ["collard_greens", 12],
  ["cassava_root", 16],
  ["bean_pod", 8],
  ["kernels", 6],
  ["white_kernels", 6],
  ["coffee_berries", 12],
  ["cassava_flour", 10],
  ["corn_flour", 8],
  ["guarana_powder", 16],
  ["dried_yerba_mate", 12],
  ["yerba_mate_leaves", 12],
  ["tucupi", 16],
  ["salt", 4],
]);

// ===== 水产（global.animalProducts）=====
addBd(global.animalProducts, [
  ["shrimp", 12],
  ["cooked_shrimp", 20],
]);

// ===== 料理 / 甜点 / 饮品（global.cooking）=====
addBd(global.cooking, [
  // 大菜 / 拼盘
  ["brazilian_dinner", 300],
  ["plate_of_feijoada", 260],
  ["plate_of_fish_moqueca", 240],
  ["plate_of_green_soup", 160],
  ["plate_of_stroganoff", 220],
  ["fried_fish_with_acai", 180],
  // 小吃 / 烘焙
  ["coxinha", 60],
  ["raw_coxinha", 30],
  ["cassava_fritters", 50],
  ["raw_cassava_fritters", 20],
  ["cheese_bread", 60],
  ["cheese_bread_dough", 20],
  ["broa", 50],
  ["couscous", 40],
  ["fried_cassava_with_butter", 60],
  ["grilled_cheese_on_a_stick", 50],
  ["minas_cheese_on_a_stick", 60],
  ["collard_greens_farofa", 60],
  ["collard_greens_salad", 50],
  ["salpicao", 90],
  // 豆类
  ["black_beans", 10],
  ["carioca_beans", 10],
  ["cooked_black_beans", 16],
  ["cooked_carioca_beans", 16],
  ["tropeiro_beans", 60],
  // 甜点
  ["brigadeiro_cream", 60],
  ["carrot_cake_slice", 80],
  ["carrot_cake_with_chocolate_slice", 90],
  ["chicken_pot_pie_slice", 100],
  ["pudding_slice", 70],
  ["acai_cream", 60],
  // 奶制品
  ["butter", 40],
  ["condensed_milk", 50],
  ["heavy_cream_bucket", 30],
  ["coconut_cream", 50],
  ["coconut_milk", 30],
  ["minas_cheese_slice", 30],
  // 饮品
  ["coconut_drink", 40],
  ["acai_tea_with_guarana", 50],
  ["chimarrao", 30],
  ["guarana_juice", 50],
  ["guarana_soda", 40],
  ["lemonade", 40],
  ["collard_lemonade", 60],
  ["garapa", 30],
]);
