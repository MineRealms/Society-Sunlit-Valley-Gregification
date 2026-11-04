# GT 附属线：UV 主体、少量 UHV 收尾

> **2026-11-04 第四批更正**：第四批已修订电路与工业量产规格。第12节的19条配方、旧assembler ID和旧部署状态仅代表第三批快照；以当前THAUMIC_CIRCUITS与验收记录为准。 [PHASE4_ACCEPTANCE.md](PHASE4_ACCEPTANCE.md)。

> 设计基线：2026-11-03。后续已完成生物线第一批及GTNN启动兼容的隔离服验证，见 [BIO_LINE_IMPLEMENTATION.md](BIO_LINE_IMPLEMENTATION.md)；第二批（GCYR燃料机制、化工厂/HV脱水机/EV火箭发电机、GTMFO食品回收）已在隔离服验收，见 [GT_ADDON_PHASE2_EXECUTION.md](GT_ADDON_PHASE2_EXECUTION.md)；其余候选仍未实施，无生产部署。
> 配套：[生物线详细方案](BIO_LINE_PLAN.md)。旧报告 [RESEARCH_LINES.md](RESEARCH_LINES.md) 只作历史，不作为实施规格。
> 本轮按包主要求停止无限扩展调查；GTNN全部机器、GCYR全部目标、GTMFO全部药物未穷举。未核实部分明确列为待验，不用推测补齐。

## 1. 范围先定死

### 1.1 已由包主确定

- 主体工业进度做到 **UV**。
- **UHV只保留少量可选收尾产物**，不是要求建设一整代UHV机器、电源和配方。
- 不规划 **UEV、UIV、UXV、OpV、MAX** 的新增内容、任务或完整电路树。
- 当前模组里已有超高阶物品不等于必须删掉；本轮不移除GTNN、不修改注册ID、不抹除老玩家物品或机器。
- 已撤销的HV～EV魔法电路替代不恢复，不换名字重新加回。

### 1.2 本线的作用

给现有GT路线增加有用途的附属设备、食品/生物化工和有限航天目标，不再单纯拉长电压阶梯。

选择标准是：

1. 当前出货版本中有完整可达配方与机器执行路径；
2. 解决UV以内真实的加工/供料/探索需求；
3. 不隐含必须去UEV～MAX才能制造的部件；
4. 相比基础GT设备有合理优势，而非无代价替代；
5. 与现有任务、配方桥接不重复、不互相删除。

## 2. 证据与版本：能搜到不等于能制造

### 2.1 当前出货指纹

实例根：`G:/MinecraftGames/Sunlit Valley(BaopuEdition)/.minecraft/versions/Society Sunlit Valley`。

| 模组 | 文件 | SHA-256 前16位 |
|---|---|---|
| GTCEu | `gtceu-1.20.1-7.5.3.jar` | `d6560d8b695828a7` |
| GTNN | `gtnn-1.20.1-1.3.10.jar` | `ae22ebfc7cca8075` |
| GCYR | `gcyr-1.20.1-0.2.9.jar` | `86538eefc0b7bd2f` |
| GTMFO | `gtmfo-0.0.9.jar` | `854cadd387e225f3` |
| Connector | `Connector-1.0.0-beta.49+1.20.1.jar` | `e39acd37e162eb48` |

TC4R、TH、Pollution的对应版本与哈希见生物线文档。研究期间部分jar改名但哈希未变，不能仅用文件名判断内容升级。

### 2.2 对“存在”的五级判断

```text
注册物品/流体
  → 数据tag正确
  → 有生产配方
  → 该配方进入本包最终注册表
  → 玩家在目标阶段能够造机器、满足输入/研究并运行
```

后一级不能由前一级代替。静态JSON不存在也不证明没有配方，GT及附属会通过Java动态生成；需要沿注册回调核查，最终用运行时配方表确认。

### 2.3 本轮运行时边界

