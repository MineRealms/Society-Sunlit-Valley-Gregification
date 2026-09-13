// priority: 1000
// ============================================================
// 临时诊断脚本（查完请删除）：打印关键食物标签的实际内容到日志
// 用法：进存档（或 /reload）后，在 logs/latest.log 里搜 [TAGDIAG]
// 目的：确认 forge:crops/onion 等标签在"你的游戏里"到底有没有物品
// ============================================================
ServerEvents.tags("item", (e) => {
  const list = [
    "forge:crops/onion",
    "forge:onion",
    "forge:vegetables/onion",
    "forge:crops/tomato",
    "forge:crops/cucumber",
    "forge:crops/wheat",
    "forge:crops/corn",
    "forge:flour/wheat",
    "forge:pasta/raw_pasta",
    "forge:seeds",
    "forge:crops",
  ];
  list.forEach((t) => {
    try {
      const w = e.get(t);
      const ids = w ? w.getObjectIds() : null;
      console.info("[TAGDIAG] " + t + " = " + (ids ? "[" + ids.join(", ") + "]" : "null"));
    } catch (err) {
      console.info("[TAGDIAG] " + t + " = ERROR " + err);
    }
  });
});
