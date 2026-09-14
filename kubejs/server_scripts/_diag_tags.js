// priority: 1000
// ============================================================
// 临时诊断脚本（查完请删除）：列出"解析后没有任何有效物品"的物品标签
// 用法：进存档（或 /reload）后，在 logs/latest.log 里搜 [TAGDIAG]
// 原理：遍历所有物品标签 → 递归解析 #标签引用（带环保护）→ 用 Item.exists() 过滤无效条目
// ============================================================
ServerEvents.tags("item", (e) => {
  const visiting = {};
  const cache = {};

  const resolve = (id, depth) => {
    if (depth > 32 || visiting[id]) return [];
    // 注意：只在顶层（depth===0）缓存结果。循环引用下，带栈计算出的结果是"部分结果"，
    // 缓存它会导致后续解析出错（这正是静态分析两次结果不一致的原因）
    if (depth === 0 && cache[id]) return cache[id];
    visiting[id] = true;
    const out = [];
    const w = e.get(id);
    if (w) {
      const ids = w.getObjectIds();
      for (let i = 0; i < ids.size(); i++) {
        const oid = ids.get(i);
        if (Item.exists(oid)) {
          out.push(String(oid));
        } else {
          // 不是有效物品：当成标签引用继续解析（若是无效物品则解析为空，无副作用）
          const sub = resolve(oid, depth + 1);
          for (let j = 0; j < sub.length; j++) out.push(sub[j]);
        }
      }
    }
    visiting[id] = false;
    if (depth === 0) cache[id] = out;
    return out;
  };

  const empty = [];
  const all = [];
  e.tags.forEach((key) => {
    all.push(String(key));
  });

  for (let i = 0; i < all.length; i++) {
    const tagName = all[i];
    const items = resolve(tagName, 0);
    if (items.length === 0) empty.push(tagName);
  }

  console.info("[TAGDIAG] TOTAL_TAGS = " + all.length + " | EMPTY_TAGS = " + empty.length);

  // 分块输出，避免单行过长
  const chunk = 15;
  for (let i = 0; i < empty.length; i += chunk) {
    console.info("[TAGDIAG] EMPTY[" + (i / chunk) + "] = " + empty.slice(i, i + chunk).join(", "));
  }

  // 关键标签内容（复核洋葱）
  ["forge:crops/onion", "forge:onion", "forge:vegetables/onion", "forge:crops", "forge:seeds",
   "forge:flour/wheat", "forge:pasta/raw_pasta"].forEach((tag) => {
    const items = resolve(tag, 0);
    console.info("[TAGDIAG] CHECK " + tag + " = [" + items.join(", ") + "]");
  });
});
