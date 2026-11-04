# FTBQ 物品与价格覆盖审计

> 生成方式：tools/sv_price_audit.py 离线扫描 FTBQ 章节、Shipping Bin 表和配方 JSON。
> 未启动 Minecraft。原始明细：build/sv_price_audit.csv。

## 1. 结论先说

之前的联动价格**只覆盖了 Shipping Bin 有价格的物品**，不是一个完整价格表：

- FTBQ 任务书共 57 章，任务 item 引用 **1,735 个唯一条目**。
- 其中只有 **529 个**能从 global.trades 拿到价格锚。
- **1,206 个**没有 Shipping Bin 价格锚。
- 配方扫描（kubejs/data + mods jar，共 63,004 个 recipe 文件）找到 **699 个**物品有直接配方；与锚重合 293 个。
- 仍然有 **800 个**物品既没有价格锚、也没有扫描到直接配方（GT 动态配方、纯任务/装饰/战利品物品）。

所以：**没有囊括全部物品；第一版只有约 105 个样本货池，第二版扩到 635 个仍是职业化的可交易子集，不是全量价格表。** 这个批评成立。

## 2. 覆盖矩阵

| 分类 | 数量 |
|---|---:|
| FTBQ 任务物品 | 1,735 |
| 有 Shipping 锚 | 529 |
| 有直接配方 | 699 |
| 锚 + 配方都有 | 293 |
| 只有锚 | 236 |
| 只有配方 | 406 |
| 两者都没有 | 800 |

配方深度分布（0 = 未找到配方；深度 >=8 归为复杂）：

| 深度 | 物品数 |
|---:|---:|
| 0 | 1,036 |
| 1 | 152 |
| 2 | 119 |
| 3 | 76 |
| 4 | 81 |
| 5 | 29 |
| 6 | 46 |
| 7 | 13 |
| >=8 | 169 |

任务阶段分布（按章节分组）：

| 阶段组 | 物品数 | 内容 |
|---|---:|---|
| 0 主/欢迎 | 227 | getting_started、welcome 等 |
| 1 建造 | 20 | 建筑、家具 |
| 2 装备 | 33 | 工具、护甲、生物 |
| 3 田园/生活 | 486 | crops、fishing、drinks、minerals、prismatic farming |
| 4 工业 | 879 | GT 各电压、Mekanism、AE2、太空、污染 |
| 5 魔法 | 66 | Astral、Thaumcraft、Botania |
| 6 中州 | 24 | Middle-earth |

任务物品最多的章节：banners 189、ore_generation 108、MV 91、crops 89、EV 80、fishing 75、HV 64、Mekanism 61、LV 60。

注意：banners、ore_generation 等章节包含大量收藏/展示/矿脉指示物品，不是适合“顾客求购”的日用品；不能简单把 1,735 个条目都塞进货池。

## 3. 应该采用的三层定价

### A. Shipping 锚（最高可信度）

    market = global.trades.value

适用于作物、鱼、原木、动物产品、料理、矿物等已有出货价的物品。已验证覆盖 529 个 FTBQ 条目。

### B. 配方成本（中等可信度）

对每个有配方的物品递归计算：

    recipe_cost = sum(input_market / output_count)
    market = max(shipping_anchor, recipe_cost * 1.15, stage_floor)

规则：
- 同一物品多配方取最高可行成本，避免廉价旁路拉低价值。
- 只递归 8 层；循环配方/无锚原料用 stage_floor 兜底。
- 输出数量必须归一化（例如一次产 4 个粉，不能按 1 个算）。

当前扫描找到 699 个直接配方物品；其中 406 个没有 Shipping 锚，这正是第二批应该补的价格。

### C. 阶段底价（低可信度，必须人工复核）

对既无锚、又无 JSON 配方的物品，用 FTBQ 阶段给底价，而不是乱填整数：

    stage_floor = band_base * (1 + 0.15 * depth)

建议 band_base：

| 阶段组 | 底价区间（spur） |
|---|---:|
| 0 主/欢迎 | 4–16 |
| 1 建造 | 8–32 |
| 2 装备 | 16–64 |
| 3 田园/生活 | 8–128 |
| 4 工业 | 32–512 |
| 5 魔法 | 64–1024 |
| 6 中州 | 32–512 |

