---
name: data-analysis-workflow
description: 数据分析与可视化工作流。当用户需要处理财务数据、制作图表、进行分析时自动触发。串联数据导入→清洗→分析→可视化→报告全流程。
arguments:
  - name: data_source
    description: 数据来源（Excel 文件/数据库/API）
    required: false
  - name: analysis_type
    description: 分析类型（财务比率/趋势/对比）
    required: false
---

# 数据分析与可视化工作流

专为会计学专业设计的数据分析工作流，整合了 Excel 处理、Python 分析、财务指标计算、可视化图表生成等功能。

## 触发场景

当用户提到以下需求时自动触发：
- "分析这个 Excel 数据"、"处理财务数据"
- "制作图表"、"数据可视化"
- "计算财务比率"、"趋势分析"
- "用 Python 分析数据"、"pandas 处理"

## 完整工作流程

```
┌─────────────┐
│  1. 数据导入  │
│  Excel/CSV  │
└──────┬──────┘
       ↓
┌─────────────┐
│  2. 数据清洗  │
│  预处理     │
└──────┬──────┘
       ↓
┌─────────────┐
│  3. 财务分析  │
│  指标计算   │
└──────┬──────┘
       ↓
┌─────────────┐
│  4. 可视化   │
│  图表生成   │
└──────┬──────┘
       ↓
┌─────────────┐
│  5. 分析报告  │
│  洞察总结   │
└─────────────┘
```

## 阶段 1：数据导入

**1.1 支持的数据格式**
```markdown
## 数据源类型

### Excel 文件
- .xlsx - Excel 2007+
- .xls - Excel 97-2003
- .xlsm - 启用宏的 Excel

### 其他格式
- .csv - 逗号分隔值
- .json - JSON 数据
- 数据库 - MySQL/PostgreSQL
- API - 财经数据接口
```

**1.2 Python 读取代码模板**
```python
import pandas as pd

# 读取 Excel
df = pd.read_excel('财务报表.xlsx', sheet_name='利润表')

# 读取 CSV
df = pd.read_csv('销售数据.csv', encoding='utf-8')

# 读取多个 sheet
sheets_dict = pd.read_excel('财务报表.xlsx', sheet_name=None)

# 查看数据
print(df.head())
print(df.info())
print(df.describe())
```

## 阶段 2：数据清洗

**2.1 常见清洗操作**
```python
import pandas as pd
import numpy as np

# 1. 删除重复值
df = df.drop_duplicates()

# 2. 处理缺失值
df = df.dropna()  # 删除缺失值
# 或
df = df.fillna(0)  # 填充为 0
# 或
df['科目'] = df['科目'].fillna('未知')  # 填充特定值

# 3. 数据类型转换
df['日期'] = pd.to_datetime(df['日期'])
df['金额'] = pd.to_numeric(df['金额'], errors='coerce')

# 4. 字符串处理
df['科目名称'] = df['科目名称'].str.strip()  # 去除空格
df['科目代码'] = df['科目代码'].str.zfill(6)  # 补零

# 5. 异常值处理
Q1 = df['金额'].quantile(0.25)
Q3 = df['金额'].quantile(0.75)
IQR = Q3 - Q1
df = df[(df['金额'] >= Q1 - 1.5*IQR) & 
        (df['金额'] <= Q3 + 1.5*IQR)]
```

**2.2 财务数据特殊处理**
```python
# 会计科目标准化
subject_mapping = {
    '货币资金': '货币资金',
    '现金': '货币资金',
    '银行存款': '货币资金',
    '应收账款': '应收账款',
    '应收帐款': '应收账款',  # 繁简统一
}
df['科目'] = df['科目'].map(subject_mapping)

# 金额单位统一（万元→元）
df.loc[df['单位'] == '万元', '金额'] *= 10000
```

## 阶段 3：财务分析

