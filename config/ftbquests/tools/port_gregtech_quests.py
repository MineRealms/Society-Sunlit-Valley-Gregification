# -*- coding: utf-8 -*-
"""
GregTech CEu Modern Community Pack → Society: Sunlit Valley
FTB 任务书批量搬运脚本（章节 + 奖励表 + 分组 + 文本键化）

用法（在整合包根目录执行）:
    python config/ftbquests/tools/port_gregtech_quests.py [源任务书目录]

产出:
    1. config/ftbquests/quests/chapters/*.snbt      （17 章，改写分组/顺序/文本键）
    2. config/ftbquests/quests/reward_tables/*.snbt （8 个奖励表）
    3. config/ftbquests/quests/chapter_groups.snbt  （新增「格雷科技」分组）
    4. config/ftbquests/tools/gt_port/en_entries.json    （key -> 英文原文）
    5. config/ftbquests/tools/gt_port/translate_queue.json（待翻译去重文本）

说明:
    - 源包任务书为英文直写文本；本脚本将其转换为 ftbquestlocalizer 语言键
      （ftbquests.chapter.<file>.quest<ID>.*），英文写入 en_entries.json
    - 缺失模组物品统一映射为本包现有替代品（见 REPLACEMENTS）
    - 脚本可重复执行（覆盖章节文件、重建队列；不删除其他章节）
"""

import json
import os
import re
import shutil
import sys

# ---------------------------------------------------------------------
# 路径与常量
# ---------------------------------------------------------------------
TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(TOOLS_DIR, "..", "..", ".."))
DST_QUESTS = os.path.join(ROOT, "config", "ftbquests", "quests")
DST_CHAPTERS = os.path.join(DST_QUESTS, "chapters")
DST_TABLES = os.path.join(DST_QUESTS, "reward_tables")
WORK_DIR = os.path.join(TOOLS_DIR, "gt_port")

DEFAULT_SRC = r"G:\MinecraftGames\GregTech Odyssey(BaopuEdition)\.minecraft\versions\GregTech CEu Modern Community Pack\config\ftbquests\quests"

GROUP_ID = "4A46A5E1358A80A6"
GROUP_TITLE = ("格雷科技", "GregTech")

# 章节顺序（按电压等级 → 资源 → 多方块 → 里程碑）
CHAPTER_ORDER = {
    "gtceu": 0,
    "steam_age": 1,
    "lv__low_voltage": 2,
    "mv__medium_voltage": 3,
    "hv__high_voltage": 4,
    "ev__extreme_voltage": 5,
    "iv__insane_voltage": 6,
    "luv__ludicrous_voltage": 7,
    "zpm__zero_point_module": 8,
    "uv__ultimate_voltage": 9,
    "ore_generation": 10,
    "ore_processing": 11,
    "renewability_and_you": 12,
    "multiblock_dilemma": 13,
    "heating_coils": 14,
    "progression": 15,
    "tips_and_tricks_2": 16,
}

# 缺失模组物品 → 本包现有替代品
REPLACEMENTS = {
    "hangglider:hang_glider": "paraglider:paraglider",
    "travelanchors:travel_anchor": "waystones:waystone",
    "travelanchors:travel_staff": "waystones:warp_stone",
    "storagedrawers:quantify_key": "functionalstorage:configuration_tool",
    "craftingstation:crafting_station": "crafting_on_a_stick:crafting_table",
    "expatternprovider:tag_storage_bus": "ae2:storage_bus",
    "expatternprovider:ex_interface": "ae2:interface",
    "expatternprovider:pattern_modifier": "ae2:blank_pattern",
    "expatternprovider:wireless_connect": "ae2:wireless_access_point",
    "expatternprovider:fishbig": "minecraft:cookie",
    "mae2:pattern_p2p_tunnel": "ae2:me_p2p_tunnel",
    "mae2:eu_p2p_tunnel": "ae2:me_p2p_tunnel",
    "mae2:4x_crafting_accelerator": "ae2:crafting_accelerator",
    "mae2:16x_crafting_accelerator": "ae2:crafting_accelerator",
    "mae2:64x_crafting_accelerator": "ae2:crafting_accelerator",
    "mae2:256x_crafting_accelerator": "ae2:crafting_accelerator",
    "ae2wtlib:quantum_bridge_card": "ae2:wireless_receiver",
    "javd:portal_block": "minecraft:ender_pearl",
}

STR_RE = r'"((?:[^"\\]|\\.)*)"'


def unescape(s):
    return s.replace('\\"', '"').replace("\\\\", "\\")


