@echo off
chcp 936 >nul
title Start Menu

echo ============================================================
echo Start Menu
echo ============================================================
echo.
echo 1. Start XueChuangBei Assistant
echo 2. Start Finance Toolbox
echo 3. Start Both
echo 4. Exit
echo.
echo ============================================================
echo.

set /p choice=Enter choice (1-4):

if "%choice%"=="1" goto xcbs
if "%choice%"=="2" goto finance
if "%choice%"=="3" goto both
if "%choice%"=="4" exit /b

echo Invalid choice
pause
goto end

:xcbs
cd xcbs_assistant
start XCB cmd /k "streamlit run app.py --server.port 8502"
echo Started XueChuangBei
pause
goto end

:finance
cd ..\FinanceToolbox
start FT cmd /k "streamlit run app.py --server.port 8501"
echo Started Finance Toolbox
pause
goto end

:both
cd xcbs_assistant
start XCB cmd /k "streamlit run app.py --server.port 8502"
cd ..\FinanceToolbox
start FT cmd /k "streamlit run app.py --server.port 8501"
echo Both started
pause
goto end

:end
