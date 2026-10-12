# Society: Sunlit Valley — Gregification

一个以**星露谷式田园生活**为底色、叠加 **GregTech 工业主线**的 Minecraft 1.20.1 整合包。

农场的种植、养殖、料理、钓鱼、季节与村民经济构成底层的资源与收入来源；工业、魔法与探索线在其之上展开，并通过材料、配方、交易、要素、战利品与任务彼此连接。

---

## 版本与运行环境

| 项目 | 值 |
|---|---|
| Minecraft | 1.20.1 |
| 模组加载器 | Forge 47.4.23 |
| Java | 17 |
| 启动器 | HMCL |
| 模组规模 | 400+ 个 JAR |

## 玩法结构

- **田园生活与经济** — 以 `Society` 为核心：作物种植、动物好感/心情/产物、钓鱼、NPC 职业与商店、`Shipping Bin` 卖货、`Create: Numismatics` 货币、`Quality Food` 品质系统。
- **季节与天气** — `Serene Seasons` 配合 dew_drop 系列（耕地生长 / 洒水壶 / 每日天气）。
- **工业主线** — `Create` → `GregTech (GTCEu)` → `Mekanism`：能量、材料加工、自动化产线与仓储（AE2 / Refined Storage）。
- **魔法与探索** — Thaumcraft 4 移植版（TC4R）、`Astral Sorcery`、`Botania`、`The Twilight Forest`、`Technomancy`（神秘科技）等支线。
- **太空** — `GCYR` 火箭与推进线，接在工业后期。
- **营养与多样性** — `GTMFO` 五类营养均衡与 `solonion` 食物多样性，鼓励玩家料理多样化。
- **任务引导** — `FTB Quests` 多分支章节，用配方门槛、任务依赖与模组自身进度共同构成“阶段”。

生活玩法仍是资源与经济的底层；工业线提供加工与长期目标；魔法和探索线通过材料、要素与任务相互咬合。

## 目录结构

| 路径 | 说明 |
|---|---|
| `config/` | 模组配置与 FTB Quests 任务数据 |
| `kubejs/` | 整合包脚本：配方、标签、阶段锁、跨模组联动 |
| `pack/` | CurseForge 格式打包源（`release` / `dev` 两套） |
| `docs/` | 设计、联动与维护文档 |
| `mods/` `resourcepacks/` `shaderpacks/` | 运行时内容 |

## 安装与更新

1. 用 HMCL 导入本实例。
2. 启动时由 **ModpackUpdater** 依据远程清单自动同步变更文件。
3. 更新后端：GitHub `MineRealms/UpdateRepo`（Release 标签 `latest` 承载文件，`manifest.json` 承载清单）。
4. 维护与打包流程见 [`docs/MAINTENANCE_GUIDE.md`](docs/MAINTENANCE_GUIDE.md)。

## 文档

全部设计与维护文档在 [`docs/`](docs/)：

- [`docs/PROJECT_OVERVIEW.md`](docs/PROJECT_OVERVIEW.md) — 整合包总览与各系统连接
- [`docs/STATUS.md`](docs/STATUS.md) — 当前进度与遗留事项
- [`docs/MAINTENANCE_GUIDE.md`](docs/MAINTENANCE_GUIDE.md) — 维护、打包、同步流程
- [`docs/FTBQ_GUIDE.md`](docs/FTBQ_GUIDE.md) — 任务书编写规范
- 各联动专项：`GT_INTEGRATION` / `GTMFO_INTEGRATION` / `TC4_INTEGRATION` / `TF_INTEGRATION` / `BOTANIA_INTEGRATION` / `SPACE_INTEGRATION`

## 版权与署名

本整合包基于 **Society: Sunlit Valley** 农场整合包，在其之上叠加 GregTech 工业线与若干魔法 / 探索 / 科技移植内容。所有模组的版权归各自作者所有；本仓库只包含整合包自身的配置、脚本与打包源。