def split_blocks(text):
    """按 quests 数组切分：header（含 quest_links）、任务块列表、footer（章节标题/副标题）。
    注意：quest_links 的条目也用 2 tab 的 { } 包着，不能按 2 tab 花括号切块，
    必须先定位到 `quests: [` 这一行，只切 quests 数组里的块。"""
    lines = text.split("\n")
    qi = None
    for i, ln in enumerate(lines):
        if ln.rstrip() == "\tquests: [":
            qi = i
            break
    if qi is None:
        # 没有（或为空的 `quests: [ ]`）任务数组：整体视为 header，不切块
        return text, [], ""
    header = "\n".join(lines[:qi + 1])  # 含 `quests: [` 行
    rest = lines[qi + 1:]
    blocks, footer, cur = [], [], None
    for ln in rest:
        if ln == "\t\t{" and cur is None:
            cur = [ln]
        elif ln == "\t\t}" and cur is not None:
            cur.append(ln)
            blocks.append("\n".join(cur))
            cur = None
        elif cur is not None:
            cur.append(ln)
        else:
            footer.append(ln)
    if cur is not None:  # 容错
        blocks.append("\n".join(cur))
    return header, blocks, "\n".join(footer)


def transform_quest_block(block, filename, en_out):
    """任务块内：description / title / subtitle / task & reward title -> 语言键。"""
    m = re.search(r'^\t\t\tid: "([0-9A-Fa-f]{16})"$', block, re.M)
    if not m:
        return block
    qid = m.group(1)

    lines = block.split("\n")
    out = []
    i = 0
    context = None
    last_id = {}

    while i < len(lines):
        ln = lines[i]

        # 上下文
        if re.match(r"^\t\t\ttasks:", ln):
            context = "task"
        elif re.match(r"^\t\t\trewards:", ln):
            context = "reward"

        # 描述数组（可能在 id 之前）
        if re.match(r"^\t\t\tdescription: \[$", ln):
            out.append(ln)
            i += 1
            n = 0
            while i < len(lines) and not re.match(r"^\t\t\t\]$", lines[i]):
                dm = re.match(r"^(\t{4,})" + STR_RE + r"$", lines[i])
                if dm and dm.group(2):
                    n += 1
                    key = f"ftbquests.chapter.{filename}.quest{qid}.description{n}"
                    en_out[key] = unescape(dm.group(2))
                    out.append(f'{dm.group(1)}"{{{key}}}"')
                else:
                    out.append(lines[i])
                i += 1
            out.append(lines[i])
            i += 1
            continue

        # 任务标题/副标题（3 tab）
        m = re.match(r"^\t\t\t(title|subtitle): " + STR_RE + r"$", ln)
        if m:
            key = f"ftbquests.chapter.{filename}.quest{qid}.{m.group(1)}"
            en_out[key] = unescape(m.group(2))
            out.append(f'\t\t\t{m.group(1)}: "{{{key}}}"')
            i += 1
            continue

        # 深层 ID
        m = re.match(r'^(\t{4,})id: "([0-9A-Fa-f]{16})"$', ln)
        if m:
            last_id[len(m.group(1))] = m.group(2)
            out.append(ln)
            i += 1
            continue

        # 任务/奖励标题（4 tab+）
        m = re.match(r"^(\t{4,})title: " + STR_RE + r"$", ln)
        if m and len(m.group(1)) in last_id and context:
            tid = last_id[len(m.group(1))]
            key = f"ftbquests.chapter.{filename}.quest{qid}.{context}.{tid}.title"
            en_out[key] = unescape(m.group(2))
            out.append(f'{m.group(1)}title: "{{{key}}}"')
            i += 1
            continue

        out.append(ln)
        i += 1

    return "\n".join(out)


def transform_chapter(text, filename, en_out):
    # 章节标题（1 tab，全文件唯一；任务标题在 3 tab+，不会误匹配）
    def chap_title(m):
        key = f"ftbquests.chapter.{filename}.title"
        en_out[key] = unescape(m.group(1))
        return f'\ttitle: "{{{key}}}"'

    text = re.sub(r'^\ttitle: "((?:[^"\\]|\\.)*)"$', chap_title, text, count=1, flags=re.M)

    # 章节副标题（单行数组）
    def chap_sub_line(m):
        key = f"ftbquests.chapter.{filename}.subtitle0"
        en_out[key] = unescape(m.group(1))
        return f'\tsubtitle: ["{{{key}}}"]'

    text = re.sub(r'^\tsubtitle: \["((?:[^"\\]|\\.)*)"\]$', chap_sub_line, text, count=1, flags=re.M)

    # 章节副标题（多行数组）
    def chap_sub_multi(m):
        inner = m.group(1)
        n = 0
        outl = []
        for ln in inner.split("\n"):
            dm = re.match(r'^(\t\t)' + STR_RE + r"$", ln)
            if dm and dm.group(2):
                key = f"ftbquests.chapter.{filename}.subtitle{n}"
                en_out[key] = unescape(dm.group(2))
                outl.append(f'{dm.group(1)}"{{{key}}}"')
                n += 1
            else:
                outl.append(ln)
        return "\tsubtitle: [\n" + "\n".join(outl) + "\n\t]"

    text = re.sub(r'^\tsubtitle: \[\n(.*?)\n\t\]$', chap_sub_multi, text, count=1, flags=re.M | re.S)

    # 分组与顺序（1 tab）
    text = re.sub(r'^\tgroup: "[^"]*"$', f'\tgroup: "{GROUP_ID}"', text, count=1, flags=re.M)
    text = re.sub(r"^\torder_index: -?\d+$", f"\torder_index: {CHAPTER_ORDER[filename]}", text, count=1, flags=re.M)

    # 切分并转换任务块（quest_links 保留在 header）
    header, blocks, footer = split_blocks(text)
    blocks = [transform_quest_block(b, filename, en_out) for b in blocks]

    return header + "\n" + "\n".join(blocks) + "\n" + footer


