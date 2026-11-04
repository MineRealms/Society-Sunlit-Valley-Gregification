#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the Middle-earth onboarding/agriculture FTB Quests chapter.

Default: write chapter + semantic ID map after validation.
--check: read-only exact comparison with published output and map.
--verify-repeat: render twice in memory and require byte-identical output.
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
OUTPUT = QUESTS / 'chapters/middle_earth.snbt'
MAP = TOOLS / 'middle_earth_ids.json'
GROUP = '5E4D3C2B1A090807'
SALT = 'society-middle-earth-onboarding-v1'
ME_JAR = ROOT / 'mods/Middle-earth-1.4.2-1.20.1-port.0.jar'
INITIAL_SHA256 = '0debe99f47e405340510a62e341983bd88c5033fbdf433eb080a56bcb6056e40'

# Preserve every already-published FTBQ identity. Never recycle retired IDs.
LEGACY_IDS = {
    'chapter': '6A1B2C3D4E5F0718',
    'quest/intro': '6A1B2C3D4E5F0721', 'task/intro/check': '6A1B2C3D4E5F0741',
    'quest/artisan': '6A1B2C3D4E5F0722', 'task/artisan/item/me:artisan_table': '6A1B2C3D4E5F0742',
    'quest/alloy': '6A1B2C3D4E5F0723', 'task/alloy/item/me:alloy_furnace': '6A1B2C3D4E5F0743',
    'quest/phial': '6A1B2C3D4E5F0724', 'task/phial/item/me:starlight_phial': '6A1B2C3D4E5F0744',
    'quest/vegetables': '6A1B2C3D4E5F0725',
    'task/vegetables/item/me:cucumber': '6A1B2C3D4E5F0745',
    'task/vegetables/item/me:lettuce': '6A1B2C3D4E5F0746',
    'task/vegetables/item/me:tomato': '6A1B2C3D4E5F0747',
    'quest/berries': '6A1B2C3D4E5F0726',
    'task/berries/item/me:strawberry': '6A1B2C3D4E5F0748',
    'task/berries/item/me:white_mushroom': '6A1B2C3D4E5F0749',
    'quest/pipeweed': '6A1B2C3D4E5F0727',
    'task/pipeweed/item/me:pipeweed': '6A1B2C3D4E5F0750',
    'task/pipeweed/item/me:pipeweed_seeds': '6A1B2C3D4E5F0751',
}

