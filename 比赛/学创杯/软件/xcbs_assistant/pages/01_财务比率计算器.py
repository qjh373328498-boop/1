"""
学创杯比赛辅助工具 - 财务比率计算器
实时计算 5 大能力指标，估算比赛得分
"""
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="财务比率计算器", page_icon="📊", layout="wide")

st.title("📊 财务比率计算器 & 得分估算")
st.markdown("**用途**: 实时计算 5 大能力 15 个指标，估算比赛得分，对标获奖标准")

# 侧边栏：获奖标准参考
st.sidebar.header("🏆 获奖标准参考")
st.sidebar.info("""
**一等奖**: ≥85 分
**二等奖**: 70-84 分
**三等奖**: 60-69 分

**三条红线**:
- 紧急借款：-5 分/次
- 逾期报税：-5 分/次
- 现金断流：-10 分/次
""")

st.sidebar.header("填写数据")
quarter = st.sidebar.selectbox("季度", ["Q1", "Q2", "Q3", "Q4"])

# 三张表数据输入
col1, col2, col3 = st.tabs(["资产负债表", "利润表", "现金流量表"])

with col1:
    st.subheader("资产负债表数据")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### 流动资产")
        cash = st.number_input("货币资金", min_value=0.0, value=50.0)
        receivables = st.number_input("应收账款", min_value=0.0, value=30.0)
        inventory = st.number_input("存货", min_value=0.0, value=20.0)
        current_assets = st.number_input("其他流动资产", min_value=0.0, value=5.0)
        total_current_assets = cash + receivables + inventory + current_assets
        st.metric("流动资产合计", f"{total_current_assets:.1f}万")
    
    with c2:
        st.markdown("#### 非流动资产")
        fa_net = st.number_input("固定资产净额", min_value=0.0, value=100.0)
        other_non_current = st.number_input("其他非流动资产", min_value=0.0, value=10.0)
        total_non_current_assets = fa_net + other_non_current
        st.metric("非流动资产合计", f"{total_non_current_assets:.1f}万")
    
    st.divider()
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### 流动负债")
        short_loan = st.number_input("短期借款", min_value=0.0, value=20.0)
        payables = st.number_input("应付账款", min_value=0.0, value=15.0)
        current_liabilities = st.number_input("其他流动负债", min_value=0.0, value=5.0)
        total_current_liabilities = short_loan + payables + current_liabilities
        st.metric("流动负债合计", f"{total_current_liabilities:.1f}万")
    
    with c2:
        st.markdown("#### 非流动负债")
        long_loan = st.number_input("长期借款", min_value=0.0, value=30.0)
        other_non_current_liab = st.number_input("其他非流动负债", min_value=0.0, value=5.0)
        total_non_current_liabilities = long_loan + other_non_current_liab
        st.metric("非流动负债合计", f"{total_non_current_liabilities:.1f}万")
    
    st.divider()
    total_assets = total_current_assets + total_non_current_assets
    total_liabilities = total_current_liabilities + total_non_current_liabilities
    equity = total_assets - total_liabilities
    
    c1, c2, c3 = st.columns(3)
    c1.metric("资产总计", f"{total_assets:.1f}万")
    c2.metric("负债合计", f"{total_liabilities:.1f}万")
    c3.metric("所有者权益", f"{equity:.1f}万")

with col2:
    st.subheader("利润表数据")
    
    c1, c2 = st.columns(2)
    with c1:
        revenue = st.number_input("营业收入", min_value=0.0, value=100.0)
        cogs = st.number_input("营业成本", min_value=0.0, value=60.0)
        gross_profit = revenue - cogs
        st.metric("毛利润", f"{gross_profit:.1f}万")
    
    with c2:
        operating_expense = st.number_input("期间费用", min_value=0.0, value=25.0)
        other_income = st.number_input("其他收益", min_value=0.0, value=2.0)
    
    st.divider()
    operating_profit = gross_profit - operating_expense
    total_profit = operating_profit + other_income
    tax = st.number_input("所得税费用", min_value=0.0, value=5.0)
    net_profit = total_profit - tax
    
    c1, c2, c3 = st.columns(3)
    c1.metric("营业利润", f"{operating_profit:.1f}万")
    c2.metric("利润总额", f"{total_profit:.1f}万")
    c3.metric("净利润", f"{net_profit:.1f}万")

with col3:
    st.subheader("现金流量表数据 (简化)")
    
    operating_cash = st.number_input("经营活动现金净流量", min_value=0.0, value=15.0)
    investing_cash = st.number_input("投资活动现金净流量", min_value=0.0, value=-20.0)
    financing_cash = st.number_input("筹资活动现金净流量", min_value=0.0, value=30.0)
    
    net_cash_flow = operating_cash + investing_cash + financing_cash
    st.metric("现金净增加额", f"{net_cash_flow:.1f}万")

# 计算财务比率
st.divider()
st.subheader("📊 财务比率计算结果")

# 1. 盈利能力 (30 分)
st.markdown("### 💰 盈利能力 (权重：30%)")

