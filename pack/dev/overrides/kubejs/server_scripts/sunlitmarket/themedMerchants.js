// priority: 0
// ============================================================
// Themed merchants for Tinkers' Construct / Thaumcraft / Astral Sorcery.
//
// Use an entity tag when spawning the shopkeeper, e.g.:
//   /summon me:npc ~ ~ ~ {Tags:["sunlitmarket.theme.tinkers"],InitializationData:{Type:"me:dale.peasant"}}
// The mod matches any entity with the tag, not only me:npc.
//
// These are sample prices; tune them against the pack economy. No tool NBT,
// research, or constellation data is priced here.
// ============================================================
if (typeof SunlitMarket !== 'undefined') {
  if (Platform.isLoaded('tconstruct')) {
    SunlitMarket.merchant({
      id: 'theme_tinkers_smith',
      name: '匠魂铸师',
      faction: 'theme:tinkers',
      tag: 'sunlitmarket.theme.tinkers',
      offers: [
        { item: 'tconstruct:cobalt_ingot', count: 1, buy: 180, sell: 110, stock: 8 },
        { item: 'tconstruct:slimesteel_ingot', count: 1, buy: 220, sell: 140, stock: 8 },
        { item: 'tconstruct:rose_gold_ingot', count: 1, buy: 260, sell: 170, stock: 6 },
        { item: 'tconstruct:manyullyn_ingot', count: 1, buy: 480, sell: 300, stock: 4, reputation: 10 }
      ]
    })
  }

  if (Platform.isLoaded('thaumcraft')) {
    SunlitMarket.merchant({
      id: 'theme_thaumcraft_curio',
      name: '神秘材料商',
      faction: 'theme:thaumcraft',
      tag: 'sunlitmarket.theme.thaumcraft',
      offers: [
        { item: 'thaumcraft:amber', count: 1, buy: 30, sell: 18, stock: 12 },
        { item: 'thaumcraft:quicksilver', count: 1, buy: 38, sell: 24, stock: 12 },
        { item: 'thaumcraft:thaumium_ingot', count: 1, buy: 160, sell: 100, stock: 8 },
        { item: 'thaumcraft:void_ingot', count: 1, buy: 320, sell: 200, stock: 4, reputation: 10 }
      ]
    })
  }

  if (Platform.isLoaded('astralsorcery')) {
    SunlitMarket.merchant({
      id: 'theme_astral_merchant',
      name: '星辉商人',
      faction: 'theme:astral',
      tag: 'sunlitmarket.theme.astral',
      offers: [
        { item: 'astralsorcery:aquamarine', count: 1, buy: 30, sell: 18, stock: 12 },
        { item: 'astralsorcery:starmetal_ingot', count: 1, buy: 240, sell: 150, stock: 6 }
      ]
    })
  }

  console.info('[SunlitMarket] themed merchants registered')
}
