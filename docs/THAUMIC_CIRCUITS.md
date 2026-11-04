# 神秘电路与工业注魔（Phase 3）

> 事实基线：2026-11-04。源码在 `H:/MinecraftMods/Pollution-Unofficial-1.20.1`
> （`loaders/recipes/ThaumicCircuitRecipes.java`、`ThaumicIndustrialRecipes.java`），
> 运行时证据来自 `G:/emoney-bio-test` 的 RecipeManager dump。
> 任务章节：`config/ftbquests/quests/chapters/thaumic_industry.snbt`（科技组，order 25，20 任务）。

## 1. 设计边界

- 工业主线做到 **UV**；`.7`~ `.12`（UHV~MAX）不规划，无配方、无标签、JEI 隐藏，只保留 ID 让老存档不丢物品。
- 17 个血魔法遗留 ID 全部保留（老存档的机器与物品不受影响），但语义改成神秘主题。
- 原版 GT 电路一个都没删：神秘电路是**并行来源**，靠标签与原版电路并列。

## 2. 四块模板（TC 侧）

| 模板 | 产物 | 做法 | 投入 | 要素 / vis | 不稳定度 |
|---|---|---|---|---|---|
| 1 | `pollution:blood_circuit` | 奥术工作台 `thaumcraft:arcane_shaped` | `TQT` / ` B `；T 神秘锭、Q 水银、B 基础集成电路 | vis 气 16 + 秩序 8 | — |
| 2 | `pollution:blood_circuit_advanced` | 注魔祭坛 | 中心 模板1 + 虚空锭 + 水晶精华×2 + 水银 | 源质16 / 金属8 / 虚空8 | 3 |
| 3 | `pollution:blood_circuit_ultimate` | 注魔祭坛 | 中心 模板2 + 秘银锭 + 影金锭 + 以太碎片×2 | 源质24 / 异界16 / 金属12 | 5 |
| 4 | `pollution:blood_circuit_supreme` | 注魔祭坛 | 中心 模板3 + 秘银锂 + 创造碎片 + 原始珍珠 | 源质32 / 异界24 / 灵气24 | 8 |

**坑（2026-11-04 实测）**：TC4R 的 `arcane_shaped` 只接受六个**原始 vis 通道**
（`aer/ignis/aqua/terra/ordo/perditio`）。vis 里写复合要素（如 `auram`）会抛
`Arcane recipe cost is not a vis channel: auram`，配方被**静默丢弃**——构建不报错，
只有服务器日志里有一行 KubeJS WARN。模板 1 曾因此整条链不可达，见 §5。

## 3. 七级神秘电路（GT 侧）

全部在 **电路组装机** 里做，配方 id `pollution:assembler/thaumic_circuit/0`~`6`。

| 级 | 产物 | 模板 | 神秘金属 | 基板 / 线材 / 框架 | 焊锡 | EU/t | 时长 | 产出 | 洁净室 |
|---|---|---|---|---|---|---|---|---|---|
| MV | `blood_circuit.0` | 1 | 神秘锭 | 塑料 PCB / 4 细红合金线 | 72 | 60 | 200t | 2 | 否 |
| HV | `blood_circuit.1` | 1 | 水晶精华 | 环氧 PCB / 8 细金银合金线 | 72 | 600 | 200t | 2 | 是 |
| EV | `blood_circuit.2` | 2 | 虚空锭 | 纤维增强 PCB / 12 细铂线 | 72 | 2400 | 200t | 2 | 是 |
| IV | `blood_circuit.3` | 2 | 秘银锭 | 多层纤维增强 PCB / 8 细铌钛线 | 72 | 9600 | 200t | 2 | 是 |
| LuV | `blood_circuit.4` | 3 | adaminite | — / 8 细钇钡铜氧线 | 72 | 38400 | 200t | 2 | 是 |
| ZPM | `blood_circuit.5` | 3 | 秘银锂 | — / 48 退火铜单线 / 2 HSS-G 框架 | 288 | 7680 | 800t | 1 | 是 |
| UV | `blood_circuit.6` | 4 | 灵液 | — / 8 铌钛单线 / 2 HSS-E 框架 | 1440 | 30720 | 800t | 1 | 否 |

「同级」的含义：电压、时长、产出数量都对齐原版 GT 同级电路配方，只把芯片／SMD 栈换成
模板 + 神秘金属。成本不优于原版，产出不多于原版。

