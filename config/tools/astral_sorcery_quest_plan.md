# Astral Sorcery 任务章规划与验收

基线日期：2026-09-27。工作区：Society Sunlit Valley；FTB Quests 2001.4.17。
源码：`H:/MinecraftMods/AstralSorcery-1.20.1`；指定工件：`build/libs/AstralSorcery-1.20.1.0.jar`。

## 写入前规划

读取 FTBQ_GUIDE.md、chapter_groups.snbt、thaumcraft.snbt、space.snbt，以及源码 PORTING_HANDOFF.md、ResearchProgression、RegistryResearch、语言文件中全部研究页面、相关配方及结构实现。旧交接文档的未实现清单不能代替当前源码和 JAR；例如当前 ActiveCrystalAttunementRecipe 已包含普通晶石到共鸣晶石的转换。

### 阶段与分区

|分区|位置|手册阶段|入口与内容|
|---|---|---|---|
|A 发现|左上|DISCOVERY / Discovery|宝典；神殿、星图；海蓝宝石、共振星杖、星辉合成台；大理石|
|B 探索|中上|BASIC_CRAFT / Exploration|星辉合成台；晶石、聚星缸、星能液、注星木；透镜、共振器、转继器、星辉祭坛；观测与照明|
|C 共鸣·光路|右上|ATTUNEMENT|星辉祭坛；连接器、透镜、星辉矿石、星尘；天文望远镜、共享知识、星门；充能星杖|
|D 共鸣·仪式|右下|ATTUNEMENT|共鸣祭坛；玩家共鸣和星能力；晶石共鸣、仪式基座；更替之星与宝石|
|E 星座|中下|CONSTELLATION|天辉祭坛；注入、共振宝石、五彩祭坛；天辉晶石和聚能；彩色透镜和映射；支线应用|
|F 五彩|左下|RADIANCE|五彩祭坛；聚焦合成、观星台、朦胧特质；圣杯与万象泉；披风、灿芒之星与结业|

BRILLIANCE / 辉煌存在于 ResearchProgression 枚举，但 RegistryResearch.init 只调用五组注册方法，没有 Brilliance 研究页面。不创建不存在的 altar_brilliance、singularity 或第五星辉祭坛目标。辉煌只在结业说明中注明边界。

### DAG 与几何布局（先算后写）

采用分区内分层 DAG 森林，非完整配方依赖图。入口物品由模组真实配方阶段约束，不把可选支线作为下一阶段总前置，也不假装 FTBQ 能检测研究状态。阶段根任务均说明上一阶段来源；共鸣分为光路和仪式两个面板。

每区原点横向相距 12、纵向相距 13.5。局部入口 `(0,4.5)`；分支最多四条，第一至第三层 x 为 3、6、9，分支 y 为 0、3、6、9；三分支面板 y 为 1.5、4.5、7.5。下排镜像朝左，以形成上排从左向右、下排从右向左的阅读方向。节点尺寸 0.9；列/行基准节距均为 3。

构图后先用拓扑最长路径分配局部层级，再在各层做确定性的向下/向上重心排序（同重心以业务 key 排序），保持短分支连续，随后计算坐标。节点中心包围盒预计 33 × 22.5；含节点外缘 33.9 × 23.4，宽高比约 1.45，落在 4:3～16:9 内。每区最长依赖仅为入口扇出边，最大约 5.41；普通分支边长 3。不同分区没有横贯全图的线。

校验包括节点方框无重叠、无关节点方框与依赖线段不相交、非共端点依赖线不交叉/重叠、共端点线不共线同向覆盖、最长边与包围盒比例。坐标必须全部通过才允许序列化。没有靠隐藏依赖线掩盖交叉。

### 分组

现有魔法组 `04716B2F19F75F08`（支线－神秘时代）。目前 thaumcraft.snbt 的 group 是 GT `4A46A5E1358A80A6`；历史曾挂魔法组。遵照“放合适现有魔法分组”，本章用仍存在的魔法组，不修改组文件或 TC4 章。该组为空，定义 max(empty)=-1，故首次 order_index=0；持久映射保存该值。Pollution 使用 GT order31，与本章无冲突。

## 内容依据与版本差异

路径以下以 `src/main/java/hellfirepvp/astralsorcery/common/` 为基准：

