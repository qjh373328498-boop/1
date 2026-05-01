---
name: research-paper-workflow-isolated
description: 学术研究/论文写作工作流（隔离知识库模式）。默认使用此工作流，仅依赖外部文献和用户提供的资料，不参考本地知识库，确保论文原创性和学术诚信。
---

# 学术研究/论文写作工作流（隔离知识库模式）

**⚠️ 重要说明**：

这是**默认的论文写作工作流**，采用**隔离模式**：
- ❌ **不参考**本地知识库内容（`知识库/` 目录）
- ❌ **不使用**个人学业档案、比赛资料等索引文档
- ✅ **仅依赖**外部权威文献和用户明确提供的资料
- ✅ **确保**论文原创性和学术诚信

## 触发场景

当用户提到以下需求时**默认触发此工作流**：
- "帮我写论文"、"写研究报告"、"做文献综述"
- "分析这个 PDF/文献"、"总结这篇论文"
- "查找相关资料"、"整理研究笔记"
- "把这篇文章转成中文"、"格式化我的论文"
- "生成论文配图"、"制作数据图表"

**除非用户明确说**：
- "可以参考知识库"
- "用知识库的资料帮我..."
- "结合我之前的资料..."

否则**始终使用此隔离模式**。

## 工作流程图

```
┌─────────────┐
│  1. 资料收集  │  ← 仅外部文献 + 用户提供
│  URL/PDF/   │
│  YouTube    │
└──────┬──────┘
       ↓
┌─────────────┐
│  2. 内容提取  │
│  转 Markdown  │
└──────┬──────┘
       ↓
┌─────────────┐
│  3. 翻译/    │
│  本地化      │
└──────┬──────┘
       ↓
┌─────────────┐
│  4. 格式化/  │
│  结构化      │
└──────┬──────┘
       ↓
┌─────────────┐
│  5. 配图/    │
│  图表生成    │
└──────┬──────┘
       ↓
┌─────────────┐
│  6. 导出/    │
│  发布        │
└─────────────┘
```

## 完整工作流程

### 阶段 1：资料收集与提取

**严格限制资料来源**：
- ✅ 用户明确提供的 PDF/Word/Excel 文件
- ✅ 用户提供的 URL 链接
- ✅ 外部学术数据库（知网、Web of Science 等）
- ✅ YouTube 教程视频
- ❌ **禁止**主动读取 `知识库/` 目录内容
- ❌ **禁止**引用个人学业档案索引

**1.1 网页资料**
```bash
# 提取网页文献为 Markdown
baoyu-url-to-markdown \
  --url "https://example.com/article" \
  --output 文献资料/{主题}/article.md

# 批量提取参考文献
baoyu-url-to-markdown \
  --urls references.txt \
  --output-dir 文献资料/{主题}/

# 输出：
# - article.md（干净的 Markdown）
# - article.html（原始 HTML 快照）
# - meta.json（元数据：标题/作者/日期）
```

**用途**：
- 提取官方博客文章
- 下载技术文档
- 保存网页文献
- 批量整理参考文献

**1.2 YouTube 视频**
```
调用：baoyu-youtube-transcript
- 下载字幕/讲义
- 支持多语言
- 可选章节划分
- 输出带时间戳的文本
```

**1.3 PDF 文档**
```
调用：pdf skill
- 提取文本内容
- 保留结构信息
- 处理表格和公式
```

**1.4 Word/Excel/PPT**
```
调用：docx/xlsx/pptx skills
- 提取文档内容
- 转换为目标格式
```

### 阶段 2：内容翻译（如需要）

如果资料是外文或用户要求翻译：

```
调用：baoyu-translate
模式选择：
- quick：简短内容快速翻译
- normal（默认）：分析后翻译，适合文章
- refined：完整出版级流程（分析→翻译→润色）

参数：
- --to zh-CN（默认中文）
- --audience academic（学术风格）
- --style formal（正式文体）
```

### 阶段 3：格式化与结构化

```
调用：baoyu-format-markdown
- 自动生成 YAML frontmatter
  - title: 标题
  - slug: 路径
  - summary: 摘要
  - coverImage: 封面图
- 格式化标题层级
- 加粗关键点
- 整理列表和代码块
- 输出：{filename}-formatted.md
```

### 阶段 4：配图与图表生成

根据内容类型选择合适的可视化：

**4.1 流程图/架构图**
```
调用：baoyu-diagram
- flowchart：流程说明
- sequence：协议/交互流程
- structural：架构/组件图
- 输出：SVG 格式，支持暗黑模式
```

**4.2 数据图表**
```
调用：baoyu-infographic
- 21 种布局可选
- 17 种视觉风格
- 适合数据可视化
```

