# Society: Sunlit Valley (Baopu Edition / 宝铺版) — 整合包说明报告

> 本报告供其他 AI / 工具做联动分析使用。数据来源：`logs/modlist.txt`、`config/ftbquests/quests/**`、
> `kubejs/assets/ftbquestlocalizer/lang/zh_cn.json`；机器可读版本见同目录 `MODPACK_REPORT.json`。

## 0. 摘要

- **版本**：Minecraft 1.20.1 / Forge 47.4.23 / Java 17 (Eclipse Adoptium jdk-17.0.18.8)
- **规模**：392 个 mod jar（Forge 统计 393 项，含嵌套 jarjar 共 434 个 mod id）
- **任务书**：FTB Quests，30 章 / 1173 任务 / 1341 任务目标 / 487 奖励
- **主题**：田园/农场生活 + 村庄经济 + 收集养成（星露谷风格），科技线 Create、魔法线 Botania、存储线 Refined Storage
- **核心 mod**：Society（农场/村民/经济）、Society Trading、Create: Numismatics（货币）、Quality Food（品质）
- **任务文本**：全量 key 化，实际文本在 `kubejs/assets/ftbquestlocalizer/lang/*.json`（客户端加载）
- **已加载但未实际使用**：GregTech 系、神秘时代系、AE2 系、灾变（Cataclysm）——任务书 0 引用、无玩法集成

## 1. 基础信息

| 项 | 值 |
|---|---|
| 整合包名 | Society: Sunlit Valley (Baopu Edition / 宝铺版) |
| 实例路径 | G:\MinecraftGames\Sunlit Valley(BaopuEdition)\.minecraft\versions\Society Sunlit Valley |
| 启动器 | HMCL 3.6.11.264 |
| mod jar 数 | 398 |
| mod id 总数 | 462 |
| 章节 / 任务 | 49 / 1766 |
| 核心 mod | society 1.22, society_trading 1.2.9, ftbquests 2001.4.17, create 6.0.8, botania 1.20.1-454, refinedstorage 1.12.4, twilightforest 4.3.2508, numismatics 1.1.0, gtceu 7.5.3, mekanism 10.4.16, thaumcraft 4R (20711) |

## 2. 模组分类总览

> 分类为人工归纳；每项格式 `modid（名称）`。完整 mod 表见第 7 节与 `MODPACK_REPORT.json`。

### 核心 / 经济

- `society`（Society）、`society_trading`（Society Trading）、`numismatics`（Create: Numismatics）、`numismatics_utils`（Create: Numismatics Utils）、`shippingbin`（ShippingBin）、`bountiful`（Bountiful）

### 农业 / 种植

- `farmersdelight`（Farmer's Delight）、`farm_and_charm`（[Let's Do] Farm & Charm）、`veggiesdelight`（Veggies Delight）、`pamhc2trees`（Pam's HarvestCraft 2 - Trees）、`croptania`（Croptania）、`botania_seeds`（Botania Seeds）、`dew_drop_farmland_growth`（Dew Drop Farmland - Growth Edition）、`dew_drop_watering_cans`（Dew Drop Watering Cans）、`farmingforblockheads`（Farming for Blockheads）、`supplementaries`（Supplementaries）、`snowyspirit`（Snowy Spirit）、`etcetera`（Etcetera）、`quality_food`（Quality Food）

### 食物 / 烹饪

- `vintagedelight`（Vintage Delight）、`crabbersdelight`（Crabber's Delight）、`bakery`（[Let's Do] Bakery）、`candlelight`（[Let's Do] Candlelight）、`cozycafe`（Cozy Cafe）、`meadow`（[Let's Do] Meadow）、`beachparty`（[Let's Do] Beachparty）、`braziliandelight`（Brazilian Delight）、`butchercraft`（Butchercraft）、`displaydelight`（Display Delight Lite）、`farmlife`（Farm Life）、`farm_and_charm`（[Let's Do] Farm & Charm）、`farmersdelight`（Farmer's Delight）、`veggiesdelight`（Veggies Delight）、`windswept`（Windswept）、`atmospheric`（Atmospheric）、`autumnity`（Autumnity）

### 饮品

- `vinery`（[Let's Do] Vinery）、`brewery`（[Let's Do] Brewery）、`herbalbrews`（[Let's Do] HerbalBrews）、`nethervinery`（[Let's Do] NetherVinery）

### 渔业

- `aquaculture`（Aquaculture 2）、`unusualfishmod`（Unusual Fish Mod）、`netherdepthsupgrade`（Nether Depths Upgrade）、`stardew_fishing`（Stardew Fishing）、`crabbersdelight`（Crabber's Delight）

### 季节 / 天气

- `sereneseasons`（Serene Seasons）、`sereneseasonsfix`（Serene Seasons Fix）、`dew_drop_daily_weather`（Dew Drop Daily Weather）、`particlerain`（Particle Rain）

### 科技 / Create

- `create`（Create）、`create_central_kitchen`（Create: Central Kitchen）、`create_enchantment_industry`（Create Enchantment Industry）、`create_factory_logistics`（Create Factory Logistics）、`create_hypertube`（Create Hypertube）、`create_mechanical_extruder`（Create Mechanical Extruder）、`create_slime`（create_slime）、`createutilities`（Create Utilities）、`railways`（Create: Steam 'n' Rails）、`createrailwaysnavigator`（Create Railways Navigator）、`copycats`（Create: Copycats+）、`extra_gauges`（Create: Extra Gauges）、`createentitycontrol`（Create:Entity Control）、`ponderjs`（PonderJS）、`mekanism`（Mekanism 10.4.16）、`mekanismgenerators`（Mekanism Generators）、`mekanismadditions`（Mekanism Additions）、`mekanismtools`（Mekanism Tools）、`applied_mekanistics`（Applied Mekanistics）、`gregmek`（GT×MEK 矿石处理联动）、`gtmfo`（GT Modern Food Option）

### 存储 / 物流

- `refinedstorage`（Refined Storage）、`refinedstorageaddons`（Refined Storage Addons）、`rsinfinitybooster`（RSInfinityBooster）、`classicpipes`（Classic Pipes）、`pipez`（Pipez）、`functionalstorage`（Functional Storage）、`sophisticatedbackpacks`（Sophisticated Backpacks）、`sophisticatedstorage`（Sophisticated Storage）、`sophisticatedstoragecreateintegration`（Sophisticated Storage Create Integration）、`labels`（Labels）、`trashslot`（TrashSlot）、`toolbelt`（Tool Belt）

### 魔法

- `botania`（Botania）、`botania_seeds`（Botania Seeds）、`croptania`（Croptania）

### 探索 / 冒险

- `twilightforest`（The Twilight Forest）、`betterarcheology`（Better Archeology）、`relics`（Relics）、`species`（Species）、`windswept`（Windswept）、`atmospheric`（Atmospheric）、`autumnity`（Autumnity）、`legendarycreatures`（Legendary Creatures）、`rottencreatures`（Rotten Creatures）、`golemoverhaul`（Golem Overhaul）、`domesticationinnovation`（Domestication Innovation (Fixed)）、`paraglider`（Paraglider）、`waystones`（Waystones）、`simplerecall`（Simple Recall Potion）、`crittersandcompanions`（Critters and Companions）

### 建筑 / 装饰

