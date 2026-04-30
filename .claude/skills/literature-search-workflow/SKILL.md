---
name: literature-search-workflow
description: 学术文献检索与引用工作流。当用户需要查找文献、管理参考文献、生成引用格式时自动触发。串联文献搜索→下载管理→阅读笔记→引用生成全流程。
arguments:
  - name: topic
    description: 研究主题/关键词
    required: true
  - name: citation_style
    description: 引用格式（GB/T 7714, APA, MLA 等）
    required: false
---

# 学术文献检索与引用工作流

专为学术写作设计的文献工作流，整合了文献搜索、下载管理、阅读笔记、引用生成等功能。

## 触发场景

当用户提到以下需求时自动触发：
- "查找 XXX 相关文献"、"找论文资料"
- "生成参考文献"、"引用格式"
- "整理文献笔记"、"文献综述"
- "知网搜索"、"Google Scholar"

## 完整工作流程

```
┌─────────────┐
│  1. 文献搜索  │
│  多平台检索  │
└──────┬──────┘
       ↓
┌─────────────┐
│  2. 文献管理  │
│  分类整理   │
└──────┬──────┘
       ↓
┌─────────────┐
│  3. 阅读笔记  │
│  摘要提取   │
└──────┬──────┘
       ↓
┌─────────────┐
│  4. 引用生成  │
│  格式化     │
└──────┬──────┘
       ↓
┌─────────────┐
│  5. 文献综述  │
│  整合分析   │
└─────────────┘
```

## 阶段 1：文献搜索

**1.1 学术数据库**
```markdown
## 推荐数据库

### 中文数据库
- **中国知网 (CNKI)**：https://www.cnki.net/
  - 学术期刊、博硕士论文、会议论文
- **万方数据**：https://www.wanfangdata.com.cn/
  - 学术期刊、学位论文
- **维普期刊**：http://www.cqvip.com/
  - 中文科技期刊

### 英文数据库
- **Google Scholar**：https://scholar.google.com/
  - 综合学术搜索
- **Web of Science**：https://www.webofscience.com/
  - SCI/SSCI 核心数据库
- **Scopus**：https://www.scopus.com/
  - 大型摘要和引文数据库
- **JSTOR**：https://www.jstor.org/
  - 人文社科期刊

### 经济/会计专业数据库
- **EBSCO Business Source**
- **ProQuest**
- **Wind 资讯**（金融数据）
- **CSMAR**（国泰安）
```

**1.2 搜索策略**
```markdown
## 搜索关键词构建

### 核心关键词
- 主概念：{如：环境会计}
- 同义词：{如：绿色会计、生态会计}
- 英文：{如：environmental accounting, green accounting}

### 搜索表达式
```
# 知网搜索示例
SU='环境会计' + '绿色会计' AND KY='信息披露'

# Google Scholar 示例
"environmental accounting" OR "green accounting" 
AND "disclosure" 
AND "china"

# 限定条件
- 时间：2020-2026（近 5 年）
- 文献类型：期刊论文
- 来源类别：核心期刊/CSSCI
```
```

**1.3 搜索指令**
```bash
# 调用 websearch 工具搜索

/search "environmental accounting research 2025"
  --filter "site:scholar.google.com"
  --count 20

/search "环境会计 信息披露 研究"
  --filter "site:cnki.net"
  --count 20
```

## 阶段 2：文献管理

**2.1 文献分类体系**
```markdown
## 文献分类

### 按重要性
- 🔴 核心文献（10-15 篇）：必须精读
- 🟡 重要文献（20-30 篇）：选读摘要结论
- 🟢 一般文献（50+ 篇）：浏览标题即可

### 按主题
- 环境会计理论基础
- 环境会计信息披露
- 环境会计与企业绩效
- 环境会计政策规制

### 按研究方法
- 实证研究
- 案例研究
- 规范研究
- 综述
```

