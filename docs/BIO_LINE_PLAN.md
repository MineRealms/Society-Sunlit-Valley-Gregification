# 生物线：TC4R / ThaumicHorizons × Pollution × GT 湿件

> 设计基线：2026-11-03。**第一批已实现并在隔离emoney服验证**，当前完成项与限制见 [BIO_LINE_IMPLEMENTATION.md](BIO_LINE_IMPLEMENTATION.md)。下文保留实施前的设计和静态证据，不代表所有候选已做完。
> 本文取代 [RESEARCH_LINES.md](RESEARCH_LINES.md) 生物部分的旧结论；旧文保留为历史记录。
> 配套：[GT 附属线与阶段边界](GT_ADDON_LINE_PLAN.md)。原调研阶段无运行时结果；后续隔离服6组探针及38项配方断言见实施记录，不能把生产服与隔离服混为一谈。

## 1. 已定范围与目标

### 1.1 包主已经确定的边界

- 工业主线做到 **UV**；允许少量 **UHV 产物作为可选收尾**，不建设完整 UHV 时代。
- **不规划 UEV～MAX** 的新电路树、机器梯级、任务或材料链。
- 不恢复已经撤销的 HV～EV 魔法电路替代方案。另开一条低投入“魔法脑直接换高阶通用电路”的路，同样不符合这个边界。
- 现有服务器有玩家进度：默认保留原 GT 配方、已有研究、机器、物品 ID 和任务 ID。
- 本次只形成文档；不能把下面的候选写成已经安装的功能。

### 1.2 推荐定位

**TH 提供生物培养与神秘素材，Pollution 负责要素流体和血肉加工，GT 负责无菌培养与精密电子制造。**

目标不是把所有湿件改成“必须养一只生物才能做”，而是让愿意经营神秘生物支线的玩家得到可量化的工业收益。纯 GT 玩家继续使用原路线；跨线玩家付出研究、设备与培养成本，换取可验证的效率或原料来源优势。

### 1.3 明确不承诺

- 不把 Curative Vat 宣传成现成的 Pollution 污染净化设备。
- 不把 somatic_brain 宣传成会生产经验、知识、神经元或干细胞的机器。
- 不因 `blood_circuit` 名字里有电压就为它补上 GT 通用电路标签。
- 不把所有 `infused_*` 一概当成可守恒往返的 TC 源质。
- 不以“JEI 能搜到”代替“生存流程可制造”；也不以“有配方 builder”代替“最终配方已加载并能在机器运行”。

## 2. 证据等级与版本基线

### 2.1 证据如何使用

| 标记 | 含义 | 本文使用方式 |
|---|---|---|
| 出货静态 | 当前实例 jar 的数据、类或字节码可确认 | 可以确认存在的 ID、声明的投入、注册链和明显代码问题 |
| 匹配源码 | 源码与出货版本对应，关键位置已经交叉核对 | 用于解释完整行为、给出可定位行号 |
| 现有包脚本 | 主实例正在放置的 KubeJS/配置文本 | 只能确认脚本写了什么，仍需核对最终加载结果 |
| 设计建议 | 本轮推荐但尚未实现 | 不出现在“已完成”或“已实测”清单里 |
| 运行时待验 | 最终配方、标签、机器实际执行或混合服务端行为 | 必须留待集中测试，不能从静态结果推断通过 |

### 2.2 当前主实例

根目录：`G:/MinecraftGames/Sunlit Valley(BaopuEdition)/.minecraft/versions/Society Sunlit Valley`。

| 模组 | 核验版本 / 当前文件 | SHA-256 前16位 |
|---|---|---|
| GTCEu Modern | `gtceu-1.20.1-7.5.3.jar` | `d6560d8b695828a7` |
| Thaumcraft 4 Reborn | `thaumcraft-forge-4.2.3.5-1.20.1-port.0.1.0-20759.jar` | `9ecced9a4681c76f` |
| ThaumicHorizons（modid `isorropia`） | `(59+)神秘视界 ThaumicHorizons-1.20.1-1.0.5-alpha.jar` | `2b9a6e5656837872` |
| Pollution（modid `pollution`） | `(59+)污染 Pollution-1.20.1-1.0.0-port.0.1.0.jar` | `38701380633ceb20` |
| Forbidden Magic | `forbidden-magic-forge-0.574-1.20.1-port.0.1.0-20759.jar` | `742b5c6449e6e9db` |

