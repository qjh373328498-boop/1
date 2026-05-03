"""
学创杯比赛辅助工具 - 现金流预测工具
"""
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="现金流预测工具", page_icon="💰", layout="wide")

st.title("💰 现金流预测与预警系统")
st.markdown("**用途**: 预测期末现金余额，避免现金断流 (-10 分) 和紧急借款 (-5 分)")

# 侧边栏
st.sidebar.header("⚠️ 安全提示")
st.sidebar.error("""
**三条死亡红线**:
- 紧急借款：-5 分/次
- 逾期报税：-5 分/次
- 现金断流：-10 分/次

**安全现金余额** ≥ 下季度固定支出 × 1.2
""")

st.sidebar.header("选择季度")
quarter = st.sidebar.selectbox("当前季度", ["Q1", "Q2", "Q3", "Q4"])

# 输入区域
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("期初数据")
    opening_cash = st.number_input("期初现金余额 (万)", min_value=0.0, value=100.0, step=10.0)
    
    st.subheader("现金流入")
    sales_collection = st.number_input("销售回款 (万)", min_value=0.0, value=80.0, step=10.0)
    loan_inflow = st.number_input("融资流入 - 贷款/股权 (万)", min_value=0.0, value=0.0, step=10.0)
    other_inflow = st.number_input("其他现金流入 (万)", min_value=0.0, value=0.0, step=1.0)

with col2:
    st.subheader("经营支出")
    purchase_payment = st.number_input("采购支出 (万)", min_value=0.0, value=30.0, step=5.0)
    payroll = st.number_input("人工费用 (万)", min_value=0.0, value=20.0, step=5.0)
    operating_expense = st.number_input("费用支出 - 管理 + 销售 (万)", min_value=0.0, value=15.0, step=2.0)
    ad_expense = st.number_input("广告投放 (万)", min_value=0.0, value=10.0, step=1.0)

with col3:
    st.subheader("投融资支出")
    loan_repayment = st.number_input("归还贷款本金 (万)", min_value=0.0, value=0.0, step=10.0)
    interest_payment = st.number_input("支付利息 (万)", min_value=0.0, value=0.0, step=1.0)
    investment = st.number_input("投资支出 - 厂房/设备 (万)", min_value=0.0, value=0.0, step=10.0)
    other_expense = st.number_input("其他支出 (万)", min_value=0.0, value=0.0, step=1.0)

# 计算
total_inflow = sales_collection + loan_inflow + other_inflow
total_outflow = (purchase_payment + payroll + operating_expense + ad_expense + 
                 loan_repayment + interest_payment + investment + other_expense)
net_cash_flow = total_inflow - total_outflow
closing_cash = opening_cash + net_cash_flow

# 现金预警
fixed_expense = operating_expense + payroll  # 固定支出估算
safe_cash_buffer = fixed_expense * 1.2

cash_status = ""
risk_level = ""

if closing_cash < 0:
    cash_status = "🚨 现金断流!"
    risk_level = "danger"
elif closing_cash < safe_cash_buffer:
    cash_status = f"⚠️ 现金不足 (安全线：{safe_cash_buffer:.1f}万)"
    risk_level = "warning"
else:
    cash_status = "✅ 现金充足"
    risk_level = "success"

# 显示结果
st.divider()
st.subheader("📊 现金流预测结果")

col1, col2, col3, col4 = st.columns(4)

col1.metric("期初现金", f"{opening_cash:.1f}万")
col2.metric("现金净流入", f"{net_cash_flow:.1f}万", delta=f"流入{total_inflow:.1f}万")
col3.metric("期末现金", f"{closing_cash:.1f}万", delta=cash_status, 
            delta_color="normal" if closing_cash >= safe_cash_buffer else "inverse")
col4.metric("安全现金线", f"{safe_cash_buffer:.1f}万")

# 风险提示
if risk_level == "danger":
    st.error("""
    🚨 **现金断流预警**：期末现金为负，将面临 -10 分扣分！
    
    **立即采取以下措施**:
    1. 暂停所有投资支出（厂房/设备）
    2. 减少广告投入（砍掉 50% 以上）
    3. 立即申请短期贷款
    4. 折价促销加速回款
    5. 如仍无法解决，准备紧急借款（扣 5 分优于扣 10 分）
    """)
elif risk_level == "warning":
    st.warning(f"""
    ⚠️ **现金不足预警**：期末现金低于安全线 {safe_cash_buffer:.1f}万
    
    **建议措施**:
    1. 适度申请短期贷款
    2. 减少非必要支出
    3. 优先接回款周期短的订单
    """)
else:
    st.success("✅ 现金流健康，可以继续经营决策")

# 现金流结构分析
st.divider()
st.subheader("📈 现金流结构分析")

c1, c2 = st.columns(2)

with c1:
    # 现金流入结构
    inflow_df = pd.DataFrame({
        '项目': ['销售回款', '融资流入', '其他流入'],
        '金额': [sales_collection, loan_inflow, other_inflow]
    })
    
    if inflow_df['金额'].sum() > 0:
        fig = px.pie(inflow_df, values='金额', names='项目', title='现金流入结构', hole=0.4,
                     color_discrete_sequence=px.colors.sequential.Blues)
        st.plotly_chart(fig, use_container_width=True)

