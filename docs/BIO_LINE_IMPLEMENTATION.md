# 生物线第一批：实现与隔离服验收

> **2026-11-04 第四批更正**：矿猪政策依赖服务端config/isorropia-common.toml，单换jar不会自动应用白名单。第四批将显式纳入交付清单；神秘LuV电路保留神经处理单元，不能绕过本生物线。 [PHASE4_ACCEPTANCE.md](PHASE4_ACCEPTANCE.md)。

> 批次：`bio-phase1`。实施与测试跨2026-11-03至11-04；这是 [BIO_LINE_PLAN.md](BIO_LINE_PLAN.md) 的第一批落地记录。
> **范围：源质安全、矿猪边界、三个可选生物配方，以及测试中发现的GTNN启动兼容。不是全部附属线/任务章节完成。**
> 主体到UV，少量UHV可选收尾的范围不变。本轮未改生产服、未发布更新器、未清理老玩家数据。

## 1. 改了什么

### 1.1 Pollution：两种源质炉

源码：`H:/MinecraftMods/Pollution-Unofficial-1.20.1`。

- 新 `api/magic/EssenceBatch.java`：一个已消费输入批次的加工进度及待输出余量。
- TC源质炉按容器返回的实际接受量扣减，同一批不会向每个罐子各发一次完整产量。
- GT源质炉遍历全部输出仓，余量以mB保存；17mB之类的零头不按整份源质截断。
- 满罐、满输出仓时保留pending，不继续消费下一批，也不为等待输出反复扣燃料。
- 暂时结构失效、仓缺失时暂停而不是清空已消耗原料的批次。
- 控制器 `saveCustomPersistedData/loadCustomPersistedData` 保存/恢复批次。
- 使用 **`AspectQueryApi.item()`** 读取有效的每件物品分解要素。原 `AspectApi.getItemAspects()` 读取的是物品内部储存源质，普通物品返回空，不能用于炼金分解。
- 机器向自己的GT输出仓写入使用 `fillInternal()`；从燃料输入仓取料使用 `drainInternal()`。外部方向性接口会拒绝这些内部操作。
- 转换矩阵同时改用内部输出仓填充接口。

这些修改不恢复旧版本已丢失的产物，也不追溯没收旧库存；仅从新版开始改善处理与输出。

### 1.2 六原始要素闭环

本批规则：

```
1点源质 = 144mB对应流体 = 1个本模组原始元素宝石/粉中的源质
```

- 六原始材料的gem/dust由4点改为1点，其他复合要素材料不在这次统一修改范围。
- 流体高压釜返造保持原配方ID与144mB投入，但输出改为Pollution自身元素宝石。
- 不再用144mB生成原生TC晶簇，因为晶簇放置/破坏可以获得多个碎片，绕过单纯粉末赋值修正。
- 原生TC晶簇照常存在、获取和使用，原晶簇粉碎路线保留；不改玩家已有方块。

运行时确认六元素粉/宝石均为1点；返造六配方输出均为本模组gem，不是TC晶簇。该断言只针对已枚举的闭环，不声称穷尽整包所有跨mod转换。

### 1.3 TH：矿猪产物策略

源码：`H:/MinecraftMods/Isorropia-1.20.1-wt/multiversion`。

新增配置：

```toml
[creatures]
ore_pig_materials = ["iron", "copper", "tin", "lead", "silver", "gold", "zinc"]
ore_pig_dust_fallback = false
```

- 通用mod默认仍为 `["*"]`＋允许dust回退，避免强行改变所有整合包。
- Sunlit Valley和测试服采用上述白名单，不允许缺矿粒时产整份粉。
- 空白名单表示不产出；配置变更会使缓存重新生成，tag重载仍可刷新。
- 不改矿猪实体ID，不删除现有矿猪，不改变已有库存。
- 测试服最终候选7项：Create铜粒/锌粒、原版金粒/铁粒、TC铅粒/银粒/锡粒；实际映射由当前tag选择。

主实例配置文件已写入策略，但**主实例旧TH jar不认识新键，必须随修复jar更新后才生效**；本轮jar只部署在本地测试服与候选交付目录。

### 1.4 三条生物配方

文件：`kubejs/server_scripts/bio/bioCultureBridges.js`。全是新增，原GT/Pollution配方保留。

| 逻辑ID尾部 | 机器 | 投入 → 产出 | 功率 / 时间 / 条件 |
|---|---|---|---|
| `bio/primitive_meat_to_meat_dust` | 研磨机 | 原始血肉1 → 肉粉1 | 2EU/t，102t；无额外骨粉或概率增产 |
| `bio/ips_brain_bootstrap` | 化学反应釜 | 鼠脑2＋脑缸1＋infused_human500＋infused_life1000＋sterilized_growth_medium1000 → iPS脑1 | 30720EU/t，1600t，无菌洁净室 |
| `bio/ips_assisted_stem_cells` | 化学反应釜 | Osmiridium小粉4＋不消耗的iPS脑1＋细菌500＋无菌培养基500 → 干细胞32＋细菌浆液500 | 30720EU/t，240t，无菌洁净室 |

