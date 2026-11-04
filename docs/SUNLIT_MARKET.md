# Sunlit Market：中州 NPC 交易与经济联动（规划 + 当前实现）

> 工程：`H:\MinecraftMods\SunlitMarket`（Forge 1.20.1）
> 集成脚本：`kubejs/server_scripts/sunlitmarket/meMerchants.js`、`kubejs/startup_scripts/me/meTrades.js`；
> 深度联动脚本：`svCustomers.js` / `svMeCustomers.js` / `svMastery.js`。
> 状态：**核心层已编译、GUI/事件/KubeJS 绑定已验证；Sunlit Valley 深度联动已静态实现，尚未启动服务器验收。**
> 价格分析与边界见 [`SUNLIT_VALLEY_INTEGRATION.md`](SUNLIT_VALLEY_INTEGRATION.md)。

## 1. 为什么不是“再造一套货币”

整合包已经有两层可用经济：

- Create: Numismatics：硬币 + 银行账户（`Numismatics.BANK` / `BankAccount`）
- `society_trading`：商店 GUI、每日货架、季节/阶段门槛、`/openshop`
- Shipping Bin / Cozy Cafe / Bountiful：农业收购、料理收购、悬赏

所以 Sunlit Market 的定位是：

> **给中州 NPC 一个可配置的交易入口，并补上独立声望；货币、价格和库存尽量复用现有系统。**

中州自带的 `me:copper_coin` / `silver_coin` / `gold_coin` 不再是第二套经济：它们通过钱庄商人兑换，或在 `SunlitMarket.coinValue` 中登记为硬币面值。

## 2. 与 Connector 上的 Fabric Middle-earth 如何兼容

本包里的 Middle-earth 是 **Fabric mod 通过 Sinytra Connector 运行**，类在运行时被 remap，不能按普通 Forge mod 编译。

Sunlit Market 的约束：

- **不编译、不 import 任何 `net.jukoz.me` 类**
- **不使用 Mixin 修改 ME**
- 识别商人只依赖：
  1. 实体 `Tags`（推荐）：`sunlitmarket.me.shire_farmer`
  2. 或 `entity.serializeNBT()` 的 `NpcData.Type`（只读 NBT，例：`me:shire.peasant`）
  3. 或 ForgeData 的 `sunlitmarket.merchant` 覆盖
- 找不到商家/解析失败时静默返回，不影响原版与 ME

这意味着 ME 更新、Connector 映射变化或换 JAR 时，只要 `me:npc` 和 NpcData 结构还在，交易层不随之崩溃。

### 风险（需游戏内确认）

- `serializeNBT()` 是否在所有 ME NPC 上包含 `NpcData.Type`（标签方式已提供兜底）
- ME NPC 对无派系玩家敌对（`TargetPlayerDiplomacyGoal`）；商人建议放在玩家同派系城镇，或后续加“商人免战”配置
- 未定型 NPC 可能被 ME 自动 discard；测试商人请带 `InitializationData.Type`

## 3. 当前实现的 KubeJS API

```js
SunlitMarket.clear()                       // 清空脚本商人（/reload 脚本开头调用）
SunlitMarket.merchant({ ... })             // 注册/覆盖商人
SunlitMarket.offer("merchant_id", { ... }) // 给已有商人追加商品
SunlitMarket.open(player, "merchant_id")   // 服务端打开交易 GUI
SunlitMarket.buy(player, "merchant_id", 0, 1)  // 脚本代买（offer 索引从 0 开始）
SunlitMarket.sell(player, "merchant_id", 0, 1) // 脚本代卖
SunlitMarket.coinValue("me:copper_coin", 1) // 登记硬币面值（spur）
SunlitMarket.balance(player)               // 当前余额
SunlitMarket.setReputation(player, "me:gondor", 10)
SunlitMarket.addReputation(player, "me:gondor", 1)
SunlitMarket.getReputation(player, "me:gondor")
SunlitMarket.reload()                      // 重新读取 config/sunlitmarket/merchants.json
SunlitMarket.priceMultiplier("merchant", "me:tomato", 1.2) // 买卖价倍率
SunlitMarket.clearPriceMultipliers()
SunlitMarket.merchants()                   // 当前商人 JSON（调试）
```

商人字段：

