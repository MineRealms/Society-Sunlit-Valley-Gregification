// priority: 0
// ============================================================
// GTCEu 玩家进度展示条箱生成器（Steam Age → LV 初期）v6
//
// 方式：指令触发生成 6~8 个【钢板条箱 gtceu:steel_crate】（72 格/个），
//       在你东侧排成一排，每个条箱装一类物资（每类 ≤72 栈，全部装得下）。
//       不再自动触发（脚本加载/重载不会刷任何东西），也不再有清理指令。
//
// 命令：
//   /gtitems         —— 生成展示条箱（新名字：/reload 后即可生效）
//   /gtdemo          —— 旧名保留（完全重启游戏进程后同样指向新逻辑）
//
// ⚠ KubeJS/Rhino 注意事项（实测踩坑）：
//   1) 循环体内的 const/let 会在每轮重新声明 → "redeclaration of var s" 报错；
//      函数体内一律用 var（函数作用域、可重复声明）
//   2) player.level 是属性，不能 player.level()
//   3) /reload、/kubejs reload 不会替换已注册的旧命令节点 → 新功能用新命令名
//   4) 命令注册需完全重启游戏进程（或重进世界）才刷新
//
// 事实核对（GTCEu 7.5.2 源码 + 7.5.3 实际存档）：
//   * 钢板条箱 gtceu:steel_crate = 72 格
//     （GTMachines.java: STEEL_CRATE = registerCrate(GTMaterials.Steel, 72, ...)；
//       存档 NBT: inventory.storage.Size = 72）
//   * GTCEu 机器 BE 暴露 Forge ITEM_HANDLER 能力
//     （MetaMachineBlockEntity.getCapability → machine.getItemHandlerCap(side, true)）
//     → KubeJS 的 block.inventory 可直接读写条箱
//   * gtceu:iron_ingot / copper_ingot / raw_iron / raw_copper / raw_gold /
//     dense_iron_plate / iron_crate 在本包不存在（统一化），已用
//     minecraft:iron_ingot / copper_ingot / raw_* 等替代
// ============================================================

const GT_DEMO_VERSION = "v6";
const GT_DEMO_BLOCK = "gtceu:steel_crate";   // 钢板条箱（72 格）
const GT_DEMO_SLOTS_FALLBACK = 72;           // 条箱格数（源码核对值）
const GT_DEMO_COUNT_MULT = 2;                // 数量倍率（贴近"普通物品 32~256"的原始需求）

console.info("[GTDEMO] gt_demo.js " + GT_DEMO_VERSION + " loaded (钢板条箱版，仅指令触发)");

