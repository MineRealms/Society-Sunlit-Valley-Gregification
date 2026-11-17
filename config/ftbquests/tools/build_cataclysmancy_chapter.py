"""Deterministic FTBQ chapter: Cataclysm Studies (Thaumcraft x L_Enders Cataclysm).

Standalone generator: reuses the validation/ID/serialization components of
industrial_quest_support.py but supplies its own GROUP (the "linkage" group)
and chapter-level ``images`` support, so the two Tian Gong chapters are untouched.

Run:
    python build_cataclysmancy_chapter.py                 # render
    python build_cataclysmancy_chapter.py --check        # read-only verify
    python build_cataclysmancy_chapter.py --check --verify-repeat
"""
import argparse
import hashlib
import json
from pathlib import Path

import nbtlib

import industrial_quest_support as S
from build_astral_sorcery_chapter import SnbtParser
from industrial_quest_support import quest as q, dump, walk

TOOLS = Path(__file__).resolve().parent
LIBRARY = TOOLS.parent / "quests"
GROUP = "14AB86BD08B253EC"          # 支线-[联动]
TC_RESEARCH = "69C391B8091CE9CA"     # 神秘时代章：第一次研究（在魔导手册中解锁任意一项研究）
FILENAME = "cataclysmancy"
SALT = "society-cataclysmancy-v1"
ORDER = 21

# 章节背景插画：1672x941 ≈ 16:9，与 space 章同规格定位
IMAGES = [
    dict(height=14.4, image="society:textures/quests/cataclysm/cataclysm_temple.png",
         rotation=0.0, width=25.6, x=9.0, y=0.0),
]

Q = [
    q("root", "观测虚渊", "cataclysm:void_core", (0, 0),
      ["灾变遗迹并非死石。它们的核心、眼球与锭块里回荡着扭曲的原初要素。",
       "用魔导透镜扫描任意灾变掉落，开启《灾变学》研究类别。研究台里的六项研究对应本章各节。",
       "本章只做认知与收容指引，不改动灾变 Boss 与祭坛的原有掉落和召唤条件。"],
      items=["cataclysm:void_core"], ext=[TC_RESEARCH],
      check="已用魔导透镜扫描过灾变掉落并在魔导手册中看到《灾变学》分类"),

    q("eyes", "裂隙之眼", "cataclysm:void_eye", (4, 0),
      ["虚空、深渊、烈焰、机械、巨兽与诅咒之眼，区别只在于哪一项要素占主导。",
       "《灾变学·裂隙之眼》研究记录了各眼的要素构成。每类留一枚样本，余下的才是坩埚燃料。"],
      deps=["root"], items=["cataclysm:void_eye", "cataclysm:abyss_eye", "cataclysm:flame_eye"],
      check="已记录至少三类眼睛的扫描结果"),

    q("materials", "四系残骸", "cataclysm:ancient_metal_ingot", (4, -5),
      ["焚天锭、凋灵锭、远古金属与诅锭是四条独立的材料链，不要混用。",
       "要素表里它们分别以 ignis / mortuus / machina / vitium 为主导，蒸馏前先分好类。"],
      deps=["root"], items=["cataclysm:ignitium_ingot", "cataclysm:witherite_ingot",
                            "cataclysm:ancient_metal_ingot", "cataclysm:cursium_ingot"],
      check="已分别存放四系材料"),

    q("contain", "缚锁与残渣", "cataclysm:chain_of_soul_binding", (8, 0),
      ["缚魂锁链的 vinculum 足够在坩埚工作时镇住样本，而它的 vitium 总要在别处付账。",
       "《灾变学·缚锁与残渣》研究说明：收容从不是免费的，接触虚空材料本身就会积累扭曲。"],
      deps=["eyes"], items=["cataclysm:chain_of_soul_binding", "cataclysm:remnant_skull"],
      check="已在工作台旁备好净化盐、便携浴符与干净法袍"),

    q("crucible", "蒸馏残骸", "thaumcraft:alumentum", (8, -5),
      ["焚天锭的热量足以抵上一整份炼金煤；虚空碎片加一点 ordo 就能析出平衡碎片。",
       "两条坩埚配方见《灾变学·蒸馏残骸》研究页。坩埚不在乎这份燃料曾属于某个庞然大物。"],
      deps=["materials"], items=["thaumcraft:alumentum", "thaumcraft:balanced_shard"],
      check="已实际完成至少一条灾变材料坩埚配方"),

    q("warp", "窥视之价", "thaumcraft:void_ingot", (12, 0),
      ["虚空核心与诅咒之眼在 alienis 之外还带着 vitium。蒸馏效率高，残渣却黏在观测者身上。",
       "《灾变学·窥视之价》会给予永久扭曲。把《扭曲理论》章的纯净泪水、净化护身符、便携浴符当作装置的一部分。",
       "这项研究有扭曲代价，进本条之前先确认净化链已经建好。"],
      deps=["contain"], items=["cataclysm:void_core", "cataclysm:cursed_eye"],
      check="已验证净化道具可用并了解永久扭曲的后果"),

    q("lens", "虚空透镜", "thaumcraft:goggles_of_revealing", (12, -5),
      ["虚空之眼置于注魔祭坛中央，环以魔导透镜、远古金属与平衡碎片。",
       "成品是一副揭示之护目镜，注魔配方见《灾变学·虚空透镜》研究页。成品寻常，路径不寻常。"],
      deps=["crucible"], items=["thaumcraft:goggles_of_revealing"],
      check="已完成虚空之眼注魔并核对 instability 与源质消耗"),

    q("altars", "四座祭坛", "cataclysm:altar_of_void", (16, 0),
      ["虚空、烈焰、深渊、紫水晶四座祭坛仍按灾变原有方式召唤，本章不修改它们的钥匙与掉落。",
       "要素表给四座祭坛都挂了 alienis/ignis/aqua/vitreus 主导的高值要素，扫描它们可以补足研究要素。"],
      deps=["warp"], items=["cataclysm:altar_of_void", "cataclysm:altar_of_fire",
                            "cataclysm:altar_of_abyss", "cataclysm:altar_of_amethyst"],
      check="已确认四座祭坛的召唤条件未被本章改动"),

    q("bosses", "渊薮之主", "cataclysm:abyssal_egg", (16, -5),
      ["利维坦、先驱、末影守卫与伊格尼斯各有独立掉落。把它们当作研究材料，而不只是装备来源。",
       "渊卵、潮汐之爪、守卫护手与残骸头骨都已在要素表里登记，扫描后可直接进研究台。"],
      deps=["lens"], items=["cataclysm:abyssal_egg", "cataclysm:tidal_claws", "cataclysm:gauntlet_of_guard"],
      check="已扫描至少一件 Boss 掉落并核对要素"),

    q("mastery", "灾变学大成", "cataclysm:void_core", (20, -2.5),
      ["观测、理解、收容、反制——四个动词走完一遍，灾变的力量才算被真正读懂。",
       "本章与《秽玄天工》《GT 核工业》并列，不设立跨章硬锁；任务勾选只记录操作检查。",
       "收容是持续状态，不是一次性成就。长期接触虚空材料请保持净化与扭曲监测。"],
      deps=["altars", "bosses"], items=["cataclysm:void_core"],
      check="已通读六项灾变学研究并完成本章全部操作检查"),
]


