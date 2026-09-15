# 项目状态快照（STATUS）

> 用途：上下文/记忆压缩时的「事实源速览」。详细内容见各专项文档。
> 最后更新：2026-09-15

---

## 1. 已完成（OK）

| 任务 | 主要产出 | 提交 |
|---|---|---|
| git 仓库（仅跟踪 `config/`、`kubejs/` + 白名单） | `.gitignore`、`MODS_BASELINE.md`（392 jar 日期/SHA256） | `ab54ed1` |
| 暮色森林教程章节（30 任务，中英） | `config/ftbquests/quests/chapters/twilight_forest.snbt` + 生成器 `config/ftbquests/tools/build_twilight_forest_chapter.py` | `8d565c5` 等 |
| 整合包说明报告（给 AI 联动用） | `MODPACK_REPORT.md` / `MODPACK_REPORT.json` | `b9473e8` |
| GT 矿脉注入（暮色森林 / 骷髅洞穴） | `kubejs/startup_scripts/gt/worldGenLayers.js`、`kubejs/server_scripts/gt/oreVeins.js` | `6c708f3` |
| GT 任务书搬运（17 章 563 任务 + 汉化 3707 键） | `GT_INTEGRATION.md` | `d2e5f3a` 等 |
| GTMFO 集成（模组/标签/配方/经济） | `GTMFO_INTEGRATION.md`、`kubejs/assets/gtceu/molecules/` | `62ed42b` 等 |
| **LV 门槛（Create × GT）** | `kubejs/server_scripts/gt/lockLVBehindCreate.js` + Create 章「LV 时代」任务 + GT LV 章 5 入口前置 | `9fb5899` |
| **Create × GT 轻量联动 R2** | `kubejs/server_scripts/gt/createBridges.js`（板材/覆膜板/碎矿/合金/橡胶） | `7b8b379` |
| **TC4 联动分析** | `TC4_INTEGRATION.md`（KubeJS 插件/10 配方 schema/数据驱动资源/候选 A~F） | `625fb77` `43759b1` |
| GregMek 修复与安装（用户完成） | `mods/gregmek-1.0-SNAPSHOT.jar`（30 KB，2026-09-15 22:10）；详见 `GT_INTEGRATION.md` 第 6 节 | 待补 |

---

## 2. 进行中

- **TC4 联动**：分析已完成（报告见 `TC4_INTEGRATION.md`），等待用户从候选 A~F 中挑选后实施。

---

## 3. 待办（TODO）

### 3.1 ★ MEK 科技锁（用户明确要求，务必保留）

**需求**：
1. Mekanism 的基础机器必须等 GT **LV 阶段「基础电路组装机」完成**之后才能制作；
2. 组装机之后的 MEK 机器，合成中加入 **Create 精密构件（`create:precision_mechanism`）**；
3. 整体目标：MEK 科技被 GT LV + Create 双重锁住。

**实施思路（待核对后动手）**：
- 先列出 Mekanism 基础机器配方清单（`mods/Mekanism-1.20.1-10.4.16.80.jar` 的 `data/mekanism/recipes/`）；
- KubeJS：`e.remove({output: 'mekanism:xxx'})` + 重新添加带门槛的配方，或 `e.replaceInput` 替换关键原料；
- 门槛物品：GT LV 电路（`gtceu:basic_electronic_circuit`）/ LV 电路组装机（`gtceu:circuit_assembler`）+ `create:precision_mechanism`；
- 新建脚本建议：`kubejs/server_scripts/mek/lockMekBehindGT.js`。

### 3.2 TC4 联动候选（A~F）

A 要素桥接（给 GT/Create/Society 标签加要素）/ B KubeJS 加 TC4 配方 / C GT 加工 TC4 材料 /
D Create 加工 TC4 材料 / E Society 经济 / F 任务书。详见 `TC4_INTEGRATION.md` 第 4 节。

### 3.3 其它

- TC4 附属（神秘工匠/禁忌魔法/污染魔法/神秘能源）联动调研（可选）。
- TC4 版本：包内 20708（自带 KubeJS schema，够用）；dev 包 20711（按需升级）。

---

## 4. 关键文件索引

- 专项文档：`GT_INTEGRATION.md`、`GTMFO_INTEGRATION.md`、`TC4_INTEGRATION.md`、`MODPACK_REPORT.md`、`TASK_GUIDE.md`
- 脚本：`kubejs/server_scripts/gt/`（LV 门槛 / Create 桥）、`kubejs/server_scripts/recipes/`、`kubejs/startup_scripts/`
- 任务书：`config/ftbquests/quests/chapters/`；文本 `kubejs/assets/ftbquestlocalizer/lang/{zh_cn,en_us}.json`
- 分析工具：根目录 `analyze_ftb_quests.py` → `ftb_quests_map.json` / `ftb_quests_report.md`
- 外部参考：GTCEu 源码 `H:\MinecraftMods\GregTech-Modern-7.5.2`；GT JEI 导出 `H:\tools\jei_names.json`；TC4 dev 包 `D:\Downloads\1.20.1-forge-20711-dev.zip`