**4.3 论文配图**
```
调用：baoyu-article-illustrator
- 自动分析文章结构
- 识别需要配图的位置
- 生成配套插图
```

### 阶段 5：整合与导出

**5.1 转 Word 文档**
```
调用：docx skill
- 将 Markdown 转为 Word
- 保留格式和样式
- 适合论文提交
```

**5.2 转 PDF**
```
调用：pdf skill（转换模式）
- 生成 PDF 格式
- 适合分享和打印
```

**5.3 转 PPT**
```
调用：baoyu-slide-deck
- 从内容生成幻灯片
- 16 种预设风格
- 自动合并为.pptx 和.pdf
```

## 快捷命令模式

```bash
# 完整流程（隔离模式）
/research-paper-workflow-isolated <URL 或文件>

# 仅提取
/research-paper-workflow-isolated <URL> --stage extract

# 仅翻译
/research-paper-workflow-isolated <文件> --stage translate --to zh-CN

# 仅格式化
/research-paper-workflow-isolated <文件> --stage format

# 仅配图
/research-paper-workflow-isolated <文件> --stage illustrate

# 导出为 Word
/research-paper-workflow-isolated <文件> --export docx

# 导出为 PPT
/research-paper-workflow-isolated <文件> --export pptx
```

## 学术诚信保障

### 引用规范
- 所有引用必须标注**外部权威来源**
- 不使用个人笔记作为引用来源
- 区分"常识"和"需要引用的观点"

### 原创性检查
- 生成内容必须基于用户提供的资料和外部文献
- 避免直接复制粘贴（除非加引用标注）
- 重要观点必须标注出处

### 资料来源优先级
1. **学术期刊论文**（同行评审）
2. **学术著作**（出版社出版）
3. **官方报告**（政府、国际组织）
4. **权威媒体**（主流新闻媒体）
5. **用户提供的资料**

## 输出产物

执行完成后在 `docs/research/` 目录下生成：

```
docs/research/
├── {topic}/
│   ├── raw/              # 原始提取内容
│   ├── translated/       # 翻译版本
│   ├── formatted/        # 格式化版本
│   ├── figures/          # 生成的图表
│   ├── output/           # 最终导出文件
│   └── references.md     # 参考文献列表（仅外部来源）
```

## 使用示例

### 示例 1：分析论文 PDF（隔离模式）

用户："帮我分析这篇论文，总结主要内容"

工作流：
1. 读取用户提供的 PDF
2. 提取核心内容
3. 格式化总结（baoyu-format-markdown）
4. 生成架构图（baoyu-diagram）
5. 输出结构化笔记
6. ❌ **不参考**知识库中的相关主题

### 示例 2：写课程论文（隔离模式）

用户："帮我写一篇关于环境会计的课程论文"

工作流：
1. 搜索外部学术文献（知网、Google Scholar）
2. 提取文献内容（baoyu-url-to-markdown）
3. 翻译整理（baoyu-translate）
4. 格式化（baoyu-format-markdown）
5. 生成配图（baoyu-article-illustrator）
6. 导出 Word（docx skill）
7. ❌ **不使用**知识库中的会计专业资料

## 依赖 Skills

| Skill | 用途 |
|-------|------|
| baoyu-url-to-markdown | 网页内容提取 |
| baoyu-youtube-transcript | 视频字幕下载 |
| pdf | PDF 文档处理 |
| docx | Word 文档处理 |
| baoyu-translate | 翻译 |
| baoyu-format-markdown | 格式化 |
| baoyu-diagram | 图表生成 |
| baoyu-infographic | 信息图表 |
| baoyu-article-illustrator | 文章配图 |
| baoyu-slide-deck | PPT 生成 |

## 注意事项

1. **隔离原则**：默认不读取 `知识库/` 目录
2. **来源标注**：所有引用必须标注外部权威来源
3. **学术诚信**：不抄袭、不捏造数据
4. **大文件处理**：超过 5000 词的内容会自动分块处理
5. **语言检测**：自动检测源语言，无需手动指定
6. **图片配额**：注意 AI 图像生成的 API 配额限制
7. **格式兼容**：导出的 Word/PPT 保持最佳兼容性

## 与知识库模式的区别

| 特性 | 隔离模式（默认） | 知识库模式（需明确） |
|------|-----------------|---------------------|
| 资料来源 | 仅外部文献 + 用户提供 | 外部文献 + 知识库 + 用户提供 |
| 适用场景 | 正式论文、学术竞赛 | 课程作业、学习笔记、草稿 |
| 引用来源 | 权威外部来源 | 可包含个人笔记 |
| 原创性 | 高（学术级） | 中（学习级） |
| 触发条件 | 默认 | 用户明确说"参考知识库" |