# key, title, icon, description lines, item objectives, manual check, dependencies, x, y
Q = [
    dict(key='intro', title='中州 · 中土之旅', icon='me:starlight_phial',
         desc=['中州（Middle-earth）是一整片中土大陆：新的群系、建筑、生物与农作。',
               '本包对它的改动：工匠台与合金炉需要 GT LV 电路；星光水晶瓶改为在星辉祭坛用冰雪女王战利品合成；蔬菜、浆果与蘑菇接入 GTMFO 营养与品质作物系统。'],
         items=[], check='已阅读中土之旅导航', deps=[], xy=(0, 0)),
    dict(key='artisan', title='工匠台（GT LV 锁）', icon='me:artisan_table',
         desc=['中州的核心 crafting 站：工匠台。',
               '科技锁：原配方中的锡锭已替换为 GT LV 电路（gtceu:basic_electronic_circuit），先推进格雷 LV。'],
         items=['me:artisan_table'], deps=['intro'], xy=(2, -2)),
    dict(key='alloy', title='合金炉（GT LV 锁）', icon='me:alloy_furnace',
         desc=['合金炉用于中州金属的冶炼与合金。',
               '科技锁：原配方的熔炉已替换为 GT LV 电路（gtceu:basic_electronic_circuit）。'],
         items=['me:alloy_furnace'], deps=['intro'], xy=(2, 2)),
    dict(key='phial', title='星光水晶瓶（星辉祭坛）', icon='me:starlight_phial',
         desc=['星光水晶瓶是中州探险的起点。',
               '本包改动：不再用工作台无序合成，改为在星辉发现祭坛合成：装水水瓶、冰雪女王战利品和 4 个发光材料。',
               '发现祭坛只能使用内圈 3×3；对照 JEI 祭坛图案。'],
         items=['me:starlight_phial'], deps=['artisan'], xy=(4, -2)),
    dict(key='vegetables', title='中州菜园', icon='me:cucumber',
desc=['中州蔬菜已接入本包 GTMFO 蔬菜营养、通用作物/种子标签；作物方块列入 Quality Food 的 quality_blocks（方块标签）。',
                '品质掉落仍由 Quality Food 的成熟作物判定和收获物资格共同决定，需游戏内测试；先认识黄瓜、生菜、番茄，再拓展地方作物。'],
         items=['me:cucumber', 'me:lettuce', 'me:tomato'], deps=['alloy'], xy=(4, 2)),
    dict(key='berries', title='浆果与蘑菇', icon='me:strawberry',
desc=['中州草莓在 GTMFO 中计入水果；多种模组蘑菇按较低值计入蔬菜。',
                '收集草莓和白蘑菇作为直接证据；若想做自动农业，请先观察各自真实作物方块、掉落和生长条件。'],
         items=['me:strawberry', 'me:white_mushroom'], deps=['vegetables'], xy=(6, 2)),
    dict(key='pipeweed', title='烟斗草', icon='me:pipeweed',
         desc=['烟斗草是中州特有作物。模组资源中有烟斗草制种配方：1 个烟斗草可制 1 个烟斗草种子。',
               '种子已接入 forge:seeds；具体生长条件以游戏内作物表现为准。'],
         items=['me:pipeweed', 'me:pipeweed_seeds'], deps=['vegetables'], xy=(6, -2)),

    dict(key='map', title='中土地图：先学会定位', icon='me:middle_earth_map',
         desc=['地图配方：8 张纸围住 1 本书。进入中土后制作并使用地图，熟悉区域、坐标与出生点。',
               '地图传送快捷键可在按键设置的 Middle-earth 分类查看；传送前确认目标点安全。'],
         items=['me:middle_earth_map'], deps=['phial'], xy=(6, -4)),
    dict(key='onboarding', title='第一次入境：角色创建', icon='me:starlight_phial',
         desc=['星光水晶瓶的右键效果是把你传送进中土；它本身不负责打开角色选择界面。',
               '模组另有 onboarding 角色流程，涉及派系、种族与出生点。首次入境观察是否出现；若没有，不要反复消耗/使用水晶瓶，请联系管理员核对服务端引导。管理员可用 `/middle_earth onboarding open`（需权限）尝试重新打开。',
               '派系是预设阵营，不是玩家自建帮会；本机未发现声望刷取或军衔晋升系统。'],
         check='已完成角色引导，记下所选派系、种族与出生点', deps=['map'], xy=(8, -4)),
    dict(key='races', title='种族：不只是外观', icon='me:middle_earth_map',
desc=['本机数据包含 8 种种族：human、elf、dwarf、hobbit、orc、uruk、goblin、snaga。',
               '种族会改变玩家基础属性，不只是外观：例如本机数据中 dwarf 为 22 HP 且有采矿效率加成，hobbit 为 14 HP、体型更小且攻击倍率降低；elf 有粉雪免疫/摔落减免，goblin 有攀爬能力。实际数值以角色界面显示为准。'],
         check='已查看种族属性，并确认当前角色的选择', deps=['onboarding'], xy=(10, -4)),
    dict(key='factions', title='派系：选择阵营与落脚点', icon='me:middle_earth_map',
         desc=['可选择多个自由民与黑暗势力派系/子派系；派系决定初始出生点及与 NPC 的外交关系。',
               '本章按当前 1.4.2-port 的数据介绍选择与敌我关系，不假设存在可刷声望、晋升军衔或自建帮会机制。'],
         check='已在角色界面/派系说明中确认可选派系与出生点', deps=['onboarding'], xy=(10, -2)),
    dict(key='diplomacy', title='外交关系：中立也可能危险', icon='me:middle_earth_map',
         desc=['派系外交用于判断 NPC 敌我；敌对派系会主动攻击。部分中立组织（如强盗、野生哥布林）也可能对你敌对。',
               '出发前看地图与玩家手册，带好护甲、食物和退路；不要把 NEUTRAL 简单理解成安全。'],
         check='已了解敌对关系会影响 NPC 行为，并准备好一次安全的野外行程', deps=['factions'], xy=(12, -2)),
    dict(key='mounts', title='坐骑与种族特性', icon='me:broadhoof_goat_spawn_egg',
         desc=['游戏内 Middle-earth 手册提供种族限制坐骑提示：矮人可用小麦驯服 Broadhoof Goat；精灵可尝试用三叶草、甜浆果、蘑菇等驯服 Great Horn；邪恶种族可用生肉驯服 Warg。',
               '手册还提到邪恶阵营可在 Cave Troll 睡眠时尝试用锁链驯服。以当前版本实际提示为准，勿在危险洞穴裸装尝试。'],
         check='已阅读坐骑手册，并确认自己种族/阵营可尝试的坐骑', deps=['races', 'factions'], xy=(12, -4)),
    dict(key='dungeons', title='遗迹与地下城：钥匙开宝库', icon='me:middle_earth_map',
         desc=['内置手册提示：地下城挑战波次会给钥匙，钥匙用于打开更深处的宝库。',
               '先准备武器、护甲、食物与撤退路线；不要把 trial key 与普通遗迹战利品混为一谈。'],
         check='已读地下城手册并完成一次有准备的遗迹探索', deps=['map'], xy=(8, 0)),
    dict(key='seeds', title='种子循环：从作物留种', icon='me:tomato_seeds',
         desc=['模组数据包提供多种 1:1 留种配方：作物产物可合成对应种子。',
               '先采到作物，再按 JEI 查看种子配方；不要假定所有作物都有独立种子或相同生长规则。'],
         items=['me:bell_pepper_seeds', 'me:cucumber_seeds', 'me:lettuce_seeds', 'me:tomato_seeds', 'me:flax_seeds'],
         deps=['vegetables'], xy=(6, 4)),
    dict(key='crop_variety', title='扩展菜园：地方作物', icon='me:leek',
         desc=['中州还有大葱、大蒜、甜椒、洋葱与亚麻等地方作物。',
               '本包已把常见蔬菜接入通用作物/种子标签；具体种子产出请看 JEI，部分种子配方是 1 个作物换 1 个种子。'],
         items=['me:leek', 'me:garlic', 'me:bell_pepper', 'me:onion'], deps=['seeds'], xy=(8, 4)),
    dict(key='flax', title='亚麻：农业副产物做线', icon='me:flax',
         desc=['亚麻有 1:1 留种配方；4 个亚麻可在工作台合成 1 根线。',
               '这是中州农业与基础材料的轻量联动，适合在稳定供粮后顺手开垦。'],
         items=['me:flax', 'me:flax_seeds'], deps=['crop_variety'], xy=(10, 6)),
    dict(key='food', title='中土厨房：把收获变成远行口粮', icon='me:vegetable_soup',
desc=['模组自带工作台配方与农夫乐事炖锅配方都已接入：蔬菜汤、鱼炖菜、蟹汤、禽肉餐、肉碗和肉蛋餐可用炖锅制作。',
                '这些料理也已加入 GTMFO 显式营养映射；用 JEI 查配方并亲自食用，确认营养显示后再作为长期远征口粮。'],
         items=['me:vegetable_soup', 'me:berry_pie', 'me:fish_stew'], deps=['crop_variety', 'berries'], xy=(10, 4)),
    dict(key='nutrition', title='营养与品质：农业接入整合包', icon='me:strawberry',
         desc=['整合脚本将中州蔬菜计入 GTMFO 蔬菜、草莓计入水果，多种蘑菇按较低值计入蔬菜；中州作物方块也接入品质作物标签。',
               'GTMFO 当前 HUD 关闭，数值看本包统一 Sunlit HUD；注意类别标签与单件显式营养值不是一回事。'],
         check='已查看统一 HUD/食物 tooltip，确认中州作物进入营养分类', deps=['food'], xy=(12, 4)),
]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def valid_id(value):
    return isinstance(value, str) and re.fullmatch(r'[0-9A-F]{16}', value) is not None and 0 < int(value, 16) <= 0x7FFFFFFFFFFFFFFF


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
        k = q['key']
        keys.append('quest/' + k)
        keys.extend('task/' + k + '/item/' + i for i in q.get('items', ()))
        if q.get('check'):
            keys.append('task/' + k + '/check')
    return keys


