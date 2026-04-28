---
name: content-publish-workflow
description: 内容创作与发布工作流。当用户需要写文章、发博客、创作内容并发布到多个平台时自动触发。串联创意→写作→配图→格式化→多平台发布全流程。
---

# 内容创作与发布工作流

这是一个端到端的内容创作和多平台发布工作流，整合了创意生成、写作、配图、格式化和社交媒体发布等多个 skills。

## 触发场景

当用户提到以下需求时自动触发：
- "写篇文章"、"写博客"、"创作内容"
- "发布到公众号"、"发微博"、"发 Twitter"
- "做个小红书图文"、"生成封面图"
- "把这篇文章多平台发布"
- "给我的视频写脚本"

## 工作流程图

```
┌─────────────┐
│  1. 创意构思  │
│  头脑风暴   │
└──────┬──────┘
       ↓
┌─────────────┐
│  2. 内容创作  │
│  撰写文章   │
└──────┬──────┘
       ↓
┌─────────────┐
│  3. 视觉设计  │
│  封面/配图   │
└──────┬──────┘
       ↓
┌─────────────┐
│  4. 格式化   │
│  排版优化   │
└──────┬──────┘
       ↓
┌─────────────┐
│  5. 多平台   │
│  一键发布   │
└─────────────┘
```

## 完整工作流程

### 阶段 1：创意构思

**1.1 头脑风暴**
```
调用：brainstorming skill
- 明确内容主题
- 确定目标受众
- 设定内容调性
- 选择呈现形式
```

**1.2 大纲设计**
```
产出：
- 文章结构
- 核心观点
- 配图需求清单
```

### 阶段 2：内容创作

**2.1 撰写正文**
```
根据内容类型选择：

技术文章：
- 代码示例
- 架构图解
- 实践案例

观点文章：
- 论点阐述
- 论据支撑
- 总结升华

教程文章：
- 步骤分解
- 注意事项
- 常见问题
```

### 阶段 3：视觉设计

**3.1 封面图生成**
```
调用：baoyu-cover-image
5 维设计系统：
- Type: hero/conceptual/typography/metaphor/scene/minimal
- Palette: 11 种配色方案
- Rendering: 7 种渲染风格
- Text: 标题排版
- Mood: subtle/balanced/bold

自动生成 77 种组合
```

**3.2 信息图表**
```
调用：baoyu-infographic
21 种布局类型：
- pyramid：层级结构
- funnel：转化流程
- timeline：时间线
- comparison：对比表
- 等等...

17 种视觉风格可选
```

**3.3 流程图解**
```
调用：baoyu-diagram
- flowchart：流程图
- sequence：时序图
- structural：架构图
- 输出 SVG，支持暗色模式
```

**3.4 文章配图**
```
调用：baoyu-article-illustrator
- 自动分析文章结构
- 识别需要配图的位置
- Type × Style × Palette 三维设计
```

**3.5 小红书图文**
```
调用：baoyu-xhs-images
- 1-10 张卡片式图片
- Style × Layout 系统
- 适合知识卡片、清单体
```

### 阶段 4：格式化

**4.1 Markdown 格式化**
```
调用：baoyu-format-markdown
- 生成 YAML frontmatter
- 格式化标题层级
- 加粗关键点
- 整理列表和代码
- 输出：{filename}-formatted.md
```

**4.2 转 HTML（如需要）**
```
调用：baoyu-markdown-to-html
- 选择主题样式
- 代码高亮
- 底部引用自动生成
- WeChat 兼容样式
```

### 阶段 5：多平台发布

**5.1 微信公众号**
```
调用：baoyu-post-to-wechat
模式：
- 文章模式：完整 Markdown/HTML
- 贴图模式：多图 + 短文

发布方式：
- API（推荐）：快速
- Browser：无需配置

支持多账号管理
```

**5.2 微博**
```
调用：baoyu-post-to-weibo
- 普通微博：文字 + 图片/视频
- 头条文章：长文 Markdown
- 最多 18 张图片
```

**5.3 Twitter/X**
```
调用：baoyu-post-to-x
- 普通推文：文字 + 图片
- X Articles：长文 Markdown
- 线程发布（多条连续）
```

**5.4 小红书**
```
调用：baoyu-xhs-images
- 生成卡片图片
- 准备文案
- 手动发布（平台限制）
```

## 快捷命令模式

```bash
# 完整流程
/content-publish-workflow "写一篇 AI 技术文章"

# 仅写作
/content-publish-workflow "写教程" --stage write

# 仅配图
/content-publish-workflow <文章> --stage design

# 仅发布
/content-publish-workflow <文章> --stage publish --platform wechat

# 指定平台组合
/content-publish-workflow <文章> --platform wechat,weibo,x

# 快速发布（用已有内容）
/content-publish-workflow --quick --platform x <文章内容>

# 仅生成封面
/content-publish-workflow --generate-cover <文章>
```

## 平台规格参考

