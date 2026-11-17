# -*- coding: utf-8 -*-
"""
太空探索章节生成器（Society: Sunlit Valley / 1.20.1 / GCYR 0.2.9 + GT-- 1.3.10）

用法（在整合包根目录执行）：
    python config/ftbquests/tools/build_space_chapter.py

产出：
    config/ftbquests/quests/chapters/space.snbt —— 30 个任务（内联中文，不写 lang 文件）

事实依据（逐条核对，非推测）：
    - GCYR（mods/gcyr-1.20.1-0.2.9.jar）：
        · 火箭扫描仪 = EV 多方块；发射台/座椅；基础/先进/精英 发动机与燃料罐
        · 燃料：汽油25t / 柴油18t / 火箭燃料75t / 氢10t / 氢等离子18t（每 mB 燃烧时长）
        · 行星：月球(t1)/火星·水星·金星(t2)/比邻星b(t3)；温度 113K~737K；仅地球/比邻星b有氧
        · 宇航服胸甲 = 16000mB 氧气罐；氧扩散器 IV~UV；温度阈值 裸装213~333K / 全套60~363K
        · 空间站组装机 LuV；太空电梯 ZPM+；戴森系统控制器 UV
    - GT--（mods/gtnn-1.20.1-1.3.10.jar）：
        · 重型合金锭 T1~T4（装配机 HV/EV/IV/LuV）→ 重型合金板（内爆压缩机）
        · 原重型锭配方依赖 ad_astra（本包未装）→ 由 KubeJS heavyAlloys.js 补全
        · 火箭引擎发电机 EV/IV/LuV 燃烧火箭燃料发电
    - Mekanism：电解分离器→旋转冷凝器 产出 forge:oxygen / forge:hydrogen 流体
        · GCYR 宇航服灌装检查 forge:oxygen → Mek 氧气直接可用
    - 章节放 GT 组（4A46A5E1358A80A6），order_index=18（MEK 17 之后）
    - 首个任务依赖 EV 章「EV组装机」任务 7A55CC71442CC854
    - ID 用固定随机种子生成；首位限制 0-7（FTBQ 有符号 64 位解析要求）
"""

import json
import os
import random
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
QUESTS_DIR = os.path.join(ROOT, "config", "ftbquests", "quests")
CHAPTERS_DIR = os.path.join(QUESTS_DIR, "chapters")
REWARD_TABLES_DIR = os.path.join(QUESTS_DIR, "reward_tables")
LANG_DIR = os.path.join(ROOT, "kubejs", "assets", "ftbquestlocalizer", "lang")
GROUPS_FILE = os.path.join(QUESTS_DIR, "chapter_groups.snbt")
CHAPTER_FILE = os.path.join(CHAPTERS_DIR, "space.snbt")

CHAPTER_FILENAME = "space"
CHAPTER_ORDER = 18
CHAPTER_ICON = "gcyr:rocket_scanner"
GROUP_TITLE = ("太空探索", "Space")
CHAPTER_GROUP = "4A46A5E1358A80A6"  # GT 组

SEED = 20260918

# 章节背景图（FTB Library：以 .png 结尾的 image 字符串按完整纹理路径解析）
# 纹理文件：kubejs/assets/society/textures/quests/space/*.png
# 尺寸按 1 单位 = 24px 换算（640/24≈26.7），四张图纵向铺满四个阶段
CHAPTER_IMAGES = [
    dict(image="society:textures/quests/space/space.png", x=9.0, y=0.0, width=25.6, height=14.4),
]

