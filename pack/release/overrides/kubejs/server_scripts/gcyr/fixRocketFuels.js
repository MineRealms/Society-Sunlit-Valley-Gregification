// priority: 0
// GCYR 0.2.9 reads getRecipeEUtTier(recipe), not the literal EUt value.
// Engine tiers BASIC/ADVANCED/ELITE=1/2/3 therefore encode as 32/128/512 V.
// These voltages are metadata for fuel eligibility; rockets do not consume EU.
ServerEvents.recipes(e => {
  if (!Platform.isLoaded('gcyr') || !Platform.isLoaded('gtceu')) return
  let fuels = [
    ['gasoline', 'gtceu:gasoline', 25, 32, 'kubejs:gcyr_fuel_gasoline'],
    ['diesel', 'gtceu:diesel', 18, 32, 'kubejs:gcyr_fuel_diesel'],
    ['rocket_fuel', 'gtceu:rocket_fuel', 75, 32, 'gcyr:rocket_fuel'],
    ['hydrogen', 'gtceu:hydrogen', 10, 32, 'gcyr:hydrogen'],
    ['hydrogen_plasma', 'gtceu:hydrogen_plasma', 18, 512, 'gcyr:hydrogen_plasma']
  ]
  fuels.forEach(([path, fluid, duration, voltage, id]) => {
    e.remove({id: 'gcyr:rocket_fuel/' + path})
    e.remove({id: 'gcyr:' + path})
    e.recipes.gcyr.rocket_fuel(id)
      .inputFluids(Fluid.of(fluid, 1))
      .duration(duration)
      .EUt(voltage, 1)
  })
  // Pollution registers its two magic propellants without a tier (ULV = any rocket), although
  // both burn more efficiently than GT rocket fuel. Gate by where they can first be produced:
  // infernal blaze (HV production) -> advanced engine, dragon pulse (IV production) -> elite.
  if (Platform.isLoaded('pollution')) {
    let magic = [
      ['infernal_blaze_propellant', 80, 128],
      ['dragon_pulse_fuel', 160, 512]
    ]
    magic.forEach(([path, duration, voltage]) => {
      let id = 'pollution:rocket_fuel/gcyr_rocket_fuel/' + path
      e.remove({id: id})
      e.recipes.gcyr.rocket_fuel('pollution:gcyr_rocket_fuel/' + path)
        .inputFluids(Fluid.of('pollution:' + path, 1))
        .duration(duration)
        .EUt(voltage, 1)
    })
  }
  console.info('[GCYR-FUEL-FIX] native fuel tiers normalized; pair with Sunlit Industry Compat for per-rocket validation')
})
