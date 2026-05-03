# 🏭 产能规划工具
# 计算产能利用率，提供投资决策建议

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="产能规划工具", page_icon="🏭", layout="wide")

st.title("🏭 产能规划工具")
st.markdown("**计算产能利用率，优化投资决策，避免产能闲置或不足**")

st.divider()

# 侧边栏：基础数据输入
with st.sidebar:
    st.header("📋 基础数据")
    
    st.subheader("当前产能")
    product_lines = st.number_input("生产线数量", min_value=1, max_value=10, value=4)
    capacity_per_line = st.number_input("单线产能 (件/季度)", min_value=100, max_value=10000, value=2000, step=100)
    
    st.subheader("订单需求")
    q1_demand = st.number_input("Q1 订单量 (件)", min_value=0, value=5000, step=500)
    q2_demand = st.number_input("Q2 订单量 (件)", min_value=0, value=6000, step=500)
    q3_demand = st.number_input("Q3 订单量 (件)", min_value=0, value=8000, step=500)
    q4_demand = st.number_input("Q4 订单量 (件)", min_value=0, value=7000, step=500)
    
    st.subheader("投资参数")
    new_line_cost = st.number_input("新生产线投资 (万元)", min_value=50, max_value=500, value=150, step=20)
    depreciation_years = st.number_input("折旧年限", min_value=1, max_value=10, value=5, step=1)
    disposal_value = st.number_input("残值率 (%)", min_value=0, max_value=50, value=10, step=5)

# 计算总产能
total_capacity = product_lines * capacity_per_line
quarterly_capacities = [q1_demand, q2_demand, q3_demand, q4_demand]
utilization_rates = [min(d / total_capacity * 100, 150) for d in quarterly_capacities]

st.divider()

st.subheader("📊 产能利用率分析")

col1, col2, col3 = st.columns(3)

with col1:
    annual_demand = sum(quarterly_capacities)
    annual_capacity = total_capacity * 4
    annual_utilization = annual_demand / annual_capacity * 100
    
    st.metric(
        label="年化产能利用率",
        value=f"{annual_utilization:.1f}%",
        delta=get_status(annual_utilization),
        delta_color="normal" if 85 <= annual_utilization <= 95 else "inverse"
    )

with col2:
    avg_quarterly_util = sum(utilization_rates) / 4
    st.metric(
        label="季度平均利用率",
        value=f"{avg_quarterly_util:.1f}%",
        delta="均衡" if max(utilization_rates) - min(utilization_rates) < 20 else "波动大"
    )

with col3:
    unused_capacity = max(0, total_capacity - max(quarterly_capacities))
    st.metric(
        label="闲置产能 (件/季)",
        value=f"{unused_capacity:.0f}",
        delta=f"相当于{unused_capacity/capacity_per_line:.1f}条线",
        delta_color="inverse" if unused_capacity > total_capacity * 0.2 else "normal"
    )

def get_status(rate):
    if rate < 70:
        return "⚠️ 产能闲置"
    elif rate < 85:
        return "👌 偏低"
    elif rate <= 95:
        return "✅ 最优"
    elif rate <= 100:
        return "👍 充分"
    else:
        return "🔥 超负荷"

# 可视化产能利用率
fig = go.Figure()

fig.add_trace(go.Bar(
    name="订单需求",
    x=["Q1", "Q2", "Q3", "Q4"],
    y=quarterly_capacities,
    marker_color="steelblue"
))

fig.add_hline(
    y=total_capacity,
    line_dash="dash",
    line_color="red",
    annotation_text=f"总产能：{total_capacity}件",
    annotation_position="right"
)

fig.add_hrect(
    y0=total_capacity * 0.85,
    y1=total_capacity * 0.95,
    fillcolor="green",
    opacity=0.2,
    annotation_text="最优区间 (85%-95%)",
    annotation_position="right"
)

