# AS 流明绑定：第四批补全与验收边界

> 2026-11-04。用户确认采用完整补全方案；不是只隐藏13条启动错误。源码已构建，143项AS单测通过；世界内绑定、补充、效果与消耗尚待完整副本验收，见 [PHASE4_ACCEPTANCE.md](PHASE4_ACCEPTANCE.md)。

## 1. 为什么涉及多个文件

原移植版起初确认三处断链，继续追踪还发现属性源和事件注册缺失：
1. JSON使用 `identifier/attribute_type/mode/value`，实际读取的却是NBT格式 `id/type/mode/baseValue`。
2. JSON来自1.21属性名，1.20.1注册表沿用1.16名称；另有六种属性在旧注册表中不存在。
3. 绑定数据、存储组件、效果类已存在，但没有生存玩法调用 `applyBinding`。

因此只改字段不会让玩法可用。此次范围限于流明绑定及其必要属性、两条液态星能配方；不改祭坛进度、星座研究树、星能传输或其它魔法体系。

## 2. 数据和属性

- 接入原有 `LumenModifierCodec`，按JSON字段读取，通过移植版属性注册表解析。
- 13份星座数据转换属性ID；保留14种绑定数据（含棱彩）及原修饰符标识。
- 新增攻击距离、跨步高度、安全摔落距离、穿甲几率、格挡几率、全伤害减免，避免把格挡错当闪避、全伤害减免错当元素抗性。
- 冷却缩减按旧实现的正数减免口径转换。
- 暴击/吸血/格挡/穿甲的零基值概率不能使用“0×加成”；数据改为加法，并区分旧百分数单位和0～1概率单位。
- 加载器拒绝损坏配方的部分结果，避免“绑定在、效果丢失、仍扣流明”。
- 穿甲接在现有LivingEntity Mixin的护甲计算返回点，保留护甲损耗和后续抗性/附魔减免；不用放大原始伤害来近似。

- 独立LumenBindingSource接入原有ModifierManager，按装备/数值快照增减修饰符，耗尽与脱下可撤销；沿用现有同步包。
- 接通13个原有消耗/效果事件处理器。内部消耗直接扣存储组件，不借用被装备canDrain=false拒绝的外部抽取接口。
- 修饰符身份包含物品和槽位，避免相同JSON修饰符被两件装备互相覆盖；棱彩放大只在棱彩仍有流明时应用。

## 3. 绑定与补充

### 绑定

向同一格液态星能**源方块**投入：
- 有流明类型的水晶×1；
- 星尘×1；
- 受支持的装备/工具/武器或星露×1。

80～119 tick阈值后消耗源方块及投入物，掉出带数据的新物品。实际完成时间受实体进入液体的时刻影响。

装备每次补入最多2000流明，受自身容量限制；新非棱彩绑定替换旧非棱彩绑定，棱彩绑定可保留。输入物品其他NBT应保留（验收必须覆盖）。

星露走药水效果分支；棱彩增强已有自定义效果。捐赠版本棱彩分支曾只构造输出、不掉出或扣料，此次按其它分支一起支付并掉出。

### 补充

同格投入流明水晶和允许接收该流明的存储物品，不投入星尘。补入最多2000、不得超过容量；同样消耗水晶和源方块，返回原物品的补满副本。

两条配方注册在现有 `LiquidStarlightCraftingRegistry`，由 `BlockLiquidStarlight.entityInside` 实际触发，不另建第二套配方系统。

## 4. 必须验证

- 所有14绑定加载，无空动态修饰符槽位；143条修饰符字段和注册名全部有效。
- 真正投物在液体中完成绑定和补充，而非仅直接调用helper。
- 装备NBT不丢、消耗恰好一份、液体只消耗一次；补充不超过容量。
- 绑定后穿戴产生效果；相应事件扣流明；耗尽后效果撤销；取下装备撤销。
- 换绑、棱彩叠加、药水分支、保存重载、客户端同步和提示。
- 客户端画面、JEI展示没有在专用服探针中验证，不能据此宣称全通过。

## 5. 文件入口

AS源码 `src/main/java/hellfirepvp/astralsorcery/`：
- `common/lumen/binding/effect/LumenModifierCodec.java`
- `common/lumen/binding/data/LumenBindingTypeLoader.java`
- `common/crafting/nojson/starlight/{BindLumenRecipe,FillLumenRecipe}.java`
- `common/perk/type/AttributeType*.java`（本轮六种属性）
- `mixin/MixinLivingEntity.java`

数据在 `src/main/resources/data/astralsorcery/lumen_binding/`。没有改旧装备修饰符的NBT字段定义。
