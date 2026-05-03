# 📋 模板中心 - 性能优化版

import streamlit as st
import pandas as pd
import io
from datetime import datetime

st.set_page_config(page_title="模板中心", page_icon="📋", layout="wide")

st.title("📋 模板中心")
st.markdown("**提供比赛常用表格模板，支持在线填写和 Excel 下载**")

st.divider()

# ========== 性能优化：缓存模板数据 ==========
@st.cache_data
def load_template(template_name):
    """缓存模板数据，避免重复创建 DataFrame"""
    templates = {
        '资产负债表': {
            'assets': {
                'cols': ['货币资金', '应收账款', '存货', '固定资产', '无形资产', '长期投资', '其他资产'],
                'rows': 7
            },
            'liabilities': {
                'cols': ['短期借款', '应付账款', '应交税费', '长期借款', '其他负债'],
                'rows': 5
            },
            'equity': {
                'cols': ['实收资本', '资本公积', '盈余公积', '未分配利润'],
                'rows': 4
            }
        },
        '利润表': {
            'items': ['营业收入', '营业成本', '税金及附加', '销售费用', '管理费用', '财务费用', '所得税'],
            'rows': 7
        },
        '现金流量表': {
            'operating': ['销售商品提供劳务收到的现金', '购买商品接受劳务支付的现金', '支付给职工以及为职工支付的现金', '支付的各项税费', '其他经营现金'],
            'investing': ['购建固定资产支付的现金', '投资支付的现金', '其他投资现金'],
            'financing': ['吸收投资收到的现金', '取得借款收到的现金', '偿还债务支付的现金', '分配股利利润支付的现金']
        }
    }
    return templates.get(template_name, {})

# ========== 懒加载：只渲染当前选中的标签页 ==========
selected_tab = st.selectbox(
    "选择模板分类",
    ["📊 财务报表模板", "💰 决策记录模板", "📈 分析报表模板", "📝 比赛用表模板", "💾 下载全部模板"],
    label_visibility="collapsed",
    key="template_category"
)

st.divider()

