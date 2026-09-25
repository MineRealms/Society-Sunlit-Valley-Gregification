# -*- coding: utf-8 -*-
"""
MEK（通用机械）章节生成器 v2（Society: Sunlit Valley / 1.20.1 / Mekanism 10.4.16.80）

用法（在整合包根目录执行）：
    python config/ftbquests/tools/build_mek_chapter.py

产出：
    config/ftbquests/quests/chapters/mekanism.snbt（内联中文，不写 lang 文件）

设计要点（v2，2026-09-22 扩写）：
    - 章节挂在「格雷科技」分组（4A46A5E1358A80A6）下，order_index = 17
    - 入门任务外部前置 = LV 章「铝锭」任务 7567E885B7166603
    - **ID 规则（重要坑）**：FTBQ 用有符号 Long.parseLong(id,16) 读 ID，
      16 位 HEX 的**首位必须 ≤ 7**（否则溢出被游戏重生成 → 任务书炸裂）；
      本脚本 make_id 只取首位 0-7。
    - **ID 保持**：脚本会读取现有 mekanism.snbt，保留其中已存在的任务/目标/奖励 ID
      （玩家进度不丢），只为新增任务生成新 ID；章节 ID 也保持。
    - 机器/物品 ID 均核对自 mods/Mekanism*(10.4.16.80).jar 的 lang 与配方 JSON
    - 文本一律内联中文（不写 lang 文件）
"""

import json
import os
import random
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
CHAPTERS_DIR = os.path.join(ROOT, "config", "ftbquests", "quests", "chapters")
REWARD_TABLES_DIR = os.path.join(ROOT, "config", "ftbquests", "quests", "reward_tables")
CHAPTER_FILE = os.path.join(CHAPTERS_DIR, "mekanism.snbt")

CHAPTER_FILENAME = "mekanism"
CHAPTER_GROUP = "4A46A5E1358A80A6"  # 格雷科技分组
CHAPTER_ORDER = 17
CHAPTER_ICON = "mekanism:metallurgic_infuser"
CHAPTER_TITLE = "&9&l隐藏科技&r - 通用机械"
SEED = 20260915

# 外部前置：LV 章「铝锭」任务（LV→MV 收尾）
EXT_DEP_LV_FINALE = "7567E885B7166603"

# 查询式 COG 奖励（经济联动）
def cog(n):
    return [{"item": "numismatics:cog", "count": n}]


def osmium(n):
    return [{"item": "mekanism:ingot_osmium", "count": n}]


