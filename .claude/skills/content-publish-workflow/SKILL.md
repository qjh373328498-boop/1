---
name: content-publish-workflow
description: 内容创作与发布工作流（23 技能整合版）。当用户需要写文章、发博客、创作内容并发布到多个平台时自动触发。串联资料收集→创意→写作→配图→PPT→格式化→多平台发布全流程。
version: v2.0
---

# 内容创作与发布工作流（23 技能整合版）

这是一个端到端的内容创作和多平台发布工作流，整合了**资料收集**、**创意生成**、**写作**、**配图**、**PPT 生成**、**格式化**和**社交媒体发布**等多个 skills。

## 触发场景

当用户提到以下需求时自动触发：
- "写篇文章"、"写博客"、"创作内容"
- "发布到公众号"、"发微博"、"发 Twitter"
- "做个小红书图文"、"生成封面图"
- "把这篇文章多平台发布"
- "给我的视频写脚本"
- "做个 PPT"、"生成幻灯片"
- "下载几个 YouTube 视频学习"

## 技能矩阵

| 阶段 | 技能 | 工具 | 输出 | 批次 |
|------|------|------|------|------|
| **0. 资料收集** | YouTube 下载 | baoyu-youtube-transcript | 参考视频 + 文稿 | 第 1 批 |
| | 网页提取 | baoyu-url-to-markdown | 参考资料.md | 第 1 批 |
| **1. 创意** | 头脑风暴 | brainstorming | 创意点子.md | 第 3 批 |
| **2. 写作** | 内容创作 | Claude | article.md | - |
| **3. 视觉** | 封面图 | baoyu-cover-image | cover.png | - |
| | 配图 | baoyu-article-illustrator | illustration_*.png | 第 3 批 |
| | 信息图 | baoyu-infographic | infographic.png | - |
| | 卡片 | baoyu-image-cards | card_*.png | 第 3 批 |
| | 小红书图 | baoyu-xhs-images | xhs_*.png | - |
| **4. PPT** | 幻灯片 | baoyu-slide-deck | presentation.pptx | 第 2 批 |
| **5. 格式** | Markdown 优化 | baoyu-format-markdown | formatted.md | 第 1 批 |
| | 转 HTML | baoyu-markdown-to-html | article.html | 第 2 批 |
| | 图片压缩 | baoyu-compress-image | compressed_*.png | 第 2 批 |
| **6. 发布** | 公众号 | baoyu-post-to-wechat | 微信推文 | 第 2 批 |
| | 微博 | baoyu-post-to-weibo | 微博推文 | 第 2 批 |
| | Twitter | baoyu-post-to-x | X 推文 | 第 2 批 |

---

## 工作流程图

```
┌─────────────┐
│  0. 资料收集  │ ← 第 1 批新增
│ YouTube/网页 │
└──────┬──────┘
       ↓
┌─────────────┐
│  1. 创意构思  │ ← 第 3 批新增
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
│  4. PPT 生成   │ ← 第 2 批新增
│  幻灯片     │
└──────┬──────┘
       ↓
┌─────────────┐
│  5. 格式化   │
│  排版优化   │
└──────┬──────┘
       ↓
┌─────────────┐
│  6. 多平台   │
│  一键发布   │
└─────────────┘
```

---

## 完整工作流程

### 阶段 0：资料收集（新增 - 第 1 批）

#### 0.1 YouTube 视频下载
```bash
# 下载参考视频并提取字幕
baoyu-youtube-transcript \
  --url "https://youtube.com/watch?v=xxx" \
  --output-dir references/ \
  --extract-transcript

# 输出：
# - references/video.mp4
# - references/transcript.md
# - references/subtitles.srt
```

**用途**：
- 学习优秀内容结构
- 提取参考文稿
- 竞品分析

#### 0.2 网页内容提取
```bash
# 提取网页为 Markdown
baoyu-url-to-markdown \
  --url "https://example.com/article" \
  --output references/article.md

# 批量提取
baoyu-url-to-markdown \
  --urls references/urls.txt \
  --output-dir references/
```

**用途**：
- 收集参考资料
- 整理数据素材
- 引用来源

---

### 阶段 1：创意构思（新增 - 第 3 批）

#### 1.1 头脑风暴
```bash
# 调用 brainstorming skill
# 输出：ideas.md

头脑风暴维度：
- 内容主题
- 目标受众
- 内容调性（专业/轻松/幽默）
- 呈现形式（文章/图文/视频）
- 差异化亮点
- 发布平台
```

#### 1.2 大纲设计
```bash
# 基于创意生成大纲
# 输出：outline.md

大纲结构：
- 标题（3-5 个备选）
- 引言（吸引注意）
- 核心观点（3-5 个）
- 论据/案例
- 总结升华
- 行动号召
```

---

### 阶段 2：内容创作

#### 2.1 撰写正文
```bash
# 根据内容类型选择

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

故事文章：
- 起承转合
- 情感共鸣
- 价值传递
```

---

### 阶段 3：视觉设计

