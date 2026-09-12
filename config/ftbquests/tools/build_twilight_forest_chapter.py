# -*- coding: utf-8 -*-
"""
暮色森林教程章节生成器 (Society: Sunlit Valley / 1.20.1 / Twilight Forest 4.3.2508)

用法（在整合包根目录执行）:
    python config/ftbquests/tools/build_twilight_forest_chapter.py

产出:
    1. config/ftbquests/quests/chapters/twilight_forest.snbt
    2. 向 kubejs/assets/ftbquestlocalizer/lang/zh_cn.json 与 en_us.json
       插入/覆盖 ftbquests.chapter.twilight_forest.* 本地化条目

说明:
    - 所有物品 ID 均取自 mods/twilightforest-1.20.1-4.3.2508-universal.jar
      与 TF 源码 1.20.1 分支（传送门 / 进度锁 / 地图填充 / 掉落与配方）。
    - 章节 ID、任务 ID、目标 ID、奖励 ID 使用固定随机种子生成，保证可重复。
    - 脚本可重复执行：会先移除旧的 twilight_forest 本地化条目再重新写入。
"""

import json
import os
import random
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
CHAPTERS_DIR = os.path.join(ROOT, "config", "ftbquests", "quests", "chapters")
REWARD_TABLES_DIR = os.path.join(ROOT, "config", "ftbquests", "quests", "reward_tables")
LANG_DIR = os.path.join(ROOT, "kubejs", "assets", "ftbquestlocalizer", "lang")
CHAPTER_FILE = os.path.join(CHAPTERS_DIR, "twilight_forest.snbt")

CHAPTER_ID = None  # 由种子生成
CHAPTER_FILENAME = "twilight_forest"
CHAPTER_GROUP = "457DCF55318282CA"  # 教程组
CHAPTER_ORDER = 6
CHAPTER_ICON = "twilightforest:filled_magic_map"

SEED = 20260913

