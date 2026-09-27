#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pollution FTBQ 2001.4.17 chapter. Python 3.10+, standard library only.

Run --check for read-only validation; run without arguments to publish after
validation. Only pollution.snbt and pollution_ids.json are generated. Semantic
keys, persisted IDs, order_index and prior output SHA protect published work.
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
OUTPUT = QUESTS / 'chapters/pollution.snbt'
MAP = TOOLS / 'pollution_ids.json'
SOURCE = Path(r'H:\MinecraftMods\Pollution-Unofficial-1.20.1')
JAVA = SOURCE / 'src/main/java/meowmel/pollution'
JAR = SOURCE / 'build/libs/pollution-1.20.1-1.0.0-1.20.1-port.0.1.0.jar'
GROUP = '4A46A5E1358A80A6'
SALT = 'pollution'


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
            raise ValueError(f'Expected {t}, got {actual} at token {self.i}')

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
    Q.append(dict(key=key, title=title, icon='pollution:' + icon,
                  description=text.split('\n'), items=list(items), evidence=list(evidence), check=check))


def p(*names):
    return tuple('pollution:' + x for x in names)


def content():
    quest('intro', 'A · Pollution：魔法工业与环境代价', 'lv_vis_generator',
          'Pollution 将 GT 电力、多方块与神秘时代的灵气/源质、植物魔法的魔力连接起来；既是工业扩展，也给部分工业活动加入环境代价。\n本章六区可以分别阅读：A 污染与能源，B 源质供应，C 魔导加工，D 电路，E 植物魔法，F 节点工程。建议先读 A；任务连线表示教学顺序，不是全部配方科技树。\n先准备 GT 基础供电、神秘时代研究/注魔和植物魔法材料。配方所需等级以 JEI 的电压、输入和研究要求为准，不能把控制器名称中的等级当成唯一制造门槛。\n物品目标只检查持有，不消耗材料，也不证明多方块成型。运行与流体操作采用明确的手动确认；请完成正文操作后再勾选。',
          evidence=('common/machine/PollutionMachines.java', 'loaders/recipes/PollutionRecipes.java'), check='已阅读六区导航与检测规则')
    quest('pollution', '按区块积累：产生、影响与扩散边界', 'lv_flux_muffler',
          '工业污染存储在各维度的区块数据中。当前实现没有相邻区块扩散/风向传播算法；同一区块不同高度共用数值。别把它与 TC4R 咒波、玩家扭曲或 MEK 辐射混为一谈。\nGT 工作多方块的 afterWorking 钩子读取每个消声仓的排放强度，在消声仓所在区块记账；机器爆炸按威力×倍率增加污染。灵气发电机每抽 1 vis 另增 0.1；大型节点发电机的 Ominous 节点另有排放。不是所有耗电机器都固定排污。\n本实例开启污染、爆炸污染和地形转换，排放倍率 1。每 200 tick 所有污染区块自然减少 0.2。停产后数值逐步下降，不会瞬间归零。\n超过 10：反胃+饥饿；达到 20/30/40：追加虚弱/挖掘疲劳/失明。每 40 tick 刷新 100 tick 效果。达到 25 后随机将表层草方块变沙；达到 50 后水源还可能变熔岩，每维度每 tick 最多转换 4 格。衰减不会自动恢复地形。\n右上角 HUD 在超过阈值时显示污染倍率。工业区与居住区分区、控制排放源、停机等待衰减是可执行的管理方法；不要主动污染住宅来完成任务。',
          evidence=('api/pollution/PollutionEngine.java', 'api/pollution/PollutionData.java', 'mixin/gregtech/WorkableMultiblockPollutionMixin.java', 'mixin/gregtech/ExplosionPollutionMixin.java'), check='理解工业污染没有跨区块扩散，完成厂区选址')
    quest('vis', '灵气发电与回充：两种方向', 'lv_vis_generator',
          '灵气发电机：TC4R 节点/中继网络中的真实 vis → EU，并增加工业污染。当前配置 1 vis→250 EU、0.1 污染；LV 以 32 EU/t 的目标速率积累抽取额度，整单位结算，低档会间歇输出。接好能量输出面；无灵气或电池满就不抽。\n灵气充能机：EU → 8 格内最近的已加载节点，优先补基础容量缺口最大的方面，不能超出基础容量。LV 每次成功付 32 EU，当前倍率下补 1 vis。不要照旧教程把它当作可无限超充节点的装置。\n两者都有 LV 型号。发电机合成用同级外壳、4 电动马达、2 活塞、2 转子；充能机把活塞换成发射器。实际零件请查 JEI。回充/抽取与污染是独立记账，不应把反复循环当作无代价供电方案。',
          p('lv_vis_generator', 'lv_vis_provider'), ('common/machine/VisGeneratorMachine.java', 'common/machine/single/VisProviderMachine.java', 'loaders/recipes/PollutionRecipes.java'))
    quest('muffler', '源头减排：咒波消声仓', 'lv_flux_muffler',
          '咒波消声仓是 GT 多方块部件，注册 MUFFLER 能力；放到结构允许的消声仓位置。它的每次操作污染强度返回 0，也不扩散 GT 环境危害。它阻止此仓的新增排放，不会吸走区块中已经积累的工业污染，也不抵消独立的 vis 发电排放。\n制造并非普通 LV 机器外壳就够：魔导组装配方使用同级 GT 消声仓、2 咒波黏浆、可用时的炼金催化器、500 mB Infused Taint；高档追加材料/流体，另有注魔路线。先建设 B 的源质供应和 C 的魔导加工。\n回收率为 min((等级−1)×10,100)%：LV 是 0%，MV 是 10%。低排放与副产物回收率是两件事；成型后检查排气口与结构提示。',
          p('lv_flux_muffler'), ('common/machine/part/FluxMufflerMachine.java', 'loaders/recipes/HatchRecipes.java'))
    quest('scrubber', '咒波洗消：EU + 滤芯', 'lv_flux_scrubber',
          'Flux 洗消机消耗 EU 与滤芯耐久，清除附近 16 格内可由 TC4R API 消耗的咒波；不调用工业污染 scrub。实例配置中旧注释称清除区块污染，已与当前源码不符。\n放入空气过滤器滤芯 I 并接电：清理额度每 tick 累加 2^(等级−1)×0.002。LV 约积累 500 tick 才够 1 quanta；成功清除时才扣一次该档 VA 的 EU 和 1 滤芯耐久。无咒波、无滤芯或电不足就不清理。\n滤芯 I 在 LV 组装机：4 纸+4 Infused Earth 粉+2 木炭粉+250 mB Infused Earth→1 滤芯，100 tick。I～V 耐久为 24/36/48/64/72 万，升级滤芯提高耐久，不直接提高清理速率。源质原料获取见 B 区。',
          p('lv_flux_scrubber', 'filter.i'), ('common/machine/single/FluxScrubberMachine.java', 'compat/tc4r/TC4RBridge.java', 'loaders/recipes/RemainingItemRecipes.java'))
    quest('integration', 'GT / MEK / Create：联动边界', 'magic_assembler',
          'GT 是本模组机器、EU、电压与物品/流体仓的基础。神秘时代提供节点网络、源质和注魔；Botania 提供魔力及材料；AE2 有明确的魔导组装批量配方。\n已核对当前 Pollution Java 注册、配方与 mixin：没有 Mekanism 或 Create 专属机器/配方、排污钩子。因此不能说 MEK 机器或 Create 蒸汽引擎会因为这个模组自动排工业污染，也不能编造转速→魔力或气体→源质的转换。\n本实例同时安装这些模组，可用各自兼容的运输系统组织工厂；但 MEK 气体/浆液不是普通流体，Create 转速也不是 GT EU。需要转换时，查询实例里实际存在的转换设备和接口。\nAstral 另有透镜仓、五类星辉加工机和星座塔，本章只作导航，不复制另一个星辉章节的进度。血魔法不在此移植版支持范围。',
          evidence=('common/machine/PollutionMachines.java', 'loaders/recipes/AERecipes.java', 'loaders/recipes/AstralIntegrationRecipes.java'), check='确认各能源/污染/流体系统边界')
    quest('fluxcell', '咒波燃料电池：先读安全范围', 'lv_flux_fuel_cell',
          '附近可清除的 TC4R 咒波 → EU；工业污染不是它的燃料。咒波不足 10 不工作，10～49 按公式变化效率，50 以上效率为 3。每 tick 耗用额度=0.005×4+0.2×(等级−1)，按整数提前扣取并保存小数缓存。\n机器先检查安全上限 60+5×4^等级；LV 上限为 80，超过就拆除自身并爆炸，检查发生在发电之前。不要为任务故意堆咒波或引爆；本节点仅要求理解范围。\n想稳定起步，可选植物魔法→EU 的魔力发电机（E 区），而不是把不可控的污染源围在家里。灵气检测器 vis_checker 实际报告玩家永久/黏性/临时扭曲，并非工业污染仪或本机燃料读数。',
          evidence=('common/machine/single/FluxFuelCellMachine.java', 'common/item/VisCheckerItem.java'), check='理解 LV 超过 80 咒波会爆炸，不进行危险实测')

    quest('essentia', 'B · 源质本体、Infused 流体与矿物', 'infused_exchange',
          'TC4R 源质是罐/管道中的方面；Pollution 的 Infused 是 GT 可输送流体。二者不是同一个储存接口。六原始方面为风、火、水、地、秩序、熵。\n起步可用神秘时代源质设施配合转换矩阵，或探索 Pollution 地下世界的原始源质矿脉。六种 Infused 粉在普通 GT 提取机中各以 1 粉→144 mB 流体，30 EU/t、200 tick；为滤芯和熔炉准备地/火源质。\n地下入口：在主世界造有实体底的 2×2 水池，岸边使用石头，或带花草/树叶等自然装饰的泥土草地，投入一颗钻石并留在附近等待仪式。按 JEI/实际传送门规则检查边界。\n本区分为转换/混合与熔炉/收集两条供应路线；化合源质一般在混合器制造，不要求先做昂贵的节点生产机。',
          evidence=('loaders/recipes/InfusedProcessingRecipes.java', 'dimension/worldgen/PollutionOreVeins.java', 'dimension/PortalFormationEvents.java', 'common/block/tile/PortalBlock.java'), check='读懂三种物料形态与起步路线')
    quest('exchange', '转换矩阵：1 点原始源质→144 mB', 'infused_exchange',
          '控制器配一个流体输出仓，按 JEI 结构预览放置；源码的两个 aisle 表示结构轴向，不应把扫描中心误当成仓室位置。\n把含原始方面的源质容器放在控制器上方一格为中心、附近 3 格内。每 10 tick 尝试一次，只抽一种原始方面的 1 点，输出 144 mB 对应流体。此转换逻辑不扣 EU。输出不足 144 mB 空间时不抽源质。\n持续抽走输出，避免一个仓被某种方面占住后堵住后续转换。这里只遍历六种原始方面，不会转换所有化合源质。\n控制器有 TC4R 注魔配方：中心为 MV 提取机，另需 Valonite、MV 电路、风/水水晶和虚空棱镜，并支付对应方面；详情以 JEI 为准。',
          p('infused_exchange'), ('common/machine/multiblock/magic/InfusedExchangeMachine.java', 'loaders/recipes/InfusionRecipes.java'))
    quest('smelter', '两种熔炉：物品→源质 / 流体', 'essence_smelter',
          '源质熔炉与 GT 源质熔炉都消耗有方面的物品、EU 和 Infused Fire。启动时处理首个合适物品的整堆，先用小批次试机。原版物品是否有方面，以 TC4R 实际方面表为准。\n普通源质熔炉把产物送往周围 5 格内可接受的 TC4R 源质运输方块，提前布置空罐与管道。GT 变体将已映射方面按 1 点→144 mB 转成 Infused 流体，必须有输出流体仓。\n当前 GT 变体只找到第一个输出流体仓并依次尝试填入各方面；不能保证多个仓自动分离所有产物。不兼容/装不下的部分可能丢失。普通熔炉没有接收容器也可能损失产物。先核对原料方面、分批加工，切勿把贵重整堆物品盲目投入。\n下列两个目标分别检测两种控制器，持有不代表已经成型或完成加工。',
          p('essence_smelter', 'gt_essence_smelter'), ('common/machine/multiblock/magic/EssenceSmelterMachine.java', 'common/machine/multiblock/magic/GtEssenceSmelterMachine.java'))
    quest('tank', '源质储罐与源质流体仓', 'lv_aspect_tank',
          'Aspect Tank 储存 TC4R 源质本体，每罐一种方面；LV 容量 10,000，逐档翻倍。用带方面的容器设置过滤，配置自动输出，并用源质管道连接；GUI 支持容器输入/输出。\nInfused Fluid Hatch 储存 GT 流体，作为魔法多方块的额外流体支付部件；不是 TC4R 源质罐。LV 容量 16,000 mB（8000×2^等级），支持流体容器槽。\n普通配方输入流体仍按结构接入流体输入仓；带特殊源质每 tick 成本的配方需要专用仓。装错仓会造成有原料却无法启动。\n两者的魔导组装路线需要同级 GT 流体输入仓、植物魔法材料与 Infused Aura，高档再追加材料；因此 LV 标签并不表示能在纯 LV 工业开局直接制造。',
          p('lv_aspect_tank', 'lv_infused_fluid_hatch'), ('common/machine/single/AspectTankMachine.java', 'common/machine/part/InfusedFluidHatchMachine.java', 'loaders/recipes/HatchRecipes.java'))
    quest('collector', '聚灵阵：干净节点环境→六种流体', 'essence_collector',
          '结构成型并接 EU、六个输出流体仓，在 8 格内准备已加载且有 vis 的 TC4R 节点。机器读取节点当前 vis 和本区块工业污染计算产速；这里代码变量 flux 指工业污染，不是 TC4R 咒波。\nvis≤0、污染≥vis 或对数产速项不为正时停产；提高线圈/能源等级和节点 vis 可提高产量。它读取节点状态作为产速条件，这段逻辑不从节点抽走 vis。\n通常产出风/火/地/水/秩序/熵六种流体；输入总线第一槽放仅含一种原始方面的晶体源质，可聚焦为该流体的三倍基础产速。不合条件的晶体会回到普通模式。\n保持输出抽取，满仓并不保证回滚该 tick 的耗电/产物。产物供滤芯、混合器、化工和节点生产机。',
          p('essence_collector'), ('common/machine/multiblock/magic/EssenceCollectorMachine.java', 'common/machine/multiblock/magic/EssenceCollectorPatterns.java'))
    quest('compound', '混合化合源质：Energy→Magic→Aura', 'magic_mixer',
          '普通 GT 混合器或魔导搅拌机可跑化合源质配方：两种流体各 1000 mB→2000 mB 产物，时间与耗电由成分复杂度决定，查 JEI 电压而不是认为全部属于同一档。\n关键链：Order+Fire→Energy；Air+Energy→Magic；Magic+Air→Aura。支线：Earth+Water→Life；Fire+Air→Light；Entropy+Light→Dark；Entropy+Magic→Taint。\nEnergy 用于节点生产和魔法燃料；Aura/Magic 用于电路、仓室与魔导加工；Taint 用于咒波消声仓。根据需求先建小规模缓冲，避免把全部原始源质烧成燃料。\n实际用混合器完成一批 Energy 和一批 Aura，记录流体管路和配方电压，再手动确认。本任务不把持有空桶当作产出检测。',
          evidence=('loaders/recipes/CompoundAspectRecipes.java',), check='完成 Energy 与 Aura 各一批并确认输入输出')
    quest('fuel', '魔法燃料：流体→EU', 'lv_magic_turbine',
          'LV/MV/HV 单方块魔法涡轮使用 MAGIC_TURBINE_FUELS。六种原始 Infused 流体的基础燃料配方是 80 mB、80 tick、输出 32 EU/t；实际机器调度/并行后的消耗显示以界面为准。化合源质也有燃料配方，复杂度决定时长和档位。\n后期魔导化学反应器可做魔力抗爆焦化硝基苯：1000 mB 甲酸铵+1000 mB 乙醇+10000 mB 硝基苯+1152 mB Infused Energy，配不消耗的焦化催化剂核心→16000 mB 燃料，HV、200 tick。不要漏掉催化剂或四路流体。\n大型/巨型轮机按预览装足对应等级转子支架与转子，并使用动力输出仓；运行有转子磨损，产能受功率/速度/效率影响。能源输入仓不能替代动力输出仓。\n燃料链是利用富余源质的选择，不是所有加工线的前置。',
          p('lv_magic_turbine'), ('loaders/recipes/CompoundAspectRecipes.java', 'loaders/recipes/MagicFuelRecipes.java', 'common/machine/multiblock/magic/AbstractMagicTurbineMachine.java'))

    quest('processing', 'C · 魔导加工：先认配方类别', 'magic_assembler',
          '魔导多方块以 GT 配方系统为基础，许多机器合并几个配方类别；不是输入任何东西都能转化。先用 JEI 选定目标配方，再按控制器预览准备外壳、线圈和仓室。\n魔导组装机兼容普通组装与专用魔导组装；魔导化反兼容普通化反与魔法化工；魔导搅拌机使用普通混合配方。配方列出的 EU、流体、特殊魔法成本分别支付。\n常见控制器来自神秘时代注魔，要求既有 GT 机器、催化剂、控制组件、棱镜与方面，不能仅凭注册档位认定它是开局机器。物品任务为制作里程碑，阅读路线不替代制造配方。',
          evidence=('common/machine/PollutionMachines.java', 'loaders/recipes/InfusionRecipes.java'), check='选定第一条要工业化的配方并查看结构')
    quest('assembler', '魔导组装与 AE2 批量处理器', 'magic_assembler',
          '魔导组装机：配方物品/流体+EU→组装产物，兼容普通与魔导组装两张配方表，是本章仓室和低中阶魔法电路的核心。制造控制器后按预览补齐结构，按配方接入物品与流体仓。\n可验证的 AE2 批量配方：4 块逻辑电路印刷件+1 红色合金板+144 mB 熔融 HSSG→16 逻辑处理器，480 EU/t、160 tick。工程/运算处理器各有同构路线，替换对应印刷件和产物。\n这里不是普通压印器配方，也不需要凭空添加硅片/红石；按当前 JEI 的魔导组装条目投料。先储备 HSSG 再尝试批量生产。',
          p('magic_assembler'), ('common/machine/PollutionMachines.java', 'loaders/recipes/AERecipes.java'))
    quest('chemical', '化反、浸洗与分层蒸馏', 'magic_chemical_reactor',
          '魔导化反接收普通 GT 化学配方和专用魔法化工配方：对应反应物+EU→化学品/魔法燃料，例子见 B 的魔法燃料任务。普通水不会代替配方里的 Infused Water。\n魔法浸洗池处理化学浸洗/洗矿，内部 5×5 池必须填满水源。补池每 5 tick 最多一格，每格需输入仓 1000 mB 水；不足一桶不会补，工艺流体与池水条件要分别满足。\n魔导蒸馏塔支持蒸馏/蒸馏室配方、1～12 层，每层输出仓接收按配方顺序分配的流体，第一种去最低层。层数不足、流体不兼容或满仓会阻塞，先检查对应层再补料。\n本任务检测化反和蒸馏控制器；浸洗说明供工厂设计参考。',
          p('magic_chemical_reactor', 'magic_distillery'), ('common/machine/PollutionMachines.java', 'common/machine/multiblock/magic/MagicChemicalBathMachine.java', 'common/machine/multiblock/LayeredMagicTowerMachine.java'))
    quest('mechanical', '研磨、成型与分离：按输入配方生产', 'magic_macerator',
          '魔导研磨机使用研磨配方，合适的矿物/材料+EU→配方规定的粉或副产物；具体倍率取决于那条配方，不统一承诺翻倍。\n魔导折弯机合并折弯、压缩、模压、锻锤；魔导离心机合并离心和热力离心。锭/板/粉、模具与电路配置均按当前配方投料，产物用于机械零件与电路。\n另有线材轧机、挤压机、筛选机、电解机、切割机和高压釜，分别承接对应 GT 配方类别；选择你工厂真正需要的机器扩产。\n先制作研磨与折弯控制器，然后用已知配方试机，勿将控制器物品检测理解为已验证全部加工模式。',
          p('magic_macerator', 'magic_bender'), ('common/machine/PollutionMachines.java',))
    quest('payment', '仓室支付：电、Vis、源质各就各位', 'lv_vis_hatch',
          'Vis 仓从 TC4R 网络抽取灵气、形成缓冲，供带 Vis 要求的魔法配方支付；Infused 流体仓供特殊源质每 tick 成本。物品/流体配方原料仍由普通 IO 仓处理。\n配方每 tick 会重新检查授权，并按并行数缩放成本。缺少所需仓室、灵气或流体会阻止进度；增幅/折扣不是免除全部原料。\n塔罗仓与星辉透镜仓用于相应授权/增幅。星辉条件还可能受夜空、月相、星座与晶体属性影响，详见独立 Astral 章节；不要给普通配方随意补上并不存在的星座条件。\n检查顺序：结构→能源方向与电压→物品/流体→特殊支付仓→输出空间→授权。这里手动确认，不用一个物品伪装整套支付系统检测。',
          evidence=('common/machine/multiblock/MagicRecipeLogic.java', 'common/machine/multiblock/MagicMultiblockController.java', 'common/machine/part/VisHatchMachine.java'), check='对照所选配方完成一次仓室支付排查')
    quest('battery', '魔法电池：储能与调峰', 'magic_battery',
          '多方块魔法电池将输入仓的 EU 储存，再向输出仓供电；本身不把污染或源质变成免费能源。容量由核心和线圈组合决定，一级组合为 250,000 EU。\n按结构预览搭建输入/输出能源仓，分别连接供电端和负载端。可在界面暂停传输；拆结构不会把已存能量直接截断到更小容量。\n先用可控负载验证充电/放电方向，再接入长周期源质加工线。不要把这种多方块电池与 battery.lv.magic 等物品电池外壳/成品混淆。',
          p('magic_battery'), ('common/machine/multiblock/magic/MagicBatteryMachine.java', 'loaders/recipes/InfusionRecipes.java'))
    quest('commission', '试产验收：先一批，再自动化', 'magic_assembler',
          '选择本区一台机器，在 JEI 记录一个明确配方的输入、数量、EU/t 和产物。只放一批原料，确认产出正确再接无限供料。\n检查特殊流体是否进了正确仓、产物是否被抽走、多流体是否互相堵塞。能量输入/输出与维护部件以结构为准。普通物品任务无法确认这些现场状态。\n生产稳定后再扩展 AE2 模式、管道或其他兼容物流；自动化必须遵守真实配方的催化剂是否消耗与多输出要求。记录一次实际投入→产出，然后勾选。',
          evidence=('common/machine/multiblock/MagicRecipeLogic.java',), check='用一批原料完成试产并核对实际产物')

    quest('circuits', 'D · 魔法电路：板与成品分开', 'magic_circuit.ulv',
          '魔法电路板 magic_circuit_board.* 与蕴魔电路 magic_circuit.* 是不同物品。拿到板不等于获得同级可用电路；本区的制作节点都分别检测板与成品。\nULV～LuV 成品走魔导组装：对应板+上一级电路（ULV 用真空管起步）+金属/魔法材料+指定流体。ZPM～MAX 成品改走 TC4R 注魔，上一级电路为中心。\n本区左支线为 ULV→LV/MV→HV/EV，右支线介绍 IV→LuV→ZPM+。两条线为紧凑阅读分区，不意味着 IV 可以跳过前级；完整材料链始终按 JEI。\n电路等级表示用途标签，不代表所有获取路线都要求同级 GT 供电，尤其注魔路线需另看研究、材料与稳定性。',
          evidence=('loaders/recipes/MagicCircuitRecipes.java',), check='理解电路板与成品的独立目标及完整前级需求')
    quest('ulv', 'ULV：真空管起步', 'magic_circuit.ulv',
          '先制作 ULV 魔法电路板，再进入魔导组装机。成品配方：板+2 真空管+2 Salisundus 粉+4 锡箔+已安装 Botania 提供的 4 魔力粉+100 mB 胶水→ULV 蕴魔电路，100 tick，使用 ULV 的 VA。\n这里的 ULV 指成品档次，魔导组装机本身仍有控制器/结构的制造门槛。不要拿到真空管就期待普通工作台合成。\n两个物品均保留，制作后用于后续升级。',
          p('magic_circuit_board.ulv', 'magic_circuit.ulv'), ('loaders/recipes/MagicCircuitRecipes.java',))
    quest('iv', 'IV：盖亚材料与三路流体', 'magic_circuit.iv',
          '此支线承接左侧 EV 成品，不能跳级。IV 魔导组装以 EV 电路+IV 板为基础，加入 8 钨钢箔、4 Salisundus 粉、各 2 高级贴片二极管/电感、1 盖亚魂锭、2 泰拉钢锭，以及已安装时的火符文。\n流体为 1000 mB Aura+500 mB Order+500 mB Magic；300 tick，IV VA。先保证三种流体都有独立供料能力。\n板有自身制造路线；下列板/成品目标都需满足，不发放高级电路奖励跳过过程。',
          p('magic_circuit_board.iv', 'magic_circuit.iv'), ('loaders/recipes/MagicCircuitRecipes.java',))
    quest('lvmv', 'LV / MV：逐级补魔力材料', 'magic_circuit.mv',
          'LV：前级电路+LV 板，配铜箔、魔力钢、Salisundus、魔力粉/魔力符文，输入 Aura 与胶水，120 tick。MV：LV 成品+MV 板，配银箔、魔力钢、Salisundus、魔力钻石/风符文，输入 Aura 与 Life，160 tick。\n上述 Botania 附加项在当前安装环境会加入配方，不是玩家可自行省略。具体堆叠数请按 JEI 投放。\n分别收集 LV 板、LV 成品、MV 板、MV 成品四项目标；这也检查生成器没有吞掉多目标分支。',
          p('magic_circuit_board.lv', 'magic_circuit.lv', 'magic_circuit_board.mv', 'magic_circuit.mv'), ('loaders/recipes/MagicCircuitRecipes.java',))
    quest('luv', 'LuV：替代注魔板与组装成品', 'magic_circuit.luv',
          'LuV 板有纯魔法替代注魔路线：IV 板为中心，配硅岩合金箔、高级贴片、Salisundus、魔力钻石/珍珠、盖亚魂锭和春符文，支付相应方面。它是既有培养链之外的另一条路线。\nLuV 成品仍走魔导组装：IV 成品+LuV 板，配硅岩合金箔、虚空锭、高级贴片电阻/电容、盖亚魂锭及植物魔法材料；三路流体为 Aura 2000、Life 1000、Light 1000 mB，400 tick，LuV VA。\n纯魔法替代板不需要把血魔法占位物品当作必需前置；成品不会因为板是注魔做的就自动免除组装耗电。',
          p('magic_circuit_board.luv', 'magic_circuit.luv'), ('loaders/recipes/MagicCircuitRecipes.java',))
    quest('hvev', 'HV / EV：贴片与复合源质', 'magic_circuit.ev',
          'HV 成品升级使用 MV 电路+HV 板，配金箔、源质钢、赛特斯石英、魔力珍珠/地符文，并输入 Aura/Magic/Light，200 tick。\nEV 成品使用 HV 电路+EV 板，配铝箔、泰拉钢、高级贴片电容/晶体管、精灵尘/水符文；流体 Aura 500、Magic 200、Light 200 mB，240 tick，EV VA。\n准备 B 区的混合链能避免每次升级临时找流体。先完成板，再做成品；四项目标均为持有检测。',
          p('magic_circuit_board.hv', 'magic_circuit.hv', 'magic_circuit_board.ev', 'magic_circuit.ev'), ('loaders/recipes/MagicCircuitRecipes.java',))
    quest('highcircuits', 'ZPM 及以后：两条注魔升级链', 'magic_circuit.zpm',
          '从 ZPM 起，板与成品分别走 TC4R 注魔：板用前级板作中心；成品用前级电路作中心，再配同级板、金属板箔、高级贴片、魔法核心和符文。两条链都要推进。\n随等级升高，方面成本、不稳定性、材料要求增加；UHV 起引入 Pollution 符文，UXV 起需要无尽材料。不要仅依靠电路名字判断已经具备制造条件。\n本节点以 ZPM 板和电路作为实作里程碑，UV～MAX 作为后续拓展；查每一档 JEI 的真实注魔祭坛输入与研究条件，而不是复制上一档数量。',
          p('magic_circuit_board.zpm', 'magic_circuit.zpm'), ('loaders/recipes/MagicCircuitRecipes.java',))

    quest('botania', 'E · 植物魔法工业化：分清三种魔力', 'lv_mana_generator',
          'Botania 的魔力、魔力能量仓中的 EU、名为 mana/InfusedAura 的流体属于不同接口。机器名称都带“魔力”也不能直接混接。\n魔力发电机接收 Botania 魔力，以 1 mana→1 EU 存入电缓存，输入速率按档位限制；LV～IV 可选。它不会通过自身 tick 逻辑新增工业污染。\n仓室、花阵列和工业化祭坛各有独立用途；先建设原生 Botania 材料供应，再看配方是耗 EU、耗纯魔力，还是耗流体燃料。',
          evidence=('common/machine/single/ManaGeneratorMachine.java', 'common/machine/part/mana/ManaHatchMachine.java', 'common/machine/part/mana/ManaPoolHatchMachine.java'), check='分清 Botania 魔力、EU 与魔力流体')
    quest('managen', '魔力发电机：稳定输入→EU', 'lv_mana_generator',
          '放置 LV 魔力发电机，用其支持的魔力接收接口提供 Botania 魔力，能量输出面接 GT 导线与负载。转换为 1:1，LV 缓存 32×64=2048 EU，并按档限制接收速率。\n没有魔力就没有新电量，缓存满时无法继续接收。不要把同名的燃料流体灌进去：这是魔力接收器，不是魔法流体涡轮。\n发电机不返还 Botania 魔力；构建原生花与池的持续供魔系统，再用于低耗电工序。',
          p('lv_mana_generator'), ('common/machine/single/ManaGeneratorMachine.java', 'loaders/recipes/MachineRecipes.java'))
    quest('daisy', '工业白雏菊与花药台', 'industrial_pure_daisy',
          '工业白雏菊和魔力花药台使用移植后的专用配方表。白雏菊类把可用的石头/原木等物品输入加工成活石/活木；花药台按花瓣组合输出对应花。\n例如末影之焰配方使用 2 棕色、1 红色、1 淡灰色花瓣→1 末影之焰。移植的花药台/白雏菊配方为 100 EU/t、200 tick；不能把原生水池与种子操作直接套进工业机器。\n此移植花药台列表忽略原生种子试剂，缺少物品形式的配方等有跳过项。按 JEI 的工业分类选配方，不保证原生所有特殊配方都有工业版。',
          p('industrial_pure_daisy', 'mana_petal_apothecary'), ('loaders/recipes/BotaniaNativeRecipes.java',))
    quest('flowers', '末影之焰阵列：燃料→纯魔力', 'endoflame_array',
          '按结构预览搭建花阵列，输入总线放末影之焰花与有效熔炉燃料，配魔力输出池仓。花留在总线中作为并行规模，燃料转为燃烧 tick 缓存。\n每 tick speed=min(花数量,剩余燃烧 tick)，请求魔力 speed×3/2，并按成功输出扣燃料缓存。更多花提高处理速度，不意味着同一份燃料能凭花数无限倍增总产量。\n池仓满时停止产魔力；燃烧缓存持久化。将产出的纯魔力用于池、原生设备或魔力发电机，注意仓的输入输出方向。\n本任务检测控制器与一朵花；运行产物仍须自行检查池仓。',
          (*p('endoflame_array'), 'botania:endoflame'), ('common/machine/multiblock/botania/EndoflameArrayMachine.java', 'common/machine/multiblock/botania/EndoflameArrayPatterns.java'))
    quest('altar', '工业符文与魔力灌注', 'mana_rune_altar',
          '魔力符文祭坛和魔力灌注反应器承接专用配方。原生移植条目把 mana 数值编码成 EU/t，持续时间为 200×对应电压等级；不是把原生魔力总量平均分摊到 200 tick。\n例：风符文条目使用魔力粉、魔力钢、地毯、羽毛、线→2 风符文，编码数值为 5200 EU/t。先检查供电是否足够，不能只因有满魔力池就认定能运行。\n灌注条目需要催化器时以不消耗物品加入；手写 Pollution 配方可能另带真实魔力每 tick 成本，需按 JEI 和仓室提示区分。做两种控制器后选择一种可负担配方试产。',
          p('mana_rune_altar', 'mana_infusion_reactor'), ('loaders/recipes/BotaniaNativeRecipes.java', 'common/machine/multiblock/botania/BotaniaRecipeMaps.java'))
    quest('manaplate', '魔力板：加速工作中的 GT 机器', 'mana_plate',
          '铺 11×11 魔力板，按预览安装一个魔力输入池仓。扫描范围在控制器背面方向 5 格为中心、上方一层的 11×11 区域。把工作中的 GT 配方机器放在此区域。\n每台每 tick 耗 2^(速度−1) 魔力，额外推进 speed 点进度；速度上限由池仓档位决定，界面可调节。魔力不足会停止本 tick 后续机器的加速。\n这段逻辑针对 GT IRecipeLogicMachine；不能据此承诺加速 Create 动力装置或 Mekanism 方块实体。先少量机器试用，观察魔力消耗再扩建。',
          p('mana_plate'), ('common/machine/multiblock/botania/ManaPlateMachine.java', 'common/machine/multiblock/botania/ManaPlatePatterns.java'))
    quest('manaturbine', '超级魔力涡轮：专用流体燃料', 'mega_mana_turbine',
          '这是使用 MANA_TO_EU 的多方块，与单方块魔力发电机及 mega_mana_rotor_turbine 分开。必须输入对应燃料流体并配动力输出仓。\n基础燃料配方均输入 100 mB、输出 8192 EU/t：Infused Aura 持续 100 tick，Impuremana/WhiteMansus 各 3，BlackMansus 6，Starrymansus 12，RichAura 25，ErichAura 400。实际放大后的总耗料与功率看机器界面。\n连续运行会提高并行上限；催化剂对可提高输出上限，并在工作时周期消耗。先稳定燃料与输出，再探索黑/白魔素等催化组合，不把尚未获得的后期流体当开局供应。',
          p('mega_mana_turbine'), ('loaders/recipes/ManaToEuRecipes.java', 'common/machine/multiblock/botania/MegaManaTurbineMachine.java'))

    quest('nodes', 'F · 节点工程：世界节点与封装节点', 'packaged_aura_node',
          '世界中的 TC4R 灵气节点提供 Vis 网络；Pollution 的封装灵气节点是携带属性的物品，供专门机器读取。两者不能不经配方就互相替代。\n封装节点记录等级 NodeTire、类型 NodeType，以及风/火/水/地/秩序/熵六种数值。生产机生成随机属性，清洗机降低熵，发电和聚变读取这些属性。\n建议 EV 及以后、已有稳定 Energy/Water/Aura/Order 流体供应再推进。本区两个分支分别讲生产→清洗→发电与高级消耗/转化，不代替 JEI 完整材料链。',
          evidence=('common/item/PackagedAuraNode.java', 'common/machine/multiblock/node/NodeProducerMachine.java'), check='读懂两种节点及六属性用途')
    quest('producer', '节点生产：EV 起的连续耗料', 'node_producer',
          '节点生产机至少需要 EV 输入电压，低于 EV 不运转。接输入能源仓、Infused Energy 流体输入与物品输出，按结构预览准备线圈、棱镜、玻璃和光束核心。\nEV 标称周期 30 秒，每工作 tick 扣 2048 EU 与 144 mB Infused Energy；按完整 600 tick 连续周期预算约 1,228,800 EU、86,400 mB 流体。定时相位会影响首次周期，不能把 144 mB 当作整颗节点成本。\n高档缩短秒数，但每 tick 流体成本翻倍递增；先算整周期而不是只看耗时。产出封装节点属性随机，及时清空输出，避免堵仓时定时/插入行为造成失败。\n本任务同时检查生产机和一颗封装节点，不限制随机 NBT 属性。',
          p('node_producer', 'packaged_aura_node'), ('common/machine/multiblock/node/NodeProducerMachine.java',))
    quest('nodeblast', '节点高炉：配方加工与节点燃烧', 'node_blast_furnace',
          '节点高炉接受普通高炉与锻炉炼金配方，仍受线圈温度和配方能源条件限制。当前结构已经允许物品/流体输入，旧教程“没有输入仓所以不可用”的结论过时。\n封装节点是额外消耗物：每个燃烧 600 tick；工作逻辑周期把 Order×10 转成 Infused Light、Entropy×10 转成 Infused Dark。先检查结构允许的仓室与流体去向，再投入贵重高品质节点。\n节点燃烧与普通配方投料是两件事，不能只放节点就期待获得 JEI 中任意高炉产物。检查输出容量，避免流体填充失败。',
          p('node_blast_furnace'), ('common/machine/multiblock/node/NodeBlastFurnaceMachine.java', 'common/machine/multiblock/node/NodeBlastFurnacePatterns.java'))
    quest('washer', '节点清洗：降低熵，保留节点', 'node_washer',
          '封装节点+144 mB Infused Water+一次输入电压量的 EU→原位降低节点的 EssenceEntropy，并清理附近 1 点 TC4R 咒波。每秒尝试一次。\n每次最多降低 max(25,线圈等级×电压等级×25) 熵，不低于 0。物品仍留在输入总线上，不是从输出槽吐出一颗全新的随机节点。\n低熵能减少节点发电的熵惩罚；但节点高炉会用熵产 Dark，所以先决定用途再清洗。它不清除工业污染，也不会给其他五种属性凭空加点。',
          p('node_washer'), ('common/machine/multiblock/node/NodeWasherMachine.java',))
    quest('tower', '中央灵气塔：Light / Dark / 星魔素', 'central_vis_tower',
          '成型后接 EU、输入 Infused Aura 与分开的流体输出仓。每秒有效操作维护费为一次输入电压量 EU+4 mB Aura。\n8 格内节点高于基础值的多余 vis→每点 10 mB Infused Light；附近清理到的 1 点 TC4R 咒波→10 mB Infused Dark。普通 Vis Provider 只补到基础容量，不能独自制造这部分超额 vis。\n无 Light/Dark 工作且通过平衡判定时，累计 400 tick 后可产星魔素，数量与能源等级/框架有关。当前版本已有输入仓和星魔素产出，不再沿用旧文档“未实现”的说法。\n输出填充不足并非所有操作都会回滚，准备充足空间；此塔清理的是 TC4R 咒波，不是把工业污染转换为 Dark。',
          p('central_vis_tower'), ('common/machine/multiblock/node/CentralVisTowerMachine.java', 'common/machine/multiblock/node/CentralVisTowerPatterns.java'))
    quest('nodegen', '封装节点发电：属性与维护', 'large_node_generator',
          '大型节点发电机把输入总线中的节点当持续能源，配动力输出仓，并供应 Infused Aura/Order 维护流体。等级、类型、火/秩序和熵会影响产能；熵≥240 时熵倍率降到 0。\nOminous 每秒额外增加 0.1 工业污染；Pure 清理 TC4R 咒波。Concussive 有烧毁概率，Voracious 在缺两种维护液时也可能烧毁。当前代码维护液不是所有节点发电的硬条件，但关系到特殊行为，不应据此宣称全部节点永久免费。\n另有 LuV～UHV 微型节点发电机：把封装节点放输入槽，只在节点仍在槽内时发电；移除后不会维持旧产能。\n本任务检测大型机；微型路线作为紧凑替代选择，依据实际电压和节点属性决定。',
          p('large_node_generator'), ('common/machine/multiblock/node/LargeNodeGeneratorMachine.java', 'common/machine/single/SmallNodeGeneratorMachine.java'))
    quest('fusion', '节点聚变：清洁度与启动缓存', 'luv_node_fusion_reactor',
          'LuV/ZPM/UV 节点聚变堆运行普通聚变和节点魔法聚变配方。输入配方物料、封装节点及所需 Light/Dark/Aura 维持流体，配合能源仓和输出仓。节点属性决定并行与每秒维持液需求。\n当前版本已经接入节点并行、工业污染≤4.2 的清洁度检查和聚变启动成本，不能再照旧教程说这些无效。玩家没有污染 HUD 也不代表满足 4.2 门槛，因为 HUD 要超过 10 才显示。\n内部启动容量=输入能源仓数量×2^(档位−6)×1000 万 EU。配方 eu_to_start 不得超过容量，还要先充够启动差额；持续运行耗电另算。\n最终验收：结构、能源、启动缓存、维持液、清洁度、输出空间逐项检查。此物品目标只证明取得 LuV 控制器，未自动验证聚变成功。',
          p('luv_node_fusion_reactor'), ('common/machine/multiblock/node/NodeFusionReactorMachine.java', 'common/machine/multiblock/MagicRecipeLogic.java'))


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


