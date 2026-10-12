# 太空线整合（GCYR × Mekanism × GT--）实施文档

> 最后更新：2026-09-18
> 内容：太空任务章（30 任务）+ 火箭硬化（GT-- 重型合金）+ GCYR×Mek / GCYR×GT-- 联动
> 事实来源：`mods/gcyr-1.20.1-0.2.9.jar`、`mods/gtnn-1.20.1-1.3.10.jar`、`mods/Mekanism-1.20.1-10.4.16.80.jar`（CFR/javap 反编译 + 数据文件核对）

---

## 1. 太空任务章（space.snbt）

| 项 | 值 |
|---|---|
| 文件 | `config/ftbquests/quests/chapters/space.snbt` |
| 生成器 | `config/ftbquests/tools/build_space_chapter.py`（固定种子、可重复执行、ID 首位 0-7） |
| 章节 ID | `141DBA5B3B33661A` |
| 分组 | GT 组 `4A46A5E1358A80A6`（order_index 18，MEK 17 之后） |
| 标题 | `&b太空探索&r`（内联中文） |
| 任务数 | 30（全部内联中文，0 lang 键） |
| 入口依赖 | EV 章「EV组装机」任务 `7A55CC71442CC854` |

**任务布局（GTO 式紧凑 2D 网格，x 0→18 / y -6→+6，蛇形横排）**：

```
y=-6   宇航服(0) 氧气(3)  发动机(6) 储罐(9)  月球资源(12) 扩散器(15) 温度(18)
y=-3   GTNN引擎(0) 激光(3) 寻矿(6)  GPS(9)   金星(12)   火星(15)   MekaSuit(18)
y= 0   扫描仪(0) 发射台(3) T1(6)    燃料(9)   组装(12)   月球(15)   T2(18)
y=+3   戴森组件(0) 电梯(3) 空间站(6) 组装机(9) 比邻星b(12) T3(15)    水星(18)
y=+6   戴森球(0)  物流(3)
```
- 主流程第 3 行左→右（扫描仪→T2），第 4 行右→左（水星→戴森组件）蛇形续接，第 5 行收尾；
- 并联部件（发动机/储罐）、卫星三连、三行星、Mek/GT-- 联动分布在上下两行，非直线排布；
- 整章控制在 18×12 单位内 → **一张 640×360 大图正好盖满**（见 §4.5）。

---

## 2. 火箭制造硬化（GT-- 重型合金）

**目标**：火箭发动机 / 燃料储罐追加 2× 对应等级重型合金板，火箭等级 = GT-- 重型合金链等级。

| 部件（装配机） | 电压 | 追加 |
|---|---|---|
| 基础燃料罐 / 基础发动机 | HV（480 EUt） | `gtnn:heavy_plate_t1` ×2 |
| 先进燃料罐 / 先进发动机 | IV（7680 EUt） | `gtnn:heavy_plate_t2` ×2 |
| 精英燃料罐 / 精英发动机 | ZPM（122880 EUt） | `gtnn:heavy_plate_t3` ×2 |

实现：`kubejs/server_scripts/gcyr/hardenRockets.js`（移除 `gcyr:*_fuel_tank`/`gcyr:*_rocket_motor` 原配方后按原参数重写）。

**重型合金链补全**（`kubejs/server_scripts/gcyr/heavyAlloys.js`）：
GTNN 原重型锭配方位于 `AdAstraRecipes`（依赖 ad_astra，本包未装）→ 用包内材料替代后镜像补全（机器/电压/时长/电路/流体量与原版一致）：

| 锭 | 配方（装配机） | 电压 |
|---|---|---|
| T1 | 黄铜/铝/钢致密板 + 72mB 不锈钢 + 电路1 | HV 480 |
| T2 | T1 + 2×钛致密板 + 72mB 钨钢 + 电路1 | EV 1920 |
| T3 | T2 + 4×钨钢致密板 + 72mB 铂 + 电路1 | IV 7680 |
| T4 | T3 + 4×钠钾合金致密板 + 72mB 三钠钾合金 + 电路1 | LuV 30720 |

> 重型板 = GTNN 自带内爆压缩机配方（重型锭 + 炸药），无需补全。

---

## 3. GCYR × Mekanism 联动