# =====================================================================
# 任务数据（前 11 个为既有任务，内容与当前文件一致；其余为本轮新增）
# 字段：key/title/(desc)/icon/x/y/deps/ext_deps/tasks/rewards
# =====================================================================
QUESTS = [
    # ---------------- 既有 11 个（保持原样） ----------------
    dict(
        key="infuser",
        title=("通用机械入门：冶金灌注机", "Mekanism Entry: Metallurgic Infuser"),
        desc=[
            ("把 &7LV&r 阶段玩得差不多后，通用机械（&9MEK&r）的大门才会打开。",
             "Once you have mostly finished the &7LV&r stage, the gate to &9Mekanism&r opens."),
            ("MEK 被 &d格雷科技&r 与 &6Create&r 双重锁住：基础机器需要 &bLV 微处理器&r（&3电路组装机&r 产物）与 &6Create 精密构件&r。",
             "Mekanism is locked behind both &dGT&r and &6Create&r: basic machines require &bLV Microchips&r (made in the &3Circuit Assembler&r) and &6Create Precision Mechanisms&r."),
            ("冶金灌注机是 MEK 的起点——用它把 &c红石&r、&8碳&r 等材料灌注进金属，做出合金、钢与电路。",
             "The Metallurgic Infuser is the entry point: infuse metals with &cRedstone&r, &8Carbon&r and more to make alloys, steel and circuits."),
        ],
        icon="mekanism:metallurgic_infuser",
        x=0.0, y=0.0,
        deps=[],
        ext_deps=[EXT_DEP_LV_FINALE],
        tasks=[{"type": "item", "item": "mekanism:metallurgic_infuser"}],
        rewards=cog(8),
    ),
    dict(
        key="casing",
        title=("钢外壳", "Steel Casing"),
        desc=[
            ("所有 MEK 机器都离不开钢外壳。钢锭既可来自 &dGT&r，也可在灌注机中用铁锭灌注 &8碳&r 得到。",
             "Every Mekanism machine needs Steel Casing. The steel can come from &dGT&r, or be infused from iron with &8Carbon&r in the Infuser."),
        ],
        icon="mekanism:steel_casing",
        x=2.5, y=0.0,
        deps=["infuser"],
        tasks=[{"type": "item", "item": "mekanism:steel_casing"}],
        rewards=cog(8),
    ),
    dict(
        key="circuit",
        title=("基础控制电路", "Basic Control Circuit"),
        desc=[
            ("在灌注机中把 &7锇锭&r 灌注 &c红石&r，得到基础控制电路；它是高级电路与众多机器的原料。",
             "Infuse an &7Osmium Ingot&r with &cRedstone&r to get a Basic Control Circuit — the ingredient of advanced circuits and many machines."),
        ],
        icon="mekanism:basic_control_circuit",
        x=0.0, y=2.5,
        deps=["infuser"],
        tasks=[{"type": "item", "item": "mekanism:basic_control_circuit"}],
        rewards=cog(8),
    ),
    dict(
        key="gregmek",
        title=("GregMek：双线矿石处理", "GregMek: Dual Ore Processing"),
        desc=[
            ("&9GregMek&r 把 GT 与 MEK 的矿石处理链打通，两条链可互相转换：",
             "&9GregMek&r bridges the GT and Mekanism ore-processing chains so they can feed each other:"),
            ("&dGT 侧&r：洗矿机（矿石 + 硫酸）→ 化学洗矿（+ 水）→ 高压釜（→ 晶体）。",
             "&dGT side&r: Ore Washer (ore + sulfuric acid) → Chemical Bath (+ water) → Autoclave (→ crystals)."),
            ("&9MEK 侧&r：压射（+ 盐酸）→ 提纯（+ 氧气）→ 粉碎 → 富集。",
             "&9MEK side&r: Injection (+ hydrochloric acid) → Purification (+ oxygen) → Crushing → Enrichment."),
        ],
        icon="gtceu:lv_ore_washer",
        x=-2.5, y=0.0,
        deps=["infuser"],
        tasks=[{"type": "checkmark", "title": ("我已了解 GregMek 的双线处理链", "I understand GregMek's dual processing chains")}],
        rewards=cog(8),
    ),
    dict(
        key="enrichment",
        title=("富集仓", "Enrichment Chamber"),
        desc=[
            ("把矿石与材料富集为更高效的形态。合成需要 &bLV 微处理器&r 与 &6Create 精密构件&r（详见 JEI）。",
             "Enriches ores and materials into more efficient forms. Crafting requires &bLV Microchips&r and &6Create Precision Mechanisms&r (see JEI)."),
        ],
        icon="mekanism:enrichment_chamber",
        x=5.0, y=-2.5,
        deps=["casing"],
        tasks=[{"type": "item", "item": "mekanism:enrichment_chamber"}],
        rewards=osmium(4),
    ),
    dict(
        key="crusher",
        title=("粉碎机", "Crusher"),
        desc=[
            ("把矿石粉碎为两份粉尘。合成需要 &bLV 微处理器&r 与 &6Create 精密构件&r（详见 JEI）。",
             "Crushes ores into two dusts. Crafting requires &bLV Microchips&r and &6Create Precision Mechanisms&r (see JEI)."),
        ],
        icon="mekanism:crusher",
        x=5.0, y=0.0,
        deps=["casing"],
        tasks=[{"type": "item", "item": "mekanism:crusher"}],
        rewards=osmium(4),
    ),
    dict(
        key="smelter",
        title=("通电冶炼炉", "Energized Smelter"),
        desc=[
            ("以能量双倍冶炼矿石。合成需要 &bLV 微处理器&r 与 &6Create 精密构件&r（详见 JEI）。",
             "Smelts ores at double output using energy. Crafting requires &bLV Microchips&r and &6Create Precision Mechanisms&r (see JEI)."),
        ],
        icon="mekanism:energized_smelter",
        x=5.0, y=2.5,
        deps=["casing"],
        tasks=[{"type": "item", "item": "mekanism:energized_smelter"}],
        rewards=osmium(4),
    ),
    dict(
        key="sawmill",
        title=("精密锯木机", "Precision Sawmill"),
        desc=[
            ("高效切割木材与材料。合成需要 &bLV 微处理器&r 与 &6Create 精密构件&r（详见 JEI）。",
             "Saws wood and materials efficiently. Crafting requires &bLV Microchips&r and &6Create Precision Mechanisms&r (see JEI)."),
        ],
        icon="mekanism:precision_sawmill",
        x=7.5, y=0.0,
        deps=["casing"],
        tasks=[{"type": "item", "item": "mekanism:precision_sawmill"}],
        rewards=osmium(4),
    ),
    dict(
        key="adv_circuit",
        title=("高级控制电路", "Advanced Control Circuit"),
        desc=[
            ("工作台上用 &9灌注合金 ×2 + 基础控制电路 ×1&r 合成高级控制电路（配方形如「合金-电路-合金」）。",
             "Craft the Advanced Control Circuit from &92 Infused Alloys + 1 Basic Control Circuit&r (pattern: alloy-circuit-alloy)."),
            ("&c阶段锁（MV）&r：配方中的“基础电路”已被替换为 &dGT 的 MV 电路（良好电子电路）&r —— 需要发展 &6MV&r 阶段。",
             "&cStage gate (MV)&r: the Basic Circuit input is replaced with &dGT's MV circuit (Good Electronic Circuit)&r — you need the &6MV&r stage."),
        ],
        icon="mekanism:advanced_control_circuit",
        x=0.0, y=5.0,
        deps=["circuit"],
        ext_deps=["0DBC148D92A9F69F"],
        tasks=[{"type": "item", "item": "mekanism:advanced_control_circuit"}],
        rewards=cog(16),
    ),
    dict(
        key="elite_circuit",
        title=("精英控制电路", "Elite Control Circuit"),
        desc=[
            ("工作台上用 &6强化合金 ×2 + 高级控制电路 ×1&r 合成精英控制电路。",
             "Craft the Elite Control Circuit from &62 Reinforced Alloys + 1 Advanced Control Circuit&r."),
            ("&c阶段锁（HV）&r：配方中的“高级电路”已被替换为 &dGT 的 HV 集成电路（高级集成电路）&r —— 需要发展 &6HV&r 阶段。",
             "&cStage gate (HV)&r: the Advanced Circuit input is replaced with &dGT's HV circuit (Advanced Integrated Circuit)&r — you need the &6HV&r stage."),
        ],
        icon="mekanism:elite_control_circuit",
        x=-2.5, y=5.0,
        deps=["adv_circuit"],
        ext_deps=["26394C1290D70AB6"],
        tasks=[{"type": "item", "item": "mekanism:elite_control_circuit"}],
        rewards=cog(32),
    ),
    dict(
        key="ultimate_circuit",
        title=("终极控制电路", "Ultimate Control Circuit"),
        desc=[
            ("工作台上用 &5原子合金 ×2 + 精英控制电路 ×1&r 合成终极控制电路。",
             "Craft the Ultimate Control Circuit from &52 Atomic Alloys + 1 Elite Control Circuit&r."),
            ("&c阶段锁（EV）&r：配方中的“精英电路”已被替换为 &dGT 的 EV 电路（微处理器计算机）&r —— 需要发展 &6EV&r 阶段。",
             "&cStage gate (EV)&r: the Elite Circuit input is replaced with &dGT's EV circuit (Microprocessor Computer)&r — you need the &6EV&r stage."),
            ("它也是绝大多数“终极”级机器的核心部件。",
             "It is the core component of nearly every \"Ultimate\"-tier machine."),
        ],
        icon="mekanism:ultimate_control_circuit",
        x=-2.5, y=7.5,
        deps=["elite_circuit", "alloy_atomic"],
        ext_deps=["4AFD3073C731A1E4"],
        tasks=[{"type": "item", "item": "mekanism:ultimate_control_circuit"}],
        rewards=cog(64),
    ),
    dict(
        key="compressor",
        title=("锇压缩机", "Osmium Compressor"),
        desc=[
            ("用高级电路解锁的高级机器：压缩金属、制造 &7强化锇&r 等关键材料。",
             "An advanced machine unlocked with advanced circuits: compresses metals and produces key materials such as &7Refined Osmium&r."),
        ],
        icon="mekanism:osmium_compressor",
        x=2.5, y=5.0,
        deps=["adv_circuit"],
        tasks=[{"type": "item", "item": "mekanism:osmium_compressor"}],
        rewards=osmium(8),
    ),
    dict(
        key="separator",
        title=("电解分离器", "Electrolytic Separator"),
        desc=[
            ("把流体/气体电解分离（如盐水 → 氢气 + 氯气）。合成需要 &9灌注合金&r 与钢外壳。",
             "Electrolyzes fluids/gases (e.g. brine → hydrogen + chlorine). Crafting requires &9Infused Alloy&r and Steel Casing."),
        ],
        icon="mekanism:electrolytic_separator",
        x=5.0, y=5.0,
        deps=["adv_circuit"],
        tasks=[{"type": "item", "item": "mekanism:electrolytic_separator"}],
        rewards=cog(16),
    ),

    # ================= 新增：材料与升级 =================
    dict(
        key="enriched",
        title=("富集材料", "Enriched Materials"),
        desc=[
            ("富集仓把普通材料变成「富集」形态：碳、红石、钻石、黑曜石、萤石、铁、金、锡……",
             "The Enrichment Chamber turns common materials into Enriched forms: Carbon, Redstone, Diamond, Obsidian, Glowstone, Iron, Gold, Tin…"),
            ("&8富集碳&r 是炼钢与基础电路的关键；&c富集红石&r 用于高级灌注；&7富集钻石→强化黑曜石&r、&e富集萤石→强化萤石&r 是后期的核心材料。",
             "&8Enriched Carbon&r is key to steel and circuits; &cEnriched Redstone&r for advanced infusions; &7Enriched Diamond → Refined Obsidian&r and &eEnriched Glowstone → Refined Glowstone&r are late-game staples."),
        ],
        icon="mekanism:enriched_redstone",
        x=0.0, y=7.5,
        deps=["infuser"],
        tasks=[{"type": "item", "item": "mekanism:enriched_carbon"}],
        rewards=cog(8),
    ),
    dict(
        key="alloy_infused",
        title=("灌注合金", "Infused Alloy"),
        desc=[
            ("用 &c富集红石&r 灌注铁锭，得到灌注合金——高级电路、电解分离器等中级机器的骨架材料。",
             "Infuse iron with &cEnriched Redstone&r to get Infused Alloy — the backbone of advanced circuits and mid-tier machines such as the Electrolytic Separator."),
        ],
        icon="mekanism:alloy_infused",
        x=5.0, y=7.5,
        deps=["infuser"],
        tasks=[{"type": "item", "item": "mekanism:alloy_infused"}],
        rewards=cog(8),
    ),
    dict(
        key="alloy_reinforced",
        title=("强化合金", "Reinforced Alloy"),
        desc=[
            ("用 &7富集钻石&r 灌注灌注合金，得到强化合金——精英机器与核工业的入场材料。",
             "Infuse Infused Alloy with &7Enriched Diamond&r to get Reinforced Alloy — the entry material for elite machines and nuclear engineering."),
        ],
        icon="mekanism:alloy_reinforced",
        x=7.5, y=7.5,
        deps=["alloy_infused", "compressor"],
        tasks=[{"type": "item", "item": "mekanism:alloy_reinforced"}],
        rewards=cog(16),
    ),
    dict(
        key="refined_obsidian",
        title=("强化黑曜石（与强化萤石）", "Refined Obsidian (and Glowstone)"),
        desc=[
            ("在锇压缩机中用 &7富集钻石&r 压缩黑曜石 → &8强化黑曜石锭&r；用 &e富集萤石&r 压缩萤石 → &e强化萤石锭&r。",
             "In the Osmium Compressor: &7Enriched Diamond + Obsidian → Refined Obsidian Ingot&r; &eEnriched Glowstone + Glowstone → Refined Glowstone Ingot&r."),
            ("两者是原子合金、强化黑曜石工具与后期模块的关键材料。",
             "Both are key materials for Atomic Alloy, Refined Obsidian tools and late-game modules."),
        ],
        icon="mekanism:ingot_refined_obsidian",
        x=2.5, y=7.5,
        deps=["enriched", "compressor"],
        tasks=[{"type": "item", "item": "mekanism:ingot_refined_obsidian"}],
        rewards=cog(16),
    ),
    dict(
        key="alloy_atomic",
        title=("原子合金", "Atomic Alloy"),
        desc=[
            ("用 &8强化黑曜石锭&r 灌注强化合金，得到原子合金——激光、Meka-Tool 与顶级机器的核心材料。",
             "Infuse Reinforced Alloy with &8Refined Obsidian Ingot&r to get Atomic Alloy — the core material of the Laser, Meka-Tool and top-tier machines."),
        ],
        icon="mekanism:alloy_atomic",
        x=5.0, y=10.0,
        deps=["alloy_reinforced", "refined_obsidian"],
        tasks=[{"type": "item", "item": "mekanism:alloy_atomic"}],
        rewards=cog(16),
    ),
    dict(
        key="upgrades",
        title=("机器升级芯片", "Machine Upgrades"),
        desc=[
            ("升级芯片装进机器就能改造它：&b速度&r、&a能量&r、&7静音&r、&3气体&r、&6过滤器&r、&e锚定（区块加载）&r……",
             "Upgrades customize machines: &bSpeed&r, &aEnergy&r, &7Muffling&r, &3Gas&r, &6Filter&r, &eAnchor (chunk-load)&r…"),
            ("速度升级会按比例增加能耗；后期流水线一般「速度拉满 + 能量升级补足」。",
             "Speed upgrades scale energy usage; late-game lines usually max Speed and compensate with Energy upgrades."),
        ],
        icon="mekanism:upgrade_speed",
        x=7.5, y=10.0,
        deps=["adv_circuit"],
        tasks=[{"type": "item", "item": "mekanism:upgrade_speed", "count": 4}],
        rewards=cog(16),
    ),
    dict(
        key="factories",
        title=("工厂系列（并行加工）", "Factories (Parallel Processing)"),
        desc=[
            ("把机器升级为「工厂」后，一台机器可同时处理多个配方：基础 3 并行 → 高级 5 → 精英 7 → 终极 9。",
             "Upgrading machines into Factories processes several recipes at once: Basic 3 → Advanced 5 → Elite 7 → Ultimate 9 parallel operations."),
            ("富集/粉碎/冶炼/锯木/灌注/压射/提纯/混合 八种机器都有工厂版；后期产能核心。",
             "All eight machine types (Enriching/Crushing/Smelting/Sawing/Infusing/Injecting/Purifying/Combining) have factory versions — the core of late-game throughput."),
        ],
        icon="mekanism:basic_smelting_factory",
        x=10.0, y=7.5,
        deps=["enrichment", "crusher", "smelter", "sawmill"],
        tasks=[{"type": "item", "item": "mekanism:basic_smelting_factory"}],
        rewards=cog(16),
    ),

    # ================= 新增：动力与发电 =================
    dict(
        key="energy_cube",
        title=("能量立方与能量平板", "Energy Cube & Tablet"),
        desc=[
            ("能量立方是 MEK 的电池（基础容量 2 MFE，可升级到终极）；&9能量平板&r 则是机器合成常用的便携组件。",
             "The Energy Cube is Mekanism's battery (Basic holds 2 MFE, upgradable to Ultimate); the &9Energy Tablet&r is a common crafting component."),
            ("用通用线缆把它们和机器连起来，功率从低到高自动协商。",
             "Link them with Universal Cables — power tiers negotiate automatically."),
        ],
        icon="mekanism:basic_energy_cube",
        x=10.0, y=0.0,
        deps=["casing"],
        tasks=[{"type": "item", "item": "mekanism:basic_energy_cube"}],
        rewards=cog(8),
    ),
    dict(
        key="cables",
        title=("通用线缆", "Universal Cables"),
        desc=[
            ("MEK 的电力靠通用线缆传输；更高等级的线缆能承载更高电压、损耗更低。",
             "Mekanism power flows through Universal Cables; higher tiers carry more voltage with less loss."),
            ("注意：MEK 线缆是「推拉式」——机器会被动地向网络推电，无需额外配置。",
             "Note: Mekanism cables are push/pull — machines feed the network automatically."),
        ],
        icon="mekanism:basic_universal_cable",
        x=10.0, y=-2.5,
        deps=["casing"],
        tasks=[{"type": "item", "item": "mekanism:basic_universal_cable", "count": 8}],
        rewards=cog(8),
    ),
    dict(
        key="heat_generator",
        title=("热力发电机", "Heat Generator"),
        desc=[
            ("入门发电机：燃烧固体燃料（煤炭、木板、岩浆桶……）发电，也可用岩浆给相邻的机器加热。",
             "The entry generator: burns solid fuel (coal, planks, lava buckets…) and can also heat adjacent machines with lava."),
            ("用它给灌注机、富集仓供电，正式开车。",
             "Use it to power the Metallurgic Infuser and Enrichment Chamber — your Mekanism industry starts here."),
        ],
        icon="mekanismgenerators:heat_generator",
        x=12.5, y=-5.0,
        deps=["energy_cube"],
        tasks=[{"type": "item", "item": "mekanismgenerators:heat_generator"}],
        rewards=cog(8),
    ),
    dict(
        key="gas_generator",
        title=("燃气发电机", "Gas-Burning Generator"),
        desc=[
            ("燃烧气体发电：氢气、乙烯、D-T 燃料……其中 &a乙烯&r 是性价比之王（加压反应室产）。",
             "Burns gasses for power: Hydrogen, Ethylene, D-T Fuel… &aEthylene&r is the best value (made in the Pressurized Reaction Chamber)."),
            ("燃气发电机的发电量随燃料热值变化，适合作为中期主力电源。",
             "Output scales with the gas's energy value — a solid mid-game power backbone."),
        ],
        icon="mekanismgenerators:gas_burning_generator",
        x=12.5, y=-2.5,
        deps=["heat_generator", "separator"],
        tasks=[{"type": "item", "item": "mekanismgenerators:gas_burning_generator"}],
        rewards=cog(16),
    ),
    dict(
        key="solar_wind",
        title=("太阳能与风力发电机", "Solar & Wind Generators"),
        desc=[
            ("&e太阳能发电机&r：白天稳定发电（雨天/夜晚衰减），可升级为&6先进太阳能&r；",
             "&eSolar Generator&r: steady daytime power (weaker in rain/night), upgradable to &6Advanced Solar&r;"),
            ("&b风力发电机&r：全天候发电，但必须放在高处（y≥ 越高越强）且不能有方块遮挡。",
             "&bWind Generator&r: runs day and night, but must be placed high with clear sky (output scales with height)."),
        ],
        icon="mekanismgenerators:solar_generator",
        x=15.0, y=-5.0,
        deps=["heat_generator"],
        tasks=[
            {"type": "item", "item": "mekanismgenerators:solar_generator"},
            {"type": "item", "item": "mekanismgenerators:wind_generator"},
        ],
        rewards=cog(16),
    ),
    dict(
        key="induction",
        title=("感应矩阵（大型储电）", "Induction Matrix"),
        desc=[
            ("用感应外壳 + 端口 + 感应电池/供应器搭建的巨型储电多方块，容量可达数十亿 FE。",
             "A giant multiblock battery built from Induction Casing + Ports + Induction Cells/Providers — holds billions of FE."),
            ("需要玻璃/钢外壳打底；后期核电与聚变的缓冲仓。",
             "Needs glass/steel casing in the structure; the buffer for late-game fission and fusion power."),
        ],
        icon="mekanism:induction_casing",
        x=12.5, y=2.5,
        deps=["adv_circuit", "energy_cube"],
        tasks=[{"type": "item", "item": "mekanism:induction_casing", "count": 4}],
        rewards=cog(32),
    ),

    # ================= 新增：化学与矿石处理 =================
    dict(
        key="oxidizer",
        title=("化学氧化器", "Chemical Oxidizer"),
        desc=[
            ("把固体转成气体：&a氧气&r（富集红石/铁矿）、&7氢气&r（铁/锌）、&5乙烯&r（生物燃料）等都从它开始。",
             "Converts solids into gasses: &aOxygen&r (enriched redstone/iron), &7Hydrogen&r (iron/zinc), &5Ethylene&r (bio fuel) all start here."),
            ("气体要先用&3加压管道&r或&3基础化学品罐&r接出来。",
             "Gasses need &3Pressurized Tubes&r or &3Basic Chemical Tanks&r to move around."),
        ],
        icon="mekanism:chemical_oxidizer",
        x=10.0, y=5.0,
        deps=["separator"],
        tasks=[{"type": "item", "item": "mekanism:chemical_oxidizer"}],
        rewards=cog(8),
    ),
    dict(
        key="chemical_infuser",
        title=("化学混合器", "Chemical Infuser"),
        desc=[
            ("把两种气体合成新气体：氢气 + 氯气 → &c盐酸&r；二氧化硫 + 氧气 → &6三氧化硫&r → 硫酸。",
             "Combines two gasses: Hydrogen + Chlorine → &cHydrochloric Acid&r; Sulfur Dioxide + Oxygen → &6Sulfur Trioxide&r → Sulfuric Acid."),
            ("&c盐酸&r 与 &6硫酸&r 是 4x/5x 矿石处理链的钥匙。",
             "&cHydrochloric Acid&r and &6Sulfuric Acid&r are the keys to 4x/5x ore processing."),
        ],
        icon="mekanism:chemical_infuser",
        x=12.5, y=5.0,
        deps=["oxidizer"],
        tasks=[{"type": "item", "item": "mekanism:chemical_infuser"}],
        rewards=cog(16),
    ),
    dict(
        key="prc",
        title=("加压反应室", "Pressurized Reaction Chamber"),
        desc=[
            ("气液固三态反应器：水 + 生物燃料 → &5乙烯&r；乙烯 + 氧气 → &aHDPE 片&r（高级材料）。",
             "A gas/fluid/item reactor: Water + Bio Fuel → &5Ethylene&r; Ethylene + Oxygen → &aHDPE Sheets&r (advanced material)."),
            ("&aHDPE&r 是 MekaSuit 与后期组件的必备合成材料。",
             "&aHDPE&r is required for the MekaSuit and many late-game components."),
        ],
        icon="mekanism:pressurized_reaction_chamber",
        x=15.0, y=5.0,
        deps=["chemical_infuser"],
        tasks=[{"type": "item", "item": "mekanism:pressurized_reaction_chamber"}],
        rewards=cog(16),
    ),
    dict(
        key="rotary",
        title=("旋转冷凝器", "Rotary Condensentrator"),
        desc=[
            ("流体 ↔ 气体的双向转换机（如 水 ↔ 水蒸气、硫 → 二氧化硫）。",
             "A two-way fluid ↔ gas converter (e.g. Water ↔ Steam, Sulfur → Sulfur Dioxide)."),
            ("硫酸链与热蒸发链都靠它来回转换。",
             "Both the sulfuric-acid chain and the thermal-evaporation chain rely on it."),
        ],
        icon="mekanism:rotary_condensentrator",
        x=10.0, y=2.5,
        deps=["separator"],
        tasks=[{"type": "item", "item": "mekanism:rotary_condensentrator"}],
        rewards=cog(8),
    ),
    dict(
        key="thermal_evap",
        title=("热蒸发厂（盐水 → 锂）", "Thermal Evaporation Plant"),
        desc=[
            ("用热蒸发方块搭建的多方块结构，把 &9盐水&r 逐级浓缩成 &7锂&r（聚变燃料的重要来源）。",
             "A multiblock made of Thermal Evaporation Blocks that concentrates &9Brine&r into &7Lithium&r (a key fusion fuel source)."),
            ("需要控制器 + 阀门 + 加热源（太阳能/热力发电机等）。",
             "Requires a Controller + Valve + a heat source (solar panels, Heat Generator…)."),
        ],
        icon="mekanism:thermal_evaporation_controller",
        x=12.5, y=0.0,
        deps=["rotary"],
        tasks=[{"type": "item", "item": "mekanism:thermal_evaporation_controller"}],
        rewards=cog(16),
    ),
    dict(
        key="injection",
        title=("化学压射室（4x 矿石）", "Chemical Injection Chamber (4x Ore)"),
        desc=[
            ("把矿石/原矿用 &c盐酸&r 压射成 &b碎片（Shard）&r，是 4 倍矿石链的关键一步。",
             "Injects ores/raw ores with &cHydrochloric Acid&r to make &bShards&r — the key step of 4x ore processing."),
            ("碎片 → 净化 → 粉碎 → 富集，最终产出 4 份粉尘。",
             "Shard → Purify → Crush → Enrich yields 4 dusts per ore."),
        ],
        icon="mekanism:chemical_injection_chamber",
        x=10.0, y=10.0,
        deps=["enrichment", "oxidizer"],
        tasks=[{"type": "item", "item": "mekanism:chemical_injection_chamber"}],
        rewards=cog(16),
    ),
    dict(
        key="purification",
        title=("净化室（3x 矿石）", "Purification Chamber (3x Ore)"),
        desc=[
            ("用 &a氧气&r 把矿石净化成 &6碎块（Clump）&r；碎块粉碎成污浊粉、富集后得 3 份粉尘。",
             "Purifies ores with &aOxygen&r into &6Clumps&r; clumps crush into dirty dust and enrich into 3 dusts."),
            ("是 4x/5x 链的中间站，也可以单独用作 3 倍矿。",
             "A middle station for the 4x/5x chains, or a standalone 3x ore line."),
        ],
        icon="mekanism:purification_chamber",
        x=12.5, y=10.0,
        deps=["injection"],
        tasks=[{"type": "item", "item": "mekanism:purification_chamber"}],
        rewards=cog(16),
    ),
    dict(
        key="dissolution",
        title=("化学溶解室（5x 起点）", "Chemical Dissolution Chamber (5x Start)"),
        desc=[
            ("用 &6硫酸&r 把矿石完全溶解成 &9矿浆（Slurry）&r——5 倍矿石链的起点。",
             "Dissolves ores with &6Sulfuric Acid&r into &9Slurry&r — the start of 5x ore processing."),
            ("后续：化学清洗机 → 化学结晶器 → 压射 → 净化 → 粉碎 → 富集 = 5 份粉尘。",
             "Next: Chemical Washer → Chemical Crystallizer → Inject → Purify → Crush → Enrich = 5 dusts."),
        ],
        icon="mekanism:chemical_dissolution_chamber",
        x=15.0, y=10.0,
        deps=["purification"],
        tasks=[{"type": "item", "item": "mekanism:chemical_dissolution_chamber"}],
        rewards=cog(16),
    ),
    dict(
        key="washer_chem",
        title=("化学清洗机", "Chemical Washer"),
        desc=[
            ("用清水把矿浆洗成&a纯净矿浆&r（脏矿浆 → 纯净矿浆），提升后续结晶效率。",
             "Washes slurry with water into &aClean Slurry&r, improving crystallization efficiency."),
        ],
        icon="mekanism:chemical_washer",
        x=17.5, y=10.0,
        deps=["dissolution"],
        tasks=[{"type": "item", "item": "mekanism:chemical_washer"}],
        rewards=cog(16),
    ),
    dict(
        key="crystallizer",
        title=("化学结晶器（5x 终点前站）", "Chemical Crystallizer"),
        desc=[
            ("把纯净矿浆结晶成&b晶体&r；晶体再走压射→净化→粉碎→富集，一个矿石变 5 份粉尘。",
             "Crystallizes clean slurry into &bCrystals&r; then Inject → Purify → Crush → Enrich turns one ore into 5 dusts."),
            ("至此你的矿石处理链全部打通（2x/3x/4x/5x 自选）。",
             "This completes the full ore pipeline (2x/3x/4x/5x — your choice)."),
        ],
        icon="mekanism:chemical_crystallizer",
        x=20.0, y=10.0,
        deps=["washer_chem"],
        tasks=[{"type": "item", "item": "mekanism:chemical_crystallizer"}],
        rewards=cog(32),
    ),
    dict(
        key="centrifuge",
        title=("同位素离心机（铀浓缩）", "Isotopic Centrifuge"),
        desc=[
            ("核燃料链的核心：把 &6六氟化铀&r 离心分离，得到 &a浓缩铀&r。",
             "The core of the nuclear fuel chain: centrifuges &6Uranium Hexafluoride&r into &aFissile Fuel&r."),
            ("配套链：铀 → 氢氟酸 → 六氟化铀 → 离心 → 裂变燃料。",
             "Chain: Uranium → Hydrofluoric Acid → Uranium Hexafluoride → Centrifuge → Fissile Fuel."),
        ],
        icon="mekanism:isotopic_centrifuge",
        x=17.5, y=5.0,
        deps=["chemical_infuser"],
        tasks=[{"type": "item", "item": "mekanism:isotopic_centrifuge"}],
        rewards=cog(16),
    ),

    # ================= 新增：核工业与终局 =================
    dict(
        key="sodium",
        title=("太阳能中子活化器", "Solar Neutron Activator"),
        desc=[
            ("核链的转化器：&7核废料&r → &d钋&r（Polonium）；&7锂&r → &b氚&r（Tritium，聚变燃料）。",
             "The nuclear converter: &7Nuclear Waste&r → &dPolonium&r; &7Lithium&r → &bTritium&r (fusion fuel)."),
            ("钋粒是 MekaSuit / Meka-Tool 的必需品，氚则是聚变燃料的一半。",
             "Polonium is required for the MekaSuit / Meka-Tool; Tritium is half of the fusion fuel."),
        ],
        icon="mekanism:solar_neutron_activator",
        x=17.5, y=7.5,
        deps=["prc"],
        tasks=[{"type": "item", "item": "mekanism:solar_neutron_activator"}],
        rewards=cog(16),
    ),
    dict(
        key="laser",
        title=("激光与点火", "Laser & Ignition"),
        desc=[
            ("激光把能量聚焦成光束，用于&c点燃聚变反应堆&r；激光放大器可串联增强。",
             "The Laser focuses energy into a beam used to &cignite the Fusion Reactor&r; Laser Amplifiers chain to boost it."),
            ("超临界相移器（SPS）的超导线圈也需要激光。",
             "The Supercritical Phase Shifter's Supercharged Coils also need Lasers."),
        ],
        icon="mekanism:laser",
        x=12.5, y=12.5,
        deps=["alloy_atomic"],
        tasks=[{"type": "item", "item": "mekanism:laser"}],
        rewards=cog(16),
    ),
    dict(
        key="fission",
        title=("裂变反应堆", "Fission Reactor"),
        desc=[
            ("用&a裂变燃料&r驱动的多方块反应堆：产出热量与&7核废料&r。",
             "A multiblock reactor powered by &aFissile Fuel&r: produces heat and &7Nuclear Waste&r."),
            ("&c注意辐射&r：燃料温度过高会熔毁（可控核事故），废料要用&9放射性废料桶&r封存；废料正是&d钋&r的来源。",
             "&cMind the radiation&r: overheating melts down; store waste in &9Radioactive Waste Barrels&r — that waste is the source of &dPolonium&r."),
            ("结构：裂变机壳 + 端口 + 燃料组件（+ 控制棒组件调节反应）。",
             "Structure: Fission Casing + Ports + Fuel Assemblies (Control Rod Assemblies regulate the reaction)."),
        ],
        icon="mekanismgenerators:fission_reactor_casing",
        x=17.5, y=12.5,
        deps=["centrifuge", "alloy_reinforced"],
        tasks=[{"type": "item", "item": "mekanismgenerators:fission_reactor_casing", "count": 8}],
        rewards=cog(32),
    ),
    dict(
        key="boiler",
        title=("热电锅炉", "Thermoelectric Boiler"),
        desc=[
            ("裂变反应堆的热量在这里把水烧成&7蒸汽&r；需要锅炉外壳 + 阀门 + &c过热元件&r + 压力分散器。",
             "The fission reactor's heat boils water into &7Steam&r here; requires Boiler Casing + Valve + &cSuperheating Elements&r + Pressure Dispersers."),
            ("蒸汽再送进工业涡轮机发电。",
             "The steam then feeds the Industrial Turbine for power."),
        ],
        icon="mekanism:boiler_casing",
        x=15.0, y=15.0,
        deps=["fission"],
        tasks=[{"type": "item", "item": "mekanism:boiler_casing", "count": 4}],
        rewards=cog(16),
    ),
    dict(
        key="turbine",
        title=("工业涡轮机", "Industrial Turbine"),
        desc=[
            ("蒸汽驱动的多方块发电机：涡轮机外壳 + 轮叶 + 转子 + 阀门，规模越大发电越多。",
             "A steam-driven multiblock generator: Turbine Casing + Blades + Rotor + Valve — bigger means more power."),
            ("裂变 → 锅炉 → 涡轮 是稳定的核电三相套。",
             "Fission → Boiler → Turbine is the stable nuclear power triad."),
        ],
        icon="mekanismgenerators:turbine_rotor",
        x=17.5, y=15.0,
        deps=["boiler"],
        tasks=[
            {"type": "item", "item": "mekanismgenerators:turbine_casing", "count": 8},
            {"type": "item", "item": "mekanismgenerators:turbine_rotor"},
        ],
        rewards=cog(32),
    ),
    dict(
        key="fusion",
        title=("聚变反应堆", "Fusion Reactor"),
        desc=[
            ("核工业的顶点之一：用 &bD-T 燃料&r（氘 + 氚）与&c激光点火&r运行，输出巨量电力。",
             "One of the peaks of nuclear engineering: runs on &bD-T Fuel&r (Deuterium + Tritium) ignited by a &cLaser&r, outputting enormous power."),
            ("结构：聚变控制器 + 聚变框架 + 端口 + 激光聚焦矩阵。",
             "Structure: Fusion Controller + Frames + Ports + Laser Focus Matrix."),
            ("聚变产出的电力足以支撑整个后期工厂；下一步是反物质。",
             "Its power can run an entire late-game factory; next stop: Antimatter."),
        ],
        icon="mekanismgenerators:fusion_reactor_controller",
        x=20.0, y=15.0,
        deps=["turbine", "laser"],
        tasks=[{"type": "item", "item": "mekanismgenerators:fusion_reactor_controller"}],
        rewards=cog(64),
    ),
    dict(
        key="sps",
        title=("超临界相移器（SPS）", "Supercritical Phase Shifter"),
        desc=[
            ("用 &d钋&r + 巨量能量把物质相移，产出&5反物质&r（Antimatter）。",
             "Phase-shifts matter using &dPolonium&r and massive energy to produce &5Antimatter&r."),
            ("结构：SPS 外壳 + 端口 + &c超级线圈&r（超导线圈需要激光与钋粒）。",
             "Structure: SPS Casing + Ports + &cSupercharged Coils&r (which need Lasers and Polonium)."),
        ],
        icon="mekanism:sps_casing",
        x=22.5, y=15.0,
        deps=["fusion"],
        tasks=[{"type": "item", "item": "mekanism:sps_casing", "count": 8}],
        rewards=cog(64),
    ),
    dict(
        key="antimatter",
        title=("反物质粒", "Antimatter Pellet"),
        desc=[
            ("把反物质气体压制成&5反物质粒&r——MEK 的终极材料，用于反质子核合成器等终局设备。",
             "Compress Antimatter gas into &5Antimatter Pellets&r — Mekanism's ultimate material for endgame devices such as the Antiprotonic Nucleosynthesizer."),
        ],
        icon="mekanism:pellet_antimatter",
        x=22.5, y=17.5,
        deps=["sps"],
        tasks=[{"type": "item", "item": "mekanism:pellet_antimatter"}],
        rewards=cog(64),
    ),

    # ================= 新增：装备与工具 =================
    dict(
        key="atomic_disassembler",
        title=("原子分解器", "Atomic Disassembler"),
        desc=[
            ("MEK 的招牌工具：一键挖矿/砍树/收割，可调速度、范围与精准采集。",
             "Mekanism's iconic tool: mines, chops and harvests in one — adjustable speed, area and silk touch."),
            ("合成主料是&9能量平板&r；它也是 Meka-Tool 的前置。",
             "Its main component is the &9Energy Tablet&r; it is also the prerequisite of the Meka-Tool."),
        ],
        icon="mekanism:atomic_disassembler",
        x=-5.0, y=0.0,
        deps=["adv_circuit"],
        tasks=[{"type": "item", "item": "mekanism:atomic_disassembler"}],
        rewards=cog(16),
    ),
    dict(
        key="jetpack",
        title=("喷气背包", "Jetpack"),
        desc=[
            ("用气体（氢气/氧气）推进的飞行背包，空中长按跳跃键悬停；&7装甲版&r提供护甲与更高效的气体利用。",
             "A gas-powered (Hydrogen/Oxygen) jetpack; hold jump to hover — the &7Armored Jetpack&r adds armor and better gas efficiency."),
            ("记得随身带&3气体罐&r或接上管道补给。",
             "Bring a &3Chemical Tank&r or hook up a gas supply."),
        ],
        icon="mekanism:jetpack",
        x=-5.0, y=-2.5,
        deps=["alloy_infused"],
        tasks=[{"type": "item", "item": "mekanism:jetpack"}],
        rewards=cog(16),
    ),
    dict(
        key="osmium_tools",
        title=("锇制工具与护甲", "Osmium Tools & Armor"),
        desc=[
            ("Mekanism Tools 提供多种材料套装：&7锇&r、&6青铜&r、&b钢&r、&e强化萤石&r、&8强化黑曜石&r、&9青金石&r。",
             "Mekanism Tools adds sets for &7Osmium&r, &6Bronze&r, &bSteel&r, &eRefined Glowstone&r, &8Refined Obsidian&r and &9Lapis Lazuli&r."),
            ("&b钢镐&r 与&8强化黑曜石镐&r 挖掘等级高，&b钢盾&r 可挡下大量伤害；每种材料都有&dPaxel&r（镐斧铲三合一）。",
             "The &bSteel&r and &8Refined Obsidian&r picks mine high tiers, the &bSteel Shield&r blocks a lot; every material has a &dPaxel&r (pick+axe+shovel in one)."),
        ],
        icon="mekanismtools:osmium_paxel",
        x=-5.0, y=2.5,
        deps=["infuser"],
        tasks=[{"type": "item", "item": "mekanismtools:osmium_paxel"}],
        rewards=cog(8),
    ),
    dict(
        key="mekatool",
        title=("Meka-Tool", "Meka-Tool"),
        desc=[
            ("终极工具：以原子分解器为基础，装上模块后可变成镐/斧/铲/剑/弓……还能连接 MEK 网络远程存取。",
             "The ultimate tool: built from the Atomic Disassembler — with modules it becomes a pick/axe/shovel/sword/bow… and links to your Mekanism network."),
            ("合成需要 &d钋粒&r（裂变链产物）+ &9基础感应元件&r + HDPE 片 + 下界合金。",
             "Requires &dPolonium Pellets&r (fission chain) + &9Basic Induction Cells&r + HDPE Sheets + Netherite."),
        ],
        icon="mekanism:meka_tool",
        x=-7.5, y=0.0,
        deps=["atomic_disassembler", "fission"],
        tasks=[{"type": "item", "item": "mekanism:meka_tool"}],
        rewards=cog(32),
    ),
    dict(
        key="modification_station",
        title=("改造站", "Modification Station"),
        desc=[
            ("给 MekaSuit / Meka-Tool 安装模块的工作台；模块通过&9模块基础&r制作。",
             "The workstation that installs modules into the MekaSuit / Meka-Tool; modules are built from the &9Module Base&r."),
        ],
        icon="mekanism:modification_station",
        x=-7.5, y=2.5,
        deps=["mekatool"],
        tasks=[{"type": "item", "item": "mekanism:modification_station"}],
        rewards=cog(16),
    ),
    dict(
        key="modules",
        title=("模块基础", "Module Base"),
        desc=[
            ("所有 MekaSuit 模块的底材（&aHDPE 片&r + 电路…）；装上&9改造站&r后即可安装到套装上。",
             "The substrate of every MekaSuit module (&aHDPE Sheets&r + circuits…); install them at the &9Modification Station&r."),
            ("常用模块：喷气单元、能量单元、护盾单元、营养单元、采矿单元……",
             "Popular modules: Jetpack Unit, Energy Unit, Dosimeter Unit, Nutritional Unit, Mining Unit…"),
        ],
        icon="mekanism:module_base",
        x=-7.5, y=5.0,
        deps=["modification_station"],
        tasks=[{"type": "item", "item": "mekanism:module_base"}],
        rewards=cog(16),
    ),
    dict(
        key="mekasuit",
        title=("MekaSuit 全套", "Full MekaSuit"),
        desc=[
            ("MEK 的终极护甲：四件套以&5下界合金装备&r为底，加入 &d钋粒&r、&9基础感应元件&r 与 HDPE 片。",
             "Mekanism's ultimate armor: netherite gear upgraded with &dPolonium Pellets&r, &9Basic Induction Cells&r and HDPE Sheets."),
            ("装上模块后：飞行、护盾、自动进食、辐射防护、水下呼吸……记得给套装充能！",
             "With modules: flight, shields, auto-feeding, radiation protection, water breathing… don't forget to charge it!"),
        ],
        icon="mekanism:mekasuit_helmet",
        x=-10.0, y=0.0,
        deps=["modules", "fission"],
        tasks=[
            {"type": "item", "item": "mekanism:mekasuit_helmet"},
            {"type": "item", "item": "mekanism:mekasuit_bodyarmor"},
            {"type": "item", "item": "mekanism:mekasuit_pants"},
            {"type": "item", "item": "mekanism:mekasuit_boots"},
        ],
        rewards=cog(64),
    ),

    # ================= 新增：物流与杂项 =================
    dict(
        key="pressurized_tube",
        title=("加压管道（气体）", "Pressurized Tube"),
        desc=[
            ("输送气体的管道；MEK 的气体系统（氧气/氢气/乙烯/核燃料气体）全靠它。",
             "The pipe that moves gasses — Mekanism's gas system (Oxygen/Hydrogen/Ethylene/nuclear gasses) runs on it."),
            ("配套还有&6机械管道&r（流体）与&c热导线&r（热量），四类管道组成完整物流。",
             "Companions: &6Mechanical Pipes&r (fluids) and &cThermodynamic Conductors&r (heat) — four pipe families form the full logistics set."),
        ],
        icon="mekanism:basic_pressurized_tube",
        x=7.5, y=-5.0,
        deps=["casing"],
        tasks=[{"type": "item", "item": "mekanism:basic_pressurized_tube", "count": 8}],
        rewards=cog(8),
    ),
    dict(
        key="logistical_sorter",
        title=("物流分拣器", "Logistical Sorter"),
        desc=[
            ("MEK 的智能分拣机：按物品/标签/模组分配路线，支持颜色标记与自填充。",
             "Mekanism's smart sorter: routes items by item/tag/mod with color tags and self-feeding."),
            ("配合&6物流运输管道&r就能自动化整个基地的物流。",
             "Pair it with &6Logistical Transporters&r to automate your base's item flow."),
        ],
        icon="mekanism:logistical_sorter",
        x=7.5, y=-7.5,
        deps=["casing"],
        tasks=[{"type": "item", "item": "mekanism:logistical_sorter"}],
        rewards=cog(8),
    ),
    dict(
        key="entangloporter",
        title=("量子传送器", "Quantum Entangloporter"),
        desc=[
            ("无线传输电、流体、气体与物品：两个传送器互相绑定即可跨维度传输。",
             "Wireless transfer of energy, fluids, gasses and items — two Entangloporters bound together work across dimensions."),
            ("后期跨基地物流的答案；合成需要&9传送核心&r。",
             "The answer to late-game cross-base logistics; crafting needs the &9Teleportation Core&r."),
        ],
        icon="mekanism:quantum_entangloporter",
        x=5.0, y=-5.0,
        deps=["adv_circuit"],
        tasks=[{"type": "item", "item": "mekanism:quantum_entangloporter"}],
        rewards=cog(16),
    ),
    dict(
        key="qio",
        title=("QIO 量子存储网络", "QIO Storage Network"),
        desc=[
            ("MEK 的无线存储系统：&9QIO 仪表板&r + &9QIO 驱动器阵列&r + 驱动器，全基地远程存取物品。",
             "Mekanism's wireless storage: &9QIO Dashboard&r + &9QIO Drive Array&r + drives give base-wide remote item access."),
            ("驱动器分四档容量（普通/超密/质量/时间膨胀），后期可跑到数十亿物品。",
             "Four drive tiers (Normal/Hyper-Dense/Supermassive/Time-Dilating) scale into billions of items."),
        ],
        icon="mekanism:qio_dashboard",
        x=10.0, y=-5.0,
        deps=["adv_circuit"],
        tasks=[
            {"type": "item", "item": "mekanism:qio_dashboard"},
            {"type": "item", "item": "mekanism:qio_drive_array"},
        ],
        rewards=cog(16),
    ),
    dict(
        key="oredictionificator",
        title=("矿典转换器", "Oredictionificator"),
        desc=[
            ("在矿典（Ore Dictionary）条目之间转换物品：把不同模组的同名矿/锭统一成你想要的版本。",
             "Converts items between Ore Dictionary entries — unify the same metal from different mods into the variant you want."),
            ("在 GT × MEK × 其他模组共存的包里非常实用（例如把各模组锡锭统一）。",
             "Very handy in a GT × Mekanism × friends pack (e.g. unifying Tin from every mod)."),
        ],
        icon="mekanism:oredictionificator",
        x=0.0, y=-5.0,
        deps=["adv_circuit"],
        tasks=[{"type": "item", "item": "mekanism:oredictionificator"}],
        rewards=cog(8),
    ),
    dict(
        key="appliedmek",
        title=("通用机械 × AE2：应用通量", "Mekanism × AE2: Applied Mekanistics"),
        desc=[
            ("&bApplied Mekanistics&r 让 AE2 网络可以存取 MEK 的&3气体&r：气体存储元件、气体终端与自动化接口。",
             "&bApplied Mekanistics&r lets AE2 store Mekanism &3gasses&r: chemical storage cells, gas terminals and automation interfaces."),
            ("配合 QIO 与量子传送器，整个基地的气体物流都能进 AE2。",
             "Together with QIO and Entangloporters, your whole base's gas logistics can live inside AE2."),
        ],
        icon="appliedmekanistics:chemical_storage_cell_1k",
        x=2.5, y=-5.0,
        deps=["separator"],
        tasks=[{"type": "checkmark", "title": ("我已了解气体进 AE2 的方式", "I understand how gasses enter AE2")}],
        rewards=cog(16),
    ),
]