// ---------- 物资表（每类最坏情况 ≤72 栈，条箱 72 格可容纳） ----------
const GT_DEMO_CHESTS = [
  {
    name: "矿物与基础资源",
    items: [
      { id: "minecraft:raw_iron", min: 64, max: 128 },
      { id: "minecraft:raw_copper", min: 64, max: 128 },
      { id: "minecraft:raw_gold", min: 32, max: 64 },
      { id: "gtceu:crushed_iron_ore", min: 32, max: 64 },
      { id: "gtceu:crushed_copper_ore", min: 32, max: 64 },
      { id: "gtceu:crushed_tin_ore", min: 32, max: 64 },
      { id: "gtceu:crushed_lead_ore", min: 32, max: 64 },
      { id: "minecraft:iron_ingot", min: 64, max: 128 },
      { id: "minecraft:copper_ingot", min: 64, max: 128 },
      { id: "gtceu:tin_ingot", min: 32, max: 64 },
      { id: "gtceu:lead_ingot", min: 32, max: 64 },
      { id: "gtceu:bronze_ingot", min: 64, max: 128 },
      { id: "gtceu:steel_ingot", min: 32, max: 64 },
      { id: "gtceu:wrought_iron_ingot", min: 32, max: 64 },
      { id: "gtceu:iron_dust", min: 32, max: 64 },
      { id: "gtceu:copper_dust", min: 32, max: 64 },
      { id: "gtceu:tin_dust", min: 32, max: 64 },
      { id: "gtceu:coal_dust", min: 32, max: 64 },
      { id: "minecraft:coal", min: 64, max: 128 },
      { id: "minecraft:redstone", min: 32, max: 64 },
      { id: "minecraft:quartz", min: 32, max: 64 },
      { id: "minecraft:lapis_lazuli", min: 32, max: 64 },
      { id: "gtceu:raw_rubber_dust", min: 32, max: 64 },
      { id: "minecraft:clay_ball", min: 32, max: 64 },
    ],
  },
  {
    name: "蒸汽加工材料",
    items: [
      { id: "gtceu:iron_plate", min: 32, max: 64 },
      { id: "gtceu:copper_plate", min: 32, max: 64 },
      { id: "gtceu:tin_plate", min: 32, max: 64 },
      { id: "gtceu:bronze_plate", min: 32, max: 64 },
      { id: "gtceu:steel_plate", min: 32, max: 64 },
      { id: "gtceu:wrought_iron_plate", min: 32, max: 64 },
      { id: "gtceu:lead_plate", min: 32, max: 64 },
      { id: "gtceu:double_iron_plate", min: 16, max: 32 },
      { id: "gtceu:double_bronze_plate", min: 16, max: 32 },
      { id: "gtceu:double_steel_plate", min: 16, max: 32 },
      { id: "gtceu:dense_steel_plate", min: 8, max: 16 },
      { id: "gtceu:iron_rod", min: 32, max: 64 },
      { id: "gtceu:copper_rod", min: 32, max: 64 },
      { id: "gtceu:bronze_rod", min: 32, max: 64 },
      { id: "gtceu:steel_rod", min: 32, max: 64 },
      { id: "gtceu:long_iron_rod", min: 16, max: 32 },
      { id: "gtceu:long_steel_rod", min: 16, max: 32 },
      { id: "gtceu:iron_gear", min: 16, max: 32 },
      { id: "gtceu:bronze_gear", min: 16, max: 32 },
      { id: "gtceu:steel_gear", min: 16, max: 32 },
      { id: "gtceu:small_iron_gear", min: 16, max: 32 },
      { id: "gtceu:small_bronze_gear", min: 16, max: 32 },
      { id: "gtceu:small_steel_gear", min: 16, max: 32 },
      { id: "gtceu:copper_single_wire", min: 32, max: 64 },
      { id: "gtceu:tin_single_wire", min: 32, max: 64 },
      { id: "gtceu:tin_single_cable", min: 32, max: 64 },
      { id: "gtceu:rubber_plate", min: 32, max: 64 },
    ],
  },
  {
    name: "蒸汽机器与部件",
    items: [
      { id: "gtceu:bronze_machine_casing", min: 16, max: 32 },
      { id: "gtceu:bronze_brick_casing", min: 16, max: 32 },
      { id: "gtceu:bronze_firebox_casing", min: 16, max: 32 },
      { id: "gtceu:bronze_gearbox", min: 8, max: 16 },
      { id: "gtceu:bronze_pipe_casing", min: 16, max: 32 },
      { id: "gtceu:bronze_drum", min: 2, max: 8 },
      { id: "gtceu:bronze_crate", min: 2, max: 8 },
      { id: "gtceu:bronze_frame", min: 16, max: 32 },
      { id: "gtceu:steel_frame", min: 16, max: 32 },
      { id: "gtceu:iron_frame", min: 16, max: 32 },
      { id: "gtceu:iron_ring", min: 16, max: 48 },
      { id: "gtceu:lp_steam_solid_boiler", min: 1, max: 2 },
      { id: "gtceu:lp_steam_liquid_boiler", min: 1, max: 2 },
      { id: "gtceu:lp_steam_solar_boiler", min: 1, max: 2 },
      { id: "gtceu:lp_steam_furnace", min: 1, max: 2 },
      { id: "gtceu:lp_steam_macerator", min: 1, max: 2 },
      { id: "gtceu:lp_steam_compressor", min: 1, max: 2 },
      { id: "gtceu:lp_steam_extractor", min: 1, max: 2 },
      { id: "gtceu:lp_steam_alloy_smelter", min: 1, max: 2 },
      { id: "gtceu:lp_steam_forge_hammer", min: 1, max: 2 },
      { id: "gtceu:lp_steam_rock_crusher", min: 1, max: 2 },
      { id: "gtceu:lp_steam_miner", min: 1, max: 1 },
      { id: "gtceu:firebricks", min: 32, max: 64 },
      { id: "gtceu:firebrick", min: 32, max: 64 },
      { id: "gtceu:coke_oven_bricks", min: 32, max: 64 },
      { id: "gtceu:coke_oven", min: 1, max: 1 },
      { id: "gtceu:coke_gem", min: 32, max: 64 },
    ],
  },
  {
    name: "化学与合成材料",
    items: [
      { id: "gtceu:rubber_ingot", min: 32, max: 64 },
      { id: "gtceu:tin_foil", min: 32, max: 64 },
      { id: "gtceu:wrought_iron_foil", min: 16, max: 48 },
      { id: "gtceu:steel_ring", min: 16, max: 48 },
      { id: "gtceu:iron_bolt", min: 32, max: 64 },
      { id: "gtceu:iron_screw", min: 32, max: 64 },
      { id: "gtceu:sulfur_dust", min: 32, max: 64 },
      { id: "gtceu:saltpeter_dust", min: 32, max: 64 },
      { id: "gtceu:calcite_dust", min: 32, max: 64 },
      { id: "gtceu:quicklime_dust", min: 32, max: 64 },
      { id: "gtceu:ash_dust", min: 32, max: 64 },
      { id: "gtceu:sodium_dust", min: 16, max: 32 },
      { id: "gtceu:carbon_dust", min: 32, max: 64 },
      { id: "gtceu:silicon_dust", min: 16, max: 32 },
      { id: "gtceu:glass_dust", min: 32, max: 64 },
      { id: "gtceu:sodium_hydroxide_dust", min: 16, max: 32 },
      { id: "gtceu:magnesium_dust", min: 16, max: 32 },
      { id: "gtceu:aluminium_dust", min: 16, max: 32 },
      { id: "gtceu:glass_tube", min: 32, max: 48 },
      { id: "gtceu:vacuum_tube", min: 32, max: 48 },
    ],
  },
  {
    name: "LV 前置材料",
    items: [
      { id: "gtceu:resistor", min: 16, max: 32 },
      { id: "gtceu:capacitor", min: 16, max: 32 },
      { id: "gtceu:diode", min: 8, max: 16 },
      { id: "gtceu:inductor", min: 8, max: 16 },
      { id: "gtceu:transistor", min: 4, max: 8 },
      { id: "gtceu:red_alloy_ingot", min: 32, max: 64 },
      { id: "gtceu:red_alloy_plate", min: 16, max: 32 },
      { id: "gtceu:fine_red_alloy_wire", min: 32, max: 64 },
      { id: "gtceu:aluminium_ingot", min: 32, max: 64 },
      { id: "gtceu:aluminium_plate", min: 16, max: 32 },
      { id: "gtceu:steel_bolt", min: 32, max: 64 },
      { id: "gtceu:steel_screw", min: 32, max: 64 },
      { id: "gtceu:bronze_bolt", min: 16, max: 48 },
      { id: "gtceu:tin_single_cable", min: 32, max: 64 },
      { id: "gtceu:copper_single_cable", min: 32, max: 64 },
      { id: "gtceu:rubber_ingot", min: 32, max: 64 },
      { id: "minecraft:glass", min: 32, max: 64 },
      { id: "minecraft:paper", min: 32, max: 64 },
      { id: "minecraft:redstone_torch", min: 16, max: 32 },
    ],
  },
  {
    name: "工具与杂物",
    items: [
      { id: "gtceu:iron_wrench", min: 1, max: 1 },
      { id: "gtceu:iron_hammer", min: 1, max: 1 },
      { id: "gtceu:iron_screwdriver", min: 1, max: 1 },
      { id: "gtceu:iron_saw", min: 1, max: 1 },
      { id: "gtceu:iron_file", min: 1, max: 1 },
      { id: "gtceu:iron_mortar", min: 1, max: 1 },
      { id: "gtceu:iron_crowbar", min: 1, max: 1 },
      { id: "gtceu:iron_wire_cutter", min: 1, max: 1 },
      { id: "gtceu:iron_mining_hammer", min: 1, max: 1 },
      { id: "gtceu:bronze_wrench", min: 1, max: 1 },
      { id: "gtceu:bronze_hammer", min: 1, max: 1 },
      { id: "gtceu:steel_wrench", min: 1, max: 1 },
      { id: "gtceu:steel_hammer", min: 1, max: 1 },
      { id: "gtceu:steel_file", min: 1, max: 1 },
      { id: "gtceu:steel_screwdriver", min: 1, max: 1 },
      { id: "gtceu:steel_drum", min: 2, max: 8 },
      { id: "gtceu:bronze_screw", min: 32, max: 64 },
      { id: "gtceu:copper_single_cable", min: 32, max: 64 },
      { id: "gtceu:coke_gem", min: 32, max: 64 },
      { id: "minecraft:torch", min: 32, max: 64 },
      { id: "minecraft:paper", min: 32, max: 64 },
    ],
  },
];

