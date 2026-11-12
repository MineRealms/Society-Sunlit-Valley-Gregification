# SunlitMarket 联动修复与操作说明

日期：2026-11-13。目标：当前 Society Sunlit Valley 客户端目录与通过 Rosetta 连接的运行中服务器。

## 已部署内容

本轮采用 KubeJS 与 FTB Quests 数据修改，不需要更换 mod jar。服务器保持运行，已执行两次 `kubejs reload server_scripts` 与一次 `ftbquests reload`。

| 修复 | 实现 |
|---|---|
| 重载后季节价格、精通阶段桥失效 | 删除跨重载保留的 `*_INSTALLED` 监听器守卫；脚本重新加载时重新注册事件 |
| 重载后季节倍率丢失 | 新监听器首个安全 tick 重设倍率，之后保持原有 200 tick 刷新周期 |
| 主 HUD 覆盖市场 HUD | 两份脚本按面板 ID 合并，只替换自己的面板 |
| 自然 NPC 同时做商人和顾客 | 移除六位中州商人的 `npcType` 泛匹配，改用专用实体标签；十位中州/主题商人附加 `MERCHANT` 身份规则 |
| 四个主题 unlock 没有发放来源 | 现有里程碑增加个人自动命令奖励 |
| 本地缺少六份选择对话 | 从现有 release overrides 同步至主目录；线上本来已有这些文件，读回一致 |
| 任务说明失真 | 改正解锁命令身份、实际里程碑、接受仓脚本拒收边界说明 |
| 无效顾客货池 | 移除未被实际平民身份使用的 `me:neutral` 与父级 `me:longbeards` 顾客池 |

原 `me:neutral` 钱庄声望桶、`me:longbeards` 矿商声望桶保留，以免已有玩家声望断开。前者是 SunlitMarket 自己的记录键，不代表 Middle-earth 存在同名原生派系。没有修改 ME 的原生外交表。

## 玩家怎么用

1. 更新后重新进入服务器。已经在线时，先正常退出再加入即可。
2. 完成下表对应任务；新奖励按玩家领取，队友也各自领取，任务完成记录保持原样。
3. 输入 `/sunlitmarket locks`，检查自己的解锁 ID。
4. 找管理员放置的对应商人，右键查看货架。解锁只移除研究阶段门槛，原有声望、库存、资金与付款限制仍生效。

| 商店 | 完成里程碑 | 任务 ID | 解锁 ID |
|---|---|---|---|
| 匠魂 | 玛玉灵 | `7C14C2BAC46CE906` | `theme.tinkers.adept` |
| 神秘 | 神秘工业：血染高级电路模板 II | `3E981A3FFE0ADA0D` | `theme.thaumcraft.adept` |
| 星辉 | 星辉矿石与星辉锭 | `28626DC2C0B74311` | `theme.astral.attuned` |
| 植物魔法 | 泰拉钢 | `46F86152B5B36A3B` | `theme.botania.adept` |

神秘基础章没有独立虚空锭检测目标，因此选用了实际消耗虚空锭的模板 II，避免在神秘锭入门阶段开放虚空锭购买。

旧进度补领依据当前 FTBQ 2001.4.17：`ServerQuestFile.playerLoggedIn` 检查任务自动完成，`TeamData.checkAutoCompletion` 为已完成任务补领未领的新个人奖励。队伍被管理员锁定等特殊状态需要先处理其锁定原因。

命令奖励为：

```snbt
command: "execute as {p} run sunlitmarket unlock theme.tinkers.adept"
elevate_perms: true
team_reward: false
auto: "no_toast"
silent: true
```

`{p}` 是实际领奖者，不能写成 `@p`。`sunlitmarket unlock` 要求玩家命令源，不能从控制台直接裸执行。

## 管理员：放置与转换 NPC

商人与顾客现在是明确分开的身份：

