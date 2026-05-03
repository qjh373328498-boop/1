"""
学创杯比赛辅助工具 - 预算编制助手
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go


# ========== 性能优化 ==========
# Session State: 保存用户输入，切换页面不丢失
if 'page_data' not in st.session_state:
    st.session_state.page_data = {}

def get_input(key, default):
    """从 session_state 获取输入"""
    if key not in st.session_state:
        st.session_state[key] = default
    return st.session_state[key]

# ========== 原始代码 ==========

st.set_page_config(page_title="预算编制助手", page_icon="📋", layout="wide")

st.title("📋 预算编制助手")
st.markdown("**用途**: 编制 4 张预算表，控制预算偏差<10%（预算能力占 10 分）")

# 侧边栏
st.sidebar.header("预算能力评分标准")
st.sidebar.info("""
| 预算偏差率 | 得分 | 等级 |
|-----------|------|------|
| <5% | 10 分 | 优秀 |
| 5-10% | 8 分 | 良好 |
| 10-15% | 6 分 | 合格 |
| >15% | 3 分 | 需改进 |

**目标**: 偏差率<10%，确保 8 分以上
""")

st.sidebar.header("选择季度")
quarter = st.sidebar.selectbox("当前季度", ["Q1", "Q2", "Q3", "Q4"])

# Tab 页签
tab1, tab2, tab3, tab4 = st.tabs(["📊 销售收入预算", "🏭 生产成本预算", "💰 费用预算", "💵 现金预算"])

with tab1:
    st.subheader("📊 销售收入预算表")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### A 产品")
        a_volume_q1 = st.number_input("A 产品预计销量 (件)", min_value=0, value=1000, key="a_vol")
        a_price_q1 = st.number_input("A 产品单价 (元)", min_value=0.0, value=100.0, key="a_price")
        a_revenue = a_volume_q1 * a_price_q1
        st.metric("A 产品销售收入", f"{a_revenue:,.0f}元")
    
    with col2:
        st.markdown("#### B 产品")
        b_volume_q1 = st.number_input("B 产品预计销量 (件)", min_value=0, value=800, key="b_vol")
        b_price_q1 = st.number_input("B 产品单价 (元)", min_value=0.0, value=120.0, key="b_price")
        b_revenue = b_volume_q1 * b_price_q1
        st.metric("B 产品销售收入", f"{b_revenue:,.0f}元")
    
    st.divider()
    total_revenue = a_revenue + b_revenue
    st.metric("销售收入合计", f"{total_revenue:,.0f}元")
    
    # 回款假设
    st.markdown("#### 回款假设")
    collection_rate = st.slider("当季回款比例 (%)", 60, 100, 80)
    current_collection = total_revenue * collection_rate / 100
    next_collection = total_revenue * (100 - collection_rate) / 100
    
    c1, c2 = st.columns(2)
    c1.metric("当季回款", f"{current_collection:,.0f}元")
    c2.metric("下季回款", f"{next_collection:,.0f}元")

with tab2:
    st.subheader("🏭 生产成本预算表")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 直接材料")
        a_material = st.number_input("A 产品单位材料成本", min_value=0.0, value=30.0, key="am")
        b_material = st.number_input("B 产品单位材料成本", min_value=0.0, value=35.0, key="bm")
        total_material = a_volume_q1 * a_material + b_volume_q1 * b_material
        st.metric("材料成本合计", f"{total_material:,.0f}元")
    
    with col2:
        st.markdown("#### 直接人工")
        a_labor = st.number_input("A 产品单位人工成本", min_value=0.0, value=20.0, key="al")
        b_labor = st.number_input("B 产品单位人工成本", min_value=0.0, value=25.0, key="bl")
        total_labor = a_volume_q1 * a_labor + b_volume_q1 * b_labor
        st.metric("人工成本合计", f"{total_labor:,.0f}元")
    
    with col3:
        st.markdown("#### 制造费用")
        manufacturing_exp = st.number_input("制造费用 (折旧 + 水电等)", min_value=0.0, value=15000.0, key="mf")
        st.metric("制造费用", f"{manufacturing_exp:,.0f}元")
    
    st.divider()
    total_production_cost = total_material + total_labor + manufacturing_exp
    
    c1, c2, c3 = st.columns(3)
    c1.metric("生产成本合计", f"{total_production_cost:,.0f}元")
    
    unit_cost_a = a_material + a_labor + manufacturing_exp / (a_volume_q1 + b_volume_q1)
    unit_cost_b = b_material + b_labor + manufacturing_exp / (a_volume_q1 + b_volume_q1)
    
    c2.metric("A 产品单位成本", f"{unit_cost_a:.2f}元")
    c3.metric("B 产品单位成本", f"{unit_cost_b:.2f}元")

with tab3:
    st.subheader("💰 费用预算表")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 管理费用")
        admin_salary = st.number_input("管理人员工资", min_value=0.0, value=10000.0)
        office_expense = st.number_input("办公费用", min_value=0.0, value=3000.0)
        other_admin = st.number_input("其他管理费用", min_value=0.0, value=2000.0)
        total_admin = admin_salary + office_expense + other_admin
        st.metric("管理费用合计", f"{total_admin:,.0f}元")
    
    with col2:
        st.markdown("#### 销售费用")
        ad_budget = st.number_input("广告费用", min_value=0.0, value=total_revenue * 0.07)
        sales_salary = st.number_input("销售人员工资", min_value=0.0, value=8000.0)
        other_sales = st.number_input("其他销售费用", min_value=0.0, value=1500.0)
        total_sales = ad_budget + sales_salary + other_sales
        st.metric("销售费用合计", f"{total_sales:,.0f}元")
    
    st.divider()
    
    col1, col2, col3 = st.columns(3)
    
    interest_expense = st.number_input("财务费用 - 利息支出", min_value=0.0, value=2000.0)
    
    total_expense = total_admin + total_sales + interest_expense
    
    col1.metric("管理费用", f"{total_admin:,.0f}元")
    col2.metric("销售费用", f"{total_sales:,.0f}元")
    col3.metric("费用总计", f"{total_expense:,.0f}元")
    
    # 费用率分析
    expense_rate = total_expense / total_revenue * 100 if total_revenue > 0 else 0
    st.metric("费用率", f"{expense_rate:.1f}%", 
              delta="优秀" if expense_rate < 20 else "良好" if expense_rate < 30 else "需控制")

with tab4:
    st.subheader("💵 现金预算表（汇总）")
    
    # 现金流入
    st.markdown("#### 现金流入")
    
    opening_cash = st.number_input("期初现金余额", min_value=0.0, value=100000.0)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("销售回款", f"{current_collection:,.0f}元")
    
    loan_inflow = st.number_input("融资流入 - 贷款", min_value=0.0, value=50000.0)
    col2.metric("融资流入", f"{loan_inflow:,.0f}元")
    
    other_inflow = st.number_input("其他现金流入", min_value=0.0, value=0.0)
    col3.metric("其他流入", f"{other_inflow:,.0f}元")
    
    total_inflow = current_collection + loan_inflow + other_inflow
    
    st.divider()
    
    # 现金流出
    st.markdown("#### 现金流出")
    
    col1, col2, col3 = st.columns(3)
    
    material_payment = st.number_input("材料采购支出", min_value=0.0, value=total_material * 0.8)
    col1.metric("采购支出", f"{material_payment:,.0f}元")
    
    payroll_payment = st.number_input("人工支出", min_value=0.0, value=total_labor)
    col2.metric("人工支出", f"{payroll_payment:,.0f}元")
    
    expense_payment = st.number_input("费用支出", min_value=0.0, value=total_expense)
    col3.metric("费用支出", f"{expense_payment:,.0f}元")
    
    loan_repayment = st.number_input("归还贷款本金", min_value=0.0, value=0.0)
    investment = st.number_input("投资支出", min_value=0.0, value=0.0)
    other_outflow = st.number_input("其他支出", min_value=0.0, value=0.0)
    
    total_outflow = material_payment + payroll_payment + expense_payment + loan_repayment + investment + other_outflow
    
    st.divider()
    
    # 汇总
    st.markdown("#### 现金预算汇总")
    
    net_cash_flow = total_inflow - total_outflow
    closing_cash = opening_cash + net_cash_flow
    
    # 安全线计算
    fixed_expense = payroll_payment + expense_payment
    safe_cash_line = fixed_expense * 1.2
    
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("期初现金", f"{opening_cash:,.0f}元")
    col2.metric("现金净流入", f"{net_cash_flow:,.0f}元")
    col3.metric("期末现金", f"{closing_cash:,.0f}元",
                delta="✅安全" if closing_cash >= safe_cash_line else "⚠️不足")
    col4.metric("安全现金线", f"{safe_cash_line:,.0f}元")
    
    # 风险提示
    if closing_cash < 0:
        st.error("🚨 现金断流预警！需要立即调整预算或增加融资")
    elif closing_cash < safe_cash_line:
        st.warning(f"⚠️ 现金不足！建议增加融资或减少支出{(safe_cash_line - closing_cash):,.0f}元")
    else:
        st.success("✅ 现金预算安全")

# 预算汇总分析
st.divider()
st.subheader("📊 预算汇总分析")

# 利润预算
gross_profit = total_revenue - total_production_cost
operating_profit = gross_profit - total_expense
net_profit_margin = (operating_profit / total_revenue * 100) if total_revenue > 0 else 0

col1, col2, col3 = st.columns(3)

col1.metric("预计毛利润", f"{gross_profit:,.0f}元")
col2.metric("预计营业利润", f"{operating_profit:,.0f}元")
col3.metric("预计利润率", f"{net_profit_margin:.1f}%")

# 预算偏差模拟
st.divider()
st.subheader("📈 预算偏差敏感性分析")

st.markdown("假设实际执行发生偏差，对预算能力得分的影响:")

variance_rates = [-20, -15, -10, -5, 0, 5, 10, 15, 20]
variance_data = []

for rate in variance_rates:
    actual_revenue = total_revenue * (1 + rate / 100)
    actual_expense = total_expense * (1 + rate / 100)
    variance = abs(rate)
    
    if variance < 5:
        score = 10
        rating = "优秀"
    elif variance < 10:
        score = 8
        rating = "良好"
    elif variance < 15:
        score = 6
        rating = "合格"
    else:
        score = 3
        rating = "需改进"
    
    variance_data.append({
        '偏差率': f"{rate:+d}%",
        '实际收入': f"{actual_revenue:,.0f}",
        '偏差绝对值': f"{variance}%",
        '预算得分': f"{score}分",
        '评级': rating
    })

variance_df = pd.DataFrame(variance_data)
st.dataframe(variance_df, use_container_width=True, hide_index=True)

# 可视化
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=[f"{r}%" for r in variance_rates],
    y=[10 if abs(r) < 5 else 8 if abs(r) < 10 else 6 if abs(r) < 15 else 3 for r in variance_rates],
    mode='lines+markers',
    name='预算得分',
    line=dict(width=3)
))

fig.update_layout(
    title='预算偏差率与得分关系',
    xaxis_title='偏差率',
    yaxis_title='得分',
    height=400,
    yaxis=dict(range=[0, 11])
)

st.plotly_chart(fig, use_container_width=True)

st.info("""
**💡 提高预算准确性的技巧**:

1. **销售收入预算**:
   - 参考历史数据和市场趋势
   - 考虑季节性因素
   - 与团队讨论确定合理销量

2. **成本费用预算**:
   - 固定费用相对稳定
   - 变动费用与销量挂钩
   - 预留 5-10% 的弹性空间

3. **现金预算**:
   - 考虑回款周期（通常 60-80% 当季回款）
   - 注意贷款到期时间
   - 保持安全现金余额（≥固定支出×1.2）
""")