#### 3.1 封面图生成
```bash
# 调用 baoyu-cover-image
baoyu-cover-image \
  --title "文章标题" \
  --subtitle "文章副标题" \
  --style "minimal" \
  --image cover.png

5 维设计系统：
- Type: hero/conceptual/typography/metaphor/scene/minimal
- Palette: 11 种配色方案
- Rendering: 7 种渲染风格
- Text: 标题排版方式
- Emotion: 情感表达
```

#### 3.2 配图生成（第 3 批）
```bash
# 根据文章内容自动配图
baoyu-article-illustrator \
  --text "文章段落" \
  --style "illustration" \
  --image illustration_01.png

# 为每个核心观点配图
for section in article.sections:
  baoyu-article-illustrator \
    --text "{section.content}" \
    --image "illustration_{section.id}.png"
```

#### 3.3 信息图生成
```bash
# 数据可视化
baoyu-infographic \
  --title "数据对比" \
  --data "A:40%, B:30%, C:20%, D:10%" \
  --style "pie_chart" \
  --image infographic.png
```

#### 3.4 信息卡片（第 3 批）
```bash
# 生成金句卡片/分享卡片
baoyu-image-cards \
  --text "核心观点/金句" \
  --style "minimal" \
  --image quote_card.png

# 多卡片批量生成
baoyu-image-cards \
  --texts key_points.txt \
  --style "professional" \
  --output-dir cards/
```

#### 3.5 小红书配图
```bash
# 生成小红书风格配图
baoyu-xhs-images \
  --title "笔记标题" \
  --style "cute" \
  --ratio "3:4" \
  --image xhs_cover.png
```

---

### 阶段 4: PPT 生成（新增 - 第 2 批）

#### 4.1 自动生成幻灯片
```bash
# 基于文章生成 PPT
baoyu-slide-deck \
  --input article.md \
  --output presentation.pptx \
  --theme "professional" \
  --slides 10

# 输出结构：
# - 封面页（标题 + 副标题）
# - 目录页（大纲）
# - 内容页（每页一个核心观点）
# - 数据页（图表/信息图）
# - 总结页
# - 结束页（Q&A/联系方式）
```

#### 4.2 PPT 定制
```bash
# 指定每页内容
baoyu-slide-deck \
  --slides-config slides.json \
  --output presentation.pptx

# slides.json 结构：
{
  "slides": [
    {"type": "title", "title": "标题", "subtitle": "副标题"},
    {"type": "bullet", "title": "要点", "bullets": ["点 1", "点 2", "点 3"]},
    {"type": "image", "title": "图示", "image": "illustration_01.png"},
    {"type": "quote", "text": "金句内容", "author": "作者"}
  ]
}
```

---

### 阶段 5：格式化与优化

#### 5.1 Markdown 格式化（第 1 批）
```bash
# 格式化文章
baoyu-format-markdown \
  --input article_raw.md \
  --style "github" \
  --output article.md

# 格式化选项：
# - github: GitHub 风格
# - medium: Medium 风格
# - jekyll: Jekyll 博客
# - hugo: Hugo 博客
# - wordpress: WordPress
```

#### 5.2 转 HTML（第 2 批）
```bash
# Markdown 转 HTML
baoyu-markdown-to-html \
  --input article.md \
  --output article.html \
  --template "blog" \
  --highlight true

# 输出:
# - 完整 HTML 页面
# - 内联 CSS 样式
# - 代码高亮
# - 响应式设计
```

#### 5.3 图片压缩（第 2 批）
```bash
# 压缩封面图和配图
baoyu-compress-image \
  --input cover.png \
  --quality 85 \
  --format webp \
  --output cover_compressed.webp

# 批量压缩
find images/ -name "*.png" | while read img; do
  baoyu-compress-image \
    --input "$img" \
    --quality 80 \
    --format webp \
    --output "compressed/$(basename "$img" .png).webp"
done
```

---

### 阶段 6：多平台发布（第 2 批）

#### 6.1 微信公众号
```bash
# 发布到微信公众号
baoyu-post-to-wechat \
  --title "文章标题" \
  --content article.md \
  --images cover_compressed.webp \
  --tags "标签 1,标签 2" \
  --auto-typeset true

# 发布后返回：
# - 公众号文章链接
# - 阅读量/点赞数追踪
```

#### 6.2 微博
```bash
# 发布到微博
baoyu-post-to-weibo \
  --text "微博文案 #话题 1# #话题 2#" \
  --images cover.webp,illustration_01.webp \
  --at "@合作账号" \
  --location "北京"

# 九宫格发布：
baoyu-post-to-weibo \
  --text "长文内容..." \
  --images img{1..9}.webp
```

#### 6.3 Twitter/X
```bash
# 发布到 Twitter/X
baoyu-post-to-x \
  --text "Tweet text #hashtag1 #hashtag2" \
  --media cover.webp \
  --thread true

# 推文串发布：
baoyu-post-to-x \
  --thread-file thread.txt \
  --media-dir images/
```

#### 6.4 一键多平台发布
```bash
# 一次性发布到所有平台
./publish_all.sh \
  --content article.md \
  --images compressed/ \
  --platforms wechat,weibo,x \
  --schedule "2026-05-02 10:00:00"
```