def collect_existing_ids():
    """收集其它章节/奖励表里的全部 ID（保证全局唯一）。"""
    ids = set()
    pat = re.compile(r'\bid:\s*"([0-9A-Fa-f]{16})"')
    for d in (CHAPTERS_DIR, REWARD_TABLES_DIR):
        if not os.path.isdir(d):
            continue
        for fn in os.listdir(d):
            if fn.endswith(".snbt") and fn != f"{CHAPTER_FILENAME}.snbt":
                with open(os.path.join(d, fn), encoding="utf-8") as f:
                    ids.update(m.upper() for m in pat.findall(f.read()))
    return ids


def make_id(rng, used):
    """16 位 HEX；首位必须 0-7（FTBQ 用有符号 Long 解析，首位 ≥8 会溢出被游戏重生成）。"""
    while True:
        i = rng.choice("01234567") + "".join(rng.choice("0123456789ABCDEF") for _ in range(15))
        if i not in used:
            used.add(i)
            return i


def split_quest_blocks(text):
    """把 quests: [ ... ] 切成顶层 { } 块（按括号配平）。"""
    m = re.search(r'\bquests:\s*\[', text)
    assert m, "找不到 quests: ["
    i = m.end()
    depth = 1
    blocks = []
    start = None
    while i < len(text):
        c = text[i]
        if c == '{':
            if depth == 1:
                start = i
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 1 and start is not None:
                blocks.append(text[start:i + 1])
                start = None
        elif c == ']' and depth == 1:
            break
        i += 1
    return blocks