**3.1 财务比率计算**
```python
def calculate_financial_ratios(df):
    """
    计算财务比率指标
    """
    ratios = {}
    
    # 1. 偿债能力
    ratios['流动比率'] = df['流动资产'] / df['流动负债']
    ratios['速动比率'] = (df['流动资产'] - df['存货']) / df['流动负债']
    ratios['资产负债率'] = df['负债总额'] / df['资产总额']
    
    # 2. 营运能力
    ratios['应收账款周转率'] = df['营业收入'] / df['应收账款平均余额']
    ratios['存货周转率'] = df['营业成本'] / df['存货平均余额']
    ratios['总资产周转率'] = df['营业收入'] / df['资产平均总额']
    
    # 3. 盈利能力
    ratios['销售毛利率'] = (df['营业收入'] - df['营业成本']) / df['营业收入']
    ratios['销售净利率'] = df['净利润'] / df['营业收入']
    ratios['净资产收益率'] = df['净利润'] / df['净资产']
    
    # 4. 发展能力
    ratios['收入增长率'] = df['营业收入'].pct_change()
    ratios['利润增长率'] = df['净利润'].pct_change()
    
    return pd.DataFrame(ratios)

# 使用示例
ratios_df = calculate_financial_ratios(financial_df)
```

**3.2 杜邦分析体系**
```python
def dupont_analysis(df):
    """
    杜邦分析法：ROE 分解
    """
    df['ROE'] = df['净利润'] / df['净资产']
    df['净利率'] = df['净利润'] / df['营业收入']
    df['周转率'] = df['营业收入'] / df['资产总额']
    df['权益乘数'] = df['资产总额'] / df['净资产']
    
    # 验证：ROE = 净利率 × 周转率 × 权益乘数
    df['ROE_验证'] = df['净利率'] * df['周转率'] * df['权益乘数']
    
    return df[['ROE', '净利率', '周转率', '权益乘数', 'ROE_验证']]
```

**3.3 趋势分析**
```python
# 同比增长率
df['收入_同比'] = df['营业收入'].pct_change(periods=1) * 100

# 环比增长率
df['收入_环比'] = df['营业收入'].pct_change(periods=1) * 100

# 移动平均
df['收入_MA3'] = df['营业收入'].rolling(window=3).mean()
df['收入_MA5'] = df['营业收入'].rolling(window=5).mean()

# 复合增长率 (CAGR)
def cagr(start, end, years):
    return (end / start) ** (1 / years) - 1
```

**3.4 对比分析**
```python
# 同行业对比
compare_df = pd.concat([
    公司 A_数据，公司 B_数据，公司 C_数据
], axis=1, keys=['公司 A', '公司 B', '公司 C'])

# 与行业平均对比
df['与行业平均差异'] = df['毛利率'] - 行业平均毛利率

# 结构分析（共同比分析）
df['收入占比'] = df['营业收入'] / df['营业收入'].sum()
df['成本占比'] = df['营业成本'] / df['营业成本'].sum()
```

## 阶段 4：可视化

**4.1 趋势图**
```python
import matplotlib.pyplot as plt
import seaborn as sns

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# 收入趋势图
plt.figure(figsize=(12, 6))
plt.plot(df['年份'], df['营业收入'], marker='o', linewidth=2, label='营业收入')
plt.title('营业收入趋势分析', fontsize=16)
plt.xlabel('年份')
plt.ylabel('营业收入（万元）')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('收入趋势图.png', dpi=300, bbox_inches='tight')
plt.show()
```

**4.2 对比柱状图**
```python
# 多公司财务指标对比
plt.figure(figsize=(14, 7))
x = np.arange(len(companies))
width = 0.25

plt.bar(x - width, company_A_ratios, width, label='公司 A')
plt.bar(x, company_B_ratios, width, label='公司 B')
plt.bar(x + width, company_C_ratios, width, label='公司 C')

plt.xlabel('公司')
plt.ylabel('财务比率')
plt.title('财务比率对比分析')
plt.xticks(x, companies)
plt.legend()
plt.savefig('财务比率对比.png', dpi=300)
```

**4.3 结构饼图**
```python
# 成本费用结构
plt.figure(figsize=(10, 8))
plt.pie(costs, labels=cost_labels, autopct='%1.1f%%', startangle=90)
plt.title('成本费用结构分析')
plt.savefig('成本结构图.png', dpi=300)
```

