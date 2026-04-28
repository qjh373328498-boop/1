---
name: research-paper-workflow
description: 学术研究/论文写作完整工作流。当用户需要写论文、做研究、分析文献、整理资料时自动触发。串联文献收集→内容提取→翻译→总结→格式化→配图→导出 Word/PDF 全流程。
---

# 学术研究/论文写作工作流

这是一个端到端的学术研究和论文写作工作流，整合了多个 skills 来实现高效的研究流程。

## 触发场景

当用户提到以下需求时自动触发：
- "帮我写论文"、"写研究报告"、"做文献综述"
- "分析这个 PDF/文献"、"总结这篇论文"
- "查找相关资料"、"整理研究笔记"
- "把这篇文章转成中文"、"格式化我的论文"
- "生成论文配图"、"制作数据图表"

## 工作流程图

```
┌─────────────┐
│  1. 资料收集  │
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

根据用户提供的资料类型，调用相应的提取 skill：

**1.1 网页资料**
```
调用：baoyu-url-to-markdown
- 读取 URL 内容
- 转换为干净 Markdown
- 保存 HTML 快照
```

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
- --audience technical（技术文档）
- --style formal（学术风格）
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

**4.4 公式/技术图**
```
调用：baoyu-diagram --type illustrative
- 解释机制原理
- 直觉性示意图
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

支持通过参数快速指定工作流阶段：

```bash
# 完整流程
/research-paper-workflow <URL 或文件>

# 仅提取
/research-paper-workflow <URL> --stage extract

# 仅翻译
/research-paper-workflow <文件> --stage translate --to zh-CN

# 仅格式化
/research-paper-workflow <文件> --stage format

# 仅配图
/research-paper-workflow <文件> --stage illustrate

# 导出为 Word
/research-paper-workflow <文件> --export docx

# 导出为 PPT
/research-paper-workflow <文件> --export pptx
```

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
│   └── metadata.json     # 元数据
```

## 使用示例

### 示例 1：分析论文 PDF

用户："帮我分析这篇论文，总结主要内容"

工作流：
1. 读取 PDF（pdf skill）
2. 提取核心内容
3. 格式化总结（baoyu-format-markdown）
4. 生成架构图（baoyu-diagram）
5. 输出结构化笔记

### 示例 2：从YouTube学习

用户："把这个教程视频转成中文笔记"

工作流：
1. 下载字幕（baoyu-youtube-transcript）
2. 翻译成中文（baoyu-translate）
3. 格式化（baoyu-format-markdown）
4. 生成流程图（baoyu-diagram）
5. 保存为 Markdown 笔记

### 示例 3：写论文

用户："帮我写一篇关于AI的研究报告"

工作流：
1. 头脑风暴（brainstorming）
2. 搜索相关资料（websearch）
3. 提取内容（baoyu-url-to-markdown）
4. 翻译整理（baoyu-translate）
5. 格式化（baoyu-format-markdown）
6. 生成配图（baoyu-article-illustrator）
7. 导出 Word（docx skill）

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

1. **大文件处理**：超过 5000 词的内容会自动分块处理
2. **语言检测**：自动检测源语言，无需手动指定
3. **图片配额**：注意 AI 图像生成的 API 配额限制
4. **格式兼容**：导出的 Word/PPT 保持最佳兼容性

## 进阶配置

创建 `~/.baoyu-skills/research-paper-workflow/EXTEND.md` 自定义：

```yaml
# 默认翻译设置
default_translate:
  mode: normal
  to: zh-CN
  audience: academic
  style: formal

# 默认图表风格
default_diagram:
  style: technical-schematic
  type: auto

# 输出路径
output_dir: docs/research
```
