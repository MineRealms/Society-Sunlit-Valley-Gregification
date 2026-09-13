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
| R2 | 经济数据（`global.trades` 定价，可卖/价格提示/村民礼物） | ✅ 完成 | `kubejs/startup_scripts/gtmfoTrades.js` | `node --check` + 121 个 ID 静态核对 | 见 git log |
| R3 | 加工配方（Create/FD/Farm&Charm 加工 GTMFO 物品，三批共 21 条） | ✅ 完成 | `kubejs/server_scripts/recipes/addGtmfoRecipes.js` | `node --check` + ID 核对 | 见 git log |
| R4 | GT 配方（GTMFO 机器加工整合包物品，8 条） | ✅ 完成 | `kubejs/server_scripts/recipes/addGtmfoGtRecipes.js` | `node --check` + ID 核对 | 见 git log |

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

## 3. R2 明细：经济数据 ✅

**文件**：`kubejs/startup_scripts/gtmfoTrades.js`（`// priority: -10`，保证在 `globalRegistry.js` 之后执行）

机制：同时 push 进对应数组（供 wikigen/悬赏等系统）+ 写入 `global.trades`（真正的交易表），
`value` 经 `global.getConfiguredValue(value, kind)` 按包内倍率换算；乘数沿用包内语义：
作物/肉/料理 → `shippingbin:crop_sell_multiplier`，酒/酿造 → `shippingbin:wood_sell_multiplier`。

**121 条定价**（参考包内同类，全部为保守值）：
- `global.crops`（39）：洋葱12、番茄24、黄瓜30、茄子42、紫/白蒜27、洋蓟30、生菜24、辣根20、
  罗勒12、牛至12、黑胡椒24、咖啡果12、玉米穗28、大米16、大豆14、豌豆荚10、啤酒花12、棉花16、
  葡萄/白葡萄20、香蕉16、杏24、柠檬40、青柠32、芒果48、橙48、椰子32、橄榄24、
  黑莓20、蓝莓24、树莓20、草莓18、黑/红/白醋栗16、越橘20、接骨木20、蔓越莓18
- `global.animalProducts`（7）：牛肉片16、生培根20、生香肠24、生香肠卷32、调味猪肉36、巴尔格肉48、碎肉3
- `global.cooking`（69）：面包/三明治/汉堡/披萨切片/意面/英式菜/炸物/奶酪/甜点/饮品，
  参考包内（面包16、三明治114-171、派切片150-165、巧克力棒30）
- `global.wines`（2）：红/白葡萄酒 400；`global.brews`（3）：啤酒80、伏特加120、列宁汽水90

自动效果（无需额外代码）：`society:sellable` / `society:farmer_product` 等标签
（`handleItemBlockFluidTags.js` 遍历 `global.trades` 生成）、价格 tooltip（`addPriceTooltips.js`）、
Shipping Bin 售价、村民礼物（`#society:sellable`）。

**静态核对**：`node --check` 通过；121 个条目全部唯一且 ID 均存在于 GTMFO 物品清单。

**回滚**：删除该文件即可（不影响其它轮次）。

**⚠️ 实机首测修复（2026-09-14 03:25）**：
- 现象：`gtmfoTrades.js#19: TypeError: Cannot call method "push" of undefined`（1 个启动脚本错误）
- 原因：**加载顺序**。`globalRegistry.js` 的优先级是 `-20`，而本脚本原为 `-10`；
  KubeJS 规则是 **priority 数值越大越先加载**，所以 `-10` 反而比 `-20` 更早执行 →
  此时 `global.crops` 尚未定义
- 修复：优先级改为 **`-30`**（在 `-20` 之后加载）；已重新 `node --check` 通过
- 教训：写文档时"依赖 globalRegistry.js 先执行"是**假设**，实际必须按包内脚本的真实 priority 排；
  后续新增 startup 脚本一律先查依赖脚本的 priority 再定值

---

## 4. R3 明细：加工配方（第一批 9 条）✅

**文件**：`kubejs/server_scripts/recipes/addGtmfoRecipes.js`

**配方 schema 来源（事实核对，非推测）**：
- `farmersdelight:cutting`：包内 `recipes/addMillingRecipes.js` 的 `addKnifeRecipe` 写法；
  另核对 `FarmersDelight-1.20.1-1.3.2.jar` 的 `data/farmersdelight/recipes/cutting/*.json`（含 `tool` 字段）
