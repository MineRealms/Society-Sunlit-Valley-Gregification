"""Staged Sunlit manufacturing lessons; stable legacy objectives stay attached."""

import json
import math
from pathlib import Path

from industrial_quest_support import quest as q

HERE = Path(__file__).resolve().parent
TARGETS = json.loads((HERE / "industry-progression-manifest.json").read_text(encoding="utf-8"))["targets"]
ASSEMBLY_LINE = "77B7B1EDD19831E0"
LUV = "7033A24F37F9B9B9"
ZPM = "370FC1CDF5F9A9CC"
UV = "3CDA855A045A9F4D"
STATION = "468EEFD9D2F69014"
HPCA = "1D6CC3C7F6BE4055"
BANK = "42760D3A86EFDCA3"
MKII = "24366846FDA52CE3"


def lesson(key, title, icon, desc, deps=(), items=(), check=None, ext=()):
    return q(key, title, icon, (0, 0), desc, deps, items, check, ext)


def apply_progression(quests):
    old = {entry["key"]: entry for entry in quests}

    def update(key, *, title=None, desc=None, deps=None, ext=None):
        entry = old[key]
        if title is not None:
            entry["title"] = title
        if desc is not None:
            entry["desc"] = desc
        if deps is not None:
            entry["deps"] = list(deps)
        if ext is not None:
            entry["ext"] = list(ext)

    update("research", title="总图 | 神秘研究 × 格雷工业", desc=[
        "本章按 IV、LuV、ZPM、UV 至 UHV 展开。原生 TC4R 研究与魔法材料负责装配原核，GT 扫描仪/研究站与装配线负责最终制造；完成任务不会授予任何配方研究。",
        "IV/LuV 使用扫描仪与数据棒；ZPM 使用研究站、16 CWU/t 与数据球；UV 工业设施使用 64 CWU/t、数据模块和数据银行光学传输。UHV 虚空 MekaSuit 使用独立的觉醒灵宝样品与 32 CWU/t 数据球路线。每台机器或护甲都有独立研究数据。",
        "阶段不是只看电路：仍需虚空金属、原始珍珠衍生物、钋与原生研究。基础 T1 机器保持原路线；超越之钥的实际制造现已进入 IV 装配线。",
        "核燃料、点火与净发电验收见《GT 核工业》。本章所有物品目标均不扣物品；手动勾选仅记录调试结果。",
    ])
    update("tier2", deps=["tier1"], desc=[
        "完成原生 TRANSCENDENCE_KEY 研究后，T2 驱动/轴承/能量/场组件可走奥术工作台路线；这一步要求研究，不要求先制造完成超越之钥。",
        "保留 T1 原件与对应末影、下界、平衡、扭曲结晶体。首台精密组装机前，使用原生奥术配方和注魔配方启动，不必依赖尚未建成的精密机器。",
        "机器建成后可改用带源质的自动化路线。原生源质、vis 与研究条件仍全部有效。",
    ])
    update("mystic", deps=["crystals"], desc=[
        "完成 TRANSCENDENCE_KEY 研究，以晶体控制电路和平衡/扭曲/末影/下界结晶体进行注魔，制得神秘电路。",
        "这条原生注魔路线可用于启动首台精密组装机；不会要求先有工业矩阵或反物质。神秘电路、分阶段工业矩阵、玄相电路是不同物品。",
    ])
    update("assembler", title="&bIV | 首台精密组装机&r", deps=["key", "mystic", "tier2"], desc=[
        "先在 TC4R 注魔祭坛制造精密组装机装配原核，再进行 GT IV 装配。原核保留超越之钥、终极灌注工厂、晶格控制核心、机器人、传送核心、T2 组件、神秘电路与原生源质。",
        "首台原核不在精密组装机内制作，也不需要尚未出现的工业矩阵；按注魔配方启动即可。最终控制器需要本机独立的扫描数据。",
    ], ext=[])
    update("assembler_structure", title="&bIV | 精密组装结构与投运&r")
    update("ports", deps=["assembler_structure"])
    update("resources", deps=["ports"])
    update("precision_infusing", deps=["resources"])
    update("servo", deps=["precision_infusing"])
    update("field", deps=["precision_infusing"])
    update("phase", deps=["precision_infusing"])
    update("parallel", title="可选 | 基础 2× 并行", deps=["precision_infusing"])
    update("me_ports", title="&bIV | ME 通玄输入与输出&r", deps=["iv_matrix", "ports"], desc=[
        "ME 通玄输入与输出分别制造装配原核，再分别扫描和装配。两个方向可以互转，但普通通玄口不能直接升级成 ME 口以绕过制造。",
        "安装 tc_energy 与未安装时保留互斥的原核配方变体；物品 ID 相同。源质输入与 ME 物品物流仍需分别安排。",
        "先设过滤和库存阈值，再测试一份样板、一批输入和产物回网。ME 网络不会授予 TC4R 研究权限。",
    ])
    update("wireless", title="&dLuV | 通玄无线连接&r", deps=["me_ports"], ext=[LUV])
    update("xuanxiang", title="&cUV | 真正的玄相电路&r", deps=["sps"], desc=[
        "玄相电路原配方保持不变：神秘电路、高纯凯达林晶体、辐照晶体核心、虚空介电板各 1，加 100 单位 MEK 反物质，产出 1。",
        "它属于 UV 之后的终局材料；IV/LuV/ZPM 工业配方改用各自阶段的奥术工业矩阵，因此不会要求先用 SPS 反物质制造 SPS 的上游机器。",
        "矩阵只在指定原核配方中替代玄相电路，不会成为全局通用替代品。反物质装备与终局超越核心仍需原版玄相链。",
    ])
    update("pump", title="&dLuV | 工业泵与流体分流&r", deps=["luv_matrix", "servo"], desc=[
        "完成 INDUSTRIAL_PUMP 研究，精密组装原核后进行 LuV 扫描与装配。原核使用 LuV 工业矩阵，并保留电动泵、T2 组件、精密伺服、泵压腔与钢外壳。",
        "无过滤升级时使用水→盐水、盐水→锂路线；这是一台消耗资源和电力的流体加工设施，不是虚空免费水源。按机器预览布置泵压腔、观察窗和通玄口。",
        "先用普通口验证一批，分别观察水、盐水、锂和 FE 变化，再接入连续生产。",
    ])
    update("fluid_plant", title="&dLuV | 流体厂与氘氚&r", deps=["luv_matrix", "field"], desc=[
        "完成 FLUID_PROCESSING_PLANT 研究，精密组装原核后进行 LuV 扫描与装配。它与工业泵是可并行建设的设施，不要求先安装泵的过滤升级。",
        "重水→氘/氧气、液态锂→氚，运行时读取当前 MEK 对应配方。输入液体和输出 MEK 气体必须用对应接口，氧气也需出口。",
        "该厂不会自动制造预混 D-T；持续 D-T 混合仍需 ZPM GT 化反。TOKAMAK 的原生研究同时要求泵与流体厂研究。",
    ])
    update("tokamak", title="&6ZPM | 托卡马克 × GT MK II&r", deps=["coil"], ext=[MKII, ZPM], desc=[
        "完成 TOKAMAK 研究；它的原生父研究是 INDUSTRIAL_PUMP 与 FLUID_PROCESSING_PLANT。先制造磁线圈，再以 8 个成品磁线圈、LuV MEK 聚变控制器和原生组件精密组装控制器原核。",
        "最终 ZPM 装配线额外消耗恰好 1 台 GT MK II：gtceu:zpm_fusion_reactor。GT 原生 MK II 的更高阶电路与材料要求继续存在，不能只看本条配方的 ZPM 电压。",
        "控制器研究样品是磁约束单元，不额外吃第二台 MK II。磁线圈和控制器各有独立研究数据；环形结构、预热、D-T 供给和产物空间分别验收。",
    ])
    update("tokamak_run", deps=["tokamak"])
    update("plasma", deps=["tokamak_run"])
    update("crusher_materials", title="&bIV | 粉碎原核与衬里&r", deps=["iv_matrix", "servo"], ext=[], desc=[
        "工业粉碎机原核改用 IV 工业矩阵，保留终极粉碎工厂、耐磨衬里、精密伺服、T2 轴承与原生研究/源质。它已从电路门槛改为实际 IV 制造。",
        "先备齐原核和专用耐磨衬里，再用扫描数据和 IV GT 部件完成装配。不可用旧的直接控制器配方跳过装配线。",
    ])
    update("crusher", title="&bIV | 工业粉碎机&r", deps=["crusher_materials"], ext=[])
    update("refinery_materials", title="&6ZPM | 炼油原核与热衬&r", deps=["zpm_matrix", "plasma"], ext=[], desc=[
        "等离子炼油原核使用 ZPM 工业矩阵，并保留原先 MEK 冶炼/灌注设施、耐热衬里与磁约束组件。PLASMA_REFINERY 仍以 TOKAMAK 为父研究。",
        "原核、研究站成果、ZPM 装配部件、等离子流体是不同准备项。控制器造出不等于上游已持续供料。",
    ])
    update("refinery", title="&6ZPM | 等离子炼油厂&r", deps=["refinery_materials"], ext=[])
    update("tianxuan_materials", title="&6ZPM | 天选原核与腔体&r", deps=["zpm_matrix", "phase"], ext=[], desc=[
        "用 ZPM 工业矩阵和原有 MEK/天工材料精密组装天选原核；天选控制器需独立研究站数据球和 ZPM 装配线制造。",
        "专用天选腔体仍是实际结构成本。装配研究只允许制造控制器，不会代替 SAINTLY_ASCENSION 或机器内部配方的研究。",
    ])
    update("tianxuan", title="&6ZPM | 天选工业设施&r", ext=[])
    update("ore_materials", title="&cUV | 综合矿处理原核&r", deps=["xuanxiang", "uv_gate"], ext=[], desc=[
        "矿处理原核继续使用真正的玄相电路与完整 MEK 矿链设备，并保留原生 TC4R 研究和源质；此处不再使用前期矩阵替代。",
        "先做 UV 数据模块，再通过数据银行光学网络提供研究；最终装配还需 UV 电路标签、部件与液体，不能只插入一个 UV 电路完成。",
    ])
    update("ore_plant", title="&cUV | 综合矿处理终局工厂&r", ext=[])
    update("settings", deps=["research"])
    update("old_world", deps=["settings"], desc=[
        "defaultconfigs 只用于新世界；已有世界实际数值读取该存档 serverconfig。修改之后，新批次才采用新值，已预订的批次保留原数值。",
        "本次保留所有旧章节、任务与目标 ID。已造好的机器不会被收回；万象笼仅在新的法杖成型成功时消耗一枚 LuV 成型核心，已成型笼继续运行。",
        "新增装配原核需要客户端和服务器都完成更新并重启。现存物品与研究数据仍应按实际 ID 核对，任务勾选不代替数据载体。",
    ])
    update("troubleshooting", deps=["old_world"])

    quests += [
        lesson("iv_gate", "&bIV | 装配线制造平台&r", "gtceu:assembly_line", [
            "从这一层开始，高阶天工不再只检查一枚 GT 电路。魔法原核→研究数据→真实 GT 装配，三段都要完成。",
            "使用普通物品输入总线和流体输入仓。服务器启用了装配线物品/流体顺序；总线顺序按 JEI 摆放，数量、输出空间、能量和数据均需满足。",
            "普通电路按 #gtceu:circuits/iv 等标签匹配，同档其他电路有效；研究数据必须对应具体成品。",
        ], deps=["research"], items=["gtceu:assembly_line"], ext=[ASSEMBLY_LINE]),
        lesson("iv_research", "&bIV | 扫描仪与数据棒&r", "gtceu:iv_scanner", [
            "扫描仪投入 JEI 指定研究样品与空数据棒，消耗样品并生成带本条研究 ID 的数据棒；研究按真实机器时间和能量运行。",
            "把完成的数据棒放入装配线数据仓。空棒、其他机器的数据、缺失数据都不能开工；正确研究棒在装配时不消耗，可重复使用。",
            "IV 与 LuV 使用这条物理数据流程。FTBQ 完成状态、原生 TC4R 研究与 GT 数据分别负责不同条件。",
        ], deps=["iv_gate"], items=["gtceu:iv_scanner", "gtceu:data_stick"]),
        lesson("key", "&bIV | 制造超越之钥&r", "zmod:transcendence_key", [
            "原生 TC4R 注魔先制造钥匙装配原核，再用独立扫描成果和 IV 装配线制成超越之钥。扫描样品为银树杖芯。",
            "已完成 TRANSCENDENCE_KEY 研究不等于已有钥匙。钥匙让原有七星基础控制器进入相应强化模式，并用于精密组装与后续制造。",
        ], deps=["mystic", "iv_research"], items=["zmod:transcendence_key"]),
        lesson("iv_matrix", "&bIV | 无反物质工业矩阵&r", "society:industrial_matrix_iv", [
            "精密组装机投运后制造 IV 奥术工业矩阵，供粉碎、ME 通玄和 4× 并行等原核使用。它不要求反物质，也不消耗成品玄相电路。",
            "辐照晶体核心仍需要钋，虚空介电板仍含原始尘。前者来自核废料链，后者保留污染魔法的原始珍珠/原始微粒研究；不要把 IV 当作唯一条件。",
        ], deps=["precision_infusing"], items=["society:industrial_matrix_iv"]),
        lesson("parallel4", "&bIV | 独立制造 4× 并行&r", "zmod:precision_assembler_parallel_4x", [
            "4× 模块独立走原核、扫描、IV 装配；2× 基础模块不会自动绕过这道工艺。精密组装机只能有一个并行口。",
            "更大批次同步增加原料、资源预留和电力需求。没有新增 8× 至 256× 的生存配方。",
        ], deps=["iv_matrix"], items=["zmod:precision_assembler_parallel_4x"]),
        lesson("luv_gate", "&dLuV | 自动化设施升级&r", "gtceu:luv_robot_arm", [
            "LuV 最终装配使用 LuV 部件、电路标签、焊锡合金、润滑油和聚苯并咪唑；仍由扫描仪生成每台机器的数据棒。",
            "泵与流体厂、太乙矩阵、样板/无线、线程与万象成型进入本阶段。原生研究照常保留，不会因为装配完成而自动解锁。",
        ], deps=["iv_matrix"], check="已核对 LuV 材料与扫描仪平台", ext=[LUV]),
        lesson("luv_matrix", "&dLuV | LuV 工业矩阵&r", "society:industrial_matrix_luv", [
            "LuV 工业矩阵保留辐照核心和虚空介电板等魔法材料，以 LuV 工业部件替代这条指定配方的反物质瓶颈。",
            "用于 LuV 设施原核，不能替代 ZPM 矩阵，也不能全局替代玄相电路。",
        ], deps=["luv_gate"], items=["society:industrial_matrix_luv"]),
        lesson("taiyi", "&dLuV | 太乙矩阵&r", "zmod:taiyi_matrix", [
            "先用带 IV 钥匙的穹历达到功能 T2，取得太乙专属研究手稿；再按原生祭坛配方制造原核，经 LuV 装配得到太乙矩阵。",
            "研究所需机器功率与 GT 装配电压不是同一指标。太乙成型保留原有结构与法杖要求，不会从普通符文矩阵免费升级出成品。",
        ], deps=["luv_matrix"], items=["zmod:taiyi_matrix", "zmod:transcendence_key"], ext=[LUV]),
        lesson("pattern", "&dLuV | 通玄样板供应器&r", "zmod:tongxuan_pattern_provider", [
            "以 ME 通玄输入口等原料注魔为原核，再用 LuV 研究数据和装配线制成样板供应器。无 tc_energy 的环境同样有对应原核路线。",
            "先验证单配方与回网，再上大订单。供应器不是自动补研究、跨区块强加载或无限资源入口。",
        ], deps=["me_ports"], items=["zmod:tongxuan_pattern_provider"], ext=[LUV]),
        lesson("thread", "&dLuV | 2× 线程仓&r", "zmod:thread_hatch_2x", [
            "2× 线程仓的原核和 LuV 装配独立制作。线程数与单批并行倍率是两种能力，分别检查机器允许的仓口、线程和供电。",
            "本次没有为更高注册倍率新增便宜生存配方；以当前机器支持和 JEI 实际配方为准。",
        ], deps=["iv_matrix"], items=["zmod:thread_hatch_2x"], ext=[LUV]),
        lesson("wanxiang", "&dLuV | 万象笼成型核心&r", "society:wanxiang_formation_core", [
            "用原生愤怒之笼、已完成的 IV 超越之钥与 LuV 工业材料，通过扫描仪和装配线制造一枚万象笼成型核心。",
            "核心放在操作者背包。法杖成型仍检查 WANXIANG_CAGE 研究、原生笼结构和 vis；仅成型成功消耗 1 枚，缺研究、缺 vis、结构错误均不扣核心。",
            "已成型的旧笼继续工作，拆除后重新成型需新核心。一次性核心不是每次刷怪燃料；刷怪仍消耗原有资源与 FE。",
        ], deps=["luv_matrix"], items=["society:wanxiang_formation_core", "zmod:transcendence_key"], ext=[LUV]),
        lesson("mek_fusion", "&dLuV | MEK 聚变控制器&r", "mekanismgenerators:fusion_reactor_controller", [
            "用聚变框架、玻璃、化学储罐等原料制作 LuV 聚变原核，再用扫描数据与 LuV 装配线制造控制器。保留钋及原生部件成本。",
            "这台控制器同时是后续天工托卡马克原核材料。分离供氘氚与点火见核工业；持续燃烧上限仍为 2 mB/t。",
        ], deps=["iv_matrix"], items=["mekanismgenerators:fusion_reactor_controller"], ext=[LUV]),
        lesson("zpm_gate", "&6ZPM | 研究站与 16 CWU/t&r", "gtceu:research_station", [
            "研究站投入指定样品和空数据球。光学计算网络必须提供至少 16 CWU/t，同时保持电力、样品架和冷却有效，才能产生本机研究成果。",
            "由 HPCA 提供计算，经光学计算仓/网络分配给研究站；数据球是物理成果，不是任务奖励或免费解锁。正确数据球供装配线重复使用。",
            "电路、材料、研究站制造本身继续使用 GT 原有门槛；现成 GT 附属机器不会免除这些条件。",
        ], deps=["luv_gate"], items=["gtceu:research_station"], check="研究站可持续取得 16 CWU/t", ext=[ZPM, STATION, HPCA]),
        lesson("zpm_matrix", "&6ZPM | ZPM 工业矩阵&r", "society:industrial_matrix_zpm", [
            "此矩阵用于托卡马克、磁线圈、天选、炼油及相应高阶原核。它延续魔法材料链，以 ZPM 工业投入解除反物质前置。",
            "原核完成后仍须研究站、每机独立数据球及最终装配；矩阵不等于成品控制器。",
        ], deps=["zpm_gate"], items=["society:industrial_matrix_zpm"]),
        lesson("coil", "&6ZPM | 托卡马克磁线圈&r", "zmod:tokamak_magnetic_coil", [
            "磁线圈原核精密配方按原生批量给出 4 枚原核，每枚再装配 1 个成品线圈；不要把原核批量误读成控制器成本已降低。",
            "线圈不依赖已建成的托卡马克。先完成线圈独立研究与装配，再给控制器原核备 8 个成品线圈。",
        ], deps=["zpm_matrix"], items=["zmod:tokamak_magnetic_coil", "zmod:magnetic_confinement_unit"]),
        lesson("warped", "&6ZPM | 扭曲聚合器&r", "zmod:warped_polymerizer_controller", [
            "完成对应 TC4R 研究，以原有精密配方制造原核，再通过 ZPM 研究站和装配线制造控制器。",
            "保留其原生物品、化学品与源质输入；GT 工艺是新增的一段制造成本，不会抹掉魔法工艺。",
        ], deps=["zpm_matrix"], items=["zmod:warped_polymerizer_controller"]),
        lesson("yaoguang", "&6ZPM | 瑶光工业设施&r", "zmod:yaoguang_controller", [
            "瑶光控制器同样进入 ZPM 原核→研究站→装配线。源质、化学品和原生研究保持，机壳不能单独运行控制器功能。",
            "先按原生结构说明投运，再检查输入、能量和产物；制造研究成果不替代机器内部配方权限。",
        ], deps=["zpm_matrix"], items=["zmod:yaoguang_controller"]),
        lesson("uv_gate", "&cUV | 64 CWU/t 与数据银行&r", "gtceu:data_bank", [
            "UV 各目标使用 64 CWU/t 研究站配方和空数据模块。算力不足或样品/电力条件不满足时，不会得到可用成果。",
            "研究完成的数据模块放入运行中的数据银行，经光学数据网络接入装配线的光学数据接收仓。普通数据仓不能直接读模块；计算网络与数据网络各司其职。",
            "数据模块不能复制降级成数据球/数据棒以绕过数据银行；同模块复制仍可用。空模块、错研究 ID 或断开光学数据都会阻止新批次。",
        ], deps=["zpm_gate"], items=["gtceu:data_bank", "gtceu:data_module"], check="已验证 64 CWU/t 及银行→装配线光学数据", ext=[UV, BANK]),
        lesson("sps", "&cUV | 先建 SPS，再有反物质&r", "mekanism:sps_casing", [
            "SPS 机壳和超级充能线圈各有原核、独立 64 CWU/t 研究和 UV 装配。机壳每枚原核对应 4 个成品；不是原先的普通组装机路线。",
            "原核保留钋、钚、HDPE、激光/铜等输入，但不要求反物质、玄相电路或终局超越核心，因此不存在自举循环。",
            "先确保钋气体和持续供电，再产反物质；完整核电、功率和供料验收见核工业。",
        ], deps=["uv_gate"], items=["mekanism:sps_casing", "mekanism:supercharged_coil"]),
        lesson("transcendence_core", "&cUV | 超越核心与终局材料&r", "zmod:transcendence_core", [
            "超越核心保留真正的反物质粒、原始结核、神秘锭与原生源质。先通过 SPS 建立反物质链，再注魔原核、完成 UV 研究并装配。",
            "这枚核心与一次性万象成型核心、GT 研究数据不是同一种物品。不同机器不得混用同名核心。",
        ], deps=["xuanxiang"], items=["zmod:transcendence_core"]),
        lesson("tianshu_t3", "&cUV | 天枢至高控制器&r", "zmod:tianshu_controller_t3", [
            "基础天枢与 IV 钥匙强化模式保留；独立 T3 控制器需原生至高研究、原核、UV 研究站及装配线。",
            "依原生结构和研究书完成最终升级，不能用基础外壳或一枚钥匙冒充独立 T3 控制器。",
        ], deps=["transcendence_core"], items=["zmod:tianshu_controller_t3"]),
        lesson("yuheng_t3", "&cUV | 玉衡至高控制器&r", "zmod:yuheng_controller_t3", [
            "玉衡 T3 需要其原生至高研究与超越核心链；保留源质和魔法材料，再完成 UV 数据模块研究与最终装配。",
            "玉衡源质有 MEK 富集铁/钢等前期来源，不要求用已造出的同一 T3 控制器生产自身源质。",
        ], deps=["transcendence_core"], items=["zmod:yuheng_controller_t3"]),
        lesson("qiongli_t3", "&cUV | 穹历至高控制器&r", "zmod:qiongli_controller_t3", [
            "先用 IV 钥匙达到穹历功能 T2，完成穹历至高专属研究及相应远古研究，再制作原核并走 UV 研究与装配。",
            "完成 T3 后才具备奇点提取器专属研究所需的穹历等级。功能 T2、研究手稿与最终 T3 实物是三步。",
        ], deps=["transcendence_core"], items=["zmod:qiongli_controller_t3"]),
        lesson("reconstructor", "&cUV | 物质重构器&r", "zmod:matter_reconstructor_controller", [
            "原核保留原生精密配方和终局材料；最终控制器需要独立 UV 数据模块与装配线，不复用矿处理厂或 SPS 数据。",
            "先核实选定物质路线的实际输入、产出和 FE 需求，再接自动化；更高档控制器不会让物质凭空产生。",
        ], deps=["transcendence_core"], items=["zmod:matter_reconstructor_controller"]),
        lesson("singularity", "&cUV | 奇点提取器&r", "zmod:singularity_controller", [
            "先建成穹历 T3，取得奇点专属手稿，再按 SINGULARITY_EXTRACTOR 研究制作原核并完成独立 UV 数据研究和装配。",
            "奇点源质可由 MEK 传送核心等既有来源提供，不需要先用奇点提取器制造它自己。仍需真实末端材料、源质与电力。",
        ], deps=["qiongli_t3"], items=["zmod:singularity_controller"]),
        lesson("void_pylon", "&cUV | 虚空信标&r", "zmod:void_pylon_beacon", [
            "虚空信标为独立高阶设施，按原生配方制造原核，使用自己的 UV 数据模块和装配配方。",
            "范围、资源和运行条件按实际结构及配置检查；它不是因为占地小就保留免费直接制造。",
        ], deps=["transcendence_core"], items=["zmod:void_pylon_beacon"]),
    ]
    seen = {}
    for entry in quests:
        for item in entry["items"]:
            seen.setdefault(item, entry)
    fallback_labels = {
        "mekanismgenerators:fusion_reactor_controller": ("mek_fusion", "LuV | MEK 聚变控制器"),
        "mekanism:sps_casing": ("sps", "UV | SPS 机壳"),
        "mekanism:supercharged_coil": ("sps", "UV | SPS 超级充能线圈"),
        "zmod:matter_reconstructor_controller": ("reconstructor", "UV | 物质重构器"),
        "zmod:tianshu_controller_t3": ("tianshu_t3", "UV | 天枢至高控制器"),
        "zmod:yuheng_controller_t3": ("yuheng_t3", "UV | 玉衡至高控制器"),
        "zmod:qiongli_controller_t3": ("qiongli_t3", "UV | 穹历至高控制器"),
        "zmod:singularity_controller": ("singularity", "UV | 奇点提取器"),
        "zmod:void_pylon_beacon": ("void_pylon", "UV | 虚空信标"),
        "zmod:tokamak_magnetic_coil": ("coil", "ZPM | 托卡马克磁线圈"),
        "zmod:tokamak_controller": ("tokamak", "ZPM | 托卡马克"),
        "zmod:industrial_crusher_controller": ("crusher", "IV | 工业粉碎机"),
        "zmod:industrial_pump_controller": ("pump", "LuV | 工业泵"),
        "zmod:fluid_processing_plant_controller": ("fluid_plant", "LuV | 流体处理厂"),
        "zmod:integrated_ore_processing_plant_controller": ("ore_plant", "UV | 综合矿处理厂"),
        "zmod:precision_assembler_controller": ("assembler", "IV | 精密组装机"),
        "zmod:transcendence_key": ("key", "IV | 超越之钥"),
        "zmod:taiyi_matrix": ("taiyi", "LuV | 太乙矩阵"),
        "zmod:warped_polymerizer_controller": ("warped", "ZPM | 扭曲聚合器"),
        "zmod:yaoguang_controller": ("yaoguang", "ZPM | 瑶光设施"),
        "zmod:tianxuan_controller": ("tianxuan", "ZPM | 天选设施"),
        "zmod:plasma_refinery_controller": ("refinery", "ZPM | 等离子炼油厂"),
        "zmod:thread_hatch_2x": ("thread", "LuV | 2x 线程仓"),
        "zmod:tongxuan_pattern_provider": ("pattern", "LuV | 通玄样板供应器"),
        "zmod:tongxuan_wireless_connector": ("wireless", "LuV | 通玄无线连接器"),
        "zmod:precision_assembler_parallel_4x": ("parallel4", "IV | 4x 并行模块"),
        "society:wanxiang_formation_core": ("wanxiang", "LuV | 万象笼成型核心"),
    }
    tier_deps = {"iv": "iv_matrix", "luv": "luv_matrix", "zpm": "zpm_matrix", "uv": "uv_gate"}
    for target in TARGETS:
        product = target["target"]
        if product not in seen:
            key, label = fallback_labels.get(
                product, ("machine_" + product.replace(":", "_").replace("/", "_"), product))
            tier = target["tier"]
            desc = [
                f"{product} 是 {tier.upper()} 阶段高阶制造目标。先完成天工精密组装的原生配方/研究，再制造这台机器自己的装配原核。",
                f"原核后走 GT 研究与装配线最终制造。电压为 {target['EUt']:,} EU/t，时长 {target['duration']} ticks；研究样品 {target['research']['sample']}，使用 #gtceu:circuits/{tier} 同档电路。",
            ]
            mode = ("扫描仪数据棒" if target["research"]["type"] == "scanner" else
                    "研究站数据模块（64 CWU/t）" if tier == "uv" else
                    "研究站数据球（16 CWU/t）")
            desc.append("该目标使用" + mode + "，研究成果不能由任务勾选或另一台机器的研究代替。")
            entry = lesson(key, "&" + {"iv": "b", "luv": "d", "zpm": "6", "uv": "c"}[tier] +
                           label.split("|", 1)[-1] + "&r", product, desc,
                           deps=[tier_deps[tier]], items=[product])
            quests.append(entry)
            old[key] = entry
            seen[product] = entry
        entry = seen[product]
        tier = target["tier"].upper().replace("LUV", "LuV")
        sample = target["research"]["sample"]
        mode = "扫描仪数据棒" if target["research"]["type"] == "scanner" else (
            "研究站数据模块（64 CWU/t）" if target["tier"] == "uv" else "研究站数据球（16 CWU/t）")
        entry["desc"].append(
            f"{product}：{tier} 装配线，{target['EUt']:,} EU/t，{target['duration']} ticks；研究方式：{mode}，消耗样品 {sample}。电路接受 #gtceu:circuits/{target['tier']} 同档标签。")
        if product not in entry["items"]:
            entry["items"].append(product)
        if target.get("core") and target["core"] not in entry["items"]:
            entry["items"].append(target["core"])
    old["tokamak"]["items"].extend(["gtceu:zpm_fusion_reactor", "mekanismgenerators:fusion_reactor_controller"])
    quests.append(lesson("uhv_void_suit", "&4UHV | 虚空 MekaSuit 终端制造&r", "zmod:void_mekasuit_bodyarmor", [
        "四件虚空 MekaSuit 分别走 GT 装配线，电压 1,966,080 EU/t（UHV）。每条都消耗对应 MEK 原装护甲、UHV 电路标签、中子素装甲、硅岩合金和魔法材料；旧直接注魔配方已移除。",
        "四份研究必须逐件完成：觉醒灵宝兜帽、长袍、护腿、靴子各自作为研究站样品，并分别配一个空数据球。研究会消耗样品；任意一份成果不能代替另三份。",
        "研究电压 UV、32 CWU/t，数据球写好后放入装配线数据仓，装配时不消耗。研究耗时按部位为 200/300/250/200 秒；装配为 120/180/150/120 秒。",
        "升级继承投入 MEK 护甲的模块、储能、附魔和自定义名称。天工禁止的重力/喷气模块仍受原有规则限制。数据球不存放在材料输入总线里。",
    ], deps=["transcendence_core"], check="已准备 UHV 装配电源与四份独立的数据球研究", ext=[STATION]))
    armor = [
        ("helmet", "冠冕：感知与控制", "兜帽", "4 个 UV 传感器、4 个 UV 发射器、2 个 UV 力场发生器，8 个 UHV 电路。"),
        ("bodyarmor", "躯壳：屏障与储能", "长袍", "4 个 UV 力场发生器、终极能量立方、4 个 UV 电机与反物质，16 个 UHV 电路。"),
        ("pants", "胫甲：动力与相位", "护腿", "8 个 UV 电机、4 个 UV 活塞、2 个 UV 力场发生器与相位耦合器，12 个 UHV 电路。"),
        ("boots", "战履：机动与定位", "靴子", "4 个 UV 电机、4 个 UV 活塞、2 个 UV 传感器与传送核心，8 个 UHV 电路。"),
    ]
    for part, title, sample, materials in armor:
        quests.append(lesson("void_suit_" + part, "&4UHV | " + title + "&r", "zmod:void_mekasuit_" + part, [
            "先以觉醒灵宝" + sample + "完成本部位独立研究，使用写入对应成果的数据球。空球或其它护甲的研究球不能启动这条配方。",
            "专用部件：" + materials + "中子素、魔法防具和其它材料数量以 JEI 装配线页面为准，按总线顺序逐项投入。",
            "先拆除不需要的模块或确认保留内容，再投入对应部位的 MEK 护甲。装配后核对模块、附魔和储能，并用 UHV 或更高等级 GT 充电器补能。",
        ], deps=["uhv_void_suit"], items=["zmod:void_mekasuit_" + part]))
    compact_layout(quests)
    return quests


