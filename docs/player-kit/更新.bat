@echo off
chcp 936 >nul
setlocal enabledelayedexpansion
cd /d "%~dp0"
title Sunlit Valley - 手动更新

echo ==========================================================
echo    Society . Sunlit Valley   手动更新
echo ==========================================================
echo.
echo  更新源: GitHub (MineRealms/UpdateRepo)
echo  如果你在国内，请先挂好梯子（系统代理 / TUN 模式）
echo  更新器会自动读取系统代理，不用额外设置
echo.

set "MANIFEST=https://raw.githubusercontent.com/MineRealms/UpdateRepo/main/manifest.json"

rem ---------- 1. 找 Java ----------
set "JAVA="
if defined JAVA_HOME if exist "%JAVA_HOME%\bin\java.exe" set "JAVA=%JAVA_HOME%\bin\java.exe"
if not defined JAVA (
  for /f "delims=" %%i in ('where java 2^>nul') do if not defined JAVA set "JAVA=%%i"
)
if not defined JAVA if exist "%~dp0jre\bin\java.exe" set "JAVA=%~dp0jre\bin\java.exe"
if not defined JAVA if exist "%~dp0java\bin\java.exe" set "JAVA=%~dp0java\bin\java.exe"
if not defined JAVA if exist "%~dp0runtime\bin\java.exe" set "JAVA=%~dp0runtime\bin\java.exe"

if not defined JAVA (
  echo [错误] 没有找到 Java。
  echo.
  echo  请先安装 Java 21（整合包必须的），装完重开这个窗口：
  echo  https://learn.microsoft.com/zh-cn/java/openjdk/download
  echo.
  pause
  exit /b 1
)
echo [1/3] Java: "!JAVA!"

rem ---------- 2. 找更新器 ----------
set "UPD="
if exist "%~dp0ModpackUpdater-all.jar" set "UPD=%~dp0ModpackUpdater-all.jar"
if not defined UPD if exist "%~dp0.minecraft\versions\Society Sunlit Valley\ModpackUpdater-all.jar" set "UPD=%~dp0.minecraft\versions\Society Sunlit Valley\ModpackUpdater-all.jar"
if not defined UPD (
  echo [错误] 没有找到 ModpackUpdater-all.jar。
  echo.
  echo  正常情况下它就在本文件夹，或者在
  echo  .minecraft\versions\Society Sunlit Valley\ 里面。
  echo  找不到的话请重新解压一遍整合包。
  echo.
  pause
  exit /b 1
)
echo [2/3] 更新器: "!UPD!"

rem ---------- 3. 跑更新 ----------
echo [3/3] 开始检查更新（弹窗里会显示进度）...
echo.
"!JAVA!" -Dfile.encoding=UTF-8 -jar "!UPD!" --client --manifest "%MANIFEST%" --target "%~dp0.minecraft" --side client

set "RC=%ERRORLEVEL%"
echo.
if "%RC%"=="0" (
  echo ==========================================================
  echo   更新完成，可以关掉这个窗口，回 HMCL 启动游戏了
  echo ==========================================================
  choice /c x /n /t 8 /d x >nul
) else (
  echo ==========================================================
  echo   更新失败（退出码 %RC%）
  echo ==========================================================
  echo   常见原因:
  echo    1. 没挂梯子 - GitHub 在国内经常连不上
  echo       开好代理后重开本窗口再试
  echo    2. 电脑时间不对 - 同步一下 Windows 时间
  echo       设置 - 时间和语言 - 立即同步
  echo    3. 杀毒软件拦截 - 暂时关掉再试
  echo.
  echo   日志: %%USERPROFILE%%\.modpackupdater\logs\
  echo.
  pause
)
endlocal