- Rosetta ping与只读配方查询返回空响应，未得到当前生产服实时注册表；这不等于已经证明服务器崩溃。
- 本轮没有启动客户端、没有重启服务器，也没有为研究修改生产配置。
- 主实例已有 `logs/latest.log` 包含GTNN 1.3.10加载、加入服务器、JEI注册完成的记录，但同一记录使用TH 1.0.0-alpha等旧组合。
- 因而“GTNN从未在包里运行”过于绝对；“已证明当前混合服务端全兼容”也不成立。日志只能证明当次组合走过部分启动/客户端路径，不能证明每台机器和全部配方可运行。

## 3. GTNN：先挑成熟设备，不扩建占位电路树

### 3.1 高阶电路的已确认与未确认

出货jar确实有以下tag：

| GT电路tag | GTNN成员 |
|---|---|
| `gtceu:circuits/uv` | `gtnn:gooware_assembly`、`gtnn:optical_processor` |
| `gtceu:circuits/uhv` | `gtnn:gooware_computer`、`gtnn:optical_assembly`、`gtnn:spintronic_processor` |

证据：jar `data/gtceu/tags/items/circuits/uv.json`、`uhv.json`；物品注册类 `dev.arbor.gtnn.data.item.EPMItems`。

本轮静态扫描未找到这些高阶EPM物品的完整生产链证据；jar没有静态recipes JSON，不能仅凭这一点排除动态生成或其他脚本来源。所以准确结论是：**有额外UV/UHV标签成员，生存可制造性未确认**。

处理：

- 不用它们来证明整包已存在第二条完整湿件替代线。
- 不为凑“生物胶质电路→宇宙电路”而补齐高阶族谱。
- 不因已有tag就让任务奖励发放这些物品；通用电路tag可能使一次奖励绕过其他机器材料要求。
- 即使后续发现可达的gooware/optical低档条目，也只评估UV以内用途，不自动接到UEV～MAX。

### 3.2 设备候选必须过筛

旧报告列出的化工厂、大型脱水机、中子活化器、元件/电路装配线、反应堆等，**目前是候选清单，不是这次承诺全部实现的名单**。

对每个拟采用设备填写：

| 字段 | 要求 |
|---|---|
| 注册ID / 出货版本 | 以当前jar与最终注册表确认 |
| 结构、控制器和部件 | 每种部件都能在UV以内取得，不能暗含更高电压前置 |
| 配方域 | 确认使用哪个RecipeType，是否兼容GT原配方、是否新增条件 |
| 输入输出能力 | 物品槽、流体种数、仓容量、方向、管道输入/输出均可用 |
| 电压与超频 | 明确电压、安培、并行、能耗和产率，不以机器名字推断 |
| 保留条件 | 普通/无菌洁净室、研究、维度、温度等不因多方块路径意外丢失 |
| 性价比 | 基础GT机器 vs 附属多方块，比较建造成本、吞吐、耗能、占地与维护 |
| 混合服务端 | 在本包实际Forge/Connector及服务端内核组合中执行、存档、重载 |

一次只选择少数有明确收益的设备，避免把“模组内容目录”误当成整合路线。

### 3.3 Mixin风险应具体化

出货 `gtnn.mixins.json`：`required: true`，**21条公共Mixin＋6条客户端Mixin**。jar里有29个mixin目录class文件，不等于29个必执行注入项。辅助类与配置声明要分开计数。

关键例子：

- `dev.arbor.gtnn.mixin.mc.MinecraftServerMixin#gtceu$injectDynamicData` 把GTNN动态数据包加入列表；需要测试启动、资源重载及失败恢复，不应笼统描述为“改了整个服务器tick”。
- `mc.RecipeManagerMixin`、`gt.GTRecipeTypeMixin`、`gt.GTRecipeBuilderMixin` 等涉及配方注册/构建；需要核查最终配方存在、条件保留和重复注册。
- 客户端日志出现过Shimmer目标缺失警告；警告本身不等于致命崩溃，也不能证明所有客户端注入都无问题。