研究期间 TH/Pollution 文件被改名加上“59+”前缀，内容哈希未变。`.bak-*` 不作为当前版本依据。旧 20748、TH 1.0.0 的日志和报告不能证明当前 20759 / TH 1.0.5 的完整行为。

源码索引：

- **GT7**：`H:/MinecraftMods/GregTech-Modern-7.5.2/src/main/java/com/gregtechceu/gtceu/`。本次使用的培养基和湿件关键配方已与 `GregTech-Modern` 的 Git 标签 `v7.5.3-1.20.1` 及出货字节码交叉核验；不把目录名7.5.2自动当成出货7.5.3。
- **P**：`H:/MinecraftMods/Pollution-Unofficial-1.20.1/src/main/java/meowmel/pollution/`。
- **TH**：`H:/MinecraftMods/Isorropia-1.20.1-wt/multiversion/src/main/java/fr/wind_blade/isorropia/`。
- **TC59**：`H:/MinecraftMods/tc4r-59-set/1.20.1-forge-20759/dev/tc/thaumcraft-forge-4.2.3.5-1.20.1-port.0.1.0-20759-sources.jar`，并抽查主实例出货 jar。

`H:/MinecraftMods/Pollution` 为1.12.2旧工程；`ThaumicHorizons` 旧源码用于机制参考，不用来断言本次出货已经移植。不要直接拿 GTCEu 当前开发分支代替7.5.3。

## 3. GT 湿件：必须保留的真实工业门槛

### 3.1 单位、名字与等级

本文流体统一按配方 API 的 **mB 数值**记录；例如4000表示4000 mB，避免和不同界面的“L”显示混用。时间单位为 tick，正常20 TPS时20 tick＝1秒。EU/t是配方功率，不等于电路标签等级。

| 用途 | 正确注册 ID |
|---|---|
| 原始生长培养基 | `gtceu:raw_growth_medium` |
| 无菌生长培养基 | **`gtceu:sterilized_growth_medium`** |
| 培养皿 | `gtceu:petri_dish` |
| 干细胞 | `gtceu:stem_cells` |
| 湿件基板，Java常量 `WETWARE_BOARD` | `gtceu:wetware_circuit_board` |
| 印刷湿件板，Java常量 `WETWARE_CIRCUIT_BOARD` | `gtceu:wetware_printed_circuit_board` |
| 神经处理单元 NPU | `gtceu:neuro_processing_unit` |

**`sterile_growth_medium` 是配方名，不是该流体的注册 ID。**脚本不能把配方ID当流体ID使用。

### 3.2 已核实关键配方

| 产物 / 机器 | 投入 → 产出 | EU/t；时间；条件 |
|---|---|---|
| 培养皿 / 流体固化机 | 不消耗圆柱模具；PTFE 36 → 培养皿1 | 480；160t；无洁净条件 |
| 培养皿替代 / 流体固化机 | 同一模具；PBI 18 → 培养皿2 | 480；40t；无洁净条件 |
| 原始培养基 / 搅拌机 | 肉粉4＋盐粉4＋钙粉4＋琼脂粉4＋诱变剂4000 → 原始培养基4000 | 7680（IV配方功率）；1200t；无菌洁净室 |
| 无菌培养基 / 流体加热机 | 电路模式1；原始培养基100 → 无菌培养基100 | 7680；20t；无菌洁净室 |
| 干细胞 / 化学反应釜 | Osmiridium粉1＋细菌500＋无菌培养基500 → 干细胞32＋细菌浆液500 | **30720（LuV）；300t；无菌洁净室** |
| 湿件基板 / 电路组装机 | 多层纤维板16＋培养皿1＋**LuV泵1＋IV传感器1＋IV电路1**＋铌钛箔16＋无菌培养基4000 → 基板16 | 30720；1200t；**普通洁净室** |
| 印刷湿件板 / 化学反应釜 | 湿件基板1＋铌钛箔32＋过硫酸钠10000，或氯化铁5000 → 印刷板1 | 480；1800t；普通洁净室 |
| NPU / 电路组装机 | 印刷湿件板1＋干细胞16＋**PBI小流体管8＋Electrum板8＋硅橡胶箔16＋HSS-E螺栓8**＋无菌培养基250 → NPU1 | **80000（ZPM供电范围）；600t；普通洁净室** |

