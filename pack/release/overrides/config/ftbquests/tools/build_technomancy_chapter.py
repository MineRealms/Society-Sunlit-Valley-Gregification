#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Technomancy FTBQ 2001.4.17 chapter. Python 3.10+, standard library only.

Run --check for read-only validation; run without arguments to publish after
validation. Only technomancy.snbt and technomancy_ids.json are generated.
Semantic keys, persisted IDs, order_index and prior output SHA protect published
work. Mirrors build_pollution_chapter.py (same group: 神秘科技支线).
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
OUTPUT = QUESTS / 'chapters/technomancy.snbt'
MAP = TOOLS / 'technomancy_ids.json'
SOURCE = Path(r'H:\MinecraftMods\Technomancy-1.20.1')
JAVA = SOURCE / 'src/main/java/theflogat/technomancy'
JAR = SOURCE / 'build/libs/technom-1.20.1-0.1.0-dev.jar'
GROUP = '4A46A5E1358A80A6'
SALT = 'technomancy'
MOD = 'technom'


def digest(data):
    return hashlib.sha256(data).hexdigest()


class SnbtParser:
    """Recursive parser for FTB relaxed SNBT: optional commas, comments, suffixes.

    Strings are tokenized before structure; duplicate keys and trailing garbage
    fail. Typed arrays and single-quoted strings are supported for existing files.
    """
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
        # SNBT permits escaped quote/backslash; preserve literal Unicode.
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


def quest(key, title, icon, text, items=(), evidence=(), check=None):
    Q.append(dict(key=key, title=title, icon=MOD + ':' + icon,
                  description=text.split('\n'), items=list(items), evidence=list(evidence), check=check))


def p(*names):
    return tuple(MOD + ':' + x for x in names)


