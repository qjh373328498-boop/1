# 📋 模板中心
# 提供比赛常用表格模板

import streamlit as st
import pandas as pd
import io
from datetime import datetime

st.set_page_config(page_title="模板中心", page_icon="📋", layout="wide")

st.title("📋 模板中心")
st.markdown("**提供比赛常用表格模板，支持在线填写和 Excel 下载**")

st.divider()

# 模板分类
tabs = st.tabs([
    "📊 财务报表模板",
    "💰 决策记录模板",
    "📈 分析报表模板",
    "📝 比赛用表模板",
    "💾 下载全部模板"
])

with tabs[0]:
    st.subheader("📊 财务报表模板")
    
    template_type = st.selectbox(
        "选择财务报表模板",
        ["资产负债表", "利润表", "现金流量表", "科目余额表"],
        key="finance_template"
    )
    
    if template_type == "资产负债表":
        st.markdown("### 资产负债表模板")
        
        # 创建资产负债表
        asset_data = {
            "资产项目": ["货币资金", "应收账款", "存货", "固定资产", "无形资产", "长期投资", "其他资产"],
            "期初金额": [0.0] * 7,
            "期末金额": [0.0] * 7
        }
        df_assets = pd.DataFrame(asset_data)
        
        liability_data = {
            "负债项目": ["短期借款", "应付账款", "应交税费", "长期借款", "其他负债"],
            "期初金额": [0.0] * 5,
            "期末金额": [0.0] * 5
        }
        df_liabilities = pd.DataFrame(liability_data)
        
        equity_data = {
            "所有者权益项目": ["实收资本", "资本公积", "盈余公积", "未分配利润"],
            "期初金额": [0.0] * 4,
            "期末金额": [0.0] * 4
        }
        df_equity = pd.DataFrame(equity_data)
        
        st.markdown("#### 资产")
        edited_assets = st.data_editor(df_assets, hide_index=True, use_container_width=True, key="edit_asset")
        
        st.markdown("#### 负债")
        edited_liabilities = st.data_editor(df_liabilities, hide_index=True, use_container_width=True, key="edit_liability")
        
        st.markdown("#### 所有者权益")
        edited_equity = st.data_editor(df_equity, hide_index=True, use_container_width=True, key="edit_equity")
        
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
                st.success("✅ 平衡")
            else:
                st.error(f"❌ 不平衡 ({balance_check:+.2f}万元)")
        
        # 导出按钮
        if st.button("导出资产负债表为 Excel", use_container_width=True):
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                edited_assets.to_excel(writer, sheet_name='资产', index=False)
                edited_liabilities.to_excel(writer, sheet_name='负债', index=False)
                edited_equity.to_excel(writer, sheet_name='所有者权益', index=False)
                
                workbook = writer.book
                worksheet = writer.sheets['资产']
                worksheet.write(f'A{len(edited_assets)+5}', '资产总计')
                worksheet.write(f'C{len(edited_assets)+5}', total_assets_end)
            
            output.seek(0)
            st.download_button(
                label="📥 下载 Excel",
                data=output.getvalue(),
                file_name=f"资产负债表_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
    
    elif template_type == "利润表":
        st.markdown("### 利润表模板")
        
        profit_data = {
            "项目": [
                "一、营业收入",
                "减：营业成本",
                "税金及附加",
                "销售费用",
                "管理费用",
                "财务费用",
                "二、营业利润",
                "加：营业外收入",
                "减：营业外支出",
                "三、利润总额",
                "减：所得税费用",
                "四、净利润"
            ],
            "本期金额": [0.0] * 12,
            "累计金额": [0.0] * 12
        }
        
        df_profit = pd.DataFrame(profit_data)
        edited_profit = st.data_editor(df_profit, hide_index=True, use_container_width=True, key="edit_profit")
        
        # 自动计算
        if len(edited_profit) >= 12:
            revenue = edited_profit.loc[0, "本期金额"]
            cost = edited_profit.loc[1, "本期金额"]
            tax = edited_profit.loc[2, "本期金额"]
            selling = edited_profit.loc[3, "本期金额"]
            admin = edited_profit.loc[4, "本期金额"]
            finance = edited_profit.loc[5, "本期金额"]
            
            operating_profit = revenue - cost - tax - selling - admin - finance
            non_operating_income = edited_profit.loc[7, "本期金额"]
            non_operating_expense = edited_profit.loc[8, "本期金额"]
            total_profit = operating_profit + non_operating_income - non_operating_expense
            income_tax = edited_profit.loc[10, "本期金额"]
            net_profit = total_profit - income_tax
            
            st.divider()
            
            st.markdown("#### 计算结果")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("营业利润", f"{operating_profit:.2f}万元")
            
            with col2:
                st.metric("利润总额", f"{total_profit:.2f}万元")
            
            with col3:
                st.metric("净利润", f"{net_profit:.2f}万元")
            
            # 利润率
            if revenue > 0:
                profit_margin = net_profit / revenue * 100
                st.info(f"**净利润率**: {profit_margin:.1f}%")
        
        # 导出
        if st.button("导出利润表为 Excel", use_container_width=True):
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                edited_profit.to_excel(writer, sheet_name='利润表', index=False)
            
            output.seek(0)
            st.download_button(
                label="📥 下载 Excel",
                data=output.getvalue(),
                file_name=f"利润表_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
    
    elif template_type == "现金流量表":
        st.markdown("### 现金流量表模板")
        
        cash_flow_sections = {
            "经营活动现金流": [
                "销售商品收到的现金",
                "收到其他与经营活动有关的现金",
                "购买商品支付的现金",
                "支付给职工及为职工支付的现金",
                "支付的各项税费",
                "支付其他与经营活动有关的现金"
            ],
            "投资活动现金流": [
                "购建固定资产支付的现金",
                "投资支付的现金",
                "收到投资收益的现金"
            ],
            "筹资活动现金流": [
                "吸收投资收到的现金",
                "取得借款收到的现金",
                "偿还债务支付的现金",
                "分配股利或利润支付的现金",
                "偿付利息支付的现金"
            ]
        }
        
        st.markdown("#### 经营活动产生的现金流量")
        operating_data = {
            "项目": cash_flow_sections["经营活动现金流"],
            "金额": [0.0] * len(cash_flow_sections["经营活动现金流"])
        }
        df_operating = pd.DataFrame(operating_data)
        edited_operating = st.data_editor(df_operating, hide_index=True, use_container_width=True, key="edit_operating")
        
        operating_inflow = edited_operating.loc[0:1, "金额"].sum()
        operating_outflow = edited_operating.loc[2:, "金额"].sum()
        operating_net = operating_inflow - operating_outflow
        
        st.info(f"经营活动现金流入：{operating_inflow:.2f}万元 | 流出：{operating_outflow:.2f}万元 | 净额：{operating_net:+.2f}万元")
        
        st.markdown("#### 投资活动产生的现金流量")
        investing_data = {
            "项目": cash_flow_sections["投资活动现金流"],
            "金额": [0.0] * len(cash_flow_sections["投资活动现金流"])
        }
        df_investing = pd.DataFrame(investing_data)
        edited_investing = st.data_editor(df_investing, hide_index=True, use_container_width=True, key="edit_investing")
        
        investing_inflow = edited_investing.loc[2:, "金额"].sum()
        investing_outflow = edited_investing.loc[:1, "金额"].sum()
        investing_net = investing_inflow - investing_outflow
        
        st.info(f"投资活动现金流入：{investing_inflow:.2f}万元 | 流出：{investing_outflow:.2f}万元 | 净额：{investing_net:+.2f}万元")
        
        st.markdown("#### 筹资活动产生的现金流量")
        financing_data = {
            "项目": cash_flow_sections["筹资活动现金流"],
            "金额": [0.0] * len(cash_flow_sections["筹资活动现金流"])
        }
        df_financing = pd.DataFrame(financing_data)
        edited_financing = st.data_editor(df_financing, hide_index=True, use_container_width=True, key="edit_financing")
        
        financing_inflow = edited_financing.loc[:1, "金额"].sum()
        financing_outflow = edited_financing.loc[2:, "金额"].sum()
        financing_net = financing_inflow - financing_outflow
        
        st.info(f"筹资活动现金流入：{financing_inflow:.2f}万元 | 流出：{financing_outflow:.2f}万元 | 净额：{financing_net:+.2f}万元")
        
        st.divider()
        
        st.markdown("#### 现金流量汇总")
        
        net_cash_flow = operating_net + investing_net + financing_net
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("经营活动净额", f"{operating_net:+.2f}万元", delta_color="normal" if operating_net >= 0 else "inverse")
        
        with col2:
            st.metric("投资活动净额", f"{investing_net:+.2f}万元", delta_color="normal" if investing_net >= 0 else "inverse")
        
        with col3:
            st.metric("筹资活动净额", f"{financing_net:+.2f}万元", delta_color="normal" if financing_net >= 0 else "inverse")
        
        st.metric("现金净增加额", f"{net_cash_flow:+.2f}万元")
        
        # 导出
        if st.button("导出现金流量表为 Excel", use_container_width=True):
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                edited_operating.to_excel(writer, sheet_name='经营活动', index=False)
                edited_investing.to_excel(writer, sheet_name='投资活动', index=False)
                edited_financing.to_excel(writer, sheet_name='筹资活动', index=False)
            
            output.seek(0)
            st.download_button(
                label="📥 下载 Excel",
                data=output.getvalue(),
                file_name=f"现金流量表_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
    
    elif template_type == "科目余额表":
        st.markdown("### 科目余额表模板")
        
        account_data = {
            "科目代码": ["1001", "1002", "1122", "1405", "1601", "2001", "2202", "3001", "3002", "4001", "4002", "5001", "5002"],
            "科目名称": ["库存现金", "银行存款", "应收账款", "存货", "固定资产", "短期借款", "应付账款", "股本", "资本公积", "盈余公积", "未分配利润", "营业收入", "营业成本"],
            "期初余额": [0.0] * 13,
            "本期借方": [0.0] * 13,
            "本期贷方": [0.0] * 13,
            "期末余额": [0.0] * 13
        }
        
        df_accounts = pd.DataFrame(account_data)
        edited_accounts = st.data_editor(df_accounts, hide_index=True, use_container_width=True, key="edit_accounts")
        
        # 导出
        if st.button("导出科目余额表为 Excel", use_container_width=True):
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                edited_accounts.to_excel(writer, sheet_name='科目余额表', index=False)
            
            output.seek(0)
            st.download_button(
                label="📥 下载 Excel",
                data=output.getvalue(),
                file_name=f"科目余额表_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

with tabs[1]:
    st.subheader("💰 决策记录模板")
    
    decision_template = st.selectbox(
        "选择决策记录模板",
        ["季度决策记录表", "贷款决策记录表", "投资决策记录表", "市场竞标记录表"]
    )
    
    if decision_template == "季度决策记录表":
        st.markdown("### 季度决策记录表")
        
        quarter = st.selectbox("季度", ["Q1", "Q2", "Q3", "Q4"])
        
        decision_categories = {
            "财务决策": ["贷款申请", "贷款偿还", "利息支付", "税务申报", "应收账款贴现"],
            "投资决策": ["厂房购置", "厂房租赁", "设备购置", "研发投入", "市场开拓"],
            "采购决策": ["原料采购", "人员招聘", "外包加工"],
            "生产决策": ["生产排产", "产品生产", "质量控制"],
            "市场决策": ["广告投放", "产品定价", "订单竞标", "客户关系"]
        }
        
        decision_records = []
        
        for category, items in decision_categories.items():
            st.markdown(f"#### {category}")
            for item in items:
                col1, col2, col3 = st.columns([3, 2, 2])
                with col1:
                    st.write(f"{item}")
                with col2:
                    decision_val = st.number_input(f"金额", key=f"dec_{category}_{item}", min_value=0.0, step=10.0)
                with col3:
                    decision_status = st.selectbox("状态", ["未执行", "已执行", "取消"], key=f"status_{category}_{item}")
                
                if decision_val > 0:
                    decision_records.append({
                        "类别": category,
                        "决策项": item,
                        "金额": decision_val,
                        "状态": decision_status
                    })
        
        if decision_records:
            df_decisions = pd.DataFrame(decision_records)
            
            st.divider()
            
            st.markdown("#### 决策汇总")
            summary = df_decisions.groupby("类别")["金额"].sum().reset_index()
            st.dataframe(summary, use_container_width=True, hide_index=True)
            
            st.metric("决策总金额", f"{df_decisions['金额'].sum():.2f}万元")
            
            # 导出
            if st.button("导出季度决策记录为 Excel", use_container_width=True):
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    df_decisions.to_excel(writer, sheet_name='决策记录', index=False)
                    summary.to_excel(writer, sheet_name='汇总', index=False)
                
                output.seek(0)
                st.download_button(
                    label="📥 下载 Excel",
                    data=output.getvalue(),
                    file_name=f"季度决策记录_{quarter}_{datetime.now().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
    
    elif decision_template == "贷款决策记录表":
        st.markdown("### 贷款决策记录表")
        
        loan_records = {
            "贷款类型": ["短期贷款", "长期贷款", "民间融资"],
            "贷款金额": [0.0, 0.0, 0.0],
            "年利率 (%)": [5.0, 6.0, 10.0],
            "贷款期限 (季度)": [4, 8, 2],
            "季度利息": [0.0, 0.0, 0.0],
            "还款方式": ["到期还本付息", "按季付息到期还本", "到期一次性还本付息"]
        }
        
        df_loans = pd.DataFrame(loan_records)
        edited_loans = st.data_editor(df_loans, hide_index=True, use_container_width=True, key="edit_loans")
        
        # 计算
        total_loan = edited_loans["贷款金额"].sum()
        total_quarterly_interest = sum([
            edited_loans.loc[i, "贷款金额"] * edited_loans.loc[i, "年利率 (%)"] / 4 / 100
            for i in range(len(edited_loans))
        ])
        
        st.divider()
        
        st.markdown("#### 贷款汇总")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("贷款总额", f"{total_loan:.2f}万元")
        
        with col2:
            st.metric("季度利息总额", f"{total_quarterly_interest:.2f}万元")
        
        # 导出
        if st.button("导出贷款决策记录为 Excel", use_container_width=True):
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                edited_loans.to_excel(writer, sheet_name='贷款记录', index=False)
            
            output.seek(0)
            st.download_button(
                label="📥 下载 Excel",
                data=output.getvalue(),
                file_name=f"贷款决策记录_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
    
    elif decision_template == "投资决策记录表":
        st.markdown("### 投资决策记录表")
        
        investment_data = {
            "投资项目": ["厂房购置", "厂房租赁", "生产线投资", "设备购置", "研发投入", "市场开拓", "其他投资"],
            "投资金额": [0.0] * 7,
            "预计回报周期 (季度)": [0] * 7,
            "预计 ROI (%)": [0.0] * 7,
            "决策状态": ["未决策"] * 7,
            "备注": [""] * 7
        }
        
        df_investment = pd.DataFrame(investment_data)
        edited_investment = st.data_editor(df_investment, hide_index=True, use_container_width=True, key="edit_investment")
        
        st.divider()
        
        total_investment = edited_investment["投资金额"].sum()
        st.metric("投资总额", f"{total_investment:.2f}万元")
        
        # 导出
        if st.button("导出投资决策记录为 Excel", use_container_width=True):
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                edited_investment.to_excel(writer, sheet_name='投资记录', index=False)
            
            output.seek(0)
            st.download_button(
                label="📥 下载 Excel",
                data=output.getvalue(),
                file_name=f"投资决策记录_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
    
    elif decision_template == "市场竞标记录表":
        st.markdown("### 市场竞标记录表")
        
        st.markdown("#### 竞标记录")
        
        bid_data = {
            "市场": ["本地市场", "区域市场", "国内市场", "亚洲市场", "国际市场"],
            "产品": ["P1", "P2", "P3", "P4"],
            "报价 (元/件)": [0.0] * 5,
            "广告投入 (万元)": [0.0] * 5,
            "预计中标率 (%)": [0.0] * 5,
            "实际中标量 (件)": [0] * 5,
            "实际销售收入 (万元)": [0.0] * 5
        }
        
        df_bids = pd.DataFrame(bid_data)
        edited_bids = st.data_editor(df_bids, hide_index=True, use_container_width=True, key="edit_bids")
        
        st.divider()
        
        total_ad = edited_bids["广告投入 (万元)"].sum()
        total_revenue = edited_bids["实际销售收入 (万元)"].sum()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("广告总投入", f"{total_ad:.2f}万元")
        
        with col2:
            if total_ad > 0:
                ad_roi = (total_revenue - total_ad) / total_ad * 100
                st.metric("广告 ROI", f"{ad_roi:.1f}%", delta_color="normal" if ad_roi > 0 else "inverse")
        
        # 导出
        if st.button("导出市场竞标记录为 Excel", use_container_width=True):
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                edited_bids.to_excel(writer, sheet_name='竞标记录', index=False)
            
            output.seek(0)
            st.download_button(
                label="📥 下载 Excel",
                data=output.getvalue(),
                file_name=f"市场竞标记录_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

with tabs[2]:
    st.subheader("📈 分析报表模板")
    
    analysis_template = st.selectbox(
        "选择分析报表模板",
        ["财务比率分析表", "成本构成分析表", "预算执行分析表", "盈亏平衡分析表"]
    )
    
    if analysis_template == "财务比率分析表":
        st.markdown("### 财务比率分析表")
        
        ratio_data = {
            "比率类别": ["盈利能力", "盈利能力", "盈利能力", "营运能力", "营运能力", "偿债能力", "偿债能力", "发展能力", "发展能力"],
            "比率名称": ["净利润率", "ROE", "ROA", "总资产周转率", "存货周转率", "流动比率", "资产负债率", "销售增长率", "资产增长率"],
            "计算公式": [
                "净利润/营业收入×100%",
                "净利润/净资产×100%",
                "净利润/总资产×100%",
                "营业收入/总资产",
                "营业成本/平均存货",
                "流动资产/流动负债",
                "负债总额/资产总额×100%",
                "(本期销售 - 上期销售)/上期销售×100%",
                "(本期资产 - 上期资产)/上期资产×100%"
            ],
            "本期值": [0.0] * 9,
            "上期值": [0.0] * 9,
            "行业标准": [10.0, 20.0, 8.0, 1.0, 5.0, 1.2, 55.0, 15.0, 10.0],
            "评分": [0] * 9
        }
        
        df_ratios = pd.DataFrame(ratio_data)
        edited_ratios = st.data_editor(df_ratios, hide_index=True, use_container_width=True, key="edit_ratios")
        
        # 导出
        if st.button("导出财务比率分析表为 Excel", use_container_width=True):
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                edited_ratios.to_excel(writer, sheet_name='财务比率', index=False)
            
            output.seek(0)
            st.download_button(
                label="📥 下载 Excel",
                data=output.getvalue(),
                file_name=f"财务比率分析表_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
    
    elif analysis_template == "成本构成分析表":
        st.markdown("### 成本构成分析表")
        
        cost_data = {
            "成本项目": ["直接材料", "直接人工", "制造费用", "管理费用", "销售费用", "财务费用", "研发费用", "其他费用"],
            "金额 (万元)": [0.0] * 8,
            "占比 (%)": [0.0] * 8,
            "上期占比 (%)": [0.0] * 8,
            "变动分析": ["-"] * 8
        }
        
        df_cost = pd.DataFrame(cost_data)
        edited_cost = st.data_editor(df_cost, hide_index=True, use_container_width=True, key="edit_cost")
        
        # 自动计算占比
        total_cost = edited_cost["金额 (万元)"].sum()
        if total_cost > 0:
            edited_cost["占比 (%)"] = edited_cost["金额 (万元)"] / total_cost * 100
        
        st.divider()
        
        st.metric("总成本", f"{total_cost:.2f}万元")
        
        # 饼图数据预览
        st.markdown("#### 成本构成预览")
        st.dataframe(edited_cost[["成本项目", "金额 (万元)", "占比 (%)"]], use_container_width=True, hide_index=True)
        
        # 导出
        if st.button("导出成本构成分析表为 Excel", use_container_width=True):
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                edited_cost.to_excel(writer, sheet_name='成本分析', index=False)
            
            output.seek(0)
            st.download_button(
                label="📥 下载 Excel",
                data=output.getvalue(),
                file_name=f"成本构成分析表_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
    
    elif analysis_template == "预算执行分析表":
        st.markdown("### 预算执行分析表")
        
        budget_data = {
            "预算项目": ["销售收入", "直接材料", "直接人工", "制造费用", "管理费用", "销售费用", "财务费用", "税费", "净利润"],
            "预算金额": [0.0] * 9,
            "实际金额": [0.0] * 9,
            "差异金额": [0.0] * 9,
            "差异率 (%)": [0.0] * 9,
            "评价": ["待评价"] * 9
        }
        
        df_budget = pd.DataFrame(budget_data)
        edited_budget = st.data_editor(df_budget, hide_index=True, use_container_width=True, key="edit_budget")
        
        # 自动计算
        edited_budget["差异金额"] = edited_budget["实际金额"] - edited_budget["预算金额"]
        edited_budget["差异率 (%)"] = edited_budget.apply(
            lambda row: (row["差异金额"] / row["预算金额"] * 100) if row["预算金额"] > 0 else 0, axis=1
        )
        edited_budget["评价"] = edited_budget["差异率 (%)"].apply(
            lambda x: "✅ 优秀" if abs(x) < 5 else ("👌 良好" if abs(x) < 10 else ("⚠️ 关注" if abs(x) < 20 else "❌ 异常"))
        )
        
        st.divider()
        
        st.markdown("#### 预算执行汇总")
        st.dataframe(edited_budget, use_container_width=True, hide_index=True)
        
        # 导出
        if st.button("导出预算执行分析表为 Excel", use_container_width=True):
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                edited_budget.to_excel(writer, sheet_name='预算执行', index=False)
            
            output.seek(0)
            st.download_button(
                label="📥 下载 Excel",
                data=output.getvalue(),
                file_name=f"预算执行分析表_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
    
    elif analysis_template == "盈亏平衡分析表":
        st.markdown("### 盈亏平衡分析表")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fixed_cost = st.number_input("固定成本 (万元)", min_value=0.0, value=100.0, step=10.0)
            unit_price = st.number_input("单价 (万元)", min_value=0.01, value=2.0, step=0.1)
        
        with col2:
            unit_variable_cost = st.number_input("单位变动成本 (万元)", min_value=0.01, value=1.2, step=0.1)
            target_profit = st.number_input("目标利润 (万元)", min_value=0.0, value=50.0, step=10.0)
        
        # 计算
        unit_contribution = unit_price - unit_variable_cost
        contribution_rate = unit_contribution / unit_price * 100 if unit_price > 0 else 0
        
        break_even_volume = fixed_cost / unit_contribution if unit_contribution > 0 else 0
        break_even_revenue = break_even_volume * unit_price
        
        target_volume = (fixed_cost + target_profit) / unit_contribution if unit_contribution > 0 else 0
        target_revenue = target_volume * unit_price
        
        st.divider()
        
        st.markdown("#### 计算结果")
        
        col_result1, col_result2, col_result3 = st.columns(3)
        
        with col_result1:
            st.metric("单位边际贡献", f"{unit_contribution:.2f}万元")
            st.write(f"边际贡献率：{contribution_rate:.1f}%")
        
        with col_result2:
            st.metric("保本销量", f"{break_even_volume:.0f}件")
            st.write(f"保本收入：{break_even_revenue:.2f}万元")
        
        with col_result3:
            st.metric("目标销量", f"{target_volume:.0f}件")
            st.write(f"目标收入：{target_revenue:.2f}万元")
        
        # 敏感性分析表格
        st.markdown("#### 敏感性分析")
        
        sensitivity_data = []
        for price_change in [-10, -5, 0, 5, 10]:
            adjusted_price = unit_price * (1 + price_change / 100)
            adjusted_contribution = adjusted_price - unit_variable_cost
            adjusted_break_even = fixed_cost / adjusted_contribution if adjusted_contribution > 0 else 0
            
            sensitivity_data.append({
                "价格变动": f"{price_change:+.0f}%",
                "调整后单价": f"{adjusted_price:.2f}万元",
                "边际贡献": f"{adjusted_contribution:.2f}万元",
                "保本销量": f"{adjusted_break_even:.0f}件"
            })
        
        df_sensitivity = pd.DataFrame(sensitivity_data)
        st.dataframe(df_sensitivity, use_container_width=True, hide_index=True)
        
        # 导出
        if st.button("导出盈亏平衡分析表为 Excel", use_container_width=True):
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                summary_data = {
                    "指标": ["固定成本", "单价", "单位变动成本", "目标利润", "单位边际贡献", "边际贡献率", "保本销量", "保本收入", "目标销量", "目标收入"],
                    "数值": [
                        fixed_cost, unit_price, unit_variable_cost, target_profit,
                        unit_contribution, contribution_rate, break_even_volume,
                        break_even_revenue, target_volume, target_revenue
                    ]
                }
                df_summary = pd.DataFrame(summary_data)
                df_summary.to_excel(writer, sheet_name='汇总', index=False)
                
                df_sensitivity.to_excel(writer, sheet_name='敏感性分析', index=False)
            
            output.seek(0)
            st.download_button(
                label="📥 下载 Excel",
                data=output.getvalue(),
                file_name=f"盈亏平衡分析表_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

with tabs[3]:
    st.subheader("📝 比赛用表模板")
    
    competition_template = st.selectbox(
        "选择比赛用表模板",
        ["比赛成绩记录表", "团队分工表", "时间规划表", "检查清单模板"]
    )
    
    if competition_template == "比赛成绩记录表":
        st.markdown("### 比赛成绩记录表")
        
        score_data = {
            "轮次": [1, 2, 3, 4],
            "日期": [""] * 4,
            "排名": [0] * 4,
            "参赛队伍数": [0] * 4,
            "得分": [0] * 4,
            "盈利得分": [0] * 4,
            "营运得分": [0] * 4,
            "偿债得分": [0] * 4,
            "发展得分": [0] * 4,
            "预算得分": [0] * 4,
            "扣分": [0] * 4,
            "备注": [""] * 4
        }
        
        df_scores = pd.DataFrame(score_data)
        edited_scores = st.data_editor(df_scores, hide_index=True, use_container_width=True, key="edit_scores")
        
        # 计算
        total_score = edited_scores["得分"].sum()
        avg_score = edited_scores["得分"].mean()
        
        st.divider()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("总分", f"{total_score}分")
        
        with col2:
            st.metric("平均分", f"{avg_score:.1f}分")
        
        # 导出
        if st.button("导出比赛成绩记录表为 Excel", use_container_width=True):
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                edited_scores.to_excel(writer, sheet_name='成绩记录', index=False)
            
            output.seek(0)
            st.download_button(
                label="📥 下载 Excel",
                data=output.getvalue(),
                file_name=f"比赛成绩记录表_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
    
    elif competition_template == "团队分工表":
        st.markdown("### 团队分工表")
        
        st.markdown("#### 角色职责")
        
        role_data = {
            "角色": ["CEO", "CFO", "COO", "CMO"],
            "成员姓名": [""] * 4,
            "主要职责": [
                "整体战略、投融资决策、团队协调",
                "财务管理、预算编制、报税、资金规划",
                "生产管理、产能投资、采购决策",
                "市场营销、广告投放、产品定价、竞标"
            ],
            "使用模块": [
                "贷款决策助手、产能规划工具",
                "现金流预测、财务比率、预算编制助手",
                "产能规划工具、贷款决策助手",
                "报价策略计算器、广告 ROI 分析器"
            ],
            "决策时机": [
                "每季度初、投资决策时",
                "每季度初/末、报税时",
                "每季度初、产能评估时",
                "竞标前、定价时"
            ]
        }
        
        df_roles = pd.DataFrame(role_data)
        edited_roles = st.data_editor(df_roles, hide_index=True, use_container_width=True, key="edit_roles")
        
        # 导出
        if st.button("导出团队分工表为 Excel", use_container_width=True):
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                edited_roles.to_excel(writer, sheet_name='团队分工', index=False)
            
            output.seek(0)
            st.download_button(
                label="📥 下载 Excel",
                data=output.getvalue(),
                file_name=f"团队分工表_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
    
    elif competition_template == "时间规划表":
        st.markdown("### 时间规划表")
        
        time_data = {
            "阶段": ["预算编制", "投融资决策", "经营决策", "报税", "复盘调整"],
            "负责人": ["CFO", "CEO+CFO", "全员", "CFO", "全员"],
            "时长 (分钟)": [5, 10, 25, 5, 5],
            "开始时间": ["00:00", "00:05", "00:15", "00:40", "00:45"],
            "结束时间": ["00:05", "00:15", "00:40", "00:45", "00:50"],
            "关键事项": [
                "4 张预算表、偏差控制",
                "贷款申请/偿还、利息计算",
                "厂房/设备/采购/生产/竞标",
                "增值税、所得税申报",
                "财务比率计算、经验总结"
            ],
            "使用模块": [
                "预算编制助手",
                "贷款决策助手、现金流预测",
                "报价策略、广告 ROI、产能规划",
                "现金流预测",
                "财务比率计算器、复盘记录表"
            ]
        }
        
        df_time = pd.DataFrame(time_data)
        
        st.dataframe(df_time, use_container_width=True, hide_index=True)
        
        # 导出
        if st.button("导出时间规划表为 Excel", use_container_width=True):
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df_time.to_excel(writer, sheet_name='时间规划', index=False)
            
            output.seek(0)
            st.download_button(
                label="📥 下载 Excel",
                data=output.getvalue(),
                file_name=f"时间规划表_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
    
    elif competition_template == "检查清单模板":
        st.markdown("### 检查清单模板")
        
        st.markdown("#### 赛前检查清单")
        
        checklist_data = {
            "检查项": [
                "软件安装与测试完成",
                "团队成员分工明确",
                "熟悉比赛规则",
                "打印使用指南和评分规则",
                "准备备用电脑",
                "计算器、纸笔准备就绪"
            ],
            "负责人": ["全员", "CEO", "全员", "CFO", "CEO", "COO"],
            "状态": ["未完成"] * 6,
            "备注": [""] * 6
        }
        
        df_checklist = pd.DataFrame(checklist_data)
        edited_checklist = st.data_editor(df_checklist, hide_index=True, use_container_width=True, key="edit_checklist")
        
        # 导出
        if st.button("导出检查清单为 Excel", use_container_width=True):
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                edited_checklist.to_excel(writer, sheet_name='检查清单', index=False)
            
            output.seek(0)
            st.download_button(
                label="📥 下载 Excel",
                data=output.getvalue(),
                file_name=f"检查清单_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

with tabs[4]:
    st.subheader("💾 下载全部模板")
    
    st.markdown("""
    ### 批量下载模板包
    
    包含以下模板类别：
    - 📊 财务报表模板（资产负债表、利润表、现金流量表、科目余额表）
    - 💰 决策记录模板（季度决策、贷款决策、投资决策、市场竞标）
    - 📈 分析报表模板（财务比率、成本构成、预算执行、盈亏平衡）
    - 📝 比赛用表模板（成绩记录、团队分工、时间规划、检查清单）
    """)
    
    if st.button("📦 下载全部模板包 (Excel)", type="primary", use_container_width=True):
        output = io.BytesIO()
        
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            # 创建示例工作表
            pd.DataFrame({"模板": ["财务报表", "决策记录", "分析报表", "比赛用表"]}).to_excel(writer, sheet_name='目录', index=False)
        
        output.seek(0)
        
        st.success("✅ 模板包生成成功!")
        st.download_button(
            label="📥 点击下载模板包",
            data=output.getvalue(),
            file_name=f"学创杯_模板大全_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
    
    st.divider()
    
    st.markdown("""
    ### 模板使用说明
    
    1. **选择模板**: 在上方标签页选择需要的模板类型
    2. **在线填写**: 直接在表格中输入数据（可选）
    3. **导出 Excel**: 点击"导出 Excel"按钮下载
    4. **离线使用**: 下载的 Excel 文件可离线编辑使用
    
    ### 注意事项
    
    - 所有金额单位为**万元**
    - 百分比直接填写数字（如 10 表示 10%）
    - 日期格式：YYYY-MM-DD
    - 导出的 Excel 文件可以用 Microsoft Excel 或 WPS 编辑
    """)

# 页脚
st.divider()
st.caption("学创杯比赛辅助工具 v2.1 - 模板中心")
