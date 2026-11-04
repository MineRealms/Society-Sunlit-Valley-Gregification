# 物品中英文名称与说明总表

整合包全部物品、方块、流体、实体的注册 ID、中文名、英文名与说明文字。用于找物品、写任务、设计配方时查名字，不用开游戏翻 JEI。

| 文件 | 内容 |
|---|---|
| `item_index.csv` | 全表，约 7.2 万条（UTF-8 BOM，Excel 可直接打开、筛选） |
| `magic_index.csv` | 神秘/魔法系子表：TC 本体与各附属、Pollution、神秘视界、星辉、植物魔法、中洲神秘学等 |
| `lang_conflicts.csv` | 同一语言键被多个来源覆盖的记录（谁覆盖了谁） |
| `runtime_names.json` | 测试服导出的运行时名称组件，用来还原 GT 材料物品与流体的名字 |
| `build_item_index.py` | 生成器；更新 mod 后重跑即可 |

## 列说明

- `namespace` / `id` / `kind`：注册命名空间、完整 ID、类型（item / block / fluid / entity）。
- `zh_cn` / `en_us`：显示名，已去掉 `§` 颜色码。
- `zh_desc` / `en_desc`：说明、提示、JEI 信息等文字。按语言键名匹配，**只是启发式**：TC 系物品的说明多在研究笔记里，这里常为空。
- `lang_key`：名称对应的语言键。
- `in_test_registry`：`yes` 表示该 ID 在测试服注册表中实际存在。
- `source`：名称来自哪个 jar / 资源包 / KubeJS。

## 来源与覆盖顺序

和游戏里一致，后者覆盖前者：

1. `mods/*.jar` 及其内嵌 `META-INF/jarjar/*.jar` 的 `assets/*/lang/{en_us,zh_cn}.json`（`.bak` 不计）
2. `options.txt` 里已启用的资源包
3. `kubejs/assets/*/lang`

GT、GTNN、Pollution 等的材料物品（粉、板、锭、流体……）名字是运行时按“前缀＋材料”拼出来的，jar 里没有逐条语言键。这部分来自 `runtime_names.json`：在本地测试服导出名称组件，再用上面的中英文语言表还原。

## 局限

- 运行时名称只覆盖测试服装载的约 20 个 mod（GT 系、TC 及部分附属、Pollution、神秘视界、星辉、植物魔法、机械动力等）。其余 mod 只收录有显式语言键的条目。
- 只有语言键、没有实际注册的条目也会出现（`in_test_registry` 为空无法区分这一点）。
- 中文全部来自 mod 自带汉化和本包覆盖，没有用在线汉化补丁。

## 重新生成

```
python -I docs/item-index/build_item_index.py
```

需要更新运行时名称时，在本地测试服用 Rosetta 执行 `H:/MinecraftMods/SunlitIndustryCompat/tools/phase3/runtime_names.snippet`，把产出的 `phase3-reports/runtime_names.json` 复制到本目录再重跑。
