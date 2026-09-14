// priority: 0
// ============================================================
// GregTech 矿脉注入：暮色森林 + 骷髅洞穴
//
// 数据来源：GTCEu 官方 GTOres.java（1.20.1 主世界石/深板岩矿脉）
//   - 暮色森林（min_y=-32, height=288）：深层矿脉整体 +20 后夹取到 [-31, 250]
//   - 骷髅洞穴（min_y=0, height=512）：主世界 Y + 64 后夹取到 [4, 500]
//
// 世界生成层：startup_scripts/gt/worldGenLayers.js
// 依赖：gtceu 7.5.3（GTCEuServerEvents.oreVeins）
// 说明：仅影响新生成区块；已探索区块不会补矿
// ============================================================
console.info("[GT-ORES] oreVeins.js loaded")

const $UniformInt = Java.loadClass("net.minecraft.util.valueproviders.UniformInt")

// 维度配置：layer 对应 worldGenLayers.js 中注册的层名
const GT_ORE_DIMENSIONS = [
  {
    key: "tf",
    layer: "twilight_forest",
    // 暮色森林：min_y=-32, height=288
    remap: (y, deep) => Math.max(-31, Math.min(250, y + (deep ? 20 : 0))),
  },
  {
    key: "skull",
    layer: "skull_cavern",
    // 骷髅洞穴：min_y=0, height=512（整体上移 64）
    remap: (y, deep) => Math.max(4, Math.min(500, y + 64)),
  },
]

