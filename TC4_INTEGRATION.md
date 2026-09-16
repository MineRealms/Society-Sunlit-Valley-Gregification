# Thaumcraft 4（TC4 移植版）× 本整合包 联动分析

> 本文档是「TC4 相关联动分析」的唯一事实源。规则沿用 `GTMFO_INTEGRATION.md`：
> 每阶段独立提交、静态自检、可回滚；**不编造内容**，所有结论标注源码出处。
> 分析对象：`D:\Downloads\1.20.1-forge-20711-dev.zip`（TC4 移植版 20711 源码/API 包）

---

## 0. 当前任务（正在进行）

**用户要求**：分析 TC4 移植版有没有模组联动能力（比如 KubeJS），并规划与本包的轻量联动。
**当前状态**：分析 + 调研完成，**并于 2026-09-15 经用户授权全部实施**（见第 7~8 节：要素/扫描、GT 加工、KubeJS 配方、Society 女巫商店）。
**关键结论速览**：包内已装 20708 自带 10 个 KubeJS 配方 schema，无需升级即可用 KubeJS 加/删 TC4 配方；研究与要素均为纯 JSON 数据。

---

## 1. 源码包结构（已验证）

外层 zip 解出 7 个 jar（`dev` 包名 `dev/tc4port`，版本 **20711**）：

| 目录 | 内容 |
|---|---|
| `tc/` | `thaumcraft-...-20711-api.jar` + `-sources.jar`（本体，5193 个条目） |
| `tt/` | `thaumic-tinkerer-...-20711-api.jar` + `-sources.jar`（神秘工匠） |
| `fm/` | `forbidden-magic-...-20711-sources.jar`（禁忌魔法） |
| `tm/` | `tainted-magic-...-20711-sources.jar`（污染魔法） |
| `te/` | `thaumic-energistics-...-20711-sources.jar`（神秘能源） |

> ⚠️ 版本差：本包 `mods/` 内是 **20708**，dev 包是 **20711**（升级与否待定）。

TC 本体源码包内主要包：`client` 352、`api` 261、`block` 163、`nativeimpl` 156、
`common` 113、`item` 93、`entity` 78、`network` 60、`registry` 54、`compat` 45、
`worldgen` 33、`recipe` 20、`data` 18、`menu` 17、`research` 16、`aspect` 4。

---

## 2. 已确认的联动能力（有源码出处）

### 2.1 KubeJS：**内置官方插件**（重点）

文件：`dev/tc4port/thaumcraft/compat/kubejs/ThaumcraftKubeJSPlugin.java`

- 插件继承 `dev.latvian.mods.kubejs.KubeJSPlugin`，在 `registerRecipeSchemas` 中：
  - 遍历所有 `thaumcraft:*` 配方序列化器，从资源
    `/data/thaumcraft/kubejs/recipe_schema/<类型>.json` 读取 schema 并注册；
  - 自定义输出组件：`thaumcraft:common_metal_output`（支持 tag+数量）、
    `thaumcraft:infusion_result`。
- 可直接用的 **10 个配方 schema**（`data/thaumcraft/kubejs/recipe_schema/`）：

| schema | 用途（键名） |
|---|---|
| `crucible` | 坩埚：`result`(item_stack) / `catalyst`(ingredient) / `aspects`(map) / `research`(可选) / `catalystAspects`(可选) |
| `infusion` | 注魔：`central` / `components`(list) / `instability`(0-499) / `aspects`(map) / … |
| `infusion_enchantment` | 注魔附魔 |
| `arcane_shaped` / `arcane_shapeless` | 奥术工作台（有序/无序） |
| `wand_assembly` | 法杖组装 |
| `banner_dye` | 旗帜染色 |
| `common_metal_crafting` / `common_metal_smelting` | 普通金属加工（输出组件 `common_metal_output`） |
| `jar_label` | 罐子标签 |

- 预期用法（KubeJS 侧，需进游戏复核一次）：
  `ServerEvents.recipes(e => { e.recipes.thaumcraft.crucible(...) })`。
- 也可用标准 `e.remove({ type: 'thaumcraft:infusion' })` 等移除原配方。

