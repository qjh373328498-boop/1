# 📊 智能决策建议
# 基于数据分析和比赛规则的 AI 决策建议

import streamlit as st
import pandas as pd
import os
import json
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

st.set_page_config(page_title="智能决策建议", page_icon="🤖", layout="wide")

st.title("🤖 智能决策建议")
st.markdown("**基于比赛规则和历史数据的智能决策辅助系统**")

st.divider()

def get_weakness_suggestions(dim, rate):
    if dim == "盈利能力":
        if rate < 50:
            return "净利润率可能<5%，产品定价过低或成本过高"
        elif rate < 70:
            return "净利润率可能 5-7%，有提升空间"
        else:
            return "表现良好，可继续保持"
    elif dim == "营运能力":
        if rate < 50:
            return "资产周转率可能<0.6，存在资产闲置或存货积压"
        elif rate < 70:
            return "资产周转率可能 0.6-0.8，运营效率一般"
        else:
            return "表现良好，可继续保持"
    elif dim == "偿债能力":
        if rate < 50:
            return "流动比例可能<1.0 或 负债率>70%，财务风险高"
        elif rate < 70:
            return "流动比率或负债率接近临界值"
        else:
            return "表现良好，可继续保持"
    elif dim == "发展能力":
        if rate < 50:
            return "销售增长可能<5%，市场拓展不足"
        elif rate < 70:
            return "增长速度一般，可加大市场投入"
        else:
            return "表现良好，可继续保持"
    else:  # 预算能力
        if rate < 50:
            return "预算偏差可能>20%，预算编制不准确"
        elif rate < 70:
            return "预算偏差 10-20%，需提升预算准确性"
        else:
            return "表现良好，可继续保持"

def get_improvement_suggestions(dim):
    if dim == "盈利能力":
        return [
            "使用【报价策略计算器】优化产品定价",
            "分析成本结构，找出降本空间",
            "考虑调整产品结构，增加高毛利产品占比",
            "控制期间费用（广告/管理/财务费用）"
        ]
    elif dim == "营运能力":
        return [
            "使用【产能规划工具】提升产能利用率",
            "优化库存管理，减少存货积压",
            "加快应收账款回收",
            "处置闲置资产，提高资产周转率"
        ]
    elif dim == "偿债能力":
        return [
            "使用【贷款决策助手】优化贷款结构",
            "控制负债率在 50-60%",
            "保持流动比率 1.2-1.5",
            "合理安排长短期贷款比例"
        ]
    elif dim == "发展能力":
        return [
            "加大市场开拓力度",
            "适时扩大产能",
            "开发新产品/新市场",
            "保持适度增速，避免大起大落"
        ]
    else:  # 预算能力
        return [
            "使用【预算编制助手】编制详细预算",
            "建立预算执行监控机制",
            "季度中检查预算偏差并及时调整",
            "提高销售和成本预测准确性"
        ]

# 数据目录
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
REVIEW_FILE = os.path.join(DATA_DIR, "review_records.json")

