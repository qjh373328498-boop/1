"""
学创杯比赛辅助工具 - 报价策略计算器
"""
import streamlit as st
import pandas as pd

st.set_page_config(page_title="报价策略计算器", page_icon="🏷️", layout="wide")

st.title("🏷️ 报价策略计算器")
st.markdown("**用途**: 根据成本和市场策略，计算最优报价，平衡利润与市场份额")

# 侧边栏
st.sidebar.header("🎯 策略选择")
strategy = st.sidebar.selectbox(
    "市场策略",
    ["激进抢市场 (Q1)", "稳健经营 (Q2-Q3)", "利润导向 (Q4)"],
    index=1
)

st.sidebar.info("""
**分季度策略建议**:
- Q1: 0.85-0.90x (抢占市场)
- Q2: 0.95-1.00x (稳定经营)
- Q3: 0.95-1.05x (灵活调整)
- Q4: 1.05-1.10x (冲刺利润)
""")

# 成本输入
st.subheader("📋 成本构成")

col1, col2, col3 = st.columns(3)

with col1:
    material_cost = st.number_input("单位材料成本", min_value=0.0, value=30.0, step=1.0)
    labor_cost = st.number_input("单位人工成本", min_value=0.0, value=20.0, step=1.0)

with col2:
    manufacturing_expense = st.number_input("单位制造费用", min_value=0.0, value=10.0, step=1.0)
    other_cost = st.number_input("其他单位成本", min_value=0.0, value=0.0, step=0.5)

with col3:
    unit_cost = material_cost + labor_cost + manufacturing_expense + other_cost
    st.metric("单位产品成本合计", f"{unit_cost:.2f}元")

# 利润率设置
st.divider()
st.subheader("💰 定价策略")

if strategy == "激进抢市场 (Q1)":
    default_margin = -10
    margin_range = (-20, 0)
elif strategy == "稳健经营 (Q2-Q3)":
    default_margin = 5
    margin_range = (-5, 15)
else:
    default_margin = 15
    margin_range = (5, 25)

target_margin = st.slider("目标毛利率 (%)", margin_range[0], margin_range[1], default_margin)

# 报价计算
markup_price = unit_cost * (1 + target_margin / 100)
market_price_q1 = unit_cost * 0.88
market_price_q2 = unit_cost * 0.98
profit_price_q4 = unit_cost * 1.08

st.divider()
st.subheader("💡 报价方案对比")

col1, col2, col3, col4 = st.columns(4)

col1.metric("成本价", f"{unit_cost:.2f}元", "零利润")
col2.metric("抢市场价", f"{market_price_q1:.2f}元", f"{-12:.1f}% 利润率", delta_color="inverse")
col3.metric("正常价", f"{market_price_q2:.2f}元", f"{-2:.1f}% 利润率", delta_color="inverse")
col4.metric("利润价", f"{profit_price_q4:.2f}元", f"{8:.1f}% 利润率")

st.divider()

# 当前方案详情
st.subheader("📊 当前报价方案详情")

selling_price = unit_cost * (1 + target_margin / 100)
gross_profit = selling_price - unit_cost
gross_margin = (gross_profit / selling_price * 100) if selling_price > 0 else 0

col1, col2, col3 = st.columns(3)

col1.metric("建议报价", f"{selling_price:.2f}元/件")
col2.metric("单位毛利润", f"{gross_profit:.2f}元")
col3.metric("毛利率", f"{gross_margin:.1f}%")

# 敏感性分析
st.divider()
st.subheader("📈 敏感性分析")

st.markdown("不同报价下的利润情况:")

prices = [
    ("超低价", unit_cost * 0.85),
    ("低价", unit_cost * 0.90),
    ("中低价", unit_cost * 0.95),
    ("正常价", unit_cost * 1.00),
    ("中高價", unit_cost * 1.05),
    ("高价", unit_cost * 1.10),
    ("超高价", unit_cost * 1.15)
]

data = []
for name, price in prices:
    profit = price - unit_cost
    margin = (profit / price * 100) if price > 0 else 0
    data.append({
        '定价策略': name,
        '报价 (元)': round(price, 2),
        '单位利润 (元)': round(profit, 2),
        '毛利率 (%)': round(margin, 1)
    })

df = pd.DataFrame(data)
st.dataframe(df, use_container_width=True, hide_index=True)

# 竞争对手分析
st.divider()
st.subheader("⚔️ 竞争策略建议")

st.info("""
**价格战应对策略**:

1. **对手低价 < 成本价**:
   - 方案 A: 跟随降价，但控制接单量
   - 方案 B: 差异化竞争，专注高利润市场 (推荐)
   - 方案 C: 战略撤退，保存实力

2. **招标竞价技巧**:
   - 第一轮：中高价位试探
   - 第二轮：根据对手调整
   - 第三轮：决定是否跟进

3. **报价心理战术**:
   - 尾数定价：99.8 元 vs 100 元
   - 阶梯报价：量大从优
   - 锚定效应：先报高价再优惠
""")

# 快捷计算
st.divider()
st.subheader("🔢 快捷计算工具")

calc_type = st.selectbox("选择计算器", [
    "目标利润倒推报价",
    "盈亏平衡点计算",
    "竞品价格对比"
])

if calc_type == "目标利润倒推报价":
    st.markdown("已知目标利润率，倒推报价")
    
    cost_input = st.number_input("单位成本", min_value=0.0, value=unit_cost)
    target_profit_margin = st.number_input("目标利润率 (%)", min_value=-20, max_value=50, value=10)
    
    # 报价 = 成本 / (1 - 利润率)
    price = cost_input / (1 - target_profit_margin / 100)
    
    st.metric("建议报价", f"{price:.2f}元")

elif calc_type == "盈亏平衡点计算":
    st.markdown("计算盈亏平衡销量")
    
    fixed_cost = st.number_input("固定成本", min_value=0.0, value=100.0)
    unit_price_calc = st.number_input("销售单价", min_value=0.0, value=selling_price)
    unit_variable_cost = st.number_input("单位变动成本", min_value=0.0, value=unit_cost)
    
    contribution_margin = unit_price_calc - unit_variable_cost
    break_even = fixed_cost / contribution_margin if contribution_margin > 0 else 0
    
    st.metric("盈亏平衡销量", f"{break_even:.0f}件")
    
    if break_even > 0:
        st.info(f"需要销售 **{break_even:.0f}件** 才能覆盖固定成本 {fixed_cost:.1f}元")

elif calc_type == "竞品价格对比":
    st.markdown("对比自己与竞争对手的价格")
    
    our_price = st.number_input("我方报价", min_value=0.0, value=selling_price)
    competitor_price = st.number_input("竞争对手报价", min_value=0.0, value=unit_cost * 0.95)
    
    diff = our_price - competitor_price
    diff_pct = (diff / competitor_price * 100) if competitor_price > 0 else 0
    
    if diff > 0:
        st.warning(f"我方价格 **高 {diff:.2f}元** ({diff_pct:.1f}%)")
    elif diff < 0:
        st.info(f"我方价格 **低 {abs(diff):.2f}元** ({abs(diff_pct):.1f}%)")
    else:
        st.success("双方价格持平")
