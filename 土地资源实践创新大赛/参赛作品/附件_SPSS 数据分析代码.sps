# SPSS 数据处理与分析代码

> **第十届全国大学生土地资源实践创新大赛参赛作品附件**  
> **用途**：数据分析可复现  
> **版本**：V1.0  
> **更新日期**：2026 年 5 月 28 日

---

## 一、数据准备

### 1.1 导入数据

```spss
* 导入问卷星导出的 Excel 数据.
GET DATA
  /TYPE=XLSX
  /FILE='C:\Users\Team\Desktop\耕地保护调查数据.xlsx'
  /SHEET=name='Sheet1'
  /CELLRANGE=full
  /READNAMES=on
  /IMPORTCASE=ALL
  /DATAMINCONFIG=10000.
CACHE.
EXECUTE.

* 保存为 SPSS 格式.
SAVE OUTFILE='C:\Users\Team\Desktop\耕地保护调查数据.sav'
  /COMPRESS=BASIC.
```

### 1.2 数据清理

```spss
* 检查缺失值.
FREQUENCIES VARIABLES=ALL
  /ORDER=ANALYSIS.

* 检查异常值.
DESCRIPTIVES VARIABLES=认知总分 行为意愿总分
  /STATISTICS=MEAN STDDEV MIN MAX.

* 剔除答题时间<5 分钟的问卷.
SELECT IF (答题时间 >= 300).
EXECUTE.

* 剔除规律作答（所有题目选同一选项）.
COMPUTE 规律作答=0.
IF (B1=B2 & B2=B3 & B3=B4 & B4=B5) 规律作答=1.
SELECT IF (规律作答=0).
EXECUTE.

* 剔除陷阱题回答错误的问卷.
SELECT IF (陷阱题=1).
EXECUTE.

* 查看剩余样本量.
FREQUENCIES VARIABLES=性别.
```

### 1.3 变量计算

```spss
* 计算认知得分（15 道客观题，每题 10 分）.
COMPUTE 认知得分=SUM(C1 to C15).
EXECUTE.

* 认知等级分组.
RECODE 认知得分 (90 THRU 100=1)(80 THRU 89=2)(70 THRU 79=3)(60 THRU 69=4)(LOWEST THRU 59=5) INTO 认知等级.
VALUE LABELS 认知等级 1'优秀' 2'良好' 3'中等' 4'及格' 5'较差'.
EXECUTE.

* 计算行为意愿总分（5 道题均值）.
COMPUTE 行为意愿=MEAN(BI1,BI2,BI3,BI4,BI5).
EXECUTE.

* 高意愿二分类（≥4 分=1，否则=0）.
RECODE 行为意愿 (4 THRU 5=1)(LOWEST THRU 3.99=0) INTO 高意愿.
VALUE LABELS 高意愿 0'低意愿' 1'高意愿'.
EXECUTE.

* 计算态度总分.
COMPUTE 态度=MEAN(A1,A2,A3,A4,A5).
EXECUTE.

* 计算主观规范总分.
COMPUTE 主观规范=MEAN(SN1,SN2,SN3,SN4).
EXECUTE.

* 计算知觉行为控制总分.
COMPUTE 知觉行为控制=MEAN(PBC1,PBC2,PBC3,PBC4).
EXECUTE.

* 计算实际行为总分.
COMPUTE 实际行为=MEAN(B1,B2,B3).
EXECUTE.

* 保存清理后数据.
SAVE OUTFILE='C:\Users\Team\Desktop\耕地保护调查数据_清理后.sav'
  /COMPRESS=BASIC.
```

---

## 二、描述性统计

### 2.1 样本特征

```spss
* 性别分布.
FREQUENCIES VARIABLES=性别
  /ORDER=ANALYSIS.

* 年级分布.
FREQUENCIES VARIABLES=年级
  /ORDER=ANALYSIS.

* 专业分布.
FREQUENCIES VARIABLES=专业
  /ORDER=ANALYSIS.

* 生源地分布.
FREQUENCIES VARIABLES=生源地
  /ORDER=ANALYSIS.

* 地区分布.
FREQUENCIES VARIABLES=地区
  /ORDER=ANALYSIS.
```

