@echo off
chcp 936 >nul
title 学创杯 + 财务工具箱 - 启动菜单

echo ============================================================
echo 学创杯 + 财务工具箱 - 启动菜单
echo ============================================================
echo.
echo 请选择要启动的软件:
echo.
echo 1. 启动 学创杯辅助软件 v2.2
echo 2. 启动 财务工具箱 v1.5
echo 3. 同时启动两个软件
echo 4. 退出
echo.
echo ============================================================
echo.

set /p choice=请输入选项 (1-4): 

if "%choice%"=="1" (
    echo 正在启动 学创杯辅助软件...
    start "" "学创杯辅助软件.exe"
    goto :end
)
if "%choice%"=="2" (
    echo 正在启动 财务工具箱...
    start "" "财务工具箱.exe"
    goto :end
)
if "%choice%"=="3" (
    echo 正在同时启动两个软件...
    start "" "学创杯辅助软件.exe"
    start "" "财务工具箱.exe"
    goto :end
)
if "%choice%"=="4" (
    exit /b
)

echo 无效的选项，请重新运行
goto :end

:end
echo.
echo 软件已启动，浏览器将自动打开
echo 学创杯辅助软件：http://localhost:8502
echo 财务工具箱：http://localhost:8501
echo.
pause