- `data/research/ResearchProgression.java`：六阶段枚举；`registry/RegistryResearch.java`：实际五组研究节点与文字页标识。
- JAR 内 `assets/astralsorcery/lang/{en_us,zh_cn}.json`：读中英文对照后改写中文教程，避免照搬旧译错误。中文名采用本 JAR：光照仪写作洞穴照明器 `illuminator`，星辉池写作聚星缸 `well`，共鸣法杖写作共振星杖 `wand`。
- `lib/ItemsAS.java`、`BlocksAS.java`、`FluidsAS.java`：显式注册名；BlocksAS 仅 registerBlockWithItem 计为物品，registerBlockOnly 不可作为目标。`RegistryRegistries` 将对应 DeferredRegister 挂入事件总线。生成器另外检查 JAR 注册类常量和物品模型，不把语言条目视为注册证明。
- `structure/PatternAltarAttunement.java`：二阶合成祭坛外缘 9×9；`PatternAltarConstellation`：三阶外缘 11×11；`PatternAltarTrait`：继承三阶后添加顶部砖结构；正文要求按手册分层图摆放，不用占地尺寸代替结构图。
- `PatternAttunementAltar`：共鸣祭坛中心炭黑大理石 15×15，外缘含角部至 ±9，整体占地 19×19。与二阶合成祭坛 `altar_attunement` 不同。
- `PatternSpectralRelay`：3×3 底座，中央炭黑大理石、四角雕纹大理石、四边大理石横梁；放入玻璃透镜。手册 SPEC_RELAY.4 给出 16 格供能距离。
- `TileAttunementAltar.searchActiveConstellation`：图形匹配后还检查当前月相下星座活跃；`AttuneCrystalRecipe` 要求夜晚；玩家仅明亮星座，朦胧星座用于特质。
- `PatternInfuser` 及 INFUSER.3：以结构中的星能液工作，无需天空，损耗后补液。JAR `recipes/infuser/aquamarine.json` 为海蓝宝石到共振宝石。
- ALTAR3 的旧中文暗示需要天辉水晶，实际 JAR 配方允许普通晶石；正文以配方为准。ALTAR4 实际需要天辉级晶石、共振宝石等。
- PED_ACCEL 的旧中文声称过载碎裂，英文已说明现代晶石不再因此碎裂；本章不复述旧机制。不承诺旧教程中的固定 Y 高度或恒定白天/夜晚倍率。
- CRAFTING_FOCUS_HINT、OBSERVATORY、ATT_TRAIT、ATT_CAPE、C_CHALICE、BORE_CORE：用于五彩阶段。没有把披风放到共鸣祭坛上；没有把有星图等同于已发现星座。

物品目标只检测背包物品，不证明结构形成、设备运行、玩家研究或晶石 NBT。需要实作的内容使用明确标注“手动确认”的 checkmark；祭坛升级会原地替换，需取回一次供物品目标检测，及时先完成前一级任务。奖励只有少量已入门原料，不赠送关键设备或共鸣晶石。

## ID 与安全生成

salt 为精确字符串 `astral_sorcery`。对象 ID 由 SHA256(salt + ':' + 业务 key) 前 64 位清最高位得到，零值或冲突立即失败；16 位大写 hex。业务 key 分 chapter、quest、task（物品名或明确 check key）、reward；不使用列表序号。`astral_sorcery_ids.json` 永久保存所有分配，包括将来退休 key。

每次扫描 quests 下所有 SNBT（章节、组、奖励表），提取所有定义而非只匹配正确长度的 ID。解析整棵对象树，检查重复 ID、类型、范围；旧库问题单列，新增 ID 与任何旧 ID 冲突均拒绝写入。依赖只引用本章任务，做 DAG 检验；所有多目标逐一比较。先在内存生成，独立 nbtlib 解析候选标准 SNBT，全部验证通过后才写章节及映射。已有输出 SHA 与映射不同就拒绝覆盖人工修改；持久映射缺失时拒绝接管已有章。

生成器使用 UTF-8 文件执行，避免 PowerShell 中文内联 python -c。默认发布；`--check` 只读；`--self-test` 仅内存负例。运行两次比较章节和映射字节，并记录最终静态结果。不开游戏、不安装 JAR、不提交。

## TC4 要素候选（仅建议，由主代理复核）

所有 ID 均带 `astralsorcery:` 前缀；生成器也验证此表引用的物品。要素只建议种类，不在本任务中写入 TC4 配置或分配数量。

