# 项目状态快照（STATUS）

> 用途：上下文/记忆压缩时的「事实源速览」。详细内容见各专项文档。
> 最后更新：2026-09-22

---

## 1. 已完成（OK）

| 任务 | 主要产出 | 提交 |
|---|---|---|
| git 仓库（仅跟踪 `config/`、`kubejs/` + 白名单） | `.gitignore`、`MODS_BASELINE.md`（402 jar 日期/SHA256，2026-09-22 重算） | `ab54ed1` |
| 暮色森林教程章节（30 任务，中英） | `config/ftbquests/quests/chapters/twilight_forest.snbt` + 生成器 `config/ftbquests/tools/build_twilight_forest_chapter.py` | `8d565c5` 等 |
| 整合包说明报告（给 AI 联动用） | `MODPACK_REPORT.md` / `MODPACK_REPORT.json` | `b9473e8` |
| GT 矿脉注入（暮色森林 / 骷髅洞穴） | `kubejs/startup_scripts/gt/worldGenLayers.js`、`kubejs/server_scripts/gt/oreVeins.js` | `6c708f3` |
| GT 任务书搬运（17 章 563 任务 + 汉化 3707 键） | `GT_INTEGRATION.md` | `d2e5f3a` 等 |
| GTMFO 集成（模组/标签/配方/经济） | `GTMFO_INTEGRATION.md`、`kubejs/assets/gtceu/molecules/` | `62ed42b` 等 |
| **LV 门槛（Create × GT）** | `kubejs/server_scripts/gt/lockLVBehindCreate.js` + Create 章「LV 时代」任务 + GT LV 章 5 入口前置 | `9fb5899` |
| **Create × GT 轻量联动 R2** | `kubejs/server_scripts/gt/createBridges.js`（板材/覆膜板/碎矿/合金/橡胶） | `7b8b379` |
| **TC4 联动分析 + 实施** | `TC4_INTEGRATION.md`（KubeJS 插件/10 配方 schema/候选 A~F → 第 7~8 节调研+实施）；产物：aspects 桥接 JSON、`kubejs/server_scripts/tc/`（GT 加工 + TC4 配方）、`kubejs/startup_scripts/tc4Trades.js`、女巫商店 11 交易 | `625fb77`…本轮 |
| **MEK 科技锁 + MEK 任务章** | `kubejs/server_scripts/mek/lockMekBehindGT.js`（B 方案=LV 微处理器）+ `config/ftbquests/quests/chapters/mekanism.snbt`（11 任务，前置=LV 章铝锭任务 `7567E885B7166603`） | `91961c4` |
| **日志数据修复 + GTCA 兼容** | 4 类标签文件修复（treasure_spot_spawns / longwings / quality_food / zhopo×2，详见 `GT_INTEGRATION.md` 第 9 节）+ `kubejs/server_scripts/gt/gtcaCasingCompat.js`；删除 `_diag_tags.js` | `f7a0128` + 本轮 |
| **TC4 入门任务章** | 新分组「神秘时代」+ `config/ftbquests/quests/chapters/thaumcraft.snbt`（17 任务，独立无前置）+ 生成器 `build_thaumcraft_chapter.py` | 本轮 |
| GregMek 修复与安装（用户完成） | `mods/gregmek-1.0-SNAPSHOT.jar`（30 KB，2026-09-15 22:10）；详见 `GT_INTEGRATION.md` 第 6 节 | 待补 |

---

## 2. 进行中

- **待重启验证**：删除 `_diag_tags.js` 后，`#society:sellable` / `#society:large_eggs` 两条 LMF 报错应消失；GTCA 两个机壳配方应在 JEI 正常显示；zhopo 矿井在骷髅洞穴生物群系生成。
- MEK 锁 + MEK 任务章、TC4 全部联动已实施完毕，详见 `GT_INTEGRATION.md` / `TC4_INTEGRATION.md`。

---

## 3. 待办（TODO）

### 3.1 ✅ MEK 科技锁（已完成，2026-09-15）

- 需求：MEK 基础机器需 GT LV 电路（微处理器，电路组装机产物）+ Create 精密构件；MEK 入门前置 = LV 玩得差不多。
- 实施：`kubejs/server_scripts/mek/lockMekBehindGT.js`（8 处 `replaceInput`）+ MEK 任务章（11 任务，前置 = LV 章铝锭任务 `7567E885B7166603`）。
- 详见 `GT_INTEGRATION.md` 第 6.4 节；校验全通过（node --check / SNBT / ID / lang）。

### 3.2 ✅ TC4 联动（已实施，2026-09-15）

