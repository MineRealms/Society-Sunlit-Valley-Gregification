// priority: 0
// Optional biology routes. Never remove the original GT/Pollution recipes.
ServerEvents.recipes(e => {
  if (!Platform.isLoaded('gtceu') || !Platform.isLoaded('pollution')) return

  // 4 rotten flesh + 500 mB biomass -> 2 primitive meat upstream; no bonus output here.
  e.recipes.gtceu.macerator('society:bio/primitive_meat_to_meat_dust')
    .itemInputs('pollution:primitive_meat')
    .itemOutputs('gtceu:meat_dust')
    .duration(102)
    .EUt(2, 1)

  // Bootstrap: the magic assembler's control component itself consumes an iPS brain.
  // Use the same biological inputs in a slower, more power-hungry LuV sterile reactor.
  // The original EV magic assembler recipe remains the cheaper mass-production route.
  e.recipes.gtceu.chemical_reactor('society:bio/ips_brain_bootstrap')
    .itemInputs('2x pollution:rat_brain', 'thaumcraft:brain_jar')
    .inputFluids(Fluid.of('pollution:infused_human', 500), Fluid.of('pollution:infused_life', 1000),
      Fluid.of('gtceu:sterilized_growth_medium', 1000))
    .itemOutputs('pollution:ips_human_brain')
    .duration(1600)
    .EUt(30720, 1)
    .cleanroom(CleanroomType.STERILE_CLEANROOM)

  // A reusable culture organ, not an extra 1500 mB of medium consumed every batch.
  // Four small dusts = one whole dust. Distinct input form avoids ambiguous matching
  // with the unmodified 300-tick GT recipe, and fits the reactor's two item inputs.
  e.recipes.gtceu.chemical_reactor('society:bio/ips_assisted_stem_cells')
    .itemInputs('4x gtceu:small_osmiridium_dust')
    .notConsumable('pollution:ips_human_brain')
    .inputFluids(Fluid.of('gtceu:bacteria', 500), Fluid.of('gtceu:sterilized_growth_medium', 500))
    .itemOutputs('32x gtceu:stem_cells')
    .outputFluids(Fluid.of('gtceu:bacterial_sludge', 500))
    .duration(240)
    .EUt(30720, 1)
    .cleanroom(CleanroomType.STERILE_CLEANROOM)

  console.info('[BIO-INTEGRATION] 3 optional culture recipes; original GT recipes kept, LuV sterile gate preserved')
})
