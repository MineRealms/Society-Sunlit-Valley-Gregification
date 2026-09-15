// priority: -30
// ============================================================
// TC4（神秘时代）× Sunlit Valley — 经济 R1：Shipping Bin 收购价
// 进度文档：TC4_INTEGRATION.md 第 7.5 节
//
// 机制（包内先例 gtmfoTrades.js 同款）：
//  - global.trades.set(item, { value, multiplier })
//  - handleItemBlockFluidTags.js:627-646 自动为 global.trades 内物品添加 society:sellable
//  - multiplier 仅四种：shippingbin:{crop,gem,wood,meat}_sell_multiplier
//    （switch 映射：gem=地质学家 / meat=冒险家 / wood=工匠 / crop=农夫）
//  - priority -30：晚于 globalRegistry.js（-20）执行，保证 global.trades 已定义
// ============================================================
console.info("[TC4-INTEGRATION] tc4Trades.js loaded (shipping bin)");

const TC4_LOADED = Platform.isLoaded("thaumcraft");
if (!TC4_LOADED) {
  console.info("[TC4-INTEGRATION] thaumcraft mod not installed, skipping trades (R1)");
}

const GEM = "shippingbin:gem_sell_multiplier";
const ADV = "shippingbin:meat_sell_multiplier";

const addTcTrades = (kind, multiplier, entries) => {
  if (!TC4_LOADED) return;
  entries.forEach(([id, value]) => {
    const item = "thaumcraft:" + id;
    global.trades.set(item, {
      value: global.getConfiguredValue(value, kind),
      multiplier: multiplier,
    });
  });
};

// 矿物类（地质学家）：琥珀 / 水银 / 辰砂 / 神秘锭 / 虚空锭
addTcTrades("gem", GEM, [
  ["amber", 24],
  ["quicksilver", 32],
  ["cinnabar_ore", 16],
  ["native_cinnabar_cluster", 24],
  ["thaumium_ingot", 96],
  ["void_ingot", 160],
]);

// 冒险类（冒险家）：六系碎片 / 均衡碎片 / 炼金煤
addTcTrades("meat", ADV, [
  ["air_shard", 8],
  ["fire_shard", 8],
  ["earth_shard", 8],
  ["water_shard", 8],
  ["order_shard", 8],
  ["entropy_shard", 8],
  ["balanced_shard", 48],
  ["alumentum", 12],
]);