证据：GT7 `data/recipe/serialized/chemistry/GrowthMediumRecipes.java:125-151`；`data/recipe/misc/CircuitRecipes.java:960-997,1479-1489`；ID见 `common/data/GTItems.java:1599,1622,2217` 和 `common/data/materials/UnknownCompositionMaterials.java:299-303`。

### 3.3 上游培养链不应被一句话省略

大体流程为植物球→生物糠→细菌→细菌浆液→富集浆液→诱变剂，再结合肉链的胶原、明胶、琼脂得到培养基。

但需要纠正两点：

1. **不是全程无菌房**。培养皿、最初的生物糠等没有统一的无菌要求；具体细菌/培养基配方声明无菌条件，基板和NPU声明普通洁净条件。
2. 富集浆液的铀投入是酿造配方中的材料，不证明需要另造“辐照机”。该段有铀238粉、铀235小撮粉等配方分支，并存在硅岩分支；任务应按实际机器引导，不能根据叙事发明设备。

`CLEANROOM` 与 `STERILE_CLEANROOM` 是不同条件。在出货实现中按类型匹配，**不能默认“无菌房更高级，所以一间房包办所有电子配方”**。最终以机器实际提供的类型、配置及运行结果验证。

### 3.4 UV 终点与少量 UHV 收尾

| 电路产物 | 标签档位 | 已核实关键制造条件 |
|---|---|---|
| 湿件处理器 | LuV | 普通路线38400 EU/t、200t、普通洁净室，当前配置输出2 |
| 湿件处理器集群 | ZPM | 38400 EU/t、400t、普通洁净室，输入湿件处理器2，输出集群2 |
| 湿件超级计算机 | UV | 流水线，38400 EU/t、400t，研究16 CWU/t |
| 湿件主机 | UHV | 流水线，300000 EU/t、2000t；研究96 CWU/t且研究EU/t为UV档 |

仅用于显示“产物档位与制造功率不同”，不是完整物料清单。完整投入必须沿GT原配方保留。

当前 `config/gtceu.yaml`：`harderCircuitRecipes: false`、启用洁净室、启用研究。湿件主机可作为UV工业能力的选修终点，因为其制造功率300000仍落在UV供电范围；**这不代表主机的每项前置都已在当前存档实测可达**，最终还须验证研究、材料及机器供电。

证据：GT7 `CircuitRecipes.java:1002,1492-1563`。高阶GTNN标签的情况见附属线文档，不以“唯一UHV”作为整包结论。

## 4. Pollution 血肉线：实际是分支，不是连续进化链

### 4.1 配方与共享培养基

| 产物 | 直接投入 | 机器；EU/t；时间 |
|---|---|---|
| `pollution:primitive_meat` ×2 | 腐肉4＋生物质500 | 化学反应釜；30；100t |
| `pollution:rat_brain` ×1 | 僵尸脑1＋原始血肉1＋GT无菌培养基250 | 化学反应釜；120；200t |
| `pollution:mitochondrion_power` ×1 | 原始血肉2＋糖4＋InfusedEnergy 288 | 化学反应釜；120；200t |
| 内啡肽稳定器 | 鼠脑1＋盐粉2＋InfusedLife 288 | 化学反应釜；480；200t |
| 溶酶体稳定器 | 鼠脑1＋Thaummix粉2＋GT无菌培养基500 | 化学反应釜；480；200t |
| 冷冻器 ×2 | 冰4＋InfusedCold 576 | 化学浸洗；120；200t |
| `pollution:ips_human_brain` ×1 | 鼠脑2＋`thaumcraft:brain_jar` 1＋InfusedHuman 500＋InfusedLife 1000＋GT无菌培养基1000 | 魔导组装机；1920；800t |
| `pollution:blood_circuit_advanced` ×1 | 基础blood_circuit、鼠脑、线粒能源体、内啡肽稳定器各1＋GT无菌培养基1000＋InfusedAura 1000 | 魔导组装机；7680；500t |

表中 InfusedX 是源码材料名。新增脚本时须从当前流体注册表导出精确ID，不按拉丁要素名猜拼写。

这些Pollution配方本身没有声明GT洁净室条件，但这不意味着前期就能完成：**它们吃的无菌培养基仍受GT上游工业门槛约束**。低EU/t配方不等于低科技整链。

