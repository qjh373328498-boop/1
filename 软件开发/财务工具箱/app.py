"""
财务工具箱 v1.3.0
企业财务会计辅助工具 - 主入口
"""
import streamlit as st
import sqlite3
from datetime import datetime
from utils.database import init_db, check_user, get_user_role, get_dashboard_stats
from utils.formatters import format_currency

st.set_page_config(
    page_title="财务工具箱",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

init_db()

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'role' not in st.session_state:
    st.session_state.role = 'guest'


def login():
    st.title("🔐 用户登录")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        username = st.text_input("用户名", key="login_username")
        password = st.text_input("密码", type="password", key="login_password")
        
        if st.button("登录", type="primary", use_container_width=True):
            if check_user(username, password):
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.role = get_user_role(username)
                st.rerun()
            else:
                st.error("用户名或密码错误")
    
    with col2:
        st.info("💡 默认管理员账户\n\n用户名：admin\n\n密码：admin123")


def logout():
    if st.button("🔓 退出登录", key="logout_btn"):
        st.session_state.authenticated = False
        st.session_state.username = None
        st.session_state.role = 'guest'
        st.rerun()


def show_dashboard():
    st.title("📊 财务工具箱仪表盘")
    st.write(f"欢迎回来，**{st.session_state.username}**！")
    
    # 获取真实统计数据
    stats = get_dashboard_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("发票总数", f"{stats['invoice_count']} 张")
    
    with col2:
        st.metric("发票总额", format_currency(stats['invoice_total']))
    
    with col3:
        st.metric("应收账款", format_currency(stats['ar_total']))
    
    with col4:
        st.metric("应付账款", format_currency(stats['ap_total']))
    
    st.subheader("📈 近期财务指标趋势")
    
    import plotly.graph_objects as go
    from utils.database import get_connection
    import pandas as pd
    
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT period, metric_name, value 
        FROM financial_metrics 
        WHERE metric_name IN ('营业收入', '经营现金流')
        ORDER BY period
    """, conn)
    conn.close()
    
    if not df.empty:
        df_pivot = df.pivot(index='period', columns='metric_name', values='value')
        
        fig = go.Figure()
        if '营业收入' in df_pivot.columns:
            fig.add_trace(go.Scatter(x=df_pivot.index, y=df_pivot['营业收入'], name='营业收入', line=dict(width=3)))
        if '经营现金流' in df_pivot.columns:
            fig.add_trace(go.Scatter(x=df_pivot.index, y=df_pivot['经营现金流'], name='经营现金流', line=dict(width=3)))
        
        fig.update_layout(
            height=400,
            showlegend=True,
            hovermode='x unified',
            xaxis_title="期间",
            yaxis_title="金额 (元)"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("暂无财务指标数据")
    
    st.subheader("📅 即将到期事件")
    
    conn = get_connection()
    from datetime import datetime, timedelta
    today = datetime.now().strftime('%Y-%m-%d')
    end_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
    
    events = pd.read_sql_query("""
        SELECT title, event_date, event_type, description
        FROM calendar_event
        WHERE event_date BETWEEN ? AND ?
        ORDER BY event_date
    """, conn, params=[today, end_date])
    conn.close()
    
    if not events.empty:
        for _, event in events.iterrows():
            event_date = datetime.strptime(event['event_date'], '%Y-%m-%d')
            days_left = (event_date - datetime.now()).days
            
            if days_left == 0:
                status = "🔴 今天"
            elif days_left <= 3:
                status = "🟠 即将到期"
            elif days_left <= 7:
                status = "🟡 本周内"
            else:
                status = "🟢"
            
            st.write(f"{status} **{event['title']}** ({event['event_type']}) - {event['event_date']}")
    else:
        st.success("未来 30 天内没有待办事件")
    
    st.subheader("🔧 可用工具")
    
    tools = [
        ("📄 发票管家", "发票录入、查询、认证管理"),
        ("🏦 银行对账", "自动匹配银行流水与企业账务"),
        ("📈 本量利分析", "盈亏平衡分析、敏感性分析"),
        ("💰 资金诊断", "资金使用效率分析与优化建议"),
        ("📊 预算分析", "预算执行差异分析"),
        ("📅 财务日历", "重要日期提醒与管理"),
        ("🎯 智能透视分析", "多维度数据透视分析"),
        ("📊 财务比率分析", "偿债、盈利、营运能力分析"),
        ("📝 凭证录入", "会计凭证录入与管理"),
        ("📊 科目余额表", "科目汇总与余额查询"),
        ("💳 应收应付管理", "往来款项管理"),
        ("🧾 纳税申报", "税费计算与申报"),
        ("🚀 增强功能", "数据导出/导入、备份恢复"),
        ("📈 高级业务分析", "经营决策支持、趋势预测"),
        ("❓ 帮助中心", "使用指南与常见问题"),
    ]
    
    cols = st.columns(3)
    for i, (name, desc) in enumerate(tools):
        with cols[i % 3]:
            st.markdown(f"**{name}**")
            st.caption(desc)
    
    st.divider()
    st.caption(f"财务工具箱 v1.5.0 | 当前用户：{st.session_state.username} | 角色：{st.session_state.role}")


def main():
    st.sidebar.title("财务工具箱")
    
    if st.session_state.authenticated:
        st.sidebar.success(f"👤 {st.session_state.username}")
        logout()
        st.sidebar.divider()
        
        page = st.sidebar.radio(
            "选择工具",
            [
                "📊 仪表盘",
                "📄 发票管家",
                "🏦 银行对账",
                "📈 本量利分析",
                "💰 资金诊断",
                "📊 预算分析",
                "📅 财务日历",
                "🎯 智能透视分析",
                "📊 财务比率分析",
                "📝 凭证录入",
                "📊 科目余额表",
                "💳 应收应付管理",
                "🧾 纳税申报",
                "🚀 增强功能",
                "📈 高级业务分析",
                "❓ 帮助中心",
            ],
            index=0
        )
        
        pages = {
            "📊 仪表盘": show_dashboard,
            "📄 发票管家": lambda: st.switch_page("pages/01_发票管家.py"),
            "🏦 银行对账": lambda: st.switch_page("pages/02_银行对账.py"),
            "📈 本量利分析": lambda: st.switch_page("pages/03_本量利分析.py"),
            "💰 资金诊断": lambda: st.switch_page("pages/04_资金诊断.py"),
            "📊 预算分析": lambda: st.switch_page("pages/05_预算分析.py"),
            "📅 财务日历": lambda: st.switch_page("pages/06_财务日历.py"),
            "🎯 智能透视分析": lambda: st.switch_page("pages/07_智能透视分析.py"),
            "📊 财务比率分析": lambda: st.switch_page("pages/08_财务比率分析.py"),
            "📝 凭证录入": lambda: st.switch_page("pages/09_凭证录入.py"),
            "📊 科目余额表": lambda: st.switch_page("pages/10_科目余额表.py"),
            "💳 应收应付管理": lambda: st.switch_page("pages/11_应收应付管理.py"),
            "🧾 纳税申报": lambda: st.switch_page("pages/12_纳税申报.py"),
            "🚀 增强功能": lambda: st.switch_page("pages/13_增强功能.py"),
            "📈 高级业务分析": lambda: st.switch_page("pages/14_高级业务分析.py"),
            "❓ 帮助中心": lambda: st.switch_page("pages/99_帮助中心.py"),
        }
        
        if page in pages:
            pages[page]()
    
    else:
        login()


if __name__ == "__main__":
    main()