| 项 | 机制（实证） | 实现 |
|---|---|---|
| 宇航服氧气 | GCYR 灌装检查 `forge:oxygen` 标签；Mek 液态氧已挂该标签 | **天然兼容，零改动**（电解分离器→旋转冷凝器→灌宇航服） |
| 氧扩散器 | GCYR 配方写死 `gtceu:oxygen` | `mekLinks.js` 补 6 档 Mek 氧气配方（750~750000 mB） |
| 火箭氢燃料 | GCYR 配方写死 `gtceu:hydrogen` | `mekLinks.js` 补 `mekanism:hydrogen` 燃料（1mB/10t/EUt 1） |
| MekaSuit 温度 | GCYR 检查物品标签 `gcyr:heat_resistant`/`freeze_resistant` | 数据标签加入全套 MekaSuit（`kubejs/data/gcyr/tags/items/`） |
| 跨行星物流 | Mek 量子纠缠器原生跨维度 | 任务章提示（无脚本） |
| 绕过检查 | Mek 传送器需两端配对（首次仍需火箭） | 无绕过 |

---

## 4. GCYR × GT-- 联动

| 方向 | 内容 | 实现 |
|---|---|---|
| B1 引擎发电 | GTNN 火箭引擎（EV/IV/LuV）燃烧 GCYR 燃料：`gtceu:rocket_fuel`(1mB/4t)、汽油(4mB/3t)、柴油(3mB/3t)、Mek 氢(8mB/3t)，EUt=-2048 发电 | `gtnnLinks.js` |
| B2 高级燃料 | GTNN 燃料驱动 GCYR 火箭（每 mB 燃烧时长）：RP-1 50 / 稠密肼 60 / UDMH 90 / MHN 100；EUt=最低发动机等级 1/2/2/3 | `gtnnLinks.js` |
| 硬化 | 火箭部件需要 T1~T3 重型合金板 | `hardenRockets.js` |
| 进度关系 | GTNN 机器本身为 EV+（GT 电压自然门槛），本次通过重型合金链把 GTNN 变成火箭必经之路 | — |

> GTNN 未额外加硬锁：其机器配方由自身机壳/装配线自锁，盲目 replaceInput 有破坏风险；如需强制锁可在确认配方后追加。

---

## 4.5 章节背景图（4 张太空贴图）

- 纹理位置：`kubejs/assets/society/textures/quests/space/{space,beyondstars,spacestation,station-1}.png`
  （KubeJS 的 `assets/` 作为资源包加载；FTB Library 对以 `.png` 结尾的 image 字符串按**完整纹理路径**解析）
- 章节引用：`space.snbt` 的 `images` 数组（生成器 `CHAPTER_IMAGES` 常量，可重复生成）：
  | 图 | x（中心） | y（中心） | 尺寸 | 说明 |
  |---|---|---|---|---|
  | space.png | 9 | 0 | 25.6 × 14.4 | **GTO 式整章背景**：一张 640×360 原生尺寸大图居中盖满 18×12 的章节 |
- **GTO 的做法（分析结论）**：GTO 的太空章（`space-station.snbt`）同样是普通 `images` 条目，但用**一张大图（25.6×14.4，约等于 640×360 原生像素）以章节中心为原点覆盖全部任务**（章节任务区 x 2~17 / y -11~-3，图片中心 (9, -6.5)），因此看起来就是"整个任务窗口的固定背景"——并不是特殊字段（2001.4.17 的 `Chapter` 无 `background` 字段，FTB Quests 也没有屏幕固定的图片类型）。
- 换图：改生成器 `CHAPTER_IMAGES` 一行即可（另外 3 张 `beyondstars / spacestation / station-1` 同样可用）。
- 游戏内调整：`/ftbquests editing_mode` → 章节内拖动/缩放图片（尺寸按 1 单位=24px 估算，640px≈26.7 单位）。

---

## 5. 校验结果

- `node --check`：4 个新脚本全部通过
- 标签 JSON：解析通过
- 太空章：30 任务、80 ID（首位 ≥8 为 0）、无重复、无 lang 键、括号平衡
- 全库：4952 ID（0 溢出 / 0 重复）、依赖引用 0 悬空
- 待运行验证：`e.recipes.gcyr.*` / `e.recipes.gtceu.rocket_engine` 配方注册；`2x #forge:plates/kapton_k` 等计数标签解析；重型合金 JEI 显示

---

## 6. 已知问题与备注

1. 服务器日志中 `gcyr:gasoline`/`gcyr:diesel` 的 "EUt can't be explicitly set to 0" 为 GCYR 自身配方问题（装饰性），本批不改动。
2. `gcyr:passes_flood_fill` 标签含 UEV+ 氧扩散器（普通模式不存在）→ 标签警告；IV~UV 正常。
3. GTNN 重型锭/板在没有 Ad Astra 时原本不可获得，本批已补全（见 §2）。
4. 太空章依赖 EV 章任务 `7A55CC71442CC854`；若 EV 章被重生成需确认该 ID 仍存在。
