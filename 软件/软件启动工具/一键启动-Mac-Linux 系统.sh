#!/bin/bash
# 一键启动脚本 - 学创杯 + 财务工具箱
# 适用：macOS / Linux
# 功能：自动检测环境 + 一键安装 Streamlit+ 依赖 + 启动应用

echo "============================================================"
echo "🚀 一键启动工具 - 学创杯 + 财务工具箱"
echo "============================================================"
echo ""

# ========== 环境检测 ==========
echo "🔍 检测运行环境..."
echo ""

# 检测 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未检测到 Python3"
    echo ""
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "📥 macOS 用户安装命令:"
        echo "   brew install python3"
    else
        echo "📥 Linux 用户安装命令:"
        echo "   sudo apt install python3 python3-pip"
    fi
    echo ""
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "✅ $PYTHON_VERSION"
echo ""

# 检测 pip
if ! command -v pip3 &> /dev/null; then
    echo "⚠️ 未检测到 pip3，尝试安装..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sudo easy_install pip 2>/dev/null || echo "需要手动安装 pip"
    else
        sudo apt-get install -y python3-pip 2>/dev/null || echo "需要手动安装 pip"
    fi
fi

PIPV_VERSION=$(pip3 --version 2>/dev/null | head -1)
echo "✅ pip3 已安装：$PIPV_VERSION"
echo ""

# ========== 一键安装 Streamlit + 依赖 ==========
echo "📦 检查并安装 Streamlit 及依赖..."
echo ""

echo "[1/3] 检查 Streamlit..."
if ! pip3 show streamlit &> /dev/null; then
    echo "⏳ Streamlit 未安装，正在安装..."
    pip3 install streamlit --quiet
    if [ $? -eq 0 ]; then
        echo "✅ Streamlit 安装成功"
    else
        echo "❌ Streamlit 安装失败"
        echo ""
        echo "💡 请手动安装：pip3 install streamlit"
        exit 1
    fi
else
    echo "✅ Streamlit 已安装"
fi
echo ""

echo "[2/3] 安装 学创杯辅助软件 依赖..."
cd "$(dirname "$0")/../学创杯辅助软件/xcbs_assistant" || exit 1
if [ -f "requirements.txt" ]; then
    pip3 install -r requirements.txt --quiet
    if [ $? -eq 0 ]; then
        echo "✅ 学创杯依赖已就绪"
    else
        echo "⚠️ 学创杯依赖安装失败，将尝试运行时修复"
    fi
fi
echo ""

echo "[3/3] 安装 财务工具箱 依赖..."
cd "$(dirname "$0")/../财务工具箱" || exit 1
if [ -f "requirements.txt" ]; then
    pip3 install -r requirements.txt --quiet
    if [ $? -eq 0 ]; then
        echo "✅ 财务工具箱依赖已就绪"
    else
        echo "⚠️ 财务工具箱依赖安装失败，将尝试运行时修复"
    fi
fi
echo ""

echo "============================================================"
echo "✅ 环境准备完成"
echo "============================================================"
echo ""

# ========== 显示菜单 ==========
echo "🎯 请选择要启动的软件"
echo ""
echo "  1) 🏆 学创杯辅助工具 v2.2 (14 个功能模块)"
echo "  2) 💰 财务工具箱 v1.5 (15 个功能模块)"
echo "  3) 📊 同时启动两个软件"
echo "  4) 🔄 重新安装 Streamlit + 所有依赖"
echo "  5) ❌ 退出"
echo ""

read -p "请输入选项 (1-5): " choice

