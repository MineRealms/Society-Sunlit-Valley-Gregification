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
| 任务章节 | `config/ftbquests/quests/chapters/*.snbt`（17 章） | 社区包整套任务书（563 任务 + 111 链接） |
| 奖励表 | `config/ftbquests/quests/reward_tables/*.snbt`（8 个） | bronze_age / hv / titanium 等 |
| 搬运脚本 | `config/ftbquests/tools/port_gregtech_quests.py` | 文本键化 + 缺失物品替换 + 分组/排序 |
| 翻译脚本 | `config/ftbquests/tools/translate_gregtech_quests.py` | 术语表 + 批量翻译 + 缓存/断点续传 |
| 翻译工作区 | `config/ftbquests/tools/gt_port/` | 英文条目 / 中文条目 / 翻译缓存 |
| 本地化 | `kubejs/assets/ftbquestlocalizer/lang/{zh_cn,en_us}.json` | 3707 条 × 2 语言 + 分组标题 |

对应提交：
- `6c708f3` feat: GT 矿脉注入暮色森林与骷髅洞穴（22 种主世界矿脉 × 2 维度）
- `d2e5f3a` feat: 批量搬运 GT 社区包任务书（17 章 563 任务 + 8 奖励表）并汉化

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

- 新增章节分组 **「格雷科技」**（ID `9F2C7A5E1B3D4C60`），包含 17 章 **563 个任务**：

| 顺序 | 章节 | 任务数 | 主题 |
|---:|---|---:|---|
| 0 | gtceu | 25 | 介绍 / 基础机制 |
| 1 | steam_age | 40 | 蒸汽时代 |
| 2 | lv__low_voltage | 75 | 低压 |
| 3 | mv__medium_voltage | 74 | 中压 |
| 4 | hv__high_voltage | 45 | 高压 |
| 5 | ev__extreme_voltage | 62 | 超高压 |
| 6 | iv__insane_voltage | 37 | 绝缘压 |
| 7 | luv__ludicrous_voltage | 37 | 剧差压 |
| 8 | zpm__zero_point_module | 27 | 零点压 |
| 9 | uv__ultimate_voltage | 20 | 极限压 |
| 10 | ore_generation | 39 | 矿脉生成 |
| 11 | ore_processing | 20 | 矿石处理 |
| 12 | renewability_and_you | 20 | 可再生资源 |
| 13 | multiblock_dilemma | 0 | 多方块图鉴（纯链接章） |
| 14 | heating_coils | 4 | 加热线圈 |
| 15 | progression | 17 | 电路进程 |
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
- 强校验：563 个任务块内的键 ID 全部与任务自身 ID 一致。

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

### 3.4 服务端下发汉化（资源包方案）

**结论**：直接把 lang 文件放进服务端 `kubejs/assets/` **无效**（客户端资源不会跨端同步）。
服务端要"下发"汉化，需用 **服务端资源包**：

```bash
# 生成资源包（把 kubejs 的 12 个语言文件打包到 assets/minecraft/lang/）
python config/ftbquests/tools/build_server_pack.py
# 产出: <启动器根目录>\server-pack\GT-Quests-Localization.zip（固定时间戳，SHA1 可复现）
```

服务端 `server.properties`：

```properties
resource-pack=<资源包直链 URL>
resource-pack-sha1=<脚本输出的 SHA1>
require-resource-pack=false          # true = 玩家拒绝下载则踢出
resource-pack-prompt={"text":"本服需要任务书汉化资源包（自动下载）","color":"gold"}
```

- 原理：`ftbquestlocalizer` 的任务文本最终由**原版/Forge 语言系统**解析
  （mod 自身的 `/ftblang export` 也是生成 `assets/minecraft/lang/` 的资源包），
  因此资源包里的 lang 会被加载，任务书的 `{ftbquests.chapter...}` 键即可解析。
- 资源包可上传到 GitHub Release（`MineRealms/UpdateRepo` 的 `latest` 标签）或任意 HTTP 直链。
- **注意**：每次改动任务文本/汉化后需重跑脚本，并把新 SHA1 填回 `server.properties`。
- 备选方案：更新器镜像里已包含这两个 lang 文件，发布后客户端启动时自动更新（无需资源包）。

---

## 4. LV 门槛（Create × GT）

**目标**：卡住 GT 的 LV 科技线 —— 先发展 Create（拿到电子管），才能进入 LV。

### 4.1 配方门槛（KubeJS）

