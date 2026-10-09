// priority: 0
// 暮色森林 × Sunlit Valley — 季节（C）：TF 树苗/植物纳入 Serene Seasons 季节标签
// 依据：Serene Seasons 使用 sereneseasons:{spring,summer,autumn,winter,year_round}_crops 方块标签控制生长；
//       温室玻璃（sereneseasons:greenhouse_glass）随之对 TF 作物生效（原生逻辑，无需改）
// 参考包内既有分配：spring 含 birch/spruce/cherry 树苗；summer 含 jungle/acacia 树苗；winter 含 spruce/sweet_berry_bush
console.info("[TF-INTEGRATION] tfSeasonsTags.js loaded (C seasons)");

ServerEvents.tags("block", (e) => {
  if (!Platform.isLoaded("twilightforest")) return;

  e.add("sereneseasons:spring_crops", [
    "twilightforest:twilight_oak_sapling",
    "twilightforest:hollow_oak_sapling",
    "twilightforest:rainbow_oak_sapling",
  ]);
  e.add("sereneseasons:summer_crops", [
    "twilightforest:canopy_sapling",
    "twilightforest:mangrove_sapling",
  ]);
  e.add("sereneseasons:autumn_crops", [
    "twilightforest:darkwood_sapling",
    "twilightforest:mayapple",
    "twilightforest:fiddlehead",
  ]);
  e.add("sereneseasons:year_round_crops", [
    "twilightforest:time_sapling",
    "twilightforest:transformation_sapling",
    "twilightforest:mining_sapling",
    "twilightforest:sorting_sapling",
    "twilightforest:mushgloom",
    "twilightforest:torchberry_plant",
    "twilightforest:moss_patch",
    "twilightforest:clover_patch",
    "twilightforest:root_strand",
    "twilightforest:fallen_leaves",
  ]);
});
