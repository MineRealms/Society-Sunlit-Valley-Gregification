# Thaumcraft 4（TC4 移植版）× 本整合包 联动分析

> 本文档是「TC4 相关联动分析」的唯一事实源。规则沿用 `GTMFO_INTEGRATION.md`：
> 每阶段独立提交、静态自检、可回滚；**不编造内容**，所有结论标注源码出处。
> 分析对象：`D:\Downloads\1.20.1-forge-20711-dev.zip`（TC4 移植版 20711 源码/API 包）

---

## 0. 当前任务（正在进行）

**用户要求**：分析 TC4 移植版有没有模组联动能力（比如 KubeJS），并规划与本包的轻量联动。
**当前状态**：源码包结构已勘察完毕，联动能力已确认（见第 2 节）；**联动候选方案待用户挑选后实施**。

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