### 2.2 数据驱动资源（datapack 可直接改）

`data/thaumcraft/` 内（源码包内已含资源，共 1926 个 JSON）：

| 资源 | 数量 | 说明 |
|---|---|---|
| `recipes/` | **449** | crafting 144 / arcane 106 / infusion 66 / crucible 58 / infusion_enchantment 27 / root 25 / compat 13 / smelting 10 |
| `research/default.json` | 297 KB | **整棵研究树 JSON 化**：`categories` + `entries`（key/category/aspects/坐标/icon/flags/parents/object_triggers…） |
| `object_aspects/` | 9 文件 | 要素定义：`direct`(物品→要素)、`tags`(标签→要素)、`complex`、`derived`、`scan_groups`、`base_overrides`；另有 `dynamic_rules.json`（法杖/药水/装备/附魔规则） |
| `entity_aspects/` | 2 | 实体要素 |
| `data_maps/` | 13 | `crafting_warp`、`equipped_warp`、`pech_values`、`wand_caps`、`wand_rods`、`vis_relay_attunements`、`equipment_abilities`、`block_aspects` 等 |
| 其他 | — | `champion_modifiers`、`golem_definitions`、`focus_catalog`、`pech_trades`、`villager_trades`、`node_ecology`、`outer_lands_definitions`、loot_tables 130、worldgen 32、tags 96 |

> 结论：**要素（aspects）与研究（research）都是纯 JSON 数据**——加联动不需要写代码，
> KubeJS 数据包 / datapack 即可（例如给 GT 的锭、Create 的构件加要素）。

### 2.3 兼容包（compat/）

已有：CraftingTweaks、Curios、Jade、JEI、**KubeJS**（无 CraftTweaker）。

### 2.4 公开 API（api/ 261 文件）

`ThaumcraftApi` / `ThaumcraftApiCommon` / `ThaumcraftApiHelper` / `ThaumcraftContent` /
`ThaumcraftTags` / `AspectApi` / `ChampionApi` / `WardingAuraApi` 等 —— 供附属模组
（神秘工匠 / 禁忌魔法 / 污染魔法 / 神秘能源，源码均在包内）使用。

### 2.5 已安装版本核对（重要）

本包 `mods/thaumcraft-forge-...-20708.jar`（17.91 MB）**已自带 KubeJS 集成**：
- 16 个 kubejs 相关条目、10 个 `data/thaumcraft/kubejs/recipe_schema/*.json`（与 dev 包一致）。
→ **无需升级即可用 KubeJS 加/删 TC4 配方**；dev 包 20711 只是更新版本，可按需再评估。

---

## 3. TC4 内容与配方结构（已核对）

- **内容**：293 物品 / 178 方块；配方 JSON 449 个
  （crafting 144 / arcane 106 / infusion 66 / crucible 58 / infusion_enchantment 27 / root 25 / compat 13 / smelting 10）。
- **配方 JSON 结构（关键：都有 `research` 字段）**：
  - 坩埚 `thaumcraft:crucible`：`{research, catalyst, result, aspects}`；
    KubeJS schema 里 `research` 是 optional_string（**省略 = 无需研究**）。
  - 注魔 `thaumcraft:infusion`：`{research, central, components[], instability, aspects, result}`。
  - 奥术 `thaumcraft:arcane_shaped/shapeless`：`{research, pattern/key 或 ingredients, result, vis}`，
    `vis` 是要素消耗（如 `{"aer": 8}`）。
- **已有跨模组先例**：`recipes/compat/common_metal_*` 全部用**标签 + 条件**
  （如 `forge:ingots/copper` + `forge:tag_empty` 条件判断），说明 TC4 原生按标签与金属模组互通。
- **关键材料物品**：`thaumium_ingot`、`void_ingot`、`alumentum`、`amber`、`quicksilver`、
  `nitor`、`balanced_shard`、`primordial_pearl`、`native_iron_cluster`、`native_gold_cluster`、
  `native_cinnabar_cluster`、`greatwood_log`、`silverwood_log`、各类 shard。
- **附属 mods**（源码均在 dev 包内，均无独立 KubeJS 集成）：
  神秘工匠 95 物品/121 配方；禁忌魔法 63/56；污染魔法 61/80；神秘能源 47/84。