- 文件：`kubejs/server_scripts/gt/lockLVBehindCreate.js`
- 核心：`event.replaceInput({ output: 'gtceu:basic_electronic_circuit' }, 'gtceu:vacuum_tube', 'create:electron_tube')`
- 依据（源码/文档/包内先例）：
  - GTCEu 7.5.x `CircuitRecipes.java`：工作台 shaped `electronic_circuit_lv` 的 `'V'` = 真空管
  - 7.5.3 注册名 `gtceu:basic_electronic_circuit`（jar 内 lang 核对）
  - KubeJS `replaceInput` 支持按 output 过滤（GTCEu 官方文档；包内 `removeRecipes.js:1086` 已有用法）
- 说明：电路组装机版使用标签 `#gtceu:circuits/ulv`，但该机器本身在 LV 门槛之后才能建造，故本次不处理。

### 4.2 任务门槛（FTB Quests）

- Create 章（`ivi__mechanical_farming`）新增任务 **「LV 时代」**（ID `1EA76C7815090684`）：
  - 位置 (7.5, 2.5)，依赖电子管任务 `1A1129507F643085`
  - 任务物品：`gtceu:basic_electronic_circuit` ×1（用电子管做出第一块 LV 电路）
  - 文本键：`ftbquests.chapter.ivi__mechanical_farming.quest1EA76C7815090684.*`（zh/en 已写入）
- GT LV 章（`lv__low_voltage`）5 个入口任务追加依赖 `1EA76C7815090684`：
  - `288CE4AA4C5AA8BF`、`2F7617C0C4B330DE`、`38993B4697B0E16C`、`6E186F9C57155BFA`、`32EA7E81885C8E87`
- 效果：完成 Create「LV 时代」后才解锁 GT 的 LV 任务线；与配方门槛形成双重锁。

### 4.3 验证

- `node --check` 通过；SNBT 解析通过；全局 1738 个任务 ID 无冲突；无断链依赖；新任务 lang 键 zh/en 齐全。

---

## 5. Create × GT 轻量联动（R2）

**目标**：让 Create 机器可以处理 GT 前期材料（ULV~LV），两边穿插发展。

**文件**：`kubejs/server_scripts/gt/createBridges.js`（只加配方，不动物品/标签）

| # | 联动 | 配方 | GT 依据 |
|---|---|---|---|
| 1 | Create 压合 → GT 板材 | 1 锭 → 1 板（铁/铜/金/锡/钢/青铜/黄铜/铅/银/锌/镍/琥珀金/熟铁） | 弯曲机 1→1（`MaterialRecipeHandler:390`） |
| 2 | Create 压合 → GT 覆膜电路板 | 1 木板 + 2 粘性树脂 → 1 `gtceu:resin_circuit_board` | 无序合成 1x（`CircuitRecipes:775-778`） |
| 3 | Create 粉碎轮 → GT 碎矿 | 原矿（tag）→ 2 碎矿（锡/铁/铜/金/煤/镍/铅/银/红石） | 研磨机 ×2（`OreRecipeHandler:194-201`） |
| 4 | Create 混合 → GT 合金粉 | 红合金 1铜+4红石→1；黄铜 3铜+1锌→4；青铜 3铜+1锡→4；琥珀金 1金+1银→2；殷钢 2铁+1镍→3 | 混合器 ULV（`MixerRecipes:143-206,223-228`） |
| 5 | Society 橡胶 → GT 橡胶 | Create 混合(加热)：1 `society:rubber` + 1 硫粉 → 1 `gtceu:rubber_ingot` | 合金炉 1硫+3生橡胶→1（`MachineRecipeLoader:423`） |

**设计说明**：
- 板材用 `create:compacting`（压床+盆）而非 `create:pressing`：Create 自带的铁/铜/金/黄铜压片占用同名标签输入，避免配方冲突。
- 原矿用 `#forge:raw_materials/*` 标签，兼容 oreganized 等模组的铅/银原矿；锌无 GT 碎矿（JEI 核对）故不含。
- 合金配方使用 `#forge:dusts/*` 标签（GT `TagUtil` 统一 `forge:` 命名空间）。

### 5.1 验证

- `node --check` 通过；脚本内 40 个物品 ID 全部命中 GT JEI 导出 / Create jar / 包内引用；10 个标签全为 `forge:` 命名空间。

---

## 6. GregMek（GT × Mekanism 矿石联动）与 MEK 科技锁

### 6.1 GregMek 是什么

GTCEu × Mekanism 的矿石处理联动 addon（原为 “GregTech Odyssey” 整合包开发），运行于
1.20.1 / Forge 47.4 + GTCEu 7.5.3 + Mekanism 10.4.16：

