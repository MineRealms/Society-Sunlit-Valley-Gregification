# 项目状态快照

## 2026-09-27：Pollution / Astral Sorcery 新增

- 已安装用户指定构建：新版同名 Pollution 替换旧版，Astral Sorcery 新增；当前 403 个 JAR、54 个章节。
- Pollution 42 任务（GT 组 order 31），AS 69 任务（魔法组 order 0）；内联中文、三列两行主题布局，规划与源码证据见 `config/ftbquests/tools/pollution_quest_plan.md` 和 `astral_sorcery_quest_plan.md`。
- 新增 `kubejs/data/thaumcraft/object_aspects/astral_sorcery_aspects.json`：39 个 AS 物品/设备，21 种现有 TC4 要素。数值为本包新增平衡设计，非 AS 原生定义；不区分同物品的晶石 NBT 属性。采用现有 object_aspects 数据格式。
- 两章合并后的静态检查通过：对象 ID、引用、DAG、SNBT、几何布局及重复生成；没有启动游戏。任务物品目标不代表多方块已成形，操作性教程使用明确的手动确认目标。
- Pollution JAR SHA256：`73c3b978087f06692d4cf5718559e745bdf13bbf371abd761a5895280d1a013f`。
- AS JAR SHA256：`b1da676c9f9db3437ce978c848ca4a988caa4c646440afc2eb67f5d977be9663`。
- 旧 Pollution 备份：`C:/Users/ADMINI~1/AppData/Local/Temp/opencode/pollution-1.20.1-1.0.0-1.20.1-port.0.1.0.jar.89dddc11d1544cd4.bak`。
- 下方 9/25 基线为历史快照；本轮未提交或推送。

> 最后核对：2026-09-25。总览：[PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)。
> 本页记录当前状态和缺口；历史过程见各专项文档，不再将历史待办与当前完成项混排。

## 当前基线

- 分支 `master`，本轮开始时 HEAD 为 `70b2b98`；与本地记录的 `origin/master` 一致（未执行 fetch，不代表已实时查询远端）。
- 活跃目录为 `mods/`、`kubejs/`；没有 `mods1/` 或 `kubejs.disabled/`。
- 当前顶层 402 个模组 JAR、52 个任务章节；MEK 58、太空 30、TC4 17、暮色 30、营养 3 个任务。
- 当前 GTMFO JAR 是 0.0.9，TC4 移植版是 20711；旧文档里的 0.0.8/20708 是历史状态。
- `MODS_BASELINE.md` 为上次哈希快照；当前数量相同不意味着哈希/版本相同。

## 系统落地情况

| 系统 | 当前文件实现 | 验证边界 |
|---|---|---|
| Society 生活与经济 | 完整 kubejs 定义、加工、养殖、商店、Shipping Bin、季节/钓鱼体系 | 需随模组更新复核 ID、标签和产物 |
| Create → GT | LV 电子管配方门、任务前置、5 组加工桥接 | 有历史加载日志；不等于所有最终配方已实测 |
| GT → Mek | 基础机 LV 微处理器 + Create 精密构件；高级/精英/终极电路使用 GT MV/HV/EV 电路 | 原子合金本身未硬锁 EV；电路等级与生产阶段需区分 |
| GregMek | 矿物形态、浆液及加工路线 addon | 具体产率、互通与 JEI 显示仍需实际验收 |
| TC4/TF/Botania | 要素、实体、加工、交易、战利品与任务联动 | 见专项文档及维护手册中的兼容修补边界 |
| GCYR/GTNN/Mek | 重型合金、火箭零件、氢氧与燃料配方桥接 | 新汽油/柴油条目需验证最终配方及油箱接受行为 |
| GTMFO 营养 | `gtmfoNutrients.js` + 营养任务章；当前营养开启、每日衰减、死亡重置 | 阶段撤销不保证 FTBQ 已完成任务回退 |
| 展示工具 | `gt_demo.js`，钢板条箱版本，指令触发 | 没有本轮游戏内验收；历史 Node 模拟不作通过凭据 |

## 优先待办

1. **修复 MEK 生成器重复运行安全性**：`load_previous_ids()` 对当前 58 任务仍使用旧 11 项顺序，压缩机/分离器会读到精英/终极电路 ID。本轮只读复现，未运行生成器。具体映射见 [FTBQ_GUIDE.md](FTBQ_GUIDE.md)。
2. **MEK 任务内容复核**：检查倍矿、电缆、化学氧化、强化材料、喷气背包燃料、核工业和装备描述。上一轮“已核对所有事实”结论过强。
3. **兑现原子合金 EV 硬锁需求**：目前只修改电路合成配方。自定义加工类型不代表不可修改，需核对实际配方 JSON/schema 后实现并查旁路。
4. **兼容补丁运行验收**：TC4 四种矿簇、GCYR 汽油/柴油、FFB 树苗、Curios 槽位、GLM 列表。文件与静态检查已落地；不要提前宣布日志消失或玩法恢复。
5. **服务器发布清单**：排除 Node 测试文件；服务器旧日志曾加载 `gt_demo_sim_v6.js`，需在目标机确认已删除；旧同步 ZIP 不能当作自动更新包。
6. **启动器管理**：两份 manifest 各 364 项，但是否完全停止 HMCL 自动修复还需启动验证。

## 当前 Git 未提交变动（本轮文档编辑前）

7 个已跟踪文件有修改，暂存区为空：

- `config/CSC/Log/CSC_Record.log`
- `config/everycomp-entries.toml`：新增 Pollution 树叶类型配置。
- `config/fabric/indigo-renderer.properties`
- `config/jei/recipe-category-sort-order.ini`
- `config/oculus.properties`
- `config/packetfixer.properties`：本次 diff 为时间戳变化。
- `config/pollution-common.toml`：新增地形转化开关、阈值 25 和每 tick 预算 4；这是功能配置，不能当普通日志删除。

未跟踪的备份/导出与工具目录：`config/forge-client-1.toml.bak`、`config/ftbquests.zip`、`config/ftbquests/quests.7z`、`config/pollution-jei-dump.txt`、`config/pollution-jei-tooltip.log`、`config/tools/`、`config/warpload-common.toml.bak`。本次均保留。

## 最近关键提交

| 提交 | 内容 |
|---|---|
| `70b2b98` | MEK 生成器与文档；生成器安全性仍见当前待办 |
| `f9ebcb4` | 58 任务 MEK 章节、Mek 电路锁及 GTMFO 配置 |
| `23767a8` | GTMFO 营养脚本、营养任务章及配置 |
| `9b4dfc8` | 取消跟踪机器本地的 HMCL 配置 |
| `d367d16` | 恢复 kubejs 全量树，兼容数据与展示脚本 |
| `7b130e4` | 太空章节/资源与 GCYR 联动 |

## 维护入口

- 全面介绍及文档导航：[PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)
- FTBQ 规范与历史坑：[FTBQ_GUIDE.md](FTBQ_GUIDE.md)
- KubeJS、日志、HMCL、同步与 Git：[MAINTENANCE_GUIDE.md](MAINTENANCE_GUIDE.md)
- 新增任务使用内联中文；原包章节的语言键不统一重写。维护时优先修改当前事实源，历史日志保留原日期和验证范围。