为什么有起步配方：原iPS脑需要魔导组装机，而魔导组装机的控制组件也需要iPS脑，存在首件循环。新增起步方保留同样生物材料与三流体，在更高LuV无菌条件下以两倍加工时间起步；原EV魔导组装机800t路线继续作为成本更低的批量生产路线。

为什么用小粉：4小粉等于1完整粉，且与原300t干细胞配方的完整粉输入分开，避免“原方是新方输入子集，放脑仍总选原方”。原方不改，催化方占化反两种物品输入，恰好放得下。

为什么脑不消耗：iPS脑制造至少含1500mB无菌培养基等投入；逐批消费脑仅换60t提速不划算。这里是一次性培养辅助投入，240t比300t少20%时间、同条件理论吞吐提高25%，不增加干细胞产量。

实际运行时ID由GT加机器类型前缀，例如：

- `society:macerator/bio/primitive_meat_to_meat_dust`
- `society:chemical_reactor/bio/ips_brain_bootstrap`
- `society:chemical_reactor/bio/ips_assisted_stem_cells`

GT自动生成两个 `society:large_chemical_reactor/bio/...` 对应项，dump核实保留无菌条件。这是正常派生，不是重复注册。

### 1.5 测试发现并处理的兼容问题

**GTNN与Botania启动冻结**

- GT7.5.3材料初始化从 `FMLConstructModEvent.enqueueWork` 启动；并非看到日志common_setup文字就能认定方块已经注册。
- GTNN `BotaniaMaterialsModification` 过早求值三个 `BotaniaBlocks.*` 字段，触发方块构造时注册表仍冻结。
- canonical Kotlin源码改为 `GTMemoizer.memoizeBlockSupplier`；锭/粒引用也显式写 `Supplier<ItemLike>`，避免Kotlin/Java的函数式接口重载误选 `ItemLike`。
- 完整GTNN Gradle构建受到远端依赖下载阻塞。本次使用本机Gradle附带的Kotlin编译器离线编译**真实修改的Kotlin源码**，将生成的class替换进原1.3.10归档，其余条目保持原样。原始jar、编译源码、生成脚本、前后哈希都有保留。
- 这是可追溯兼容候选产物，**不是宣称完整GTNN工程构建通过**，不要无说明覆盖正式发布版本。

**已有KubeJS的可选依赖**

`gcyr/gtnnLinks.js` 的 Mekanism 氢条目在未装Mek时产生空流体，阻断回调后续配方。本批加 `Platform.isLoaded('mekanism')` 守卫，主包装Mek时行为不变；两处新触碰的声明改为 `let`。测试服不为一条可选燃料拉入整套Mekanism。

同时将整合包已有4份 `thaumcraft/recipes/compat/native_*_cluster_smelting.json` 带到测试服。它们是已有修补，不计作本次新功能。

## 2. 测试环境

目录：**`G:/emoney-bio-test`**，复用本地emoney服务端库，新建 `bio-test` 世界，不复制生产世界。

- 服务端：Rosetta-Mohist 1.20.1-ecf8d5ad，内置Forge47.4.13，Java21.0.8。
- 游戏端口127.0.0.1:25589；本地RCON25590；Rosetta127.0.0.1:48790。
- 19个顶层mod及其jar-in-jar依赖：GTCEu/GTNN/GCYR/GTMFO、TC4R20759/Forbidden Magic/TH、Pollution/AS/Botania/Create、Curios/TerraBlender/Patchouli、KubeJS/Rhino/Architectury/GeckoLib、Rosetta。
- 仅8个相关server脚本（生物、GCYR桥、魔法研磨、TC配方）及矿簇数据覆盖，不复制整包任务/经济/客户端内容。
- 不含Connector/ME、Mekanism、整套Sunlit经济等非本批必需内容。因此本次通过不等于完整435+模组组合通过。
- `BIO_MANIFEST.json` 记录精确jar SHA；`kotlin-compat-build.json`记录GTNN特殊构建方式。

## 3. 验证结果

### 3.1 编译与单测

- Pollution `test build`：6项单测，0失败。
- TH Forge1.20.1 `test build`：16项单测，0失败。
- GTNN canonical Kotlin修改类离线编译通过；完整Gradle构建未通过依赖下载阶段。
- Pollution本机ForgeGradle缓存缺少部分Minecraft传递依赖，使用本地init脚本补回已安装Minecraft库；没有把它们打进mod jar。

### 3.2 最新冷启动的六组运行时探针

