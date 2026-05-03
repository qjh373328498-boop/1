#!/usr/bin/env python3
"""
财务工具箱 - 综合测试脚本
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.database import (
    init_db, get_connection, check_user, get_user_role,
    get_dashboard_stats, clear_all_data
)
from utils.validators import (
    validate_invoice_code, validate_invoice_number, validate_amount,
    validate_date, format_currency, parse_amount
)
from utils.formatters import (
    format_currency as fmt_currency, format_percentage, format_number
)
import sqlite3

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)

def test_database():
    print_section("数据库测试")
    
    # 初始化
    init_db()
    print("✅ 数据库初始化")
    
    # 测试用户登录
    assert check_user('admin', 'admin123') == True, "默认用户登录失败"
    print("✅ 用户登录验证")
    
    # 测试错误密码
    assert check_user('admin', 'wrong') == False, "错误密码应该失败"
    print("✅ 错误密码拦截")
    
    # 测试用户角色
    assert get_user_role('admin') == 'admin', "管理员角色错误"
    print("✅ 用户角色获取")
    
    # 测试仪表盘统计
    stats = get_dashboard_stats()
    assert isinstance(stats, dict), "统计应该返回字典"
    print(f"✅ 仪表盘统计：{stats}")
    
    # 测试数据插入
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT OR REPLACE INTO invoice (code, number, date, amount, type) VALUES (?, ?, ?, ?, ?)",
            ('1100113090', '99999999', '2024-05-03', 1000.00, '专用发票')
        )
        conn.commit()
        print("✅ 发票数据插入")
    except sqlite3.IntegrityError:
        print("⚠️ 发票已存在（正常）")
    
    # 验证插入
    cursor.execute("SELECT COUNT(*) FROM invoice")
    count = cursor.fetchone()[0]
    assert count > 0, "发票表应该至少有数据"
    print(f"✅ 发票总数：{count}")
    
    conn.close()

def test_validators():
    print_section("验证器测试")
    
    # 发票代码验证
    assert validate_invoice_code('1100113090') == True
    assert validate_invoice_code('110011309012') == True
    assert validate_invoice_code('12345') == False
    print("✅ 发票代码验证")
    
    # 发票号码验证
    assert validate_invoice_number('12345678') == True
    assert validate_invoice_number('1234567') == False
    print("✅ 发票号码验证")
    
    # 金额验证
    assert validate_amount(100.50) == True
    assert validate_amount(0) == True
    assert validate_amount(-10) == False
    assert validate_amount('abc') == False
    print("✅ 金额验证")
    
    # 日期验证
    assert validate_date('2024-01-15') == True
    assert validate_date('2024-13-01') == False
    assert validate_date('abc') == False
    print("✅ 日期验证")
    
    # 格式化
    assert format_currency(1234567.89) == '1,234,567.89'
    assert parse_amount('1,234.56') == 1234.56
    print("✅ 格式化功能")

def test_formatters():
    print_section("格式化工具测试")
    
    # 货币格式化
    assert '$1,234.56' in fmt_currency(1234.56) or '¥' in fmt_currency(1234.56)
    print(f"✅ 货币格式化：{fmt_currency(1234567.89)}")
    
    # 百分比格式化
    result = format_percentage(0.1525)
    assert '15.25%' in result or '15' in result
    print(f"✅ 百分比格式化：{format_percentage(0.1525)}")
    
    # 数字格式化
    result = format_number(1234567)
    assert '1,234,567' in result
    print(f"✅ 数字格式化：{format_number(1234567)}")

def test_pages_syntax():
    print_section("页面语法检查")
    
    pages_dir = 'pages'
    success = 0
    failed = 0
    
    for file in sorted(os.listdir(pages_dir)):
        if file.endswith('.py') and not file.startswith('__'):
            try:
                with open(f'{pages_dir}/{file}', 'r', encoding='utf-8') as f:
                    compile(f.read(), file, 'exec')
                print(f"✅ {file}")
                success += 1
            except SyntaxError as e:
                print(f"❌ {file}: {e}")
                failed += 1
    
    print(f"\n总计：{success} 通过，{failed} 失败")
    assert failed == 0, f"{failed} 个文件语法错误"

def test_data_integrity():
    print_section("数据完整性测试")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # 检查所有必要表是否存在
    required_tables = [
        'users', 'invoice', 'bank_statement', 'company_statement',
        'voucher', 'voucher_entry', 'ar_ap', 'calendar_event',
        'balance_sheet', 'financial_metrics'
    ]
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    existing_tables = [row[0] for row in cursor.fetchall()]
    
    for table in required_tables:
        assert table in existing_tables, f"缺少表：{table}"
        print(f"✅ 表 {table} 存在")
    
    # 检查默认用户
    cursor.execute("SELECT COUNT(*) FROM users WHERE username='admin'")
    count = cursor.fetchone()[0]
    assert count > 0, "默认管理员账户不存在"
    print("✅ 默认管理员账户存在")
    
    conn.close()

def main():
    print("\n" + "="*60)
    print("  财务工具箱 v1.3.0 - 综合测试")
    print("="*60)
    
    tests = [
        ("数据库测试", test_database),
        ("验证器测试", test_validators),
        ("格式化工具测试", test_formatters),
        ("页面语法检查", test_pages_syntax),
        ("数据完整性测试", test_data_integrity),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            test_func()
            passed += 1
        except Exception as e:
            print(f"\n❌ {name} 失败：{e}")
            failed += 1
            import traceback
            traceback.print_exc()
    
    print_section("测试结果汇总")
    print(f"通过：{passed}/{len(tests)}")
    print(f"失败：{failed}/{len(tests)}")
    
    if failed == 0:
        print("\n✅ 所有测试通过！")
        return 0
    else:
        print(f"\n❌ {failed} 个测试失败")
        return 1

if __name__ == '__main__':
    exit(main())
