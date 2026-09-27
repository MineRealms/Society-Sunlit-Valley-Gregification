# Society: Sunlit Valley Gregification — 整合包总览

> **2026-09-27 增量**：已更新 Pollution 并安装 Astral Sorcery；当前 403 JAR、54 章节。新增 Pollution 42 任务、AS 69 任务及 39 个 AS 物品/设备的 TC4 要素。两章采用三列两行主题分区，详见 `config/ftbquests/tools/pollution_quest_plan.md`、`astral_sorcery_quest_plan.md`。仅完成静态验证，未启动游戏。下方表格保留 9/25 快照。

> 核对日期：2026-09-25。依据本地文件、当前提交 `70b2b98` 及其前序提交。
> 本文介绍当前工程；[STATUS.md](STATUS.md) 记录未完成事项；专项文档保留实现细节和历史。
> “文件存在”“加载成功”“游戏内实测通过”是不同的证据等级，本文不把它们混为一谈。

## 1. 整合包定位

本项目以 Society: Sunlit Valley 的农场生活、季节、养殖、料理、钓鱼、村民交易和社区收集为基础，加入 GregTech 工业主线，并把 Create、Mekanism、Thaumcraft 4 移植版、Botania 和 GCYR 太空线接入资源加工与任务引导。

生活玩法仍是底层经济和资源来源。工业线提供材料加工、自动化与长期目标；魔法和探索线通过材料、交易、要素、战利品和任务相互连接。这里的“阶段”有三种实现：配方原料要求、任务依赖、模组自身进度机制。任务未解锁不等于物品无法合成。

## 2. 当前实例与版本

| 项目 | 2026-09-25 本地核对结果 |
|---|---|
| Minecraft | 1.20.1，Forge 生态 |
| 活跃模组目录 | `mods/`，顶层 402 个 JAR；当前没有 `mods1/` |
| 活跃脚本目录 | `kubejs/`；当前没有 `kubejs.disabled/` |
| 脚本数量 | server 208、startup 101、client 19 个 `.js` 文件（含子目录） |
| Create | 6.0.8 |
| GTCEu | 7.5.3 |
| Mekanism | 本体、Additions、Generators、Tools 均为 10.4.16.80 |
| GregMek | `gregmek-1.0-SNAPSHOT.jar`；文件名不是唯一版本指纹 |
| GTMFO | 本地文件为 `gtmfo-0.0.9.jar` |
| TC4 移植版 | `thaumcraft-forge-4.2.3.5-1.20.1-port.0.1.0-20711.jar` |
| MAE2 | 2.0.1 |
| 任务书 | 52 个章节文件；MEK 58、太空 30、TC4 17、暮色 30、营养 3 个任务（按当前章节结构统计） |
| 下载清单 | `manifest.json` 与 `modpack.cfg` 内嵌清单均为 364 项；不等于 JAR 数量 |

`MODS_BASELINE.md` 是上次 SHA256 快照，不是每次启动自动更新的清单。例如其表中 GTMFO 0.0.8 已落后于当前 0.0.9；即使 JAR 总数仍为 402，也不能据此认为二进制完全一致。Forge 版本、Java 版本及服务端内核应分别从实际启动信息核对，不能用 CurseForge manifest 的 loader 字段代替。

## 3. 生活、经济与营养

原包的 Society 脚本覆盖作物、生长与季节、动物好感/心情/产物、钓鱼、NPC、礼物、商店、Shipping Bin 和社区收集。主要入口是 `kubejs/startup_scripts/` 的定义，以及 `server_scripts/entities/`、`playerEvents/`、`recipes/`、`loot/` 和 `datagen/`。

GTMFO 将食品加工接入 GT 机器、作物标签及交易经济。当前新增的营养集成见：

- `kubejs/server_scripts/gtmfo/gtmfoNutrients.js`：五类营养标签和食物数值；每 20 个玩家 tick 更新一次营养阶段标记。
- `config/ftbquests/quests/chapters/nutrition.snbt`：3 个营养任务。
- `config/gtmfo.yaml`：当前 `gtfoNutrientConfig.enabled: true`，每类上限 30、每日衰减 1、标签食品基础值 0.75、死亡重置开启。
- 达标阈值 5，每类增加 1 点最大生命，总上限 5 点（2.5 颗心）；没有配置全营养达标额外药水效果。
- 当前 `exportJeiRecipes: true`，导出目标仍为 `H:/tools/`。此前“默认关闭”的提交不能代表当前配置。

脚本会撤销低于阈值的阶段标记，但 FTBQ 已完成任务是否重新变为未完成，取决于任务机制；不能把阶段值变化直接解释为任务进度回退。

## 4. Create、GT、Mekanism 如何连接

| 连接 | 当前实现 | 边界 |
|---|---|---|
| Create → GT LV | `gt/lockLVBehindCreate.js` 将基础电子电路的真空管改为 Create 电子管；任务书也有 LV 入口依赖 | 需检查替代配方、奖励及交易是否提供绕行路线 |
| Create 加工 GT 材料 | `gt/createBridges.js`：压合板材、覆膜电路板、碎矿、合金粉、橡胶等 5 组桥接 | 桥接的是部分早期材料，并非全材料全机器互通 |
| GT/Create → Mek 入门 | `mek/lockMekBehindGT.js`：灌注机与四台基础机需 GT LV 微处理器；四台机器还需 Create 精密构件 | 未改 `steel_casing`；保留了原来的机壳配方 |
| Mek 电路分层 | 高级电路需要 `gtceu:good_electronic_circuit`；精英需要 `gtceu:advanced_integrated_circuit`；终极需要 `gtceu:micro_processor_computer` | 分别标称 MV/HV/EV 电路，但“电路等级”不自动等于“生产设备已经达到该电压” |
| GT ↔ Mek 选矿 | GregMek 提供材料形态、浆液和处理链桥接 | 应对照当前 JAR、配置和最终配方核验具体产率 |
| 仓储自动化 | AE2、Applied Greg、Applied Mekanistics 等提供各自的接入能力；另有 RS、QIO 等方案 | 多套仓储共存，不代表网络或所有化学品自动互通 |