**4.4 财务仪表板**
```python
# 创建多子图仪表板
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# 左上：收入趋势
axes[0, 0].plot(df['年份'], df['营业收入'])
axes[0, 0].set_title('收入趋势')

# 右上：利润率
axes[0, 1].bar(df['年份'], df['净利率'])
axes[0, 1].set_title('净利率')

# 左下：资产负债率
axes[1, 0].plot(df['年份'], df['资产负债率'])
axes[1, 0].set_title('资本结构')

# 右下：ROE 趋势
axes[1, 1].plot(df['年份'], df['ROE'])
axes[1, 1].set_title('净资产收益率')

plt.tight_layout()
plt.savefig('财务仪表板.png', dpi=300)
```

**4.5 热力图**
```python
# 相关性热力图
correlation = df[['收入', '成本', '利润', '资产', '负债']].corr()
plt.figure(figsize=(10, 8))
sns.heatmap(correlation, annot=True, cmap='RdYlBu_r', center=0)
plt.title('财务指标相关性分析')
plt.savefig('相关性热力图.png', dpi=300)
```

## 阶段 5：分析报告

**5.1 报告模板**
```markdown
# 财务分析报告

## 分析概要
- **分析对象**：{公司/项目名}
- **数据期间**：{起始日期} - {结束日期}
- **数据来源**：{来源}
- **分析日期**：{日期}

## 核心发现

### 1. 整体表现
- 营业收入：{X}万元，同比增长{X}%
- 净利润：{X}万元，净利率{X}%
- 资产总额：{X}万元

### 2. 优势
- {优势 1}
- {优势 2}

### 3. 风险点
- ⚠️ {风险 1}
- ⚠️ {风险 2}

## 详细分析

### 偿债能力分析
| 指标 | 数值 | 行业平均 | 评价 |
|------|------|----------|------|
| 流动比率 | X | X | 偏强/偏弱 |
| 资产负债率 | X% | X% | 合理/偏高 |

### 盈利能力分析
...

## 建议
1. {建议 1}
2. {建议 2}
```

## 快捷命令

```bash
# 完整数据分析流程
/data-analysis-workflow {数据文件}

# 仅数据清洗
/data-analysis-workflow {文件} --stage clean

# 仅财务比率计算
/data-analysis-workflow {文件} --stage ratios

# 仅可视化
/data-analysis-workflow {文件} --stage visualize

# 生成分析报告
/data-analysis-workflow {文件} --stage report

# 指定分析类型
/data-analysis-workflow {文件} --type dupont  # 杜邦分析
/data-analysis-workflow {文件} --type trend   # 趋势分析
/data-analysis-workflow {文件} --type compare # 对比分析
```

## Python 环境配置

```bash
# 创建虚拟环境
python -m venv data_analysis

# 激活环境
# Windows: data_analysis\Scripts\activate
# Mac/Linux: source data_analysis/bin/activate

# 安装依赖
pip install pandas numpy matplotlib seaborn openpyxl xlsxwriter
pip install scipy statsmodels
pip install jupyter notebook
```

## 输出产物

```
数据分析报告/{项目名}/
├── 01-原始数据/
│   └── {原始文件}.xlsx
├── 02-清洗后数据/
│   └── {清洗后文件}.csv
├── 03-分析结果/
│   ├── 财务比率表.xlsx
│   └── 分析数据.csv
├── 04-可视化图表/
│   ├── 趋势图.png
│   ├── 对比图.png
│   ├── 结构图.png
│   └── 仪表板.png
├── 05-分析报告/
│   └── 财务分析报告.md
└── 06-Python 代码/
    └── 分析脚本.ipynb
```

## 依赖 Skills

| Skill | 用途 |
|-------|------|
| xlsx | Excel 文件处理 |
| baoyu-infographic | 信息图表生成 |
| baoyu-diagram | 流程图/关系图 |
| baoyu-format-markdown | 报告格式化 |

## 注意事项

1. **数据备份**：分析前备份原始数据
2. **单位统一**：确保所有数据单位一致
3. **异常检查**：识别并处理异常值
4. **结果验证**：交叉验证分析结果
5. **可视化简洁**：图表要清晰易懂