- 没有商人标签：沿用自然类型、职业、命名 NPC 规则；符合 `CIVILIAN` 且有货池时，可成为柜台顾客。
- 有下表专用标签：右键打开商店，身份为 `MERCHANT`，不生成新的柜台顾客需求。
- 一个 NPC 只给一个商人标签。转换类型时先移除旧标签，再添加新标签。
- 移除商人标签后，身份回到其自然规则。已经生成的短期柜台需求由现有过期机制清理，不修改玩家交易记录。

| 商人 | 完整实体标签 | 商店 ID |
|---|---|---|
| 夏尔农户 | `sunlitmarket.me.shire_farmer` | `me_shire_farmer` |
| 刚铎军需官 | `sunlitmarket.me.gondor_quartermaster` | `me_gondor_quartermaster` |
| 洛汗猎手 | `sunlitmarket.me.rohan_hunter` | `me_rohan_hunter` |
| 萝林草药师 | `sunlitmarket.me.lothlorien_herbalist` | `me_lothlorien_herbalist` |
| 孤山矿商 | `sunlitmarket.me.erebor_smith` | `me_erebor_smith` |
| 中州钱庄 | `sunlitmarket.me.moneychanger` | `me_moneychanger` |
| 匠魂铸师 | `sunlitmarket.theme.tinkers` | `theme_tinkers_smith` |
| 神秘材料商 | `sunlitmarket.theme.thaumcraft` | `theme_thaumcraft_curio` |
| 星辉商人 | `sunlitmarket.theme.astral` | `theme_astral_merchant` |
| 植物魔法材料商 | `sunlitmarket.theme.botania` | `theme_botania_merchant` |

### 直接生成一位夏尔农户

在管理员玩家聊天中执行：

```mcfunction
/summon me:npc ~ ~ ~ {Tags:["sunlitmarket.me.shire_farmer"],InitializationData:{Type:"me:shire.peasant"}}
/sunlitmarket identity @e[type=me:npc,tag=sunlitmarket.me.shire_farmer,distance=..3,sort=nearest,limit=1]
```

预期身份包含 `rank=MERCHANT`、`customer=false`，然后右键查看货架。

### 把现有 NPC 指定为商人

确认目标实体 UUID 后，使用 UUID 避免误选邻居；以下 `<NPC_UUID>` 替换为实际值：

```mcfunction
/tag <NPC_UUID> add sunlitmarket.theme.tinkers
/sunlitmarket identity <NPC_UUID>
```

恢复自然顾客：

```mcfunction
/tag <NPC_UUID> remove sunlitmarket.theme.tinkers
/sunlitmarket identity <NPC_UUID>
```

恢复后不保证任何 NPC 都能采购，仍取决于它的自然身份与对应货池。新规则不会自动在地图上生成这十位商人。

### 查商品与人工补发

```mcfunction
/sunlitmarket near 32
/sunlitmarket debug theme_tinkers_smith
/sunlitmarket locks
```

`debug` 需要管理员权限。若确已完成任务但重新登录仍未补领，管理员先核对任务与队伍状态，再针对指定在线玩家执行：

```mcfunction
/execute as <玩家名> run sunlitmarket unlock theme.tinkers.adept
```

撤销时在命令末尾加 `off`。不要对 `@a` 无条件发放，避免跳过正常里程碑。

## 维护与重载

仅改商人、季节、HUD、身份脚本时：

```mcfunction
/kubejs reload server_scripts
```

仅改本轮任务文件时：

```mcfunction
/ftbquests reload
```

本轮不改配方、标签或服务器已有对话数据，不需要整服 `/reload`。以后新增或修改数据包内容时，单独重载脚本不会重载那些内容，需安排对应数据重载。

任务维护命令（在整合包根目录运行）：

```powershell
python config/ftbquests/tools/build_market_theme_unlocks.py --check
python config/ftbquests/tools/build_trade_chapter.py --check
```

