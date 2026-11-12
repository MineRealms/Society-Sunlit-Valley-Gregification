#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the Tinkers' Construct tutorial chapter.

Same contract as build_trade_chapter.py: stable business key -> persisted
16-hex ID map, deterministic render, fail-closed validation.
Every icon/item is checked against the shipped TConstruct jar before render.
新增章节，不改动任何既有章节文件。
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import zipfile

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parents[2]
QUESTS = ROOT / 'config/ftbquests/quests'
OUTPUT = QUESTS / 'chapters/tinkers.snbt'
MAP = TOOLS / 'tinkers_ids.json'
JAR = ROOT / 'mods/TConstruct-1.20.1-3.12.0.220.jar'

GROUP = '4A46A5E1358A80A6'
SALT = 'society-tinkers-chapter-v1'
ORDER = 31
THEME_UNLOCKS = {'advanced': 'theme.tinkers.adept'}

Q = [
    dict(key='intro', title='匠魂入门：为什么用它', icon='tconstruct:tinkers_anvil',
         desc=['原版工具一次成型、坏了重做；匠魂把工具拆成部件：镐头、手柄、绑定结各自选材料，属性相加，坏了只换部件。',
               '它还有一套强化系统：石英加伤害、红石加速度、青金石加时运、钻石加耐久，强化数量受工具种类限制。',
               '本章只讲前中期怎么从零做出一把能用的工具和一座冶炼炉。高阶材料与强化另开章节。'],
         check='已了解匠魂和原版工具的区别', deps=[], xy=(0, 0)),

    dict(key='pattern', title='图案与合成站', icon='tconstruct:pattern',
         desc=['先做空白图案：一个木板 + 一个木棍，做出 2 个图案。',
               '把图案放进合成站（8 个木板围一圈），选择你要做的部件形状，得到对应的木质模具，这叫图案。',
               '图案只决定形状，不决定材料。同一张镐头图案，可以浇铜、浇铁，也可以浇玛玉灵。'],
         items=['tconstruct:pattern'], deps=['intro'], xy=(2, 0)),

    dict(key='station', title='工具装配站', icon='tconstruct:tinker_station',
         desc=['工具装配站是组装工具的地方：4 个木板 + 2 个原木 + 1 个铁锭。',
               '把部件按槽位放进去：镐 = 镐头 + 手柄 + 绑定结，每换一个部件的材料，成品属性就变一次。',
               '装配站还能修补工具、替换单个部件，不用整把重做。'],
         items=['tconstruct:tinker_station'], deps=['pattern'], xy=(4, 0)),

    dict(key='first_tool', title='第一把镐', icon='tconstruct:pickaxe',
         desc=['石头镐头 + 木手柄 + 木绑定结，是最便宜的一套。石头的挖掘等级够挖铁，木头给速度和耐久。',
               '做完先别急着升级——把工具拿在手里按 Shift 看属性面板，你会看到挖掘速度 / 耐久 / 挖掘等级三个值分别由哪个部件贡献。',
               '这一步的意义：以后想换材料，只要换一个部件，不用重新做整把。'],
         check='已装配出第一把匠魂工具', deps=['station'], xy=(6, 0)),

    dict(key='smeltery', title='冶炼炉：焦黑砖与控制器', icon='tconstruct:smeltery_controller',
         desc=['冶炼炉是匠魂的心脏，用焦黑砖搭：先烧砂砾得焦黑砖，再围成 3x3 底座。',
               '结构：一层焦黑砖做底，四周砌墙，正面放冶炼炉控制器，任意一面放排液口，上面接焦黑储罐存熔融金属。',
               '控制器右键打开界面，左边是熔炼槽，右边显示储罐里的液体。至少 3x3x3 才能开始熔炼。'],
         items=['tconstruct:smeltery_controller'], deps=['intro'], xy=(0, 3)),

    dict(key='casting', title='铸造：铸模与铸造台', icon='tconstruct:seared_table',
         desc=['铸造台（浇小件，如锭、部件）和铸造盆（浇大块，如方块）要用焦黑砖做。',
               '第一次浇铸需要铸模：金铸模最耐用（blank_cast 打底再浇金），沙铸模一次性（红沙或普通沙）。',
               '流程：把图案放进铸造台，浇一次金得到金铸模，以后直接浇金属成型，不用再消耗图案。'],
         items=['tconstruct:seared_table'], deps=['smeltery'], xy=(2, 3)),

    dict(key='metal', title='第一块匠魂金属：钴', icon='tconstruct:cobalt_ingot',
         desc=['钴矿石只在下界生成，挖回来直接丢进冶炼炉熔成熔融钴。',
               '钴的特点是挖掘速度快，但耐久一般，适合做镐头，不适合做手柄。',
               '浇铸时注意：熔融金属要够量。一个镐头需要 1 锭的量（144 mB），不够会卡在铸造台里。'],
         items=['tconstruct:cobalt_ingot'], deps=['casting', 'first_tool'], xy=(4, 3)),

    dict(key='anvil', title='匠魂砧与强化', icon='tconstruct:tinkers_anvil',
         desc=['匠魂砧是强化工作台：2 个焦黑砖 + 1 个铁块。比装配站多一个强化槽。',
               '把工具放进去，再加强化材料：石英（+伤害）、红石（+速度）、青金石（+时运）、钻石（+耐久）、下界合金（+等级）。',
               '每种工具能装的强化数量有限，界面右下角会显示已用与上限。超了就得先用强化工作台扩容。'],
         items=['tconstruct:tinkers_anvil'], deps=['metal'], xy=(6, 3)),

    dict(key='mend', title='修补：让工具活得久', icon='tconstruct:slimesteel_ingot',
         desc=['匠魂工具不会凭空消失，耐久归零只是损坏（变红、不能挖）。',
               '修补两种方式：一是在装配站里放同材料部件；二是在冶炼炉里浇同种熔融金属。',
               '粘液钢（slimesteel）自带自修复特性，适合做长期用的手柄。'],
         check='已修补过一次工具', deps=['anvil'], xy=(8, 3)),

    dict(key='quartz', title='石英强化：直接加伤害', icon='minecraft:quartz',
         desc=['下界石英是最容易拿到的强化材料：一个石英 = +0.5 伤害，可以叠。',
               '近战武器优先堆石英，尤其是劈刀、长剑这类高基础伤害的。',
               '注意：石英只加攻击伤害，不加挖掘速度。挖矿工具堆石英没用。'],
         items=['minecraft:quartz'], deps=['anvil'], xy=(4, 6)),

    dict(key='redstone', title='红石强化：直接加速度', icon='minecraft:redstone',
         desc=['红石强化加挖掘速度，每个 +0.1，堆满能到原版的 3 倍以上。',
               '镐、铲、斧这类采集工具优先堆红石；武器不用。',
               '速度和耐久是跷跷板：堆太多红石会占掉强化槽，导致装不下钻石（耐久）。'],
         items=['minecraft:redstone'], deps=['mend'], xy=(6, 6)),

    dict(key='slime', title='粘液：匠魂的另一种材料', icon='tconstruct:sky_slime_ball',
         desc=['三种粘液各有用途：天蓝粘液（天空岛）、末影粘液（末地）、血粘液（下界）。',
               '粘液能做粘液工具（自带弹性、摔不死）、粘液靴（弹跳）、粘液史莱姆（会走的存储）。',
               '粘液木还能做手柄，给工具加弹性特性——用坏了会弹一下，不容易断。'],
         items=['tconstruct:sky_slime_ball'], deps=['smeltery'], xy=(2, 6)),

    dict(key='advanced', title='高阶材料：玛玉灵', icon='tconstruct:manyullyn_ingot',
         desc=['玛玉灵 = 钴 + 下界合金，是匠魂的中期天花板：高伤害、高耐久。',
               '冶炼炉里按比例熔：4 钴 + 1 下界合金 得到 1 玛玉灵。合金要在冶炼炉控制器的合金页里配比。',
               '再往上是女皇史莱姆（末影粘液 + 岩浆）和灵魂钢（灵魂沙 + 铁），属于后期内容。'],
         items=['tconstruct:manyullyn_ingot'], deps=['anvil'], xy=(8, 6)),
]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def valid_id(value):
    return bool(re.fullmatch(r'[0-7][0-9A-F]{15}', value))


