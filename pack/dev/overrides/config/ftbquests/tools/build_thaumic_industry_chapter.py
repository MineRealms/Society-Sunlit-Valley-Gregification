#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the thaumic-industry FTB Quests chapter (Pollution mystic circuits + industrial infusion).

Follows build_trade_chapter.py: stable business key -> persisted 16-hex ID map,
deterministic render, fail-closed validation. Text is inline Chinese.

Chapter hangs in the tech group (4A46A5E1358A80A6), order 25 (bio_wetware took 24).

External deps (resolved 2026-11-04 against the live chapter set):
  35F501BCCBED6EC4  thaumcraft  : 神秘学的起点：魔导透镜
  4F9A048DEAAA894C  pollution   : 两种熔炉：物品→源质 / 流体
  769ADA236C630FC7  pollution   : 选定第一条要工业化的配方并查看结构

Every icon/item below was checked with ForgeRegistries.ITEMS.getValue on the live
1.20.1 test server on 2026-11-04. Recipe facts were dumped from the same server's
RecipeManager in the same session:
  pollution:assembler/thaumic_circuit/0..6      200t x5, 800t x2
  pollution:infusion/blood_circuit_template_2..4
  pollution:industrial_infusion_recipes/industrial_infusion/thaumic/...  (19 total)
