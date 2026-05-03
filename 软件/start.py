# -*- coding: utf-8 -*-
import os
import sys
import subprocess

def print_header():
    print("=" * 60)
    print("              软件启动器 - 交互式菜单")
    print("=" * 60)
    print()
    print("提示：如果启动失败，可以直接双击各软件目录下的：")
    print("      一键启动.bat")
    print()

def select_software():
    print("请选择要启动的软件：")
    print("  1. 学创杯辅助软件")
    print("  2. 财务工具箱")
    print("  3. 自定义软件路径")
    print("  0. 退出")
    print()
    
    choice = input("请输入选项 (0-3): ").strip()
    
    if choice == "0":
        return None
    elif choice == "1":
        return "学创杯辅助软件"
    elif choice == "2":
        return "财务工具箱"
    elif choice == "3":
        path = input("请输入软件目录路径: ").strip()
        # 处理拖拽文件的情况（路径带引号）
        path = path.strip('"\'')
        return path
    else:
        print("无效的选项！")
        return None

def check_and_create_venv(software_path):
    venv_path = os.path.join(software_path, "venv")
    pyvenv_cfg = os.path.join(venv_path, "pyvenv.cfg")
    venv_python = os.path.join(venv_path, "Scripts", "python.exe")
    
    # 检查 venv 是否完整（pyvenv.cfg 和 python.exe 必须都存在）
    need_recreate = False
    
    if not os.path.exists(venv_path):
        print("  检测到未创建虚拟环境")
        need_recreate = True
    elif not os.path.exists(pyvenv_cfg):
        print("  检测到不完整的虚拟环境（缺少 pyvenv.cfg），正在清理...")
        need_recreate = True
    elif not os.path.exists(venv_python):
        print("  检测到损坏的虚拟环境（缺少 python.exe），正在清理...")
        need_recreate = True
    
    # 清理并重新创建
    if need_recreate and os.path.exists(venv_path):
        try:
            import shutil
            shutil.rmtree(venv_path)
            print("  已清理损坏的虚拟环境")
        except Exception as e:
            print(f"  错误：清理失败 - {e}")
            print(f"  请手动删除：{venv_path}")
            return False
    
    if not os.path.exists(venv_path):
        print("  [1/3] 正在创建虚拟环境...")
        try:
            subprocess.run([sys.executable, "-m", "venv", venv_path], check=True)
            print("  虚拟环境创建成功！")
        except subprocess.CalledProcessError as e:
            print(f"  错误：创建虚拟环境失败 - {e}")
            return False
        except FileNotFoundError:
            print(f"  错误：找不到 Python，请确认已安装 Python 3.8+")
            return False
    
    return True

def activate_and_run(software_path):
    venv_python = os.path.join(software_path, "venv", "Scripts", "python.exe")
    venv_pip = os.path.join(software_path, "venv", "Scripts", "pip.exe")
    venv_pip_cmd = f'"{venv_pip}"'
    app_path = os.path.join(software_path, "app.py")
    
    if not os.path.exists(app_path):
        print(f"  错误：找不到 app.py 文件")
        print(f"  路径：{app_path}")
        return False
    
    # 检查 Python 是否存在
    if not os.path.exists(venv_python):
        print(f"  错误：虚拟环境未创建或已损坏")
        print(f"  路径：{venv_python}")
        return False
    
    print("  [2/3] 正在升级 pip...")
    upgrade_cmd = f'"{venv_python}" -m pip install --upgrade pip'
    subprocess.run(upgrade_cmd, shell=True, capture_output=True)
    
    print("  [3/3] 正在安装依赖包 (首次启动可能需要 2-3 分钟)...")
    
    # 安装依赖，使用清华镜像源加速
    req_path = os.path.join(software_path, "requirements.txt")
    install_cmd = f'"{venv_pip}" install -r "{req_path}" -i https://pypi.tuna.tsinghua.edu.cn/simple'
    result = subprocess.run(install_cmd, shell=True)
    
    if result.returncode != 0:
        print()
        print("  " + "=" * 50)
        print("   警告：依赖安装出现问题")
        print("=" * 50)
        print()
        print("  可能的原因：")
        print("  1. 路径太深（建议放在根目录，如 G:\\软件\\）")
        print("  2. 缺少 Microsoft C++ Build Tools")
        print("  3. 网络问题导致下载失败")
        print()
        print("  即使安装不完整，程序仍可能正常运行，正在尝试启动...")
        print()
    
    print()
    print("  " + "=" * 50)
    print("   正在启动 Streamlit...")
    print("   浏览器将自动打开 http://localhost:8501")
    print("=" * 50)
    print()
    
    # 启动 Streamlit
    run_cmd = f'"{venv_python}" -m streamlit run "{app_path}"'
    try:
        subprocess.run(run_cmd, shell=True)
    except KeyboardInterrupt:
        print("\n  已停止运行")
    
    return True

def main():
    # 使用 UTF-8 编码处理路径
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print_header()
        
        software_name = select_software()
        
        if software_name is None:
            print("再见！")
            break
        
        print()
        print(f"正在启动：{software_name}")
        print("-" * 50)
        
        # 如果是预设软件，使用绝对路径
        if software_name in ["学创杯辅助软件", "财务工具箱"]:
            software_path = os.path.join(script_dir, software_name)
        else:
            software_path = software_name
        
        # 规范化路径（处理中文和特殊字符）
        software_path = os.path.normpath(os.path.abspath(software_path))
        
        if not os.path.exists(software_path):
            print(f"错误：找不到软件目录 - {software_path}")
            input("按回车键返回菜单...")
            continue
        
        # 创建虚拟环境
        if not check_and_create_venv(software_path):
            input("按回车键返回菜单...")
            continue
        
        # 启动软件
        activate_and_run(software_path)
        
        print()
        input("按回车键返回主菜单...")

if __name__ == "__main__":
    main()
