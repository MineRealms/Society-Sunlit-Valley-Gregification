# GregTech 内容集成记录（Society: Sunlit Valley）

> 本文档记录「基于本包已有模组，引入 GT 矿脉生成 + 批量搬运 GT 社区包任务书并汉化」的完整工作。
> 规则沿用 `GTMFO_INTEGRATION.md`：每阶段独立提交、语法/结构自检、可回滚、脚本可重复执行。
> 原则：**不新增模组**，只使用本包已加载的 GT 生态（gtceu 7.5.3 + GTCA / GTMFO / GTSE / GTNN / GTMM 等）。

---

## 0. 内容一览

| 模块 | 文件 | 说明 |
|---|---|---|
| 世界生成层 | `kubejs/startup_scripts/gt/worldGenLayers.js` | 暮色森林 / 骷髅洞穴的 GT 可替换岩层 |
| 矿脉注入 | `kubejs/server_scripts/gt/oreVeins.js` | 22 种主世界矿脉 × 2 维度 = 44 条 |
| 任务分组 | `config/ftbquests/quests/chapter_groups.snbt` | 新增分组「格雷科技」`9F2C7A5E1B3D4C60` |
| 任务章节 | `config/ftbquests/quests/chapters/*.snbt`（17 章） | 社区包整套任务书（674 任务） |
| 奖励表 | `config/ftbquests/quests/reward_tables/*.snbt`（8 个） | bronze_age / hv / titanium 等 |
| 搬运脚本 | `config/ftbquests/tools/port_gregtech_quests.py` | 文本键化 + 缺失物品替换 + 分组/排序 |
| 翻译脚本 | `config/ftbquests/tools/translate_gregtech_quests.py` | 术语表 + 批量翻译 + 缓存/断点续传 |
| 翻译工作区 | `config/ftbquests/tools/gt_port/` | 英文条目 / 中文条目 / 翻译缓存 |
| 本地化 | `kubejs/assets/ftbquestlocalizer/lang/{zh_cn,en_us}.json` | 3707 条 × 2 语言 + 分组标题 |

对应提交：
- `6c708f3` feat: GT 矿脉注入暮色森林与骷髅洞穴（22 种主世界矿脉 × 2 维度）
- `d2e5f3a` feat: 批量搬运 GT 社区包任务书（17 章 674 任务 + 8 奖励表）并汉化

---

## 1. 世界生成：GT 矿脉

### 1.1 机制

- GTCEu 矿脉由 `ChunkGeneratorMixin` 注入 `applyBiomeDecoration` 生成，**对所有维度生效**；
  能否生成取决于 `GTOreDefinition` 的**世界生成层（layer）**与**维度过滤**。
- 因此需要：① `GTCEuStartupEvents.registry("gtceu:world_gen_layer")` 注册维度岩层；
  ② `GTCEuServerEvents.oreVeins` 注册使用该层的矿脉。
- 参考：GTCEu 官方文档 `docs/content/Modpacks/Ore-Generation/`。

### 1.2 目标维度

| 维度 | ID | min_y / height | 岩层 targets |
|---|---|---|---|
| 暮色森林 | `twilightforest:twilight_forest` | -32 / 288 | 石头/深板岩标签 |
| 骷髅洞穴 | `society:skull_cavern` | 0 / 512 | 上述标签 + 6 种 `society:skull_*` 岩 |

### 1.3 矿脉与映射

- 逐条镜像 GTCEu 官方 `GTOres.java` 的 22 条主世界矿脉（石头层 14 + 深板岩层 8）。
- 高度重映射：暮色森林 `clamp(y + (deep?20:0), -31, 250)`；骷髅洞穴 `clamp(y + 64, 4, 500)`。
- 每条矿脉带地表指示矿；矿脉 ID：`kubejs:tf_<name>_vein` / `kubejs:skull_<name>_vein`。

### 1.4 限制

1. **只影响新生成区块**（已探索区域不补矿）。
2. 骷髅洞穴 `ore_veins_enabled: false` 不影响 GT（GT 走 mixin）。
3. 调整矿脉：改 `oreVeins.js` 的 `weight/density/remap`。

---

## 2. 任务书批量搬运：「格雷科技」分组

### 2.1 结构

- 新增章节分组 **「格雷科技」**（ID `9F2C7A5E1B3D4C60`），包含 17 章 **674 个任务**：

| 顺序 | 章节 | 任务数 | 主题 |
|---:|---|---:|---|
| 0 | gtceu | 25 | 介绍 / 基础机制 |
| 1 | steam_age | 40 | 蒸汽时代 |
| 2 | lv__low_voltage | 75 | 低压 |
| 3 | mv__medium_voltage | 74 | 中压 |
| 4 | hv__high_voltage | 49 | 高压 |
| 5 | ev__extreme_voltage | 67 | 超高压 |
| 6 | iv__insane_voltage | 37 | 绝缘压 |
| 7 | luv__ludicrous_voltage | 45 | 剧差压 |
| 8 | zpm__zero_point_module | 29 | 零点压 |
| 9 | uv__ultimate_voltage | 24 | 极限压 |
| 10 | ore_generation | 45 | 矿脉生成 |
| 11 | ore_processing | 20 | 矿石处理 |
| 12 | renewability_and_you | 20 | 可再生资源 |
| 13 | multiblock_dilemma | 42 | 多方块图鉴 |
| 14 | heating_coils | 16 | 加热线圈 |
| 15 | progression | 45 | 电路进程 |
| 16 | tips_and_tricks_2 | 21 | 技巧与机制 |

- 8 个奖励表一并搬运（`bronze_age`、`distillation_tower`、`gallium_arsenide`、`hv`、`hv_components`、
  `platinum_group_processing`、`polyethylene`、`titanium`），ID 与本包现有表无冲突。