- **新增材料形态**（GT TagPrefix）：污浊粉 `dirtyDust`、碎块 `clump`、碎片 `shard`、晶体 `crystal`；
- **新增流体**：纯净浆液 `pure_slurry`、污浊浆液 `dirty_slurry`（对所有带 ORE 属性的材料自动挂载）；
- **GT 侧处理链**：洗矿机（矿石/粗矿 + 硫酸 → 污浊浆液）→ 化学洗矿（污浊浆液 + 水 → 纯净浆液）→ 高压釜（纯净浆液 → 晶体）；
- **Mekanism 侧配方**：压射（晶体/矿石/粗矿 + 盐酸 → 碎片）、提纯（碎片/矿石/粗矿 + 氧气 → 碎块）、粉碎（碎块 → 污浊粉）、富集（矿石/污浊粉 → 粉尘）；
- **GT 机器版同链配方**（化学反应釜/研磨机/离心机），不造 MEK 机器也能走；
- 有配置：开关两条链、产出倍率、副产概率倍率。

### 6.2 本轮对 GregMek 的改动（用户完成）

1. **构建**：`fg.deobf` + `flatDir` 引入三个 jar（gtceu 7.5.3 / Mekanism 10.4.16.80 / JEI），
   补 ldlib 1.0.52.a，从 gtceu jar 抽出 JiJ 的 Registrate、configuration 到 `libs/`，编译通过。
2. **现代化重构**：`@Mod` 与 `@GTAddon` 拆类（避免 AddonFinder 反射重复 new）；配置改构造器注入
   `FMLJavaModLoadingContext`；浆液流体改 `PostMaterialEvent` 挂载（7.5.3 不再调 `registerMaterials()`，
   原为死代码）；配方统一走 `IGTAddon#addRecipes(Consumer)` 数据生成；加 JEI/EMI 配方分类；
   配置倍率生效；时长按材料质量缩放；生成前检查 `shouldGenerateRecipesFor`；清理 2969 个过期 datagen JSON
   （GTCEu 7.x 配方运行时动态生成，旧文件会 ID 冲突）。
3. **修复自造崩溃**：`FluidBuilder.name("pure_slurry")` 覆盖按材料生成的流体名 → ~200 流体重名 →
   建世界 `intrusive holders were not registered` 崩溃；改回裸 `FluidBuilder()` 后修复并安装
   （旧 jar 备份为 `.broken-fluidnames`）。

### 6.3 现状

- `mods/gregmek-1.0-SNAPSHOT.jar`（30 KB，2026-09-15 22:10）已安装；
- Mekanism 全家桶 10.4.16.80（本体 + Additions + Generators + Tools）在包内；
- 运行时验证待进存档（矿石处理链、JEI 分类、浆液流体显示）。

### 6.4 ★ MEK 科技锁（用户明确要求）—— 已实施

**目标**：MEK 科技被 GT + Create 双重锁：

1. MEK 基础机器需 GT **LV「基础电路组装机」**（`gtceu:circuit_assembler`）阶段后才能制作（等价 LV 电路门槛）；
2. 后续 MEK 机器合成加入 **`create:precision_mechanism`**（Create 精密构件）。

**配方调研结果**（`mods/Mekanism-1.20.1-10.4.16.80.jar` → `data/mekanism/recipes/`，共 4223 个配方）：

| 机器 | 电路需求 | 关键材料 |
|---|---|---|
| 冶金灌注机 `metallurgic_infuser`（入门，**无电路**） | 无 | 熔炉×2 + 铁锭×4 + 红石×4 + 锇锭×1 |
| 钢外壳 `steel_casing`（**所有机器都要**） | 无 | 钢锭×4 + 硅玻璃×4 + 锇锭×1（居中） |
| 富集仓 `enrichment_chamber` | `#forge:circuits/basic`×2 | 基础合金×4 + 铁锭×2 + 钢外壳 |
| 粉碎机 `crusher` | basic×2 | 红石×4 + 熔岩桶×2 + 钢外壳 |
| 电炉 `energized_smelter` | basic×2 | 基础合金×4 + 硅玻璃×2 + 钢外壳 |
| 精密锯木厂 `precision_sawmill` | basic×2 | 灌注合金×2 + 铁锭×4 + 钢外壳 |
| 锇压缩机 `osmium_compressor` | advanced×2 | 灌注合金×4 + 钢外壳 |

> `forge:circuits/basic` 标签 = `mekanism:basic_control_circuit`（MEK 内部链：锇锭+红石→基础电路；灌注合金×4+基础电路→高级电路）。

**锁设计（推荐方案，共 6 处改动，全用 `e.replaceInput`，无需 remove/重加）**：