800 个“两者都没有”的物品中，预计只有一部分适合上货架；其余应该标记为 quest-only、decorative、technical，不进入交易池。

## 4. 顾客与商人的价格公式（下一版）

对每个已分级物品：

    market = max(A, B, C)
    customer_ask = market * clamp(0.94 - 0.02*min(depth,6) - 0.01*stage_band, 0.68, 0.94)
    merchant_buy = market * 1.30   // 玩家向商人买
    merchant_sell = market * 0.80  // 玩家卖给商人

- customer_ask 始终低于 market，玩家有利润，但深度/阶段越高，折价越小。
- merchant_buy 高于 market，堵住“商人买入 → 出货箱卖出”。
- merchant_sell 低于 market，避免“柜台收货 → 商人倒卖”无限循环。
- 只有 market 可信度达到 B 以上，才进入顾客池；C 级只作为阶段商人/任务奖励的备选。

## 5. 还需要补的

1. 解析 **GTCEu 动态配方**（当前 800 个缺口里很大一部分是 GT/多方块/电压机器），不能只靠 JSON。
2. 给 banners、ore_generation 等章节做 tradeable/quest-only 分类，避免把收藏品当商品。
3. 解析配方 **output count** 和 tag 成员，当前 recipe_cost 还没进入实际脚本。
4. 用 FTBQ dependency 的拓扑深度替代简单 chapter order，判断真实阶段。
5. 重生成 svCustomers.js / 商人货架，并按阶段设置解锁，不要继续加手工 fallback。

## 6. 当前状态

- 现有 delta 包里的货池是**第二版**：完整 global 数组 631 条，覆盖的是 Shipping 锚 + 重点 FTBQ 商品 + AS/TC/BOT 材料，不是全量。
- 本文的审计数据已经生成；在完成 A/B/C 统一生成器之前，**不应把当前 delta 当作最终经济版本**。
- 静态审计未启动游戏；GT 动态配方和任务-only 分类需要服务器/JEI 数据继续补。

## 7. 第二版：手工选定的 FTBQ 商品覆盖

按用户要求，不再追 800 个 GT 动态配方物品，只对 FTBQ 中真正适合柜台/商人的章节做手工清单：

| 章节 | FTBQ 物品 | 已有货池 | 缺口 |
|---|---:|---:|---:|
| crops | 89 | 89 | 0 |
| fishing | 75 | 75 | 0 |
| pantry | 12 | 12 | 0 |
| minerals | 44 | 44 | 0 |
| gems | 14 | 13 | 1（numismatics:prismatic_coin 无 Shipping 锚） |
| artifacts | 25 | 24 | 1（token_of_unity 价值 3，跳过） |
| drinks | 45 | 41 个有锚（其余无锚的鸡尾酒除外） | 4（laputa_franc 等无锚） |
| middle_earth | 24 | 14 个有锚的商品 | 10（种子/机器/地图等无锚，不进商品池） |

实现方式：

- 修复了原货池过滤器的两个实际 bug：`cabbage` 被 `bag` 子串误排除，鱼只覆盖 16–80 导致高价值鱼全丢。
- 作物现在覆盖 FTBQ 89/89；鱼覆盖 75/75；矿物覆盖 44/44。
- 饮料按 `global.wines/brews/cocktails/herbalBrews` 全量生成；`global.brews` 在运行时由 `brewingStationRecipes` 填充，包含 19 种啤酒/威士忌。
- 文物（artifacts）和宝石只进旅行商人，按价值 0.78–0.82 收购；不进普通农户/渔夫池。
- 第二版静态执行：**646 条规则 / 631 个货池 / 15 条 NPC 规则，0 重复、0 个 ask≥market 的坏池**（完整 global 数组）。
- AS/TC/BOT 材料：19 条旅行商人货池；AS/TC 用现有主题商人价 + 配方深度，Botania 用 Shipping 锚；高阶星辉锭/共鸣宝石/虚空锭/魔力钻石只在主题商人 unlock 货架。

仍未覆盖：

- GT/Mek/AE2/太空/污染等工业章节：保留给玩家产线，不做顾客商品。
- Astral/Thaumcraft/Botania/Technomancy 的机器与高阶材料：仍走主题商人/阶段解锁，不做全量顾客池。
- 中州种子、机器、地图等无 Shipping 锚物品：不进普通商品池。
