@echo off
title Roblox Rejoin Tool
color 0A

:menu
cls
echo THOI GIAN HIEN TAI:
time /t
echo A project made by vibe coder, ty for using
echo.
echo ===============================================================================
echo            CHOOSE ANDROID EMULATOR TO RUN THE TOOL
echo            (REQUIRES PYTHON INSTALLED ON YOUR PC)
echo ===============================================================================
echo.
echo [1] MuMu Player
echo     (Use this if option 4 does not work after running it more than 2 times)
echo.
echo [2] LDPlayer
echo     (New MuMu Player also works)
echo.
echo [3] Install required Python modules
echo.
echo [4] LDPlayer (Roblox VNG)
echo     (New MuMu Player also works)
echo.
echo [5] MuMu Player (Roblox VNG)
echo.
echo [6] Check device
echo     (Can be used to start the ADB server)
echo.
echo [7] Open logcat
echo     (Android device debugger - may cause bugs)
echo.
echo [8] Kill ADB server
echo.
echo [9] EXIT
echo.
echo ===============================================================================
systeminfo | find "Hyper-V Requirements"
echo Not all messages are in English.
echo If you get errors, try to understand them or contact me on Discord: w11user
echo.

set /p choice=Nhap lua chon (choose your opinion) [1-9]: 

if "%choice%"=="1" goto mumu
if "%choice%"=="2" goto ldplayer
if "%choice%"=="3" goto install
if "%choice%"=="4" goto ldvng
if "%choice%"=="5" goto mumuvng
if "%choice%"=="6" goto check
if "%choice%"=="7" goto logcat
if "%choice%"=="8" goto killadb
if "%choice%"=="9" goto end

echo.
echo Invalid option! Please choose between 1 and 9.
pause
goto menu

:install
echo.
echo Installing required Python modules...
call "install request.cmd"
echo Done.
pause
goto menu

:check
echo.
echo Checking ADB devices...
adb devices
pause
goto menu

:logcat
echo.
echo Opening logcat...
adb logcat
pause
goto menu

:killadb
echo.
echo Killing ADB server...
adb kill-server
echo ADB server stopped.
pause
goto menu

:mumu
echo.
echo Selected option 1 - MuMu Player
python "final rj when kick (for mumu player).py"
echo Something went wrong? Press any key to return to menu.
pause >nul
goto menu

:ldplayer
echo.
echo Selected option 2 - LDPlayer
python "final rj when kick (for ldplayer).py"
echo Something went wrong? Press any key to return to menu.
pause >nul
goto menu

:ldvng
echo.
echo Selected option 4 - LDPlayer (Roblox VNG)
python "rj vng (for ldplayer).py"
echo Something went wrong? Press any key to return to menu.
pause >nul
goto menu

:mumuvng
echo.
echo Selected option 5 - MuMu Player (Roblox VNG)
python "rj vng (for mumu player).py"
echo Something went wrong? Press any key to return to menu.
pause >nul
goto menu

:end
echo.
echo Tool da dung. Nhan phim bat ky de thoat...
pause >nul
exit