### 2.2 缺失模组物品替换（18 处）

社区包引用但本包未安装的物品，统一映射为现有替代品（可玩性优先）：

| 原物品 | 替代 |
|---|---|
| `hangglider:hang_glider` | `paraglider:paraglider` |
| `travelanchors:travel_anchor` / `travel_staff` | `waystones:waystone` / `waystones:warp_stone` |
| `storagedrawers:quantify_key` | `functionalstorage:configuration_tool` |
| `craftingstation:crafting_station` | `crafting_on_a_stick:crafting_table` |
| `expatternprovider:tag_storage_bus` / `ex_interface` | `ae2:storage_bus` / `ae2:interface` |
| `expatternprovider:pattern_modifier` / `wireless_connect` / `fishbig` | `ae2:blank_pattern` / `ae2:wireless_access_point` / `minecraft:cookie` |
| `mae2:*_p2p_tunnel` | `ae2:me_p2p_tunnel` |
| `mae2:*_crafting_accelerator` | `ae2:crafting_accelerator`（OR 列表去重） |
| `ae2wtlib:quantum_bridge_card` | `ae2:wireless_receiver` |
| `javd:portal_block` | `minecraft:ender_pearl` |

> 任务文本中仍会提到原模组名（纯文本，无影响）；如需完全改写文本，可编辑
> `gt_port/en_entries.json` 后重跑翻译脚本。

### 2.3 文本键化与 ID 校验

- 所有标题/副标题/描述/任务标题/奖励标题转换为
  `ftbquests.chapter.<file>.quest<ID>.*` 键（与暮色森林章节规范一致）。
- **ID 零冲突**：搬运 ID 1668 个，与本包既有 3031 个 ID 无交集。
- 强校验：674 个任务块内的键 ID 全部与任务自身 ID 一致。

---

## 3. 汉化（翻译流水线）

### 3.1 方案

1. **术语预替换**：从 gtceu / gtca / gtmfo / gtse / gtmthings / gtnn / ae2 的官方 `zh_cn` 语言文件
   构建 5100+ 条英中术语表（含手工补充的通用词条），按最长匹配先替换；
   颜色代码先以占位符保护（避免 `&3Large` 破坏词边界）。
2. **批量翻译**：使用 `clients5.google.com` 免费接口，**每请求合并 40 条文本**（`\n@@@\n` 分隔），
   实测 60 条/请求仍可正确拆分；失败自动回退逐条翻译。
3. **缓存与续传**：`translation_cache.json` 按原文去重缓存（3350 条唯一文本），支持断点续传。
4. **后处理**：修正机器翻译常见偏差（格雷格→格雷、汽轮机→涡轮、多块→多方块 等）；
   修复残留占位符（38 条异常中 17 条完全修复、21 条仅缺失个别颜色码，无乱码残留）。

### 3.2 性能

- 全量 3350 条唯一文本：**约 83 秒**（批量模式），单条模式需 40+ 分钟。
- 翻译覆盖：3707 条语言键，除 295 条 `{@pagebreak}` 分页符（不应翻译）外 100% 覆盖。

### 3.3 重新执行

```bash
# 重新搬运（覆盖 17 章 + 奖励表 + 分组，重建队列）
python config/ftbquests/tools/port_gregtech_quests.py

# 重新翻译（有缓存则跳过；--no-lang 只生成 zh_entries.json）
python config/ftbquests/tools/translate_gregtech_quests.py
```

---

## 4. 验证记录

| 项目 | 结果 |
|---|---|
| `node --check`（两个 GT 脚本） | ✅ |
| GTMaterials 材料字段（70 个） | ✅ 全部存在 |
| 矿脉/章节 ID 唯一性 | ✅ 1668 个搬运 ID 与既有 3031 个零冲突 |
| 任务块键 ID 一致性（674 块） | ✅ 0 不匹配 |
| 物品 ID 校验（替代后） | ✅ 无缺失命名空间引用 |
| 奖励表 ID 冲突 | ✅ 无 |
| SNBT 结构（括号/引号平衡） | ✅ 17 章全部通过 |
| 本地化键完整性 | ✅ 3707 键 × 2 语言，0 缺失 |
| 颜色码完整性 | 3374/3412 完全一致（38 条异常已修复，21 条缺个别颜色码） |
| 占位符乱码残留 | ✅ 0 |

> 运行时验证（需进存档）：打开任务书检查「格雷科技」分组排版与文本；
> 旧存档请前往未探索区域观察新矿脉。建议 `/ftbquests editing_mode` 预览。

---

## 5. 后续可选项（TODO）

- [ ] 人工润色机器翻译文本（重点：长描述、幽默文案、专有名词）
- [ ] 按本包进度调整部分任务奖励（numismatics 货币联动）
- [ ] 为骷髅洞穴各群系差异化矿脉权重
- [ ] 将 `gt_port` 工作文件纳入更新流程（版本升级时增量翻译）
- [ ] 若补充安装 eAE/MAE2/AE2WTLib，可把替代映射还原为原物品

---

## 6. 进度日志

| 时间 | 事件 |
|---|---|
| 2026-09-14 | 侦察 GTCEu 世界生成 API、两维度定义、任务书规范 |
| 2026-09-14 | 新增 `worldGenLayers.js` / `oreVeins.js`；提交 `6c708f3` |
| 2026-09-14 | 手写小章节尝试（已 `308697b` revert，改为整包搬运） |
| 2026-09-14 | 完成 17 章搬运脚本 + 18 处物品替换 + 分组/排序；674 任务块强校验通过 |
| 2026-09-14 | 翻译流水线（术语表 5151 条 + 批量翻译 83 秒）；3707 键写入 zh/en；提交 `d2e5f3a` |