# 加载中复盘数据
def load_reviews():
    if os.path.exists(REVIEW_FILE):
        with open(REVIEW_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

reviews = load_reviews()

# 侧边栏
with st.sidebar:
    st.header("📋 分析设置")
    
    analysis_mode = st.selectbox(
        "分析模式",
        ["赛前策略规划", "赛中决策辅助", "赛后复盘分析"],
        index=0
    )
    
    target_score = st.selectbox("目标奖项", ["一等奖 (≥85 分)", "二等奖 (70-84 分)", "三等奖 (60-69 分)"], index=0)
    
    st.divider()
    
    if reviews:
        st.info(f"已加载 {len(reviews)} 条复盘记录")
    else:
        st.warning("暂无复盘数据")

st.divider()

if analysis_mode == "赛前策略规划":
    st.subheader("📋 赛前策略规划")
    
    st.markdown("""
    **使用说明**: 根据目标奖项和历史表现，生成赛前策略建议
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 当前能力评估")
        
        # 如果没有历史数据，提供默认评估
        if reviews:
            avg_score = sum(r.get('final_score', 0) for r in reviews) / len(reviews)
            avg_profit = sum(r.get('scores', {}).get('profit', 0) for r in reviews) / len(reviews)
            avg_operation = sum(r.get('scores', {}).get('operation', 0) for r in reviews) / len(reviews)
            avg_debt = sum(r.get('scores', {}).get('debt', 0) for r in reviews) / len(reviews)
            avg_growth = sum(r.get('scores', {}).get('growth', 0) for r in reviews) / len(reviews)
            avg_budget = sum(r.get('scores', {}).get('budget', 0) for r in reviews) / len(reviews)
        else:
            avg_score = 70
            avg_profit = 45
            avg_operation = 35
            avg_debt = 28
            avg_growth = 20
            avg_budget = 7
        
        st.metric("历史平均分", f"{avg_score:.1f}分")
        
        # 能力雷达图数据
        capability_data = {
            "维度": ["盈利能力", "营运能力", "偿债能力", "发展能力", "预算能力"],
            "当前得分": [avg_profit, avg_operation, avg_debt, avg_growth, avg_budget],
            "满分": [60, 50, 20, 15, 10],
            "得分率": [
                avg_profit/60*100,
                avg_operation/50*100,
                avg_debt/20*100,
                avg_growth/15*100,
                avg_budget/10*100
            ]
        }
        
        df_capability = pd.DataFrame(capability_data)
        st.dataframe(df_capability, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("### 目标分解")
        
        target = 85 if "一等奖" in target_score else (70 if "二等奖" in target_score else 60)
        gap = target - avg_score
        
        st.metric("目标分数", f"{target}分")
        st.metric("分数差距", f"{gap:+.1f}分", delta_color="normal" if gap <= 0 else "inverse")
        
        # 目标分解建议
        if gap > 0:
            st.info(f"""
            **需要提升 {gap:.1f} 分，建议**:
            
            1. **盈利能力** +{min(5, gap*0.3):.1f}分
               - 提升净利润率至 10%+
               - 优化产品结构
            
            2. **营运能力** +{min(5, gap*0.25):.1f}分
               - 提高资产周转率
               - 减少存货积压
            
            3. **偿债能力** +{min(3, gap*0.2):.1f}分
               - 保持流动比率 1.2-1.5
               - 控制负债率<60%
            
            4. **发展能力** +{min(2, gap*0.15):.1f}分
               - 销售增长>15%
               - 资产增长>10%
            
            5. **预算能力** +{min(2, gap*0.1):.1f}分
               - 预算偏差<10%
            """)
        else:
            st.success("✅ 当前水平已达到目标！")
    
    st.divider()
    
    st.markdown("### 赛前准备清单")
    
    checklist = {
        "软件准备": [
            "✅ 安装 Streamlit 及依赖",
            "✅ 测试所有功能模块",
            "✅ 准备备用电脑",
            "✅ 打印使用指南"
        ],
        "数据准备": [
            "📋 准备历史经营数据（如有）",
            "📋 熟悉比赛初始条件",
            "📋 了解竞争对手情况"
        ],
        "团队准备": [
            "👥 明确角色分工（CEO/CFO/COO/CMO）",
            "👥 制定沟通机制",
            "👥 进行 1-2 次模拟训练"
        ],
        "物资准备": [
            "📝 纸笔（快速计算）",
            "📝 计算器",
            "📝 打印评分规则",
            "📝 饮用水和零食"
        ]
    }
    
    for category, items in checklist.items():
        with st.expander(f"**{category}**"):
            for item in items:
                st.write(item)

elif analysis_mode == "赛中决策辅助":
    st.subheader("🎯 赛中决策辅助")
    
    st.markdown("""
    **使用说明**: 根据当前季度和财务状况，生成实时决策建议
    """)
    
    # 选择当前季度
    current_quarter = st.select_slider(
        "当前季度",
        options=["Q1", "Q2", "Q3", "Q4"],
        value="Q1"
    )
    
    st.divider()
    
    # 根据季度提供建议
    if current_quarter == "Q1":
        st.markdown("### 🌱 Q1 决策建议")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info("""
            **💰 财务策略**
            
            **贷款建议**:
            - 申请长期贷款：资产负债率≤65%
            - 短贷补充流动资金
            - 预计贷款额度：300-500 万
            
            **现金流**:
            - 期初现金：100-200 万
            - 确保期末为正
            """)
        
        with col2:
            st.info("""
            **🏭 产能策略**
            
            **投资重点**:
            - 购置 1-2 条生产线
            - 投资金额：150-300 万
            - 目标产能：8000-12000件/季
            
            **厂房**:
            - 购买或租赁均可
            - 建议：资金充足时购买
            """)
        
        with col3:
            st.info("""
            **📢 市场策略**
            
            **广告投放**:
            - 投入比例：8-10% 预计销售额
            - 重点市场：本地/区域
            - 目标中标率：≥70%
            
            **定价**:
            - 抢市场策略：0.85-0.90x成本
            - 目标：拿下足够订单
            """)
        
        st.divider()
        
        st.markdown("### ⚠️ Q1 风险提示")
        
        st.warning("""
        **常见失误**:
        1. ❌ 过于保守，不敢贷款 → 错失发展机会
        2. ❌ 盲目扩张，产能过剩 → 固定成本过高
        3. ❌ 广告投入不足 → 订单不足
        4. ❌ 定价过高 → 丢单严重
        
        **规避建议**:
        1. ✅ 充分利用财务杠杆，但要控制负债率
        2. ✅ 根据订单预测投资产能
        3. ✅ 使用【广告 ROI 分析器】计算最优投入
        4. ✅ 使用【报价策略计算器】制定合理价格
        """)
    
    elif current_quarter == "Q2":
        st.markdown("### 📈 Q2 决策建议")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info("""
            **💰 财务策略**
            
            **贷款建议**:
            - 适度贷款：资产负债率≤60%
            - 关注现金流安全
            - 偿还到期短贷
            
            **现金流**:
            - 安全线：期末≥固定支出×1.2
            - 使用【现金流预测】模块
            """)
        
        with col2:
            st.info("""
            **🏭 产能策略**
            
            **优化重点**:
            - 提升产能利用率至≥85%
            - 如不足考虑接低毛利订单
            - 暂不新增产能投资
            
            **效率**:
            - 优化排产计划
            - 减少换线次数
            """)
        
        with col3:
            st.info("""
            **📢 市场策略**
            
            **广告投放**:
            - 投入比例：5-7% 预计销售额
            - 精准投放高 ROI 市场
            - 目标中标率：≥75%
            
            **定价**:
            - 稳健策略：0.95-1.00x成本
            - 目标：保持市场份额同时提升毛利
            """)
        
        st.divider()
        
        st.markdown("### ⚠️ Q2 风险提示")
        
        st.warning("""
        **常见失误**:
        1. ❌ 现金断流 → -10 分
        2. ❌ 产能利用率低 (<70%) → 固定成本高
        3. ❌ 忘记报税 → -5 分
        4. ❌ 广告投放过于分散
        
        **规避建议**:
        1. ✅ 每轮必用【现金流预测】
        2. ✅ 使用【产能规划工具】检查利用率
        3. ✅ 设置报税提醒（使用计时器）
        4. ✅ 使用【广告 ROI 分析器】聚焦高回报市场
        """)
    
    elif current_quarter == "Q3":
        st.markdown("### 🚀 Q3 决策建议")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info("""
            **💰 财务策略**
            
            **贷款建议**:
            - 适度扩张：资产负债率≤65%
            - 可考虑追加投资贷款
            - 注意季度末还款压力
            
            **现金流**:
            - 预留还款资金
            - 确保不紧急借款
            """)
        
        with col2:
            st.info("""
            **🏭 产能策略**
            
            **扩张时机**:
            - 如产能利用率>95%，考虑扩产
            - 投资回收期<3 年可行
            - 新增 1-2 条生产线
            
            **效率**:
            - 满负荷生产
            - 最大化规模效应
            """)
        
        with col3:
            st.info("""
            **📢 市场策略**
            
            **广告投放**:
            - 投入比例：7-9% 预计销售额
            - 重点投放高毛利产品市场
            - 目标中标率：≥80%
            
            **定价**:
            - 平衡策略：0.95-1.05x成本
            - 根据竞争情况动态调整
            """)
        
        st.divider()
        
        st.markdown("### ⚠️ Q3 风险提示")
        
        st.warning("""
        **常见失误**:
        1. ❌ 错过扩张窗口期 → Q4 产能不足
        2. ❌ 过度投资 → 负债率超标
        3. ❌ 广告投放效率低 → ROI<100%
        4. ❌ 财务指标恶化未及时调整
        
        **规避建议**:
        1. ✅ 使用【产能规划工具】评估扩产必要性
        2. ✅ 使用【贷款决策助手】优化贷款结构
        3. ✅ 使用【广告 ROI 分析器】提升投放效率
        4. ✅ 使用【财务比率计算器】实时监控得分
        """)
    
    else:  # Q4
        st.markdown("### 💰 Q4 决策建议")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info("""
            **💰 财务策略**
            
            **贷款建议**:
            - 收缩战略：资产负债率≤55%
            - 优先偿还高息贷款
            - 降低财务费用
            
            **现金流**:
            - 确保不出现紧急借款
            - 预留充足现金收尾
            """)
        
        with col2:
            st.info("""
            **🏭 产能策略**
            
            **利润最大化**:
            - 满负荷生产
            - 不再新增投资
            - 清理库存
            
            **效率**:
            - 聚焦高毛利产品
            - 减少不必要开支
            """)
        
        with col3:
            st.info("""
            **📢 市场策略**
            
            **广告投放**:
            - 投入比例：3-5% 预计销售额
            - 控制成本
            - 目标中标率：≥70%
            
            **定价**:
            - 利润导向：1.05-1.10x成本
            - 冲刺高利润
            """)
        
        st.divider()
        
        st.markdown("### ⚠️ Q4 风险提示")
        
        st.warning("""
        **常见失误**:
        1. ❌ 期末现金断流 → -10 分（功亏一篑）
        2. ❌ 忘记报税 → -5 分
        3. ❌ 负债率过高 → 偿债能力扣分
        4. ❌ 预算偏差大 → 预算能力扣分
        
        **规避建议**:
        1. ✅ 反复使用【现金流预测】确保安全
        2. ✅ 定报税闹钟（使用计时器）
        3. ✅ 使用【财务比率计算器】检查最终得分
        4. ✅ 使用【预算编制助手】控制偏差<10%
        """)
    
    st.divider()
    
    # 快速决策入口
    st.markdown("### 🚀 快速打开相关工具")
    
    col_q1, col_q2, col_q3, col_q4 = st.columns(4)
    
    with col_q1:
        if st.button("💰 现金流预测", use_container_width=True):
            st.switch_page("pages/02_现金流预测.py")
    
    with col_q2:
        if st.button("📊 财务比率", use_container_width=True):
            st.switch_page("pages/01_财务比率计算器.py")
    
    with col_q3:
        if st.button("🏷️ 报价策略", use_container_width=True):
            st.switch_page("pages/04_报价策略计算器.py")
    
    with col_q4:
        if st.button("⏱️ 比赛计时", use_container_width=True):
            st.switch_page("pages/09_快捷工具箱.py")

else:  # 赛后复盘分析
    st.subheader("📝 赛后复盘分析")
    
    if not reviews:
        st.info("暂无复盘数据，请先在【比赛复盘记录表】中记录数据")
    else:
        # 最新一轮数据
        latest = reviews[-1]
        
        st.markdown(f"### 第{latest.get('round', '?')}轮 复盘分析")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("最终得分", f"{latest.get('final_score', 0)}分")
        
        with col2:
            st.metric("获奖等级", latest.get('achievement', '未知'))
        
        with col3:
            rank = latest.get('final_rank', '?')
            total = latest.get('total_teams', '?')
            st.metric("排名", f"{rank}/{total}")
        
        with col4:
            penalty = latest.get('scores', {}).get('penalty', 0)
            st.metric("违规扣分", f"-{penalty}分")
        
        st.divider()
        
        # 得分分析
        st.markdown("### 📊 得分构成分析")
        
        scores = latest.get('scores', {})
        
        score_data = {
            "维度": ["盈利能力", "营运能力", "偿债能力", "发展能力", "预算能力", "违规扣分"],
            "得分": [
                scores.get('profit', 0),
                scores.get('operation', 0),
                scores.get('debt', 0),
                scores.get('growth', 0),
                scores.get('budget', 0),
                -scores.get('penalty', 0)
            ],
            "满分": [60, 50, 20, 15, 10, 0]
        }
        
        df_scores = pd.DataFrame(score_data)
        df_scores["得分率"] = (df_scores["得分"] / df_scores["满分"].replace(0, 1) * 100).apply(lambda x: f"{x:.1f}%")
        
        st.dataframe(df_scores, use_container_width=True, hide_index=True)
        
        st.divider()
        
        # 弱项识别
        st.markdown("### ⚠️ 弱项识别与改进建议")
        
        # 找出得分率最低的 3 项
        score_rates = [
            ("盈利能力", scores.get('profit', 0) / 60 * 100),
            ("营运能力", scores.get('operation', 0) / 50 * 100),
            ("偿债能力", scores.get('debt', 0) / 20 * 100),
            ("发展能力", scores.get('growth', 0) / 15 * 100),
            ("预算能力", scores.get('budget', 0) / 10 * 100)
        ]
        
        score_rates.sort(key=lambda x: x[1])
        
        for i, (dim, rate) in enumerate(score_rates[:3], 1):
            st.markdown(f"""
            **{i}. {dim}** (得分率：{rate:.1f}%)
            
            **可能问题**:
            - {get_weakness_suggestions(dim, rate)}
            
            **改进建议**:
            - {get_improvement_suggestions(dim)}
            """)
            st.divider()
        
        # 复盘总结
        st.markdown("### 📝 复盘总结")
        
        summary = latest.get('summary', {})
        
        col_good, col_bad = st.columns(2)
        
        with col_good:
            st.markdown("**✅ 做得好的地方**")
            if summary.get('good_points'):
                st.write(summary['good_points'])
            else:
                st.write("暂无记录")
        
        with col_bad:
            st.markdown("**❌ 需要改进的地方**")
            if summary.get('bad_points'):
                st.write(summary['bad_points'])
            else:
                st.write("暂无记录")
        
        st.markdown("**💡 改进计划**")
        if summary.get('action_items'):
            st.write(summary['action_items'])
        else:
            st.write("暂无记录")

# 页脚
st.divider()
st.caption("学创杯比赛辅助工具 v2.0 - 智能决策建议")