数量不能直接换算“风险最高”或“肯定会崩”。真正判据是目标方法是否匹配出货GT版本、是否与其他转换冲突、发生失败时会不会阻断关键数据包与机器。

### 3.4 Botania/Create材料兼容

“材料在GT材料表里注册”只能说明存在命名与物料形式，不能证明它已用于某条必要配方。

本轮不新设Botania必须投入GTNN高阶电路的硬门槛。若某个UV以内设备已经消费这些材料，任务中解释现有连接即可；若没有，应作为单独alternate提案，不能为所谓“深度”强行把全部魔法系统串成必修课。

## 4. GCYR：包内已有桥接，优先修语义和验证闭环

### 4.1 11个维度，不是11颗行星

出货jar的 `data/gcyr/dimension/` 实际含11份定义：

- 地表/天体：`luna`、`mars`、`mercury`、`venus`、`proxima_centauri_b`；
- 轨道：`overworld_orbit`、`luna_orbit`、`mars_orbit`、`mercury_orbit`、`venus_orbit`；
- 其他：`black_hole_orbit`。

这个计数包含轨道，不能写成“11颗可登陆行星”。也不能用维度数量直接推出“启动时同时大量生成11个世界”。应分别测数据加载、首次抵达的区块生成、往返传送、已加载维度与强制区块；哪一项慢由实测决定。

### 4.2 已有整合不重复建设

当前主实例已有：

| 文件 | 代码中已有的作用 | 本轮需要复核的点 |
|---|---|---|
| `kubejs/server_scripts/gcyr/heavyAlloys.js` | 补GTNN重型合金T1～T4，使未装Ad Astra的环境有材料来源 | 最终原配方条件是否仍相同，避免重复来源；T4实际用Naquadah Alloy不是“钠钾合金” |
| `gcyr/hardenRockets.js` | 火箭发动机和燃料罐加重型板，基础/先进/精英分别用T1/T2/T3 | 保留已有玩家路线；前置材料是否真的可制造 |
| `gcyr/gtnnLinks.js` | GTNN引擎接受部分燃料，GTNN高级燃料用于GCYR火箭 | **EUt字段与引擎等级的解释**、燃料单位、收益和可逆转换 |
| `gcyr/mekLinks.js` | Mek相关燃料与装备标签桥 | 气体/流体注册ID与转换量是否匹配 |
| `gcyr/fixRocketFuels.js` | 汽油/柴油燃料补丁 | 最终配方是否存在、无重复/空流体、发动机匹配 |
| 现有GCYR任务与太空文档 | 太空引导已有章节 | 按当前生成器和ID登记表增量修改，不重新造平行章节 |

`heavyAlloys.js:51-58` 实际T4材料为 `#forge:dense_plates/naquadah_alloy` 和 `gcyr:trinaquadalloy`；旧注释中的“钠钾合金”不应复制到新任务。Naquadah与钠钾不是同一个材料。

`hardenRockets.js` 当前代码给基础、先进、精英部件的EU/t分别为480、7680、122880。数值可以确认，但还不能单凭这三个数认定整条火箭链已验收。

### 4.3 燃料字段不能凭注释改

`gtnnLinks.js` 将 `EUt(tier, 1)` 中的1/2/3注释为最低发动机等级；既有 `PROJECT_OVERVIEW.md:87` 已指出GCYR会经 `RecipeHelper.getRecipeEUtTier` 等路径解释数值。

实施前必须核对出货 `argent_matter.gcyr.data.recipe.RocketFuelRecipes`、`common.entity.RocketEntity` 的实际消费路径。不能因为参数看起来像tier，就把GT电压字段直接写1/2/3；也不能未经核验擅自改为某组电压。

这条属于**已有桥接的语义复核**，优先级高于扩建新星球任务。

### 4.4 本轮推荐玩法边界