### 标签

七个产物写进 `data/gtceu/tags/items/circuits/{mv,hv,ev,iv,luv,zpm,uv}.json`。
标签只影响**配方匹配**：写 `gtceu:circuits/mv` 的配方同时接受原版与神秘电路。
它是「可替代」，不是「自动替换」——原版路线一直有效。

## 4. 工业注魔（TC 配方 → GT 配方）

多方块 `pollution:industrial_infusion`，配方类型 `gtceu:industrial_infusion_recipes`。

转换规则：

- 只转**白名单产物**（默认 16 个 id；`EXTRA_THAUMIC_INDUSTRIAL_WHITELIST` 可追加）。
- 物品输入 = 原配方中心物／催化剂／组件；`tag` 转 tag ingredient；带 NBT 的跳过。
- 要素 → 对应注魔流体，**每点 144mB**；奥术 vis **每点 36mB**（灵气可再生，比源质便宜）。
- EUt 固定 **HV 档**；时长 = `max(100, 要素总量 × 5)` tick。
- 原研究键写进 `MagicRecipeProperties.THAUMCRAFT_RESEARCH`，机主必须持有该研究。
- 不转：附魔、法杖装配、生物注魔；未映射要素、流体种类 > 8、物品 > 25 的配方跳过并计数。
- 确定性 id：`pollution:industrial_infusion_recipes/industrial_infusion/thaumic/<ns>/<原路径>`。

### 已注册的 19 条（运行时 dump）

| 产物 | 时长 |
|---|---|
| 平衡碎片 ×6（气/火/水/地/秩序/熵） | 100t |
| 神秘锭 / 虚空锭 | 100t |
| 以太碎片 | 360t |
| 秘银锂 | 475t |
| 灵液注魔 | 640t |
| 秘银 | 1350t |
| 创造碎片 | 1650t |
| adaminite | 2150t |
| 灵液 | 3000t |
| 模板 2 / 3 / 4（代码孪生） | 160t / 260t / 400t |

启动日志会打印
`[thaumic-industrial] scan: 16 whitelisted TC recipes, 16 converted, skipped (...)`
与 `registered 19 industrial infusion recipes from TC JSONs`。**N 变小说明有配方被跳过**，
先看跳过计数再改白名单。

## 5. 验证记录与已修缺陷

运行时（2026-11-04，新 jar 部署后）：

- `pollution:arcane/blood_circuit_template_1` → `ArcaneRecipe`，
  `result = 1 blood_circuit`，`vis = {ORDO=8, AER=16}`，`research = Optional.empty`。
- `pollution:assembler/thaumic_circuit/0..6` 全部存在（200t×5、800t×2）。
- `pollution:infusion/blood_circuit_template_2..4` 全部存在。
- 工业注魔 19 条，扫描 16/16 转换、0 跳过。

修复的缺陷（Pollution `15d35f6`）：模板 1 原本

1. 产物写成 `thaumcraft:thaumium_ingot`（复制粘贴残留）；
2. `vis` 用了 `auram`（复合要素，不是 vis 通道）。

结果：配方被 TC4R 拒绝加载，而 `pollution:blood_circuit` 在全量 recipe manager 里
**0 个产出源**——模板 2/3/4 与 MV 电路全部断链。构建与单测都不会发现这类问题，
只能靠「配方是否真的加载」的运行时断言。

## 6. 维护

| 想改什么 | 改哪里 |
|---|---|
| 电路数值／材料 | `ThaumicCircuitRecipes.TierSpec`（每级一行） |
| 模板配方 | `ThaumicCircuitRecipes.templates()` |
| 工业注魔白名单 | `ThaumicIndustrialRecipes.DEFAULT_WHITELIST` 或配置项 |
| 任务文案／依赖 | `config/ftbquests/tools/build_thaumic_industry_chapter.py` |

生成器命令：

```
python config/ftbquests/tools/build_thaumic_industry_chapter.py --check
python config/ftbquests/tools/build_thaumic_industry_chapter.py --verify-repeat
python config/ftbquests/tools/build_thaumic_industry_chapter.py
```

**加一级电路必须同时**：改 TierSpec、确认金属在包里存在（缺物品时该级会被跳过并只留一行 WARN）、
补 `data/gtceu/tags/items/circuits/<tier>.json`、补任务。
