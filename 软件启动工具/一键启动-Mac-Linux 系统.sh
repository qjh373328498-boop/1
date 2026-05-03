#!/bin/bash
# 一键启动脚本 - 学创杯 + 财务工具箱
# 适用系统：macOS / Linux (Ubuntu, Debian, CentOS, etc.)

echo "============================================================"
echo "🚀 一键启动工具 - 学创杯辅助软件 + 财务工具箱"
echo "============================================================"
echo ""
echo "💻 适用系统：macOS / Linux"
echo ""

# 检测 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误：未检测到 Python3，请先安装 Python 3.8+"
    echo "   macOS: brew install python3"
    echo "   Ubuntu/Debian: sudo apt install python3 python3-pip"
    exit 1
fi

echo "✅ Python 版本：$(python3 --version)"
echo ""

# 检测 pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ 错误：未检测到 pip3"
    exit 1
fi

echo "✅ pip3 版本：$(pip3 --version)"
echo ""

# 选择要启动的软件
echo "请选择要启动的软件："
echo ""
echo "  1) 🏆 学创杯辅助工具 v2.2 (端口 8502)"
echo "  2) 💰 财务工具箱 v1.5 (端口 8501)"
echo "  3) 📊 同时启动两个软件"
echo "  4) ❌ 退出"
echo ""

read -p "请输入选项 (1-4): " choice

case $choice in
    1)
        echo ""
        echo "============================================================"
        echo "🏆 启动 学创杯辅助工具 v2.2"
        echo "============================================================"
        echo ""
        
        cd "$(dirname "$0")/../比赛/学创杯/软件/xcbs_assistant" || exit 1
        
        echo "📦 检查依赖..."
        pip3 install -r requirements.txt --quiet
        
        echo "🚀 启动应用..."
        echo ""
        echo "访问地址：http://localhost:8502"
        echo "按 Ctrl+C 停止服务"
        echo ""
        
        # 尝试打开浏览器
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
        echo ""
        
        cd "$(dirname "$0")/../软件开发/财务工具箱" || exit 1
        
        echo "📦 检查依赖..."
        pip3 install -r requirements.txt --quiet
        
        echo "🚀 启动应用..."
        echo ""
        echo "访问地址：http://localhost:8501"
        echo "登录账号：admin"
        echo "登录密码：703102"
        echo "按 Ctrl+C 停止服务"
        echo ""
        
        # 尝试打开浏览器
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
        
        # 启动学创杯（后台）
        (
            cd "$(dirname "$0")/../比赛/学创杯/软件/xcbs_assistant" || exit 1
            pip3 install -r requirements.txt --quiet
            streamlit run app.py --server.port 8502 --server.headless true > /dev/null 2>&1
        ) &
        XCBS_PID=$!
        
        # 启动财务工具箱（后台）
        (
            cd "$(dirname "$0")/../软件开发/财务工具箱" || exit 1
            pip3 install -r requirements.txt --quiet
            streamlit run app.py --server.port 8501 --server.headless true > /dev/null 2>&1
        ) &
        FINANCE_PID=$!
        
        echo "✅ 两个服务已启动"
        echo ""
        echo "🏆 学创杯辅助工具：http://localhost:8502"
        echo "💰 财务工具箱：http://localhost:8501 (admin / 703102)"
        echo ""
        
        # 尝试打开浏览器
        if command -v xdg-open &> /dev/null; then
            xdg-open http://localhost:8502 &>/dev/null &
            xdg-open http://localhost:8501 &>/dev/null &
        elif command -v open &> /dev/null; then
            open http://localhost:8502 &>/dev/null &
            open http://localhost:8501 &>/dev/null &
        fi
        
        echo "按任意键停止所有服务"
        read -p ""
        
        # 停止服务
        echo "正在停止服务..."
        kill $XCBS_PID 2>/dev/null
        kill $FINANCE_PID 2>/dev/null
        pkill -f "streamlit run app.py" 2>/dev/null
        
        echo "✅ 所有服务已停止"
        ;;
    
    4)
        echo "👋 再见!"
        exit 0
        ;;
    
    *)
        echo "❌ 无效选项"
        exit 1
        ;;
esac
