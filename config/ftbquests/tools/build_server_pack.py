# -*- coding: utf-8 -*-
"""
生成「服务端任务书汉化资源包」：把 kubejs 的 ftbquestlocalizer 语言文件
打包成资源包（assets/minecraft/lang/*.json），供服务端 server.properties 下发。

用法（在整合包根目录执行）:
    python config/ftbquests/tools/build_server_pack.py

产出:
    <整合包上级目录>/server-pack/GT-Quests-Localization.zip

服务端配置（server.properties）:
    resource-pack=<资源包直链 URL>
    resource-pack-sha1=<脚本输出的 SHA1>
    require-resource-pack=false          # true = 玩家拒绝则踢出
    resource-pack-prompt={"text":"本服需要任务书汉化资源包（自动下载）","color":"gold"}

说明:
    - 客户端进服会自动下载该资源包，原版/Forge 语言系统会加载其中的 lang，
      从而解析任务书里的 {ftbquests.chapter...} 键
    - 每次改动任务文本/汉化后需重新运行本脚本，并把新的 SHA1 填回 server.properties
"""

import hashlib
import json
import os
import zipfile

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(TOOLS_DIR, "..", "..", ".."))
LANG_DIR = os.path.join(ROOT, "kubejs", "assets", "ftbquestlocalizer", "lang")
# 输出到启动器根目录（整合包版本目录之外），避免被更新器误发布
OUT_DIR = os.path.abspath(os.path.join(ROOT, "..", "..", "..", "server-pack"))
OUT = os.path.join(OUT_DIR, "GT-Quests-Localization.zip")

PACK_FORMAT = 15  # 1.20.1 资源包格式
DESCRIPTION = "Society: Sunlit Valley - FTB Quests Localization"
FIXED_TIME = (2026, 1, 1, 0, 0, 0)  # 固定时间戳，保证内容不变时 SHA1 稳定


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    lang_files = sorted(f for f in os.listdir(LANG_DIR) if f.endswith(".json"))
    if not lang_files:
        raise SystemExit(f"未找到语言文件: {LANG_DIR}")

    def writestr(z, name, data):
        info = zipfile.ZipInfo(name, date_time=FIXED_TIME)
        info.compress_type = zipfile.ZIP_DEFLATED
        z.writestr(info, data)

    pack_mcmeta = {"pack": {"pack_format": PACK_FORMAT, "description": DESCRIPTION}}
    with zipfile.ZipFile(OUT, "w") as z:
        writestr(z, "pack.mcmeta", json.dumps(pack_mcmeta, ensure_ascii=False, indent=2))
        for fn in lang_files:
            data = open(os.path.join(LANG_DIR, fn), encoding="utf-8").read()
            writestr(z, f"assets/minecraft/lang/{fn}", data)
            print(f"  + assets/minecraft/lang/{fn}  ({len(data)/1024:.0f} KB)")

    raw = open(OUT, "rb").read()
    sha1 = hashlib.sha1(raw).hexdigest()
    print()
    print(f"资源包: {OUT}")
    print(f"大小  : {len(raw)/1024/1024:.2f} MB")
    print(f"SHA1  : {sha1}")
    print()
    print("把资源包上传到可访问的直链（如 GitHub Release 附件），然后配置:")
    print("  resource-pack=<直链>")
    print(f"  resource-pack-sha1={sha1}")


if __name__ == "__main__":
    main()
