# 第三批总结：从魔法到科技

> **2026-11-04 第四批更正**：第三批历史记录。高阶电路、工业孪生、换算错误和遗漏部署项已由第四批修订；下面的旧数值和“全部完成”判断不可直接作为现状。 [PHASE4_ACCEPTANCE.md](PHASE4_ACCEPTANCE.md)。

> 时间：2026-11-03 ~ 2026-11-04。范围：源质估值、神秘电路、工业注魔、生物湿件、
> 六章任务与 kubejs 补交。**主体到 UV，少量 UHV 选修，不规划 UEV~MAX。**
> 详细规则见 [THAUMIC_CIRCUITS.md](THAUMIC_CIRCUITS.md)、[MAGIC_GT_SCALING.md](MAGIC_GT_SCALING.md)、
> [BIO_LINE_IMPLEMENTATION.md](BIO_LINE_IMPLEMENTATION.md)。

## 0. 一句话

把「魔法素材」变成「可估值的工业原料」：先统一源质换算与材料要素表（地基），
再用四块祭坛模板把魔法接进 GT 电路梯（桥），然后用工业注魔把 TC 配方批量工业化
（产能），最后让生物线给湿件电路供料（第二个来源）——每一步都保留了原版路线。

```
L0 地基   材料要素表（5,965 条） + 源质估值（1 点 = 144mB = 1 元素粉）
            ↓
L1 桥     祭坛模板 1/2/3/4  →  奥术电路 MV · HV · EV · IV · LuV · ZPM · UV
            ↓                          ↘ 写进 gtceu:circuits/mv..uv 标签
L2 产能   工业注魔多方块（19 条 TC 配方 → GT 配方，并行仓 + 超频）
            ↓
L3 生物   血肉→肉粉→培养基→iPS 脑→干细胞→湿件基板→NPU→UV（与原版 GT 链并行）
            ↓
L4 引导   生物湿件章 / 神秘工业章 / 贸易章 / 要素桥 / AE2 附属 / 中州 / 太空
```

## 1. L0 地基：让魔法素材有「价」

| 项目 | 结果 |
|---|---|
| 材料要素表 | 离线数据包 `data/pollution/thaumcraft/object_aspects/`，`direct` **5,965 条** + gtnn/gcyr/gtmfo 三张附属表 |
| 为什么离线 | 运行时 `registerRuntime` 是 O(条目×物品)，1.5 万物品会卡死启动 |
| 路径铁律 | 必须在**自己 mod 的命名空间**下；放 `data/thaumcraft/object_aspects/` 会被静默忽略 |
| 条件 schema | `{"type":"forge:mod_loaded","modid":...}`；NeoForge 写法会崩启动 |
| 源质估值 | 1 点 = 144mB 对应流体 = 1 个本模组元素粉/宝石（六原始闭环） |
| 守恒审计 | 4,118 → 2,883 个 flag，修复 2,244 条；残余 9 条均为有界单次放大 |
| 关键改法 | 单主导要素 + 精确 unit 缩放（GT 宝石梯双向：flawless 2 / exquisite 4） |
| 不再产 TC 晶簇 | 晶簇放置/破坏可得多个碎片，会绕过多点赋值；改产 Pollution 自身元素宝石 |

## 2. L1 桥：祭坛 → 电路

**四块模板**（17 个血魔法遗留 ID 保留、改神秘主题）

| 模板 | 产物 | 做法 | 要素 / vis |
|---|---|---|---|
| 1 | 基础血电路 | 奥术工作台 `TQT` / ` B ` | vis 气 16 + 秩序 8 |
| 2 | 进阶血电路 | 注魔（不稳定度 3） | 源质16 / 金属8 / 虚空8 |
| 3 | 终极血电路 | 注魔（不稳定度 5） | 源质24 / 异界16 / 金属12 |
| 4 | 至尊血电路 | 注魔（不稳定度 8） | 源质32 / 异界24 / 灵气24 |

**七级电路**（电路组装机，`pollution:assembler/thaumic_circuit/0..6`）

