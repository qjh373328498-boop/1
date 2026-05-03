@echo off
chcp 936 >nul
title 学创杯 + 财务工具箱 - 自动打包工具

echo ============================================================
echo 学创杯 + 财务工具箱 - Windows EXE 打包工具
echo ============================================================
echo.
echo 本工具将自动完成以下操作:
echo   1. 检查 Python 环境
echo   2. 安装 PyInstaller 和依赖
echo   3. 打包学创杯辅助软件为 .exe
echo   4. 打包财务工具箱为 .exe
echo   5. 创建启动菜单
echo.
echo 预计耗时：5-10 分钟
echo ============================================================
echo.

pause

echo [1/6] 检查 Python 环境...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo 未检测到 Python，请先安装 Python 3.8+
    echo 下载地址：https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

python --version
echo Python 检查通过
echo.

echo [2/6] 安装 PyInstaller...
pip install pyinstaller -q
if %errorlevel% neq 0 (
    echo PyInstaller 安装失败
    pause
    exit /b 1
)
echo PyInstaller 安装完成
echo.

echo [3/6] 安装 Streamlit 和依赖...
pip install streamlit pandas plotly -q
echo 依赖安装完成
echo.

echo [4/6] 打包 学创杯辅助软件...
echo.

cd /d "%~dp0\学创杯辅助软件"
if not exist "xcbs_assistant\app.py" (
    echo 未找到学创杯辅助软件源码
    pause
    exit /b 1
)

if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "*.spec" del /q "*.spec"

echo 正在打包...
pyinstaller --name "学创杯辅助软件" ^
            --windowed ^
            --onefile ^
            --add-data "pages;pages" ^
            --hidden-import streamlit ^
            --hidden-import pandas ^
            --hidden-import plotly ^
            --hidden-import xlsxwriter ^
            xcbs_assistant\app.py

if %errorlevel% neq 0 (
    echo 学创杯打包失败
    pause
    exit /b 1
)

echo 学创杯辅助软件 打包完成
echo.
cd /d "%~dp0"

echo [5/6] 打包 财务工具箱...
echo.

cd /d "%~dp0\财务工具箱"
if not exist "app.py" (
    echo 未找到财务工具箱源码
    pause
    exit /b 1
)

if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "*.spec" del /q "*.spec"

echo 正在打包...
pyinstaller --name "财务工具箱" ^
            --windowed ^
            --onefile ^
            --add-data "pages;pages" ^
            --hidden-import streamlit ^
            --hidden-import pandas ^
            --hidden-import plotly ^
            --hidden-import openpyxl ^
            app.py

if %errorlevel% neq 0 (
    echo 财务工具箱打包失败
    pause
    exit /b 1
)

echo 财务工具箱 打包完成
echo.
cd /d "%~dp0"

echo [6/6] 创建启动菜单...
copy /y "%~dp0\软件启动工具\一键启动-Windows 系统.bat" "启动菜单.bat" >nul
echo 启动菜单已创建
echo.

echo ============================================================
echo 打包完成！
echo ============================================================
echo.
echo 生成文件:
echo   - 学创杯辅助软件\dist\学创杯辅助软件.exe
echo   - 财务工具箱\dist\财务工具箱.exe
echo   - 启动菜单.bat
echo.
echo 下一步操作:
echo   1. 测试：双击"启动菜单.bat"
echo   2. 分发：将 exe 文件和启动菜单复制到一起
echo   3. 压缩：打包成 zip 分发给用户
echo.
echo ============================================================
echo.

pause
