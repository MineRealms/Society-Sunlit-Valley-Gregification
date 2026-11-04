# Sunlit Valley 深度联动与价格规划

> 工程：SunlitMarket（Java）+ 整合包 kubejs/server_scripts/sunlitmarket/
> 状态：**第一版静态实现完成，未做游戏内验收**（本地整合包 400+ mod，单人世界无法进入；等待服务器验证）。
> 全量覆盖审计见 [SV_PRICE_AUDIT.md](SV_PRICE_AUDIT.md)：1,735 个 FTBQ 任务物品中只有 529 个有 Shipping 锚，699 个有直接配方，800 个仍需 GT 动态配方/阶段兜底。
> 本文是价格和边界的说明；第一版货池不是最终全量价格表。

## 1. 目标与不做什么

### 做

- 让 **Sunlit 村民职业** 和 **Middle-earth 平民** 成为当铺柜台的顾客，而不是只让 ME 商人当货架。
- 用整合包已有的 **Shipping Bin 价格表**作为唯一价格锚，而不是再发明一套货币价值。
- 让 ME 商人收购 Sunlit 农产品/料理，形成“柜台低价收货 → 商人/出货箱卖出”的小额贸易闭环。
- 用 FTBQ/GameStages 的 mastery 阶段同步 SunlitMarket 解锁 id，给高阶货品一个可追踪的阶段门槛。

### 不做

- **不改 GT 配方**，不卡 GT 后期万级产量。GT 的 LV/Create、MEK 门槛保持原生整合包脚本。
- 不把 GT 的机器/电路做成无限货架；高阶 GT 仍走玩家自己的产线。
- 不修改 Middle-earth 的静态外交表、不 import net.jukoz.me.*。
- 不新增货币；Numismatics / 硬币回退仍是唯一支付层。
- 不在客户端/单人环境做运行时验收。

## 2. 价格锚：Shipping Bin

整合包的 startup_scripts/globalRegistry.js 维护 global.trades：

    global.trades.set(item, {
      value: global.getConfiguredValue(baseValue, kind), // 已乘 farmer/artisan/mining/adventurer 倍率
      multiplier: "shippingbin:crop_sell_multiplier"
    })

基准条目规模（静态统计）：

| 表 | 条目 | 原始值范围 |
|---|---:|---:|
| global.crops | 202 | 1–1440 |
| global.fish | 83 | 4–666 |
| global.logs | 71 | 2–32 |
| global.animalProducts | 93 | 4–1800 |
| global.artisanGoods | 53 | 4–10368 |
| global.ore | 33 | 4–23040 |
| global.gems | 6 | 112–1024 |

规则：**Shipping Bin 的 value 是玩家保底能拿到的钱**。任何“从 NPC 买入再出货”的路径必须留出运费/时间/风险，否则就是无限套利。

## 3. 三个价格面

### 3.1 柜台顾客求售价（NPC 卖给你）

    market = shippingValue(item) * count
    base   = round(market * 0.60)      // 展示/还价参考
    ask    = round(market * ratio)     // 玩家实际支付

ask < market，玩家买下后送到 Shipping Bin 或 ME 商人处，才有正向收益。

| 类别 | ratio | 玩家毛利 | 说明 |
|---|---:|---:|---|
| 普通作物 | 0.92 | ~8% | 量大、稳定 |
| 鱼 | 0.92 | ~8% | 受季节/水域限制 |
| 原木 | 0.90 | ~10% | 单次 16 个，绝对值低 |
| 动物产品 | 0.90–0.92 | 8–10% | 奶/蛋/肉 |
| 矿石/锭 | 0.88–0.90 | 10–12% | 与 GT 原料竞争，必须留加工利润 |
| 加工品/料理 | 0.88–0.92 | 8–12% | 老练玩家可走高质量路线 |
| 稀有/魔法材料 | 0.72–0.88 | 12–28% | 数量少，风险/阶段门槛高 |
| 赃物 | 0.50–0.58 | 42–50% | 附带 heat 与 wanted，执法会没收 |

