# 📝 比赛复盘记录表
# 记录决策数据，快速提升比赛水平

import streamlit as st
import pandas as pd
import json
from datetime import datetime
import os

st.set_page_config(page_title="比赛复盘记录表", page_icon="📝", layout="wide")

st.title("📝 比赛复盘记录表")
st.markdown("**记录每轮决策数据，分析得失，快速提升比赛水平**")

st.divider()

# 数据文件路径
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
os.makedirs(DATA_DIR, exist_ok=True)
REVIEW_FILE = os.path.join(DATA_DIR, "review_records.json")

# 加载历史数据
def load_reviews():
    if os.path.exists(REVIEW_FILE):
        with open(REVIEW_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_reviews(data):
    with open(REVIEW_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

reviews_data = load_reviews()

# 侧边栏：操作菜单
with st.sidebar:
    st.header("📋 操作菜单")
    
    mode = st.radio(
        "选择模式",
        ["📝 新建复盘记录", "📊 查看历史记录", "📈 数据分析"],
        index=0
    )
    
    st.divider()
    
    if mode == "📊 查看历史记录":
        if reviews_data:
            st.subheader("历史复盘")
            for i, review in enumerate(reviews_data):
                round_num = review.get("round", "?")
                date = review.get("date", "未知日期")
                score = review.get("final_score", "未知")
                st.write(f"**第{round_num}轮** - {date} (得分：{score})")
                if st.button("删除", key=f"del_{i}"):
                    reviews_data.pop(i)
                    save_reviews(reviews_data)
                    st.rerun()
        else:
            st.info("暂无历史记录")

st.divider()

if mode == "📝 新建复盘记录":
    st.subheader("📋 基本信息")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        round_num = st.number_input("比赛轮次", min_value=1, max_value=100, value=1)
        team_name = st.text_input("队伍名称", value="我的队伍")
    
    with col2:
        date = st.date_input("比赛日期", value=datetime.now())
        duration = st.selectbox("比赛时长", ["30 分钟", "45 分钟", "60 分钟", "90 分钟"])
    
    with col3:
        final_rank = st.number_input("最终排名", min_value=1, max_value=100, value=1)
        total_teams = st.number_input("参赛队伍数", min_value=1, max_value=100, value=16)
    
    st.divider()
    
    st.subheader("📊 四轮经营数据")
    
    quarters_data = {}
    
    for q in [1, 2, 3, 4]:
        with st.expander(f"**第{q}轮 (Q{q})**", expanded=(q==1)):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                q_sales = st.number_input(f"Q{q} 销售收入", min_value=0, key=f"q{q}_sales")
                q_cost = st.number_input(f"Q{q} 直接成本", min_value=0, key=f"q{q}_cost")
                q_gross = q_sales - q_cost
                
            with col2:
                q_ad = st.number_input(f"Q{q} 广告投入", min_value=0, key=f"q{q}_ad")
                q_rd = st.number_input(f"Q{q} 研发投入", min_value=0, key=f"q{q}_rd")
                q_other = st.number_input(f"Q{q} 其他费用", min_value=0, key=f"q{q}_other")
            
            with col3:
                q_loan = st.number_input(f"Q{q} 新增贷款", min_value=0, key=f"q{q}_loan")
                q_invest = st.number_input(f"Q{q} 投资支出", min_value=0, key=f"q{q}_invest")
                q_cash = st.number_input(f"Q{q} 期末现金", min_value=0, key=f"q{q}_cash")
            
            q_net = q_gross - q_ad - q_rd - q_other
            st.info(f"Q{q} 毛利润：{q_gross}万元 | 净利润：{q_net}万元")
            
            quarters_data[f"Q{q}"] = {
                "销售收入": q_sales,
                "直接成本": q_cost,
                "毛利润": q_gross,
                "广告投入": q_ad,
                "研发投入": q_rd,
                "其他费用": q_other,
                "净利润": q_net,
                "新增贷款": q_loan,
                "投资支出": q_invest,
                "期末现金": q_cash
            }
    
    st.divider()
    
    st.subheader("🏆 财务指标得分")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**盈利能力 (30 分)**")
        profit_score = st.slider("净利润率得分", 0, 30, 25, key="score_profit")
        roe_score = st.slider("ROE 得分", 0, 30, 20, key="score_roe")
        profit_total = profit_score + roe_score
        st.write(f"小计：**{profit_total}/60**")
    
    with col2:
        st.markdown("**营运能力 (25 分)**")
        turnover_score = st.slider("总资产周转率得分", 0, 25, 20, key="score_turnover")
        inventory_score = st.slider("存货周转率得分", 0, 25, 18, key="score_inventory")
        operation_total = turnover_score + inventory_score
        st.write(f"小计：**{operation_total}/50**")
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("**偿债能力 (20 分)**")
        current_ratio_score = st.slider("流动比率得分", 0, 20, 16, key="score_current")
        debt_ratio_score = st.slider("资产负债率得分", 0, 20, 15, key="score_debt")
        debt_total = current_ratio_score + debt_ratio_score
        st.write(f"小计：**{debt_total}/40**")
    
    with col4:
        st.markdown("**发展能力 (15 分)**")
        growth_score = st.slider("销售增长率得分", 0, 15, 12, key="score_growth")
        asset_growth_score = st.slider("资产增长率得分", 0, 15, 10, key="score_asset_growth")
        growth_total = growth_score + asset_growth_score
        st.write(f"小计：**{growth_total}/30**")
    
    st.divider()
    
    st.subheader("📋 预算能力 (10 分)")
    
    budget_accuracy = st.slider("预算准确率 (%)", 0, 100, 90)
    if budget_accuracy >= 90:
        budget_score = 10
        budget_msg = "✅ 优秀"
    elif budget_accuracy >= 80:
        budget_score = 8
        budget_msg = "👌 良好"
    elif budget_accuracy >= 70:
        budget_score = 6
        budget_msg = "👍 合格"
    else:
        budget_score = 4
        budget_msg = "⚠️ 需改进"
    
    st.write(f"预算得分：**{budget_score}/10** ({budget_msg})")
    
    st.divider()
    
    st.subheader("⚠️ 违规扣分")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        emergency_loans = st.number_input("紧急借款次数", min_value=0, max_value=10, value=0)
        emergency_penalty = emergency_loans * 5
    
    with col2:
        tax_violations = st.number_input("逾期报税次数", min_value=0, max_value=10, value=0)
        tax_penalty = tax_violations * 5
    
    with col3:
        cash_shortage = st.number_input("现金断流次数", min_value=0, max_value=10, value=0)
        cash_penalty = cash_shortage * 10
    
    total_penalty = emergency_penalty + tax_penalty + cash_penalty
    
    st.error(f"**违规扣分总计：-{total_penalty}分**")
    if total_penalty > 0:
        st.write(f"- 紧急借款：-{emergency_penalty}分")
        st.write(f"- 逾期报税：-{tax_penalty}分")
        st.write(f"- 现金断流：-{cash_penalty}分")
    
    st.divider()
    
    # 计算总分
    final_score = profit_total + operation_total + debt_total + growth_total + budget_score - total_penalty
    max_score = 60 + 50 + 40 + 30 + 10  # 190 分
    
    st.subheader("🏆 最终成绩")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("最终得分", f"{final_score}分", 
                  delta=f"满分{max_score}分",
                  delta_color="normal" if final_score >= 85 else "inverse")
    
    with col2:
        achievement = get_achievement_level(final_score)
        st.metric("获奖等级", achievement, 
                  delta="🎯 目标达成" if final_score >= 85 else "继续努力")
    
    with col3:
        percentile = (1 - (final_rank - 1) / total_teams) * 100 if total_teams > 0 else 0
        st.metric("排名百分位", f"{percentile:.1f}%", 
                  delta=f"{final_rank}/{total_teams}名")
    
    def get_achievement_level(score):
        if score >= 95:
            return "🥇 特等奖"
        elif score >= 85:
            return "🥇 一等奖"
        elif score >= 70:
            return "🥈 二等奖"
        elif score >= 60:
            return "🥉 三等奖"
        else:
            return "🏅 参与奖"
    
    st.divider()
    
    st.subheader("📝 复盘总结")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**✅ 做得好的地方**")
        good_points = st.text_area(
            "总结成功经验",
            placeholder="例如：\n- 现金流管理到位，零紧急借款\n- Q2 广告投入精准，中标率 85%\n- 预算准确率达 92%",
            height=150
        )
    
    with col2:
        st.markdown("**❌ 需要改进的地方**")
        bad_points = st.text_area(
            "总结失败教训",
            placeholder="例如：\n- Q3 产能规划失误，损失订单\n- 定价过于保守，毛利偏低\n- 贷款时机不对，利息偏高",
            height=150
        )
    
    st.markdown("**💡 下轮改进计划**")
    action_items = st.text_area(
        "制定具体行动计划",
        placeholder="例如：\n1. 建立现金流预测模型，每季度初测算\n2. 研究竞争对手定价策略，动态调整\n3. 提前 2 季度规划产能投资",
        height=100
    )
    
    st.divider()
    
    # 保存按钮
    if st.button("💾 保存复盘记录", type="primary", use_container_width=True):
        review_record = {
            "round": round_num,
            "team_name": team_name,
            "date": str(date),
            "duration": duration,
            "final_rank": final_rank,
            "total_teams": total_teams,
            "quarters_data": quarters_data,
            "scores": {
                "profit": profit_total,
                "operation": operation_total,
                "debt": debt_total,
                "growth": growth_total,
                "budget": budget_score,
                "penalty": total_penalty
            },
            "final_score": final_score,
            "achievement": get_achievement_level(final_score),
            "summary": {
                "good_points": good_points,
                "bad_points": bad_points,
                "action_items": action_items
            }
        }
        
        reviews_data.append(review_record)
        save_reviews(reviews_data)
        
        st.success("✅ 复盘记录已保存！")
        st.balloons()

elif mode == "📊 查看历史记录":
    if not reviews_data:
        st.info("暂无历史记录，请先创建复盘记录")
    else:
        # 显示最新记录
        latest = reviews_data[-1]
        
        st.subheader(f"📊 第{latest['round']}轮复盘 - {latest['date']}")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("最终得分", f"{latest['final_score']}分")
        
        with col2:
            st.metric("获奖等级", latest['achievement'])
        
        with col3:
            st.metric("排名", f"{latest['final_rank']}/{latest['total_teams']}")
        
        with col4:
            penalty = latest['scores']['penalty']
            st.metric("违规扣分", f"-{penalty}分")
        
        st.divider()
        
        # 得分详情
        st.markdown("**📋 得分详情**")
        
        scores = latest['scores']
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("盈利能力", f"{scores['profit']}分")
        
        with col2:
            st.metric("营运能力", f"{scores['operation']}分")
        
        with col3:
            st.metric("偿债能力", f"{scores['debt']}分")
        
        with col4:
            st.metric("发展能力", f"{scores['growth']}分")
        
        with col5:
            st.metric("预算能力", f"{scores['budget']}分")
        
        st.divider()
        
        # 四轮数据对比
        st.markdown("**📊 四轮经营数据对比**")
        
        if 'quarters_data' in latest:
            df_quarters = pd.DataFrame(latest['quarters_data'])
            st.dataframe(df_quarters, use_container_width=True)
        
        st.divider()
        
        # 复盘总结
        if 'summary' in latest:
            summary = latest['summary']
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**✅ 做得好的地方**")
                if summary.get('good_points'):
                    st.write(summary['good_points'])
            
            with col2:
                st.markdown("**❌ 需要改进的地方**")
                if summary.get('bad_points'):
                    st.write(summary['bad_points'])
            
            st.markdown("**💡 改进计划**")
            if summary.get('action_items'):
                st.write(summary['action_items'])

elif mode == "📈 数据分析":
    if len(reviews_data) < 2:
        st.info("至少需要 2 条记录才能进行数据分析")
    else:
        st.subheader("📈 成绩趋势分析")
        
        # 提取数据
        rounds = [r['round'] for r in reviews_data]
        scores = [r['final_score'] for r in reviews_data]
        ranks = [r['final_rank'] for r in reviews_data]
        penalties = [r['scores']['penalty'] for r in reviews_data]
        
        col1, col2 = st.columns(2)
        
        with col1:
            import plotly.graph_objects as go
            
            fig_score = go.Figure()
            fig_score.add_trace(go.Scatter(
                x=rounds,
                y=scores,
                mode="lines+markers",
                name="得分",
                line=dict(color="blue", width=3)
            ))
            fig_score.add_hline(y=85, line_dash="dash", line_color="green", annotation_text="一等奖线")
            fig_score.add_hline(y=70, line_dash="dash", line_color="orange", annotation_text="二等奖线")
            fig_score.update_layout(title="得分趋势", xaxis_title="轮次", yaxis_title="得分", height=400)
            st.plotly_chart(fig_score, use_container_width=True)
        
        with col2:
            fig_rank = go.Figure()
            fig_rank.add_trace(go.Scatter(
                x=rounds,
                y=ranks,
                mode="lines+markers",
                name="排名",
                line=dict(color="red", width=3)
            ))
            fig_rank.update_layout(title="排名趋势", xaxis_title="轮次", yaxis_title="排名", height=400, yaxis_autorange="reversed")
            st.plotly_chart(fig_rank, use_container_width=True)
        
        st.divider()
        
        # 得分构成分析
        st.subheader("📊 得分构成分析")
        
        profit_scores = [r['scores']['profit'] for r in reviews_data]
        operation_scores = [r['scores']['operation'] for r in reviews_data]
        debt_scores = [r['scores']['debt'] for r in reviews_data]
        growth_scores = [r['scores']['growth'] for r in reviews_data]
        budget_scores = [r['scores']['budget'] for r in reviews_data]
        
        fig_pie = go.Figure(data=[
            go.Pie(labels=["盈利能力", "营运能力", "偿债能力", "发展能力", "预算能力"],
                   values=[sum(profit_scores), sum(operation_scores), sum(debt_scores), 
                           sum(growth_scores), sum(budget_scores)],
                   hole=0.3)
        ])
        fig_pie.update_layout(title="得分构成", height=400)
        st.plotly_chart(fig_pie, use_container_width=True)
        
        st.divider()
        
        # 平均分对比
        st.subheader("📋 各项能力平均分")
        
        avg_data = {
            "能力维度": ["盈利能力", "营运能力", "偿债能力", "发展能力", "预算能力", "违规扣分"],
            "平均分": [
                sum(profit_scores)/len(profit_scores),
                sum(operation_scores)/len(operation_scores),
                sum(debt_scores)/len(debt_scores),
                sum(growth_scores)/len(growth_scores),
                sum(budget_scores)/len(budget_scores),
                sum(penalties)/len(penalties)
            ],
            "满分": [60, 50, 40, 30, 10, 0]
        }
        
        df_avg = pd.DataFrame(avg_data)
        df_avg["得分率"] = (df_avg["平均分"] / df_avg["满分"].replace(0, 1) * 100).apply(lambda x: f"{x:.1f}%")
        
        st.dataframe(df_avg, use_container_width=True, hide_index=True)