with c2:
    # 现金流出结构
    outflow_df = pd.DataFrame({
        '项目': ['经营支出', '投融资支出', '财务费用'],
        '金额': [
            purchase_payment + payroll + operating_expense + ad_expense,
            investment,
            loan_repayment + interest_payment + other_expense
        ]
    })
    
    if outflow_df['金额'].sum() > 0:
        fig = px.pie(outflow_df, values='金额', names='项目', title='现金流出结构', hole=0.4,
                     color_discrete_sequence=px.colors.sequential.Reds)
        st.plotly_chart(fig, use_container_width=True)

# 季度策略建议
st.divider()
st.subheader("💡 分季度决策建议")

if quarter == "Q1":
    st.info("""
    **Q1 策略**: 激进扩张，抢占市场
    
    | 项目 | 建议 |
    |------|------|
    | 报价策略 | 成本价×0.85-0.90 (低价抢市场) |
    | 广告投入 | 销售收入×8-10% |
    | 贷款策略 | 积极贷款，资产负债率≤65% |
    | 投资重点 | 设备购置，满足产能需求 |
    | 厂房策略 | 租赁优先，减少初期投资 |
    | 目标 | 中标率≥70%, 市场占有率进入前 30% |
    """)
elif quarter == "Q2":
    st.info("""
    **Q2 策略**: 稳定经营，优化现金流
    
    | 项目 | 建议 |
    |------|------|
    | 报价策略 | 成本价×0.95-1.00 (正常定价) |
    | 广告投入 | 销售收入×5-7% |
    | 贷款策略 | 控制规模，资产负债率≤60% |
    | 投资重点 | 优化配置，淘汰低效产能 |
    | 厂房策略 | 观察后再决定是否购置 |
    | 目标 | 净利润率≥7%, 流动比率≥1.2 |
    """)
elif quarter == "Q3":
    st.info("""
    **Q3 策略**: 扩张发展，提升竞争力
    
    | 项目 | 建议 |
    |------|------|
    | 报价策略 | 成本价×0.95-1.05 (灵活调整) |
    | 广告投入 | ROI≥1:6 才投放 |
    | 贷款策略 | 适度扩张，资产负债率≤65% |
    | 投资重点 | ROI≥30% 才投资 |
    | 厂房策略 | 可以购置，折旧抵税 |
    | 目标 | 销售增长率≥15%, 市场占有率进入前 20% |
    """)
else:
    st.info("""
    **Q4 策略**: 冲刺利润，美化报表
    
    | 项目 | 建议 |
    |------|------|
    | 报价策略 | 成本价×1.05-1.10 (利润导向) |
    | 广告投入 | 销售收入×3-5% (减少投入) |
    | 贷款策略 | 偿还债务，降低负债率≤55% |
    | 投资重点 | 停止新投资 |
    | 厂房策略 | 已购则持有，不再新增 |
    | 目标 | 净利润率≥10%, 资产负债率≤55% |
    """)

# 快捷计算器
st.divider()
st.subheader("🔢 快捷计算工具")

calc_type = st.selectbox("选择计算器", [
    "安全现金余额计算",
    "贷款需求测算",
    "最低销售回款测算"
])

if calc_type == "安全现金余额计算":
    fixed_expense_calc = st.number_input("下月固定支出 (万)", min_value=0.0, value=50.0)
    safety_factor = st.slider("安全系数", 1.0, 2.0, 1.2, 0.1)
    result = fixed_expense_calc * safety_factor
    st.metric("建议安全现金余额", f"{result:.1f}万")
    st.caption(f"计算公式：固定支出{fixed_expense_calc:.1f}万 × 安全系数{safety_factor:.1f} = {result:.1f}万")
    
elif calc_type == "贷款需求测算":
    cash_shortfall = st.number_input("预计现金缺口 (万)", min_value=0.0, value=20.0)
    buffer = st.number_input("额外安全边际 (万)", min_value=0.0, value=10.0)
    loan_needed = cash_shortfall + buffer
    st.metric("建议贷款金额", f"{loan_needed:.1f}万")
    st.caption(f"计算公式：现金缺口{cash_shortfall:.1f}万 + 安全边际{buffer:.1f}万 = {loan_needed:.1f}万")
    
elif calc_type == "最低销售回款测算":
    target_cash = st.number_input("目标期末现金 (万)", min_value=0.0, value=50.0)
    other_inflow_calc = st.number_input("其他现金流入 (万)", min_value=0.0, value=10.0)
    total_outflow_calc = st.number_input("预计现金流出 (万)", min_value=0.0, value=80.0)
    opening_calc = st.number_input("期初现金 (万)", min_value=0.0, value=30.0)
    
    min_collection = total_outflow_calc + target_cash - opening_calc - other_inflow_calc
    st.metric("最低销售回款需求", f"{max(0, min_collection):.1f}万")
    st.caption(f"计算公式：流出{total_outflow_calc:.1f}万 + 目标{target_cash:.1f}万 - 期初{opening_calc:.1f}万 - 其他{other_inflow_calc:.1f}万")
