// priority: 10
// ============================================================
// 骷髅洞穴（society:skull_cavern）岩层兼容：
// GTCEU 的 mat() 通过 ChemicalHelper.getOrePrefix(围岩) 判断矿石前缀，
// 该映射 ORES_INVERSE 只含 GTCEU 注册的原版石头类型（stone/deepslate/granite...）。
// skull_cavern 用 society:skull_* 自定义围岩，不在映射里，导致 GTCEU 矿脉几乎不生成。
// 这里把 skull 岩层注册为 TagPrefix.ore 的 stoneType，使其按基础 ore 前缀处理。
// ============================================================
console.info("[GT-ORES] skullOreCompat.js loaded")

const $ItemMaterialData = Java.loadClass("com.gregtechceu.gtceu.api.data.chemical.material.ItemMaterialData")
const $TagPrefix = Java.loadClass("com.gregtechceu.gtceu.api.data.tag.TagPrefix")
const $ForgeRegistries = Java.loadClass("net.minecraftforge.registries.ForgeRegistries")
const $ResourceLocation = Java.loadClass("net.minecraft.resources.ResourceLocation")

const SKULL_ROCKS = [
  "skull_stone",
  "skull_blackstone",
  "skull_arid_sandstone",
  "skull_sandstone",
  "skull_end_stone",
  "skull_permafrost",
]

const $Supplier = Java.loadClass("java.util.function.Supplier")
const $ChemicalHelper = Java.loadClass("com.gregtechceu.gtceu.api.data.chemical.ChemicalHelper")

let ok = 0
SKULL_ROCKS.forEach(name => {
  const block = $ForgeRegistries.BLOCKS.getValue(new $ResourceLocation("society", name))
  if (!block) {
    console.warn("[GT-ORES] missing block society:" + name)
    return
  }
  const state = block.defaultBlockState()
  const lz = Utils.lazy(function () { return block.defaultBlockState() })
  $ItemMaterialData.ORES_INVERSE.put(lz, $TagPrefix.ore)
  console.info("[GT-ORES] " + name + " state=" + state + " lazyget=" + lz.get())
  const prefix = $ChemicalHelper.getOrePrefix(state)
  const got = prefix.isPresent() ? prefix.get().toString() : "EMPTY"
  console.info("[GT-ORES] " + name + " -> " + got)
  if (prefix.isPresent()) ok++
})
console.info("[GT-ORES] registered " + ok + "/" + SKULL_ROCKS.length + " skull rock types to GTCEU ORES_INVERSE")
