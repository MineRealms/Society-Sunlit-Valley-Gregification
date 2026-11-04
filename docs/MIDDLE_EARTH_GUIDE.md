# Middle-earth（中州）任务与玩法引导

> 当前目标版本：整合包安装的 `Middle-earth-1.4.2-1.20.1-port.0.jar`。官方 wiki 页面目前标注为 1.5.3，故只把它当概念参考；下文具体配方/ID 优先取本地 jar 与整合包脚本。尚未游戏内实测的操作以“手动确认”任务表达。

## 1. 给玩家的主线顺序

FTB Quests 章节：`config/ftbquests/quests/chapters/middle_earth.snbt`，生成器：`config/ftbquests/tools/build_middle_earth_chapter.py`，ID map：`config/ftbquests/tools/middle_earth_ids.json`。

1. **中土之旅导航**：先读本章，了解这是独立维度、NPC 敌我与农业内容。
2. **工匠台、合金炉**：本包把工匠台的锡锭、合金炉的熔炉分别改成 `gtceu:basic_electronic_circuit`；先达 GT LV。脚本在 `kubejs/server_scripts/me/meRecipes.js`。
3. **星光水晶瓶**：原始空瓶配方在中州 jar 的 `data/me/recipes/empty_phial.json`（铁粒 + 玻璃）；持 `me:empty_phial` 对水使用得到 `me:water_phial`；再将水瓶与 `#me:glowy`、冰雪女王战利品按本包配方放进**星辉发现祭坛**。见 `kubejs/data/society/recipes/altar/starlight_phial.json` 和 JEI。
4. **进入中土**：星光水晶瓶右键在代码中直接传送到 Middle-earth。它本身不等于开启角色创建界面。角色 onboarding 是另一条流程：包括派系、种族、出生点；任务要求玩家观察并手动确认。若未出现，先检查服务端 Connector/Middle-earth 加载与同步，不要引导玩家反复消耗瓶子。管理员调试命令 `/middle_earth onboarding open` 需权限。
5. **探索与定位**：`me:middle_earth_map` 配方是 8 张纸围 1 本书（`data/me/recipes/middle_earth_map.json`）；地图传送/全屏按键可在按键设置的 Middle-earth 分类查看。
6. **种族与派系**：先看角色界面的属性和可选出生点，选好后理解敌我关系，再尝试坐骑、遗迹与地下城。这个版本确认有预设阵营外交；未找到声望刷取、军衔晋升或玩家自建帮会系统证据，不把这些写成现存玩法。
7. **农业 → 食物 → 营养**：从野外作物/种子开始，扩种后做中州料理。相关作物与食物已有 GTMFO 营养、通用种子/蔬菜标签和品质作物接入。

## 2. 种族、派系：已核实与未核实

### 种族

本机语言/数据包含：`me:human`、`me:elf`、`me:dwarf`、`me:hobbit`、`me:orc`、`me:uruk`、`me:goblin`、`me:snaga`。当前代码给玩家应用基础属性，种族不只是皮肤；生命、体型、速度等数值直接看游戏内选择页，不把 NPC 属性误写成玩家属性。

### 派系

当前 jar 的派系 JSON 分为 GOOD、EVIL、NEUTRAL，并定义可加入性、初始外交、可选种族和出生点。例：Dale、Gondor、Rohan、Shire、Longbeards、Lothlórien；Mordor、Isengard、Moria、Goblin Town、Gundabad 等。Neutral 也可能与玩家敌对（例如 brigand、wild goblins），不能当作安全中立。

这是**预设派系/阵营**而非通常意义的玩家帮会系统。不要承诺声望、刷任务晋级、招募 NPC 或自建公会，除非对当前 jar 的实现另有验证。

### 官方 wiki（版本警告）

