#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the AE2 addon-integration FTB Quests chapter.

Follows build_trade_chapter.py: stable business key -> persisted 16-hex ID map,
deterministic render, fail-closed validation. Text is inline Chinese.

Chapter hangs in the tech group (4A46A5E1358A80A6) right after ae2_overview (19):
pollution=20, technomancy=21, thaumic_addons=22, so this chapter takes order 23.

Every icon/item below was extracted from the pack's own mod jars on 2026-11-03:
  ae2                appliedenergistics2-forge-15.4.10.jar   assets/ae2/models/item
  ae2wtlib           ae2wtlib-15.3.3-forge.jar               assets/ae2wtlib/models/item
  mae2               mae2-2.0.1.jar                          assets/mae2/models/item
  appbot             applied-botanics-forge-1.5.2.jar        assets/appbot/models/item
  appmek             Applied-Mekanistics-1.4.2.jar           assets/appmek/models/item
  applied_greg       applied_greg-1.0.3-fix1.jar             assets/applied_greg/models/item
  appliedas          Applied Astralsorcery-1.20.1-0.5.0.jar  assets/appliedas/models/item
  thaumicenergistics thaumicenergistics-2.3.40-...-20746.jar assets/.../models/item + blockstates
  sunlitmarket       from build_trade_chapter.py's live-verified list
