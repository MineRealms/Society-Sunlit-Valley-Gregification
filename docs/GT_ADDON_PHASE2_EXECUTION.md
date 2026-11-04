# GT附属第二批：详细执行记录

> **2026-11-04 第四批更正**：第二批历史验收仍有效，但用户提供的正式服快照没有加载SunlitIndustryCompat。第四批以0.2.0修正遗漏并补VintageDelight酿造；完整服复验与部署状态另记，不把旧测试通过当成生产已部署。 [PHASE4_ACCEPTANCE.md](PHASE4_ACCEPTANCE.md)。

> 批次目标：GCYR燃料语义/缓存/小数耗油、GTNN三台实用设备、GTMFO培养原料及明胶回收。
> **当前状态（2026-11-04）：已在隔离emoney测试服完成验收，候选交付见 `H:/MinecraftMods/dist/gt-addon-phase2-validated`。** 未部署生产服、未发布更新器；第9节列出未覆盖项。
> 范围：UV以内主体、少量UHV收尾；不做UEV～MAX。不得自动发布更新器或操作生产服。

## 1. 工程与部署边界

- 兼容mod新工程：`H:/MinecraftMods/SunlitIndustryCompat`，Forge1.20.1 / Java17，modid `sunlitindustry`。
- 本地测试服：`G:/emoney-bio-test`，沿用第一批已验证19mod闭包，增加兼容mod成为20个顶层jar。
- 主包脚本：`kubejs/server_scripts/gcyr/{fixRocketFuels,gtnnLinks,mekLinks}.js` 和 `bio/foodByproductRecovery.js`。
- 测试结果计划目录：`G:/emoney-bio-test/phase2-reports`；未得到新dump之前不得引用旧报告验收。
- 第一批产物 `dist/bio-phase1-validated` 保持不动，本批独立交付。

## 2. 执行清单

| 编号 | 内容 | 状态 | 实测结果 |
|---|---|---|---|
| A1 | GCYR EUt→发动机等级修正 | **通过** | 11种燃料各仅1条定义，运行时tier=1/2/3符合下表 |
| A2 | 每台火箭独立校验燃料 | **通过** | 11燃料×3档×低→高/高→低共66个真实油箱用例 |
| A3 | 小数耗油、存档与重载 | **通过** | MHN单推进器300次付200mB；NBT恢复信用；`minecraft:reload`后改用新配方对象 |
| B1 | 化工厂工艺与壳等级 | **通过（条件级）** | 铝壳(3)拒绝、不锈钢壳(4)接受RP-1混合；MV机器壳拒绝HV配方；控制器原料一层可达 |
| B2 | HV脱水机及回收用途 | **通过** | 明胶回收、湿溴→溴、脱溴水→盐水均在HV机实际产出；MV脱水机拒绝明胶回收 |
| B3 | EV火箭发电机 | **通过（附发现）** | 4mB混合RP-1实测3tick、6144EU；标称80%效率在此短配方上未生效 |
| C1 | 复用GTMFO肉粉/污泥链 | **通过（配方级）** | 碎肉研磨在HV研磨机实际产出；污泥→生物质原方完整保留（大型化反未实跑） |
| D1 | 同批冷启动/探针/交付 | **通过** | 第二批7项探针同进程通过；第一批6组探针/38断言回归通过；正常save/stop |

## 3. Mixin明细

### 3.1 为什么需要代码兼容

出货GCYR0.2.9 `RocketEntity` 存在三个机制问题：

1. 油箱validator通过静态 `FUEL_CACHE<Fluid,Boolean>` 缓存，但计算捕获当前火箭的 `motorTier`；同一流体在不同发动机间互相影响。
2. contents callback中的 `selectedFuelRecipe` 更新主要按流体匹配，不保证重新验证等级、重载后的对象和duration。
3. `consumeFuel` 把连续耗量直接转int，低于1mB的需求变成0，影响推进与支付；存档仍可能带旧配方ID及duration。

只改KubeJS配方EUt不能修这三项，因此以独立兼容mod补齐，不把火箭代码塞进Pollution。

### 3.2 目标与签名

目标：`argent_matter.gcyr.common.entity.RocketEntity`，锁定GCYR **0.2.9**，编译GT **7.5.3**。

| 接入点 | 注入位置 | 改动 |
|---|---|---|
| `<init>` | RETURN | 替换fuelTank validator，按当前火箭tier/服务端实时配方表校验，不用全局fluid布尔缓存 |
| `lambda$new$9` | TAIL | 保留原油量同步，随后刷新合法的selectedFuelRecipe和duration |
| `consumeFuel` | HEAD可取消 | 服务端重新校验、按原连续公式计算需求、预付小数耗油；不调用旧int截断逻辑 |
| `readAdditionalSaveData` / SRG `m_7378_` | TAIL | 恢复已付燃料信用，丢弃旧selected recipe对象/duration，恢复油箱容量 |
| `addAdditionalSaveData` / SRG `m_7380_` | TAIL | 写入兼容mod自己的两个NBT键 |