def content():
    # ---- A · 入门与能源 ----
    quest('intro', 'A · 神秘科技：精华与能量的桥梁', 'ritual_tome',
          'Technomancy（神秘科技）把神秘时代的源质/灵气与科技能量（FE/EU）连接起来：源质发电机、能量凝聚器等把精华转成电力，节点机器则读取世界中的灵气节点。\n本章六区：A 入门与能源，B 精华加工，C 节点与法杖，D 仪式材料，E 存在网络，F 深层 TC 与植物魔法。任务连线表示教学顺序，不是完整配方树。\n前置：神秘时代研究（神秘锭/注魔）、GT 起步（真空管/基础电路）。本实例已把它卡在 LV 阶段之后。\n物品目标只检查持有，不消耗材料，也不证明机器已成型；运行类请完成正文操作后勾选。',
          evidence=(), check='已阅读六区导航与前置要求')
    quest('tome', '仪式书与源质学入门', 'ritual_tome',
          '仪式书是本模组的索引：翻它查看仪式与机器条目。原版用书+荧石+黑染料即可；本实例追加了 GT 真空管，需先进入 GT 阶段。\n仪式系统需要先完成神秘时代的注魔与研究，五色水晶与催化器是后续仪式的核心材料。\n真正开工前先建一颗稳定的源质来源：空罐接管从灵气罐/炼金炉收集，或用本模组的分解路线取物体要素。',
          p('ritual_tome'), ())
    quest('qjar', '量子罐：十倍容量的源质容器', 'quantum_jar',
          '量子罐单方面大容量存一种源质（十只符文罐的容量）。用带要素的容器设过滤，配源质管道进出；顶面接受输入。\n量化玻璃与中子化金属是它的门槛，分别来自奥术合成与注魔/坩埚路线。\n它向相邻运输方块提供吸气，是精华加工线的基础缓冲；先做成一只再扩产。',
          p('quantum_jar'), ())
    quest('dynamo', '源质发电机：精华 -> 电力', 'essentia_dynamo',
          '源质发电机燃烧源质产出电能（FE/EU），是「精华闭环」的产电端。接好能量输出面与源质输入面，按 JEI 查看可接受的要素与倍率。\n配一个量子罐作缓冲，避免频繁断料。输出可经本整合包的能量转换接入 GT 电网。\n它是把 TC4 精华转成工业电力的核心，也是 GT/MEK 之外的第三条供电路线。',
          p('essentia_dynamo'), ())
    quest('condenser', '能量凝聚器：注魔机器 -> 电力', 'energy_condenser',
          '能量凝聚器是高级注魔机器，把注魔祭坛的运作/要素凝聚为可用能量。它走暗术注魔路线，需要已成型的神秘时代注魔设施与相应研究。\n放好后按结构提示接入能量输出；与源质发电机配合可平滑供电曲线。\n它是 S1「精华闭环」的收尾，之后进入 S2 核心机器。',
          p('energy_condenser'), ())
    quest('qglass', '量化玻璃：量子结构基材', 'quantized_glass',
          '量化玻璃来自奥术合成（4 玻璃 -> 4 量化玻璃），需要研究 QUANTUMJARS，并支付 ordo/ignis 各 5 点灵气。\n它是量子罐等量子结构件的基材，先备一批再谈扩产。\n研究在神秘时代的神秘表推进，灵气由法杖/祭坛提供。',
          p('quantized_glass'), ())
    quest('ndynamo', '节点发电机：灵气节点 -> 电力', 'node_dynamo',
          '节点发电机读取世界中（或封装后）的灵气节点，把节点的 vis 转成电力；节点属性越高产出越强。\n它把「节点」这一神秘时代核心资源接入电力体系，是 A 与 C 区的分界。\n先有稳定节点来源，再谈规模化发电；节点工程见 C 区。',
          p('node_dynamo'), ())

    # ---- B · 精华加工 ----
    quest('coil', '源质线圈：抽取与传输', 'essentia_coil',
          '源质线圈从相邻容器/管道抽取指定源质并推送出去，是精华物流的泵。用耦合器设定过滤目标。\n它参与量子罐、储库与融合器的供料，是 B 区的中枢部件。\n按 JEI 准备中子化金属与神秘锭，先把一只线圈接到量子罐上跑通。',
          p('essentia_coil'), ())
    quest('coupler', '线圈耦合器：绑定过滤', 'coil_coupler',
          '线圈耦合器用于把过滤目标绑定到线圈，改变它抽取/推送的要素。\n它是配置工具而非动力件，做一只备用即可。\n绑定后核对线圈朝向与过滤，避免把贵要素抽进错误的罐。',
          p('coil_coupler'), ())
    quest('ecoil', '附魔线圈：基础合成件', 'enchanted_coil',
          '附魔线圈 = 红石 + 神秘锭，是多种机器的通用合成件。\n本实例额外加了 GT 组装机量产配方（见 bridgeTechnomGt.js），规模化后改走 GT 自动产线，不必手工堆。\n它是贯穿 S2/S4 的基础件，前期先备若干。',
          p('enchanted_coil'), ())
    quest('fusor', '源质融合器：合成复合要素', 'essentia_fusor',
          '源质融合器按表把两种基本要素合成为复合要素，是缺料时的自造途径（也可从世界直接采集）。\n它走注魔路线，需要已成型的神秘时代注魔设施。\n先做一只，用于补齐稀有要素，而不是拿来大批量替代采集。',
          p('essentia_fusor'), ())
    quest('reservoir', '源质储库：大批量缓冲', 'essentia_reservoir',
          '源质储库是大容量源质缓冲，用于平抑产/耗波动。\n它走注魔路线；与量子罐配合构成精华仓储层。\n建成后让线圈把多余要素汇入储库，再向发电机与加工机供料。',
          p('essentia_reservoir'), ())
    quest('decon', '高级分解台：物体 -> 要素', 'adv_decon_table',
          '高级分解台读取物品的要素并分解，是对「扫描/取要素」的加速途径，依赖 TC4R 的要素查询接口。\n它走注魔路线，需要相应研究。\n用它把多余物品稳定转成源质，喂给发电机或融合器。',
          p('adv_decon_table'), ())
    quest('consumer', '邪术吞噬器：危险的分解源', 'eldritch_consumer',
          '邪术吞噬器是重型分解/吞噬装置，产出可观但有代价（面板动画与工作状态见 Jade 提示）。\n它走注魔路线，属于 B 区的收尾机器。\n先小批量试机，确认产出与副作用，再决定是否纳入主产线。',
          p('eldritch_consumer'), ())

    # ---- C · 节点与法杖 ----
    quest('nfab', '节点制造器：人造灵气节点', 'node_fabricator',
          '节点制造器成对使用并驱动一段仪式，在指定位置生成一颗灵气节点；配套外壳用于成型。\n它让节点不再依赖自然生成，是规模化灵气/电力的起点，也最吃中子化金属。\n先备齐中子化材料与法杖，再按仪式步骤放置。',
          p('node_fabricator'), ())
    quest('ptc', 'TC 处理器：魔法电路件', 'processor_tc',
          'TC 处理器是神秘科技侧的电路部件，由红石、油脂块、中子化齿轮、神秘锭与附魔线圈合成。\n它相当于把 GT 电路体系延伸到魔法侧，是高级机器的门槛。\n本实例已在 GT 侧加了组装量产路线，规模生产改走 GT。',
          p('processor_tc'), ())
    quest('nmetal', '中子化金属：坩埚路线', 'neutronized_metal',
          '中子化金属是多种机器的骨架材料，走神秘时代坩埚（crucible）路线，需相应研究与要素。\n它是整个 S2 的硬门槛，先囤一批再谈机器。\n批量前先算好要素来源，避免坩埚临时缺料。',
          p('neutronized_metal'), ())
    quest('ngear', '中子化齿轮', 'neutronized_gear',
          '中子化齿轮 = 中子化金属 + 铁锭，是机器传动件。\n本实例提供 GT 组装量产配方。\n它与附魔线圈共同构成机器的骨架级材料。',
          p('neutronized_gear'), ())
    quest('wand', '充能法杖芯：电力法杖', 'energized_wand_core',
          '充能法杖芯把电能引入法杖体系，是神秘科技特色装备的起点，走注魔路线。\n充能后可执行魔法操作而不必反复充灵气，是本模组对传统法杖的现代化。\n先做一支体验，再考虑批量。',
          p('energized_wand_core'), ())
    quest('tcore', '神秘术士芯：终局法杖', 'technoturge_core',
          '神秘术士芯是顶阶法杖核心，走注魔路线；本实例额外要求 GT 高级电路组装（见 bridgeTechnomGt.js），把它卡在 HV 之后。\n它代表神秘科技与工业的融合顶点。\n先备好充能法杖芯与高级电路。',
          p('technoturge_core'), ())
    quest('potency', '效力宝石：增幅件', 'potency_gem',
          '效力宝石由红石、石英与金锭合成，是机器/法杖的增幅材料（具体用途见 JEI 各配方）。\n它便宜但用途广，日常备货即可。\nC 区以此收尾，转入仪式系统。',
          p('potency_gem'), ())

    # ---- D · 仪式材料 ----
    quest('basalt', '玄武岩：仪式基座', 'basalt',
          '玄武岩是仪式结构的基础方块，用于搭建仪式平台。\n先备一批，仪式多为 3x3 或更大结构。\n它是 D 区仪式的第一块料。',
          p('basalt'), ())
    quest('crystal', '五色水晶：仪式核心', 'crystal_light',
          '五色水晶（光/暗/火/地/水）是仪式与存在网络的核心构件，由荧石粉 + 对应染料合成。\n本实例把荧石粉换成神秘锭，使其卡在神秘时代之后。\n五种各备若干，多数仪式按颜色取用。',
          p('crystal_light', 'crystal_dark', 'crystal_fire', 'crystal_earth', 'crystal_water'), ())
    quest('catalyst', '五催化器：仪式触媒', 'catalyst_light',
          '五催化器（光/暗/火/地/水）是仪式的触媒，原以金块为中心 + 染料 + 材料。\n本实例把金块换成 GT 基础电路，对齐 LV 阶段。\n与五色水晶配套，仪式前先集齐。',
          p('catalyst_light', 'catalyst_dark', 'catalyst_fire', 'catalyst_earth', 'catalyst_water'), ())
    quest('xgem', '存在宝石：Existence 网络起点', 'existence_gem',
          '存在宝石是 Existence 系列机器与网络的核心材料，由金粒 + 绿宝石合成。\n本实例追加 GT 基础电路，使其接在 LV 之后。\n它开启 E 区的存在网络。',
          p('existence_gem'), ())
    quest('focus', '融合焦点：节点塑形', 'fusion_focus',
          '融合焦点用于对着节点塑形/搬迁（潜行右键吸收、空地右键立起），让节点工程更可控。\n它走注魔路线，配合 C 区节点制造器使用。\n先做一只备用。',
          p('fusion_focus'), ())
    quest('pen', '神秘笔：命名与记录', 'pen',
          '神秘笔用于给机器/容器命名或做记录，由铁锭、铁杖端、笔芯与金粒合成。\n它是便利工具，非必需但有帮助。\nD 区以此收尾。',
          p('pen'), ())
    quest('treasure', '宝物：受击与摧毁副作用', 'treasure_fire_gem',
          '三件宝物（火宝石、力量板、金翼）由 S3 仪式与宝物村民带来，携带/受击时有特殊效果；未封印者死亡会摧毁宝物。\n本实例默认开启宝物保护（world.treasures），先了解规则再使用。\n它们连接 E 区的存在网络与玩法奖励。',
          p('treasure_fire_gem'), ())

    # ---- E · Existence 网络 ----
    quest('fountain', '存在之泉：网络能源', 'existence_fountain',
          '存在之泉把周围环境的存在能量采集并送入 Existence 网络，是网络的供能端。\n它走仪式体系，需先备齐五色水晶与催化器。\n建成后接入存在之塔，形成可持续的能量网络。',
          p('existence_fountain'), ())
    quest('burner', '存在燃烧器：网络消耗', 'existence_burner',
          '存在燃烧器把存在能量燃烧转化为具体效果（配合网络节点使用）。\n它是网络的需求侧，与存在之泉平衡。\n按 JEI 与结构提示摆放。',
          p('existence_burner'), ())
    quest('dburner', '动态存在燃烧器', 'existence_dynamic_burner',
          '动态燃烧器是燃烧器的增强变体，接入更强的网络输出。\n它与基础燃烧器共用存在宝石材料。\n确认网络容量足够再升级。',
          p('existence_dynamic_burner'), ())
    quest('pbasic', '基础存在之塔：网络枢纽', 'existence_pylon_basic',
          '存在之塔是 Existence 网络的枢纽，从泉抽取存在能量并分发。\n基础塔是三阶中的入门，配存在宝石与活塞即可。\n先立一座基础塔跑通网络，再升级。',
          p('existence_pylon_basic'), ())
    quest('padv', '高级存在之塔', 'existence_pylon_advanced',
          '高级存在之塔在网络中提供更大的容量与吞吐，由基础塔升级/合成而来。\n它需要前置的三个存在宝石系列材料。\n网络吃紧时升级到高级。',
          p('existence_pylon_advanced'), ())
    quest('pcomplex', '复合存在之塔', 'existence_pylon_complex',
          '复合存在之塔是网络的最高阶枢纽，适合大型存在网络。\n与高级塔同族，材料更重（中子化金属等）。\n按实际网络规模决定是否上复合塔。',
          p('existence_pylon_complex'), ())
    quest('harv', '存在收割与农业网络', 'existence_harvester',
          '存在收割机、作物加速器与封存器把存在网络用于农业与存储：自动收割、催熟、封存物品。\n它们由存在宝石 + 金苹果/金萝卜/铁锄等合成，是存在网络的实用出口。\nE 区以此收尾，转入 F 区的深层神秘科技。',
          p('existence_harvester', 'existence_crop_accelerator', 'existence_sealer'), ())

    # ---- F · 深层 TC 与植物魔法 ----
    quest('lamp', '注魔稳定灯：治理注魔不稳定', 'flux_lamp',
          '注魔稳定灯读取运行中的注魔祭坛不稳定性，并以 ordo/淤泥机制降低它，减少注魔失败与杂质。\n它走注魔路线，是自动化注魔线的稳定器。\n先在真实祭坛旁试装一盏，观察不稳定度变化。',
          p('flux_lamp'), ())
    quest('bellows', '电动风箱：机械加速', 'electric_bellows',
          '电动风箱以电力吹动相邻的奥术炼金炉或原版熔炉，加速其炼制作业（原版熔炉按一充能买 80 tick 推进）。\n它是把 TC4 炉灶接入电力自动化的一环。\n按朝向摆放并供电，先小规模试用。',
          p('electric_bellows'), ())
    quest('morpher', '生态转换器：改写群系', 'biome_morpher',
          '生态转换器右键可把一片区域改写为魔法森林/阴森/污染之地等特殊群系，用于取材或改造基地环境。\n它走奥术路线，需要相应研究。\n使用前确认目标区域，避免误改家园。',
          p('biome_morpher'), ())
    quest('fflower', '花之发电机：Botania 联动', 'flower_dynamo',
          '花之发电机是 Technomancy 的 Botania 选装模块，把 Botania 魔力接入其能量体系。\n四台 Botania 机器在本实例里卡在泰拉钢阶段（见 gateTechnomBotania.js）。\n需先推进植物魔法章节。',
          p('flower_dynamo'), ())
    quest('mfab', '魔力制造机', 'mana_fabricator',
          '魔力制造机把电力/材料转成 Botania 相关的魔力产物，是植物魔法与科技之间的加工桥。\n材料含魔力钻石与魔力钢，门槛较高。\n按 JEI 查看具体配方。',
          p('mana_fabricator'), ())
    quest('mexch', '魔力交换器', 'mana_exchanger',
          '魔力交换器在 Botania 魔力与科技能量之间做交换，是可选的能源互转件。\n它含魔力池与活石，需稳定的魔力来源。\n按需接入，不必强上。',
          p('mana_exchanger'), ())
    quest('pbo', 'BO 处理器：植物魔法电路件', 'processor_bo',
          'BO 处理器是 Botania 侧的电路部件，由红石、活石、魔力钢与魔力线圈合成。\n它是 Technomancy Botania 模块的收尾件，与 TC 处理器对应。\nF 区以此收尾，神秘科技全章完成。',
          p('processor_bo'), ())


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
            # ItemStack NBT uses namespaced id; this is not an FTB object.
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
    with zipfile.ZipFile(JAR) as jar:
        names = set(jar.namelist())
        for ident in sorted(ids):
            ns, name = ident.split(':', 1)
            if ns != MOD:
                continue
            model = f'assets/{MOD}/models/item/{name}.json'
            assert model in names, f'Missing jar item model: {ident}'
            json.loads(jar.read(model))
            evidence[ident] = dict(jar=JAR.name, model=model)
    for ns in sorted({i.split(':')[0] for i in ids} - {MOD}):
        wanted = {i.split(':')[1] for i in ids if i.startswith(ns + ':')}
        matches = []
        for f in sorted((ROOT / 'mods').glob('*.jar')):
            with zipfile.ZipFile(f) as jar:
                names = set(jar.namelist())
                if all(f'assets/{ns}/models/item/{n}.json' in names for n in wanted):
                    matches.append(f)
        assert len(matches) == 1, f'Ambiguous/missing jar for {ns}: {matches}'
        f = matches[0]
        with zipfile.ZipFile(f) as jar:
            for name in wanted:
                evidence[f'{ns}:{name}'] = dict(jar=f.name, sha256=digest(f.read_bytes()),
                                                model=f'assets/{ns}/models/item/{name}.json')
    return evidence


