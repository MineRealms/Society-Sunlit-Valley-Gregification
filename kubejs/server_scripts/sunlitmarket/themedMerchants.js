// priority: 0
// ============================================================
// Themed merchants for Tinkers' Construct / Thaumcraft / Astral Sorcery / Botania.
//
// Use an entity tag when spawning the shopkeeper, e.g.:
//   /summon me:npc ~ ~ ~ {Tags:["sunlitmarket.theme.tinkers"],InitializationData:{Type:"me:dale.peasant"}}
// The mod matches any entity with the tag, not only me:npc.
//
// High-tier goods carry an "unlock" id. Purchase requires the matching unlock:
//   KubeJS:      SunlitMarket.unlock(player, 'theme.tinkers.adept')
//   FTBQ reward: execute as {p} run sunlitmarket unlock theme.tinkers.adept
//                (per-player reward with elevated permissions)
//   Manual test: /sunlitmarket unlock theme.astral.attuned
// FTBQ milestones: manyullyn / blood template II / starmetal / terrasteel.
// ============================================================
if (typeof SunlitMarket !== 'undefined') {
  let registerMerchant = (spec) => {
    SunlitMarket.merchant(spec)
    SunlitMarket.rule({ type: 'npc', id: 'sv.theme.merchant.' + spec.id,
      faction: spec.faction, tag: spec.tag, rank: 'MERCHANT' })
  }
  if (Platform.isLoaded('tconstruct')) {
    registerMerchant({
      id: 'theme_tinkers_smith',
      name: '匠魂铸师',
      faction: 'theme:tinkers',
      tag: 'sunlitmarket.theme.tinkers',
      offers: [
        { item: 'tconstruct:cobalt_ingot', count: 1, buy: 180, sell: 110, stock: 8, repGain: 1 },
        { item: 'tconstruct:slimesteel_ingot', count: 1, buy: 220, sell: 140, stock: 8, repGain: 1 },
        { item: 'tconstruct:rose_gold_ingot', count: 1, buy: 260, sell: 170, stock: 6, repGain: 1 },
        { item: 'tconstruct:manyullyn_ingot', count: 1, buy: 480, sell: 300, stock: 4, reputation: 10, unlock: 'theme.tinkers.adept' }
      ]
    })
  }

  if (Platform.isLoaded('thaumcraft')) {
    registerMerchant({
      id: 'theme_thaumcraft_curio',
      name: '神秘材料商',
      faction: 'theme:thaumcraft',
      tag: 'sunlitmarket.theme.thaumcraft',
      offers: [
        { item: 'thaumcraft:amber', count: 1, buy: 30, sell: 18, stock: 12, repGain: 1 },
        { item: 'thaumcraft:quicksilver', count: 1, buy: 38, sell: 24, stock: 12, repGain: 1 },
        { item: 'thaumcraft:thaumium_ingot', count: 1, buy: 160, sell: 100, stock: 8, repGain: 1 },
        { item: 'thaumcraft:void_ingot', count: 1, buy: 320, sell: 200, stock: 4, reputation: 10, unlock: 'theme.thaumcraft.adept' },
        { item: 'thaumcraft:alumentum', count: 1, buy: 36, sell: 22, stock: 12 },
        { item: 'thaumcraft:nitor', count: 1, buy: 24, sell: 14, stock: 12 },
        { item: 'thaumcraft:greatwood_log', count: 1, buy: 18, sell: 10, stock: 16 }
      ]
    })
  }

  if (Platform.isLoaded('astralsorcery')) {
    registerMerchant({
      id: 'theme_astral_merchant',
      name: '星辉商人',
      faction: 'theme:astral',
      tag: 'sunlitmarket.theme.astral',
      offers: [
        { item: 'astralsorcery:aquamarine', count: 1, buy: 30, sell: 18, stock: 12, repGain: 1 },
        { item: 'astralsorcery:starmetal_ingot', count: 1, buy: 240, sell: 150, stock: 6, reputation: 10, unlock: 'theme.astral.attuned' },
        { item: 'astralsorcery:stardust', count: 1, buy: 36, sell: 22, stock: 12 },
        { item: 'astralsorcery:infused_wood', count: 1, buy: 24, sell: 14, stock: 16 },
        { item: 'astralsorcery:resonating_gem', count: 1, buy: 220, sell: 130, stock: 6 },
        { item: 'astralsorcery:illumination_powder', count: 1, buy: 18, sell: 10, stock: 16 },
        { item: 'astralsorcery:nocturnal_powder', count: 1, buy: 26, sell: 15, stock: 16 }
      ]
    })
  }

  if (Platform.isLoaded('botania')) {
    registerMerchant({
      id: 'theme_botania_merchant',
      name: '植物魔法材料商',
      faction: 'theme:botania',
      tag: 'sunlitmarket.theme.botania',
      offers: [
        { item: 'botania:livingwood_log', count: 1, buy: 24, sell: 16, stock: 16 },
        { item: 'botania:livingrock', count: 1, buy: 8, sell: 5, stock: 16 },
        { item: 'botania:manasteel_ingot', count: 1, buy: 48, sell: 30, stock: 12, repGain: 1 },
        { item: 'botania:mana_pearl', count: 1, buy: 130, sell: 85, stock: 8, repGain: 1 },
        { item: 'botania:mana_diamond', count: 1, buy: 1600, sell: 1050, stock: 4, reputation: 10, unlock: 'theme.botania.adept' },
        { item: 'botania:terrasteel_ingot', count: 1, buy: 52000, sell: 34000, stock: 1, reputation: 20, unlock: 'theme.botania.adept' }
      ]
    })
  }

  console.info('[SunlitMarket] themed merchants registered')
}