def parse_section_ids(block, section):
    """取块内某一段（tasks/rewards）里按出现顺序的全部 id。"""
    m = re.search(r'\b' + section + r':\s*\[', block)
    if not m:
        return []
    j = m.end()
    depth = 1
    end = j
    while end < len(block) and depth > 0:
        if block[end] == '[':
            depth += 1
        elif block[end] == ']':
            depth -= 1
        end += 1
    seg = block[m.end():end]
    return [x.upper() for x in re.findall(r'\bid:\s*"([0-9A-Fa-f]{16})"', seg)]


# 旧文件（v1）里的任务顺序 —— 用于把旧 ID 按 key 正确回填。
# ⚠ 新增任务一律追加到 QUESTS 列表末尾；若在既有任务之间插入，必须同步维护此表，
#    否则旧 ID 会错位到别的任务上（玩家进度错乱）。
OLD_KEY_ORDER = [
    "infuser", "casing", "circuit", "gregmek", "enrichment", "crusher",
    "smelter", "sawmill", "adv_circuit", "compressor", "separator",
]


def load_previous_ids():
    """读现有章节：返回 (chapter_id, {key: {'qid','tasks',[...],'rewards',[...]}})
    旧文件按 OLD_KEY_ORDER 的 key 对齐（而不是按新列表下标）。"""
    if not os.path.exists(CHAPTER_FILE):
        return None, {}
    text = open(CHAPTER_FILE, encoding="utf-8").read()
    cm = re.search(r'\bid:\s*"([0-9A-Fa-f]{16})"', text)
    chapter_id = cm.group(1).upper() if cm else None
    blocks = split_quest_blocks(text)
    out = {}
    for i, b in enumerate(blocks):
        if i >= len(OLD_KEY_ORDER):
            break
        qid_m = re.search(r'\bid:\s*"([0-9A-Fa-f]{16})"', b)
        if not qid_m:
            break
        key = OLD_KEY_ORDER[i]
        out[key] = {
            "qid": qid_m.group(1).upper(),
            "tasks": parse_section_ids(b, "tasks"),
            "rewards": parse_section_ids(b, "rewards"),
        }
    return chapter_id, out


