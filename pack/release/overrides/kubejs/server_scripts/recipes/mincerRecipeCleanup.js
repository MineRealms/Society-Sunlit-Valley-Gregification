// The native wheat tag includes wheat, oat, barley and corn. Its generic
// four-flour mincer recipe overlaps all four grain-specific pack recipes.
ServerEvents.recipes((e) => {
  e.remove({ id: "farm_and_charm:mincer/flour" });
});