| 平台 | 类型 | 图片 | 文字 | 最佳实践 |
|------|------|------|------|----------|
| 公众号 | 文章 | 不限 | 不限 | 深度内容 |
| 微博 | 短文 | ≤18 | ≤2000 | 热点 + 图片 |
| X/Twitter | 短文 | ≤4 | ≤280* | 线程长文 |
| 小红书 | 图文 | 1-10 | ≤1000 | 知识卡片 |

*X 平台文字限制因账号而异

## 输出产物

```
content/
├── drafts/
│   └── YYYY-MM-DD-<topic>.md       # 草稿
├── formatted/
│   └── YYYY-MM-DD-<topic>-formatted.md  # 格式化版本
├── images/
│   ├── covers/                      # 封面图
│   ├── infographics/                # 信息图
│   ├── diagrams/                    # 流程图
│   └── illustrations/               # 配图
├── html/
│   └── YYYY-MM-DD-<topic>.html      # HTML 版本
└── published/
    └── metadata.json                # 发布记录
```

## 使用示例

### 示例 1：技术博客

用户："写一篇关于 Vibe Coding 的技术博客，发到公众号和 Twitter"

工作流：
1. brainstorming：确定文章角度和受众
2. 撰写正文：技术说明 + 代码示例
3. baoyu-cover-image：生成封面
4. baoyu-diagram：生成 Vibe Coding 流程图
5. baoyu-format-markdown：格式化
6. baoyu-markdown-to-html：转 HTML（公众号用）
7. baoyu-post-to-wechat：发布公众号
8. baoyu-post-to-x：发布 Twitter 线程

### 示例 2：小红书运营

用户："把这个知识点做成小红书图文"

工作流：
1. 分析内容结构
2. baoyu-xhs-images：生成 5-7 张卡片
3. 准备文案（含 emoji 和标签）
4. 输出到 content/published/xiaohongshu/

### 示例 3：多平台分发

用户："把这篇文章发到所有平台"

工作流：
1. 读取文章
2. 检查/生成封面图
3. 根据各平台规格调整格式
4. 依次发布到：
   - 微信公众号（文章模式）
   - 微博（头条文章）
   - X（Articles）
5. 记录发布结果

## 依赖 Skills

| Skill | 阶段 | 用途 |
|-------|------|------|
| brainstorming | 1 | 创意构思 |
| baoyu-cover-image | 3 | 封面生成 |
| baoyu-infographic | 3 | 信息图表 |
| baoyu-diagram | 3 | 流程图 |
| baoyu-article-illustrator | 3 | 文章配图 |
| baoyu-xhs-images | 3 | 小红书卡片 |
| baoyu-format-markdown | 4 | 格式化 |
| baoyu-markdown-to-html | 4 | 转 HTML |
| baoyu-post-to-wechat | 5 | 公众号发布 |
| baoyu-post-to-weibo | 5 | 微博发布 |
| baoyu-post-to-x | 5 | Twitter 发布 |

## 内容类型预设

```bash
# 技术教程
/content-publish-workflow --type tutorial "主题"

# 观点文章
/content-publish-workflow --type opinion "主题"

# 产品评测
/content-publish-workflow --type review "产品名"

# 新闻资讯
/content-publish-workflow --type news "事件"

# 清单体
/content-publish-workflow --type list "主题"

# 深度分析
/content-publish-workflow --type deep-dive "主题"
```

## 风格预设

```bash
# 专业正式
/content-publish-workflow --style formal

# 轻松幽默
/content-publish-workflow --style casual

# 故事化
/content-publish-workflow --style storytelling

# 学术严谨
/content-publish-workflow --style academic

# 销售导向
/content-publish-workflow --style persuasive
```

## 进阶配置

创建 `~/.baoyu-skills/content-publish-workflow/EXTEND.md`：

```yaml
# 默认发布平台
default_platforms:
  - wechat
  - weibo

# 封面图风格
default_cover:
  type: conceptual
  palette: cool
  rendering: digital
  mood: balanced

# 发布设置
publish:
  wechat:
    method: api  # 或 browser
    theme: grace
    color: blue
  weibo:
    article_type: headline
  x:
    thread_auto: true  # 自动分线程

# 内容模板
templates:
  tutorial: |
    # {title}
    ## 前言
    ## 背景
    ## 步骤
    ## 总结
  opinion: |
    # {title}
    ## 问题
    ## 分析
    ## 观点
    ## 建议
```

## 最佳实践

1. **封面先行**：先确定视觉风格，再写作
2. **一源多发**：一份内容，多平台适配
3. **平台差异化**：根据平台调整语气和格式
4. **图片压缩**：大图先压缩再发布
5. **发布时间**：考虑各平台流量高峰时段

## 注意事项

1. **API 配置**：微信公众号发布需提前配置 API 密钥
2. **登录会话**：微博/X 首次发布需手动登录
3. **图片限制**：注意各平台图片大小和数量限制
4. **内容审核**：发布前确认内容符合平台规范
5. **频率限制**：避免短时间内大量发布触发限流
