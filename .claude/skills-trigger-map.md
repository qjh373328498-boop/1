# Skills 触发关键词映射（精简版）

> **版本**：v3.0  
> **最后更新**：2026-05-01  
> **说明**：L2 扩展触发词（77 技能），按需加载~2,500 tokens  
> **L1 核心**：12 技能见 `CLAUDE.md`

---

## 加载规则

```
加载时机：
1. 置信度 50-79% → 自动加载本文件
2. 用户请求 → 查看完整触发词列表
3. 同步检查 → ./skills.sh check-sync
```

---

## L2 扩展触发词（78 技能）

### exam-prep-workflow
```
- 帮我复习、我要备考、准备考试、背题、划重点
- 复习、备考、考试（+ 时间词如"下周"）
```

### competition-prep-workflow
```
- 准备比赛、参加比赛、备赛、写商业计划书、路演 PPT
- 学创杯、挑战杯、国创赛、互联网 +
```

### research-paper-workflow-isolated
```
- 帮我写论文、写研究报告、写文献综述、论文写作
- 你看看这个论文/报告
```

### research-paper-workflow-with-kb
```
- 参考知识库写论文、用知识库的资料、结合之前的资料
```

### literature-search-workflow
```
- 查找文献、找论文、生成参考文献、引用格式
```

### data-analysis-workflow
```
- 帮我分析、分析一下、分析数据、处理 Excel、财务分析
- financial analysis、analysis、制作图表、用 Python 分析
```

### weekly-planning-workflow
```
- 制定周计划、安排日程、时间管理、周回顾、周计划
```

### knowledge-manage-workflow
```
- 帮我整理这些资料、整理资料、整理文件、批量处理文档
```

### feature-design
```
- 需求分析、功能设计、写需求文档、设计一个功能
```

### video-use
```
- 剪辑视频、剪视频、自动剪辑、有原始素材、处理视频
- 去掉废话、加字幕、调色、精简视频、视频去水印
```

### hyperframes
```
- 生成视频、创建视频、制作视频、没有素材、从零开始
- 动画视频、图文视频、数据可视化视频、代码生成视频
```

### tts-voice
```
- 转语音、生成语音、文字转语音、TTS、语音合成、配音
- 朗读、有声书、旁白、男声/女声、配音员
```

### auto-subtitles
```
- 加字幕、生成字幕、字幕文件、SRT、ASS、VTT
- 语音转文字、听写、转录、视频字幕
```

### music-gen
```
- 背景音乐、BGM、配乐、生成音乐、创作音乐、作曲
- 免版权音乐、音效、背景音
```

---

## Baoyu 系列技能

### baoyu-translate
```
- 翻译、多语言、字幕翻译、English、日本語
```

### baoyu-format-markdown
```
- 格式化、排版、Markdown 优化、整理格式
```

### baoyu-markdown-to-html
```
- 转 HTML、生成网页、Markdown 转 HTML
```

### baoyu-url-to-markdown
```
- 网页提取、下载网页、转 Markdown、抓取内容
```

### baoyu-youtube-transcript
```
- YouTube 下载、提取字幕、参考视频、下载视频
```

### baoyu-diagram
```
- 流程图、示意图、图表、mermaid、draw.io
```

### baoyu-infographic
```
- 信息图、数据图表、长图
```

### baoyu-article-illustrator
```
- 配图、插图、旁白配图、文章配图
```

### baoyu-cover-image
```
- 封面图、头图、缩略图
```

### baoyu-imagine
```
- 高质量图片、精细生成、AI 绘画、精美图片
- （原 baoyu-image-gen 已合并到此技能）
```

### baoyu-comic
```
- 漫画分镜、故事性视频、教育漫画、多格漫画
```

### baoyu-slide-deck
```
- PPT、幻灯片、演示文稿、PowerPoint
```

### baoyu-post-to-wechat
```
- 公众号、微信发布、发微信
```

### baoyu-post-to-weibo
```
- 微博发布、发微博
```

### baoyu-post-to-x
```
- Twitter、X发布、发推特
```

### baoyu-compress-image
```
- 压缩图片、优化图片、转 WebP、减小体积
```

---

## 工具类技能

### git-sync
```
- git、同步、commit、push、提交代码
```

### brainstorming
```
- 头脑风暴、创意、点子、集思广益
```

### feature-implementer
```
- 实现功能、写代码、开发功能
```

### software-dev-workflow
```
- 软件开发、完整项目、从零开发
```

### debug-troubleshoot-workflow
```
- 调试、排查问题、修复 bug、报错
```

### frontend-design
```
- 前端设计、UI、页面设计
```

### deploy-website
```
- 部署网站、上线、预览
```

### skill-creator
```
- 创建 skill、编写 skill、自定义技能
```

### mcp-builder
```
- MCP、Model Context Protocol
```

### project-wiki
```
- 项目文档、生成 wiki、build docs
```

---

## 文档处理技能

### pdf
```
- PDF、pdf 文件、阅读 PDF
```

### docx
```
- Word、docx、doc 文件
```

### xlsx
```
- Excel、xlsx、xls、表格
```

### pptx
```
- PPT、pptx、演示文稿
```

---

## Caveman 系列

### caveman-commit
```
- caveman commit、简化提交消息
```

### caveman-compress
```
- caveman compress、压缩文档
```

### caveman-review
```
- caveman review、代码审查
```

---

## 文件类型推断

| 扩展名 | 推断 skill |
|--------|-----------|
| .xlsx/.xls | data-analysis |
| .pdf | research-paper/literature-search |
| .docx/.doc | knowledge-manage/feature-design |
| .ppt/.pptx | competition-prep/baoyu-slide-deck |

---

## 否定词列表（不触发）

```
不想、不要、不需要、别、没空、没时间、懒得
don't、do not、won't、no need、never
```

---

## 置信度阈值

```json
{
  "direct_trigger": 80,
  "confirm_trigger": 50,
  "ask_confirm": 30
}
```

| 置信度 | 决策 |
|--------|------|
| ≥80% | 直接触发 |
| 50-79% | 加载本文件 + 触发 |
| 30-49% | 询问确认 |
| <30% | 不触发 |

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-04-30 | 初始版本 |
| v2.0 | 2026-05-01 | 触发词外部化 |
| v3.0 | 2026-05-01 | 精简到~2,500 tokens |