def load_map():
    if MAP.exists():
        doc = json.loads(MAP.read_text(encoding='utf-8'))
        if doc.get('schema') != 1 or doc.get('salt') != SALT or doc.get('group') != GROUP:
            raise ValueError('ID map owner/schema mismatch')
        return doc
    if not OUTPUT.exists() or digest(OUTPUT.read_bytes()) != INITIAL_SHA256:
        raise ValueError('Existing Middle-earth chapter differs from audited bootstrap; refusing to invent ID mapping')
    return dict(schema=1, salt=SALT, group=GROUP, ids=dict(LEGACY_IDS))


def allocate(old, keys, external):
    ids = dict(old.get('ids', {}))
    if ids.get('chapter') != LEGACY_IDS['chapter']:
        raise ValueError('Chapter identity changed')
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


def external_ids():
    result = {GROUP}
    pattern = re.compile(r'\bid:\s*"([0-9A-F]{16})"')
    for path in sorted(QUESTS.rglob('*.snbt')):
        if path == OUTPUT:
            continue
        result.update(pattern.findall(path.read_text(encoding='utf-8-sig')))
    return result


def build(ids, order):
    doc = dict(default_hide_dependency_lines=False, default_quest_shape='', filename='middle_earth',
               group=GROUP, icon='me:starlight_phial', id=ids['chapter'], order_index=order,
               quest_links=[], quests=[], title='&2&l中州&r · 中土之旅')
    quest_keys = {q['key'] for q in Q}
    for q in Q:
        for dep in q['deps']:
            if dep not in quest_keys:
                raise ValueError(f'Unknown dependency {dep} for {q["key"]}')
        tasks = [dict(id=ids['task/' + q['key'] + '/item/' + item], type='item', item=item, count=1,
                      consume_items=False, match_nbt=False, only_from_crafting=False) for item in q.get('items', ())]
        if q.get('check'):
            tasks.append(dict(id=ids['task/' + q['key'] + '/check'], title=q['check'], type='checkmark'))
        if not tasks:
            raise ValueError('Quest must have at least one objective: ' + q['key'])
        doc['quests'].append(dict(description=q['desc'], dependencies=[ids['quest/' + d] for d in q['deps']],
                                  icon=q['icon'], id=ids['quest/' + q['key']], tasks=tasks,
                                  title=q['title'], x=float(q['xy'][0]), y=float(q['xy'][1])))
    return doc