def stable_id(key, reserved):
    salt = 0
    while True:
        suffix = ':%d' % salt if salt else ''
        value = int.from_bytes(hashlib.sha256(('%s:%s%s' % (SALT, key, suffix)).encode('utf-8')).digest()[:8], 'big') & 0x7FFFFFFFFFFFFFFF
        candidate = '%016X' % value
        if value and candidate not in reserved:
            return candidate
        salt += 1


def get_keys():
    keys = ['chapter']
    for q in Q:
        keys.append('quest/' + q['key'])
        for item in q.get('items', ()):
            keys.append('task/%s/item/%s' % (q['key'], item))
        if q.get('check'):
            keys.append('task/%s/check' % q['key'])
        if q['key'] in THEME_UNLOCKS:
            keys.append('reward/%s/unlock/%s' % (q['key'], THEME_UNLOCKS[q['key']]))
    return keys


def installed_items():
    if not JAR.is_file():
        raise SystemExit('missing jar: %s' % JAR)
    z = zipfile.ZipFile(JAR)
    mine = {n.split('/')[-1][:-5] for n in z.namelist()
            if n.startswith('assets/tconstruct/models/item/') and n.endswith('.json')}
    blocks = {n.split('/')[-1][:-5] for n in z.namelist()
              if n.startswith('assets/tconstruct/blockstates/') and n.endswith('.json')}
    return mine | blocks


def verify_items(ids):
    have = installed_items()
    for item in sorted(ids):
        ns, name = item.split(':', 1)
        if ns != 'tconstruct':
            continue
        if name not in have:
            raise SystemExit('item not shipped by TConstruct: %s' % item)