- 保留已有火箭、重型合金和基础燃料路线，先实现可靠的起飞—抵达—返回—卸货闭环。
- 根据真实前置筛选UV以内可达目标，而不是要求玩家完成所有11维度。
- 不把“进入某维度”写成生物线通往NPU的必需条件；当前生物方案不需要太空解锁。
- 戴森球、太空电梯等名称只作为现有内容候选。只有完整制造和使用流程均在本轮范围内，才列入任务；超出UV及少量UHV收尾范围的直接不展开。
- 世界生成材料不能在没有新区域/新维度实测时保证“旧区块必定已经有”。

## 5. GTMFO：保留生活玩法，不把食品变成纯工业货币

### 5.1 已确认接线

- 出货存在食品化学相关类，如 `com.ironsword.gtmfo.common.data.recipe.chain.CheeseRecipes`、`VanillinRecipes`，以及 `ItalianBuffaloEntity`。
- 包内 `kubejs/startup_scripts/gtmfoTrades.js:23-32` 已把选定食品写入 `global.trades`；不是所有GTMFO物品自动可售。
- 营养逻辑与阈值已在 `kubejs/server_scripts/gtmfo/gtmfoNutrients.js` 和 `config/gtmfo.yaml` 管理，参考 [GTMFO_INTEGRATION.md](GTMFO_INTEGRATION.md)。
- 季节、食品品质、NPC赠礼与售卖也有既有脚本；新增生物工业路线须复用它们，而不是另设互相矛盾的食品分类。

旧报告列出的药物清单、精确效果数量、全部生物化工路线，本轮没有全部复验，**不把它们写成已经确定的任务目录**。

### 5.2 生物线可借用的角色

- 农业与畜牧提供低阶稳定原料；不要要求玩家为高阶电路反复手工做复杂料理。
- 食品副产/肉源可以成为培养耗材候选，但须算已有卖价与加工机会成本。
- 药物/工业中间体若要参与配方，先核注册和门槛，不因为名字像“培养营养物”就赋予替代能力。
- 不把所有药品、粉末、培养介质接入 `global.trades` 或接受仓价格表，避免循环加工→卖钱的新印币口。

对于能批量自动化的物品，分别评估：每单位成本、现实分钟产量、出售通道、品质/职业倍率和系统愿付预算。SunlitMarket的C/R只约束接入它的交易，**不代表已经限制出货箱等所有外部货币来源**。

### 5.3 药品与污染功能不要混称

某食物有治疗/抗性效果，不能推断它能清理TC warp或Pollution区块污染。若日后加专用药剂/净化耗材，必须明确作用对象、消耗、上限与冷却，并和生物线文档的四种污染/治疗概念保持一致。

## 6. 两条线的关系：可以分批做，不是“完全独立”

| 共享面 | 生物线使用 | 附属线使用 | 必须协调 |
|---|---|---|---|
| GT版本、配方管理器 | 培养基、干细胞、NPU | 多方块、燃料、材料 | 最终配方注册与兼容组合 |
| 流体和材料注册 | 培养基、Infused要素 | 化工和材料加工 | ID、单位、回收比率 |
| 普通/无菌洁净室 | 湿件两类条件 | 设备可能代执行GT配方 | 不让替代机器漏检查条件 |
| 研究/任务 | 神秘研究与工业研究 | 高阶设备引导 | 任务依赖不替代真实门槛 |
| 经济 | 动物产物、工业副产 | 食品/燃料产能 | 无限生产不应自动等于无限系统付款 |
| 旧存档 | 已有研究与库存 | 已有机器、维度、任务 | 独立ID、增量改动、回滚 |

可以采用两批实施，但共享面不止 `infused_*`。未确认可制造的gooware不作为两线的必要交点；当前共同锚点使用已经核实的培养基与GT湿件即可。

## 7. 少量 UHV 收尾的准入标准

优先候选：**GT湿件主机 `gtceu:wetware_processor_mainframe`**。