net_profit_margin = (net_profit / revenue * 100) if revenue > 0 else 0
roe = (net_profit / equity * 100) if equity > 0 else 0
roa = (total_profit / total_assets * 100) if total_assets > 0 else 0

avg_assets = total_assets  # 简化处理，用期末数代替平均数

col1, col2, col3 = st.columns(3)

col1.metric(
    "净利润率",
    f"{net_profit_margin:.2f}%",
    "优秀" if net_profit_margin > 10 else "良好" if net_profit_margin > 7 else "合格" if net_profit_margin > 5 else "需改进"
)

col2.metric(
    "ROE 净资产收益率",
    f"{roe:.2f}%",
    "优秀" if roe > 20 else "良好" if roe > 15 else "合格" if roe > 10 else "需改进"
)

col3.metric(
    "ROA 总资产报酬率",
    f"{roa:.2f}%",
    "优秀" if roa > 15 else "良好" if roa > 10 else "合格" if roa > 8 else "需改进"
)

# 盈利能力得分估算
profit_score = 0
if net_profit_margin > 10: profit_score += 10
elif net_profit_margin > 7: profit_score += 7
elif net_profit_margin > 5: profit_score += 5
else: profit_score += 3

if roe > 20: profit_score += 12
elif roe > 15: profit_score += 9
elif roe > 10: profit_score += 6
else: profit_score += 3

if roa > 15: profit_score += 8
elif roa > 10: profit_score += 5
elif roa > 8: profit_score += 3
else: profit_score += 1

st.caption(f"估算得分：{min(30, profit_score):.1f}/30")

# 2. 营运能力 (25 分)
st.markdown("### 🔄 营运能力 (权重：25%)")

receivables_turnover = revenue / receivables if receivables > 0 else 0
inventory_turnover = cogs / inventory if inventory > 0 else 0
assets_turnover = revenue / avg_assets if avg_assets > 0 else 0

col1, col2, col3 = st.columns(3)

col1.metric(
    "应收账款周转率",
    f"{receivables_turnover:.2f}次",
    "优秀" if receivables_turnover > 6 else "良好" if receivables_turnover > 4 else "合格" if receivables_turnover > 3 else "需改进"
)

col2.metric(
    "存货周转率",
    f"{inventory_turnover:.2f}次",
    "优秀" if inventory_turnover > 5 else "良好" if inventory_turnover > 3 else "合格" if inventory_turnover > 2 else "需改进"
)

col3.metric(
    "总资产周转率",
    f"{assets_turnover:.2f}次",
    "优秀" if assets_turnover > 1.5 else "良好" if assets_turnover > 1.0 else "合格" if assets_turnover > 0.8 else "需改进"
)

# 营运能力得分
operation_score = 0
if receivables_turnover > 6: operation_score += 9
elif receivables_turnover > 4: operation_score += 6
elif receivables_turnover > 3: operation_score += 4
else: operation_score += 2

if inventory_turnover > 5: operation_score += 9
elif inventory_turnover > 3: operation_score += 6
elif inventory_turnover > 2: operation_score += 4
else: operation_score += 2

if assets_turnover > 1.5: operation_score += 7
elif assets_turnover > 1.0: operation_score += 5
elif assets_turnover > 0.8: operation_score += 3
else: operation_score += 1

st.caption(f"估算得分：{min(25, operation_score):.1f}/25")

# 3. 偿债能力 (20 分)
st.markdown("### 💳 偿债能力 (权重：20%)")

current_ratio = total_current_assets / total_current_liabilities if total_current_liabilities > 0 else 0
quick_ratio = (total_current_assets - inventory) / total_current_liabilities if total_current_liabilities > 0 else 0
debt_ratio = total_liabilities / total_assets * 100 if total_assets > 0 else 0

col1, col2, col3 = st.columns(3)

col1.metric(
    "流动比率",
    f"{current_ratio:.2f}",
    "优秀" if current_ratio > 1.5 else "良好" if current_ratio > 1.2 else "合格" if current_ratio > 1.0 else "⚠️危险"
)

col2.metric(
    "速动比率",
    f"{quick_ratio:.2f}",
    "优秀" if quick_ratio > 1.2 else "良好" if quick_ratio > 0.8 else "合格" if quick_ratio > 0.6 else "⚠️危险"
)

col3.metric(
    "资产负债率",
    f"{debt_ratio:.1f}%",
    "优秀" if debt_ratio < 50 else "良好" if debt_ratio < 60 else "合格" if debt_ratio < 70 else "⚠️危险"
)

# 偿债能力得分
solvency_score = 0
if current_ratio > 1.5: solvency_score += 7
elif current_ratio > 1.2: solvency_score += 5
elif current_ratio > 1.0: solvency_score += 3
else: solvency_score += 1

if quick_ratio > 1.2: solvency_score += 7
elif quick_ratio > 0.8: solvency_score += 5
elif quick_ratio > 0.6: solvency_score += 3
else: solvency_score += 1

if debt_ratio < 50: solvency_score += 6
elif debt_ratio < 60: solvency_score += 4
elif debt_ratio < 70: solvency_score += 2
else: solvency_score += 0

st.caption(f"估算得分：{min(20, solvency_score):.1f}/20")