"""
from pathlib import Path
import argparse
import hashlib
import json
import re

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parents[2]
QUESTS = ROOT / 'config/ftbquests/quests'
OUTPUT = QUESTS / 'chapters/ae2_addons.snbt'
MAP = TOOLS / 'ae2_addons_ids.json'
GROUP = '4A46A5E1358A80A6'
SALT = 'society-ae2-addons-chapter-v1'
ORDER = 23

# External quest ids used as cross-chapter dependencies (must exist in other .snbt files).
EXT_AUTO = '55DE6BB7C9DF4ACE'          # ae2_overview: 自动合成
EXT_BIN_ENERGY = '543AB0B2A093F8B6'    # trade: 接受仓 FE 通道
EXT_BIN_MANA = '4040D45BF06D0973'      # trade: 接受仓魔力通道
EXT_BIN_ESSENTIA = '7160EA5E15705A84'  # trade: 接受仓源质通道
EXT_DEPS = {EXT_AUTO, EXT_BIN_ENERGY, EXT_BIN_MANA, EXT_BIN_ESSENTIA}

VERIFIED_ITEMS = {
    'ae2:controller', 'ae2:item_cell_housing', 'ae2:item_storage_cell_1k', 'ae2:cell_workbench',
    'ae2wtlib:wireless_universal_terminal', 'ae2wtlib:wireless_pattern_access_terminal',
    'mae2:item_multi_p2p_tunnel', 'mae2:256x_crafting_accelerator', 'mae2:cloud_chamber',
    'appbot:mana_storage_cell_1k', 'appbot:fluix_mana_pool',
    'appmek:chemical_storage_cell_1k',
    'applied_greg:eu_storage_cell_1k', 'applied_greg:ev_me_energy_input_hatch',
    'appliedas:lumen_storage_cell_1k', 'appliedas:altar_automation_interface',
    'appliedas:constellation_relay',
    'thaumicenergistics:essentia_cell_1k', 'thaumicenergistics:essentia_terminal',
    'thaumicenergistics:arcane_crafting_terminal', 'thaumicenergistics:essentia_export_bus',
    'thaumicenergistics:essentia_import_bus', 'thaumicenergistics:essentia_provider',
    'sunlitmarket:deposit_bin',
}

Q = [
    dict(key='intro', title='AE2 附属总览：这包里装了哪些扩展', icon='ae2:controller',
         desc=['本包在 AE2 15.4.10 之上装了 7 个附属：',
               'ae2wtlib（无线终端）、MAE2（多路 P2P 与合成加速）、Applied Botanics（魔力）、',
               'Applied Mekanistics（化学气体）、Applied Greg（GT 能量 EU）、Applied Astral Sorcery（星光）、Thaumic Energistics（源质）。',
               '它们的共同思路：让 ME 网络不只存物品和流体，还能存魔法与能量，并把整条产线接进同一个终端。',
               '前置：先看完 ae2_overview 章节的自动合成，再回来。'],
         check='已了解本包的 AE2 附属清单', deps=[], ext=[EXT_AUTO], xy=(0, 0)),

    dict(key='wt_universal', title='无线通用终端：全网络揣兜里', icon='ae2wtlib:wireless_universal_terminal',
         desc=['ae2wtlib 的看家货：无线通用终端 = 终端 + 合成终端 + 样板访问 + 物流终端四合一。',
               '前提是你在 ME 网络里插过一张对应能力的卡，再配合无线访问点覆盖。',
               '升级卡可以扩无线范围与功耗档位；出门挖矿也能查库存、下单自动合成。'],
         items=['ae2wtlib:wireless_universal_terminal'], deps=['intro'], xy=(2, 0)),

    dict(key='wt_patacc', title='无线样板访问终端：远程下单', icon='ae2wtlib:wireless_pattern_access_terminal',
         desc=['样板访问终端的无线版：把家里样板供应器上的合成方案全部拉到手上。',
               '配量子桥可以把两个基地的 ME 网络并成一个，样板互相可见。',
               '和 ae2wtlib 的无线编码终端搭配，远程改样板也不用跑回主机房。'],
         items=['ae2wtlib:wireless_pattern_access_terminal'], deps=['wt_universal'], xy=(4, 0)),

    dict(key='mae2_p2p', title='MAE2 多路 P2P：一根线当八根', icon='mae2:item_multi_p2p_tunnel',
         desc=['原版 P2P 一路信号就要一对隧道；MAE2 的 multi P2P 一对隧道可以挂 8 路。',
               '全家桶：物品 / 流体 / FE / EU / 样板 / 红石都有 multi 版，EU 和 FE 还互转。',
               '大网络里先上 multi P2P，再考虑加控制器，频道压力小得多。'],
         items=['mae2:item_multi_p2p_tunnel'], deps=['wt_patacc'], xy=(6, 0)),

    dict(key='mae2_accel', title='MAE2 合成加速器与云室', icon='mae2:256x_crafting_accelerator',
         desc=['4x / 16x / 64x / 256x 合成加速器直接叠在分子装配室旁，一次并行抓八个任务。',
               '大规模自动合成（GT 电路板、神秘注魔材料）靠它把等待时间压到秒级。',
               '云室（cloud_chamber）是 MAE2 的另一个小玩具：给协作处理器提供概率侧输出，前期缺粒崽时有用。'],
         items=['mae2:256x_crafting_accelerator'], deps=['mae2_p2p'], xy=(8, 0)),

    dict(key='cells_base', title='存储细胞：外壳、组件与工作台', icon='ae2:item_storage_cell_1k',
         desc=['所有附属细胞的套路都一样：外壳 + 对应组件在工作台合成，再用细胞工作台分区、改优先级。',
               'ME 物品细胞（1k~64k）只认“分区里的物品”，全空分区 = 什么都收。',
               '后面五张卡片：魔力 / 气体 / 星光 / EU / 源质，全是同一套逻辑，学会一次就会全部。'],
         items=['ae2:item_cell_housing', 'ae2:cell_workbench'], deps=['intro'], xy=(2, 6)),

    dict(key='appbot_mana', title='魔力细胞：植物魔法入库', icon='appbot:mana_storage_cell_1k',
         desc=['Applied Botanics 把魔力池变成 ME 网络的存储节点：魔力细胞放进驱动器，魔力池旁接上网络即可。',
               'fluix_mana_pool 是它的专属池子，直接以 ME 流体/魔力接口对接蓟花与精灵。',
               '魔力进 ME 后， Mana P2P 也能远距离传魔力，不用再拉魔力中继器长龙。'],
         items=['appbot:mana_storage_cell_1k'], deps=['cells_base'], xy=(4, 6)),

    dict(key='appmek_gas', title='化学细胞：气体入库', icon='appmek:chemical_storage_cell_1k',
         desc=['Applied Mekanistics 给 Mekanism 的气体 / 矿泥 / 渗液做了 ME 存储：化学细胞 1k~256k。',
               '机械爪、化学注射器产线接上网络后，气体直接进细胞，不用一排排气罐。',
               '化学 P2P 也能远距离输气，跨厂房走一根线。'],
         items=['appmek:chemical_storage_cell_1k'], deps=['cells_base'], xy=(6, 6)),

    dict(key='appas_lumen', title='星光细胞：星辉入库', icon='appliedas:lumen_storage_cell_1k',
         desc=['Applied Astral Sorcery 把星光（Illumination）变成 ME 存储资源：lumen 细胞系列。',
               '星光晶体在祭坛聚光后灌进网络，自动祭坛从此不用人守着看进度。',
               'astral_fluix 晶体系列是它的专属荧光材料，配合荧光簇（cluster）方块布置聚光。'],
         items=['appliedas:lumen_storage_cell_1k'], deps=['cells_base'], xy=(8, 6)),

    dict(key='appgreg_eu', title='EU 细胞与 GT 能量舱：格雷电力入网', icon='applied_greg:eu_storage_cell_1k',
         desc=['Applied Greg 让 ME 网络直接当 GT 的电池：EU 细胞（最高 256M）存电。',
               'ME 能量输入/输出舱（EV/HV/IV 各档，4a/16a）把 GT 电网和网络双向接通。',
               'ME 二极管（diode）用来单向限流，防止两个电网互相倒灌。'],
         items=['applied_greg:eu_storage_cell_1k', 'applied_greg:ev_me_energy_input_hatch'], deps=['cells_base'], xy=(10, 6)),

    dict(key='te_cell', title='源质细胞：神秘时代入库', icon='thaumicenergistics:essentia_cell_1k',
         desc=['Thaumic Energistics 把源质变成 ME 物品：源质细胞 1k~64k，装进驱动器即用。',
               '源质管从蒸馏器 / 陶罐接到网络任意接口，源质按要素自动入库。',
               '它是后面所有神秘自动化的地基：没有源质细胞，就没有源质终端。'],
         items=['thaumicenergistics:essentia_cell_1k'], deps=['cells_base'], xy=(12, 6)),

    dict(key='te_terminal', title='神秘终端与奥术合成终端', icon='thaumicenergistics:arcane_crafting_terminal',
         desc=['源质终端：在网络任何终端上直接看全网络源质存量，按要素搜索。',
               '奥术合成终端：站在原地做奥术合成台的一切，材料源质从网络里扣。',
               '无线版（wireless_essentia_terminal / wireless_arcane_crafting_terminal）配合 ae2wtlib 的访问点随处可用。'],
         items=['thaumicenergistics:essentia_terminal', 'thaumicenergistics:arcane_crafting_terminal'],
         deps=['te_cell'], xy=(14, 6)),

    dict(key='te_bus', title='源质总线：进出口与供应器', icon='thaumicenergistics:essentia_export_bus',
         desc=['源质导出总线把网络里的源质按要素定量喂给注魔祭坛、聚能晶块；导入总线反过来回收余量。',
               'essentia_provider / infusion_provider 是方块形态的大流量接口，接祭坛和蒸馏器用。',
               '奥术装配器（arcane_assembler）+ 蒸馏编码器（distillation_encoder）能把奥术配方写成样板全自动跑。'],
         items=['thaumicenergistics:essentia_export_bus', 'thaumicenergistics:essentia_import_bus',
                'thaumicenergistics:essentia_provider'],
         deps=['te_terminal'], xy=(16, 6)),

    dict(key='appas_altar', title='星辉祭坛自动化', icon='appliedas:altar_automation_interface',
         desc=['appliedas:altar_automation_interface 装在星空祭坛旁，祭坛的进料出料全走 ME。',
               'constellation_relay / constellation_core 把星座仪式的锁链拉进网络，配合样板做全套自动注星。',
               'me_celestial_gateway 是它的终局玩具：网络直接开星光传送门。'],
         items=['appliedas:altar_automation_interface', 'appliedas:constellation_relay'],
         deps=['appas_lumen'], xy=(8, 2)),

    dict(key='money_link', title='把能量和魔法换成钱', icon='sunlitmarket:deposit_bin',
         desc=['接受仓（SunlitMarket）对外就是五个口：物品、流体、FE、源质、魔力——全都能从 ME 网络直接灌。',
               'FE 50000 = 1 spur；魔力 2000 点 = 1 spur；源质按要素分三档（4/2/1 点 = 1 spur）。',
               'EU 先经 Applied Greg 的 ME 能量舱转成 FE 再卖；多余的细胞耗材别乱卖，先看价目表。',
               '详见「贸易」章节的接受仓五路。'],
         check='已把网络里的能量或魔法卖进接受仓',
         deps=['te_cell'], ext=[EXT_BIN_ENERGY, EXT_BIN_MANA, EXT_BIN_ESSENTIA], xy=(12, 2)),
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
    doc = dict(default_hide_dependency_lines=False, default_quest_shape='square', filename='ae2_addons',
               group=GROUP, icon='ae2:controller', id=ids['chapter'], order_index=ORDER,
               quest_links=[], quests=[], title='&b&l科技&r - AE2 附属联动')
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
        raise ValueError('AE2 chapter group missing from chapter_groups.snbt')
    doc = build(ids)
    payload = validate(doc, external_ids())
    map_doc = dict(schema=1, salt=SALT, group=GROUP, order_index=ORDER,
                   ids=dict(sorted(ids.items())), output_sha256=digest(payload))
    map_bytes = (json.dumps(map_doc, ensure_ascii=False, indent=2, sort_keys=True) + '\n').encode('utf-8')
    return payload, map_bytes

def check_stable():
    payload, _ = render()
    if OUTPUT.exists() and OUTPUT.read_bytes() != payload:
        raise SystemExit('ae2_addons.snbt exists but differs from the deterministic render')

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
    doc = json.loads(map_bytes.decode('utf-8'))
    print('wrote %s (%d bytes, %d quests) and %s' % (OUTPUT.name, len(payload), len(Q), MAP.name))