已核实：原流水线配方300000 EU/t、2000t；UV研究电压、96 CWU/t。它是UHV标签电路，但不强制先建设UHV电源。完整材料仍须逐项验证，不能只根据制造功率称“必定UV可达”。

新增任何收尾目标必须满足：

1. 主要制造、研究设备和电源可在UV体系内完成；
2. 没有隐藏UEV～MAX材料/研究；
3. 不把它设为所有后续生活、魔法、基础自动化内容的强制前置；
4. 不顺手延伸出UHV→UEV→MAX的新任务梯子；
5. 原版本已有的生产和存档不受破坏。

此“少量”是内容边界，不是本次文档擅自替包主确定一个具体任务数量。

## 8. 实施批次与验收清单

### A. 可达性基线（只读）

同一测试服会话导出：

- GTNN候选设备控制器/部件/实际RecipeType；
- 候选配方的完整输入、输出、电压、安培、时间、洁净/研究条件；
- 有tag却无已知产出配方的电路列表，单独标为未证实；
- GCYR最终燃料表、引擎匹配条件与当前重型合金配方；
- GTMFO候选食物/生物材料的最终配方与经济映射；
- 所有基线配方ID和当前mod哈希。

### B. 第一批改动原则

- 优先修已经存在的桥接错误和生物线阻断项，不先扩写几十页任务。
- 新增alternate使用独立 `kubejs:` ID，不删除GT原方；新增数据文件检查与原命名冲突。
- 需要覆盖同ID以修复错误的配方，单独记录原JSON、变化字段与回滚文件。
- 生物线与附属线各一个变更清单，避免一次合并时难以定位来源。
- 任务修改走生成器＋ID登记表，运行 `--check`、`--verify-repeat`；不手改一批随机ID。
- 新server脚本只用 `let`，明确优先级，避免同名全局类绑定。现有脚本包含 `const` 不是新脚本沿用的理由。

### C. 测试矩阵

| 测试 | 最低通过标准 |
|---|---|
| 冷启动 | 当前mod组合完成启动，未出现目标Mixin致命失败/关键配方类型缺失 |
| 资源/脚本重载 | 在实际服务端支持的重载方式下，不丢配方、不重复注册、失败明确报告 |
| 机器实际加工 | 正常输入能完成；缺关键条件不能完成；输出和副产量符合记录 |
| 高低电压边界 | 低于要求不运行；满足电压/安培时运行；多方块不意外绕过门槛 |
| 洁净室/研究 | 在不满足与满足环境下分别测，而非只看JEI提示 |
| GCYR往返 | 燃料正确匹配引擎、首次抵达/回程完成、卸货不丢失；实际测耗时和区块生成 |
| 兼容网络 | 如使用AE2/管道自动化，验证物品NBT、流体、仓容量与失败恢复 |
| 经济 | 自动化产能乘售卖倍率后没有新增无预算套利；区分玩家成交与系统收购 |
| 老存档 | 原机器、任务ID、研究、维度和库存正常；先用副本验证 |

“所有单测通过”“客户端开到主菜单”“GTNN Loaded”均不能替代上表的机器级测试。

## 9. 部署限制与回滚

- 本轮仅写文档，不同步到mirror、不发布更新器、不上传jar、不改服务器任务。
- 正式部署前列出客户端/服务端必须同时升级的mod和脚本；二进制按停服后的安全流程替换，不能覆盖运行中的jar。
- 先备份配置、脚本、任务ID登记和世界；不要用清空世界/删除旧物品解决注册兼容。
- 原配方保留时，撤掉新增alternate可回到旧玩法；若修改了产率/污染转换，另发迁移说明，不能宣传经济完全无影响。
- 当前文档没有授予自动部署或重启生产服的权限。

## 10. 最终推荐路线