```js
{
  id: "me_shire_farmer",
  name: "夏尔农户",
  faction: "me:shire",          // 独立声望桶，可以与 ME 派系同名
  tag: "sunlitmarket.me.shire_farmer",
  npcType: "",                  // 可选：me:shire.peasant
  offers: [
    { item: "me:tomato", count: 1, buy: 16, sell: 10, reputation: 0, stock: 16 }
  ]
}
```

- `buy`：玩家付钱买入的价格（spur）
- `sell`：玩家卖出的价格（spur）
- `reputation`：该商品要求的最低独立声望
- 同一商品可同时有 buy/sell；为 0 表示不提供该方向
- `stock`：每日库存；`-1` 或不填 = 无限；游戏日切换时自动重置
- `priceMultiplier` 是 KubeJS 运行期倍率，不写盘；需要在脚本里按季节/事件重新设置

也可写 `config/sunlitmarket/merchants.json`（数组或 `{merchants:[...]}`），不依赖脚本。

## 4. 当前功能边界

已实现：

- 右键商人 NPC（主手）打开 GUI
- 买卖、余额/声望显示、声望门槛
- Numismatics 银行优先；缺失时退回硬币物品
- 独立声望按玩家 UUID + faction 存入 overworld `SavedData`
- 商人 JSON 配置 + KubeJS 注册
- 中州 5 类商人 + 钱庄示例脚本
- ME 作物/料理进入 Shipping Bin 价格表（`meTrades.js`）
- 每日库存（`stock`）与每玩家每日限购（`limit`）
- KubeJS 价格倍率（`priceMultiplier`）；声望提供买入折扣/卖出加成
- 匠魂/神秘/星辉示例商人（`themedMerchants.js`）
- 季节价格示例（`meSeasonPrices.js`）
- 带 `sunlitmarket.` 标签的商人不会被 AI 选为目标，也不会主动选定玩家；ME 原生派系日志仍不属于本 mod 控制

尚未实现（P2/P3）：

- 季节/派系价格曲线继续扩展；声望衰减/任务提升
- 自定义多标签交易界面（目前单列表）
- 中州币与银行的双向兑换 GUI（当前用钱庄买卖实现）
- 与 FTBQ / SVDialog 的对话联动
- 匠魂/神秘/星辉商人继续补阶段门槛与更多材料

## 5. 测试系统

### 最小客户端（无经济模组）

工程：`H:\MinecraftMods\SunlitMarket`

```
run-client/
  kubejs/server_scripts/sunlitmarket_test.js   # 注册 Test Farmer，自动打开
  saves/smtest/                                # 测试世界
```

- 30 秒后自动打开测试商店
- 测试货币：`minecraft:emerald` 面值 1（仅 dev harness，生产环境由 KubeJS 覆盖）
- 已验证：KubeJS 插件加载、商人注册、GUI 打开、声望行显示

启动：

```powershell
H:\MinecraftMods\gradle-8.14.5\bin\gradle.bat --no-daemon runClient -PquickPlay=smtest
```

（非阻塞启动后轮询 `run-client/logs/latest.log`，不要用长 Sleep 占住命令。）

### 生产整合包测试

需要把构建产物 `sunlittrade`/`sunlitmarket-1.20.1-0.1.0.jar` 放入客户端与服务端 mods，并把：

- `kubejs/server_scripts/sunlitmarket/meMerchants.js`
- `kubejs/startup_scripts/me/meTrades.js`

同步到两边。服务端只允许手动放置 mod；kubejs 可走 Rosetta。

## 6. 路线图

| 阶段 | 内容 |
|---|---|
| P0（当前） | GUI + 买卖 + 独立声望 + KubeJS API + 中州示例商人 |
| P1 | 每日库存/补货、买卖限额、季节价格、ME NPC 免战 |
| P2 | 声望任务/衰减、派系专属折扣、FTBQ/SVDialog 对话入口 |
| P3 | 匠魂/神秘/星辉主题商人、商队/随机货架、银行兑换界面 |

## 7. 重要事实与限制

- `society_trading` 的 `entity_data` 是字符串子串匹配，不适合直接绑定全部 `me:npc`；Sunlit Market 用 Tags/NpcData.Type 精确匹配。
- `me:npc` 只有一个实体类型；不要按实体类型判断商人。
- ME 没有原生声望/交易/任务 API；本 mod 的声望是独立 SavedData，不修改 ME 的静态外交表。
- Quality Food 的品质是 NBT；当前交易按物品 ID 计价，品质差价留给 P1。
