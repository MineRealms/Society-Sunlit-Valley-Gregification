// priority: 0
// ============================================================
// GTCA（GT Community Additions 2.2.0）× GTCEu 7.5.3 — 机壳兼容配方
//
// 问题（日志 + 源码 + 反编译核对，非推测）：
//  - 运行日志 [22:31:13] 报：
//      Input item 0 of recipe gtceu:reactive_gas_cont_cas is empty
//      Input item 0 of recipe gtceu:inert_filtration_casing is empty
//  - 原因：gtca 材料 flags 与 GTCEu 7.5.3 不匹配（源码 GTCAMetals.java，7.5.x 分支）：
//      hastelloy_n    : 无 GENERATE_FRAME / GENERATE_ROTOR
//      hastealloy_276 : 无 GENERATE_GEAR（原配方还需 rotor）
//      GTCEu hastelloy_x 也无 GENERATE_ROTOR
//    → GT TagPrefix 的 generationCondition 判定物品不存在，ChemicalHelper 取到空栈，
//      原配方会以缺失输入的残缺形态注册（可能导致异常廉价可合成）
//  - 处理：按产出物移除这两个残缺配方，补两条用「可验证存在」物品的兼容配方
//
// 数值镜像 gtca 原配方（CasingRecipes.java 7.5.x 分支 289-311 行）：
//   EUt = GTValues.VA[IV] = 7680、duration 680、circuitMeta 6、产出 ×2
// 物品 ID 证据：H:\tools\jei_names.json（GT 物品导出，逐条核对存在）
//   gtceu:double_hastelloy_c_276_plate / gtceu:hastelloy_c_276_frame
//   gtceu:hastelloy_x_plate / gtceu:tungsten_steel_rotor / gtceu:tungsten_steel_gear
//   gtceu:iv_electric_pump / gtceu:polytetrafluoroethylene（流体）
// ============================================================
console.info("[GTCA-COMPAT] gtcaCasingCompat.js loaded");

ServerEvents.recipes((e) => {
  if (!Platform.isLoaded("gtca")) return;

  // 移除 gtca 原残缺配方（按产出物移除，覆盖其唯一来源 CasingRecipes）
  e.remove({ output: "gtca:reactive_gas_contantment_casing" });
  e.remove({ output: "gtca:inert_filtration_casing" });

  // 反应气体密封机壳：6× 双层铪合金板 + 框架 + 转子（转子用 IV 级钨钢件替代缺失前缀）
  e.recipes.gtceu.assembler("gtca:compat/reactive_gas_contantment_casing")
    .itemInputs(
      "6x gtceu:double_hastelloy_c_276_plate",
      "gtceu:hastelloy_c_276_frame",
      "gtceu:tungsten_steel_rotor"
    )
    .itemOutputs("2x gtca:reactive_gas_contantment_casing")
    .circuit(6)
    .duration(680)
    .EUt(7680, 1);

  // 惰性过滤机壳：框架 + 6× 铪合金板 + 2× 转子 + 2× 齿轮 + IV 电动泵 + 576mB PTFE
  e.recipes.gtceu.assembler("gtca:compat/inert_filtration_casing")
    .itemInputs(
      "gtceu:hastelloy_c_276_frame",
      "6x gtceu:hastelloy_x_plate",
      "2x gtceu:tungsten_steel_rotor",
      "2x gtceu:tungsten_steel_gear",
      "gtceu:iv_electric_pump"
    )
    .inputFluids(Fluid.of("gtceu:polytetrafluoroethylene", 576))
    .itemOutputs("2x gtca:inert_filtration_casing")
    .circuit(6)
    .duration(680)
    .EUt(7680, 1);
});
