# -*- coding: utf-8 -*-
"""
格雷科技（GregTech）教程章节生成器 (Society: Sunlit Valley / 1.20.1 / GTCEu 7.5.3)

用法（在整合包根目录执行）:
    python config/ftbquests/tools/build_gregtech_chapter.py

产出:
    1. config/ftbquests/quests/chapters/gregtech.snbt
    2. 向 kubejs/assets/ftbquestlocalizer/lang/zh_cn.json 与 en_us.json
       插入/更新 ftbquests.chapter.gregtech.* 本地化条目

说明:
    - 本章只使用本包已存在的模组内容（gtceu + GTCA/GTMFO/GTSE/GTNN 等附属）
    - 物品 ID 均经过静态核对（GTCEu 7.5.3 lang / 附属 lang / 既有任务与脚本引用）
    - 固定随机种子生成 ID（章节 ID、任务 ID、目标 ID、奖励 ID），保证不重复
    - 脚本可重复执行：会先移除旧的 gregtech 本地化条目再重写
"""

import json
import os
import random
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
CHAPTERS_DIR = os.path.join(ROOT, "config", "ftbquests", "quests", "chapters")
REWARD_TABLES_DIR = os.path.join(ROOT, "config", "ftbquests", "quests", "reward_tables")
LANG_DIR = os.path.join(ROOT, "kubejs", "assets", "ftbquestlocalizer", "lang")
CHAPTER_FILE = os.path.join(CHAPTERS_DIR, "gregtech.snbt")

CHAPTER_ID = None  # 运行时生成
CHAPTER_FILENAME = "gregtech"
CHAPTER_GROUP = "457DCF55318282CA"  # 教程组
CHAPTER_ORDER = 7
CHAPTER_ICON = "gtceu:lv_machine_hull"

SEED = 20260914

