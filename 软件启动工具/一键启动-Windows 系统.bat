@echo off
chcp 65001 >nul
title 一键启动工具 - 学创杯 + 财务工具箱

echo ============================================================
echo 🚀 一键启动工具 - 学创杯辅助软件 + 财务工具箱
echo ============================================================
echo.
echo 💻 适用系统：Windows 10 / 11
echo.

REM 检测 Python
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 错误：未检测到 Python，请先安装 Python 3.8+
    echo    下载地址：https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python 版本:
python --version
echo.

REM 检测 pip
where pip >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 错误：未检测到 pip
    pause
    exit /b 1
)

echo ✅ pip 版本:
pip --version
echo.

echo 请选择要启动的软件:
echo.
echo   1^) 🏆 学创杯辅助工具 v2.2 (端口 8502)
echo   2^) 💰 财务工具箱 v1.5 (端口 8501)
echo   3^) 📊 同时启动两个软件
echo   4^) ❌ 退出
echo.

set /p choice=请输入选项 (1-4^): 

if "%choice%"=="1" goto start_xcbs
if "%choice%"=="2" goto start_finance
if "%choice%"=="3" goto start_both
if "%choice%"=="4" goto exit_program

echo ❌ 无效选项
pause
exit /b 1

:start_xcbs
echo.
echo ============================================================
echo 🏆 启动 学创杯辅助工具 v2.2
echo ============================================================
echo.

cd /d "%~dp0..\比赛\学创杯\软件\xcbs_assistant"

echo 📦 检查依赖...
pip install -r requirements.txt --quiet

echo 🚀 启动应用...
echo.
echo 访问地址：http://localhost:8502
echo 按 Ctrl+C 停止服务
echo.

start http://localhost:8502
streamlit run app.py --server.port 8502 --server.headless true
goto end

:start_finance
echo.
echo ============================================================
echo 💰 启动 财务工具箱 v1.5
echo ============================================================
echo.

cd /d "%~dp0..\软件开发\财务工具箱"

echo 📦 检查依赖...
pip install -r requirements.txt --quiet

echo 🚀 启动应用...
echo.
echo 访问地址：http://localhost:8501
echo 登录账号：admin
echo 登录密码：703102
echo 按 Ctrl+C 停止服务
echo.

start http://localhost:8501
streamlit run app.py --server.port 8501 --server.headless true
goto end

:start_both
echo.
echo ============================================================
echo 📊 同时启动两个软件
echo ============================================================
echo.

REM 启动学创杯（后台）
start /B cmd /c "cd /d %~dp0..\比赛\学创杯\软件\xcbs_assistant && pip install -r requirements.txt --quiet && streamlit run app.py --server.port 8502 --server.headless true"

REM 启动财务工具箱（后台）
start /B cmd /c "cd /d %~dp0..\软件开发\财务工具箱 && pip install -r requirements.txt --quiet && streamlit run app.py --server.port 8501 --server.headless true"

timeout /t 5 >nul

echo ✅ 两个服务已启动
echo.
echo 🏆 学创杯辅助工具：http://localhost:8502
echo 💰 财务工具箱：http://localhost:8501 (admin / 703102)
echo.
pause

echo 正在打开浏览器...
start http://localhost:8502
timeout /t 2 >nul
start http://localhost:8501

echo.
echo 停止服务请按窗口右上角 X 或 Ctrl+C
echo.
goto end

:exit_program
echo 👋 再见!
exit /b

:end
echo.
pause
