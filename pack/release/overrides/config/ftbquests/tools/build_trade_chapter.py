#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the trade / pawnshop FTB Quests chapter.

Follows config/ftbquests/tools/build_middle_earth_chapter.py: stable business key ->
persisted 16-hex ID map, deterministic render, fail-closed validation.
Text is inline Chinese (FTBQ_GUIDE.md section 5, since 2026-09-17).

Every icon/item below was checked against the live server registry
(ForgeRegistries.ITEMS.containsKey) on 2026-11-03.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parents[2]
QUESTS = ROOT / 'config/ftbquests/quests'
OUTPUT = QUESTS / 'chapters/trade.snbt'
MAP = TOOLS / 'trade_ids.json'
GROUP = '7B3E5A9C1D2F4068'
SALT = 'society-trade-chapter-v1'
ORDER = 0

VERIFIED_ITEMS = {
    'sunlitmarket:counter', 'sunlitmarket:deposit_bin',
    'numismatics:spur', 'numismatics:cog', 'numismatics:bevel', 'numismatics:crown',
    'me:leek', 'me:vegetable_soup', 'me:starlight_phial',
    'tconstruct:cobalt_ingot', 'tconstruct:manyullyn_ingot',
    'thaumcraft:amber', 'thaumcraft:essentia_tube', 'thaumcraft:warded_jar',
    'astralsorcery:starmetal_ingot', 'astralsorcery:aquamarine',
    'botania:mana_pearl', 'botania:mana_spreader',
    'gtceu:lv_1a_energy_converter',
    'minecraft:bucket', 'minecraft:chest', 'minecraft:hopper', 'minecraft:barrel',
    'minecraft:compass', 'minecraft:filled_map', 'minecraft:written_book',
    'minecraft:emerald', 'minecraft:gold_ingot', 'minecraft:iron_ingot', 'minecraft:paper',
}