# =====================================================================
# 任务数据
# 字段:
#   key       : 任务键（仅用于依赖引用）
#   title     : (中文, English)
#   desc      : [(中文, English), ...]
#   icon      : 任务图标物品 ID
#   x, y      : 章节内坐标
#   deps      : 依赖的任务 key 列表
#   tasks     : [{"type": "item", "item": ..., "count": n} 或 {"type": "checkmark", "title": (zh, en)}]
#   rewards   : [{"item": ..., "count": n}]
#   optional  : 可选任务
# =====================================================================
QUESTS = [
    dict(
        key="portal",
        title=("暮色森林之门", "The Twilight Forest Portal"),
        desc=[
            ("在2×2的水池四周种上&6花朵&r（树苗、树叶、作物也可以），再向水中投入一颗&6钻石&r。",
             "Surround a 2x2 water pool with &6flowers&r (saplings, leaves or crops also work), then throw a &6diamond&r into the water."),
            ("闪电劈下后，传送门便会开启。传送门只能建在主世界，返回传送门会出现在你进入的位置附近。",
             "Lightning will strike and the portal opens. Portals can only be built in the Overworld; the return portal appears near where you entered."),
            ("&o暮色森林并不和平，但它的宝藏值得冒险。&r",
             "&oThe Twilight Forest is not peaceful, but its treasures are worth the risk.&r"),
        ],
        icon="twilightforest:twilight_portal_miniature_structure",
        x=0.0, y=0.0,
        deps=[],
        tasks=[{"type": "checkmark", "title": ("建造传送门并进入暮色森林", "Build the portal and enter the Twilight Forest")}],
        rewards=[{"item": "minecraft:diamond", "count": 1}, {"item": "numismatics:cog", "count": 4}],
    ),
    dict(
        key="wood",
        title=("暮色森林的木材", "Twilight Timbers"),
        desc=[
            ("暮色森林有四种基础树木：&6暮色橡木&r、&6苍穹木&r、&6红树木&r与&6黑木&r，它们都能制作完整的木制套装。",
             "The Twilight Forest has four basic trees: &6Twilight Oak&r, &6Canopy&r, &6Mangrove&r and &6Darkwood&r. Each has a full wood set."),
            ("用斧头采集它们。留意&6空心原木&r——那是可以攀爬的天然梯子。",
             "Chop them with an axe. Watch for &6hollow logs&r - natural ladders you can climb."),
        ],
        icon="twilightforest:twilight_oak_log",
        x=0.0, y=2.5,
        deps=["portal"],
        tasks=[
            {"type": "item", "item": "twilightforest:twilight_oak_log", "count": 1},
            {"type": "item", "item": "twilightforest:canopy_log", "count": 1},
            {"type": "item", "item": "twilightforest:mangrove_log", "count": 1},
            {"type": "item", "item": "twilightforest:dark_log", "count": 1},
        ],
        rewards=[{"item": "numismatics:cog", "count": 4}, {"item": "twilightforest:twilight_oak_sapling", "count": 1}],
    ),
    dict(
        key="magic_map",
        title=("魔法地图", "Magic Map"),
        desc=[
            ("合成&6魔法地图核心&r：&6乌鸦羽毛&r（乌鸦掉落）+ &6火炬浆果&r（生长在暮色森林的灌木上）+ &6萤石粉&r。",
             "Craft a &6Magic Map Focus&r: &6Raven Feather&r (dropped by ravens) + &6Torchberries&r (grow on bushes in the forest) + &6Glowstone Dust&r."),
            ("用8张纸与核心合成&6空白魔法地图&r，然后在暮色森林中&6右键使用&r，将它填充为真正的魔法地图。",
             "Combine 8 paper with the focus into a &6Blank Magic Map&r, then &6right-click&r it inside the Twilight Forest to fill it."),
            ("魔法地图会标出暮色森林中所有&6地标结构&r的位置，是冒险的第一件必备品。",
             "The Magic Map marks every &6landmark structure&r - your first essential tool."),
        ],
        icon="twilightforest:filled_magic_map",
        x=0.0, y=5.0,
        deps=["wood"],
        tasks=[{"type": "item", "item": "twilightforest:filled_magic_map", "count": 1}],
        rewards=[{"item": "numismatics:cog", "count": 8}],
    ),
    dict(
        key="naga",
        title=("娜迦", "The Naga"),
        desc=[
            ("&6娜迦庭院&r是暮色森林的第一场考验。娜迦会冲撞并破坏沿途的方块，注意走位与距离。",
             "The &6Naga Courtyard&r is your first trial. The Naga charges and destroys blocks in its path - keep your distance."),
            ("击败它可获得6~11枚&6娜迦鳞片&r与&6娜迦奖杯&r。庭院没有进度锁，随时可以挑战。",
             "Defeating it yields 6-11 &6Naga Scales&r and a &6Naga Trophy&r. The courtyard has no progression lock."),
        ],
        icon="twilightforest:naga_trophy",
        x=0.0, y=7.5,
        deps=["magic_map"],
        tasks=[{"type": "item", "item": "twilightforest:naga_scale", "count": 4}],
        rewards=[{"item": "numismatics:cog", "count": 12}],
    ),
    dict(
        key="naga_armor",
        title=("娜迦鳞甲", "Naga Scale Armor"),
        desc=[
            ("用娜迦鳞片制作&6娜迦胸甲&r与&6娜迦护腿&r，它们提供可观的护甲值，是暮色森林早期性价比最高的装备。",
             "Craft the &6Naga Scale Tunic&r and &6Naga Scale Leggings&r. They offer solid protection and are the best early armor in the forest."),
        ],
        icon="twilightforest:naga_chestplate",
        x=0.0, y=10.0,
        deps=["naga"],
        tasks=[
            {"type": "item", "item": "twilightforest:naga_chestplate", "count": 1},
            {"type": "item", "item": "twilightforest:naga_leggings", "count": 1},
        ],
        rewards=[{"item": "numismatics:cog", "count": 8}],
    ),
    dict(
        key="lich",
        title=("巫妖", "The Lich"),
        desc=[
            ("&6巫妖怪塔&r需要先击败娜迦才能进入——进度保护会阻止你破坏塔内的方块、打开塔内的箱子。",
             "The &6Lich Tower&r unlocks after the Naga - enforced progression stops you from breaking blocks or opening chests inside until then."),
            ("巫妖会召唤分身并举起护盾，击破护盾后才能对它造成伤害。",
             "The Lich summons clones and raises shields; break the shields before you can hurt it."),
            ("击败它可获得&6巫妖奖杯&r与四把权杖。塔中的&6奖杯基座&r可以展示你的战利品。",
             "Defeat it for the &6Lich Trophy&r and four scepters. The &6Trophy Pedestal&r inside can display your trophies."),
        ],
        icon="twilightforest:lich_trophy",
        x=0.0, y=12.5,
        deps=["naga_armor"],
        tasks=[{"type": "item", "item": "twilightforest:lich_trophy", "count": 1}],
        rewards=[{"item": "numismatics:cog", "count": 20}],
    ),
    dict(
        key="scepters",
        title=("众杖合力", "All the Scepters"),
        desc=[
            ("巫妖的四把权杖各有妙用：&6黄昏权杖&r（瞬移）、&6僵尸权杖&r（召唤僵尸）、&6吸血权杖&r（吸取生命）、&6护盾权杖&r（防护）。",
             "The Lich's four scepters each have a use: &6Twilight&r (teleport), &6Zombie&r (summon), &6Life Draining&r (drain life) and &6Fortification&r (protect)."),
            ("权杖的使用次数有限，收集全部四把作为你实力的证明。",
             "They have limited charges. Collect all four as proof of your strength."),
        ],
        icon="twilightforest:twilight_scepter",
        x=0.0, y=15.0,
        deps=["lich"],
        tasks=[
            {"type": "item", "item": "twilightforest:twilight_scepter", "count": 1},
            {"type": "item", "item": "twilightforest:zombie_scepter", "count": 1},
            {"type": "item", "item": "twilightforest:lifedrain_scepter", "count": 1},
            {"type": "item", "item": "twilightforest:fortification_scepter", "count": 1},
        ],
        rewards=[{"item": "twilightforest:charm_of_life_1", "count": 1}],
    ),
    dict(
        key="labyrinth",
        title=("迷宫与米诺菇", "Labyrinth & Minoshroom"),
        desc=[
            ("&6迷宫地图核心&r可以在迷宫宝箱中找到，也会由&6米诺陶&r掉落。用8张纸与核心合成&6空白迷宫地图&r，在迷宫中右键填充。",
             "&6Maze Map Focuses&r are found in Labyrinth chests and dropped by &6Minotaurs&r. Combine 8 paper with one into a &6Blank Maze Map&r, then use it inside the Labyrinth."),
            ("迷宫深处的&6米诺菇&r会掉落牛头人肉与&6牛头人沙拉酱肉&r。",
             "Deep inside, the &6Minoshroom&r drops Meef and &6Meef Stroganoff&r."),
            ("迷宫中还有密室与稀有战利品，别忘了搜刮。",
             "Don't forget the vaults and rare loot hidden in the maze."),
        ],
        icon="twilightforest:minoshroom_trophy",
        x=0.0, y=17.5,
        deps=["scepters"],
        tasks=[
            {"type": "item", "item": "twilightforest:maze_map_focus", "count": 1},
            {"type": "item", "item": "twilightforest:minoshroom_trophy", "count": 1},
        ],
        rewards=[{"item": "numismatics:cog", "count": 16}],
    ),
    dict(
        key="meef",
        title=("适应酷热", "Beat the Heat"),
        desc=[
            ("吃下&6牛头人沙拉酱肉&r，你的身体将适应&6火焰沼泽&r的酷热。",
             "Eat the &6Meef Stroganoff&r to adapt to the searing heat of the &6Fire Swamp&r."),
            ("没有它，沼泽的烈焰会让你寸步难行——这是通往九头蛇的必经之路。",
             "Without it the swamp will burn you at every step - this is the only way to the Hydra."),
        ],
        icon="twilightforest:meef_stroganoff",
        x=0.0, y=20.0,
        deps=["labyrinth"],
        tasks=[{"type": "item", "item": "twilightforest:meef_stroganoff", "count": 1}],
        rewards=[{"item": "numismatics:cog", "count": 8}],
    ),
    dict(
        key="hydra",
        title=("九头蛇", "The Hydra"),
        desc=[
            ("&6九头蛇&r盘踞在火焰沼泽的巢穴中，每一颗头都会喷吐火球与烈焰。",
             "The &6Hydra&r dwells in its lair in the Fire Swamp, spitting fireballs from every head."),
            ("击败它可获得&6九头蛇奖杯&r、&6九头蛇肉排&r与&6炽热之血&r。九头蛇肉排在饥饿值见底时食用效果最佳。",
             "Defeat it for the &6Hydra Trophy&r, &6Hydra Chop&r and &6Fiery Blood&r. The chop is best eaten when you are starving."),
        ],
        icon="twilightforest:hydra_trophy",
        x=0.0, y=22.5,
        deps=["meef"],
        tasks=[
            {"type": "item", "item": "twilightforest:hydra_trophy", "count": 1},
            {"type": "item", "item": "twilightforest:hydra_chop", "count": 1},
        ],
        rewards=[{"item": "numismatics:cog", "count": 24}],
    ),
    dict(
        key="yeti",
        title=("雪怪首领", "The Alpha Yeti"),
        desc=[
            ("&6雪怪洞穴&r需要巫妖进度才能进入。雪怪首领比普通雪怪更强壮，会投掷冰块。",
             "The &6Yeti Cave&r unlocks after the Lich. The Alpha Yeti is far stronger than a common Yeti and hurls ice bombs."),
            ("击败它可获得&6雪怪首领毛皮&r与&6雪怪首领奖杯&r。",
             "Defeat it for &6Alpha Yeti Fur&r and the &6Alpha Yeti Trophy&r."),
        ],
        icon="twilightforest:alpha_yeti_trophy",
        x=0.0, y=25.0,
        deps=["hydra"],
        tasks=[
            {"type": "item", "item": "twilightforest:alpha_yeti_trophy", "count": 1},
            {"type": "item", "item": "twilightforest:alpha_yeti_fur", "count": 1},
        ],
        rewards=[{"item": "numismatics:cog", "count": 16}],
    ),
    dict(
        key="yeti_armor",
        title=("雪怪毛皮装备", "Yeti Fur Gear"),
        desc=[
            ("用&6雪怪首领毛皮&r制作雪怪装备，它们自带保护II，还能&6冻结攻击者&r。",
             "Craft Yeti gear from &6Alpha Yeti Fur&r. It comes with Protection II and &6chills attackers&r."),
            ("毛皮不够就多找几座雪怪洞穴——每只雪怪首领都会掉落6张毛皮。",
             "Need more fur? Find another Yeti Cave - every Alpha Yeti drops 6 fur."),
        ],
        icon="twilightforest:yeti_helmet",
        x=2.5, y=25.0,
        deps=["yeti"],
        tasks=[{"type": "item", "item": "twilightforest:yeti_helmet", "count": 1}],
        rewards=[{"item": "numismatics:cog", "count": 12}],
        optional=True,
    ),
    dict(
        key="snow_queen",
        title=("冰雪女王", "The Snow Queen"),
        desc=[
            ("&6极光宫殿&r矗立在冰川之巅，需要雪怪首领进度才能进入。",
             "The &6Aurora Palace&r stands atop the glacier and unlocks after the Alpha Yeti."),
            ("冰雪女王会召唤寒冰水晶与雪守卫，善用走位躲避冰弹。",
             "The Snow Queen summons ice crystals and snow guardians - keep moving to dodge the ice."),
            ("击败她可获得&6冰雪女王奖杯&r与&6极光方块&r。",
             "Defeat her for the &6Snow Queen Trophy&r and &6Aurora Blocks&r."),
        ],
        icon="twilightforest:snow_queen_trophy",
        x=0.0, y=27.5,
        deps=["yeti"],
        tasks=[
            {"type": "item", "item": "twilightforest:snow_queen_trophy", "count": 1},
            {"type": "item", "item": "twilightforest:aurora_block", "count": 1},
        ],
        rewards=[{"item": "numismatics:cog", "count": 24}],
    ),
    dict(
        key="pedestal",
        title=("蒙尘的荣耀", "Dusty Glory"),
        desc=[
            ("在&6黑暗森林遗迹&r中寻找&6奖杯基座&r，把获得的奖杯放上去，就能获得对应的&6头衔&r。",
             "Find a &6Trophy Pedestal&r in the &6Dark Forest ruins&r and place a trophy on it to earn a &6title&r."),
            ("放置奖杯也会推进暮色森林的进度。",
             "Placing a trophy also advances Twilight Forest progression."),
        ],
        icon="twilightforest:trophy_pedestal",
        x=0.0, y=30.0,
        deps=["snow_queen"],
        tasks=[{"type": "item", "item": "twilightforest:trophy_pedestal", "count": 1}],
        rewards=[{"item": "numismatics:cog", "count": 8}],
    ),
    dict(
        key="knights",
        title=("幻影骑士", "Knight Phantoms"),
        desc=[
            ("&6骑士之墓&r（哥布林骑士要塞）需要奖杯基座进度才能进入。击败所有&6幻影骑士&r，让它们安息。",
             "The &6Goblin Knight Stronghold&r unlocks after the Trophy Pedestal. Defeat every &6Knight Phantom&r to lay them to rest."),
            ("骑士掉落&6骑士金属&r，可以制作强力装备；要塞宝箱中还有稀有战利品。",
             "Knights drop &6Knightmetal&r for powerful gear, and the stronghold holds rare loot."),
            ("完成后，你将能控制&6幽冥高塔&r中的&6砷铅铁机关&r。",
             "Afterwards you can control the &6Carminite mechanisms&r of the &6Dark Tower&r."),
        ],
        icon="twilightforest:knight_phantom_trophy",
        x=0.0, y=32.5,
        deps=["pedestal"],
        tasks=[
            {"type": "item", "item": "twilightforest:knight_phantom_trophy", "count": 1},
            {"type": "item", "item": "twilightforest:knightmetal_ingot", "count": 1},
        ],
        rewards=[{"item": "numismatics:cog", "count": 24}],
    ),
    dict(
        key="ghast_trap",
        title=("高塔里的奇怪装置", "The Strange Device"),
        desc=[
            ("&6幽冥高塔&r中藏着一个&6恶魂陷阱&r。收集&6砷铅铁&r制作并激活它，让&6暮初恶魂&r陷入自己建造的机关。",
             "A &6Ghast Trap&r lies hidden in the &6Dark Tower&r. Gather &6Carminite&r to build and activate it, trapping the &6Ur-Ghast&r in its own device."),
        ],
        icon="twilightforest:ghast_trap",
        x=0.0, y=35.0,
        deps=["knights"],
        tasks=[{"type": "item", "item": "twilightforest:carminite", "count": 1}],
        rewards=[{"item": "numismatics:cog", "count": 16}],
    ),
    dict(
        key="ur_ghast",
        title=("炽厄之泪", "Fiery Tears"),
        desc=[
            ("借助恶魂陷阱削弱&6暮初恶魂&r，击败它并触碰它炽红的&6炽热之泪&r。",
             "Weaken the &6Ur-Ghast&r with the trap, then defeat it and claim its &6Fiery Tears&r."),
            ("现在你可以制作&6炽铁锭&r：炽热之血或炽热之泪 + 铁锭。炽铁工具自带&6自动烧炼&r，防具会&6灼烧攻击者&r。",
             "Now you can craft &6Fiery Ingots&r: Fiery Blood or Tears + an Iron Ingot. Fiery tools &6auto-smelt&r and armor &6burns attackers&r."),
        ],
        icon="twilightforest:ur_ghast_trophy",
        x=0.0, y=37.5,
        deps=["ghast_trap"],
        tasks=[
            {"type": "item", "item": "twilightforest:ur_ghast_trophy", "count": 1},
            {"type": "item", "item": "twilightforest:fiery_tears", "count": 1},
        ],
        rewards=[{"item": "numismatics:cog", "count": 32}],
    ),
    dict(
        key="merge",
        title=("最终进军", "The Final Push"),
        desc=[
            ("要踏足&6高原&r，你必须先击败&6九头蛇&r、&6冰雪女王&r与&6暮初恶魂&r——只有这样，高原上空的酸雨才会停歇。",
             "To set foot on the &6Highlands&r you must first defeat the &6Hydra&r, the &6Snow Queen&r and the &6Ur-Ghast&r - only then will the acid rain above the plateau stop."),
            ("检查你的奖杯，看看还缺哪一位。",
             "Check your trophies and see who is missing."),
        ],
        icon="twilightforest:uberous_soil",
        x=0.0, y=40.0,
        deps=["ur_ghast"],
        tasks=[{"type": "checkmark", "title": ("我已击败九头蛇、冰雪女王与暮初恶魂", "I have defeated the Hydra, Snow Queen and Ur-Ghast")}],
        rewards=[{"item": "numismatics:cog", "count": 32}],
    ),
    dict(
        key="troll",
        title=("让烈焰燃烧得更猛烈些吧", "Let It Burn"),
        desc=[
            ("&6巨魔洞穴&r需要三巨头进度才能进入。在洞穴深处找到&6余烬之灯&r。",
             "The &6Troll Caves&r unlock after all three bosses. Find the &6Lamp of Cinders&r deep inside."),
            ("用它焚烧掉高原前的&6荆棘高墙&r，为前进开路。",
             "Use it to burn away the &6thorn wall&r blocking the way to the Highlands."),
        ],
        icon="twilightforest:lamp_of_cinders",
        x=0.0, y=42.5,
        deps=["merge"],
        tasks=[{"type": "item", "item": "twilightforest:lamp_of_cinders", "count": 1}],
        rewards=[{"item": "numismatics:cog", "count": 24}],
    ),
    dict(
        key="beanstalk",
        title=("杰克与豆茎", "Jack and the Beanstalk"),
        desc=[
            ("&6巨魔&r会掉落&6魔豆&r，巨魔花园的宝箱中也能找到。",
             "&6Trolls&r drop &6Magic Beans&r, and more can be found in Troll Garden chests."),
            ("把魔豆种在&6肥沃泥土&r上，它会一路长到云层之上，通往云上楼阁。",
             "Plant a bean on &6Uberous Soil&r and it will grow all the way above the clouds, leading to the cloud castle."),
        ],
        icon="twilightforest:huge_stalk",
        x=0.0, y=45.0,
        deps=["troll"],
        tasks=[{"type": "item", "item": "twilightforest:magic_beans", "count": 1}],
        rewards=[{"item": "numismatics:cog", "count": 16}],
    ),
    dict(
        key="giants",
        title=("飘然云上", "Above the Clouds"),
        desc=[
            ("云层之上栖居着&6巨人&r与&6巨人矿工&r。击败巨人矿工可获得&6巨人镐&r。",
             "&6Giants&r and the &6Giant Miner&r live above the clouds. Defeat the Giant Miner for the &6Giant's Pickaxe&r."),
            ("巨人镐可以破坏&6巨型方块&r（巨型原木、巨型圆石、巨型黑曜石等），这些方块同样存在于云上楼阁中。",
             "It breaks &6giant blocks&r (giant logs, cobblestone, obsidian) - the very blocks the cloud castle is built from."),
        ],
        icon="twilightforest:giant_pickaxe",
        x=0.0, y=47.5,
        deps=["beanstalk"],
        tasks=[{"type": "item", "item": "twilightforest:giant_pickaxe", "count": 1}],
        rewards=[{"item": "numismatics:cog", "count": 32}],
    ),
    dict(
        key="end",
        title=("进度完成", "To Be Continued"),
        desc=[
            ("欢迎来到&6高原&r。在当前的暮色森林版本中，这里的内容仍在开发中，未来会继续完善。",
             "Welcome to the &6Highlands&r. In this version of the Twilight Forest this area is still under development and will be expanded in the future."),
            ("暮色森林的冒险暂时告一段落——但奖杯墙还在等着你。",
             "Your adventure pauses here - but the trophy wall is still waiting."),
        ],
        icon="twilightforest:giant_obsidian",
        x=0.0, y=50.0,
        deps=["giants"],
        tasks=[{"type": "checkmark", "title": ("抵达高原", "Reach the Highlands")}],
        rewards=[{"item": "numismatics:cog", "count": 64}],
    ),
    # ---------------- 支线 ----------------
    dict(
        key="moonworm",
        title=("月光蠕虫女王", "Moonworm Queen"),
        desc=[
            ("在&6空心矿山&r与&6高塔&r的宝箱中能找到&6月光蠕虫女王&r。",
             "The &6Moonworm Queen&r is found in &6Hollow Hill&r and &6Tower&r chests."),
            ("右键放置一只&6月光蠕虫&r作为照明，左键可以回收它。",
             "Right-click to place a &6Moonworm&r as a light source; left-click to pick it back up."),
        ],
        icon="twilightforest:moonworm_queen",
        x=-2.5, y=7.5,
        deps=["magic_map"],
        tasks=[{"type": "item", "item": "twilightforest:moonworm_queen", "count": 1}],
        rewards=[{"item": "numismatics:cog", "count": 8}],
        optional=True,
    ),
    dict(
        key="ore_magnet",
        title=("矿石磁铁", "Ore Magnet"),
        desc=[
            ("在&6空心矿山&r的宝箱中能找到&6矿石磁铁&r。",
             "The &6Ore Magnet&r is found in &6Hollow Hill&r chests."),
            ("长按右键，它会把视线前方的整条矿脉拉到你身边（每次最多24块，最远32格）。",
             "Hold right-click and it pulls a whole ore vein from up to 32 blocks away right to your feet (up to 24 blocks per use)."),
        ],
        icon="twilightforest:ore_magnet",
        x=-2.5, y=10.0,
        deps=["magic_map"],
        tasks=[{"type": "item", "item": "twilightforest:ore_magnet", "count": 1}],
        rewards=[{"item": "numismatics:cog", "count": 8}],
    ),
    dict(
        key="transformation_powder",
        title=("转换粉末", "Transformation Powder"),
        desc=[
            ("&6转换粉末&r可以让暮色森林的生物变回原版生物，也可以逆向转换——比如大角羊变羊、野猪变猪。",
             "&6Transformation Powder&r turns Twilight creatures into their vanilla counterparts, and back again - Bighorn Sheep to Sheep, Boar to Pig."),
            ("空心矿山、高塔与墓地宝箱中都能找到它。小心别对着自己的坐骑使用！",
             "Found in Hollow Hill, Tower and Graveyard chests. Don't use it on your own mount!"),
        ],
        icon="twilightforest:transformation_powder",
        x=-2.5, y=12.5,
        deps=["magic_map"],
        tasks=[{"type": "item", "item": "twilightforest:transformation_powder", "count": 1}],
        rewards=[{"item": "numismatics:cog", "count": 4}],
    ),
    dict(
        key="uncrafting",
        title=("拆解台", "Uncrafting Table"),
        desc=[
            ("用8张工作台与一个&6迷宫地图核心&r合成&6拆解台&r。",
             "Craft the &6Uncrafting Table&r from 8 crafting tables and a &6Maze Map Focus&r."),
            ("它可以拆解物品返还材料、修复装备，还能在重铸时保留附魔——全部会消耗经验。",
             "It uncrafts items, repairs gear and keeps enchantments when recrafting - all at the cost of experience."),
        ],
        icon="twilightforest:uncrafting_table",
        x=-2.5, y=17.5,
        deps=["labyrinth"],
        tasks=[{"type": "item", "item": "twilightforest:uncrafting_table", "count": 1}],
        rewards=[{"item": "numismatics:cog", "count": 8}],
    ),
    dict(
        key="quest_ram",
        title=("完美的羊", "The Quest Ram"),
        desc=[
            ("&6谜题羊&r会向你要16种颜色的羊毛。喂齐所有颜色后，它会给予你&6谜题羊奖杯&r与&6瓦解之号角&r。",
             "The &6Quest Ram&r asks for wool in all 16 colors. Feed it every color and it rewards you with the &6Quest Ram Trophy&r and the &6Crumble Horn&r."),
            ("它在&6谜题树林&r中等待着你。",
             "It waits for you in the &6Quest Grove&r."),
        ],
        icon="twilightforest:quest_ram_trophy",
        x=-5.0, y=7.5,
        deps=["magic_map"],
        tasks=[{"type": "item", "item": "twilightforest:quest_ram_trophy", "count": 1}],
        rewards=[{"item": "twilightforest:crumble_horn", "count": 1}],
    ),
    dict(
        key="magic_trees",
        title=("魔法树", "Magic Trees"),
        desc=[
            ("暮色森林中生长着四种魔法树：&6时间树&r、&6转化树&r、&6采矿树&r与&6分类树&r。",
             "Four magic trees grow in the Twilight Forest: &6Time&r, &6Transformation&r, &6Mining&r and &6Sorting&r."),
            ("树苗长成大树后会出现&6核心&r，在16格范围内分别加速时间、转化生物、自动采矿与分类物品。",
             "Their cores accelerate time, transform creatures, auto-mine or sort items within a 16-block radius."),
        ],
        icon="twilightforest:time_sapling",
        x=-5.0, y=10.0,
        deps=["magic_map"],
        tasks=[
            {"type": "item", "item": "twilightforest:time_sapling", "count": 1},
            {"type": "item", "item": "twilightforest:transformation_sapling", "count": 1},
            {"type": "item", "item": "twilightforest:mining_sapling", "count": 1},
            {"type": "item", "item": "twilightforest:sorting_sapling", "count": 1},
        ],
        rewards=[{"item": "numismatics:cog", "count": 16}],
        optional=True,
    ),
    dict(
        key="glass_sword",
        title=("会心一击", "Critical Hit"),
        desc=[
            ("&6玻璃剑&r有着极高的伤害，但一次攻击后就会碎裂。",
             "The &6Glass Sword&r deals massive damage but shatters after a single hit."),
            ("它无法合成，只能在&6极光宫殿&r的宝箱中找到。",
             "It cannot be crafted - it is only found in &6Aurora Palace&r chests."),
        ],
        icon="twilightforest:glass_sword",
        x=-5.0, y=12.5,
        deps=["snow_queen"],
        tasks=[{"type": "item", "item": "twilightforest:glass_sword", "count": 1}],
        rewards=[{"item": "numismatics:cog", "count": 4}],
        optional=True,
    ),
    dict(
        key="trophy_wall",
        title=("奖杯墙", "The Trophy Wall"),
        desc=[
            ("把暮色森林所有首领的奖杯摆在一起：娜迦、巫妖、米诺菇、九头蛇、幻影骑士、暮初恶魂、雪怪首领与冰雪女王。",
             "Bring every Twilight Forest boss trophy together: Naga, Lich, Minoshroom, Hydra, Knight Phantom, Ur-Ghast, Alpha Yeti and Snow Queen."),
            ("八座奖杯，就是你在暮色森林全部荣耀的证明。",
             "Eight trophies - the proof of all your glory in the Twilight Forest."),
        ],
        icon="twilightforest:lich_trophy",
        x=2.5, y=50.0,
        deps=["end"],
        tasks=[
            {"type": "item", "item": "twilightforest:naga_trophy", "count": 1},
            {"type": "item", "item": "twilightforest:lich_trophy", "count": 1},
            {"type": "item", "item": "twilightforest:minoshroom_trophy", "count": 1},
            {"type": "item", "item": "twilightforest:hydra_trophy", "count": 1},
            {"type": "item", "item": "twilightforest:knight_phantom_trophy", "count": 1},
            {"type": "item", "item": "twilightforest:ur_ghast_trophy", "count": 1},
            {"type": "item", "item": "twilightforest:alpha_yeti_trophy", "count": 1},
            {"type": "item", "item": "twilightforest:snow_queen_trophy", "count": 1},
        ],
        rewards=[{"item": "twilightforest:charm_of_life_2", "count": 1}, {"item": "numismatics:cog", "count": 64}],
    ),
]