const GT_DEMO_BONUS = [
  {
    name: "燃料与建材",
    items: [
      { id: "gtceu:coke_gem", min: 64, max: 128 },
      { id: "minecraft:coal", min: 64, max: 128 },
      { id: "minecraft:charcoal", min: 64, max: 128 },
      { id: "gtceu:firebricks", min: 32, max: 64 },
      { id: "gtceu:firebrick", min: 32, max: 64 },
      { id: "gtceu:coke_oven_bricks", min: 32, max: 64 },
      { id: "minecraft:glass", min: 64, max: 128 },
      { id: "minecraft:bricks", min: 32, max: 64 },
      { id: "gtceu:bronze_drum", min: 2, max: 8 },
    ],
  },
  {
    name: "库存与杂项",
    items: [
      { id: "gtceu:steel_drum", min: 2, max: 8 },
      { id: "gtceu:bronze_crate", min: 2, max: 8 },
      { id: "minecraft:torch", min: 64, max: 128 },
      { id: "minecraft:paper", min: 64, max: 128 },
      { id: "minecraft:string", min: 32, max: 64 },
      { id: "minecraft:leather", min: 32, max: 64 },
      { id: "gtceu:tin_foil", min: 32, max: 64 },
      { id: "gtceu:bronze_plate", min: 32, max: 64 },
      { id: "gtceu:bronze_gear", min: 16, max: 32 },
    ],
  },
];

