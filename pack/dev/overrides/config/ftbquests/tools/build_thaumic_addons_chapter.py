#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Thaumcraft 扩展（Warptheory / NodalMechanics / Isorropia）FTBQ chapter.

Run --check for read-only validation; run without arguments to publish.
Only thaumic_addons.snbt and thaumic_addons_ids.json are generated.
Mirrors build_technomancy_chapter.py. Group: 神秘科技支线 (4A46A5E1358A80A6).
"""
from pathlib import Path
import argparse
import hashlib
import itertools
import json
import math
import re
import subprocess
import sys
import zipfile

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parents[2]
QUESTS = ROOT / 'config/ftbquests/quests'
OUTPUT = QUESTS / 'chapters/thaumic_addons.snbt'
MAP = TOOLS / 'thaumic_addons_ids.json'
GROUP = '4A46A5E1358A80A6'
SALT = 'thaumicaddons'
JARS = {
    'warptheory': Path(r'H:\MinecraftMods\WarpTheory-Unofficial\versions\1.20.1-forge\build\devlibs\warptheory-1.20.1-forge-1.5.8-port.0.1.0.jar'),
    'nodalmechanics': Path(r'H:\MinecraftMods\NodalMechanics-Unofficial\build\distributions\nodalmechanics-1.20.1-forge-1.0.0-dev.jar'),
    'isorropia': Path(r'H:\MinecraftMods\Isorropia-1.20.1-wt\multiversion\versions\1.20.1-forge\build\devlibs\thaumic-horizons(Isorropia)-1.20.1-0.1.0-dev.jar'),
}


def digest(data):
    return hashlib.sha256(data).hexdigest()


class SnbtParser:
    token = re.compile(r'''\s+|\#[^\n]*|//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|[{}\[\]:,;]|[^\s{}\[\]:,;]+''')

    def __init__(self, text):
        text = text.lstrip('\ufeff')
        self.tokens = []
        end = 0
        for match in self.token.finditer(text):
            if match.start() != end:
                raise ValueError('Unrecognized SNBT token')
            end = match.end()
            t = match.group()
            if not t.isspace() and not t.startswith(('#', '//', '/*')):
                self.tokens.append(t)
        if end != len(text):
            raise ValueError('Unrecognized trailing SNBT token')
        self.i = 0

    def take(self):
        if self.i >= len(self.tokens):
            raise ValueError('Unexpected SNBT EOF')
        t = self.tokens[self.i]
        self.i += 1
        return t

    def peek(self):
        return self.tokens[self.i] if self.i < len(self.tokens) else None

    def expect(self, t):
        actual = self.take()
        if actual != t:
            raise ValueError(f'Expected {t}, got {actual}')

    def value(self):
        t = self.take()
        if t == '{':
            result = {}
            while self.peek() != '}':
                key = self.take()
                if key.startswith(('"', "'")):
                    key = self.string(key)
                self.expect(':')
                if key in result:
                    raise ValueError(f'Duplicate SNBT key {key}')
                result[key] = self.value()
                if self.peek() == ',':
                    self.take()
            self.take()
            return result
        if t == '[':
            result = []
            if self.peek() in ('B', 'I', 'L') and self.tokens[self.i + 1:self.i + 2] == [';']:
                self.take()
                self.take()
            while self.peek() != ']':
                result.append(self.value())
                if self.peek() == ',':
                    self.take()
            self.take()
            return result
        if t.startswith(('"', "'")):
            return self.string(t)
        if t in ('true', 'false'):
            return t == 'true'
        if re.fullmatch(r'[-+]?\d+[bBsSlL]?', t):
            return int(t.rstrip('bBsSlL'))
        if re.fullmatch(r'[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?[fFdD]?', t):
            return float(t.rstrip('fFdD'))
        if t in ('}', ']', ':', ',', ';'):
            raise ValueError(f'Unexpected {t}')
        return t

    @staticmethod
    def string(t):
        return re.sub(r'\\(.)', lambda m: {'n': '\n', 'r': '\r', 't': '\t'}.get(m[1], m[1]), t[1:-1])

    def parse(self):
        result = self.value()
        if self.peek() is not None:
            raise ValueError('Trailing SNBT content')
        return result


def dump(value, level=0):
    tab = '\t' * level
    if isinstance(value, dict):
        return '{\n' + '\n'.join(tab + '\t' + k + ': ' + dump(v, level + 1) for k, v in value.items()) + '\n' + tab + '}'
    if isinstance(value, list):
        if not value:
            return '[ ]'
        return '[\n' + '\n'.join(tab + '\t' + dump(v, level + 1) for v in value) + '\n' + tab + ']'
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False)
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, float):
        return f'{value:.1f}d'
    return str(value)


Q = []


def quest(key, title, icon, text, items=(), check=None):
    Q.append(dict(key=key, title=title, icon=icon, description=text.split('\n'),
                  items=list(items), check=check))


def content():
    # ---- A · 扭曲理论 ----
    quest('wt_intro', 'A · 扭曲理论：认识扭曲与净化', 'warptheory:cleanser_minor',
          '扭曲理论（Warp Theory）是神秘时代的补充：它把「扭曲」从惩罚变成可研究、可治理的机制。\n本章六区：A/B 扭曲理论，C-F 神秘视界（Thaumic Horizons）。二者都建立在神秘时代研究之上，先完成基础研究再推进。\n任务连线表示教学顺序，不是完整配方树；具体配方、研究要求与数值以 JEI 与神秘表为准。',
          (), check='已阅读扭曲理论与本章导航')
    quest('wt_paper', '研究笔记：扭曲的记录', 'warptheory:paper',
          '扭曲理论引入记载扭曲研究的材料与笔记；先取得基础材料，再解锁净化类配方。\n按 JEI 查看其合成与研究前置。',
          ['warptheory:paper'], )
    quest('wt_something', '某种东西', 'warptheory:something',
          '「某种东西」是扭曲研究的中间产物，用于后续净化与实验。\n注意它可能带有副作用，先在小范围试用。',
          ['warptheory:something'], )
    quest('wt_cleanser_minor', '小净化剂：处理临时扭曲', 'warptheory:cleanser_minor',
          '小净化剂用于处理临时/轻度扭曲。使用前先查看它清除的扭曲类型与代价。\n扭曲分永久/黏性/临时三类，小净化剂未必作用于永久扭曲。',
          ['warptheory:cleanser_minor'], )
    quest('wt_cleanser', '净化剂：更彻底的净化', 'warptheory:cleanser',
          '净化剂比小净化剂更强，用于更严重的扭曲。\n配方与研究门槛更高，材料准备周期更长。',
          ['warptheory:cleanser'], )
    quest('wt_amulet', '净化护符', 'warptheory:amulet',
          '净化护符在佩戴时提供扭曲相关的防护/净化效果。\n与其他饰品共用 curios 槽位，注意冲突。',
          ['warptheory:amulet'], )
    quest('wt_ward_amulet', '扭曲护符：长期防护', 'warptheory:warp_ward_amulet',
          '扭曲护符用于长期抵抗扭曲积累，适合常年探索神秘遗迹的玩家。\n它是 A 区的收尾，之后进入 B 区的高阶净化与节点机械。',
          ['warptheory:warp_ward_amulet'], )

    # ---- B · 扭曲理论进阶 + 节点机械 ----
    quest('wt_oblivion', '遗忘药水：重置扭曲', 'warptheory:oblivion_potion',
          '遗忘药水用于重置/清除扭曲（具体范围以 JEI 与实测为准）。\n属高价手段，谨慎使用。',
          ['warptheory:oblivion_potion'], )
    quest('nm_intro', 'B · 节点机械：给灵气节点充能', 'nodalmechanics:matrix',
          '节点机械（Nodal Mechanics）围绕「矩阵」工作，用于给神秘时代的灵气节点重新充能/调整。\n节点一旦被耗尽会变得无用，节点机械提供了一条「回收—再造」的路径。\n先备好矩阵，再研究调谐与充能配方。',
          (), check='已阅读节点机械说明')
    quest('nm_matrix', '矩阵', 'nodalmechanics:matrix',
          '矩阵是节点机械的核心物品，用于承载并转运灵气。\n按 JEI 查看其合成与用法。',
          ['nodalmechanics:matrix'], )
    quest('nm_unattuned', '未调谐矩阵', 'nodalmechanics:matrix',
          '未调谐矩阵是尚未绑定目标的中间态。\n先把节点/目标就位，再考虑调谐。',
          (), check='理解未调谐矩阵的用途')
    quest('nm_attuned', '已调谐矩阵', 'nodalmechanics:matrix',
          '已调谐矩阵绑定到目标节点，用于充能/迁移灵气。\n调谐后通常不可逆，操作前先确认目标。',
          (), check='理解已调谐矩阵的用途')
    quest('wt_vanish', '扭曲理论·隐匿', 'warptheory:warp_ward_amulet',
          '扭曲理论还提供与「隐匿」相关的机制，用于规避神秘遗迹中的危险探测。\n具体效果与触发条件以实测与 JEI 为准。',
          (), check='已了解隐匿相关机制')
    quest('wt_complete', '扭曲治理完成', 'warptheory:cleanser',
          '至此你已掌握扭曲理论的主要净化与防护手段，并接入了节点机械。\n接下来进入神秘视界（C-F 区），内容量最大的一条支线。',
          (), check='完成扭曲理论与节点机械入门')

    # ---- C · 神秘视界：核心机器 ----
    quest('iso_intro', 'C · 神秘视界：核心机器', 'isorropia:recombinator',
          '神秘视界（Isorropia / Thaumic Horizons）是神秘时代的重型扩展，引入大量机器、材料与生物改造。\n本区先认识核心机器：重组器、血肉灌注器、节点监控器、转导放大器与两类发电机。\n它们多为注魔/奥术路线，研究门槛高，先推进神秘时代主线再动手。',
          (), check='已阅读神秘视界核心机器导航')
    quest('iso_recombinator', '重组器', 'isorropia:recombinator',
          '重组器是神秘视界的核心加工机器之一，用于重组/转化材料（具体配方见 JEI）。\n先按结构/研究要求成型，再接入原料与能量。',
          ['isorropia:recombinator'], )
    quest('iso_blood_infuser', '血肉灌注器', 'isorropia:blood_infuser',
          '血肉灌注器用于处理「血肉」等生物材料，是生物改造线的起点。\n注意它涉及高风险材料，单独分区摆放。',
          ['isorropia:blood_infuser'], )
    quest('iso_node_monitor', '节点监控器', 'isorropia:node_monitor',
          '节点监控器用于观测灵气节点/网络的状态，是调试节点工程与能量线的实用方块。\n与神秘科技的节点机器配合使用。',
          ['isorropia:node_monitor'], )
    quest('iso_transduction', '转导放大器', 'isorropia:transduction_amplifier',
          '转导放大器用于增益/放大灵气相关的处理过程。\n按 JEI 查看其配方与安装方式。',
          ['isorropia:transduction_amplifier'], )
    quest('iso_vis_dynamo', '灵气发电机', 'isorropia:vis_dynamo',
          '灵气发电机把灵气（vis）转成能量，是神秘视界的供能端之一。\n与源质发电机配合可稳定供电。',
          ['isorropia:vis_dynamo'], )
    quest('iso_essentia_dynamo', '源质发电机', 'isorropia:essentia_dynamo',
          '源质发电机把源质转成能量。\n注意：神秘科技（Technomancy）也有同名概念，二者是不同的机器，按 JEI 区分。',
          ['isorropia:essentia_dynamo'], )

    # ---- D · 神秘视界：工具与材料 ----
    quest('iso_alchemite', '炼金岩', 'isorropia:alchemite',
          '炼金岩是神秘视界的基础材料，用于多种配方与结构。\n先备一批再谈机器扩产。',
          ['isorropia:alchemite'], )
    quest('iso_dust', '神秘粉尘', 'isorropia:dust',
          '神秘粉尘是通用加工材料，参与多种反应与合成。\n按 JEI 查看来源与用途。',
          ['isorropia:dust'], )
    quest('iso_flesh', '血肉', 'isorropia:flesh',
          '血肉是生物改造线的原料，来自灌注/培养流程。\n单独储存，避免污染其它仓库。',
          ['isorropia:flesh'], )
    quest('iso_shard', '以太碎片', 'isorropia:ethereal_shard',
          '以太碎片是灵性/灵魂线的材料，用于灵魂信标等高级内容。\n获取门槛较高。',
          ['isorropia:ethereal_shard'], )
    quest('iso_putty', '虚空腻子', 'isorropia:void_putty',
          '虚空腻子用于修复/塑形特定结构或物品（以 JEI 为准）。\n是虚空材料的应用之一。',
          ['isorropia:void_putty'], )
    quest('iso_golem_powder', '傀儡粉末', 'isorropia:golem_powder',
          '傀儡粉末用于与神秘时代傀儡相关的改造/强化。\n配合傀儡工程使用。',
          ['isorropia:golem_powder'], )
    quest('iso_crystal_wand', '水晶法杖', 'isorropia:crystal_wand',
          '水晶法杖是神秘视界的施法工具，用于消耗灵气执行特定操作。\n与焦点配合使用。',
          ['isorropia:crystal_wand'], )

    # ---- E · 神秘视界：焦点与透镜 ----
    quest('iso_focus_intro', 'E · 焦点与透镜：施法与观测', 'isorropia:focus_animation',
          '神秘视界扩展了法杖焦点（Focus）与透镜（Lens）体系。\n焦点决定法杖右键/蓄力的行为，透镜用于观察与增幅；二者都可深度定制。\n按 JEI 查看每种焦点的配方与研究前置。',
          (), check='已阅读焦点与透镜导航')
    quest('iso_focus_animation', '动画焦点', 'isorropia:focus_animation',
          '动画焦点用于临时活化物体（具体效果以 JEI/实测为准）。\n先做基础焦点再解锁分支。',
          ['isorropia:focus_animation'], )
    quest('iso_focus_containment', '遏制焦点', 'isorropia:focus_containment',
          '遏制焦点用于限制/收容目标，适合处理危险的活化方块或实体。',
          ['isorropia:focus_containment'], )
    quest('iso_focus_disintegration', '分解焦点', 'isorropia:focus_disintegration',
          '分解焦点用于将目标分解为基础物质。\n高风险高回报，注意误伤与掉落。',
          ['isorropia:focus_disintegration'], )
    quest('iso_focus_illumination', '照明焦点', 'isorropia:focus_illumination',
          '照明焦点是实用的辅助焦点，提供多种色温/形态的光源（有多个变体）。\n日常探索必备。',
          ['isorropia:focus_illumination'], )
    quest('iso_focus_liquefaction', '液化焦点', 'isorropia:focus_liquefaction',
          '液化焦点把目标转化为流体形态，接入神秘视界的流体处理线。',
          ['isorropia:focus_liquefaction'], )
    quest('iso_lens', '透镜（气/火/嫉妒/秩序）', 'isorropia:lens',
          '透镜用于对灵气/源质流进行观测与增幅，不同透镜对应不同方面。\n集齐基础透镜即可深入神秘视界的高级内容。',
          ['isorropia:lens', 'isorropia:lens_air', 'isorropia:lens_fire', 'isorropia:lens_envy', 'isorropia:lens_ordo'], )

    # ---- F · 神秘视界：灵魂与传送 ----
    quest('iso_jar_soul', '灵魂罐', 'isorropia:jar_soul',
          '灵魂罐用于封存灵魂，是灵魂线的基础容器。\n注意区分已封装（jarred）与空罐状态。',
          ['isorropia:jar_soul'], )
    quest('iso_corpse_effigy', '尸骸雕像', 'isorropia:corpse_effigy',
          '尸骸雕像用于死亡/复活相关的机制，属于灵魂线的一环。\n使用前了解其代价。',
          ['isorropia:corpse_effigy'], )
    quest('iso_somatic_brain', '躯体脑', 'isorropia:somatic_brain',
          '躯体脑用于高阶生物改造/意识相关的配方。\n获取周期长，先小批量。',
          ['isorropia:somatic_brain'], )
    quest('iso_soul_beacon', '灵魂信标', 'isorropia:soul_beacon',
          '灵魂信标以灵魂为能源，提供范围效果（以 JEI/实测为准）。\n与灵魂罐配合使用。',
          ['isorropia:soul_beacon'], )
    quest('iso_gateway', '传送门框', 'isorropia:gateway',
          '传送门框是跨维度/远距离传送的结构件之一。\n先搭好框架，再接入端口。',
          ['isorropia:gateway'], )
    quest('iso_portal', '传送门', 'isorropia:portal',
          '传送门接通后即可用于快速移动/跨维度。\n确认坐标与安全性后再启用。',
          ['isorropia:portal'], )
    quest('iso_vortex', '漩涡与稳定器', 'isorropia:vortex',
          '漩涡与漩涡稳定器用于稳定/收束神秘视界的能量流。\n这是 F 区与整章的收尾，完成后神秘视界主要系统即已接入。',
          ['isorropia:vortex', 'isorropia:vortex_stabilizer'], )


def walk(obj):
    if isinstance(obj, dict):
        yield obj
        for v in obj.values():
            yield from walk(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from walk(v)


def load_library():
    return {str(f.relative_to(QUESTS)): SnbtParser(f.read_text(encoding='utf-8-sig')).parse()
            for f in sorted(QUESTS.rglob('*.snbt')) if f != OUTPUT}


def library_report(library):
    definitions, quests, issues = {}, {}, []
    for path, doc in library.items():
        for o in walk(doc):
            ident = o.get('id')
            if isinstance(ident, str) and ':' not in ident:
                if not re.fullmatch('[0-9A-F]{16}', ident) or not 0 < int(ident, 16) < 2**63:
                    issues.append(f'invalid ID {path}: {ident}')
                if ident in definitions:
                    issues.append(f'duplicate ID {ident}: {definitions[ident]}, {path}')
                definitions[ident] = path
        for q in doc.get('quests', []):
            quests[q['id']] = q
    for ident, q in quests.items():
        for dep in q.get('dependencies', []):
            if dep not in quests:
                issues.append(f'dangling dependency {ident} -> {dep}')
        for task in q.get('tasks', []):
            if not task.get('type'):
                issues.append(f'missing task type in {ident}')
    for path, doc in library.items():
        for link in doc.get('quest_links', []):
            if link.get('linked_quest') not in quests:
                issues.append(f'dangling linked_quest in {path}')
        if doc.get('group') and doc['group'] not in definitions:
            issues.append(f'dangling group in {path}')
        for obj in walk(doc):
            for field in ('reward_table', 'table_id'):
                ref = obj.get(field)
                if isinstance(ref, str) and re.fullmatch('[0-9A-F]{16}', ref) and ref not in definitions:
                    issues.append(f'dangling {field} {ref} in {path}')
    state = {}

    def visit(k):
        if state.get(k) == 1:
            raise ValueError(f'Cycle at quest {k}')
        if state.get(k) == 2:
            return
        state[k] = 1
        for dep in quests[k].get('dependencies', []):
            if dep in quests:
                visit(dep)
        state[k] = 2
    for k in quests:
        visit(k)
    return definitions, issues, len(quests)


def verify_items(ids):
    evidence = {}
    opened = {ns: zipfile.ZipFile(p) for ns, p in JARS.items()}
    try:
        for ident in sorted(ids):
            ns, name = ident.split(':', 1)
            if ns in opened:
                model = f'assets/{ns}/models/item/{name}.json'
                assert model in opened[ns].namelist(), f'Missing jar item model: {ident}'
                evidence[ident] = dict(jar=JARS[ns].name, model=model)
        # other namespaces (numismatics:cog) resolved against installed pack mods
        for ns in sorted({i.split(':')[0] for i in ids} - set(JARS)):
            wanted = {i.split(':')[1] for i in ids if i.startswith(ns + ':')}
            matches = []
            for f in sorted((ROOT / 'mods').glob('*.jar')):
                with zipfile.ZipFile(f) as jar:
                    names = set(jar.namelist())
                    if all(f'assets/{ns}/models/item/{n}.json' in names for n in wanted):
                        matches.append(f)
            assert len(matches) == 1, f'Ambiguous/missing jar for {ns}: {matches}'
            f = matches[0]
            for name in wanted:
                evidence[f'{ns}:{name}'] = dict(jar=f.name, sha256=digest(f.read_bytes()),
                                                model=f'assets/{ns}/models/item/{name}.json')
    finally:
        for z in opened.values():
            z.close()
    return evidence


def layout():
    # Six independent layered teaching DAGs (7 each). Fixed local pattern.
    local = [(2, 0), (0, 2), (4, 2), (0, 4), (4, 4), (0, 6), (4, 6)]
    parents = [None, 0, 0, 1, 2, 3, 4]
    edges = []
    assert len(Q) == 42, len(Q)
    for cluster in range(6):
        origin = ((cluster % 3) * 10, (cluster // 3) * 10)
        subset = Q[cluster * 7:cluster * 7 + 7]
        for i, q in enumerate(subset):
            q['x'], q['y'] = (float(origin[j] + local[i][j]) for j in (0, 1))
            q['deps'] = [] if parents[i] is None else [subset[parents[i]]['key']]
            if q['deps']:
                edges.append((q['deps'][0], q['key']))
    points = {q['key']: (q['x'], q['y']) for q in Q}

    def point_distance(p, a, b):
        dx, dy = b[0]-a[0], b[1]-a[1]
        t = max(0, min(1, ((p[0]-a[0])*dx + (p[1]-a[1])*dy)/(dx*dx+dy*dy)))
        return math.hypot(p[0]-a[0]-t*dx, p[1]-a[1]-t*dy)

    def cross(a, b, c):
        return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])

    for a, b in itertools.combinations(points, 2):
        assert math.dist(points[a], points[b]) >= 2, f'Overlapping nodes: {a}, {b}'
    for a, b in edges:
        assert math.dist(points[a], points[b]) <= math.sqrt(8) + 1e-9
        for k, pt in points.items():
            if k not in (a, b):
                assert point_distance(pt, points[a], points[b]) > .9 / math.sqrt(2), f'Edge hits {k}'
    for (a, b), (c, d) in itertools.combinations(edges, 2):
        if len({a, b, c, d}) < 4:
            continue
        aa, bb, cc, dd = (points[k] for k in (a, b, c, d))
        if max(min(aa[0], bb[0]), min(cc[0], dd[0])) <= min(max(aa[0], bb[0]), max(cc[0], dd[0])) and max(min(aa[1], bb[1]), min(cc[1], dd[1])) <= min(max(aa[1], bb[1]), max(cc[1], dd[1])):
            assert not (cross(aa, bb, cc)*cross(aa, bb, dd) <= 0 and cross(cc, dd, aa)*cross(cc, dd, bb) <= 0), 'Crossing dependency lines'
    return dict(clusters=6, edges=len(edges), center_bounds=[24, 16], icon_bounds=[24.9, 16.9],
                min_spacing=2, max_edge=round(math.sqrt(8), 6), crossings=0, overlaps=0, edge_node_hits=0)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--check', action='store_true', help='Validate without writing')
    ap.add_argument('--verify-repeat', action='store_true')
    args = ap.parse_args()
    if args.verify_repeat:
        snapshots = []
        for _ in range(2):
            subprocess.run([sys.executable, str(Path(__file__).resolve())], check=True, capture_output=True)
            snapshots.append((OUTPUT.read_bytes(), MAP.read_bytes()))
        assert snapshots[0] == snapshots[1], 'Two builds differ byte-for-byte'
        print(json.dumps(dict(repeat_equal=True, chapter_sha256=digest(snapshots[0][0]), mapping_sha256=digest(snapshots[0][1])), indent=2))
        return
    content()
    geometry = layout()
    library = load_library()
    used, legacy_issues, _ = library_report(library)
    assert GROUP in used
    prior = json.loads(MAP.read_text(encoding='utf-8')) if MAP.exists() else None
    if OUTPUT.exists():
        assert prior, 'Existing chapter without ID map; refusing overwrite'
        assert digest(OUTPUT.read_bytes()) == prior['chapter_sha256'], 'Chapter manually modified; refusing overwrite'
    elif prior:
        raise ValueError('ID map exists but chapter missing')
    order_values = [d.get('order_index', 0) for d in library.values() if d.get('group') == GROUP and 'quests' in d]
    order = prior['order_index'] if prior else max(order_values) + 1
    assert order not in order_values, f'order_index {order} occupied'
    ids = dict(prior['ids']) if prior else {}
    assert len(set(ids.values())) == len(ids)

    def sid(key):
        expected = f'{int.from_bytes(hashlib.sha256((SALT + ":ftbquests:v1:" + key).encode()).digest()[:8], "big") & 0x7FFFFFFFFFFFFFFF:016X}'
        assert int(expected, 16) > 0
        if key in ids:
            assert ids[key] == expected, f'Mapping changed: {key}'
        else:
            assert expected not in used and expected not in ids.values(), f'ID collision: {key}'
            ids[key] = expected
        return ids[key]

    chapter = dict(default_hide_dependency_lines=False, default_quest_shape='', filename='thaumic_addons',
                   group=GROUP, icon='isorropia:recombinator', id=sid('chapter'), order_index=order,
                   quest_links=[], quests=[], title='&5Thaumic Addons&r · 神秘时代扩展')
    all_items = {chapter['icon']}
    for q in Q:
        targets = [dict(id=sid('task/' + q['key'] + '/item/' + item), type='item', item=item, count=1,
                        consume_items=False, match_nbt=False, only_from_crafting=False)
                   for item in q['items']]
        if q['check']:
            targets.append(dict(id=sid('task/' + q['key'] + '/check'), type='checkmark', title=q['check']))
        assert targets, f'No tasks: {q["key"]}'
        assert len(q['items']) == len(set(q['items']))
        rewards = []
        if q['items']:
            rewards.append(dict(id=sid('reward/' + q['key'] + '/cog'), type='item', item='numismatics:cog', count=2))
            all_items.add('numismatics:cog')
        entry = dict(id=sid('quest/' + q['key']), title=q['title'], icon=q['icon'],
                     description=q['description'], dependencies=[sid('quest/' + k) for k in q['deps']],
                     tasks=targets, rewards=rewards, size=.9, x=q['x'], y=q['y'])
        chapter['quests'].append(entry)
        all_items.add(q['icon'])
        all_items.update(q['items'])
    for ns, p in JARS.items():
        assert p.is_file(), f'Jar missing: {p}'
    item_evidence = verify_items(all_items)
    comments = '# Generated by build_thaumic_addons_chapter.py; semantic IDs persisted in thaumic_addons_ids.json.\n'
    comments += ''.join('# ' + k + ' = ' + v + '\n' for k, v in sorted(ids.items()))
    encoded = (comments + dump(chapter) + '\n').encode('utf-8')
    parsed = SnbtParser(encoded.decode()).parse()
    assert parsed == chapter, 'Serialization changed structure'
    for spec, result in zip(Q, parsed['quests']):
        assert len(result['tasks']) == len(spec['items']) + bool(spec['check'])
        assert [t['item'] for t in result['tasks'] if t['type'] == 'item'] == spec['items']
    combined = {**library, 'chapters/thaumic_addons.snbt': parsed}
    all_ids, combined_issues, total = library_report(combined)
    assert combined_issues == legacy_issues, 'New library errors: ' + str(combined_issues)
    report = dict(quests=len(Q), objectives=sum(len(q['tasks']) for q in parsed['quests']),
                  rewards=sum(len(q['rewards']) for q in parsed['quests']), unique_items=len(all_items),
                  group=GROUP, order_index=order, layout=geometry, global_quests=total,
                  global_definitions=len(all_ids), baseline_issues=legacy_issues, chapter_sha256=digest(encoded))
    stable = {k: v for k, v in report.items() if k not in ('global_quests', 'global_definitions', 'baseline_issues')}
    manifest = dict(schema=2, salt=SALT, order_index=order, chapter_sha256=digest(encoded),
                    ids=dict(sorted(ids.items())), item_evidence=item_evidence, validation=stable)
    map_bytes = (json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + '\n').encode('utf-8')
    assert load_library() == library, 'Quest library changed; rerun'
    if not args.check:
        OUTPUT.write_bytes(encoded)
        MAP.write_bytes(map_bytes)
        assert OUTPUT.read_bytes() == encoded and MAP.read_bytes() == map_bytes
    elif prior:
        assert OUTPUT.read_bytes() == encoded, 'Generated content differs from published'
        assert MAP.read_bytes() == map_bytes, 'Evidence/map differs'
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