def allocate(spec):
    """Same deterministic ID scheme as the shared library, own registry."""
    path = TOOLS / (FILENAME + "_ids.json")
    old = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    if old and (old.get("schema") != 1 or old.get("salt") != SALT or old.get("group") != GROUP):
        raise ValueError("ID registry owner/schema changed")
    keys = {"chapter"}
    for item in spec["quests"]:
        keys.add("quest/" + item["key"])
        keys.update("task/" + item["key"] + "/item/" + i for i in item["items"])
        if item["check"]:
            keys.add("task/" + item["key"] + "/check")
    ids = {k: v for k, v in old.get("ids", {}).items() if k in keys}
    retired = dict(old.get("retired_ids", {}))
    retired.update({k: v for k, v in old.get("ids", {}).items() if k not in keys})
    external, _ = S.library(LIBRARY / "chapters" / (FILENAME + ".snbt"))
    reserved = set(external) | set(ids.values()) | set(retired.values())
    for key in sorted(keys - ids.keys()):
        attempt = 0
        while True:
            suffix = f":{attempt}" if attempt else ""
            value = int.from_bytes(hashlib.sha256(f"{SALT}:{key}{suffix}".encode()).digest()[:8], "big") & 0x7FFFFFFFFFFFFFFF
            candidate = f"{value:016X}"
            if value and candidate not in reserved:
                ids[key] = candidate
                reserved.add(candidate)
                break
            attempt += 1
    if not all(S.valid_id(v) for v in [*ids.values(), *retired.values()]):
        raise ValueError("Invalid registry ID")
    if len(ids) != len(set(ids.values())):
        raise ValueError("Repeated active registry ID")
    return ids, retired


def build(spec, ids):
    doc = dict(default_hide_dependency_lines=False, default_quest_shape="square",
               filename=FILENAME, group=GROUP, icon=spec["icon"],
               id=ids["chapter"], order_index=ORDER, quest_links=[],
               quests=[], title=spec["title"], images=IMAGES)
    keys = {i["key"] for i in spec["quests"]}
    if len(keys) != len(spec["quests"]):
        raise ValueError("Repeated quest key")
    for item in spec["quests"]:
        if set(item["deps"]) - keys:
            raise ValueError("Unknown prerequisite for " + item["key"])
        tasks = [dict(id=ids["task/" + item["key"] + "/item/" + i], type="item", item=i,
                      count=1, consume_items=False, match_nbt=False, only_from_crafting=False)
                 for i in item["items"]]
        if item["check"]:
            tasks.append(dict(id=ids["task/" + item["key"] + "/check"], title=item["check"], type="checkmark"))
        if not tasks:
            raise ValueError("Missing objective for " + item["key"])
        doc["quests"].append(dict(description=item["desc"],
            dependencies=[ids["quest/" + k] for k in item["deps"]] + item["ext"],
            icon=item["icon"], id=ids["quest/" + item["key"]], tasks=tasks,
            title=item["title"], x=float(item["xy"][0]), y=float(item["xy"][1])))
    return doc