// 矿脉表（镜像 GTCEu 默认主世界矿脉；deep=true 表示深板岩层矿脉）
// size: [min,max]  clusterSize；height: [min,max] 主世界 Y 范围
// gen: (vein, remap) => 配置生成器；remap(y) 用于 dike 矿脉的绝对 Y
// indicator: 地表指示矿（GTMaterials.*）；placement 缺省为 surface
const GT_ORE_VEINS = [
  // ---------------- 石头层 ----------------
  {
    name: "apatite", weight: 40, density: 0.25, size: [32, 40], height: [10, 80], deep: false,
    indicator: GTMaterials.Apatite,
    gen: vein => vein.layeredVeinGenerator(g => g.buildLayerPattern(p => {
      p.layer(l => l.weight(3).mat(GTMaterials.Apatite).size(2, 4))
      p.layer(l => l.weight(2).mat(GTMaterials.TricalciumPhosphate).size(1, 1))
      p.layer(l => l.weight(1).mat(GTMaterials.Pyrochlore).size(1, 1))
    })),
  },
  {
    name: "cassiterite", weight: 80, density: 1.0, size: [40, 52], height: [10, 80], deep: false,
    indicator: GTMaterials.Cassiterite,
    gen: vein => vein.veinedVeinGenerator(g => {
      g.oreBlock(GTMaterials.Tin, 4)
      g.rareBlock(GTMaterials.Cassiterite, 2)
      g.rareBlockChance(0.33)
      g.veininessThreshold(0.01)
      g.maxRichnessThreshold(0.175)
      g.minRichness(0.7)
      g.maxRichness(1.0)
      g.edgeRoundoffBegin(3)
      g.maxEdgeRoundoff(0.1)
    }),
  },
  {
    name: "coal", weight: 80, density: 0.25, size: [38, 44], height: [10, 140], deep: false,
    indicator: GTMaterials.Coal,
    gen: vein => vein.layeredVeinGenerator(g => g.buildLayerPattern(p => {
      p.layer(l => l.weight(3).mat(GTMaterials.Coal).size(2, 4))
    })),
  },
  {
    name: "copper_tin", weight: 50, density: 1.0, size: [40, 52], height: [-10, 160], deep: false,
    indicator: GTMaterials.Chalcopyrite,
    gen: vein => vein.veinedVeinGenerator(g => {
      g.oreBlock(GTMaterials.Chalcopyrite, 5)
      g.oreBlock(GTMaterials.Zeolite, 2)
      g.oreBlock(GTMaterials.Cassiterite, 2)
      g.rareBlock(GTMaterials.Realgar, 1)
      g.rareBlockChance(0.1)
      g.veininessThreshold(0.01)
      g.maxRichnessThreshold(0.175)
      g.minRichness(0.7)
      g.maxRichness(1.0)
      g.edgeRoundoffBegin(3)
      g.maxEdgeRoundoff(0.1)
    }),
  },
  {
    name: "galena", weight: 40, density: 0.25, size: [32, 40], height: [-15, 45], deep: false,
    indicator: GTMaterials.Galena,
    gen: vein => vein.layeredVeinGenerator(g => g.buildLayerPattern(p => {
      p.layer(l => l.weight(3).mat(GTMaterials.Galena).size(2, 4))
      p.layer(l => l.weight(2).mat(GTMaterials.Silver).size(1, 1))
      p.layer(l => l.weight(1).mat(GTMaterials.Lead).size(1, 1))
    })),
  },
  {
    name: "garnet_tin", weight: 80, density: 0.4, size: [32, 40], height: [30, 60], deep: false,
    indicator: GTMaterials.GarnetSand,
    gen: vein => vein.layeredVeinGenerator(g => g.buildLayerPattern(p => {
      p.layer(l => l.weight(3).mat(GTMaterials.CassiteriteSand).size(2, 4))
      p.layer(l => l.weight(2).mat(GTMaterials.GarnetSand).size(1, 1))
      p.layer(l => l.weight(2).mat(GTMaterials.Asbestos).size(1, 1))
      p.layer(l => l.weight(1).mat(GTMaterials.Diatomite).size(1, 1))
    })),
  },
  {
    name: "garnet", weight: 40, density: 0.75, size: [50, 64], height: [-10, 50], deep: false,
    indicator: GTMaterials.GarnetRed, placement: "above",
    gen: (vein, remap) => vein.dikeVeinGenerator(g => {
      g.withBlock(GTMaterials.GarnetRed, 3, remap(-10), remap(50))
      g.withBlock(GTMaterials.GarnetYellow, 2, remap(-10), remap(50))
      g.withBlock(GTMaterials.Amethyst, 2, remap(-10), remap(22))
      g.withBlock(GTMaterials.Opal, 1, remap(18), remap(50))
    }),
  },
  {
    name: "iron", weight: 120, density: 1.0, size: [40, 52], height: [-10, 60], deep: false,
    indicator: GTMaterials.Goethite,
    gen: vein => vein.veinedVeinGenerator(g => {
      g.oreBlock(GTMaterials.Goethite, 5)
      g.oreBlock(GTMaterials.Limonite, 2)
      g.oreBlock(GTMaterials.Hematite, 2)
      g.oreBlock(GTMaterials.Malachite, 1)
      g.veininessThreshold(0.01)
      g.maxRichnessThreshold(0.175)
      g.minRichness(0.7)
      g.maxRichness(1.0)
      g.edgeRoundoffBegin(3)
      g.maxEdgeRoundoff(0.1)
    }),
  },
  {
    name: "lubricant", weight: 40, density: 0.25, size: [25, 29], height: [0, 50], deep: false,
    indicator: GTMaterials.Talc,
    gen: vein => vein.layeredVeinGenerator(g => g.buildLayerPattern(p => {
      p.layer(l => l.weight(3).mat(GTMaterials.Soapstone).size(2, 4))
      p.layer(l => l.weight(2).mat(GTMaterials.Talc).size(1, 1))
      p.layer(l => l.weight(2).mat(GTMaterials.GlauconiteSand).size(1, 1))
      p.layer(l => l.weight(1).mat(GTMaterials.Pentlandite).size(1, 1))
    })),
  },
  {
    name: "magnetite", weight: 80, density: 0.15, size: [38, 44], height: [10, 60], deep: false,
    indicator: GTMaterials.Magnetite,
    gen: vein => vein.layeredVeinGenerator(g => g.buildLayerPattern(p => {
      p.layer(l => l.weight(3).mat(GTMaterials.Magnetite).size(2, 4))
      p.layer(l => l.weight(2).mat(GTMaterials.VanadiumMagnetite).size(1, 1))
      p.layer(l => l.weight(1).mat(GTMaterials.Gold).size(1, 1))
    })),
  },
  {
    name: "mineral_sand", weight: 80, density: 0.2, size: [32, 40], height: [15, 60], deep: false,
    indicator: GTMaterials.BasalticMineralSand,
    gen: vein => vein.layeredVeinGenerator(g => g.buildLayerPattern(p => {
      p.layer(l => l.weight(3).mat(GTMaterials.BasalticMineralSand).size(2, 4))
      p.layer(l => l.weight(2).mat(GTMaterials.GraniticMineralSand).size(1, 1))
      p.layer(l => l.weight(2).mat(GTMaterials.FullersEarth).size(1, 1))
      p.layer(l => l.weight(1).mat(GTMaterials.Gypsum).size(1, 1))
    })),
  },
  {
    name: "nickel", weight: 40, density: 0.25, size: [32, 40], height: [-10, 60], deep: false,
    indicator: GTMaterials.Nickel,
    gen: vein => vein.layeredVeinGenerator(g => g.buildLayerPattern(p => {
      p.layer(l => l.weight(3).mat(GTMaterials.Garnierite).size(2, 4))
      p.layer(l => l.weight(2).mat(GTMaterials.Nickel).size(1, 1))
      p.layer(l => l.weight(2).mat(GTMaterials.Cobaltite).size(1, 1))
      p.layer(l => l.weight(1).mat(GTMaterials.Pentlandite).size(1, 1))
    })),
  },
  {
    name: "salts", weight: 50, density: 0.2, size: [32, 40], height: [30, 70], deep: false,
    indicator: GTMaterials.Salt,
    gen: vein => vein.layeredVeinGenerator(g => g.buildLayerPattern(p => {
      p.layer(l => l.weight(3).mat(GTMaterials.RockSalt).size(2, 4))
      p.layer(l => l.weight(2).mat(GTMaterials.Salt).size(1, 1))
      p.layer(l => l.weight(1).mat(GTMaterials.Lepidolite).size(1, 1))
      p.layer(l => l.weight(1).mat(GTMaterials.Spodumene).size(1, 1))
    })),
  },
  {
    name: "oilsands", weight: 40, density: 0.3, size: [25, 29], height: [30, 80], deep: false,
    indicator: GTMaterials.Oilsands,
    gen: vein => vein.layeredVeinGenerator(g => g.buildLayerPattern(p => {
      p.layer(l => l.weight(3).mat(GTMaterials.Oilsands).size(2, 4))
      p.layer(l => l.weight(2).mat(GTMaterials.Oilsands).size(1, 1))
      p.layer(l => l.weight(1).mat(GTMaterials.Oilsands).size(1, 1))
      p.layer(l => l.weight(1).mat(GTMaterials.Oilsands).size(1, 1))
    })),
  },
  // ---------------- 深板岩层 ----------------
  {
    name: "copper", weight: 80, density: 1.0, size: [40, 52], height: [-40, 10], deep: true,
    indicator: GTMaterials.Copper,
    gen: vein => vein.veinedVeinGenerator(g => {
      g.oreBlock(GTMaterials.Chalcopyrite, 5)
      g.oreBlock(GTMaterials.Iron, 2)
      g.oreBlock(GTMaterials.Pyrite, 2)
      g.oreBlock(GTMaterials.Copper, 2)
      g.veininessThreshold(0.01)
      g.maxRichnessThreshold(0.175)
      g.minRichness(0.7)
      g.maxRichness(1.0)
      g.edgeRoundoffBegin(3)
      g.maxEdgeRoundoff(0.1)
    }),
  },
  {
    name: "diamond", weight: 40, density: 0.25, size: [32, 40], height: [-55, -30], deep: true,
    indicator: GTMaterials.Diamond, placement: "above", indicatorDensity: 0.1, indicatorRadius: 2,
    gen: vein => vein.classicVeinGenerator(g => {
      g.primary(b => b.mat(GTMaterials.Graphite).size(4))
      g.secondary(b => b.mat(GTMaterials.Graphite).size(3))
      g.between(b => b.mat(GTMaterials.Diamond).size(3))
      g.sporadic(b => b.mat(GTMaterials.Coal).size(1))
    }),
  },
  {
    name: "lapis", weight: 40, density: 0.75, size: [40, 52], height: [-60, 10], deep: true,
    indicator: GTMaterials.Lapis, placement: "above", indicatorDensity: 0.15, indicatorRadius: 3,
    gen: (vein, remap) => vein.dikeVeinGenerator(g => {
      g.withBlock(GTMaterials.Lazurite, 3, remap(-60), remap(10))
      g.withBlock(GTMaterials.Sodalite, 2, remap(-50), remap(0))
      g.withBlock(GTMaterials.Lapis, 2, remap(-50), remap(0))
      g.withBlock(GTMaterials.Calcite, 1, remap(-40), remap(10))
    }),
  },
  {
    name: "manganese", weight: 20, density: 0.75, size: [50, 64], height: [-30, 0], deep: true,
    indicator: GTMaterials.Grossular, indicatorDensity: 0.15, indicatorRadius: 3,
    gen: (vein, remap) => vein.dikeVeinGenerator(g => {
      g.withBlock(GTMaterials.Grossular, 3, remap(-50), remap(-5))
      g.withBlock(GTMaterials.Spessartine, 2, remap(-40), remap(-15))
      g.withBlock(GTMaterials.Pyrolusite, 2, remap(-40), remap(-15))
      g.withBlock(GTMaterials.Tantalite, 1, remap(-30), remap(-5))
    }),
  },
  {
    name: "mica", weight: 20, density: 0.25, size: [32, 40], height: [-40, -10], deep: true,
    indicator: GTMaterials.Mica, indicatorRadius: 3,
    gen: vein => vein.layeredVeinGenerator(g => g.buildLayerPattern(p => {
      p.layer(l => l.weight(3).mat(GTMaterials.Kyanite).size(2, 4))
      p.layer(l => l.weight(2).mat(GTMaterials.Mica).size(1, 1))
      p.layer(l => l.weight(2).mat(GTMaterials.Bauxite).size(1, 1))
      p.layer(l => l.weight(1).mat(GTMaterials.Pollucite).size(1, 1))
    })),
  },
  {
    name: "olivine", weight: 20, density: 0.25, size: [32, 40], height: [-20, 10], deep: true,
    indicator: GTMaterials.Olivine, indicatorDensity: 0.15, indicatorRadius: 3,
    gen: vein => vein.layeredVeinGenerator(g => g.buildLayerPattern(p => {
      p.layer(l => l.weight(3).mat(GTMaterials.Bentonite).size(2, 4))
      p.layer(l => l.weight(2).mat(GTMaterials.Magnesite).size(1, 1))
      p.layer(l => l.weight(2).mat(GTMaterials.Olivine).size(1, 1))
      p.layer(l => l.weight(1).mat(GTMaterials.GlauconiteSand).size(1, 1))
    })),
  },
  {
    name: "redstone", weight: 60, density: 0.2, size: [32, 40], height: [-65, -10], deep: true,
    indicator: GTMaterials.Redstone,
    gen: vein => vein.layeredVeinGenerator(g => g.buildLayerPattern(p => {
      p.layer(l => l.weight(3).mat(GTMaterials.Redstone).size(2, 4))
      p.layer(l => l.weight(2).mat(GTMaterials.Ruby).size(1, 1))
      p.layer(l => l.weight(1).mat(GTMaterials.Cinnabar).size(1, 1))
    })),
  },
  {
    name: "sapphire", weight: 60, density: 0.25, size: [25, 29], height: [-40, 0], deep: true,
    indicator: GTMaterials.Sapphire, placement: "above", indicatorDensity: 0.15, indicatorRadius: 3,
    gen: vein => vein.layeredVeinGenerator(g => g.buildLayerPattern(p => {
      p.layer(l => l.weight(3).mat(GTMaterials.Almandine).size(2, 4))
      p.layer(l => l.weight(2).mat(GTMaterials.Pyrope).size(1, 1))
      p.layer(l => l.weight(1).mat(GTMaterials.Sapphire).size(1, 1))
      p.layer(l => l.weight(1).mat(GTMaterials.GreenSapphire).size(1, 1))
    })),
  },
]