**还价**：界面 -10% / -20% 会让 ask 进一步下降；成功则玩家利润更高，失败则顾客撤回并扣该派系结盟值。+1 奖励只在 ask 达到 market 的 90% 时结算，所以“压价”与“声望”是取舍。

示例（当前脚本实际算法）：

| 物品 | count | shipping value | market | ask (90–92%) | 出货利润 |
|---|---:|---:|---:|---:|---:|
| 小麦 | 4 | 46 | 184 | 169 | 15 |
| 番茄 | 4 | 24 | 96 | 88 | 8 |
| 卷心菜 | 2 | 70 | 140 | 129 | 11 |
| 生鳟鱼 | 1 | 40 | 40 | 37 | 3 |
| 铁矿原矿 | 8 | 8 | 64 | 58 | 6 |
| 钻石（赃物） | 1 | 256 | 256 | 141 | 115 + 12 wanted |

### 3.2 柜台顾客的验收门槛

- 顾客必须在柜台 8 格内（counter.range）。
- 每个 NPC 有全局冷却/每日配额，多个柜台不会复制同一顾客请求。
- 请求有 lifetime（默认 1200 tick），过期/离区/换维度即失效。
- 请求价格是快照；结算前重新校验身份、池存在、期限和距离。

### 3.3 ME/主题商人买卖价

已有 ME 商人的基础货架保留，同时做两件事：

1. **修复倒挂**：minecraft:bread 原 buy=8, sell=4，而 Shipping Bin 价值 16；玩家可 8 买 16 卖无限套利。现在 buy=22, sell=14。
2. **Sunlit 商品收购**：ME 商人新增 sell-only（只买玩家货）条目，价格 = ceil(shipping * 1.02)。玩家从柜台按 90–92% 买入，再卖给 ME 商人按 102% 卖出，毛利约 10–12%，且不需要改动 Shipping Bin。

| 商人 | 新增收购（示例） | 价格锚 |
|---|---|---|
| 夏尔农户 | 蓝莓、蔓越莓、番茄、卷心菜 | shipping × 1.02 |
| 刚铎军需官 | 熟成奶酪、油、枫糖浆 | shipping × 1.02 |
| 洛汗猎手 | 牛肉、猪肉、火腿 | shipping × 1.02 |
| 萝林草药师 | 水晶莓、魔力果 | shipping × 1.02 / 高阶 |
| 孤山矿商 | 铁矿、煤、铅矿 | shipping × 1.02 |

**高阶货品**（有 unlock）：

| 商人 | 物品 | buy | sell | 解锁 |
|---|---|---:|---:|---|
| 刚铎军需官 | 松露油 | 1.24× | 0.78× | sv.farming.master |
| 萝林草药师 | 魔力果 | 1.25× | 0.78× | sv.farming.master |
| 孤山矿商 | 棱彩碎片 | 1.27× | 0.78× | sv.mining.master |

这些价格永远高于 Shipping Bin 价值，避免“买入再出货”套利；高阶货只作为阶段奖励的便利入口。

## 4. Sunlit 职业 → 顾客派系

svCustomers.js 不依赖自定义名称/语言，按实体类型 + 职业识别：

| Sunlit 职业 | 实体/职业 | 顾客派系 |
|---|---|---|
| 农户 | minecraft:villager / farmer | society:farmer |
| 渔夫 | minecraft:villager / fisherman | society:fisher |
| 牧羊人 | minecraft:villager / shepherd | society:shepherd |
| 铁匠 | minecraft:villager / toolsmith | society:blacksmith |
| 木匠 | minecraft:villager / mason | society:carpenter |
| 屠夫 | minecraft:villager / butcher | society:butcher |
| 图书管理员 | minecraft:villager / librarian | society:librarian |
| 银行家 | minecraft:villager / cartographer | society:banker |
| 集市商人 | farmingforblockheads:merchant | society:market |
| 旅行商人 | minecraft:wandering_trader | society:trader |