"""
from pathlib import Path
import argparse
import hashlib
import json
import re

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parents[2]
QUESTS = ROOT / 'config/ftbquests/quests'
OUTPUT = QUESTS / 'chapters/thaumic_industry.snbt'
MAP = TOOLS / 'thaumic_industry_ids.json'
GROUP = '4A46A5E1358A80A6'
SALT = 'society-thaumic-industry-chapter-v1'
ORDER = 25

EXT_TC_INTRO = '4F15F9F6021B0AF8'        # thaumcraft: 神秘学的起点：魔导透镜
# 4F15F9F6021B0AF8 才是魔导透镜的 quest id；35F501BCCBED6EC4 是它那条 8 cog 奖励的 id，
# 抄成奖励 id 会让依赖悬空（FTBQ 不报错，但前置永远不满足）。
EXT_ESSENTIA_FURNACE = '4F9A048DEAAA894C'  # pollution: 两种熔炉
EXT_INDUSTRIALIZE = '769ADA236C630FC7'   # pollution: 选定第一条要工业化的配方
EXT_DEPS = {EXT_TC_INTRO, EXT_ESSENTIA_FURNACE, EXT_INDUSTRIALIZE}

VERIFIED_ITEMS = {
    'pollution:industrial_infusion', 'pollution:essence_smelter', 'pollution:infused_exchange',
    'pollution:blood_circuit', 'pollution:blood_circuit_advanced',
    'pollution:blood_circuit_ultimate', 'pollution:blood_circuit_supreme',
    'pollution:blood_circuit.0', 'pollution:blood_circuit.1', 'pollution:blood_circuit.2',
    'pollution:blood_circuit.3', 'pollution:blood_circuit.4', 'pollution:blood_circuit.5',
    'pollution:blood_circuit.6', 'pollution:blood_circuit.7',
    'thaumcraft:thaumium_ingot', 'thaumcraft:void_ingot', 'thaumcraft:crystal_essence',
    'thaumcraft:quicksilver', 'thaumcraft:primordial_pearl', 'thaumcraft:infusion_altar',
    'thaumcraft:thaumonomicon',
    'thaumadds:mithminite_ingot', 'thaumadds:mithrillium_ingot',
    'tainted_magic:shadow_metal_ingot', 'tainted_magic:creation_shard',
    'isorropia:ethereal_shard', 'thaumictinkerer:ichorium',
    'gtceu:circuit_assembler',
}

Q = [
    dict(key='intro', title='神秘工业：祭坛搬进车间', icon='pollution:industrial_infusion',
         desc=['魔法×GT 的总原则：前期用神秘手段（坩埚／奥术／注魔祭坛）打基础，高级阶段解锁工业化批量生产。',
               '本章三件事：① &6奥术电路&r——神秘主题的 GT 电路梯，MV 到 UV 七级；② &6工业注魔&r——把 TC 配方批量转写成 GT 配方；③ &6源质估值&r——1 点源质到底等于多少。',
               '工业化是&e杠杆&r，不是替代：所有手工祭坛配方都保留，老存档的研究、机器、物品 ID 不变。',
               '本章的产物直接进 gtceu:circuits/mv..uv 标签，所以 GT 主线里写「电路」的地方都能吃。'],
         check='已了解本章的三条主线', deps=[], ext=[EXT_INDUSTRIALIZE], xy=(0, 0)),

    dict(key='templates', title='模板 1：奥术工作台造出基础血电路', icon='pollution:blood_circuit',
         items=['pollution:blood_circuit'],
         desc=['奥术工作台（附魔台旁的书架阵）：&7T Q T / 空格 B 空格&r，T = 神秘锭、Q = 水银、B = 基础集成电路。',
               'vis 消耗：&6气 16 + 秩序 8&r。TC4R 的奥术配方只认六个原始 vis 通道，写成复合要素（如灵气）会被静默丢弃，配方根本不会加载。',
               '产物是 &6基础血电路（pollution:blood_circuit）&r——整条神秘电路梯的起点，也是模板 2 的中心物。',
               '这条配方没有研究门槛，拿到材料就能做；后面的模板 2／3／4 才是注魔。'],
         check='已在奥术工作台做出基础血电路', deps=['intro'], ext=[EXT_TC_INTRO], xy=(2, 0)),

    dict(key='template_2', title='模板 2：虚空锭 + 水晶精华', icon='pollution:blood_circuit_advanced',
         items=['pollution:blood_circuit_advanced'],
         desc=['注魔祭坛：中心物 &6基础血电路&r，组件 &7虚空锭 1 + 水晶精华 2 + 水银 1&r。',
               '要素：&6源质 16 / 金属 8 / 虚空 8&r；不稳定度 3。',
               '产物 &6进阶血电路&r 是 EV／IV 两级神秘电路的模板。'],
         check='已注魔出进阶血电路', deps=['templates'], xy=(4, 0)),

    dict(key='template_3', title='模板 3：秘银 + 影金', icon='pollution:blood_circuit_ultimate',
         items=['pollution:blood_circuit_ultimate'],
         desc=['注魔祭坛：中心物 &6进阶血电路&r，组件 &7秘银锭（thaumadds:mithminite_ingot）+ 影金锭（tainted_magic:shadow_metal_ingot）+ 以太碎片 2&r。',
               '要素：&6源质 24 / 异界 16 / 金属 12&r；不稳定度 5。',
               '产物 &6终极血电路&r 是 LuV／ZPM 两级的模板。'],
         check='已注魔出终极血电路', deps=['template_2'], xy=(6, 0)),

    dict(key='template_4', title='模板 4：秘银锂 + 创造碎片', icon='pollution:blood_circuit_supreme',
         items=['pollution:blood_circuit_supreme'],
         desc=['注魔祭坛：中心物 &6终极血电路&r，组件 &7秘银锂（thaumadds:mithrillium_ingot）+ 创造碎片（tainted_magic:creation_shard）+ 原始珍珠&r。',
               '要素：&6源质 32 / 异界 24 / 灵气 24&r；不稳定度 8。',
               '产物 &6至尊血电路&r 是 UV 神秘电路的模板——也是这条梯子的顶端。'],
         check='已注魔出至尊血电路', deps=['template_3'], xy=(8, 0)),

    dict(key='circuit_mv', title='神秘电路 MV：模板 1 + 神秘锭', icon='pollution:blood_circuit.0',
         items=['pollution:blood_circuit.0'],
         desc=['GT 电路组装机：&7模板 1 + 神秘锭 + 塑料印刷电路板 + 4 细红合金线 + 72mB 焊锡 → 2 个&r，60 EU/t、200t，无洁净室。',
               '配方 id：pollution:assembler/thaumic_circuit/0。',
               '严格同级：电压、时长、产量都对齐原版 MV 电路配方，只把芯片组换成模板 + 神秘金属。',
               '从这一级起，配方写 gtceu:circuits/mv 的地方都会接受它。'],
         check='已做出 MV 神秘电路', deps=['templates'], xy=(4, -6)),

    dict(key='circuit_hv', title='神秘电路 HV：水晶精华', icon='pollution:blood_circuit.1',
         items=['pollution:blood_circuit.1'],
         desc=['电路组装机：&7模板 1 + 水晶精华 + 环氧印刷电路板 + 8 细金银合金线 + 72mB 焊锡 → 2 个&r，600 EU/t、200t，&e普通洁净室&r。',
               '配方 id：pollution:assembler/thaumic_circuit/1。',
               '从 HV 起进入洁净室时代：没有洁净室直接不开机。'],
         check='已做出 HV 神秘电路', deps=['circuit_mv'], xy=(6, -6)),

    dict(key='circuit_ev', title='神秘电路 EV：虚空锭', icon='pollution:blood_circuit.2',
         items=['pollution:blood_circuit.2'],
         desc=['电路组装机：&7模板 2 + 虚空锭 + 纤维增强印刷电路板 + 12 细铂线 + 72mB 焊锡 → 2 个&r，2400 EU/t、200t，洁净室。',
               '配方 id：pollution:assembler/thaumic_circuit/2。',
               '模板从这一级换成进阶血电路——电路梯与祭坛模板是同步升级的。'],
         check='已做出 EV 神秘电路', deps=['circuit_hv'], xy=(8, -6)),

    dict(key='circuit_iv', title='神秘电路 IV：秘银', icon='pollution:blood_circuit.3',
         items=['pollution:blood_circuit.3'],
         desc=['电路组装机：&7模板 2 + 秘银锭 + 多层纤维增强印刷电路板 + 8 细铌钛线 + 72mB 焊锡 → 2 个&r，9600 EU/t、200t，洁净室。',
               '配方 id：pollution:assembler/thaumic_circuit/3。',
               '秘银（mithminite）来自神秘附属，是本包 IV 级神秘材料的骨干。'],
         check='已做出 IV 神秘电路', deps=['circuit_ev'], xy=(10, -6)),

    dict(key='circuit_luv', title='神秘电路 LuV：adaminite', icon='pollution:blood_circuit.4',
         items=['pollution:blood_circuit.4'],
         desc=['电路组装机：&7模板 3 + adaminite（thaumadds:adaminite_ingot）+ 8 细钇钡铜氧线 + 72mB 焊锡 → 2 个&r，38400 EU/t、200t，洁净室。',
               '配方 id：pollution:assembler/thaumic_circuit/4。',
               '这一级不需要电路基板，靠框架与线材堆叠；与湿件线并列为 LuV 的两条电路来源。'],
         check='已做出 LuV 神秘电路', deps=['circuit_iv'], xy=(12, -6)),

    dict(key='circuit_zpm', title='神秘电路 ZPM：秘银锂', icon='pollution:blood_circuit.5',
         items=['pollution:blood_circuit.5'],
         desc=['电路组装机：&7模板 3 + 秘银锂 + 48 退火铜单线 + 2 个 HSS-G 框架 + 288mB 焊锡 → 1 个&r，7680 EU/t、800t，洁净室。',
               '配方 id：pollution:assembler/thaumic_circuit/5。',
               '产量从 2 掉到 1、时长翻四倍：ZPM 级的成本台阶在这里，别按 MV 的产能规划。'],
         check='已做出 ZPM 神秘电路', deps=['circuit_luv'], xy=(14, -6)),

    dict(key='circuit_uv', title='神秘电路 UV：灵液', icon='pollution:blood_circuit.6',
         items=['pollution:blood_circuit.6'],
         desc=['电路组装机：&7模板 4 + 灵液（thaumictinkerer:ichorium）+ 8 铌钛单线 + 2 个 HSS-E 框架 + 1440mB 焊锡 → 1 个&r，30720 EU/t、800t，&e无洁净室条件&r。',
               '配方 id：pollution:assembler/thaumic_circuit/6。',
               '灵液是神秘工匠的顶级材料，产量受注魔速度限制——UV 神秘电路是本章的终点。'],
         check='已做出 UV 神秘电路', deps=['circuit_zpm'], xy=(16, -6)),

    dict(key='tag_note', title='标签是「可替代」，不是「自动替换」', icon='gtceu:circuit_assembler',
         desc=['七个电路已写进 gtceu:circuits/mv..uv 物品标签（数据包 data/gtceu/tags/items/circuits/*.json）。',
               'GT 配方按标签匹配：写 circuits/mv 的配方同时接受原版 MV 电路与神秘 MV 电路。',
               '所以它们是&e并行来源&r，不是替代品——用哪条取决于你手上的材料，原版路线一直有效。',
               '标签只影响配方匹配，不改物品本身的用途。'],
         check='已确认标签的作用方式', deps=['circuit_uv'], xy=(8, -12)),

    dict(key='disabled', title='退役的 7 个 ID：.7 ~ .12', icon='pollution:blood_circuit.7',
         desc=['blood_circuit.7 到 .12 对应 UHV ~ MAX。本包不规划这些时代：没有配方、没有标签、JEI 里隐藏。',
               '保留 ID 只是为了让老存档的物品不变成「空气」——它们不会消失，但也不再有用途。',
               '不要为它们补配方或标签：一旦某个奖励或合成发出占位物品，就可能直接绕过整段工业链。'],
         check='已了解退役电路的处理方式', deps=['circuit_uv'], xy=(12, -12)),

    dict(key='industrial_intro', title='工业注魔：把 TC 配方批量转写', icon='pollution:industrial_infusion',
         items=['pollution:industrial_infusion'],
         desc=['工业注魔多方块把 TC 的 &6infusion / crucible / arcane&r 配方转写成 GT 配方，用并行仓（IV/LuV/ZPM/UV = 4/16/64/256）与超频做量产。',
               '只转&e白名单产物&r：神秘锭、虚空锭、水银、平衡碎片、水晶精华、原始珍珠、盐、秘银／锇铱系、影金、创造碎片、以太碎片、灵液。',
               '要素 → 对应注魔流体，每点 &6144mB&r；奥术 vis 每点 &636mB&r（灵气可再生，比源质便宜）。',
               'EUt 固定 HV 档；时长 = max(100, 要素总量 × 5) tick；原研究键写进配方属性，机主必须有对应研究才能开机。',
               '手工祭坛保留——工业注魔是产能杠杆，不是解锁门槛。'],
         check='已搭建工业注魔多方块', deps=['intro'], ext=[EXT_ESSENTIA_FURNACE], xy=(2, 6)),

    dict(key='industrial_batch', title='已转写的 19 条配方', icon='thaumcraft:thaumium_ingot',
         items=['thaumcraft:thaumium_ingot'],
         desc=['运行时统计：&619 条&r工业注魔配方 = 16 条来自模组 JSON + 3 条代码孪生模板（2／3／4）。',
               '典型时长：神秘锭／虚空锭／平衡碎片（六种）100t；以太碎片 360t；秘银锂 475t；灵液注魔 640t；秘银 1350t；创造碎片 1650t；adaminite 2150t；灵液 3000t。',
               '配方 id 形如 &6pollution:industrial_infusion_recipes/industrial_infusion/thaumic/<命名空间>/<原路径>&r，可用 JEI 直接搜。',
               '模板 2／3／4 的工业孪生不需要不稳定度，但要素流体一分不少。'],
         check='已用工业注魔量产至少一种白名单产物', deps=['industrial_intro'], xy=(4, 6)),

    dict(key='industrial_limit', title='不转什么：附魔、法杖、生物注魔', icon='thaumcraft:infusion_altar',
         desc=['附魔、法杖装配、生物注魔（活体注魔）一律不转——它们不是「产物 + 要素」的简单结构。',
               '带 NBT 的输入或输出跳过；未映射要素、或流体种类超过 8 的配方也跳过并计数。',
               '转换日志在启动时打印：「registered N industrial infusion recipes from TC JSONs」。N 变小说明有配方被跳过，先看日志再改白名单。',
               '想加产物：改配置项 EXTRA_THAUMIC_INDUSTRIAL_WHITELIST，不要动默认白名单。'],
         check='已了解转换的边界', deps=['industrial_batch'], xy=(6, 6)),

    dict(key='aspect_value', title='源质估值：1 点 = 144mB = 1 元素粉', icon='pollution:infused_exchange',
         items=['pollution:infused_exchange'],
         desc=['六原始要素的闭环规则：&61 点源质 = 144mB 对应流体 = 1 个本模组原始元素粉／宝石中的源质&r。',
               '转换矩阵每 10t 最多转 1 点，不额外扣 EU；高压釜返造保持原配方 ID 与 144mB 投入，但输出改为 Pollution 自身元素宝石。',
               '为什么不再产出 TC 晶簇：晶簇放置／破坏可得多个碎片，会绕过 1 点赋值，形成放大链。',
               '这条规则只覆盖已枚举的六原始闭环，不声称穷尽整包所有跨 mod 转换。'],
         check='已理解源质与流体的换算', deps=['intro'], ext=[EXT_ESSENTIA_FURNACE], xy=(2, 12)),

    dict(key='aspect_whitelist', title='数据包：材料要素表放在哪', icon='thaumcraft:thaumonomicon',
         desc=['材料要素来自数据包 &6data/pollution/thaumcraft/object_aspects/*.json&r，当前 5,965 条 direct 定义。',
               '路径必须在&e自己 mod 的命名空间&r下：TC4R 自己用 data/thaumcraft/thaumcraft/object_aspects/，你放 data/thaumcraft/object_aspects/ 会被&c静默忽略、不报错&r。',
               '条件 schema 用 Forge 的 &6{"type":"forge:mod_loaded","modid":...}&r；NeoForge 的 {"condition":...,"values":[...]} 会抛 JsonSyntaxException 并崩启动。',
               '要素表只影响「扫视」与炼金分解的取值，不改物品本身。'],
         check='已确认要素表的路径与条件写法', deps=['aspect_value'], xy=(4, 12)),

    dict(key='smelter', title='两种源质炉：按实际接受量记账', icon='pollution:essence_smelter',
         desc=['TC 源质炉按容器&e实际接受量&r扣减；GT 源质炉遍历输出仓，余量按 mB 保存，17mB 这类零头不截断。',
               '满罐／满输出仓时保留 pending：不继续消费下一批，也不为等输出反复扣燃料。',
               '结构失效、仓缺失时&e暂停&r而不是清空已消耗原料的批次；控制器保存／恢复批次进度。',
               '别把源质炉当成无限缓冲：产出上限由罐与仓的容量决定，规划产线时按最慢的一环算。'],
         check='已确认源质炉的记账行为', deps=['aspect_value'], ext=[EXT_ESSENTIA_FURNACE], xy=(6, 12)),
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


def quest_ids():
    """全库"任务" id，不含 task/reward id。

    external_ids() 收的是任意 16-hex，把某条奖励的 id 当成前置也能通过校验，
    结果是依赖悬空、游戏内前置永远不满足（35F501BCCBED6EC4 那次就是）。
    这里按 quests: [] 的顶层块重新收一遍，只取每个块的第一个 id。"""
    result = set()
    for path in sorted(QUESTS.rglob('*.snbt')):
        if path == OUTPUT:
            continue
        text = path.read_text(encoding='utf-8-sig')
        m = re.search(r'\bquests:\s*\[', text)
        if not m:
            continue
        i, depth, start = m.end(), 1, None
        while i < len(text):
            c = text[i]
            if c == '{':
                if depth == 1:
                    start = i
                depth += 1
            elif c == '}':
                depth -= 1
                if depth == 1 and start is not None:
                    block = re.search(r'\bid:\s*"([0-9A-F]{16})"', text[start:i + 1])
                    if block:
                        result.add(block.group(1))
                    start = None
            elif c == ']' and depth == 1:
                break
            i += 1
    return result


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
    doc = dict(default_hide_dependency_lines=False, default_quest_shape='square', filename='thaumic_industry',
               group=GROUP, icon='pollution:industrial_infusion', id=ids['chapter'], order_index=ORDER,
               quest_links=[], quests=[], title='&6&l神秘工业&r · 奥术电路与工业注魔')
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
                raise ValueError('Item not in the live-verified registry list: ' + item)
    return (dump(doc) + '\n').encode('utf-8')


def render():
    bad_ext = EXT_DEPS - quest_ids()
    assert not bad_ext, '外部前置不是任务 id（多半抄成了 task/reward id）: ' + str(sorted(bad_ext))
    ids = allocate(get_keys(), external_ids())
    group_doc = (QUESTS / 'chapter_groups.snbt').read_text(encoding='utf-8-sig')
    if GROUP not in re.findall(r'id:\s*"([0-9A-F]{16})"', group_doc):
        raise ValueError('Thaumic industry chapter group missing from chapter_groups.snbt')
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