def collect_existing_ids():
    ids = set()
    pat = re.compile(r'\bid:\s*"([0-9A-Fa-f]{16})"')
    for d in (CHAPTERS_DIR, REWARD_TABLES_DIR):
        for fn in os.listdir(d):
            if fn.endswith(".snbt") and fn != f"{CHAPTER_FILENAME}.snbt":
                with open(os.path.join(d, fn), encoding="utf-8") as f:
                    ids.update(m.upper() for m in pat.findall(f.read()))
    return ids


def make_id(rng, used):
    while True:
        i = "".join(rng.choice("0123456789ABCDEF") for _ in range(16))
        if i not in used:
            used.add(i)
            return i


def quest_id(quest):
    return quest["qid"]


def build_snbt():
    rng = random.Random(SEED)
    used = collect_existing_ids()
    global CHAPTER_ID
    CHAPTER_ID = make_id(rng, used)

    for q in QUESTS:
        q["qid"] = make_id(rng, used)
        for t in q["tasks"]:
            t["tid"] = make_id(rng, used)
        for r in q["rewards"]:
            r["rid"] = make_id(rng, used)

    key2id = {q["key"]: q["qid"] for q in QUESTS}

    lines = []
    lines.append("{")
    lines.append("\tdefault_hide_dependency_lines: false")
    lines.append('\tdefault_quest_shape: ""')
    lines.append(f'\tfilename: "{CHAPTER_FILENAME}"')
    lines.append(f'\tgroup: "{CHAPTER_GROUP}"')
    lines.append(f'\ticon: "{CHAPTER_ICON}"')
    lines.append(f'\tid: "{CHAPTER_ID}"')
    lines.append(f"\torder_index: {CHAPTER_ORDER}")
    lines.append("\tquest_links: [ ]")
    lines.append("\tquests: [")

    first_quest = True
    for q in QUESTS:
        if not first_quest:
            pass
        first_quest = False
        lines.append("\t\t{")
        deps = [key2id[d] for d in q["deps"]]
        if deps:
            lines.append("\t\t\tdependencies: [" + ", ".join(f'"{d}"' for d in deps) + "]")
        # description
        desc = q.get("desc") or []
        if desc:
            lines.append("\t\t\tdescription: [")
            for i, (zh, en) in enumerate(desc):
                if i > 0:
                    lines.append('\t\t\t\t""')
                lines.append(f'\t\t\t\t"{{ftbquests.chapter.{CHAPTER_FILENAME}.quest{q["qid"]}.description{i+1}}}"')
            lines.append("\t\t\t]")
        lines.append(f'\t\t\ticon: "{q["icon"]}"')
        lines.append(f'\t\t\tid: "{q["qid"]}"')
        if q.get("optional"):
            lines.append("\t\t\toptional: true")
        # rewards
        rewards = q.get("rewards") or []
        if rewards:
            lines.append("\t\t\trewards: [")
            for i, r in enumerate(rewards):
                lines.append("\t\t\t\t{")
                if r.get("count", 1) != 1:
                    lines.append(f'\t\t\t\t\tcount: {r["count"]}')
                lines.append(f'\t\t\t\t\tid: "{r["rid"]}"')
                lines.append(f'\t\t\t\t\titem: "{r["item"]}"')
                lines.append('\t\t\t\t\ttype: "item"')
                lines.append("\t\t\t\t}")
            lines.append("\t\t\t]")
        # tasks
        tasks = q["tasks"]
        if len(tasks) == 1:
            t = tasks[0]
            lines.append("\t\t\ttasks: [{")
            if t["type"] == "item":
                if t.get("count", 1) != 1:
                    lines.append(f'\t\t\t\tcount: {t["count"]}L')
                lines.append(f'\t\t\t\tid: "{t["tid"]}"')
                lines.append(f'\t\t\t\titem: "{t["item"]}"')
                lines.append('\t\t\t\ttype: "item"')
            else:
                lines.append(f'\t\t\t\tid: "{t["tid"]}"')
                lines.append(f'\t\t\t\ttitle: "{{ftbquests.chapter.{CHAPTER_FILENAME}.quest{q["qid"]}.task.{t["tid"]}.title}}"')
                lines.append('\t\t\t\ttype: "checkmark"')
            lines.append("\t\t\t}]")
        else:
            lines.append("\t\t\ttasks: [")
            for t in tasks:
                lines.append("\t\t\t\t{")
                if t["type"] == "item":
                    if t.get("count", 1) != 1:
                        lines.append(f'\t\t\t\t\tcount: {t["count"]}L')
                    lines.append(f'\t\t\t\t\tid: "{t["tid"]}"')
                    lines.append(f'\t\t\t\t\titem: "{t["item"]}"')
                    lines.append('\t\t\t\t\ttype: "item"')
                else:
                    lines.append(f'\t\t\t\t\tid: "{t["tid"]}"')
                    lines.append(f'\t\t\t\t\ttitle: "{{ftbquests.chapter.{CHAPTER_FILENAME}.quest{q["qid"]}.task.{t["tid"]}.title}}"')
                    lines.append('\t\t\t\t\ttype: "checkmark"')
                lines.append("\t\t\t\t}")
            lines.append("\t\t\t]")
        lines.append(f'\t\t\ttitle: "{{ftbquests.chapter.{CHAPTER_FILENAME}.quest{q["qid"]}.title}}"')
        lines.append(f'\t\t\tx: {q["x"]}d')
        lines.append(f'\t\t\ty: {q["y"]}d')
        lines.append("\t\t}")
    lines.append("\t]")
    lines.append("}")
    return "\n".join(lines) + "\n"


