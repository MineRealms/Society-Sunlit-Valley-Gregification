# 神秘电路与工业注魔

> 2026-11-04 第四批修订。下表来自当前 Pollution 源码；完整隔离副本运行时验收仍在进行，结果统一见 [PHASE4_ACCEPTANCE.md](PHASE4_ACCEPTANCE.md)。第三批的 19 条配方/普通组装机实现不是当前规格。
> 任务章节 `thaumic_industry.snbt` 保持 20 个任务和原有 ID。

## 1. 边界与平衡

- 保留全部 17 个 `blood_circuit*` 旧 ID；MV～UV 七个成品进入同级 GT 通用电路标签。
- `.7`～`.12` 共 **6** 个 UHV～MAX 神秘电路停用：无配方、无标签、JEI 隐藏；老存档物品不删。
- 原有 `magic_circuit` 蕴魔电路是另一条专用件路线；该族 UEV～MAX 板/电路继续停用。
- 魔法替换的是芯片、存储芯片、贴片元件；**不替换基板、下级电路、生物前置、线材、金属结构件与研究设备**。
- “同级”是结构性约束：与选定 GT 参考配方保持同一机器、能耗、时间、产出、洁净室、下级电路数量。魔法材料不与电子元件宣称等价原料成本，仍须监测量产后的实际经济成本。

## 2. 四个模板

模板是消耗品，不是永久催化剂。模板 2～4 都消耗上一块模板。

| 模板 ID（pollution:） | 原始制作 | 材料 | 要素 / vis | 不稳定度 |
|---|---|---|---|---|
| blood_circuit | 奥术工作台 | 神秘锭×2、水银×1、gtceu:basic_integrated_circuit×1 | vis aer 16、ordo 8 | — |
| blood_circuit_advanced | 注魔 | 模板1、虚空锭×1、水晶精华×2、水银×1 | praecantatio 16、metallum 8、vacuos 8 | 3 |
| blood_circuit_ultimate | 注魔 | 模板2、thaumadds:mithrillium_ingot、影金锭、以太碎片×2 | praecantatio 24、alienis 16、metallum 12 | 5 |
| blood_circuit_supreme | 注魔 | 模板3、thaumictinkerer:ichorium×2、创造碎片、下界之星 | praecantatio 32、alienis 24、auram 24 | 8 |

- 两颗水晶精华/以太碎片用两个独立 Ingredient/基座；`Ingredient.of(a,a)` 是候选列表，不能表达数量 2。
- 模板1研究为空；模板2～4挂 `INFUSION`。
- 创造碎片的原配方已消耗原始珍珠，模板4不再额外消耗第二颗。
- 四模板均有工业孪生：保持相同实物投入；源质 144mB/点、vis 36mB/点。

## 3. 成品与 GT 参考配方逐级对照

以下线材、基板和焊锡均是 GT 物品/流体。焊锡指 `gtceu:soldering_alloy`。

| 级 | 魔法投入 | 保留的科技投入 | 焊锡mB | EU/t | tick | 产出 | 机器 / 附加条件 | GT参考配方 |
|---|---|---|---:|---:|---:|---:|---|---|
| MV .0 | 模板1、神秘锭 | 塑料PCB、细红合金线×4 | 72 | 60 | 200 | 2 | 电路组装机 | processor_mv |
| HV .1 | 模板1、水晶精华 | 环氧PCB、细金银合金线×8 | 72 | 600 | 200 | 2 | 电路组装机、洁净室 | nano_processor_hv |
| EV .2 | 模板2、虚空锭 | 纤维增强PCB、细铂线×12 | 72 | 2400 | 200 | 2 | 电路组装机、洁净室 | quantum_processor_ev |
| IV .3 | 模板2、mithrillium_ingot | 多层纤维增强PCB、细铌钛线×8 | 72 | 9600 | 200 | 2 | 电路组装机、洁净室 | crystal_processor_iv |
| LuV .4 | 模板3、ichorium | **神经处理单元**、细钇钡铜氧线×8 | 72 | 38400 | 200 | 2 | 电路组装机、洁净室 | wetware_processor_luv |
| ZPM .5 | 模板3、adaminite_ingot | 湿件PCB、**神秘LuV电路×2**、细钇钡铜氧线×16 | 144 | 38400 | 400 | 2 | 电路组装机、洁净室 | wetware_processor_assembly_zpm |
| UV .6 | 模板4、mithminite_ingot | 湿件PCB、**神秘ZPM电路×2**、细钇钡铜氧线×24、PBI箔×32、铕板×4 | 1152 | 38400 | 400 | 1 | **装配线、研究站16 CWU/t研究神秘ZPM电路** | wetware_super_computer_uv |

