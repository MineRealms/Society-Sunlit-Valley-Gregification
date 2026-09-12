# 暮色森林任务章节 — 开发指南与进度跟踪

> 本文件用于说明本次工作的目标、约定、步骤与验证方式，并作为进度跟踪清单。
> 每完成一步，勾选对应复选框并在文末「进度日志」追加记录。

---

## 1. 总目标

1. 在整合包实例根目录建立 git 仓库，**仅跟踪 `config/` 与 `kubejs/`**，并生成一份 `mods` 基准表（修改日期 + SHA256）纳入 git。
2. 为 1.20.1（暮色森林 TF 4.3.2508）新增一章**暮色森林教程任务**：
   - 独立任务线，不阻塞现有主线；
   - 风格、命名、ID 规则与现有 FTB Quests 完全一致；
   - 物品/方块 ID 必须来自本包实际加载的 `twilightforest-1.20.1-4.3.2508-universal.jar`；
   - 任务文本加入 `kubejs/assets/ftbquestlocalizer/lang/` 的本地化文件（zh_cn 必做，en_us 同步）。

---

## 2. 仓库约定

| 项目 | 说明 |
|---|---|
| 仓库位置 | 整合包实例根目录（本目录） |
| 跟踪范围 | `config/`、`kubejs/` |
| 白名单例外 | `/.gitignore`、`/MODS_BASELINE.md`、`/TASK_GUIDE.md`（用户要求纳入 git） |
| 忽略 | 其余全部（`mods/`、`saves/`、`logs/`、`resourcepacks/` 等） |
| 基准表 | `MODS_BASELINE.md`：`mods/` 下全部 jar 的 修改日期 / 大小 / SHA256 |
| 提交节奏 | ① 基准提交；② 暮色森林章节提交；后续修改单独提交 |

---

## 3. 关键文件与数据源

| 用途 | 路径 |
|---|---|
| 任务书设置 | `config/ftbquests/quests/data.snbt` |
| 章节组 | `config/ftbquests/quests/chapter_groups.snbt`（教程组 ID：`457DCF55318282CA`） |
| 现有章节样例 | `config/ftbquests/quests/chapters/*.snbt`（29 章） |
| 任务文本 | `kubejs/assets/ftbquestlocalizer/lang/zh_cn.json`、`en_us.json` |
| 快速索引脚本 | 根目录 `analyze_ftb_quests.py`（产出 `ftb_quests_map.json` / `ftb_quests_report.md`） |
| 暮色森林 jar | `mods/twilightforest-1.20.1-4.3.2508-universal.jar`（ID/进度/配方的第一手来源） |
| TF 源码（可选） | 网络不佳时 clone 至 `H:\MinecraftMods\` 本地阅读 |

---

## 4. 暮色森林章节设计（已完成，30 个任务）

- **位置**：教程组（`457DCF55318282CA`），`order_index: 6`，标题「V - 暮色森林」。
  - 章节内任务不依赖任何其他章节；其他章节也不依赖它，属于独立支线。
  - 如需移动位置：改生成器里的 `CHAPTER_GROUP` / `CHAPTER_ORDER` / 标题后重新生成即可。
- **文件**：`config/ftbquests/quests/chapters/twilight_forest.snbt`（章节 ID `367BCDA1BC6451FF`，`filename: "twilight_forest"`）。
- **生成器**：`config/ftbquests/tools/build_twilight_forest_chapter.py`（可重复执行，ID 固定、幂等）。
- **本地化前缀**：`ftbquests.chapter.twilight_forest.*`（zh_cn / en_us 各 98 条）。
- **主线（22 任务，x=0 纵向）**：
  1. 传送门（2×2 水 + 花朵 + 钻石）→ 2. 四种木材 → 3. 魔法地图（核心合成 + 在 TF 内右键填充）
  → 4. 娜迦 → 5. 娜迦鳞甲 → 6. 巫妖（进度锁）→ 7. 四权杖 → 8. 迷宫与米诺菇 → 9. 牛头人沙拉酱肉（火焰沼泽抗热）
  → 10. 九头蛇 → 11. 雪怪首领 → 12. 雪怪毛皮装备（可选）→ 13. 冰雪女王 → 14. 奖杯基座 → 15. 幻影骑士
  → 16. 恶魂陷阱（砷铅铁）→ 17. 暮初恶魂 → 18. 最终进军（三巨头）→ 19. 余烬之灯 → 20. 魔豆与豆茎
  → 21. 巨人镐 → 22. 进度完成（高原施工中）
- **支线（8 任务）**：月光蠕虫女王、矿石磁铁、转换粉末、拆解台、谜题羊、魔法树、玻璃剑、奖杯墙（8 奖杯毕业）。
- **任务类型**：全部 `item` + 3 个 `checkmark`；未使用观察/击杀类任务，避免版本行为差异。
- **奖励**：`numismatics:cog` 为主 + 生命符咒/瓦解之号角等 TF 便利物品。
- **机制依据（TF 1.20.1 / 4.3.2508 源码核对）**：
  - 传送门：水塘 ≥4 格、边缘为泥土类方块、其上为 `PORTAL_DECO`（花/树苗/树叶/作物）、投掷 `#forge:gems/diamond`。
  - `tfEnforcedProgression` 默认开启：巫妖塔/迷宫/雪怪洞/极光宫殿/骑士要塞/幽冥高塔/巨魔洞穴等按成就顺序锁定。
  - 空白魔法/迷宫/矿物地图需在对应场景内右键填充为 `filled_*`。
  - 关键获取途径与掉落数量均来自 jar 内 loot table / recipe（如娜迦 6~11 鳞片、雪怪首领 6 毛皮、炽铁锭 = 炽热之血/泪 + 铁锭）。

