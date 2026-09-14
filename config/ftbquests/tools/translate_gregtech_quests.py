# -*- coding: utf-8 -*-
"""
GT 任务书翻译脚本（英文 -> 中文），并写回 ftbquestlocalizer 语言文件。

用法（在整合包根目录执行）:
    python config/ftbquests/tools/translate_gregtech_quests.py [--limit N] [--no-lang]

流程:
    1. 读取 gt_port/translate_queue.json（去重后的英文文本）
    2. 用 GTCEu / 附属 / AE2 的官方 zh_cn 构建术语表，先做术语预替换
    3. 调用翻译接口（clients5.google.com），带缓存与重试，支持断点续传
    4. 生成 gt_port/zh_entries.json，并把 en/zh 条目写入
       kubejs/assets/ftbquestlocalizer/lang/{en_us,zh_cn}.json
"""

import argparse
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(TOOLS_DIR, "..", "..", ".."))
WORK_DIR = os.path.join(TOOLS_DIR, "gt_port")
LANG_DIR = os.path.join(ROOT, "kubejs", "assets", "ftbquestlocalizer", "lang")
MODS_DIR = os.path.join(ROOT, "mods")

QUEUE_PATH = os.path.join(WORK_DIR, "translate_queue.json")
EN_PATH = os.path.join(WORK_DIR, "en_entries.json")
CACHE_PATH = os.path.join(WORK_DIR, "translation_cache.json")
ZH_PATH = os.path.join(WORK_DIR, "zh_entries.json")
GROUP_PATH = os.path.join(WORK_DIR, "group_title.json")

# 术语表来源：模组 jar 的 zh_cn 语言文件
GLOSSARY_SOURCES = [
    ("gtceu-1.20.1-7.5.3.jar", "gtceu"),
    ("gtca-1.20.1-2.2.0.jar", "gtca"),
    ("gtmfo-0.0.6.jar", "gtmfo"),
    ("gtse-1.3.1.jar", "gtse"),
    ("gtmthings-1.6.0.jar", "gtmthings"),
    ("gtmutils-2.10.2.jar", "gtmutils"),
    ("gtnn-1.20.1-1.3.10.jar", "gtnn"),
    ("appliedenergistics2-forge-15.4.10.jar", "ae2"),
]

# 翻译后的通用修正（仅安全替换）
POST_FIX = [
    ("格雷格", "格雷"),
    ("汽轮机", "涡轮"),
    ("格雷技术", "格雷科技"),
    ("多块体", "多方块"),
    ("多块发电机", "多方块发电机"),
    ("多块生成器", "多方块发电机"),
    ("多块机械", "多方块机械"),
    ("多块结构", "多方块结构"),
    ("多块控制器", "多方块控制器"),
    ("多块部件", "多方块部件"),
    ("多方块生成器", "多方块发电机"),
]

# 手工补充术语（优先级高于自动术语表，长词优先）
MANUAL_TERMS = {
    "Multiblock": "多方块",
    "Multiblocks": "多方块",
    "Quest": "任务",
    "Energy Hatch": "能源仓",
    "Energy Hatches": "能源仓",
    "Dynamo Hatch": "动力仓",
    "Dynamo Hatches": "动力仓",
    "Input Bus": "输入总线",
    "Input Buses": "输入总线",
    "Output Bus": "输出总线",
    "Output Buses": "输出总线",
    "Input Hatch": "输入仓",
    "Input Hatches": "输入仓",
    "Output Hatch": "输出仓",
    "Output Hatches": "输出仓",
    "Maintenance Hatch": "维护仓",
    "Maintenance Hatches": "维护仓",
    "Muffler Hatch": "消声仓",
    "Muffler Hatches": "消声仓",
    "Machine Hull": "机器外壳",
    "Machine Hulls": "机器外壳",
    "Machine Casing": "机器外壳",
    "Machine Casings": "机器外壳",
    "Circuit Board": "电路板",
    "Circuit Boards": "电路板",
    "Heating Coil": "加热线圈",
    "Heating Coils": "加热线圈",
    "Ore Vein": "矿脉",
    "Ore Veins": "矿脉",
    "Surface Rock": "地表指示矿",
    "Surface Rocks": "地表指示矿",
    "Data Orb": "数据球",
    "Data Orbs": "数据球",
    "Data Module": "数据模块",
    "Data Modules": "数据模块",
    "Assembly Line": "装配线",
    "Cleanroom": "洁净室",
    "Maintenance": "维护",
    "Turbine Rotor": "涡轮转子",
    "Turbine Rotors": "涡轮转子",
    "Generator": "发电机",
    "Generators": "发电机",
    "Electric Blast Furnace": "电力高炉",
    "Large Chemical Reactor": "大型化学反应釜",
    "Distillation Tower": "蒸馏塔",
    "Pyrolyse Oven": "热解炉",
    "Implosion Compressor": "内爆压缩机",
    "Vacuum Freezer": "真空冷冻机",
    "Research Station": "研究站",
    "Fusion Reactor": "聚变反应堆",
    "Coke Oven": "焦炉",
    "Primitive Blast Furnace": "原始高炉",
    "Steam Grinder": "蒸汽研磨机",
    "Combustion Generator": "燃烧发电机",
    "Gas Turbine": "燃气涡轮",
    "Steam Turbine": "蒸汽涡轮",
}