NBT新增键：`sunlitindustry.fuelCredit`、`sunlitindustry.creditFluid`。不改实体ID、物品注册、火箭构造数据；缺字段视为0信用。非有限、负数或≥1的信用视为无效，不能从坏NBT凭空多飞。

`@Pseudo`＋插件按加载列表判断gcyr存在；未装GCYR时不应用其Mixin。兼容类不应在无gcyr环境被主动初始化。注入签名与锁定版本绑定，升级GCYR必须重新验证，不能设成全部静默失败。

### 3.3 耗油定义

保留原连续需求：

```
需求 = 2 × (推进器数 + max(1,目标维度等级)) / (duration/20 + 1)
```

- `duration`不是“每mB一定燃烧duration个tick”；其用途由上述GCYR公式决定。
- 本批使用**预付信用**，不是允许欠费：首次不足1mB时先扣1mB，剩余小数信用留给下一tick。
- 总实际扣量减剩余信用应等于累计需求（允许浮点误差）；整份不足时拒绝，不扣掉仅有的半份再假装成功。
- 油箱已经空但仍有已付信用，可按原流体/合法配方消费信用；信用也不足则停止。
- 更换燃料不能把旧燃料信用折算成新燃料；切换时旧信用不转移，损失最多不足1mB，不生成额外燃料。
- 配方重载后校验活对象，旧选方不能永久绕过新tier或使用旧duration。
- 客户端维持原视觉逻辑，服务端拥有扣费权。真实网络飞行视觉仍需另行客户端验证，不以服务端探针代替。

## 4. 燃料数据矩阵

引擎tier BASIC/ADVANCED/ELITE=1/2/3；GT原电压映射将1、2、3EUt都视为ULV=0。

| 燃料 | 最低发动机tier | EUt编码 | duration |
|---|---:|---:|---:|
| GT汽油 | 1 | 32 | 25 |
| GT柴油 | 1 | 32 | 18 |
| GT火箭燃料 | 1 | 32 | 75 |
| GT氢 / 可选Mek氢 | 1 | 32 | 10 |
| GTNN RP-1 | 1 | 32 | 50 |
| GTNN浓肼 | 2 | 128 | 60 |
| GTNN UDMH | 2 | 128 | 90 |
| GTNN MHN | 3 | 512 | 100 |
| GT氢等离子 | 3 | 512 | 18 |
| Pollution焚天烈焰推进剂 | 2 | 128 | 80 |
| Pollution龙脉星轨燃剂 | 3 | 512 | 160 |

这是燃料等级元数据，不表示火箭要接EU电源。运行时必须反算并核对，不只看表格。

Pollution两种魔法推进剂原注册无EUt（=ULV，任何基础火箭可用），而燃烧duration 80/160优于GT火箭燃料75。按最早可生产阶段设门槛：焚天烈焰（HV产出）→先进，龙脉星轨（IV产出）→精英；duration保持原值，只在整合包KubeJS中重定义，不改Pollution jar。

GCYR原同流体默认定义移除并重建，KJS既有ID尽量保留。缺Mek时只跳过Mek条目，不安装一整套无关依赖，也不注册空流体配方。

## 5. 三台设备与工艺卡

### 化工厂 `gtnn:exxonmobil_chemical_plant`

类型 `gtceu:chemical_plant`。控制器使用MV外壳、退火铜板、聚乙烯大管、铝齿轮、BlackMatter框架和黑钢；内部机器壳与厂壳共同限制可执行配方。

本批重点：BlackMatter材料→控制器/壳体→RP-1精制与混合→发电或航天燃料。RP-1混合原方氧2000＋精制RP-1 500→混合RP-1 1000、HV、300t、不锈钢厂壳条件。控制器是MV配方不等于MV就能跑所有工艺。

### HV脱水机 `gtnn:hv_dehydrator`

类型 `gtceu:dehydrator`。控制器HV电路/机壳/机械臂、琥珀金细线、银线缆、钾铜合金齿轮等原投入保留。

原用途：湿溴1000→溴1000、脱溴水1000→盐水100，360EUt/80t。碘浆1200→碘粉1需要1280EUt，因此不是HV用例。大型脱水机后置，不加新早期旁路。

新增用途：食品明胶溶液回收，见下一节。

### EV火箭发电机 `gtnn:ev_rocket_engine`

类型 `gtceu:rocket_engine`。需要EV活塞/电机/电路/外壳及钨钢齿轮，不能宣传“刚进EV即可造”。

原发电配方EUt是负数，这和GCYR的正EUt等级元数据不是同一规则。源码效率逻辑写的是 `duration * efficiency / 100`（EV=80%），**但实测4mB混合RP-1在EV机上调整后仍为3tick、产6144EU（=1536EU/mB），标称效率在这条短配方上没有体现**。玩家收益以实测为准，不按80%宣传；本批不改GTNN发电数值。新增航天燃料等级不改变这段发电收益。