货池：

- **农户**：所有 global.crops 中 value 4–512 的散装作物；排除 _crate/_bag/_block/_sack/_basket/_barrel/_box/_tray，避免一次请求搬空仓库。
- **渔夫**：global.fish 中所有非 _barrel 的鱼，包括高价值鱼。
- **矿物/宝石**：global.ore、global.gems、geode/frozen/magma geode、miscGeologist 全量货池；低价值进铁匠，高价值进旅行商人。
- **饮料**：global.wines/brews/cocktails/herbalBrews；普通进集市，高价值收藏酒进旅行商人。
- **文物**：global.artifacts/relics 只进旅行商人，不在普通农户池。
- **木匠**：global.logs 中 value 2–16 的原木，单次 16 个。
- **牧羊人**：奶、蛋、羊毛、牛猪羊、火腿、羊奶酪。
- **铁匠**：铁/铜/金/煤/红石/青金石/锌/铅/银原矿与锭。
- **集市**：蛋黄酱、帆布、油、枫糖浆、熟成奶酪、电池、松露油、葡萄酒、烤鸡。
- **图书管理员**：纸、书、书架、命名牌、星之书。
- **旅行商人**：晶石、紫水晶、海蓝宝石、红宝石、玉、尖晶石、棱彩碎片、文物，以及 AS/TC/BOT 魔法材料；其中赃物条目带 heat/wanted。

## 4b. AS / TC / BOT 魔法材料

只选材料，不选机器。

**Astral Sorcery**（无 Shipping 锚，按现有星辉商人价格阶梯 + 配方深度）

| 物品 | 数量 | 市场参考 | 顾客 ask |
|---|---:|---:|---:|
| astralsorcery:aquamarine | 2 | 80 | 64 |
| astralsorcery:stardust | 4 | 96 | 79 |
| astralsorcery:infused_wood | 4 | 64 | 54 |
| astralsorcery:illumination_powder | 4 | 48 | 40 |

**Thaumcraft**（无 Shipping 锚，按现有神秘材料商 30/38/160/320 阶梯）

| 物品 | 数量 | 市场参考 | 顾客 ask |
|---|---:|---:|---:|
| thaumcraft:amber | 2 | 80 | 66 |
| thaumcraft:quicksilver | 2 | 100 | 82 |
| thaumcraft:thaumium_ingot | 1 | 220 | 176 |
| thaumcraft:alumentum | 4 | 96 | 81 |
| thaumcraft:nitor | 4 | 64 | 54 |

**Botania**（有 Shipping 锚，锚价优先）

| 物品 | 数量 | 市场参考 | 顾客 ask |
|---|---:|---:|---:|
| botania:livingwood_log | 8 | 128 | 115 |
| botania:livingrock | 16 | 32 | 28 |
| botania:manasteel_ingot | 1 | 32 | 28 |
| botania:mana_pearl | 1 | 96 | 81 |
| botania:white_petal | 8 | 16 | 14 |

AS/TC/BOT 材料由旅行商人求购/求售；机器、多方块、仪式结构不进顾客池。星辉锭/共鸣宝石、虚空锭、魔力钻石属于高阶材料，只放在主题商人的 unlock 货架，不进普通旅行商人池；新增 `theme_botania_merchant`（tag `sunlitmarket.theme.botania`），高阶材料使用 `theme.botania.adept` 解锁。

## 5. Middle-earth 派系货池

svMeCustomers.js 给 ME 平民补货池，身份仍由 NpcData.Type 的原生 faction/rank 提供，不修改 ME 数据：

