# 暮色森林 × Sunlit Valley 农业联动分析

> 目的：盘点暮色森林（TF）的农业/植物内容，与包内农业/经济系统的联动点，并标注 KubeJS 可行性。
> 事实来源：TF jar 反编译（javap 方法签名）、包内 KubeJS 源码、Serene Seasons jar 标签。
> 最后更新：2026-09-16

---

## 1. TF 农业/植物内容（已核对）

### 1.1 可种植 / 可催熟的植物（javap 反编译证据）

| 方块 | 机制结论（反编译） | 农场化 |
|---|---|---|
| `twilightforest:torchberry_plant` | 实现 `BonemealableBlock`（`has_berries` 属性 + `performBonemeal` + 右键收获） | ✅ 骨粉催熟 + 收获 |
| `twilightforest:mushgloom` | 继承 `MushroomBlock`（`isValidBonemealTarget` → 巨菇 `BigMushgloomFeature`） | ✅ 蘑菇式种植/催熟 |
| `twilightforest:unripe_trollber` | `randomTick` + `RIPEN_THRESHOLD` 自然成熟 | ✅ 可等待成熟 |
| `twilightforest:uberous_soil` | `BonemealableBlock` + tick/neighborChanged（lambda 用 FakePlayer 自动对上方植物施骨粉） | ✅ 生长加速器 |
| `twilightforest:growing_beanstalk` + `magic_beans` | 方块实体 ticker 生长 | ✅ 豆茎农场 |
| 各树苗（twilight_oak / canopy / mangrove / darkwood / time / transformation / mining / sorting / hollow_oak / rainbow_oak） | 普通树苗 | ✅ 树木农场 |
| `huge_lily_pad` / `huge_water_lily` | 水面放置 | ✅ 装饰/种植 |

### 1.2 农产品 / 食物 / 材料（物品 ID 已核对）

- **食物**：`torchberries`、`raw_venison`/`cooked_venison`、`raw_meef`/`cooked_meef`、`meef_stroganoff`、`hydra_chop`、`maze_wafer`、`experiment_115`、`trollber`/`unripe_trollber`、`magic_beans`
- **农业材料**：`liveroot`、`steeleaf_ingot`、`ironwood_ingot`、`raven_feather`、`arctic_fur`、`alpha_yeti_fur`、`naga_scale`、`knightmetal_ingot`
- **木材**：TF 全系原木（含 4 种魔法原木）
- **动物**：bighorn_sheep、deer、boar、squirrel、penguin、raven、dwarf_rabbit、quest_ram 等

---

## 2. 包内农业/经济系统（实现方式与数据入口）

| 系统 | 实现 | 入口（KubeJS） |
|---|---|---|
| 卖货价格 | `global.trades`（`{value, multiplier}`） | startup 脚本（priority -30 后写，参考 `gtmfoTrades.js`） |
| 分类列表 | `global.crops` / `animalProducts` / `artisanGoods` / `cooking` / `pristineItems`（`globalRegistry.js` 末尾 forEach → trades） | 同上 |
| 品质食物 | `quality_food:material_whitelist`（物品标签，replace:true） | `kubejs/data/quality_food/tags/items/material_whitelist.json` |
| 季节 | Serene Seasons 方块标签 `sereneseasons:{spring,summer,autumn,winter,year_round}_crops` | KubeJS `ServerEvents.tags("block")` |
| 温室 | `sereneseasons:greenhouse_glass` 标签（玻璃保护作物免受季节影响） | 已存在，无需改 |
| 催熟 | `society:enriched_bone_meal`（8 骨块+1 `farm_and_charm:fertilizer` → 16），由 `enrichedBonemeal.js` 对特定方块右键生效 | KubeJS BlockEvents 可扩展 |
| 畜牧 | `globalAnimalVariables.js`（husbandry/milkable/coopmaster/tierTwo 名单）+ `husbandryDefinitions.js`（挤奶/觅食定义）+ 实体标签 `society:husbandry_animal`（`handleEntityTags.js`） | KubeJS 直接编辑 |
| 村民礼物 | `globalNPCHandlers.js` 的 loved/liked 列表 | KubeJS 编辑 |
| 收集任务 | `config/ftbquests/quests/chapters/crops.snbt`（190 任务） | SNBT（内联中文） |