def lang_entries():
    """返回 {key: (zh, en)}"""
    out = {}
    out[f"ftbquests.chapter.{CHAPTER_FILENAME}.title"] = ("V - 暮色森林", "V - The Twilight Forest")
    for q in QUESTS:
        base = f"ftbquests.chapter.{CHAPTER_FILENAME}.quest{q['qid']}"
        out[base + ".title"] = q["title"]
        for i, (zh, en) in enumerate(q.get("desc") or []):
            out[f"{base}.description{i+1}"] = (zh, en)
        for t in q["tasks"]:
            if t["type"] == "checkmark":
                out[f"{base}.task.{t['tid']}.title"] = t["title"]
    return out


def insert_lang(path, entries, lang_index):
    """在现有 lang 文件中原位插入条目：不改动既有行，只做最小插入。"""
    with open(path, encoding="utf-8") as f:
        text = f.read()
    has_trailing_newline = text.endswith("\n")
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines = lines[:-1]
    assert lines[0].strip() == "{", path
    assert lines[-1].strip() == "}", path
    body = lines[1:-1]

    def key_of(line):
        m = re.match(r'^\s*"((?:[^"\\]|\\.)*)"\s*:', line)
        return m.group(1) if m else None

    parsed = []
    for line in body:
        k = key_of(line)
        assert k is not None, f"unexpected lang line: {line!r}"
        v = line.rstrip()
        if v.endswith(","):
            v = v[:-1]
        parsed.append((k, v))

    # 移除旧的 twilight_forest 条目（保证脚本可重复执行）
    parsed = [(k, l) for (k, l) in parsed if not k.startswith(f"ftbquests.chapter.{CHAPTER_FILENAME}.")]

    # 新条目按 key 排序
    new_items = []
    for k in sorted(entries):
        v = json.dumps(entries[k][lang_index], ensure_ascii=False)
        new_items.append((k, f"  {json.dumps(k, ensure_ascii=False)}: {v}"))

    # 插入到第一个比新键更大的既有键之前（保持既有顺序不变）
    insert_at = len(parsed)
    for i, (k, _) in enumerate(parsed):
        if k > new_items[0][0]:
            insert_at = i
            break
    parsed[insert_at:insert_at] = new_items

    out = ["{"]
    for i, (k, line) in enumerate(parsed):
        line = line.rstrip()
        if line.endswith(","):
            line = line[:-1]
        if i < len(parsed) - 1:
            line += ","
        out.append(line)
    out.append("}")
    result = "\n".join(out)
    if has_trailing_newline:
        result += "\n"
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(result)


def main():
    snbt = build_snbt()
    with open(CHAPTER_FILE, "w", encoding="utf-8", newline="\n") as f:
        f.write(snbt)
    print(f"chapter -> {CHAPTER_FILE}  (id={CHAPTER_ID})")

    entries = lang_entries()
    insert_lang(os.path.join(LANG_DIR, "zh_cn.json"), entries, 0)
    insert_lang(os.path.join(LANG_DIR, "en_us.json"), entries, 1)
    print(f"lang entries: {len(entries)} -> zh_cn.json / en_us.json")
    print(f"quests: {len(QUESTS)}")


if __name__ == "__main__":
    main()
