#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HXTG practical chapter; verified against 1.40.03 recipes, structures and settings.

The four controller milestones migrate from gt_nuclear_industry with every old
quest and item-task ID intact. Checkmark tasks document manual commissioning;
they do not grant Thaumcraft research or bypass recipe conditions.
"""

from industrial_quest_support import quest as q, run

EV = "7A55CC71442CC854"
LUV = "7033A24F37F9B9B9"
ZPM = "370FC1CDF5F9A9CC"
UV = "3CDA855A045A9F4D"

PRESERVED = {
    "quest/crusher": "1B5DF2BB27287255",
    "task/crusher/item/zmod:industrial_crusher_controller": "5DA756559C3DC19B",
    "task/crusher/item/zmod:crusher_wear_lining": "0441AF7B50830FD6",
    "quest/refinery": "23654BEC29AA7E78",
    "task/refinery/item/zmod:plasma_refinery_controller": "3BC52810EC437AA1",
    "task/refinery/item/zmod:refinery_heat_lining": "3F7234B83039CA26",
    "quest/tianxuan": "445BAB57B40BC70A",
    "task/tianxuan/item/zmod:tianxuan_controller": "07E790FD1925B328",
    "task/tianxuan/item/zmod:tianxuan_chamber": "714FECC9F44F12ED",
    "quest/ore_plant": "536076EF8FB42373",
    "task/ore_plant/item/zmod:integrated_ore_processing_plant_controller": "35DB9102AA5AADD7",
    "task/ore_plant/item/zmod:ore_processing_chamber": "54B05A1889668DF6",
}

Q = [
    q("research", "天工总图：研究与工业要同时准备", "zmod:configurator_focus", (0, 0), [
        "本章独立描述秽玄天工的材料、研究、精密制造、通玄物流与工业设施。核电站的燃料和净发电验收见《GT 核工业》，天工建设不要求先勾完那条任务线。",
        "在 TC4R 研究书从 FIRST_INSIGHT 推进至 TRANSCENDENCE_KEY；精密组装机研究 PRECISION_ASSEMBLER 的父节点是 TRANSCENDENCE_KEY，工业粉碎/天选/矿处理/泵/流体厂需要 SAINTLY_ASCENSION。",
        "研究条件和 GT 电路标签门槛同时生效。粉碎 EV、炼油 LuV、天选 ZPM、矿处理 UV 只表示控制器最低电路档位，不表示整个材料链在该阶段都已可得。",
        "这里的手动勾选只记录你做过的检查，不会赠送研究、材料或结构。所有物品目标都不消耗物品。",
    ], items=["zmod:configurator_focus"], check="已在研究书核对天工的制造与工业研究位置"),
    q("crystals", "晶体材料：先建立分流库存", "zmod:high_purity_kaydarin_crystal", (4, 0), [
        "凯达林晶体在 MEK 富集仓中成为高纯凯达林晶体；原子合金与对应凯达林灌注资源制造晶体导电合金。分别看 JEI 中的物品输入和灌注资源。",
        "平衡、扭曲、末影、下界结晶体是不同材料，后续分别用于能量、场、驱动、轴承组件。不要把名字相似的结晶体统一丢进同一条无过滤管道。",
        "先制作样品确认物品 ID/资源类别，再备批量库存。灌注材料与流体、气体、源质并不是可互换的四个名字。",
    ], deps=["research"], items=["zmod:high_purity_kaydarin_crystal", "zmod:crystal_conductive_alloy"]),
    q("tier1", "基础组件：驱动、轴承与能量", "zmod:drive_unit_t1", (8, 0), [
        "按 JEI/研究书准备 T1 驱动单元、轴承单元、能量耦合器和场发生器。先手工完成基础链，给 T2 升级保留对应 T1 原件。",
        "不同组件承担不同用途：机械件进入伺服与耐磨衬里，能量/场组件进入磁约束和相位耦合。不要只囤电路而忽视结构部件。",
        "一开始不必追求并行；用一套完整物料链做出首台精密组装机，后面再迁移自动化配方。",
    ], deps=["crystals"], items=["zmod:drive_unit_t1", "zmod:bearing_unit_t1", "zmod:energy_coupler_t1", "zmod:field_generator_t1"]),
    q("tier2", "T2 升级：保留四种结晶体分工", "zmod:drive_unit_t2", (12, 0), [
        "TRANSCENDENCE_KEY 下的奥术升级用 T1 原件、下界合金锭和相应结晶体：驱动用末影，轴承用下界，能量耦合器用平衡，场发生器用扭曲。",
        "四种 T2 组件当前奥术配方都要求 ordo 16、terra 16、aer 8 的 vis；具体摆法看研究书。物品齐全但研究/法杖资源不足，仍不能制作。",
        "精密组装机建成后有带源质的等价自动化路线；首台机器前仍要保留可手工启动的制作方法。",
    ], deps=["tier1"], items=["zmod:drive_unit_t2", "zmod:bearing_unit_t2", "zmod:energy_coupler_t2", "zmod:field_generator_t2"]),
    q("mystic", "神秘电路：首台机器前的注魔", "zmod:mystic_circuit", (16, 0), [
        "TRANSCENDENCE_KEY 下，以晶体控制电路为中心，配平衡、扭曲、末影、下界结晶体进行 TC 注魔，得到神秘电路。",
        "当前配方不稳定度 2，源质需求 ordo 16、machina 16、praecantatio 16、vinculum 8。先按 TC 注魔规则安排稳定性、基座与源质供给。",
        "它和玄相电路不是同一个物品；后者还需要反物质等材料。先保留神秘电路用于精密组装机控制器，避免把启动材料全部投入后续配方。",
    ], deps=["tier2"], items=["zmod:mystic_circuit"]),
    q("assembler", "精密组装机控制器：先注魔启动", "zmod:precision_assembler_controller", (20, 0), [
        "完成 PRECISION_ASSEMBLER 研究。控制器是 TC 注魔配方，中心为晶格控制核心，组件含终极灌注工厂、超越之钥、机器人、传送核心、T2 驱动/轴承和两块神秘电路。",
        "当前控制器不稳定度 5；源质为 machina 96、ordo 64、vinculum 48、praecantatio 32、motus 32、cognitio 32。逐项备料后再启动。",
        "首台控制器不是在尚未建成的精密组装机里制造。JEI 页面存在不代表玩家已经完成研究或能绕过注魔条件。",
    ], deps=["mystic"], items=["zmod:lattice_control_core", "zmod:precision_assembler_controller"]),
    q("assembler_structure", "精密组装机结构：5×4×5", "zmod:precision_assembler_window", (24, 0), [
        "按 5×4×5 外框建立：基础方案含 75 个框架位置、6 个观察窗、1 个控制器和 18 个内部空气格。框架使用高级机器框架，观察窗不能用普通玻璃代替。",
        "两侧共 8 个指定框架位置可放通玄/样板/并行接口；其余框架、前方观察窗和内部空气不能随意改。端口替换会减少所需框架数量。",
        "按研究书或机器预览核对朝向和缺失位置，先形成空结构，再接物流。结构跨未加载区块会显示未就绪，不应靠自动强加载掩盖布置错误。",
    ], deps=["assembler"], items=["zmod:advanced_machine_frame", "zmod:precision_assembler_window"], check="结构形成、朝向和内部空气已核对"),
    q("ports", "通玄基本口：输入与输出是两种方向", "zmod:tongxuan_input_port", (28, 0), [
        "在允许的结构口位置放通玄输入口与输出口。输入口接收原料/能量，输出口供外部提取产物；输出口拒绝外部插入是正常设计。",
        "先测试投入少量同种物品，再尝试 17 个或一组，并从输出提取；同物品不同数量应能合并，NBT 不同的物品不能随意视为同一种。",
        "端口必须绑定已形成的结构，不能由两个控制器共享。插上管道而控制器没有识别该位置时，不会凭空获得资源访问。",
    ], deps=["assembler_structure"], items=["zmod:tongxuan_input_port", "zmod:tongxuan_output_port"]),
    q("resources", "四类输入：物品、化学品、流体、源质", "zmod:precision_assembler_controller", (32, 0), [
        "精密组装配方支持最多 16 种物品输入、4 种 MEK 化学品输入和 32 种源质输入。各类上限分别计算，不是把源质和流体也挤进四种通用资源里。",
        "逐条分清 JEI 的 ingredient、chemical_inputs 与 essentia_inputs：MEK 气体/灌注资源走对应能力，TC 源质走源质接口，普通流体不能直接冒充源质。",
        "先用最简单的一条配方确认物品、资源、研究权限和 FE 供电全部满足；一次塞满许多无关材料会让缺项更难定位。",
    ], deps=["ports"], check="已逐项核对一条配方的物品与资源类别"),
    q("precision_infusing", "精密制造：源质路线与注魔路线", "zmod:bearing_unit_t2", (36, 0), [
        "例如 T2 轴承的精密组装路线：T1 轴承 1、下界结晶体 4、下界合金锭 4，外加 ordo 16、terra 16、aer 8 源质，得到 1 个 T2 轴承。",
        "精密组装还承接可用的 MEK 灌注与 TC 注魔配方；不同配方类型的资源、研究与处理规则不同，应在 JEI/机器当前批次中确认所选配方。",
        "首批验证正常后再迁移自动化。取消批次只退还仍预留的材料，已经消耗的能量/逐 tick 化学品不是免费返还。",
    ], deps=["resources"], check="已验证一种带源质的组件自动化配方"),
    q("parallel", "可选 | 并行模块：一个位置，一种倍率", "zmod:precision_assembler_parallel_2x", (40, -8), [
        "精密组装机最多允许一个并行接口；多个并行接口会使结构无效。模块是整机批量能力，不是把两个 2× 叠成 4×。",
        "提高倍率会放大单批原料、资源预留与用电。先在无模块下验证配方，再装 2× 或 4×，同时核查输入、输出和供电。",
        "工业粉碎最多 4×，天选最多 2×，综合矿处理厂不接受并行模块；这些是不同机器的规则，不能把精密组装机可用模块照搬到所有外壳。",
    ], deps=["precision_infusing"], items=["zmod:precision_assembler_parallel_2x"]),
    q("me_ports", "可选 | ME 通玄：先建过滤，再开批量", "zmod:tongxuan_me_input_port", (40, 8), [
        "ME 通玄输入/输出口提供网络集成，需按界面设过滤与资源方向。先保留普通通玄口作为已验证的基线，再接 ME 网络。",
        "安装 tc_energy 与未安装时使用不同的制作材料，但产物都是同一个 ME 通玄口，不存在名为 without_essentia 的独立端口物品。精密配方需要源质时仍须确认对应源质路径。",
        "按一份样板/一批原料测试输入，再检查产物回网；使用库存阈值和过滤防止持续灌入无关材料。研究权限仍归服务器判定。",
    ], deps=["ports"], items=["zmod:tongxuan_me_input_port", "zmod:tongxuan_me_output_port"]),
    q("wireless", "可选 | 无线连接：资源权限与区块状态", "zmod:tongxuan_wireless_connector", (44, 8), [
        "无线连接器用于已有通玄网络的连接配置，不是把未形成结构变成可用机器。先验证近距离有线端口，再按连接器说明绑定目标。",
        "网络所有者与配置权限需一致；不属于自己的网络或接口不能仅靠放一个连接器取得管理权。",
        "控制器、端口或目标区块未加载时，先查区块状态与绑定；不要用无线连接来推断远端机器正在 tick。",
    ], deps=["me_ports"], items=["zmod:tongxuan_wireless_connector"]),
    q("servo", "精密伺服：两种机械件合一", "zmod:precision_servo_component", (40, 0), [
        "SAINTLY_ASCENSION 下的精密组装：T2 驱动 1 + T2 轴承 1 + 晶体导电合金 2 + 锇锭 2 → 精密伺服组件 2，基础配方 duration=20。",
        "供料之前先确认研究已经被机器识别；原料齐全但缺研究时，它不会变成普通无条件机械合成。",
        "按控制器用量准备伺服，同时保留 T2 驱动与轴承给其它结构件，避免单个自动合成订单吃空全线启动库存。",
    ], deps=["precision_infusing"], items=["zmod:precision_servo_component"]),
    q("field", "磁约束：能量与场组件的汇合", "zmod:magnetic_confinement_unit", (44, 0), [
        "T2 场发生器 1 + T2 能量耦合器 1 + 原子合金 2 + 扭曲结晶体 2 → 磁约束单元 2；需要 SAINTLY_ASCENSION。",
        "磁约束进入炼油厂、天选及托卡马克相关制造链。预留足够的 T2 场/能量组件，不要把整批全部组装成单一成品。",
        "duration 是配方基准，不是保证机器在缺电、缺料或输出堵塞时也按那个 tick 数完成。观察真实批次状态再估算吞吐。",
    ], deps=["servo"], items=["zmod:magnetic_confinement_unit"]),
    q("phase", "相位耦合：传送核心也要生产", "zmod:phase_coupler", (48, 0), [
        "T2 能量耦合器 1 + MEK 传送核心 1 + 末影结晶体 2 + 晶体导电合金 2 → 相位耦合器 2；需要 SAINTLY_ASCENSION。",
        "相位耦合器用于天选腔体与综合矿处理腔体。组件虽能批量制造，但其中的 MEK 原件与魔法材料仍应纳入成本。",
        "先按一批材料运行，确认产物回到正确输出仓，再挂大订单。回收/返还区有材料时先核查，不要误当作复制品或普通产物。",
    ], deps=["field"], items=["zmod:phase_coupler"]),
    q("xuanxiang", "玄相电路：反物质是实际门槛", "zmod:xuanxiang_circuit", (52, 0), [
        "现行精密组装需要神秘电路、高纯凯达林晶体、辐照晶体核心、虚空介电板各 1，加 100 单位 MEK 反物质，得到玄相电路 1；研究为 SAINTLY_ASCENSION。",
        "四类工业控制器都保留玄相电路，因此 EV/LuV/ZPM/UV 标签只是最低电路档位。没有反物质和完整研究链，不能仅凭 EV 电路就建工业粉碎机。",
        "GT 电路和天工玄相电路是两类输入，同时需要，不能相互替代。JEI 以服务器实际配方为准。普通通玄口即可生产这些组件，ME、无线和并行模块属于可选扩展。",
    ], deps=["phase"], items=["zmod:xuanxiang_circuit"]),
    q("pump", "工业泵：是流体加工设施", "zmod:industrial_pump_controller", (56, 32), [
        "INDUSTRIAL_PUMP 研究的父节点是 SAINTLY_ASCENSION。控制器、超越机器框架、泵压腔、观察窗按机器预览布置，不是摆一台控制器就自动获得整条水线。",
        "控制器同样需要玄相电路：另备电动泵 4、精密伺服 2、T2 驱动 2、T2 能量耦合器 2、泵压腔 4、钢外壳 2；它不是绕过反物质的早期水线。",
        "当前不装过滤升级时提供水 → 盐水、盐水 → 锂的加工路线；JEI 基准分别为 10:1。它需要真实输入资源与电力，不等同于从虚空无成本取水。",
        "先从普通通玄口输入水并确认盐水产出；再独立验证盐水到锂，不要把未接的输出库存当作永远无限。",
    ], deps=["xuanxiang"], items=["zmod:industrial_pump_controller", "zmod:pump_pressure_chamber"]),
    q("pump_filter", "过滤模式：重水替代盐水水线", "mekanism:upgrade_filter", (60, 32), [
        "工业泵的原生过滤升级槽只接受 MEK 过滤升级。装上后，水的加工路线切为重水，不会同时运行原来的水→盐水路线；盐水→锂路线仍保留。",
        "当前默认一操作 800 mB 水 → 8 mB 重水，能耗随服务器 FluidWorks 配置。调整过滤模式前先看输出和缓冲，避免误以为盐水凭空停产是机器故障。",
        "这是泵的物料转换模式，不是并行模块。该数值属于流体工业配置，不由四类工业机的能耗倍率统一控制。",
    ], deps=["pump"], items=["mekanism:upgrade_filter"], check="已分别确认无过滤与有过滤的水处理产物"),
    q("fluid_plant", "流体处理厂：氘氚的电力路线", "zmod:fluid_processing_plant_controller", (64, 32), [
        "FLUID_PROCESSING_PLANT 同样需要 SAINTLY_ASCENSION。准备反应腔、超越框架与正确通玄口，分别接流体输入和 MEK 气体输出。",
        "基准路线：2 mB 重水 → 2 氘 + 1 氧气；1 mB 液态锂 → 1 氚。运行时会读取当前 MEK 相关配方，服务器改配方后应以实时 JEI 为准。",
        "供料可能是流体，而产物是 MEK 气体；氧气副产也需出口。该厂不自动生成预混 D-T，持续直接 D-T 仍走 ZPM GT 化反路线。",
    ], deps=["pump_filter"], items=["zmod:fluid_processing_plant_controller", "zmod:plant_reaction_chamber"]),
    q("tokamak", "托卡马克：先完成泵与流体厂研究", "zmod:tokamak_controller", (68, 32), [
        "TOKAMAK 研究明确要求 INDUSTRIAL_PUMP 与 FLUID_PROCESSING_PLANT；PLASMA_REFINERY 又以 TOKAMAK 为父研究。研究树要按这条顺序推进。",
        "按托卡马克预览建立环形结构、磁线圈、超越框架、观察窗与端口。它有独立结构与配置，不能照搬 MEK 聚变堆尺寸。",
        "输入燃料是 MEK 预混 D-T 气体 mekanismgenerators:fusion_fuel；本包持续制备 D-T 的 GT 混合路线在 ZPM。LuV 炼油控制器电路门槛不代表 LuV 已有全部等离子供料。",
    ], deps=["fluid_plant"], items=["zmod:tokamak_controller", "zmod:tokamak_magnetic_coil"]),
    q("tokamak_run", "托卡马克投运：预热、燃料、产物空间", "zmod:tokamak_controller", (72, 32), [
        "托卡马克要先形成结构、输入 D-T、提供 FE 预热并启用反应；温度达到点火阈值后才会燃烧。启用开关关闭会停止整个反应，不只是关闭加热器。",
        "产物空间会限制实际燃烧。等离子输出满、燃料不足或温度未达阈值时，不能靠加大上游管道就保证启动。",
        "天工托卡马克使用独立配置；MEK 原生聚变的 2 mB/t 限流不能直接当作它的燃烧上限。应独立计量燃料、输出和净能耗，再设置供料与产物缓冲。",
    ], deps=["tokamak"], check="已核对托卡马克预热、开关、D-T 和产物空间"),
    q("plasma", "等离子物流：新产物走流体输出", "zmod:refinery_heat_lining", (76, 32), [
        "当前天工托卡马克的新等离子产物走真实流体输出；旧 zmod:plasma 气体只保留用于旧资源回收兼容。不要照旧教程把新产物按 MEK 气体接线。",
        "用匹配的流体管/接口把等离子送到炼油厂。先运行少量燃料，确认一端减少、另一端增加，再启用大批量熔炼。",
        "等离子消耗与 D-T 混合、预热和输电全部属于炼油成本。托卡马克有能量输出不等于整条等离子链净赚电。",
    ], deps=["tokamak_run"], check="已确认实际等离子资源类型、流向和缓冲"),
    q("crusher_materials", "粉碎备料：耐磨衬里与终极工厂", "zmod:crusher_wear_lining", (80, -18), [
        "工业粉碎研究为 INDUSTRIAL_CRUSHER，父研究 SAINTLY_ASCENSION。耐磨衬里每批：钢锭 4 + 钻石 4 + T2 轴承 1 + 末影结晶体 2 → 衬里 4。",
        "控制器还要终极粉碎工厂、玄相电路、精密伺服 2、T2 驱动 1、T2 轴承 2、衬里 4、钢外壳 2，以及 #gtceu:circuits/ev。",
        "终极工厂本身也受整合包工厂/安装器成本约束，不要把一台低阶机器无成本升级当作材料准备完成。",
    ], deps=["xuanxiang"], check="已按当前配方核对粉碎控制器和衬里物料"),
    q("crusher", "EV 门槛 | 工业粉碎机", "zmod:industrial_crusher_controller", (84, -18), [
        "本机采用 7×4×5 结构：超越机器框架、超越观察窗、控制器与四个指定底部位置的耐磨衬里；精确摆法用机器预览核对，内部空气要保留。",
        "四个前侧指定框架位置可作为接口，最多一处并行模块。不要把衬里、观察窗或其它普通框架格随意换为通玄口。",
        "现行基础并行 8，模块上限 4×；能耗倍率 4、额外耗时倍率 2。EV 是最低电路档位，玄相电路/反物质与研究条件仍保留。",
    ], deps=["crusher_materials"], items=["zmod:industrial_crusher_controller", "zmod:crusher_wear_lining"], ext=[EV]),
    q("crusher_run", "粉碎验收：先单路线，再装模块", "zmod:precision_assembler_parallel_4x", (88, -18), [
        "先投入 64 个确定有粉碎配方的原料，观察输入下降、实际批次、FE 库存与输出数量；不要默认每条粉碎路线都能增殖矿物。",
        "无模块跑通后再上 2×/4×。模块扩大批次需求，供电不足时大并行可能停在等待态；先查实际能量流入，再怀疑配方没注册。",
        "圆石/碎石等简单路线适合先排查物流；它们的产量不能代表矿物增殖收益。生产线应按目标配方重新验收。",
    ], deps=["crusher"], check="已完成一批粉碎并记录投入、产出与能耗"),
    q("refinery_materials", "炼油备料：热衬里与磁约束", "zmod:refinery_heat_lining", (80, -6), [
        "PLASMA_REFINERY 的父研究是 TOKAMAK。热衬里：下界结晶体 4 + 下界合金锭 2 + 精制黑曜石锭 4 + T2 场发生器 1 → 衬里 4。",
        "控制器需要 #gtceu:circuits/luv、终极熔炼工厂、玄相电路、磁约束单元 2、T2 场发生器 2、衬里 4、精制黑曜石锭 4、下界结晶体 4。",
        "先具备真实等离子来源，再建长期开机能力。LuV 标签不免除反物质、托卡马克研究和 D-T 供料的更晚要求。",
    ], deps=["xuanxiang", "plasma"], check="已核对炼油材料、研究与等离子来源"),
    q("refinery", "LuV 门槛 | 等离子炼油厂", "zmod:plasma_refinery_controller", (84, -6), [
        "采用 5×5×5 结构，超越框架/观察窗、控制器与四块指定底部热衬里。精确端口位置和空气格以预览为准。",
        "本机扩展常规熔炼路线，并额外消耗等离子；当前普通物品每件 1 mB。基础并行 8，能耗倍率 6、额外耗时倍率 2。",
        "机器支持单个最高 256× 并行模块，不能把基础并行 8 理解为最终上限；实际批次还受材料、等离子、能量和容量限制。扩大模块前先核算全线供给。",
    ], deps=["refinery_materials"], items=["zmod:plasma_refinery_controller", "zmod:refinery_heat_lining"], ext=[LUV]),
    q("refinery_run", "炼油验收：逐件等离子成本", "mekanism:energized_smelter", (88, -6), [
        "固定一种常规熔炼配方，记录 N 个输入、N 对应产出、等离子减少量、能量减少量和 ticks。副产物或特殊配方仍需分别验证。",
        "当前默认普通路线 N 件对应 N mB 等离子。缓冲不够时机器会等待，不要把半批输入未处理误认为物品丢失。",
        "对比 GT/MEK 时把托卡马克与燃料制备一并计入，而不只比较炼油厂内部耗电。高吞吐是整线能力，不是免费效率。",
    ], deps=["refinery"], check="已有炼油投入、产出、等离子和能量记录"),
    q("tianxuan_materials", "天选备料：相位与处理腔", "zmod:tianxuan_chamber", (80, 6), [
        "TIANXUAN_REFINERY 的工业研究需 SAINTLY_ASCENSION。处理腔每批：精制黑曜石锭 4 + 萤石 4 + 平衡结晶体 4 + 相位耦合器 1 → 腔体 4。",
        "控制器的 GT 电路为 #gtceu:circuits/zpm，此外还保留氧化机、溶解室、玄相电路、相位耦合器、磁约束、T2 能量耦合器、处理腔、神秘电路和钢外壳。",
        "控制器所用机器只是制造材料，不表示运行时接收这些机器的全部配方。富集部分还受服务端白名单限制。",
    ], deps=["xuanxiang"], check="天选控制器、腔体与 ZPM 电路已核对"),
    q("tianxuan", "ZPM 门槛 | 天选富集工厂", "zmod:tianxuan_controller", (84, 6), [
        "采用 7×6×5 结构，超越框架/观察窗和四个指定底部天选腔体；通过预览核对窗带、空气与端口位置。",
        "当前基础并行 2，模块最多 2×；能耗倍率 4、额外耗时倍率 2。4× 及更高模块不属于本包天选的允许范围。",
        "天选的富集不是全 MEK 配方无条件搬运，实际允许哪些加工取决于配置与已加载配方。先用白名单样例验收。",
    ], deps=["tianxuan_materials"], items=["zmod:tianxuan_controller", "zmod:tianxuan_chamber"], ext=[ZPM]),
    q("tianxuan_run", "天选白名单：用配方 ID 判定", "zmod:high_purity_kaydarin_crystal", (88, 6), [
        "当前允许的富集配方 ID 为 zmod:materials/high_purity_kaydarin_crystal 和 mekanism:enriching/hdpe_sheet。配置匹配的是配方 ID，不是物品显示名，也不是任意含 HDPE 的配方。",
        "先用凯达林晶体或对应 HDPE 路线验证；其它富集原料被拒绝可能正是白名单生效，不应随意移除限制。",
        "普通 MEK/GT 处理线仍负责未开放路线。管理员修改白名单后检查新批次与真实配方 ID，避免让旧测试库存误导判断。",
    ], deps=["tianxuan"], check="已验证白名单允许项与一个拒绝项"),
    q("ore_materials", "矿处理备料：保留完整 MEK 部件链", "zmod:ore_processing_chamber", (80, 18), [
        "INTEGRATED_ORE_PROCESSING_PLANT 需要 SAINTLY_ASCENSION。腔体每批含富集仓、粉碎机、精制黑曜石锭 8、相位耦合器 2、平衡结晶体 4，得到腔体 4。",
        "控制器需要 #gtceu:circuits/uv、溶解室、洗矿机、结晶器、压射机、提纯仓、冶炼炉，外加玄相电路 2、腔体 4、T2 驱动 2。",
        "这保留了 MEK 矿处理设备的制造投入。不要把 UV 电路门槛误当作删除所有原有化工与魔法组件。",
    ], deps=["xuanxiang"], check="已列出 UV 控制器的整组 MEK 与天工材料"),
    q("ore_plant", "UV 门槛 | 综合矿处理终局工厂", "zmod:integrated_ore_processing_plant_controller", (84, 18), [
        "采用 9×6×7 结构，超越框架/观察窗、控制器及四块指定底部矿处理腔体。端口仍只能放在指定框架位置，内部应留空。",
        "当前基础并行 8、路线最高 2 倍、能耗倍率 8、额外耗时倍率 2；不接受并行模块。不是把 MEK 五倍矿链无条件折叠成免费终局机器。",
        "每种物品容量 32768，资源槽容量 4,000,000，储能 128,000,000 FE。容量是缓冲上限，不是每 tick 吞吐或持续供电能力。",
    ], deps=["ore_materials"], items=["zmod:integrated_ore_processing_plant_controller", "zmod:ore_processing_chamber"], ext=[UV]),
    q("ore_routes", "矿路线验收：矿石、粗矿和粗矿块", "minecraft:raw_iron", (88, 18), [
        "分别测试铁矿石、粗铁与粗铁块，记录归一化原料数量和产物。粗矿块是打包原料，不能把一块直接当一份矿石比较倍率。",
        "当前识别兼容 forge:/c: 材料标签；其它模组矿石没有预期标签或没有可用产物映射时，仍可能没有路线。不要仅凭名称包含矿字判断它必能处理。",
        "管理员可按 route、item、input tag 阻止路线；当前最高倍率为 2。以实际 JEI 路线和服务器配置验收，不引用旧默认 22000 并行或高倍矿结果。",
    ], deps=["ore_plant"], check="已对照普通矿石、粗矿与粗矿块的实际产出"),
    q("settings", "全厂配置：并行、能耗与容量一起看", "zmod:transcendent_machine_frame", (92, 0), [
        "四类工业机配置文件为 zmod-industrial-machines.toml：基础并行粉碎/炼油/矿处理各 8，天选 2；能耗倍率分别 4/6/8/4；额外耗时倍率都为 2。",
        "普通工业机每种物品容量 32768、资源槽 256000、储能 64000000 FE；矿处理资源与储能更大。满槽拒收与输出等待是正常保护，不代表材料消失。",
        "还有 MEK 满速时间基准 fullSpeedDurationMultiplier=0.5 和全局 energyUseMultiplier=1。计算实际耗时/能耗应看所选路线与机器批次，不只拿一个倍率相乘。",
        "泵/流体厂与托卡马克使用各自配置。管理员不能只调整四类工业机文件便宣称全部天工机器已按同一比例削弱。",
    ], deps=["crusher_run", "refinery_run", "tianxuan_run", "ore_routes"], check="已按本服配置记录各机的并行、成本与容量"),
    q("old_world", "旧世界迁移：默认文件不会追写存档", "minecraft:writable_book", (96, 0), [
        "defaultconfigs/zmod-industrial-machines.toml 是新世界模板；已存在世界应同步 <世界>/serverconfig/zmod-industrial-machines.toml。客户端同名文件不能覆盖远程服务器实际值。",
        "修改后已经预订的批次保留其数值，新批次才采用新配置。先让旧批完成或按机器规则处理，再用同一新批材料比较。",
        "保留旧文件和一次物料/能量记录，更新前后核对库存与回收区。任务书进度不会因本次拆章丢失：四个原工业控制器任务和目标 ID 均已迁入本章。",
    ], deps=["settings"], check="已确认本服使用的是存档配置而非仅新世界模板"),
    q("troubleshooting", "天工排错：从结构到真实批次", "minecraft:book", (100, 0), [
        "结构不形成：查朝向、机器尺寸、专用底部部件、观察窗、空气格、允许端口位置、模块数量、模块等级与区块是否加载；不同机器的外壳不能凭相似外形互换。",
        "配方不出现/不启动：先查服务端是否加载 JSON、研究与可选依赖，再查真实配方 ID/白名单、GT 等级标签、物品/NBT、资源类别、FE 实收与输出空间。JEI 只显示本地页面不证明服务器已注册。",
        "自动化失效：普通输入/输出先各测一批，随后再查 ME 过滤、样板、网络权限与无线绑定。气体、流体、灌注资源和源质要分别检查，输出口拒绝插入是预期行为。",
        "吞吐偏低：同时记录实际 tick、输入/产物数量、等离子/其它资源和能量变化，注明是否有外部补能。整座基地的长期净收益要把辅助系统纳入同一窗口计量。",
    ], deps=["old_world"], check="已有一条可复现的结构、配方和整线产能检查记录"),
]

from staged_tiangong_progression import apply_progression

Q = apply_progression(Q)

SPEC = dict(filename="huixuan_tiangong", salt="society-huixuan-tiangong-v1", order=20,
            title="&5&l秽玄天工&r：研究、制造与工业设施",
            icon="zmod:precision_assembler_controller", quests=Q, preserved=PRESERVED,
            minimum_spacing=1.8)

if __name__ == "__main__":
    run(SPEC)
