#!/bin/bash
# Society · Sunlit Valley 手动更新（macOS）
# 双击运行；第一次如果提示没有权限，先在终端执行:
#   chmod +x "更新.command"

cd "$(dirname "$0")" || exit 1

MANIFEST="https://raw.githubusercontent.com/MineRealms/UpdateRepo/main/manifest.json"

echo "=========================================================="
echo "   Society · Sunlit Valley   手动更新（macOS）"
echo "=========================================================="
echo ""
echo " 更新源: GitHub (MineRealms/UpdateRepo)"
echo " 国内请先开梯子（ClashX / Surge 的「系统代理」或 TUN 模式）"
echo " 脚本会自动读取 macOS 系统代理设置"
echo ""

# ---------- 1. 找 Java ----------
JAVA=""
if [ -n "$JAVA_HOME" ] && [ -x "$JAVA_HOME/bin/java" ]; then
  JAVA="$JAVA_HOME/bin/java"
fi
if [ -z "$JAVA" ] && [ -x "/usr/libexec/java_home" ]; then
  JH=$(/usr/libexec/java_home -v 21 2>/dev/null)
  if [ -n "$JH" ] && [ -x "$JH/bin/java" ]; then JAVA="$JH/bin/java"; fi
fi
if [ -z "$JAVA" ] && command -v java >/dev/null 2>&1; then
  JAVA=$(command -v java)
fi
for CAND in "./jre/bin/java" "./java/bin/java" "./runtime/bin/java"; do
  if [ -z "$JAVA" ] && [ -x "$CAND" ]; then JAVA="$CAND"; fi
done

if [ -z "$JAVA" ]; then
  echo "[错误] 没有找到 Java。"
  echo ""
  echo "  请先安装 Java 21（整合包必须的），装完重开这个窗口："
  echo "  https://learn.microsoft.com/zh-cn/java/openjdk/download"
  echo ""
  read -n 1 -s -r -p "按任意键关闭..."
  exit 1
fi
echo "[1/3] Java: $JAVA"

# ---------- 2. 找更新器 ----------
UPD=""
if [ -f "./ModpackUpdater-all.jar" ]; then
  UPD="./ModpackUpdater-all.jar"
elif [ -f "./.minecraft/versions/Society Sunlit Valley/ModpackUpdater-all.jar" ]; then
  UPD="./.minecraft/versions/Society Sunlit Valley/ModpackUpdater-all.jar"
fi

if [ -z "$UPD" ]; then
  echo "[错误] 没有找到 ModpackUpdater-all.jar。"
  echo ""
  echo "  正常情况下它就在本文件夹，或者在"
  echo "  .minecraft/versions/Society Sunlit Valley/ 里面。"
  echo "  找不到的话请重新解压一遍整合包。"
  echo ""
  read -n 1 -s -r -p "按任意键关闭..."
  exit 1
fi
echo "[2/3] 更新器: $UPD"

# ---------- 3. 系统代理 ----------
PROXY_OPTS=()
PH=$(scutil --proxy 2>/dev/null | awk '/HTTPSProxy/ {print $3}')
PP=$(scutil --proxy 2>/dev/null | awk '/HTTPSPort/ {print $3}')
if [ -n "$PH" ] && [ -n "$PP" ]; then
  echo "[3/4] 使用系统代理 $PH:$PP"
  PROXY_OPTS=(-Dhttps.proxyHost="$PH" -Dhttps.proxyPort="$PP" -Dhttp.proxyHost="$PH" -Dhttp.proxyPort="$PP")
else
  echo "[3/4] 没检测到系统代理，直连 GitHub（国内可能失败）"
fi

# ---------- 4. 更新 ----------
echo "[4/4] 开始检查更新..."
echo ""
"$JAVA" -Dfile.encoding=UTF-8 "${PROXY_OPTS[@]}" -jar "$UPD" --client --manifest "$MANIFEST" --target "./.minecraft" --side client
RC=$?

echo ""
if [ "$RC" -eq 0 ]; then
  echo "=========================================================="
  echo "  更新完成，可以关掉这个窗口，回 HMCL 启动游戏了"
  echo "=========================================================="
  sleep 5
else
  echo "=========================================================="
  echo "  更新失败（退出码 $RC）"
  echo "=========================================================="
  echo "  常见原因:"
  echo "   1. 没挂梯子 - GitHub 在国内经常连不上"
  echo "      开好代理后重开本窗口再试"
  echo "   2. 系统时间不对 - 打开「日期与时间」勾选自动设置"
  echo "   3. 安全软件拦截 - 暂时关掉再试"
  echo ""
  echo "  日志: ~/.modpackupdater/logs/"
  echo ""
  read -n 1 -s -r -p "按任意键关闭..."
fi
