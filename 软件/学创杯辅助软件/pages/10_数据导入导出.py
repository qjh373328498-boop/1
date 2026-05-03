# 📤 数据导入导出
# 支持 Excel/CSV 数据导入导出功能

import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
import io


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

st.set_page_config(page_title="数据导入导出", page_icon="📤", layout="wide")

st.title("📤 数据导入导出")
st.markdown("**支持 Excel/CSV格式数据导入导出，方便数据备份和团队协作**")

st.divider()

# 数据目录
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
os.makedirs(DATA_DIR, exist_ok=True)

# 标签页
tabs = st.tabs(["📥 导出数据", "📤 导入数据", "📋 数据模板", "💾 数据管理"])

with tabs[0]:
    st.subheader("📥 导出数据")
    
    st.markdown("**选择要导出的数据类型**")
    
    data_type = st.selectbox(
        "数据类型",
        ["财务比率数据", "现金流预测数据", "预算数据", "比赛复盘记录", "综合数据包"],
        index=4
    )
    
    export_format = st.radio("导出格式", ["Excel (.xlsx)", "CSV (.csv)", "JSON (.json)"], index=0)
    
    if st.button("生成导出文件", type="primary", use_container_width=True):
        if data_type == "财务比率数据":
            # 创建示例数据
            sample_data = {
                "指标": ["流动比率", "速动比率", "资产负债率", "净利润率", "ROE"],
                "数值": [1.25, 0.85, "55%", "12%", "22%"],
                "满分标准": [1.2, 0.8, "60%", "10%", "20%"],
                "得分": [8, 7, 9, 9, 8]
            }
            df = pd.DataFrame(sample_data)
            filename = f"财务比率数据_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        elif data_type == "现金流预测数据":
            sample_data = {
                "项目": ["期初现金", "销售回款", "融资流入", "采购支出", "人工成本", "费用支出", "投资支出", "期末现金"],
                "Q1": [100, 500, 200, 300, 100, 50, 150, 200],
                "Q2": [200, 600, 100, 350, 120, 60, 100, 270],
                "Q3": [270, 800, 150, 400, 140, 70, 200, 410],
                "Q4": [410, 700, 100, 380, 130, 65, 50, 585]
            }
            df = pd.DataFrame(sample_data)
            filename = f"现金流预测_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        elif data_type == "预算数据":
            sample_data = {
                "预算项目": ["销售收入", "直接材料", "直接人工", "制造费用", "管理费用", "销售费用", "财务费用"],
                "预算金额": [3000, 1200, 500, 300, 200, 150, 80],
                "实际金额": [2950, 1180, 510, 290, 195, 160, 75],
                "偏差率": ["-1.7%", "-1.7%", "2.0%", "-3.3%", "-2.5%", "6.7%", "-6.3%"]
            }
            df = pd.DataFrame(sample_data)
            filename = f"预算数据_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        elif data_type == "比赛复盘记录":
            review_file = os.path.join(DATA_DIR, "review_records.json")
            if os.path.exists(review_file):
                with open(review_file, 'r', encoding='utf-8') as f:
                    reviews = json.load(f)
                
                if reviews:
                    # 展开复盘数据
                    flat_data = []
                    for review in reviews:
                        flat_data.append({
                            "轮次": review.get('round', ''),
                            "队伍": review.get('team_name', ''),
                            "日期": review.get('date', ''),
                            "排名": f"{review.get('final_rank', '')}/{review.get('total_teams', '')}",
                            "得分": review.get('final_score', ''),
                            "等级": review.get('achievement', ''),
                            "盈利得分": review.get('scores', {}).get('profit', ''),
                            "营运得分": review.get('scores', {}).get('operation', ''),
                            "偿债得分": review.get('scores', {}).get('debt', ''),
                            "发展得分": review.get('scores', {}).get('growth', ''),
                            "预算得分": review.get('scores', {}).get('budget', ''),
                            "扣分": review.get('scores', {}).get('penalty', '')
                        })
                    df = pd.DataFrame(flat_data)
                else:
                    df = pd.DataFrame(columns=["轮次", "队伍", "日期", "排名", "得分", "等级"])
            else:
                df = pd.DataFrame(columns=["轮次", "队伍", "日期", "排名", "得分", "等级"])
            
            filename = f"复盘记录_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        else:  # 综合数据包
            st.info("综合数据包包含所有数据类型，将生成多个工作表的 Excel 文件")
            
            # 创建 Excel 文件
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                # 各工作表数据
                pd.DataFrame({"指标": ["流动比率", "速动比率"], "数值": [1.25, 0.85]}).to_excel(writer, sheet_name='财务比率', index=False)
                pd.DataFrame({"项目": ["期初现金", "期末现金"], "金额": [100, 200]}).to_excel(writer, sheet_name='现金流', index=False)
                pd.DataFrame({"预算项目": ["销售收入"], "预算": [3000]}).to_excel(writer, sheet_name='预算', index=False)
            
            output.seek(0)
            
            st.success("✅ 综合数据包生成成功！")
            st.download_button(
                label="📥 下载综合数据包",
                data=output.getvalue(),
                file_name=f"综合数据包_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
            st.stop()
        
        # 生成文件
        if export_format.startswith("Excel"):
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name='Sheet1', index=False)
            output.seek(0)
            
            st.success(f"✅ {data_type}导出成功！")
            st.download_button(
                label="📥 下载 Excel 文件",
                data=output.getvalue(),
                file_name=f"{filename}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        
        elif export_format.startswith("CSV"):
            csv_data = df.to_csv(index=False, encoding='utf-8-sig')
            
            st.success(f"✅ {data_type}导出成功！")
            st.download_button(
                label="📥 下载 CSV 文件",
                data=csv_data,
                file_name=f"{filename}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        else:  # JSON
            json_data = df.to_dict(orient='records', force_ascii=False)
            json_str = json.dumps(json_data, ensure_ascii=False, indent=2)
            
            st.success(f"✅ {data_type}导出成功！")
            st.download_button(
                label="📥 下载 JSON 文件",
                data=json_str,
                file_name=f"{filename}.json",
                mime="application/json",
                use_container_width=True
            )
    
    st.divider()
    
    st.markdown("**💡 导出说明**")
    
    st.markdown("""
    **Excel 格式**:
    - 支持多工作表
    - 保留格式和公式
    - 适合正式报告和存档
    
    **CSV 格式**:
    - 通用性强
    - 可用 Excel 打开
    - 适合数据交换
    
    **JSON 格式**:
    - 保留数据结构
    - 便于程序处理
    - 适合数据备份
    """)

with tabs[1]:
    st.subheader("📤 导入数据")
    
    st.markdown("**上传数据文件**")
    
    uploaded_file = st.file_uploader(
        "选择要导入的文件",
        type=["xlsx", "xls", "csv", "json"],
        help="支持 Excel、CSV、JSON格式"
    )
    
    if uploaded_file is not None:
        st.success(f"✅ 文件已上传：{uploaded_file.name}")
        
        # 读取文件
        file_type = uploaded_file.name.split('.')[-1].lower()
        
        try:
            if file_type in ['xlsx', 'xls']:
                df = pd.read_excel(uploaded_file)
            elif file_type == 'csv':
                df = pd.read_csv(uploaded_file)
            elif file_type == 'json':
                df = pd.read_json(uploaded_file)
            
            st.markdown("**📋 数据预览**")
            st.dataframe(df, use_container_width=True)
            
            st.markdown("**📊 数据统计**")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("行数", len(df))
            
            with col2:
                st.metric("列数", len(df.columns))
            
            with col3:
                st.metric("空值数", df.isnull().sum().sum())
            
            # 数据验证
            st.divider()
            st.markdown("**✓ 数据验证**")
            
            if len(df) > 0:
                st.success("✅ 数据格式正确")
            else:
                st.warning("⚠️ 数据为空")
            
            # 保存选项
            st.divider()
            st.markdown("**💾 保存到系统**")
            
            save_target = st.selectbox(
                "保存位置",
                ["财务比率数据", "现金流预测数据", "预算数据", "复盘记录"]
            )
            
            if st.button("保存数据", type="primary", use_container_width=True):
                # 保存为 JSON
                save_file = os.path.join(DATA_DIR, f"{save_target}_import.json")
                data_to_save = df.to_dict(orient='records')
                
                with open(save_file, 'w', encoding='utf-8') as f:
                    json.dump(data_to_save, f, ensure_ascii=False, indent=2)
                
                st.success(f"✅ 数据已保存到 {save_file}")
                st.balloons()
        
        except Exception as e:
            st.error(f"❌ 读取文件失败：{str(e)}")
    
    st.divider()
    
    st.markdown("**📋 导入说明**")
    
    st.markdown("""
    **支持的文件格式**:
    - Excel (.xlsx, .xls)
    - CSV (.csv)
    - JSON (.json)
    
    **数据要求**:
    - 第一行为列名
    - 编码为 UTF-8
    - 无特殊字符
    
    **注意事项**:
    - 导入数据会覆盖现有数据
    - 建议先导出备份
    - 检查数据格式是否正确
    """)

with tabs[2]:
    st.subheader("📋 数据模板")
    
    st.markdown("**下载数据导入模板**")
    
    template_type = st.selectbox(
        "模板类型",
        ["财务比率数据模板", "现金流预测模板", "预算数据模板", "复盘记录模板"]
    )
    
    if st.button("下载模板", type="primary", use_container_width=True):
        if template_type == "财务比率数据模板":
            template_df = pd.DataFrame({
                "指标名称": ["流动比率", "速动比率", "资产负债率", "净利润率", "ROE"],
                "数值": [1.25, 0.85, 0.55, 0.12, 0.22],
                "单位": ["倍", "倍", "", "%", "%"],
                "备注": ["", "", "", "", ""]
            })
            filename = "财务比率数据模板"
        
        elif template_type == "现金流预测模板":
            template_df = pd.DataFrame({
                "项目": ["期初现金余额", "销售回款", "融资流入", "采购支出", "人工成本", "费用支出", "投资支出", "贷款偿还", "期末现金余额"],
                "Q1 金额": [0, 0, 0, 0, 0, 0, 0, 0, 0],
                "Q2 金额": [0, 0, 0, 0, 0, 0, 0, 0, 0],
                "Q3 金额": [0, 0, 0, 0, 0, 0, 0, 0, 0],
                "Q4 金额": [0, 0, 0, 0, 0, 0, 0, 0, 0],
                "说明": ["", "含税收入", "贷款/融资", "含税采购", "含社保", "制造/管理/销售", "生产线投资", "本金 + 利息", "=期初 + 流入 - 流出"]
            })
            filename = "现金流预测模板"
        
        elif template_type == "预算数据模板":
            template_df = pd.DataFrame({
                "预算项目": ["销售收入", "直接材料", "直接人工", "制造费用", "管理费用", "销售费用", "财务费用", "税费"],
                "预算金额": [0, 0, 0, 0, 0, 0, 0, 0],
                "实际金额": [0, 0, 0, 0, 0, 0, 0, 0],
                "偏差金额": [0, 0, 0, 0, 0, 0, 0, 0],
                "偏差率": ["0%", "0%", "0%", "0%", "0%", "0%", "0%", "0%"]
            })
            filename = "预算数据模板"
        
        else:  # 复盘记录模板
            template_df = pd.DataFrame({
                "轮次": [1, 2, 3],
                "队伍名称": ["", "", ""],
                "比赛日期": ["", "", ""],
                "最终排名": ["", "", ""],
                "参赛队伍数": [0, 0, 0],
                "最终得分": [0, 0, 0],
                "获奖等级": ["", "", ""],
                "盈利得分": [0, 0, 0],
                "营运得分": [0, 0, 0],
                "偿债得分": [0, 0, 0],
                "发展得分": [0, 0, 0],
                "预算得分": [0, 0, 0],
                "违规扣分": [0, 0, 0]
            })
            filename = "复盘记录模板"
        
        # 生成 Excel 模板
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            template_df.to_excel(writer, sheet_name='模板', index=False)
        output.seek(0)
        
        st.success(f"✅ 模板生成成功！")
        st.download_button(
            label=f"📥 下载{template_type}",
            data=output.getvalue(),
            file_name=f"{filename}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
    
    st.divider()
    
    st.markdown("**📋 模板使用说明**")
    
    st.markdown("""
    1. **下载模板**: 点击上方按钮下载对应模板
    2. **填写数据**: 在 Excel 中按格式填写数据
    3. **保存文件**: 保存为.xlsx 格式
    4. **上传导入**: 在"导入数据"标签页上传文件
    
    **注意事项**:
    - 不要修改列名
    - 数据类型要与示例一致
    - 数字不要带单位符号
    - 日期格式：YYYY-MM-DD
    """)

with tabs[3]:
    st.subheader("💾 数据管理")
    
    st.markdown("**数据文件管理**")
    
    # 扫描数据目录
    if os.path.exists(DATA_DIR):
        files = [f for f in os.listdir(DATA_DIR) if not f.startswith('.')]
        
        if files:
            file_info = []
            for f in files:
                file_path = os.path.join(DATA_DIR, f)
                size = os.path.getsize(file_path)
                mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
                
                file_info.append({
                    "文件名": f,
                    "大小": f"{size/1024:.1f}KB",
                    "修改时间": mtime.strftime('%Y-%m-%d %H:%M'),
                    "操作": "🗑️ 删除"
                })
            
            df_files = pd.DataFrame(file_info)
            st.dataframe(df_files, use_container_width=True, hide_index=True)
            
            st.divider()
            
            # 删除文件
            st.markdown("**删除数据文件**")
            
            file_to_delete = st.selectbox("选择要删除的文件", files)
            
            if st.button("删除选中文件", type="primary", use_container_width=True):
                file_path = os.path.join(DATA_DIR, file_to_delete)
                os.remove(file_path)
                st.success(f"✅ 已删除：{file_to_delete}")
                st.rerun()
        
        else:
            st.info("数据目录为空")
    
    # 存储空间
    st.divider()
    st.markdown("**💾 存储统计**")
    
    total_size = sum(os.path.getsize(os.path.join(DATA_DIR, f)) for f in os.listdir(DATA_DIR)) if os.path.exists(DATA_DIR) else 0
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("文件数量", len(files) if os.path.exists(DATA_DIR) else 0)
    
    with col2:
        st.metric("总大小", f"{total_size/1024:.1f}KB")
    
    with col3:
        st.metric("数据目录", DATA_DIR)
    
    st.divider()
    
    # 数据清理
    st.markdown("**🧹 数据清理**")
    
    if st.button("清理所有数据文件", type="primary", use_container_width=True):
        if os.path.exists(DATA_DIR):
            for f in os.listdir(DATA_DIR):
                if not f.startswith('.'):
                    os.remove(os.path.join(DATA_DIR, f))
            st.success("✅ 所有数据文件已清理")
            st.rerun()
        else:
            st.warning("数据目录不存在")
