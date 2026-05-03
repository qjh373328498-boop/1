# 💳 贷款决策助手
# 优化贷款结构，计算利息最小化方案

import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="贷款决策助手", page_icon="💳", layout="wide")

st.title("💳 贷款决策助手")
st.markdown("**优化贷款结构，降低利息支出，避免高负债扣分**")

st.divider()

# 比赛规则中的贷款限制
MAX_LOAN_RATIO = 0.65  # 资产负债率上限 65%
LOAN_INTEREST_RATE = 0.05  # 年利率 5%
QUARTERLY_INTEREST_RATE = LOAN_INTEREST_RATE / 4  # 季度利率

with st.sidebar:
    st.header("📋 当前财务状况")
    
    col1, col2 = st.columns(2)
    with col1:
        total_assets = st.number_input(
            "总资产 (万元)",
            min_value=0.0,
            value=1000.0,
            step=50.0
        )
        current_loans = st.number_input(
            "现有贷款 (万元)",
            min_value=0.0,
            value=300.0,
            step=50.0
        )
    with col2:
        cash_balance = st.number_input(
            "现金余额 (万元)",
            min_value=0.0,
            value=150.0,
            step=20.0
        )
        planned_investment = st.number_input(
            "计划投资 (万元)",
            min_value=0.0,
            value=200.0,
            step=50.0
        )

st.divider()

# 计算当前负债率
current_loan_ratio = current_loans / total_assets if total_assets > 0 else 0

st.subheader("📊 当前负债状况")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="当前资产负债率",
        value=f"{current_loan_ratio:.1%}",
        delta="超标" if current_loan_ratio > MAX_LOAN_RATIO else "安全",
        delta_color="normal" if current_loan_ratio <= MAX_LOAN_RATIO else "inverse"
    )

with col2:
    max_additional_loan = total_assets * MAX_LOAN_RATIO - current_loans
    st.metric(
        label="最大可新增贷款",
        value=f"{max_additional_loan:.1f}万元",
        help=f"基于{MAX_LOAN_RATIO:.0%}负债率上限计算"
    )

with col3:
    quarterly_interest = current_loans * QUARTERLY_INTEREST_RATE
    st.metric(
        label="当前季度利息",
        value=f"{quarterly_interest:.2f}万元",
        help=f"按年利率{LOAN_INTEREST_RATE:.0%}计算"
    )

st.divider()

st.subheader("💰 贷款方案对比")

loan_options = []

# 方案 1: 不新增贷款
loan_options.append({
    "方案": "保守方案",
    "新增贷款 (万元)": 0,
    "总贷款 (万元)": current_loans,
    "资产负债率": current_loans / total_assets if total_assets > 0 else 0,
    "季度利息 (万元)": current_loans * QUARTERLY_INTEREST_RATE,
    "资金缺口 (万元)": max(0, planned_investment - cash_balance),
    "可行性": "✅" if cash_balance >= planned_investment else "❌"
})

# 方案 2: 最小额度贷款
min_needed = max(0, planned_investment - cash_balance)
if min_needed <= max_additional_loan:
    loan_options.append({
        "方案": "最小贷款",
        "新增贷款 (万元)": min_needed,
        "总贷款 (万元)": current_loans + min_needed,
        "资产负债率": (current_loans + min_needed) / total_assets if total_assets > 0 else 0,
        "季度利息 (万元)": (current_loans + min_needed) * QUARTERLY_INTEREST_RATE,
        "资金缺口 (万元)": 0,
        "可行性": "✅"
    })

# 方案 3: 最大可贷额度
if max_additional_loan > 0:
    loan_options.append({
        "方案": "最大额度",
        "新增贷款 (万元)": max_additional_loan,
        "总贷款 (万元)": current_loans + max_additional_loan,
        "资产负债率": (current_loans + max_additional_loan) / total_assets if total_assets > 0 else MAX_LOAN_RATIO + 0.01,
        "季度利息 (万元)": (current_loans + max_additional_loan) * QUARTERLY_INTEREST_RATE,
        "资金缺口 (万元)": 0,
        "可行性": "⚠️ 顶格"
    })

# 方案 4: 自定义贷款
custom_loan = st.number_input(
    "🔧 自定义贷款金额 (万元)",
    min_value=0.0,
    max_value=max_additional_loan * 1.5,
    value=min(min_needed, max_additional_loan) if min_needed > 0 else 0,
    step=20.0
)

custom_total = current_loans + custom_loan
custom_ratio = custom_total / total_assets if total_assets > 0 else 0
custom_interest = custom_total * QUARTERLY_INTEREST_RATE
custom_gap = max(0, planned_investment - cash_balance - custom_loan)

loan_options.append({
    "方案": "自定义方案",
    "新增贷款 (万元)": custom_loan,
    "总贷款 (万元)": custom_total,
    "资产负债率": custom_ratio,
    "季度利息 (万元)": custom_interest,
    "资金缺口 (万元)": custom_gap,
    "可行性": "❌ 超标" if custom_ratio > MAX_LOAN_RATIO else ("✅" if custom_gap == 0 else "⚠️ 不足")
})

# 显示对比表
df_loans = pd.DataFrame(loan_options)
df_loans["资产负债率"] = df_loans["资产负债率"].apply(lambda x: f"{x:.1%}")
df_loans["季度利息 (万元)"] = df_loans["季度利息 (万元)"].apply(lambda x: f"{x:.2f}")
df_loans["资金缺口 (万元)"] = df_loans["资金缺口 (万元)"].apply(lambda x: f"{x:.1f}")
df_loans["总贷款 (万元)"] = df_loans["总贷款 (万元)"].apply(lambda x: f"{x:.1f}")
df_loans["新增贷款 (万元)"] = df_loans["新增贷款 (万元)"].apply(lambda x: f"{x:.1f}")

