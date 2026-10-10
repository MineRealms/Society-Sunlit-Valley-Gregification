// priority: 0
// ============================================================
// 巴西乐事（Brazilian Delight）× Sunlit Valley — 营养定义
// 独立注册：即使本模组物品缺失/异常，也不影响 gtmfoNutrients.js 的主批次。
// 依赖：GTMFO 的营养接口 GTMFO.nutrients.addMany({ "item:id": { nutrient: value } })。
// 数值参考：奶 1.0 / 水果 0.75-1.0 / 谷物 0.5-1.0 / 蛋白 1.0-1.75 / 蔬菜 0.5-1.25。
// ============================================================
console.info("[BRAZILIANDELIGHT-INTEGRATION] braziliandelightNutrients.js loaded");

const BD_NUTRIENT_DEFINITIONS = {
  "braziliandelight:acai_berries": { fruit: 1.0 },
  "braziliandelight:guarana_fruit": { fruit: 1.0 },
  "braziliandelight:lemon": { fruit: 0.75 },
  "braziliandelight:sweet_love_apple": { fruit: 1.0 },
  "braziliandelight:corn": { grain: 0.75, vegetable: 0.5 },
  "braziliandelight:cooked_corn": { grain: 0.75, vegetable: 0.75 },
  "braziliandelight:buttered_corn": { grain: 0.75, vegetable: 0.75, dairy: 0.25 },
  "braziliandelight:roasted_garlic": { vegetable: 1.0 },
  "braziliandelight:garlic_bulb": { vegetable: 0.75 },
  "braziliandelight:collard_greens": { vegetable: 1.0 },
  "braziliandelight:collard_greens_farofa": { vegetable: 1.25, grain: 0.5 },
  "braziliandelight:collard_greens_salad": { vegetable: 1.25 },
  "braziliandelight:cassava_root": { grain: 0.75 },
  "braziliandelight:cassava_flour": { grain: 0.5 },
  "braziliandelight:corn_flour": { grain: 0.5 },
  "braziliandelight:bean_pod": { vegetable: 0.5 },
  "braziliandelight:kernels": { grain: 0.5 },
  "braziliandelight:white_kernels": { grain: 0.5 },
  "braziliandelight:coffee_berries": { fruit: 0.5 },
  "braziliandelight:shrimp": { protein: 1.0 },
  "braziliandelight:cooked_shrimp": { protein: 1.25 },
  "braziliandelight:brazilian_dinner": { protein: 1.5, vegetable: 1.0, grain: 0.75 },
  "braziliandelight:plate_of_feijoada": { protein: 1.75, grain: 0.75 },
  "braziliandelight:plate_of_fish_moqueca": { protein: 1.5, vegetable: 0.75 },
  "braziliandelight:plate_of_green_soup": { vegetable: 1.5, protein: 0.5 },
  "braziliandelight:plate_of_stroganoff": { protein: 1.5, grain: 0.5 },
  "braziliandelight:fried_fish_with_acai": { protein: 1.25, fruit: 0.75 },
  "braziliandelight:coxinha": { grain: 0.75, protein: 1.0 },
  "braziliandelight:raw_coxinha": { grain: 0.5, protein: 0.5 },
  "braziliandelight:cassava_fritters": { grain: 0.75 },
  "braziliandelight:raw_cassava_fritters": { grain: 0.5 },
  "braziliandelight:cheese_bread": { grain: 0.75, dairy: 0.5 },
  "braziliandelight:cheese_bread_dough": { grain: 0.5 },
  "braziliandelight:broa": { grain: 0.75 },
  "braziliandelight:couscous": { grain: 1.0 },
  "braziliandelight:fried_cassava_with_butter": { grain: 0.75, dairy: 0.25 },
  "braziliandelight:grilled_cheese_on_a_stick": { dairy: 1.0 },
  "braziliandelight:minas_cheese_on_a_stick": { dairy: 1.0 },
  "braziliandelight:salpicao": { vegetable: 1.0, protein: 0.5 },
  "braziliandelight:black_beans": { grain: 0.5, vegetable: 0.5 },
  "braziliandelight:carioca_beans": { grain: 0.5, vegetable: 0.5 },
  "braziliandelight:cooked_black_beans": { grain: 0.75, protein: 0.5 },
  "braziliandelight:cooked_carioca_beans": { grain: 0.75, protein: 0.5 },
  "braziliandelight:tropeiro_beans": { grain: 0.75, protein: 1.0, vegetable: 0.5 },
  "braziliandelight:brigadeiro_cream": { dairy: 0.75, grain: 0.5 },
  "braziliandelight:carrot_cake_slice": { grain: 0.75, vegetable: 0.25 },
  "braziliandelight:carrot_cake_with_chocolate_slice": { grain: 0.75, vegetable: 0.25 },
  "braziliandelight:chicken_pot_pie_slice": { grain: 0.75, protein: 1.0 },
  "braziliandelight:pudding_slice": { dairy: 0.5, grain: 0.5 },
  "braziliandelight:acai_cream": { fruit: 0.75, dairy: 0.5 },
  "braziliandelight:butter": { dairy: 1.0 },
  "braziliandelight:condensed_milk": { dairy: 1.25 },
  "braziliandelight:heavy_cream_bucket": { dairy: 1.0 },
  "braziliandelight:coconut_cream": { dairy: 0.75, fruit: 0.25 },
  "braziliandelight:coconut_milk": { dairy: 0.5, fruit: 0.25 },
  "braziliandelight:minas_cheese_slice": { dairy: 1.0 },
  "braziliandelight:coconut_drink": { fruit: 0.75 },
  "braziliandelight:acai_tea_with_guarana": { fruit: 0.75 },
  "braziliandelight:chimarrao": { vegetable: 0.5 },
  "braziliandelight:guarana_juice": { fruit: 1.0 },
  "braziliandelight:guarana_soda": { fruit: 0.75 },
  "braziliandelight:lemonade": { fruit: 0.75 },
  "braziliandelight:collard_lemonade": { fruit: 0.5, vegetable: 0.5 },
  "braziliandelight:garapa": { grain: 0.5 },
};

if (Platform.isLoaded("braziliandelight") && typeof GTMFO !== "undefined") {
  console.info("[BRAZILIANDELIGHT-INTEGRATION] nutrient definitions registered: "
    + GTMFO.nutrients.addMany(BD_NUTRIENT_DEFINITIONS));
}
