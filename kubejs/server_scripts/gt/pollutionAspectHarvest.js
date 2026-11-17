// priority: -100

if (Platform.isLoaded("pollution")) {
  ServerEvents.tags("block", event => {
    event.add("sunlitindustry:no_player_harvest", /^(pollution|gtceu):(.*_)?infused_(air|earth|entropy|fire|order|water)_ore$/)
  })

  LootJS.modifiers(event => {
    const FakePlayer = Java.loadClass("net.minecraftforge.common.util.FakePlayer")
    event.addBlockLootModifier("#sunlitindustry:no_player_harvest")
      .matchEntity(entity => entity.anyType("minecraft:player"))
      .entityPredicate(entity => !(entity instanceof FakePlayer))
      .removeLoot("*")
  })
}
