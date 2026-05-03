"""
学创杯比赛辅助工具 - 主入口 v2.2
"""
import streamlit as st

st.set_page_config(
    page_title="学创杯比赛辅助工具",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🏆 学创杯比赛辅助工具 v2.2")

st.markdown("""
## 📊 软件功能模块

### 核心功能 (8/8 完成)

| 模块 | 功能 | 重要性 |
|------|------|--------|
| 📊 财务比率计算器 | 5 大能力 15 指标，实时估算得分 | ⭐⭐⭐⭐⭐ |
| 💰 现金流预测 | 避免断流 (-10 分) 和紧急借款 (-5 分) | ⭐⭐⭐⭐⭐ |
| 📋 预算编制助手 | 4 张预算表，偏差<10% 得 9-10 分 | ⭐⭐⭐⭐⭐ |
| 🏷️ 报价策略计算器 | 动态定价，中标率≥70% | ⭐⭐⭐⭐ |
| 💳 贷款决策助手 | 优化贷款结构，利息最小化 | ⭐⭐⭐⭐ |
| 🏭 产能规划工具 | 产能利用率 85%-95% 最优 | ⭐⭐⭐⭐ |
| 📈 广告 ROI 分析器 | 广告投入 ROI≥100% | ⭐⭐⭐⭐ |
| 📝 比赛复盘记录表 | 记录决策，快速提升 | ⭐⭐⭐⭐⭐ |

### 增强工具 (6/6 完成)

| 工具 | 功能 |
|------|------|
| 🧰 快捷工具箱 | 快速计算、批量对比、比赛计时器 |
| 📤 数据导入导出 | Excel/CSV 导入导出、数据模板 |
| 👥 团队协作 | 多角色分工、决策审批流程 |
| 🤖 智能决策建议 | 基于数据的 AI 决策辅助 |
| 📋 模板中心 | 16 种比赛常用表格模板 |
| ❓ 帮助中心 | 使用指南、比赛规则、FAQ |
""")

st.divider()

st.subheader("🚀 核心功能")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 📊 财务比率计算器
    
    **功能**:
    - 5 大能力 15 个指标
    - 自动估算得分
    - 雷达图可视化
    - 改进建议
    
    **用途**: 每轮结束后评估成绩
    """)
    
    if st.button("打开财务比率计算器", key="btn1", use_container_width=True):
        st.switch_page("pages/01_财务比率计算器.py")

with col2:
    st.markdown("""
    ### 💰 现金流预测
    
    **功能**:
    - 期末现金预测
    - 安全线预警
    - 贷款需求测算
    
    **用途**: 避免 -10 分断流
    """)
    
    if st.button("打开现金流预测", key="btn2", use_container_width=True):
        st.switch_page("pages/02_现金流预测.py")

with col3:
    st.markdown("""
    ### 📋 预算编制助手
    
    **功能**:
    - 4 张预算表
    - 偏差分析
    - 评分估算
    
    **用途**: 预算能力 10 分
    """)
    
    if st.button("打开预算编制助手", key="btn3", use_container_width=True):
        st.switch_page("pages/03_预算编制助手.py")

col4, col5, col6 = st.columns(3)

with col4:
    st.markdown("""
    ### 🏷️ 报价策略计算器
    
    **功能**:
    - 成本分析
    - 多策略对比
    - 竞争定价
    
    **用途**: 竞标前快速定价
    """)
    
    if st.button("打开报价策略计算器", key="btn4", use_container_width=True):
        st.switch_page("pages/04_报价策略计算器.py")

with col5:
    st.markdown("""
    ### 💳 贷款决策助手
    
    **功能**:
    - 方案对比
    - 利息测算
    - 投资回报
    
    **用途**: 优化贷款结构
    """)
    
    if st.button("打开贷款决策助手", key="btn5", use_container_width=True):
        st.switch_page("pages/05_贷款决策助手.py")

with col6:
    st.markdown("""
    ### 🏭 产能规划工具
    
    **功能**:
    - 利用率分析
    - 扩产建议
    - 情景模拟
    
    **用途**: 产能投资决策
    """)
    
    if st.button("打开产能规划工具", key="btn6", use_container_width=True):
        st.switch_page("pages/06_产能规划工具.py")

st.divider()

st.subheader("📈 进阶功能")

col7, col8, col9 = st.columns(3)

with col7:
    st.markdown("""
    ### 📈 广告 ROI 分析器
    
    **功能**:
    - ROI 趋势分析
    - 中标率计算
    - 季度预算规划
    
    **用途**: 广告投放优化
    """)
    
    if st.button("打开广告 ROI 分析器", key="btn7", use_container_width=True):
        st.switch_page("pages/07_广告 ROI 分析器.py")

with col8:
    st.markdown("""
    ### 📝 比赛复盘记录表
    
    **功能**:
    - 决策数据记录
    - 历史趋势分析
    - 经验总结
    
    **用途**: 快速提升水平
    """)
    
    if st.button("打开比赛复盘记录表", key="btn8", use_container_width=True):
        st.switch_page("pages/08_比赛复盘记录表.py")

with col9:
    st.markdown("""
    ### 🧰 快捷工具箱
    
    **功能**:
    - 快速计算器
    - 批量对比
    - 比赛计时器
    - 检查清单
    
    **用途**: 提升决策效率
    """)
    
    if st.button("打开快捷工具箱", key="btn9", use_container_width=True):
        st.switch_page("pages/09_快捷工具箱.py")

st.divider()

st.subheader("🛠️ 工具与协作")

col10, col11, col12 = st.columns(3)

with col10:
    st.markdown("""
    ### 📤 数据导入导出
    
    **功能**:
    - Excel/CSV 导出
    - 数据导入
    - 模板下载
    - 数据管理
    
    **用途**: 数据备份与共享
    """)
    
    if st.button("打开数据导入导出", key="btn10", use_container_width=True):
        st.switch_page("pages/10_数据导入导出.py")

with col11:
    st.markdown("""
    ### 👥 团队协作
    
    **功能**:
    - 角色分工
    - 决策录入
    - 审批流程
    - 统计分析
    
    **用途**: 团队高效协作
    """)
    
    if st.button("打开团队协作", key="btn11", use_container_width=True):
        st.switch_page("pages/11_团队协作.py")

with col12:
    st.markdown("""
    ### 🤖 智能决策建议
    
    **功能**:
    - 赛前策略规划
    - 赛中决策辅助
    - 赛后复盘分析
    - 弱项识别
    
    **用途**: AI 辅助决策
    """)
    
    if st.button("打开智能决策建议", key="btn12", use_container_width=True):
        st.switch_page("pages/12_智能决策建议.py")

st.divider()

st.subheader("📋 报表与模板")

col13, col14 = st.columns(2)

with col13:
    st.markdown("""
    ### 📋 模板中心
    
    **功能**:
    - 16 种比赛表格模板
    - 在线填写编辑
    - 一键导出 Excel
    
    **用途**: 快速生成报表
    """)
    
    if st.button("打开模板中心", key="btn13", use_container_width=True):
        st.switch_page("pages/13_模板中心.py")

with col14:
    st.markdown("""
    ### 📤 数据导入导出
    
    **功能**:
    - 数据导入导出
    - 模板下载
    - 数据管理
    
    **用途**: 数据备份
    """)
    
    if st.button("打开数据管理", key="btn14", use_container_width=True):
        st.switch_page("pages/10_数据导入导出.py")

st.divider()

st.subheader("📖 支持与帮助")

col15, col16 = st.columns(2)

with col15:
    st.markdown("""
    ### ❓ 帮助中心
    
    **功能**:
    - 使用指南
    - 比赛规则
    - 常见问题
    - 技术支持
    
    **用途**: 快速上手
    """)
    
    if st.button("打开帮助中心", key="btn15", use_container_width=True):
        st.switch_page("pages/99_帮助中心.py")

with col16:
    st.markdown("""
    ### 📚 功能清单
    
    **内容**:
    - 完整功能说明
    - 使用场景
    - 版本历史
    
    **用途**: 了解软件全貌
    """)
    
    st.info("📄 功能清单文档：`功能清单.md`")

st.divider()

st.subheader("📅 每季度决策流程")

st.markdown("""
```
【阶段 1】预算编制（5 分钟）→ CFO 负责
    - 销售收入预算
    - 生产成本预算
    - 费用预算
    - 现金预算
    ↓
【阶段 2】投融资决策（10 分钟）→ CEO+CFO
    - 申请贷款（短贷/长贷）
    - 归还到期贷款
    - 支付利息
    ↓
【阶段 3】经营决策（25 分钟）→ 全员
    - 厂房购置/租赁
    - 设备购置
    - 原料采购
    - 人员招聘
    - 生产投料
    - 订单报价 + 广告投放
    ↓
【阶段 4】报税（5 分钟）⚠️ 必须完成 → CFO
    - 增值税申报
    - 所得税申报
    ↓
【阶段 5】复盘调整（5 分钟）→ 全员
    - 检查财务指标
    - 使用本软件计算得分
    - 准备下季度预算
```
""")

st.divider()

st.subheader("📊 比赛评分公式")

st.info("""
**总成绩** = 盈利能力 (30 分) + 营运能力 (25 分) + 偿债能力 (20 分) + 发展能力 (15 分) + 预算能力 (10 分) - 违规扣分

**违规扣分项**:
- 紧急借款：-5 分/次
- 逾期报税：-5 分/次
- 现金断流：-10 分/次
""")

st.subheader("🏆 获奖标准")

col1, col2, col3 = st.columns(3)

col1.success("""
**🥇 一等奖**
总分 ≥ 85 分

关键指标:
- 净利润率 ≥ 10%
- ROE ≥ 20%
- 流动比率 1.2-1.5
- 资产负债率 < 60%
""")

col2.info("""
**🥈 二等奖**
总分 70-84 分

关键指标:
- 净利润率 7-10%
- 流动比率 ≥ 1.0
- 资产负债率 ≤ 65%
""")

col3.warning("""
**🥉 三等奖**
总分 60-69 分

关键指标:
- 净利润率 5-7%
- 避免重大扣分
""")

st.divider()

st.caption("学创杯比赛辅助工具 v2.2 | 适用：第十三届学创杯财务决策模拟赛项 (K1 赛道) | 比赛时间：2026 年 5 月 16 日")
