#!/bin/bash

echo "正在启动模型重命名工具..."

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3，请先安装Python3"
    exit 1
fi

# 检查依赖是否安装
echo "检查依赖包..."
if ! python3 -c "import streamlit, pandas, openpyxl" &> /dev/null; then
    echo "正在安装依赖包..."
    pip3 install -r requirements.txt
fi

# 启动应用
echo "启动Web应用..."
echo "应用将在浏览器中打开: http://localhost:8501"
echo "按 Ctrl+C 停止应用"

streamlit run app.py --server.port 8501