已实施：要素/扫描桥接（16 机器 + 6 金属标签）、GT 加工 3 配方、KubeJS TC4 配方 4 条、女巫商店 11 交易 + Shipping Bin 14 项。
文件：`kubejs/data/thaumcraft/object_aspects/pack_bridge_aspects.json`、`kubejs/server_scripts/tc/`、`kubejs/startup_scripts/tc4Trades.js`、`kubejs/data/society_trading/shops/witch.json`。
详见 `TC4_INTEGRATION.md` 第 7~8 节（含校验结果与运行时验证清单）。

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

---

## 5. 任务书文本约定（2026-09-17 起）

- **新增/修改的任务文本一律内联中文**（直接写在 snbt 里），不写 lang 文件、不做 i18n。
- 我们新增的章节（暮色森林 / 神秘时代 / MEK / GT 17 章）已全部内联；原 Sunlit Valley 章节保持原有 lang 键不动。
- 生成器同步：`build_twilight_forest_chapter.py`、`build_thaumcraft_chapter.py`、`build_mek_chapter.py` 均输出内联中文。

---

## 6. 太空线整合（2026-09-18）

详见 `SPACE_INTEGRATION.md`。摘要：

- **太空任务章**：`config/ftbquests/quests/chapters/space.snbt`（30 任务，内联中文，GT 组 order 18，入口=EV 组装机 `7A55CC71442CC854`）；生成器 `build_space_chapter.py`。
- **火箭硬化**：火箭发动机/燃料罐追加 `gtnn:heavy_plate_t1~t3` ×2（`kubejs/server_scripts/gcyr/hardenRockets.js`）。
- **GT-- 重型合金补全**：GTNN 原重型锭配方依赖未安装的 Ad Astra → 用钛/钨钢/钠钾合金替代补全 T1~T4（`gcyr/heavyAlloys.js`）。
- **Mek 联动**：宇航服氧气天然兼容（forge:oxygen）；补 Mek 氧扩散器配方与 Mek 氢燃料（`gcyr/mekLinks.js`）；全套 MekaSuit 获耐热/耐寒标签（`kubejs/data/gcyr/tags/items/`）。
- **GT-- 联动**：GTNN 火箭引擎燃烧 GCYR 燃料发电；GTNN 高级燃料（RP-1/UDMH/MHN）驱动 GCYR 火箭（`gcyr/gtnnLinks.js`）。

---

## 7. 服务器日志修复与工程整理（2026-09-22）

基于服务器日志（`latest.log` / `debug.log`，431 ERROR / 1032 WARN）的事实分析与修复：

### 7.1 已修复（新增文件，提交 `d367d16`）
- **GCYR 汽油/柴油火箭燃料**：GCYR 0.2.9 以 `EUt(0)` 注册被 GTCEu 7.5.x 拒绝 → `gcyr/fixRocketFuels.js` 以 `EUt(1,1)` 重注册（汽油 25t / 柴油 18t，与原值一致）→ 火箭油箱重新接受二者。
- **TC4 原生矿簇熔炼**（4 条）：`data/thaumcraft/recipes/compat/native_{copper,tin,lead,silver}_cluster_smelting.json` 标签输出 → 固定物品输出（铜=原版铜锭，锡/铅/银=`gtceu:*_ingot`，×2）；同时修复 GT 代理配方空产物报错。
- **Quark 树苗购买**：`quark_saplings.json` 去掉不存在的 `pink_blossom_sapling`（整组解析失败 → 5 个有效树苗）。
- **饰品槽位**：`relics` 实体文件去掉无定义的 `talisman`；补 `society:clock` 槽位定义。
- **战利品表**：`data/forge/loot_modifiers/global_loot_modifiers.json` 改为合法空表（原结构非法报错）。
- **`gt_demo.js`**：钢板条箱展示生成器 v6（`/gtitems`，仅指令触发；Rhino 兼容：函数体内全 `var`）。

### 7.2 工程整理
- **mods 文件夹**：`mods1` → `mods`（402 jar）；旧测试集删除；独有 jar `pollution` / `rosetta_remote_debug_bridge` 备份到桌面 `mods-test-backup-20260922/`。
- **清单清理**：`manifest.json` / `modpack.cfg`（HMCL 依据）删掉本地不存在的 3 条（旧 JEI 15.20.0.129、Emojiful、selectivebounds），防止 HMCL 启动时把旧文件拉回来；资源包/光影条目保留。
- **基线**：`MODS_BASELINE.md` 按 402 jar 重算（新增 6 / 移除 2 / 变更 0）。
- **联动现状**：Create × GT × Mek 事实核对见 `GT_INTEGRATION.md` 第 11 节。

### 7.3 服务器侧手动事项
- 删除服务器 `kubejs/server_scripts/gt_demo_sim_v6.js`（测试脚本误同步，会报 SyntaxError）；
- 同步包：桌面 `starvalley-server-sync-20260922.zip`（10 个文件 + 说明）。