配方 ID：
- `.0`～`.5`：`pollution:circuit_assembler/thaumic_circuit/<N>`。
- `.6`：`pollution:assembly_line/thaumic_circuit/6`。
- 原来的 `pollution:assembler/thaumic_circuit/*` 不再注册。物品 ID 不变；已存储旧机器配方的行为仍需运行时/存档测试，不承诺旧批次自动迁移。

### 材料顺序与不可绕过的门槛

神秘领域的实际合成顺序是 `mithrillium → adaminite → mithminite`，不是按模糊中文名称推定高低。LuV保留神经处理单元，因此前一批生物线、无菌洁净室和培养材料仍有作用。ZPM不能再用IV电压直接得到；UV不能再在普通组装机跳过研究造出。

## 4. 后期珍珠供应

只把注魔祭坛变成并行机器不能解决 Boss 掉落材料瓶颈。因此新增**独立的晚期工业替代**，原始掉落与附属配方不删除：

- 设备：工业注魔；电压 `VA[LuV]`；耗时 1200 tick；产出原始珍珠×1。
- 实物：下界之星×1、平衡碎片×4、以太碎片×2，全部消耗。
- 流体：praecantatio / auram / alienis / vacuos 各32点，即各4608mB。
- 机主必须持有 `PRIMPEARL` 研究；只缓存该机主已在线验证的研究供离线继续生产。无机主/新机主未验证/非法键不放行，拆机掉落不携带授权。
- 配方：`pollution:industrial_infusion_recipes/industrial_infusion/thaumic/primordial_pearl_synthesis`。

这不是免费复制，也不是拿一颗珍珠永远循环；每颗都有能源、材料与源质投入。adaminite、mithminite、创造碎片继续照原配方消耗珍珠。并行仓与超频提供后期产能。

## 5. 工业转换规则与本轮修复

- 仅转换白名单的 infusion / crucible / arcane_shaped / arcane_shapeless；常规转换HV起，时间 `max(100, 总要素×5)`。
- 遍历 Forge 模组资源文件系统，兼容内嵌 jar；不再对虚拟路径直接 `new ZipFile(...)`。
- 每个有序合成格都计数；相同符号出现四次就消耗四份，而非按 key 只算一次。
- 流体换算只进行一次：1点源质=144mB，1点vis=36mB。旧转换代码的重复×144已去除。
- 工业模板2～4保留中心模板；旧代码漏掉中心模板会绕过前级供应。
- 遇到不存在的实物、特殊自定义 Ingredient、NBT、特殊产物变换、不支持的研究格式，跳过整条并记录原因，禁止静默删输入。
- 白名单可通过 `EXTRA_THAUMIC_INDUSTRIAL_WHITELIST` 扩展，但必须先检查转换边界与守恒。
- 配方条数取决于模组组合，不能把最小测试服19条或正式服20条当固定验收目标。验收逐条看配方内容和可执行性。

## 6. 维护与验证

源码：`H:/MinecraftMods/Pollution-Unofficial-1.20.1/src/main/java/meowmel/pollution/loaders/recipes/` 下 `ThaumicCircuitRecipes`、`ThaumicIndustrialRecipes`、`ThaumicRecipeData`。

| 修改项 | 必须同步 |
|---|---|
| 模板 | 祭坛原配方与工业孪生、数量测试、任务描述 |
| 电路阶级 | GT运行时参考、机器/研究条件、标签、生成器文案 |
| 转换规则 | 源质/vis单测、重复符号单测、缺失输入拒绝测试、运行时dump |
| 发布 | jar SHA256、服务端差分包、客户端同版要求、旧jar删除清单 |

2026-11-04：Pollution `test build` 成功，11项单测通过，其中5项覆盖本轮转换规则。完整服机器运行、研究正反例和长期产能尚待 [第四批验收](PHASE4_ACCEPTANCE.md)，不能用此构建结果替代。

任务生成流程：`build_thaumic_industry_chapter.py --verify-repeat` → 生成 → `--check`。本轮20个任务业务键与ID保持不变。