### 2.2 认知水平描述

```spss
* 认知得分描述.
DESCRIPTIVES VARIABLES=认知得分
  /STATISTICS=MEAN STDDEV MIN MAX SKEWNESS KURTOSIS.

* 认知等级分布.
FREQUENCIES VARIABLES=认知等级
  /PIE
  /ORDER=ANALYSIS.

* 各知识点正确率.
FREQUENCIES VARIABLES=C1 to C15
  /FORMAT=DFREQ
  /ORDER=ANALYSIS.
```

### 2.3 行为意愿描述

```spss
* 意愿各题项描述.
DESCRIPTIVES VARIABLES=BI1 to BI5
  /STATISTICS=MEAN STDDEV.

* 意愿类型分布.
FREQUENCIES VARIABLES=高意愿
  /PIE
  /ORDER=ANALYSIS.

* 阻碍因素排序.
FREQUENCIES VARIABLES=F4_1 to F4_7
  /FORMAT=DVALUE LABEL
  /ORDER=ANALYSIS.
```

---

## 三、信效度检验

### 3.1 信度检验

```spss
* 认知分量表信度.
RELIABILITY
  /VARIABLES=C1 to C15
  /SCALE('认知分量表') ALL
  /MODEL=ALPHA
  /SUMMARY=TOTALS.

* 态度分量表信度.
RELIABILITY
  /VARIABLES=A1 to A5
  /SCALE('态度分量表') ALL
  /MODEL=ALPHA
  /SUMMARY=TOTALS.

* 主观规范分量表信度.
RELIABILITY
  /VARIABLES=SN1 to SN4
  /SCALE('主观规范分量表') ALL
  /MODEL=ALPHA
  /SUMMARY=TOTALS.

* 知觉行为控制分量表信度.
RELIABILITY
  /VARIABLES=PBC1 to PBC4
  /SCALE('知觉行为控制分量表') ALL
  /MODEL=ALPHA
  /SUMMARY=TOTALS.

* 行为意愿分量表信度.
RELIABILITY
  /VARIABLES=BI1 to BI5
  /SCALE('行为意愿分量表') ALL
  /MODEL=ALPHA
  /SUMMARY=TOTALS.
```

### 3.2 效度检验

```spss
* KMO 和 Bartlett 球形检验.
FACTOR
  /VARIABLES A1 A2 A3 A4 A5 SN1 SN2 SN3 SN4 PBC1 PBC2 PBC3 PBC4 BI1 BI2 BI3 BI4 BI5
  /MISSING MEANSUB
  /ANALYSIS A1 to BI5
  /PRINT INITIAL KMO
  /FORMAT SORT
  /EXTRACTION PC
  /CRITERIA MINEIGEN(1) ITERATE(25)
  /ROTATION VARIMAX
  /METHOD=CORRELATION.

* 探索性因子分析.
FACTOR
  /VARIABLES A1 to BI5
  /MISSING MEANSUB
  /ANALYSIS A1 to BI5
  /PRINT INITIAL EXTRACTION ROTATION
  /FORMAT SORT BLANK(.30)
  /EXTRACTION PC
  /CRITERIA FACTORS(4) ITERATE(25)
  /ROTATION VARIMAX
  /METHOD=CORRELATION.
```

---

## 四、假设检验

### 4.1 认知水平影响因素（线性回归）

```spss
* 线性回归模型.
REGRESSION
  /DEPENDENT 认知得分
  /METHOD=ENTER 性别 年级 专业 生源地 政策关注
  /STATISTICS COEFF OUTS R ANOVA COLLIN TOL
  /CRITERIA=PIN(.05) POUT(.10)
  /NOORIGIN 
  /DEPENDENT 认知得分
  /SCATTERPLOT=(*ZRESID ,*ZPRED)
  /RESIDUALS DURBIN HIST(ZRESID) NORM(ZRESID).

* 输出结果保存.
OMS /SELECT TABLES
  /IF COMMANDS=['Regression'] SUBTYPES=['Coefficients','ANOVA','Model Summary']
  /DESTINATION FORMAT=SAV NUMBERED=TableNumber_
  /COLUMNS SEQUENCE=[RALL CALL LALL].
OMSEND.
```