def validate(doc, minimum_spacing=2.5):
    definitions = [obj["id"] for obj in walk(doc) if "id" in obj]
    if len(definitions) != len(set(definitions)) or not all(S.valid_id(v) for v in definitions):
        raise ValueError("Invalid or repeated chapter/quest/objective ID")
    external, external_quests = S.library(LIBRARY / "chapters" / (FILENAME + ".snbt"))
    collision = set(definitions) & external.keys()
    if collision:
        raise ValueError("Global ID collision: " + repr({k: external[k] for k in collision}))
    graph = {x["id"]: x for x in doc["quests"]}
    missing = {d for x in graph.values() for d in x["dependencies"]} - graph.keys() - external_quests
    if missing:
        raise ValueError("Missing quest prerequisite: " + repr(sorted(missing)))
    groups = SnbtParser((LIBRARY / "chapter_groups.snbt").read_text(encoding="utf-8-sig")).parse()
    if not any(g["id"] == GROUP for g in groups.get("chapter_groups", ())):
        raise ValueError("Linkage chapter group missing")
    import math
    positions = list(graph.values())
    minimum = min(math.dist((a["x"], a["y"]), (b["x"], b["y"]))
                  for i, a in enumerate(positions) for b in positions[i + 1:])
    if minimum < minimum_spacing:
        raise ValueError("Quest positions overlap: %.2f" % minimum)
    for x in positions:
        if not all(math.isfinite(x[k]) for k in ("x", "y")):
            raise ValueError("Nonfinite quest position")
        for dep in x["dependencies"]:
            if dep not in graph:
                continue
            start = graph[dep]
            if start["x"] >= x["x"]:
                raise ValueError("Local prerequisite must point right: " + x["title"])
            dx, dy = x["x"] - start["x"], x["y"] - start["y"]
            for other in positions:
                if other["id"] in (dep, x["id"]):
                    continue
                t = ((other["x"] - start["x"]) * dx + (other["y"] - start["y"]) * dy) / (dx * dx + dy * dy)
                if 0 < t < 1 and math.dist((other["x"], other["y"]), (start["x"] + t * dx, start["y"] + t * dy)) < 0.65:
                    raise ValueError("Prerequisite crosses node: " + x["title"] + " from " + start["title"])
    return minimum, len(definitions)


def render(spec):
    ids, retired = allocate(spec)
    doc = build(spec, ids)
    minimum, count = validate(doc)
    payload = (dump(doc) + "\n").encode("utf-8")
    text = payload.decode("utf-8")
    parsed = SnbtParser(text).parse()
    independent = nbtlib.parse_nbt(text).unpack()
    if parsed != doc or independent != S.nbt_normalize(doc):
        raise ValueError("Independent SNBT parse mismatch: local=" + str(parsed == doc) +
                         " nbtlib=" + str(independent == S.nbt_normalize(doc)))
    registry = dict(schema=1, salt=SALT, group=GROUP, order_index=ORDER,
                    ids=dict(sorted(ids.items())), output_sha256=hashlib.sha256(payload).hexdigest())
    if retired:
        registry["retired_ids"] = dict(sorted(retired.items()))
    map_bytes = (json.dumps(registry, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    return payload, map_bytes, minimum, count


SPEC = dict(icon="cataclysm:void_core",
            title="&5&l灾变学&r：观测、收容与虚空的代价", quests=Q)


def run(spec):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--verify-repeat", action="store_true")
    args = parser.parse_args()
    output = LIBRARY / "chapters" / (FILENAME + ".snbt")
    registry = TOOLS / (FILENAME + "_ids.json")
    result = render(spec)
    if args.verify_repeat:
        if result != render(spec):
            raise ValueError("Nondeterministic render")
        print("Independent repeat render: identical")
    payload, map_bytes, minimum, count = result
    if args.check:
        for path, expected in ((output, payload), (registry, map_bytes)):
            if not path.exists() or path.read_bytes() != expected:
                raise SystemExit(path.name + " differs from deterministic render")
        print("Read-only check passed")
    else:
        output.write_bytes(payload)
        registry.write_bytes(map_bytes)
    print(f"{FILENAME}: {len(spec['quests'])} quests, {count} IDs; min spacing {minimum:.1f}; all local edges point right; no node crossings")


if __name__ == "__main__":
    run(SPEC)