---

## 4. 联动候选（待用户挑选后逐条实施）

| # | 方向 | 具体做法 | 状态 |
|---|---|---|---|
| A | **要素桥接（最安全）** | 在 `object_aspects` 数据里给 GT/Create/Society 的标签加要素（如 `#forge:ingots/*`、`#forge:plates/*`、`#forge:dusts/*`），让 TC4 扫描/坩埚认识新模组材料 | 待做 |
| B | **KubeJS 加 TC4 配方** | `e.recipes.thaumcraft.crucible / infusion / arcane_shaped / ...`：用 GT/Create 材料做 TC4 配方（如用 GT 板做奥术合成、给 GT 装备加注魔配方） | 待做 |
| C | **GT 机器加工 TC4 材料** | GT 研磨/离心处理 TC4 矿（native cluster / cinnabar 等）→ GT 粉尘/金属（需先核对 GT 对应材料 ID） | 待调研 |
| D | **Create 机器加工 TC4 材料** | Create 研磨/压合处理 TC4 材料（需先核对 TC4 有无对应产物与合理数值） | 待调研 |
| E | **Society 经济联动** | 商店/村民交易 TC4 物品（`global.trades` 体系） | 待调研 |
| F | **任务书** | 新增「神秘时代」入门章（可参考 GT 搬运模式）或轻量任务 | 待用户决定 |

**实施注意**：
1. TC4 配方的 `research` 字段决定解锁门槛；新增配方建议复用现有研究键或省略（无条件）。
2. 要素（aspects）与研究（research）都是纯 JSON 数据，datapack/KubeJS data 即可，无需写 Java。
3. 包内已装 20708 自带 KubeJS 插件，**无需升级**；如需 20711 再单独评估。

---

## 5. 下一步（按顺序）

1. 与用户确认要做哪几条候选（A~F）。
2. 逐条实施：脚本/JSON → `node --check`（JS）/ JSON 校验 → 更新本文件 → git 提交。
3. 候选 C/D 需先做「TC4 材料 ↔ GT/Create 加工适配表」（列 TC4 矿/材料与 GT 机器输出）。

---

## 6. 进度日志

| 时间 | 事件 |
|---|---|
| 2026-09-15 | 解包 dev zip，确认 7 个源码/API jar；确认 TC4 内置 KubeJS 插件与 10 个配方 schema；确认研究/要素均为 JSON 数据驱动；建立本文档 |
| 2026-09-15 | 核对包内 20708 已自带 KubeJS schema（无需升级）；盘点 TC4 内容/配方结构/关键材料；给出 A~F 候选清单 |
| 2026-09-15 | **联动方案调研完成**（第 7 节）：要素/标签结构、扫描机制澄清（魔导透镜 vs 护目镜）、GT 加工清单、KubeJS 配方清单、Society 女巫方案；待用户确认 |
| 2026-09-15 | **全部实施完成**（第 8 节）：要素/扫描 JSON（16 机器+6 标签）、GT 加工 3 配方、KubeJS TC4 配方 4 条、女巫商店 11 交易、Shipping Bin 14 项 |

---

## 7. 联动方案调研（2026-09-15，待用户确认）

> 本节记录调研事实与拟定方案，**实施需用户挑选确认**（用户要求：先调查后确认）。

### 7.1 要素/标签桥接（候选 A）— 可行，数据结构已确认

- 数据位置与结构（源码包核对）：
  - `data/thaumcraft/object_aspects/definitions.json`：顶层 `direct`（290 条物品）/ `tags`（40 条标签）/ `complex`（64）/ `derived`（7）等；
  - 标签条目格式（`common_material_aspects.json` 样例）：
    `{"id": "forge:ores/uranium", "aspects": {"metallum": 2, "venenum": 2, "potentia": 2}}`；
  - `data/thaumcraft/data_maps/block/block_aspects.json`：方块要素（`{"mode": "add", "aspects": {...}}`）。
