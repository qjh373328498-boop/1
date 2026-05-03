# 👥 团队协作
# 支持多角色分工和数据共享

import streamlit as st
import pandas as pd
import json
import os
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

st.set_page_config(page_title="团队协作", page_icon="👥", layout="wide")

st.title("👥 团队协作")
st.markdown("**支持多角色分工、数据共享和决策审批流程**")

st.divider()

# 数据目录
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
os.makedirs(DATA_DIR, exist_ok=True)
TEAM_FILE = os.path.join(DATA_DIR, "team_info.json")
DECISION_FILE = os.path.join(DATA_DIR, "decisions.json")

# 加载数据
def load_team():
    if os.path.exists(TEAM_FILE):
        with open(TEAM_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"members": [], "current_round": 1}

def save_team(data):
    with open(TEAM_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_decisions():
    if os.path.exists(DECISION_FILE):
        with open(DECISION_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_decisions(data):
    with open(DECISION_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

team_data = load_team()
decisions = load_decisions()

# 侧边栏
with st.sidebar:
    st.header("👤 当前用户")
    
    current_user = st.selectbox(
        "选择角色",
        ["未设置"] + ([m["name"] for m in team_data.get("members", [])]),
        index=0
    )
    
    if current_user != "未设置":
        member = next((m for m in team_data["members"] if m["name"] == current_user), None)
        if member:
            st.info(f"**角色**: {member.get('role', '未设置')}")
            st.write(f"**权限**: {member.get('permission', '普通')}")
    
    st.divider()
    
    st.header("⚙️ 团队设置")
    
    if st.button("⚙️ 管理团队", use_container_width=True):
        st.session_state.show_team_management = True

st.divider()

# 团队管理
if st.session_state.get("show_team_management", False):
    st.subheader("⚙️ 团队管理")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**➕ 添加成员**")
        
        new_name = st.text_input("成员姓名", key="new_name")
        new_role = st.selectbox("角色", ["CEO", "CFO", "COO", "CMO"], key="new_role")
        new_permission = st.selectbox("权限", ["决策权", "建议权", "查看权"], key="new_perm")
        
        if st.button("添加成员", type="primary", use_container_width=True):
            if new_name:
                team_data.setdefault("members", []).append({
                    "name": new_name,
                    "role": new_role,
                    "permission": new_permission,
                    "added_date": datetime.now().strftime('%Y-%m-%d')
                })
                save_team(team_data)
                st.success(f"✅ 已添加：{new_name} ({new_role})")
                st.rerun()
    
    with col2:
        st.markdown("**📋 团队成员**")
        
        if team_data.get("members"):
            for i, member in enumerate(team_data["members"]):
                with st.container():
                    col_a, col_b, col_c = st.columns([3, 2, 1])
                    with col_a:
                        st.write(f"**{member['name']}**")
                    with col_b:
                        st.write(f"{member['role']} - {member['permission']}")
                    with col_c:
                        if st.button("🗑️", key=f"del_{i}"):
                            team_data["members"].pop(i)
                            save_team(team_data)
                            st.rerun()
        
        else:
            st.info("暂无团队成员")
    
    st.divider()
    
    st.markdown("**🔢 比赛设置**")
    
    current_round = st.number_input("当前轮次", min_value=1, max_value=10, value=team_data.get("current_round", 1))
    team_name = st.text_input("队伍名称", value=team_data.get("team_name", "我的队伍"))
    
    if st.button("保存设置", use_container_width=True):
        team_data["current_round"] = current_round
        team_data["team_name"] = team_name
        save_team(team_data)
        st.success("✅ 设置已保存")
        st.rerun()
    
    st.divider()
    
    if st.button("✅ 完成设置", use_container_width=True):
        st.session_state.show_team_management = False
        st.rerun()

else:
    # 主界面
    st.subheader("📊 决策面板")
    
    round_num = team_data.get("current_round", 1)
    st.markdown(f"**当前轮次**: 第{round_num}轮")
    
    # 决策标签页
    tabs = st.tabs(["📝 决策录入", "📋 决策列表", "✅ 决策审批", "📊 决策统计"])
    
    with tabs[0]:
        st.subheader("📝 决策录入")
        
        if current_user == "未设置":
            st.warning("⚠️ 请先在侧边栏选择用户")
        else:
            member = next((m for m in team_data["members"] if m["name"] == current_user), None)
            
            if member:
                st.info(f"当前用户：{member['name']} | 角色：{member['role']} | 权限：{member['permission']}")
                
                decision_type = st.selectbox(
                    "决策类型",
                    ["财务决策", "市场决策", "生产决策", "采购决策", "人事决策"]
                )
                
                col1, col2 = st.columns(2)
                
                with col1:
                    decision_content = st.text_area("决策内容", height=150, placeholder="详细描述决策内容...")
                
                with col2:
                    expected_impact = st.text_area("预期影响", height=150, placeholder="该决策可能带来的影响...")
                    
                    financial_impact = st.number_input("财务影响 (万元)", min_value=-1000.0, max_value=1000.0, value=0.0, step=10.0)
                    risk_level = st.selectbox("风险等级", ["低风险", "中风险", "高风险"])
                
                priority = st.select_slider("优先级", options=["低", "中", "高", "紧急"])
                
                attachments = st.multiselect(
                    "关联模块",
                    ["现金流预测", "财务比率", "预算编制", "报价策略", "贷款决策", "产能规划", "广告投放"]
                )
                
                col_submit, col_preview = st.columns([3, 1])
                
                with col_submit:
                    if st.button("💾 提交决策", type="primary", use_container_width=True):
                        if decision_content:
                            decision_record = {
                                "id": len(decisions) + 1,
                                "round": round_num,
                                "submitter": current_user,
                                "role": member['role'],
                                "type": decision_type,
                                "content": decision_content,
                                "expected_impact": expected_impact,
                                "financial_impact": financial_impact,
                                "risk_level": risk_level,
                                "priority": priority,
                                "attachments": attachments,
                                "status": "待审批" if member['permission'] != "决策权" else "已批准",
                                "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            }
                            
                            decisions.append(decision_record)
                            save_decisions(decisions)
                            
                            if member['permission'] == "决策权":
                                st.success("✅ 决策已提交并自动批准！")
                            else:
                                st.info("📋 决策已提交，等待审批")
                            st.balloons()
                            st.rerun()
                        else:
                            st.error("请填写决策内容")
    
    with tabs[1]:
        st.subheader("📋 决策列表")
        
        if decisions:
            # 筛选器
            col_filter1, col_filter2, col_filter3 = st.columns(3)
            
            with col_filter1:
                filter_round = st.multiselect("轮次", list(set([d["round"] for d in decisions])), default=list(set([d["round"] for d in decisions])))
            
            with col_filter2:
                filter_status = st.multiselect("状态", list(set([d["status"] for d in decisions])), default=list(set([d["status"] for d in decisions])))
            
            with col_filter3:
                filter_user = st.multiselect("提交人", list(set([d["submitter"] for d in decisions])), default=list(set([d["submitter"] for d in decisions])))
            
            # 筛选结果
            filtered = [
                d for d in decisions
                if d["round"] in filter_round
                and d["status"] in filter_status
                and d["submitter"] in filter_user
            ]
            
            # 显示决策卡片
            for decision in filtered:
                with st.expander(f"**{decision['type']}** - {decision['submitter']} ({decision['status']})"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.write(f"**轮次**: 第{decision['round']}轮")
                        st.write(f"**提交人**: {decision['submitter']} ({decision['role']})")
                    
                    with col2:
                        st.write(f"**优先级**: {decision['priority']}")
                        st.write(f"**风险**: {decision['risk_level']}")
                    
                    with col3:
                        st.write(f"**财务影响**: {decision['financial_impact']:+.1f}万元")
                        st.write(f"**时间**: {decision['created_at']}")
                    
                    st.write(f"**决策内容**: {decision['content']}")
                    
                    if decision.get('expected_impact'):
                        st.write(f"**预期影响**: {decision['expected_impact']}")
                    
                    if decision.get('attachments'):
                        st.write(f"**关联模块**: {', '.join(decision['attachments'])}")
            
            st.divider()
            st.write(f"共 {len(filtered)} 条决策")
        
        else:
            st.info("暂无决策记录")
    
    with tabs[2]:
        st.subheader("✅ 决策审批")
        
        # 查找待审批决策
        pending = [d for d in decisions if d["status"] == "待审批"]
        
        if pending:
            st.markdown(f"**待审批决策**: {len(pending)} 条")
            
            for decision in pending:
                with st.container():
                    st.markdown(f"**ID**: {decision['id']} | **类型**: {decision['type']} | **提交人**: {decision['submitter']}")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.write(f"**优先级**: {decision['priority']}")
                    
                    with col2:
                        st.write(f"**风险**: {decision['risk_level']}")
                    
                    with col3:
                        st.write(f"**财务影响**: {decision['financial_impact']:+.1f}万元")
                    
                    st.write(f"**内容**: {decision['content']}")
                    
                    col_approve, col_reject = st.columns(2)
                    
                    with col_approve:
                        if st.button("✅ 批准", key=f"approve_{decision['id']}"):
                            decision["status"] = "已批准"
                            decision["approved_at"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            decision["approver"] = current_user
                            save_decisions(decisions)
                            st.success("✅ 已批准")
                            st.rerun()
                    
                    with col_reject:
                        reject_reason = st.text_input("驳回原因", key=f"reject_reason_{decision['id']}")
                        if st.button("❌ 驳回", key=f"reject_{decision['id']}"):
                            decision["status"] = "已驳回"
                            decision["reject_reason"] = reject_reason
                            decision["rejected_at"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            save_decisions(decisions)
                            st.info("📋 已驳回")
                            st.rerun()
                    
                    st.divider()
        
        else:
            st.success("✅ 所有决策已审批完毕")
    
    with tabs[3]:
        st.subheader("📊 决策统计")
        
        if decisions:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("总决策数", len(decisions))
            
            with col2:
                approved = len([d for d in decisions if d["status"] == "已批准"])
                st.metric("已批准", approved)
            
            with col3:
                pending = len([d for d in decisions if d["status"] == "待审批"])
                st.metric("待审批", pending)
            
            with col4:
                rejected = len([d for d in decisions if d["status"] == "已驳回"])
                st.metric("已驳回", rejected)
            
            st.divider()
            
            # 决策类型分布
            st.markdown("**决策类型分布**")
            
            type_counts = {}
            for d in decisions:
                t = d["type"]
                type_counts[t] = type_counts.get(t, 0) + 1
            
            df_types = pd.DataFrame({
                "类型": list(type_counts.keys()),
                "数量": list(type_counts.values())
            })
            st.dataframe(df_types, use_container_width=True, hide_index=True)
            
            # 成员决策统计
            st.divider()
            st.markdown("**成员决策统计**")
            
            user_counts = {}
            for d in decisions:
                u = d["submitter"]
                user_counts[u] = user_counts.get(u, 0) + 1
            
            df_users = pd.DataFrame({
                "成员": list(user_counts.keys()),
                "决策数": list(user_counts.values())
            })
            st.dataframe(df_users, use_container_width=True, hide_index=True)
            
            # 财务影响分析
            st.divider()
            st.markdown("**财务影响分析**")
            
            total_impact = sum(d["financial_impact"] for d in decisions)
            positive_impact = sum(d["financial_impact"] for d in decisions if d["financial_impact"] > 0)
            negative_impact = sum(d["financial_impact"] for d in decisions if d["financial_impact"] < 0)
            
            col_f1, col_f2, col_f3 = st.columns(3)
            
            with col_f1:
                st.metric("净影响", f"{total_impact:+.1f}万元")
            
            with col_f2:
                st.metric("正面影响", f"+{positive_impact:.1f}万元")
            
            with col_f3:
                st.metric("负面影响", f"{negative_impact:.1f}万元")
        
        else:
            st.info("暂无决策数据")
