// priority: -30
// ============================================================
// 暮色森林 × Sunlit Valley — 经济（A）：农产品 / 肉类 / 木材 / 材料上架
// 进度文档：TF_INTEGRATION.md
//
// 机制（包内先例 gtmfoTrades.js 同款）：
//  - push 到 global 列表（客户端价格 tooltip 与分类系统读取）
//  - global.trades.set(item, { value, multiplier })（Shipping Bin 售价与 society:sellable 标签来源）
//  - priority -30：晚于 globalRegistry.js（-20）执行
//
// 数值平衡基准（包内同类）：
//  - 浆果：sweet_berries 4 / cranberry 18 / blueberry 24；生肉 beef 16；熟肉 cooked_porkchop 32
//  - 原木 2（artisanGoods）；皮革 8 / 兔皮 12 / 羽毛 16 / 鸭羽 64
// ============================================================
console.info("[TF-INTEGRATION] tfTrades.js loaded (A trades)");

const TF_LOADED = Platform.isLoaded("twilightforest");
if (!TF_LOADED) {
  console.info("[TF-INTEGRATION] twilightforest not installed, skipping trades (A)");
}

const CROP = "shippingbin:crop_sell_multiplier";
const WOOD = "shippingbin:wood_sell_multiplier";
const TF_GEM = "shippingbin:gem_sell_multiplier";

const addTfTrades = (list, kind, multiplier, entries) => {
  if (!TF_LOADED) return;
  entries.forEach(([id, value]) => {
    const item = "twilightforest:" + id;
    list.push({ item: item, value: value });
    global.trades.set(item, {
      value: global.getConfiguredValue(value, kind),
      multiplier: multiplier,
    });
  });
};

// ===== 作物（农夫产品）：浆果 / 蘑菇 / 块根 =====
addTfTrades(global.crops, "crop", CROP, [
  ["torchberries", 12],
  ["mushgloom", 16],
  ["trollber", 24],
  ["unripe_trollber", 8],
  ["magic_beans", 64],
  ["liveroot", 12],
  ["mayapple", 8],
  ["fiddlehead", 8],
]);

// ===== 畜产 / 肉类 / 魔法食物（沿用动物产品分类）=====
addTfTrades(global.animalProducts, "crop", CROP, [
  ["raw_venison", 16],
  ["cooked_venison", 24],
  ["raw_meef", 14],
  ["cooked_meef", 22],
  ["meef_stroganoff", 48],
  ["hydra_chop", 96],
  ["maze_wafer", 12],
  ["experiment_115", 48],
  ["raven_feather", 24],
  ["arctic_fur", 32],
  ["alpha_yeti_fur", 128],
  ["naga_scale", 64],
]);

// ===== 木材（工匠产品）：普通原木 2 / 魔法原木 4 =====
addTfTrades(global.artisanGoods, "wood", WOOD, [
  ["twilight_oak_log", 2],
  ["canopy_log", 2],
  ["mangrove_log", 2],
  ["dark_log", 2],
  ["hollow_oak_log", 2],
  ["time_log", 4],
  ["transformation_log", 4],
  ["mining_log", 4],
  ["sorting_log", 4],
  ["giant_log", 4],
  ["stripped_twilight_oak_log", 2],
  ["stripped_canopy_log", 2],
  ["stripped_mangrove_log", 2],
  ["stripped_dark_log", 2],
]);

// ===== 材料（地质学家）：树产金属与甲片 =====
addTfTrades(global.miscGeologist, "gem", TF_GEM, [
  ["ironwood_ingot", 20],
  ["steeleaf_ingot", 24],
  ["knightmetal_ingot", 48],
  ["armor_shard", 12],
]);