证据：P `loaders/recipes/RemainingItemRecipes.java:524-636`；`loaders/recipes/MagicIntegrationRecipes.java:171-188`。GTAddon注册链可达这些方法，出货字节码中存在对应调用；最终是否被包脚本覆盖仍待运行时确认。

### 4.2 原报告的链条应这样纠正

- 线粒能源体不以鼠脑为输入；它与鼠脑是从原始血肉展开的并行分支。
- iPS脑不需要先制造两类稳定器和冷冻器。
- iPS脑没有通过现有配方变成 `blood_circuit_advanced`。
- advanced血电路反而依赖基础 `blood_circuit`，后者在本轮搜索范围内没有找到生产配方。
- `blood_circuit.0` 至 `.12` 的MV～MAX名称是占位物品注册，未找到GT通用电路tag或生产链；基础、ultimate、supreme也不能凭名称认定可达。

因此，**“Pollution 已修好70%的湿件联动”不是可量化结论**。它确实提供了可复用的生物加工节点，但缺失的生产前置与跨系统连接仍需设计，不能只补一个tag了事。

证据：P `common/item/PollutionItems.java:209-228,362-368`、`MagicIntegrationRecipes.java:178-185`。

## 5. TC4R / TH：可用素材与不可借用的能力

### 5.1 脑素材

- 普通僵尸且满足击杀归属条件时，脑掉率为10%＋每级掠夺10个百分点；脑僵尸独立掉落表为50%＋每级10个百分点。旧报告把两者混淆。
- 脑缸研究为 `JARBRAIN`，默认容量2000 **经验点**，不是2000级；容量可被数据覆盖。不是无限无损经验存储。
- `isorropia:somatic_brain` 是Curios头部饰品。出货类只实现装备位条件，没有“知识拦截”“生产神经组织”一类行为。
- 当前包有Forbidden Magic，活体脑分支研究为大小写敏感的 **`isorropia:somaticbrainFm`**。配方消费脑缸、铁锭、漏斗、僵尸脑2，以及cognitio150、lucrum100、`forbidden_magic:invidia`20。把脑缸上游算进去共需3个僵尸脑。

研究完成后配方可重复制造，但“可重复”不等于“自动化吞吐已经充足”。如将其作为工业输入，必须把研究、源质和注魔时间算入成本。

证据：TC59 `TCCommonEvents#onLivingDrops`、出货僵尸/脑僵尸loot、`BrainJarBlockEntity#configuredMaximumExperience`；TH `common/items/baubles/ItemSomaticBrain.java`、出货 `somatic_brain_fm.json` 和 `research/isorropia.json`。

### 5.2 生物生产

| 生物 | 已核实行为 | 设计含义 |
|---|---|---|
| 矿猪 | 吃掉落物形式的圆石；每块累加1～15进度，达到100产生一份；由矿物tag找矿粒，缺矿粒时可退回整份粉 | 必须审计最终材料池和每份价值，不能无条件接所有GT材料 |
| 金鸡 | 成年每6000～11999t产金蛋；金蛋烧炼得1金粒 | 是低速副产路线，不是每蛋一锭金或高端肉源 |
| 学者鸡 | 同周期产墨蛋，另有羽毛产出；墨蛋带黑染料标签 | 不是研究点/知识自动生成器 |
| 彩羊 | 按周期换色，仍按羊的剪毛玩法取毛 | 不等于自动生成所有染料 |

矿猪平均吞吐需测量，不能把“每块平均进度8，所以精确12.5块产物”当作实测产率；越界丢弃/保留进度、进食频率、目标选择都会影响结果。

证据：TH `common/entities/OrePigDrops.java:19-22,58-75`、`EntityOrePig#eatStone`、鸡/羊类 `aiStep`；出货金蛋烧炼JSON。

### 5.3 治疗、warp、flux与工业污染分开记账

| 系统 | 作用对象 | 当前实际接线 |
|---|---|---|
| Curative Vat 的victus | 生物生命值 | 每次符合条件时消耗源质治疗 |
| Curative Vat 的其他效果 | 饱食、亡灵治疗、腐化实体 | 有对应被动效果，但不是全局净化 |
| warped_tumor | 玩家TC warp | 暂存最多50，死亡归还；不是永久删除 |
| TC flux | 魔法环境排放 | 缸的排污会释放TC flux，不等于净化外界 |
| Pollution区块污染 | 工业污染存档值 | 独立机制；真正清理需要明确调用对应API |

