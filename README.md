# 模型重命名工具

这是一个基于Streamlit的Web应用，用于批量重命名模型配置。该工具可以：

1. 根据parent_model筛选模型
2. 自动将model字段重命名为`<supplier_name>-<parent_model>`格式
3. 复制model_configs表中的配置并生成新的配置
4. 提供修改记录和导出功能

## 功能特点

### 📊 数据处理
- **model_suppliers表**: 直接修改原始文件中的model字段
- **model_configs表**: 直接在原始文件中新增配置记录
- **supplier表**: 提供供应商名称映射
- **实时文件更新**: 所有操作直接修改原始Excel文件

### 🎯 核心功能
1. **模型筛选**: 根据parent_model筛选相关模型
2. **自动重命名**: 根据supplier_id自动生成新的model名称
3. **配置复制**: 选择要复制的model_configs配置
4. **实时预览**: 显示修改前后的对比
5. **修改记录**: 详细记录所有修改和新增操作
6. **数据导出**: 导出修改后的Excel文件

### 🎨 UI设计特点
- **黑白配色**: 简洁优雅的黑白主题设计
- **分栏布局**: 清晰的两栏式布局，左右对比显示
- **步骤指示**: 直观的4步骤操作流程
- **删除线提示**: 原始内容用删除线清晰标识
- **卡片设计**: 模块化的卡片式界面布局
- **响应式**: 适配不同屏幕尺寸

## 📁 项目结构

```
oepnsource model rename/
├── app.py                      # 🎨 主应用文件
├── start.sh                    # 🚀 一键启动脚本
├── requirements.txt            # 📦 Python依赖
├── README.md                   # 📖 项目说明文档
├── model_suppliers.xlsx        # 📊 Model Suppliers数据表
├── model_configs.xlsx          # 📊 Model Configs数据表
└── supplier.xlsx               # 📊 供应商数据表
```

## 使用方法

### 1. 启动应用
```bash
# 安装依赖
pip install -r requirements.txt

# 启动应用
streamlit run app.py

# 或使用快速启动脚本
./start.sh
```

### 2. 使用步骤

#### 步骤1: 输入Parent Model
- 在左侧边栏输入要处理的parent_model名称
- 例如: `bce-reranker-base`

#### 步骤2: 查看筛选结果
- 应用会显示该parent_model对应的所有model_suppliers记录
- 可以展开/折叠查看详细信息

#### 步骤3: 预览重命名结果
- 左侧显示原始model字段
- 右侧显示修改后的model字段（格式：`<supplier_name>-<parent_model>`）

#### 步骤4: 选择要复制的Model Configs
- 在左侧选择框中选择要复制的model_configs
- 右侧会实时预览将要生成的新配置

#### 步骤5: 执行操作
- 点击"执行修改和新增"按钮
- 系统会自动：
  - 修改model_suppliers表中的model字段
  - 复制选中的model_configs并生成新配置
  - 记录所有操作日志

#### 步骤6: 查看修改记录
- 在页面底部查看详细的修改记录
- 区分model_suppliers表的修改和model_configs表的新增

#### 步骤7: 导出结果
- 点击"下载修改后的Excel文件"按钮
- 获得包含所有修改的Excel文件

## 数据结构

### 输入文件
- `model_suppliers.xlsx`: 模型供应商表
- `model_configs.xlsx`: 模型配置表  
- `supplier.xlsx`: 供应商表

### 输出文件
- `modified_models.xlsx`: 包含修改后的所有表

## 重命名规则

新的model名称格式：`<supplier_name>-<parent_model>`

例如：
- 原始: `bce-reranker-base`, supplier_id: 11 (百度)
- 修改后: `baidu-bce-reranker-base`

## 注意事项

1. **数据备份**: 建议在操作前备份原始Excel文件
2. **parent_model**: 确保输入的parent_model在model_suppliers表中存在
3. **supplier映射**: 确保supplier表中包含所有需要的供应商信息
4. **配置选择**: 可以选择多个model_configs进行批量复制

## 技术栈

- **Python**: 主要编程语言
- **Streamlit**: Web应用框架
- **Pandas**: 数据处理
- **OpenPyXL**: Excel文件操作

## 故障排除

### 常见问题

1. **文件读取错误**
   - 检查Excel文件是否在正确目录
   - 确保文件格式正确（.xlsx）

2. **找不到Parent Model**
   - 检查parent_model拼写
   - 确认该parent_model在model_suppliers表中存在

3. **供应商名称未知**
   - 检查supplier表是否包含对应的supplier_id
   - 确认supplier_name字段正确

### 联系支持

如遇到问题，请检查：
1. 控制台错误信息
2. Excel文件格式和内容
3. 依赖包是否正确安装