MEK 高级/精英/终极电路的任务还依赖 GT 的对应电路任务。当前是**消耗指定 GT 电路的配方门槛 + 任务引导**；不能证明整个科技树绝无旁路。尤其“原子合金也必须等 EV 才能制作”这一要求，目前脚本没有直接实现。

原子合金属于 Mek 自定义加工配方，但自定义类型并非“不可修改”。可核对序列化格式后通过同 ID 数据覆盖或删除并重加配方实现；当前没有这类覆盖，不应在文档里宣布已锁定。

## 5. 魔法与探索

| 支线 | 已落地的文件与连接 |
|---|---|
| 暮色森林 | 30 任务；GT 矿脉注入；TF 物品/实体要素；季节、品质、畜牧、交易和礼物联动，见 `TF_INTEGRATION.md` |
| TC4 移植版 | 17 任务；要素/扫描数据；GT 加工配方；TC4 配方；女巫商店和 Shipping Bin，见 `TC4_INTEGRATION.md` |
| Botania | `botania/gateBotania.js` 将早期器件与暮色材料/战利品连接，泰拉钢路线引入 TC4 虚空锭，见 `BOTANIA_INTEGRATION.md` |
| 自定义维度与洞穴 | GT 世界生成脚本覆盖暮色森林与骷髅洞穴；矿脉变更通常需要新生成区块才能观察 |

TC4 的铜/锡/铅/银原生矿簇修补已在 `kubejs/data/thaumcraft/recipes/compat/`：把动态标签输出改成确定物品输出，保留每矿簇 2 锭。原日志中的空产物出现在 GT 代理配方转换路径，不能据此断言整个 TC4 无法使用。修补后的炉子行为和 GT 代理结果仍需实际存档验收。

## 6. 太空与长期目标

GCYR 太空章 30 任务，属于 GT 组，入口依赖 EV 组装机任务。配套脚本位于 `kubejs/server_scripts/gcyr/`：

- `heavyAlloys.js`：为未安装 Ad Astra 的环境补 GTNN 重型合金路线。
- `hardenRockets.js`：火箭零件引入重型板。
- `mekLinks.js`：Mek 氢/氧的相关配方桥接，另有 MekaSuit 热环境标签。
- `gtnnLinks.js`：GTNN 引擎与 GCYR 燃料互通。
- `fixRocketFuels.js`：补汽油/柴油火箭燃料条目；旧的 `EUt(0)` 日志和这份补丁的实际效果应分开判断。

GCYR 的 EUt 会参与引擎等级判断，不能把 EUt 数值 1/2/3 直接当作引擎等级 1/2/3。确切门槛需沿 `RecipeHelper.getRecipeEUtTier` 与当前 RocketEntity 的调用链核验。

## 7. 任务书当前质量与发布边界

任务文本采用内联中文；原 Sunlit Valley 章节的语言键保持原样。GT 章节、暮色、TC4、MEK、太空和营养线组成了多分支任务书。依赖图是玩家的引导，不应冒充配方限制。

当前 MEK 章有 58 个任务，但不能仅凭数量宣称教程完整可靠：

1. **生成器有重复运行风险**：旧 11 任务顺序表仍用于读取扩写后的 58 任务章，见 [FTBQ_GUIDE.md](FTBQ_GUIDE.md)。本次没有运行生成器或重写任务章。
2. **教程文本仍需二次事实校对**：现有文本包括“通电冶炼炉双倍矿”“强化锇”“通用线缆高电压/低损耗”等表述；不能继续作为已核验教程引用。机器显示名、配方数量、气液种类、发电倍率均应查本包最终配方/配置。
3. 过去的 Node 模拟只能证明 JavaScript 模拟环境里的逻辑，不能证明 Rhino、机器库存能力或游戏配方真的工作。

完整的编写与发布要求见 [FTBQ_GUIDE.md](FTBQ_GUIDE.md)，维护及同步流程见 [MAINTENANCE_GUIDE.md](MAINTENANCE_GUIDE.md)。

## 8. 文档索引

| 阅读目的 | 文档 |
|---|---|
| 当前整合包是什么、各系统如何连接 | 本文 |
| 当前缺口、待验收事项、Git 状态 | [STATUS.md](STATUS.md) |
| FTBQ ID、生成器、旧进度、内联文本 | [FTBQ_GUIDE.md](FTBQ_GUIDE.md) |
| KubeJS、配方、日志、打包、HMCL、Git | [MAINTENANCE_GUIDE.md](MAINTENANCE_GUIDE.md) |
| GT/Create/Mek 专项记录 | [GT_INTEGRATION.md](GT_INTEGRATION.md) |
| 食品与营养 | [GTMFO_INTEGRATION.md](GTMFO_INTEGRATION.md) |
| 魔法与探索 | [TC4_INTEGRATION.md](TC4_INTEGRATION.md)、[TF_INTEGRATION.md](TF_INTEGRATION.md)、[BOTANIA_INTEGRATION.md](BOTANIA_INTEGRATION.md) |
| 太空 | [SPACE_INTEGRATION.md](SPACE_INTEGRATION.md) |
| 二进制历史快照 | [MODS_BASELINE.md](MODS_BASELINE.md) |
| 历史调研与最初实施 | [MODPACK_REPORT.md](MODPACK_REPORT.md)、[TASK_GUIDE.md](TASK_GUIDE.md)；旧计数不代表当前状态 |