---

## 自动化脚本

### publish_content.sh（总控脚本）
```bash
#!/bin/bash

# 内容创作与发布总控脚本
# 用法：./publish_content.sh <主题> <平台> <定时>

THEME="$1"        # 如："AI 趋势分析"
PLATFORMS="$2"    # 如："wechat,weibo,x"
SCHEDULE="$3"     # 如："2026-05-02 10:00:00"

echo "=== 开始内容创作与发布 ==="
echo "主题：$THEME"
echo "平台：$PLATFORMS"
echo "定时：$SCHEDULE"

# 0. 收集资料
echo "[0/8] 收集资料..."
./collect_materials.sh "$THEME"

# 1. 头脑风暴
echo "[1/8] 头脑风暴..."
./brainstorm.sh "$THEME"

# 2. 撰写文章
echo "[2/8] 撰写文章..."
./write_article.sh outline.md

# 3. 生成视觉素材
echo "[3/8] 生成封面/配图..."
./gen_visuals.sh article.md

# 4. 生成 PPT
echo "[4/8] 生成幻灯片..."
./gen_ppt.sh article.md

# 5. 格式化优化
echo "[5/8] 格式化..."
./format.sh article_raw.md

# 6. 压缩图片
echo "[6/8] 压缩图片..."
./compress_images.sh images/

# 7. 转 HTML
echo "[7/8] 转 HTML..."
./to_html.sh article.md

# 8. 多平台发布
echo "[8/8] 发布到 $PLATFORMS..."
./publish.sh article.md "$PLATFORMS"

echo "✅ 内容创作与发布完成！"
```

---

## 质量检查清单

### 内容质量
- [ ] 标题吸引人（3 个备选）
- [ ] 结构清晰（有目录）
- [ ] 论据充分（有数据/案例）
- [ ] 无错别字
- [ ] 引用规范

### 视觉质量
- [ ] 封面图精美
- [ ] 配图与内容相关
- [ ] 信息图清晰
- [ ] 卡片设计美观
- [ ] 图片已压缩优化

### PPT 质量
- [ ] 幻灯片结构完整
- [ ] 每页信息量适中
- [ ] 设计风格统一
- [ ] 动画效果适度
- [ ] 字体大小可读

### 发布质量
- [ ] 多平台格式适配
- [ ] 话题标签正确
- [ ] 发布时间优化
- [ ] 互动回复及时
- [ ] 数据追踪完整

---

## 平台适配规则

| 平台 | 标题长度 | 正文长度 | 图片数 | 最佳时间 |
|------|----------|----------|--------|----------|
| 公众号 | <30 字 | 2000-5000 字 | 3-5 张 | 8:00/12:00/20:00 |
| 微博 | <20 字 | <140 字 | 1-9 张 | 9:00/12:00/18:00 |
| Twitter | <60 字符 | <280 字符 | 1-4 张 | 8:00/13:00/17:00 |
| 小红书 | <20 字 | 500-1000 字 | 3-6 张 | 10:00/15:00/21:00 |
| 知乎 | <30 字 | 1000-5000 字 | 3-8 张 | 9:00/14:00/20:00 |

---

## 相关技能

### 核心技能
- `brainstorming` - 创意生成
- `content-publish-workflow` - 本工作流
- `baoyu-cover-image` - 封面图
- `baoyu-slide-deck` - PPT 生成

### 图片技能
- `baoyu-imagine` - 图片生成（含原 baoyu-image-gen）
- `baoyu-article-illustrator` - 配图
- `baoyu-infographic` - 信息图
- `baoyu-image-cards` - 卡片
- `baoyu-xhs-images` - 小红书图
- `baoyu-compress-image` - 压缩

### 格式技能
- `baoyu-format-markdown` - Markdown 格式化
- `baoyu-markdown-to-html` - 转 HTML
- `baoyu-translate` - 翻译
- `baoyu-url-to-markdown` - 网页提取

### 发布技能
- `baoyu-post-to-wechat` - 微信公众号
- `baoyu-post-to-weibo` - 微博
- `baoyu-post-to-x` - Twitter/X

---

## 版本历史

| 版本 | 日期 | 变更内容 |
|------|------|----------|
| v1.0 | 2026-04-30 | 初始版本 |
| v2.0 | 2026-05-01 | 23 技能完整整合 |
| | - 第 1 批：资料收集 + 格式优化 | 5 技能 |
| | - 第 2 批：PPT+ 发布 | 5 技能 |
| | - 第 3 批：创意 + 配图 | 4 技能 |

---

## 性能指标

| 指标 | v1.0 | v2.0 | 提升 |
|------|------|------|------|
| 技能数 | 8 | 15 | +88% |
| 自动化程度 | 50% | 90%+ | +40% |
| 支持平台 | 3 | 5 | +2 平台 |
| PPT 生成 | ❌ | ✅ | +新功能 |
| 多语言 | ❌ | ✅ | +新功能 |
| 定时发布 | ❌ | ✅ | +新功能 |

---