def compact_layout(quests):
    """Rank the DAG, then place each node clear of prior lines and nodes."""
    graph = {entry["key"]: entry for entry in quests}
    ranks, visiting = {}, set()

    def rank(key):
        if key in ranks:
            return ranks[key]
        if key in visiting:
            raise ValueError("Quest cycle: " + key)
        visiting.add(key)
        value = max((rank(dep) + 1 for dep in graph[key]["deps"]), default=0)
        visiting.remove(key)
        ranks[key] = value
        return value

    lanes = {
        "settings": -5, "old_world": -5, "troubleshooting": -5,
        "iv_gate": -2, "iv_research": -2, "key": -2,
        "crystals": 0, "tier1": 0, "tier2": 0, "mystic": 2,
        "servo": -2, "field": 2, "phase": 4, "parallel": -4,
        "parallel4": -4, "me_ports": -6, "pattern": -6, "wireless": -8,
        "crusher_materials": 2, "crusher": 2, "crusher_run": 2,
        "luv_gate": 0, "luv_matrix": 0, "taiyi": -4, "thread": -2,
        "wanxiang": -10, "mek_fusion": 0,
        "pump": 4, "pump_filter": 6, "fluid_plant": 2,
        "zpm_gate": -2, "zpm_matrix": -2,
        "coil": 0, "tokamak": 2, "tokamak_run": 2, "plasma": 2,
        "refinery_materials": 2, "refinery": 2, "refinery_run": 2,
        "tianxuan_materials": -2, "tianxuan": -2, "tianxuan_run": -2,
        "warped": -4, "yaoguang": -6,
        "uv_gate": -10, "sps": -10, "xuanxiang": -10,
        "transcendence_core": -10, "qiongli_t3": -10, "singularity": -10,
        "tianshu_t3": -14, "yuheng_t3": -12, "reconstructor": -8, "void_pylon": -6,
        "ore_materials": -4, "ore_plant": -4, "ore_routes": -4,
        "uhv_void_suit": -18, "void_suit_helmet": -22, "void_suit_bodyarmor": -20,
        "void_suit_pants": -18, "void_suit_boots": -16,
    }
    placed = []
    for entry in sorted(quests, key=lambda item: (rank(item["key"]), quests.index(item))):
        x = round(rank(entry["key"]) * 1.8, 1)
        preferred = lanes.get(entry["key"], 0)
        candidates = [preferred + offset for step in range(2001)
                      for offset in ((0.0,) if step == 0 else (-step * 0.5, step * 0.5))]

        def incoming_crossings(y):
            total = 0
            end = (x, y)
            for dep in entry["deps"]:
                start = graph[dep]["xy"]
                dx, dy = end[0] - start[0], end[1] - start[1]
                length_sq = dx * dx + dy * dy
                for other in placed:
                    if other["key"] == dep:
                        continue
                    ox, oy = other["xy"]
                    t = ((ox - start[0]) * dx + (oy - start[1]) * dy) / length_sq
                    if 0 < t < 1 and math.dist((ox, oy), (start[0] + t * dx, start[1] + t * dy)) < 0.65:
                        total += 1
            # A newly placed node must also stay clear of every edge already drawn.
            point = (x, y)
            for child in placed:
                for dep in child["deps"]:
                    if dep not in graph:
                        continue
                    start = graph[dep]["xy"]
                    finish = child["xy"]
                    dx, dy = finish[0] - start[0], finish[1] - start[1]
                    length_sq = dx * dx + dy * dy
                    t = ((point[0] - start[0]) * dx + (point[1] - start[1]) * dy) / length_sq
                    if 0 < t < 1 and math.dist(point, (start[0] + t * dx, start[1] + t * dy)) < 0.65:
                        total += 1
            return total

        for y in candidates:
            if any(math.dist((x, y), other["xy"]) < 1.8 for other in placed):
                continue
            if incoming_crossings(y) == 0:
                entry["xy"] = (x, round(y, 1))
                placed.append(entry)
                break
        else:
            zeros = [y for y in candidates if incoming_crossings(y) == 0]
            blockers = [(y, other["key"], math.dist((x, y), other["xy"]))
                        for y in zeros[:5] for other in placed
                        if math.dist((x, y), other["xy"]) < 1.8]
            free = [y for y in candidates if all(math.dist((x, y), other["xy"]) >= 1.8 for other in placed)]
            raise ValueError("Cannot place quest without crossing a prior node: " + entry["key"] +
                             " rank=" + str(rank(entry["key"])) + " deps=" + repr(entry["deps"]) +
                             " nearest=" + repr(min((incoming_crossings(y), y) for y in candidates)) +
                             " zeros=" + repr(len(zeros)) + " blockers=" + repr(blockers) +
                             " best_free=" + repr(min((incoming_crossings(y), y) for y in free)))