fig.update_layout(
    title="季度产能利用率趋势",
    xaxis_title="季度",
    yaxis_title="产能 (件)",
    height=400,
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

# 详细数据表
st.markdown("**📋 季度产能分析表**")

df_capacity = pd.DataFrame({
    "季度": ["Q1", "Q2", "Q3", "Q4"],
    "订单需求 (件)": quarterly_capacities,
    "总产能 (件)": [total_capacity] * 4,
    "利用率": [f"{u:.1f}%" for u in utilization_rates],
    "状态": [get_status(u) for u in utilization_rates],
    "闲置/缺口 (件)": [total_capacity - d if d < total_capacity else f"-{d - total_capacity}" for d in quarterly_capacities]
})

st.dataframe(df_capacity, use_container_width=True, hide_index=True)

st.divider()

st.subheader("💡 产能优化建议")

if annual_utilization < 70:
    st.warning(f"""
    **⚠️ 产能严重闲置**
    
    当前年化利用率仅 **{annual_utilization:.1f}%**，存在资源浪费
    
    **建议**：
    1. 考虑出售 {(1 - annual_utilization/90) * product_lines:.1f} 条生产线（约可回收 {(1 - annual_utilization/90) * product_lines * new_line_cost * (1 - 0.2):.1f}万元）
    2. 加大市场开拓力度，争取更多订单
    3. 提高广告投放效率，提升中标率
    4. 考虑开发新产品，利用闲置产能
    """)
    
elif annual_utilization < 85:
    st.info(f"""
    **👌 产能利用率偏低**
    
    当前利用率 **{annual_utilization:.1f}%**，有提升空间
    
    **建议**：
    1. 适度增加广告投入，目标提升中标率 {85 - annual_utilization:.0f} 个百分点
    2. 优化产品定价，提升竞争力
    3. 暂不投资新生产线
    4. 可考虑接受低毛利订单填补产能
    """)
    
elif annual_utilization <= 95:
    st.success(f"""
    **✅ 产能利用最优**
    
    当前利用率 **{annual_utilization:.1f}%**，处于理想区间
    
    **建议**：
    1. 保持当前产能配置
    2. 关注 Q3 高峰期的产能调配
    3. 如有新订单，可考虑小幅扩产
    4. 优化排产计划，减少换线损失
    """)
    
elif annual_utilization <= 100:
    st.info(f"""
    **👍 产能充分利用**
    
    当前利用率 **{annual_utilization:.1f}%**，接近满负荷
    
    **建议**：
    1. 评估是否需要增加 {max(quarterly_capacities) / capacity_per_line - product_lines:.1f} 条生产线
    2. 考虑优化排产，提升单线效率
    3. 高峰期可考虑外包部分产能
    4. 投资新线需提前 {depreciation_years} 季度规划
    """)
    
else:
    shortage_quarters = [f"Q{i+1}" for i, u in enumerate(utilization_rates) if u > 100]
    st.error(f"""
    **🔥 产能超负荷**
    
    当前利用率 **{annual_utilization:.1f}%**，超产可能影响交货
    
    **需扩产季度**: {', '.join(shortage_quarters)}
    
    **建议**：
    1. **立即投资** {max(quarterly_capacities) / capacity_per_line - product_lines + 1:.0f} 条新生产线（投资 {(max(quarterly_capacities) / capacity_per_line - product_lines + 1) * new_line_cost:.1f}万元）
    2. 短期可考虑外包生产（成本约增加 15%-20%）
    3. 与客户协商延期交付部分订单
    4. 优化排产，优先保障高毛利订单
    """)

st.divider()

st.subheader("🏗️ 投资回报分析")

# 投资方案对比
investment_options = []

# 方案 1: 不投资
annual_interest_save = 0  # 不投资节省的利息
capacity_shortage = max(0, max(quarterly_capacities) - total_capacity)
lost_profit = capacity_shortage * 0.15  # 假设每件利润 0.15 万元

investment_options.append({
    "方案": "维持现状",
    "投资额 (万元)": 0,
    "新增产能 (件)": 0,
    "年折旧 (万元)": 0,
    "产能缺口 (件)": capacity_shortage,
    "机会成本 (万元)": lost_profit,
    "净影响 (万元)": f"-{lost_profit:.2f}"
})

# 方案 2: 刚好满足高峰需求
if capacity_shortage > 0:
    lines_needed = (capacity_shortage // capacity_per_line) + 1
    investment = lines_needed * new_line_cost
    annual_depreciation = investment * (1 - disposal_value/100) / depreciation_years
    new_total_capacity = total_capacity + lines_needed * capacity_per_line
    new_utilization = annual_demand / (new_total_capacity * 4) * 100
    
    investment_options.append({
        "方案": "精准扩产",
        "投资额 (万元)": investment,
        "新增产能 (件)": lines_needed * capacity_per_line,
        "年折旧 (万元)": f"{annual_depreciation:.2f}",
        "产能缺口 (件)": 0,
        "机会成本 (万元)": 0,
        "净影响 (万元)": f"-{annual_depreciation:.2f}"
    })
    
    # 方案 3: 保守扩产（预留 10% 缓冲）
    buffer_lines = int((max(quarterly_capacities) * 1.1 / capacity_per_line) - product_lines) + 1
    if buffer_lines > lines_needed:
        investment_buffer = buffer_lines * new_line_cost
        annual_depreciation_buffer = investment_buffer * (1 - disposal_value/100) / depreciation_years
        
        investment_options.append({
            "方案": "保守扩产 (+10%)",
            "投资额 (万元)": investment_buffer,
            "新增产能 (件)": buffer_lines * capacity_per_line,
            "年折旧 (万元)": f"{annual_depreciation_buffer:.2f}",
            "产能缺口 (件)": 0,
            "机会成本 (万元)": 0,
            "净影响 (万元)": f"-{annual_depreciation_buffer:.2f}"
        })

df_investment = pd.DataFrame(investment_options)
st.dataframe(df_investment, use_container_width=True, hide_index=True)

# 投资回收期计算
if capacity_shortage > 0:
    lines_needed = (capacity_shortage // capacity_per_line) + 1
    investment = lines_needed * new_line_cost
    avoided_loss = capacity_shortage * 0.15  # 避免的机会损失
    payback_period = investment / avoided_loss if avoided_loss > 0 else float('inf')
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            label="投资回收期 (年)",
            value=f"{payback_period:.1f}年" if payback_period < 10 else "不划算",
            delta="推荐" if payback_period < 3 else "谨慎"
        )
    
    with col2:
        roi = avoided_loss / investment * 100 if investment > 0 else 0
        st.metric(
            label="投资回报率",
            value=f"{roi:.1f}%",
            delta="优秀" if roi > 25 else "一般"
        )

st.divider()

st.subheader("📈 产能规划情景模拟")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**需求增长情景**")
    
    growth_rates = [0, 10, 20, 30, 40, 50]
    scenario_data = []
    
    for growth in growth_rates:
        new_demand = annual_demand * (1 + growth/100)
        new_util = new_demand / (total_capacity * 4) * 100
        if new_util > 100:
            lines_to_add = int((new_demand/4) / capacity_per_line - product_lines) + 1
            investment_needed = lines_to_add * new_line_cost
        else:
            lines_to_add = 0
            investment_needed = 0
        
        scenario_data.append({
            "需求增长": f"+{growth}%",
            "新利用率": f"{new_util:.0f}%",
            "需扩产": f"{lines_to_add}条线" if lines_to_add > 0 else "无需",
            "投资额": f"{investment_needed}万元" if investment_needed > 0 else "-"
        })
    
    df_scenarios = pd.DataFrame(scenario_data)
    st.dataframe(df_scenarios, use_container_width=True, hide_index=True)

with col2:
    st.markdown("**单位成本分析**")
    
    fixed_cost = product_lines * 50  # 假设每条线固定成本 50 万元/年
    
    utilization_levels = [50, 60, 70, 80, 90, 100]
    unit_cost_data = []
    
    for util in utilization_levels:
        actual_output = total_capacity * 4 * util / 100
        unit_fixed_cost = fixed_cost / actual_output if actual_output > 0 else 0
        unit_cost = unit_fixed_cost + 0.5  # 假设单位变动成本 0.5 万元
        
        unit_cost_data.append({
            "利用率": f"{util}%",
            "单位固定成本": f"{unit_fixed_cost:.3f}万元",
            "单位总成本": f"{unit_cost:.3f}万元"
        })
    
    df_unit_cost = pd.DataFrame(unit_cost_data)
    st.dataframe(df_unit_cost, use_container_width=True, hide_index=True)

st.divider()

st.subheader("⚠️ 决策注意事项")

st.markdown("""
**产能投资决策要点**：

1. **投资建设周期**：新生产线通常需要 1-2 个季度才能投产，需提前规划
2. **折旧影响**：投资会增加年度折旧，直接影响净利润和 ROE
3. **残值回收**：生产线出售可回收部分资金，但通常有较大折损
4. **需求预测**：基于历史数据和市场趋势做出准确预测
5. **柔性产能**：考虑保留一定的产能弹性应对市场波动

**关键指标参考**：
- 最优产能利用率：**85%-95%**
- 投资回收期：< **3 年** 为优，> **5 年** 需谨慎
- 产能弹性缓冲：**10%-15%** 为宜
""")