# =====================================================================
# 任务数据（17 个；坐标 2D 网格 x:0~7.5 / y:0~10）
# =====================================================================
QUESTS = [
    dict(key="scanner", title=["太空时代：火箭扫描仪", "The Space Age: Rocket Scanner"],
         desc=[
               ("造出&6火箭扫描仪&r（EV 多方块）：用发射台搭出底座、不锈钢框架搭出塔身（JEI 可查结构）。",
                "Build the &6Rocket Scanner&r (EV multiblock): launch pads as the base, stainless steel frames as the tower."),
               ("在发射台上用火箭部件搭出火箭，然后点扫描仪界面的&6「扫描火箭」&r——整枚火箭会变成可发射的实体。",
                "Build a rocket from parts on the pad, then press &6Scan Rocket&r to turn it into a launchable entity."),
               ("本整合包中火箭部件需要&6GT-- 的重型合金板&r，先准备 T1 重型合金。",
                "In this pack rocket parts require &6GT-- heavy alloy plates&r - start with T1.")
         ],
         icon="gcyr:rocket_scanner", x=0.0, y=0.0, deps=[],
         tasks=[{"type": "item", "item": "gcyr:rocket_scanner"}],
         rewards=[{"item": "numismatics:cog", "count": 32}]),
    dict(key="pad", title=["发射台与座椅", "Launch Pad & Seat"],
         desc=[
               ("发射台是火箭的着陆面，也是扫描仪结构的底座；座椅是乘员位——没有座椅的火箭只能运货。",
                "Launch Pads form the rocket's base; Seats carry passengers - without one a rocket is cargo-only."),
               ("按需多做一批：发射台可以铺成任意大小的平台。",
                "Craft a batch - pads can be laid out as any size platform.")
         ],
         icon="gcyr:launch_pad", x=3.0, y=0.0, deps=["scanner"],
         tasks=[{"type": "item", "item": "gcyr:launch_pad"}, {"type": "item", "item": "gcyr:seat"}],
         rewards=[{"item": "numismatics:cog", "count": 16}]),
    dict(key="heavy1", title=["T1 重型合金", "T1 Heavy Alloy"],
         desc=[
               ("&6GT--&r 的重型合金链：用&6装配机（HV）&r把黄铜/铝/钢的致密板与不锈钢液压成&6T1 重型合金锭&r。",
                "&6GT--&r heavy alloy chain: compress brass/aluminium/steel dense plates with stainless steel in an &6HV Assembler&r into &6T1 Heavy Ingots&r."),
               ("再把重型锭送进&6内爆压缩机&r（需要炸药）得到&6T1 重型合金板&r——火箭发动机与燃料罐都要用它。",
                "Then implosion-compress the ingots (needs explosives) into &6T1 Heavy Plates&r - required by rocket motors and fuel tanks.")
         ],
         icon="gtnn:heavy_plate_t1", x=6.0, y=0.0, deps=["pad"],
         tasks=[{"type": "item", "item": "gtnn:heavy_ingot_t1"}, {"type": "item", "item": "gtnn:heavy_plate_t1"}],
         rewards=[{"item": "numismatics:cog", "count": 24}]),
    dict(key="motor1", title=["基础火箭发动机", "Basic Rocket Motor"],
         desc=[
               ("装配机（HV）：4×动力推进器 + 6×Kapton-K 板 + 不锈钢框架 + &6T1 重型合金板&r。",
                "HV Assembler: 4 Power Thrusters + 6 Kapton-K Plates + Stainless Frame + &6T1 Heavy Plates&r."),
               ("基础发动机：载重 25、单发动机——刚好够一次月球往返。",
                "Basic motor: carry weight 25, single motor - just enough for a Luna round trip.")
         ],
         icon="gcyr:basic_rocket_motor", x=6.0, y=-6.0, deps=["heavy1"],
         tasks=[{"type": "item", "item": "gcyr:basic_rocket_motor"}],
         rewards=[{"item": "numismatics:cog", "count": 32}]),
    dict(key="tank1", title=["基础燃料储罐", "Basic Fuel Tank"],
         desc=[
               ("装配机（HV）：2×不锈钢桶 + 6×Kapton-K 板 + 不锈钢框架 + &6T1 重型合金板&r。",
                "HV Assembler: 2 Stainless Steel Drums + 6 Kapton-K Plates + Stainless Frame + &6T1 Heavy Plates&r."),
               ("容量 5000 mB——月球往返需要 8 桶燃料，记得带够。",
                "Capacity 5000 mB - a Luna round trip needs 8 buckets of fuel.")
         ],
         icon="gcyr:basic_fuel_tank", x=9.0, y=-6.0, deps=["heavy1"],
         tasks=[{"type": "item", "item": "gcyr:basic_fuel_tank"}],
         rewards=[{"item": "numismatics:cog", "count": 32}]),
    dict(key="fuel", title=["火箭燃料", "Rocket Fuel"],
         desc=[
               ("GCYR 接受多种燃料（每 mB 燃烧时长）：&6汽油 25 / 柴油 18 / 火箭燃料 75 / 氢 10 / 氢等离子 18&r。",
                "GCYR fuels (burn time per mB): &6Gasoline 25 / Diesel 18 / Rocket Fuel 75 / Hydrogen 10 / Hydrogen Plasma 18&r."),
               ("&6Mek 联动&r：电解分离器产氢 → 旋转冷凝器出液态氢，直接当火箭燃料；GT-- 的 RP-1/UDMH 等高级燃料也能用。",
                "&6Mek link&r: Electrolytic Separator hydrogen -> Rotary Condensentrator liquid hydrogen works as rocket fuel; GT-- fuels (RP-1/UDMH...) also work."),
               ("准备好至少 8 桶燃料再发射。",
                "Prepare at least 8 buckets before launch.")
         ],
         icon="gcyr:basic_fuel_tank", x=9.0, y=0.0, deps=["motor1", "tank1"],
         tasks=[{"type": "checkmark", "title": ["准备好 8 桶火箭燃料", "Prepare 8 buckets of rocket fuel"]}],
         rewards=[{"item": "numismatics:cog", "count": 24}]),
    dict(key="assemble", title=["组装第一枚火箭", "Assemble Your First Rocket"],
         desc=[
               ("在发射台上搭好火箭（发动机+燃料罐+座椅），用扫描仪扫描成实体，右键加注燃料。",
                "Build the rocket on the pads (motor + tank + seat), scan it into an entity, then right-click to fuel it."),
               ("放入&6ID 芯片&r选择目的地；倒计时 200 刻后发射。",
                "Insert an &6ID Chip&r to pick a destination; the launch countdown is 200 ticks.")
         ],
         icon="gcyr:rocket_scanner", x=12.0, y=0.0, deps=["fuel"],
         tasks=[{"type": "checkmark", "title": ["用扫描仪组装出一枚可发射的火箭", "Scan a complete, launchable rocket"]}],
         rewards=[{"item": "numismatics:cog", "count": 48}]),
    dict(key="suit", title=["宇航服四件套", "Space Suit"],
         desc=[
               ("航空织物 = PTFE + 芳纶 + PBI 箔 + 玻璃纤维；头盔/胸甲/护腿/靴子各一件。",
                "Space Fabric = PTFE + Para-Aramid + PBI foils + Fiberglass; craft helmet, chestplate, leggings and boots."),
               ("胸甲内置 &616000 mB 氧气罐&r——用流体罐或 Mek 氧气给它充氧。",
                "The chestplate holds a &616000 mB oxygen tank&r - fill it from a fluid tank or Mek oxygen."),
               ("只有穿齐四件套，氧气才会生效。",
                "Oxygen only works with the full four-piece set.")
         ],
         icon="gcyr:space_chestplate", x=0.0, y=-6.0, deps=["pad"],
         tasks=[{"type": "item", "item": "gcyr:space_helmet"}, {"type": "item", "item": "gcyr:space_chestplate"}, {"type": "item", "item": "gcyr:space_leggings"}, {"type": "item", "item": "gcyr:space_boots"}],
         rewards=[{"item": "numismatics:cog", "count": 32}]),
    dict(key="oxygen", title=["氧气供应（Mek 联动）", "Oxygen Supply (Mek)"],
         desc=[
               ("&6电解分离器&r把水分解成氧与氢，&6旋转冷凝器&r把氧气转成液态氧。",
                "The &6Electrolytic Separator&r splits water into oxygen and hydrogen; the &6Rotary Condensentrator&r liquefies it."),
               ("GCYR 宇航服直接认&6forge:oxygen&r 流体标签——Mek 氧气无需转换即可灌装。",
                "GCYR suits accept the &6forge:oxygen&r fluid tag - Mek oxygen fills them directly.")
         ],
         icon="mekanism:electrolytic_separator", x=3.0, y=-6.0, deps=["suit"],
         tasks=[{"type": "item", "item": "mekanism:electrolytic_separator"}, {"type": "item", "item": "mekanism:rotary_condensentrator"}],
         rewards=[{"item": "numismatics:cog", "count": 24}]),
    dict(key="moon", title=["首飞：月球", "First Flight: Luna"],
         desc=[
               ("目的地选&6月球（gcyr:luna）&r：无大气、无氧气、113K、重力 1.625。",
                "Destination &6Luna&r: no atmosphere, no oxygen, 113K, gravity 1.625."),
               ("带上氧气、燃料与备用宇航服——这是你的第一次出地球。",
                "Bring oxygen, fuel and a spare suit - your first trip off Earth.")
         ],
         icon="gcyr:moon_stone", x=15.0, y=0.0, deps=["assemble", "oxygen"],
         tasks=[{"type": "checkmark", "title": ["乘火箭抵达月球", "Reach Luna by rocket"]}],
         rewards=[{"item": "numismatics:cog", "count": 64}]),
    dict(key="moon_res", title=["月球资源", "Lunar Resources"],
         desc=[
               ("月石、月沙与月海表层土都是月球建材；月球矿脉由 GT 矿脉系统生成。",
                "Lunar Stone, Sand and Mare Regolith are building materials; ores spawn via GT's vein system."),
               ("想长期驻留？带一套&6氧气扩散器&r来建立呼吸区。",
                "Staying long? Bring an &6Oxygen Spreader&r to create a breathable zone.")
         ],
         icon="gcyr:lunar_mare_regolith", x=12.0, y=-6.0, deps=["moon"],
         tasks=[{"type": "item", "item": "gcyr:moon_stone"}, {"type": "item", "item": "gcyr:lunar_mare_regolith"}, {"type": "item", "item": "gcyr:moon_sand"}],
         rewards=[{"item": "numismatics:cog", "count": 24}]),
    dict(key="spreader", title=["氧气扩散器", "Oxygen Spreader"],
         desc=[
               ("IV/LuV/ZPM/UV 四档；把氧气（或空气）灌进机器，它会给密闭空间充氧（气闸门+防洪填充判定）。",
                "Available in IV/LuV/ZPM/UV; feed it oxygen (or air) to oxygenate sealed rooms (airlock doors + flood-fill rules)."),
               ("&6Mek 联动&r：KubeJS 已给扩散器补上 Mek 氧气配方，直接连通你的电解产线。",
                "&6Mek link&r: KubeJS adds Mek oxygen recipes to the spreader - connect it straight to your electrolysis line."),
               ("气泡内温度恒定为 293K，是行星基地的核心。",
                "Inside the bubble the temperature is a comfortable 293K - the heart of any planetary base.")
         ],
         icon="gcyr:iv_oxygen_spreader", x=15.0, y=-6.0, deps=["moon_res"],
         tasks=[{"type": "item", "item": "gcyr:iv_oxygen_spreader"}],
         rewards=[{"item": "numismatics:cog", "count": 32}]),
    dict(key="thermal", title=["温度防护", "Thermal Protection"],
         desc=[
               ("裸装耐受 213~333K；全套宇航服 60~363K——水星 440K、金星 737K 都超出范围。",
                "Bare armor tolerates 213-333K; a full suit 60-363K - Mercury (440K) and Venus (737K) exceed it."),
               ("用&6隔热织物&r（耐热）与&6绝缘织物&r（耐寒）配合热升级锻造模板，给每件护甲打上防护。",
                "Use &6Heat Shielding Fabric&r and &6Insulating Fabric&r with the thermal smithing template on every piece."),
               ("&6Mek 联动&r：全套 MekaSuit 已获耐热/耐寒标签，可替代织物升级。",
                "&6Mek link&r: a full MekaSuit carries heat/freeze resistance tags - an alternative to fabric upgrades.")
         ],
         icon="gcyr:heat_shielding_fabric", x=18.0, y=-6.0, deps=["moon"],
         tasks=[{"type": "item", "item": "gcyr:heat_shielding_fabric"}, {"type": "item", "item": "gcyr:insulating_fabric"}, {"type": "item", "item": "gcyr:space_suit_thermal_upgrade_smithing_template"}],
         rewards=[{"item": "numismatics:cog", "count": 24}]),
    dict(key="heavy2", title=["T2 重型合金与先进火箭", "T2 Alloy & Advanced Rocket"],
         desc=[
               ("T2 重型锭 = T1 锭 + 钛致密板 + 钨钢液（装配机 EV）；再内爆成&6T2 重型合金板&r。",
                "T2 ingots = T1 + titanium dense plates + tungstensteel (EV Assembler); implosion-compress into &6T2 Heavy Plates&r."),
               ("先进发动机（载重 50、2 台）与先进燃料罐（7000 mB）都需要 T2 板。",
                "Advanced motors (weight 50, 2 engines) and tanks (7000 mB) need T2 plates.")
         ],
         icon="gtnn:heavy_plate_t2", x=18.0, y=0.0, deps=["thermal"],
         tasks=[{"type": "item", "item": "gtnn:heavy_plate_t2"}, {"type": "item", "item": "gcyr:advanced_rocket_motor"}, {"type": "item", "item": "gcyr:advanced_fuel_tank"}],
         rewards=[{"item": "numismatics:cog", "count": 48}]),
    dict(key="mars", title=["火星", "Mars"],
         desc=[
               ("火星：火箭等级 2、薄大气、无氧、208K、重力 3.72。",
                "Mars: rocket tier 2, thin atmosphere, no oxygen, 208K, gravity 3.72."),
               ("火星岩与表层土是红色建材；矿脉同样来自 GT 系统。",
                "Martian rock and regolith make red building blocks; ores come from GT veins.")
         ],
         icon="gcyr:martian_rock", x=15.0, y=-3.0, deps=["heavy2"],
         tasks=[{"type": "item", "item": "gcyr:martian_rock"}],
         rewards=[{"item": "numismatics:cog", "count": 32}]),
    dict(key="mercury", title=["水星", "Mercury"],
         desc=[
               ("水星：等级 2、无大气、440K（必须耐热）、重力 3.7。",
                "Mercury: tier 2, no atmosphere, 440K (heat protection required), gravity 3.7."),
               ("太阳能丰富（19）——适合建太阳能阵列。",
                "Rich solar power (19) - a great spot for solar arrays.")
         ],
         icon="gcyr:mercury_rock", x=18.0, y=3.0, deps=["heavy2"],
         tasks=[{"type": "item", "item": "gcyr:mercury_rock"}],
         rewards=[{"item": "numismatics:cog", "count": 32}]),
    dict(key="venus", title=["金星", "Venus"],
         desc=[
               ("金星：等级 2、浓大气、737K（最高温）、重力 8.87——没有耐热防护寸步难行。",
                "Venus: tier 2, thick atmosphere, 737K (hottest), gravity 8.87 - heat protection is mandatory."),
               ("金星沙与岩石偏黄，适合做基地外墙。",
                "Venusian sand and rock are yellowish - good base walls.")
         ],
         icon="gcyr:venus_rock", x=12.0, y=-3.0, deps=["heavy2"],
         tasks=[{"type": "item", "item": "gcyr:venus_rock"}],
         rewards=[{"item": "numismatics:cog", "count": 32}]),
    dict(key="gps", title=["GPS 卫星", "GPS Satellite"],
         desc=[
               ("把卫星放进火箭的卫星槽发射入轨；GPS 卫星配合&6GPS 跟踪器&r可追踪实体。",
                "Launch satellites from the rocket's satellite slot; GPS satellites track entities with the &6GPS Tracker&r.")
         ],
         icon="gcyr:gps_satellite", x=9.0, y=-3.0, deps=["mars"],
         tasks=[{"type": "item", "item": "gcyr:gps_satellite"}],
         rewards=[{"item": "numismatics:cog", "count": 24}]),
    dict(key="orefinder", title=["寻矿卫星", "Ore Finder Satellite"],
         desc=[
               ("寻矿卫星按 32×32×32 区块扫描行星矿石（#ores），为你标记矿脉位置。",
                "The Ore Finder Satellite scans 32x32x32 chunks for ores (#ores) and marks veins for you.")
         ],
         icon="gcyr:ore_finder_satellite", x=6.0, y=-3.0, deps=["mars"],
         tasks=[{"type": "item", "item": "gcyr:ore_finder_satellite"}],
         rewards=[{"item": "numismatics:cog", "count": 24}]),
    dict(key="laser", title=["激光卫星", "Laser Satellite"],
         desc=[
               ("激光卫星可对地攻击实体或定点挖掘——危险但高效。",
                "Laser Satellites strike entities or mine at a target - dangerous but efficient.")
         ],
         icon="gcyr:laser_satellite", x=3.0, y=-3.0, deps=["mars"],
         tasks=[{"type": "item", "item": "gcyr:laser_satellite"}],
         rewards=[{"item": "numismatics:cog", "count": 24}]),
    dict(key="heavy3", title=["T3 重型合金与精英火箭", "T3 Alloy & Elite Rocket"],
         desc=[
               ("T3 重型锭 = T2 锭 + 钨钢致密板 + 铂液（装配机 IV）；内爆成&6T3 重型合金板&r。",
                "T3 ingots = T2 + tungstensteel dense plates + platinum (IV Assembler); implosion-compress into &6T3 Heavy Plates&r."),
               ("精英发动机（载重 75、3 台）与精英燃料罐（12000 mB）都需要 T3 板。",
                "Elite motors (weight 75, 3 engines) and tanks (12000 mB) need T3 plates.")
         ],
         icon="gtnn:heavy_plate_t3", x=15.0, y=3.0, deps=["mars"],
         tasks=[{"type": "item", "item": "gtnn:heavy_plate_t3"}, {"type": "item", "item": "gcyr:elite_rocket_motor"}, {"type": "item", "item": "gcyr:elite_fuel_tank"}],
         rewards=[{"item": "numismatics:cog", "count": 64}]),
    dict(key="proxima", title=["比邻星 b", "Proxima Centauri B"],
         desc=[
               ("比邻星 b：火箭等级 3、有大气与&6氧气&r、303K——另一颗恒星系里的可居住世界。",
                "Proxima Centauri B: rocket tier 3, atmosphere with &6oxygen&r, 303K - a habitable world in another star system."),
               ("跨恒星系飞行需要 26 桶燃料（同星系）——精英火箭是硬性要求。",
                "Interstellar travel needs 26 buckets of fuel - the elite rocket is mandatory.")
         ],
         icon="gcyr:proxima_centauri_b_turf", x=12.0, y=3.0, deps=["heavy3"],
         tasks=[{"type": "item", "item": "gcyr:proxima_centauri_b_turf"}],
         rewards=[{"item": "numismatics:cog", "count": 64}]),
    dict(key="station_packager", title=["空间站组装机", "Space Station Packager"],
         desc=[
               ("LuV 多方块：把搭建好的平台结构打包成&6空间站包裹&r（记录全部方块）。",
                "A LuV multiblock that packs a built platform into a &6Space Station Package&r (stores every block)."),
               ("在轨道上发射包裹即可部署空间站，最多 512 格。",
                "Launch the package in orbit to deploy the station (up to 512 blocks).")
         ],
         icon="gcyr:space_station_packager", x=9.0, y=3.0, deps=["proxima"],
         tasks=[{"type": "item", "item": "gcyr:space_station_packager"}],
         rewards=[{"item": "numismatics:cog", "count": 64}]),
    dict(key="station", title=["空间站", "Space Station"],
         desc=[
               ("把空间站包裹装进火箭发往轨道；用&6钥匙卡&r保存空间站编号，之后可随时往返。",
                "Send the package to orbit; save the station ID with a &6Keycard&r for repeat trips."),
               ("空间站是跨行星中转与工业基地的最佳选址。",
                "Space stations make ideal transit hubs and orbital industry bases.")
         ],
         icon="gcyr:space_station_package", x=6.0, y=3.0, deps=["station_packager"],
         tasks=[{"type": "item", "item": "gcyr:space_station_package"}, {"type": "item", "item": "gcyr:keycard"}],
         rewards=[{"item": "numismatics:cog", "count": 32}]),
    dict(key="gtnn_engine", title=["火箭引擎发电（GT-- 联动）", "Rocket Engines (GT--)"],
         desc=[
               ("GT-- 的&6火箭引擎发电机&r（EV/IV/LuV）燃烧火箭燃料发电。",
                "GT-- &6Rocket Engine Generators&r (EV/IV/LuV) burn rocket fuel for power."),
               ("KubeJS 已把 GCYR 的&6gtceu:rocket_fuel/汽油/柴油&r接入 GTNN 引擎——你的燃料产线现在能同时驱动火箭与电网。",
                "KubeJS bridges GCYR's &6rocket_fuel/gasoline/diesel&r into GTNN engines - your fuel line now powers both rockets and the grid.")
         ],
         icon="gtnn:ev_rocket_engine", x=0.0, y=-3.0, deps=["mars"],
         tasks=[{"type": "item", "item": "gtnn:ev_rocket_engine"}],
         rewards=[{"item": "numismatics:cog", "count": 32}]),
    dict(key="qe", title=["跨行星物流（Mek 联动）", "Interplanetary Logistics (Mek)"],
         desc=[
               ("Mek 的&6量子纠缠器&r原生支持跨维度传输物品/流体/气体——行星基地与主基地之间的物流神器。",
                "Mek's &6Quantum Entangloporter&r works across dimensions for items/fluids/gases - perfect for planetary logistics.")
         ],
         icon="mekanism:quantum_entangloporter", x=3.0, y=6.0, deps=["station"],
         tasks=[{"type": "item", "item": "mekanism:quantum_entangloporter"}],
         rewards=[{"item": "numismatics:cog", "count": 32}]),
    dict(key="mekasuit", title=["MekaSuit 耐温（Mek 联动）", "MekaSuit Thermal (Mek)"],
         desc=[
               ("本包已给全套 MekaSuit 打上&6gcyr:heat_resistant / freeze_resistant&r 标签：穿着它可在水星/金星/太空自由行动。",
                "The full MekaSuit is tagged &6gcyr:heat_resistant / freeze_resistant&r in this pack - walk Mercury, Venus and space freely."),
               ("注意：它不替代氧气系统，仍需要氧气供应或宇航服。",
                "Note: it does not replace oxygen - you still need oxygen supply or a space suit.")
         ],
         icon="mekanism:mekasuit_helmet", x=18.0, y=-3.0, deps=["thermal"],
         tasks=[{"type": "checkmark", "title": ["穿上全套 MekaSuit（已具备耐热/耐寒）", "Wear a full MekaSuit (heat/freeze resistant)"]}],
         rewards=[{"item": "numismatics:cog", "count": 48}]),
    dict(key="elevator", title=["太空电梯", "Space Elevator"],
         desc=[
               ("ZPM+ 巨型多方块：制造戴森球机械方块、太阳能电池与维护端口。",
                "A ZPM+ megastructure that builds Dyson Sphere casings, solar cells and maintenance ports."),
               ("支撑柱用波束接收器与钨钢框架——准备大量材料。",
                "Beam Receivers and tungstensteel frames - stock up.")
         ],
         icon="gcyr:space_elevator", x=3.0, y=3.0, deps=["station"],
         tasks=[{"type": "item", "item": "gcyr:space_elevator"}],
         rewards=[{"item": "numismatics:cog", "count": 64}]),
    dict(key="dyson_parts", title=["戴森球组件", "Dyson Sphere Components"],
         desc=[
               ("在太空电梯里生产&6戴森球机械方块 / 太阳能电池 / 维护端口&r，并组装&6戴森施工无人机&r（装配线 ZPM）。",
                "Produce &6Dyson Casings / Solar Cells / Maintenance Ports&r in the Space Elevator, plus &6Construction Drones&r (Assembly Line, ZPM)."),
               ("光子电池由硅岩晶圆与 LuV 电路制成。",
                "Photovoltaic Cells come from naquadah wafers and LuV circuits.")
         ],
         icon="gcyr:dyson_sphere_casing", x=0.0, y=3.0, deps=["elevator"],
         tasks=[{"type": "item", "item": "gcyr:dyson_sphere_casing"}, {"type": "item", "item": "gcyr:dyson_solar_cell"}, {"type": "item", "item": "gcyr:dyson_construction_drone"}],
         rewards=[{"item": "numismatics:cog", "count": 64}]),
    dict(key="dyson", title=["戴森球：终局", "The Dyson Sphere"],
         desc=[
               ("在轨道上建造&6戴森系统控制器&r（UV 多方块），投入组件与无人机开始建造。",
                "Build the &6Dyson System Controller&r (UV multiblock) in orbit and feed it components and drones."),
               ("建成后运行戴森球：UV/UXV 级别的持续发电——这是整合包太空线的终点。",
                "Once running, the sphere generates UV/UXV-class power - the endgame of the space line.")
         ],
         icon="gcyr:dyson_system_controller", x=0.0, y=6.0, deps=["dyson_parts"],
         tasks=[{"type": "item", "item": "gcyr:dyson_system_controller"}, {"type": "checkmark", "title": ["在轨道上建造戴森球并开始发电", "Build the Dyson Sphere in orbit and start generating"]}],
         rewards=[{"item": "numismatics:cog", "count": 64}]),
]


