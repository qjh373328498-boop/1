---
name: knowledge-manage-workflow
description: 文档处理与知识管理工作流。当用户需要处理 PDF/Word/Excel、整理资料、构建知识库时自动触发。串联文档提取→内容总结→格式化→知识组织→检索利用全流程。
---

# 文档处理与知识管理工作流

这是一个端到端的文档处理和知识管理工作流，整合了 PDF/Word/Excel 处理、内容总结、格式化、知识组织等 skills，帮助构建个人/团队知识库。

## 触发场景

当用户提到以下需求时自动触发：
- "处理这个 PDF"、"提取 Word 内容"
- "整理这些资料"、"建知识库"
- "总结这个文档"、"提取关键信息"
- "搜索相关内容"、"找 XXX 资料"
- "把 Excel 转成 Markdown"、"PPT 转文档"

## 工作流程图

```
┌─────────────┐
│  1. 文档导入  │
│  多格式支持  │
└──────┬──────┘
       ↓
┌─────────────┐
│  2. 内容提取  │
│  结构化处理  │
└──────┬──────┘
       ↓
┌─────────────┐
│  3. 内容总结  │
│  关键信息   │
└──────┬──────┘
       ↓
┌─────────────┐
│  4. 格式化   │
│  标准化     │
└──────┬──────┘
       ↓
┌─────────────┐
│  5. 知识组织  │
│  分类标签   │
└──────┬──────┘
       ↓
┌─────────────┐
│  6. 检索/    │
│  利用        │
└─────────────┘
```

## 完整工作流程

### 阶段 1：文档导入

**1.1 PDF 文档**
```
调用：pdf skill
功能：
- 文本提取
- 表格识别
- 图片 OCR（如需要）
- 目录结构保留
```

**1.2 Word 文档**
```
调用：docx skill
功能：
- 内容提取
- 格式保留
- 转 Markdown/纯文本
```

**1.3 Excel 表格**
```
调用：xlsx skill
功能：
- 数据读取
- 公式计算
- 转 CSV/Markdown 表格
- 数据可视化
```

**1.4 PPT 幻灯片**
```
调用：pptx skill
功能：
- 内容提取
- 转 Markdown 大纲
- 图片导出
```

**1.5 网页内容**
```
调用：baoyu-url-to-markdown
功能：
- 网页抓取
- 转 Markdown
- HTML 快照保存
```

### 阶段 2：内容提取

**2.1 文本预处理**
```
动作：
- 清理乱码
- 修正格式
- 统一编码
- 分段处理
```

**2.2 结构识别**
```
识别：
- 标题层级
- 段落边界
- 列表结构
- 表格内容
- 代码块
```

**2.3 元数据提取**
```
提取：
- 标题/副标题
- 作者信息
- 日期
- 来源
- 关键词
```

### 阶段 3：内容总结

**3.1 自动摘要**
```
动作：
- 提取核心观点
- 生成执行摘要
- 列出关键结论
- 标记重要数据
```

**3.2 要点提炼**
```
产出：
- 要点列表（Bullet Points）
- 关键数据表
- 决策树/流程图
- 行动项清单
```

**3.3 关系梳理**
```
调用：baoyu-diagram
- 概念关系图
- 流程图
- 架构图
```

### 阶段 4：格式化

**4.1 Markdown 格式化**
```
调用：baoyu-format-markdown
- YAML frontmatter
- 标题层级
- 列表格式
- 代码块
- 表格对齐
```

**4.2 内容转换**
```
可选转换：
- Markdown → HTML（baoyu-markdown-to-html）
- Markdown → Word（docx skill）
- Markdown → PDF（pdf skill）
```

### 阶段 5：知识组织

**5.1 分类体系**
```
组织方式：
- 按主题分类
- 按项目分类
- 按时间分类
- 按重要性分类
```

**5.2 标签系统**
```
标签类型：
- 主题标签
- 类型标签（文档/代码/数据）
- 状态标签（草稿/审核/发布）
- 优先级标签
```

**5.3 索引构建**
```
索引：
- 关键词索引
- 时间线索引
- 关联文档索引
- 人物/组织索引
```

### 阶段 6：检索与利用

**6.1 全文检索**
```
功能：
- 关键词搜索
- 模糊匹配
- 高亮显示
- 相关性排序
```

**6.2 知识输出**
```
输出形式：
- 研究报告
- 学习总结
- 培训材料
- 决策参考
```

**6.3 知识分享**
```
分享渠道：
- 内部 Wiki
- 团队文档
- 博客文章
- 社交媒体
```

## 快捷命令模式

```bash
# 完整流程
/knowledge-manage-workflow <文件/文件夹>

# 仅提取
/knowledge-manage-workflow <PDF> --stage extract

# 仅总结
/knowledge-manage-workflow <文档> --stage summarize

# 仅格式化
/knowledge-manage-workflow <内容> --stage format

# 批量处理
/knowledge-manage-workflow <文件夹> --batch

# 指定输出格式
/knowledge-manage-workflow <文件> --output html
/knowledge-manage-workflow <文件> --output docx
/knowledge-manage-workflow <文件> --output pdf

# 构建知识库
/knowledge-manage-workflow <文件夹> --build-kb

# 搜索
/knowledge-manage-workflow --search "关键词"
```

## 知识库目录结构

