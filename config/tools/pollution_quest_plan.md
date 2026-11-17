# Pollution 任务章设计与证据

基线：2026-09-27；实例 `Society Sunlit Valley`；源码 `H:/MinecraftMods/Pollution-Unofficial-1.20.1`；指定工件 `build/libs/pollution-1.20.1-1.0.0-1.20.1-port.0.1.0.jar`。

## 写入前的依赖与布局规划

使用现有 GT 组 `4A46A5E1358A80A6`，不改分组文件。六个模块按三列两行排列：

|位置|模块|目的|
|---|---|---|
|左上|A 能源与污染|Vis 发电/回充、魔力发电、咒波处理与污染区别|
|中上|B 源质供应|交换器、储罐、混合化合源质、两种熔炉及收集器|
|右上|C 魔导加工|组装与基础加工、化工、多方块支付与投产检查|
|左下|D 魔法电路|电路板与电路分开检测，ULV 至后期注魔路线|
|中下|E 植物魔法工业化|能源型/纯魔力仓、四类原生配方移植与发电燃料|
|右下|F 节点工程|生产、清洗、发电、节点高炉、中央塔、聚变|

每模块 7 个节点。局部坐标：入口 (2,0)，两分支 (0,2)/(4,2)，第二层 (0,4)/(4,4)，末层 (0,6)/(4,6)。边：0→1→3→5，0→2→4→6。最终将原点步长调整为 **(10,10)**，节点中心包围盒 **24×16（3:2）**，图标尺寸 0.9；含图标外缘 **24.9×16.9（约 1.473:1）**。相比原草案 20×16，最终比例处于用户要求的 4:3～16:9 内。各模块为可独立进入的教学树，章节依赖表示阅读/实作顺序，不伪称完整配方科技树；跨模块原料需求明确写入正文，机器电压标称不自动变成硬阶段锁。

预定几何验收：中心间距至少 2；所有边长不超过 √8；线段不得穿过无关节点，非共端点线段不得相交或重叠。没有跨区长线，无隐藏依赖线掩饰交叉。模块入口标题包含模块名，正文给出阶段与原料准备。

## 稳定 ID 与写入约束

所有对象按 `SHA256("pollution:ftbquests:v1:" + semantic_key)` 的前 64 位与 `0x7FFFFFFFFFFFFFFF` 掩码确定，零值报错。语义 key 包含章节、任务、目标类别/物品、奖励；不使用列表下标分配 ID。章节内用 SNBT 注释保存 key→ID，便于校验已发布归属。重跑首先验证旧文件的全部映射、内容及全库冲突，人工编辑导致内容变化时拒绝覆盖。

生成 `chapters/pollution.snbt` 与 `tools/pollution_ids.json`；脚本和本文为维护源文件。候选先在内存完整校验，不产生未经验证的章节文件；正式写入前重新读取全库并验证。全库既有异常单列报告，本章引入的冲突/悬空引用必须阻止写入。不得运行其他章生成器。首次选择该组最大 order_index+1，之后持久化排序值；如其他章占用此值则报错，不悄悄重排。

映射 schema 2 只持久化本章稳定验证结果、业务 ID、章节摘要及物品/源码/JAR 证据。全库任务/ID 数量和既有异常属于每次运行时诊断：仍在 `--check` 中全量计算、核对新旧异常，但不写入映射。新增其他章节不会触发“Evidence/map differs”。源码构建的 Pollution JAR 必须与实例 `mods` 中的同名工件 SHA256 一致。

## 证据取舍

已读实例 FTBQ_GUIDE.md、现有 GT/神秘章节及 chapter_groups.snbt；源码目录未发现 AGENTS.md。README、GAMEPLAY_TUTORIAL、HATCH_SEMANTICS、CIRCUIT_CHAIN 用于定位，最终依据注册代码、机器实现、配方注册和指定 JAR 类。

关键纠正：旧 GAMEPLAY_TUTORIAL 中节点高炉没有物品/流体仓、中央塔没有输入仓/星辉产出、节点聚变没有启动缓存/并行等描述已不符合当前源码；不能照抄。源质交换器结构的 aisle 方向与扫描中心不是同一概念，教程要求按结构预览放仓，搜索以控制器上方为中心。GT 源质熔炉当前只选择首个输出流体仓进行 fill，不能承诺六个仓自动分流全部方面。节点生产机 EV 持续扣款：2048 EU/t×600 tick=1,228,800 EU，144 mB/t×600=86,400 mB；旧文档 EU 总量计算错误。

