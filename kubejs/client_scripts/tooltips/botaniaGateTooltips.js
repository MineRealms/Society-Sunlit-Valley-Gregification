// 植物魔法阶段锁提示（与 kubejs/server_scripts/botania/gateBotania.js 对应）
ItemEvents.tooltip((tooltip) => {
  const lock = (text) => [Text.of(" ").append(Text.of("阶段锁：").gold()).append(Text.of(text).gray())];

  tooltip.add(["botania:mana_spreader", "botania:mana_pool"], lock("需要暮色森林的火把浆果（先进入暮色森林）"));
  tooltip.add("botania:runic_altar", lock("需要暮色森林巫妖王的战利品（击败巫妖王）"));
  tooltip.add("botania:terrasteel_ingot", lock("聚合需要神秘时代的虚空锭（研究出虚空金属后）"));
});