| 级 | 模板 | 神秘金属 | 功率 | 时长 | 产出 | 洁净室 |
|---|---|---|---|---|---|---|
| MV | 1 | 神秘锭 | 60 | 200t | 2 | 否 |
| HV | 1 | 水晶精华 | 600 | 200t | 2 | 是 |
| EV | 2 | 虚空锭 | 2400 | 200t | 2 | 是 |
| IV | 2 | 秘银 | 9600 | 200t | 2 | 是 |
| LuV | 3 | adaminite | 38400 | 200t | 2 | 是 |
| ZPM | 3 | 秘银锂 | 7680 | 800t | 1 | 是 |
| UV | 4 | 灵液 | 30720 | 800t | 1 | 否 |

- 全部写进 `gtceu:circuits/mv..uv` 标签：**可替代**，不是自动替换，原版电路一直有效。
- `.7`~`.12`（UHV~MAX）退役：无配方、无标签、JEI 隐藏，只保留 ID 防老存档丢物品。

**本批修掉的阻断缺陷**（Pollution `15d35f6`）：模板 1 的产物写成了神秘锭、
`vis` 用了复合要素 `auram` → TC4R 静默丢弃配方，`pollution:blood_circuit`
全包 0 个产出源，整条链断。修复后运行时确认 `result=1 blood_circuit, vis={ORDO=8, AER=16}`。

## 3. L2 产能：工业注魔

| 规则 | 数值 |
|---|---|
| 转换来源 | TC 的 `infusion` / `crucible` / `arcane_shaped` 配方 JSON |
| 白名单 | 16 个产物 id（神秘锭、虚空锭、水银、平衡碎片、水晶精华、原始珍珠、盐、秘银系、影金、创造碎片、以太碎片、灵液） |
| 要素 → 流体 | 每点 **144mB**；奥术 vis 每点 **36mB** |
| 功率 / 时长 | HV 档 EUt；`max(100, 要素总量 × 5)` tick |
| 门槛 | 原研究键写入配方属性，机主必须持有该研究 |
| 不转 | 附魔、法杖装配、生物注魔；NBT、未映射要素、>8 流体、>25 物品 |
| 实际注册 | **19 条**（16 条模组 JSON + 3 条代码孪生模板），扫描 16/16 转换、0 跳过 |

手工祭坛全部保留：工业注魔是产能杠杆，不是解锁门槛。

## 4. L3 生物：第二个来源

| 环节 | 配方 | 参数 |
|---|---|---|
| 原始血肉 | 腐肉 4 + 生物质 500mB → 2 | 30 EU/t、100t |
| 肉粉 | 1 原始血肉 → 1 肉粉 | 2 EU/t、102t |
| 鼠脑 | 僵尸脑 + 原始血肉 + 250mB 无菌培养基 | 120 EU/t、200t |
| 原始培养基 | 肉粉4 + 盐4 + 钙4 + 琼脂4 + 诱变剂 4000mB → 4000mB | 7680 EU/t、1200t、**无菌** |
| 无菌培养基 | 100mB → 100mB | 7680 EU/t、20t、**无菌** |
| iPS 脑（首件） | 2 鼠脑 + 脑缸 + 500 人类 + 1000 生命 + 1000 无菌 | 30720 EU/t、1600t、**无菌** |
| 催化干细胞 | 4 小锇铱粉 + 不消耗 iPS 脑 + 500 细菌 + 500 无菌 → 32 干细胞 | 30720 EU/t、**240t**（原方 300t） |
| 湿件基板 | 16 多层纤维板 + 培养皿 + LuV 泵 + IV 传感器 + IV 电路 + 16 铌钛箔 + 4000 无菌 → 16 | 30720 EU/t、1200t、普通洁净室 |

- 首件配方解决的是**自举死循环**：原 iPS 脑走魔导组装机，而魔导组装机的控制组件本身要 iPS 脑。
- 脑不消耗：造一枚要 1500mB 培养基 + 800t 起步工时，按批消耗换 60t 提速永远回不了本。
- 湿件链后续（NPU → UV 超级计算机 → UHV 主机选修）仍走 GT 原版，本批不重复。
- GTMFO 回收：废肉 8 → 10 肉粉 + 16 小骨粉 + 10 脂肪（20 EU/t、400t）；大化反 32 废肉 →
  32 肉粉 + 3500 硬脂酸 + 16000 污泥；污泥 24000 → 生物质 10000（30 EU/t、800t）；
  七种原料提取明胶；脱水机 1000mB 明胶溶液 → 8 明胶（有损）。

