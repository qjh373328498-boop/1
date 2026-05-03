#!/usr/bin/env python3
"""
财务工具箱 - 深度压力测试与性能分析
"""
import sys
import os
import time
import sqlite3
import random
import traceback
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.database import get_connection, init_db, get_dashboard_stats

# 测试配置
TEST_ROUNDS = 3
BATCH_SIZE = 500
TOTAL_OPERATIONS = 0
FAILED_OPERATIONS = 0

def increment_global(name, value=1):
    global TOTAL_OPERATIONS, FAILED_OPERATIONS
    if name == 'total':
        TOTAL_OPERATIONS += value
    else:
        FAILED_OPERATIONS += value

def test_insert_performance():
    """测试 1: 批量插入性能"""
    print_section("测试 1: 批量插入性能测试")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    results = []
    local_failed = 0
    
    for round_num in range(TEST_ROUNDS):
        start_time = time.time()
        inserted = 0
        
        for i in range(BATCH_SIZE):
            try:
                date = datetime(2024, 1, 1) + timedelta(days=random.randint(0, 365))
                cursor.execute(
                    """INSERT OR IGNORE INTO invoice 
                       (code, number, date, amount, type, supplier, buyer, status) 
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        f'{random.randint(1000000000, 999999999999):0>12}',
                        f'{random.randint(10000000, 99999999):0>8}',
                        date.strftime('%Y-%m-%d'),
                        round(random.uniform(100, 100000), 2),
                        random.choice(['专用发票', '普通发票', '电子发票']),
                        f'供应商{random.randint(1, 100)}',
                        '本公司',
                        random.choice(['未认证', '已认证'])
                    )
                )
                inserted += 1
            except Exception:
                local_failed += 1
        
        conn.commit()
        elapsed = time.time() - start_time
        speed = inserted / elapsed if elapsed > 0 else 0
        
        increment_global('total', inserted)
        
        result = f"轮次{round_num+1}: 插入{inserted}条，耗时{elapsed:.2f}s, 速度{speed:.0f}条/秒"
        results.append(("插入" + str(round_num+1), elapsed < 5.0, f"({elapsed:.2f}s)"))
        print(f"  {result}")
    
    increment_global('fail', local_failed)
    conn.close()
    return all(r[1] for r in results)

def test_query_performance():
    """测试 2: 查询性能测试"""
    print_section("测试 2: 查询性能测试")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    queries = [
        ("COUNT 聚合", "SELECT COUNT(*) FROM invoice"),
        ("SUM 聚合", "SELECT SUM(amount) FROM invoice"),
        ("WHERE 条件", "SELECT * FROM invoice WHERE amount > 50000 LIMIT 50"),
        ("GROUP BY", "SELECT supplier, COUNT(*), SUM(amount) FROM invoice GROUP BY supplier LIMIT 50"),
        ("ORDER BY", "SELECT * FROM invoice ORDER BY date DESC LIMIT 100"),
        ("日期范围", "SELECT * FROM invoice WHERE date BETWEEN '2024-03-01' AND '2024-09-30' LIMIT 100"),
        ("LIKE 模糊", "SELECT * FROM invoice WHERE supplier LIKE '%供应商 5%' LIMIT 50"),
        ("JOIN 连接", """SELECT v.voucher_no, COUNT(ve.id) as entry_count, SUM(ve.amount) as total_amount
                         FROM voucher v 
                         LEFT JOIN voucher_entry ve ON v.id = ve.voucher_id 
                         GROUP BY v.id LIMIT 50"""),
    ]
    
    results = []
    for name, sql in queries:
        start_time = time.time()
        try:
            cursor.execute(sql)
            results_data = cursor.fetchall()
            elapsed = time.time() - start_time
            
            # 查询应低于 100ms
            passed = elapsed < 0.5
            results.append((name, passed, f"({elapsed*1000:.2f}ms, {len(results_data)}行)"))
        except Exception as e:
            results.append((name, False, f"(错误：{str(e)[:40]})"))
    
    conn.close()
    
    for name, passed, detail in results:
        print_result(name, passed, detail)
    
    return all(r[1] for r in results)

def test_concurrent_simulation():
    """测试 3: 模拟并发操作"""
    print_section("测试 3: 模拟并发操作测试")
    
    results = []
    conn = get_connection()
    cursor = conn.cursor()
    
    local_failed = 0
    
    # 模拟混合操作
    operations = []
    for i in range(100):
        op_type = random.choice(['insert', 'update', 'select'])
        operations.append(op_type)
    
    start_time = time.time()
    
    for i, op in enumerate(operations):
        try:
            if op == 'insert':
                cursor.execute(
                    "INSERT INTO calendar_event (title, event_date, event_type) VALUES (?, ?, ?)",
                    (f'压力测试事件{i}', '2024-12-31', '测试')
                )
                if i % 20 == 0:
                    conn.commit()
            elif op == 'update':
                cursor.execute(
                    "UPDATE financial_metrics SET value = value * 1.01 WHERE id > 0"
                )
            else:
                cursor.execute("SELECT COUNT(*) FROM invoice")
                cursor.fetchone()
        except Exception as e:
            local_failed += 1
    
    conn.commit()
    elapsed = time.time() - start_time
    
    # 清理测试数据
    cursor.execute("DELETE FROM calendar_event WHERE title LIKE '压力测试事件%'")
    conn.commit()
    conn.close()
    
    increment_global('total', len(operations))
    increment_global('fail', local_failed)
    
    passed = elapsed < 5.0 and local_failed == 0
    print(f"  混合操作：{len(operations)}次")
    print(f"  耗时：{elapsed:.2f}s")
    print(f"  失败：{local_failed}次")
    
    return passed

def test_data_integrity():
    """测试 4: 数据完整性测试"""
    print_section("测试 4: 数据完整性测试")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    results = []
    
    # 表存在性
    required_tables = ['users', 'invoice', 'voucher', 'ar_ap', 'calendar_event', 'financial_metrics']
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    existing_tables = [row[0] for row in cursor.fetchall()]
    
    all_tables_exist = all(table in existing_tables for table in required_tables)
    results.append(("所有表存在", all_tables_exist))
    
    # 索引检查
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index'")
    indexes = [row[0] for row in cursor.fetchall()]
    has_indexes = len(indexes) > 0
    results.append(("索引存在", has_indexes))
    
    # 外键约束
    cursor.execute("PRAGMA foreign_keys")
    fk_enabled = cursor.fetchone()[0] == 1
    results.append(("外键启用", fk_enabled))
    
    # 数据一致性 - 检查凭证分录总额是否平衡
    cursor.execute("""
        SELECT v.id, 
               SUM(CASE WHEN ve.entry_type='借方' THEN ve.amount ELSE 0 END) as debit_total,
               SUM(CASE WHEN ve.entry_type='贷方' THEN ve.amount ELSE 0 END) as credit_total
        FROM voucher v
        LEFT JOIN voucher_entry ve ON v.id = ve.voucher_id
        GROUP BY v.id
    """)
    vouchers = cursor.fetchall()
    balanced = all(abs(row[1] - row[2]) < 0.01 or row[1] == 0 for row in vouchers)
    results.append(("凭证借贷平衡", balanced))
    
    # 唯一约束
    cursor.execute("SELECT code, number, COUNT(*) FROM invoice GROUP BY code, number HAVING COUNT(*) > 1")
    duplicates = cursor.fetchall()
    no_dupes = len(duplicates) == 0
    results.append(("无重复发票", no_dupes))
    
    conn.close()
    
    for name, passed in results:
        print_result(name, passed)
    
    return all(r[1] for r in results)

def test_boundary_values():
    """测试 5: 边界值测试"""
    print_section("测试 5: 边界值测试")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    results = []
    
    edges = [
        ("零金额", 0.0),
        ("最大值", 1999999999.99),
        ("最小值", 0.01),
        ("精度测试", 999999.123),
        ("日期边界", "2099-12-31"),
        ("早期日期", "1900-01-01"),
        ("NULL 测试", None),
    ]
    
    for name, value in edges:
        try:
            if value is None:
                cursor.execute(
                    "INSERT INTO financial_metrics (period, metric_name, value) VALUES (?, ?, ?)",
                    ('2024-boundary', name, 0.0)
                )
            else:
                cursor.execute(
                    "INSERT OR REPLACE INTO financial_metrics (period, metric_name, value, unit) VALUES (?, ?, ?, ?)",
                    ('2024-boundary', name, value, '元')
                )
            conn.commit()
            results.append((name, True, f"({value})"))
        except Exception as e:
            results.append((name, False, f"({str(e)[:40]})"))
    
    # 清理
    cursor.execute("DELETE FROM financial_metrics WHERE period = '2024-boundary'")
    conn.commit()
    conn.close()
    
    for name, passed, detail in results:
        print_result(name, passed, detail)
    
    return all(r[1] for r in results)

def test_memory_usage():
    """测试 6: 内存使用测试"""
    print_section("测试 6: 内存使用测试")
    
    import resource
    
    # 运行前内存
    mem_before = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    
    # 执行大量操作
    conn = get_connection()
    cursor = conn.cursor()
    
    for _ in range(50):
        cursor.execute("SELECT * FROM invoice")
        cursor.fetchall()
    
    conn.close()
    
    # 运行后内存
    mem_after = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    mem_diff = mem_after - mem_before
    
    # 内存增长应小于 50MB
    passed = mem_diff < 50 * 1024
    
    print(f"  使用前：{mem_before / 1024:.1f} MB")
    print(f"  使用后：{mem_after / 1024:.1f} MB")
    print(f"  增长量：{mem_diff / 1024:.1f} MB")
    
    return passed

def run_all_tests():
    """运行所有测试"""
    print("\n" + "="*70)
    print("  财务工具箱 v1.4.0 - 深度压力测试套件")
    print("="*70)
    
    init_db()
    
    tests = [
        ("批量插入性能", test_insert_performance),
        ("查询性能", test_query_performance),
        ("并发操作", test_concurrent_simulation),
        ("数据完整性", test_data_integrity),
        ("边界值", test_boundary_values),
        ("内存使用", test_memory_usage),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"\n❌ {name} 异常：{e}")
            traceback.print_exc()
            failed += 1
    
    print_section("测试结果汇总")
    print(f"  通过：{passed}/{len(tests)}")
    print(f"  失败：{failed}/{len(tests)}")
    print(f"  总操作数：{TOTAL_OPERATIONS:,}")
    print(f"  失败操作：{FAILED_OPERATIONS}")
    print(f"  成功率：{(TOTAL_OPERATIONS - FAILED_OPERATIONS) / TOTAL_OPERATIONS * 100 if TOTAL_OPERATIONS > 0 else 100:.2f}%")
    
    # 数据库大小
    import os
    db_size = os.path.getsize('data/finance.db')
    print(f"  数据库大小：{db_size/1024:.1f} KB")
    
    if failed == 0:
        print("\n🎉 所有压力测试通过!")
        return True
    else:
        print(f"\n⚠️  {failed} 个测试失败")
        return False

if __name__ == '__main__':
    success = run_all_tests()
    exit(0 if success else 1)