Q = [
    dict(key='intro', title='贸易总览：钱从哪来，货卖给谁', icon='numismatics:spur',
         desc=['本包的钱不走虚拟钱包：能花的就是硬币和 Numismatics 银行账户。出货箱、村民商店、医院债务全都直接走银行。',
               '当铺（SunlitMarket）给你三条生意：① 直接和商人 NPC 买卖；② 摆柜台让村民与命名 NPC 上门采购；③ 接受仓把产线多出来的能量和魔法换成钱。',
               '先 /sunlitmarket balance 看手上有多少钱，/sunlitmarket factions 看 16 个中州派系。'],
         check='已看过余额与派系列表', deps=[], xy=(0, 0)),

    dict(key='merchant_me', title='中州商路：六位商人', icon='me:leek',
         desc=['中州商人共六位：夏尔农户、刚铎军需官、洛汗猎手、萝林草药师、孤山矿商、中州钱庄。',
               '他们按货架卖货、每天有库存，收购价高于出货箱——把中州作物和矿石卖给他们，比扔出货箱划算。',
               '商人是管理员放置的 NPC（带 sunlitmarket.me.<商人> 标签），不会自然生成。找到后右键开面板，或用 /sunlitmarket near 32 扫一圈；附近一个都没有，说明这批商人还没放置，找管理员。',
               '声望到 100 时买价 9 折、卖价 +5%，每笔成交都会涨声望。'],
         check='已和一位中州商人完成一次买卖', deps=['intro'], xy=(2, -6)),

    dict(key='merchant_themed', title='主题商人：匠魂 / 神秘 / 星辉 / 植物魔法', icon='tconstruct:cobalt_ingot',
         desc=['装了对应模组后，管理员可通过专用标签放置四位商人：匠魂铸师、神秘材料商、星辉商人、植物魔法材料商。',
               '他们卖的是别的章节要用的高阶材料（钴、玛玉灵、琥珀、水银、星辉锭、魔力珍珠……）。价格按本包经济定，比自造省时间但更贵。',
               '他们同时也收货：把多余的钴、琥珀、星辉锭卖回去，比接受仓更划算。'],
         check='已查看主题商人的货架', deps=['merchant_me'], xy=(4, -6)),

    dict(key='merchant_unlock', title='解锁门槛：先做任务再买', icon='tconstruct:manyullyn_ingot',
         desc=['高阶货带 unlock id（theme.tinkers.adept、theme.astral.attuned 等），未解锁时不能购买，货架会标出门槛。',
               '匠魂「高阶材料：玛玉灵」→ theme.tinkers.adept；星辉「铁矿石到星辉锭」→ theme.astral.attuned。',
               '神秘工业「模板 2：虚空锭 + 水晶精华」→ theme.thaumcraft.adept；植物魔法的泰拉钢锭任务 → theme.botania.adept。神秘锭入门任务不会解锁虚空锭。',
               '奖励命令以领奖玩家身份、临时提升权限执行；队友分别领取。本章不发这些 unlock；旧存档已完成里程碑的玩家，也可在对应任务领取新增的个人奖励，用 /sunlitmarket locks 查看结果。'],
         check='已了解 unlock 门槛的来源', deps=['merchant_themed'], xy=(6, -6)),

    dict(key='counter', title='摆一张柜台', icon='sunlitmarket:counter',
         desc=['柜台 = 3 个木板台阶 + 5 块木板，开局就能做。',
               '放下后归放置者所有，周围 8 格内的村民与命名 NPC 会陆续过来提需求。',
               '柜台不是货架商店：你把货放进柜台库存，顾客按需求买走。'],
         items=['sunlitmarket:counter'], deps=['intro'], xy=(2, 0)),

    dict(key='counter_owner', title='柜台怎么运作', icon='minecraft:chest',
         desc=['每 10 秒扫描一次，最多同时挂 3 个需求，每个需求存活 1 分钟。',
               '每个 NPC 冷却 60 秒、每天最多提 12 次，防止一个村民被反复薅。',
               '需求按 sv.npc.* 规则和货池生成；价格锚是出货箱价，顾客出价 = 出货箱价 × 分类系数（低于 1.0，所以你有差价可赚）。',
               '带 sunlitmarket.me.* 或 sunlitmarket.theme.* 专用商人标签的 NPC 只开商店，不再兼任柜台顾客。没有这些标签的自然平民仍可提出需求。'],
         check='已理解需求的生成与过期规则', deps=['counter'], xy=(4, 0)),

    dict(key='counter_customer', title='服务第一位顾客', icon='numismatics:cog',
         desc=['右键柜台打开界面，把顾客要的货放进去成交。',
               '成交会涨该派系的结盟值，也会记进 /sunlitmarket rep。',
               '顾客是谁取决于附近有什么：原版村民按职业认，命名 NPC 按 dialog.npc.<id>.name 里的 id 认。'],
         check='已完成一次柜台成交', deps=['counter_owner'], xy=(6, 0)),

    dict(key='counter_haggle', title='议价、公平交易与赃物', icon='minecraft:emerald',
         desc=['价格会随声望和货架稀缺度浮动：卖得越多库存越少，价格往上走；补货后回落。',
               '宰客会掉结盟值。带 heat 的货（赃物）还会加通缉值，用 /sunlitmarket wanted 查看。',
               '收赃会被执法派系盯上，通缉值只能靠时间或罚金清零。'],
         check='已了解议价与通缉的影响', deps=['counter_customer'], xy=(8, 0)),

    dict(key='bin', title='造一台接受仓', icon='sunlitmarket:deposit_bin',
         desc=['接受仓 = 7 铁锭 + 1 金锭 + 1 箱子。',
               '它同时对外暴露五种接口：物品、流体、FE 能量、源质、魔力。管道、线缆、源质管、魔力扩散器都能直接往里灌。',
               '这是本包唯一「把能量和魔法换成钱」的出口。'],
         items=['sunlitmarket:deposit_bin'], deps=['intro'], xy=(2, 6)),

    dict(key='bin_items', title='物品通道：只收出货箱不收的', icon='minecraft:hopper',
         desc=['出货箱已收购物品的拒收边界，由 svAcceptBoundary.js 按 global.trades 中的有效价格生成；每次脚本重载重新建立，不是 deposit_values.json 中固定数量的物品表。',
               '没有单独定价的物品，回落到商人货架的收购价。当前真正能卖进接受仓的，主要是主题模组材料（星辉、植物魔法、匠魂、神秘）与中州硬币。',
               'svDepositItems.js 另外给 16 种采石/挖矿废料开了最低价（圆石、深板岩、下界岩、凝灰岩、方解石、砂砾、安山岩 / 闪长岩 / 花岗岩、玄武岩、黑石、末地石、沙、红沙、土、燧石），1 spur/件。',
               '一句话：接受仓收的是「出货箱不要的东西」，别指望拿它当第二台出货箱。'],
         check='已确认接受仓收哪些物品', deps=['bin'], xy=(4, 6)),

    dict(key='bin_fluid', title='流体通道：柴油 / 汽油 / 石油', icon='minecraft:bucket',
         desc=['流体按单位计价，默认 1，按物品覆盖：柴油 8、汽油 10、原油 6、硫酸 3、杂酚油 2、重燃油 7、轻燃油 7、石脑油 6、炼油气 4（见 svDepositRates.js）。',
               '接 GT 流体管道或任意 IFluidHandler 管道即可。',
               '这是把炼油与化工副产品变现的主要途径。'],
         check='已把一条流体管道接进接受仓', deps=['bin_items'], xy=(6, 6)),

    dict(key='bin_energy', title='FE 通道：50000 FE = 1 spur', icon='gtceu:lv_1a_energy_converter',
         desc=['接受仓吃 Forge Energy（FE）。GT 的 EU 不是 FE，中间要一台能量转换器（gtceu:lv_1a_energy_converter）。',
               '汇率 50,000 FE = 1 spur，写在 energy.fePerSpur。',
               '拿一台能量转换器对着接受仓输出，就能把多余电力变成钱。'],
         check='已把 FE 接进接受仓', deps=['bin_fluid'], xy=(8, 6)),

    dict(key='bin_essentia', title='源质通道：按要素稀有度分三档', icon='thaumcraft:essentia_tube',
         desc=['接受仓挂的是神秘时代的源质传输能力，用源质管把罐子或蒸馏器接过来即可。',
               '价格按要素分档（svDepositRates.js）：常见 20 种（aer / terra / ignis / aqua / ordo / perditio 等）4 点 = 1 spur；',
               '少见 21 种（gelum / lux / motus / potentia / praecantatio 等）2 点 = 1 spur；',
               '稀有 7 种（auram / alienis / cognitio / vitium / tempestas / vacuos / tenebrae）1 点 = 1 spur。',
               '想改哪一档，改脚本里对应的数组即可，不用动 mod。'],
         check='已把源质管接进接受仓', deps=['bin_energy'], xy=(10, 6)),

    dict(key='bin_mana', title='魔力通道：2000 mana = 1 spur', icon='botania:mana_pearl',
         desc=['接受仓吃植物魔法的魔力能力，用魔力扩散器或魔力池接过来。',
               '汇率 2,000 mana = 1 spur（mana.manaPerSpur）。',
               '魔力本来就是自动产出的，接过来等于给花田加一条被动收入。'],
         check='已把魔力接进接受仓', deps=['bin_essentia'], xy=(12, 6)),

    dict(key='bin_buyback', title='每日回收预算：它不是印钞机', icon='numismatics:bevel',
         desc=['接受仓有回收上限：每天全服 100,000、每人 20,000（buyback.dailyCap / playerCap）。',
               '用满就等日结——日结跟着可见天数走，睡觉会推进。',
               '规划产线时按这个额度算，别按无限产能算。'],
         check='已确认每日回收上限', deps=['bin_mana'], xy=(14, 6)),

    dict(key='chart', title='行情面板：先看价再动手', icon='minecraft:filled_map',
         desc=['/sunlitmarket chart 打开行情面板，/sunlitmarket chart <指数> [周期] 直接跳到某一条。',
               '蜡烛只由真实成交生成：没人买卖的时段就是空的，不会拿报价回填。',
               '中州 NPC 的对话里也有「看行情」选项，效果相同。'],
         check='已打开行情面板', deps=['intro'], xy=(2, 12)),

    dict(key='indices', title='三条指数', icon='minecraft:compass',
         desc=['谷蔬指（sv.produce）、金属指（sv.metal）、料理指（sv.delicacy）。',
               '指数是成员货架「价格倍率 × 稀缺度」的几何平均，起点 1000。',
               '/sunlitmarket index 打印实时值；还没有成交时显示 n/a。'],
         check='已查看三条指数的实时值', deps=['chart'], xy=(4, 12)),

    dict(key='futures', title='期货：和别的玩家对赌未来价', icon='numismatics:crown',
         desc=['/sunlitfutures offer | list | mine | take | cancel | claim | history | status。',
               '期货是玩家对玩家：你挂一张「某指数到某天到某价」的合约，别人接单。',
               '到期按真实指数结算，钱从对手方来，系统不印钱。',
               '离线期间结算的合约，下次登录自动补发。'],
         check='已看懂一张期货合约的条款', deps=['indices'], xy=(6, 12)),

    dict(key='alignment', title='结盟值：中州派系怎么看你', icon='me:starlight_phial',
         desc=['16 个中州派系各有结盟值：/sunlitmarket rep 看自己的，/sunlitmarket align 看全部。',
               '来源有三条：与派系 NPC 成交、给 NPC 送礼（好感度 ×2 映射过来）、击杀敌对派系。',
               '结盟值决定价格阶梯和部分商人的可买清单，并且每天向 0 回落一点。'],
         check='已查看当前派系结盟值', deps=['counter_haggle'], xy=(10, 0)),

    dict(key='stages', title='任务阶段：成交 1 / 10 / 50 次', icon='minecraft:written_book',
         desc=['成交 1、10、50 次分别解锁 sm_pawn_first / sm_pawn_ten / sm_pawn_fifty，并镜像成 sv.pawn.<阶段>。',
               '这些 id 可以直接写进 FTBQ 条件，也可以作为商人 offer 的 unlock。'],
         check='已确认自己的成交阶段', deps=['alignment'], xy=(12, 0)),

    dict(key='debt', title='债务先扣：绕不开的医院账单', icon='minecraft:gold_ingot',
         desc=['当铺给你付款时，先扣 server.persistentData.debts 里的欠款再入账——和出货箱同一顺序。',
               '所以「欠着医院的钱去当铺套现」这条路是堵死的。',
               '欠款还清之前，柜台收购与接受仓结算都会先拿去抵债。'],
         check='已了解付款会先抵债', deps=['counter_customer'], xy=(6, 2)),
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
    doc = dict(default_hide_dependency_lines=False, default_quest_shape='', filename='trade',
               group=GROUP, icon='numismatics:spur', id=ids['chapter'], order_index=ORDER,
               quest_links=[], quests=[], title='&6&l贸易&r · 当铺与商路')
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
        doc['quests'].append(dict(description=q['desc'], dependencies=[ids['quest/' + d] for d in q['deps']],
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
    if refs - qids:
        raise ValueError('Dangling quest dependency: ' + repr(sorted(refs - qids)))
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
                raise ValueError('Item not in the live-verified registry list: ' + item)
    return (dump(doc) + '\n').encode('utf-8')


def render():
    ids = allocate(get_keys(), external_ids())
    group_doc = (QUESTS / 'chapter_groups.snbt').read_text(encoding='utf-8-sig')
    if GROUP not in re.findall(r'id:\s*"([0-9A-F]{16})"', group_doc):
        raise ValueError('Trade chapter group missing from chapter_groups.snbt')
    doc = build(ids)
    payload = validate(doc, external_ids())
    map_doc = dict(schema=1, salt=SALT, group=GROUP, order_index=ORDER,
                   ids=dict(sorted(ids.items())), output_sha256=digest(payload))
    map_bytes = (json.dumps(map_doc, ensure_ascii=False, indent=2, sort_keys=True) + '\n').encode('utf-8')
    return payload, map_bytes, doc


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--verify-repeat', action='store_true')
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
            raise SystemExit('Generated output/map differs; inspect before writing')
        print(json.dumps({'check': 'ok', 'quests': len(doc['quests']), 'sha256': digest(payload)}, ensure_ascii=False))
        return
    if current_map is not None:
        old = json.loads(current_map)
        if current_output is None or digest(current_output) != old.get('output_sha256'):
            raise SystemExit('Published chapter differs from ID map; refusing overwrite')
    OUTPUT.write_bytes(payload)
    MAP.write_bytes(map_bytes)
    print(json.dumps({'written': True, 'quests': len(doc['quests']), 'sha256': digest(payload)}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
