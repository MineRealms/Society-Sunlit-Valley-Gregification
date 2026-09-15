# -*- coding: utf-8 -*-
"""
MEK（通用机械）章节生成器（Society: Sunlit Valley / 1.20.1 / Mekanism 10.4.16.80）

用法（在整合包根目录执行）：
    python config/ftbquests/tools/build_mek_chapter.py

产出：
    1. config/ftbquests/quests/chapters/mekanism.snbt（内联中文，不写 lang 文件）

说明：
    - 章节挂在「格雷科技」分组（4A46A5E1358A80A6）下，order_index = 17（排在 UV 之后）
    - 入门任务外部前置 = LV 章「铝锭」任务 7567E885B7166603（LV→MV 收尾标志）
    - 机器物品 ID 均核对自 mods/Mekanism-1.20.1-10.4.16.80.jar（lang + recipes）
    - 章节 ID、任务 ID、目标 ID、奖励 ID 使用固定随机种子生成，保证可重复执行
    - 脚本可重复执行：会先移除旧的 mekanism 本地化条目再重新写入
"""

import json
import os
import random
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
CHAPTERS_DIR = os.path.join(ROOT, "config", "ftbquests", "quests", "chapters")
REWARD_TABLES_DIR = os.path.join(ROOT, "config", "ftbquests", "quests", "reward_tables")
LANG_DIR = os.path.join(ROOT, "kubejs", "assets", "ftbquestlocalizer", "lang")
CHAPTER_FILE = os.path.join(CHAPTERS_DIR, "mekanism.snbt")

CHAPTER_FILENAME = "mekanism"
CHAPTER_GROUP = "4A46A5E1358A80A6"  # 格雷科技分组
CHAPTER_ORDER = 17
CHAPTER_ICON = "mekanism:metallurgic_infuser"

SEED = 20260915

# 外部前置：LV 章「铝锭」任务（LV→MV 收尾）
EXT_DEP_LV_FINALE = "7567E885B7166603"

# =====================================================================
# 任务数据
# 字段：
#   key       : 任务键（仅用于依赖引用）
#   title     : (中文, English)
#   desc      : [(中文, English), ...]
#   icon      : 任务图标物品 ID
#   x, y      : 章节内坐标
#   deps      : 依赖的任务 key 列表
#   ext_deps  : 依赖的外部任务 ID 列表（跨章节）
#   tasks     : [{"type": "item", "item": ..., "count": n} | {"type": "checkmark", "title": (zh, en)}]
#   rewards   : [{"item": ..., "count": n}]
# =====================================================================
QUESTS = [
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
        rewards=[{"item": "numismatics:cog", "count": 8}],
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
        rewards=[{"item": "numismatics:cog", "count": 8}],
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
        rewards=[{"item": "numismatics:cog", "count": 8}],
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
        rewards=[{"item": "numismatics:cog", "count": 8}],
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
        rewards=[{"item": "mekanism:ingot_osmium", "count": 4}],
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
        rewards=[{"item": "mekanism:ingot_osmium", "count": 4}],
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
        rewards=[{"item": "mekanism:ingot_osmium", "count": 4}],
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
        rewards=[{"item": "mekanism:ingot_osmium", "count": 4}],
    ),
    dict(
        key="adv_circuit",
        title=("高级控制电路", "Advanced Control Circuit"),
        desc=[
            ("在灌注机中用 &9灌注合金 ×4 + 基础控制电路&r 合成高级控制电路。",
             "Craft an Advanced Control Circuit from &94 Infused Alloys + 1 Basic Control Circuit&r in the Infuser."),
        ],
        icon="mekanism:advanced_control_circuit",
        x=0.0, y=5.0,
        deps=["circuit"],
        tasks=[{"type": "item", "item": "mekanism:advanced_control_circuit"}],
        rewards=[{"item": "numismatics:cog", "count": 16}],
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
        rewards=[{"item": "mekanism:ingot_osmium", "count": 8}],
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
        rewards=[{"item": "numismatics:cog", "count": 16}],
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
    lines.append('\ttitle: "&9MEK&r - 通用机械"')
    lines.append("}")
    return "\n".join(lines) + "\n", chapter_id


def lang_entries():
    out = {}
    out[f"ftbquests.chapter.{CHAPTER_FILENAME}.title"] = ("&9MEK&r - 通用机械", "&9MEK&r - Mekanism")
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
    snbt, chapter_id = build_snbt()
    with open(CHAPTER_FILE, "w", encoding="utf-8", newline="\n") as f:
        f.write(snbt)
    print(f"chapter -> {CHAPTER_FILE}  (id={chapter_id})")
    print(f"quests: {len(QUESTS)}")


if __name__ == "__main__":
    main()