Pollution的部分事件读取玩家TC warp，因此肿瘤暂存可能间接影响事件概率；这不是清除区块污染。

若将来做“生物净化”，须单独实现消耗、净化量、范围和冷却。已找到 `Pollution.scrub(Level, int x, int z, double amount)` 入口，但仍要核实坐标语义和权限，不得仅因玩家站在治疗缸里就无限清污染。

证据：TH `common/curative/CurativeEffects.java:22-30`、`TileVat#ventFlux`、`SelfInfusions#absorbWarp/#releaseTumorWarp`；P `PollutionWarpEvents#totalWarp`、`PollutionJS#scrub`。

## 6. 扩展生物自动化之前的两个阻断项

### B0-1：源质转化不是守恒等价

出货静态链（六原始要素适用）：

```text
1 点 TC 源质
  → 转换矩阵：144 mB pollution:infused_<element>
  → 高压釜：1 个 thaumcraft:<element>_crystal_cluster
  → 粉碎机：1 个 pollution:infused_<element>_dust
  → 源质冶炼：该粉注册了4点对应源质
```

`element` 为air/fire/water/earth/order/entropy，分别对应aer/ignis/aqua/terra/ordo/perditio。

- 转换矩阵每10t最多转换1点，所查转换代码没有EU扣款。
- 高压釜144 mB→1晶簇，120 EU/t、200t；粉碎1晶簇→1粉，120 EU/t、20t。
- 对应粉和宝石通过物品级注册得到4点源质；没有来源NBT来区分“原矿产的”与“流体回造的”。
- GT源质炉可能将4点按144 mB/点重新流体化；普通流体提取路线却是1粉→144 mB。

**这是有能耗、时间和火流体燃料成本的放大链，不是已经证明的免费永动。**它说明各转换比例不统一，尚未实机复现本包最终闭环。不能将这个介质作为工业量产底座之后再补平衡。

推荐处理：先列出各条正反向兑换的源质当量，选定统一标准，并使任一可重复闭环的输出当量不大于输入。可调整返造晶簇的耗量或粉的源质赋值，但需选择一个一致方案，不能随意改单边数字破坏其他用途。修复应针对新增产出，不清玩家已有库存。

定点证据：P `common/machine/multiblock/magic/InfusedExchangeMachine.java:66-96`；`loaders/recipes/MagicGCYMRecipes.java:622-648`；`api/magic/PollutionObjectAspects.java:50-60,84-89`。

### B0-2：冶炼输出没有按实际接受量扣余量

`EssenceSmelterMachine` 开工先消费物品，完成后对范围内每个符合条件的源质容器发送整份产量，忽略 `EssentiaApi.add` 返回的实际接受量，再清空pending。

后果取决于布局：多个能接受的容器可能得到重复产出；全部满载或方向不符时可能丢失产出。不是任何方向摆两个罐都必定复现，守卫罐等有输入面约束。

修复的必要不变量：

```text
本次生成总量 = 已成功送出量 + 机器保留待送量
```

- 每次传输后执行 `remaining -= accepted`，不能对下一个容器再次发送原始总量。
- 无处接收时保留剩余并保存NBT，不能直接reset销毁。
- 重启后继续输出未送余量，不再次扣原料，也不重放已送量。
- GT流体输出版本同样检查实际fill接受量，不能只修TC罐路径。

证据：P `common/machine/multiblock/magic/EssenceSmelterMachine.java:119-145,164-179`；`GtEssenceSmelterMachine.java:111-158`；TC59 `EssentiaApi#add`。**本轮未修改或实机复现此缺陷。**

## 7. 推荐联动：少量、有收益、不绕过门槛

### 7.1 第一批只选两个接点，不铺开新电路家族

| 接点 | 推荐方向 | 必须保留 | 开工前仍需确定 |
|---|---|---|---|
| 血肉材料→培养耗材 | 原始血肉经过明确的加工步骤，成为培养基肉源的可选输入 | 诱变剂、琼脂、盐/钙链、IV无菌要求与灭菌流程 | 原始血肉当量、输入槽数量、原配方实际吞吐、替代收益 |
| 神秘脑组织→培养效率 | iPS/脑素材参与一个可重复使用或按多批摊销的培养辅助件，增强干细胞生产 | Osmiridium、细菌、无菌培养基、LuV无菌要求；不直接输出NPU/湿件电路 | 辅助件制造成本、是否消耗/耐久、机器能否支持该催化形式、收益与摊销周期 |