st.dataframe(
    df_loans[["方案", "新增贷款 (万元)", "总贷款 (万元)", "资产负债率", "季度利息 (万元)", "资金缺口 (万元)", "可行性"]],
    use_container_width=True,
    hide_index=True
)

st.divider()

st.subheader("🎯 推荐策略")

if current_loan_ratio > MAX_LOAN_RATIO:
    st.error(f"""
    **⚠️ 负债率已超标！**
    
    当前资产负债率 **{current_loan_ratio:.1%}**，超过上限 **{MAX_LOAN_RATIO:.0%}**
    
    **建议**：
    1. 本季度不要再新增贷款
    2. 考虑使用应收账款贴现或出售资产
    3. 优先偿还部分贷款降低负债率
    """)
elif max_additional_loan < planned_investment - cash_balance:
    st.warning(f"""
    **⚠️ 资金缺口较大，但贷款额度有限**
    
    最大可贷额度 **{max_additional_loan:.1f}万元**，但资金需求 **{planned_investment - cash_balance:.1f}万元**
    
    **建议**：
    1. 申请最大额度贷款 **{max_additional_loan:.1f}万元**
    2. 考虑调整投资计划，分期投入
    3. 加快应收账款回收
    4. 可以考虑应收账款贴现（注意贴息成本）
    """)
elif cash_balance >= planned_investment:
    st.success(f"""
    **✅ 资金充足，无需贷款**
    
    当前现金 **{cash_balance:.1f}万元** > 投资需求 **{planned_investment:.1f}万元**
    
    **建议**：
    1. 使用自有资金完成投资
    2. 考虑偿还部分现有贷款，降低利息支出
    3. 每季度可节省利息 **{current_loans * QUARTERLY_INTEREST_RATE:.2f}万元**
    """)
else:
    optimal_loan = min(planned_investment - cash_balance, max_additional_loan * 0.9)
    st.info(f"""
    **💡 建议采用稳健贷款策略**
    
    推荐新增贷款 **{optimal_loan:.1f}万元**（保留 10% 缓冲）
    
    **优势**：
    1. 满足投资需求，无资金缺口
    2. 负债率 **{(current_loans + optimal_loan) / total_assets:.1%}**，低于上限
    3. 季度利息 **{(current_loans + optimal_loan) * QUARTERLY_INTEREST_RATE:.2f}万元**，成本可控
    4. 保留一定融资空间应对突发情况
    """)

st.divider()

st.subheader("📈 贷款对利润的影响分析")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**利息支出测算**")
    
    loan_amounts = [0, 100, 200, 300, 400, 500]
    interest_data = []
    
    for loan in loan_amounts:
        total = current_loans + loan
        ratio = total / total_assets if total_assets > 0 else 0
        if ratio <= MAX_LOAN_RATIO + 0.1:
            quarterly_int = total * QUARTERLY_INTEREST_RATE
            annual_int = total * LOAN_INTEREST_RATE
            interest_data.append({
                "新增贷款": f"{loan}万元",
                "季度利息": f"{quarterly_int:.2f}万元",
                "年度利息": f"{annual_int:.2f}万元",
                "影响利润": f"-{annual_int:.2f}万元"
            })
    
    df_interest = pd.DataFrame(interest_data)
    st.dataframe(df_interest, use_container_width=True, hide_index=True)

with col2:
    st.markdown("**盈亏平衡分析**")
    
    if planned_investment > 0:
        roi_break_even = ((current_loans + max_additional_loan) * LOAN_INTEREST_RATE) / planned_investment * 100
        
        st.write(f"""
        若贷款 **{max_additional_loan:.1f}万元** 用于投资：
        
        - 年利息支出：**{(current_loans + max_additional_loan) * LOAN_INTEREST_RATE:.2f}万元**
        - 投资回报率需达到 **{roi_break_even:.1f}%** 才能覆盖利息
        - 建议投资 ROI 目标：**{roi_break_even * 1.5:.1f}%**（1.5 倍安全边际）
        """)
        
        # 可视化
        import plotly.graph_objects as go
        
        fig = go.Figure()
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=roi_break_even,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "保本 ROI (%)"},
            gauge={
                'axis': {'range': [0, 30]},
                'bar': {'color': "blue"},
                'steps': [
                    {'range': [0, roi_break_even], 'color': "lightyellow"},
                    {'range': [roi_break_even, roi_break_even * 2], 'color': "lightgreen"},
                    {'range': [roi_break_even * 2, 30], 'color': "green"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': roi_break_even
                }
            }
        ))
        
        fig.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("⚠️ 风险提示")

st.markdown("""
**贷款决策注意事项**：

1. **负债率红线**：资产负债率 >70% 会被判定为高风险，影响评分
2. **利息侵蚀利润**：贷款利息直接减少净利润，影响盈利能力得分
3. **还本压力**：长期贷款需在到期季度一次性偿还，提前做好现金规划
4. **贷款额度限制**：某些赛季可能限制 single 季度最大贷款额度

**优化建议**：
- 优先使用自有资金，贷款作为补充
- 贷款额度控制在 60% 以内，保留缓冲空间
- 季度末提前规划还款，避免现金断流
- 高利润季度可考虑提前还贷，减少利息支出
""")