def validate(doc, ids, external, jar_items):
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
    if refs - qids:
        raise ValueError('Dangling quest dependency: ' + repr(sorted(refs - qids)))
    # Topological DFS: reject cycles before SNBT output.
    graph = {q['id']: q['dependencies'] for q in doc['quests']}
    active, done = set(), set()
    def visit(n):
        if n in active:
            raise ValueError('Quest dependency cycle at ' + n)
        if n in done:
            return
        active.add(n)
        for d in graph[n]:
            visit(d)
        active.remove(n); done.add(n)
    for n in graph:
        visit(n)
    for q in Q:
        for item in [q['icon']] + list(q.get('items', ())):
            if item.startswith('me:') and item not in jar_items:
                raise ValueError('Middle-earth item missing from current EN lang registry evidence: ' + item)
    return (dump(doc) + '\n').encode('utf-8')


def verify_mod_resources():
    if not ME_JAR.is_file():
        raise ValueError('Middle-earth jar missing: ' + str(ME_JAR))
    with zipfile.ZipFile(ME_JAR) as z:
        entries = set(z.namelist())
        lang = json.loads(z.read('assets/me/lang/en_us.json'))
        registered = {'me:' + key[len('item.me.'):] for key in lang if key.startswith('item.me.')}
        all_items = {q['icon'] for q in Q}
        all_items.update(item for q in Q for item in q.get('items', ()))
        for item in sorted(all_items):
            if item.startswith('me:'):
                path = item.split(':', 1)[1]
                if item not in registered:
                    raise ValueError('Item lacks current English registry key: ' + item)
                if f'assets/me/models/item/{path}.json' not in entries:
                    raise ValueError('Item model absent from current JAR: ' + item)
        expected_recipes = {
            'middle_earth_map': 'me:middle_earth_map',
            'empty_phial': 'me:empty_phial',
            'starlight_phial': 'me:starlight_phial',
            'bell_pepper_seeds': 'me:bell_pepper_seeds',
            'cucumber_seeds': 'me:cucumber_seeds',
            'lettuce_seeds': 'me:lettuce_seeds',
            'tomato_seeds': 'me:tomato_seeds',
            'flax_seeds': 'me:flax_seeds',
            'pipeweed_seeds': 'me:pipeweed_seeds',
            'string_from_flax': 'minecraft:string',
            'berry_pie': 'me:berry_pie',
            'vegetable_soup': 'me:vegetable_soup',
            'fish_stew': 'me:fish_stew',
        }
        for recipe, result in expected_recipes.items():
            name = f'data/me/recipes/{recipe}.json'
            if name not in entries:
                raise ValueError('Recipe resource missing: ' + name)
            doc = json.loads(z.read(name))
            actual = doc.get('result', {}).get('item')
            if actual != result:
                raise ValueError(f'Recipe output mismatch in {name}: {actual!r} != {result!r}')
        for tag in ('vegetable', 'berries', 'glowy'):
            name = f'data/me/tags/items/{tag}.json'
            if name not in entries:
                raise ValueError('Item tag missing: ' + name)
            json.loads(z.read(name))
    return len(all_items), len(expected_recipes)