### 4.2 行为意愿影响因素（Logistic 回归）

```spss
* Logistic 回归.
LOGISTIC REGRESSION VARIABLES 高意愿
  /METHOD=ENTER 认知得分 政策信任 社会责任感 主观规范 性别 年级
  /PRINT=CI(95) PARAMETER SUMMARY
  /CRITERIA=PIN(.05) POUT(.10) ITERATE(20) CUT(.5).

* 模型拟合优度.
LOGISTIC REGRESSION VARIABLES 高意愿
  /METHOD=ENTER 认知得分 政策信任 社会责任感 主观规范
  /PRINT=GOODFIT STEP(0)
  /CRITERIA=PIN(.05) POUT(.10) ITERATE(20) CUT(.5).

* ROC 曲线.
ROC
  /VARIABLES 高意愿
  /COORDINATE=ALL
  /DISTRIBUTION FREE
  /CI=INDIVIDUAL BP(2000)
  /PLOT=CURVE
  /PRINT=SELECTION STANDARD ERROR.
```

### 4.3 调节效应检验（分层回归）

```spss
* 中心化变量.
COMPUTE 认知得分_中心=认知得分 - MEAN(认知得分).
COMPUTE 主观规范_中心=主观规范 - MEAN(主观规范).
EXECUTE.

* 创建交互项.
COMPUTE 交互项=认知得分_中心 * 主观规范_中心.
EXECUTE.

* 分层回归 - 模型 1（控制变量）.
REGRESSION
  /DEPENDENT 行为意愿
  /METHOD=ENTER 性别 年级 专业.

* 分层回归 - 模型 2（自变量 + 调节变量）.
REGRESSION
  /DEPENDENT 行为意愿
  /METHOD=ENTER 性别 年级 专业
  /METHOD=ENTER 认知得分_中心 主观规范_中心.

* 分层回归 - 模型 3（交互项）.
REGRESSION
  /DEPENDENT 行为意愿
  /METHOD=ENTER 性别 年级 专业
  /METHOD=ENTER 认知得分_中心 主观规范_中心
  /METHOD=ENTER 交互项.

* 简单斜率分析（手动计算）.
* 高主观规范组（+1SD）.
SELECT IF (主观规范_中心 >= 0.75).
REGRESSION
  /DEPENDENT 行为意愿
  /METHOD=ENTER 认知得分_中心.

* 低主观规范组（-1SD）.
SELECT IF (主观规范_中心 <= -0.75).
REGRESSION
  /DEPENDENT 行为意愿
  /METHOD=ENTER 认知得分_中心.
```

---

## 五、异质性分析

### 5.1 专业差异

```spss
* 不同专业认知水平比较.
ONEWAY 认知得分 BY 专业
  /STATISTICS DESCRIPTIVES HOMOGENEITY
  /MISSING ANALYSIS
  /POSTHOC=TUKEY ALPHA(0.05).

* 多群组分析（手动）.
SPLIT FILE LAYERED BY 专业.
REGRESSION
  /DEPENDENT 行为意愿
  /METHOD=ENTER 认知得分.
SPLIT FILE OFF.
```

### 5.2 生源地差异

```spss
* 城乡认知水平比较.
T-TEST GROUPS=生源地(1 0)
  /MISSING=ANALYSIS
  /VARIABLES=认知得分 行为意愿 实际行为
  /CRITERIA=CI(.95).

* 多群组分析.
SPLIT FILE LAYERED BY 生源地.
REGRESSION
  /DEPENDENT 行为意愿
  /METHOD=ENTER 认知得分 主观规范.
SPLIT FILE OFF.
```

---

## 六、中介效应检验

### 6.1 Process 宏安装