## 6. 食品、生物化工与新增回收

### 原链复用，不新增更便宜重复方

- GTMFO碎肉8→肉粉10＋原副产（小骨粉/动物脂肪），再接原GT培养基。
- 原食品污泥24000＋细菌1000＋方解石3＋非消耗碳网/电路2→生物质10000等流体，后接GT无菌菌液链。
- 低阶研磨机输出槽不足时实际副产少于配方全表，经济收益按真实机器输出计，不把所有概率副产都当必得。
- 不把食品污泥等价菌液，不把食用明胶等价GT工业明胶，不跳过胶原/琼脂/无菌流程。

### 新增 `foodByproductRecovery.js`

- 原方：食用明胶8＋水1000→`gtceu:gelatin_solution`1000，480EUt/200t。
- 新方：溶液1000→`gtmfo:gelatin`8，GTNN脱水机480EUt/400t。
- 水不返还，往返耗EU且不增加固体数量；不新增任何卖价、金币输出或清污染效果。
- 验收前核对真实流体ID、是否已存在同类回收，防止重复配方。

## 7. 运行时验收步骤

1. 备份测试服上批jar与脚本，确认没有运行进程后替换；不改生产目录。
2. 冷启动：核对sunlitindustry加载、Mixin应用、8+脚本注册无新错误。独立AS等已有告警不冒称已修。
3. Dump最终燃料与设备配方：ID/类型、EUt及tier、duration、流体、条件、控制器与关键原料来源。
4. 每种燃料×三档真实RocketEntity油箱：低→高、高→低，确保不同实体不串缓存；装/拆发动机、NBT恢复、重载也复查。
5. 分数耗油：300次同步consume、最后不足、空箱、更换燃料、NBT信用恢复；记录实际扣量，不能仅单测。
6. 脱水回收实际HV加工，MV拒绝；原明胶溶解方仍在，循环不增殖。
7. 化工厂/火箭发电机按真实部件与RecipeLogic运行至少一条工艺，壳条件负例，净EU按实际计。
8. 复用并回归第一批6组探针/38项断言。
9. 所有结果写新报告；失败修复后重新dump，禁止拿旧PASS或“加载脚本无报错”替代执行成功。
10. 正常保存停服。候选交付含jar、delta、源diff、SHA和复跑命令；正式全量整合包/客户端飞行/长期吞吐仍单列。

## 8. 回滚和上线边界

- 本批只在本地emoney测试服部署。主包脚本可编辑，但生产同步/更新器发布另行授权。
- 兼容mod不新增物品/实体注册，新增NBT仅记录不足1mB的已付信用。移除mod会失去这部分信用且回到原缓存/截断问题；回滚须停服、备份，并恢复配套燃料脚本，不能只拆一半。
- 新食品回收配方使用独立ID，移除不破坏原食品或培养路线。
- 不重置玩家研究、机器、阶段或已有任务ID，不生成免费控制器掩盖断链。
- 后续FTBQ新增章节未纳入本批完成标准；本批先给出可验证工艺卡和配方证据。

## 9. 实测记录与未覆盖项

### 9.1 报告文件（`G:/emoney-bio-test/phase2-reports/`）

- `runtime-recipes.json`：155条相关配方（燃料、化工厂、脱水、食品、发电）的输入输出、tier、条件。
- `rocket-probe.json`、`plant-fuel-probe.json`（含完整燃料表）、`equipment-probe.json`、`controller-reachability.json`。
- `phase2-probes.json` / `final-probes.txt`：7项探针同进程原始结果，含重载前后对比。
- 第一批回归：`bio-reports/` 下6组探针及38项断言，本批进程内重跑。
- 复跑：`python -I H:/MinecraftMods/SunlitIndustryCompat/tools/phase2/run_phase2_probes.py`（仅连本机测试服）。

### 9.2 过程中发现并处理的问题

- Pollution魔法推进剂无等级（见第4节）——已在燃料表中加门槛。
- **Mohist下 `reload` 是被拒绝的Bukkit插件重载，什么都不做**；配方热重载必须用 `minecraft:reload`。第一次重载测试因此无效，已改命令重测通过。
- EV火箭发电机效率与源码标称不符（见第5节）——仅记录，未改数值。

### 9.3 未覆盖、不得宣称已验收

- 真实发射/飞行/跨维度：油箱、耗油、存档用真实RocketEntity逐项调用，未在世界里组装火箭起飞，未开客户端看视觉。
- 化工厂只验证厂壳条件与机器壳电压门槛，未搭建完整多方块运行一次RP-1混合。
- 食品污泥→生物质在大型化反上未实跑；控制器可达性只查一层配方，未逐层追到矿物。
- Mek氢燃料分支：测试服无Mekanism，只做了守卫静态检查。
- 完整整合包（Connector/中州等400+mod）组合未回归；本批测试闭包为20个顶层mod。
- `lambda$new$9` 是GCYR 0.2.9编译器生成名，升级GCYR必须重新核对注入点。
