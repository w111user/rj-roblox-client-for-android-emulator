@echo off
title Roblox Rejoin Tool
color 0A

:menu
cls
echo THOI GIAN HIEN TAI:
time /t
echo A project made by vibe coder, ty for using
echo =====================================================================================
echo                 CHON GIA LAP DE CHAY TOOL (YEU CAU: MAY CO PYTHON)
echo       CHOOSE YOUR ANDROID EMULATOR TO RUN (NEED TO HAVE PYTHON ON YOUR DEVICES)
echo =====================================================================================
echo [1] MuMu Player (run it if the selection 4 not working when u runned it for more than 2 times)
echo [2] LDPlayer (New MuMu Player works too)
echo [3] Install some important python modules
echo [4] LDPlayer (for roblox vng, also new MuMu Player works too)
echo [5] MuMu Player (for roblox vng)
echo [6] Check device (u can use this to start adb server)
echo [7] Open logcat (android device debugger, idc it will cause bugs or not)
echo [8] Kill server adb
echo [9] EXIT
systeminfo | find "Hyper-V Requirements"
echo Not all of them are english, try your best to know the error or contact me in discord: w11user
echo.
set /p choice=Nhap lua chon (choose your opinions) [1-9]: 

if "%choice%"=="1" goto mumu
if "%choice%"=="2" goto ldplayer
if "%choice%"=="3" goto install
if "%choice%"=="4" goto ldvng
if "%choice%"=="5" goto mumuvng
if "%choice%"=="6" goto check
if "%choice%"=="7" adb logcat
if "%choice%"=="8" adb kill-server
if "%choice%"=="9" exit
goto menu

:install
echo.
echo Installing...
"install request.cmd"
echo done
pause
goto menu

:check
echo.
echo loading adb command...
adb devices
pause
goto menu

:mumu
echo.
echo Selected optinion 1, loading...
python "final rj when kick (for mumu player).py"
echo co j do sai sai... nhan phim bat ki de ve menu
pause >nul
goto menu

:ldplayer
echo.
echo Selected optinion 2, loading...
python "final rj when kick (for ldplayer).py"
echo co j do sai sai... nhan phim bat ki de ve menu
pause >nul
goto menu

:ldvng
echo.
echo Selected optinion 4, loading...
python "rj vng (for ldplayer).py"
echo co j do sai sai... nhan phim bat ki de ve menu
pause >nul
goto menu

:mumuvng
echo.
echo Selected optinion 5, loading...
python "rj vng (for mumu player).py"
echo co j do sai sai... nhan phim bat ki de ve menu
pause >nul
goto menu

:end
echo.
echo Tool da dung. Nhan phim bat ky de thoat...
pause >nul
