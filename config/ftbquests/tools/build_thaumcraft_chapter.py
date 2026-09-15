# -*- coding: utf-8 -*-
"""
神秘时代（TC4）入门章节生成器（Society: Sunlit Valley / 1.20.1 / thaumcraft port 20711）

用法（在整合包根目录执行）：
    python config/ftbquests/tools/build_thaumcraft_chapter.py

产出：
    1. config/ftbquests/quests/chapter_groups.snbt —— 新增「神秘时代」分组（若不存在）
    2. config/ftbquests/quests/chapters/thaumcraft.snbt —— 17 个入门任务
    3. 向 kubejs/assets/ftbquestlocalizer/lang/zh_cn.json / en_us.json 插入文本

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
               ("它是神秘学的起点：用它扫描方块与物品，认识隐藏在世界中的&d要素&r。",
                "It is the entry point of Thaumaturgy: scan blocks and items to discover the &dAspects&r hidden in the world.")],
         icon="thaumcraft:thaumometer", x=0.0, y=0.0, deps=[],
         tasks=[{"type": "item", "item": "thaumcraft:thaumometer"}],
         rewards=[{"item": "numismatics:cog", "count": 8}]),
    dict(key="scan", title=("观察世界", "Observe the World"),
         desc=[("手持魔导透镜，对准任意方块或物品&6长按右键&r完成扫描。",
                "Hold the Thaumometer and &6hold right-click&r on any block or item to scan it."),
               ("首次发现的要素会存入你的&d要素池&r，之后的研究都要消耗它。",
                "Newly discovered Aspects are stored in your &dAspect Pool&r — research consumes them later.")],
         icon="thaumcraft:thaumometer", x=2.5, y=0.0, deps=["thaumometer"],
         tasks=[{"type": "checkmark", "title": ("用魔导透镜扫描任意方块或物品", "Scan any block or item with the Thaumometer")}],
         rewards=[{"item": "numismatics:cog", "count": 8}]),
    dict(key="shards", title=("原质碎片", "Primal Shards"),
         desc=[("碎片来自散落在地表与洞穴中的&5水晶簇&r。",
                "Shards come from &5crystal clusters&r found on the surface and in caves."),
               ("透镜、研究、炼金都要用到它——顺手多收集一些。",
                "They are used by the Thaumometer, research and alchemy — gather a few extra.")],
         icon="thaumcraft:air_shard", x=5.0, y=0.0, deps=["thaumometer"],
         tasks=[{"type": "checkmark", "title": ("收集至少 8 个原质碎片", "Collect at least 8 primal shards")}],
         rewards=[{"item": "numismatics:cog", "count": 8}, {"item": "thaumcraft:air_shard", "count": 2}]),
    dict(key="greatwood", title=("宏伟之木", "Greatwood"),
         desc=[("魔法森林中的&5宏伟之木&r是法杖杆与多种魔法制品的材料。",
                "&5Greatwood&r from the magical forest is used for wand rods and many arcane crafts."),
               ("找不到森林？可以在魔导手册的分类里查看它的分布。",
                "Can't find a forest? Check the Thaumonomicon for hints.")],
         icon="thaumcraft:greatwood_log", x=7.5, y=0.0, deps=["thaumometer"],
         tasks=[{"type": "item", "item": "thaumcraft:greatwood_log", "count": 4}],
         rewards=[{"item": "numismatics:cog", "count": 8}]),
    dict(key="wand", title=("学徒法杖", "Wand of the Apprentice"),
         desc=[("用 &62 个铁杖端 + 1 根木棍&r合成&5学徒法杖&r。",
                "Craft the &5Wand of the Apprentice&r from &62 Iron Wand Caps + 1 Wooden Rod&r."),
               ("在这个世界，法杖不只是施法工具，还是各种魔法设备的&6成型核心&r。",
                "Here a wand is not only a casting tool — it is the &6core&r that forms magical devices.")],
         icon="thaumcraft:wand", x=0.0, y=2.5, deps=["thaumometer"],
         tasks=[{"type": "item", "item": "thaumcraft:wand"}],
         rewards=[{"item": "numismatics:cog", "count": 8}]),
    dict(key="thaumonomicon", title=("魔导手册", "Thaumonomicon"),
         desc=[("手持法杖，对着&6书架&r右键——法杖会在仪式中成型为&5魔导手册&r。",
                "Hold your wand and right-click a &6Bookshelf&r — it forms into the &5Thaumonomicon&r."),
               ("一切研究都从这本手册开始；JEI 的&6复合合成&r分类里能看到所有成型蓝图。",
                "All research starts here. The &6Compound Crafting&r category in JEI shows every blueprint.")],
         icon="thaumcraft:thaumonomicon", x=2.5, y=2.5, deps=["wand"],
         tasks=[{"type": "item", "item": "thaumcraft:thaumonomicon"}],
         rewards=[{"item": "numismatics:cog", "count": 16}]),
    dict(key="table", title=("术式桌台", "Arcane Table"),
         desc=[("普通的&6桌子&r是研究台与奥术工作台的基础（普通合成即可）。",
                "A plain &6Table&r is the base for both the Research Table and the Arcane Worktable (normal crafting).")],
         icon="thaumcraft:table", x=5.0, y=2.5, deps=["thaumonomicon"],
         tasks=[{"type": "item", "item": "thaumcraft:table"}],
         rewards=[{"item": "numismatics:cog", "count": 8}]),
    dict(key="inkwell", title=("墨水瓶", "Inkwell"),
         desc=[("用&6玻璃瓶 + 羽毛 + 黑色染料&r合成墨水瓶，研究台成型时需要它。",
                "Craft an Inkwell from &6a Glass Bottle + Feather + Black Dye&r; it is needed to form the Research Table.")],
         icon="thaumcraft:inkwell", x=7.5, y=2.5, deps=["thaumonomicon"],
         tasks=[{"type": "item", "item": "thaumcraft:inkwell"}],
         rewards=[{"item": "numismatics:cog", "count": 8}]),
    dict(key="first_research", title=("第一次研究", "Your First Research"),
         desc=[("打开魔导手册，消耗要素池解锁一项研究。",
                "Open the Thaumonomicon and spend your Aspect Pool to unlock a research entry."),
               ("推荐先研究&6炼金（坩埚）&r与&6奥术工作台&r方向。",
                "Alchemy (Crucible) and the Arcane Worktable are good first choices.")],
         icon="thaumcraft:thaumonomicon", x=0.0, y=5.0, deps=["thaumonomicon"],
         tasks=[{"type": "checkmark", "title": ("在魔导手册中解锁任意一项研究", "Unlock any research in the Thaumonomicon")}],
         rewards=[{"item": "numismatics:cog", "count": 8}]),
    dict(key="crucible", title=("坩埚", "Crucible"),
         desc=[("手持法杖，对着&6炼药锅&r右键，成型为&5坩埚&r。",
                "Hold your wand and right-click a &6Cauldron&r to form the &5Crucible&r."),
               ("炼金的核心设备：把材料溶解成要素，再合成魔法物品。",
                "The heart of alchemy: dissolve materials into Aspects, then craft magical items.")],
         icon="thaumcraft:crucible", x=2.5, y=5.0, deps=["thaumonomicon"],
         tasks=[{"type": "item", "item": "thaumcraft:crucible"}],
         rewards=[{"item": "numismatics:cog", "count": 8}]),
    dict(key="research_table", title=("研究台", "Research Table"),
         desc=[("按蓝图摆放&6两张桌子&r并手持&6墨水瓶&r右键，成型为&5研究台&r（JEI 可查布局）。",
                "Place &6two Tables&r, hold the &6Inkwell&r and right-click to form the &5Research Table&r (see JEI).")],
         icon="thaumcraft:research_table", x=5.0, y=5.0, deps=["table", "inkwell"],
         tasks=[{"type": "item", "item": "thaumcraft:research_table"}],
         rewards=[{"item": "numismatics:cog", "count": 8}]),
    dict(key="arcane_worktable", title=("奥术工作台", "Arcane Worktable"),
         desc=[("手持法杖对着&6桌子&r右键，成型为&5奥术工作台&r。",
                "Hold your wand and right-click a &6Table&r to form the &5Arcane Worktable&r."),
               ("消耗法杖内的魔力，进行魔法合成。",
                "It consumes vis from your wand to craft arcane recipes.")],
         icon="thaumcraft:arcane_worktable", x=7.5, y=5.0, deps=["table"],
         tasks=[{"type": "item", "item": "thaumcraft:arcane_worktable"}],
         rewards=[{"item": "numismatics:cog", "count": 8}]),
    dict(key="nitor", title=("闪耀之光", "Nitor"),
         desc=[("炼金配方：&6荧石粉&r + 要素 &bpotentia 3 / ignis 3 / lux 3&r → &5闪耀之光&r。",
                "Alchemy: &6Glowstone Dust&r + Aspects &bpotentia 3 / ignis 3 / lux 3&r → &5Nitor&r."),
               ("丢进坩埚的材料会提供要素；要永久光源就靠它了。",
                "Materials thrown into the Crucible provide Aspects — this is your permanent light source.")],
         icon="thaumcraft:nitor", x=0.0, y=7.5, deps=["crucible"],
         tasks=[{"type": "item", "item": "thaumcraft:nitor"}],
         rewards=[{"item": "numismatics:cog", "count": 8}]),
    dict(key="alumentum", title=("炼金煤", "Alumentum"),
         desc=[("炼金配方：&6煤炭&r + 要素 &bpotentia 3 / ignis 3 / perditio 3&r → &5炼金煤&r。",
                "Alchemy: &6Coal&r + Aspects &bpotentia 3 / ignis 3 / perditio 3&r → &5Alumentum&r."),
               ("一种高效的魔法燃料，也能当作投掷物使用。",
                "An efficient magical fuel that can also be thrown.")],
         icon="thaumcraft:alumentum", x=2.5, y=7.5, deps=["crucible"],
         tasks=[{"type": "item", "item": "thaumcraft:alumentum"}],
         rewards=[{"item": "numismatics:cog", "count": 8}]),
    dict(key="thaumium", title=("神秘锭", "Thaumium Ingot"),
         desc=[("炼金配方：&6铁锭&r + 要素 &bpraecantatio 4&r → &5神秘锭&r。",
                "Alchemy: &6Iron Ingot&r + Aspect &bpraecantatio 4&r → &5Thaumium Ingot&r."),
               ("比铁更坚硬、更容易附魔的魔法金属，可制作工具与护甲。",
                "A magical metal harder than iron and easier to enchant — tools and armor await.")],
         icon="thaumcraft:thaumium_ingot", x=5.0, y=7.5, deps=["crucible"],
         tasks=[{"type": "item", "item": "thaumcraft:thaumium_ingot"}],
         rewards=[{"item": "numismatics:cog", "count": 16}]),
    dict(key="thaumium_pickaxe", title=("神秘工具", "Thaumium Tools"),
         desc=[("用神秘锭合成&5神秘镐&r（其他工具同理）。",
                "Craft a &5Thaumium Pickaxe&r (other tools work the same way)."),
               ("神秘工具天生容易附魔，是冒险途中的好伙伴。",
                "Thaumium tools accept enchantments eagerly — great companions for adventuring.")],
         icon="thaumcraft:thaumium_pickaxe", x=5.0, y=10.0, deps=["thaumium"],
         tasks=[{"type": "item", "item": "thaumcraft:thaumium_pickaxe"}],
         rewards=[{"item": "numismatics:cog", "count": 16}]),
    dict(key="goggles", title=("揭示之护目镜", "Goggles of Revealing"),
         desc=[("在奥术工作台用&6魔导透镜 + 金锭 + 皮革&r合成&5揭示之护目镜&r（需先研究对应条目）。",
                "Craft the &5Goggles of Revealing&r from &6Thaumometer + Gold + Leather&r at the Arcane Worktable (research required)."),
               ("戴上它，方块与物品的要素会直接显示在视野里。",
                "Wear them to see Aspects on blocks and items directly in the world.")],
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
        if i not in used:
            used.add(i)
            return i


def ensure_group(group_id):
    """把新分组写入 chapter_groups.snbt（若不存在）"""
    with open(GROUPS_FILE, encoding="utf-8") as f:
        text = f.read()
    if group_id in text:
        return False
    key = f"ftbquests.chapter_groups.{int(group_id, 16)}.title"
    entry = f'\t\t{{ id: "{group_id}", title: "{{{key}}}" }}\n'
    marker = "\t]\n}"
    assert marker in text, "chapter_groups.snbt 结构不符合预期"
    text = text.replace(marker, entry + marker)
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
                lines.append(f'\t\t\t\t"{{ftbquests.chapter.{CHAPTER_FILENAME}.quest{q["qid"]}.description{i+1}}}"')
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
                lines.append(f'\t\t\t\ttitle: "{{ftbquests.chapter.{CHAPTER_FILENAME}.quest{q["qid"]}.task.{t["tid"]}.title}}"')
                lines.append('\t\t\t\ttype: "checkmark"')
            lines.append("\t\t\t}]")
        lines.append(f'\t\t\ttitle: "{{ftbquests.chapter.{CHAPTER_FILENAME}.quest{q["qid"]}.title}}"')
        lines.append(f'\t\t\tx: {q["x"]}d')
        lines.append(f'\t\t\ty: {q["y"]}d')
        lines.append("\t\t}")
    lines.append("\t]")
    lines.append(f'\ttitle: "{{ftbquests.chapter.{CHAPTER_FILENAME}.title}}"')
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


def main():
    global GROUP_KEY_ID
    rng = random.Random(SEED + 7)
    used = collect_existing_ids()
    group_id = make_id(rng, used)
    GROUP_KEY_ID = group_id

    created = ensure_group(group_id)
    print(f"分组: {group_id}（{'新增' if created else '已存在'}）")

    snbt, chapter_id = build_snbt(group_id)
    with open(CHAPTER_FILE, "w", encoding="utf-8", newline="\n") as f:
        f.write(snbt)
    print(f"章节 -> {CHAPTER_FILE}  (id={chapter_id})")

    entries = lang_entries(group_id)
    insert_lang(os.path.join(LANG_DIR, "zh_cn.json"), entries, 0)
    insert_lang(os.path.join(LANG_DIR, "en_us.json"), entries, 1)
    print(f"lang entries: {len(entries)}")
    print(f"quests: {len(QUESTS)}")


if __name__ == "__main__":
    main()
