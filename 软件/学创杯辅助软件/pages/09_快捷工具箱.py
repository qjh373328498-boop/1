# 🧰 快捷工具箱
# 快速计算常用指标和快捷功能

import streamlit as st
import pandas as pd
from datetime import datetime


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

st.set_page_config(page_title="快捷工具箱", page_icon="🧰", layout="wide")

st.title("🧰 快捷工具箱")
st.markdown("**快速获取常用计算结果，提升决策效率**")

st.divider()

# 标签页布局
tabs = st.tabs(["📐 快速计算器", "📊 批量计算", "⏱️ 比赛计时器", "📋 决策检查清单"])

with tabs[0]:
    st.subheader("📐 快速计算器")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**💹 本量利分析**")
        
        sell_price = st.number_input("单价 (万元)", min_value=0.01, value=2.0, step=0.1, key="calc_price")
        unit_cost = st.number_input("单位变动成本 (万元)", min_value=0.01, value=1.2, step=0.1, key="calc_cost")
        fixed_cost = st.number_input("固定成本 (万元)", min_value=0.0, value=100.0, step=10.0, key="calc_fixed")
        
        if sell_price > unit_cost:
            unit_contribution = sell_price - unit_cost
            contribution_rate = unit_contribution / sell_price * 100
            break_even_volume = fixed_cost / unit_contribution
            break_even_revenue = break_even_volume * sell_price
            
            st.success(f"""
            **单位边际贡献**: {unit_contribution:.2f}万元
            **边际贡献率**: {contribution_rate:.1f}%
            **保本销量**: {break_even_volume:.0f}件
            **保本收入**: {break_even_revenue:.1f}万元
            """)
        else:
            st.error("单价必须高于单位变动成本！")
    
    with col2:
        st.markdown("**📊 定价计算**")
        
        cost_base = st.number_input("成本基数 (万元)", min_value=0.01, value=1.5, step=0.1, key="price_cost")
        markup_method = st.selectbox("定价方法", ["成本加成", "目标 ROI", "竞争导向"])
        
        if markup_method == "成本加成":
            markup_rate = st.slider("加成率 (%)", 0, 100, 20, key="markup")
            target_price = cost_base * (1 + markup_rate / 100)
            profit_margin = markup_rate / (100 + markup_rate) * 100
            
        elif markup_method == "目标 ROI":
            target_roi = st.slider("目标 ROI (%)", 0, 100, 25, key="roi")
            target_price = cost_base * (1 + target_roi / 100)
            profit_margin = target_roi / (100 + target_roi) * 100
            
        else:  # 竞争导向
            competitor_price = st.number_input("竞争对手价格 (万元)", min_value=0.01, value=2.0, step=0.1, key="comp_price")
            strategy = st.selectbox("竞争策略", ["低于对手", "持平", "高于对手"])
            
            if strategy == "低于对手":
                discount = st.slider("折扣率 (%)", 0, 30, 10, key="discount")
                target_price = competitor_price * (1 - discount / 100)
            elif strategy == "持平":
                target_price = competitor_price
            else:
                premium = st.slider("溢价率 (%)", 0, 50, 10, key="premium")
                target_price = competitor_price * (1 + premium / 100)
            
            profit_margin = (target_price - cost_base) / target_price * 100
        
        st.info(f"""
        **建议售价**: {target_price:.2f}万元
        **利润率**: {profit_margin:.1f}%
        **单位利润**: {target_price - cost_base:.2f}万元
        """)
    
    st.divider()
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("**💰 货币时间价值**")
        
        pv = st.number_input("现值 (万元)", min_value=0.01, value=100.0, step=10.0, key="pv")
        rate = st.number_input("年利率 (%)", min_value=0.01, value=5.0, step=0.5, key="rate")
        periods = st.number_input("期数 (年)", min_value=1, max_value=50, value=5, step=1, key="periods")
        
        fv = pv * (1 + rate / 100) ** periods
        total_interest = fv - pv
        
        st.write(f"""
        **终值**: {fv:.2f}万元
        **利息总额**: {total_interest:.2f}万元
        """)
    
    with col4:
        st.markdown("**📉 折旧计算**")
        
        asset_cost = st.number_input("资产原值 (万元)", min_value=1.0, value=150.0, step=10.0, key="asset_cost")
        salvage_rate = st.slider("残值率 (%)", 0, 20, 10, key="salvage")
        useful_life = st.number_input("使用年限", min_value=1, max_value=30, value=5, step=1, key="life")
        
        salvage_value = asset_cost * salvage_rate / 100
        annual_depreciation = (asset_cost - salvage_value) / useful_life
        monthly_depreciation = annual_depreciation / 12
        
        st.write(f"""
        **残值**: {salvage_value:.1f}万元
        **年折旧额**: {annual_depreciation:.2f}万元
        **月折旧额**: {monthly_depreciation:.2f}万元
        """)
    
    st.divider()
    
    col5, col6 = st.columns(2)
    
    with col5:
        st.markdown("**🔄 财务比率速算**")
        
        current_assets = st.number_input("流动资产 (万元)", min_value=0.0, value=500.0, step=50.0, key="ca")
        current_liabilities = st.number_input("流动负债 (万元)", min_value=0.01, value=300.0, step=30.0, key="cl")
        
        quick_assets = st.number_input("速动资产 (万元)", min_value=0.0, value=350.0, step=30.0, key="qa")
        inventory = st.number_input("存货 (万元)", min_value=0.0, value=150.0, step=20.0, key="inv")
        
        if current_liabilities > 0:
            current_ratio = current_assets / current_liabilities
            quick_ratio = quick_assets / current_liabilities
            
            st.write(f"""
            **流动比率**: {current_ratio:.2f} {'✅' if current_ratio >= 1.2 else '⚠️' if current_ratio >= 1.0 else '❌'}
            **速动比率**: {quick_ratio:.2f} {'✅' if quick_ratio >= 0.8 else '⚠️' if quick_ratio >= 0.6 else '❌'}
            """)
    
    with col6:
        st.markdown("**📊 盈利能力速算**")
        
        revenue = st.number_input("营业收入 (万元)", min_value=0.0, value=1000.0, step=100.0, key="rev")
        cost = st.number_input("营业成本 (万元)", min_value=0.0, value=700.0, step=50.0, key="cost")
        net_profit = st.number_input("净利润 (万元)", min_value=-500.0, value=150.0, step=20.0, key="net")
        
        if revenue > 0:
            gross_profit_rate = (revenue - cost) / revenue * 100
            net_profit_margin = net_profit / revenue * 100
            
            st.write(f"""
            **毛利率**: {gross_profit_rate:.1f}%
            **净利率**: {net_profit_margin:.1f}%
            """)

