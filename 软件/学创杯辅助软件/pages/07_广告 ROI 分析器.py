# 📈 广告 ROI 分析器
# 优化广告投放效率，提升中标率

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

st.set_page_config(page_title="广告 ROI 分析器", page_icon="📈", layout="wide")

st.title("📈 广告 ROI 分析器")
st.markdown("**优化广告投放策略，提升投入产出比， maximize 中标率**")


# ========== 性能优化：缓存图表和计算 ==========
@st.cache_data
def calculate_roi_scenarios(params):
    """缓存 ROI 方案计算"""
    results = []
    for ad_multiplier in [0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0]:
        ad_spend = params['avg_competitor_ad'] * ad_multiplier
        estimated_share = (ad_spend / (ad_spend + (params['num_competitors'] - 1) * params['avg_competitor_ad'])) * 0.8 + (1/params['num_competitors']) * 0.2
        if ad_multiplier > 1.5:
            estimated_share *= 0.9
        elif ad_multiplier > 1.25:
            estimated_share *= 0.95
        
        estimated_orders = min(int(params['total_market_size'] * estimated_share), params['capacity'])
        revenue = estimated_orders * params['product_price']
        gross_profit = estimated_orders * (params['product_price'] - params['product_cost'])
        net_profit = gross_profit - ad_spend
        roi = (net_profit / ad_spend * 100) if ad_spend > 0 else 0
        
        results.append({
            "投入档次": ad_multiplier,
            "广告投入": ad_spend,
            "预估份额": estimated_share,
            "预计订单": estimated_orders,
            "毛利润": gross_profit,
            "净利润": net_profit,
            "ROI": roi
        })
    return results

st.divider()

# 侧边栏输入
with st.sidebar:
    st.header("📋 市场数据")
    
    st.subheader("本市场情况")
    total_market_size = st.number_input("市场总容量 (件)", min_value=1000, max_value=100000, value=20000, step=1000)
    num_competitors = st.number_input("竞争对手数量", min_value=1, max_value=20, value=8, step=1)
    avg_competitor_ad = st.number_input("对手平均广告投入 (万元)", min_value=5, max_value=200, value=50, step=10)
    
    st.subheader("产品信息")
    product_cost = st.number_input("单位产品成本 (万元)", min_value=0.1, max_value=10.0, value=1.5, step=0.1)
    product_price = st.number_input("单位产品售价 (万元)", min_value=0.1, max_value=15.0, value=2.0, step=0.1)
    capacity = st.number_input("本季度产能 (件)", min_value=100, max_value=50000, value=8000, step=500)
    
    st.subheader("历史数据")
    last_ad_spend = st.number_input("上季度广告投入 (万元)", min_value=0.0, max_value=500.0, value=40.0, step=10.0)
    last_market_share = st.number_input("上季度市场份额 (%)", min_value=0.0, max_value=100.0, value=12.5, step=2.5)

# 计算单位毛利
unit_margin = product_price - product_cost
margin_rate = unit_margin / product_price if product_price > 0 else 0

st.divider()

st.subheader("💰 广告投放方案对比")

# 生成不同广告投入方案
ad_scenarios = []

def get_tier(multiplier):
    if multiplier < 0.75:
        return "🐢 保守"
    elif multiplier < 1.0:
        return "🚶 稳健"
    elif multiplier < 1.25:
        return "🏃 积极"
    elif multiplier < 1.5:
        return "🚀 激进"
    else:
        return "🔥 疯狂"

def get_recommendation(roi, multiplier):
    if roi > 200:
        return "⭐⭐⭐⭐⭐"
    elif roi > 150:
        return "⭐⭐⭐⭐"
    elif roi > 100:
        return "⭐⭐⭐"
    elif roi > 50:
        return "⭐⭐"
    else:
        return "⭐"

def get_comprehensive_recommendation(best, high_roi, margin):
    if margin > 0.4:
        return f"当前毛利率{margin:.0%}较高，建议采用**{best['投入档次']}**策略，投入**{best['广告投入 (万元)']:.1f}万元**，最大化市场份额和利润。"
    elif margin > 0.25:
        return f"当前毛利率{margin:.0%}中等，建议采用**{high_roi['投入档次']}**策略，投入**{high_roi['广告投入 (万元)']:.1f}万元**，平衡 ROI 和利润。"
    else:
        return f"当前毛利率{margin:.0%}较低，建议**控制广告投入**，优先采用**{high_roi['投入档次']}**策略，投入**{high_roi['广告投入 (万元)']:.1f}万元**，避免亏损。"

# 生成不同广告投入方案
ad_scenarios = []

