// priority: 0
console.info("[SOCIETY] unifyOreAndCropTags.js loaded");

// Ore-dictionary unification + crop-tag repair.
//
// Context (verified against the running server tag registry):
//  - forge:ores/<mat> already merges Mekanism and GTCEu for osmium / tin / lead /
//    uranium / fluorite, so those need no work.
//  - Society's own iridium ore (society:iridium_ore / deepslate) only carried the
//    generic forge:ores tag, so it was invisible to forge:ores/iridium used by GT
//    tag recipes. Add it to the same dictionary entry as gtceu:iridium_ore.
//  - forge:onion / forge:crops/onion / forge:vegetables/onion form a circular
//    reference (each includes the others). Whatever tag is resolved first wins,
//    and forge:crops/onion ended up WITHOUT the pack's canonical
//    farm_and_charm:onion, so recipes that require forge:crops/onion could not use it.
//    Re-adding the item directly makes every onion tag independent of resolve order.

const societyIridiumOres = ["society:iridium_ore", "society:deepslate_iridium_ore"];

ServerEvents.tags("item", (e) => {
  societyIridiumOres.forEach((ore) => {
    e.add("forge:ores", ore);
    e.add("forge:ores/iridium", ore);
  });
  e.add("forge:crops/onion", "farm_and_charm:onion");
});

ServerEvents.tags("block", (e) => {
  societyIridiumOres.forEach((ore) => {
    e.add("forge:ores", ore);
    e.add("forge:ores/iridium", ore);
  });
});