CODE_RE = re.compile(r"&[0-9a-fk-or]")


def protect_codes(text):
    codes = []

    def repl(m):
        codes.append(m.group(0))
        return f"[[[c{len(codes) - 1}]]]"

    return CODE_RE.sub(repl, text), codes


def restore_codes(text, codes):
    for i, c in enumerate(codes):
        text = text.replace(f"[[[c{i}]]]", c)
    return text


def load_glossary():
    glossary = dict(MANUAL_TERMS)
    for jar, modid in GLOSSARY_SOURCES:
        path = os.path.join(MODS_DIR, jar)
        if not os.path.exists(path):
            print(f"  glossary skip (missing): {jar}")
            continue
        try:
            z = zipfile.ZipFile(path)
            en = json.loads(z.read(f"assets/{modid}/lang/en_us.json"))
            try:
                zh = json.loads(z.read(f"assets/{modid}/lang/zh_cn.json"))
            except KeyError:
                continue
            n = 0
            for k, v in en.items():
                if (k.startswith("block.") or k.startswith("item.") or k.startswith("material.")) and k in zh:
                    zt = zh[k]
                    if zt and zt != v and not zt.startswith("%") and v not in glossary:
                        glossary[v] = zt
                        n += 1
            print(f"  glossary {modid}: +{n} (total {len(glossary)})")
        except Exception as e:
            print(f"  glossary {jar} ERR: {e}")
    return glossary


def pre_sub(text, glossary_sorted):
    for en, zh in glossary_sorted:
        if en in text:
            text = re.sub(r"(?<![A-Za-z0-9])" + re.escape(en) + r"(?![A-Za-z0-9])", zh, text)
    return text


def translate(text, retries=4):
    q = urllib.parse.quote(text)
    url = f"https://clients5.google.com/translate_a/t?client=dict-chrome-ex&sl=en&tl=zh-CN&q={q}"
    last = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            data = urllib.request.urlopen(req, timeout=30).read().decode("utf-8")
            j = json.loads(data)
            if isinstance(j, list):
                return "".join(x if isinstance(x, str) else "".join(x) for x in j)
            return str(j)
        except Exception as e:
            last = e
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"translate failed: {last}")


def post_fix(text):
    for a, b in POST_FIX:
        text = text.replace(a, b)
    return text


def insert_lang(path, entries):
    """向 lang 文件原位插入条目（幂等，最小插入）。"""
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

    # 移除旧的移植章节键（可重复执行）
    prefixes = tuple(f"ftbquests.chapter.{p}." for p in PORTED_FILES) + (
        "ftbquests.chapter_groups.11469676895608327264.",)
    parsed = [(k, l) for (k, l) in parsed if not k.startswith(prefixes)]

    new_items = []
    for k in sorted(entries):
        v = json.dumps(entries[k], ensure_ascii=False)
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


