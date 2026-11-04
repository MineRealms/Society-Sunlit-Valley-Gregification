# 魔法 ↔ 工业的换算与守恒（源质 / 要素流体 / vis）

> 事实基线：2026-11-04。所有比例都来自源码常量与运行时 dump，
> 不是按叙事估算。配套：[THAUMIC_CIRCUITS.md](THAUMIC_CIRCUITS.md)、
> [BIO_LINE_IMPLEMENTATION.md](BIO_LINE_IMPLEMENTATION.md)。

## 1. 三种「魔法货币」

| 单位 | 存在形式 | 谁在用 |
|---|---|---|
| 源质（点） | TC4R 的 essentia，罐／管／蒸馏器 | 祭坛、注魔、源质炉、转换矩阵 |
| 要素流体（mB） | `pollution:infused_<aspect>` | GT 机器（化学反应釜、注魔多方块） |
| vis（点） | 奥术工作台／法杖的六原始通道 | `thaumcraft:arcane_shaped` 配方 |

关键区别：**vis 只有六个原始通道**（`aer/ignis/aqua/terra/ordo/perditio`），
源质与要素流体覆盖全部要素。把复合要素写进 `vis` 会让配方被静默丢弃。

## 2. 官方换算表

| 换算 | 数值 | 出处 |
|---|---|---|
| 源质 1 点 → 要素流体 | **144 mB** | `PollutionAspectMapping` / 转换矩阵 |
| 转换矩阵速度 | 每 10t 最多 1 点，不额外扣 EU | `InfusedExchangeMachine` |
| 奥术 vis 1 点 → 注魔流体 | **36 mB** | `ThaumicIndustrialRecipes.MB_PER_VIS_POINT` |
| 工业注魔要素 1 点 → 流体 | **144 mB** | `MB_PER_POINT` |
| 六原始闭环 | 1 点 = 144mB = 1 个本模组元素粉／宝石 | Phase 1 统一 |

「六原始」= 气/火/水/地/秩序/熵（`aer/ignis/aqua/terra/ordo/perditio`）。
复合要素不在统一赋值范围内，不要假设它们也守恒。

## 3. 为什么不再产出 TC 晶簇

旧链是「144mB → 高压釜 → 1 个 `thaumcraft:<element>_crystal_cluster` → 粉碎 → 粉」。
问题在于晶簇**放置／破坏可得多个碎片**，等于给 1 点源质加了一个乘法出口。

现在：高压釜返造保持原配方 ID 与 144mB 投入，但输出改为 Pollution 自身的元素宝石；
原生 TC 晶簇照常存在、照常可用，只是不再由流体回造。老存档里的晶簇方块不动。

## 4. 材料要素表（数据包）

路径铁律：

```
data/<自己的 modid>/thaumcraft/object_aspects/*.json     ← 正确
data/thaumcraft/object_aspects/*.json                    ← 静默忽略，不报错
```

TC4R 自己的表在 `data/thaumcraft/thaumcraft/object_aspects/`（双重命名空间）。
本包的表在 `data/pollution/thaumcraft/object_aspects/`，当前 `direct` 共 **5,965 条**。

条件 schema 必须是 **Forge 1.20.1** 形式：

```json
{ "type": "forge:mod_loaded", "modid": "gtnn" }
```

写成 NeoForge 的 `{"condition":..., "values":[...]}` 会抛
`JsonSyntaxException: Missing type` 并**崩启动**。

## 5. 数值守恒的三条实测规则

1. **单主导要素 + 精确 unit 缩放**。GT 的宝石梯是双向的（切割 1 flawless → 2 gem；
   雕刻 2 flawless → 1 exquisite；提取档位 → 流体），多要素截断混合会在档位之间发散。
   生成器 `tools/phase3/gen_gt_aspects.py` 只保留主导要素，按 unit 精确缩放：
   `flawlessGem=2`、`exquisiteGem=4`、`block=9`、`rawOreBlock=9`、其余 = 1。
2. **显式 `{}` 安全，缺失不安全**。TC4R 的 `finishInference` 只对 `inferredEmpty` 重算，
   所以显式空表不会被推算覆盖；但 `resolveDerived` 会**无条件覆写** direct 值。
3. **有界放大可接受，无限循环不可接受**。Phase 3 审计 4,118 → 2,883 个 flag，
   修复 2,244 条；残余 9 条「有值输入」全部 triage 为 GT 配方颗粒度导致的有界单次放大
   （例如 1 锭 → 5 尘的余数），没有可重复闭环。

## 6. 源质炉记账

两台源质炉都必须满足：

```
本次生成总量 = 已成功送出量 + 机器保留待送量
```

- TC 源质炉按容器**实际接受量**扣减，同一批不会向每个罐各发一次完整产量。
- GT 源质炉遍历输出仓，余量按 mB 保存；17mB 这类零头不按整份截断。
- 满罐／满输出仓时保留 pending；结构失效时暂停而不是清空批次。
- 控制器 `saveCustomPersistedData/loadCustomPersistedData` 保存批次。

## 7. 不要做的事

- 不要把复合要素写进 `vis`（配方会被静默丢弃，构建不报错）。
- 不要把 `infused_*` 一概当成可守恒往返的源质：只有六原始要素做了统一赋值。
- 不要用「JEI 能搜到」代替「生存流程可制造」；也不要用「有配方 builder」代替
  「最终配方已加载」——模板 1 的 bug 就属于后一类。
- 不要为了平衡去改单边数字：改一边会破坏另一边的用途，先列正反兑换当量再定方案。
