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

---

## 3. 联动候选（初步，待用户挑选后逐条验证实施）

| # | 方向 | 做法（全部基于已确认能力） | 验证状态 |
|---|---|---|---|
| A | **GT 材料加要素** | 改/加 `object_aspects` JSON：给 `#forge:ingots/*`、`#forge:plates/*`、`#forge:dusts/*` 等 GT 标签加要素（如 metallum/praecantatio） | 待做（JSON 结构已验证） |
| B | **TC4 配方用 GT/Create 材料** | KubeJS `e.recipes.thaumcraft.crucible/infusion/arcane_*` 加配方；数值镜像 TC4 原配方 | 待做（schema 已验证） |
| C | **GT 机器加工 TC4 材料** | 用 GT 研磨/离心/提取处理 TC4 的矿石/材料（需先列出 TC4 可加工材料与 GT 机器适配） | 待调研 |
| D | **Create 机器加工 TC4 材料** | Create 研磨/混合/压合处理 TC4 材料（如要素罐、魔法金属等） | 待调研 |
| E | **Society 经济联动** | 村民/商店收购或出售 TC4 物品（`global.trades` 体系） | 待调研 |
| F | **任务书** | 新增「神秘时代」入门章（参考 GT 17 章搬运模式）或轻量任务 | 待用户决定 |

**限制（先记录，避免踩坑）**：
- TC4 的「要素」不是物品（罐装要素是 `thaumcraft:*` 物品/流体）；跨模组桥接优先走 **要素 JSON + KubeJS 配方** 两条路。
- dev 包版本 20711 > 包内 20708，实施前需确认是否先升级 mods。

---

## 4. 下一步（按顺序）

1. 列出 TC4 本体 `recipes/` 的关键配方类型与代表配方（坩埚/注魔/奥术）→ 作为数值镜像来源。
2. 与用户确认要做哪几条候选（A~F）。
3. 逐条实施：脚本/JSON → `node --check`（JS）/ JSON 校验 → 更新本文件 → git 提交。

---

## 5. 进度日志

| 时间 | 事件 |
|---|---|
| 2026-09-15 | 解包 dev zip，确认 7 个源码/API jar；确认 TC4 内置 KubeJS 插件与 10 个配方 schema；确认研究/要素均为 JSON 数据驱动；建立本文档 |