- 拟定：新增数据文件给 GT/Create/Society 标签补要素（如 `#forge:ingots/steel`、`#forge:plates/*`、`#forge:dusts/*`）；
  TC4 已有 40 条标签条目（铁/铜/金/锡/铅/银/黄铜/青铜/铀等），新增时避开重复。

### 7.2 扫描（候选 A 延伸）— 事实澄清 + 方案

- **扫描是魔导透镜（Thaumometer）的功能**：源码 `item/ThaumometerItem.java` → `common/ScanManager.java`；
  **揭示之护目镜**只负责显示要素（`client/GogglesAspectView.java`），本身不扫描（如需要"护目镜扫描"需额外定制）。
- 扫描取要素逻辑（`ScanManager.resolveBlockTarget`）：
  - 方块：`BlockAspectCatalog.resolve(state)`（block_aspects 数据图）＋ 物品 `ObjectAspectResolver.resolve(stack)` 合并；
  - 因此给机器**物品 ID 写要素**即可被扫描（方块形态走其物品堆）。
- 拟定（不追求全覆盖，先做基础机器）：
  - GT：`gtceu:lv_macerator`、`gtceu:lv_assembler`、`gtceu:lv_electric_furnace`、`gtceu:lv_circuit_assembler` 等；
  - Create：`create:mechanical_press`、`create:crushing_wheel`、`create:mechanical_mixer`、`create:deployer` 等；
  - MEK：`mekanism:metallurgic_infuser`、`enrichment_chamber`、`crusher`、`energized_smelter`、`precision_sawmill` 等；
  - 要素示例：能量机器 → `potentia` 2-3 + `machina` 2 + `motus` 1；金属机器 → `metallum` 3 + `instrumentum` 1。

### 7.3 GT 加工 TC4 材料（候选 C）— 拟定清单（待确认）

已核对 ID：
- TC4：`thaumcraft:cinnabar_ore`、`native_cinnabar_cluster`、`quicksilver`、`quicksilver_drop`、`amber`、`amber_bearing_stone`、`amber_block`、`thaumium_ingot`、`void_ingot`、`alumentum`、`{air,fire,earth,water,entropy,order}_shard`、`balanced_shard`、`*_infused_stone`、`greatwood_log`、`silverwood_log`。
- GT：`gtceu:cinnabar_dust`、`gtceu:cinnabar_gem`、`gtceu:cinnabar_ore`、`gtceu:crushed_cinnabar_ore`、`gtceu:mercury`、`gtceu:flowing_mercury`。

拟定配方（数值镜像 GT 惯例，实施时核对形态）：
1. 研磨机：`thaumcraft:cinnabar_ore` → 2× `gtceu:cinnabar_dust`；
2. 研磨机：`thaumcraft:amber_bearing_stone` → `thaumcraft:amber`（数量待定 1~3）；
3. 水银互换：`thaumcraft:quicksilver` ↔ `gtceu:mercury`（形态/数量实现时核对）；
4. （可选）研磨机：`thaumcraft:native_cinnabar_cluster` → `gtceu:crushed_cinnabar_ore`。

### 7.4 KubeJS 加 TC4 配方（候选 B）— 拟定清单（待确认）

KubeJS 用法（schema 已核对）：`e.recipes.thaumcraft.crucible(result, catalyst, aspects[, research])`、
`infusion(central, components, aspects, instability, result[, research])`、`arcane_shaped(pattern, key, result[, vis])`。

拟定：
1. 坩埚：`gtceu:cinnabar_dust` + aspects → `thaumcraft:quicksilver`（GT 水银粉 → 炼金水银）；
2. 奥术/注魔：用 Create 精密构件 / GT 板材替代 TC4 配方中的基础材料（tag 替换，如 `#forge:plates/iron`）；
3. 注魔：给 GT/Create 装备加注魔配方（附魔/属性）——具体目标待定；
4. （可选）坩埚：GT 粉 → TC4 材料（如 `gtceu:gold_dust` → ?）。

### 7.5 Society 经济（候选 E）— 推荐 NPC：女巫（witch）

