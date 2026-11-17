// priority: 10

if (Platform.isLoaded("pollution")) {
  GTCEuServerEvents.oreVeins(event => {
    const aspects = ["air", "earth", "entropy", "fire", "order", "water"]
    let modified = 0
    aspects.forEach(aspect => {
      event.modify(`pollution:thaumastic_${aspect}_vein`, vein => {
        // Set both: changing the layer alone retains the old dimension filter.
        vein.layer("pollution_underground")
        vein.dimensions("pollution:underground")
        modified++
      })
    })
    console.info(`[GT-ORES] restricted ${modified}/6 Pollution aspect veins to pollution:underground`)
  })
}
