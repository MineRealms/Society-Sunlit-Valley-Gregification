# 工具与命令（发布 / 打包 / HUD / 服务器）

> 所有路径以本机为准；`powershell` 为 5.1，链式命令用 `; if ($?) { ... }`，不要用 `&&`。

## 1. 任务生成器

位置：`config/ftbquests/tools/`

| 脚本 | 章节 | ID 登记表 |
|---|---|---|
| `build_thaumic_addons_chapter.py` | `thaumic_addons.snbt`（56 任务 / 8 集群） | `thaumic_addons_ids.json` |
| `build_middle_earth_chapter.py` | `middle_earth.snbt`（19 任务；保留旧 7 任务 ID） | `middle_earth_ids.json` |
| `build_astral_sorcery_chapter.py` | `astral_sorcery.snbt`（69 任务） | `astral_sorcery_ids.json` |
| `build_pollution_chapter.py` | `pollution.snbt`（42 任务） | `pollution_ids.json` |
| `build_technomancy_chapter.py` | `technomancy.snbt` | `technomancy_ids.json` |
| `build_space_chapter.py` | `space.snbt` | — |
| `build_mek_chapter.py` | `mekanism.snbt` | — |
| `build_twilight_forest_chapter.py` | `twilight_forest.snbt` | `twilightforest_ids.md` |
| `build_thaumcraft_chapter.py` | `thaumcraft.snbt` | — |

中州章节（`--verify-repeat` 为只读检查）：

```powershell
$tool = 'config\ftbquests\tools\build_middle_earth_chapter.py'
python $tool --check            # 只校验，需 map 与输出均和生成结果一致
python $tool --verify-repeat    # 两次内存生成，要求 SNBT/map 字节一致
python $tool                    # 验证通过后写入 middle_earth.snbt + middle_earth_ids.json
```

中州 generator 会核对当前 ME jar 的英文物品键/模型、13 个关键 recipe 资源、旧 7 个任务 ID、全库 FTBQ ID 冲突及依赖环。建任务用手动 checkmark 表示派系/操作确认，别假称 item task 能检测玩家选择。

标准流程：

```powershell
$tool = 'config\ftbquests\tools\build_thaumic_addons_chapter.py'
python $tool --check            # 只校验（含已发布字节比对），不写盘
python $tool --verify-repeat    # 两次构建字节一致（防随机 ID）
python $tool                    # 生成并写盘
```

- 校验失败 = 不要写盘，先修脚本/登记表。
- 新增任务 ID 必须先在 `*_ids.json` 登记（16 位大写十六进制）。
- 改完任务后跑 `--check`，再同步到服务器（只允许 kubejs / ftbquests）。

历史脚本（一次性，别重复跑）：`port_gregtech_quests.py`、`translate_gregtech_quests.py`、`build_server_pack.py`。

## 2. 发布到 GitHub 更新器

```powershell
& 'H:\MinecraftMods\ModpackUpdater\dist\ModpackUpdater\cli.cmd' --publish-all "G:\MinecraftGames\Sunlit Valley(BaopuEdition)\mirror"
```

- 发布源 = `...\mirror\versions\Society Sunlit Valley`（mods / config / kubejs）
- 输出：`H:\MinecraftMods\pack-manifest.json` + GitHub release 资产（tag `latest`）
- 核对：`pack-manifest.json` 里目标文件的 `sha256` 与本地一致
- 客户端清单：`https://raw.githubusercontent.com/MineRealms/UpdateRepo/main/manifest.json`（CDN 约 5 分钟缓存，急用时等或在 URL 后加参数）
- 玩家端自动更新由 `ModpackUpdater-all.jar` 在 HMCL 的 `precalledCommand` 里执行：
  `"$INST_JAVA" -jar "$INST_DIR\ModpackUpdater-all.jar" --client --manifest https://raw.githubusercontent.com/MineRealms/UpdateRepo/main/manifest.json --side client`
  （配置在 `versions/<版本>/hmclversion.cfg`；`gameDirType: 1` = 版本隔离）

