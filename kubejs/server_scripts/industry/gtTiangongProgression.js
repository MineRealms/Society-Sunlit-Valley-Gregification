// priority: -1000
// Final assembly uses GT data carriers; magic cores retain their original research/resources.
console.info("[SUNLIT-INDUSTRY] GT manufacturing gates loaded");
ServerEvents.recipes(function(event) {
  event.remove({ output: "zmod:transcendence_key" });
  event.remove({ output: "zmod:taiyi_matrix" });
  event.remove({ output: "zmod:transcendence_core" });
  event.remove({ output: "zmod:precision_assembler_controller" });
  event.remove({ output: "zmod:industrial_crusher_controller" });
  event.remove({ output: "zmod:industrial_pump_controller" });
  event.remove({ output: "zmod:fluid_processing_plant_controller" });
  event.remove({ output: "zmod:tokamak_controller" });
  event.remove({ output: "zmod:tokamak_magnetic_coil" });
  event.remove({ output: "zmod:tianxuan_controller" });
  event.remove({ output: "zmod:plasma_refinery_controller" });
  event.remove({ output: "zmod:warped_polymerizer_controller" });
  event.remove({ output: "zmod:yaoguang_controller" });
  event.remove({ output: "zmod:integrated_ore_processing_plant_controller" });
  event.remove({ output: "zmod:matter_reconstructor_controller" });
  event.remove({ output: "zmod:tianshu_controller_t3" });
  event.remove({ output: "zmod:yuheng_controller_t3" });
  event.remove({ output: "zmod:qiongli_controller_t3" });
  event.remove({ output: "zmod:singularity_controller" });
  event.remove({ output: "zmod:void_pylon_beacon" });
  event.remove({ output: "zmod:tongxuan_me_input_port" });
  event.remove({ output: "zmod:tongxuan_me_output_port" });
  event.remove({ output: "zmod:tongxuan_pattern_provider" });
  event.remove({ output: "zmod:tongxuan_wireless_connector" });
  event.remove({ output: "zmod:precision_assembler_parallel_4x" });
  event.remove({ output: "zmod:thread_hatch_2x" });
  event.remove({ output: "mekanismgenerators:fusion_reactor_controller" });
  event.remove({ output: "mekanism:sps_casing" });
  event.remove({ output: "mekanism:supercharged_coil" });
  event.remove({ output: "society:wanxiang_formation_core" });
  event.recipes.gtceu.assembly_line("society:industry/zmod_transcendence_key")
    .itemInputs("society:assembly_core_zmod_transcendence_key", "4x gtceu:iv_robot_arm", "4x gtceu:iv_field_generator", "4x gtceu:iv_electric_motor", "2x gtceu:iv_sensor", "4x gtceu:iv_emitter", "8x #gtceu:circuits/iv")
    .inputFluids(Fluid.of("gtceu:soldering_alloy", 576), Fluid.of("gtceu:lubricant", 1000))
    .itemOutputs("zmod:transcendence_key")
    .duration(1200)
    .EUt(7680)
    ['scannerResearch(java.util.function.UnaryOperator)'](function(builder) {
      return builder
        .researchStack(Item.of("thaumcraft:silverwood_staff_core"))
        .researchId("sunlit_industry_zmod_transcendence_key_v1")
        .EUt(7680)
        .duration(2400);
    });
  event.recipes.gtceu.assembly_line("society:industry/zmod_taiyi_matrix")
    .itemInputs("society:assembly_core_zmod_taiyi_matrix", "4x gtceu:luv_robot_arm", "4x gtceu:luv_field_generator", "4x gtceu:luv_electric_motor", "2x gtceu:luv_sensor", "4x gtceu:luv_emitter", "8x #gtceu:circuits/luv")
    .inputFluids(Fluid.of("gtceu:soldering_alloy", 1152), Fluid.of("gtceu:lubricant", 2000), Fluid.of("gtceu:polybenzimidazole", 1152))
    .itemOutputs("zmod:taiyi_matrix")
    .duration(1600)
    .EUt(30720)
    ['scannerResearch(java.util.function.UnaryOperator)'](function(builder) {
      return builder
        .researchStack(Item.of("thaumcraft:runic_matrix"))
        .researchId("sunlit_industry_zmod_taiyi_matrix_v1")
        .EUt(7680)
        .duration(3200);
    });
  event.recipes.gtceu.assembly_line("society:industry/zmod_transcendence_core")
    .itemInputs("society:assembly_core_zmod_transcendence_core", "4x gtceu:uv_robot_arm", "4x gtceu:uv_field_generator", "4x gtceu:uv_electric_motor", "2x gtceu:uv_sensor", "4x gtceu:uv_emitter", "16x #gtceu:circuits/uv")
    .inputFluids(Fluid.of("gtceu:soldering_alloy", 4608), Fluid.of("gtceu:lubricant", 8000), Fluid.of("gtceu:polybenzimidazole", 4608))
    .itemOutputs("zmod:transcendence_core")
    .duration(2400)
    .EUt(491520)
    .stationResearch(function(builder) {
      return builder
        .researchStack(Item.of("zmod:yuheng_furnace_core"))
        .researchId("sunlit_industry_zmod_transcendence_core_v1")
        .EUt(491520)
        .CWUt(64, 256000);
    });
  event.recipes.gtceu.assembly_line("society:industry/zmod_precision_assembler_controller")
    .itemInputs("society:assembly_core_zmod_precision_assembler_controller", "4x gtceu:iv_robot_arm", "2x gtceu:iv_field_generator", "4x gtceu:iv_electric_motor", "2x gtceu:iv_sensor", "8x #gtceu:circuits/iv")
    .inputFluids(Fluid.of("gtceu:soldering_alloy", 576), Fluid.of("gtceu:lubricant", 1000))
    .itemOutputs("zmod:precision_assembler_controller")
    .duration(1200)
    .EUt(7680)
    ['scannerResearch(java.util.function.UnaryOperator)'](function(builder) {
      return builder
        .researchStack(Item.of("zmod:lattice_control_core"))
        .researchId("sunlit_industry_zmod_precision_assembler_controller_v1")
        .EUt(7680)
        .duration(2400);
    });
  event.recipes.gtceu.assembly_line("society:industry/zmod_industrial_crusher_controller")
    .itemInputs("society:assembly_core_zmod_industrial_crusher_controller", "4x gtceu:iv_robot_arm", "2x gtceu:iv_field_generator", "4x gtceu:iv_electric_motor", "2x gtceu:iv_sensor", "8x #gtceu:circuits/iv")
    .inputFluids(Fluid.of("gtceu:soldering_alloy", 576), Fluid.of("gtceu:lubricant", 1000))
    .itemOutputs("zmod:industrial_crusher_controller")
    .duration(1200)
    .EUt(7680)
    ['scannerResearch(java.util.function.UnaryOperator)'](function(builder) {
      return builder
        .researchStack(Item.of("zmod:crusher_wear_lining"))
        .researchId("sunlit_industry_zmod_industrial_crusher_controller_v1")
        .EUt(7680)
        .duration(2400);
    });
  event.recipes.gtceu.assembly_line("society:industry/zmod_industrial_pump_controller")
    .itemInputs("society:assembly_core_zmod_industrial_pump_controller", "4x gtceu:luv_robot_arm", "2x gtceu:luv_field_generator", "4x gtceu:luv_electric_pump", "2x gtceu:luv_sensor", "8x #gtceu:circuits/luv")
    .inputFluids(Fluid.of("gtceu:soldering_alloy", 1152), Fluid.of("gtceu:lubricant", 2000), Fluid.of("gtceu:polybenzimidazole", 1152))
    .itemOutputs("zmod:industrial_pump_controller")
    .duration(1600)
    .EUt(30720)
    ['scannerResearch(java.util.function.UnaryOperator)'](function(builder) {
      return builder
        .researchStack(Item.of("zmod:pump_pressure_chamber"))
        .researchId("sunlit_industry_zmod_industrial_pump_controller_v1")
        .EUt(7680)
        .duration(3200);
    });
  event.recipes.gtceu.assembly_line("society:industry/zmod_fluid_processing_plant_controller")
    .itemInputs("society:assembly_core_zmod_fluid_processing_plant_controller", "4x gtceu:luv_robot_arm", "2x gtceu:luv_field_generator", "4x gtceu:luv_electric_pump", "2x gtceu:luv_sensor", "8x #gtceu:circuits/luv")
    .inputFluids(Fluid.of("gtceu:soldering_alloy", 1152), Fluid.of("gtceu:lubricant", 2000), Fluid.of("gtceu:polybenzimidazole", 1152))
    .itemOutputs("zmod:fluid_processing_plant_controller")
    .duration(1600)
    .EUt(30720)
    ['scannerResearch(java.util.function.UnaryOperator)'](function(builder) {
      return builder
        .researchStack(Item.of("zmod:plant_reaction_chamber"))
        .researchId("sunlit_industry_zmod_fluid_processing_plant_controller_v1")
        .EUt(7680)
        .duration(3200);
    });
  event.recipes.gtceu.assembly_line("society:industry/zmod_tokamak_controller")
    .itemInputs("society:assembly_core_zmod_tokamak_controller", "4x gtceu:zpm_robot_arm", "4x gtceu:zpm_field_generator", "4x gtceu:zpm_electric_motor", "2x gtceu:zpm_sensor", "4x gtceu:zpm_emitter", "12x #gtceu:circuits/zpm", "gtceu:zpm_fusion_reactor")
    .inputFluids(Fluid.of("gtceu:soldering_alloy", 2304), Fluid.of("gtceu:lubricant", 4000), Fluid.of("gtceu:polybenzimidazole", 2304))
    .itemOutputs("zmod:tokamak_controller")
    .duration(2000)
    .EUt(122880)
    .stationResearch(function(builder) {
      return builder
        .researchStack(Item.of("zmod:magnetic_confinement_unit"))
        .researchId("sunlit_industry_zmod_tokamak_controller_v1")
        .EUt(122880)
        .CWUt(16, 64000);
    });
  event.recipes.gtceu.assembly_line("society:industry/zmod_tokamak_magnetic_coil")
    .itemInputs("society:assembly_core_zmod_tokamak_magnetic_coil", "1x gtceu:zpm_field_generator", "2x gtceu:zpm_electric_motor", "2x #gtceu:circuits/zpm")
    .inputFluids(Fluid.of("gtceu:soldering_alloy", 2304), Fluid.of("gtceu:lubricant", 4000), Fluid.of("gtceu:polybenzimidazole", 2304))
    .itemOutputs("zmod:tokamak_magnetic_coil")
    .duration(2000)
    .EUt(122880)
    .stationResearch(function(builder) {
      return builder
        .researchStack(Item.of("zmod:field_generator_t2"))
        .researchId("sunlit_industry_zmod_tokamak_magnetic_coil_v1")
        .EUt(122880)
        .CWUt(16, 64000);
    });
  event.recipes.gtceu.assembly_line("society:industry/zmod_tianxuan_controller")
    .itemInputs("society:assembly_core_zmod_tianxuan_controller", "4x gtceu:zpm_robot_arm", "2x gtceu:zpm_field_generator", "4x gtceu:zpm_electric_pump", "2x gtceu:zpm_sensor", "12x #gtceu:circuits/zpm")
    .inputFluids(Fluid.of("gtceu:soldering_alloy", 2304), Fluid.of("gtceu:lubricant", 4000), Fluid.of("gtceu:polybenzimidazole", 2304))
    .itemOutputs("zmod:tianxuan_controller")
    .duration(2000)
    .EUt(122880)
    .stationResearch(function(builder) {
      return builder
        .researchStack(Item.of("zmod:tianxuan_chamber"))
        .researchId("sunlit_industry_zmod_tianxuan_controller_v1")
        .EUt(122880)
        .CWUt(16, 64000);
    });
  event.recipes.gtceu.assembly_line("society:industry/zmod_plasma_refinery_controller")
    .itemInputs("society:assembly_core_zmod_plasma_refinery_controller", "4x gtceu:zpm_robot_arm", "2x gtceu:zpm_field_generator", "4x gtceu:zpm_electric_motor", "2x gtceu:zpm_sensor", "12x #gtceu:circuits/zpm")
    .inputFluids(Fluid.of("gtceu:soldering_alloy", 2304), Fluid.of("gtceu:lubricant", 4000), Fluid.of("gtceu:polybenzimidazole", 2304))
    .itemOutputs("zmod:plasma_refinery_controller")
    .duration(2000)
    .EUt(122880)
    .stationResearch(function(builder) {
      return builder
        .researchStack(Item.of("zmod:refinery_heat_lining"))
        .researchId("sunlit_industry_zmod_plasma_refinery_controller_v1")
        .EUt(122880)
        .CWUt(16, 64000);
    });
  event.recipes.gtceu.assembly_line("society:industry/zmod_warped_polymerizer_controller")
    .itemInputs("society:assembly_core_zmod_warped_polymerizer_controller", "4x gtceu:zpm_robot_arm", "4x gtceu:zpm_field_generator", "4x gtceu:zpm_electric_motor", "2x gtceu:zpm_sensor", "4x gtceu:zpm_emitter", "12x #gtceu:circuits/zpm")
    .inputFluids(Fluid.of("gtceu:soldering_alloy", 2304), Fluid.of("gtceu:lubricant", 4000), Fluid.of("gtceu:polybenzimidazole", 2304))
    .itemOutputs("zmod:warped_polymerizer_controller")
    .duration(2000)
    .EUt(122880)
    .stationResearch(function(builder) {
      return builder
        .researchStack(Item.of("zmod:polymerization_chamber"))
        .researchId("sunlit_industry_zmod_warped_polymerizer_controller_v1")
        .EUt(122880)
        .CWUt(16, 64000);
    });
  event.recipes.gtceu.assembly_line("society:industry/zmod_yaoguang_controller")
    .itemInputs("society:assembly_core_zmod_yaoguang_controller", "4x gtceu:zpm_robot_arm", "4x gtceu:zpm_field_generator", "4x gtceu:zpm_electric_motor", "2x gtceu:zpm_sensor", "4x gtceu:zpm_emitter", "12x #gtceu:circuits/zpm")
    .inputFluids(Fluid.of("gtceu:soldering_alloy", 2304), Fluid.of("gtceu:lubricant", 4000), Fluid.of("gtceu:polybenzimidazole", 2304))
    .itemOutputs("zmod:yaoguang_controller")
    .duration(2000)
    .EUt(122880)
    .stationResearch(function(builder) {
      return builder
        .researchStack(Item.of("mekanism:ultimate_energy_cube"))
        .researchId("sunlit_industry_zmod_yaoguang_controller_v1")
        .EUt(122880)
        .CWUt(16, 64000);
    });
  event.recipes.gtceu.assembly_line("society:industry/zmod_integrated_ore_processing_plant_controller")
    .itemInputs("society:assembly_core_zmod_integrated_ore_processing_plant_controller", "4x gtceu:uv_robot_arm", "2x gtceu:uv_field_generator", "4x gtceu:uv_electric_pump", "2x gtceu:uv_sensor", "16x #gtceu:circuits/uv")
    .inputFluids(Fluid.of("gtceu:soldering_alloy", 4608), Fluid.of("gtceu:lubricant", 8000), Fluid.of("gtceu:polybenzimidazole", 4608))
    .itemOutputs("zmod:integrated_ore_processing_plant_controller")
    .duration(2400)
    .EUt(491520)
    .stationResearch(function(builder) {
      return builder
        .researchStack(Item.of("zmod:ore_processing_chamber"))
        .researchId("sunlit_industry_zmod_integrated_ore_processing_plant_controller_v1")
        .EUt(491520)
        .CWUt(64, 256000);
    });
  event.recipes.gtceu.assembly_line("society:industry/zmod_matter_reconstructor_controller")
    .itemInputs("society:assembly_core_zmod_matter_reconstructor_controller", "4x gtceu:uv_robot_arm", "4x gtceu:uv_field_generator", "4x gtceu:uv_electric_motor", "2x gtceu:uv_sensor", "4x gtceu:uv_emitter", "16x #gtceu:circuits/uv")
    .inputFluids(Fluid.of("gtceu:soldering_alloy", 4608), Fluid.of("gtceu:lubricant", 8000), Fluid.of("gtceu:polybenzimidazole", 4608))
    .itemOutputs("zmod:matter_reconstructor_controller")
    .duration(2400)
    .EUt(491520)
    .stationResearch(function(builder) {
      return builder
        .researchStack(Item.of("zmod:reconstruction_chamber"))
        .researchId("sunlit_industry_zmod_matter_reconstructor_controller_v1")
        .EUt(491520)
        .CWUt(64, 256000);
    });
  event.recipes.gtceu.assembly_line("society:industry/zmod_tianshu_controller_t3")
    .itemInputs("society:assembly_core_zmod_tianshu_controller_t3", "4x gtceu:uv_robot_arm", "4x gtceu:uv_field_generator", "4x gtceu:uv_electric_motor", "2x gtceu:uv_sensor", "4x gtceu:uv_emitter", "16x #gtceu:circuits/uv")
    .inputFluids(Fluid.of("gtceu:soldering_alloy", 4608), Fluid.of("gtceu:lubricant", 8000), Fluid.of("gtceu:polybenzimidazole", 4608))
    .itemOutputs("zmod:tianshu_controller_t3")
    .duration(2400)
    .EUt(491520)
    .stationResearch(function(builder) {
      return builder
        .researchStack(Item.of("zmod:tianshu_controller_t1"))
        .researchId("sunlit_industry_zmod_tianshu_controller_t3_v1")
        .EUt(491520)
        .CWUt(64, 256000);
    });
  event.recipes.gtceu.assembly_line("society:industry/zmod_yuheng_controller_t3")
    .itemInputs("society:assembly_core_zmod_yuheng_controller_t3", "4x gtceu:uv_robot_arm", "4x gtceu:uv_field_generator", "4x gtceu:uv_electric_motor", "2x gtceu:uv_sensor", "4x gtceu:uv_emitter", "16x #gtceu:circuits/uv")
    .inputFluids(Fluid.of("gtceu:soldering_alloy", 4608), Fluid.of("gtceu:lubricant", 8000), Fluid.of("gtceu:polybenzimidazole", 4608))
    .itemOutputs("zmod:yuheng_controller_t3")
    .duration(2400)
    .EUt(491520)
    .stationResearch(function(builder) {
      return builder
        .researchStack(Item.of("zmod:yuheng_controller_t1"))
        .researchId("sunlit_industry_zmod_yuheng_controller_t3_v1")
        .EUt(491520)
        .CWUt(64, 256000);
    });
  event.recipes.gtceu.assembly_line("society:industry/zmod_qiongli_controller_t3")
    .itemInputs("society:assembly_core_zmod_qiongli_controller_t3", "4x gtceu:uv_robot_arm", "4x gtceu:uv_field_generator", "4x gtceu:uv_electric_motor", "2x gtceu:uv_sensor", "4x gtceu:uv_emitter", "16x #gtceu:circuits/uv")
    .inputFluids(Fluid.of("gtceu:soldering_alloy", 4608), Fluid.of("gtceu:lubricant", 8000), Fluid.of("gtceu:polybenzimidazole", 4608))
    .itemOutputs("zmod:qiongli_controller_t3")
    .duration(2400)
    .EUt(491520)
    .stationResearch(function(builder) {
      return builder
        .researchStack(Item.of("zmod:qiongli_controller_t1"))
        .researchId("sunlit_industry_zmod_qiongli_controller_t3_v1")
        .EUt(491520)
        .CWUt(64, 256000);
    });
  event.recipes.gtceu.assembly_line("society:industry/zmod_singularity_controller")
    .itemInputs("society:assembly_core_zmod_singularity_controller", "4x gtceu:uv_robot_arm", "4x gtceu:uv_field_generator", "4x gtceu:uv_electric_motor", "2x gtceu:uv_sensor", "4x gtceu:uv_emitter", "16x #gtceu:circuits/uv")
    .inputFluids(Fluid.of("gtceu:soldering_alloy", 4608), Fluid.of("gtceu:lubricant", 8000), Fluid.of("gtceu:polybenzimidazole", 4608))
    .itemOutputs("zmod:singularity_controller")
    .duration(2400)
    .EUt(491520)
    .stationResearch(function(builder) {
      return builder
        .researchStack(Item.of("mekanism:sps_port"))
        .researchId("sunlit_industry_zmod_singularity_controller_v1")
        .EUt(491520)
        .CWUt(64, 256000);
    });
  event.recipes.gtceu.assembly_line("society:industry/zmod_void_pylon_beacon")
    .itemInputs("society:assembly_core_zmod_void_pylon_beacon", "4x gtceu:uv_robot_arm", "4x gtceu:uv_field_generator", "4x gtceu:uv_electric_motor", "2x gtceu:uv_sensor", "4x gtceu:uv_emitter", "16x #gtceu:circuits/uv")
    .inputFluids(Fluid.of("gtceu:soldering_alloy", 4608), Fluid.of("gtceu:lubricant", 8000), Fluid.of("gtceu:polybenzimidazole", 4608))
    .itemOutputs("zmod:void_pylon_beacon")
    .duration(2400)
    .EUt(491520)
    .stationResearch(function(builder) {
      return builder
        .researchStack(Item.of("zmod:pylon_beacon"))
        .researchId("sunlit_industry_zmod_void_pylon_beacon_v1")
        .EUt(491520)
        .CWUt(64, 256000);
    });
  event.recipes.gtceu.assembly_line("society:industry/zmod_tongxuan_me_input_port")
    .itemInputs("society:assembly_core_zmod_tongxuan_me_input_port", "1x gtceu:iv_robot_arm", "1x gtceu:iv_sensor", "2x #gtceu:circuits/iv")
    .inputFluids(Fluid.of("gtceu:soldering_alloy", 576), Fluid.of("gtceu:lubricant", 1000))
    .itemOutputs("zmod:tongxuan_me_input_port")
    .duration(1200)
    .EUt(7680)
    ['scannerResearch(java.util.function.UnaryOperator)'](function(builder) {
      return builder
        .researchStack(Item.of("ae2:interface"))
        .researchId("sunlit_industry_zmod_tongxuan_me_input_port_v1")
        .EUt(7680)
        .duration(2400);
    });
  event.recipes.gtceu.assembly_line("society:industry/zmod_tongxuan_me_output_port")
    .itemInputs("society:assembly_core_zmod_tongxuan_me_output_port", "1x gtceu:iv_robot_arm", "1x gtceu:iv_sensor", "2x #gtceu:circuits/iv")
    .inputFluids(Fluid.of("gtceu:soldering_alloy", 576), Fluid.of("gtceu:lubricant", 1000))
    .itemOutputs("zmod:tongxuan_me_output_port")
    .duration(1200)
    .EUt(7680)
    ['scannerResearch(java.util.function.UnaryOperator)'](function(builder) {
      return builder
        .researchStack(Item.of("ae2:interface"))
        .researchId("sunlit_industry_zmod_tongxuan_me_output_port_v1")
        .EUt(7680)
        .duration(2400);
    });
  event.recipes.gtceu.assembly_line("society:industry/zmod_tongxuan_pattern_provider")
    .itemInputs("society:assembly_core_zmod_tongxuan_pattern_provider", "1x gtceu:luv_robot_arm", "1x gtceu:luv_sensor", "2x #gtceu:circuits/luv")
    .inputFluids(Fluid.of("gtceu:soldering_alloy", 1152), Fluid.of("gtceu:lubricant", 2000), Fluid.of("gtceu:polybenzimidazole", 1152))
    .itemOutputs("zmod:tongxuan_pattern_provider")
    .duration(1600)
    .EUt(30720)
    ['scannerResearch(java.util.function.UnaryOperator)'](function(builder) {
      return builder
        .researchStack(Item.of("ae2:pattern_provider"))
        .researchId("sunlit_industry_zmod_tongxuan_pattern_provider_v1")
        .EUt(7680)
        .duration(3200);
    });
  event.recipes.gtceu.assembly_line("society:industry/zmod_tongxuan_wireless_connector")
    .itemInputs("society:assembly_core_zmod_tongxuan_wireless_connector", "2x gtceu:luv_emitter", "2x gtceu:luv_sensor", "1x gtceu:luv_field_generator", "4x #gtceu:circuits/luv")
    .inputFluids(Fluid.of("gtceu:soldering_alloy", 1152), Fluid.of("gtceu:lubricant", 2000), Fluid.of("gtceu:polybenzimidazole", 1152))
    .itemOutputs("zmod:tongxuan_wireless_connector")
    .duration(1600)
    .EUt(30720)
    ['scannerResearch(java.util.function.UnaryOperator)'](function(builder) {
      return builder
        .researchStack(Item.of("ae2:wireless_receiver"))
        .researchId("sunlit_industry_zmod_tongxuan_wireless_connector_v1")
        .EUt(7680)
        .duration(3200);
    });
  event.recipes.gtceu.assembly_line("society:industry/zmod_precision_assembler_parallel_4x")
    .itemInputs("society:assembly_core_zmod_precision_assembler_parallel_4x", "2x gtceu:iv_robot_arm", "2x gtceu:iv_field_generator", "4x #gtceu:circuits/iv")
    .inputFluids(Fluid.of("gtceu:soldering_alloy", 576), Fluid.of("gtceu:lubricant", 1000))
    .itemOutputs("zmod:precision_assembler_parallel_4x")
    .duration(1200)
    .EUt(7680)
    ['scannerResearch(java.util.function.UnaryOperator)'](function(builder) {
      return builder
        .researchStack(Item.of("zmod:precision_assembler_parallel_2x"))
        .researchId("sunlit_industry_zmod_precision_assembler_parallel_4x_v1")
        .EUt(7680)
        .duration(2400);
    });
  event.recipes.gtceu.assembly_line("society:industry/zmod_thread_hatch_2x")
    .itemInputs("society:assembly_core_zmod_thread_hatch_2x", "2x gtceu:luv_robot_arm", "2x gtceu:luv_field_generator", "4x #gtceu:circuits/luv")
    .inputFluids(Fluid.of("gtceu:soldering_alloy", 1152), Fluid.of("gtceu:lubricant", 2000), Fluid.of("gtceu:polybenzimidazole", 1152))
    .itemOutputs("zmod:thread_hatch_2x")
    .duration(1600)
    .EUt(30720)
    ['scannerResearch(java.util.function.UnaryOperator)'](function(builder) {
      return builder
        .researchStack(Item.of("zmod:precision_assembler_parallel_4x"))
        .researchId("sunlit_industry_zmod_thread_hatch_2x_v1")
        .EUt(7680)
        .duration(3200);
    });
  event.recipes.gtceu.assembly_line("society:industry/mekanismgenerators_fusion_reactor_controller")
    .itemInputs("society:assembly_core_mekanismgenerators_fusion_reactor_controller", "4x gtceu:luv_robot_arm", "4x gtceu:luv_field_generator", "4x gtceu:luv_electric_motor", "2x gtceu:luv_sensor", "4x gtceu:luv_emitter", "8x #gtceu:circuits/luv")
    .inputFluids(Fluid.of("gtceu:soldering_alloy", 1152), Fluid.of("gtceu:lubricant", 2000), Fluid.of("gtceu:polybenzimidazole", 1152))
    .itemOutputs("mekanismgenerators:fusion_reactor_controller")
    .duration(1600)
    .EUt(30720)
    ['scannerResearch(java.util.function.UnaryOperator)'](function(builder) {
      return builder
        .researchStack(Item.of("mekanism:basic_chemical_tank"))
        .researchId("sunlit_industry_mekanismgenerators_fusion_reactor_controller_v1")
        .EUt(7680)
        .duration(3200);
    });
  event.recipes.gtceu.assembly_line("society:industry/mekanism_sps_casing")
    .itemInputs("society:assembly_core_mekanism_sps_casing", "4x gtceu:uv_robot_arm", "4x gtceu:uv_field_generator", "4x gtceu:uv_electric_motor", "2x gtceu:uv_sensor", "4x gtceu:uv_emitter", "16x #gtceu:circuits/uv")
    .inputFluids(Fluid.of("gtceu:soldering_alloy", 4608), Fluid.of("gtceu:lubricant", 8000), Fluid.of("gtceu:polybenzimidazole", 4608))
    .itemOutputs("4x mekanism:sps_casing")
    .duration(2400)
    .EUt(491520)
    .stationResearch(function(builder) {
      return builder
        .researchStack(Item.of("mekanism:pellet_polonium"))
        .researchId("sunlit_industry_mekanism_sps_casing_v1")
        .EUt(491520)
        .CWUt(64, 256000);
    });
  event.recipes.gtceu.assembly_line("society:industry/mekanism_supercharged_coil")
    .itemInputs("society:assembly_core_mekanism_supercharged_coil", "1x gtceu:uv_field_generator", "2x gtceu:uv_electric_motor", "4x #gtceu:circuits/uv")
    .inputFluids(Fluid.of("gtceu:soldering_alloy", 4608), Fluid.of("gtceu:lubricant", 8000), Fluid.of("gtceu:polybenzimidazole", 4608))
    .itemOutputs("mekanism:supercharged_coil")
    .duration(2400)
    .EUt(491520)
    .stationResearch(function(builder) {
      return builder
        .researchStack(Item.of("mekanism:laser"))
        .researchId("sunlit_industry_mekanism_supercharged_coil_v1")
        .EUt(491520)
        .CWUt(64, 256000);
    });
  event.recipes.gtceu.assembly_line("society:industry/society_wanxiang_formation_core")
    .itemInputs("forbidden_magic:wrath_cage", "zmod:transcendence_key", "4x gtceu:luv_robot_arm", "4x gtceu:luv_field_generator", "4x gtceu:luv_electric_motor", "2x gtceu:luv_sensor", "4x gtceu:luv_emitter", "8x #gtceu:circuits/luv")
    .inputFluids(Fluid.of("gtceu:soldering_alloy", 1152), Fluid.of("gtceu:lubricant", 2000), Fluid.of("gtceu:polybenzimidazole", 1152))
    .itemOutputs("society:wanxiang_formation_core")
    .duration(1600)
    .EUt(30720)
    ['scannerResearch(java.util.function.UnaryOperator)'](function(builder) {
      return builder
        .researchStack(Item.of("forbidden_magic:wrath_cage"))
        .researchId("sunlit_industry_society_wanxiang_formation_core_v1")
        .EUt(7680)
        .duration(3200);
    });
  console.info("[SUNLIT-INDUSTRY] Registered 30 assembly lines with physical GT research data");
});
