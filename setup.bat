@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

cd /d "%~dp0"
title ⚡ ZYRON ASSISTANT - PREMIUM SETUP ⚡
color 0D

cls
echo.
echo.
echo      ███████╗██╗   ██╗██████╗  ██████╗ ███╗   ██╗
echo      ╚══███╔╝╚██╗ ██╔╝██╔══██╗██╔═══██╗████╗  ██║
echo        ███╔╝  ╚████╔╝ ██████╔╝██║   ██║██╔██╗ ██║
echo       ███╔╝    ╚██╔╝  ██╔══██╗██║   ██║██║╚██╗██║
echo      ███████╗   ██║   ██║  ██║╚██████╔╝██║ ╚████║
echo      ╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
echo.
echo            ⚡  Z Y R O N   A S S I S T A N T  ⚡
echo.

color 0D
echo   ═══════════════════════════════════════════════════════════════════════
echo            ⚡  SYSTEM INITIALIZATION SEQUENCE ENGAGED  ⚡
echo   ═══════════════════════════════════════════════════════════════════════
echo.

:: ===================== STEP 1 =====================
echo   [1/6] Selecting Python Version...

py -3.11 --version >nul 2>&1
if not errorlevel 1 (
    set "PYTHON_CMD=py -3.11"
    echo   [✓] Found Python 3.11 (via Launcher)
    goto :FoundPython
)

for /f "tokens=2 delims= " %%v in ('python --version 2^>nul') do set CUR_VER=%%v
if "!CUR_VER:~0,4!"=="3.11" (
    set "PYTHON_CMD=python"
    echo   [✓] Default Python is 3.11
    goto :FoundPython
)

if "!CUR_VER:~0,4!"=="3.10" set "PYTHON_CMD=python" & goto :FoundPython
if "!CUR_VER:~0,4!"=="3.12" set "PYTHON_CMD=python" & goto :FoundPython

color 0C
echo.
echo   [X] CRITICAL ERROR: Python 3.11 not found!
echo.
pause
exit /b 1

:FoundPython
echo.

:: ===================== STEP 2 =====================
echo   [2/6] Configuring Environment...

if exist venv (
    echo   [i] Removing old environment to prevent conflicts...
    rmdir /s /q venv
)

echo   [+] Creating new environment using Python 3.11...
%PYTHON_CMD% -m venv venv

if errorlevel 1 (
    color 0C
    echo   [X] Failed to create environment.
    pause
    exit /b 1
)
echo   [✓] Environment created.
echo.

:: ===================== STEP 3 =====================
echo   [3/6] Installing Libraries...
call venv\Scripts\activate
python -m pip install --upgrade pip --quiet
pip install -r requirements.txt

if errorlevel 1 (
    color 0C
    echo   [X] Install Failed. Check internet.
    pause
    exit /b 1
)
echo   [✓] Libraries installed.
echo.

:: ===================== STEP 4 =====================
echo   [4/6] Checking AI Brain...
ollama list | findstr /i "qwen2.5-coder:7b" >nul
if errorlevel 1 (
    echo   [!] Downloading Model (This might take time)...
    ollama pull qwen2.5-coder:7b
) else (
    echo   [✓] AI Model ready.
)
echo.

:: ===================== STEP 5 =====================
echo   [5/6] Creating Silent Launcher...

if not exist .env (
    (
        echo TELEGRAM_TOKEN=PASTE_TOKEN_HERE
        echo MODEL_NAME=qwen2.5-coder:7b
    ) > .env
    echo   [!] Created .env file. PLEASE ADD YOUR TOKEN!
)

:: Create the VBS launcher script
(
    echo Set WshShell = CreateObject^("WScript.Shell"^)
    echo WshShell.Run chr^(34^) ^& "%~dp0start_pikachu.bat" ^& chr^(34^), 0
    echo Set WshShell = Nothing
) > run_silent.vbs

echo   [✓] Silent launcher created.
echo.

:: ===================== STEP 6 - AUTO-START SETUP =====================
echo   [6/6] Configuring Windows Auto-Start...

:: Get the Windows Startup folder path
set "STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"

:: Remove old startup entries if they exist
if exist "%STARTUP_FOLDER%\PikachuAgent.lnk" (
    echo   [i] Removing old startup shortcut...
    del "%STARTUP_FOLDER%\PikachuAgent.lnk" >nul 2>&1
)

if exist "%STARTUP_FOLDER%\Pikachu.lnk" (
    del "%STARTUP_FOLDER%\Pikachu.lnk" >nul 2>&1
)

if exist "%STARTUP_FOLDER%\run_silent.vbs" (
    del "%STARTUP_FOLDER%\run_silent.vbs" >nul 2>&1
)

:: Create a VBS script to generate the shortcut
echo   [+] Creating startup shortcut...

:: This VBS script will create a proper Windows shortcut
(
    echo Set WshShell = WScript.CreateObject^("WScript.Shell"^)
    echo Set oShellLink = WshShell.CreateShortcut^("%STARTUP_FOLDER%\PikachuAssistant.lnk"^)
    echo oShellLink.TargetPath = "%~dp0run_silent.vbs"
    echo oShellLink.WorkingDirectory = "%~dp0"
    echo oShellLink.Description = "Pikachu Desktop Assistant - Auto Start"
    echo oShellLink.IconLocation = "shell32.dll,137"
    echo oShellLink.Save
) > create_startup_shortcut.vbs

:: Execute the VBS script to create the shortcut
cscript //nologo create_startup_shortcut.vbs

:: Clean up the temporary VBS script
del create_startup_shortcut.vbs

:: Verify the shortcut was created
if exist "%STARTUP_FOLDER%\PikachuAssistant.lnk" (
    echo   [✓] Auto-start configured successfully!
    echo   [✓] Pikachu will now start automatically on Windows boot/restart.
) else (
    color 0C
    echo   [!] Warning: Auto-start shortcut creation failed.
    echo   [!] You may need to manually copy run_silent.vbs to the Startup folder.
    echo.
    echo   Startup folder location:
    echo   %STARTUP_FOLDER%
)

echo.
echo   ══════════════════════════════════════════════════════════════════════
echo                   ✅  SETUP COMPLETE — PIKACHU IS READY
echo   ══════════════════════════════════════════════════════════════════════
echo.
echo   🎯 IMPORTANT NEXT STEPS:
echo   ───────────────────────────────────────────────────────────────────────
echo   1. Open the .env file and add your TELEGRAM_TOKEN
echo   2. The assistant will now start automatically on every boot/restart
echo   3. To start manually now, run: run_silent.vbs
echo   4. To disable auto-start, delete: 
echo      "%STARTUP_FOLDER%\PikachuAssistant.lnk"
echo   ══════════════════════════════════════════════════════════════════════
echo.
pause