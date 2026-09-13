# GTMFO × Sunlit Valley 联动进度跟踪

> 本文件是 **GTMFO 与本整合包联动工作的唯一进度事实源**。任何接手的人/AI 先读这里。
> 工作纪律（用户要求）：
> 1. 每轮只动**一个独立主题**，避免链式炸 BUG；先做静态可验证、互不依赖的项目。
> 2. 先**不开客户端测试**；用 `node --check` 做语法自检，必要时用脚本静态核对 ID。
> 3. 每轮结束 **git 提交**（只提交本轮新增/修改的文件，不碰包内既有改动）。
> 4. 每轮结束**更新本文件**（状态表 + 明细 + 下一步）。
> 5. 原则：**不添加新物品**；只做「标签合并 + 配方添加 + 经济数据」。

---

## 0. 上下文交接（给接手者）

| 项 | 值 |
|---|---|
| 整合包目录（= 本 git 仓库） | `G:\MinecraftGames\Sunlit Valley(BaopuEdition)\.minecraft\versions\Society Sunlit Valley` |
| 被整合模组源码 | `H:\MinecraftMods\GregTechModernFoodOption`（GTMFO，1.20.1 Forge，381 物品） |
| GTMFO 整合分析报告 | GTMFO 仓库 `docs/PACK_INTEGRATION_ANALYSIS.md` |
| GTCEu | 包内 **7.5.3**；GTMFO 编译于 7.5.2 → 类级 diff 0 删除/1 新增，二进制兼容 ✅ |
| JEI | 包内 **15.56.0.205**；GTMFO 使用的 API 全部存在 ✅ |
| LDLib | 包内 1.0.52.a（GTMFO 开发环境 1.0.50） |
| KubeJS | 2001.6.5-build.16；GTCEu 自带 KubeJS 集成（可写 GT 配方） |
| 本包食物体系 | forge 标准标签 + Quality Food（吃 `#forge:crops` 等）+ Serene Seasons（`sereneseasons:*_crops`）+ Society 经济（`global.trades`） |
| 暂缓项 | FTB 任务书改动（用户明确暂缓）；GT 配方（R4，可选） |

**包内既有改动（不要提交）**：`config/CSC/...`、`config/fabric/...`、`config/oculus.properties`、
`config/packetfixer.properties`、`config/ftbquests.zip` —— 这些是整合包作者/运行时的改动。

---

## 1. 轮次状态表

| 轮次 | 主题 | 状态 | 新增/修改文件 | 验证方式 | commit |
|---|---|---|---|---|---|
| R1 | 标签合并（forge 标准标签 + 季节标签） | ✅ 完成 | `kubejs/server_scripts/tags/handleGtmfoTags.js` | `node --check` | 见 git log |
| R2 | 经济数据（`global.trades` 定价，可卖/价格提示/村民礼物） | ⏳ 计划 | `kubejs/startup_scripts/gtmfoTrades.js`（拟） | `node --check` + 静态核对 | |
| R3 | 加工配方（Create/FD/Farm&Charm 加工 GTMFO 物品） | ⏳ 计划 | `kubejs/server_scripts/recipes/addGtmfoRecipes.js`（拟） | `node --check` | |
| R4 | GT 配方（GTMFO 机器加工整合包物品，可选） | ⏳ 计划 | `kubejs/server_scripts/recipes/addGtmfoGtRecipes.js`（拟） | `node --check` | |

---

## 2. R1 明细：标签合并 ✅

**文件**：`kubejs/server_scripts/tags/handleGtmfoTags.js`（独立文件，不改动包内既有脚本）

内容：
1. `forge:seeds`：17 个 GTMFO 种子（不含 `seed_unknown`）
2. `forge:crops` + `forge:crops/<name>`：主要作物
3. `forge:vegetables`（+ 子标签）：洋葱/番茄/黄瓜/茄子/蒜/洋蓟/生菜/辣根
4. `forge:fruits`：香蕉/杏/柠檬/青柠/芒果/橙/葡萄/白葡萄/椰子/各类浆果
5. `forge:berries`：黑莓/蓝莓/树莓/黑·红·白醋栗/越橘/接骨木/蔓越莓/草莓
6. `forge:raw_meat`：生培根/生香肠/生香肠卷/牛肉片/调味猪肉/巴尔格肉/碎肉
7. `forge:cooked_meat`：培根/香肠/香肠卷/烤牛肉片/熟肉末/熟肉锭/意式烤肉
8. `forge:cheeses` + `c:cheeses`：马苏里拉/切达/戈贡佐拉/帕尔玛/里科塔
9. `forge:dough`：各类面团 + 未烤面包/法棍/小圆面包
10. `farmersdelight:sweets`：苹果糖/巧克力/棉花糖/全麦饼干/冰淇淋/雪葩
11. `society:need_seeds`：需要种子种植的作物产物（Society 语义：这些作物从种子来）
12. `sereneseasons:*_crops`（**item + block 双标签**）：按季节分配种子/产物/作物方块