const GT_DEMO_AIR = ["minecraft:air", "minecraft:cave_air", "minecraft:void_air"];
const GT_DEMO_NON_SOLID = GT_DEMO_AIR.concat([
  "minecraft:water", "minecraft:flowing_water",
  "minecraft:lava", "minecraft:flowing_lava",
  "minecraft:short_grass", "minecraft:tall_grass", "minecraft:fern",
  "minecraft:snow",
]);

// ============================================================
// 工具函数（函数体内一律 var —— Rhino 不允许循环内重复声明 const/let）
// ============================================================
function gtDemoRandomInt(min, max) {
  return min + Math.floor(Math.random() * (max - min + 1));
}

function gtDemoSend(player, text) {
  player.tell(Text.gold("[GTDEMO] ").append(Text.white(text)));
}

// 判断某位置是否可放条箱：本身与上方为空气、下方为实体
function gtDemoCanPlace(level, x, y, z) {
  var here = level.getBlock(x, y, z);
  if (!GT_DEMO_AIR.includes(String(here.id))) return false;
  var above = level.getBlock(x, y + 1, z);
  if (!GT_DEMO_AIR.includes(String(above.id))) return false;
  var below = level.getBlock(x, y - 1, z);
  if (GT_DEMO_NON_SOLID.includes(String(below.id))) return false;
  return true;
}