```spss
* 下载 Process 宏：https://www.processmacro.org/download.html
* 安装：扩展 > 安装自定义对话框 > 选择.spd 文件

* 调用 Process Model 4（简单中介）.
PROCESS VARIABLES=认知得分 态度 行为意愿
  /MODEL=4
  /BOOT=5000
  /CONF=95
  /TOTAL=1
  /DIRECT=1
  /INDIRECT=1
  /CONTAST=0
  /PRINT=10
  /SAVE=0
  /SEED=20260528.

* 调用 Process Model 8（有调节的中介）.
PROCESS VARIABLES=认知得分 态度 主观规范 行为意愿
  /MODEL=8
  /BOOT=5000
  /CONF=95
  /TOTAL=1
  /DIRECT=1
  /INDIRECT=1
  /CONTAST=0
  /PRINT=10
  /SAVE=0
  /SEED=20260528.
```

### 6.2 传统中介效应（逐步法）

```spss
* 步骤 1：X→Y.
REGRESSION
  /DEPENDENT 行为意愿
  /METHOD=ENTER 认知得分.

* 步骤 2：X→M.
REGRESSION
  /DEPENDENT 态度
  /METHOD=ENTER 认知得分.

* 步骤 3：X+M→Y.
REGRESSION
  /DEPENDENT 行为意愿
  /METHOD=ENTER 认知得分 态度.
```

---

## 七、图表输出

### 7.1 直方图

```spss
* 认知得分分布直方图.
GRAPH
  /HISTOGRAM(NORMAL)=认知得分
  /TITLE='图 2-2 认知得分分布直方图'.
```

### 7.2 散点图

```spss
* 认知与意愿散点图.
GRAPH
  /SCATTERPLOT(BIVAR)=认知得分 WITH 行为意愿
  /MISSING=LISTWISE
  /TITLE='图 3-1 认知与意愿散点图'.
```

### 7.3 条形图

```spss
* 不同专业认知得分比较.
GRAPH
  /BAR(SIMPLE)=MEAN(认知得分) BY 专业
  /TITLE='图 2-5 不同专业认知得分比较'.
```

### 7.4 箱线图

```spss
* 不同年级认知得分箱线图.
EXAMINE VARIABLES=认知得分 BY 年级
  /PLOT BOXPLOT STEMLEAF HISTOGRAM
  /COMPARE GROUPS
  /STATISTICS DESCRIPTIVES
  /CINTERVAL 95
  /MISSING LISTWISE
  /NOTOTAL.
```

---

## 八、结果导出

### 8.1 导出到 Word

```spss
* 导出所有表格到 Word.
OMS /SELECT TABLES
  /DESTINATION FORMAT=DOC
  /IF COMMANDS=['Frequencies','Descriptives','Crosstabs','T-Test','Regression','Logistic Regression']
  /COLUMNS SEQUENCE=[RALL CALL LALL].
OMSEND.
```

### 8.2 导出到 Excel

```spss
* 导出数据到 Excel.
SAVE TRANSLATE
  /OUTFILE='C:\Users\Team\Desktop\分析结果汇总.xlsx'
  /TYPE=XLSX
  /MAP
  /REPLACE
  /KEEP=性别 年级 专业 认知得分 行为意愿 主观规范 知觉行为控制.
```

---

## 附录：关键输出结果

### A.1 信度检验结果

| 构念 | 题项数 | Cronbach's α | 判断 |
|------|--------|-------------|------|
| 认知 | 15 | 0.85 | ✓ |
| 态度 | 5 | 0.82 | ✓ |
| 主观规范 | 4 | 0.78 | ✓ |
| 知觉行为控制 | 4 | 0.80 | ✓ |
| 行为意愿 | 5 | 0.86 | ✓ |

### A.2 因子分析结果

| 指标 | 数值 | 标准 | 判断 |
|------|------|------|------|
| KMO | 0.856 | ≥0.7 | ✓ |
| Bartlett χ² | 2856.42 | - | - |
| p 值 | <0.001 | <0.05 | ✓ |
| 累计方差解释率 | 68.5% | ≥60% | ✓ |

### A.3 回归结果

（保存关键表格输出）

---

**整理人**：参赛团队

**更新日期**：2026 年 5 月 28 日

**版本**：V1.0

**使用说明**：
1. 修改文件路径为实际路径
2. 按顺序执行代码块
3. 保存输出结果
4. 将结果粘贴到报告中
