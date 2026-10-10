// priority: -30
// ============================================================
// 暮色乐事（Twilight Delight）× Sunlit Valley — 经济数据（定价 + 可售）
// 文档：TF_INTEGRATION.md（扩展）/ 本会话设计
//
// 依赖：globalRegistry.js（priority -20）先执行；本脚本 -30 保证其后。
// 效果：自动获得 society:sellable 标签（handleItemBlockFluidTags.js 遍历 global.trades 生成）
//       + 价格 tooltip（addPriceTooltips.js）+ Shipping Bin 售价 + 村民礼物。
// 定价参考（包内同类）：生浆果 4-24 / 生肉 16 / 熟肉 22-32 / 冰淇淋 60 / 三明治 90-200 /
//                       大菜 160-300 / 整蛋糕 200-240。
// ============================================================
console.info("[TWILIGHTDELIGHT-INTEGRATION] twilightdelightTrades.js loaded");

const TD_LOADED = Platform.isLoaded("twilightdelight");
if (!TD_LOADED) {
  console.info("[TWILIGHTDELIGHT-INTEGRATION] twilightdelight not installed, skipping trades");
}

const TD_CROP = "shippingbin:crop_sell_multiplier";
const td = (id) => "twilightdelight:" + id;

const addTd = (list, entries) => {
  if (!TD_LOADED) return;
  entries.forEach(([id, value]) => {
    const item = td(id);
    list.push({ item: item, value: value });
    global.trades.set(item, {
      value: global.getConfiguredValue(value, "crop"),
      multiplier: TD_CROP,
    });
  });
};

// ===== 作物 / 产果（本模组的原料类）=====
addTd(global.crops, [
  ["torchberries_crate", 72],
]);

// ===== 生肉 / 熟肉（global.animalProducts）=====
addTd(global.animalProducts, [
  ["raw_venison_rib", 16],
  ["cooked_venison_rib", 26],
  ["raw_meef_slice", 14],
  ["cooked_meef_slice", 24],
  ["raw_tomahawk_smeak", 18],
  ["cooked_tomahawk_smeak", 30],
  ["grilled_tomahawk_smeak", 40],
  ["hydra_piece", 64],
  ["raw_insect", 4],
  ["fried_insect", 12],
  ["cooked_insect", 12],
]);

// ===== 料理 / 甜点 / 饮品（global.cooking）=====
addTd(global.cooking, [
  // 冰淇淋
  ["aurora_ice_cream", 60],
  ["glacier_ice_cream", 60],
  ["phytochemical_ice_cream", 60],
  ["refreshing_ice_cream", 60],
  ["torchberry_ice_cream", 60],
  ["twilight_ice_cream", 60],
  ["rainbow_ice_cream", 90],
  // 奶昔
  ["aurora_milkshake", 70],
  ["glacier_milkshake", 70],
  ["phytochemical_milkshake", 70],
  ["torchberry_milkshake", 70],
  // 果汁 / 茶
  ["glacier_ice_tea", 50],
  ["phytochemical_juice", 50],
  ["torchberry_juice", 50],
  ["tear_drink", 60],
  ["thorn_rose_tea", 40],
  // 蛋糕 / 派
  ["torchberry_cake", 240],
  ["torchberry_pie", 200],
  ["aurora_cake_slice", 80],
  ["glacier_cake_slice", 80],
  ["phytochemical_cake_slice", 80],
  ["torchberry_cake_slice", 80],
  ["aurora_pie_slice", 90],
  ["torchberry_pie_slice", 80],
  // 主菜 / 大菜
  ["hydra_burger", 260],
  ["ghast_burger", 180],
  ["glowstew", 120],
  ["glow_venison_rib_with_pasta", 200],
  ["grilled_ghast", 160],
  ["meef_wrap", 90],
  ["mushgloom_meef_pasta", 180],
  ["borer_tear_soup", 140],
  ["ghast_brain_salad", 160],
  ["thousand_plant_stew", 220],
  ["plate_of_fiery_snakes", 220],
  ["plate_of_lily_chicken", 240],
  ["plate_of_meef_wellington", 260],
  ["naga_chip", 120],
  ["berry_stick", 40],
  // Experiment / 113 系列（本模组特色）
  ["experiment_110", 30],
  ["experiment_113", 40],
  ["chocolate_113", 30],
  ["glow_113", 40],
  ["honey_113", 20],
  ["milky_113", 20],
  // 零食 / 酱
  ["chocolate_wafer", 20],
  ["torchberry_cookie", 20],
  ["mushgloom_sauce", 30],
]);
