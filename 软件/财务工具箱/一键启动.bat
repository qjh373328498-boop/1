@echo off
chcp 65001 >nul
title 财务工具箱

cd /d "%~dp0"

echo ============================================
echo            财务工具箱 - 启动器
echo ============================================
echo.

REM 检查虚拟环境是否完整
if exist "venv\Scripts\python.exe" (
    echo [检测] 虚拟环境已存在
) else (
    echo [1/3] 正在创建虚拟环境...
    if exist "venv" rmdir /s /q venv
    python -m venv venv
    if errorlevel 1 (
        echo 错误：创建虚拟环境失败!
        echo 请确保已安装 Python 3.8+
        pause
        exit /b 1
    )
    echo 虚拟环境创建成功!
)

REM 激活虚拟环境
echo [2/3] 正在激活虚拟环境...
call venv\Scripts\activate.bat

REM 安装依赖
echo [3/3] 正在安装依赖包 (首次启动可能需要 2-3 分钟)...
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

echo.
echo ============================================
echo  启动成功！浏览器将自动打开
echo  如果未自动打开，请访问：http://localhost:8501
echo ============================================
echo.

REM 启动 Streamlit
python -m streamlit run app.py

pause
