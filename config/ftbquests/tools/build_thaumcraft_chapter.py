# -*- coding: utf-8 -*-
"""
神秘时代（TC4）入门章节生成器（Society: Sunlit Valley / 1.20.1 / thaumcraft port 20711）

用法（在整合包根目录执行）：
    python config/ftbquests/tools/build_thaumcraft_chapter.py

产出：
    1. config/ftbquests/quests/chapter_groups.snbt —— 新增「神秘时代」分组（若不存在）
    2. config/ftbquests/quests/chapters/thaumcraft.snbt —— 17 个入门任务（内联中文，不写 lang 文件）

事实依据（逐条核对，非推测）：
    - 物品/机制：包内 mods/thaumcraft-forge-...-20711.jar
        · 魔导透镜：thaumometer.json（2 金 + 玻璃 + 2 碎片标签）
        · 法杖：wand_wood_iron.json（2 铁杖端 + 木棍）
        · 复合成型（compound_blueprints/default.json）：
            魔导手册 = 法杖 + 书架（触发：书架）
            奥术工作台 = 法杖 + 桌子（触发：桌子）
            研究台 = 墨水瓶 + 桌子×2（触发：桌子）
            坩埚 = 法杖 + 炼药锅（触发：炼药锅）
        · 触发方式：TableBlock/CrucibleBlock 源码 = 手持对应工具右键触发块
          （JEI 有「复合合成」分类展示全部蓝图）
        · 坩埚配方：nitor（荧石粉+potentia3/ignis3/lux3）、alumentum（煤+3/3/3）、
          thaumium（铁锭+praecantatio4）
        · 表格/墨水瓶：普通合成（table 配方、墨水瓶=玻璃瓶+羽毛+黑色染料）
    - 分组标题 lang 键 = 分组 ID 作为无符号 64 位整数的十进制
      （已用 457DCF55318282CA→5007386325515666122 等现有分组验证）
    - 章节/任务 ID 用固定随机种子生成，保证可重复执行；脚本可重复运行
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
CHAPTER_FILE = os.path.join(CHAPTERS_DIR, "thaumcraft.snbt")

CHAPTER_FILENAME = "thaumcraft"
CHAPTER_ORDER = 0
CHAPTER_ICON = "thaumcraft:thaumonomicon"
GROUP_TITLE = ("神秘时代", "Thaumcraft")

SEED = 20260916

# =====================================================================
# 任务数据（17 个；坐标 2D 网格 x:0~7.5 / y:0~10）
# =====================================================================
QUESTS = [
    dict(key="thaumometer", title=("神秘学的起点：魔导透镜", "The First Step: Thaumometer"),
                  desc=[("用 &62 个金锭 + 1 块玻璃 + 2 个任意原质碎片&r合成&5魔导透镜&r。",
                "Craft a &5Thaumometer&r from &62 Gold Ingots + 1 Glass + 2 Shards&r of any type."),
               ("它是神秘学的起点：手持透镜对准方块或物品&6长按右键&r扫描，就能发现隐藏在世界中的&d要素&r（Aspects）。",
                "Hold it and &6hold right-click&r on blocks or items to scan them and discover the &dAspects&r hidden in the world."),
               ("扫描是&6一次性&r的：每种方块/物品首次扫描会永久记入你的要素池，之后再扫描不再获得新要素。",
                "Scanning is &6one-time&r: each new block/item permanently records its aspects into your pool.")],
         icon="thaumcraft:thaumometer", x=0.0, y=0.0, deps=[],
         tasks=[{"type": "item", "item": "thaumcraft:thaumometer"}],
         rewards=[{"item": "numismatics:cog", "count": 8}]),
    dict(key="scan", title=("观察世界", "Observe the World"),
                  desc=[("手持魔导透镜，对准任意方块或物品&6长按右键&r完成扫描；准星上的进度条走满即扫描成功。",
                "Hold the Thaumometer and &6hold right-click&r on any block or item until the progress bar fills."),
               ("首次发现的要素会存入你的&d要素池&r，之后的研究、合成都要消耗它——见到没见过的东西就扫一下。",
                "Newly discovered Aspects are stored in your &dAspect Pool&r and consumed by research and crafting - scan everything new."),
               ("扫描生物同样有效；配合后期的&6揭示之护目镜&r，可以随时看到周围物体的要素。",
                "Scanning mobs works too; later the &6Goggles of Revealing&r show aspects at a glance.")],
         icon="thaumcraft:thaumometer", x=2.5, y=0.0, deps=["thaumometer"],
         tasks=[{"type": "checkmark", "title": ("用魔导透镜扫描任意方块或物品", "Scan any block or item with the Thaumometer")}],
         rewards=[{"item": "numismatics:cog", "count": 8}]),
    dict(key="shards", title=("原质碎片", "Primal Shards"),
                  desc=[("碎片来自散落在地表与洞穴中的&5水晶簇&r，共有六种：风、火、土、水、秩序、熵。",
                "Shards come from &5crystal clusters&r on the surface and in caves - six types: Air, Fire, Earth, Water, Order, Entropy."),
               ("透镜、法杖、研究与炼金都要用到碎片——顺手多收集一些。",
                "They are used by the Thaumometer, wands, research and alchemy - gather extras."),
               ("注意：水晶簇在本整合包中&6不会重新生长&r，碎片属于不可再生资源，请节约使用。",
                "Note: crystal clusters &6do not regrow&r in this pack - shards are non-renewable, use them wisely.")],
         icon="thaumcraft:air_shard", x=5.0, y=0.0, deps=["thaumometer"],
         tasks=[{"type": "checkmark", "title": ("收集至少 8 个原质碎片", "Collect at least 8 primal shards")}],
         rewards=[{"item": "numismatics:cog", "count": 8}, {"item": "thaumcraft:air_shard", "count": 2}]),
    dict(key="greatwood", title=("宏伟之木", "Greatwood"),
                  desc=[("&5宏伟之木&r生长在魔法森林中，是法杖杆与多种魔法制品的材料。",
                "&5Greatwood&r grows in the magical forest and is used for wand rods and many arcane crafts."),
               ("找不到魔法森林？打开魔导手册查看生物群系提示；宏伟之木的树皮与木材都能使用。",
                "Can't find a magical forest? Check the Thaumonomicon for biome hints; both bark and wood are usable."),
               ("顺带留意&5银木&r——它们周围常有魔力节点。",
                "Keep an eye out for &5Silverwood&r - magical nodes often grow near them.")],
         icon="thaumcraft:greatwood_log", x=7.5, y=0.0, deps=["thaumometer"],
         tasks=[{"type": "item", "item": "thaumcraft:greatwood_log", "count": 4}],
         rewards=[{"item": "numismatics:cog", "count": 8}]),
    dict(key="wand", title=("学徒法杖", "Wand of the Apprentice"),
                  desc=[("用 &62 个铁杖端 + 1 根木棍&r合成&5学徒法杖&r。",
                "Craft the &5Wand of the Apprentice&r from &62 Iron Wand Caps + 1 Wooden Rod&r."),
               ("在这个世界，法杖不只是施法工具，还是各种魔法设备的&6成型核心&r——右键书架、桌子、炼药锅等方块就能把它们变成魔法设备。",
                "A wand is not only a casting tool - it is the &6core&r that forms magical devices by right-clicking bookshelves, tables, cauldrons and more."),
               ("法杖施法与成型都会消耗魔力（Vis），可以用魔导手册查看充能方式。",
                "Casting and forming consume Vis; check the Thaumonomicon for how to recharge.")],
         icon="thaumcraft:wand", x=0.0, y=2.5, deps=["thaumometer"],
         tasks=[{"type": "item", "item": "thaumcraft:wand"}],
         rewards=[{"item": "numismatics:cog", "count": 8}]),
    dict(key="thaumonomicon", title=("魔导手册", "Thaumonomicon"),
                  desc=[("手持法杖，对着&6书架&r右键——法杖会在仪式中成型为&5魔导手册&r。",
                "Hold your wand and right-click a &6Bookshelf&r - it forms into the &5Thaumonomicon&r."),
               ("一切研究都从这本手册开始：打开它可以看到研究树，消耗要素池解锁新条目。",
                "All research starts here: open it to see the research tree and spend your aspect pool to unlock entries."),
               ("JEI 的&6复合合成&r分类里能看到所有成型蓝图（法杖 + 方块 → 设备）。",
                "The &6Compound Crafting&r category in JEI shows every blueprint (wand + block = device).")],
         icon="thaumcraft:thaumonomicon", x=2.5, y=2.5, deps=["wand"],
         tasks=[{"type": "item", "item": "thaumcraft:thaumonomicon"}],
         rewards=[{"item": "numismatics:cog", "count": 16}]),
    dict(key="table", title=("术式桌台", "Arcane Table"),
                  desc=[("普通的&6桌子&r（普通合成即可）是研究台与奥术工作台的基础。",
                "A plain &6Table&r (normal crafting) is the base for both the Research Table and the Arcane Worktable."),
               ("建议一次多做几张：研究台需要 2 张桌子，奥术工作台需要 1 张。",
                "Make several: the Research Table needs 2 tables, the Arcane Worktable needs 1.")],
         icon="thaumcraft:table", x=5.0, y=2.5, deps=["thaumonomicon"],
         tasks=[{"type": "item", "item": "thaumcraft:table"}],
         rewards=[{"item": "numismatics:cog", "count": 8}]),
    dict(key="inkwell", title=("墨水瓶", "Inkwell"),
                  desc=[("用&6玻璃瓶 + 羽毛 + 黑色染料&r合成墨水瓶。",
                "Craft an Inkwell from &6a Glass Bottle + Feather + Black Dye&r."),
               ("研究台成型时需要它；研究过程也会消耗墨水，记得多备几个。",
                "It is needed to form the Research Table; research also consumes ink, so stock up.")],
         icon="thaumcraft:inkwell", x=7.5, y=2.5, deps=["thaumonomicon"],
         tasks=[{"type": "item", "item": "thaumcraft:inkwell"}],
         rewards=[{"item": "numismatics:cog", "count": 8}]),
    dict(key="first_research", title=("第一次研究", "Your First Research"),
                  desc=[("打开魔导手册，消耗要素池解锁一项研究。",
                "Open the Thaumonomicon and spend your aspect pool to unlock a research entry."),
               ("推荐先研究&6炼金（坩埚）&r与&6奥术工作台&r方向——它们是后续所有配方的基础。",
                "Start with &6Alchemy (Crucible)&r and the &6Arcane Worktable&r - they are the base for everything else."),
               ("研究需要对应的要素（由扫描获得）；要素不足时，多扫描新方块与物品。",
                "Research needs the matching aspects (gained by scanning) - scan more when you run short.")],
         icon="thaumcraft:thaumonomicon", x=0.0, y=5.0, deps=["thaumonomicon"],
         tasks=[{"type": "checkmark", "title": ("在魔导手册中解锁任意一项研究", "Unlock any research in the Thaumonomicon")}],
         rewards=[{"item": "numismatics:cog", "count": 8}]),
    dict(key="crucible", title=("坩埚", "Crucible"),
                  desc=[("手持法杖，对着&6炼药锅&r右键，成型为&5坩埚&r。",
                "Hold your wand and right-click a &6Cauldron&r to form the &5Crucible&r."),
               ("炼金的核心设备：把材料丢进坩埚，它们会溶解成要素；当要素达到配方要求时，再丢入&6催化剂&r即可合成。",
                "The heart of alchemy: throw materials in to dissolve them into aspects, then add the &6catalyst&r when the aspects match a recipe."),
               ("小心：要素过量会产生&6咒波污染&r，污染会蔓延成腐化之地——炼金时不要乱丢杂物。",
                "Careful: excess aspects create &6Flux&r, which spreads taint - do not dump random items in.")],
         icon="thaumcraft:crucible", x=2.5, y=5.0, deps=["thaumonomicon"],
         tasks=[{"type": "item", "item": "thaumcraft:crucible"}],
         rewards=[{"item": "numismatics:cog", "count": 8}]),
    dict(key="research_table", title=("研究台", "Research Table"),
                  desc=[("按蓝图摆放&6两张桌子&r并手持&6墨水瓶&r右键，成型为&5研究台&r（JEI 可查布局）。",
                "Place &6two Tables&r as shown in the blueprint and right-click with an &6Inkwell&r to form the &5Research Table&r (see JEI)."),
               ("研究台是进行深入研究的工作台；配合魔导手册使用。",
                "The Research Table is your workstation for deeper research; use it together with the Thaumonomicon.")],
         icon="thaumcraft:research_table", x=5.0, y=5.0, deps=["table", "inkwell"],
         tasks=[{"type": "item", "item": "thaumcraft:research_table"}],
         rewards=[{"item": "numismatics:cog", "count": 8}]),
    dict(key="arcane_worktable", title=("奥术工作台", "Arcane Worktable"),
                  desc=[("手持法杖对着&6桌子&r右键，成型为&5奥术工作台&r。",
                "Hold your wand and right-click a &6Table&r to form the &5Arcane Worktable&r."),
               ("在奥术工作台中消耗法杖内的魔力进行魔法合成——比如揭示之护目镜、魔杖部件与各种魔法物品。",
                "It crafts arcane items by spending the wand's Vis - Goggles of Revealing, wand parts and more."),
               ("合成时注意法杖的魔力储备，不足时需要先充能。",
                "Watch your wand's Vis; recharge it when it runs low.")],
         icon="thaumcraft:arcane_worktable", x=7.5, y=5.0, deps=["table"],
         tasks=[{"type": "item", "item": "thaumcraft:arcane_worktable"}],
         rewards=[{"item": "numismatics:cog", "count": 8}]),
    dict(key="nitor", title=("闪耀之光", "Nitor"),
                  desc=[("炼金配方：&6荧石粉&r + 要素 &bpotentia 3 / ignis 3 / lux 3&r → &5闪耀之光&r。",
                "Crucible recipe: &6Glowstone Dust&r + aspects &bpotentia 3 / ignis 3 / lux 3&r = &5Nitor&r."),
               ("丢进坩埚的材料会提供要素；闪耀之光可以放置为永久光源，也能制作其他魔法物品。",
                "Materials thrown in provide aspects; Nitor is a permanent light source and a crafting ingredient.")],
         icon="thaumcraft:nitor", x=0.0, y=7.5, deps=["crucible"],
         tasks=[{"type": "item", "item": "thaumcraft:nitor"}],
         rewards=[{"item": "numismatics:cog", "count": 8}]),
    dict(key="alumentum", title=("炼金煤", "Alumentum"),
                  desc=[("炼金配方：&6煤炭&r + 要素 &bpotentia 3 / ignis 3 / perditio 3&r → &5炼金煤&r。",
                "Crucible recipe: &6Coal&r + aspects &bpotentia 3 / ignis 3 / perditio 3&r = &5Alumentum&r."),
               ("一种高效的魔法燃料（可当煤炭使用），也能当作投掷物造成爆炸伤害。",
                "An efficient magical fuel (works as coal) and a throwable explosive.")],
         icon="thaumcraft:alumentum", x=2.5, y=7.5, deps=["crucible"],
         tasks=[{"type": "item", "item": "thaumcraft:alumentum"}],
         rewards=[{"item": "numismatics:cog", "count": 8}]),
    dict(key="thaumium", title=("神秘锭", "Thaumium Ingot"),
                  desc=[("炼金配方：&6铁锭&r + 要素 &bpraecantatio 4&r → &5神秘锭&r。",
                "Crucible recipe: &6Iron Ingot&r + aspect &bpraecantatio 4&r = &5Thaumium Ingot&r."),
               ("比铁更坚硬、更容易附魔的魔法金属，可制作工具、护甲与更多魔法部件。",
                "A magical metal harder than iron and easier to enchant - used for tools, armor and components."),
               ("神秘锭也是研究&6虚空金属&r（VOIDMETAL）的前置之一。",
                "Thaumium is also a prerequisite for the &6Void Metal&r (VOIDMETAL) research.")],
         icon="thaumcraft:thaumium_ingot", x=5.0, y=7.5, deps=["crucible"],
         tasks=[{"type": "item", "item": "thaumcraft:thaumium_ingot"}],
         rewards=[{"item": "numismatics:cog", "count": 16}]),
    dict(key="thaumium_pickaxe", title=("神秘工具", "Thaumium Tools"),
                  desc=[("用神秘锭合成&5神秘镐&r（其他工具同理）。",
                "Craft the &5Thaumium Pickaxe&r from Thaumium Ingots (other tools work the same way)."),
               ("神秘工具天生容易附魔，是冒险途中的好伙伴；耐久与铁制相当，附魔收益更高。",
                "Thaumium tools are naturally enchantable and make great adventuring gear.")],
         icon="thaumcraft:thaumium_pickaxe", x=5.0, y=10.0, deps=["thaumium"],
         tasks=[{"type": "item", "item": "thaumcraft:thaumium_pickaxe"}],
         rewards=[{"item": "numismatics:cog", "count": 16}]),
    dict(key="goggles", title=("揭示之护目镜", "Goggles of Revealing"),
                  desc=[("在奥术工作台用&6魔导透镜 + 金锭 + 皮革&r合成&5揭示之护目镜&r（需先研究对应条目）。",
                "Craft the &5Goggles of Revealing&r at the Arcane Worktable from &6Thaumometer + Gold + Leather&r (research required)."),
               ("戴上它，方块与物品的要素会直接显示在视野里，无需逐个扫描。",
                "Wear them to see aspects on blocks and items directly - no scanning needed."),
               ("这是整理仓库、规划炼金时最实用的装备。",
                "The most practical gear for organizing storage and planning alchemy.")],
         icon="thaumcraft:goggles_of_revealing", x=7.5, y=7.5, deps=["arcane_worktable"],
         tasks=[{"type": "item", "item": "thaumcraft:goggles_of_revealing"}],
         rewards=[{"item": "numismatics:cog", "count": 32}]),
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
        lines.append("\t\t\ttitle: " + json.dumps(q["title"][0], ensure_ascii=False))
        lines.append(f'\t\t\tx: {q["x"]}d')
        lines.append(f'\t\t\ty: {q["y"]}d')
        lines.append("\t\t}")
    lines.append("\t]")
    lines.append('\ttitle: "&5神秘时代&r - 入门"')
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
    group_id = find_existing_group()
    if group_id is None:
        rng = random.Random(SEED + 7)
        used = collect_existing_ids()
        group_id = make_id(rng, used)
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
