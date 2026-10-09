// priority: 0
// ============================================================
// GCYR 火箭制造硬化：火箭发动机 / 燃料储罐 需要 GT-- 重型合金板
//
// 原配方（GCYR MiscRecipes.java，装配机）：
//   基础燃料罐 = 2×不锈钢桶 + 6×Kapton-K板 + 不锈钢框架        （HV，480，300t）
//   基础发动机 = 4×动力推进器 + 6×Kapton-K板 + 不锈钢框架      （HV，480，300t）
//   先进燃料罐 = 2×钨钢桶 + 6×Kapton-K板 + 钨钢框架           （IV，7680，300t）
//   先进发动机 = 4×先进动力推进器 + 6×Kapton-K板 + 钨钢框架    （IV，7680，300t）
//   精英燃料罐 = 2×ZPM量子缸 + 6×Kapton-K板 + 钠钾合金框架     （ZPM，122880，300t）
//   精英发动机 = 4×引力引擎 + 6×Kapton-K板 + 钠钾合金框架      （ZPM，122880，300t）
//
// 硬化：每件部件追加 2× 对应等级重型合金板（T1/T2/T3），
//       即火箭等级 = GT-- 重型合金链等级，与太空章进度一致。
// ============================================================
console.info("[GCYR-GTNN] hardenRockets.js loaded");

ServerEvents.recipes((e) => {
  if (!Platform.isLoaded("gcyr") || !Platform.isLoaded("gtnn")) return;

  const KAPTON = "6x #forge:plates/kapton_k";

  // ---- 基础（HV）：T1 重型合金板 ----
  e.remove({ id: "gcyr:basic_fuel_tank" });
  e.recipes.gtceu.assembler("gcyr:basic_fuel_tank")
    .itemInputs("2x gtceu:stainless_steel_drum", KAPTON, "#forge:frames/stainless_steel", "2x gtnn:heavy_plate_t1")
    .itemOutputs("gcyr:basic_fuel_tank")
    .duration(300)
    .EUt(480, 1);

  e.remove({ id: "gcyr:basic_rocket_motor" });
  e.recipes.gtceu.assembler("gcyr:basic_rocket_motor")
    .itemInputs("4x gtceu:power_thruster", KAPTON, "#forge:frames/stainless_steel", "2x gtnn:heavy_plate_t1")
    .itemOutputs("gcyr:basic_rocket_motor")
    .duration(300)
    .EUt(480, 1);

  // ---- 先进（IV）：T2 重型合金板 ----
  e.remove({ id: "gcyr:advanced_fuel_tank" });
  e.recipes.gtceu.assembler("gcyr:advanced_fuel_tank")
    .itemInputs("2x gtceu:tungsten_steel_drum", KAPTON, "#forge:frames/tungsten_steel", "2x gtnn:heavy_plate_t2")
    .itemOutputs("gcyr:advanced_fuel_tank")
    .duration(300)
    .EUt(7680, 1);

  e.remove({ id: "gcyr:advanced_rocket_motor" });
  e.recipes.gtceu.assembler("gcyr:advanced_rocket_motor")
    .itemInputs("4x gtceu:advanced_power_thruster", KAPTON, "#forge:frames/tungsten_steel", "2x gtnn:heavy_plate_t2")
    .itemOutputs("gcyr:advanced_rocket_motor")
    .duration(300)
    .EUt(7680, 1);

  // ---- 精英（ZPM）：T3 重型合金板 ----
  e.remove({ id: "gcyr:elite_fuel_tank" });
  e.recipes.gtceu.assembler("gcyr:elite_fuel_tank")
    .itemInputs("2x gtceu:zpm_quantum_tank", KAPTON, "#forge:frames/naquadah_alloy", "2x gtnn:heavy_plate_t3")
    .itemOutputs("gcyr:elite_fuel_tank")
    .duration(300)
    .EUt(122880, 1);

  e.remove({ id: "gcyr:elite_rocket_motor" });
  e.recipes.gtceu.assembler("gcyr:elite_rocket_motor")
    .itemInputs("4x gtceu:gravitation_engine_unit", KAPTON, "#forge:frames/naquadah_alloy", "2x gtnn:heavy_plate_t3")
    .itemOutputs("gcyr:elite_rocket_motor")
    .duration(300)
    .EUt(122880, 1);
});