- `create:milling`：包内 `addMillingRecipes.js` 的 `addMillRecipe`；另核对 `create-1.20.1-6.0.8.jar`
  自带 `data/create/recipes/milling/*.json`（`processingTime` 为合法字段，支持 `chance`）
- `create:compacting`：包内 `recipes/addPressingRecipes.js`；另核对 `create-1.20.1-6.0.8.jar`
  的 `data/create/recipes/compacting/*.json`（**无** `processingTime` 字段，故不写）

**数值来源（镜像 GTMFO 自身配方，保证与 GT 路径同比例）**：
| 整合包配方 | 输入 → 输出 | 镜像的 GTMFO 配方 |
|---|---|---|
| FD 切菜板 | `gtmfo:cheddar_block` → `gtmfo:cheddar_slice` ×9 | `CheeseRecipes.cheddar_slice`（切片机 1→9） |
| FD 切菜板 | `gtmfo:gorgonzola_wheel_fully_cured` → `gtmfo:gorgonzola_triangular_slice` ×16 | `CheeseRecipes.gorgonzola_triangular_slice`（切片机 1→16） |
| FD 切菜板 | `minecraft:bread` → `gtmfo:bread_slice` ×4 | `BreadsRecipes.bread_slice_by_hand`（手搓刀 1→4） |
| FD 切菜板 | `gtmfo:bun` → `gtmfo:bun_sliced` ×1 | `BreadsRecipes.bun_sliced_by_hand` |
| FD 切菜板 | `gtmfo:baguette` → `gtmfo:baguette_sliced` ×1 | `BreadsRecipes.baguette_sliced_by_hand` |
| Create 研磨 | `gtmfo:cocoa_beans_hulled` → `gtmfo:cocoa_nibs` ×1（200t） | `ChocolateRecipes.cocoa_nibs`（研磨机 1→1） |
| Create 研磨 | `minecraft:potato` → `gtmfo:potato_mashed` ×1（200t） | `CoreChain.mashed_potato`（研磨机 1→1） |
| Create 研磨 | `gtmfo:apple_candy` → `gtmfo:apple_candy_crushed` ×2（400t） | `AppleRecipes.apple_candy_crushed_2`（研磨机 1→2） |
| Create 压块 | `gtmfo:cheddar_curd_mold` → `gtmfo:cheddar_aged_mold` ×1 | `CheeseRecipes.aged_cheddar_mold`（压缩机） |

**静态核对**：`node --check` 通过；9 条配方调用；16 个 `gtmfo:` ID 全部存在于物品清单。

**回滚**：删除该文件即可（不影响 R1/R2）。

### R3 第二批：Create 混合（5 条）✅

**schema 核对**：包内 `recipes/addMixerRecipes.js` + `create-1.20.1-6.0.8.jar` 自带
`data/create/recipes/mixing/chocolate.json`（支持 `fluid` / `fluidTag` 输入、fluid 输出、`heatRequirement`）。

**流体 ID 核对**：GTMFO 材料以 `GTCEu.id()` 注册 → 命名空间是 **`gtceu:`** 而不是 `gtmfo:`。
证据：开发实例 JEI 导出 `H:\tools\jei_names.json` 中存在 `gtceu:apple_extract`、`gtceu:cocoa_butter`、
`gtceu:molten_dark_chocolate`、`gtceu:molten_milk_chocolate`。

| Create 混合配方 | 输入 → 输出 | 镜像的 GTMFO 配方 |
|---|---|---|
| 面团 | `#forge:grain/wheat` ×2 + 水 250 → `gtceu:dough` ×3 | GTCEu `MiscRecipeLoader.flour_to_dough`（混合器同数值） |
| 苹果汁 | 玻璃瓶 + `gtceu:apple_extract` 100 → `gtmfo:juice_apple` ×1 | `CoreChain.apple_juice_bottling`（罐装机 100mB） |
| 橙汁 | 玻璃瓶 + `gtceu:orange_extract` 100 → `gtmfo:juice_orange` ×1 | `CoreChain.orange_juice_bottling`（罐装机 100mB） |
| 熔融黑巧克力 | 糖 + `gtceu:cocoa_butter` 144 + `gtceu:molten_unsweetened_chocolate` 1008 → `gtceu:molten_dark_chocolate` 1152（需加热） | `ChocolateRecipes.molten_dark_chocolate` |
| 熔融牛奶巧克力 | `gtceu:molten_dark_chocolate` 864 + `#forge:milk`(fluidTag) 288 → `gtceu:molten_milk_chocolate` 1152（需加热） | `ChocolateRecipes.molten_milk_chocolate` |