with tabs[1]:
    st.subheader("📊 批量计算")
    
    st.markdown("**📋 多方案对比计算**")
    
    # 创建对比表格
    num_plans = st.number_input("方案数量", min_value=2, max_value=6, value=3, step=1)
    
    cols = st.columns(num_plans)
    plans = []
    
    for i in range(num_plans):
        with cols[i]:
            st.markdown(f"**方案{i+1}**")
            name = st.text_input(f"方案{i+1}名称", value=f"方案{i+1}", key=f"plan_name_{i}")
            sales = st.number_input(f"销售收入", min_value=0.0, value=1000.0 * (i+1) * 0.8, step=100.0, key=f"plan_sales_{i}")
            costs = st.number_input(f"总成本", min_value=0.0, value=800.0 * (i+1) * 0.8, step=50.0, key=f"plan_cost_{i}")
            investment = st.number_input(f"投资额", min_value=0.0, value=500.0, step=50.0, key=f"plan_invest_{i}")
            
            profit = sales - costs
            roi = profit / investment * 100 if investment > 0 else 0
            
            plans.append({
                "方案": name,
                "销售收入": sales,
                "总成本": costs,
                "利润": profit,
                "投资额": investment,
                "ROI": f"{roi:.1f}%"
            })
    
    df_plans = pd.DataFrame(plans)
    st.dataframe(df_plans, use_container_width=True, hide_index=True)
    
    # 推荐最佳方案
    best_plan = max(plans, key=lambda x: float(x["ROI"].replace("%", "")))
    st.success(f"🏆 **推荐**: {best_plan['方案']} (ROI: {best_plan['ROI']})")
    
    st.divider()
    
    st.markdown("**📈 敏感性分析**")
    
    base_sales = st.number_input("基准销售收入 (万元)", min_value=0.0, value=1000.0, step=100.0, key="sens_base")
    base_cost = st.number_input("基准总成本 (万元)", min_value=0.0, value=750.0, step=50.0, key="sens_base_cost")
    
    change_rates = [-20, -10, 0, 10, 20]
    sensitivity_data = []
    
    for change in change_rates:
        sales_adjusted = base_sales * (1 + change / 100)
        profit = sales_adjusted - base_cost
        profit_change = (profit - (base_sales - base_cost)) / (base_sales - base_cost) * 100 if base_sales != base_cost else 0
        
        sensitivity_data.append({
            "收入变化": f"{change:+.0f}%",
            "调整后收入": f"{sales_adjusted:.1f}万元",
            "利润": f"{profit:.1f}万元",
            "利润变化": f"{profit_change:+.1f}%"
        })
    
    df_sensitivity = pd.DataFrame(sensitivity_data)
    st.dataframe(df_sensitivity, use_container_width=True, hide_index=True)

