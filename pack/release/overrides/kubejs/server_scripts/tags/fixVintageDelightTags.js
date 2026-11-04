// VintageDelight 0.1.6 ships forge:fruits -> #forge:fruits/gearo_berry and
// forge:protein -> #forge:protein/peanut but never defines either sub-tag, so the
// TagLoader drops both entries and gearo berries / peanuts fall out of forge:fruits /
// forge:protein (splendid_slimes, diet and GTMFO nutrition read those parents).
// Defining the sub-tags lets the mod's own references resolve.
ServerEvents.tags("item", (e) => {
  if (!Platform.isLoaded("vintagedelight")) return;
  e.add("forge:fruits/gearo_berry", "vintagedelight:gearo_berry");
  e.add("forge:protein/peanut", "vintagedelight:peanut");
});
