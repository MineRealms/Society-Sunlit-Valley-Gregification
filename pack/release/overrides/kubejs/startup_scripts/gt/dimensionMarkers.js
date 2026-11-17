// priority: 0

GTCEuStartupEvents.registry("gtceu:dimension_marker", event => {
  const markers = [
    ["society:skull_cavern", "society", "minecraft:skeleton_skull", "dimension.society.skull_cavern"],
    ["pollution:alfheim", "pollution", Platform.isLoaded("botania") ? "botania:elementium_ingot" : "minecraft:amethyst_shard", "dimension.pollution.alfheim"],
    ["me:middle-earth", "me", "me:mithril_ingot", "dimension.me.middle_earth"],
    ["twilightforest:twilight_forest", "twilightforest", "twilightforest:magic_map", "dimension.twilightforest.twilight_forest"],
    ["pollution:underground", "pollution", "minecraft:deepslate", "dimension.pollution.underground"],
  ]

  markers.forEach(marker => {
    if (!Platform.isLoaded(marker[1])) return
    event.create(marker[0])
      // Resolve items after their deferred registries have finished loading.
      .iconSupplier(() => Item.of(marker[2]).item)
      .overrideName(marker[3])
  })
})