# =====================================================================
# 任务数据
# 字段:
#   key       : 任务标识（仅用于内部依赖引用）
#   title     : (中文, English)
#   desc      : [(中文, English), ...] 可选
#   icon      : 图标物品 ID
#   x, y      : 任务坐标
#   deps      : 依赖任务 key 列表
#   tasks     : [{"type": "item", "item": ..., "count": n} 或
#               {"type": "checkmark", "title": (zh, en)}]
#   rewards   : [{"item": ..., "count": n}]
#   optional  : 可选任务
# =====================================================================
QUESTS = [
    # ================= 主线：入门 =================
    dict(
        key="intro",
        title=("格雷科技", "GregTech"),
        desc=[
            ("本包内置了 &6GregTech CEu Modern 7.5.3&r 与多个附属（GTCA / GTMFO / GTSE / GTNN / GTMM 等）。这是一条独立于农业主线的 &6工业支线&r，随时可以开始，不会阻塞你的农场进度。",
             "This pack ships &6GregTech CEu Modern 7.5.3&r plus several addons (GTCA / GTMFO / GTSE / GTNN / GTMM and more). This is an &6industrial side-line&r independent of the farming main story - start any time."),
            ("GT 的起点是 &6蒸汽时代&r：先做一套格雷工具，再用蒸汽机器处理矿石与材料。之后逐级攀爬电压：LV → MV → HV → EV → IV → LuV → ZPM → UV。",
             "GregTech starts in the &6Steam Age&r: craft the GT tool set, then process ores and materials with steam machines. From there you climb the voltage tiers: LV → MV → HV → EV → IV → LuV → ZPM → UV."),
            ("矿石是工业的粮食：本包已让 &6骷髅洞穴&r 与 &6暮色森林&r 生成 GT 矿脉（见左侧矿石分支）。地表的&6指示矿&r会提示你脚下埋着什么。",
             "Ores are the food of industry: in this pack &6Skull Cavern&r and the &6Twilight Forest&r now spawn GT ore veins (see the ore branch on the left). &6Surface indicators&r reveal what lies beneath."),
        ],
        icon="gtceu:steam_grinder",
        x=0.0, y=0.0,
        deps=[],
        tasks=[{"type": "checkmark", "title": ("开始你的工业化之路", "Begin your industrialization")}],
        rewards=[{"item": "numismatics:cog", "count": 4}],
    ),
    dict(
        key="tools",
        title=("格雷工具", "GregTech Tools"),
        desc=[
            ("GT 的合成体系依赖一套专用工具，用 &6锤子&r 敲板、&6锉刀&r 磨杆、&6锯子&r 切块、&6剪线钳&r 剪线缆、&6螺丝刀&r 调机器、&6扳手&r 拆机器、&6杵与研钵&r 粉碎、&6软锤&r 开关机器。",
             "GregTech crafting relies on a dedicated tool set: &6Hammer&r for plates, &6File&r for rods, &6Saw&r for blocks, &6Wire Cutter&r for cables, &6Screwdriver&r for machines, &6Wrench&r for dismantling, &6Mortar&r for crushing and the &6Soft Mallet&r for toggling machines."),
            ("任意一种常见金属（铁、钢、青铜等）都能制作整套工具；工具会消耗耐久，注意多备几把。",
             "Any common metal (iron, steel, bronze...) can make the full set. Tools consume durability, so keep spares."),
        ],
        icon="gtceu:iron_bolt",
        x=0.0, y=2.5,
        deps=["intro"],
        tasks=[{"type": "checkmark", "title": ("制作一套格雷工具", "Craft a full set of GT tools")}],
        rewards=[{"item": "numismatics:cog", "count": 4}],
    ),
    dict(
        key="materials",
        title=("板材与零件", "Plates and Parts"),
        desc=[
            ("工业化的第一步是把金属变成标准零件：&6锤子 + 锭 = 板&r，&6锉刀 + 板 = 杆/螺栓&r，&6锯子 + 板 = 螺丝&r，&6锤子 + 两个锭 = 齿轮&r。",
             "First step of industry: turn metal into standard parts. &6Hammer + Ingot = Plate&r, &6File + Plate = Rod/Bolt&r, &6Saw + Plate = Screw&r, &6Hammer + 2 Ingots = Gear&r."),
            ("把常用零件放进 &6钢板箱&r 或抽屉里，后面每一台机器都会用到它们。",
             "Stock common parts in &6Steel Crates&r or drawers - every machine later will need them."),
        ],
        icon="gtceu:iron_plate",
        x=0.0, y=5.0,
        deps=["tools"],
        tasks=[
            {"type": "item", "item": "gtceu:iron_plate", "count": 8},
            {"type": "item", "item": "gtceu:iron_bolt", "count": 8},
            {"type": "item", "item": "gtceu:steel_rod", "count": 4},
        ],
        rewards=[{"item": "numismatics:cog", "count": 6}],
    ),
    dict(
        key="steam_boiler",
        title=("蒸汽锅炉", "Steam Boilers"),
        desc=[
            ("&6锅炉&r 是蒸汽时代的动力源：固体锅炉烧燃料、液体锅炉烧岩浆/杂酚油、太阳能锅炉靠太阳。产出的 &6蒸汽&r 通过管道送往蒸汽机器。",
             "&6Boilers&r power the Steam Age: Solid burns fuel, Liquid burns lava/creosote, Solar relies on the sun. The &6Steam&r they produce is piped to steam machines."),
            ("小锅炉只有一格容量，建议尽早换成 &6大型锅炉&r 或多做几台。",
             "Small boilers hold little steam - upgrade to a &6Large Boiler&r or build several early."),
        ],
        icon="gtceu:lp_steam_solid_boiler",
        x=0.0, y=7.5,
        deps=["materials"],
        tasks=[
            {"type": "item", "item": "gtceu:lp_steam_solid_boiler", "count": 1},
        ],
        rewards=[{"item": "numismatics:cog", "count": 6}],
    ),
    dict(
        key="steam_machines",
        title=("蒸汽机器", "Steam Machines"),
        desc=[
            ("蒸汽机器把矿石变成材料：&6蒸汽打粉机&r、&6蒸汽锻锤&r、&6蒸汽合金炉&r、&6蒸汽压缩机&r 是最常用的四台。",
             "Steam machines process ores into materials: the &6Steam Macerator&r, &6Steam Forge Hammer&r, &6Steam Alloy Smelter&r and &6Steam Compressor&r are the workhorses."),
            ("普通蒸汽机器只有一半速度，&6高压（HP）版本&r没有速度惩罚——燃料够用后优先升级。",
             "Regular steam machines run at half speed; &6High Pressure (HP)&r versions have no penalty - upgrade once fuel allows."),
        ],
        icon="gtceu:lp_steam_macerator",
        x=0.0, y=10.0,
        deps=["steam_boiler"],
        tasks=[
            {"type": "item", "item": "gtceu:lp_steam_macerator", "count": 1},
            {"type": "item", "item": "gtceu:lp_steam_forge_hammer", "count": 1},
            {"type": "item", "item": "gtceu:lp_steam_alloy_smelter", "count": 1},
            {"type": "item", "item": "gtceu:lp_steam_compressor", "count": 1},
        ],
        rewards=[{"item": "numismatics:cog", "count": 8}],
    ),
    dict(
        key="pbf",
        title=("原始高炉", "Primitive Blast Furnace"),
        desc=[
            ("&6原始高炉&r 是 GT 的第一台多方块：用 &6铁锭 + 砖块&r 搭建，燃料用 &6煤炭/木炭&r，一次能烧出 &6钢锭&r。",
             "The &6Primitive Blast Furnace&r is GT's first multiblock: build it from &6Iron Ingots + Bricks&r, fuel it with &6Coal/Charcoal&r and smelt &6Steel Ingots&r."),
            ("它还能把铁锭烧成钢、把煤烧成焦炭（需要 &6焦炉&r 更好）。",
             "It also turns iron into steel, and coal into coke (the &6Coke Oven&r is better at that)."),
        ],
        icon="gtceu:primitive_blast_furnace",
        x=0.0, y=12.5,
        deps=["steam_machines"],
        tasks=[{"type": "item", "item": "gtceu:primitive_blast_furnace", "count": 1}],
        rewards=[{"item": "numismatics:cog", "count": 8}],
    ),
    dict(
        key="steel",
        title=("钢", "Steel"),
        desc=[
            ("&6钢&r 是进入电力时代的门票：机器外壳、工具、管道都要它。",
             "&6Steel&r is your ticket to the electric age: machine hulls, tools and pipes all need it."),
            ("把钢锭做成 &6钢板&r、&6钢杆&r 备用；&6钢齿轮箱&r 是很多多方块的核心部件。",
             "Turn steel into &6Steel Plates&r and &6Steel Rods&r; the &6Steel Gearbox&r is a core part of many multiblocks."),
        ],
        icon="gtceu:steel_ingot",
        x=0.0, y=15.0,
        deps=["pbf"],
        tasks=[
            {"type": "item", "item": "gtceu:steel_ingot", "count": 16},
            {"type": "item", "item": "gtceu:steel_plate", "count": 8},
        ],
        rewards=[{"item": "numismatics:cog", "count": 8}],
    ),
    dict(
        key="coke_oven",
        title=("焦炉", "Coke Oven"),
        desc=[
            ("&6焦炉&r 把煤炭变成 &6焦炭&r（更好的燃料）并副产 &6杂酚油&r（液体锅炉的燃料、后期化工原料）。",
             "The &6Coke Oven&r turns coal into &6Coke&r (a better fuel) and produces &6Creosote&r as a byproduct (fuel for liquid boilers, chemical feedstock later)."),
            ("焦炉本身是多方块，用 &6焦炉砖&r 搭建；产出的杂酚油记得用桶或储罐接住。",
             "The Coke Oven is a multiblock built from &6Coke Oven Bricks&r; catch the creosote with buckets or tanks."),
        ],
        icon="gtceu:coke_oven",
        x=0.0, y=17.5,
        deps=["steel"],
        tasks=[{"type": "item", "item": "gtceu:coke_oven", "count": 1}],
        rewards=[{"item": "numismatics:cog", "count": 8}],
    ),
    dict(
        key="lv_power",
        title=("低压电力", "Low Voltage Power"),
        desc=[
            ("进入 &6LV（低压）&r 后，能源从蒸汽变成 &6EU&r：&6蒸汽涡轮&r 把蒸汽转成电，&6燃烧发电机&r 直接烧燃料，&6燃气涡轮&r 烧气体燃料。",
             "In &6LV (Low Voltage)&r power becomes &6EU&r: the &6Steam Turbine&r converts steam, the &6Combustion Generator&r burns fuel and the &6Gas Turbine&r burns gases."),
            ("&6导线&r 把电送到机器：细线 1A、单线 4A、双线 16A……电压越高线损越大，记得用对等级。",
             "&6Wires/Cables&r deliver power: fine wire 1A, single 4A, double 16A... higher voltage means higher loss, so match the tier."),
        ],
        icon="gtceu:lv_steam_turbine",
        x=0.0, y=20.0,
        deps=["coke_oven"],
        tasks=[
            {"type": "item", "item": "gtceu:lv_steam_turbine", "count": 1},
            {"type": "item", "item": "gtceu:lv_combustion", "count": 1},
        ],
        rewards=[{"item": "numismatics:cog", "count": 10}],
    ),
    dict(
        key="lv_hull",
        title=("LV 机器外壳", "LV Machine Hull"),
        desc=[
            ("&6机器外壳&r 是每台机器的心脏：钢板 + 电路 + 线缆。做外壳之前先准备好 &6基础电子电路&r。",
             "The &6Machine Hull&r is the heart of every machine: steel plates + circuits + cables. Prepare &6Basic Electronic Circuits&r first."),
            ("从 LV 开始，每一级电压都有自己的外壳，外壳等级决定了机器能承受的电压。",
             "Each voltage tier has its own hull; the hull tier decides the voltage a machine can take."),
        ],
        icon="gtceu:lv_machine_hull",
        x=0.0, y=22.5,
        deps=["lv_power"],
        tasks=[{"type": "item", "item": "gtceu:lv_machine_hull", "count": 2}],
        rewards=[{"item": "numismatics:cog", "count": 10}],
    ),
    dict(
        key="lv_machines",
        title=("LV 机器", "LV Machines"),
        desc=[
            ("有了外壳就能造第一批电动机器：&6打粉机&r（粉碎矿石）、&6电炉&r（烧炼）、&6组装机&r（自动合成）。",
             "With hulls you can build the first electric machines: the &6Macerator&r (crushing), &6Electric Furnace&r (smelting) and &6Assembler&r (auto-crafting)."),
            ("接下来逐步补齐：&6离心机、电解机、混合机、高压釜、卷板机、拉丝机、车床、压模机&r……它们是所有配方的基石。",
             "Then fill in the rest: &6Centrifuge, Electrolyzer, Mixer, Autoclave, Bender, Wiremill, Lathe, Extruder&r... the backbone of every recipe."),
        ],
        icon="gtceu:lv_macerator",
        x=0.0, y=25.0,
        deps=["lv_hull"],
        tasks=[
            {"type": "item", "item": "gtceu:lv_macerator", "count": 1},
            {"type": "item", "item": "gtceu:lv_electric_furnace", "count": 1},
            {"type": "item", "item": "gtceu:lv_assembler", "count": 1},
        ],
        rewards=[{"item": "numismatics:cog", "count": 10}],
    ),
    dict(
        key="lv_circuits",
        title=("LV 电路", "LV Circuits"),
        desc=[
            ("电路是机器的灵魂：&6基础电子电路&r 用 &6树脂电路板 + 真空管 + 电阻&r 制作，是 LV 机器外壳与大量配方的必需品。",
             "Circuits are the soul of machines: the &6Basic Electronic Circuit&r uses a &6Resin Circuit Board + Vacuum Tubes + Resistors&r, required for LV hulls and many recipes."),
            ("电路板从 &6树脂板&r 开始，经过 &6蚀刻&r 与 &6压印&r 逐步升级为酚醛/塑料/环氧板。",
             "Circuit boards start from &6Resin&r, then are etched and pressed into phenolic/plastic/epoxy boards."),
        ],
        icon="gtceu:basic_electronic_circuit",
        x=0.0, y=27.5,
        deps=["lv_machines"],
        tasks=[
            {"type": "item", "item": "gtceu:basic_electronic_circuit", "count": 4},
            {"type": "item", "item": "gtceu:resin_printed_circuit_board", "count": 1},
        ],
        rewards=[{"item": "numismatics:cog", "count": 10}],
    ),
    dict(
        key="mv",
        title=("中压（MV）", "Medium Voltage"),
        desc=[
            ("升级到 &6MV&r 意味着更强的机器与更复杂的化学：&6铝合金外壳&r、&6高级电路&r、&6不锈钢&r。",
             "Upgrading to &6MV&r brings stronger machines and deeper chemistry: &6Aluminium Hulls&r, &6Good Electronic Circuits&r and &6Stainless Steel&r."),
            ("别忘了 &6电路组装机&r——它让电路生产自动化；以及 &6化学浴&r、&6化学反应釜&r 解锁石化工业。",
             "Don't miss the &6Circuit Assembler&r to automate circuits, plus the &6Chemical Bath&r and &6Chemical Reactor&r that unlock petrochemistry."),
        ],
        icon="gtceu:mv_machine_hull",
        x=0.0, y=30.0,
        deps=["lv_circuits"],
        tasks=[
            {"type": "item", "item": "gtceu:mv_machine_hull", "count": 1},
            {"type": "item", "item": "gtceu:mv_assembler", "count": 1},
            {"type": "item", "item": "gtceu:good_electronic_circuit", "count": 2},
        ],
        rewards=[{"item": "numismatics:cog", "count": 12}],
    ),
    dict(
        key="hv",
        title=("高压（HV）", "High Voltage"),
        desc=[
            ("&6HV&r 解锁 &6不锈钢&r 与 &6钛&r 产线，并带来 &6SMD 元件&r——更小、更便宜、更快的电路零件。",
             "&6HV&r unlocks &6Stainless Steel&r and &6Titanium&r chains, plus &6SMD components&r - smaller, cheaper, faster circuit parts."),
            ("&6高级集成电路&r 是 HV 的招牌电路；&6洁净室&r 则是后续所有高精度电路的前提。",
             "The &6Advanced Integrated Circuit&r is HV's signature circuit; the &6Cleanroom&r gates all high-precision circuits after it."),
        ],
        icon="gtceu:hv_machine_hull",
        x=0.0, y=32.5,
        deps=["mv"],
        tasks=[
            {"type": "item", "item": "gtceu:hv_machine_hull", "count": 1},
            {"type": "item", "item": "gtceu:hv_assembler", "count": 1},
            {"type": "item", "item": "gtceu:advanced_integrated_circuit", "count": 2},
        ],
        rewards=[{"item": "numismatics:cog", "count": 12}],
    ),
    dict(
        key="ev",
        title=("超高压（EV）", "Extreme Voltage"),
        desc=[
            ("&6EV&r 的关键词是 &6微处理器&r、&6环氧树脂&r 与 &6蒸馏塔&r：石化产线在此成型，钛、钨开始量产。",
             "&6EV&r is about &6Microprocessors&r, &6Epoxy&r and the &6Distillation Tower&r: petrochemistry matures, titanium and tungsten enter mass production."),
            ("&6纳米处理器&r 将在 IV 接棒；提前准备好 &6铂系金属&r 产线。",
             "The &6Nano Processor&r takes over at IV; prepare the &6Platinum Group&r chain in advance."),
        ],
        icon="gtceu:ev_machine_hull",
        x=0.0, y=35.0,
        deps=["hv"],
        tasks=[
            {"type": "item", "item": "gtceu:ev_machine_hull", "count": 1},
            {"type": "item", "item": "gtceu:micro_processor", "count": 2},
            {"type": "item", "item": "gtceu:epoxy_printed_circuit_board", "count": 1},
        ],
        rewards=[{"item": "numismatics:cog", "count": 14}],
    ),
    dict(
        key="iv",
        title=("绝缘电压（IV）", "Insane Voltage"),
        desc=[
            ("&6IV&r 的门槛是 &6装配线（Assembly Line）&r：它把一堆零件按顺序组装成高级机器部件。",
             "&6IV&r is gated by the &6Assembly Line&r: it assembles parts in order into advanced machine components."),
            ("&6纳米处理器&r 与 &6纤维增强电路板&r 是这一阶段的主力；&6钨钢&r 与 &6铱&r 产线也要跟上。",
             "&6Nano Processors&r and &6Fiber-Reinforced Boards&r carry this tier; keep &6Tungstensteel&r and &6Iridium&r flowing."),
        ],
        icon="gtceu:iv_machine_hull",
        x=0.0, y=37.5,
        deps=["ev"],
        tasks=[
            {"type": "item", "item": "gtceu:iv_machine_hull", "count": 1},
            {"type": "item", "item": "gtceu:nano_processor", "count": 2},
        ],
        rewards=[{"item": "numismatics:cog", "count": 16}],
    ),
    dict(
        key="luv",
        title=("剧差压（LuV）", "Ludicrous Voltage"),
        desc=[
            ("&6LuV&r 带来 &6聚变反应堆 I&r 与 &6量子处理器&r；&6铕&r、&6铱&r、&6三钛&r 是这一阶段的关键材料。",
             "&6LuV&r brings &6Fusion Reactor I&r and &6Quantum Processors&r; &6Europium&r, &6Iridium&r and &6Trinium&r are the key materials."),
            ("聚变需要大量能量，先备好 &6等离子涡轮&r 与 &6大型涡轮&r。",
             "Fusion demands huge power - prepare &6Plasma Turbines&r and &6Large Turbines&r first."),
        ],
        icon="gtceu:luv_machine_hull",
        x=0.0, y=40.0,
        deps=["iv"],
        tasks=[
            {"type": "item", "item": "gtceu:luv_machine_hull", "count": 1},
            {"type": "item", "item": "gtceu:quantum_processor", "count": 2},
        ],
        rewards=[{"item": "numismatics:cog", "count": 18}],
    ),
    dict(
        key="zpm",
        title=("零点压（ZPM）", "Zero Point Module"),
        desc=[
            ("&6ZPM&r 需要 &6湿件&r 与 &6晶体处理器&r；&6零点模块&r 是这一阶段的终极目标。",
             "&6ZPM&r requires &6Wetware&r and &6Crystal Processors&r; the &6Zero Point Module&r is the tier's ultimate goal."),
            ("&6研究站&r 与 &6无菌洁净室&r 会打开新配方；&6硅岩（Naquadah）&r 链也要打通。",
             "The &6Research Station&r and &6Sterile Cleanroom&r open new recipes; get the &6Naquadah&r chain running."),
        ],
        icon="gtceu:zpm_machine_hull",
        x=0.0, y=42.5,
        deps=["luv"],
        tasks=[
            {"type": "item", "item": "gtceu:zpm_machine_hull", "count": 1},
            {"type": "item", "item": "gtceu:crystal_processor", "count": 2},
        ],
        rewards=[{"item": "numismatics:cog", "count": 20}],
    ),
    dict(
        key="uv",
        title=("极限压（UV）", "Ultimate Voltage"),
        desc=[
            ("&6UV&r 是原版 GT 的最后一站：&6湿件处理器&r、&6中子素&r、&6聚变堆 III&r。",
             "&6UV&r is the last stop of vanilla GT: &6Wetware Processors&r, &6Neutronium&r and &6Fusion Reactor III&r."),
            ("完成 UV 后，你已经是这个包里的工业大师了——剩下的就是享受自动化。",
             "Finishing UV makes you the industrial master of this pack - now enjoy your automation."),
        ],
        icon="gtceu:uv_machine_hull",
        x=0.0, y=45.0,
        deps=["zpm"],
        tasks=[
            {"type": "item", "item": "gtceu:uv_machine_hull", "count": 1},
            {"type": "item", "item": "gtceu:wetware_processor", "count": 1},
        ],
        rewards=[{"item": "numismatics:cog", "count": 24}],
    ),
    dict(
        key="finale",
        title=("工业大师", "Industrial Master"),
        desc=[
            ("从第一块钢板到湿件处理器，你已经走完了 GT 的全部电压等级。",
             "From the first steel plate to wetware processors - you have walked the entire voltage ladder of GregTech."),
            ("接下来：把 GT 与你的农场结合——温室自动化、GTSE 农业机器、AE2 自动合成，让山谷彻底工业化。",
             "Next: fuse GregTech with your farm - automated greenhouses, GTSE farm machines and AE2 autocrafting. Industrialize the valley."),
        ],
        icon="gtceu:wetware_processor_mainframe",
        x=0.0, y=47.5,
        deps=["uv"],
        tasks=[{"type": "checkmark", "title": ("完成格雷科技主线", "Complete the GregTech main line")}],
        rewards=[{"item": "numismatics:cog", "count": 32}],
    ),

    # ================= 多方块分支（右侧 x=4.5） =================
    dict(
        key="multiblock_intro",
        title=("多方块结构", "Multiblocks"),
        desc=[
            ("多方块由 &6控制器 + 结构方块 + 仓室&r 组成：&6输入总线/输入仓&r 进料，&6输出总线/输出仓&r 出料，&6能源仓&r 供电，&6维护仓&r 处理故障。",
             "A multiblock is &6Controller + structural blocks + hatches&r: &6Input Bus/Hatch&r feed it, &6Output Bus/Hatch&r collect, &6Energy Hatch&r powers it and the &6Maintenance Hatch&r handles repairs."),
            ("结构成型后会显示预览；用 &6扳手&r 旋转、&6软锤&r 开关、&6螺丝刀&r 调整仓室。",
             "A formed structure shows a preview; use the &6Wrench&r to rotate, &6Soft Mallet&r to toggle and &6Screwdriver&r to configure hatches."),
        ],
        icon="gtceu:maintenance_hatch",
        x=4.5, y=17.5,
        deps=["steel"],
        tasks=[{"type": "checkmark", "title": ("了解多方块的基本构成", "Understand multiblock basics")}],
        rewards=[{"item": "numismatics:cog", "count": 8}],
    ),
    dict(
        key="steam_grinder",
        title=("蒸汽研磨机", "Steam Grinder"),
        desc=[
            ("&6蒸汽研磨机&r 是蒸汽时代最强的矿石处理机：8 个并行槽位，直接把矿石磨成粉。",
             "The &6Steam Grinder&r is the Steam Age's ultimate ore processor: 8 parallel slots, grinding ores straight into dust."),
            ("它需要蒸汽与 &6蒸汽输入仓&r；记得给它接上锅炉。",
             "It needs steam via a &6Steam Input Hatch&r - hook up your boilers."),
        ],
        icon="gtceu:steam_grinder",
        x=4.5, y=20.0,
        deps=["multiblock_intro"],
        tasks=[{"type": "item", "item": "gtceu:steam_grinder", "count": 1}],
        rewards=[{"item": "numismatics:cog", "count": 10}],
    ),
    dict(
        key="ebf",
        title=("电力高炉", "Electric Blast Furnace"),
        desc=[
            ("&6电力高炉（EBF）&r 是 GT 最重要的多方块：铝、钛、钨、钢……几乎所有高级金属都要在这里高温冶炼。",
             "The &6Electric Blast Furnace (EBF)&r is GT's most important multiblock: aluminium, titanium, tungsten, steel... nearly every advanced metal is smelted here."),
            ("冶炼温度由 &6加热线圈&r 决定：白铜 → 坎塔尔 → 镍铬 → RTM → HSS……线圈越热，能烧的金属越多。",
             "Smelting temperature comes from the &6Heating Coils&r: Cupronickel → Kanthal → Nichrome → RTM → HSS... hotter coils unlock more metals."),
            ("需要 &6能源仓 + 输入/输出总线 + 维护仓&r；别忘了给它接上电。",
             "Requires &6Energy Hatch + Input/Output Buses + Maintenance Hatch&r - and power, of course."),
        ],
        icon="gtceu:electric_blast_furnace",
        x=4.5, y=22.5,
        deps=["lv_machines"],
        tasks=[
            {"type": "item", "item": "gtceu:electric_blast_furnace", "count": 1},
            {"type": "item", "item": "gtceu:cupronickel_coil_block", "count": 8},
        ],
        rewards=[{"item": "numismatics:cog", "count": 12}],
    ),
    dict(
        key="large_chemical_reactor",
        title=("大型化学反应釜", "Large Chemical Reactor"),
        desc=[
            ("&6大型化学反应釜（LCR）&r 是化学产线的核心：多流体输入输出、支持大配方，后期几乎所有化工都靠它。",
             "The &6Large Chemical Reactor (LCR)&r is the core of chemistry: multiple fluid I/O and large recipes - most late-game chemistry runs here."),
            ("它还能执行普通化学反应釜做不了的特殊配方。",
             "It can also run special recipes the regular Chemical Reactor cannot."),
        ],
        icon="gtceu:large_chemical_reactor",
        x=4.5, y=27.5,
        deps=["mv"],
        tasks=[{"type": "item", "item": "gtceu:large_chemical_reactor", "count": 1}],
        rewards=[{"item": "numismatics:cog", "count": 14}],
    ),
    dict(
        key="distillation_tower",
        title=("蒸馏塔", "Distillation Tower"),
        desc=[
            ("&6蒸馏塔&r 把原油/燃料一次性分离成多种产物：汽油、柴油、石脑油、润滑油……石化工业的心脏。",
             "The &6Distillation Tower&r splits oil/fuel into many products at once: gasoline, diesel, naphtha, lubricant... the heart of petrochemistry."),
            ("塔身越高产出的馏分越多；用 &6输出仓&r 分层收集。",
             "Taller towers yield more fractions; collect them with layered &6Output Hatches&r."),
        ],
        icon="gtceu:distillation_tower",
        x=4.5, y=30.0,
        deps=["large_chemical_reactor"],
        tasks=[{"type": "item", "item": "gtceu:distillation_tower", "count": 1}],
        rewards=[{"item": "numismatics:cog", "count": 14}],
    ),
    dict(
        key="pyrolyse_oven",
        title=("热解炉", "Pyrolyse Oven"),
        desc=[
            ("&6热解炉&r 在缺氧环境下把有机物（木头、煤）分解成 &6木炭、木煤气、苯&r 等，是化工与发电的原料来源。",
             "The &6Pyrolyse Oven&r decomposes organics (wood, coal) into &6Charcoal, Wood Gas, Benzene&r and more - feedstock for chemistry and power."),
        ],
        icon="gtceu:pyrolyse_oven",
        x=4.5, y=32.5,
        deps=["distillation_tower"],
        tasks=[{"type": "item", "item": "gtceu:pyrolyse_oven", "count": 1}],
        rewards=[{"item": "numismatics:cog", "count": 14}],
    ),
    dict(
        key="implosion_compressor",
        title=("内爆压缩机", "Implosion Compressor"),
        desc=[
            ("&6内爆压缩机&r 用炸药把材料瞬间压成 &6工业钻石、铱合金&r 等超硬材料。",
             "The &6Implosion Compressor&r uses explosives to instantly compress materials into &6Industrial Diamonds, Iridium Alloys&r and other ultra-hard materials."),
            ("每次工作会消耗 TNT，记得自动供料。",
             "Each cycle consumes TNT - automate the supply."),
        ],
        icon="gtceu:implosion_compressor",
        x=4.5, y=35.0,
        deps=["hv"],
        tasks=[{"type": "item", "item": "gtceu:implosion_compressor", "count": 1}],
        rewards=[{"item": "numismatics:cog", "count": 16}],
    ),
    dict(
        key="vacuum_freezer",
        title=("真空冷冻机", "Vacuum Freezer"),
        desc=[
            ("&6真空冷冻机&r 用于冷却热锭（如热钛锭、热钨锭）与生产液氧/液氦，是高温产线的下游。",
             "The &6Vacuum Freezer&r cools hot ingots (hot titanium, hot tungsten) and makes liquid oxygen/helium - downstream of your hot lines."),
        ],
        icon="gtceu:vacuum_freezer",
        x=4.5, y=37.5,
        deps=["implosion_compressor"],
        tasks=[{"type": "item", "item": "gtceu:vacuum_freezer", "count": 1}],
        rewards=[{"item": "numismatics:cog", "count": 16}],
    ),
    dict(
        key="assembly_line",
        title=("装配线", "Assembly Line"),
        desc=[
            ("&6装配线&r 是 IV 的通行证：把零件按顺序送入，组装出高级电路、聚变线圈等复杂部件。",
             "The &6Assembly Line&r is your IV passport: feed parts in order to assemble advanced circuits, fusion coils and other complex components."),
            ("可以开启 &6研究&r 前置（需要研究站）；装配线越长，能做的配方越高级。",
             "You can enable &6Research&r requirements (needs the Research Station); longer lines unlock higher recipes."),
        ],
        icon="gtceu:assembly_line",
        x=4.5, y=40.0,
        deps=["iv"],
        tasks=[{"type": "item", "item": "gtceu:assembly_line", "count": 1}],
        rewards=[{"item": "numismatics:cog", "count": 18}],
    ),
    dict(
        key="research_station",
        title=("研究站", "Research Station"),
        desc=[
            ("&6研究站&r 用 &6数据球/数据模块&r 解锁装配线的高级配方；扫描仪负责生产数据。",
             "The &6Research Station&r consumes &6Data Orbs/Modules&r to unlock advanced Assembly Line recipes; the Scanner produces the data."),
            ("它是 IV 之后所有高级产线的钥匙。",
             "It is the key to every advanced line after IV."),
        ],
        icon="gtceu:research_station",
        x=4.5, y=42.5,
        deps=["assembly_line"],
        tasks=[{"type": "item", "item": "gtceu:research_station", "count": 1}],
        rewards=[{"item": "numismatics:cog", "count": 18}],
    ),
    dict(
        key="fusion_reactor",
        title=("聚变反应堆", "Fusion Reactor"),
        desc=[
            ("&6聚变反应堆&r 用巨大能量把元素融合成新元素（铕、铱、等离子体），是 LuV 的标志性结构。",
             "The &6Fusion Reactor&r fuses elements into new ones (europium, iridium, plasma) - the landmark structure of LuV."),
            ("它需要 &6聚变线圈 + 聚变外壳&r，并用 &6等离子涡轮&r 回收能量。",
             "It needs &6Fusion Coils + Fusion Casings&r and a &6Plasma Turbine&r to recover power."),
        ],
        icon="gtceu:luv_fusion_reactor",
        x=4.5, y=45.0,
        deps=["luv"],
        tasks=[
            {"type": "item", "item": "gtceu:luv_fusion_reactor", "count": 1},
            {"type": "item", "item": "gtceu:fusion_casing", "count": 8},
        ],
        rewards=[{"item": "numismatics:cog", "count": 20}],
    ),
    dict(
        key="large_turbines",
        title=("大型涡轮", "Large Turbines"),
        desc=[
            ("&6大型蒸汽/燃气/等离子涡轮&r 把流体转化为大量 EU：越大越快，需要 &6涡轮转子&r。",
             "&6Large Steam/Gas/Plasma Turbines&r convert fluids into large amounts of EU: bigger means faster, and they need &6Turbine Rotors&r."),
            ("转子材料决定效率与耐久：钢 → 不锈钢 → 钛 → 钨钢 →……",
             "Rotor material decides efficiency and durability: Steel → Stainless Steel → Titanium → Tungstensteel →..."),
        ],
        icon="gtceu:steam_large_turbine",
        x=4.5, y=47.5,
        deps=["hv"],
        tasks=[
            {"type": "item", "item": "gtceu:steam_large_turbine", "count": 1},
            {"type": "item", "item": "gtceu:gas_large_turbine", "count": 1},
        ],
        rewards=[{"item": "numismatics:cog", "count": 16}],
    ),
    dict(
        key="large_combustion",
        title=("大型内燃机", "Large Combustion Engine"),
        desc=[
            ("&6大型内燃机&r 与 &6极限内燃机&r 烧柴油/汽油/高十六烷值柴油，是 EV 之后的主力发电机。",
             "The &6Large Combustion Engine&r and &6Extreme Combustion Engine&r burn diesel/gasoline/cetane-boosted diesel - the main generators after EV."),
        ],
        icon="gtceu:large_combustion_engine",
        x=4.5, y=50.0,
        deps=["ev"],
        tasks=[
            {"type": "item", "item": "gtceu:large_combustion_engine", "count": 1},
            {"type": "item", "item": "gtceu:extreme_combustion_engine", "count": 1},
        ],
        rewards=[{"item": "numismatics:cog", "count": 18}],
    ),

    # ================= 矿石分支（左侧 x=-4.5） =================
    dict(
        key="ore_intro",
        title=("矿石与矿脉", "Ores and Veins"),
        desc=[
            ("GT 的矿石以 &6矿脉&r 形式成簇生成，每个矿脉由 1~4 种矿物组成，地表常有 &6指示矿&r（小矿石块）提示位置。",
             "GT ores spawn in &6veins&r: each vein holds 1-4 minerals and often leaves &6surface indicators&r (small ore rocks) on the ground."),
            ("不同维度生成不同矿脉；本包已把 22 种主世界矿脉注入 &6骷髅洞穴&r 与 &6暮色森林&r。",
             "Different dimensions host different veins; this pack injected 22 overworld veins into the &6Skull Cavern&r and the &6Twilight Forest&r."),
            ("右键地面上的指示矿可以查看矿脉信息；&6勘探器&r 能扫描更大范围。",
             "Right-click surface indicators for vein info; the &6Prospector&r scans a much larger area."),
        ],
        icon="gtceu:raw_tin",
        x=-4.5, y=20.0,
        deps=["lv_power"],
        tasks=[{"type": "checkmark", "title": ("了解 GT 矿脉与指示矿", "Understand GT veins and indicators")}],
        rewards=[{"item": "numismatics:cog", "count": 8}],
    ),
    dict(
        key="prospector",
        title=("矿石勘探器", "Ore Prospector"),
        desc=[
            ("&6LV 勘探器&r 扫描 3×3 区块，&6HV 勘探器&r 扫描 7×7，&6LuV 超级勘探器&r 扫描 15×15（并显示流体）。",
             "The &6LV Prospector&r scans 3×3 chunks, the &6HV Prospector&r 7×7 and the &6LuV Super Prospector&r 15×15 (with fluids)."),
            ("拿在手上右键即可扫描，按 &6Ctrl&r 切换模式；扫描结果会生成路径点。",
             "Right-click to scan and press &6Ctrl&r to switch modes; results become waypoints."),
        ],
        icon="gtceu:prospector.lv",
        x=-4.5, y=22.5,
        deps=["ore_intro"],
        tasks=[{"type": "item", "item": "gtceu:prospector.lv", "count": 1}],
        rewards=[{"item": "numismatics:cog", "count": 10}],
    ),
    dict(
        key="ore_processing_1",
        title=("矿石处理 I：粉碎", "Ore Processing I: Crushing"),
        desc=[
            ("把原矿送进 &6打粉机&r 得到 &6粉碎矿石&r，再洗矿得到 &6洗净矿石&r，最后离心/热离心得到 &6纯净矿粉&r。",
             "Run raw ore through the &6Macerator&r for &6Crushed Ore&r, wash it into &6Purified Ore&r, then centrifuge into &6Pure Dust&r."),
            ("每多一道工序，产出就多一份副产：这就是 GT 的 &6矿物增值链&r。",
             "Each extra step yields bonus byproducts - that's GT's &6ore value chain&r."),
        ],
        icon="gtceu:crushed_gold_ore",
        x=-4.5, y=25.0,
        deps=["ore_intro"],
        tasks=[
            {"type": "item", "item": "gtceu:crushed_gold_ore", "count": 4},
            {"type": "item", "item": "gtceu:purified_gold_ore", "count": 2},
        ],
        rewards=[{"item": "numismatics:cog", "count": 10}],
    ),
    dict(
        key="ore_processing_2",
        title=("矿石处理 II：副产", "Ore Processing II: Byproducts"),
        desc=[
            ("&6热离心机&r 处理洗净矿石产出纯净矿粉，&6电磁分离器&r 从矿粉中分离磁性副产，&6离心机&r 把矿粉拆成多种元素。",
             "The &6Thermal Centrifuge&r purifies washed ore, the &6Electromagnetic Separator&r extracts magnetic byproducts and the &6Centrifuge&r splits dusts into elements."),
            ("红石、硫、铂系金属等稀有资源大多来自副产——不要直接烧矿石！",
             "Redstone, sulfur and platinum-group metals mostly come from byproducts - never smelt ores directly!"),
        ],
        icon="gtceu:pure_redstone_dust",
        x=-4.5, y=27.5,
        deps=["ore_processing_1"],
        tasks=[
            {"type": "item", "item": "gtceu:pure_redstone_dust", "count": 4},
        ],
        rewards=[{"item": "numismatics:cog", "count": 10}],
    ),
    dict(
        key="ore_veins_skull",
        title=("骷髅洞穴的矿脉", "Veins in the Skull Cavern"),
        desc=[
            ("本包已让 &6骷髅洞穴&r 生成 22 种主世界矿脉（石头层 + 深板岩层），高度为 &6主世界 Y + 64&r（洞窟从 Y=0 开始）。",
             "This pack makes the &6Skull Cavern&r spawn 22 overworld veins (stone + deepslate layers), at &6Overworld Y + 64&r (the cavern starts at Y=0)."),
            ("常见矿脉：锡、铜/锡、铁、煤、磁铁、镍、铅、盐、油砂……深层还有钻石、红石、青金石、蓝宝石等。",
             "Common veins: Tin, Copper/Tin, Iron, Coal, Magnetite, Nickel, Lead, Salts, Oilsands... deeper down: Diamond, Redstone, Lapis, Sapphire and more."),
            ("注意：只对 &6新生成区块&r 生效，已探索的区域不会补矿。",
             "Note: only &6newly generated chunks&r are affected - explored areas will not receive ores."),
        ],
        icon="gtceu:raw_lead",
        x=-4.5, y=30.0,
        deps=["ore_intro"],
        tasks=[{"type": "checkmark", "title": ("前往骷髅洞穴寻找 GT 矿脉", "Find GT veins in the Skull Cavern")}],
        rewards=[{"item": "numismatics:cog", "count": 10}],
    ),
    dict(
        key="ore_veins_tf",
        title=("暮色森林的矿脉", "Veins in the Twilight Forest"),
        desc=[
            ("&6暮色森林&r 同样注入了这 22 种矿脉（Y 范围已重映射到该维度：min_y=-32）。",
             "The &6Twilight Forest&r received the same 22 veins (Y ranges remapped for the dimension: min_y=-32)."),
            ("冒险与挖矿两不误——不过小心迷宫与九头蛇。",
             "Adventure and mining in one trip - just mind the labyrinths and the Hydra."),
        ],
        icon="gtceu:raw_silver",
        x=-4.5, y=32.5,
        deps=["ore_veins_skull"],
        tasks=[{"type": "checkmark", "title": ("在暮色森林挖到 GT 矿石", "Mine GT ores in the Twilight Forest")}],
        rewards=[{"item": "numismatics:cog", "count": 10}],
    ),
    dict(
        key="ore_processing_3",
        title=("矿石处理 III：元素化", "Ore Processing III: Elemental"),
        desc=[
            ("终极处理是 &6电解&r：把矿粉拆成元素（如铝土矿 → 铝 + 氧 + 钛副产），实现资源利用最大化。",
             "The ultimate step is &6Electrolysis&r: split dusts into elements (e.g. Bauxite → Aluminium + Oxygen + Titanium byproduct) for maximum resource efficiency."),
            ("给 &6电解机&r 接上充足的电力，长期收益巨大。",
             "Feed the &6Electrolyzer&r plenty of power - the long-term payoff is huge."),
        ],
        icon="gtceu:lv_electromagnetic_separator",
        x=-4.5, y=35.0,
        deps=["ore_processing_2"],
        tasks=[
            {"type": "item", "item": "gtceu:lv_thermal_centrifuge", "count": 1},
            {"type": "item", "item": "gtceu:lv_electromagnetic_separator", "count": 1},
        ],
        rewards=[{"item": "numismatics:cog", "count": 12}],
    ),

    # ================= 联动分支（右侧 x=9） =================
    dict(
        key="gt_greenhouse",
        title=("温室：工业农业", "Greenhouses: Industrial Farming"),
        desc=[
            ("本包已内置两种温室：&6GTCA 的温室多方块&r（配方类型 gtceu:green_house，支持树苗/作物/橡胶树 + 肥料增产）与 &6GTMFO 的树木温室&r（需要自然光，雨天/夜晚变慢）。",
             "This pack already has two greenhouses: the &6GTCA Greenhouse&r multiblock (recipe type gtceu:green_house, saplings/crops/rubber + fertilizer boost) and the &6GTMFO Greenhouse&r (needs natural light, slower at night/rain)."),
            ("把它们接上 GT 电力与自动输入，就是全自动的工业农场。",
             "Hook them up to GT power and automated input for a fully automatic industrial farm."),
        ],
        icon="gtca:green_house",
        x=9.0, y=27.5,
        deps=["mv"],
        tasks=[
            {"type": "item", "item": "gtca:green_house", "count": 1},
            {"type": "item", "item": "gtmfo:greenhouse", "count": 1},
        ],
        rewards=[{"item": "numismatics:cog", "count": 16}],
    ),
    dict(
        key="gt_farm_machines",
        title=("农业机器（GTSE）", "Farm Machines (GTSE)"),
        desc=[
            ("&6GTSE（Greg Tech Simple Extension）&r 提供了从 LV 到 IV 的 &6收割机&r、&6怪物模拟器&r、&6捕鱼机&r、&6下界收集器&r 等农业/资源机器。",
             "&6GTSE (Greg Tech Simple Extension)&r adds tiered &6Harvesters&r, &6Mob Simulators&r, &6Large Fishers&r and &6Nether Collectors&r from LV to IV."),
            ("配合 &6GTNN/GTMM&r 等附属，还能把机器并行与产线做得更大。",
             "Together with addons like &6GTNN/GTMM&r you can scale parallelism and production lines further."),
        ],
        icon="gtse:lv_harvester",
        x=9.0, y=30.0,
        deps=["gt_greenhouse"],
        tasks=[
            {"type": "item", "item": "gtse:lv_harvester", "count": 1},
        ],
        rewards=[{"item": "numismatics:cog", "count": 16}],
    ),
    dict(
        key="gt_ae2",
        title=("GT 与 AE2", "GregTech meets AE2"),
        desc=[
            ("本包的 &6applied_greg&r 提供了 &6ME 能源仓/ME 二极管&r，把 GT 机器直接接进 AE 网络供电与传输。",
             "This pack's &6applied_greg&r adds &6ME Energy Hatches / ME Diodes&r that plug GT machines straight into your AE network."),
            ("GT 自身的 &6ME 样板缓存、库存输入总线/仓&r 还能让多方块直接读取样板与库存。",
             "GT itself adds the &6ME Pattern Buffer&r and &6ME Stocking Input Bus/Hatch&r so multiblocks can read patterns and stock directly."),
        ],
        icon="gtceu:me_pattern_buffer",
        x=9.0, y=32.5,
        deps=["gt_farm_machines"],
        tasks=[
            {"type": "item", "item": "gtceu:me_stocking_input_bus", "count": 1},
        ],
        rewards=[{"item": "numismatics:cog", "count": 18}],
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
                lines.append(f'\t\t\t\t"{{ftbquests.chapter.{CHAPTER_FILENAME}.quest{q["qid"]}.description{i+1}}}"')
            lines.append("\t\t\t]")
        lines.append(f'\t\t\ticon: "{q["icon"]}"')
        lines.append(f'\t\t\tid: "{q["qid"]}"')
        if q.get("optional"):
            lines.append("\t\t\toptional: true")
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
    lines.append(f'\ttitle: "{{ftbquests.chapter.{CHAPTER_FILENAME}.title}}"')
    lines.append("}")
    return "\n".join(lines) + "\n"


def lang_entries():
    """返回 {key: (zh, en)}"""
    out = {}
    out[f"ftbquests.chapter.{CHAPTER_FILENAME}.title"] = ("VI - 格雷科技", "VI - GregTech")
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
    """向 lang 文件原位插入条目（幂等，只做最小插入）。"""
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

    parsed = [(k, l) for (k, l) in parsed if not k.startswith(f"ftbquests.chapter.{CHAPTER_FILENAME}.")]

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
