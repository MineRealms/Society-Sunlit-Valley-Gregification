# Sunlit Valley 研究线规划（2026-11-03，历史初稿）

> **已被同日后续复核取代，不可直接按本文实施。**
>
> - 当前生物线规格与证据：[BIO_LINE_PLAN.md](BIO_LINE_PLAN.md)。
> - 当前GT附属范围与验证方案：[GT_ADDON_LINE_PLAN.md](GT_ADDON_LINE_PLAN.md)。
> - 包主最终范围：**主体做到UV，少量UHV可选收尾；不规划UEV～MAX。**
> - 本文旧版“干细胞ZPM”“全程无菌房”“血肉链串联”“治疗缸现成净化工业污染”“活体配方无JSON”等结论已纠正。
> - GTNN高阶电路tag存在不代表生产可达；六原始源质转换还发现放大链和输出记账疑点，须先复核修复。
> - 下方记录保留供追溯，含旧20748/TH版本和当时服务器状态；不能当作当前20759/TH1.0.5的运行时验收。

两条独立推进的深度研究线：**生物线**（TC4/TH × Pollution × GT 湿件）与 **GT 附属线**（GTCEu 生态）。
分析基于四个并行 subagent 的只读 jar 审计（gtceu 7.5.3 / thaumcraft 20748 / isorropia / pollution / gcyr / gtnn / gtmfo），
所有配方级结论均为字节码+JSON 证据，**尚未运行时验证**（服务器宕机中）。

---

## 一、GT 湿件线 = "生物电路"（两条线的共同锚点）

`wetware_processor`（LuV）→ assembly（ZPM）→ computer（UV）→ mainframe（UHV），**唯一通到 UHV 的电路家族**。

### GT 自带生物链（GrowthMediumRecipes.class / CircuitRecipes.class 字节码核实）

- 生物质入口：植物球→研磨→生物糠；酿造(生物糠+蒸馏水)=细菌；肉粉→胶原→明胶→琼脂
- 培养链：细菌→浆液→富集浆液(铀曝射)→诱变剂→原始生长培养基→流体加热=**无菌生长培养基**（全程无菌超净间）
- 智慧链：**干细胞** = Osmiridium 粉+细菌+无菌培养基（ZPM 洁净室）；湿件基板 = 多层纤维板×16+**培养皿**+铌钛箔×16+无菌培养基 4000L →×16；印刷板+**干细胞×16**→`neuro_processing_unit`；NPU+晶体CPU+纳米CPU→wetware_processor×2
- 关键物品 id：`gtceu:wetware_circuit_board` / `wetware_printed_circuit_board` / `wetware_processor` / `wetware_processor_assembly` / `wetware_processor_computer` / `wetware_processor_mainframe` / `neuro_processing_unit` / `stem_cells` / `petri_dish` / `bio_chaff`
- GT **没有克隆/培养机器**——"生物"输入全是化学品/流体形态

## 二、线一：生物线（TC4 / TH(Isorropia) × Pollution × GT 湿件）

### 核心发现：Pollution 已自建同构血肉计算链（直接消费 TC 物品）

```
腐肉+生物质 → pollution:primitive_meat 原始血肉团（化学釜）
  → +thaumcraft:zombie_brain +无菌繁殖介质 → pollution:rat_brain 鼠脑
  → +灌注·能 → pollution:mitochondrion_power 线粒能源体
  → 内啡肽稳定器 → 溶酶体稳定器 → 冷冻器（各化学釜）
  → +thaumcraft:brain_jar +灌注·物灵/生 → pollution:ips_human_brain iPS重建人脑
  → blood_circuit_advanced 神经分化模板
```

与 GT 湿件**共用 `GTMaterials.SterileGrowthMedium` 流体**；40+ TC 要素已流体化
（`infused_life/humanus/aura/energy/taint...`）——TC↔GT 通用媒介。

### TC4R / TH 脑素材三级链（两 jar 内已打通）

`thaumcraft:zombie_brain`（brainy_zombie 10%+掠夺）
→ 注魔 `thaumcraft:brain_jar`（research JARBRAIN，吸经验，容量 2000）
→ TH 注魔 `isorropia:somatic_brain`（research isorropia:somaticbrain，活体脑饰品）