def render():
    old = load_map()
    external = external_ids()
    ids = allocate(old, get_keys(), external)
    group_doc = (QUESTS / 'chapter_groups.snbt').read_text(encoding='utf-8-sig')
    if GROUP not in re.findall(r'id:\s*"([0-9A-F]{16})"', group_doc):
        raise ValueError('Middle-earth chapter group missing')
    with zipfile.ZipFile(ME_JAR) as z:
        lang = json.loads(z.read('assets/me/lang/en_us.json'))
    jar_items = {'me:' + key[len('item.me.'):] for key in lang if key.startswith('item.me.')}
    # Keep pre-existing chapter group order. New chapter remains in the current existing slot.
    order = old.get('order_index', 0)
    doc = build(ids, order)
    payload = validate(doc, ids, external, jar_items)
    checked_items, checked_recipes = verify_mod_resources()
    map_doc = dict(schema=1, salt=SALT, group=GROUP, order_index=order,
                   ids=dict(sorted(ids.items())), output_sha256=digest(payload),
                   source_jar_sha256=digest(ME_JAR.read_bytes()), checked_items=checked_items,
                   checked_recipe_resources=checked_recipes)
    map_bytes = (json.dumps(map_doc, ensure_ascii=False, indent=2, sort_keys=True) + '\n').encode('utf-8')
    return payload, map_bytes, doc


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='validate without writing')
    parser.add_argument('--verify-repeat', action='store_true', help='render twice in memory and compare exact bytes')
    args = parser.parse_args()
    payload, map_bytes, doc = render()
    if args.verify_repeat:
        payload2, map_bytes2, _ = render()
        if (payload, map_bytes) != (payload2, map_bytes2):
            raise SystemExit('Repeated render differs')
        print(json.dumps({'repeat_equal': True, 'quests': len(doc['quests']), 'sha256': digest(payload)}, ensure_ascii=False))
        return
    current_output = OUTPUT.read_bytes() if OUTPUT.exists() else None
    current_map = MAP.read_bytes() if MAP.exists() else None
    if args.check:
        if current_output != payload or current_map != map_bytes:
            raise SystemExit('Generated output/map differs; inspect and run without --check after approval')
        print(json.dumps({'check': 'ok', 'quests': len(doc['quests']), 'sha256': digest(payload)}, ensure_ascii=False))
        return
    # Fail closed if a generated chapter/map was edited outside this generator.
    if current_map is not None:
        old = json.loads(current_map)
        if current_output is None or digest(current_output) != old.get('output_sha256'):
            raise SystemExit('Published chapter differs from ID map; refusing overwrite')
    snapshots = {p: digest(p.read_bytes()) for p in sorted(QUESTS.rglob('*.snbt')) if p != OUTPUT}
    payload_again, map_again, _ = render()
    if payload_again != payload or map_again != map_bytes:
        raise SystemExit('Non-deterministic render; refusing write')
    if snapshots != {p: digest(p.read_bytes()) for p in sorted(QUESTS.rglob('*.snbt')) if p != OUTPUT}:
        raise SystemExit('Concurrent quest file change detected; rerun after review')
    OUTPUT.write_bytes(payload)
    MAP.write_bytes(map_bytes)
    print(json.dumps({'written': True, 'quests': len(doc['quests']), 'sha256': digest(payload)}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