```
knowledge-base/
├── inbox/                    # 待处理文档
│   └── YYYY-MM-DD-<name>.pdf
├── processed/                # 已处理文档
│   ├── markdown/             # Markdown 版本
│   ├── summaries/            # 摘要
│   └── original/             # 原始文件
├── topics/                   # 按主题分类
│   ├── topic-a/
│   │   ├── index.md          # 主题索引
│   │   ├── docs/             # 相关文档
│   │   └── notes/            # 相关笔记
│   └── topic-b/
├── projects/                 # 按项目分类
│   └── project-x/
├── archive/                  # 归档
│   └── by-year/
└── index/
    ├── keywords.md           # 关键词索引
    ├── timeline.md           # 时间线索引
    └── related.md            # 关联索引
```

## 使用示例

### 示例 1：PDF 论文整理

用户："把这些论文 PDF 整理成知识库"

工作流：
1. pdf skill：提取每篇论文的文本
2. baoyu-format-markdown：格式化为 Markdown
3. 自动生成摘要（背景、方法、结论）
4. 按主题分类到 knowledge-base/topics/
5. 构建关键词索引
6. 生成知识图谱（概念关系）

### 示例 2：会议纪要整理

用户："整理这些会议记录"

工作流：
1. docx skill / baoyu-url-to-markdown：提取内容
2. 识别会议信息（时间、参会人、议题）
3. 提炼决策项和行动项
4. 格式化输出
5. 关联相关文档
6. 保存到 knowledge-base/projects/

### 示例 3：技术资料收集

用户："收集 React 相关的资料建成知识库"

工作流：
1. baoyu-url-to-markdown：抓取网页内容
2. baoyu-youtube-transcript：处理视频教程
3. 内容分类（基础/进阶/最佳实践）
4. 生成学习路径
5. 构建索引和导航
6. 输出为可浏览的文档站

## 依赖 Skills

| Skill | 阶段 | 用途 |
|-------|------|------|
| pdf | 1 | PDF 处理 |
| docx | 1 | Word 处理 |
| xlsx | 1 | Excel 处理 |
| pptx | 1 | PPT 处理 |
| baoyu-url-to-markdown | 1 | 网页抓取 |
| baoyu-youtube-transcript | 1 | 视频处理 |
| baoyu-format-markdown | 4 | Markdown 格式化 |
| baoyu-markdown-to-html | 4 | 转 HTML |
| baoyu-diagram | 3 | 生成图表 |
| baoyu-translate | 3 | 外语翻译 |

## 文档类型处理策略

### 技术文档
```
重点：
- 保留代码块
- 维护链接关系
- 提取 API 信息
- 生成术语表
```

### 学术论文
```
重点：
- 提取摘要和结论
- 识别研究方法
- 整理参考文献
- 标记关键数据
```

### 商业报告
```
重点：
- 执行摘要
- 关键指标
- 趋势分析
- 建议行动
```

### 会议记录
```
重点：
- 决策项
- 行动项（责任人 + 截止日期）
- 议题分类
- 跟进状态
```

### 学习笔记
```
重点：
- 核心概念
- 知识关联
- 疑问标记
- 复习计划
```

## 进阶配置

创建 `~/.baoyu-skills/knowledge-manage-workflow/EXTEND.md`：

```yaml
# 默认分类体系
taxonomy:
  primary_categories:
    - technical
    - business
    - meeting
    - research
  tags:
    auto_generate: true
    min_frequency: 2

# 摘要设置
summary:
  max_length: 300  # 字
  include_sections:
    - background
    - key_points
    - conclusions
    - action_items

# 格式化选项
format:
  heading_style: atx  # atx 或 setext
  list_style: dash  # dash, asterisk, plus
  code_block_fences: true

# 知识库设置
knowledge_base:
  root: knowledge-base
  auto_index: true
  generate_nav: true
  include_metadata: true
```

## 最佳实践

1. **及时处理**：收到文档尽快处理，避免堆积
2. **统一格式**：所有文档转为 Markdown 便于检索
3. **摘要必备**：每个文档都要有摘要
4. **标签适度**：不要过度标签化
5. **定期整理**：定期回顾和归档

## 注意事项

1. **版权意识**：注意文档的版权和使用权限
2. **数据隐私**：敏感信息要加密或脱敏
3. **版本管理**：重要文档保留版本历史
4. **备份策略**：知识库定期备份
5. **访问控制**：团队知识库设置访问权限

## 输出模板

### 文档摘要模板
```markdown
# {标题}

## 元数据
- 来源：{来源}
- 日期：{日期}
- 类型：{文档类型}
- 标签：{标签}

## 执行摘要
{200-300 字摘要}

## 核心要点
- 要点 1
- 要点 2
- 要点 3

## 关键数据
| 指标 | 数值 | 说明 |
|------|------|------|
| ... | ... | ... |

## 行动项
- [ ] 行动 1
- [ ] 行动 2

## 关联文档
- [[相关文档 1]]
- [[相关文档 2]]
```

### 主题索引模板
```markdown
# {主题名称}

## 概述
{主题简介}

## 文档列表
| 文档 | 日期 | 类型 | 摘要 |
|------|------|------|------|
| ... | ... | ... | ... |

## 核心概念
- 概念 1：解释
- 概念 2：解释

## 学习路径
1. 入门 → [[文档 A]]
2. 进阶 → [[文档 B]]
3. 精通 → [[文档 C]]

## 相关知识
- [[相关主题 1]]
- [[相关主题 2]]
```
