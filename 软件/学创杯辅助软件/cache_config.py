"""
全局缓存配置和性能优化设置
"""
import streamlit as st

# 页面配置 - 优化首次加载速度
st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items=None
)

# 隐藏 Streamlit 默认菜单和页脚，提升性能
hide_style = """
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stSidebar"] {z-index: 99999;}
</style>
"""
st.markdown(hide_style, unsafe_allow_html=True)

# 缓存配置
CACHE_TTL = 3600  # 缓存过期时间：1 小时

def setup_cache():
    """配置缓存参数"""
    return {
        'cache_data': CACHE_TTL,
        'cache_resource': CACHE_TTL,
        'suppress_st_warning': True
    }