- 商店系统：`kubejs/data/society_trading/shops/*.json`（现有 39 家，含 `witch.json`；结构：`offer / request(numismatics 货币) / second_request / numismatics_cost / stage_required / trade_id`）。
- **推荐女巫**：魔法主题完全对口（现有商品：`society:sunlit_crystal`、`society:plushie_wand`、附魔书等）。
- 方案：
  - 女巫商店上架 TC4 基础：`thaumcraft:amber`、`quicksilver`、`cinnabar_ore`/`native_cinnabar_cluster`、`*_shard`、`alumentum`（定价参考现有档位）；
  - 玩家出售 TC4 物品：`global.trades`（Shipping Bin 收购价，参照 `gtmfoTrades.js` 先例）。
- 备选：librarian（书/研究主题）、trader（杂货）。

### 7.6 待用户确认清单

1. **要素/扫描**：机器范围（各 mod 5-8 台？是否含多方块）与要素分配是否按 7.2 示例？
2. **GT 加工 TC4**：7.3 的 1~3 条是否全做？数值偏好（1:1 / 1:2）？
3. **KubeJS TC4 配方**：7.4 里挑哪几条？
4. **Society**：女巫商店上架清单与价位档位？是否需要 Shipping Bin 收购？
5. 版本：维持包内 20708（默认）还是升 dev 包 20711？

---

## 8. 实施记录（2026-09-15，已全部实施）

> 用户授权「你来决定，做就完了」后，按第 7 节方案全部落地。

### 8.1 要素 / 扫描（A）

- 新增 **`kubejs/data/thaumcraft/object_aspects/pack_bridge_aspects.json`**：
  - `direct`：16 台基础机器（GT 5 / Create 6 / MEK 5）→ machina / potentia / motus / metallum 等；
  - `tags`：6 条 GT 金属标签（aluminium / nickel / zinc / invar / electrum / stainless_steel；steel 已有不重复）；
  - 依据：`ObjectAspectCatalog` 加载器扫描 `data/*/object_aspects/`（源码 `common/ObjectAspectCatalog.java`）；
    `direct`/`tags` 结构镜像 `definitions.json` / `common_material_aspects.json`（已核对）。
- 扫描链路：`ThaumometerItem` → `ScanManager`（方块 = block_aspects + 物品要素合并）。
- 效果：魔导透镜扫描 GT/Create/MEK 基础机器可发现要素（如能量机器给 potentia）。
- 注意：**扫描用魔导透镜；揭示之护目镜只显示要素**（如要护目镜扫描需另行定制）。

### 8.2 GT 加工 TC4（C）

新增 **`kubejs/server_scripts/tc/tcGtCompat.js`**：

1. 研磨机：`thaumcraft:cinnabar_ore` → 2× `gtceu:cinnabar_dust`（EUt 2 / 400t，镜像 OreRecipeHandler.java:121-128）
2. 研磨机：`thaumcraft:amber_bearing_stone` → 2× `thaumcraft:amber`
3. 提取机：`thaumcraft:quicksilver` → 144mB `gtceu:mercury`（EUt 30 / 60t）

### 8.3 KubeJS TC4 配方（B）

新增 **`kubejs/server_scripts/tc/tcRecipes.js`**（全部 `e.custom` 原始 JSON，规避 schema 参数顺序风险）：

1. 坩埚：`gtceu:cinnabar_dust` + {metallum 2, permutatio 2} → `thaumcraft:quicksilver`
2. 坩埚：`gtceu:steel_ingot` + {praecantatio 4} → `thaumcraft:thaumium_ingot`（研究 THAUMIUM）
3. 坩埚：`gtceu:coke_dust` + {potentia 2, ignis 2} → `thaumcraft:alumentum`（研究 ALUMENTUM）
4. 注魔：`thaumcraft:thaumometer` + [create:precision_mechanism, gtceu:basic_electronic_circuit,
   thaumcraft:balanced_shard, minecraft:gold_ingot] + {sensus 16, auram 8, machina 16}、不稳定 2
   → `thaumcraft:goggles_of_revealing`（研究 GOGGLES，机械魔法路线）

### 8.4 Society 经济（E）

- 女巫商店（`kubejs/data/society_trading/shops/witch.json`）新增 11 条 TC4 基础交易
  （琥珀×4 / 水银×4 / 辰砂矿×2 / 炼金煤×8 / 均衡碎片×1 / 六系碎片×4，各 1 sun = 4096）；