| 派系 | 典型货池 |
|---|---|
| me:shire | 韭葱、黄瓜、生菜、番茄、草莓、白蘑菇、蔬菜汤 |
| me:gondor | 面包、肉碗、肉串、蛋肉餐、铁锭 |
| me:rohan | 鹅/鸭/天鹅/鼠肉、马饲料、牛肉 |
| me:lothlorien | 草莓、幽灵菇、黄鹅膏、喇叭菇、烟叶 |
| me:longbeards.erebor | 亚麻、铁矿、煤、铅矿、银矿 |
| me:dale | 面包、线、卷心菜、蓝莓 |
| me:neutral | 纸、书、晶石、帆布 |
| me:brigand / me:isengard / me:mordor | 便宜赃物（钻石、金、下界合金碎片、火药），带 heat/wanted |
| me:moria / me:goblin_town / me:hobgoblin_tribes.gundabad / me:wild_goblins | 矿石、煤、赃物 |

另加显式平民身份规则（me:shire.peasant 等），避免未来 ME 派系表 rank 改动导致顾客消失。

## 6. 阶段桥

svMastery.js 只做“阶段 → SunlitMarket unlock”的镜像，不改 FTBQ：

| 阶段 | 解锁 id |
|---|---|
| mastery_unlocked | sv.mastery |
| farming_mastery | sv.farming.master |
| fishing_mastery | sv.fishing.master |
| husbandry_mastery | sv.husbandry.master |
| mining_mastery | sv.mining.master |
| adventuring_mastery | sv.adventure.master |
| invited_* | sv.shop.* |

玩家登录和每 100 tick 同步一次；只有缺失时才写入，避免反复 dirty。

## 7. 代码位置

整合包：

- kubejs/server_scripts/sunlitmarket/svCustomers.js — Sunlit 职业顾客、货池、价格公式
- kubejs/server_scripts/sunlitmarket/svMeCustomers.js — ME 派系顾客货池
- kubejs/server_scripts/sunlitmarket/svMastery.js — 阶段镜像
- kubejs/server_scripts/sunlitmarket/svMagicCustomers.js — AS/TC/BOT 材料货池
- kubejs/server_scripts/sunlitmarket/meMerchants.js — ME 商人价格修复/跨经济收购
- kubejs/startup_scripts/me/meTrades.js — ME 农产品 Shipping Bin 价格（已有）

mod：

- MarketRules 新增 entity / profession 选择器，规则可以匹配 minecraft:villager + farmer，或 farmingforblockheads:merchant。
- 原有 tag / npcType / ME NpcData.Type 逻辑保持兼容。

## 8. 静态检查记录

- node --check：svCustomers.js、svMeCustomers.js、svMastery.js、meMerchants.js 全部通过。
- Node 静态执行（完整价格数组）：646 条规则 / 631 个货池 / 15 条 NPC 规则，0 重复、0 个 ask≥market 的坏池；bread 为 22/14。FTBQ 重点章节覆盖：crops 89/89、fishing 75/75、pantry 12/12、minerals 44/44；AS/TC/BOT 魔法材料 19 条。
- gradle --no-daemon test build：通过（22 个单测，构建产物可生成）。
- 未运行游戏；没有验证实体类型/职业名、物品 ID、货池实际生成、界面显示。
- 服务端首次启动时建议检查 [SV-INTEGRATION] ... registered 日志和 SunlitMarket.factions()。

## 9. 服务器验收清单

1. 启动服务器，确认无 KubeJS 脚本错误，日志出现三个 [SV-INTEGRATION] 注册行。
2. 在柜台附近生成农夫/渔夫/牧羊人/铁匠/旅行商人，确认柜台请求来自对应货池。
3. 收一单后把货物送 Shipping Bin，核对实际收益与本文示例一致。
4. 完成 farming_mastery，确认 /sunlitmarket locks 出现 sv.farming.master，松露油/魔力果解锁。
5. 用 /sunlitmarket debug me_shire_farmer 检查新增收购条目的价格与库存。
6. 检查购买赃物后 /sunlitalignment 的 wanted 增加，再验证检查员没收。
