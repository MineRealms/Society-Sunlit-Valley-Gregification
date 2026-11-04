#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the aspect-bridge FTB Quests chapter (TC4 x magic mods x GT).

Follows build_ae2_addons_chapter.py: stable business key -> persisted 16-hex ID map,
deterministic render, fail-closed validation. Text is inline Chinese.

Chapter hangs in the magic group (04716B2F19F75F08, thaumcraft=1 / botania=5 /
twilightforest=6), takes order 30. External deps: thaumcraft intro quest +
the trade chapter's deposit-bin essentia/mana quests.

Every icon/item below was extracted from the pack's own mod jars on 2026-11-03:
  thaumcraft        thaumcraft-forge-4.2.3.5-...-20748.jar   (chapter icon reuse)
  botania           Botania-1.20.1-454-FORGE.jar             assets/botania/models/item
  twilightforest    twilightforest-1.20.1-4.3.2508-universal.jar  models/item
  me                Middle-earth-1.4.2-1.20.1-port.0.jar     assets/me/models/item
  gtceu             gtceu-1.20.1-7.5.3.jar                   lang en_us.json keys
  sunlitmarket      live-verified in build_trade_chapter.py
"""
from pathlib import Path
import argparse
import hashlib
import json
import re

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parents[2]
QUESTS = ROOT / 'config/ftbquests/quests'
OUTPUT = QUESTS / 'chapters/aspect_bridge.snbt'
MAP = TOOLS / 'aspect_bridge_ids.json'
GROUP = '04716B2F19F75F08'
SALT = 'society-aspect-bridge-chapter-v1'
ORDER = 30

EXT_TC_INTRO = '35F501BCCBED6EC4'       # thaumcraft chapter: first quest
EXT_BIN_ESSENTIA = '7160EA5E15705A84'   # trade: 接受仓源质通道
EXT_BIN_MANA = '4040D45BF06D0973'       # trade: 接受仓魔力通道
EXT_DEPS = {EXT_TC_INTRO, EXT_BIN_ESSENTIA, EXT_BIN_MANA}

VERIFIED_ITEMS = {
    'thaumcraft:thaumonomicon', 'thaumcraft:crucible',
    'botania:manasteel_ingot', 'botania:livingrock',
    'twilightforest:torchberries', 'twilightforest:ironwood_ingot',
    'me:athelas', 'me:mithril_ingot', 'me:gold_coin',
    'gtceu:talc_dust', 'gtceu:wood_dust', 'gtceu:lv_macerator',
    'sunlitmarket:deposit_bin',
}

Q = [
    dict(key='intro', title='要素桥：让神秘侧认识魔法材料', icon='thaumcraft:thaumonomicon',
         desc=['本包把各魔法模组的关键材料都登记进了神秘的要素表（object_aspects 数据桥）：',
               '植物魔法、暮色森林、中洲的材料现在都能被 &6扫视仪&r 识别出要素。',
               '这意味着：神秘炼金、注魔、研究任务的"材料要素"从此覆盖全部魔法产线。',
               '例：植物魔力锭 = 金属 2 + 草药 2 + 能量 1；中洲秘银 = 金属 3 + 财富 2 + 光 1。',
               '数据文件：kubejs/data/thaumcraft/object_aspects/pack_bridge_aspects.json（可自行增补）。'],
         check='已了解要素桥的存在', deps=[], ext=[EXT_TC_INTRO], xy=(0, 0)),

    dict(key='scan_botania', title='扫视：植物魔法', icon='botania:manasteel_ingot',
         desc=['拿起魔力锭 / 泰拉钢 / 元素锭扫一遍，看要素构成。',
               '泰拉钢 = 金属+草药+能量×3；元素锭带虚无 2（精灵侧材料）；魔力珍珠 = 水+能量+玻璃。',
               '活石=大地、活木=树木——它们是后面 GT 研磨桥的原料。'],
         items=['botania:manasteel_ingot'], deps=['intro'], xy=(2, 0)),

    dict(key='scan_tf', title='扫视：暮色森林', icon='twilightforest:torchberries',
         desc=['暮色的材料各有性格：铁木锭 = 金属+树木（铁与活的树杂交）。',
               '炽热锭 = 火×3+金属；炽热之血带生命；纪元粉 = 转换×3（复制/反制的核心要素）。',
               '战利品也是要素源：巫妖/九头蛇/娜迦奖杯各带专属要素组合。'],
         items=['twilightforest:torchberries'], deps=['intro'], xy=(4, 0)),

    dict(key='scan_me', title='扫视：中洲', icon='me:athelas',
         desc=['中洲冶金全部入表：秘银（金属+财富+光）、魔古尔钢（黑暗×3+死亡）、',
               '奥克钢（武器+野兽）、卡扎德钢（金属×3+大地，矮人钢）。',
               '药材&0王室苜蓿&r = 康复×3+草药——注魔回复药水的优质材料。',
               '三种硬币也带财富要素：把中洲硬币扫出来看，本身就是学要素的教材。'],
         items=['me:athelas'], deps=['intro'], xy=(6, 0)),

    dict(key='gt_pre', title='GT 研磨桥：魔法材料的物理预处理', icon='gtceu:lv_macerator',
         desc=['GT 只做物理处理，魔法核心循环不被绕过（详见 JEI）：',
               '活石 → 滑石粉（纯华蓑菊可再生，GT 化学用）；活木 → 木浆 ×2；',
               '星辉大理石 → 滑石粉 ×2；星辉金属锭回收 → 铁粉 ×1（净亏，防刷铁）。',
               '滑石/木浆都是 GT 中期的消耗品，纯华蓑菊农场可以稳定供货。'],
         items=['gtceu:talc_dust', 'gtceu:wood_dust'], deps=['scan_botania'], xy=(8, 0)),

    dict(key='sell_magic', title='魔法变现闭环', icon='sunlitmarket:deposit_bin',
         desc=['要素桥的终点是经济：接受仓的源质/魔力通道直接吃神秘与植物魔法的产出',
               '（源质按要素分三档 4/2/1 点 = 1 spur；魔力 2000 点 = 1 spur）。',
               '结合当铺柜台与中洲商人，魔法产线可以稳定换钱——见「贸易」章节。'],
         check='已把魔法产出卖进接受仓',
         deps=['gt_pre'], ext=[EXT_BIN_ESSENTIA, EXT_BIN_MANA], xy=(10, 0)),


]
def digest(data):
    return hashlib.sha256(data).hexdigest()

def valid_id(value):
    return isinstance(value, str) and re.fullmatch(r'[0-9A-F]{16}', value) is not None \
        and 0 < int(value, 16) <= 0x7FFFFFFFFFFFFFFF

def stable_id(key, reserved):
    salt = 0
    while True:
        suffix = f':{salt}' if salt else ''
        value = int.from_bytes(hashlib.sha256(f'{SALT}:{key}{suffix}'.encode('utf-8')).digest()[:8], 'big') & 0x7FFFFFFFFFFFFFFF
        candidate = f'{value:016X}'
        if value and candidate not in reserved:
            return candidate
        salt += 1

def get_keys():
    keys = ['chapter']
    for q in Q:
        keys.append('quest/' + q['key'])
        keys.extend('task/' + q['key'] + '/item/' + i for i in q.get('items', ()))
        if q.get('check'):
            keys.append('task/' + q['key'] + '/check')
    return keys

def external_ids():
    result = {GROUP}
    pattern = re.compile(r'\bid:\s*"([0-9A-F]{16})"')
    for path in sorted(QUESTS.rglob('*.snbt')):
        if path == OUTPUT:
            continue
        result.update(pattern.findall(path.read_text(encoding='utf-8-sig')))
    return result

def allocate(keys, external):
    if MAP.exists():
        doc = json.loads(MAP.read_text(encoding='utf-8'))
        if doc.get('schema') != 1 or doc.get('salt') != SALT or doc.get('group') != GROUP:
            raise ValueError('ID map owner/schema mismatch')
        ids = dict(doc['ids'])
    else:
        ids = {}
    if len(ids.values()) != len(set(ids.values())):
        raise ValueError('Duplicate ID in persisted map')
    reserved = set(external) | set(ids.values())
    for key in sorted(keys):
        if key not in ids:
            ids[key] = stable_id(key, reserved)
            reserved.add(ids[key])
    for key, value in ids.items():
        if not valid_id(value):
            raise ValueError('Invalid persisted ID: ' + key)
    return ids

def dump(value, depth=0):
    tab = '\t' * depth
    if isinstance(value, dict):
        return '{\n' + ',\n'.join(tab + '\t' + key + ': ' + dump(child, depth + 1) for key, child in value.items()) + '\n' + tab + '}'
    if isinstance(value, list):
        return '[\n' + ',\n'.join(tab + '\t' + dump(child, depth + 1) for child in value) + '\n' + tab + ']' if value else '[ ]'
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False)
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, float):
        return f'{value:.1f}d'
    return str(value)

def build(ids):
    doc = dict(default_hide_dependency_lines=False, default_quest_shape='square', filename='aspect_bridge',
               group=GROUP, icon='thaumcraft:thaumonomicon', id=ids['chapter'], order_index=ORDER,
               quest_links=[], quests=[], title='&5&l魔法&r - 要素桥')
    keys = {q['key'] for q in Q}
    for q in Q:
        for dep in q['deps']:
            if dep not in keys:
                raise ValueError('Unknown dependency %s for %s' % (dep, q['key']))
        tasks = [dict(id=ids['task/' + q['key'] + '/item/' + item], type='item', item=item, count=1,
                      consume_items=False, match_nbt=False, only_from_crafting=False) for item in q.get('items', ())]
        if q.get('check'):
            tasks.append(dict(id=ids['task/' + q['key'] + '/check'], title=q['check'], type='checkmark'))
        if not tasks:
            raise ValueError('Quest must have at least one objective: ' + q['key'])
        deps = [ids['quest/' + d] for d in q['deps']] + list(q.get('ext', ()))
        doc['quests'].append(dict(description=q['desc'], dependencies=deps,
                                  icon=q['icon'], id=ids['quest/' + q['key']], tasks=tasks,
                                  title=q['title'], x=float(q['xy'][0]), y=float(q['xy'][1])))
    return doc

def validate(doc, external):
    definitions = [doc['id']]
    refs = set()
    for q in doc['quests']:
        definitions.append(q['id'])
        refs.update(q['dependencies'])
        for task in q['tasks']:
            definitions.append(task['id'])
    if len(definitions) != len(set(definitions)) or not all(valid_id(i) for i in definitions):
        raise ValueError('Invalid or duplicate definition ID')
    if set(definitions) & external:
        raise ValueError('Global FTBQ ID collision')
    qids = {q['id'] for q in doc['quests']}
    dangling = (refs - qids) - EXT_DEPS
    if dangling:
        raise ValueError('Dangling quest dependency: ' + repr(sorted(dangling)))
    missing_ext = {d for q in doc['quests'] for d in q['dependencies'] if d in EXT_DEPS and d not in external}
    if missing_ext:
        raise ValueError('External dependency not found in any chapter: ' + repr(sorted(missing_ext)))
    graph = {q['id']: q['dependencies'] for q in doc['quests']}
    active, done = set(), set()

    def visit(n):
        if n in active:
            raise ValueError('Quest dependency cycle at ' + n)
        if n in done:
            return
        active.add(n)
        for d in graph[n]:
            if d in graph:
                visit(d)
        active.remove(n)
        done.add(n)

    for n in graph:
        visit(n)
    coords = [(q['x'], q['y']) for q in doc['quests']]
    if len(coords) != len(set(coords)):
        raise ValueError('Duplicate quest coordinates')
    for q in Q:
        for item in [q['icon']] + list(q.get('items', ())):
            if item not in VERIFIED_ITEMS:
                raise ValueError('Item not in the verified registry list: ' + item)
    return (dump(doc) + '\n').encode('utf-8')

def render():
    ids = allocate(get_keys(), external_ids())
    group_doc = (QUESTS / 'chapter_groups.snbt').read_text(encoding='utf-8-sig')
    if GROUP not in re.findall(r'id:\s*"([0-9A-F]{16})"', group_doc):
        raise ValueError('Aspect bridge chapter group missing from chapter_groups.snbt')
    doc = build(ids)
    payload = validate(doc, external_ids())
    map_doc = dict(schema=1, salt=SALT, group=GROUP, order_index=ORDER,
                   ids=dict(sorted(ids.items())), output_sha256=digest(payload))
    map_bytes = (json.dumps(map_doc, ensure_ascii=False, indent=2, sort_keys=True) + '\n').encode('utf-8')
    return payload, map_bytes

def check_stable():
    payload, _ = render()
    if OUTPUT.exists() and OUTPUT.read_bytes() != payload:
        raise SystemExit('aspect_bridge.snbt exists but differs from the deterministic render')

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true', help='fail if the output would change')
    ap.add_argument('--verify-repeat', action='store_true', help='render twice, require byte-identical output')
    args = ap.parse_args()
    if args.check:
        check_stable()
    if args.verify_repeat:
        first = render()
        second = render()
        if first != second:
            raise SystemExit('render is not deterministic')
        print('render is deterministic, chapter id %s, %d quests' % (json.loads(second[1])['ids']['chapter'], len(Q)))
    payload, map_bytes = render()
    OUTPUT.write_bytes(payload)
    MAP.write_bytes(map_bytes)
    print('wrote %s (%d bytes, %d quests) and %s' % (OUTPUT.name, len(payload), len(Q), MAP.name))
