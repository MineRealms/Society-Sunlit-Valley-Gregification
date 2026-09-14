# GregTech 内容集成记录（Society: Sunlit Valley）

> 本文档记录本次「基于本包已有模组，新增 GT 矿脉生成 + GT 教程任务章节」的完整工作。
> 规则沿用 `GTMFO_INTEGRATION.md`：每阶段独立提交、`node --check` 语法自检、可回滚、可重复执行。
> 原则：**不新增模组**，只使用本包已加载的 GT 生态（gtceu 7.5.3 + GTCA / GTMFO / GTSE / GTNN / GTMM 等）。

---

## 0. 本次新增内容一览

| 模块 | 文件 | 说明 |
|---|---|---|
| 世界生成层 | `kubejs/startup_scripts/gt/worldGenLayers.js` | 为暮色森林 / 骷髅洞穴注册 GT 可替换岩层 |
| 矿脉注入 | `kubejs/server_scripts/gt/oreVeins.js` | 22 种主世界矿脉 × 2 维度 = 44 条矿脉 |
| 任务章节 | `config/ftbquests/quests/chapters/gregtech.snbt` | 「VI - 格雷科技」43 任务 |
| 章节生成器 | `config/ftbquests/tools/build_gregtech_chapter.py` | 可重复执行，固定种子 ID |
| 本地化 | `kubejs/assets/ftbquestlocalizer/lang/{zh_cn,en_us}.json` | 138 条 × 2 语言 |

对应提交：
- `6c708f3` feat: GT 矿脉注入暮色森林与骷髅洞穴（22 种主世界矿脉 × 2 维度）
- `272c03b` feat: 新增 GT 教程章节（43 任务：电压等级/多方块/矿石/联动）+ 中英本地化

---

## 1. 世界生成：GT 矿脉

### 1.1 机制

- GTCEu 的矿脉由 `ChunkGeneratorMixin` 注入 `applyBiomeDecoration` 生成，**对所有维度生效**；
  能否生成取决于 `GTOreDefinition` 的 **世界生成层（layer）** 与 **维度过滤**。
- 因此要让 GT 矿石出现在新维度，必须：
  1. 用 `GTCEuStartupEvents.registry("gtceu:world_gen_layer")` 注册该维度的岩层（决定可替换方块与适用维度）；
  2. 用 `GTCEuServerEvents.oreVeins` 注册使用该层的矿脉。
- 参考：GTCEu 官方文档 `docs/content/Modpacks/Ore-Generation/`（Customizing-Veins / Layers-and-Dimensions / Generators）。

### 1.2 目标维度

| 维度 | ID | min_y / height | 岩层 targets |
|---|---|---|---|
| 暮色森林 | `twilightforest:twilight_forest` | -32 / 288 | `#minecraft:stone_ore_replaceables`、`#minecraft:deepslate_ore_replaceables` |
| 骷髅洞穴 | `society:skull_cavern` | 0 / 512 | 上述两个标签 + `society:skull_stone` / `skull_blackstone` / `skull_arid_sandstone` / `skull_sandstone` / `skull_end_stone` / `skull_permafrost` |

### 1.3 矿脉数据来源与映射

- 矿脉参数**逐条镜像** GTCEu 官方 `GTOres.java`（1.20.1）的 22 条主世界矿脉：
  - 石头层 14 条：磷灰石、锡石、煤、铜锡、方铅矿、石榴石砂、石榴石、铁、润滑、磁铁矿、矿砂、镍、盐、油砂
  - 深板岩层 8 条：铜、钻石、青金石、锰、云母、橄榄石、红石、蓝宝石
- 高度重映射（因为两个维度 min_y / height 与主世界不同）：
  - 暮色森林：`y → clamp(y + (deep ? 20 : 0), -31, 250)`
  - 骷髅洞穴：`y → clamp(y + 64, 4, 500)`
  - Dike 矿脉的绝对 Y 参数同样经过 remap
- 每条矿脉均带 &6地表指示矿&r（surface indicator），便于地面探矿。

### 1.4 重要限制

1. **只影响新生成区块**：已探索区域不会补矿（世界生成缓存 `OreGenCache` 按区块计算）。
2. 骷髅洞穴噪声设置 `ore_veins_enabled: false` **不影响** GT（GT 走 mixin，不走原版矿脉开关）。
3. 矿脉 ID 命名：`kubejs:tf_<name>_vein` / `kubejs:skull_<name>_vein`。
4. 若要单独调整某维度，可修改 `oreVeins.js` 中 `GT_ORE_DIMENSIONS` 的 `remap`，或拆分为两套矿脉。

