// priority: 10
// ============================================================
// GregTech 矿脉改道：HV 材料只去暮色森林，主世界不生成
//
// 末地来源（bauxite / magnetite）→ 新建暮色森林副本并移除末地原版
// 主世界来源（magnetite_ow / nickel / manganese_ow / olivine）→ 移除主世界原版
//   （暮色森林副本已由 oreVeins.js 注册）
//
// 说明：
//   - 只影响新生成区块；已探索区块不会补矿
//   - 被移走的矿脉不再在末地/主世界生成
//   - 岩层：oreVeins.js 的 twilight_forest 层
// ============================================================
console.info("[GT-ORES] tfHvOreVeins.js loaded")

const $UniformInt = Java.loadClass("net.minecraft.util.valueproviders.UniformInt")

// 末地 HV 矿脉的暮色森林副本（去掉宿主层，由 twilight_forest 层决定宿主）
const TF_END_VEINS = [
  {
    name: "tf_bauxite_vein", weight: 40, density: 0.3, size: [32, 40], height: [10, 80],
    indicator: GTMaterials.Bauxite,
    gen: vein => vein.layeredVeinGenerator(g => g.buildLayerPattern(p => {
      p.layer(l => l.weight(2).mat(GTMaterials.Bauxite).size(1, 4))
      p.layer(l => l.weight(1).mat(GTMaterials.Ilmenite).size(1, 2))
      p.layer(l => l.weight(1).mat(GTMaterials.Aluminium).size(1, 1))
    })),
  },
  {
    name: "tf_magnetite_end_vein", weight: 30, density: 0.15, size: [38, 44], height: [20, 80],
    indicator: GTMaterials.Magnetite,
    gen: vein => vein.layeredVeinGenerator(g => g.buildLayerPattern(p => {
      p.layer(l => l.weight(3).mat(GTMaterials.Magnetite).size(2, 4))
      p.layer(l => l.weight(2).mat(GTMaterials.VanadiumMagnetite).size(1, 1))
      p.layer(l => l.weight(2).mat(GTMaterials.Chromite).size(1, 1))
      p.layer(l => l.weight(1).mat(GTMaterials.Gold).size(1, 1))
    })),
  },
]

GTCEuServerEvents.oreVeins(event => {
  TF_END_VEINS.forEach(v => {
    event.add(`kubejs:${v.name}`, vein => {
      vein.weight(v.weight)
      vein.density(v.density)
      vein.clusterSize($UniformInt.of(v.size[0], v.size[1]))
      vein.layer("twilight_forest")
      vein.heightRangeUniform(v.height[0], v.height[1])
      v.gen(vein)
      if (v.indicator) {
        vein.surfaceIndicatorGenerator(indicator => indicator.surfaceRock(v.indicator))
      }
    })
  })

  // 移除原版：末地 HV 矿脉 + 主世界 HV 矿脉
  event.remove("gtceu:bauxite_vein_end")
  event.remove("gtceu:magnetite_vein_end")
  event.remove("gtceu:magnetite_vein_ow")
  event.remove("gtceu:nickel_vein")
  event.remove("gtceu:manganese_vein_ow")
  event.remove("gtceu:olivine_vein")

  console.info("[GT-ORES] HV veins moved to Twilight Forest")
})
