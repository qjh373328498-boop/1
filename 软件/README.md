# 软件启动说明

## 快速开始

### Windows 用户

**方法 1：交互式启动器（推荐）**

双击 `一键启动.bat`，会出现菜单：
```
============================================
         软件启动器 - 交互式菜单
============================================

请选择要启动的软件：
  1. 学创杯辅助软件
  2. 财务工具箱
  3. 自定义软件路径
  0. 退出

请输入选项 (0-3):
```

- 输入 `1` 或 `2` 启动对应软件
- 输入 `3` 可以手动输入其他软件路径
- 首次运行会自动创建虚拟环境并安装依赖

**方法 2：单独启动**

双击软件目录下的 `一键启动.bat`：
- `学创杯辅助软件/一键启动.bat`
- `财务工具箱/一键启动.bat`

### Mac/Linux 用户

打开终端，执行：

```bash
# 学创杯辅助软件
cd 学创杯辅助软件
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m streamlit run app.py

# 财务工具箱
cd 财务工具箱
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m streamlit run app.py
```

## 系统要求

- **Python**: 3.8 或更高版本
- **操作系统**: Windows 10/11, macOS 10.15+, Linux
- **内存**: 至少 2GB 可用内存

## 常见问题

### Q: 提示"找不到 Python"
**解决**: 安装 Python 3.8+，安装时勾选"Add Python to PATH"

### Q: 首次启动很慢
**解决**: 首次运行需要下载安装依赖包，耐心等待

### Q: 如何重新安装依赖？
**解决**: 删除软件目录下的 `venv` 文件夹，重新运行即可

## 目录结构

```
软件/
├── README.md              # 本说明文件
├── start.py               # 交互式启动器
├── 一键启动.bat           # Windows 启动入口
├── 学创杯辅助软件/
│   ├── app.py
│   └── requirements.txt
└── 财务工具箱/
    ├── app.py
    └── requirements.txt
```
