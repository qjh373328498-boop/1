@echo off
chcp 936 >nul
title 一键启动 - 学创杯 + 财务工具箱

echo ============================================================
echo 一键启动工具 - 学创杯 + 财务工具箱
echo ============================================================
echo.

REM ========== 环境检测 ==========
echo 检测运行环境...
echo.

REM 检测 Python
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Python
    echo.
    echo Python 下载地址：https://www.python.org/downloads/
    echo.
    echo 或使用 winget 安装:
    echo    winget install Python.Python.3.11
    echo.
    pause
    exit /b 1
)

echo [成功] Python 已安装：
python --version
echo.

REM 检测 pip
where pip >nul 2>&1
if %errorlevel% neq 0 (
    echo [警告] 未检测到 pip，尝试修复...
    python -m ensurepip --default-pip 2>nul
    if %errorlevel% neq 0 (
        echo [错误] pip 修复失败，请重新安装 Python
        pause
        exit /b 1
    )
)

echo [成功] pip 已安装
echo.

REM ========== 一键安装 Streamlit + 依赖 ==========
echo 检查并安装 Streamlit 及依赖...
echo.

echo [1/3] 检查 Streamlit...
pip show streamlit >nul 2>&1
if %errorlevel% neq 0 (
    echo Streamlit 未安装，正在安装...
    pip install streamlit --quiet
    if %errorlevel% equ 0 (
        echo [成功] Streamlit 安装成功
    ) else (
        echo [错误] Streamlit 安装失败
        echo.
        echo 请手动安装：pip install streamlit
        pause
        exit /b 1
    )
) else (
    echo [成功] Streamlit 已安装
)
echo.

echo [2/3] 安装 学创杯辅助软件 依赖...
cd /d "%~dp0..\学创杯辅助软件\xcbs_assistant"
if exist "requirements.txt" (
    pip install -r requirements.txt --quiet
    if %errorlevel% equ 0 (
        echo [成功] 学创杯依赖已就绪
    ) else (
        echo [警告] 学创杯依赖安装失败，将尝试运行时修复
    )
)
echo.

echo [3/3] 安装 财务工具箱 依赖...
cd /d "%~dp0..\财务工具箱"
if exist "requirements.txt" (
    pip install -r requirements.txt --quiet
    if %errorlevel% equ 0 (
        echo [成功] 财务工具箱依赖已就绪
    ) else (
        echo [警告] 财务工具箱依赖安装失败，将尝试运行时修复
    )
)
echo.

echo ============================================================
echo 环境准备完成
echo ============================================================
echo.

REM ========== 显示菜单 ==========
echo 请选择要启动的软件:
echo.
echo 1. 启动 学创杯辅助软件
echo 2. 启动 财务工具箱
echo 3. 同时启动两个软件
echo 4. 重新安装 Streamlit + 所有依赖
echo 5. 退出
echo.
echo ============================================================
echo.

set /p choice=请输入选项 (1-5): 

if "%choice%"=="1" goto :start_xcbs
if "%choice%"=="2" goto :start_finance
if "%choice%"=="3" goto :start_both
if "%choice%"=="4" goto :reinstall
if "%choice%"=="5" exit /b

echo 无效的选项
pause
exit /b

:start_xcbs
echo.
echo 正在启动 学创杯辅助软件...
echo 访问地址：http://localhost:8502
echo.
cd /d "%~dp0..\学创杯辅助软件\xcbs_assistant"
start "学创杯辅助软件" cmd /k "streamlit run app.py --server.port=8502"
goto :end

:start_finance
echo.
echo 正在启动 财务工具箱...
echo 访问地址：http://localhost:8501 (密码：703102)
echo.
cd /d "%~dp0..\财务工具箱"
start "财务工具箱" cmd /k "streamlit run app.py --server.port=8501"
goto :end

:start_both
echo.
echo 正在同时启动两个软件...
echo.
cd /d "%~dp0..\学创杯辅助软件\xcbs_assistant"
start "学创杯辅助软件" cmd /k "streamlit run app.py --server.port=8502"
cd /d "%~dp0..\财务工具箱"
start "财务工具箱" cmd /k "streamlit run app.py --server.port=8501"
goto :end

:reinstall
echo.
echo 正在重新安装依赖...
echo.
pip install --upgrade streamlit
pip install -r "%~dp0..\学创杯辅助软件\xcbs_assistant\requirements.txt"
pip install -r "%~dp0..\财务工具箱\requirements.txt"
echo.
echo 依赖安装完成！
echo.
pause
goto :main

:main
goto :start

:end
echo.
echo 软件已启动，浏览器将自动打开
echo.
echo 学创杯辅助软件：http://localhost:8502
echo 财务工具箱：http://localhost:8501 (密码：703102)
echo.
echo 按任意键关闭此窗口，软件将继续运行
pause >nul