case $choice in
    1)
        echo ""
        echo "============================================================"
        echo "🏆 启动 学创杯辅助工具 v2.2"
        echo "============================================================"
        
        cd "$(dirname "$0")/../学创杯辅助软件/xcbs_assistant" || exit 1
        
        echo "📦 验证依赖..."
        pip3 install -r requirements.txt --quiet 2>/dev/null
        
        echo "🚀 启动中..."
        echo ""
        echo "✅ 访问地址：http://localhost:8502"
        echo "📱 按 Ctrl+C 停止服务"
        echo ""
        
        # 打开浏览器
        if command -v xdg-open &> /dev/null; then
            xdg-open http://localhost:8502 &>/dev/null &
        elif command -v open &> /dev/null; then
            open http://localhost:8502 &>/dev/null &
        fi
        
        streamlit run app.py --server.port 8502 --server.headless true
        ;;
    
    2)
        echo ""
        echo "============================================================"
        echo "💰 启动 财务工具箱 v1.5"
        echo "============================================================"
        
        cd "$(dirname "$0")/../财务工具箱" || exit 1
        
        echo "📦 验证依赖..."
        pip3 install -r requirements.txt --quiet 2>/dev/null
        
        echo "🚀 启动中..."
        echo ""
        echo "✅ 访问地址：http://localhost:8501"
        echo "👤 登录账号：admin"
        echo "🔑 登录密码：703102"
        echo "📱 按 Ctrl+C 停止服务"
        echo ""
        
        # 打开浏览器
        if command -v xdg-open &> /dev/null; then
            xdg-open http://localhost:8501 &>/dev/null &
        elif command -v open &> /dev/null; then
            open http://localhost:8501 &>/dev/null &
        fi
        
        streamlit run app.py --server.port 8501 --server.headless true
        ;;
    
    3)
        echo ""
        echo "============================================================"
        echo "📊 同时启动两个软件"
        echo "============================================================"
        echo ""
        
        # 启动学创杯
        (
            cd "$(dirname "$0")/../学创杯辅助软件/xcbs_assistant" || exit 1
            pip3 install -r requirements.txt --quiet 2>/dev/null
            streamlit run app.py --server.port 8502 --server.headless true > /dev/null 2>&1
        ) &
        
        # 启动财务工具箱
        (
            cd "$(dirname "$0")/../财务工具箱" || exit 1
            pip3 install -r requirements.txt --quiet 2>/dev/null
            streamlit run app.py --server.port 8501 --server.headless true > /dev/null 2>&1
        ) &
        
        sleep 3
        
        echo "✅ 两个服务已启动"
        echo ""
        echo "🏆 学创杯辅助工具：http://localhost:8502"
        echo "💰 财务工具箱：http://localhost:8501 (admin / 703102)"
        echo ""
        
        # 打开浏览器
        if command -v xdg-open &> /dev/null; then
            xdg-open http://localhost:8502 &>/dev/null &
            xdg-open http://localhost:8501 &>/dev/null &
        elif command -v open &> /dev/null; then
            open http://localhost:8502 &>/dev/null &
            open http://localhost:8501 &>/dev/null &
        fi
        
        echo "按任意键停止所有服务"
        read -p ""
        
        echo "正在停止服务..."
        pkill -f "streamlit run app.py" 2>/dev/null
        
        echo "✅ 所有服务已停止"
        ;;
    
    4)
        echo ""
        echo "============================================================"
        echo "🔄 重新安装 Streamlit + 所有依赖"
        echo "============================================================"
        echo ""
        
        echo "[1/3] 重新安装 Streamlit..."
        pip3 uninstall streamlit -y --quiet 2>/dev/null
        pip3 install streamlit --quiet
        echo "✅ Streamlit 已重装"
        echo ""
        
        echo "[2/3] 安装 学创杯辅助软件 依赖..."
        cd "$(dirname "$0")/../学创杯辅助软件/xcbs_assistant" || exit 1
        pip3 install -r requirements.txt --force-reinstall --quiet
        echo "✅ 学创杯依赖已重装"
        echo ""
        
        echo "[3/3] 安装 财务工具箱 依赖..."
        cd "$(dirname "$0")/../财务工具箱" || exit 1
        pip3 install -r requirements.txt --force-reinstall --quiet
        echo "✅ 财务工具箱依赖已重装"
        echo ""
        
        echo "✅ 所有依赖重新安装完成"
        echo ""
        read -p "按回车键返回菜单..."
        ;;
    
    5)
        echo "👋 再见!"
        exit 0
        ;;
    
    *)
        echo "❌ 无效选项"
        exit 1
        ;;
esac