```text
现有农业/食品/神秘生物
        ↓ 可选原料与培养辅助
GT IV无菌培养 → LuV干细胞 → ZPM制造条件下的NPU
        ↓
湿件电路与UV工业
        └─ 可选：少量UHV湿件主机收尾

并行支线：
  GTNN已可达设备：优化UV以内生产，不展开高阶占位电路树
  GCYR：复核现有合金/燃料桥，完成有限航天目标
  GTMFO：食物、营养、有限生物化工，保持生活玩法价值
```

图中的电压是工艺节点，不表示整条链只有这些机器；详见 [BIO_LINE_PLAN.md](BIO_LINE_PLAN.md) 的完整关键配方表。**下一步先完成守恒与注册基线，之后再挑少量联动开工。**

## 11. 定点证据索引

- GTNN出货：`gtnn.mixins.json`、`dev.arbor.gtnn.mixin.mc.MinecraftServerMixin#gtceu$injectDynamicData`、`GTRecipeTypeMixin`、`EPMItems`、`data/gtceu/tags/items/circuits/{uv,uhv}.json`。
- GCYR出货：`data/gcyr/dimension/*.json`、`argent_matter.gcyr.data.recipe.RocketFuelRecipes`、`common.entity.RocketEntity`；这里只将维度列表和类存在视为已确认，不据此确认全部玩法完成度。
- GTMFO出货：`CheeseRecipes`、`VanillinRecipes`、`ItalianBuffaloEntity`；完整药物线保留待验。
- 包脚本：`kubejs/server_scripts/gcyr/{heavyAlloys,hardenRockets,gtnnLinks,mekLinks,fixRocketFuels}.js`；`kubejs/startup_scripts/gtmfoTrades.js`；`kubejs/server_scripts/gtmfo/gtmfoNutrients.js`。
- 现有文档：[GT_INTEGRATION.md](GT_INTEGRATION.md)、[SPACE_INTEGRATION.md](SPACE_INTEGRATION.md)、[GTMFO_INTEGRATION.md](GTMFO_INTEGRATION.md)、[FTBQ_GUIDE.md](FTBQ_GUIDE.md)。旧文的时间戳、计数、中文材料翻译须对照当前代码使用。

## 12. 第三批落地（2026-11-04）

本节只记录已实现并在测试服验证的部分；第 1~11 节仍是范围与设计基线。

| 项目 | 结果 | 证据 |
|---|---|---|
| 神秘电路 MV~UV | 7 级，`pollution:assembler/thaumic_circuit/0..6`，200t×5 / 800t×2 | 运行时 recipe dump |
| 四块祭坛模板 | 模板 1 奥术 + 2/3/4 注魔（不稳定度 3/5/8） | `pollution:arcane/blood_circuit_template_1`、`pollution:infusion/blood_circuit_template_2..4` |
| 电路标签 | `gtceu:circuits/mv..uv` 各含对应 `blood_circuit.N` | `data/gtceu/tags/items/circuits/*.json` + 标签探针 |
| 工业注魔 | 19 条（16 JSON + 3 代码孪生），0 跳过 | 启动日志 `scan: 16 converted`、`registered 19` |
| 源质估值 | 4,118 → 2,883 flag，修复 2,244 条 | `SunlitIndustryCompat/.local/aspect-audit-r4.json` |
| 生物湿件任务章 | `bio_wetware.snbt` 23 任务 | `build_bio_wetware_chapter.py --check` |
| 神秘工业任务章 | `thaumic_industry.snbt` 20 任务 | `build_thaumic_industry_chapter.py --check` |

**遗留**：`.7`~`.12` 永久退役；UEV~MAX 不规划；主实例的 Pollution jar 仍是修复前版本
（模板 1 的修复只在测试服与 `dist/thaumic-phase3-validated/`）。

详细规则与维护入口：[THAUMIC_CIRCUITS.md](THAUMIC_CIRCUITS.md)、[MAGIC_GT_SCALING.md](MAGIC_GT_SCALING.md)。
