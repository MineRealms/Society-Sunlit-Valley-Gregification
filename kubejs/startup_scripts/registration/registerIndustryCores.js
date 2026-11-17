// priority: 100
// Registry IDs are shared by the client and server; changes require a full restart.
StartupEvents.registry("item", function(event) {
  let items = [
  {
    "id": "society:industrial_matrix_iv",
    "name": "IV \u5965\u672f\u5de5\u4e1a\u77e9\u9635",
    "texture": "zmod:item/mystic_circuit"
  },
  {
    "id": "society:industrial_matrix_luv",
    "name": "LuV \u5965\u672f\u5de5\u4e1a\u77e9\u9635",
    "texture": "zmod:item/mystic_circuit"
  },
  {
    "id": "society:industrial_matrix_zpm",
    "name": "ZPM \u5965\u672f\u5de5\u4e1a\u77e9\u9635",
    "texture": "zmod:item/mystic_circuit"
  },
  {
    "id": "society:assembly_core_zmod_transcendence_key",
    "name": "[IV] \u5316\u5883\u7384\u94a5\u88c5\u914d\u539f\u6838",
    "texture": "zmod:item/lattice_control_core"
  },
  {
    "id": "society:assembly_core_zmod_taiyi_matrix",
    "name": "[LuV] \u592a\u4e00\u7b26\u67a2\u88c5\u914d\u539f\u6838",
    "texture": "zmod:item/lattice_control_core"
  },
  {
    "id": "society:assembly_core_zmod_transcendence_core",
    "name": "[UV] \u8d85\u8d8a\u6838\u5fc3\u88c5\u914d\u539f\u6838",
    "texture": "zmod:item/lattice_control_core"
  },
  {
    "id": "society:assembly_core_zmod_precision_assembler_controller",
    "name": "[IV] \u7cbe\u5bc6\u88c5\u914d\u4eea\u63a7\u5236\u5668\u88c5\u914d\u539f\u6838",
    "texture": "zmod:item/lattice_control_core"
  },
  {
    "id": "society:assembly_core_zmod_industrial_crusher_controller",
    "name": "[IV] \u78c1\u51b2\u7c89\u788e\u673a\u63a7\u5236\u5668\u88c5\u914d\u539f\u6838",
    "texture": "zmod:item/lattice_control_core"
  },
  {
    "id": "society:assembly_core_zmod_industrial_pump_controller",
    "name": "[LuV] \u5de5\u4e1a\u6cf5\u7ad9\u63a7\u5236\u5668\u88c5\u914d\u539f\u6838",
    "texture": "zmod:item/lattice_control_core"
  },
  {
    "id": "society:assembly_core_zmod_fluid_processing_plant_controller",
    "name": "[LuV] \u6d41\u4f53\u5904\u7406\u5382\u63a7\u5236\u5668\u88c5\u914d\u539f\u6838",
    "texture": "zmod:item/lattice_control_core"
  },
  {
    "id": "society:assembly_core_zmod_tokamak_controller",
    "name": "[ZPM] \u6258\u5361\u9a6c\u514b\u63a7\u5236\u5668\u88c5\u914d\u539f\u6838",
    "texture": "zmod:item/lattice_control_core"
  },
  {
    "id": "society:assembly_core_zmod_tokamak_magnetic_coil",
    "name": "[ZPM] \u78c1\u7ea6\u675f\u7ebf\u5708\u88c5\u914d\u539f\u6838",
    "texture": "zmod:item/lattice_control_core"
  },
  {
    "id": "society:assembly_core_zmod_tianxuan_controller",
    "name": "[ZPM] \u5316\u5b66\u53cd\u5e94\u7089\u63a7\u5236\u5668\u88c5\u914d\u539f\u6838",
    "texture": "zmod:item/lattice_control_core"
  },
  {
    "id": "society:assembly_core_zmod_plasma_refinery_controller",
    "name": "[ZPM] \u7b49\u79bb\u5b50\u7cbe\u70bc\u7089\u63a7\u5236\u5668\u88c5\u914d\u539f\u6838",
    "texture": "zmod:item/lattice_control_core"
  },
  {
    "id": "society:assembly_core_zmod_warped_polymerizer_controller",
    "name": "[ZPM] \u626d\u66f2\u805a\u5408\u5668\u63a7\u5236\u5668\u88c5\u914d\u539f\u6838",
    "texture": "zmod:item/lattice_control_core"
  },
  {
    "id": "society:assembly_core_zmod_yaoguang_controller",
    "name": "[ZPM] \u6447\u5149\u63a7\u5236\u6743\u88c5\u914d\u539f\u6838",
    "texture": "zmod:item/lattice_control_core"
  },
  {
    "id": "society:assembly_core_zmod_integrated_ore_processing_plant_controller",
    "name": "[UV] \u96c6\u6210\u5f0f\u77ff\u7269\u5904\u7406\u5382\u63a7\u5236\u5668\u88c5\u914d\u539f\u6838",
    "texture": "zmod:item/lattice_control_core"
  },
  {
    "id": "society:assembly_core_zmod_matter_reconstructor_controller",
    "name": "[UV] \u7269\u8d28\u91cd\u6784\u4eea\u63a7\u5236\u5668\u88c5\u914d\u539f\u6838",
    "texture": "zmod:item/lattice_control_core"
  },
  {
    "id": "society:assembly_core_zmod_tianshu_controller_t3",
    "name": "[UV] \u8d85\u51e1\u5165\u5723\u00b7\u5929\u67a2\u63a7\u5236\u5668\u88c5\u914d\u539f\u6838",
    "texture": "zmod:item/lattice_control_core"
  },
  {
    "id": "society:assembly_core_zmod_yuheng_controller_t3",
    "name": "[UV] \u8d85\u51e1\u5165\u5723\u00b7\u7389\u8861\u63a7\u5236\u5668\u88c5\u914d\u539f\u6838",
    "texture": "zmod:item/lattice_control_core"
  },
  {
    "id": "society:assembly_core_zmod_qiongli_controller_t3",
    "name": "[UV] \u7edd\u9ad8\u65e0\u4e0a\u00b7\u795e\u79d8\u4e4b\u773c-\u7a77\u7406\u63a7\u5236\u5668\u88c5\u914d\u539f\u6838",
    "texture": "zmod:item/lattice_control_core"
  },
  {
    "id": "society:assembly_core_zmod_singularity_controller",
    "name": "[UV] \u7edd\u9ad8\u65e0\u4e0a\u00b7\u5929\u6743\u88c5\u914d\u539f\u6838",
    "texture": "zmod:item/lattice_control_core"
  },
  {
    "id": "society:assembly_core_zmod_void_pylon_beacon",
    "name": "[UV] \u865a\u7a7a\u6c34\u6676\u6298\u8d8a\u4fe1\u6807\u88c5\u914d\u539f\u6838",
    "texture": "zmod:item/lattice_control_core"
  },
  {
    "id": "society:assembly_core_zmod_tongxuan_me_input_port",
    "name": "[IV] \u901a\u7384ME \u8f93\u5165\u7aef\u53e3\u88c5\u914d\u539f\u6838",
    "texture": "zmod:item/lattice_control_core"
  },
  {
    "id": "society:assembly_core_zmod_tongxuan_me_output_port",
    "name": "[IV] \u901a\u7384ME \u8f93\u51fa\u7aef\u53e3\u88c5\u914d\u539f\u6838",
    "texture": "zmod:item/lattice_control_core"
  },
  {
    "id": "society:assembly_core_zmod_tongxuan_pattern_provider",
    "name": "[LuV] \u901a\u7384\u6837\u677f\u4f9b\u5e94\u5668\u88c5\u914d\u539f\u6838",
    "texture": "zmod:item/lattice_control_core"
  },
  {
    "id": "society:assembly_core_zmod_tongxuan_wireless_connector",
    "name": "[LuV] \u901a\u7384\u65e0\u7ebf\u8fde\u63a5\u5668\u88c5\u914d\u539f\u6838",
    "texture": "zmod:item/lattice_control_core"
  },
  {
    "id": "society:assembly_core_zmod_precision_assembler_parallel_4x",
    "name": "[IV] \u5e76\u884c\u63a5\u53e3\uff084X\uff09\u88c5\u914d\u539f\u6838",
    "texture": "zmod:item/lattice_control_core"
  },
  {
    "id": "society:assembly_core_zmod_thread_hatch_2x",
    "name": "[LuV] 2\u00d7\u7ebf\u7a0b\u4ed3\u88c5\u914d\u539f\u6838",
    "texture": "zmod:item/lattice_control_core"
  },
  {
    "id": "society:assembly_core_mekanismgenerators_fusion_reactor_controller",
    "name": "[LuV] MEK \u805a\u53d8\u53cd\u5e94\u5806\u88c5\u914d\u539f\u6838",
    "texture": "zmod:item/lattice_control_core"
  },
  {
    "id": "society:assembly_core_mekanism_sps_casing",
    "name": "[UV] MEK SPS \u5916\u58f3\u88c5\u914d\u539f\u6838",
    "texture": "zmod:item/lattice_control_core"
  },
  {
    "id": "society:assembly_core_mekanism_supercharged_coil",
    "name": "[UV] MEK \u8d85\u7ea7\u5145\u80fd\u7ebf\u5708\u88c5\u914d\u539f\u6838",
    "texture": "zmod:item/lattice_control_core"
  },
  {
    "id": "society:wanxiang_formation_core",
    "name": "[LuV] \u4e07\u8c61\u7b3c\u6210\u578b\u6838\u5fc3",
    "texture": "zmod:item/lattice_control_core"
  }
];
  items.forEach(function(item) {
    event.create(item.id).texture(item.texture).displayName(item.name).maxStackSize(64);
  });
});