---

## 5. 实施步骤（清单）

- [x] 5.1 `git init`
- [x] 5.2 编写 `.gitignore`（仅跟踪 config、kubejs + 白名单）
- [x] 5.3 生成 `MODS_BASELINE.md`（392 个 jar 的日期/大小/SHA256）
- [x] 5.4 基准提交（baseline commit `ab54ed1`，6418 个文件）
- [x] 5.5 解包 TF jar，导出物品/方块/实体/进度（advancements）/配方 ID 清单
- [x] 5.6 核对 1.20.1 TF 机制（传送门、Boss 顺序、关键物品用途）
- [x] 5.7 设计任务树（ID、坐标、依赖、任务、奖励、文本）
- [x] 5.8 写入 `twilight_forest.snbt`（30 任务，章节 ID `367BCDA1BC6451FF`）
- [x] 5.9 写入 zh_cn / en_us 本地化文本（各 98 条，最小插入 diff 98/0）
- [x] 5.10 静态验证（SNBT 可解析、ID 存在、lang 键齐全、无重复 ID）
- [x] 5.11 更新 `analyze_ftb_quests.py` 索引并复核（30 章 / 1173 任务）
- [ ] 5.12 章节提交（feat commit）
- [ ] 5.13 更新本指南进度日志

---

## 6. 验证清单

- [x] 新章节 SNBT 可被解析器解析，字段顺序与现有章节一致
- [x] 章节 ID / 任务 ID / 目标 ID / 奖励 ID 全局唯一（16 位大写十六进制，全库 3051 个 ID 无冲突）
- [x] 所有引用的 `twilightforest:*` 物品 ID 均能在 TF jar 中证实存在（54 个物品全部命中）
- [x] 所有 `{ftbquests.chapter.twilight_forest.*}` 键在 zh_cn、en_us 中均有值（各 98 条，0 缺失）
- [x] 无跨章节断链依赖；不影响现有任务（章节根任务无依赖，其他章节未改动）
- [x] `git status` 仅显示预期文件；`MODS_BASELINE.md` 与指南已跟踪

---

## 7. 进度日志

| 时间 | 事件 |
|---|---|
| 2026-09-13 | 建立仓库与 `.gitignore`；创建本指南 |
| 2026-09-13 | 生成 mods 基准表（392 文件 / 0.89 GiB）并完成基准提交 `ab54ed1` |
| 2026-09-13 | 解包 TF jar：645 个物品 ID、70+ 实体、17 条进度成就、Boss 掉落与配方全部导出 |
| 2026-09-13 | clone TF 源码 `1.20.1` 分支至 `H:\MinecraftMods\twilightforest`，核对传送门/进度锁/地图填充等机制 |
| 2026-09-13 | 完成 30 任务章节生成器与中英文本；验证全部通过（30 章 / 1173 任务 / 3051 个唯一 ID） |
| 2026-09-13 | 生成器幂等性修正（排除自身文件 + 保留文件尾换行），语言文件实现最小插入（98/0） |