TH(Isorropia, fr.wind_blade.isorropia) 其他：Curative Vat 多方块（victus 治伤/净化咒波）、
20 种活体注魔、复活换体线（corpse_effigy→soul_beacon）、特殊生物群
（**ore_pig 吃石头产矿**、golden_chicken、scholar_chicken、chromatic_sheep）、
vis/essentia 发电机、Jar of Souls。注意：老 TH 的羊克隆/兽化人未原样出现；
活体注魔配方走代码不走 JSON（有 HorizonsKubePlugin 钩子）。

### 联动候选（按性价比排序）

1. **Pollution 生物部件 ⇄ GT 湿件互供**：KubeJS alternate 配方（ips_human_brain/rat_brain 参与湿件基板或 NPU，双倍产出激励）
2. **somatic_brain 作湿件魔法输入**：替代部分干细胞，神秘侧深度绑定
3. **TH 生物农场端**：ore_pig/golden_chicken 自动化原料 + Curative Vat × Pollution 净化联动（现成机制）
4. **blood_circuit（13 档 MV..MAX）补挂电路 tag**：agent 未找到其合成配方（仅作输入消费），待运行时确认是否已在 circuits/* tag
5. **要素流体统一媒介**：后续生物/魔法配方一律用 `infused_*` 流体做中间体

## 三、线二：GT 附属线

| Mod | 身份（证据） | 内容 | 定位 |
|---|---|---|---|
| **gtnn "GT--"** (Arborsm) | 29 mixin 深改 GTCEu/原版 | 化工厂/大型脱水机/naquadah 反应堆/中子活化器(独立物理系统)/电路+元件装配线；**UEV→OpV→MAX 电路树**(optical/gooware/cosmic/etched crystal)；Botania 材料(manasteel/elementium/terrasteel)+Create 材料已注册进 GT | **主菜**；gooware(生物胶质)电路是两线交点 |
| **gcyr** | Gregicality Rocketry (Argent-Matter) | 11 维度(水星→比邻星)、火箭组装/发射、戴森球、太空电梯、23 航天材料、卫星 | 纯太空线，无生物/魔法，后期独立推 |
| **gtmfo** | GregTech Modern Food Options | 食品化学(香兰素/干酪系)+**药物线**(锂盐/可待因/吩噻嗪系)、italian_buffalo、SereneSeasons 四季兼容 | 与包内四季+当铺经济(食物卖钱)亲和 |
| GTCEu 兼容层 | 344 类 integration | **AE2 内容级最深**(~60 类)、CC:Tweaked、Create… | TE/MAE2 章节已在使用 |

**风险**：gtnn 的 29 mixin（含 MinecraftServerMixin/GTRecipeTypeMixin）在 Mohist+Connector 环境是最大不确定性，先 DEV 验证再设计配方；gcyr 11 维度拖世界生成。

## 四、边界与验证

- 边界：生物线不动附属机器，附属线不碰 TC 内容；唯一共享媒介是 Pollution 要素流体
- 待运行时验证清单：① blood_circuit 的 circuits/* tag 归属 ② gtnn mixin 在 Mohist/Connector 稳定性
  ③ Pollution GTAddon 配方在生产服正确生成 ④ 湿件链在生产服 EUt/洁净室行为

---

## 附：包状态更新（2026-11-03）

- **HV-EV 电路魔法替代配方已撤销**（当日实施当日撤销，包主决定）：gtMagicCircuits.js 已删（4 端）、
  aspect_bridge 章节回到 6 题（ID 不变）、README 7c/TC4_INTEGRATION.md §9.4 已回滚记录；
  SHA256SUMS 49 条、zip 2,403,041 B。
- **KubeJS 启动脚本 CROP 冲突已解决**（无需再改）：meTrades.js:16 已用 `let ME_CROP`，
  tfTrades.js:22 的 `const CROP` 现为全 startup_scripts 唯一声明；latest.log（11-03 12:56 run）
  两脚本正常加载、KubeJS 错误 0 条。
- **HUD 现状**（sunlithud-0.2.0）：两块面板——左上 `sunlit_status`（天数/季节/五项营养条/扭曲/光照/污染，
  数据源 day·season·nutrient.*·warp.total·light·pollution）+ 左下 `sunlitmarket`（余额/结盟/通缉，
  SunlitHud.provider 脚本注册）。**注意**：sunlitHud.js 目前只在 -DEV 实例，主实例仅有 svHud.js
  （左下面板），需要时同步过去。行类型 text/bar，支持 hideBelow/hideAbove/anchor/scale，/reload 热生效。