// 为第 index 个条箱找位置：优先玩家东侧一排，其次上下与邻近
function gtDemoFindSpot(level, px, py, pz, index) {
  var baseX = px + 2 + 2 * index;
  var candidates = [
    [baseX, py, pz], [baseX, py + 1, pz], [baseX, py - 1, pz],
    [baseX + 1, py, pz], [baseX - 1, py, pz],
    [baseX, py + 1, pz + 1], [baseX, py + 1, pz - 1],
    [baseX, py, pz + 1], [baseX, py, pz - 1],
    [baseX, py + 1, pz + 2], [baseX, py + 1, pz - 2],
    [baseX, py, pz + 2], [baseX, py, pz - 2],
    [baseX, py - 1, pz + 1], [baseX, py - 1, pz - 1],
  ];
  for (var i = 0; i < candidates.length; i++) {
    var c = candidates[i];
    if (gtDemoCanPlace(level, c[0], c[1], c[2])) {
      return { x: c[0], y: c[1], z: c[2] };
    }
  }
  return null;
}

// 放置条箱并用【新的 getBlock】读回验证
// 返回 { spot, block } 或 null；条箱放置失败时兜底改用木箱（并在日志/聊天说明）
function gtDemoPlace(level, spot) {
  level.getBlock(spot.x, spot.y, spot.z).set(GT_DEMO_BLOCK);
  var check = level.getBlock(spot.x, spot.y, spot.z);
  var id = String(check.id);
  if (id === GT_DEMO_BLOCK) {
    return { spot: spot, block: GT_DEMO_BLOCK };
  }
  console.warn("[GTDEMO] 条箱放置失败 @ " + spot.x + "," + spot.y + "," + spot.z
    + " -> " + id + "，改用木箱兜底");
  level.getBlock(spot.x, spot.y, spot.z).set("minecraft:chest");
  var check2 = level.getBlock(spot.x, spot.y, spot.z);
  if (String(check2.id) === "minecraft:chest") {
    return { spot: spot, block: "minecraft:chest" };
  }
  console.warn("[GTDEMO] 放置彻底失败 @ " + spot.x + "," + spot.y + "," + spot.z);
  return null;
}

// 装填一类物资；返回 { filled, leftover, countBack, slots }
function gtDemoFill(level, spot, category, skipped) {
  var inv = level.getBlock(spot.x, spot.y, spot.z).inventory;
  if (!inv) {
    console.warn("[GTDEMO] 取不到容器 @ " + spot.x + "," + spot.y + "," + spot.z);
    return { filled: 0, leftover: -1, countBack: -1, slots: 0 };
  }
  var slots = GT_DEMO_SLOTS_FALLBACK;
  try {
    slots = inv.getSlots();
  } catch (err) {
    slots = GT_DEMO_SLOTS_FALLBACK;
  }
  var filled = 0;
  var leftover = 0;
  var slot = 0;
  for (var i = 0; i < category.items.length; i++) {
    var entry = category.items[i];
    if (Item.of(entry.id).isEmpty()) {
      skipped.add(entry.id);
      continue;
    }
    var remaining = gtDemoRandomInt(entry.min, entry.max) * GT_DEMO_COUNT_MULT;
    while (remaining > 0) {
      if (slot >= slots) {
        leftover += remaining;
        break;
      }
      var n = Math.min(remaining, 64);
      inv.setStackInSlot(slot, Item.of(entry.id, n));
      filled++;
      remaining -= n;
      slot++;
    }
  }
  var countBack = 0;
  try {
    for (var k = 0; k < slots; k++) {
      var st = inv.getStackInSlot(k);
      if (st && !st.isEmpty()) countBack += st.getCount();
    }
  } catch (err2) {
    countBack = -1;
  }
  return { filled: filled, leftover: leftover, countBack: countBack, slots: slots };
}