**静态核对**：`node --check` 通过；18 个 `gtmfo:` ID 全部存在；文件内共 14 条配方调用。

### R3 第三批：Create 压制 + Farm & Charm 绞肉机（7 条）✅

**schema 核对**：
- `create:pressing`：包内 `recipes/addPressingRecipes.js`（`createPressingRecipe`）
- `farm_and_charm:mincer`：包内 `addMillingRecipes.js` + `letsdo-farm_and_charm-forge-1.0.4.jar` 的
  `data/farm_and_charm/recipes/mincer/*.json`；**合法 `recipe_type`：MEAT / STONE / METAL / WOOD**（统计自 jar 内 56 条配方）

| 配方 | 输入 → 输出 | 镜像的 GTMFO 配方 |
|---|---|---|
| Create 压制 | `gtceu:dough` → `gtmfo:flat_dough` ×1 | `GTMFORecipes.dough_flat`（锻锤） |
| 绞肉机 ×6 | 牛肉/猪肉/鸡肉/羊肉/兔肉/生水牛肉 → `gtceu:meat_dust` ×1（MEAT） | GTFO 手搓肉末（臼+肉 → 肉末 1:1）；`gtceu:meat_dust` = "Mince Meat"（证据：JEI 导出） |

> 说明：肉末进 GTMFO 烘焙炉即得 `gtmfo:mince_meat_cooked`（GTFO 原有链）✓

### R3 后续批次（可选待办）
- 意面面团 / 披萨面团等中间品（需先核对 GTMFO 现有配方）
- Create 压制：马苏里拉/帕尔玛等奶酪成型（需先核对 GTMFO 对应配方数值）

---

## 4.5 R4 明细：GT 配方（GTMFO 机器加工整合包物品，8 条）✅

**文件**：`kubejs/server_scripts/recipes/addGtmfoGtRecipes.js`

**事实依据（源码核对，非推测）**：
- GTCEu 7.5.2 `integration/kjs/GregTechKubeJSPlugin.registerRecipeSchemas`：
  每个 GT 配方类型注册为 `event.recipes.<namespace>.<path>`
- GTMFO 自定义配方类型经 `GTRecipeTypes.register("slicer"/"extractor", ...)` 注册，
  内部用 `GTCEu.id(name)` → **命名空间是 `gtceu:`**（证据：JEI 导出分类 `gtceu:slicer` 等）
- 方法来自 `GTRecipeSchema.GTRecipeJS`：`itemInputs` / `itemOutputs("Nx id")` / `notConsumable` /
  `outputFluids` / `duration` / `EUt`；id 会自动加 `<类型路径>/` 前缀
- `Fluid.of("id", mB)`：与包内 `globalBlockEntityHandlers.js` 写法一致（KubeJS 自动转换字符串）

| GT 配方 | 输入 → 输出 | 镜像的 GTMFO 配方 |
|---|---|---|
| 切片机 | `farm_and_charm:onion` → `gtmfo:onion_slice` ×8 | `CoreChain.slice_onion`（EUt18/30t，平板刀片） |
| 切片机 | `farmersdelight:tomato` → `gtmfo:tomato_slice` ×8 | `CoreChain.tomato_slice` |
| 切片机 | `vintagedelight:cucumber` → `gtmfo:cucumber_slice` ×8 | `CoreChain.slice_cucumber` |
| 切片机 | `society:eggplant` → `gtmfo:eggplant_slice` ×8 | `CoreChain.slice_eggplant` |
| 提取机 | `pamhc2trees:orangeitem` → 碎皮粉 + `gtceu:orange_extract` 100 | `CoreChain.orange_zest`（EUt5/100t） |
| 提取机 | `atmospheric:orange` → 同上 | 同上 |
| 提取机 | `pamhc2trees:lemonitem` → 碎皮粉 + `gtceu:lemon_extract` 100 | `CoreChain.lemon_zest` |
| 提取机 | `farmersdelight:tomato` → `gtceu:tomato_sauce` 100 | `CoreChain.tomato_sauce`（EUt2/10t；GTFO 用番茄片，此处用整番茄） |

**静态核对**：`node --check` 通过；5 个 `gtmfo:` ID 全部存在；8 条配方。

**注意**：GT 配方需要玩家有 GT 电力（LV+）；R3 的 Create/FD 配方已提供非 GT 路径。

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