第二项是**设计方向而非已经确定的配方**。不得先写一个“消耗1个iPS脑换20%提速”的脚本就宣布完成。

### 7.2 为什么原先几个奖励方案不能直接用

- **双倍湿件**：会同时稀释晶体CPU、纳米CPU、元件和精密材料成本，不只是奖励生物部分；而原processor配置已输出2，再翻倍相当于输出4。必须计算对整个后续电路树的影响。
- **每批干细胞消耗1个iPS脑只省60t**：原干细胞一批用500 mB无菌培养基；iPS脑本体用1000，两个鼠脑再用500。添加剂至少额外花1500 mB无菌培养基，还没计脑缸、要素与800t魔导组装。仅把300t降到240t通常不值，不能当作已平衡方案。
- **给原始培养基另加一格血肉输入**：原配方已有4类物品和1种流体。第五物品输入能否放进目标机器/配方类型，要检查输入槽；不能只看builder能编译。
- **用somatic_brain直接替16个干细胞**：它的现有配方并未承载Osmiridium或GT无菌培养门槛，容易把神秘研究变成工业旁路。
- **只补blood电路tag**：不能修复缺失的生产配方；反而一旦某个奖励或合成提供占位物品，就可能直接绕过整段工业链。

### 7.3 收益评估模板

每条候选必须填写以下表格后才能定数量：

| 维度 | 原GT路线 | 跨线候选 |
|---|---|---|
| 每件最终产物的原料当量 | 包括副产回收后的净耗 | 同口径，包含魔法素材的完整制造链 |
| EU总耗 / 主设备占用时间 | `EU/t × duration`，区分并行 | 不能只看末端机器省时 |
| 关键瓶颈 | 培养基、干细胞或电路组装 | 是否真的改善原瓶颈 |
| 装置及研究投入 | 原有GT能力 | 新增治疗缸、注魔、Pollution机器、辅助件成本 |
| 摊销 | 基准 | 做多少批后才优于原路线 |
| 槽位与流体仓 | 原机可容纳 | 物品输入种数、不可消耗槽、流体种数都能容纳 |
| 可逆闭环 | 原有回收 | 不增加免费原料/源质/货币循环 |

建议优先做“明确的额外来源或合理摊销后的效率优势”，不是为了证明联动而添加一个永远亏损的配方。

## 8. 实施落点：KubeJS为主，只有机制缺陷才改mod

### 8.1 预计文件分工，尚未创建

- `kubejs/server_scripts/bio/bioCultureBridges.js`：少量GT/Pollution alternate；注册ID建议 `kubejs:bio_bridge/...`，原GT配方保留。
- `kubejs/server_scripts/bio/bioCreatureData.js`：只有确实需要调整活体注魔时才创建。
- `config/ftbquests/tools/build_bio_chapter.py` ＋ `bio_ids.json`：正式实施时先检查是否已经有同主题生成器，优先复用而非重复造章。
- Pollution Java：修源质输出记账/满载丢失；这是机器机制，不能靠一个KJS价格或配方补丁解决。
- TH Java或公开配置：如现有入口不能限制矿猪候选池，再最小化增加过滤配置，不改实体ID。

生产脚本使用 `let`，不得新写 `const`；避免重复全局 `Java.loadClass` 绑定。价格、配方数值与材料白名单归整合包数据，不硬编码进通用mod。

### 8.2 TH 1.0.5 的活体配方接口

实际出货为19份creature＋10份self JSON，经自有reload listener加载，**不是旧报告说的“20种硬编码、没有JSON”**。

准确接口：

- `ThaumicHorizons.creature(DataPackEventJS event, String id, JsonObject data)`
- `ThaumicHorizons.self(DataPackEventJS event, String id, JsonObject data)`
- `removeCreature(event, id)` / `removeSelf(event, id)`

调用位置是 `ServerEvents.highPriorityData`，不是普通 `event.recipes` 或捏造的 `type: 'isorropia:living_infusion'`。

以下仅展示**保留原配方字段的语法**，不属于本轮已安装的更改：