---

## 2. 任务章节：「VI - 格雷科技」

### 2.1 位置与规模

- 章节组：教程组（`457DCF55318282CA`），`order_index: 7`（接在「V - 暮色森林」之后）
- 章节 ID：`DEB0B9691B5A733B`，图标 `gtceu:lv_machine_hull`
- **43 个任务**，四列布局：
  - `x=0` 主线：入门 → 工具 → 材料 → 蒸汽 → LV → MV → HV → EV → IV → LuV → ZPM → UV → 终章
  - `x=-4.5` 矿石分支：矿脉机制、勘探器、矿石处理 I/II/III、骷髅洞穴/暮色森林矿脉
  - `x=4.5` 多方块分支：蒸汽研磨机、EBF、大化反、蒸馏塔、热解炉、内爆、真空冷冻、装配线、研究站、聚变堆、大型涡轮、大型内燃机
  - `x=9` 联动分支：GTCA/GTMFO 温室、GTSE 农业机器、GT + AE2（applied_greg）
- 文本本地化：`ftbquests.chapter.gregtech.*`（zh_cn / en_us 各 138 条）

### 2.2 物品 ID 校验（静态）

所有任务/图标 ID 均经过三层校验（0 条未验证）：
1. GTCEu 7.5.3 lang（机器/方块，2639 条）
2. 附属 lang（GTCA 189 / GTMFO 649 / GTSE 48 / GTMM 346 / GTNN 403 等）
3. 既有任务书与脚本中的已验证引用（含社区包 852 条任务物品）

校验脚本口径：`id ∈ 上述集合`，排除 `.tooltip` 键。

### 2.3 重新生成（幂等）

```bash
python config/ftbquests/tools/build_gregtech_chapter.py
```

- 固定种子 `20260914`，ID 生成前会收集全库已有 ID，保证全局唯一（当前 157 个 ID，与其他章节 0 冲突）
- 本地化采用「先删除 `ftbquests.chapter.gregtech.*` 再按序插入」，可重复执行
- 修改任务内容后重新运行即可；如需调整位置改 `CHAPTER_ORDER` / 任务 `x,y`

---

## 3. 验证记录

| 项目 | 结果 |
|---|---|
| `node --check`（两个 GT 脚本） | ✅ 通过 |
| GTMaterials 材料字段核对（70 个） | ✅ 全部存在于 `GTMaterials.class` |
| 矿脉 JSON/JS 语法、ID 唯一性 | ✅ |
| 章节 ID 全局唯一（157 个 vs 其他章节） | ✅ 0 冲突 |
| 物品/图标 ID 校验 | ✅ 0 条未验证 |
| 依赖引用完整性 | ✅ 全部指向本章任务 |
| 本地化键（138×2） | ✅ 0 缺失 |
| 任务坐标重复 | ✅ 无重复（4 列 × 21 行） |

> 运行时验证（需进存档）：新开区域观察骷髅洞穴/暮色森林矿石；任务书打开检查排版与文本。
> 提示：旧存档请前往**未探索区域**或新开维度区块；建议先用 `/ftbquests editing_mode` 预览排版。

---

## 4. 后续可选项（TODO）

- [ ] 骷髅洞穴各群系差异化矿脉权重（当前两维度共用同一套矿脉）
- [ ] 为暮色森林加入 GT 特有的地下结构/地标（可选）
- [ ] GT 任务章节与农业主线的交叉奖励（用 numismatics 货币联动）
- [ ] 若加入 GTNN/GTMM 的专属机器，补充对应任务
- [ ] 旧存档矿脉补刷方案（暂不提供；如需要可做一次性回填工具）

---

## 5. 进度日志

| 时间 | 事件 |
|---|---|
| 2026-09-14 | 完成侦察：GTCEu 世界生成 API、两个维度定义、任务书规范 |
| 2026-09-14 | 新增 `worldGenLayers.js` / `oreVeins.js`，`node --check` 通过；提交 `6c708f3` |
| 2026-09-14 | 生成 GT 教程章节（43 任务）+ 中英本地化 138×2；全量静态校验通过；提交 `272c03b` |