- `furniture`（[Let's Do] Furniture）、`refurbished_furniture`（MrCrayfish's Furniture Mod: Refurbished）、`fantasyfurniture`（Fantasy's Furniture）、`tanukidecor`（Tanuki Decor）、`whimsy_deco`（Whimsy Deco）、`cluttered`（Cluttered）、`beautify`（Beautify）、`chimes`（Chimes）、`amendments`（Amendments）、`decorative_blocks`（Decorative Blocks）、`diagonalfences`（Diagonal Fences）、`diagonalwalls`（Diagonal Walls）、`twigs`（Twigs）、`clayworks`（Clayworks）、`supplementaries`（Supplementaries）

### 生物 / 宠物

- `crittersandcompanions`（Critters and Companions）、`buzzier_bees`（Buzzier Bees）、`ribbits`（Ribbits）、`snowpig`（Snow Pig）、`snuffles`（Snuffles）、`untitledduckmod`（Untitled Duck Mod）、`domesticationinnovation`（Domestication Innovation (Fixed)）、`golemoverhaul`（Golem Overhaul）、`legendarycreatures`（Legendary Creatures）、`hamsters`（Hamsters）、`snowyspirit`（Snowy Spirit）、`species`（Species）、`windswept`（Windswept）

### 收藏 / 趣味

- `longwings`（Longwings）、`splendid_slimes`（Splendid Slimes）、`trofers`（Trofers）、`simplehats`（SimpleHats）、`perfectplushies`（Perfect Plushies）、`gamediscs`（Game Discs）、`exposure`（Exposure）、`exposure_catalog`（Exposure Catalog）、`portfolio`（Portfolio）、`gallery`（Gallery）、`etched`（Etched）、`signpicture`（SignPicture-Rebornified）、`immersive_paintings`（Immersive Paintings）、`waterframes`（WaterFrames）、`webdisplays`（WebDisplays）、`simplemagnets`（Simple Magnets）

### 交通

- `moreminecarts`（More Minecarts and Rails）、`automobility`（Automobility）、`smallships`（Small Ships）、`waystones`（Waystones）、`simplerecall`（Simple Recall Potion）、`createrailwaysnavigator`（Create Railways Navigator）、`railways`（Create: Steam 'n' Rails）、`paraglider`（Paraglider）、`create_hypertube`（Create Hypertube）

### 任务 / 队伍

- `ftbquests`（FTB Quests）、`ftbquestlocalizer`（FTB Quests Localizer）、`ftbchunks`（FTB Chunks）、`ftbteams`（FTB Teams）、`ftblibrary`（FTB Library）、`questsadditions`（Quests Additions）、`certain_questing_additions`（Certain Questing Additions）、`ftbxmodcompat`（FTB XMod Compat）、`ftbbackups2`（FTB Backups 2）

### 旅行 / 世界

- `journeymap`（Journeymap）、`naturescompass`（Nature's Compass）、`biomespawnpoint`（Biome Spawn Point）、`lithostitched`（Lithostitched）、`terrablender`（TerraBlender）、`chunky`（Chunky）、`moonlight`（Moonlight Library）、`mysticaloaktree`（Mystical Oak Tree）、`hobbit_hill_village`（Hobbit Hill Village）、`moogs_structures`（Moog's Structure Lib）、`yungsapi`（YUNG's API）

### 未使用 / 乘客 mod

- `gtceu`（GregTech）、`gtmutils`（GregTech Modern Utilities）、`gtse`（Greg Tech Simple Extension）、`gtnn`（GT--）、`moldraw`（GregTech Molecule Drawings）、`gcyr`（Gregicality Rocketry）、`gregic_tinkering`（Gregic Tinkering）、`applied_greg`（Applied Greg）、`gtceuterminal`（Gregtech Terminals）、`gtca`（GT Community Additions）、`thaumcraft`（Thaumcraft 4R）、`thaumictinkerer`（Thaumic Tinkerer）、`forbidden_magic`（Forbidden Magic）、`tainted_magic`（Tainted Magic）、`ae2`（Applied Energistics 2）、`appbot`（Applied Botanics）、`cataclysm`（Cataclysm Mod）

> 其余 259 个 mod 为前置库 / 性能优化 / UI 辅助 / 杂项，完整清单见第 7 节与 `MODPACK_REPORT.json`。

## 3. 食物与农作物（重点）

### 3.1 核心循环

- **赚钱**：Shipping Bin（卖货箱）出售作物/加工品 → Create: Numismatics 货币（cog/sprocket 等）
- **村庄**：Society 村民职业（木匠/银行家/铁匠/市场/牧羊人/渔夫/图书管理员/女巫/商人），邀请入驻、建造房屋、解锁商店
- **品质**：Quality Food + Society 品质系统，作物/农产品有 铁/金/铱 三档品质，影响售价与料理效果
- **农业设施**：温室（greenhouse）、洒水器（铜/铁/铱）、自动抚摸机（auto petter）、鱼塘（fish pond）
- **季节**：Serene Seasons（春夏秋冬），dew_drop 系列（耕地生长/洒水壶/每日天气）
- **酒窖**：Vinery 葡萄种植与陈酿，Brewery 啤酒/威士忌，HerbalBrews 茶/咖啡

### 3.2 作物清单（来自任务书「作物」章，91 任务）

- **atmospheric**（6）：`aloe_leaves`、`blood_orange`、`currant`、`orange`、`passion_fruit`、`yucca_fruit`
- **autumnity**（1）：`foul_berries`
- **beachparty**（1）：`coconut`
- **brewery**（1）：`hops`
- **etcetera**（1）：`cotton_flower`
- **farm_and_charm**（6）：`barley`、`corn`、`lettuce`、`oat`、`onion`、`strawberry`
- **farmersdelight**（3）：`cabbage`、`rice`、`tomato`
- **herbalbrews**（4）：`coffee_beans`、`green_tea_leaf`、`rooibos_leaf`、`yerba_mate_leaf`
- **minecraft**（18）：`apple`、`beetroot`、`brown_mushroom`、`cactus`、`carrot`、`chorus_fruit`、`cocoa_beans`、`glow_berries`、`melon_slice`、`nether_wart`、`pitcher_plant`、`potato`、`pumpkin`、`red_mushroom`、`sugar_cane`、`sweet_berries`、`torchflower`、`wheat`
- **moreminecarts**（1）：`glass_cactus`
- **nethervinery**（2）：`crimson_grape`、`warped_grape`
- **pamhc2trees**（11）：`bananaitem`、`cinnamonitem`、`dragonfruititem`、`hazelnutitem`、`lemonitem`、`lycheeitem`、`mangoitem`、`pawpawitem`、`peachitem`、`plumitem`、`starfruititem`
- **quark**（1）：`ancient_fruit`
- **snowyspirit**（1）：`ginger`
- **society**（11）：`ancient_fruit`、`blueberry`、`boysenberry`、`cranberry`、`crystalberry`、`eggplant`、`mana_fruit`、`mossberry`、`salmonberry`、`sparkpod`、`tubabacco_leaf`
- **supplementaries**（1）：`flax`
- **veggiesdelight**（7）：`bellpepper`、`broccoli`、`cauliflower`、`garlic`、`sweet_potato`、`turnip`、`zucchini`
- **vinery**（9）：`cherry`、`jungle_grapes_red`、`jungle_grapes_white`、`red_grape`、`savanna_grapes_red`、`savanna_grapes_white`、`taiga_grapes_red`、`taiga_grapes_white`、`white_grape`
- **vintagedelight**（4）：`cucumber`、`gearo_berry`、`ghost_pepper`、`peanut`
- **windswept**（1）：`wild_berries`

### 3.3 烹饪（任务书「烹饪」章，214 任务）

- **bakery**（32 项）：`apple_cupcake`、`apple_pie`、`baguette`、`braided_bread`、`bread`、`bread_with_jam`、`bun`、`bundt_cake`、`chocolate_cake`、`chocolate_donut`、`chocolate_gateau`、`chocolate_glazed_cookie` …
- **candlelight**（28 项）：`beef_tartare`、`beef_wellington`、`beef_with_mushroom_in_wine_and_potatoes`、`beetroot_salad`、`bolognese`、`chicken_alfredo`、`chicken_teriyaki`、`chicken_with_vegetables`、`chocolate_mousse`、`fillet_steak`、`fresh_garden_salad`、`harvest_plate` …
- **crabbersdelight**（15 项）：`bisque`、`clam_bake`、`clam_chowder`、`coral_crunch`、`crab_cakes`、`crab_legs`、`fish_stick`、`frog_leg_kebob`、`jar_of_pickles`、`seafood_gumbo`、`shrimp_fried_rice`、`shrimp_skewer` …
- **farm_and_charm**（30 项）：`bacon_with_eggs`、`baked_lamb_ham`、`barley_patties_with_potatoes`、`barley_soup`、`beef_patty_with_vegetables`、`chicken_wrapped_in_bacon`、`cooked_cod`、`cooked_salmon`、`corn_grits`、`farmer_salad`、`farmers_bread`、`farmers_breakfast` …
- **farmersdelight**（47 项）：`apple_pie`、`bacon_sandwich`、`baked_cod_stew`、`barbecue_stick`、`beef_stew`、`bone_broth`、`cabbage_rolls`、`chicken_sandwich`、`chicken_soup`、`chocolate_pie`、`cod_roll`、`cooked_rice` …
- **minecraft**（1 项）：`cake`
- **veggiesdelight**（41 项）：`beetroot_brownie_tray`、`broccoli_salad`、`broccoli_soup`、`cacciatore`、`carrot_cake`、`carrot_juice`、`cauliflower_bread`、`cauliflower_kuku`、`cauliflower_soup`、`cesar_salad`、`chicken_fajitas_wrap`、`dandelion_and_eggs` …
- **vintagedelight**（15 项）：`century_egg`、`cheese_burger`、`cheese_pasta`、`chocolate_nut_granola_bar`、`cucumber_salad`、`deluxe_burger`、`deluxe_granola_bar`、`fruity_granola_bar`、`ghostly_chili`、`oatmeal_cookie`、`overnight_oats`、`pad_thai` …

### 3.4 饮品（任务书「精酿」章，85 任务）

- **brewery**（16 项）：`beer_barley`、`beer_haley`、`beer_hops`、`beer_nettle`、`beer_oat`、`beer_wheat`、`dark_brew`、`whiskey_ak`、`whiskey_carrasconlabel`、`whiskey_cristelwalker`、`whiskey_highland_hearth`、`whiskey_jamesons_malt` …
- **herbalbrews**（12 项）：`black_tea`、`chai_tea`、`cinnamon_coffee`、`coffee`、`green_tea`、`hazelnut_coffee`、`hibiscus_tea`、`lavender_tea`、`milk_coffee`、`oolong_tea`、`rooibos_tea`、`yerba_mate_tea`
- **nethervinery**（7 项）：`blazewine_pinot`、`ghastly_grenache`、`improved_lava_fizz`、`improved_nether_fizz`、`lava_fizz`、`nether_fizz`、`netherite_nectar`
- **society**（20 项）：`ancient_cider`、`ancient_vespertine`、`beer_attunecore`、`beer_london`、`bowl_of_soul`、`dewy_star`、`dirty_chai`、`espresso`、`forks_of_blue`、`good_catawba`、`laputa_franc`、`latte` …
- **vinery**（26 项）：`aegis_wine`、`apple_cider`、`apple_wine`、`bolvar_wine`、`bottle_mojang_noir`、`chenet_wine`、`cherry_wine`、`chorus_wine`、`clark_wine`、`creepers_crush`、`cristel_wine`、`eiswein` …

### 3.5 渔业（任务书「鱼获」章，80 任务）

- **aquaculture**（34 项）：`arapaima`、`arrau_turtle`、`atlantic_cod`、`atlantic_halibut`、`atlantic_herring`、`bayad`、`blackfish`、`bluegill`、`boulti`、`box_turtle`、`brown_shrooma`、`brown_trout` …
- **crabbersdelight**（4 项）：`clam`、`clawster`、`crab`、`shrimp`
- **crittersandcompanions**（1 项）：`koi_fish`
- **minecraft**（4 项）：`cod`、`pufferfish`、`salmon`、`tropical_fish`
- **netherdepthsupgrade**（11 项）：`blazefish`、`bonefish`、`eyeball_fish`、`fortress_grouper`、`glowdine`、`lava_pufferfish`、`magmacubefish`、`obsidianfish`、`searing_cod`、`soulsucker`、`wither_bonefish`
- **society**（4 项）：`neptuna`、`nether_jelly`、`ocean_jelly`、`river_jelly`
- **unusualfishmod**（19 项）：`raw_aero_mono`、`raw_amber_goby`、`raw_bark_angelfish`、`raw_beaked_herring`、`raw_blind_sailfin`、`raw_circus_fish`、`raw_copperflame_anthias`、`raw_demon_herring`、`raw_drooping_gourami`、`raw_duality_damselfish`、`raw_eyelash`、`raw_forkfish` …

### 3.6 食物相关 mod 一览

- `farmersdelight` — Farmer's Delight 1.20.1-1.3.2
- `farm_and_charm` — [Let's Do] Farm & Charm 1.0.4
- `veggiesdelight` — Veggies Delight 1.9.3
- `vintagedelight` — Vintage Delight 0.1.6
- `crabbersdelight` — Crabber's Delight 1.1.7d
- `bakery` — [Let's Do] Bakery 2.0.3
- `candlelight` — [Let's Do] Candlelight 2.0.2
- `cozycafe` — Cozy Cafe 1.10
- `meadow` — [Let's Do] Meadow 1.3.23
- `beachparty` — [Let's Do] Beachparty 1.1.5
- `braziliandelight` — Brazilian Delight 1.1.0
- `butchercraft` — Butchercraft 2.4.1
- `displaydelight` — Display Delight Lite 0.0.1-lite
- `farmlife` — Farm Life 1.20.1-1.1.0
- `vinery` — [Let's Do] Vinery 1.4.41
- `brewery` — [Let's Do] Brewery 2.0.3
- `herbalbrews` — [Let's Do] HerbalBrews 1.0.12
- `nethervinery` — [Let's Do] NetherVinery 1.2.19
- `aquaculture` — Aquaculture 2 2.5.7
- `unusualfishmod` — Unusual Fish Mod 1.1.10
- `netherdepthsupgrade` — Nether Depths Upgrade 3.1.5-1.20
- `stardew_fishing` — Stardew Fishing 3.7
- `pamhc2trees` — Pam's HarvestCraft 2 - Trees 1.0.2
- `quality_food` — Quality Food 2.4.3
- `dew_drop_farmland_growth` — Dew Drop Farmland - Growth Edition 9.0
- `dew_drop_watering_cans` — Dew Drop Watering Cans 1.0.2
- `sereneseasons` — Serene Seasons 9.1.0.2
- `farmingforblockheads` — Farming for Blockheads 14.0.2
- `croptania` — Croptania 0.3
- `botania_seeds` — Botania Seeds 1.1.1

## 4. 任务系统

- 结构：4 个章节组（教程/社区中心/指南/收藏）+ 无分组「欢迎」章，共 30 章
- 任务类型：item 为主，另有 checkmark/stat/gamestage/observation/dimension/biome/structure
- 进度模式：`linear`（线性解锁）；`default_consume_items: false`（交任务不扣物品）
- 本地化：任务文件只存 `{ftbquests.chapter.<file>.quest<ID>.*}` 键；文本在 `kubejs/assets/ftbquestlocalizer/lang/`
- 服务端权威：服务器读 `config/ftbquests/quests/`；客户端只负责显示文本（语言文件在客户端）
- 自制内容：`chapters/twilight_forest.snbt`（暮色森林教程 30 任务，生成器 `config/ftbquests/tools/build_twilight_forest_chapter.py`）

### 章节表

| 章节文件 | 标题 | 分组 | 任务数 |
|---|---|---|---:|
| `armor_weapons__tools` | 装备 | 指南 | 38 |
| `creatures` | 生物 | 指南 | 10 |
| `tools` | 建筑工具 | 指南 | 18 |
| `transportation` | 交通 | 指南 | 20 |
| `villagers` | 村民 | 指南 | 14 |
| `artifacts` | 文物 | 收藏 | 28 |
| `banners` | 烹饪 | 收藏 | 214 |
| `crops` | 作物 | 收藏 | 91 |
| `drinks` | 精酿 | 收藏 | 85 |
| `fishing` | 鱼获 | 收藏 | 80 |
| `gems` | 宝石 | 收藏 | 15 |
| `longwings` | 蝴蝶 \& 飞蛾 | 收藏 | 85 |
| `minerals` | 矿产 | 收藏 | 48 |
| `perfection` | 至善至美 | 收藏 | 22 |
| `relics` | 遗物 | 收藏 | 26 |
| `slimes` | 史莱姆 | 收藏 | 25 |
| `botania` | IV.II - 神秘农业 | 教程 | 32 |
| `getting_started` | I - 旅程伊始 | 教程 | 23 |
| `ii__building_up_the_farm` | II - 建设农场 | 教程 | 67 |
| `iii__advanced_farming` | III - 高级农业 | 教程 | 50 |
| `iv__prismatic_farming` | IV - 五彩农业 | 教程 | 66 |
| `ivi__mechanical_farming` | IV.I - 动力农业 | 教程 | 42 |
| `twilight_forest` | V - 暮色森林 | 教程 | 30 |
| `welcome` | 欢迎 | 未分组 | 14 |
| `abandoned_farm` | 废弃农场 | 社区中心 | 2 |
| `boiler_room` | 锅炉房 | 社区中心 | 5 |
| `crafts_room` | 工坊 | 社区中心 | 6 |
| `fish_tank` | 鱼缸 | 社区中心 | 6 |
| `pantry` | 储藏室 | 社区中心 | 6 |
| `vault` | 金库 | 社区中心 | 5 |

## 5. 未使用 / 低耦合 mod

以下 mod 已随包加载，但任务书无引用、玩法未集成（可安全移除或需要另行设计内容）：

- GregTech 系：`gtceu` 及 `gtmutils`/`gtse`/`gtnn`/`moldraw`/`gcyr`/`gregic_tinkering`/`applied_greg`/`gtceuterminal` 等（另有 `gregfluxology` jar 无 mod id）
- 神秘时代系：`thaumcraft`、`thaumictinkerer`、`forbidden_magic`、`tainted_magic`
- 应用能源系：`ae2`、`appbot`（存储线实际使用 Refined Storage）
- 灾变：`cataclysm`
- 说明：暮色森林原先也无任务，现已由本仓库新增「V - 暮色森林」章节覆盖

## 6. 文件与工具索引（给 AI/开发者的接口）

| 用途 | 路径 |
|---|---|
| 任务数据 | `config/ftbquests/quests/`（chapters/*.snbt、reward_tables/*.snbt、data.snbt、chapter_groups.snbt） |
| 任务文本 | `kubejs/assets/ftbquestlocalizer/lang/zh_cn.json` / `en_us.json` |
| FTB Quests UI 汉化 | `kubejs/assets/ftbquests/lang/zh_cn.json` |
| 任务索引脚本 | 根目录 `analyze_ftb_quests.py` → `ftb_quests_map.json` / `ftb_quests_report.md` |
| TF 章节生成器 | `config/ftbquests/tools/build_twilight_forest_chapter.py` |
| TF ID 参考 | `config/ftbquests/tools/twilightforest_ids.md`（645 物品 + 101 实体） |
| mod 基准表 | `MODS_BASELINE.md`（392 jar 的日期/大小/SHA256） |
| 开发指南 | `TASK_GUIDE.md` |
| 本报告 JSON | `MODPACK_REPORT.json` |

### 约定

- ID：章节/任务/目标/奖励均为 16 位大写十六进制，全局唯一
- 任务键：`ftbquests.chapter.<章节文件名>.quest<任务ID>.title/descriptionN/task.<目标ID>.title`
- 物品 ID：`<modid>:<name>`；跨模组用标签（itemfilters/tag）
- 新增章节：照抄 `twilight_forest.snbt` 结构，字段顺序 dependencies→description→icon→id→optional→rewards→tasks→title→x→y
- 新增文本：向 zh_cn/en_us JSON 插入同键条目（保持排序、最小 diff），客户端 F3+T 生效

## 7. 完整 mod 表

| mod id | 名称 | 版本 |
|---|---|---|
| `additional_attributes` | Additional Attributes | 1.3.6 |
| `advancementplaques` | Advancement Plaques | 1.6.7 |
| `ae2` | Applied Energistics 2 | 15.4.10 |
| `ali` | AdvancedLootInfo | 1.12.0 |
| `allmusic_client` | AllMusic Client | 3.9.2 |
| `alltheleaks` | All The Leaks | 1.1.1+1.20.1-forge |
| `alternate_current` | Alternate Current | 1.7.0 |
| `ambientsounds` | AmbientSounds | 6.1.11 |
| `amendments` | Amendments | 1.20-2.2.5 |
| `apexcore` | ApexCore | 10.0.0 |
| `appbot` | Applied Botanics | 1.5.2 |
| `appleskin` | AppleSkin | 2.5.1+mc1.20.1 |
| `applied_greg` | Applied Greg | 1.0.3-fix1 |
| `aquaculture` | Aquaculture 2 | 2.5.7 |
| `architectury` | Architectury | 9.2.14 |
| `architectury` | Architectury | 9.1.12 |
| `armorstatues` | Armor Statues | 8.0.6 |
| `atmospheric` | Atmospheric | 6.1.1 |
| `attributefix` | AttributeFix | 21.0.4 |
| `automobility` | Automobility | 0.4.2+1.20.1-forge |
| `autumnity` | Autumnity | 5.0.2 |
| `badpackets` | Bad Packets | 0.4.3 |
| `bakery` | [Let's Do] Bakery | 2.0.3 |
| `balloonbox` | Balloon Box | 1.20.1-1.0.3 |
| `balm` | Balm | 7.3.38 |
| `bcc` | Better Compatibility Checker | 4.0.8 |
| `beachparty` | [Let's Do] Beachparty | 1.1.5 |
| `beautify` | Beautify | 2.0.2 |
| `betteradvancedtooltips` | Better Advanced Tooltips Backport | 1.20.1-1.2.1 |
| `betteradvancements` | Better Advancements | 0.4.2.10 |
| `betterarcheology` | Better Archeology | 1.2.1-1.20.1 |
| `biomespawnpoint` | Biome Spawn Point | 2.3 |
| `blueprint` | Blueprint | 7.1.3 |
| `bobby` | Bobby Reforged | 5.0.0 |
| `bookshelf` | Bookshelf | 20.2.13 |
| `botania` | Botania | 1.20.1-454-FORGE |
| `botania_seeds` | Botania Seeds | 1.1.1 |
| `bots_lib` | Bots Lib | 4.1 |
| `bountiful` | Bountiful | 6.0.4+1.20.1 |
| `braziliandelight` | Brazilian Delight | 1.1.0 |
| `brewery` | [Let's Do] Brewery | 2.0.3 |
| `buildinggadgets2` | Building Gadgets 2 | 1.0.7 |
| `butchercraft` | Butchercraft | 2.4.1 |
| `buzzier_bees` | Buzzier Bees | 6.0.1 |
| `bwncr` | Bad Wither No Cookie Reloaded | 3.17.2 |
| `caelus` | Caelus API | 3.2.0+1.20.1 |
| `candlelight` | [Let's Do] Candlelight | 2.0.2 |
| `carryon` | Carry On | 2.1.2.7 |
| `cataclysm` | Cataclysm Mod | 2.39 |
| `certain_questing_additions` | Certain Questing Additions | 1.2.0.2 |
| `chat_heads` | Chat Heads | 0.13.7 |
| `cherishedworlds` | Cherished Worlds | 6.1.7+1.20.1 |
| `chimes` | Chimes | 2.1.1 |
| `chunky` | Chunky | 1.3.146 |
| `citadel` | Citadel | 2.6.3 |
| `classicpipes` | Classic Pipes | 1.1.5 |
| `clayworks` | Clayworks | 3.0.4 |
| `cleanview` | CleanView | 1.20.1-v1 |
| `cloth_config` | Cloth Config v10 API | 11.1.136 |
| `clumps` | Clumps | 12.0.0.4 |
| `cluttered` | Cluttered | 3.0.3-1.20.1 |
| `collective` | Collective | 7.87 |
| `colorfulhearts` | Colorful Hearts | 4.3.16 |
| `colorwheel` | Colorwheel | 1.2.9+mc1.20.1 |
| `colorwheel_patcher` | Colorwheel Patcher | 1.0.5+mc1.20.1 |
| `com_teamresourceful_bytecodecs` | bytecodecs | 1.0.2 |
| `com_teamresourceful_yabn` | yabn | 1.0.3 |
| `comforts` | Comforts | 6.4.0+1.20.1 |
| `commonality` | Commonality | 7.0.0 |
| `commonnetworking` | Common Networking | 1.0.5-1.20.1 |
| `configuration` | Configuration | 2.2.0 |
| `connectivity` | Connectivity Mod | 1.20.1-7.2 |
| `constructionwand` | Construction Wand | 1.20.1-2.11 |
| `controllable` | Controllable | 0.21.9 |
| `controlling` | Controlling | 12.0.2 |
| `copycats` | Create: Copycats+ | 3.0.7+mc.1.20.1-forge |
| `coroutil` | CoroUtil | 1.20.1-1.3.7 |
| `cosmeticarmorreworked` | CosmeticArmorReworked | 1.20.1-v1a |
| `cozycafe` | Cozy Cafe | 1.10 |
| `crabbersdelight` | Crabber's Delight | 1.1.7d |
| `crafting_on_a_stick` | Crafting On A Stick | 1.1.5 |
| `craftingtweaks` | CraftingTweaks | 18.2.8 |
| `crash_assistant` | Crash Assistant | 1.11.10 |
| `crash_assistant` | Crash Assistant | 1.11.10 |
| `crashutilities` | Crash Utilities | 8.1.4 |
| `create` | Create | 6.0.8 |
| `create_central_kitchen` | Create: Central Kitchen | 1.5.0 |
| `create_enchantment_industry` | Create Enchantment Industry | 1.3.3-for-create-6.0.6 |
| `create_factory_abstractions` | Create Factory Abstractions | 1.4.7 |
| `create_factory_logistics` | Create Factory Logistics | 1.4.7 |
| `create_hypertube` | Create Hypertube | 0.4.0 |
| `create_mechanical_extruder` | Create Mechanical Extruder | 1.20.1-1.6.10-6.0.6 |
| `create_slime` | create_slime | 1.20 |
| `createentitycontrol` | Create:Entity Control | 0.3.8.4-6.0 |
| `createrailwaysnavigator` | Create Railways Navigator | 1.20.1-beta-0.8.5-C6 |
| `createschematicchecker` | Create:Schematic Checker | 0.21.18-6.0 |
| `createutilities` | Create Utilities | 0.3.2+1.20.1 |
| `creativecore` | CreativeCore | 2.12.32 |
| `creeperconfetti` | Creeper Confetti | 4.3 |
| `crittersandcompanions` | Critters and Companions | 1.20.1-2.3.5 |
| `croptania` | Croptania | 0.3 |
| `cupboard` | Cupboard utilities | 1.20.1-2.7 |
| `curios` | Curios API | 5.14.1+1.20.1 |
| `curious_armor_stands` | Curious Armor Stands | 1.20-5.1.0 |
| `customskinloader` | CustomSkinLoader | 14.22 |
| `dataanchor` | Data Anchor | 1.0.0.20 |
| `decorative_blocks` | Decorative Blocks | 4.1.3 |
| `deltaboxlib` | Deltabox Lib | 1.1.2 |
| `dew_drop_daily_weather` | Dew Drop Daily Weather | 1.1.1 |
| `dew_drop_farmland_growth` | Dew Drop Farmland - Growth Edition | 9.0 |
| `dew_drop_watering_cans` | Dew Drop Watering Cans | 1.0.2 |
| `diagonalblocks` | Diagonal Blocks | 8.0.6 |
| `diagonalblocks` | Diagonal Blocks | 8.0.6 |
| `diagonalfences` | Diagonal Fences | 8.1.5 |
| `diagonalwalls` | Diagonal Walls | 8.0.4 |
| `dialog` | SVDialog | 0.6 |
| `displaydelight` | Display Delight Lite | 0.0.1-lite |
| `doapi` | [Let's Do] API | 1.2.15 |
| `domesticationinnovation` | Domestication Innovation (Fixed) | 1.7.2 |
| `dragonlib` | DragonLib | 1.20.1-2.2.24 |
| `dramaticdoors` | Dramatic Doors | 1.20.1-3.3.3 |
| `drippyloadingscreen` | Drippy Loading Screen | 3.0.12 |
| `dsurround` | DynamicSurroundings-Forge | 0.3.3 |
| `ears` | Ears | 1.4.7 |
| `easy_npc` | Easy NPC | 6.1.0 |
| `easyanvils` | Easy Anvils | 8.0.2 |
| `embeddium` | Embeddium | 0.3.31+mc1.20.1 |
| `emberstextapi` | Ember's Text API | 1.4.1 |
| `emi` | EMI | 1.1.24+1.20.1+forge |
| `emojiful` | Emojiful | 4.2.0 |
| `enchdesc` | EnchantmentDescriptions | 17.1.19 |
| `entity_model_features` | Entity Model Features | 3.2.4 |
| `entity_texture_features` | Entity Texture Features | 7.1 |
| `entityjs` | EntityJS | 0.6.6-1.20.1 |
| `etcetera` | Etcetera | 1.20.1-1.1.3 |
| `etched` | Etched | 3.0.4 |
| `everycomp` | Every Compat | 1.20-2.9.24 |
| `expandability` | ExpandAbility | 9.0.4 |
| `exposure` | Exposure | 1.7.16 |
| `exposure_catalog` | Exposure Catalog | 1.0.3 |
| `extra_gauges` | Create: Extra Gauges | 2.0.7 |
| `extractinator` | Extractinator | 2.3.0 |
| `extremesoundmuffler` | Extreme Sound Muffler | 3.48 |
| `fabric-api-base` | Fabric API Base | 0.4.29+b04edc7a27 |
| `fabric-command-api-v2` | Fabric Command API (v2) | 2.2.11+b3afc78b27 |
| `fabric-events-interaction-v0` | Fabric Events Interaction (v0) | 0.6.0+b3afc78b27 |
| `fabric-lifecycle-events-v1` | Fabric Lifecycle Events (v1) | 2.2.20+b3afc78b27 |
| `fabric-networking-api-v1` | Fabric Networking API (v1) | 1.3.8+b3afc78b27 |
| `fabric_api_base` | Fabric API Base | 0.4.32+ef105b4977 |
| `fabric_api_base` | Fabric API Base | 0.4.31+ef105b4977 |
| `fabric_api_base` | Fabric API Base | 0.4.31+ef105b4977 |
| `fabric_renderer_api_v1` | Fabric Renderer API (v1) | 3.2.2+cf68abbe77 |
| `fabric_renderer_indigo` | Fabric Renderer - Indigo | 1.5.3+b5b2da4177 |
| `fallingleaves` | Fallingleaves | 2.1.2 |
| `fallingtrees` | Panda's Falling Tree's | 0.13.2 |
| `fancymenu` | FancyMenu | 3.7.0 |
| `fantasyfurniture` | Fantasy's Furniture | 9.0.0 |
| `farm_and_charm` | [Let's Do] Farm & Charm | 1.0.4 |
| `farmersdelight` | Farmer's Delight | 1.20.1-1.3.2 |
| `farmingforblockheads` | Farming for Blockheads | 14.0.2 |
| `farmlife` | Farm Life | 1.20.1-1.1.0 |
| `fasterladderclimbing` | Faster Ladder Climbing | 0.2.10 |
| `fastfurnace` | FastFurnace | 8.0.2 |
| `fastleafdecay` | Fast Leaf Decay | 32 |
| `fastpaintings` | Fast Paintings | 1.20-1.2.7 |
| `fastsuite` | Fast Suite | 5.1.2 |
| `ferritecore` | Ferrite Core | 6.0.1 |
| `findme` | FindMe | 3.2.3 |
| `flerovium` | Flerovium | 1.2.18 |
| `flywheel` | Flywheel | 1.0.5 |
| `flywheel` | Flywheel | 1.0.0 |
| `flywheel` | Flywheel | 1.0.6-beta-265 |
| `forbidden_magic` | Forbidden Magic | 0.574-1.20.1-port.0.1.0-20708 |
| `forge` | forge | fmlloader-1.20.1-47.4.23.jar |
| `fragmentum` | Fragmentum | 1.1.4 |
| `framework` | Framework | 0.7.15 |
| `ftbbackups2` | FTB Backups 2 | 1.0.23 |
| `ftbchunks` | FTB Chunks | 2001.3.6 |
| `ftblibrary` | FTB Library | 2001.2.12 |
| `ftbquestlocalizer` | FTB Quests Localizer | 3.2.3 |
| `ftbquests` | FTB Quests | 2001.4.17 |
| `ftbteams` | FTB Teams | 2001.3.2 |
| `ftbxmodcompat` | FTB XMod Compat | 2.1.3 |
| `functionalstorage` | Functional Storage | 1.20.1-1.2.13 |
| `furniture` | [Let's Do] Furniture | 1.0.4 |
| `fusion` | Fusion | 1.2.11+c |
| `gag` | Gadgets Against Grind | 3.0.0-build.13 |
| `galena_hats` | Galena Hats | 1.20.1-1.2.2 |
| `gallery` | Gallery | 1.0.3 |
| `gamediscs` | Game Discs | 0.3.2-forge |
| `gcyr` | Gregicality Rocketry | 0.2.9 |
| `geckojs` | GeckoJS | 2001forge-1.5.2 |
| `geckolib` | GeckoLib 4 | 4.8 |
| `glitchcore` | GlitchCore | 0.0.1.1 |
| `gnetum` | Gnetum | 2.4.6 |
| `golemoverhaul` | Golem Overhaul | 1.1.0 |
| `gpumemleakfix` | Gpu memory leak fix | 1.20.1-1.8 |
| `gregic_tinkering` | Gregic Tinkering | 1.3.0 |
| `gtca` | GT Community Additions | 2.2.0 |
| `gtceu` | GregTech | 7.5.3 |
| `gtceuterminal` | Gregtech Terminals | 6.8.5-fix |
| `gtmadvancedhatch` | GTMAdvancedHatch-NOVAFork | 0.2.0 |
| `gtmthings` | GTMThings | 1.6.0 |
| `gtmutils` | GregTech Modern Utilities | 2.10.2 |
| `gtnn` | GT-- | 1.3.10 |
| `gtse` | Greg Tech Simple Extension | 1.3.1 |
| `guiclock` | GUI Clock | 4.6 |
| `guideme` | GuideME | 20.1.14 |
| `hamsters` | Hamsters | 1.20.1-1.0.3 |
| `herbalbrews` | [Let's Do] HerbalBrews | 1.0.12 |
| `hobbit_hill_village` | Hobbit Hill Village | 0.0.4 |
| `hopo` | HopoBetterMineshaft | 1.2.2 |
| `horseman` | Horseman | 1.3.15 |
| `iceberg` | Iceberg | 1.1.25 |
| `immediatelyfast` | ImmediatelyFast | 1.5.5+1.20.4 |
| `immersive_paintings` | Immersive Paintings | 0.6.13+1.20.1 |
| `incontrol` | InControl | 1.20-9.4.1 |
| `irons_rpg_tweaks` | Iron's RPG Tweaks | 1.20-1.4.0 |
| `itemfilters` | Item Filters | 2001.1.0-build.59 |
| `jade` | Jade | 11.13.2+forge |
| `jadeaddons` | Jade Addons | 5.5.0+forge |
| `jeed` | Just Enough Effects Descriptions | 1.20-2.2.5 |
| `jei` | Just Enough Items | 15.20.0.129 |
| `jei` | Just Enough Items | 15.56.0.205 |
| `jmi` | JourneyMap Integration | 1.20.1-0.14-48 |
| `journeymap` | Journeymap | 5.10.3 |
| `justhammers` | Just Hammers | 2.0.3+mc1.20.1 |
| `kambrik` | Kambrik | 6.1.1+1.20.1 |
| `kiwi` | Kiwi Library | 11.9.2+forge |
| `konkrete` | Konkrete | 1.8.0 |
| `kotlinforforge` | Kotlin For Forge | 4.20.0 |
| `kotlinforforge` | Kotlin For Forge | 4.12.0 |
| `kubejs` | KubeJS | 2001.6.5-build.16 |
| `kubejs_curios` | KubeJSCurios | 1.0.4 |
| `kubejsadditions` | KubeJS Addditions (Forge) | 4.3.3 |
| `kuma_api` | KumaAPI | 20.1.12 |
| `l2library` | L2 Library | 2.4.16 |
| `labels` | Labels | 1.20-2.0.0 |
| `ldlib` | LowDragLib | 1.0.40.b |
| `ldlib` | LowDragLib | 1.0.52.a |
| `leavesbegone` | Leaves Be Gone | 8.0.0 |
| `legendarycreatures` | Legendary Creatures | 1.20.1-1.1.1.3 |
| `libtooltips` | wd's Tooltips Library | 2.3-FORGE-1.20.1 |
| `liltractor` | Little Tractor | 1.20.1-1.2 |
| `lionfishapi` | LionfishAPI | 2.4-Fix |
| `lithostitched` | Lithostitched | 1.4.11 |
| `littlejoys` | Little Joys | 20.1.14 |
| `lmft` | Load My F***ing Tags | 1.0.4+1.20.1 |
| `logbegone` | Log Begone | 1.0.8 |
| `longwings` | Longwings | 0.9.5 |
| `loot_journal` | Loot Journal | 6.1.2 |
| `lootjs` | LootJS | 1.20.1-2.13.1 |
| `lootr` | Lootr | 0.7.35.90 |
| `mantle` | Mantle | 1.11.117 |
| `maxenchantx` | Max Enchant X | 1.3 |
| `mcef` | MCEF (Minecraft Chromium Embedded Framework) | 2.1.6-1.20.1 |
| `meadow` | [Let's Do] Meadow | 1.3.23 |
| `melody` | Melody | 1.0.2 |
| `midnightlib` | MidnightLib | 1.9.2 |
| `moblassos` | Mob Lassos | 8.0.1 |
| `mod id` | mod name | mod version |
| `modernfix` | ModernFix | 5.27.8+mc1.20.1 |
| `moldraw` | GregTech Molecule Drawings | 3.4.0 |
| `moogs_structures` | Moog's Structure Lib | 1.1.0-1.20-1.20.4 |
| `moonlight` | Moonlight Library | 1.20-2.16.34 |
| `morejs` | MoreJS | 0.10.1 |
| `moreminecarts` | More Minecarts and Rails | 1.8.3 |
| `moreoverlays` | More Overlays Updated | 1.24.1 |
| `mousetweaks` | Mouse Tweaks | 2.25.1 |
| `multikulti_datagen_fixes` | Multi-Kulti | 1.20.1-1.1.5 |
| `mvs` | Moog's Voyager Structures | 5.0.4 |
| `myserveriscompatible` | MyServerIsCompatible | 1.0 |
| `mysticaloaktree` | Mystical Oak Tree | 1.20-1.11 |
| `naturescompass` | Nature's Compass | 1.20.1-1.11.2-forge |
| `neo_auth` | NeoAuth | 1.0.3 |
| `nerb` | Not Enough Recipe Book | 0.4.1 |
| `netherdepthsupgrade` | Nether Depths Upgrade | 3.1.5-1.20 |
| `netherportalfix` | NetherPortalFix | 13.0.1 |
| `nethervinery` | [Let's Do] NetherVinery | 1.2.19 |
| `nightlights` | Night Lights | 1.1 |
| `nochatreports` | No Chat Reports | 1.20.1-v2.2.2 |
| `nochatrestrictions` | No Chat Restrictions | 1.20.1-v1.0.0 |
| `numismatics` | Create: Numismatics | 1.1.0+forge-mc1.20.1 |
| `numismatics_utils` | Create: Numismatics Utils | 2.2 |
| `observable` | Observable | 4.4.1 |
| `octolib` | OctoLib | 0.5.0.1 |
| `oculus` | Oculus | 1.8.0 |
| `ok_zoomer` | Ok Zoomer | 5.4.0-beta.8 |
| `online_detector` | Online Detector | 1.20-6.0.0 |
| `oreganized` | Oreganized | 4.3.2 |
| `packetfixer` | PacketFixer | 3.3.1 |
| `pamhc2trees` | Pam's HarvestCraft 2 - Trees | 1.0.2 |
| `pandalib` | PandaLib | 0.5.2 |
| `paraglider` | Paraglider | 20.1.3 |
| `particlerain` | Particle Rain | 4.0.0-beta.10 |
| `passablefoliage` | Passable Foliage | 8.2.1 |
| `patchouli` | Patchouli | 1.20.1-84.1-FORGE |
| `patchouli` | Patchouli | 1.20.1-85-FORGE |
| `perfectplushieapi` | Perfect Plushie API | 1.0.7 |
| `perfectplushies` | Perfect Plushies | 1.13.3 |
| `pipez` | Pipez | 1.20.1-1.2.21 |
| `placebo` | Placebo | 8.6.3 |
| `platform` | Platform | 1.3.4 |
| `playeranimator` | Player Animator | 1.0.2-rc1+1.20 |
| `plonk` | Plonk | 10.0.5 |
| `polylib` | PolyLib | 2000.0.3-build.143 |
| `ponder` | Ponder | 1.0.91 |
| `ponder` | Ponder | 1.0.92 |
| `ponderjs` | PonderJS | 2.1.0 |
| `portable_blueprints` | Portable blueprints | 2.0.11 |
| `portfolio` | Portfolio | 1.20.1-1.5.0 |
| `powerfuljs` | PowerfulJS | 1.6.1 |
| `puffish_attributes` | Pufferfish's Attributes | 0.7.2 |
| `puffish_skills` | Pufferfish's Skills | 0.16.1 |
| `puzzlesaccessapi` | Puzzles Access Api | 8.0.7 |
| `puzzlesaccessapi` | Puzzles Access Api | 20.1.1 |
| `puzzlesaccessapi` | Puzzles Access Api | 8.0.7 |
| `puzzlesapi` | Puzzles Api | 8.1.4 |
| `puzzlesapi` | Puzzles Api | 8.1.4 |
| `puzzleslib` | Puzzles Lib | 8.1.33 |
| `quality_food` | Quality Food | 2.4.3 |
| `quark` | Quark | 4.0-462 |
| `questsadditions` | Quests Additions | 1.4.7 |
| `radiantgear` | Radiant Gear | 2.2.0+1.20.1 |
| `radium` | Radium | 0.12.4+git.26c9d8e |
| `railways` | Create: Steam 'n' Rails | 1.7.2+forge-mc1.20.1 |
| `rainbowoaks` | Rainbow Oaks | 1.0.0 |
| `recipeessentials` | recipeessentials mod | 1.20.1-4.0 |
| `refinedstorage` | Refined Storage | 1.12.4 |
| `refinedstorageaddons` | Refined Storage Addons | 0.10.0 |
| `refurbished_furniture` | MrCrayfish's Furniture Mod: Refurbished | 1.0.20 |
| `rehooked` | ReHooked | 1.8.3-1.20.1 |
| `relics` | Relics | 0.8.0.11 |
| `remi` | Reliable EMI | 4.6.8 |
| `resourcefulconfig` | Resourcefulconfig | 2.1.3 |
| `resourcefullib` | Resourceful Lib | 2.1.29 |
| `resourcepackoverrides` | Resource Pack Overrides | 8.0.3 |
| `rhino` | Rhino | 2001.2.3-build.10 |
| `ribbits` | Ribbits | 1.20.1-Forge-3.0.5 |
| `rottencreatures` | Rotten Creatures | 1.1.0 |
| `rsinfinitybooster` | RSInfinityBooster | 1.20.1-1.0+41 |
| `rsmixin` | Refined Storage Mixin | 1.1.0-b431-release |
| `sawmill` | Universal Sawmill | 1.20-1.4.10 |
| `scholar` | Scholar | 1.2.5.1 |
| `sdrp` | Simple Discord Rich Presence | 4.0.3-build.40+mc1.20.1 |
| `searchables` | Searchables | 1.0.3 |
| `seasonhud` | SeasonHud | 2.0.4 |
| `selectivebounds` | SelectiveBounds | 0.0.2 |
| `sereneseasons` | Serene Seasons | 9.1.0.2 |
| `sereneseasonsfix` | Serene Seasons Fix | 1.2.0 |
| `serializer_debug` | Serializer Debug | 1.0.1 |
| `serverconfigupdater` | ServerConfig Updater | 4.0.2 |
| `servercore` | ServerCore | 1.5.2+1.20.1 |
| `sewingkit` | Sewing Kit | 1.8.1 |
| `shippingbin` | ShippingBin | 4 |
| `shouldersurfing` | Shoulder Surfing Reloaded | 1.20.1-4.16.0 |
| `signpicture` | SignPicture-Rebornified | 1.0.0 |
| `simplehats` | SimpleHats | 1.20.1-0.3.2 |
| `simplemagnets` | Simple Magnets | 1.1.12 |
| `simplerecall` | Simple Recall Potion | 1.0.2 |
| `skillsexpnotifier` | SkillsEXPNotifier | 1.0-SNAPSHOT |
| `smallships` | Small Ships | 2.0.0-b1.4 |
| `smartbrainlib` | SmartBrainLib | 1.15 |
| `snowpig` | Snow Pig | 1.20.1-6.0.3 |
| `snowrealmagic` | Snow! Real Magic! | 10.7.0 |
| `snowyspirit` | Snowy Spirit | 1.20-3.0.10 |
| `snuffles` | Snuffles | 1.2.0.1 |
| `society` | Society | 1.22 |
| `society_trading` | Society Trading | 1.2.9 |
| `sodiumdynamiclights` | Sodium Dynamic Lights | 1.0.9 |
| `sodiumoptionsapi` | Sodium Options API | 1.0.10 |
| `solonion` | Spice of Life Onion | 1.4.5 |
| `sophisticatedbackpacks` | Sophisticated Backpacks | 3.24.60.1982 |
| `sophisticatedcore` | Sophisticated Core | 1.3.71.2181 |
| `sophisticatedstorage` | Sophisticated Storage | 1.4.74.1997 |
| `sophisticatedstoragecreateintegration` | Sophisticated Storage Create Integration | 0.1.22.190 |
| `spark` | spark | 1.10.53 |
| `species` | Species | 3.5 |
| `spectrelib` | SpectreLib | 0.13.15+1.20.1 |
| `splendid_slimes` | Splendid Slimes | 0.20.5 |
| `squidnoglitch` | Squid No Glitch | 1.0.3 |
| `stardew_fishing` | Stardew Fishing | 3.7 |
| `strawstatues` | Straw Statues | 8.0.3 |
| `structureessentials` | Structure Essentials mod | 1.20.1-4.8 |
| `structurify` | Structurify | 1.0.21 |
| `supermartijn642configlib` | SuperMartijn642's Config Library | 1.1.8 |
| `supermartijn642corelib` | SuperMartijn642's Core Lib | 1.1.19 |
| `supplementaries` | Supplementaries | 1.20-3.1.43 |
| `tainted_magic` | Tainted Magic | 8.1.1-1.20.1-port.0.1.0-20708 |
| `tanukidecor` | Tanuki Decor | 20.1.1.0 |
| `tconstruct` | Tinkers' Construct | 3.12.0.220 |
| `terrablender` | TerraBlender | 3.0.1.10 |
| `thaumcraft` | Thaumcraft 4R | 4.2.3.5-1.20.1-port.0.1.0-20708 |
| `thaumictinkerer` | Thaumic Tinkerer | 2.5-1.20.1-port.0.1.0-20708 |
| `tipsmod` | Tips | 12.1.9 |
| `titanium` | Titanium | 3.8.32 |
| `toastcontrol` | Toast Control | 8.0.3 |
| `toofast` | Too Fast | 0.4.3.5 |
| `toolbelt` | Tool Belt | 1.20.02 |
| `tooltipoverhaul` | Tooltip Overhaul | 1.5.0 |
| `torchmaster` | Torchmaster | 20.1.9 |
| `trashslot` | TrashSlot | 15.1.3 |
| `treechop` | HT's TreeChop | 0.19.0 |
| `trials` | Trials Chambers Reuploaded | 2.3.3 |
| `trofers` | Trofers | 5.0.2 |
| `twigs` | Twigs | 1.20.1-3.1.1 |
| `twilightdelight` | Twilight's Flavor & Delight | 2.0.13 |
| `twilightforest` | The Twilight Forest | 4.3.2508 |
| `untitledduckmod` | Untitled Duck Mod | 1.5.2 |
| `unusualfishmod` | Unusual Fish Mod | 1.1.10 |
| `vanillabackport` | VanillaBackport | 1.1.7.10 |
| `veggiesdelight` | Veggies Delight | 1.9.3 |
| `verdantvibes` | Verdant Vibes | 1.0.3-1.20.1 |
| `via_romana` | Via Romana | 2.2.2+1.20.1-forge |
| `vinery` | [Let's Do] Vinery | 1.4.41 |
| `vintagedelight` | Vintage Delight | 0.1.6 |
| `visual_keybinder` | Raw's Visual Keybinder | 1.20.1 - 0.1.7 |
| `waterframes` | WaterFrames | 2.1.20 |
| `watermedia` | WaterMedia | 2.1.34 |
| `watervision` | WaterVision | 0.1.0-alpha |
| `watut` | What Are They Up To | 1.20.1-1.2.3 |
| `waystones` | Waystones | 14.1.17 |
| `webdisplays` | WebDisplays | 2.0.1-1.20.1 |
| `whimsy_deco` | Whimsy Deco | 1.2 |
| `wildernature` | [Let's Do] Wilder Nature | 1.0.5 |
| `windswept` | Windswept | 3.0.4 |
| `worldedit` | WorldEdit | 7.2.15+6463-5ca4dff |
| `wrench_wrapper` | Wrench Wrapper | 0.6.2 |
| `xlpackets` | XXL Packets | 1.0.5 |
| `yet_another_config_lib_v3` | YetAnotherConfigLib | 3.6.6+1.20.1-forge |
| `yungsapi` | YUNG's API | 1.20-Forge-4.0.6 |
| `ywzj_midi` | Limitless Concert | 1.20.1-forge-1.9.1 |
| `zeta` | Zeta | 1.0-31 |
| `zetter` | Zetter | 0.21.7 |