// ============================================================
// 生成逻辑（仅由指令调用）
// ============================================================
function generateDemo(player) {
  var level = player.level; // 属性，不是方法
  var center = player.blockPosition();
  var px = Math.floor(Number(center.getX()));
  var py = Math.floor(Number(center.getY()));
  var pz = Math.floor(Number(center.getZ()));
  console.info("[GTDEMO] === " + GT_DEMO_VERSION + " 生成条箱 @ " + px + "," + py + "," + pz
    + " dim=" + String(level.dimension) + " ===");

  var skipped = new Set();
  var chestList = GT_DEMO_CHESTS.slice();
  var bonusCount = Math.floor(Math.random() * 3);
  for (var b = 0; b < bonusCount; b++) chestList.push(GT_DEMO_BONUS[b]);

  var generated = 0;
  var fallback = 0;
  var coords = [];
  for (var c = 0; c < chestList.length; c++) {
    var category = chestList[c];
    try {
      var spot = gtDemoFindSpot(level, px, py, pz, c);
      if (!spot) {
        console.warn("[GTDEMO] 跳过 #" + (c + 1) + " " + category.name + "：找不到安全位置");
        continue;
      }
      var placed = gtDemoPlace(level, spot);
      if (!placed) continue;
      if (placed.block !== GT_DEMO_BLOCK) fallback++;
      var result = gtDemoFill(level, placed.spot, category, skipped);
      generated++;
      coords.push("#" + (c + 1) + "(" + placed.spot.x + "," + placed.spot.y + "," + placed.spot.z + ")");
      console.info("[GTDEMO] OK #" + (c + 1) + " " + category.name + " @ "
        + placed.spot.x + "," + placed.spot.y + "," + placed.spot.z
        + " 容器=" + placed.block + " 格数=" + result.slots + " 填入=" + result.filled
        + " 读回=" + result.countBack + " 溢出=" + result.leftover);
    } catch (err) {
      console.error("[GTDEMO] 异常 #" + (c + 1) + " " + category.name + ": " + err);
    }
  }

  var msg = "【" + GT_DEMO_VERSION + "】已生成 " + generated + " 个钢板条箱（72 格/个）";
  if (fallback > 0) msg += "（其中 " + fallback + " 个条箱放置失败，已用木箱兜底）";
  if (skipped.size > 0) msg += "；跳过 " + skipped.size + " 个不存在的物品（见控制台）";
  gtDemoSend(player, msg);
  if (coords.length > 0) {
    gtDemoSend(player, "位置：" + coords.join(" "));
  }
  if (skipped.size > 0) {
    console.warn("[GTDEMO] 不存在的物品 ID（已跳过）: " + Array.from(skipped).join(", "));
  }
  console.info("[GTDEMO] generated " + generated + " crates");
}

// ============================================================
// 命令注册
//   /gtitems   —— 生成展示条箱（新名字：/reload 后即可生效）
//   /gtdemo    —— 旧名保留（完全重启游戏进程后同样指向新逻辑）
// ============================================================
ServerEvents.commandRegistry((event) => {
  var Commands = event.commands;

  function registerGtDemoCommand(name) {
    event.register(
      Commands.literal(name)
        .requires((source) => source.hasPermission(2))
        .executes((ctx) => {
          if (ctx.source.player) generateDemo(ctx.source.player);
          return 1;
        })
    );
  }

  // 先注册新名字（即使旧名字重复注册报错也不影响新命令生效）
  registerGtDemoCommand("gtitems");
  registerGtDemoCommand("gtdemo");
});