---

## 3. 联动方案（KubeJS 可行）

### A. 经济：TF 农产品/肉/木材上架 ✅
新脚本 `kubejs/startup_scripts/tfTrades.js`（priority -30）：
- 作物（farmer）：`torchberries 8`、`mushgloom 12`、`trollber 16`、`unripe_trollber 6`、`magic_beans 24`、`liveroot 10`、`mayapple 6`、`fiddlehead 6`
- 肉类（adventurer）：`raw_venison 24`、`cooked_venison 36`、`raw_meef 20`、`cooked_meef 32`、`hydra_chop 120`、`meef_stroganoff 60`、`maze_wafer 12`、`experiment_115 48`
- 木材（artisan）：TF 原木 3~6（魔法原木更高）、planks/stripped 同系
- 材料：`raven_feather 12`、`arctic_fur 32`、`alpha_yeti_fur 96`、`naga_scale 64`、`steeleaf_ingot 24`、`ironwood_ingot 20`、`knightmetal_ingot 48`
- 机制：`global.trades.set(...)` → `handleItemBlockFluidTags.js` 自动加 `society:sellable` + 分类标签

### B. 品质：TF 食物可产出品质 ✅
- TF 食物加入 `quality_food:material_whitelist`（物品标签）；`torchberry_plant` 等可加入 `quality_food:quality_blocks`。

### C. 季节：TF 树苗/植物随季节 ✅
- 标签分配（示例）：spring = twilight_oak/hollow_oak/rainbow_oak 树苗；summer = canopy/mangrove；autumn = darkwood；year_round = time/transformation/mining/sorting 树苗 + mushgloom；torchberry_plant 归 summer。
- 温室玻璃对 TF 作物随之生效（SS 原生逻辑）。

### D. 畜牧：TF 动物入栏 ✅（需逐项设计）
- `globalAnimalVariables.js`：bighorn_sheep（+milkable）、deer、boar、squirrel、dwarf_rabbit
- `husbandryDefinitions.js`：bighorn_sheep → 羊奶；boar → 松露觅食（同猪）；squirrel → 坚果觅食；raven → 羽毛觅食
- 喂食槽/自动抚摸机按 `society:husbandry_animal` 标签工作（已核对 `feedingTrough.js`/`autoPetter.js`），无需改

### E. 村民礼物 ✅
- 例：blacksmith liked += `knightmetal_ingot`/`armor_shard`；witch liked += `torchberries`/`mushgloom`；market liked += `maze_wafer`

### F. 生长辅助：Uberous Soil ✅
- 配方：`society:enriched_bone_meal` + `twilightforest:root`/`liveroot` → `twilightforest:uberous_soil`
- 可选：把 enriched bone meal 的右键催熟扩展到 TF 作物（BlockEvents）

### G. 烹饪 ✅（有限）
- 可以：为 TF 肉写 Farmer's Delight 锅/砧板配方，产出**已有**菜品
- 不能：新增菜品物品（需 Java）

### H. 收集任务 ✅（可选）
- `crops.snbt` 增加 TF 作物条目（内联中文）

---

## 4. KubeJS 做不到的

1. **新增 TF 专属菜品/加工品**（新物品需 Java）
2. **修改 TF 植物生长机制**（`mayPlaceOn`/生长条件由 Java 固定，反编译已确认）
3. **让 TF 动物产出新品类**（只能用包内现成的挤奶/觅食系统）
4. **让 TF 植物原生支持 `society:enriched_bone_meal`**（可用 BlockEvents 模拟，属重实现）
5. （不存在的需求）温室作物白名单——温室靠 SS 标签，已可行

---

## 5. 建议实施顺序

1. **A 经济 + B 品质**（低风险、收益直观）
2. **C 季节 + F 肥料**（农业玩法闭环）
3. **D 畜牧 + E 礼物**（需逐项平衡）
4. G/H 可选