# 根据选择渲染对应内容（懒加载）
if selected_tab == "📊 财务报表模板":
    st.subheader("📊 财务报表模板")
    
    template_choice = st.selectbox(
        "选择财务报表模板",
        ["资产负债表", "利润表", "现金流量表", "科目余额表"],
        key="finance_template"
    )
    
    if template_choice == "资产负债表":
        st.markdown("### 资产负债表模板")
        
        # 使用缓存的模板结构
        template = load_template('资产负债表')
        
        asset_data = {
            "资产项目": template['assets']['cols'],
            "期初金额": [0.0] * len(template['assets']['cols']),
            "期末金额": [0.0] * len(template['assets']['cols'])
        }
        df_assets = pd.DataFrame(asset_data)
        
        liability_data = {
            "负债项目": template['assets']['liabilities']['cols'] if 'liabilities' in template['assets'] else ['短期借款', '应付账款', '应交税费', '长期借款', '其他负债'],
            "期初金额": [0.0] * 5,
            "期末金额": [0.0] * 5
        }
        df_liabilities = pd.DataFrame(liability_data)
        
        equity_data = {
            "所有者权益项目": template['assets']['equity']['cols'] if 'equity' in template['assets'] else ['实收资本', '资本公积', '盈余公积', '未分配利润'],
            "期初金额": [0.0] * 4,
            "期末金额": [0.0] * 4
        }
        df_equity = pd.DataFrame(equity_data)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 资产")
            edited_assets = st.data_editor(df_assets, hide_index=True, use_container_width=True, key="edit_asset", height=300)
        
        with col2:
            st.markdown("#### 负债 + 所有者权益")
            edited_liabilities = st.data_editor(df_liabilities, hide_index=True, use_container_width=True, key="edit_liability", height=200)
            edited_equity = st.data_editor(df_equity, hide_index=True, use_container_width=True, key="edit_equity", height=150)
        
        # 计算总计
        total_assets_end = edited_assets["期末金额"].sum()
        total_liabilities_end = edited_liabilities["期末金额"].sum()
        total_equity_end = edited_equity["期末金额"].sum()
        
        st.divider()
        
        st.markdown("#### 平衡验证")
        balance_check = total_assets_end - (total_liabilities_end + total_equity_end)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("资产总计", f"{total_assets_end:.2f}万元")
        
        with col2:
            st.metric("负债 + 所有者权益", f"{total_liabilities_end + total_equity_end:.2f}万元")
        
        with col3:
            if abs(balance_check) < 0.01:
                st.metric("平衡检查", "✅ 平衡")
            else:
                st.metric("平衡检查", f"❌ 差{balance_check:.2f}万元", delta_color="inverse")
        
        # 导出 Excel
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            edited_assets.to_excel(writer, sheet_name='资产', index=False)
            edited_liabilities.to_excel(writer, sheet_name='负债', index=False)
            edited_equity.to_excel(writer, sheet_name='所有者权益', index=False)
        
        st.download_button(
            label="📥 下载资产负债表 Excel",
            data=output.getvalue(),
            file_name=f"资产负债表_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.ms-excel"
        )
    
    elif template_choice == "利润表":
        st.markdown("### 利润表模板")
        
        template = load_template('利润表')
        profit_data = {
            "项目": template['items'],
            "本期金额": [0.0] * len(template['items']),
            "上期金额": [0.0] * len(template['items'])
        }
        df_profit = pd.DataFrame(profit_data)
        
        edited_profit = st.data_editor(df_profit, hide_index=True, use_container_width=True, key="edit_profit", height=400)
        
        revenue = edited_profit.loc[0, "本期金额"] if len(edited_profit) > 0 else 0
        cost = edited_profit.loc[1, "本期金额"] if len(edited_profit) > 0 else 0
        net_profit = edited_profit.loc[6, "本期金额"] if len(edited_profit) > 0 else 0
        
        st.divider()
        
        col1, col2, col3 = st.columns(3)
        col1.metric("营业收入", f"{revenue:.2f}万元")
        col2.metric("营业成本", f"{cost:.2f}万元")
        col3.metric("净利润", f"{net_profit:.2f}万元")
        
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            edited_profit.to_excel(writer, sheet_name='利润表', index=False)
        
        st.download_button(
            label="📥 下载利润表 Excel",
            data=output.getvalue(),
            file_name=f"利润表_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.ms-excel"
        )
    
    elif template_choice == "现金流量表":
        st.markdown("### 现金流量表模板")
        
        template = load_template('现金流量表')
        
        st.markdown("#### 经营活动现金流")
        operating_data = {
            "项目": template['operating'],
            "金额": [0.0] * len(template['operating'])
        }
        df_operating = pd.DataFrame(operating_data)
        edited_operating = st.data_editor(df_operating, hide_index=True, use_container_width=True, key="edit_operating", height=200)
        
        st.markdown("#### 投资活动现金流")
        investing_data = {
            "项目": template['investing'],
            "金额": [0.0] * len(template['investing'])
        }
        df_investing = pd.DataFrame(investing_data)
        edited_investing = st.data_editor(df_investing, hide_index=True, use_container_width=True, key="edit_investing", height=150)
        
        st.markdown("#### 筹资活动现金流")
        financing_data = {
            "项目": template['financing'],
            "金额": [0.0] * len(template['financing'])
        }
        df_financing = pd.DataFrame(financing_data)
        edited_financing = st.data_editor(df_financing, hide_index=True, use_container_width=True, key="edit_financing", height=180)
        
        st.divider()
        
        net_operating = edited_operating["金额"].sum()
        net_investing = edited_investing["金额"].sum()
        net_financing = edited_financing["金额"].sum()
        total_cash_flow = net_operating + net_investing + net_financing
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("经营现金净额", f"{net_operating:.2f}万元")
        col2.metric("投资现金净额", f"{net_investing:.2f}万元")
        col3.metric("筹资现金净额", f"{net_financing:.2f}万元")
        col4.metric("现金净增加额", f"{total_cash_flow:.2f}万元")
        
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            edited_operating.to_excel(writer, sheet_name='经营活动', index=False)
            edited_investing.to_excel(writer, sheet_name='投资活动', index=False)
            edited_financing.to_excel(writer, sheet_name='筹资活动', index=False)
        
        st.download_button(
            label="📥 下载现金流量表 Excel",
            data=output.getvalue(),
            file_name=f"现金流量表_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.ms-excel"
        )
    
    elif template_choice == "科目余额表":
        st.markdown("### 科目余额表模板")
        
        account_data = {
            "科目代码": ["1001", "1002", "1122", "1405", "1601", "2001", "2202", "4001", "4101", "5001", "6001", "6401"],
            "科目名称": ["库存现金", "银行存款", "应收账款", "存货", "固定资产", "短期借款", "应付账款", "实收资本", "本年利润", "主营业务收入", "主营业务成本", "管理费用"],
            "期初借方": [0.0]*12,
            "期初贷方": [0.0]*12,
            "本期借方": [0.0]*12,
            "本期贷方": [0.0]*12,
            "期末借方": [0.0]*12,
            "期末贷方": [0.0]*12
        }
        df_accounts = pd.DataFrame(account_data)
        
        edited_accounts = st.data_editor(df_accounts, hide_index=True, use_container_width=True, key="edit_accounts", height=500)
        
        st.download_button(
            label="📥 下载科目余额表 Excel",
            data=edited_accounts.to_csv(index=False).encode('utf-8-sig'),
            file_name=f"科目余额表_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

elif selected_tab == "💰 决策记录模板":
    st.subheader("💰 决策记录模板")
    
    decision_type = st.selectbox(
        "选择决策记录类型",
        ["贷款决策记录", "投资决策记录", "广告竞标记录"],
        key="decision_template"
    )
    
    if decision_type == "贷款决策记录":
        st.markdown("### 贷款决策记录表")
        
        loan_records = {
            "贷款日期": [datetime.now().strftime('%Y-%m-%d')],
            "贷款类型": ["短期贷款"],
            "贷款金额": [0.0],
            "贷款年限": [1],
            "年利率 (%)": [5.0],
            "还款方式": ["等额本息"],
            "经办人": [""]
        }
        df_loans = pd.DataFrame(loan_records)
        
        edited_loans = st.data_editor(df_loans, hide_index=True, use_container_width=True, key="edit_loans", num_rows="dynamic", height=250)
        
        total_loan = edited_loans["贷款金额"].sum() if "贷款金额" in edited_loans.columns else 0
        
        st.divider()
        st.metric("贷款总额", f"{total_loan:.2f}万元")
        
        st.download_button(
            label="📥 下载贷款记录 Excel",
            data=edited_loans.to_csv(index=False).encode('utf-8-sig'),
            file_name=f"贷款记录_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    elif decision_type == "投资决策记录":
        st.markdown("### 投资决策记录表")
        
        investment_data = {
            "投资项目": ["生产线投资", "市场开拓投资", "产品研发投资"],
            "投资金额": [0.0, 0.0, 0.0],
            "预计回报期 (月)": [12, 6, 18],
            "预期收益率 (%)": [15.0, 10.0, 20.0],
            "决策日期": [datetime.now().strftime('%Y-%m-%d')]*3,
            "决策理由": ["扩大产能", "增加市场份额", "提升竞争力"]
        }
        df_investment = pd.DataFrame(investment_data)
        
        edited_investment = st.data_editor(df_investment, hide_index=True, use_container_width=True, key="edit_investment", height=250)
        
        total_investment = edited_investment["投资金额"].sum() if "投资金额" in edited_investment.columns else 0
        
        st.divider()
        st.metric("投资总额", f"{total_investment:.2f}万元")
        
        st.download_button(
            label="📥 下载投资记录 Excel",
            data=edited_investment.to_csv(index=False).encode('utf-8-sig'),
            file_name=f"投资记录_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    elif decision_type == "广告竞标记录":
        st.markdown("### 广告竞标记录表")
        
        bid_data = {
            "市场名称": ["本地市场", "区域市场", "国内市场"],
            "广告投入 (万元)": [0.0, 0.0, 0.0],
            "预期中标率 (%)": [80.0, 60.0, 40.0],
            "预计订单量": [0, 0, 0],
            "竞争对手数": [3, 5, 8],
            "竞标结果": ["待公布", "待公布", "待公布"]
        }
        df_bids = pd.DataFrame(bid_data)
        
        edited_bids = st.data_editor(df_bids, hide_index=True, use_container_width=True, key="edit_bids", height=250)
        
        total_bid = edited_bids["广告投入 (万元)"].sum() if "广告投入 (万元)" in edited_bids.columns else 0
        
        st.divider()
        st.metric("广告总投入", f"{total_bid:.2f}万元")
        
        st.download_button(
            label="📥 下载竞标记录 Excel",
            data=edited_bids.to_csv(index=False).encode('utf-8-sig'),
            file_name=f"竞标记录_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

elif selected_tab == "📈 分析报表模板":
    st.subheader("📈 分析报表模板")
    
    analysis_type = st.selectbox(
        "选择分析报表类型",
        ["财务比率分析", "成本结构分析", "预算执行分析", "敏感性分析"],
        key="analysis_template"
    )
    
    if analysis_type == "财务比率分析":
        st.markdown("### 财务比率分析表")
        
        ratio_data = {
            "财务比率": ["流动比率", "速动比率", "资产负债率", "净利润率", "ROE", "ROA", "应收账款周转率", "存货周转率"],
            "本期值": [0.0]*8,
            "上期值": [0.0]*8,
            "行业平均": [1.5, 1.0, 50.0, 10.0, 15.0, 8.0, 4.0, 3.0],
            "差异": [0.0]*8
        }
        df_ratios = pd.DataFrame(ratio_data)
        
        edited_ratios = st.data_editor(df_ratios, hide_index=True, use_container_width=True, key="edit_ratios", height=350)
        
        st.download_button(
            label="📥 下载财务比率分析 Excel",
            data=edited_ratios.to_csv(index=False).encode('utf-8-sig'),
            file_name=f"财务比率分析_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    elif analysis_type == "成本结构分析":
        st.markdown("### 成本结构分析表")
        
        cost_data = {
            "成本项目": ["直接材料", "直接人工", "制造费用", "管理费用", "销售费用", "财务费用"],
            "预算金额": [0.0]*6,
            "实际金额": [0.0]*6,
            "差异金额": [0.0]*6,
            "差异率 (%)": [0.0]*6
        }
        df_cost = pd.DataFrame(cost_data)
        
        edited_cost = st.data_editor(df_cost, hide_index=True, use_container_width=True, key="edit_cost", height=300)
        
        # 自动计算
        if "预算金额" in edited_cost.columns and "实际金额" in edited_cost.columns:
            edited_cost["差异金额"] = edited_cost["实际金额"] - edited_cost["预算金额"]
            edited_cost["差异率 (%)"] = (edited_cost["差异金额"] / edited_cost["预算金额"].replace(0, 1) * 100)
        
        st.dataframe(edited_cost[["成本项目", "预算金额", "实际金额", "差异金额", "差异率 (%)"]], use_container_width=True, hide_index=True, height=300)
        
        st.download_button(
            label="📥 下载成本分析 Excel",
            data=edited_cost.to_csv(index=False).encode('utf-8-sig'),
            file_name=f"成本分析_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    elif analysis_type == "预算执行分析":
        st.markdown("### 预算执行分析表")
        
        budget_data = {
            "项目": ["营业收入", "营业成本", "税金及附加", "销售费用", "管理费用", "财务费用", "利润总额"],
            "预算数": [0.0]*7,
            "实际数": [0.0]*7,
            "执行率 (%)": [0.0]*7,
            "差异分析": [""]*7
        }
        df_budget = pd.DataFrame(budget_data)
        
        edited_budget = st.data_editor(df_budget, hide_index=True, use_container_width=True, key="edit_budget", height=350)
        
        st.download_button(
            label="📥 下载预算分析 Excel",
            data=edited_budget.to_csv(index=False).encode('utf-8-sig'),
            file_name=f"预算分析_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    elif analysis_type == "敏感性分析":
        st.markdown("### 敏感性分析表")
        
        sensitivity_data = {
            "变量": ["销售价格", "销售数量", "单位成本", "固定成本"],
            "变动幅度": ["+10%", "+5%", "0%", "-5%", "-10%"],
            "对利润影响": [0.0]*4,
            "敏感程度": ["待分析"]*4
        }
        df_sensitivity = pd.DataFrame(sensitivity_data)
        
        st.dataframe(df_sensitivity, use_container_width=True, hide_index=True)
        
        st.info("💡 填写实际数据后导出分析结果")
    
    elif analysis_type == "科目余额表":
        st.markdown("### 科目余额表")
        
        account_data = {
            "科目代码": ["1001", "1002", "1122", "1405", "1601", "2001", "2202", "4001", "4101", "5001", "6001", "6401"],
            "科目名称": ["库存现金", "银行存款", "应收账款", "存货", "固定资产", "短期借款", "应付账款", "实收资本", "本年利润", "主营业务收入", "主营业务成本", "管理费用"],
            "期初借方": [0.0]*12,
            "期初贷方": [0.0]*12,
            "本期借方": [0.0]*12,
            "本期贷方": [0.0]*12,
            "期末借方": [0.0]*12,
            "期末贷方": [0.0]*12
        }
        df_accounts = pd.DataFrame(account_data)
        
        edited_accounts = st.data_editor(df_accounts, hide_index=True, use_container_width=True, key="edit_accounts2", height=500)
        
        st.download_button(
            label="📥 下载科目余额表 Excel",
            data=edited_accounts.to_csv(index=False).encode('utf-8-sig'),
            file_name=f"科目余额表_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

elif selected_tab == "📝 比赛用表模板":
    st.subheader("📝 比赛用表模板")
    
    competition_type = st.selectbox(
        "选择比赛用表类型",
        ["决策记录表", "贷款记录表", "投资记录表", "广告竞标表", "财务比率分析表"],
        key="competition_template"
    )
    
    if competition_type == "决策记录表":
        st.markdown("### 比赛决策记录表")
        
        decision_records = []
        for i in range(8):
            decision_records.append({
                "季度": f"Q{i+1}",
                "决策要点": "",
                "执行结果": "",
                "得分": 0.0,
                "改进措施": ""
            })
        
        df_decisions = pd.DataFrame(decision_records)
        
        edited_decisions = st.data_editor(df_decisions, hide_index=True, use_container_width=True, key="edit_decisions", height=400)
        
        st.download_button(
            label="📥 下载决策记录表 Excel",
            data=edited_decisions.to_csv(index=False).encode('utf-8-sig'),
            file_name=f"决策记录_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    elif competition_type == "贷款记录表":
        st.markdown("### 比赛贷款记录表")
        
        loan_records = {
            "贷款季度": ["Q1", "Q2", "Q3", "Q4"],
            "贷款类型": ["短期贷款", "长期贷款", "短期贷款", "长期贷款"],
            "贷款金额": [0.0]*4,
            "贷款年限": [1, 3, 1, 3],
            "年利率 (%)": [5.0, 6.0, 5.0, 6.0],
            "还款计划": [""]*4
        }
        df_loans = pd.DataFrame(loan_records)
        
        edited_loans = st.data_editor(df_loans, hide_index=True, use_container_width=True, key="edit_loans2", height=300)
        
        st.download_button(
            label="📥 下载贷款记录表 Excel",
            data=edited_loans.to_csv(index=False).encode('utf-8-sig'),
            file_name=f"贷款记录_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    elif competition_type == "投资记录表":
        st.markdown("### 比赛投资记录表")
        
        investment_data = {
            "投资季度": ["Q1", "Q2", "Q3", "Q4"],
            "投资项目": ["生产线", "市场开拓", "产品研发", "生产线"],
            "投资金额": [0.0]*4,
            "预计回报": [0.0]*4,
            "实际回报": [0.0]*4,
            "投资效果": ["待评估"]*4
        }
        df_investment = pd.DataFrame(investment_data)
        
        edited_investment = st.data_editor(df_investment, hide_index=True, use_container_width=True, key="edit_investment2", height=300)
        
        st.download_button(
            label="📥 下载投资记录表 Excel",
            data=edited_investment.to_csv(index=False).encode('utf-8-sig'),
            file_name=f"投资记录_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    elif competition_type == "广告竞标表":
        st.markdown("### 比赛广告竞标表")
        
        bid_data = {
            "市场类型": ["本地市场", "区域市场", "国内市场", "国际市场"],
            "广告预算": [0.0]*4,
            "实际投入": [0.0]*4,
            "竞标排名": [0]*4,
            "获得订单": [0]*4,
            "ROI": [0.0]*4
        }
        df_bids = pd.DataFrame(bid_data)
        
        edited_bids = st.data_editor(df_bids, hide_index=True, use_container_width=True, key="edit_bids2", height=300)
        
        st.download_button(
            label="📥 下载广告竞标表 Excel",
            data=edited_bids.to_csv(index=False).encode('utf-8-sig'),
            file_name=f"广告竞标_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    elif competition_type == "财务比率分析表":
        st.markdown("### 比赛财务比率分析表")
        
        ratio_data = {
            "比率名称": ["流动比率", "速动比率", "资产负债率 (%)", "净利润率 (%)", "ROE (%)", "ROA (%)", "应收账款周转率", "存货周转率"],
            "Q1 实际": [0.0]*8,
            "Q1 标准": [1.5, 1.0, 50.0, 10.0, 15.0, 8.0, 4.0, 3.0],
            "Q1 得分": [0.0]*8,
            "Q2 实际": [0.0]*8,
            "Q2 标准": [1.5, 1.0, 50.0, 10.0, 15.0, 8.0, 4.0, 3.0],
            "Q2 得分": [0.0]*8
        }
        df_ratios = pd.DataFrame(ratio_data)
        
        edited_ratios = st.data_editor(df_ratios, hide_index=True, use_container_width=True, key="edit_ratios2", height=400)
        
        st.download_button(
            label="📥 下载财务比率分析表 Excel",
            data=edited_ratios.to_csv(index=False).encode('utf-8-sig'),
            file_name=f"财务比率分析_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

elif selected_tab == "💾 下载全部模板":
    st.subheader("💾 下载全部模板")
    
    st.markdown("""
    ### 一键下载所有模板
    
    点击下方按钮，下载包含所有模板的 Excel 文件。
    """)
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        # 目录
        pd.DataFrame({"模板": ["财务报表", "决策记录", "分析报表", "比赛用表"]}).to_excel(writer, sheet_name='目录', index=False)
        
        # 财务报表
        pd.DataFrame({"项目": ["货币资金", "应收账款", "存货"], "金额": [0, 0, 0]}).to_excel(writer, sheet_name='资产负债表', index=False)
        pd.DataFrame({"项目": ["营业收入", "营业成本", "净利润"], "金额": [0, 0, 0]}).to_excel(writer, sheet_name='利润表', index=False)
        
        # 决策记录
        pd.DataFrame({"决策类型": ["贷款", "投资", "广告"], "金额": [0, 0, 0]}).to_excel(writer, sheet_name='决策记录', index=False)
        
        # 分析报表
        pd.DataFrame({"比率": ["流动比率", "速动比率", "资产负债率"], "数值": [0, 0, 0]}).to_excel(writer, sheet_name='财务比率', index=False)
    
    st.download_button(
        label="📥 下载全部模板 (Excel 打包)",
        data=output.getvalue(),
        file_name=f"全部模板包_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
        mime="application/vnd.ms-excel",
        use_container_width=True
    )
    
    st.divider()
    
    st.markdown("""
    ### 使用说明
    
    1. **在线填写**: 在各模板标签页中在线填写数据
    2. **导出 Excel**: 填写完成后点击导出按钮下载
    3. **批量下载**: 在本页面一键下载所有模板
    
    ### 模板分类
    
    | 分类 | 模板数量 | 用途 |
    |------|----------|------|
    | 财务报表 | 4 个 | 记录财务数据 |
    | 决策记录 | 3 个 | 记录重大决策 |
    | 分析报表 | 4 个 | 财务分析 |
    | 比赛用表 | 5 个 | 比赛专用 |
    """)