| 探针 | 实际结果 |
|---|---|
| 最终配方dump | 70条相关配方；38项自动断言全部通过 |
| TC源质炉双罐/满罐 | 100点分到64＋36；两罐满时10点保留；控制器NBT恢复后按6＋4补出，无复制 |
| GT源质炉输出仓 | 144mB中第一仓只收17，保留127；NBT恢复后第二仓接收127，无截断/复制 |
| 源质炉实际加工 | TC和GT两种均消费2个元素粉一次；10t时NBT恢复、结构失效暂停后继续；20t共扣640EU、20mB火流体，分别产2点源质/288mB |
| 干细胞催化 | 无房、普通洁净房、缺脑均拒绝；LuV无菌fixture下两批240t，8小粉＋两流体各1000 → 64干细胞＋1000浆液，脑仍1 |
| 首件iPS | IV不能接受；LuV无菌fixture下消耗全部规定原料/流体，1600t得到1脑 |

**验证边界必须保留**：

- 使用实际控制器、仓、TC罐、GT配方查找和RecipeLogic；多方块部件列表与成型标记由探针注入，未验收完整结构搭建。
- 洁净室由ICleanroomProvider测试fixture提供，验证条件判断而非实际洁净室成型/污染度模拟。
- 加工调用真实逻辑并注入测试能源，批次推进为同步调用，不等同全服长期吞吐压测。
- 已验证NBT保存/恢复及冷启动配方持久加载；未宣称跨不同区块存档具有崩溃原子性。
- 矿猪验证最终候选表与策略单测，未跑长期动物农场产率统计。
- 肉粉alternate注册/输入产出已断言，未另做实际研磨机完整流水线探针。

### 3.3 仍存在的非本批启动告警

测试服仍有AS lumen/perk数据告警、GT/GCYR个别原有配方/lookup告警、未安装JEI的可选Mixin警告等。本批KubeJS加载8/8、0脚本错误，新生物配方可实际执行，**不把整个启动日志说成零错误**。这些独立问题没有通过删掉模组隐藏，也没有扩展到本轮之外进行全面修复。

首次启动还观察到Mohist依次准备多个维度出生区；这属于本次环境的真实启动开销，不再仅凭“11个维度”猜测。

## 4. 证据与复跑

测试服中：

- `bio-reports/runtime-recipes.json`：最终输入输出、电压、时间、条件、派生配方、源质值、矿猪池。
- `bio-reports/assertions.json` / `assertions.txt`：38项断言。
- `bio-reports/machine-probes.json` / `final-probes.txt`：最新6组探针结果。
- `bio-console-verified.log`：最后一次冷启动日志（包含调试桥启动敏感信息，不对外打包原文）。
- `BIO_MANIFEST.json`、`kotlin-compat-build.json`：版本与特殊编译说明。

可复跑探针已收录 Pollution源码 `tools/bio/`。测试桥工具只读取本地测试目录token，不使用生产凭据。

## 5. 当前部署状态与后续

- 修复jar已部署并验证在 **G:/emoney-bio-test**；该测试服完成后正常保存停止。
- 主实例已写入三条新配方脚本、可选Mek守卫、矿猪策略和文档；主实例修复jar尚未替换，因此不能宣称主实例整套生物功能已验收。
- 本轮未同步mirror、未发布更新器、未上传生产服jar或脚本。
- 可供人工审阅的候选交付目录：`H:/MinecraftMods/dist/bio-phase1-validated/`，含产物、哈希、pack delta、探针与精简报告；其中GTNN构建限制必须随包保留。
- 贸易/生物FTBQ新章节、GCYR燃料tier语义复核、更多UV设备筛选，以及完整生产组合回归，仍属于后续批次，不在本次完成清单。

## 6. 第二批：任务章节与后续状态（2026-11-04）

- 新增 `config/ftbquests/quests/chapters/bio_wetware.snbt`（科技组 order 24，23 任务），
  生成器 `build_bio_wetware_chapter.py` + `bio_wetware_ids.json`。
  覆盖：血肉→肉粉→培养基→灭菌→培养皿、鼠脑→iPS 脑→催化干细胞、
  湿件基板→NPU→UV→UHV 选修、GTMFO 废肉/污泥/明胶回收、矿猪白名单与躯体脑边界。
- 外部前置 6 个：无菌洁净室、干细胞、最佳UV电路、湿件主机、两种熔炉、躯体脑。
- 运行时核对：本章 21 个图标/物品 id 全部存在；4 条 `society:bio/*` 与 GTMFO/GT
  配方 id 均从服务器 RecipeManager dump 确认（含 `society:macerator/bio/primitive_meat_to_meat_dust`
  102t、`ips_brain_bootstrap` 1600t、`ips_assisted_stem_cells` 240t、
  `food_gelatin_recovery` 400t）。
- 相关章节：`thaumic_industry.snbt`（神秘工业，20 任务）承接源质→要素流体与工业注魔；
  原版 GT 湿件链仍在 `zpm__zero_point_module.snbt`，本批不重复。
- **仍未做**：主实例 Pollution 修复 jar 替换；完整生产组合回归；生产服部署。
