#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一键打包工具 - 生成 Windows .exe 安装包
功能：打包学创杯辅助软件 + 财务工具箱 为独立的 Windows 应用
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

# 颜色输出
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_step(msg):
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}{msg}{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}")

def print_success(msg):
    print(f"{Colors.GREEN}✅ {msg}{Colors.END}")

def print_warning(msg):
    print(f"{Colors.YELLOW}⚠️  {msg}{Colors.END}")

def print_error(msg):
    print(f"{Colors.RED}❌ {msg}{Colors.END}")

def check_environment():
    """检查 Python 环境和必要工具"""
    print_step("🔍 检查运行环境")
    
    # 检查 Python
    python_version = sys.version
    print(f"✅ Python 版本：{python_version.split()[0]}")
    
    # 检查 PyInstaller
    try:
        import PyInstaller
        print_success(f"PyInstaller 已安装：v{PyInstaller.__version__}")
    except ImportError:
        print_warning("PyInstaller 未安装，正在安装...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print_success("PyInstaller 安装成功")
    
    # 检查 NSIS (用于制作安装程序)
    nsis_paths = [
        r"C:\Program Files (x86)\NSIS\makensis.exe",
        r"C:\Program Files\NSIS\makensis.exe"
    ]
    nsis_installed = any(os.path.exists(p) for p in nsis_paths)
    
    if nsis_installed:
        print_success("NSIS 已安装（可用于制作安装程序）")
    else:
        print_warning("NSIS 未安装，将生成绿色版 exe（可选：安装 NSIS 制作专业安装包）")
        print("   下载地址：https://sourceforge.net/projects/nsis/")
    
    return nsis_installed

def build_xcbs_exe():
    """打包学创杯辅助软件"""
    print_step("📦 打包 学创杯辅助软件")
    
    build_dir = Path("软件/学创杯辅助软件")
    spec_dir = Path("build_xcbs")
    dist_dir = Path("dist_xcbs")
    
    # 清理旧构建
    if spec_dir.exists():
        shutil.rmtree(spec_dir)
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    
    # PyInstaller 命令 (Windows 用分号，Linux/Mac 用冒号)
    data_sep = ";" if sys.platform == "win32" else ":"
    
    cmd = [
        "pyinstaller",
        "--name", "学创杯辅助软件",
        "--windowed",
        "--onefile",
        f"--add-data=pages{data_sep}pages",
        "--hidden-import", "streamlit",
        "--hidden-import", "pandas",
        "--hidden-import", "plotly",
        "--hidden-import", "xlsxwriter",
        "--workpath", str(spec_dir),
        "--distpath", str(dist_dir),
        "xcbs_assistant/app.py"
    ]
    
    print(f"执行打包命令...")
    os.chdir(build_dir)
    
    try:
        subprocess.check_call(cmd)
        print_success("学创杯辅助软件 打包完成")
        return dist_dir / "学创杯辅助软件.exe"
    except subprocess.CalledProcessError as e:
        print_error(f"打包失败：{e}")
        return None
    finally:
        os.chdir("../..")

def build_finance_exe():
    """打包财务工具箱"""
    print_step("📦 打包 财务工具箱")
    
    build_dir = Path("软件/财务工具箱")
    spec_dir = Path("build_finance")
    dist_dir = Path("dist_finance")
    
    # 清理旧构建
    if spec_dir.exists():
        shutil.rmtree(spec_dir)
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    
    # PyInstaller 命令
    data_sep = ";" if sys.platform == "win32" else ":"
    
    cmd = [
        "pyinstaller",
        "--name", "财务工具箱",
        "--windowed",
        "--onefile",
        f"--add-data=pages{data_sep}pages",
        "--hidden-import", "streamlit",
        "--hidden-import", "pandas",
        "--hidden-import", "plotly",
        "--hidden-import", "openpyxl",
        "--workpath", str(spec_dir),
        "--distpath", str(dist_dir),
        "app.py"
    ]
    
    print(f"执行打包命令...")
    os.chdir(build_dir)
    
    try:
        subprocess.check_call(cmd)
        print_success("财务工具箱 打包完成")
        return dist_dir / "财务工具箱.exe"
    except subprocess.CalledProcessError as e:
        print_error(f"打包失败：{e}")
        return None
    finally:
        os.chdir("../..")

def create_launcher():
    """创建启动器菜单"""
    print_step("🚀 创建启动菜单")
    
    output_dir = Path("软件/Windows 安装包")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 复制 exe 文件
    xcbs_exe = Path("软件/学创杯辅助软件/dist_xcbs/学创杯辅助软件.exe")
    finance_exe = Path("软件/财务工具箱/dist_finance/财务工具箱.exe")
    
    if xcbs_exe.exists():
        shutil.copy2(xcbs_exe, output_dir)
        print_success(f"已复制：{xcbs_exe.name}")
    
    if finance_exe.exists():
        shutil.copy2(finance_exe, output_dir)
        print_success(f"已复制：{finance_exe.name}")
    
    # 创建启动菜单批处理
    launcher_content = '''@echo off
chcp 65001 >nul
title 学创杯 + 财务工具箱 - 启动菜单

echo ============================================================
echo 🚀 学创杯 + 财务工具箱 - 启动菜单
echo ============================================================
echo.
echo 请选择要启动的软件:
echo.
echo 1️⃣  启动 学创杯辅助软件 v2.2
echo 2️⃣  启动 财务工具箱 v1.5
echo 3️⃣  同时启动两个软件
echo 4️⃣  退出
echo.
echo ============================================================
echo.

set /p choice="请输入选项 (1-4): "

if "%choice%"=="1" (
    echo 正在启动 学创杯辅助软件...
    start "" "学创杯辅助软件.exe"
) else if "%choice%"=="2" (
    echo 正在启动 财务工具箱...
    start "" "财务工具箱.exe"
) else if "%choice%"=="3" (
    echo 正在同时启动两个软件...
    start "" "学创杯辅助软件.exe"
    start "" "财务工具箱.exe"
) else if "%choice%"=="4" (
    exit /b
) else (
    echo 无效的选项，请重新运行
)

echo.
echo 软件已启动，浏览器将自动打开
echo 学创杯辅助软件：http://localhost:8502
echo 财务工具箱：http://localhost:8501
echo.
pause
'''
    
    launcher_path = output_dir / "启动菜单.bat"
    with open(launcher_path, "w", encoding="utf-8") as f:
        f.write(launcher_content)
    
    print_success(f"已创建：{launcher_path.name}")
    
    # 创建说明文件
    readme_content = '''# 学创杯 + 财务工具箱 - Windows 版

## 📦 包含内容

- `学创杯辅助软件.exe` - 比赛辅助工具（14 个功能模块）
- `财务工具箱.exe` - 企业财务管理（15 个功能模块）
- `启动菜单.bat` - 一键启动工具

## 🚀 使用方法

### 方法 1: 使用启动菜单（推荐）
双击运行 `启动菜单.bat`，选择要启动的软件

### 方法 2: 直接运行
双击对应的 `.exe` 文件直接启动

## 🌐 访问地址

- 学创杯辅助软件：http://localhost:8502
- 财务工具箱：http://localhost:8501（密码：703102）

## ⚙️ 系统要求

- Windows 10/11
- 无需安装 Python 或其他依赖
- 已打包所有必要组件

## 📝 注意事项

1. 首次启动可能需要 10-30 秒（解压内置 Python 环境）
2. 启动后会自动打开默认浏览器
3. 关闭 exe 后服务器仍在运行，需关闭浏览器标签页

## 🆘 问题反馈

如遇问题，请检查：
1. 端口是否被占用（8501, 8502）
2. 防火墙设置
3. 重新运行启动菜单

---
版本：v2.2 + v1.5
日期：2026-05-03
'''
    
    readme_path = output_dir / "使用说明.md"
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print_success(f"已创建：{readme_path.name}")
    
    return output_dir

def create_nsis_installer():
    """使用 NSIS 创建专业安装程序（可选）"""
    print_step("📥 创建 NSIS 安装程序（可选）")
    
    nsis_paths = [
        r"C:\Program Files (x86)\NSIS\makensis.exe",
        r"C:\Program Files\NSIS\makensis.exe"
    ]
    makensis = next((p for p in nsis_paths if os.path.exists(p)), None)
    
    if not makensis:
        print_warning("NSIS 未安装，跳过安装程序制作")
        print("   如需制作专业安装包，请安装 NSIS 后重新运行")
        return None
    
    # 创建 NSIS 脚本
    nsis_script = '''
!include "MUI2.nsh"
!define PRODUCT_NAME "学创杯 + 财务工具箱"
!define PRODUCT_VERSION "2.2+1.5"
!define PRODUCT_PUBLISHER "MonkeyCode-AI"
!define PRODUCT_WEB_SITE "https://github.com"

Name "${PRODUCT_NAME} v${PRODUCT_VERSION}"
OutFile "学创杯 + 财务工具箱_安装版.exe"
InstallDir "$PROGRAMFILES\\学创杯工具箱"
InstallDirRegKey HKLM "Software\\${PRODUCT_NAME}" ""

!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_LANGUAGE "SimpChinese"

Section "安装" SecInstall
    SetOutPath "$INSTDIR"
    File "学创杯辅助软件.exe"
    File "财务工具箱.exe"
    File "启动菜单.bat"
    File "使用说明.md"
    File "卸载.exe"
    
    CreateDirectory "$SMPROGRAMS\\学创杯工具箱"
    CreateShortCut "$SMPROGRAMS\\学创杯工具箱\\启动菜单.lnk" "$INSTDIR\\启动菜单.bat"
    CreateShortCut "$DESKTOP\\学创杯工具箱.lnk" "$INSTDIR\\启动菜单.bat"
    
    WriteRegStr HKLM "Software\\${PRODUCT_NAME}" "" $INSTDIR
    WriteUninstaller "$INSTDIR\\卸载.exe"
SectionEnd

Section "卸载" SecUninstall
    DeleteRegKey HKLM "Software\\${PRODUCT_NAME}"
    Delete "$INSTDIR\\*.*"
    RMDir "$INSTDIR"
    Delete "$SMPROGRAMS\\学创杯工具箱\\*.*"
    RMDir "$SMPROGRAMS\\学创杯工具箱"
    Delete "$DESKTOP\\学创杯工具箱.lnk"
SectionEnd
'''
    
    script_path = Path("软件/Windows 安装包/installer.nsi")
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(nsis_script)
    
    print(f"NSIS 脚本已创建：{script_path}")
    print(f"运行以下命令生成安装程序:")
    print(f'  "{makensis}" "{script_path}"')
    
    return script_path

def main():
    """主函数"""
    print("\n" + "="*60)
    print("🚀 学创杯 + 财务工具箱 - Windows 打包工具")
    print("="*60)
    
    # 检查环境
    nsis_available = check_environment()
    
    # 打包两个软件
    xcbs_exe = build_xcbs_exe()
    finance_exe = build_finance_exe()
    
    # 创建启动菜单
    output_dir = create_launcher()
    
    # 可选：创建 NSIS 安装程序
    if nsis_available:
        create_nsis_installer()
    
    # 完成总结
    print_step("✨ 打包完成")
    print(f"\n输出目录：{output_dir.absolute()}")
    print("\n包含文件:")
    for f in output_dir.iterdir():
        print(f"  - {f.name}")
    
    print("\n" + "="*60)
    print_success("用户现在可以：")
    print("  1. 直接运行 启动菜单.bat 使用软件")
    print("  2. 或安装 NSIS 后制作专业安装包")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