指定 JAR 不含配方 JSON，配方由 Java 注册；不能把资源模型或语言条目单独当成注册证据。构建器逐个核对所用 Pollution 物品的注册源码、对应 JAR 类常量及模型，并记录机制证据与 JAR SHA256。未启动游戏，实际成型、GUI 视觉、自动检测/联机同步仍属于运行时验收范围。

## 最终内容与教学 DAG

|区|入口|左支线|右支线|
|---|---|---|---|
|A|intro|pollution → muffler → integration|vis → scrubber → fluxcell|
|B|essentia|exchange → tank → compound|smelter → collector → fuel|
|C|processing|assembler → mechanical → battery|chemical → payment → commission|
|D|circuits|ulv → lvmv → hvev|iv → luv → highcircuits|
|E|botania|managen → flowers → manaplate|daisy → altar → manaturbine|
|F|nodes|producer → washer → nodegen|nodeblast → tower → fusion|

每行入口同时连接两支线。固定语义节点分层 0/1/2/3；首层两个子节点按左右分支排序，后续节点与父节点重心对齐，这是树形 DAG 的零交叉分层布局，不需要以隐藏连线掩盖跨区交叉。图上阅读依赖不是严格工艺依赖：例如 IV 正文明确仍需 EV 电路，消声仓正文明确先建设源质与魔导组装。布局函数先算全部坐标，再做节点间距、非相邻节点到线段距离、线段相交/共线重叠、最大边长检查，最后序列化。

## 机制证据要点

所有路径相对源码 `src/main/java/meowmel/pollution/`；精确源码和对应编译类 SHA256，以及逐任务证据索引保存在 `pollution_ids.json`。

- `api/pollution/PollutionData.java:60–117`、`PollutionEngine.java:61–155,177–223`：按区块存储，无邻区扩散；每 200 tick 衰减、分级负面效果和预算限流的地形转换。当前实例配置：10/20/30/40 效果档、25/50 地形档、每 200 tick 减 0.2。
- `mixin/gregtech/WorkableMultiblockPollutionMixin.java:15–24`：GT 多方块 afterWorking 在各消声仓的位置记账；`ExplosionPollutionMixin.java` 是 GT 爆炸入口。不能把所有机器统称固定排放。
- `common/machine/part/FluxMufflerMachine.java:51–59` 返回零排放；`single/FluxScrubberMachine.java:48–77` 只清理 TC4R 咒波，成功清理才扣 EU/滤芯；配置文件旧注释不是当前实现。
- `common/item/VisCheckerItem.java:40–47` 报告玩家扭曲，不是工业污染读数。`single/FluxFuelCellMachine.java:60–84` 的 LV 咒波安全上限为 80。
- `loaders/recipes/CompoundAspectRecipes.java:42–125` 给出两路各 1000 mB→2000 mB 混合表；`InfusedProcessingRecipes.java:39–44` 给出粉→144 mB 提取路线。
- `common/machine/multiblock/magic/GtEssenceSmelterMachine.java:75–78,145–178` 只选首个输出仓，无满仓回滚保证；教程明确告知试机与产物损失边界。
- `loaders/recipes/AERecipes.java:148–181`：4 印刷件+红色合金板+144 mB HSSG→16 处理器，480 EU/t、160 tick。
- `loaders/recipes/MagicCircuitRecipes.java:189–305,323–344`：板和电路独立，ULV～LuV 魔导组装，ZPM+ 注魔；各目标以物品业务 key 稳定分配。
- `loaders/recipes/BotaniaNativeRecipes.java`：工业白雏菊/花药台 100 EU/t、200 tick；符文/灌注 mana 数值编码为 EU/t，不能误当一次性纯魔力支付。
- `common/machine/multiblock/node/NodeProducerMachine.java:80–113`：EV 每 tick 扣 2048 EU+144 mB；完整 600 tick 周期预算 1,228,800 EU+86,400 mB，首次受计时相位影响。
- `NodeFusionReactorMachine.java:103–165`：节点并行、≤4.2 工业污染检查、启动缓存均已实现。`CentralVisTowerMachine.java:87–174` 已有星魔素生产。
- 搜索当前 Pollution Java 源码未找到 Mekanism/Create 专属注册、配方或排污 hook；章内只说明已证实的联动边界，不编造两者机器。实例 KubeJS 中搜索到的 pollution 字样仅为钓鱼技能 stage，不是上述工业机制修改。

## 验收方法、复现命令和局限

在实例根目录运行：