1. `steel_casing`：居中锇锭 → `gtceu:basic_electronic_circuit`（1 个）→ **所有 MEK 机器（含附属）一并被 LV 电路门住**；
2. `metallurgic_infuser`：熔炉 → `gtceu:basic_electronic_circuit`（×2）→ 入门机器也要 LV 电路；
3. 4 台基础机器（富集仓/粉碎机/电炉/精密锯木厂）：`#forge:circuits/basic` → `create:precision_mechanism`（各 ×2）→ 用上 Create 精密构件。

**实施（已完成）**：

- 脚本：`kubejs/server_scripts/mek/lockMekBehindGT.js`（8 处 `replaceInput`，B 方案 = `gtceu:microchip_processor`）；
- 任务章：`config/ftbquests/quests/chapters/mekanism.snbt`（11 任务，挂在「格雷科技」分组 `4A46A5E1358A80A6`，order 17）；
  生成器 `config/ftbquests/tools/build_mek_chapter.py`；任务文本内联中文（无 lang 依赖）；
- **入门前置**：LV 章「铝锭」任务 `7567E885B7166603`（LV→MV 收尾标志）——“LV 玩得差不多才能进 MEK”；
- 校验：`node --check` ✅；SNBT 括号平衡 ✅；34 个新 ID 全局唯一 ✅；11 条依赖全部存在 ✅；文本内联中文 ✅。

---

## 7. 验证记录

| 项目 | 结果 |
|---|---|
| `node --check`（两个 GT 脚本） | ✅ |
| GTMaterials 材料字段（70 个） | ✅ 全部存在 |
| 矿脉/章节 ID 唯一性 | ✅ 1668 个搬运 ID 与既有 3031 个零冲突 |
| 任务块键 ID 一致性（563 块） | ✅ 0 不匹配 |
| 物品 ID 校验（替代后） | ✅ 无缺失命名空间引用 |
| 奖励表 ID 冲突 | ✅ 无 |
| SNBT 结构（括号/引号平衡） | ✅ 17 章全部通过 |
| 本地化键完整性 | ✅ 3707 键 × 2 语言，0 缺失 |
| 颜色码完整性 | 3374/3412 完全一致（38 条异常已修复，21 条缺个别颜色码） |
| 占位符乱码残留 | ✅ 0 |
| LV 门槛依赖（LV 章 5 入口） | ✅ 5/5 已追加 |
| LV 门槛任务/文本（Create 章） | ✅ 新增「LV 时代」+ zh/en 键齐全 |
| Create 联动脚本（`createBridges.js`） | ✅ `node --check` + 40 物品 ID / 10 标签全部核对通过 |
| MEK 锁脚本（`lockMekBehindGT.js`） | ✅ `node --check`；8 处替换按 Mekanism jar 配方逐条核对 |
| MEK 任务章（`mekanism.snbt`） | ✅ SNBT 括号平衡；34 ID 全局唯一；11 依赖完整；文本内联中文 |

> 运行时验证（需进存档）：打开任务书检查「格雷科技」分组排版与文本；
> 旧存档请前往未探索区域观察新矿脉。建议 `/ftbquests editing_mode` 预览。

---

## 8. 后续可选项（TODO）

- [ ] **MEK 科技锁（GT LV 电路组装机 + Create 精密构件）—— 见第 6.4 节（用户明确要求）**
- [ ] 人工润色机器翻译文本（重点：长描述、幽默文案、专有名词）
- [ ] 按本包进度调整部分任务奖励（numismatics 货币联动）
- [ ] 为骷髅洞穴各群系差异化矿脉权重
- [ ] 将 `gt_port` 工作文件纳入更新流程（版本升级时增量翻译）
- [ ] 若补充安装 eAE/MAE2/AE2WTLib，可把替代映射还原为原物品
- [ ] TC4（神秘时代）× GT 联动分析（见 `TC4_INTEGRATION.md`）

---

## 9. 数据修复与 GTCA 兼容（2026-09-15）

> 来源：latest.log（22:26 会话）分析结论；每项均先核对事实再修改，证据随附。

### 9.1 标签数据修复（LMF 报错项，逐条核对）