## 3. 客户端整合包打包

根目录：`G:\MinecraftGames\Sunlit Valley(BaopuEdition)\`

| 文件 | 内容 |
|---|---|
| `Society-Sunlit-Valley-1.20.1.zip` | HMCL + `.minecraft/versions/<版本>`（mods/config/kubejs） |
| `...-assets-libraries.zip` | `.minecraft/assets` + `.minecraft/libraries`（离线用） |
| `...-DELTA*.zip` | 增量修复（缺库/更新器/HUD 配置） |

注意（踩过的坑）：
- **必须**包含 `versions/<版本>/hmclversion.cfg`（版本隔离 + 更新器命令）、`ModpackUpdater-all.jar`、`modpack.cfg`、`servers.dat`
- **必须**包含 `.hmcl/`（HMCL 便携模式；否则启动器用 `%APPDATA%\.minecraft`）
- `.minecraft/libraries` 需要 Forge 运行库：`client-1.20.1-…-srg.jar`、`-extra.jar`、`forge-…-client.jar`、`-universal.jar`、`fmlcore`/`javafmllanguage`/`lowcodelanguage`/`mclanguage`（部分在 `delta\.minecraft\libraries` 里）
- 校验方法：从对端 `launch.bat` 或崩溃日志里提取 `libraries\...jar` 列表，逐个 `Test-Path`
- `Sync-SunlitPack.ps1` 可按 `reference-manifest.tsv` 做 SHA256 差异检查/修复，`-Fix <zip>` 模式不需要参照安装

## 4. Sunlit HUD 构建

```powershell
& 'H:\MinecraftMods\gradle-8.14.5\bin\gradle.bat' --no-daemon build   # 工作目录 H:\MinecraftMods\SunlitHud
# 产物 build\libs\sunlithud-1.20.1-0.1.0.jar
```

- 依赖：`dev.latvian.mods:kubejs-forge:2001.6.5-build.16` + `rhino-forge`（compileOnly/runtimeOnly 都配了）
- 客户端 + 服务端都要放；`kubejs.plugins.txt` 里注册 `com.society.sunlithud.kjs.SunlitHudPlugin`
- 面板脚本：`kubejs/server_scripts/sunlitHud.js`

## 5. 服务器（Rosetta 桥）

```powershell
$R = 'H:\MinecraftMods\RainJava-work\RosettaRemoteDebugBridge\legacy\tools\rosetta_remote.py'
$base = @('--host','frp-top.com','--port','17799','--token','<token>')
python $R @base ping
python $R @base ls 'C:/Users/Administrator/Downloads/emoney/kubejs/server_scripts'
python $R @base upload <本地文件> 'C:/Users/Administrator/Downloads/emoney/kubejs/...'
python $R @base console 'minecraft:reload'
python $R @base tail 'C:/Users/Administrator/Downloads/emoney/logs/latest.log' 500
```

- 只允许传 **kubejs / ftbquests**；mod 由人工放置并重启
- `console`/`shell` 可能超时（返回 TimeoutException），实际命令已下发，用 `tail` 看日志确认
- 服务端 = Mohist（Forge + Bukkit 插件）；插件放 `plugins/`，mod 放 `mods/`

## 6. 常用体检命令

```powershell
# 章节任务数
(Select-String -Path config\ftbquests\quests\chapters\thaumic_addons.snbt -Pattern '^\s*id: "').Count
# 脚本加载是否报错
Select-String -Path logs\kubejs\server.log -Pattern 'ERROR|WARN'
# 配方解析错误
Select-String -Path logs\latest.log -Pattern 'Parsing error loading recipe'
# 指定 mod 的哈希
Get-FileHash -LiteralPath mods\<jar> -Algorithm SHA256
```
