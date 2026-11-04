// priority: 0
// ============================================================
// 神秘视界（Isorropia）× 甜品：巧克力食用属性
//
// 事实依据（源码核对，1.0.0-alpha）：
//  - isorropia:chocolate_cream 本身可食用（营养 3/高饱和），本次追加食用效果
//  - isorropia:chocolate_bar 不可食用（纯材料：9 棒 = 巧克力块）
//  - isorropia:chocolate_milk_bucket = MilkBucketItem（饮下清除效果）
//  - 营养归类：见 gtmfo/gtmfoNutrients.js（乳制品）
//  - tooltip 提示：client_scripts/tooltips/isorropiaFoodTooltips.js
// ============================================================
console.info("[ISO-CHOCO] chocoFood.js loaded");

ItemEvents.foodEaten((event) => {
  if (!Platform.isLoaded("isorropia")) return;
  if (!event.item || event.item.id !== "isorropia:chocolate_cream") return;
  const entity = event.entity;
  if (!entity || !entity.isPlayer()) return;
  entity.potionEffects.add("minecraft:speed", 600, 0, false, true);
  entity.potionEffects.add("minecraft:saturation", 1, 1, false, false);
});
