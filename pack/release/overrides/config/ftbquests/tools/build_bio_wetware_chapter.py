#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the bio / wetware FTB Quests chapter (Pollution x GTMFO x ThaumicHorizons x GT).

Follows build_trade_chapter.py: stable business key -> persisted 16-hex ID map,
deterministic render, fail-closed validation. Text is inline Chinese.

Chapter hangs in the tech group (4A46A5E1358A80A6), takes order 24 (the first
free slot in that group after thaumic_addons=22 / ae2_addons=23).

External deps (all resolved 2026-11-04 against the live chapter set):
  690E013DFCB060ED  zpm__zero_point_module : 无菌洁净室
  33A1FF5C31EAF716  zpm__zero_point_module : 干细胞
  359121584E056022  zpm__zero_point_module : 最佳UV电路!
  3B49BD004F38E1A2  uv__ultimate_voltage   : 湿件处理器主机 - UHV电路
  4F9A048DEAAA894C  pollution              : 两种熔炉：物品→源质 / 流体
  493D9465A1F00304  thaumic_addons         : 躯体脑
  (769ADA236C630FC7 pollution 工业化配方 is reserved for the thaumic-industry
   chapter, not used here.)

Every icon/item below was checked with ForgeRegistries.ITEMS.getValue on the
live 1.20.1 test server on 2026-11-04 (41 ids, all present). Every recipe id
quoted in the descriptions was dumped from the server's RecipeManager in the
same session (70 matching GT recipes).
"""
from pathlib import Path
import argparse
import hashlib
import json
import re

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parents[2]
QUESTS = ROOT / 'config/ftbquests/quests'
OUTPUT = QUESTS / 'chapters/bio_wetware.snbt'
MAP = TOOLS / 'bio_wetware_ids.json'
GROUP = '4A46A5E1358A80A6'
SALT = 'society-bio-wetware-chapter-v1'
ORDER = 24

EXT_STERILE = '690E013DFCB060ED'      # zpm: 无菌洁净室
EXT_STEM_CELLS = '33A1FF5C31EAF716'   # zpm: 干细胞
EXT_UV_CIRCUIT = '359121584E056022'   # zpm: 最佳UV电路!
EXT_UHV_MAINFRAME = '3B49BD004F38E1A2'  # uv: 湿件处理器主机 - UHV电路
EXT_ESSENTIA_FURNACE = '4F9A048DEAAA894C'  # pollution: 两种熔炉
EXT_SOMATIC_BRAIN = '493D9465A1F00304'  # thaumic_addons: 躯体脑
EXT_DEPS = {EXT_STERILE, EXT_STEM_CELLS, EXT_UV_CIRCUIT, EXT_UHV_MAINFRAME,
            EXT_ESSENTIA_FURNACE, EXT_SOMATIC_BRAIN}

VERIFIED_ITEMS = {
    'pollution:primitive_meat', 'pollution:rat_brain', 'pollution:ips_human_brain',
    'pollution:infused_exchange',
    'gtceu:meat_dust', 'gtceu:raw_growth_medium_bucket', 'gtceu:sterilized_growth_medium_bucket',
    'gtceu:petri_dish', 'gtceu:stem_cells', 'gtceu:wetware_circuit_board',
    'gtceu:neuro_processing_unit', 'gtceu:wetware_processor_computer',
    'gtceu:wetware_processor_mainframe', 'gtceu:stearin_bucket', 'gtceu:biomass_bucket',
    'gtceu:gelatin_solution_bucket',
    'gtmfo:scrap_meat', 'gtmfo:animal_fat', 'gtmfo:gelatin',
    'isorropia:ore_pig_spawn_egg', 'isorropia:somatic_brain',
}

Q = [
    dict(key='intro', title='生物湿件：从腐肉到芯片', icon='pollution:primitive_meat',
         desc=['GT 的湿件（Wetware）电路是 UV 时代的主力。本包在原版 GT 路线之外，多给了一条&6生物支线&r：用神秘与污染的生物材料，换一条并行的原料来源。',
               '本章只讲&a生物侧&r：血肉、鼠脑、培养基、iPS 脑、干细胞，以及废肉／污泥／明胶的回收。',
               '原版 GT 湿件链（洁净室、湿件基板、NPU、处理器）在&6ZPM&r章节；源质与工业注魔在&6神秘工业&r章节。',
               '三条支线：① 血肉→肉粉→培养基；② 鼠脑→iPS 脑→催化干细胞；③ 屠宰废料→脂肪／明胶／生物质。',
               '纯 GT 玩家可以完全不碰这条线——原配方一个都没删。跨线玩家付出研究与培养成本，换原料来源与吞吐。'],
         check='已了解生物支线的三条主线', deps=[], xy=(0, 0)),

    dict(key='flesh', title='原始血肉：腐肉不是垃圾', icon='pollution:primitive_meat',
         items=['pollution:primitive_meat'],
         desc=['Pollution 的化学反应釜：&7腐肉 4 + 生物质 500mB → 原始血肉 2&r，30 EU/t、100t。',
               '生物质来自 GT 的发酵／离心链，LV 就能起步，所以这条线从蒸汽时代的尾巴就可以开始攒。',
               '原始血肉是鼠脑、线粒能源体、冷冻器等生物配方的共同上游——先囤一批。',
               '注意：这是&e并行分支&r，不是一条连续进化链。鼠脑与线粒能源体都从原始血肉分叉，互不依赖。'],
         check='已产出第一批原始血肉', deps=['intro'], xy=(2, 0)),

    dict(key='meat_dust', title='血肉→肉粉：生物桥的第一环', icon='gtceu:meat_dust',
         items=['gtceu:meat_dust'],
         desc=['新增配方（研磨机）：&71 原始血肉 → 1 肉粉&r，2 EU/t、102t。',
               '原 GT 肉粉来自生肉／熟肉研磨，生物桥不改原配方，只是多一个来源。',
               '肉粉是&6原始生长培养基&r的四类粉之一，也是 GTMFO 废肉线的产物。',
               '配方 ID：society:macerator/bio/primitive_meat_to_meat_dust。'],
         check='已研磨出肉粉', deps=['flesh'], xy=(4, 0)),

    dict(key='rat_brain', title='鼠脑：僵尸脑的第二次生命', icon='pollution:rat_brain',
         items=['pollution:rat_brain'],
         desc=['Pollution 化学反应釜：&7僵尸脑 1 + 原始血肉 1 + 无菌生长培养基 250mB → 鼠脑 1&r，120 EU/t、200t。',
               '僵尸脑靠击杀掉落：普通僵尸 10%，每级抢夺 +10%；脑僵尸 50%，每级 +10%。',
               '配方本身不要求洁净室，但它吃&e无菌培养基&r——上游的灭菌门槛照样卡着。低 EU/t 不等于低科技整链。',
               '鼠脑是 iPS 脑的两种物品输入之一；稳定器、冷冻器也是从它分叉。'],
         check='已做出第一个鼠脑', deps=['flesh'], xy=(6, 0)),

    dict(key='medium', title='原始生长培养基：肉粉的用处', icon='gtceu:raw_growth_medium_bucket',
         items=['gtceu:raw_growth_medium_bucket'],
         desc=['GT 搅拌机：&7肉粉 4 + 盐粉 4 + 钙粉 4 + 琼脂粉 4 + 诱变剂 4000mB → 原始培养基 4000mB&r，7680 EU/t、1200t，&c无菌洁净室&r。',
               '四类粉都可自动化：肉粉来自生物桥或废肉，盐／钙来自矿物处理，琼脂来自海带链。',
               '诱变剂由细菌→细菌浆液→富集浆液这条上游链产出，不是凭空出现的耗材。',
               '机器条件是&cSTERILE&r，普通洁净室跑不了这条配方。'],
         check='已合成第一批原始培养基', deps=['meat_dust'], xy=(8, 0)),

    dict(key='sterilized', title='灭菌：原始→无菌培养基', icon='gtceu:sterilized_growth_medium_bucket',
         items=['gtceu:sterilized_growth_medium_bucket'],
         desc=['GT 流体加热机：&7电路 1 + 原始培养基 100mB → 无菌培养基 100mB&r，7680 EU/t、20t，&c无菌洁净室&r。',
               '流体 ID 是 &6gtceu:sterilized_growth_medium&r；&esterile_growth_medium&r 只是配方名，不是流体 ID，脚本里别混用。',
               '整条生物线的瓶颈就在这里：无菌培养基是干细胞、iPS 脑、湿件基板的共同耗材。',
               'GT 的两种洁净室条件不能互换：&cSTERILE&r 与&eCLEANROOM&r 是不同条件，一间房包办不了所有配方。'],
         check='已产出无菌培养基', deps=['medium'], xy=(10, 0)),

    dict(key='petri', title='培养皿：PTFE 还是 PBI', icon='gtceu:petri_dish',
         items=['gtceu:petri_dish'],
         desc=['流体固化机（不消耗圆柱模具）：&7PTFE 36mB → 培养皿 1&r，480 EU/t、160t；或 &7PBI 18mB → 培养皿 2&r，480 EU/t、40t。',
               'PBI 路线产量翻倍、时间只有四分之一，是中期以后的正确选择。',
               '培养皿用于湿件基板，也是生物线的通用器皿——多备一些。'],
         check='已做出培养皿', deps=['sterilized'], xy=(12, 0)),

    dict(key='stem_gt', title='原版干细胞：锇铱 + 细菌', icon='gtceu:stem_cells',
         items=['gtceu:stem_cells'],
         desc=['GT 化学反应釜：&7锇铱粉 1 + 细菌 500mB + 无菌培养基 500mB → 干细胞 32 + 细菌浆液 500mB&r，30720 EU/t、300t，&c无菌洁净室&r。',
               '这是原版路线，不改动；下一节的催化配方是它的&e替代&r，不是升级。',
               '细菌浆液可以回流到细菌／富集浆液链，别当废液倒掉。',
               '配方 ID：gtceu:chemical_reactor/stem_cells（大化反派生 gtceu:large_chemical_reactor/stem_cells）。'],
         check='已用原版配方产出干细胞', deps=['sterilized'], ext=[EXT_STEM_CELLS], xy=(6, -6)),

    dict(key='ips_first', title='首件 iPS 脑：绕开自举循环', icon='pollution:ips_human_brain',
         items=['pollution:ips_human_brain'],
         desc=['原版 iPS 脑走魔导组装机（1920 EU/t、800t），但魔导组装机的控制组件本身就要 iPS 脑——首件死循环。',
               '新增起步配方（化学反应釜）：&72 鼠脑 + 脑缸 1 + 注入·人类 500mB + 注入·生命 1000mB + 无菌培养基 1000mB → iPS 脑 1&r。',
               '代价是更高电压与更长工时：&e30720 EU/t、1600t、无菌洁净室&r（原方 800t）。原方保留，作为批量生产的低成本路线。',
               '注入流体来自 Pollution 的转换矩阵：源质 → 要素流体。见本章「源质→要素流体」。',
               '配方 ID：society:chemical_reactor/bio/ips_brain_bootstrap。'],
         check='已做出第一枚 iPS 脑', deps=['rat_brain', 'sterilized'], ext=[EXT_STERILE], xy=(8, -6)),

    dict(key='ips_stem', title='催化干细胞：把 iPS 脑当培养器官', icon='gtceu:stem_cells',
         items=['gtceu:stem_cells'],
         desc=['新增配方（化学反应釜）：&74 锇铱小粉 + 不消耗的 iPS 脑 1 + 细菌 500mB + 无菌培养基 500mB → 干细胞 32 + 细菌浆液 500mB&r。',
               '240t，比原方 300t 少 20% 时间、同条件理论吞吐 +25%；iPS 脑&e不消耗&r，是培养辅助件而不是每批耗材。',
               '为什么用&e小粉&r：4 小粉 = 1 完整粉，但输入形态与原方的整粉不同，避免 JEI 里两方互相盖住、放脑时总选原方。',
               '为什么脑不消耗：造一枚 iPS 脑要 1500mB 培养基与 800t 起步工时，按批消耗换 60t 提速永远回不了本。',
               '配方 ID：society:chemical_reactor/bio/ips_assisted_stem_cells。'],
         check='已用催化配方产出干细胞', deps=['ips_first', 'stem_gt'], xy=(10, -6)),

    dict(key='wetware_board', title='湿件基板：进入电路链', icon='gtceu:wetware_circuit_board',
         items=['gtceu:wetware_circuit_board'],
         desc=['GT 电路组装机：&7多层纤维板 16 + 培养皿 1 + LuV 泵 1 + IV 传感器 1 + IV 电路 1 + 铌钛箔 16 + 无菌培养基 4000mB → 湿件基板 16&r，30720 EU/t、1200t。',
               '条件是&e普通洁净室&r，不是无菌房——两种条件不能互相顶替。',
               '从这里开始回到 GT 原版湿件链，后续任务在&6ZPM&r章节展开。',
               '配方 ID：gtceu:circuit_assembler/wetware_board。'],
         check='已做出湿件基板', deps=['ips_stem', 'petri'], xy=(12, -6)),

    dict(key='npu', title='神经处理单元：湿件的心脏', icon='gtceu:neuro_processing_unit',
         items=['gtceu:neuro_processing_unit'],
         desc=['GT 电路组装机：&7印刷湿件板 1 + 干细胞 16 + PBI 小流体管 8 + 铱金板 8 + 硅橡胶箔 16 + HSS-E 螺栓 8 + 无菌培养基 250mB → NPU 1&r。',
               '&e80000 EU/t、600t、普通洁净室&r——ZPM 级供电才能长时间跑。',
               '干细胞是这里的硬瓶颈：一批 16 枚。生物支线的意义就是把这条供给做成可自动化。'],
         check='已做出神经处理单元', deps=['wetware_board'], xy=(14, -6)),

    dict(key='uv_end', title='UV 湿件：支线的终点', icon='gtceu:wetware_processor_computer',
         items=['gtceu:wetware_processor_computer'],
         desc=['湿件处理器（LuV）→ 集群（ZPM）→ 超级计算机（UV），全部走 GT 原版流水线。',
               '超级计算机：装配线、38400 EU/t、400t，研究 16 CWU/t。配方 ID：gtceu:assembly_line/wetware_super_computer_uv。',
               '生物支线到 UV 为止：本包不规划 UEV～MAX 的新电路树、机器梯级或任务。',
               '「电路标签档位」与「制造功率」是两件事，别把 UV 标签当成 UV 供电就够。'],
         check='已做出 UV 级湿件电路', deps=['npu'], ext=[EXT_UV_CIRCUIT], xy=(16, -6)),

    dict(key='uhv_opt', title='选修：UHV 湿件主机', icon='gtceu:wetware_processor_mainframe',
         items=['gtceu:wetware_processor_mainframe'],
         desc=['湿件主机是 UHV 标签产物：装配线、300000 EU/t、2000t，研究 96 CWU/t。配方 ID：gtceu:assembly_line/wetware_mainframe_uhv。',
               '它的制造功率仍落在 UV 供电范围内，所以可以当 UV 能力的&e选修收尾&r；但它不是一条完整 UHV 时代的开始。',
               '前置研究、材料与供电请按原配方逐项核对，本章不承诺全部可达。'],
         check='已做出湿件主机', deps=['uv_end'], ext=[EXT_UHV_MAINFRAME], xy=(18, -6)),

    dict(key='scrap_meat', title='废肉：屠宰线的副产', icon='gtmfo:scrap_meat',
         items=['gtmfo:scrap_meat'],
         desc=['GTMFO 的 &6废肉（Scrap Meat）&r是屠宰与食品加工的副产：人们通常不吃的那部分。',
               '它本身不能直接吃，但脂肪、明胶、生物质都能从它身上榨出来。',
               '先攒一箱，后面三条回收线都要用。'],
         check='已获得废肉', deps=['intro'], xy=(2, 6)),

    dict(key='scrap_mac', title='废肉研磨：脂肪与骨粉', icon='gtmfo:animal_fat',
         items=['gtmfo:animal_fat'],
         desc=['研磨机：&7废肉 8 → 肉粉 10 + 小撮骨粉 16 + 动物脂肪 10&r，另有 50% 概率再出 4 脂肪。',
               '20 EU/t、400t，是本章最便宜的回收配方——一台 LV 研磨机就能吃下整条屠宰线。',
               '动物脂肪可以提取硬脂酸，走生物柴油支线。配方 ID：gtmfo:macerator/scrap_meat_maceration。'],
         check='已研磨废肉得到脂肪', deps=['scrap_meat'], xy=(4, 6)),

    dict(key='scrap_extract', title='大化反：废肉的工业级拆解', icon='gtceu:stearin_bucket',
         items=['gtceu:stearin_bucket'],
         desc=['大化学反应釜：&7废肉 32 + 甲醇 4000mB + 三氯甲烷 4000mB → 肉粉 32 + 骨粉 20 + 硬脂酸 3500mB + 污泥 16000mB + 氯 12000mB&r。',
               '256 EU/t、1000t。肉粉产出与投入 1:1，真正的价值在硬脂酸、污泥与回收的氯。',
               '氯可以回氯化线，甲醇来自木材／沼气——这条线是闭环的，不是一次性消耗。',
               '配方 ID：gtmfo:large_chemical_reactor/scrap_meat_extract。'],
         check='已用大化反拆解废肉', deps=['scrap_mac'], xy=(6, 6)),

    dict(key='sludge', title='污泥→生物质：把废液变原料', icon='gtceu:biomass_bucket',
         items=['gtceu:biomass_bucket'],
         desc=['大化学反应釜：&7污泥 24000mB + 细菌 1000mB + 方解石粉 3&r（碳网 + 电路 2 不消耗）→ &7生物质 10000mB + 水 14000mB + 二氧化硫 8000mB + 甲烷 8000mB&r。',
               '30 EU/t、800t，几乎不要电；瓶颈是污泥产量与细菌供给。',
               '生物质回流到原始血肉配方，等于把屠宰废料重新变成生物原料。',
               '配方 ID：gtmfo:large_chemical_reactor/sludge_to_biomass。'],
         check='已把污泥转回生物质', deps=['scrap_extract'], xy=(8, 6)),

    dict(key='gelatin', title='明胶：七种原料，一台提取机', icon='gtmfo:gelatin',
         items=['gtmfo:gelatin'],
         desc=['提取机：&7骨／皮革／猪排／牛排／鸡肉／兔肉／羊肉&r 任选其一 → 明胶 1，120 EU/t、100t。',
               '七个配方 ID 是 gtmfo:extractor/gelatin_from_<原料>，同一台机器轮着跑即可。',
               '这是&e食品级&r明胶，不要拿它冒充 GT 工业明胶／琼脂。'],
         check='已提取出明胶', deps=['scrap_meat'], xy=(10, 6)),

    dict(key='gelatin_recovery', title='明胶返造：别把水当成免费的', icon='gtceu:gelatin_solution_bucket',
         items=['gtceu:gelatin_solution_bucket'],
         desc=['新增配方（脱水机）：&7明胶溶液 1000mB → 明胶 8&r，480 EU/t、400t。',
               '正向是 8 明胶 + 1000mB 水 → 1000mB 溶液；返造最多还原同样的 8 个固体，水丢了，还要付电费。',
               '所以这是&e有损回收&r，不是把溶液变多的漏洞。',
               '配方 ID：society:dehydrator/bio/food_gelatin_recovery。'],
         check='已用脱水机回收明胶', deps=['gelatin'], xy=(12, 6)),

    dict(key='ore_pig', title='矿猪：白名单只有七种金属', icon='isorropia:ore_pig_spawn_egg',
         items=['isorropia:ore_pig_spawn_egg'],
         desc=['神秘视界的矿猪吃掉落物形式的圆石，每块累加 1～15 进度，满 100 产出一份矿物。',
               '本包把产物池收紧为七种：&6铜、金、铁、铅、银、锡、锌&r。',
               '白名单外的高阶材料不会出现；缺对应矿粒时&e不回退整份粉&r（ore_pig_dust_fallback = false）。',
               '它不是自动矿物倍产：吞吐取决于进食频率与目标选择，按副产而不是主产规划。'],
         check='已确认矿猪产物池', deps=['intro'], xy=(2, 12)),

    dict(key='somatic', title='躯体脑：Curios 头部饰品', icon='isorropia:somatic_brain',
         items=['isorropia:somatic_brain'],
         desc=['躯体脑是&e装备位饰品&r，不是生产机器：它没有「产出经验／知识／神经组织」的行为。',
               '本包装有禁忌魔法，活体脑分支研究 ID 是大小写敏感的 &6isorropia:somaticbrainFm&r。',
               '注魔配方消耗脑缸、铁锭、漏斗、僵尸脑 2，以及认知 150、贪婪 100、&6forbidden_magic:invidia&r 20——把脑缸上游算进去共需 3 个僵尸脑。',
               '研究完成后可重复制造，但「可重复」不等于「可自动化吞吐」。'],
         check='已做出躯体脑', deps=['intro'], ext=[EXT_SOMATIC_BRAIN], xy=(6, 12)),

    dict(key='essentia', title='源质→要素流体：生物配方的供料口', icon='pollution:infused_exchange',
         items=['pollution:infused_exchange'],
         desc=['iPS 脑要 &6注入·人类（infused_human）&r 与 &6注入·生命（infused_life）&r，它们不是矿物流体，而是由源质转换来的。',
               'Pollution 的&6转换矩阵&r把 1 点源质转成 144mB 对应要素流体，每 10t 最多 1 点，不额外扣 EU。',
               '上游供料是 Pollution 的两种源质炉：物品→源质、流体→源质（见「污染」章节）。',
               '别把注入流体当成守恒等价物：六原始要素在本包已统一为 1 点 = 144mB = 1 个本模组元素粉／宝石。'],
         check='已把源质转成要素流体', deps=['intro'], ext=[EXT_ESSENTIA_FURNACE], xy=(2, 18)),
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
    doc = dict(default_hide_dependency_lines=False, default_quest_shape='square', filename='bio_wetware',
               group=GROUP, icon='pollution:ips_human_brain', id=ids['chapter'], order_index=ORDER,
               quest_links=[], quests=[], title='&2&l生物&r · 血肉与湿件')
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
    ids = allocate(get_keys(), external_ids())
    group_doc = (QUESTS / 'chapter_groups.snbt').read_text(encoding='utf-8-sig')
    if GROUP not in re.findall(r'id:\s*"([0-9A-F]{16})"', group_doc):
        raise ValueError('Bio chapter group missing from chapter_groups.snbt')
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