def collect_existing_ids():
    ids = set()
    pat = re.compile(r'\bid:\s*"([0-9A-Fa-f]{16})"')
    for d in (CHAPTERS_DIR, REWARD_TABLES_DIR):
        for fn in os.listdir(d):
            if fn.endswith(".snbt") and fn != f"{CHAPTER_FILENAME}.snbt":
                with open(os.path.join(d, fn), encoding="utf-8") as f:
                    ids.update(m.upper() for m in pat.findall(f.read()))
    with open(GROUPS_FILE, encoding="utf-8") as f:
        ids.update(m.upper() for m in pat.findall(f.read()))
    return ids


def make_id(rng, used):
    while True:
        i = "".join(rng.choice("0123456789ABCDEF") for _ in range(16))
        # FTB Quests 以有符号 64 位 long 解析 ID（Long.parseLong(s, 16)）：
        # 首位 >= 8 会溢出抛异常，加载时被游戏重新生成 → 首位必须 <= 7
        if i[0] > "7":
            i = "%X" % (int(i[0], 16) - 8) + i[1:]
        if i not in used:
            used.add(i)
            return i


def ensure_group(group_id):
    """把新分组写入 chapter_groups.snbt（内联中文标题）；已存在时确保标题为内联"""
    with open(GROUPS_FILE, encoding="utf-8") as f:
        text = f.read()
    key_ref = "{ftbquests.chapter_groups." + str(int(group_id, 16)) + ".title}"
    entry = '\t\t{ id: "' + group_id + '", title: "' + GROUP_TITLE[0] + '" }\n'
    if group_id not in text:
        marker = "\t]\n}"
        assert marker in text, "chapter_groups.snbt 结构不符合预期"
        text = text.replace(marker, entry + marker)
    elif key_ref in text:
        text = text.replace(key_ref, GROUP_TITLE[0])
    else:
        return False
    with open(GROUPS_FILE, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    return True


def build_snbt(group_id):
    rng = random.Random(SEED)
    used = collect_existing_ids()
    chapter_id = make_id(rng, used)

    for q in QUESTS:
        q["qid"] = make_id(rng, used)
        for t in q["tasks"]:
            t["tid"] = make_id(rng, used)
        for r in q.get("rewards") or []:
            r["rid"] = make_id(rng, used)

    key2id = {q["key"]: q["qid"] for q in QUESTS}

    lines = []
    lines.append("{")
    lines.append("\tdefault_hide_dependency_lines: false")
    lines.append('\tdefault_quest_shape: ""')
    lines.append(f'\tfilename: "{CHAPTER_FILENAME}"')
    lines.append(f'\tgroup: "{group_id}"')
    lines.append(f'\ticon: "{CHAPTER_ICON}"')
    lines.append(f'\tid: "{chapter_id}"')
    lines.append(f"\torder_index: {CHAPTER_ORDER}")
    lines.append("\tquest_links: [ ]")
    if CHAPTER_IMAGES:
        lines.append("\timages: [")
        for img in CHAPTER_IMAGES:
            lines.append("\t\t{")
            lines.append(f'\t\t\timage: "{img["image"]}"')
            lines.append(f'\t\t\tx: {img["x"]}d')
            lines.append(f'\t\t\ty: {img["y"]}d')
            lines.append(f'\t\t\twidth: {img["width"]}d')
            lines.append(f'\t\t\theight: {img["height"]}d')
            lines.append("\t\t\trotation: 0.0d")
            lines.append("\t\t}")
        lines.append("\t]")
    lines.append("\tquests: [")

    for q in QUESTS:
        lines.append("\t\t{")
        deps = [key2id[d] for d in q["deps"]]
        if deps:
            lines.append("\t\t\tdependencies: [" + ", ".join(f'"{d}"' for d in deps) + "]")
        desc = q.get("desc") or []
        if desc:
            lines.append("\t\t\tdescription: [")
            for i, (zh, en) in enumerate(desc):
                if i > 0:
                    lines.append('\t\t\t\t""')
                lines.append("\t\t\t\t" + json.dumps(zh, ensure_ascii=False))
            lines.append("\t\t\t]")
        lines.append(f'\t\t\ticon: "{q["icon"]}"')
        lines.append(f'\t\t\tid: "{q["qid"]}"')
        rewards = q.get("rewards") or []
        if rewards:
            lines.append("\t\t\trewards: [")
            for r in rewards:
                lines.append("\t\t\t\t{")
                if r.get("count", 1) != 1:
                    lines.append(f'\t\t\t\t\tcount: {r["count"]}')
                lines.append(f'\t\t\t\t\tid: "{r["rid"]}"')
                lines.append(f'\t\t\t\t\titem: "{r["item"]}"')
                lines.append('\t\t\t\t\ttype: "item"')
                lines.append("\t\t\t\t}")
            lines.append("\t\t\t]")
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
                lines.append("\t\t\t\ttitle: " + json.dumps(t["title"][0], ensure_ascii=False))
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
                    lines.append("\t\t\t\t\ttitle: " + json.dumps(t["title"][0], ensure_ascii=False))
                    lines.append('\t\t\t\t\ttype: "checkmark"')
                lines.append("\t\t\t\t}")
            lines.append("\t\t\t]")
        lines.append("\t\t\ttitle: " + json.dumps(q["title"][0], ensure_ascii=False))
        lines.append(f'\t\t\tx: {q["x"]}d')
        lines.append(f'\t\t\ty: {q["y"]}d')
        lines.append("\t\t}")
    lines.append("\t]")
    lines.append('\ttitle: "&b太空探索&r"')
    lines.append("}")
    return "\n".join(lines) + "\n", chapter_id


def lang_entries(group_id):
    out = {}
    out[f"ftbquests.chapter.{CHAPTER_FILENAME}.title"] = ("&5神秘时代&r - 入门", "&5Thaumcraft&r - Getting Started")
    out[f"ftbquests.chapter_groups.{int(group_id, 16)}.title"] = GROUP_TITLE
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
    with open(path, encoding="utf-8") as f:
        text = f.read()
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines = lines[:-1]
    assert lines[0].strip() == "{" and lines[-1].strip() == "}", path
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

    prefix = f"ftbquests.chapter.{CHAPTER_FILENAME}."
    group_prefix = f"ftbquests.chapter_groups.{int(GROUP_KEY_ID, 16)}."
    parsed = [(k, l) for (k, l) in parsed if not k.startswith(prefix) and not k.startswith(group_prefix)]

    new_items = []
    for k in sorted(entries):
        v = json.dumps(entries[k][lang_index], ensure_ascii=False)
        new_items.append((k, f"  {json.dumps(k, ensure_ascii=False)}: {v}"))

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
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(out) + "\n")


GROUP_KEY_ID = None


def find_existing_group():
    """复用已存在的分组：优先读章节文件的 group 字段，其次按标题匹配分组表"""
    if os.path.exists(CHAPTER_FILE):
        t = open(CHAPTER_FILE, encoding="utf-8").read()
        m = re.search(r'group:\s*"([0-9A-F]{16})"', t)
        if m:
            return m.group(1)
    t = open(GROUPS_FILE, encoding="utf-8").read()
    for m in re.finditer(r'\{ id: "([0-9A-F]{16})", title: "([^"]*)" \}', t):
        if m.group(2) == GROUP_TITLE[0]:
            return m.group(1)
    return None


def main():
    global GROUP_KEY_ID
    group_id = CHAPTER_GROUP
    GROUP_KEY_ID = group_id

    created = ensure_group(group_id)
    print(f"分组: {group_id}（{'新增' if created else '已存在/已内联'}）")

    snbt, chapter_id = build_snbt(group_id)
    with open(CHAPTER_FILE, "w", encoding="utf-8", newline="\n") as f:
        f.write(snbt)
    print(f"章节 -> {CHAPTER_FILE}  (id={chapter_id})")
    print(f"quests: {len(QUESTS)}")


if __name__ == "__main__":
    main()
