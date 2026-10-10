// priority: 0
// ============================================================
// 暮色乐事（Twilight Delight）× Sunlit Valley — 营养定义
// 独立注册：与 gtmfoNutrients.js 主批次隔离，即使本模组物品缺失/异常也不拖垮其它。
//
// ⚠️ 现状（2026-10-11）：本包的 twilightdelight 2.0.13 与 FarmersDelight 1.20.1-1.3.2
//    版本不兼容——服务端日志 `twilightdelight.mixins.json:StoveBlockEntityMixin` 超类
//    `SyncedBlockEntity` 找不到，导致其实物物品未注册（配方 result 为空）。
//    在模组修复/换用兼容版本之前，本文件会静默失败并只记一条日志；
//    一旦物品恢复注册，本定义会自动生效。
// 数值参考：奶 0.75-1.0 / 水果 0.5-1.0 / 谷物 0.5-1.0 / 蛋白 1.0-2.0 / 蔬菜 0.5-1.75。
// ============================================================
console.info("[TWILIGHTDELIGHT-INTEGRATION] twilightdelightNutrients.js loaded");

const TD_NUTRIENT_DEFINITIONS = {
  "twilightdelight:raw_venison_rib": { protein: 1.25 },
  "twilightdelight:cooked_venison_rib": { protein: 1.5 },
  "twilightdelight:raw_meef_slice": { protein: 1.0 },
  "twilightdelight:cooked_meef_slice": { protein: 1.25 },
  "twilightdelight:raw_tomahawk_smeak": { protein: 1.25 },
  "twilightdelight:cooked_tomahawk_smeak": { protein: 1.5 },
  "twilightdelight:grilled_tomahawk_smeak": { protein: 1.5 },
  "twilightdelight:hydra_piece": { protein: 2.0 },
  "twilightdelight:raw_insect": { protein: 0.5 },
  "twilightdelight:fried_insect": { protein: 1.0 },
  "twilightdelight:cooked_insect": { protein: 1.0 },
  "twilightdelight:aurora_ice_cream": { dairy: 0.75, fruit: 0.5 },
  "twilightdelight:glacier_ice_cream": { dairy: 0.75, fruit: 0.5 },
  "twilightdelight:phytochemical_ice_cream": { dairy: 0.75, vegetable: 0.5 },
  "twilightdelight:refreshing_ice_cream": { dairy: 0.75, fruit: 0.5 },
  "twilightdelight:torchberry_ice_cream": { dairy: 0.75, fruit: 0.75 },
  "twilightdelight:twilight_ice_cream": { dairy: 0.75, fruit: 0.5 },
  "twilightdelight:rainbow_ice_cream": { dairy: 1.0, fruit: 1.0 },
  "twilightdelight:aurora_milkshake": { dairy: 1.0, fruit: 0.75 },
  "twilightdelight:glacier_milkshake": { dairy: 1.0, fruit: 0.75 },
  "twilightdelight:phytochemical_milkshake": { dairy: 1.0, vegetable: 0.5 },
  "twilightdelight:torchberry_milkshake": { dairy: 1.0, fruit: 1.0 },
  "twilightdelight:glacier_ice_tea": { fruit: 0.75 },
  "twilightdelight:phytochemical_juice": { fruit: 0.5, vegetable: 0.5 },
  "twilightdelight:torchberry_juice": { fruit: 1.0 },
  "twilightdelight:tear_drink": { protein: 0.5 },
  "twilightdelight:thorn_rose_tea": { vegetable: 0.5 },
  "twilightdelight:torchberry_cake": { grain: 1.0, fruit: 1.0, dairy: 0.5 },
  "twilightdelight:torchberry_pie": { grain: 1.0, fruit: 1.0 },
  "twilightdelight:aurora_cake_slice": { grain: 0.75, fruit: 0.5 },
  "twilightdelight:glacier_cake_slice": { grain: 0.75, fruit: 0.5 },
  "twilightdelight:phytochemical_cake_slice": { grain: 0.75, vegetable: 0.5 },
  "twilightdelight:torchberry_cake_slice": { grain: 0.75, fruit: 0.75 },
  "twilightdelight:aurora_pie_slice": { grain: 0.75, fruit: 0.75 },
  "twilightdelight:torchberry_pie_slice": { grain: 0.75, fruit: 0.75 },
  "twilightdelight:hydra_burger": { grain: 1.0, protein: 2.0 },
  "twilightdelight:ghast_burger": { grain: 0.75, protein: 1.5 },
  "twilightdelight:glowstew": { protein: 1.0, vegetable: 1.0 },
  "twilightdelight:glow_venison_rib_with_pasta": { grain: 1.0, protein: 1.5 },
  "twilightdelight:grilled_ghast": { protein: 1.75 },
  "twilightdelight:meef_wrap": { grain: 0.75, protein: 1.25 },
  "twilightdelight:mushgloom_meef_pasta": { grain: 1.0, protein: 1.5, vegetable: 0.5 },
  "twilightdelight:borer_tear_soup": { protein: 1.0, vegetable: 0.75 },
  "twilightdelight:ghast_brain_salad": { protein: 1.25, vegetable: 0.5 },
  "twilightdelight:thousand_plant_stew": { vegetable: 1.75 },
  "twilightdelight:plate_of_fiery_snakes": { protein: 1.75, vegetable: 1.0 },
  "twilightdelight:plate_of_lily_chicken": { protein: 1.5, vegetable: 1.0, grain: 0.5 },
  "twilightdelight:plate_of_meef_wellington": { grain: 1.0, protein: 1.75 },
  "twilightdelight:naga_chip": { vegetable: 1.0, grain: 0.5 },
  "twilightdelight:berry_stick": { fruit: 0.75, grain: 0.5 },
  "twilightdelight:experiment_110": { protein: 1.0 },
  "twilightdelight:experiment_113": { protein: 1.25 },
  "twilightdelight:chocolate_113": { grain: 0.75, dairy: 0.25 },
  "twilightdelight:glow_113": { fruit: 0.75 },
  "twilightdelight:honey_113": { fruit: 0.75 },
  "twilightdelight:milky_113": { dairy: 1.0 },
  "twilightdelight:chocolate_wafer": { grain: 0.5, dairy: 0.25 },
  "twilightdelight:torchberry_cookie": { grain: 0.5, fruit: 0.5 },
  "twilightdelight:mushgloom_sauce": { vegetable: 0.5 },
};

// 只在模组物品确实已注册时才登记（用哨兵物品探测，避免未知 id 让本批次报错）。
if (Platform.isLoaded("twilightdelight") && typeof GTMFO !== "undefined"
    && Ingredient.of("twilightdelight:aurora_ice_cream").itemIds.size() > 0) {
  console.info("[TWILIGHTDELIGHT-INTEGRATION] nutrient definitions registered: "
    + GTMFO.nutrients.addMany(TD_NUTRIENT_DEFINITIONS));
} else {
  console.info("[TWILIGHTDELIGHT-INTEGRATION] twilightdelight items not registered; nutrient defs skipped");
}