def load_map():
    if MAP.is_file():
        return json.loads(MAP.read_text(encoding='utf-8'))
    return {'salt': SALT, 'ids': {}}


def allocate():
    doc = load_map()
    if doc.get('salt') != SALT:
        raise SystemExit('ID map owner mismatch')
    ids = dict(doc['ids'])
    reserved = set(ids.values())
    for key in get_keys():
        if key in ids:
            if not valid_id(ids[key]):
                raise SystemExit('bad persisted id for %s' % key)
            continue
        new = stable_id(key, reserved)
        ids[key] = new
        reserved.add(new)
    return ids


def dump(value, depth=0):
    tab = '\t' * depth
    if isinstance(value, dict):
        return '{\n' + ',\n'.join(tab + '\t' + k + ': ' + dump(v, depth + 1) for k, v in value.items()) + '\n' + tab + '}'
    if isinstance(value, list):
        if not value:
            return '[ ]'
        return '[\n' + ',\n'.join(tab + '\t' + dump(v, depth + 1) for v in value) + '\n' + tab + ']'
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False)
    if isinstance(value, bool):
        return 'true' if value else 'false'
    if isinstance(value, float):
        return '%.1fd' % value
    return str(value)


def build(ids):
    doc = dict(default_hide_dependency_lines=False, default_quest_shape='', filename='tinkers',
               group=GROUP, icon='tconstruct:smeltery_controller', id=ids['chapter'],
               order_index=ORDER, quest_links=[], quests=[],
               title='&b&l匠魂&r · 部件与强化')
    keys = {q['key'] for q in Q}
    for q in Q:
        for dep in q['deps']:
            if dep not in keys:
                raise SystemExit('unknown dependency %s for %s' % (dep, q['key']))
        tasks = [dict(id=ids['task/%s/item/%s' % (q['key'], item)], type='item', item=item,
                      count=1, consume_items=False, match_nbt=False, only_from_crafting=False)
                 for item in q.get('items', ())]
        if q.get('check'):
            tasks.append(dict(id=ids['task/%s/check' % q['key']], title=q['check'], type='checkmark'))
        if not tasks:
            raise SystemExit('quest needs an objective: ' + q['key'])
        node = dict(description=list(q['desc']), dependencies=[ids['quest/' + d] for d in q['deps']],
                                  icon=q['icon'], id=ids['quest/' + q['key']], tasks=tasks,
                                  title=q['title'], x=float(q['xy'][0]), y=float(q['xy'][1]))
        if q['key'] in THEME_UNLOCKS:
            unlock = THEME_UNLOCKS[q['key']]
            node['description'].append('完成后解锁匠魂主题商人的高阶材料报价；声望和每日库存限制仍然生效。')
            node['rewards'] = [dict(id=ids['reward/%s/unlock/%s' % (q['key'], unlock)],
                                    type='command', command='execute as {p} run sunlitmarket unlock ' + unlock,
                                    title='解锁匠魂高阶材料贸易', elevate_perms=True, silent=True,
                                    team_reward=False, auto='no_toast')]
        doc['quests'].append(node)
    return doc


def validate(doc):
    ids = [doc['id']]
    for quest in doc['quests']:
        ids.append(quest['id'])
        ids.extend(target['id'] for target in quest['tasks'])
        ids.extend(reward['id'] for reward in quest.get('rewards', ()))
    if len(ids) != len(set(ids)) or not all(valid_id(value) for value in ids):
        raise SystemExit('invalid or duplicate ids inside chapter')
    for q in doc['quests']:
        if not q['tasks']:
            raise SystemExit('quest without task: ' + q['title'])
        for t in q['tasks']:
            if t['type'] == 'item' and not t.get('item'):
                raise SystemExit('item task without item: ' + q['title'])
        for other in q['dependencies']:
            if other == q['id']:
                raise SystemExit('self dependency: ' + q['title'])
    coords = [(q['x'], q['y']) for q in doc['quests']]
    if len(coords) != len(set(coords)):
        raise SystemExit('duplicate quest coordinates')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()

    items = {q['icon'] for q in Q}
    for q in Q:
        items.update(q.get('items', ()))
    verify_items(items)

    ids = allocate()
    doc = build(ids)
    validate(doc)
    payload = (dump(doc) + '\n').encode('utf-8')

    if args.check:
        if not OUTPUT.is_file():
            raise SystemExit('output missing: %s' % OUTPUT)
        if OUTPUT.read_bytes() != payload:
            raise SystemExit('output differs; rerun without --check')
        print(json.dumps({'check': 'ok', 'quests': len(Q), 'sha256': digest(payload)}))
        return

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_bytes(payload)
    MAP.write_text(json.dumps({'salt': SALT, 'ids': dict(sorted(ids.items()))}, indent=2, ensure_ascii=False) + '\n',
                   encoding='utf-8')
    print(json.dumps({'written': 'chapters/tinkers.snbt', 'quests': len(Q), 'sha256': digest(payload)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