PORTED_FILES = ['gtceu', 'steam_age', 'lv__low_voltage', 'mv__medium_voltage', 'hv__high_voltage',
                'ev__extreme_voltage', 'iv__insane_voltage', 'luv__ludicrous_voltage', 'zpm__zero_point_module',
                'uv__ultimate_voltage', 'ore_generation', 'ore_processing', 'renewability_and_you',
                'multiblock_dilemma', 'heating_coils', 'progression', 'tips_and_tricks_2']


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0, help="只翻译前 N 条（调试）")
    ap.add_argument("--batch", type=int, default=40, help="每请求合并的文本条数")
    ap.add_argument("--no-lang", action="store_true", help="只生成 zh_entries.json，不写 lang 文件")
    args = ap.parse_args()

    queue = json.load(open(QUEUE_PATH, encoding="utf-8"))
    en_entries = json.load(open(EN_PATH, encoding="utf-8"))
    cache = {}
    if os.path.exists(CACHE_PATH):
        cache = json.load(open(CACHE_PATH, encoding="utf-8"))
        print(f"cache loaded: {len(cache)}")

    print("building glossary...")
    glossary = load_glossary()
    glossary_sorted = sorted(glossary.items(), key=lambda kv: len(kv[0]), reverse=True)

    todo = [t for t in queue if t not in cache]
    if args.limit:
        todo = todo[: args.limit]
    print(f"queue: {len(queue)}  cached: {len(cache)}  todo: {len(todo)}")

    t0 = time.time()
    batch_size = args.batch
    try:
        i = 0
        while i < len(todo):
            batch = todo[i:i + batch_size]
            i += len(batch)
            # 逐条预处理（颜色码保护 + 术语预替换）
            prepped = []
            codes_list = []
            for src in batch:
                if not re.search(r"[A-Za-z]", src) or "@@@" in src:
                    prepped.append(None)
                    codes_list.append(None)
                    continue
                cp, codes = protect_codes(src)
                prepped.append(pre_sub(cp, glossary_sorted))
                codes_list.append(codes)

            # 批量翻译
            batch_texts = [p for p in prepped if p is not None]
            results = {}
            if batch_texts:
                joined = "\n@@@\n".join(batch_texts)
                try:
                    out = translate(joined, retries=3)
                    parts = out.split("@@@")
                    if len(parts) == len(batch_texts):
                        for src_text, zh in zip(batch_texts, parts):
                            results[src_text] = zh.strip()
                    else:
                        raise RuntimeError(f"batch split mismatch: {len(parts)} != {len(batch_texts)}")
                except Exception:
                    # 回退：逐条翻译
                    for src_text in batch_texts:
                        try:
                            results[src_text] = translate(src_text, retries=3)
                        except Exception as e:
                            print(f"  FAIL: {src_text[:50]!r} {e}")
                        time.sleep(0.25)

            for src, prep, codes in zip(batch, prepped, codes_list):
                if prep is None:
                    cache[src] = src
                elif prep in results:
                    cache[src] = restore_codes(post_fix(results[prep]), codes)

            with open(CACHE_PATH, "w", encoding="utf-8") as f:
                json.dump(cache, f, ensure_ascii=False, indent=1)
            rate = i / max(1e-6, time.time() - t0)
            left = (len(todo) - i) / max(1e-6, rate)
            print(f"  {i}/{len(todo)}  {rate:.1f}/s  eta {left/60:.1f} min")
            time.sleep(0.5)
    finally:
        with open(CACHE_PATH, "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False, indent=1)

    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=1)

    # 生成 zh entries
    zh_entries = {}
    missing = 0
    for key, src in en_entries.items():
        if src in cache:
            zh_entries[key] = cache[src]
        else:
            zh_entries[key] = src
            missing += 1
    with open(ZH_PATH, "w", encoding="utf-8") as f:
        json.dump(zh_entries, f, ensure_ascii=False, indent=1)
    print(f"zh entries: {len(zh_entries)}  untranslated fallback: {missing}")

    if not args.no_lang:
        group = json.load(open(GROUP_PATH, encoding="utf-8"))
        en_all = dict(en_entries)
        zh_all = dict(zh_entries)
        en_all["ftbquests.chapter_groups.11469676895608327264.title"] = group["en"]
        zh_all["ftbquests.chapter_groups.11469676895608327264.title"] = group["zh"]
        insert_lang(os.path.join(LANG_DIR, "zh_cn.json"), zh_all)
        insert_lang(os.path.join(LANG_DIR, "en_us.json"), en_all)
        print("lang files updated: zh_cn.json / en_us.json")


if __name__ == "__main__":
    main()