def layout():
    # Six independent layered teaching DAGs. Fixed semantic keys, not ID indices.
    # Each local tree has ranks 0,1,2,3 and stable left/right barycenter ordering.
    local = [(2, 0), (0, 2), (4, 2), (0, 4), (4, 4), (0, 6), (4, 6)]
    parents = [None, 0, 0, 1, 2, 3, 4]
    edges = []
    assert len(Q) == 42
    for cluster in range(6):
        origin = ((cluster % 3) * 10, (cluster // 3) * 10)
        subset = Q[cluster * 7:cluster * 7 + 7]
        for i, q in enumerate(subset):
            q['x'], q['y'] = (float(origin[j] + local[i][j]) for j in (0, 1))
            q['deps'] = [] if parents[i] is None else [subset[parents[i]]['key']]
            if q['deps']:
                edges.append((q['deps'][0], q['key']))
    by_key = {q['key']: q for q in Q}
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
    ap.add_argument('--verify-repeat', action='store_true', help='Run two validated builds and compare exact bytes')
    args = ap.parse_args()
    if args.verify_repeat:
        snapshots = []
        for _ in range(2):
            subprocess.run([sys.executable, str(Path(__file__).resolve())], check=True, capture_output=True)
            snapshots.append((OUTPUT.read_bytes(), MAP.read_bytes()))
        assert snapshots[0] == snapshots[1], 'Two builds differ byte-for-byte'
        print(json.dumps(dict(repeat_equal=True, chapter_sha256=digest(snapshots[0][0]),
                              mapping_sha256=digest(snapshots[0][1])), indent=2))
        return
    content()
    geometry = layout()  # Calculate before serialization or any output writes.
    library = load_library()
    used, legacy_issues, old_quest_count = library_report(library)
    assert GROUP in used
    prior = json.loads(MAP.read_text(encoding='utf-8')) if MAP.exists() else None
    if OUTPUT.exists():
        assert prior, 'Existing chapter without ID map; refusing overwrite'
        assert digest(OUTPUT.read_bytes()) == prior['chapter_sha256'], 'Chapter manually modified; refusing overwrite'
    elif prior:
        raise ValueError('ID map exists but chapter missing; investigate before publication')
    order_values = [d.get('order_index', 0) for d in library.values() if d.get('group') == GROUP and 'quests' in d]
    order = prior['order_index'] if prior else max(order_values) + 1
    assert order not in order_values, f'order_index {order} is now occupied; coordinate with other chapter author'
    ids = dict(prior['ids']) if prior else {}
    assert len(set(ids.values())) == len(ids), 'Duplicate persisted IDs'
    for key, value in ids.items():
        assert re.fullmatch('[0-9A-F]{16}', value) and 0 < int(value, 16) < 2**63
        assert value not in used, f'Published ID collision: {key}'

    def sid(key):
        expected = f'{int.from_bytes(hashlib.sha256((SALT + ":ftbquests:v1:" + key).encode()).digest()[:8], "big") & 0x7FFFFFFFFFFFFFFF:016X}'
        assert int(expected, 16) > 0
        if key in ids:
            assert ids[key] == expected, f'Mapping changed: {key}'
        else:
            assert expected not in used and expected not in ids.values(), f'ID collision: {key}'
            ids[key] = expected
        return ids[key]

    chapter = dict(default_hide_dependency_lines=False, default_quest_shape='', filename='technomancy',
                   group=GROUP, icon=MOD + ':ritual_tome', id=sid('chapter'), order_index=order,
                   quest_links=[], quests=[], title='&5Technomancy&r · 神秘科技')
    all_items = {chapter['icon']}
    for q in Q:
        targets = [dict(id=sid('task/' + q['key'] + '/item/' + item), type='item', item=item, count=1,
                        consume_items=False, match_nbt=False, only_from_crafting=False)
                   for item in q['items']]
        if q['check']:
            targets.append(dict(id=sid('task/' + q['key'] + '/check'), type='checkmark', title=q['check']))
        assert targets, f'No tasks: {q["key"]}'
        assert len(q['items']) == len(set(q['items'])), 'Duplicate item objective'
        # Reading nodes carry no reward; construction nodes get 2 cogs only.
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
    assert JAR.is_file(), f'Technomancy source jar missing: {JAR}'
    jar_hash = digest(JAR.read_bytes())
    item_evidence = verify_items(all_items)
    source_evidence = {}
    with zipfile.ZipFile(JAR) as jar:
        for rel in sorted({path for q in Q for path in q['evidence']}):
            f = JAVA / rel
            assert f.is_file(), f'Missing source: {rel}'
            compiled = 'theflogat/technomancy/' + rel[:-5] + '.class'
            assert compiled in jar.namelist(), f'Missing compiled class: {rel}'
            source_evidence[rel] = dict(source_sha256=digest(f.read_bytes()), class_sha256=digest(jar.read(compiled)))
    # Reparse actual serialized candidate, not only the Python data model.
    comments = '# Generated by build_technomancy_chapter.py; semantic IDs persisted in technomancy_ids.json.\n'
    comments += ''.join('# ' + k + ' = ' + v + '\n' for k, v in sorted(ids.items()))
    encoded = (comments + dump(chapter) + '\n').encode('utf-8')
    parsed = SnbtParser(encoded.decode()).parse()
    assert parsed == chapter, 'Serialization changed structure'
    assert len(parsed['quests']) == len(Q)
    for spec, result in zip(Q, parsed['quests']):
        assert len(result['tasks']) == len(spec['items']) + bool(spec['check']), 'Lost multi-objective'
        assert [t['item'] for t in result['tasks'] if t['type'] == 'item'] == spec['items']
    combined = {**library, 'chapters/technomancy.snbt': parsed}
    all_ids, combined_issues, total_quests = library_report(combined)
    assert combined_issues == legacy_issues, 'New library errors: ' + str(combined_issues)
    expected_keys = {'chapter'}
    for q in Q:
        expected_keys.add('quest/' + q['key'])
        expected_keys.update('task/' + q['key'] + '/item/' + i for i in q['items'])
        if q['check']:
            expected_keys.add('task/' + q['key'] + '/check')
        if q['items']:
            expected_keys.add('reward/' + q['key'] + '/cog')
    assert expected_keys == set(ids), 'Orphan or lost business keys in map'
    report = dict(quests=len(Q), objectives=sum(len(q['tasks']) for q in parsed['quests']),
                  multi_objective_quests=sum(len(q['tasks']) > 1 for q in parsed['quests']),
                  rewards=sum(len(q['rewards']) for q in parsed['quests']), unique_items=len(all_items),
                  group=GROUP, order_index=order, layout=geometry, global_quests=total_quests,
                  global_definitions=len(all_ids), baseline_issues=legacy_issues, chapter_sha256=digest(encoded))
    # Library totals belong to this invocation's report, not the persisted map:
    # adding an unrelated chapter must never invalidate this chapter's --check.
    stable_validation = {k: v for k, v in report.items()
                         if k not in ('global_quests', 'global_definitions', 'baseline_issues')}
    manifest = dict(schema=2, salt=SALT, order_index=order, chapter_sha256=digest(encoded),
                    ids=dict(sorted(ids.items())), technom_jar_sha256=jar_hash,
                    item_evidence=item_evidence, source_evidence=source_evidence,
                    quest_evidence={q['key']: q['evidence'] for q in Q}, validation=stable_validation)
    map_bytes = (json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + '\n').encode('utf-8')
    # Re-read shared library just before write to detect concurrent chapter work.
    assert load_library() == library, 'Quest library changed during validation; rerun'
    if not args.check:
        OUTPUT.write_bytes(encoded)
        MAP.write_bytes(map_bytes)
        assert OUTPUT.read_bytes() == encoded and MAP.read_bytes() == map_bytes
    elif prior:
        assert OUTPUT.read_bytes() == encoded, 'Generated content differs from published chapter'
        assert MAP.read_bytes() == map_bytes, 'Evidence/map differs; regenerate after review'
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