for ad_multiplier in [0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0]:
    ad_spend = avg_competitor_ad * ad_multiplier
    
    # 估算市场份额（简化模型：与广告投入成正比，但边际效应递减）
    total_ad_spend = ad_spend + (num_competitors - 1) * avg_competitor_ad
    estimated_share = (ad_spend / total_ad_spend) * 0.8 + (1/num_competitors) * 0.2  # 80% 广告效应 + 20% 基础份额
    
    # 考虑广告效应的边际递减
    if ad_multiplier > 1.5:
        estimated_share *= 0.9
    elif ad_multiplier > 1.25:
        estimated_share *= 0.95
    
    estimated_orders = min(int(total_market_size * estimated_share), capacity)
    revenue = estimated_orders * product_price
    gross_profit = estimated_orders * unit_margin
    net_profit = gross_profit - ad_spend
    roi = (net_profit / ad_spend * 100) if ad_spend > 0 else 0
    
    ad_scenarios.append({
        "投入档次": get_tier(ad_multiplier),
        "广告投入 (万元)": ad_spend,
        "预估份额": f"{estimated_share:.1%}",
        "预计订单 (件)": estimated_orders,
        "毛利润 (万元)": gross_profit,
        "净利润 (万元)": net_profit,
        "ROI": f"{roi:.0f}%",
        "推荐指数": get_recommendation(roi, ad_multiplier)
    })

df_scenarios = pd.DataFrame(ad_scenarios)
st.dataframe(
    df_scenarios,
    use_container_width=True,
    hide_index=True,
    column_config={
        "投入档次": st.column_config.TextColumn(width="small"),
        "广告投入 (万元)": st.column_config.NumberColumn(format="%.1f"),
        "预估份额": st.column_config.TextColumn(width="small"),
        "预计订单 (件)": st.column_config.NumberColumn(format="%d"),
        "毛利润 (万元)": st.column_config.NumberColumn(format="%.1f"),
        "净利润 (万元)": st.column_config.NumberColumn(format="%.1f"),
        "ROI": st.column_config.TextColumn(width="small"),
        "推荐指数": st.column_config.TextColumn(width="small")
    }
)

st.divider()

st.subheader("📊 ROI 趋势分析")

col1, col2 = st.columns(2)

with col1:
    # ROI 曲线图
    fig_roi = go.Figure()
    
    fig_roi.add_trace(go.Scatter(
        x=df_scenarios["广告投入 (万元)"],
        y=[float(r.replace("%", "")) for r in df_scenarios["ROI"]],
        mode="lines+markers",
        name="ROI",
        line=dict(color="green", width=3),
        marker=dict(size=10)
    ))
    
    fig_roi.add_hline(
        y=100,
        line_dash="dash",
        line_color="orange",
        annotation_text="ROI=100% (盈亏平衡点 2 倍)",
        annotation_position="right"
    )
    
    fig_roi.update_layout(
        title="广告投入 ROI 趋势",
        xaxis_title="广告投入 (万元)",
        yaxis_title="ROI (%)",
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig_roi, use_container_width=True)

with col2:
    # 利润曲线图
    fig_profit = go.Figure()
    
    fig_profit.add_trace(go.Bar(
        x=df_scenarios["广告投入 (万元)"],
        y=df_scenarios["净利润 (万元)"],
        marker_color="steelblue",
        name="净利润"
    ))
    
    max_profit_idx = df_scenarios["净利润 (万元)"].idxmax()
    best_ad = df_scenarios.loc[max_profit_idx, "广告投入 (万元)"]
    
    fig_profit.add_vline(
        x=best_ad,
        line_dash="dash",
        line_color="red",
        annotation_text=f"最优投入：{best_ad}万元",
        annotation_position="top"
    )
    
    fig_profit.update_layout(
        title="广告投入与净利润关系",
        xaxis_title="广告投入 (万元)",
        yaxis_title="净利润 (万元)",
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig_profit, use_container_width=True)

st.divider()

# 找出最优方案
best_scenario = df_scenarios.loc[df_scenarios["净利润 (万元)"].idxmax()]
high_roi_scenario = df_scenarios.loc[[float(r.replace("%", "")) for r in df_scenarios["ROI"]].index(max([float(r.replace("%", "")) for r in df_scenarios["ROI"]]))]

st.subheader("🎯 推荐策略")

st.info(f"""
**💡 利润最大化方案**: {best_scenario['投入档次']}

- 广告投入：**{best_scenario['广告投入 (万元)']:.1f}万元**
- 预计订单：**{best_scenario['预计订单 (件)']:,}件**
- 净利润：**{best_scenario['净利润 (万元)']:.1f}万元**
- ROI: **{best_scenario['ROI']}**

**📈 最高 ROI 方案**: {high_roi_scenario['投入档次']}

- 广告投入：**{high_roi_scenario['广告投入 (万元)']:.1f}万元**
- ROI: **{high_roi_scenario['ROI']}**
- 净利润：**{high_roi_scenario['净利润 (万元)']:.1f}万元**

**🏆 综合建议**：
{get_comprehensive_recommendation(best_scenario, high_roi_scenario, margin_rate)}
""")