def build_snbt():
    rng = random.Random(SEED)
    used = collect_existing_ids()
    prev_chapter_id, prev = load_previous_ids()

    # 章节 ID：优先保持
    if prev_chapter_id:
        chapter_id = prev_chapter_id
        used.add(chapter_id)
    else:
        chapter_id = make_id(rng, used)

    for q in QUESTS:
        p = prev.get(q["key"])
        if p and p["qid"] and p["qid"] not in used:
            q["qid"] = p["qid"]
            used.add(q["qid"])
        else:
            q["qid"] = make_id(rng, used)
        # 任务 ID
        pt = p["tasks"] if p else []
        for k, t in enumerate(q["tasks"]):
            if k < len(pt) and pt[k] and pt[k] not in used:
                t["tid"] = pt[k]
                used.add(pt[k])
            else:
                t["tid"] = make_id(rng, used)
        # 奖励 ID
        pr = p["rewards"] if p else []
        for k, r in enumerate(q.get("rewards") or []):
            if k < len(pr) and pr[k] and pr[k] not in used:
                r["rid"] = pr[k]
                used.add(pr[k])
            else:
                r["rid"] = make_id(rng, used)

    key2id = {q["key"]: q["qid"] for q in QUESTS}
    # 校验依赖
    for q in QUESTS:
        for d in q["deps"]:
            assert d in key2id, "未定义的依赖 key: " + d

    lines = []
    lines.append("{")
    lines.append("\tdefault_hide_dependency_lines: false")
    lines.append('\tdefault_quest_shape: ""')
    lines.append(f'\tfilename: "{CHAPTER_FILENAME}"')
    lines.append(f'\tgroup: "{CHAPTER_GROUP}"')
    lines.append(f'\ticon: "{CHAPTER_ICON}"')
    lines.append(f'\tid: "{chapter_id}"')
    lines.append(f"\torder_index: {CHAPTER_ORDER}")
    lines.append("\tquest_links: [ ]")
    lines.append("\tquests: [")

    for q in QUESTS:
        lines.append("\t\t{")
        deps = [key2id[d] for d in q["deps"]] + list(q.get("ext_deps") or [])
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
    lines.append('\ttitle: ' + json.dumps(CHAPTER_TITLE, ensure_ascii=False))
    lines.append("}")
    return "\n".join(lines) + "\n", chapter_id