**2.2 文献信息记录**
```markdown
## 文献信息卡片

**编号**：Lit-2025-001

**基本信息**
- 标题：{完整标题}
- 作者：{作者姓名}
- 年份：{发表年份}
- 期刊：{期刊名}
- 卷期：{卷 (期)}
- 页码：{起止页码}
- DOI: {DOI 号}

**获取信息**
- 来源：{数据库名称}
- 下载日期：{日期}
- PDF 路径：{./pdfs/文件名.pdf}
- 链接：{URL}

**阅读状态**
- 状态：□ 待读 □ 阅读中 □ 已读完
- 优先级：🔴 高 / 🟡 中 / 🟢 低
- 质量评分：⭐⭐⭐⭐⭐（1-5 星）
```

**2.3 Zotero 集成**
```markdown
## Zotero 使用规范

### 文件夹结构
Zotero Library/
├── 01_待整理/
├── 02_按主题/
│   ├── 环境会计理论/
│   ├── 信息披露/
│   └── 企业绩效/
├── 03_按项目/
│   └── {论文题目}/
└── 04_已读/

### 标签规范
- #核心理论
- #实证研究
- #研究方法/定量
- #重要引用
```

## 阶段 3：阅读笔记

**3.1 标准阅读笔记模板**
```markdown
# 文献阅读笔记

## 文献信息
**标题**：{标题}
**作者**：{作者}
**期刊**：{期刊名}
**年份**：{年份}

## 研究问题
- 核心研究问题是什么？
- 为什么这个问题重要？

## 理论基础
- 使用了什么理论？
- 理论框架是什么？

## 研究方法
- 研究设计：□ 实证 □ 案例 □ 规范
- 数据来源：{数据来源}
- 样本：{样本描述}
- 方法：{回归分析/内容分析等}

## 主要发现
1. {发现 1}
2. {发现 2}
3. {发现 3}

## 创新点
- 理论贡献
- 方法创新
- 实践启示

## 局限性
- 作者承认的局限
- 自己的批评

## 对我的研究启发
- 可以引用的观点
- 可以借鉴的方法
- 可以拓展的方向

## 重要摘录
> "重要原文" (p.XX)

## 引用记录
- 本文引用了：[文献 A], [文献 B]
- 被 [文献 C] 引用
```

**3.2 批量文献摘要**
```markdown
## 文献综述表格

| 作者 | 年份 | 研究问题 | 方法 | 主要发现 | 局限 |
|------|------|----------|------|----------|------|
| 张三 | 2025 | XXX | 回归分析 | XXX | 样本单一 |
| 李四 | 2024 | XXX | 案例研究 | XXX | 普适性差 |
```

## 阶段 4：引用生成

**4.1 支持的引用格式**
```markdown
## 常用引用格式

### GB/T 7714-2015（中国国家标准）
**期刊论文**：
[序号] 主要责任者。题名：其他题名信息 [J]. 刊名，年，卷 (期): 起止页码.

示例：
[1] 张三，李四。环境会计信息披露研究 [J]. 会计研究，2025, (1): 45-56.

**学位论文**：
[序号] 作者。题名 [D]. 保存地点：保存单位，年份.

示例：
[2] 王五。环境会计与企业绩效关系研究 [D]. 北京：中国人民大学，2025.

### APA 格式（第 7 版）
**期刊论文**：
Author, A. A., & Author, B. B. (Year). Title of article. *Title of Periodical, volume*(issue), pages. https://doi.org/xxx

示例：
Wang, J., & Li, M. (2025). Environmental accounting disclosure. *Accounting Research*, (1), 45-56. https://doi.org/10.1234/ar.2025.01.005

### MLA 格式
**期刊论文**：
Author(s). "Title of Article." *Title of Periodical*, vol. volume, no. issue, Year, pp. pages.

### Chicago 格式
**脚注格式**：
1. Author, "Title," *Journal* volume, no. issue (Year): page.
```