第一份补丁生成器使用现有 SNBT 的语法树与位置，只追加四条奖励及说明，保留布局与全部旧 ID。二次执行不产生改动。三个原主题生成器也已加入相同奖励定义；但匠魂/星辉原完整生成器仍有历史分组、默认值和游戏保存格式差异，不要为通过它们的旧 `--check` 直接重生成整章。此轮四主题章使用 `build_market_theme_unlocks.py --check` 校验。

## 文件范围

- 主目录 7 份服务端 JS：`sunlitHud.js` 与 `sunlitmarket/` 下的 `meMerchants.js`、`meSeasonPrices.js`、`svHud.js`、`svMastery.js`、`svMeCustomers.js`、`themedMerchants.js`。
- `kubejs/data/dialog/dialogs/sunlitmarket_*_choice.json` 六份。
- 任务章：`tinkers.snbt`、`thaumic_industry.snbt`、`astral_sorcery.snbt`、`botania.snbt`、`trade.snbt`。
- 对应生成器与 ID 登记表；新增 `build_market_theme_unlocks.py`、`market_theme_unlock_ids.json`。
- `SunlitMarket/examples/sunlit-valley/` 中六份对应市场脚本。
- `SunlitMarket/tools/`：本轮部署清单、备份上传工具及只读探针。

主目录的运行文件与对应生成器/登记表已同步到 `pack/dev/overrides` 与 `pack/release/overrides`，两套各 28 文件逐一核对 SHA-256。没有发布更新器；不改 mod jar、旧 SavedData、已有任务完成记录。

## 验证结果

- 线上两次脚本重载：257/257，0 errors，0 warnings。
- 线上任务载入：10 分组、69 章节、2397 任务、28 奖励表。
- 第一轮有效探针 03:00:39：10 位商人、10 项身份检查通过，四个任务奖励全部存在且为个人自动奖励。
- 第二轮有效探针 03:07:27：再次通过；暂存注册关闭，KubeJS 错误数 0，HUD 为 `sunlitmarket` 与 `sunlit_status`，没有重复面板。
- 季节倍率在重载后的首 tick 应用，随后继续更新：03:05:11 为春季 51%，03:09:50 为 52%。
- 本地主题补丁校验通过，全库 6582 个有效定义，新增奖励各唯一，重复执行零变化；贸易章校验通过。
- 服务端 18 个运行文件逐一读回 SHA-256 核验，其中 12 个内容发生变化，六份对话线上本来已一致。
- 身份探针只构造未加入世界的测试实体，不放置 NPC、不发金币、不改真实玩家任务。早期探针误选 Mohist 的牵引关系 Set，产生过 FAIL 日志；改为严格匹配 `Set<String>` 后通过。
- 未操作客户端 GUI，货架、对话与 HUD 的最终视觉由玩家进入游戏确认。服务端仍有与本轮无关的 Astral 区块加载与 ModernFix 跳过潜在死锁事件警告，不能把脚本零警告解读为全服没有其它警告。

## 备份与恢复

实际部署前备份：

```text
H:\MinecraftMods\sunlitmarket-integration-20261113\server-backups\20261113-025435-310447
```

其中 `deployment.json` 记录每个路径部署前后的 SHA-256。备份是从正在运行的服务器读取，不是从客户端推测。

需要恢复本轮运行文件时，在 `H:\MinecraftMods\SunlitMarket` 中运行下面命令；工具会先备份恢复前状态，再上传旧文件，并读回核验：

```powershell
python tools/deploy_market_integration.py 'H:\MinecraftMods\sunlitmarket-integration-20261113\server-backups\20261113-025435-310447' tools/market_integration_files.json --backup-root 'H:\MinecraftMods\sunlitmarket-integration-20261113\rollback-backups' --apply
```

随后执行脚本和任务热重载。恢复运行文件不会撤销已经发给玩家的永久 unlock；如确需撤销，使用前述针对玩家的 `unlock <id> off`，不要删除整份经济 SavedData。