def class_strings(data):
    """Read JVM constant-pool UTF8 entries without loading or executing a mod."""
    if data[:4] != b'\xca\xfe\xba\xbe':
        raise ValueError('Not a class')
    size = int.from_bytes(data[8:10], 'big')
    pos, i, strings = 10, 1, set()
    lengths = {3: 4, 4: 4, 5: 8, 6: 8, 7: 2, 8: 2, 9: 4, 10: 4, 11: 4,
               12: 4, 15: 3, 16: 2, 17: 4, 18: 4, 19: 2, 20: 2}
    while i < size:
        tag = data[pos]
        pos += 1
        if tag == 1:
            n = int.from_bytes(data[pos:pos+2], 'big')
            pos += 2
            strings.add(data[pos:pos+n].decode('utf-8', errors='replace'))
            pos += n
        else:
            pos += lengths[tag]
            if tag in (5, 6):
                i += 1
        i += 1
    return strings


def verify_items(ids):
    evidence = {}
    with zipfile.ZipFile(JAR) as jar:
        machine_path = 'common/machine/PollutionMachines.java'
        item_path = 'common/item/PollutionItems.java'
        sources = {k: (JAVA / k).read_text(encoding='utf-8') for k in (machine_path, item_path)}
        constants = {k: class_strings(jar.read('meowmel/pollution/' + k[:-5] + '.class')) for k in sources}
        for ident in sorted(ids):
            ns, name = ident.split(':', 1)
            if ns != 'pollution':
                continue
            model = f'assets/pollution/models/item/{name}.json'
            assert model in jar.namelist(), f'Missing jar item model: {ident}'
            json.loads(jar.read(model))
            registration = name
            if name.startswith('lv_'):
                registration = name[3:]
            elif name == 'luv_node_fusion_reactor':
                registration = name
            found = []
            for path, source in sources.items():
                if registration in constants[path] and ('"' + registration + '"') in source:
                    found.append(path)
            if name == 'lv_aspect_tank':
                assert any(s.endswith('_aspect_tank') for s in constants[machine_path])
                assert '"_aspect_tank"' in sources[machine_path]
                found = [machine_path]
            assert found, f'No registration/class evidence: {ident}'
            evidence[ident] = dict(jar=JAR.name, model=model, registration=found)
    for ns in sorted({i.split(':')[0] for i in ids} - {'pollution'}):
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
            remaining = set(wanted)
            classes = {}
            for n in jar.namelist():
                if n.endswith('.class'):
                    found = remaining & class_strings(jar.read(n))
                    for item in found:
                        classes[item] = n
                    remaining -= found
                    if not remaining:
                        break
            assert not remaining, f'No compiled registry-name evidence: {remaining}'
            for name in wanted:
                evidence[f'{ns}:{name}'] = dict(jar=f.name, sha256=digest(f.read_bytes()),
                                              model=f'assets/{ns}/models/item/{name}.json', compiled_name=classes[name])
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

    chapter = dict(default_hide_dependency_lines=False, default_quest_shape='', filename='pollution',
                   group=GROUP, icon='pollution:lv_vis_generator', id=sid('chapter'), order_index=order,
                   quest_links=[], quests=[], title='&5Pollution&r · 魔法工业与污染治理')
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
    jar_hash = digest(JAR.read_bytes())
    installed_jar = ROOT / 'mods' / JAR.name
    assert installed_jar.is_file(), f'Pollution jar is not installed: {installed_jar}'
    assert digest(installed_jar.read_bytes()) == jar_hash, 'Installed Pollution jar differs from source build'
    item_evidence = verify_items(all_items)
    source_evidence = {}
    with zipfile.ZipFile(JAR) as jar:
        for rel in sorted({path for q in Q for path in q['evidence']}):
            f = JAVA / rel
            assert f.is_file(), f'Missing source: {rel}'
            compiled = 'meowmel/pollution/' + rel[:-5] + '.class'
            assert compiled in jar.namelist(), f'Missing compiled class: {rel}'
            source_evidence[rel] = dict(source_sha256=digest(f.read_bytes()), class_sha256=digest(jar.read(compiled)))
    config = (ROOT / 'config/pollution-common.toml').read_text(encoding='utf-8-sig')
    expected_config = {'enablePollution': 'true', 'enableTerrainConversion': 'true', 'enableExplosionPollution': 'true',
                       'effectThreshold': '10.0', 'pollutionDecayPerTick': '0.001', 'terrainConversionThreshold': '25.0',
                       'terrainConversionBudgetPerTick': '4', 'visGeneratorEuPerVis': '250',
                       'visGeneratorPollutionMultiplier': '0.1', 'mufflerPollutionMultiplier': '1.0',
                       'fluxScrubberMultiplier': '0.002', 'visProviderMultiplier': '0.05', 'fluxFuelCellFluxPerTick': '0.005'}
    for key, val in expected_config.items():
        assert re.search(r'^\s*' + key + r'\s*=\s*' + re.escape(val) + r'\s*$', config, re.M), f'Config changed: {key}; revise tutorial'
    # Reparse actual serialized candidate, not only the Python data model.
    comments = '# Generated by build_pollution_chapter.py; semantic IDs persisted in pollution_ids.json.\n'
    comments += ''.join('# ' + k + ' = ' + v + '\n' for k, v in sorted(ids.items()))
    encoded = (comments + dump(chapter) + '\n').encode('utf-8')
    parsed = SnbtParser(encoded.decode()).parse()
    assert parsed == chapter, 'Serialization changed structure'
    assert len(parsed['quests']) == len(Q)
    for spec, result in zip(Q, parsed['quests']):
        assert len(result['tasks']) == len(spec['items']) + bool(spec['check']), 'Lost multi-objective'
        assert [t['item'] for t in result['tasks'] if t['type'] == 'item'] == spec['items']
    combined = {**library, 'chapters/pollution.snbt': parsed}
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
                    ids=dict(sorted(ids.items())), pollution_jar_sha256=jar_hash,
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