**4.2 自动化工具**
```markdown
## 参考文献管理工具

### Zotero + Better BibTeX
- 自动抓取文献元数据
- Word 插件插入引用
- 自动生成参考文献列表

### 知网研学
- 中文文献管理
- 一键生成 GB/T 7714 格式

### 在线工具
- **Cite This For Me**：https://www.citethisforme.com/
- **BibTeX Generator**：https://biblatex.github.io/
```

**4.3 引用生成命令**
```
/generate-citation
  --style "GB/T 7714"
  --type "journal"
  --title "环境会计信息披露研究"
  --author "张三，李四"
  --journal "会计研究"
  --year "2025"
  --issue "1"
  --pages "45-56"
```

## 阶段 5：文献综述

**5.1 文献综述结构**
```markdown
# 文献综述

## 引言
- 研究背景
- 综述范围
- 组织结构

## 理论基础
### 环境会计理论发展
- 早期研究（1990s）
- 理论框架建立（2000s）
- 最新发展（2010s-至今）

## 主题 1：环境会计信息披露
### 披露内容研究
- 国内研究现状
- 国外研究现状

### 披露影响因素
- 制度因素
- 公司特征
- 高层管理者特征

## 主题 2：环境会计与企业绩效
### 正相关论
- 支持证据
- 理论解释

### 负相关论
- 支持证据
- 理论解释

### 不确定关系论
- 支持证据
- 权变因素

## 研究评述
- 已有研究贡献
- 存在的不足
- 未来研究方向

## 结论
```

**5.2 文献分析矩阵**
```
                  │ 环境会计披露 │ 环境绩效 │ 财务绩效 │
──────────────────┼─────────────┼─────────┼─────────┤
王五 (2025)       │     ✓       │    ✓    │    ✓    │
张三 (2024)       │     ✓       │    ✓    │         │
李四 (2023)       │     ✓       │         │    ✓    │
```

## 输出产物

```
文献资料/{研究主题}/
├── 01-搜索结果/
│   ├── 知网搜索结果.md
│   ├── Google Scholar 搜索结果.md
│   └── 文献清单.xlsx
├── 02-文献 PDF/
│   ├── 核心文献/
│   └── 一般文献/
├── 03-阅读笔记/
│   ├── 笔记 1-{标题}.md
│   ├── 笔记 2-{标题}.md
│   └── 文献综述表格.md
├── 04-参考文献/
│   ├── references_gbt7714.txt
│   ├── references_apa.txt
│   └── references_bibtex.bib
└── 05-文献综述/
    └── 文献综述_完整版.md
```

## 快捷命令

```bash
# 完整文献检索流程
/literature-search-workflow {研究主题}

# 仅搜索文献
/literature-search-workflow {主题} --stage search

# 仅生成引用
/literature-search-workflow {主题} --stage cite

# 指定引用格式
/literature-search-workflow {主题} --citation-style APA

# 导出参考文献
/literature-search-workflow {主题} --export bibtex
```

## 会计学专业搜索示例

```markdown
## 搜索示例：环境会计信息披露

### 中文搜索词
- 环境会计
- 绿色会计
- 生态会计
- 环境信息披露
- 企业社会责任报告

### 英文搜索词
- environmental accounting
- green accounting
- environmental disclosure
- sustainability reporting
- CSR reporting

### 组合搜索
```
("environmental accounting" OR "green accounting") 
AND ("disclosure" OR "reporting") 
AND ("firm performance" OR "financial performance")
```
```

## 依赖 Skills

| Skill | 用途 |
|-------|------|
| websearch | 搜索学术文献 |
| baoyu-url-to-markdown | 提取网页内容 |
| pdf | 阅读 PDF 文献 |
| baoyu-format-markdown | 格式化笔记 |
| xlsx | 导出文献清单 |

## 注意事项

1. **优先核心期刊**：优先选择核心期刊/权威期刊
2. **注意时效性**：优先近 5 年文献
3. **追踪重要作者**：关注领域内大牛
4. **善用引用链**：从参考文献找到更多文献
5. **做好笔记**：边读边记，方便后续引用
