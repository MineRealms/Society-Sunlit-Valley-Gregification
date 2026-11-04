// priority: 8
// ============================================================
// Magic-material customer pools: Astral Sorcery / Thaumcraft / Botania.
//
// Only materials, not machines or multiblocks. AS/TC have no Shipping Bin
// anchor in this pack, so their market values are derived from the existing
// themed-merchant price ladder and recipe depth in the FTBQ audit. Botania
// materials use the real Shipping Bin anchors where available.
//
// These are offered by the travelling trader: magic goods are a convenience
// purchase, not a Shipping Bin arbitrage loop.
// ============================================================
if (typeof SunlitMarket !== 'undefined' && typeof global !== 'undefined' && Platform.isLoaded('society')) {
  let addMagic = (key, item, count, market, ratio, extra) => {
    let total = Math.max(1, Math.round(market * count))
    let ask = Math.round(total * ratio)
    if (ask >= total) ask = total - 1
    if (total < 2) return
    let rule = {
      type: 'pool',
      id: 'sv.magic.' + key,
      faction: 'society:trader',
      item: item,
      count: count,
      baseValue: Math.max(1, Math.round(total * 0.60)),
      marketValue: total,
      askPrice: Math.max(1, ask),
      repGain: extra && extra.repGain !== undefined ? extra.repGain : 2
    }
    SunlitMarket.rule(rule)
  }

  // ---- Astral Sorcery -------------------------------------------------------
  // 40 is the existing theme merchant's aquamarine buy price; starmetal is
  // scaled from the 240/150 ladder. Deeper materials carry a small premium.
  addMagic('as_aquamarine', 'astralsorcery:aquamarine', 2, 40, 0.80)
  addMagic('as_stardust', 'astralsorcery:stardust', 4, 24, 0.82)
  addMagic('as_infused_wood', 'astralsorcery:infused_wood', 4, 16, 0.84)
  addMagic('as_illumination', 'astralsorcery:illumination_powder', 4, 12, 0.84)
  addMagic('as_nocturnal', 'astralsorcery:nocturnal_powder', 4, 18, 0.84)
  addMagic('as_glass_lens', 'astralsorcery:glass_lens', 1, 40, 0.82)
  addMagic('as_marble', 'astralsorcery:marble_raw', 8, 4, 0.88)

  // ---- Thaumcraft -----------------------------------------------------------
  // The first four follow the existing curio merchant: 30/38/160/320.
  addMagic('tc_amber', 'thaumcraft:amber', 2, 40, 0.82)
  addMagic('tc_quicksilver', 'thaumcraft:quicksilver', 2, 50, 0.82)
  addMagic('tc_thaumium', 'thaumcraft:thaumium_ingot', 1, 220, 0.80)
  addMagic('tc_alumentum', 'thaumcraft:alumentum', 4, 24, 0.84)
  addMagic('tc_nitor', 'thaumcraft:nitor', 4, 16, 0.84)
  addMagic('tc_greatwood', 'thaumcraft:greatwood_log', 8, 12, 0.88)

  // ---- Botania --------------------------------------------------------------
  // Botania materials have Shipping values in global.trades, so use those as
  // the market reference; the values here are fallbacks only.
  let botanical = (id, fallback) => {
    let row = global.trades ? global.trades.get(id) : null
    return row && row.value > 0 ? row.value : fallback
  }
  addMagic('bot_livingwood', 'botania:livingwood_log', 8, botanical('botania:livingwood_log', 16), 0.90)
  addMagic('bot_livingrock', 'botania:livingrock', 16, botanical('botania:livingrock', 2), 0.88)
  addMagic('bot_manasteel', 'botania:manasteel_ingot', 1, botanical('botania:manasteel_ingot', 32), 0.88)
  addMagic('bot_mana_pearl', 'botania:mana_pearl', 1, botanical('botania:mana_pearl', 96), 0.84)
  addMagic('bot_white_petal', 'botania:white_petal', 8, botanical('botania:white_petal', 2), 0.88)
  addMagic('bot_spark', 'botania:spark', 1, botanical('botania:spark', 9), 0.86)

  console.info('[SV-INTEGRATION] magic material pools registered')
}