- [Getting Started](https://middleearthmcmod.wiki.gg/wiki/Getting_Started)：讲解空瓶、装水、星光瓶、进入中土和角色选择；页面本身有旧版本安装说明，勿照抄到本 Forge 整合包。
- [Factions](https://middleearthmcmod.wiki.gg/wiki/Factions)：派系背景/阵营概念；页面标记版本 1.5.3 / Old，与本机 1.4.2 port 不完全等价。

## 3. 可落地的农业与食物联动

### 作物、种子和本包接入

- 作物/种子示例：`me:leek`、`me:cucumber`、`me:lettuce`、`me:garlic`、`me:tomato`、`me:bell_pepper`、`me:onion`、`me:flax`；种子包括 `me:bell_pepper_seeds`、`me:cucumber_seeds`、`me:lettuce_seeds`、`me:tomato_seeds`、`me:flax_seeds`、`me:pipeweed_seeds`。
- jar 有 1 作物 → 1 种子的配方资源，如 `data/me/recipes/tomato_seeds.json`、`flax_seeds.json`、`pipeweed_seeds.json`；未核实每种作物的野外首粒种子和全部成熟掉落，任务不要承诺。
- `kubejs/server_scripts/me/meTags.js` 将中州蔬菜/种子接入 `forge:crops/*`、`forge:vegetables`、`forge:seeds`；作物方块通过 **block tag** 接入 `quality_food:quality_blocks`。Quality Food 2.4.3 的该标签是 `TagKey<Block>`，不是 item tag；成熟作物判定来自 `CropBlock`，标签只参与品质方块资格，不能保证每次收获必出品质。
- `kubejs/server_scripts/gtmfo/gtmfoNutrients.js` 明确设置：中州常见蔬菜 1.0 vegetable、草莓 0.75 fruit、多种蘑菇 0.5 vegetable、肉类按条目设置 protein；本次还补齐蔬菜汤、莓果派、鱼炖菜、蟹汤、禽肉餐、肉碗、肉蛋餐、串类等成品料理的显式营养值。营养种类标签和单件显式数值不是同一层，改动需检查两处。
- `kubejs/server_scripts/me/meCooking.js` 在中州模组自带的合成配方之外，为 6 道料理增加 `farmersdelight:cooking`（炖锅）做法：蔬菜汤、鱼炖菜、蟹汤、禽肉餐、肉碗、肉蛋餐。这样这些作物可直接进入现有厨房设施，而不是只走原版工作台。

### 已核实配方（本地 jar）

| 配方 | 原料 | 产物 |
|---|---|---|
| `middle_earth_map.json` | 8 paper + 1 book（有序） | `me:middle_earth_map` |
| `vegetable_soup.json` | 3 × `#me:vegetable` + bowl（无序） | `me:vegetable_soup` |
| `berry_pie.json` | `#me:berries` + wheat + sugar + egg（无序） | `me:berry_pie` |
| `fish_stew.json` | `#me:cooked_fish` + 2 × `#me:vegetable` + bowl（无序） | `me:fish_stew` |
| `string_from_flax.json` | 4 `me:flax`（2×2） | 1 string |

此外有 crab soup、poultry meal、meat bowl/skewer、mushroom stew 等资源；添加任务前先检查配方 JSON 的实际 ingredients/result。食物配方存在不自动等于该食物有 GTMFO 单件营养值。

### 可继续扩写的任务/联动方向

- **菜园经营**：首粒种子 → 留种 → 多作物轮种 → 蔬菜汤/莓果派 → GTMFO 营养补齐。标签按 item/block 分开：作物产物走 item 标签，品质方块走 block 标签。**品质产出需游戏内实测**，不要把标签接入写成已保证效果。
- **中土农贸**：将料理接入 FTBQ 交付/Numismatics 奖励，或做低科技远征口粮；奖励量需按本包经济平衡。
- **地方材料**：亚麻 → 线；烟斗草作为独立农业支线；树木/浆果/蘑菇可接入季节或品质（需先确认当前方块掉落/季节行为）。
- **派系探索**：按出生区域设置“地图定位—安全补给—敌对营地—地下城钥匙”的手动确认链；不把角色选择或外交关系伪装成自动检测目标。
- **种族坐骑**：本机手册文本给出 Broadhoof Goat / Great Horn / Warg / Cave Troll 的种族或阵营提示。实际驯服条件需要游戏内逐项验证；任务目前采用手动确认，不要求可能不存在的坐骑蛋/驯服物品。

## 4. 实现 / 更新约定

- Middle-earth 任务由 `build_middle_earth_chapter.py` 生成，语义 ID 持久化在 `middle_earth_ids.json`。编辑数据后运行 `--check`、`--verify-repeat`，确认后才无参数写盘。
- 配方/脚本分别位于 `kubejs/data/society/recipes/altar/` 与 `kubejs/server_scripts/me/`；修改后检查服务器 `logs/kubejs/server.log`、`logs/latest.log`，特别搜索 `Parsing error loading recipe`。
- 服务器不得通过自动上传改 mod jar；本章目前只要求现有 Middle-earth/AS mods，服务器 KubeJS/FTBQ 改动按维护流程同步。
- FTBQ item 任务只证明拿到物品，不证明玩家选了该种族/派系、已建立农场或正确理解外交；后几类目标使用明确文字 + 手动 checkmark。