|ID|建议原版 TC4 要素|
|---|---|
|astralsorcery:tome|cognitio, praecantatio|
|astralsorcery:aquamarine|vitreus, aqua, lux|
|astralsorcery:marble_raw|terra, ordo|
|astralsorcery:black_marble_raw|terra, tenebrae|
|astralsorcery:rock_crystal|vitreus, lux|
|astralsorcery:celestial_crystal|vitreus, lux, alienis|
|astralsorcery:attuned_rock_crystal|vitreus, ordo, praecantatio|
|astralsorcery:constellation_paper|cognitio, sensus, alienis|
|astralsorcery:wand|instrumentum, lux, praecantatio|
|astralsorcery:resonator|sensus, lux|
|astralsorcery:hand_telescope|sensus, vitreus|
|astralsorcery:illuminator|lux, machina|
|astralsorcery:well|aqua, lux, permutatio|
|astralsorcery:liquid_starlight_bucket|aqua, lux, metallum|
|astralsorcery:altar_discovery|fabrico, lux|
|astralsorcery:altar_attunement|fabrico, lux, praecantatio|
|astralsorcery:altar_constellation|fabrico, ordo, alienis|
|astralsorcery:altar_radiance|fabrico, auram, praecantatio|
|astralsorcery:attunement_altar|ordo, alienis, praecantatio|
|astralsorcery:spectral_relay|lux, motus|
|astralsorcery:lens|vitreus, lux, ordo|
|astralsorcery:linking_tool|instrumentum, vinculum|
|astralsorcery:starmetal_ingot|metallum, lux|
|astralsorcery:stardust|metallum, lux, perditio|
|astralsorcery:infuser|aqua, permutatio, praecantatio|
|astralsorcery:resonating_gem|vitreus, auram|
|astralsorcery:ritual_pedestal|praecantatio, ordo|
|astralsorcery:observatory|sensus, alienis|
|astralsorcery:chalice|vacuos, aqua|
|astralsorcery:mantle|tutamen, pannus, praecantatio|

## 验收结果（2026-09-27）

- 章节共 69 个任务、90 个目标、18 个多目标任务、21 个手动 checkmark、6 个入口奖励；每个任务至少有一个目标。共分六区：A 发现 10、B 探索 13、C 共鸣·光路 10、D 共鸣·仪式 10、E 星座 13、F 五彩 13。
- 生成 166 个本章对象 ID（章节 1 + 任务 69 + 目标 90 + 奖励 6），全部 16 位大写十六进制，范围 `1..7FFFFFFFFFFFFFFF`。映射按 SHA-256(`astral_sorcery:` + 业务 key) 稳定生成，映射文件保留输出 SHA。
- 生成 SNBT 通过自有递归 parser 与 `nbtlib` round-trip；任务依赖 DAG 无环、无悬空引用，目标/奖励/图标物品均通过源码注册、JAR 类常量和 JAR 模型核对。关键配方资源做了源码/JAR 字节语义对照。
- 布局中心包围盒 33×22.5，含 0.9 节点外缘为 33.9×23.4，宽高比 1.4487；最长依赖边 5.4083；63 条边，交叉 0、节点重叠 0、边穿节点 0。两次连续运行的章节 SHA 为 `170ef9432a1efd6fff2a654c76d84f3817580b9f392521acf9f3ea408f926282`，映射 SHA 为 `81e8d2c5d9869f13b11d8b2ce5b4100337f99dc9d9898ae096f62fe588ff15a4`。
- 全库对象扫描只收集章节根、任务、目标、奖励、链接、章节组和奖励表定义中的 `id`。物品 NBT、附魔、过滤器、配方和其它嵌套数据中的命名空间 `id`（如 `minecraft:potion`、`trofers:large_pillar`）不属于 FTBQ 对象，不会进入冲突或问题报告。当前 `existing_library_issues` 只保留真实对象定义的格式/重复问题；没有真实对象问题时报告为空。

静态通过不等于游戏验证；本次没有启动游戏或安装 JAR。主代理仍需在存档中检查任务 UI、物品/NBT 检测、祭坛原地升级后的拾取检测、共鸣研究同步、结构实际成型、配方加载及服务端奖励同步。另需由主代理复核本文 TC4 要素建议与当前 TC4 目标注册。
