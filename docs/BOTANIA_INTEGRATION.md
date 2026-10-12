# 植物魔法（Botania）阶段锁 × 暮色森林 / 神秘时代

> 最后更新：2026-09-17
> 需求：植物魔法卡阶段，卡到「进入暮色森林 + 击败巫妖王」；泰拉钢锭需要神秘时代出虚空锭。

---

## 1. 手册流程依据（Botania 内置 Patchouli 手册 Lexicon）

来源：`assets/botania/patchouli_books/lexicon/en_us/entries/**` 的 `advancement` 字段（解锁链）：

| 手册条目 | 解锁条件（advancement） |
|---|---|
| `mana/intro`（魔力体系） | `botania:main/pure_daisy_pickup`（白雏菊） |
| `basics/rune_altar`（符文祭坛） | `botania:main/mana_pool_pickup_lexicon`（魔力池） |
| `basics/terrasteel`（泰拉钢） | `botania:main/runic_altar_pickup`（符文祭坛） |
| `alfhomancy/intro`（精灵门） | `botania:main/terrasteel_pickup_lexicon`（泰拉钢） |
| `alfhomancy/gaia_ritual`（盖亚仪式） | `botania:main/elf_lexicon_pickup`（精灵门） |

即官方进度：**花/花药台/法杖 → 白雏菊 → 魔力（散布器/池）→ 符文祭坛 → 泰拉钢 → 精灵门 → 盖亚**。

---

## 2. 阶段锁设计

| 阶段 | 锁对象 | 新增材料 | 材料来源 |
|---|---|---|---|
| ① 进入暮色森林 | `botania:mana_spreader`（魔力散布器）、`botania:mana_pool`（魔力池） | `twilightforest:torchberries` ×1 | 暮色森林火把浆果植株掉落（无需剪刀，战利品表已核对） |
| ② 击败巫妖王 | `botania:runic_altar`（符文祭坛） | `twilightforest:lich_trophy` ×1 | 巫妖王击杀掉落（仅需 1 个，不重复消耗） |
| ③ 神秘出虚空锭 | `botania:terrasteel_ingot`（泰拉钢锭，大地聚合） | `thaumcraft:void_ingot` ×1 | TC4 坩埚：虚空种子 + metallum 8（虚空种子可再生） |

**连锁效果（无需额外锁）**：
- 魔力散布器/池 → 卡住一切魔力获取（产能花/功能花无池可用）
- 符文祭坛 → 卡住全部符文 → 卡住大地聚合板（需 5 符文）→ 卡住泰拉钢 → 卡住精灵门（泰拉钢粒）→ 卡住盖亚（源质锭来自精灵门）
- 泰拉钢 → 同时卡住包内既有泰拉钢装备配方（`addToolRecipes.js`，消耗泰拉钢锭）

---

## 3. 关键事实（核对自 JAR，非推测）

- `botania:mana_spreader` 原配方为 `botania:gog_alternation` 类型（含 Garden of Glass 变体），KubeJS 无法对嵌套配方做 `replaceInput`，因此采用**移除 + 重写**。
- `botania:mana_pool` 原配方：`R R / RRR`（5 活石）；`botania:runic_altar` 原配方：`SSS / SPS`（5 活石 + 1 魔力珍珠）。
- 大地聚合配方类型 `botania:terra_plate` 的序列化格式：`{type, ingredients[], mana, result}`；其方块实体 `TerrestrialAgglomerationPlateBlockEntity#getInventory` 由盘上物品动态构建 `SimpleContainer`（上限 64 个物品），**支持 4 个材料**（已反编译核对）。
- 泰拉钢原配方：魔力钢锭 + 魔力珍珠 + 魔力钻石 + 500,000 mana；本包改为追加 1 虚空锭。
- TC4 虚空锭：`thaumcraft:void_ingot`，坩埚配方 `research: VOIDMETAL`（催化剂 `thaumcraft:void_seed`，metallum 8）；研究 `VOIDMETAL` 位于 ELDRITCH 分类，parents = `THAUMIUM` + `ELDRITCHMINOR`。
- 虚空种子配方：坩埚（research `VOIDMETAL`，催化剂小麦种子，tenebrae 8 + vacuos 8 + alienis 2）→ 可再生。
- 女巫商店（`kubejs/data/society_trading/shops/witch.json`）**不出售虚空锭**，任务书亦无虚空锭奖励 → 无绕过路径。
- 巫妖王掉落 `twilightforest:lich_trophy`（实体战利品表 `entities/lich.json` 含权杖池；奖杯为击杀掉落物），本设计仅消耗 1 个，无软锁风险。

---

## 4. 实现文件

| 文件 | 内容 |
|---|---|
| `kubejs/server_scripts/botania/gateBotania.js` | 三阶段配方锁（移除原配方 + 重写） |
| `kubejs/client_scripts/tooltips/botaniaGateTooltips.js` | 四个受锁物品的「阶段锁」提示（内联中文） |
| `config/ftbquests/quests/chapters/botania.snbt` | 三个相关任务追加阶段锁说明行（存储魔力 / 合成符文 / 泰拉钢）+ 详细解锁指引（进入暮色森林方法 / 巫妖塔打法 / 虚空锭研究链） |
| `kubejs/assets/ftbquestlocalizer/lang/{zh_cn,en_us}.json` | 对应任务文本（description5 / description4 ×2；其他语言自动回退 en_us） |

> 备注：任务书「泰拉钢」原描述本就写着「将所需的**四种**材料放到泰拉凝聚板上」，本次把第四种材料定为虚空锭，与该文案正好吻合。

---

## 5. 校验结果

- `node --check`：两个 JS 语法通过
- 物品/标签存在性：`twilightforest:torchberries` ✓、`twilightforest:lich_trophy` ✓、`thaumcraft:void_ingot` ✓、`#botania:livingwood_logs` / `#botania:petals` ✓
- 无冲突：包内既有 Botania 修改仅涉及花朵种子（`addMysticalFlowerSeedRecipes.js`）、装备配方重写（`removeRecipes.js` + `addToolRecipes.js`），与本锁不冲突
- 待运行验证：JEI 中魔力散布器/魔力池/符文祭坛/泰拉钢配方显示；大地聚合 4 材料实际可合成

---

## 6. 可选调整

- 火把浆果获取困难时，可换成 `twilightforest:liveroot` 或暮色树木苗（改 `TF_BERRY` 常量）
- 如需把符文祭坛锁后移到巫妖王之后的更多内容，可对 `botania:terra_plate`（方块）追加战利品要求（需再杀一次巫妖王，谨慎）
- 数量调整：`B: TF_BERRY` 可在 pattern 中出现多次以要求更多浆果