```powershell
python config/ftbquests/tools/build_pollution_chapter.py --check
python config/ftbquests/tools/build_pollution_chapter.py
python config/ftbquests/tools/build_pollution_chapter.py --verify-repeat
```

生成器仅依赖 Python 标准库。检查涵盖：支持注释/字符串/可省逗号/数字后缀的递归 SNBT 解析；序列化回读；扫描所有 quests 下 SNBT（包括分组/奖励表）的 ID 格式、正有符号范围和唯一性；依赖目标类型、悬空引用和全库 DAG；多目标逐项对比；全部 item/icon/reward 的静态注册证据；配置数值与教程一致；布局几何。

用实例 FTBQ 2001.4.17 的 `ItemTask` 与 FTB Library 2001.2.12 的 `Tristate` 字节码核实 `consume_items`、`match_nbt`、`only_from_crafting` 布尔读取。物品目标明确不消耗、不要求合成事件、不匹配随机 NBT。阅读/试产确认不发奖励，30 个制作任务各奖励 2 cog，总计 60 cog，不奖励机器、电路或关键材料。

物品验证使用 Pollution 注册源码+指定 JAR 对应编译类名称常量+item 模型；跨模组仅用 `botania:endoflame` 与 `numismatics:cog`，核对实例 mods 中对应 JAR 的 item 模型和编译类名称常量。该方法是静态注册证据，不是启动 Forge 后的注册表快照；源码/类摘要可追溯但不能独自证明每条源码指令与工件完全一致。配方在运行时动态注册，SafeItems、研究与服务端最终数据可能影响实际可用性。

遵守不开游戏：尚未验证 FTBQ 实际 GUI、缩放时标题显示、多人同步、领取奖励、成型或运行产物；几何检查不等同于游戏内视觉验收。SNBT 使用本次自包含递归解析器，未调用 Forge/FTB 原生加载器。没有安装或替换模组 JAR，没有改分组文件，没有提交。

## 2026-09-27 静态验收结果

- 章节：42 任务、62 目标（50 物品目标+12 手动确认）、16 个多目标任务、30 项奖励。
- 稳定业务映射：135 个对象（1 章节+42 任务+62 目标+30 奖励）；均为 16 位大写十六进制，范围 1..7FFFFFFFFFFFFFFF。
- 分组：GT `4A46A5E1358A80A6`；首次扫描组内最大排序为 30，本章 **order_index=31**。请 Astral 作者避开 31。
- 初次全库合并：1909 任务、5277 个 FTB ID 定义。此计数仅为当时快照，后续新增章节不会改变本章映射的有效性；每次运行仍实时报告全库检查结果。
- 全部 54 个不同的 item/icon/reward ID 静态证据检查通过，明细在映射 JSON。
- 六个主题区，36 条边；中心边界 24×16，图标外缘 24.9×16.9；最小中心距 2，最长边 √8≈2.828427；节点重叠 0、依赖线穿节点 0、非共端点边交叉/重叠 0。
- `--verify-repeat` 连续两次真实生成后，章节和完整映射 JSON **逐字节相同**；`--check` 验证发布文件与候选一致。
- 章节 SHA256：`602895651cc058309123225eaa8b9874966e375766aba07a90711790935ccfb6`。
- 初次映射 SHA256：`54ef41e2a69fa167489dd037de42730ba368c88e4e7579cf30c241e5d9b38a09`；此历史值不用于当前检查。
- 本次输出范围：`chapters/pollution.snbt`、`tools/build_pollution_chapter.py`、`tools/pollution_quest_plan.md`、`tools/pollution_ids.json`。

## Astral 章节合并后的复验

- 指定源码构建和实例已安装 Pollution JAR 一致：SHA256 `73c3b978087f06692d4cf5718559e745bdf13bbf371abd761a5895280d1a013f`。Astral JAR 由其章节脚本检查，本章不修改它。
- `astral_sorcery.snbt` 在神秘时代组 `04716B2F19F75F08`；本章仍在 GT 组、排序 31，互不占用。
- Astral 章扩充期间全库计数发生变化；复验时实时扫描 1978 个任务、5443 个 ID，异常 0。全库计数不再出现在 `pollution_ids.json` 中。
- 章节 SHA256 保持 `602895651cc058309123225eaa8b9874966e375766aba07a90711790935ccfb6`；135 个持久业务 ID 和所有任务正文保持不变。
- 映射 schema 2 SHA256：`9590ed69f5bd5e8676f2e5f34f7481a2931f02f49a29dceb735f4702d347c113`。两次真实生成逐字节一致；两章的 `--check` 均通过。