```js
ServerEvents.highPriorityData(e => {
  if (!Platform.isLoaded('isorropia')) return
  ThaumicHorizons.creature(e, 'isorropia:golden_chicken', {
    kind: 'specie', research: 'isorropia:goldchicken',
    target: { entity: 'minecraft:chicken' },
    result: 'isorropia:golden_chicken',
    components: [
      { item: 'minecraft:golden_apple', count: 2 },
      { item: 'thaumcraft:crucible' },
      { item: 'thaumcraft:thaumium_ingot' }
    ],
    aspects: { 'thaumcraft:fabrico': 45, 'thaumcraft:lucrum': 30, 'thaumcraft:metallum': 30 },
    instability: 2
  })
})
```

写入路径为 `data/<namespace>/isorropia/creature_infusions/<path>.json`。同ID是覆盖原配方，不是创建额外线路；研究字段及附属要素命名空间必须保留。

证据：TH `common/compat/kubejs/HorizonsData.java:17-30,50-58`、`HorizonsKubePlugin#registerBindings`、`InfusionRecipes#onAddReloadListeners`。

## 9. 任务引导，不伪装成配方锁

建议分为4组，不预先固定任务总数：

1. **认识活体材料**：僵尸脑、脑缸、治疗缸与要素；强调研究前置、warp/flux区别。
2. **培养与加工**：原始血肉、鼠脑、培养基；展示分支而非错误的串联箭头。
3. **工业化培养**：无菌房、干细胞、普通洁净房、NPU、湿件；明确“电路档位”与“制造功率”。
4. **可选收尾**：UV湿件超级计算机；少量UHV湿件主机作为选修，不向更高阶段扩展。

原GT/神秘任务ID保留；新增ID使用生成器与16位大写十六进制登记表。获取一个物品只证明拿到它，不证明机器运行过、研究完成或洁净室成型；这些目标需要相应事件条件或明确标注的人工确认。

奖励优先教程、装饰或阶段标记，不发绕过培养基/研究的关键电路和整套机器。任务书未解锁不是硬配方门槛，不要靠隐藏任务宣称“杜绝越级”。

## 10. 集中验证与发布标准

### 10.1 先只读建立运行时基线

同一次完整测试服会话收集：模组版本和哈希、最终RecipeManager、自有TH配方表、GT电路tag、矿猪材料池、研究启用配置。不能只读普通RecipeManager就宣称TH所有自有配方不存在。

### 10.2 验收矩阵

| 用例 | 必须证明 |
|---|---|
| 原配方回归 | 已有GT培养基、干细胞、NPU配方ID仍在，原机器能执行 |
| 普通/无菌洁净室 | 分别在符合与不符合条件下开机，禁止无条件绕过 |
| 源质守恒 | 以六原始分别跑正反转换；记录真实接受量、能耗、燃料和最终库存 |
| 多容器输出 | 空罐、半罐、满罐、两罐、方向错误、卸载/重启均不复制或丢失待输出量 |
| 矿猪 | 打印最终候选，白名单外高阶材料不出现；统计一段足够长的进食/产物记录 |
| alternate | 原料不全、缺研究、低电压、缺洁净条件应拒绝；正常条件下收益与成本表一致 |
| KJS重载 | 成功重载不重复注册；失败不得静默删除原方或产生空流体输入 |
| 旧存档 | 老机器、已有库存、研究、任务进度不被清除；在副本上验证后再部署 |
| 魔法行为 | 治疗仍是治疗，不凭空清工业污染；若另写净化桥，则实测范围、费用和冷却 |

不要每个小功能启动一次游戏：先单测/静态校验，累计一批后在同一隔离会话内验证。真实客户端只用于JEI、书本、渲染及交互，不能把“界面显示正常”当成整个生产链通过。

### 10.3 发布与回滚

- 不在本次文档工作中更新jar或服务器。
- Java机制修复须单独构建、版本指纹、数据兼容说明；不能运行中覆盖jar。
- KJS alternate按独立ID和独立脚本提交，便于只撤新增配方；原方不删，回滚不会锁死旧玩家。
- 涉及矿猪产出限制/转换比例的经济变化要写上线说明；不追溯没收玩家已有物品。
- 正式模组部署、更新器发布、生产服重启均另行取得明确授权。

## 11. 下一步唯一推荐顺序

**封住源质输出/倍率问题 → 核查矿猪最终产物池 → 建立完整服运行时配方基线 → 计算两个生物接点成本 → 实施最小alternate → 写任务 → 同批回归。**

不是先加几十个配方，再用任务文字解释为什么可以越级。