季节分配（与包内既有作物对齐）：
- **春**：洋蓟、罗勒、豆、黄瓜、蒜、辣根、生菜、洋葱、牛至、豌豆、大豆、草莓
- **夏**：罗勒、豆、黑莓、黑·红·白醋栗、蓝莓、咖啡、棉花、玉米、黄瓜、葡萄、白葡萄、啤酒花、洋葱、牛至、豌豆、树莓、大米、大豆、草莓、番茄、黑胡椒
- **秋**：豆、黑·红·白醋栗、玉米、蔓越莓、接骨木、茄子、葡萄、白葡萄、辣根、越橘、洋葱、大米、番茄、黑胡椒
- **冬**：蒜（越冬作物，与包内冬季列表同样克制）

> 作物方块 ID 与物品 ID 的对应：`crop_aubergine`=茄子、`crop_garlic`=两种蒜、`crop_hops`=啤酒花、
> `crop_white_grape`=白葡萄、`crop_black_currant`/`crop_red_currant`/`crop_white_currant`=三种醋栗。

**静态核对**：脚本中所有 ID 均来自 GTMFO 仓库的生成资源清单（381 物品 / 31 作物方块）。

**验证方式**：`node --check` 通过；进游戏后可用 `/reload` + F3 调试标签查看（本轮未开客户端，留待后续统一验证）。

**影响面**：纯标签，不改配方/物品；对包内既有内容零破坏（只会让别的模组更认识 GTMFO 物品）。
Quality Food 品质系统会通过 `#forge:crops`/`#forge:seeds` 等自动作用于 GTMFO 作物 ✅
SoLOnion 饮食多样性对所有食物自动生效，无需标签 ✅

---

## 3. R2 计划：经济数据

目标：让 GTMFO 的作物/料理可卖、有价格提示、能当村民礼物。

做法（`kubejs/startup_scripts/gtmfoTrades.js`，`// priority: -10` 保证在 `globalRegistry.js` 之后加载）：
- 把 GTMFO 作物 push 进 `global.crops`、料理 push 进 `global.cooking`、肉制品 push 进 `global.animalProducts`
- `value` 参考包内同类物品（先读取 `globalRegistry.js` 现有数值表再定）
- 自动效果：`society:sellable`/`farmer_product` 标签（由 `handleItemBlockFluidTags.js` 遍历 `global.trades` 生成）、
  价格 tooltip（`addPriceTooltips.js`）、Shipping Bin 售价、村民礼物

风险：定价会影响经济平衡 → 先少量、保守定价；独立文件便于回滚。

---

## 4. R3 计划：加工配方（Create / Farmer's Delight / Farm & Charm）

目标：用整合包的机器加工 GTMFO 物品，给玩家**非 GT 电力**路径。

拟做（照抄包内 `addMillingRecipes.js` 的写法）：
- Create 研磨：`gtmfo:cocoa_beans_roasted`→`gtmfo:cocoa_nibs`、`gtmfo:soybean`→豆粉 等
- Create 压块：奶酪类（马苏里拉/切达）成型
- Create 混合：`gtmfo:juice_*`、面团类
- FD 切菜板：`gtmfo:cheddar_block`→切片、面包→面包片
- Farm & Charm mincer：GTMFO 肉 → `gtmfo:mince_meat_cooked` 前置（生肉末）

原则：只加配方，不动物品；每个配方独立小条目，便于单独回滚。

---

## 5. 决策点 / 风险（持续更新）

1. **GT 电力门槛**：GTMFO 机器是 GTCEu 电力机器（LV+）；本包科技线是 Create。R3 用 Create/FD 配方
   提供非 GT 路径；GT 配方（R4）只做可选补充。
2. **GTCEu 矿石已存在**：包内 GTCEu 世界生成是默认配置（`removeVanillaOreGen: true`），GT 矿石其实已在世界里；
   GTMFO 只是让 GT 食物机器可用。
3. **GTMFO 原版覆盖配置**：`useBakingOvenForMeats` / `useRollingPinForPaper` / `deleteBreadRecipe` 会改原版配方，
   可能撞任务书 → 后续（R3 或单独一轮）评估是否在包内关闭。
4. **暂缓**：FTB 任务章节（用户明确）；JEI 15.56 下 GTMFO 的 JEI 导出工具未验证（可选工具，低优先）。

---

## 6. 回滚方式

- 每轮一个独立文件 → 回滚 = 删除该文件（或 `git revert <commit>`）
- R2 若改 `globalRegistry.js`（不推荐，优先独立 startup 脚本）需特别注意加载顺序