GTCEuServerEvents.oreVeins(event => {
  GT_ORE_DIMENSIONS.forEach(dim => {
    const remap = y => dim.remap(y, false)
    const remapDeep = y => dim.remap(y, true)

    GT_ORE_VEINS.forEach(v => {
      event.add(`kubejs:${dim.key}_${v.name}_vein`, vein => {
        vein.weight(v.weight)
        vein.density(v.density)
        vein.clusterSize($UniformInt.of(v.size[0], v.size[1]))
        vein.layer(dim.layer)
        vein.heightRangeUniform(
          v.deep ? remapDeep(v.height[0]) : remap(v.height[0]),
          v.deep ? remapDeep(v.height[1]) : remap(v.height[1])
        )
        v.gen(vein, v.deep ? remapDeep : remap)

        if (v.indicator) {
          vein.surfaceIndicatorGenerator(indicator => {
            indicator.surfaceRock(v.indicator)
            if (v.placement) indicator.placement(v.placement)
            if (v.indicatorDensity) indicator.density(v.indicatorDensity)
            if (v.indicatorRadius) indicator.radius(v.indicatorRadius)
          })
        }
      })
    })
  })
  console.info(`[GT-ORES] registered ${GT_ORE_VEINS.length * GT_ORE_DIMENSIONS.length} veins for ${GT_ORE_DIMENSIONS.length} dimensions`)
})