- 新增 **`kubejs/startup_scripts/tc4Trades.js`**：Shipping Bin 收购价 14 项
  （矿物走 gem、碎片/炼金煤走 adventurer；机制与 `gtmfoTrades.js` 相同）。

### 8.5 校验

| 项目 | 结果 |
|---|---|
| `node --check`（3 个 JS） | ✅ |
| `pack_bridge_aspects.json` 解析（direct 16 / tags 6） | ✅ |
| `witch.json` 解析（49 交易、trade_id 无重复） | ✅ |
| 新增配方物品 ID | ✅ 全部核对自 TC4 源码包 / jei_names.json |

### 8.6 待运行时验证（进游戏）

- 魔导透镜扫描机器 → 要素发现提示；
- JEI 查看 GT 加工 / TC4 新配方；
- 女巫商店新交易；Shipping Bin 收购价 tooltip。

### 8.7 入门任务章（FTB Quests，2026-09-16 新增）

- 独立分组「神秘时代」（组 ID `B79B7DF60161F21A`，无前置，可直接开始）；
- 章节 `config/ftbquests/quests/chapters/thaumcraft.snbt`（17 任务，章节 ID `1C53B7E775D8EDDC`）；
- 生成器 `config/ftbquests/tools/build_thaumcraft_chapter.py`（可重复执行）；
- 布局：4 列 × 5 行网格（x 0~7.5 / y 0~10），依赖呈树状分支，无超长单行/单列；
- 任务线（全部核对自 `mods/thaumcraft-...-20711.jar`）：
  1. 魔导透镜（2 金+玻璃+2 碎片）→ 2. 扫描（检查）→ 3. 碎片收集（检查）
  → 4. 宏伟之木；5. 学徒法杖（2 铁杖端+木棍）→ 6. 魔导手册（法杖右手书架成型）
  → 7. 桌子 / 8. 墨水瓶 → 11. 研究台（两桌+墨水瓶）；9. 第一次研究（检查）
  → 10. 坩埚（法杖+炼药锅）→ 13. 闪耀之光 / 14. 炼金煤 / 15. 神秘锭
  → 16. 神秘镐；12. 奥术工作台（法杖+桌子）→ 17. 揭示之护目镜；
- 校验：SNBT 平衡 ✅、53 ID 全局唯一 ✅、17 依赖完整 ✅、文本内联中文（无 lang 依赖）✅、坐标无重叠 ✅。

### 8.8 暮色森林要素桥接（2026-09-16）

- **参考来源**：`G:\DOWNLOAD-EDGE\TwilightAspects.zs`（1.7.10 的 TC4 扩展脚本，ZenScript/ModTweaker 语法）；
- **产出**：`kubejs/data/thaumcraft/object_aspects/twilightforest_aspects.json`（**203 个条目**，direct）；
- **映射方式**：1.7.10 旧 ID → 1.20.1 新 ID（逐条核对 TF jar 的 item/block 清单），数值取自参考脚本；
  - 修正参考脚本拼写：`cognito` → `cognitio`、`viniculum` → `vinculum`；
  - 参考脚本未覆盖的 1.20.1 新物品（迷你蘑菇牛/骑士幽灵/雪怪奖杯、carminite_reactor、盾牌等）按同风格补值；
  - 奖杯 meta 0~4 → 娜迦/巫妖/九头蛇/暮色恶魂/冰雪女王；
  - 植物（TFPlant 各 meta）按主题对应到 1.20.1 方块（moss_patch/clover_patch/fiddlehead/mayapple/fallen_leaves/root_strand/mushgloom/torchberry_plant）；
  - 魔法原木（TFMagicLogSpecial 0~3 → time/transformation/mining/sorting_log，含 arbor 4 + praecantatio 2 + 特性要素）；
  - 普通原木/树苗/树叶仍由原版标签（`minecraft:logs` 等）覆盖，不重复添加；
- **校验**：203 个物品全部存在于 TF jar（item/block 清单）；所有要素名均在 TC4 端口合法集（48 种）内 ✅。