def validate(snbt, chapter_id):
    # 1) 所有 16 位 ID 合规且唯一
    ids = re.findall(r'\bid:\s*"([0-9A-Fa-f]{16})"', snbt)
    bad = [i for i in ids if i[0] not in "01234567"]
    assert not bad, "非法 ID（首位 ≥8）: " + str(bad)
    dup = [i for i in set(ids) if ids.count(i) > 1]
    assert not dup, "重复 ID: " + str(dup)
    # 2) 括号配平
    depth = 0
    for c in snbt:
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
        assert depth >= 0
    assert depth == 0, "括号不配平"
    # 3) 任务数
    nq = snbt.count("\t\t{\n")
    return len(ids), nq


def verify_preserved(snbt, prev):
    """按 key 校验旧 ID 是否保持在原任务上（防止插入新任务导致错位）。"""
    if not prev:
        print("ID 保持校验: 无既有文件（全量新建）")
        return
    blocks = split_quest_blocks(snbt)
    key2idx = {q["key"]: i for i, q in enumerate(QUESTS)}
    for key, p in prev.items():
        idx = key2idx.get(key)
        assert idx is not None, "旧任务 key 在新列表中缺失: " + key
        assert idx < len(blocks), "任务块数量不足: " + key
        m = re.search(r'\bid:\s*"([0-9A-Fa-f]{16})"', blocks[idx])
        got = m.group(1).upper() if m else None
        assert got == p["qid"], "ID 未按 key 保持: %s 期望 %s 实得 %s" % (key, p["qid"], got)
    print("ID 保持校验: 通过（%d 个既有任务按 key 对齐）" % len(prev))


def main():
    _, prev = load_previous_ids()
    snbt, chapter_id = build_snbt()
    with open(CHAPTER_FILE, "w", encoding="utf-8", newline="\n") as f:
        f.write(snbt)
    n_ids, n_quests = validate(snbt, chapter_id)
    verify_preserved(snbt, prev)
    print("chapter -> %s  (id=%s)" % (CHAPTER_FILE, chapter_id))
    print("quests: %d | 文件中 ID 总数: %d" % (len(QUESTS), n_ids))
    print("外部前置: %s" % EXT_DEP_LV_FINALE)


if __name__ == "__main__":
    main()