with tabs[2]:
    st.subheader("⏱️ 比赛计时器")
    
    st.markdown("**📅 倒计时管理**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        total_minutes = st.number_input("比赛总时长 (分钟)", min_value=1, max_value=180, value=60, step=5)
        
        if st.button("🚀 开始计时", type="primary", use_container_width=True):
            st.session_state.start_time = datetime.now()
            st.session_state.total_minutes = total_minutes
            st.session_state.timer_running = True
            st.rerun()
    
    with col2:
        if st.button("⏹️ 重置", use_container_width=True):
            st.session_state.timer_running = False
            st.session_state.start_time = None
            st.rerun()
    
    if st.session_state.get("timer_running", False) and st.session_state.get("start_time"):
        import time
        from datetime import timedelta
        
        start = st.session_state.start_time
        total = st.session_state.total_minutes
        
        elapsed = datetime.now() - start
        elapsed_minutes = elapsed.total_seconds() / 60
        remaining = max(0, total - elapsed_minutes)
        
        hours = int(remaining // 60)
        minutes = int(remaining % 60)
        seconds = int((remaining % 1) * 60)
        
        progress = min(100, elapsed_minutes / total * 100)
        
        # 显示倒计时
        if remaining <= 5:
            st.error(f"## ⚠️ 剩余时间：{hours:02d}:{minutes:02d}:{seconds:02d}")
        elif remaining <= 15:
            st.warning(f"## ⏰ 剩余时间：{hours:02d}:{minutes:02d}:{seconds:02d}")
        else:
            st.success(f"## ⏱️ 剩余时间：{hours:02d}:{minutes:02d}:{seconds:02d}")
        
        st.progress(progress / 100)
        
        # 时间分配建议
        st.markdown("**📋 时间分配建议**")
        
        quarters_time = total / 4
        
        col_q1, col_q2, col_q3, col_q4 = st.columns(4)
        
        with col_q1:
            st.info(f"**Q1**\n\n{quarters_time:.0f}分钟\n\n市场开拓")
        
        with col_q2:
            st.info(f"**Q2**\n\n{quarters_time:.0f}分钟\n\n稳定经营")
        
        with col_q3:
            st.info(f"**Q3**\n\n{quarters_time:.0f}分钟\n\n扩张发展")
        
        with col_q4:
            st.info(f"**Q4**\n\n{quarters_time:.0f}分钟\n\n冲刺利润")
        
        st.rerun()
    
    st.divider()
    
    st.markdown("**📋 季度时间分配**")
    
    decision_phases = {
        "数据分析": "15%",
        "方案制定": "25%",
        "决策录入": "20%",
        "结果分析": "15%",
        "调整优化": "25%"
    }
    
    for phase, time_alloc in decision_phases.items():
        st.write(f"- **{phase}**: {time_alloc}")

with tabs[3]:
    st.subheader("📋 决策检查清单")
    
    st.markdown("**✅ 季度决策检查清单**")
    
    st.markdown("### 🎯 季度初检查")
    
    checklist_start = {
        "现金流预测已完成": False,
        "期末现金≥安全线": False,
        "贷款额度已规划": False,
        "产能充足性确认": False,
        "市场策略已制定": False
    }
    
    for item in checklist_start:
        st.checkbox(item, key=f"start_{item}")
    
    st.markdown("### 💰 竞标前检查")
    
    checklist_bid = {
        "产品成本已计算": False,
        "竞争对手分析完成": False,
        "报价策略已确定": False,
        "广告投入已规划": False,
        "中标率预估>70%": False
    }
    
    for item in checklist_bid:
        st.checkbox(item, key=f"bid_{item}")
    
    st.markdown("### 📊 季度末检查")
    
    checklist_end = {
        "财务报表已生成": False,
        "财务比率已计算": False,
        "得分已估算": False,
        "预算偏差<10%": False,
        "无违规扣分项": False
    }
    
    for item in checklist_end:
        st.checkbox(item, key=f"end_{item}")
    
    st.divider()
    
    st.markdown("**⚠️ 红线检查**")
    
    red_lines = {
        "❌ 紧急借款": "确保期末现金>0",
        "❌ 现金断流": "保持现金≥固定支出×1.2",
        "❌ 逾期报税": "按时完成税务申报"
    }
    
    for line, note in red_lines.items():
        col1, col2 = st.columns([3, 2])
        with col1:
            st.warning(line)
        with col2:
            st.info(note)
    
    st.divider()
    
    st.markdown("**📝 复盘检查**")
    
    checklist_review = {
        "决策数据已记录": False,
        "得分已分析": False,
        "经验已总结": False,
        "改进计划已制定": False
    }
    
    for item in checklist_review:
        st.checkbox(item, key=f"review_{item}")
    
    # 完成度统计
    total_checks = len(checklist_start) + len(checklist_bid) + len(checklist_end) + len(checklist_review)
    completed = sum(1 for k in st.session_state if k.startswith(('start_', 'bid_', 'end_', 'review_')) and st.session_state.get(k, False))
    
    st.progress(completed / total_checks)
    st.write(f"检查完成度：{completed}/{total_checks} ({completed/total_checks*100:.0f}%)")
