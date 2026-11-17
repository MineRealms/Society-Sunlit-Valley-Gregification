// priority: 0
// ============================================================
// GregTech / 全包矿物生成 Dump（KubeJS 版）
//
// 启动时自动把矿物世界生成数据打到 KubeJS 日志（logs/kubejs/server.log）：
//   摘要 + DIMENSIONS + GTCEU_VEINS + PLACED_FEATURES
// 手动执行 /oregendump 会额外输出 BIOME_MODIFIERS 与 ITEM_TAGS。
//
// 覆盖四层数据源：
//   1) GTCEU ORE_VEINS（代码注册的矿脉）
//   2) 全部 placed_feature 中的矿石类 feature（含 Y 范围、数量、宿主方块）
//   3) Forge biome_modifier（add_features 等）
//   4) forge:ores / raw_materials / dusts / ingots 标签成员
//   5) 维度 min_y / height 等参数
//
// 说明：
//   - KubeJS class filter 禁止 java.nio/java.io，文件写入可能不可用；本脚本以日志输出为主。
//   - 整个脚本包在 IIFE 里，避免顶层 const/let 与别的脚本（如 seasonSync.js 的 const data）冲突。
//   - 只读操作，不改任何世界生成。
// ============================================================
(function () {
  console.info("[GT-ORES] dumpOreGen.js loaded")

  const $GTRegistries = Java.loadClass("com.gregtechceu.gtceu.api.registry.GTRegistries")
  const $Registries = Java.loadClass("net.minecraft.core.registries.Registries")
  const $BuiltInRegistries = Java.loadClass("net.minecraft.core.registries.BuiltInRegistries")
  const $JsonOps = Java.loadClass("com.mojang.serialization.JsonOps")
  const $HeightRangePlacement = Java.loadClass("net.minecraft.world.level.levelgen.placement.HeightRangePlacement")
  const $PlacementModifier = Java.loadClass("net.minecraft.world.level.levelgen.placement.PlacementModifier")
  const $ForgeRegistries = Java.loadClass("net.minecraftforge.registries.ForgeRegistries")
  const $Component = Java.loadClass("net.minecraft.network.chat.Component")
  const $Commands = Java.loadClass("net.minecraft.commands.Commands")

  // KubeJS 的 class filter 默认禁止 java.nio / java.io，所以文件写入在部分环境不可用。
  let $Files = null
  let $StandardCharsets = null
  try {
    $Files = Java.loadClass("java.nio.file.Files")
    $StandardCharsets = Java.loadClass("java.nio.charset.StandardCharsets")
  } catch (err) {
    console.warn('[GT-ORES] file IO disabled by class filter, dump goes to log only: ' + err)
  }

  // 把一个 codec 编码成 JS 对象（失败返回 null）
  function encodeObject(codec, value) {
    try {
      const result = codec.encodeStart($JsonOps.INSTANCE, value).result()
      if (result.isPresent()) {
        const text = result.get().toString()
        try { return JSON.parse(text) } catch (err) { return text }
      }
    } catch (err) { return null }
    return null
  }

  function holderId(holder) {
    if (!holder) return null
    try {
      if (holder.unwrapKey().isPresent()) return holder.unwrapKey().get().location().toString()
    } catch (err) {}
    return null
  }

  function dumpOres(server) {
    const ra = server.registryAccess()
    const out = { timestamp: new Date().toISOString() }

    // ---- 维度 ----
    out.dimensions = []
    try {
      const stems = ra.registryOrThrow($Registries.LEVEL_STEM)
      stems.entrySet().forEach(e => {
        const dt = e.getValue().type().value()
        out.dimensions.push({
          id: e.getKey().location().toString(),
          min_y: dt.minY(), height: dt.height(), logical_height: dt.logicalHeight(),
          has_skylight: dt.hasSkyLight(), natural: dt.natural(),
          has_ceiling: dt.hasCeiling(), coordinate_scale: dt.coordinateScale()
        })
      })
    } catch (err) { out.dimensions.push({ error: String(err) }) }

    // ---- GTCEU 矿脉 ----
    out.gtceu_veins = []
    try {
      const oreRegistry = $GTRegistries.ORE_VEINS
      for (const def of oreRegistry) {
        let layer = def.layer()
        let oreId = oreRegistry.getKey(def)
        let v = {
          id: oreId == null ? 'unknown' : oreId.toString(),
          layer: layer ? layer.getSerializedName() : 'null',
          layer_levels: [],
          dimensions: [],
          biomes: [],
          height_range: encodeObject($HeightRangePlacement.CODEC, def.range()),
          cluster_min: def.clusterSize().getMinValue(),
          cluster_max: def.clusterSize().getMaxValue(),
          density: def.density(),
          weight: def.weight(),
          discard_chance_on_air_exposure: def.discardChanceOnAirExposure(),
          generator: def.veinGenerator() ? def.veinGenerator().getClass().getSimpleName() : 'null'
        }
        if (layer) layer.getLevels().forEach(l => v.layer_levels.push(l.toString()))
        def.dimensionFilter().forEach(k => v.dimensions.push(k.location().toString()))
        if (def.biomes()) {
          let set = def.biomes().get()
          if (set) set.forEach(h => { const id = holderId(h); if (id) v.biomes.push(id) })
        }
        out.gtceu_veins.push(v)
      }
    } catch (err) { out.gtceu_veins.push({ error: String(err) }) }

    // ---- 放置特征（矿石类）----
    out.placed_features = []
    try {
      const registry = ra.registryOrThrow($Registries.PLACED_FEATURE)
      registry.entrySet().forEach(e => {
        const placed = e.getValue()
        const configured = placed.feature().value()
        const feature = configured.feature()
        const featureId = $BuiltInRegistries.FEATURE.getKey(feature)
        const featureClass = feature.getClass().getSimpleName()
        const configClass = configured.config().getClass().getSimpleName()
        const isOre = featureClass.contains('Ore') || configClass == 'OreConfiguration'
        if (!isOre) return

        const o = {
          id: e.getKey().location().toString(),
          feature: featureId ? featureId.toString() : 'unknown'
        }
        if (configClass == 'OreConfiguration') {
          // Rhino: this arrow callback also contains a nested arrow, and a
          // `const` inside a nested block of such a function throws
          // "redeclaration of var ore" on call. Use let here.
          let ore = configured.config()
          o.size = ore.size
          o.discard_chance_on_air_exposure = ore.discardChanceOnAirExposure
          o.targets = []
          ore.targetStates.forEach(t => {
            o.targets.push({
              state: t.state ? t.state.getBlock().builtInRegistryHolder().key().location().toString() : 'null',
              target_type: t.target.getClass().getSimpleName()
            })
          })
        }
        o.placements = []
        placed.placement().forEach(m => {
          const mt = m.type()
          const mtId = $BuiltInRegistries.PLACEMENT_MODIFIER_TYPE.getKey(mt)
          o.placements.push({
            type: mtId ? mtId.toString() : 'unknown',
            config: encodeObject($PlacementModifier.CODEC, m)
          })
        })
        out.placed_features.push(o)
      })
    } catch (err) { out.placed_features.push({ error: String(err) }) }

    // ---- Forge biome modifier ----
    out.biome_modifiers = []
    try {
      const registry = ra.registryOrThrow($ForgeRegistries.Keys.BIOME_MODIFIERS)
      registry.entrySet().forEach(e => {
        const modifier = e.getValue()
        const cls = modifier.getClass().getSimpleName()
        const rec = { id: e.getKey().location().toString(), class: cls }
        if (cls == 'AddFeaturesBiomeModifier') {
          rec.step = modifier.step().toString()
          rec.features = []
          modifier.features().forEach(h => { const id = holderId(h); if (id) rec.features.push(id) })
          rec.biomes = []
          modifier.biomes().forEach(h => { const id = holderId(h); if (id) rec.biomes.push(id) })
        }
        out.biome_modifiers.push(rec)
      })
    } catch (err) { out.biome_modifiers.push({ error: String(err) }) }

    // ---- 物品标签 ----
    out.item_tags = {}
    try {
      const items = ra.registryOrThrow($Registries.ITEM)
      items.getTags().forEach(pair => {
        const tagId = pair.getFirst().location()
        const path = tagId.getPath()
        const interesting = path.startsWith('ores') || path.startsWith('raw_materials')
          || path.startsWith('dusts') || path.startsWith('ingots')
        if (!interesting) return
        const members = []
        pair.getSecond().forEach(h => { const id = holderId(h); if (id) members.push(id) })
        out.item_tags[tagId.toString()] = members
      })
    } catch (err) { out.item_tags.error = String(err) }

    return out
  }

  function writeDump(server, payload) {
    if (!$Files) return null
    try {
      const dir = server.getServerDirectory().toPath().resolve('debug')
      $Files.createDirectories(dir)
      const out = dir.resolve('kubejs-ore-gen-dump.json')
      $Files.writeString(out, JSON.stringify(payload, null, 2), $StandardCharsets.UTF_8)
      return out.toString()
    } catch (err) {
      console.warn('[GT-ORES] file write failed: ' + err)
      return null
    }
  }

  function printJson(tag, value) {
    console.info(`[GT-ORES:${tag}-BEGIN]`)
    console.info(JSON.stringify(value))
    console.info(`[GT-ORES:${tag}-END]`)
  }

  // verbose=false：摘要 + 维度/矿脉/放置特征（矿石核心信息，自动输出）
  // verbose=true ：再额外输出 biome modifier、标签
  function runDump(server, verbose) {
    try {
      const gtDumpResult = dumpOres(server)
      console.info(`[GT-ORES] summary: dimensions=${gtDumpResult.dimensions.length}`
        + ` gtceu_veins=${gtDumpResult.gtceu_veins.length}`
        + ` placed_features=${gtDumpResult.placed_features.length}`
        + ` biome_modifiers=${gtDumpResult.biome_modifiers.length}`
        + ` item_tags=${Object.keys(gtDumpResult.item_tags).length}`)
      printJson('DIMENSIONS', gtDumpResult.dimensions)
      printJson('GTCEU_VEINS', gtDumpResult.gtceu_veins)
      printJson('PLACED_FEATURES', gtDumpResult.placed_features)
      if (verbose) {
        printJson('BIOME_MODIFIERS', gtDumpResult.biome_modifiers)
        printJson('ITEM_TAGS', gtDumpResult.item_tags)
      }
      const file = writeDump(server, gtDumpResult)
      return file || 'log-only'
    } catch (err) {
      console.error('[GT-ORES] dump failed: ' + err)
      return null
    }
  }

  // 启动时自动 dump（无需手动触发）
  ServerEvents.loaded(event => runDump(event.server, false))

  // 供其它脚本调用
  global.dumpOreGen = function () {
    try {
      const hooks = Java.loadClass('net.minecraftforge.server.ServerLifecycleHooks')
      return runDump(hooks.getCurrentServer())
    } catch (err) {
      console.error('[GT-ORES] global.dumpOreGen failed: ' + err)
      return null
    }
  }

  // 手动命令：/oregendump
  function registerDumpCommand(apiName) {
    try {
      ServerEvents[apiName](event => {
        const builder = $Commands.literal('oregendump')
          .requires(src => src.hasPermission(0))
          .executes(ctx => {
            const out = runDump(ctx.getSource().getServer(), true)
            ctx.getSource().sendSuccess(() => $Component.literal(
              out ? '[GT-ORES] dump -> ' + out : '[GT-ORES] dump failed'), false)
            return out ? 1 : 0
          })
        event.register(builder)
      })
      console.info('[GT-ORES] command /oregendump registered via ServerEvents.' + apiName)
    } catch (err) {
      console.warn('[GT-ORES] command registration via ' + apiName + ' failed: ' + err)
    }
  }

  if (typeof ServerEvents.commandRegistry === 'function') {
    registerDumpCommand('commandRegistry')
  } else if (typeof ServerEvents.commandRegistration === 'function') {
    registerDumpCommand('commandRegistration')
  }
})()
