// 神秘视界（Isorropia）甜品属性提示 —— 对应 kubejs/server_scripts/isorropia/chocoFood.js
ItemEvents.tooltip((tooltip) => {
  const note = (text) => [Text.of(" ").append(Text.of("属性 ").gold()).append(Text.of(text).gray())];

  tooltip.add("isorropia:chocolate_bar", note("材料·不可食用（9 棒 = 巧克力块）"));
  tooltip.add("isorropia:chocolate", note("建筑方块·不可食用"));
  tooltip.add("isorropia:chocolate_milk_bucket", note("饮用同牛奶：清除药水效果"));
  tooltip.add("isorropia:chocolate_cream", note("食用：迅捷 I（30 秒）+ 少量饱和·计入乳制品营养"));
});
