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

## 4. 暮色森林章节设计（草案）

- **位置**：教程组（`457DCF55318282CA`），`order_index: 6`，标题「V - 暮色森林」。
- **文件**：`config/ftbquests/quests/chapters/twilight_forest.snbt`（`filename: "twilight_forest"`）。
- **本地化前缀**：`ftbquests.chapter.twilight_forest.*`。
- **结构**（约 20~28 个任务，线性 + 少量可选分支）：
  1. 入口/传送门建造（2x2 水 + 12 朵花 + 投掷钻石）
  2. 初见：暮色橡木/树苗、魔法地图、迷宫地图
  3. 娜迦 → 娜迦鳞甲
  4. 巫妖 → 权杖
  5. 米诺陶/迷宫 → 骑士金属
  6. 九头蛇 → 炽热之血
  7. 骑士幽灵 → 骑士金属装备
  8. 厄加斯特 → 炽热之泪
  9. 雪怪（Alpha Yeti）→ 雪怪毛皮
  10. 冰雪女王 → 极光方块
  11. 巨人/高地 → 巨人镐（以本版本实际进度为准）
  12. 收集向可选任务（奖杯墙、护符、矿石磁铁、猪灵交易、不合成台等）
- **任务类型**：以 `item` 为主（与收藏/教程章一致），入口用 `checkmark`；观察/击杀类如无把握不用。
- **奖励**：沿用包内经济（`numismatics:cog` 等）+ 少量 TF 便利物品，避免跳过进度。
- **依赖**：章节内自洽；不依赖其他章节任务，其他章节也不依赖它。

---

## 5. 实施步骤（清单）

- [x] 5.1 `git init`
- [x] 5.2 编写 `.gitignore`（仅跟踪 config、kubejs + 白名单）
- [ ] 5.3 生成 `MODS_BASELINE.md`（392 个 jar 的日期/大小/SHA256）
- [ ] 5.4 基准提交（baseline commit）
- [ ] 5.5 解包 TF jar，导出物品/方块/实体/进度（advancements）/配方 ID 清单
- [ ] 5.6 核对 1.20.1 TF 机制（传送门、Boss 顺序、关键物品用途）
- [ ] 5.7 设计任务树（ID、坐标、依赖、任务、奖励、文本）
- [ ] 5.8 写入 `twilight_forest.snbt`
- [ ] 5.9 写入 zh_cn / en_us 本地化文本
- [ ] 5.10 静态验证（SNBT 可解析、ID 存在、lang 键齐全、无重复 ID）
- [ ] 5.11 更新 `analyze_ftb_quests.py` 索引并复核
- [ ] 5.12 章节提交（feat commit）
- [ ] 5.13 更新本指南进度日志

---

## 6. 验证清单

- [ ] 新章节 SNBT 可被解析器解析，字段顺序与现有章节一致
- [ ] 章节 ID / 任务 ID / 目标 ID / 奖励 ID 全局唯一（16 位大写十六进制）
- [ ] 所有引用的 `twilightforest:*` 物品 ID 均能在 TF jar 中证实存在
- [ ] 所有 `{ftbquests.chapter.twilight_forest.*}` 键在 zh_cn、en_us 中均有值
- [ ] 无跨章节断链依赖；不影响现有任务
- [ ] `git status` 仅显示预期文件；`MODS_BASELINE.md` 与指南已跟踪

---

## 7. 进度日志

| 时间 | 事件 |
|---|---|
| 2026-09-13 | 建立仓库与 `.gitignore`；创建本指南 |