## 5. L4 引导：任务与经济

| 章节 | 任务 | 作用 |
|---|---|---|
| `thaumic_industry` | 20 | 模板 → 七级电路 → 标签 → 工业注魔 → 源质估值 |
| `bio_wetware` | 23 | 血肉 → 培养基 → iPS 脑 → 干细胞 → 湿件；回收；矿猪；躯体脑 |
| `trade` | 21 | 当铺五通道、行情、期货、结盟、债务 |
| `aspect_bridge` | 6 | 要素桥：扫视示例、GT 研磨桥、魔法变现 |
| `ae2_addons` | 15 | AE2 附属清单与用法 |
| `middle_earth` | 19 | 中州 onboarding / 派系 / 农业 |
| `space` | 30 | 燃料改三档（11 种），生成器加 `--check` / `--verify-repeat` |

全包现状：**62 章、6,013 个任务 id、0 跨文件重复**；六个生成器全部通过
`--check`（与已发布文件逐字节一致）与 `--verify-repeat`。

## 6. kubejs 侧

- 新增目录：`bio/`、`magic/`、`thaumadds/`、`isorropia/`、`me/`、`sunlitmarket/`、
  `startup_scripts/me/`、`client_scripts/tooltips/`，以及 `data/dialog/dialogs/sunlitmarket_*.json`
  与 `data/society/recipes/altar/`。
- 与魔法→科技直接相关的三处：
  - `bio/bioCultureBridges.js`：iPS 首件 / 催化干细胞 / 血肉→肉粉三条配方
  - `bio/foodByproductRecovery.js`：明胶返造（有损）
  - `magic/gtMagicBridge.js` + `thaumadds/thaumaddsFarmBridge.js`：魔法材料与 GT 加工互转
- 田园联动（`astral/gateAstralFarmBridge.js`、`tc/tcFarmBridge.js`、`botania/gateBotania.js`）
  在 2026-10-17 被一次文件级还原抹掉了任务文案，本批已把三章还原回 `99fb1bf` 状态，
  配方与文案重新一致。
- 全量语法检查：**370 个 .js，`node --check` 0 失败**。
- 上一次整包运行的 kubejs 统计：新增 2,349 条配方 / 移除 2,087 条 / 修改 17 条 / 失败 1 条；
  唯一失败是 `technom:compat/technoturge_core` 用了不存在的
  `gtceu:advanced_electronic_circuit`（应为 `advanced_integrated_circuit`），已修（`62aa4d5`）。

## 7. 验证矩阵

| 项目 | 验证方式 | 结论 |
|---|---|---|
| 源质估值 | 静态审计 + 生成器单测 8 项 | 通过，残余 9 条有界 |
| 要素表生效 | 运行时反射读 `ObjectAspectCatalog.direct` | 通过（修路径前曾完全失效） |
| 七级电路 | 运行时 recipe dump | 7 条全在，200t×5 / 800t×2 |
| 电路标签 | `ItemStack.is(tag)` 逐档 | 每档恰好含自身 `.N` |
| 模板 1~4 | 运行时 recipe dump | 模板 1 修复后加载；2/3/4 本来就在 |
| 工业注魔 | 启动日志 + recipe dump | 19 条，0 跳过 |
| 生物配方 | 隔离服 6 组探针 + 38 项断言 | 通过（详见 BIO_LINE_IMPLEMENTATION） |
| 任务章节 | 生成器 `--check` / `--verify-repeat` + 全局 ID 唯一性 | 通过 |
| kubejs | `node --check` 全量 + 上次运行日志 | 语法全过；1 条配方 id 已修，**未重跑整包确认** |

## 8. 未做 / 风险

- **主实例的 Pollution jar 仍是修复前版本**：模板 1 的修复只在测试服与
  `dist/thaumic-phase3-validated/`。上线必须停服换 jar。
- `technom` 配方修复**没有重跑整包验证**，只做了 id 存在性核对与语法检查。
- 洁净室用测试 fixture 验证条件判定，不等同实际成型；矿猪未跑长期产率统计。
- 未发布更新器、未同步 mirror、未动生产服。
- 工作区仍有未提交项：`mekanism` / `thaumic_addons` 两章与其生成器、若干游戏自写配置
  ——这些不是本批产物，提交前需单独确认。
