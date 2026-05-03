# 📦 Windows EXE 打包指南

## 🎯 目标

将学创杯辅助软件和财务工具箱打包成独立的 `.exe` 文件，用户无需安装 Python 即可运行。

---

## 📋 方案选择

### 方案 A：PyInstaller（推荐 ⭐）
**优点**：
- 打包成单个 .exe 文件
- 无需用户安装任何依赖
- 支持一键启动菜单

**缺点**：
- 需要在 Windows 系统上执行打包
- 打包后的文件较大（约 15-20MB/个）

### 方案 B：NSIS 安装程序
**优点**：
- 专业的安装向导界面
- 可创建桌面快捷方式
- 支持卸载程序

**缺点**：
- 需要额外安装 NSIS 工具
- 需要先打包成 exe 再制作安装包

---

## 🚀 快速开始（方案 A）

### 步骤 1：准备 Windows 电脑

在 Windows 10/11 电脑上操作，确保已安装：
- Python 3.8+ 
- pip

### 步骤 2：复制项目到 Windows

将整个 `软件` 文件夹复制到 Windows 电脑，例如：`C:\Users\YourName\Desktop\软件`

### 步骤 3：安装依赖

打开命令提示符（CMD）或 PowerShell：

```cmd
cd C:\Users\YourName\Desktop\软件
pip install pyinstaller streamlit pandas plotly
```

### 步骤 4：打包学创杯辅助软件

```cmd
cd 学创杯辅助软件
pyinstaller --name "学创杯辅助软件" ^
            --windowed ^
            --onefile ^
            --add-data "pages;pages" ^
            --hidden-import streamlit ^
            --hidden-import pandas ^
            --hidden-import plotly ^
            --hidden-import xlsxwriter ^
            xcbs_assistant\app.py
```

完成后，`dist\学创杯辅助软件.exe` 就是打包好的可执行文件。

### 步骤 5：打包财务工具箱

```cmd
cd ..\财务工具箱
pyinstaller --name "财务工具箱" ^
            --windowed ^
            --onefile ^
            --add-data "pages;pages" ^
            --hidden-import streamlit ^
            --hidden-import pandas ^
            --hidden-import plotly ^
            --hidden-import openpyxl ^
            app.py
```

### 步骤 6：创建启动菜单

在 `软件` 文件夹中创建 `启动菜单.bat`：

```batch
@echo off
chcp 65001 >nul
title 学创杯 + 财务工具箱

echo ============================================================
echo 🚀 学创杯 + 财务工具箱 - 启动菜单
echo ============================================================
echo.
echo 1️⃣  启动 学创杯辅助软件
echo 2️⃣  启动 财务工具箱
echo 3️⃣  同时启动两个软件
echo 4️⃣  退出
echo.

set /p choice=请输入选项 (1-4): 

if "%choice%"=="1" start "" "学创杯辅助软件.exe"
if "%choice%"=="2" start "" "财务工具箱.exe"
if "%choice%"=="3" (start "" "学创杯辅助软件.exe" & start "" "财务工具箱.exe")
if "%choice%"=="4" exit /b

echo 软件已启动！
pause
```

### 步骤 7：测试运行

双击 `启动菜单.bat`，选择选项测试两个软件是否正常运行。

---

## 📦 方案 B：制作专业安装包（可选）

### 安装 NSIS

1. 下载 NSIS：https://sourceforge.net/projects/nsis/
2. 安装到默认路径：`C:\Program Files (x86)\NSIS\`

### 创建安装脚本

创建 `installer.nsi` 文件：

```nsis
!include "MUI2.nsh"
!define PRODUCT_NAME "学创杯 + 财务工具箱"
!define PRODUCT_VERSION "2.2+1.5"

Name "${PRODUCT_NAME}"
OutFile "学创杯工具箱_安装版.exe"
InstallDir "$PROGRAMFILES\学创杯工具箱"

!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_LANGUAGE "SimpChinese"

Section "安装"
    SetOutPath "$INSTDIR"
    File "学创杯辅助软件.exe"
    File "财务工具箱.exe"
    File "启动菜单.bat"
    
    CreateDirectory "$SMPROGRAMS\学创杯工具箱"
    CreateShortCut "$SMPROGRAMS\学创杯工具箱\启动菜单.lnk" "$INSTDIR\启动菜单.bat"
    CreateShortCut "$DESKTOP\学创杯工具箱.lnk" "$INSTDIR\启动菜单.bat"
SectionEnd
```

### 生成安装包

```cmd
"C:\Program Files (x86)\NSIS\makensis.exe" installer.nsi
```

生成 `学创杯工具箱_安装版.exe` 安装包。

---

## 📁 最终文件结构

```
软件/
├── 启动菜单.bat              # 启动工具
├── 使用说明.md               # 使用文档
├── 学创杯辅助软件.exe        # 打包后的 exe（约 15-20MB）
└── 财务工具箱.exe            # 打包后的 exe（约 15-20MB）
```

---

## 🎁 分发给用户

### 方式 1：绿色版（推荐）
将整个 `软件` 文件夹压缩为 zip，用户解压后双击 `启动菜单.bat` 即可使用。

**优点**：
- 无需安装
- 可放在任意位置
- 方便携带

### 方式 2：安装版
将 `学创杯工具箱_安装版.exe` 分发给用户，双击运行安装向导。

**优点**：
- 专业安装体验
- 自动创建快捷方式
- 可添加到系统 PATH

---

## ⚠️ 注意事项

1. **首次启动较慢**：打包的 exe 首次启动会解压内置的 Python 环境（约 10-30 秒）

2. **防火墙提示**：首次运行会提示允许网络访问，需点击"允许"

3. **端口占用**：确保 8501 和 8502 端口未被其他程序占用

4. **杀毒软件**：某些杀毒软件可能误报，需添加信任

5. **文件大小**：每个 exe 约 15-20MB（因为包含了完整的 Python 环境）

---

## 🔧 高级选项

### 自定义图标

下载 `.ico` 图标文件，在打包时添加：

```cmd
pyinstaller ... --icon=myapp.ico app.py
```

### 优化打包体积

使用 UPX 压缩（可减小 30-50% 体积）：

```cmd
pip install pyinstaller[encryption]
pyinstaller --noupx ...  # 或使用默认 UPX
```

### 添加版本信息

创建 `version.txt`：

```
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(2, 2, 0, 0),
    prodvers=(2, 2, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[...],
)
```

打包时添加：`--version-file=version.txt`

---

## 📞 问题排查

**问题 1：运行时提示找不到模块**
解决方法：重新打包，确保添加了所有 `--hidden-import` 参数

**问题 2：pages 目录未找到**
解决方法：检查 `--add-data` 参数语法（Windows 用分号）

**问题 3：启动后浏览器未自动打开**
解决方法：exe 启动后手动访问 `http://localhost:8501`

**问题 4：杀毒软件报毒**
解决方法：这是误报，添加到杀毒软件白名单即可

---

## ✅ 验证清单

打包完成后检查：

- [ ] exe 文件可在无 Python 环境的 Windows 上运行
- [ ] 双击 exe 后浏览器自动打开（或手动访问可正常运行）
- [ ] 两个软件可同时运行不冲突
- [ ] 所有功能模块都能正常使用
- [ ] 关闭后无残留进程
- [ ] 文件大小合理（每个 15-25MB）

---

## 📚 参考链接

- PyInstaller 官方文档：https://pyinstaller.org/
- NSIS 官方文档：https://nsis.sourceforge.io/
- Streamlit 打包指南：https://docs.streamlit.io/

---

**版本**：v1.0  
**更新日期**：2026-05-03