st.divider()

st.subheader("📋 中标率计算器")

col1, col2, col3 = st.columns(3)

with col1:
    my_bid_ad = st.number_input("我的广告投入 (万元)", min_value=0, max_value=500, value=50, step=10)
    
with col2:
    competitor_avg_ad = st.number_input("对手平均广告 (万元)", min_value=10, max_value=300, value=50, step=10)
    
with col3:
    num_bidders = st.number_input("竞标对手数", min_value=1, max_value=20, value=8, step=1)

# 计算中标率
total_bid = my_bid_ad + (num_bidders - 1) * competitor_avg_ad
win_rate = (my_bid_ad / total_bid) * 100 if total_bid > 0 else 0

# 考虑价格因素
price_factor = st.slider("价格竞争力 (-20% 到 +20%)", min_value=-20, max_value=20, value=0, step=5)
adjusted_win_rate = min(95, max(5, win_rate + price_factor))

st.metric(
    label="预估中标率",
    value=f"{adjusted_win_rate:.1f}%",
    delta=f"价格因素：{price_factor:+.0f}%",
    delta_color="normal" if adjusted_win_rate > 70 else "inverse"
)

# 不同投入的中标率对比
win_rate_scenarios = []
for ad in [20, 40, 60, 80, 100, 120, 140, 160]:
    total = ad + (num_bidders - 1) * competitor_avg_ad
    rate = (ad / total) * 100 if total > 0 else 0
    win_rate_scenarios.append({
        "广告投入": f"{ad}万元",
        "基础中标率": f"{rate:.1f}%",
        "调整后中标率": f"{min(95, max(5, rate + price_factor)):.1f}%"
    })

df_win_rate = pd.DataFrame(win_rate_scenarios)
st.dataframe(df_win_rate, use_container_width=True, hide_index=True)

st.divider()

st.subheader("🎛️ 广告策略模拟器")

# 多季度模拟
st.markdown("**📅 季度广告策略规划**")

quarters = ["Q1", "Q2", "Q3", "Q4"]
ad_allocations = {}

cols = st.columns(4)
for i, quarter in enumerate(quarters):
    with cols[i]:
        st.markdown(f"**{quarter}**")
        ad_allocations[quarter] = st.slider(
            f"{quarter} 广告预算",
            min_value=0,
            max_value=200,
            value=int(last_ad_spend),
            step=10,
            key=f"ad_{quarter}"
        )

total_budget = sum(ad_allocations.values())

st.metric(
    label="年度广告总预算",
    value=f"{total_budget}万元",
    delta=f"季度平均：{total_budget/4:.1f}万元"
)

# 可视化分配
fig_pie = go.Figure(data=[go.Pie(
    labels=quarters,
    values=list(ad_allocations.values()),
    hole=0.3
)])

fig_pie.update_layout(
    title="季度广告预算分配",
    height=400
)

st.plotly_chart(fig_pie, use_container_width=True)

# 季度策略建议
st.markdown("**📋 季度策略建议**")

seasonal_strategies = {
    "Q1": "🌱 **市场开拓期** - 高投入抢占市场，建议 10-12% 销售额",
    "Q2": "📈 **稳定发展期** - 维持份额，优化 ROI，建议 5-7% 销售额",
    "Q3": "🚀 **快速扩张期** - 精准投放高 ROI 市场，建议 7-9% 销售额",
    "Q4": "💰 **利润收割期** - 控制成本，保利润，建议 3-5% 销售额"
}

for quarter, strategy in seasonal_strategies.items():
    st.markdown(f"- {strategy}")

st.divider()

st.subheader("⚠️ 广告投放注意事项")

st.markdown("""
**关键决策点**：

1. **边际效应递减**：广告投入超过一定阈值后，效果增幅会显著下降
2. **竞争博弈**：需根据对手策略动态调整，避免被碾压或过度竞争
3. **产能匹配**：广告带来订单不能超过产能，否则影响交付和信誉
4. **现金流**：广告费当期支付，确保现金充足
5. **产品生命周期**：
   - 新品上市：高投入快速占领市场
   - 成熟产品：维持性投入，追求 ROI
   - 衰退产品：减少投入，准备退出

**优化技巧**：
- 关注广告投入占销售额比例（通常 5%-12%）
- 季度间预算分配要符合市场节奏
- 高毛利产品可承受更高广告投入
- 避免与对手恶性竞争，寻找市场空白点
""")