def dedupe_or_entries(text):
    """移除 itemfilters:or 中重复的 { Count: 1b / id: "..." } 条目（保留首个）。"""
    pat = re.compile(r'\n(\t+)\{\n\t+Count: 1b\n\t+id: "([^"]+)"\n\t+\}')
    seen = set()

    def repl(m):
        key = m.group(2)
        if key in seen:
            return ""
        seen.add(key)
        return m.group(0)

    return pat.sub(repl, text)


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_SRC
    src_chapters = os.path.join(src, "chapters")
    src_tables = os.path.join(src, "reward_tables")

    if not os.path.isdir(src_chapters):
        raise SystemExit(f"源任务书目录不存在: {src_chapters}")

    os.makedirs(WORK_DIR, exist_ok=True)
    en_out = {}
    report = []

    # ---- 1) 章节搬运 ----
    for fn in sorted(os.listdir(src_chapters)):
        if not fn.endswith(".snbt"):
            continue
        stem = fn[:-5]
        if stem not in CHAPTER_ORDER:
            continue
        text = open(os.path.join(src_chapters, fn), encoding="utf-8").read()

        replaced = 0
        for old, new in REPLACEMENTS.items():
            cnt = text.count(f'"{old}"')
            if cnt:
                text = text.replace(f'"{old}"', f'"{new}"')
                replaced += cnt
        text = dedupe_or_entries(text)
        text = transform_chapter(text, stem, en_out)

        with open(os.path.join(DST_CHAPTERS, fn), "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
        report.append((fn, replaced))

    # ---- 2) 奖励表搬运 ----
    table_count = 0
    if os.path.isdir(src_tables):
        for fn in sorted(os.listdir(src_tables)):
            if fn.endswith(".snbt"):
                shutil.copyfile(os.path.join(src_tables, fn), os.path.join(DST_TABLES, fn))
                table_count += 1

    # ---- 3) 新增分组（解析现有分组后整体重写，幂等） ----
    groups_path = os.path.join(DST_QUESTS, "chapter_groups.snbt")
    gtext = open(groups_path, encoding="utf-8").read()
    entries = re.findall(r'\{\s*id:\s*"([0-9A-Fa-f]{16})"\s*,\s*title:\s*"([^"]+)"\s*\}', gtext)
    entries = [e for e in entries if e[0] != GROUP_ID]
    decimal = int(GROUP_ID, 16)
    entries.append((GROUP_ID, f"{{ftbquests.chapter_groups.{decimal}.title}}"))
    body = "\n".join(f'\t\t{{ id: "{i}", title: "{t}" }}' for i, t in entries)
    new_gtext = "{\n\tchapter_groups: [\n" + body + "\n\t]\n}\n"
    with open(groups_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(new_gtext)

    # ---- 4) 输出英文条目与翻译队列 ----
    with open(os.path.join(WORK_DIR, "en_entries.json"), "w", encoding="utf-8") as f:
        json.dump(en_out, f, ensure_ascii=False, indent=1)

    queue = {}
    for key, text in en_out.items():
        if text and text != "{@pagebreak}":
            queue.setdefault(text, []).append(key)
    with open(os.path.join(WORK_DIR, "translate_queue.json"), "w", encoding="utf-8") as f:
        json.dump(queue, f, ensure_ascii=False, indent=1)

    with open(os.path.join(WORK_DIR, "group_title.json"), "w", encoding="utf-8") as f:
        json.dump({"zh": GROUP_TITLE[0], "en": GROUP_TITLE[1]}, f, ensure_ascii=False)

    print(f"chapters: {len(report)} -> {DST_CHAPTERS}")
    for fn, r in report:
        print(f"   {fn:32s} replacements={r}")
    print(f"reward tables: {table_count} -> {DST_TABLES}")
    print(f"en entries: {len(en_out)}")
    print(f"unique strings to translate: {len(queue)}")
    print(f"work dir: {WORK_DIR}")


if __name__ == "__main__":
    main()