# 4. 发展能力 (15 分)
st.markdown("### 📈 发展能力 (权重：15%)")

st.info("💡 发展能力需要上期数据对比，此处使用简化估算")

growth_assumption = st.slider("假设销售增长率", -20, 50, 15)
capital_growth = st.slider("假设资本积累率", -10, 30, 10)
asset_growth = st.slider("假设总资产增长率", -10, 30, 10)

col1, col2, col3 = st.columns(3)

col1.metric(
    "销售增长率 (假设)",
    f"{growth_assumption:.1f}%",
    "优秀" if growth_assumption > 20 else "良好" if growth_assumption > 10 else "合格" if growth_assumption > 5 else "需改进"
)

col2.metric(
    "资本积累率 (假设)",
    f"{capital_growth:.1f}%",
    "优秀" if capital_growth > 15 else "良好" if capital_growth > 10 else "合格" if capital_growth > 5 else "需改进"
)

col3.metric(
    "总资产增长率 (假设)",
    f"{asset_growth:.1f}%",
    "优秀" if asset_growth > 15 else "良好" if asset_growth > 10 else "合格" if asset_growth > 5 else "需改进"
)

growth_score = 0
if growth_assumption > 20: growth_score += 5
elif growth_assumption > 10: growth_score += 3
elif growth_assumption > 5: growth_score += 2

if capital_growth > 15: growth_score += 5
elif capital_growth > 10: growth_score += 3
elif capital_growth > 5: growth_score += 2

if asset_growth > 15: growth_score += 5
elif asset_growth > 10: growth_score += 3
elif asset_growth > 5: growth_score += 2

st.caption(f"估算得分：{min(15, growth_score):.1f}/15")

# 5. 预算能力 (10 分)
st.markdown("### 📋 预算能力 (权重：10%)")

budget_variance = st.slider("预算偏差率（估计值）", 0, 30, 8)

if budget_variance < 5:
    budget_score = 10
    rating = "优秀"
elif budget_variance < 10:
    budget_score = 8
    rating = "良好"
elif budget_variance < 15:
    budget_score = 6
    rating = "合格"
else:
    budget_score = 3
    rating = "需改进"

st.metric("预算偏差率", f"{budget_variance:.1f}%", delta=rating)
st.caption(f"估算得分：{budget_score:.1f}/10")

# 总分汇总
st.divider()
st.subheader("🏆 总分汇总")

total_score = profit_score + operation_score + solvency_score + growth_score + budget_score

col1, col2, col3 = st.columns(3)

col1.metric("盈利能力", f"{profit_score:.1f}/30")
col2.metric("营运能力", f"{operation_score:.1f}/25")
col3.metric("偿债能力", f"{solvency_score:.1f}/20")

col1.metric("发展能力", f"{growth_score:.1f}/15")
col2.metric("预算能力", f"{budget_score:.1f}/10")
col3.metric("总分估算", f"{total_score:.1f}/100")

# 获奖等级判断
st.divider()
if total_score >= 85:
    st.success(f"""
    ## 🎉 恭喜！当前成绩可达 **一等奖**
    
    总分：**{total_score:.1f}分** (≥85 分)
    
    **关键优势**:
    - 盈利能力强劲
    - 营运效率高
    - 财务结构稳健
    """)
elif total_score >= 70:
    st.info(f"""
    ## 👍 当前成绩可达 **二等奖**
    
    总分：**{total_score:.1f}分** (70-84 分)
    
    **改进建议**:
    - 提升净利润率到 10% 以上
    - 加快应收账款周转
    - 优化资产负债结构
    """)
elif total_score >= 60:
    st.warning(f"""
    ## ✅ 当前成绩可达 **三等奖**
    
    总分：**{total_score:.1f}分** (60-69 分)
    
    **亟需改进**:
    - 控制成本费用
    - 减少存货积压
    - 避免紧急借款和逾期报税
    """)
else:
    st.error(f"""
    ## ⚠️ 当前成绩 **未获奖**
    
    总分：**{total_score:.1f}分** (<60 分)
    
    **立即采取行动**:
    1. 检查现金流，避免断流 (-10 分)
    2. 准时报税，避免扣分 (-5 分)
    3. 减少紧急借款 (-5 分/次)
    4. 提升产能利用率
    """)

# 可视化对比
st.divider()
st.subheader("📊 雷达图分析")

categories = ['盈利能力', '营运能力', '偿债能力', '发展能力', '预算能力']
scores = [profit_score/30*100, operation_score/25*100, solvency_score/20*100, growth_score/15*100, budget_score/10*100]
perfect = [100, 100, 100, 100, 100]

radar_df = pd.DataFrame({
    '指标': categories + [categories[0]],
    '当前得分': scores + [scores[0]],
    '满分': perfect + [perfect[0]]
})

fig = px.line_polar(
    radar_df,
    r='当前得分',
    theta='指标',
    title='财务能力雷达图',
    line_close=True,
    template='plotly_white'
)
fig.update_traces(fill='toself', line_color='#1f77b4')
fig.update_layout(height=500)
st.plotly_chart(fig, use_container_width=True)
