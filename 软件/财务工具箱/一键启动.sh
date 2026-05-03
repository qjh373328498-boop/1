#!/bin/bash
# 财务工具箱 - Mac/Linux 启动脚本

echo "============================================"
echo "           财务工具箱 - 启动器"
echo "============================================"
echo ""

# 检查虚拟环境是否存在
if [ ! -d "venv" ]; then
    echo "[1/2] 正在创建虚拟环境..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo ""
        echo "错误：创建虚拟环境失败!"
        echo "请确保已安装 Python 3.8+"
        exit 1
    fi
fi

# 激活虚拟环境
echo "[1/2] 正在激活虚拟环境..."
source venv/bin/activate

# 检查依赖是否已安装
echo "[2/2] 检查依赖..."
python -c "import streamlit" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "正在安装依赖包 (首次启动可能需要几分钟)..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo ""
        echo "错误：安装依赖失败!"
        exit 1
    fi
fi

echo ""
echo "============================================"
echo "  启动成功！浏览器将自动打开"
echo "  如果未自动打开，请访问：http://localhost:8501"
echo "============================================"
echo ""

# 启动 Streamlit 应用
python -m streamlit run app.py
