// priority: 0
// Recover food-grade gelatin only. Never substitute it for GT industrial gelatin/agar.
ServerEvents.recipes(e => {
  if (!Platform.isLoaded('gtmfo') || !Platform.isLoaded('gtnn')) return
  let input = Fluid.of('gtceu:gelatin_solution', 1000)
  if (input.isEmpty() || Item.of('gtmfo:gelatin').isEmpty()) {
    console.error('[BIO-RECOVERY] Missing gelatin solution/item; refusing to register an empty recipe')
    return
  }
  // Native forward route: 8 food gelatin + 1000 mB water -> 1000 mB solution.
  // Reverse restores at most the same eight solids; water is lost, processing costs EU.
  e.recipes.gtceu.dehydrator('society:bio/food_gelatin_recovery')
    .inputFluids(input)
    .itemOutputs('8x gtmfo:gelatin')
    .duration(400)
    .EUt(480, 1)
  console.info('[BIO-RECOVERY] HV dehydrator food gelatin recovery installed; original meat/sludge routes retained')
})
