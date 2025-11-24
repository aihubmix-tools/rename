import pandas as pd
import streamlit as st
from io import BytesIO
import openpyxl

# 配置页面样式
st.set_page_config(
    page_title="模型重命名工具",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""
<style>
    /* 全局样式 */
    .main {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    
    /* 标题样式 */
    .title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1a1a1a;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    .subtitle {
        font-size: 1.1rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* 卡片样式 */
    .card {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* 侧边栏卡片样式调整 */
    .css-1lcbmhc .card {
        background: transparent;
        border: none;
        padding: 0;
        margin-bottom: 1rem;
        box-shadow: none;
    }
    
    /* 侧边栏标题样式 */
    .css-1lcbmhc h3 {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* 步骤标题 */
    .step-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #1a1a1a;
        margin-bottom: 1rem;
        padding-left: 0.5rem;
    }
    
    /* 数据表格样式 */
    .dataframe {
        border: 1px solid #e0e0e0;
        border-radius: 4px;
        overflow: hidden;
    }
    
    /* 按钮样式 */
    .stButton > button {
        background-color: #1a1a1a;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.2s;
    }
    
    .stButton > button:hover {
        background-color: #333;
        transform: translateY(-1px);
    }
    
    /* 输入框样式 */
    .stTextInput > div > div > input {
        border: 1px solid #e0e0e0;
        border-radius: 4px;
        padding: 0.5rem;
    }
    
    /* 选择框样式 */
    .stSelectbox > div > div > select {
        border: 1px solid #e0e0e0;
        border-radius: 4px;
        padding: 0.5rem;
    }
    
    /* 多选框样式 */
    .stMultiSelect > div > div > div {
        border: 1px solid #e0e0e0;
        border-radius: 4px;
    }
    
    /* 成功消息样式 */
    .success-message {
        background-color: #f0f9f0;
        border: 1px solid #4caf50;
        color: #2e7d32;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
    
    /* 警告消息样式 */
    .warning-message {
        background-color: #fff3e0;
        border: 1px solid #ff9800;
        color: #f57c00;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
    
    /* 错误消息样式 */
    .error-message {
        background-color: #ffebee;
        border: 1px solid #f44336;
        color: #d32f2f;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
    
    /* 分隔线 */
    .divider {
        border: none;
        border-top: 1px solid #e0e0e0;
        margin: 2rem 0;
    }
    
    /* 侧边栏样式 */
    .css-1d391kg {
        background-color: #fafafa;
    }
    
    /* 步骤指示器 */
    .step-indicator {
        display: flex;
        justify-content: space-between;
        margin-bottom: 2rem;
        padding: 1rem;
        background-color: #f8f9fa;
        border-radius: 8px;
    }
    
    .step {
        flex: 1;
        text-align: center;
        padding: 0.5rem;
        border-radius: 4px;
        margin: 0 0.5rem;
        font-weight: 500;
    }
    
    .step.active {
        background-color: #1a1a1a;
        color: white;
    }
    
    .step.completed {
        background-color: #e8f5e8;
        color: #2e7d32;
    }
    
    /* 修改记录样式 */
    .log-entry {
        padding: 0.5rem;
        margin: 0.5rem 0;
        border-left: 3px solid #333;
        background-color: #f8f9fa;
        border-radius: 0 4px 4px 0;
    }
</style>
""", unsafe_allow_html=True)

def load_data():
    """加载所有Excel文件"""
    try:
        # 读取supplier表
        supplier_df = pd.read_excel('supplier.xlsx')
        
        # 检查是否有上传的文件，优先使用上传的文件
        if 'uploaded_model_suppliers' in st.session_state and st.session_state.uploaded_model_suppliers is not None:
            model_suppliers_df = pd.read_excel(st.session_state.uploaded_model_suppliers)
        else:
            model_suppliers_df = pd.read_excel('model_suppliers.xlsx')
            
        if 'uploaded_model_configs' in st.session_state and st.session_state.uploaded_model_configs is not None:
            model_configs_df = pd.read_excel(st.session_state.uploaded_model_configs)
        else:
            model_configs_df = pd.read_excel('model_configs.xlsx')
        
        return supplier_df, model_suppliers_df, model_configs_df
    except Exception as e:
        st.error(f"读取文件时出错: {e}")
        return None, None, None

def get_supplier_name(supplier_df, supplier_id):
    """根据supplier_id获取supplier_name"""
    supplier_row = supplier_df[supplier_df['id'] == supplier_id]
    if not supplier_row.empty:
        return str(supplier_row.iloc[0]['supplier_name']).lower()
    return f"unknown-{supplier_id}"

def filter_by_parent_model(df, parent_model):
    """根据parent_model筛选数据"""
    return df[df['parent_model'] == parent_model].copy()

def main():
    # 页面标题
    st.markdown('<h1 class="title">🔄 模型重命名工具</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">批量重命名模型配置，支持自动生成供应商前缀</p>', unsafe_allow_html=True)
    
    # 初始化session state
    if 'modification_log' not in st.session_state:
        st.session_state.modification_log = []
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 1
    if 'new_configs' not in st.session_state:
        st.session_state.new_configs = []
    if 'execution_success' not in st.session_state:
        st.session_state.execution_success = False
    
    # 加载数据
    supplier_df, model_suppliers_df, model_configs_df = load_data()
    
    if supplier_df is None:
        st.error("无法加载数据文件")
        return
    
    # 步骤指示器
    steps = ["选择模型", "预览修改", "执行操作", "查看结果"]
    step_html = '<div class="step-indicator">'
    for i, step in enumerate(steps):
        step_class = "active" if i + 1 == st.session_state.current_step else "completed" if i + 1 < st.session_state.current_step else ""
        step_html += f'<div class="step {step_class}">{i+1}. {step}</div>'
    step_html += '</div>'
    st.markdown(step_html, unsafe_allow_html=True)
    
    # 侧边栏：输入parent_model
    with st.sidebar:
        st.markdown('<h3 style="color: #1a1a1a; margin-bottom: 1rem;">📋 筛选条件</h3>', unsafe_allow_html=True)
        
        parent_model = st.text_input(
            "输入 Parent Model:",
            placeholder="例如: bce-reranker-base",
            key="parent_model_input"
        )
        
        if parent_model:
            # 筛选model_suppliers表
            filtered_suppliers = filter_by_parent_model(model_suppliers_df, parent_model)
            
            if not filtered_suppliers.empty:
                st.success(f"找到 {len(filtered_suppliers)} 条记录")
                st.session_state.current_step = 2
            else:
                st.warning(f"未找到 '{parent_model}' 的记录")
                st.session_state.current_step = 1
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 数据统计
        st.markdown('<h3 style="color: #1a1a1a; margin-bottom: 1rem;">📊 数据统计</h3>', unsafe_allow_html=True)
        st.write(f"**Model Suppliers**: {len(model_suppliers_df)} 条记录")
        st.write(f"**Model Configs**: {len(model_configs_df)} 条记录")
        st.write(f"**Suppliers**: {len(supplier_df)} 个供应商")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 文件上传
        st.markdown('<h3 style="color: #1a1a1a; margin-bottom: 1rem;">📁 文件上传</h3>', unsafe_allow_html=True)
        st.markdown('<p style="color: #666; font-size: 0.9rem; margin-bottom: 1rem;">可选择上传自定义的Excel文件：</p>', unsafe_allow_html=True)
        
        # Model Suppliers 文件上传
        if 'uploaded_model_suppliers' not in st.session_state or st.session_state.uploaded_model_suppliers is None:
            uploaded_model_suppliers = st.file_uploader(
                "上传 Model Suppliers 表:",
                type=['xlsx'],
                key="model_suppliers_upload",
                help="上传自定义的 model_suppliers.xlsx 文件"
            )
            
            if uploaded_model_suppliers is not None:
                st.session_state.uploaded_model_suppliers = uploaded_model_suppliers
                st.success("✅ Model Suppliers 文件已上传")
                st.rerun()
        else:
            st.success("✅ Model Suppliers 文件已上传")
            if st.button("🔄 重新上传 Model Suppliers", key="resupload_suppliers"):
                st.session_state.uploaded_model_suppliers = None
                st.rerun()
        
        # Model Configs 文件上传
        if 'uploaded_model_configs' not in st.session_state or st.session_state.uploaded_model_configs is None:
            uploaded_model_configs = st.file_uploader(
                "上传 Model Configs 表:",
                type=['xlsx'],
                key="model_configs_upload",
                help="上传自定义的 model_configs.xlsx 文件"
            )
            
            if uploaded_model_configs is not None:
                st.session_state.uploaded_model_configs = uploaded_model_configs
                st.success("✅ Model Configs 文件已上传")
                st.rerun()
        else:
            st.success("✅ Model Configs 文件已上传")
            if st.button("🔄 重新上传 Model Configs", key="resupload_configs"):
                st.session_state.uploaded_model_configs = None
                st.rerun()
        
        # 显示当前使用的文件状态
        st.markdown('<h4 style="color: #1a1a1a; margin-bottom: 0.5rem; margin-top: 1rem;">📋 当前文件状态</h4>', unsafe_allow_html=True)
        
        model_suppliers_status = "📤 自定义文件" if 'uploaded_model_suppliers' in st.session_state and st.session_state.uploaded_model_suppliers is not None else "📄 默认文件"
        model_configs_status = "📤 自定义文件" if 'uploaded_model_configs' in st.session_state and st.session_state.uploaded_model_configs is not None else "📄 默认文件"
        
        st.write(f"**Model Suppliers**: {model_suppliers_status}")
        st.write(f"**Model Configs**: {model_configs_status}")
        
        # 清除上传文件按钮
        if ('uploaded_model_suppliers' in st.session_state and st.session_state.uploaded_model_suppliers is not None) or \
           ('uploaded_model_configs' in st.session_state and st.session_state.uploaded_model_configs is not None):
            if st.button("🗑️ 清除上传文件", use_container_width=True):
                if 'uploaded_model_suppliers' in st.session_state:
                    st.session_state.uploaded_model_suppliers = None
                if 'uploaded_model_configs' in st.session_state:
                    st.session_state.uploaded_model_configs = None
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 主要内容区域
    if parent_model and 'filtered_suppliers' in locals() and not filtered_suppliers.empty:
        # 分栏布局
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<h3 class="step-title">📝 原始数据</h3>', unsafe_allow_html=True)
            
            # 显示筛选结果
            with st.expander("查看原始记录", expanded=True):
                st.dataframe(filtered_suppliers, width='stretch', hide_index=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<h3 class="step-title">🔄 修改预览</h3>', unsafe_allow_html=True)
            
            # 修改预览
            for idx, row in filtered_suppliers.iterrows():
                supplier_name = get_supplier_name(supplier_df, row['supplier_id'])
                old_model = row['model']
                new_model = f"{supplier_name}-{parent_model.lower()}"
                
                st.markdown(f"""
                <div style="padding: 1rem; margin: 0.5rem 0; background-color: #f8f9fa; border-radius: 4px; border-left: 4px solid #333;">
                    <div style="font-weight: 600; color: #1a1a1a;">ID: {row['id']}</div>
                    <div style="color: #666; margin: 0.5rem 0;">
                        <span style="text-decoration: line-through; color: #999;">{old_model}</span>
                        <br>
                        <span style="color: #2e7d32; font-weight: 500;">→ {new_model}</span>
                    </div>
                    <div style="font-size: 0.9rem; color: #666;">
                        Supplier: {supplier_name} (ID: {row['supplier_id']})
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        # Model配置处理 - 使用Tabs优化布局
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<h3 class="step-title">⚙️ Model Configs 处理</h3>', unsafe_allow_html=True)
        
        # 获取所有可用的model名称
        available_models = model_configs_df['model'].unique().tolist()
        
        # 使用Tabs来组织内容
        tab1, tab2, tab3 = st.tabs(["📋 选择配置", "🎯 配置供应商", "📊 总体预览"])
        
        with tab1:
            st.markdown('<h4 style="color: #1a1a1a; margin-bottom: 1rem;">选择要复制的配置</h4>', unsafe_allow_html=True)
            st.markdown('<p style="color: #666; font-size: 0.9rem; margin-bottom: 1rem;">从所有可用的Model Configs中选择要复制的配置：</p>', unsafe_allow_html=True)
            
            selected_models = st.multiselect(
                "选择 Model Configs:",
                available_models,
                key="source_models",
                help="选择要复制到新供应商的配置"
            )
            
            # 显示选中配置的详细信息 - 使用网格布局
            if selected_models:
                st.markdown('<h5 style="color: #1a1a1a; margin-bottom: 1rem;">选中的配置详情:</h5>', unsafe_allow_html=True)
                
                # 使用columns创建网格布局
                cols = st.columns(min(3, len(selected_models)))
                for i, model_name in enumerate(selected_models):
                    with cols[i % 3]:
                        # 获取这个model在model_configs中的信息
                        model_config_info = model_configs_df[model_configs_df['model'] == model_name]
                        if not model_config_info.empty:
                            config_info = model_config_info.iloc[0]
                            
                            st.markdown(f"""
                            <div style="padding: 1rem; margin: 0.5rem 0; background-color: #f8f9fa; border-radius: 8px; border-left: 4px solid #333; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                                <div style="font-weight: 600; color: #1a1a1a; margin-bottom: 0.5rem;">{model_name}</div>
                                <div style="font-size: 0.85rem; color: #666; line-height: 1.4;">
                                    <div>📝 ID: {config_info.get('id', 'N/A')}</div>
                                    <div>🔗 Parent: {config_info.get('parent_model', 'N/A')}</div>
                                    <div>📏 Context: {config_info.get('context_length', 'N/A')}</div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
        
        with tab2:
            st.markdown('<h4 style="color: #1a1a1a; margin-bottom: 1rem;">配置目标供应商</h4>', unsafe_allow_html=True)
            st.markdown('<p style="color: #666; font-size: 0.9rem; margin-bottom: 1rem;">为每个选中的配置单独选择目标供应商：</p>', unsafe_allow_html=True)
            
            if selected_models:
                # 为每个选中的model配置创建供应商选择
                model_supplier_selections = {}
                
                # 使用expander来组织每个配置的选择
                for i, model_name in enumerate(selected_models):
                    with st.expander(f"🔧 配置 '{model_name}' 的供应商", expanded=i==0):
                        # 创建供应商选择选项
                        supplier_options = []
                        for _, supplier_row in filtered_suppliers.iterrows():
                            supplier_name = get_supplier_name(supplier_df, supplier_row['supplier_id'])
                            supplier_options.append(f"{supplier_name} (ID: {supplier_row['supplier_id']})")
                        
                        selected_suppliers_display = st.multiselect(
                            f"为 {model_name} 选择供应商:",
                            supplier_options,
                            key=f"target_suppliers_{i}",
                            help=f"选择要为 {model_name} 生成新配置的供应商"
                        )
                        
                        # 解析选中的供应商
                        selected_suppliers = []
                        if selected_suppliers_display:
                            for supplier_display in selected_suppliers_display:
                                # 从显示字符串中提取supplier_id
                                supplier_id = int(supplier_display.split("ID: ")[1].split(")")[0])
                                selected_suppliers.append(supplier_id)
                        
                        model_supplier_selections[model_name] = selected_suppliers
                        
                        if selected_suppliers:
                            # 使用columns显示选中的供应商和预览
                            col_a, col_b = st.columns([1, 1])
                            
                            with col_a:
                                st.markdown('<h6 style="color: #1a1a1a; margin-bottom: 0.5rem;">📋 选中的供应商:</h6>', unsafe_allow_html=True)
                                for supplier_id in selected_suppliers:
                                    supplier_row = filtered_suppliers[filtered_suppliers['supplier_id'] == supplier_id].iloc[0]
                                    supplier_name = get_supplier_name(supplier_df, supplier_id)
                                    st.markdown(f"""
                                    <div style="padding: 0.75rem; margin: 0.5rem 0; background-color: #f8f9fa; border-radius: 6px; border-left: 3px solid #2e7d32;">
                                        <div style="font-weight: 600; color: #1a1a1a;">{supplier_name}</div>
                                        <div style="font-size: 0.85rem; color: #666;">Supplier ID: {supplier_id}</div>
                                    </div>
                                    """, unsafe_allow_html=True)
                            
                            with col_b:
                                st.markdown('<h6 style="color: #1a1a1a; margin-bottom: 0.5rem;">🔮 新配置预览:</h6>', unsafe_allow_html=True)
                                for supplier_id in selected_suppliers:
                                    supplier_row = filtered_suppliers[filtered_suppliers['supplier_id'] == supplier_id].iloc[0]
                                    supplier_name = get_supplier_name(supplier_df, supplier_id)
                                    new_model_name = f"{supplier_name}-{parent_model.lower()}"
                                    
                                    st.markdown(f"""
                                    <div style="padding: 0.75rem; margin: 0.5rem 0; background-color: #e8f5e8; border-radius: 6px; border-left: 3px solid #2e7d32;">
                                        <div style="color: #2e7d32; font-weight: 600; font-size: 0.95rem;">{new_model_name}</div>
                                    </div>
                                    """, unsafe_allow_html=True)
                        else:
                            st.info("尚未选择供应商")
            else:
                st.info("请先在'选择配置'标签页中选择要复制的配置")
        
        with tab3:
            st.markdown('<h4 style="color: #1a1a1a; margin-bottom: 1rem;">📊 总体预览</h4>', unsafe_allow_html=True)
            
            if selected_models:
                # 重新获取选择结果
                model_supplier_selections = {}
                for i, model_name in enumerate(selected_models):
                    supplier_options = []
                    for _, supplier_row in filtered_suppliers.iterrows():
                        supplier_name = get_supplier_name(supplier_df, supplier_row['supplier_id'])
                        supplier_options.append(f"{supplier_name} (ID: {supplier_row['supplier_id']})")
                    
                    selected_suppliers_display = st.session_state.get(f"target_suppliers_{i}", [])
                    selected_suppliers = []
                    if selected_suppliers_display:
                        for supplier_display in selected_suppliers_display:
                            supplier_id = int(supplier_display.split("ID: ")[1].split(")")[0])
                            selected_suppliers.append(supplier_id)
                    
                    model_supplier_selections[model_name] = selected_suppliers
                
                # 检查是否有任何配置选择了供应商
                has_any_selection = any(len(suppliers) > 0 for suppliers in model_supplier_selections.values())
                
                if has_any_selection:
                    # 统计信息
                    total_configs = sum(len(suppliers) for suppliers in model_supplier_selections.values())
                    selected_count = len([s for s in model_supplier_selections.values() if len(s) > 0])
                    
                    st.markdown(f"""
                    <div style="padding: 1rem; background-color: #f8f9fa; border-radius: 8px; margin-bottom: 1rem; border-left: 4px solid #333;">
                        <div style="font-size: 1.1rem; font-weight: 600; color: #1a1a1a; margin-bottom: 0.5rem;">📈 生成统计</div>
                        <div style="color: #666;">
                            <div>🎯 已配置的模型: {selected_count} / {len(selected_models)}</div>
                            <div>🔧 将生成的新配置: {total_configs} 个</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # 详细预览 - 使用网格布局
                    st.markdown('<h5 style="color: #1a1a1a; margin-bottom: 1rem;">📋 详细预览:</h5>', unsafe_allow_html=True)
                    
                    for model_name, selected_suppliers in model_supplier_selections.items():
                        if selected_suppliers:
                            with st.expander(f"📝 {model_name} ({len(selected_suppliers)} 个新配置)", expanded=False):
                                # 使用columns创建网格
                                cols = st.columns(min(2, len(selected_suppliers)))
                                for i, supplier_id in enumerate(selected_suppliers):
                                    with cols[i % 2]:
                                        supplier_row = filtered_suppliers[filtered_suppliers['supplier_id'] == supplier_id].iloc[0]
                                        supplier_name = get_supplier_name(supplier_df, supplier_id)
                                        new_model_name = f"{supplier_name}-{parent_model.lower()}"
                                        
                                        st.markdown(f"""
                                        <div style="padding: 1rem; background-color: #e8f5e8; border-radius: 8px; border-left: 4px solid #2e7d32; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                                            <div style="color: #2e7d32; font-weight: 600; margin-bottom: 0.5rem;">{new_model_name}</div>
                                            <div style="font-size: 0.85rem; color: #666;">
                                                <div>🏢 供应商: {supplier_name}</div>
                                                <div>🆔 ID: {supplier_id}</div>
                                                <div>📋 源配置: {model_name}</div>
                                            </div>
                                        </div>
                                        """, unsafe_allow_html=True)
                else:
                    st.warning("⚠️ 尚未为任何配置选择供应商")
            else:
                st.info("请先在'选择配置'标签页中选择要复制的配置")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 执行按钮
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 执行修改和新增", type="primary", use_container_width=True):
                st.session_state.current_step = 3
                try:
                    # 执行model_suppliers表修改 - 直接修改原始文件
                    model_suppliers_df_modified = model_suppliers_df.copy()
                    for idx, row in filtered_suppliers.iterrows():
                        supplier_name = get_supplier_name(supplier_df, row['supplier_id'])
                        old_model = row['model']
                        new_model = f"{supplier_name}-{parent_model.lower()}"
                        
                        # 修改DataFrame中的值
                        model_suppliers_df_modified.loc[model_suppliers_df_modified['id'] == row['id'], 'model'] = new_model
                        
                        # 记录修改
                        st.session_state.modification_log.append({
                            'table': 'model_suppliers',
                            'action': '修改',
                            'id': row['id'],
                            'old_value': old_model,
                            'new_value': new_model,
                            'supplier_id': row['supplier_id']
                        })
                    
                    # 保存修改到原始文件
                    model_suppliers_df_modified.to_excel('model_suppliers.xlsx', index=False)
                    
                    # 执行model_configs表新增
                    new_configs = []
                    for model_name, selected_suppliers in model_supplier_selections.items():
                        if selected_suppliers:  # 只为有选择供应商的配置生成
                            original_config = model_configs_df[model_configs_df['model'] == model_name].iloc[0]
                            
                            # 只为选中的供应商生成配置
                            for supplier_id in selected_suppliers:
                                supplier_row = filtered_suppliers[filtered_suppliers['supplier_id'] == supplier_id].iloc[0]
                                supplier_name = get_supplier_name(supplier_df, supplier_id)
                                new_model_name = f"{supplier_name}-{parent_model.lower()}"
                                
                                new_config = original_config.copy()
                                new_config['model'] = new_model_name
                                new_config['supplier_id'] = supplier_id
                                new_configs.append(new_config)
                                
                                # 记录新增
                                st.session_state.modification_log.append({
                                    'table': 'model_configs',
                                    'action': '新增',
                                    'model': new_model_name,
                                    'supplier_id': supplier_id,
                                    'source_model': model_name
                                })
                    
                    # 将新配置添加到原始model_configs文件
                    if new_configs:
                        new_configs_df = pd.DataFrame(new_configs)
                        model_configs_df_updated = pd.concat([model_configs_df, new_configs_df], ignore_index=True)
                        model_configs_df_updated.to_excel('model_configs.xlsx', index=False)
                    
                    # 保存new_configs到session_state
                    st.session_state.new_configs = new_configs
                    st.session_state.execution_success = True
                    st.session_state.current_step = 4
                    st.rerun()
                    
                except Exception as e:
                    st.markdown(f'<div class="error-message">❌ 操作失败: {e}</div>', unsafe_allow_html=True)
        
        # 显示修改后的数据 - 只在执行完成后显示
        if st.session_state.current_step == 4 and st.session_state.execution_success and st.session_state.new_configs:
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<h3 class="step-title">📋 新增的 Model Configs</h3>', unsafe_allow_html=True)
            
            new_configs_df = pd.DataFrame(st.session_state.new_configs)
            with st.expander("查看新增配置", expanded=True):
                st.dataframe(new_configs_df, width='stretch', hide_index=True)
            
            # 导出按钮
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                # 修改后的model_suppliers
                final_suppliers = model_suppliers_df.copy()
                for idx, row in filtered_suppliers.iterrows():
                    supplier_name = get_supplier_name(supplier_df, row['supplier_id'])
                    new_model_name = f"{supplier_name}-{parent_model.lower()}"
                    final_suppliers.loc[final_suppliers['id'] == row['id'], 'model'] = new_model_name
                
                final_suppliers.to_excel(writer, sheet_name='model_suppliers', index=False)
                new_configs_df.to_excel(writer, sheet_name='model_configs', index=False)
                supplier_df.to_excel(writer, sheet_name='supplier', index=False)
            
            st.download_button(
                label="📥 下载修改后的Excel文件",
                data=output.getvalue(),
                file_name="modified_models.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # 显示修改记录
    if st.session_state.modification_log:
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<h3 class="step-title">📝 修改记录</h3>', unsafe_allow_html=True)
        
        # 创建修改记录的DataFrame
        log_df = pd.DataFrame(st.session_state.modification_log)
        
        # 分别显示不同表的记录
        supplier_logs = log_df[log_df['table'] == 'model_suppliers']
        config_logs = log_df[log_df['table'] == 'model_configs']
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if not supplier_logs.empty:
                st.markdown('<h4 style="color: #1a1a1a; margin-bottom: 1rem;">Model Suppliers 表修改</h4>', unsafe_allow_html=True)
                for _, log in supplier_logs.iterrows():
                    st.markdown(f"""
                    <div class="log-entry">
                        <div style="font-weight: 600;">ID {log['id']}</div>
                        <div style="color: #666; margin: 0.25rem 0;">
                            <span style="text-decoration: line-through;">{log['old_value']}</span>
                            <br>
                            <span style="color: #2e7d32;">→ {log['new_value']}</span>
                        </div>
                        <div style="font-size: 0.9rem; color: #666;">Supplier ID: {log['supplier_id']}</div>
                    </div>
                    """, unsafe_allow_html=True)
        
        with col2:
            if not config_logs.empty:
                st.markdown('<h4 style="color: #1a1a1a; margin-bottom: 1rem;">Model Configs 表新增</h4>', unsafe_allow_html=True)
                for _, log in config_logs.iterrows():
                    st.markdown(f"""
                    <div class="log-entry">
                        <div style="font-weight: 600; color: #2e7d32;">{log['model']}</div>
                        <div style="color: #666; margin: 0.25rem 0;">基于: {log['source_model']}</div>
                        <div style="font-size: 0.9rem; color: #666;">Supplier ID: {log['supplier_id']}</div>
                    </div>
                    """, unsafe_allow_html=True)
        
        # 清除记录按钮
        if st.button("🗑️ 清除修改记录", use_container_width=True):
            st.session_state.modification_log = []
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