| 文件 | 问题（核对证据） | 修复 |
|---|---|---|
| `kubejs/data/society/tags/blocks/treasure_spot_spawns.json` | `minecraft:pitcher_pod` 是物品；方块为 `pitcher_crop`（gtceu tall_plants / SereneSeasons summer_crops / WorldEdit 注册表均引用） | 改为 `minecraft:pitcher_crop` |
| `kubejs/data/longwings/tags/blocks/pollination_banned_crops.json` | `atmospheric:aloe_kernels` 仅物品模型（方块 `aloe_vera` 同文件已列）；`minecraft:torchflower` 是物品 | 删除 kernels 行；`torchflower` → `torchflower_crop` |
| `kubejs/data/quality_food/tags/blocks/quality_blocks.json` | 方块标签混入物品/过期 ID：vinery 葡萄/樱桃/苹果、`create:wheat_flour(_bag)`、`farmersdelight:stacked_melons/pumpkins`、`farm_and_charm:lettuce/tomato/*_from_bag/*_from_ball`、`supplementaries:sugar_cube_uncrafting` | 葡萄 → `vinery:white_grape_bush`/`red_grape_bush`（方块已验证）；删除其余无效项；顺带去重 |
| `kubejs/data/zhopo/tags/worldgen/biome/has_structure/*.json` | `society:skull_cavern` 是**维度** ID（见 `dimension/skull_cavern.json`），不是生物群系；仅 stone/deepslate 两个文件残留无效值（其余 10 个已是有效群系） | stone → `skull_caves`；deepslate → `blackstone_caves + skull_caves`（最小修正，保留作者原有分布意图） |

> 备注：`society:sellable` / `society:large_eggs` 两条 LMF 报错源于 `_diag_tags.js` 在物品标签事件抛异常（该脚本已删除，提交 `f7a0128`），需下次启动验证。

### 9.2 GTCA 兼容（机壳配方）

- **现象**：日志 `Input item 0 of recipe gtceu:reactive_gas_cont_cas is empty`（`inert_filtration_casing` 同）。
- **根因（GTCA 源码 7.5.x + GTCEu TagPrefix 生成条件核对）**：
  - gtca `hastelloy_n` 无 GENERATE_FRAME / GENERATE_ROTOR；`hastealloy_276` 无 GENERATE_GEAR；GT 的 `hastelloy_x` 无 GENERATE_ROTOR → 对应零件物品不存在。
  - GT 的 `inputItems(空栈)` 会记录 ERROR 并**跳过该输入**，配方仍以残缺形态注册（潜在异常廉价合成）。
- **处理**：`kubejs/server_scripts/gt/gtcaCasingCompat.js`
  - 按产出物移除两个残缺配方；
  - 补两条兼容配方（数值镜像原配方：EUt = 7680 / IV、duration 680、circuit 6、产出 ×2）：
    - `reactive_gas_contantment_casing`：`6x double_hastelloy_c_276_plate` + `hastelloy_c_276_frame` + `tungsten_steel_rotor`
    - `inert_filtration_casing`：`hastelloy_c_276_frame` + `6x hastelloy_x_plate` + `2x tungsten_steel_rotor` + `2x tungsten_steel_gear` + `iv_electric_pump` + 576mB PTFE
  - 物品 ID 全部逐条核对自 JEI 导出；`node --check` 通过。

---

## 10. 进度日志

| 时间 | 事件 |
|---|---|
| 2026-09-14 | 侦察 GTCEu 世界生成 API、两维度定义、任务书规范 |
| 2026-09-14 | 新增 `worldGenLayers.js` / `oreVeins.js`；提交 `6c708f3` |
| 2026-09-14 | 手写小章节尝试（已 `308697b` revert，改为整包搬运） |
| 2026-09-14 | 完成 17 章搬运脚本 + 18 处物品替换 + 分组/排序；563 任务块强校验通过 |
| 2026-09-14 | 翻译流水线（术语表 5151 条 + 批量翻译 83 秒）；3707 键写入 zh/en；提交 `d2e5f3a` |
| 2026-09-15 | LV 门槛（Create × GT）：`lockLVBehindCreate.js` + Create 章「LV 时代」任务 + GT LV 章 5 入口前置；静态校验全通过；提交 `9fb5899` |
| 2026-09-15 | Create × GT 轻量联动 R2：`createBridges.js`（板材/覆膜板/碎矿/合金/橡胶 5 组）；ID 与标签核对通过 |
| 2026-09-15 | 记录 GregMek（GT × Mekanism 联动 addon）：修复流体重名崩溃后安装 `gregmek-1.0-SNAPSHOT.jar`；新增第 6 节 |
| 2026-09-15 | 新增 MEK 科技锁 TODO（GT LV 电路组装机 + Create 精密构件）；建立 `STATUS.md` 状态快照 |
| 2026-09-15 | **MEK 科技锁实施完成**（B 方案 = LV 微处理器 + Create 精密构件 8 处 `replaceInput`）+ MEK 任务章（11 任务，前置 = LV 章铝锭任务） |
| 2026-09-15 | 日志分析后的数据修复（4 类标签文件）+ GTCA 机壳兼容配方；删除诊断脚本 `_diag_tags.js`（f7a0128） |
