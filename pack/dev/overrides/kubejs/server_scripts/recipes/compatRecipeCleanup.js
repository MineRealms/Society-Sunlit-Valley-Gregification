// Remove known upstream recipes whose conditional ingredients/results are empty
// in this exact server mod set. This keeps the invalid definitions from entering
// the active recipe manager after KubeJS has parsed the pack.
ServerEvents.recipes((e) => {
  var broken = [
    "veggiesdelight:cauliflower_burger",
    "crabbersdelight:lanternfish_from_barrel",
    "twilightdelight:rainbow_ice_cream",
    "crabbersdelight:lanternfish_barrel",
    "meadow:limestone_bricks_stairs",
    "farmlife:cooked_fuli_from_campfire_cooking",
    "translocators:item_translocator",
    "dramaticdoors:short_palm_door_universal_sawmill",
    "twilightdelight:twilight_ice_cream",
    "farmlife:cooked_fuli_from_smoking",
    "farmlife:cooked_fuli",
    "twilightdelight:teardrop_sword",
    "dramaticdoors:tall_palm_door"
  ];
  broken.forEach((id) => e.remove({ id: id }));

  // Sophisticated Storage's Quark bridge recipes serialize an empty first
  // ingredient when Quark's optional chest is absent.
  ["oak", "spruce", "birch", "jungle", "acacia", "dark_oak", "mangrove", "cherry", "bamboo", "crimson", "warped"]
    .forEach((wood) => e.remove({ id: "sophisticatedstorage:" + wood + "_chest_from_quark_" + wood + "_chest" }));
});
