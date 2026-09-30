// Pack policy: the Twilight Forest Uncrafting Table is intentionally inert.
// This event guard takes effect on server-script reload without a full restart.
BlockEvents.rightClicked("twilightforest:uncrafting_table", (event) => {
  event.cancel();
});

ServerEvents.recipes((event) => {
  event.remove({ output: "twilightforest:uncrafting_table" });
});

console.info("[SV-POLICY] Twilight Forest Uncrafting Table right-click and crafting disabled");
