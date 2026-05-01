# Claude 配置 — 工作流集成（精简版）

> 方案 D：按需加载技能  
> 常驻 Token：~1,500（30 技能核心触发词 + 索引）  
> 最后更新：2026-05-01  
> 版本：v1.4（25 技能整合后）  
> 触发词外部化：核心词常驻，完整表按需加载

---

## 核心规则

### 1. Git 同步
```bash
git add . && git commit -m "auto: <描述>" && git push
```

### 2. 文件整理
- 删除重复文件（带 (1)(2) 版本号）
- 分类到：作业/比赛/知识库
- 清理空目录

### 3. Token 策略
- 单次读取 ≤200 行
- 大文件分段读取
- 按需加载 skills

---

## 工作流触发

**机制**：检测关键词 → 读取对应 skill → 执行

### 核心触发词（Level 1 - 直接触发）

| 触发词 | 技能 | 批次 |
|--------|------|------|
| 复习/备考/考试/背题/划重点 | `exam-prep` | 核心 |
| 比赛/竞赛/备赛/学创杯/挑战杯 | `competition-prep` | 核心 |
| 写论文/写报告/论文写作/文献综述 | `research-paper-isolated` | 核心 |
| 参考知识库/用知识库/结合之前资料 | `research-paper-with-kb` | 核心 |
| 查文献/找论文/引用格式/参考文献 | `literature-search` | 核心 |
| 分析数据/处理 Excel/财务分析/图表 | `data-analysis` | 核心 |
| 周计划/日程安排/时间管理/周回顾 | `weekly-planning` | 核心 |
| 整理资料/整理文件/批量处理/索引 | `knowledge-manage` | 核心 |
| 需求分析/功能设计/写需求文档 | `feature-design` | 核心 |
| 剪辑视频/剪视频/去废话/加字幕 | `video-use` | 核心 |
| 生成视频/做视频/动画视频/从零开始 | `hyperframes` | 核心 |
| 转语音/TTS/配音/语音合成/朗读 | `tts-voice` | 核心 |
| 背景音乐/BGM/配乐/生成音乐 | `music-gen` | 核心 |
| Git/同步/commit/push | `git-sync` | 核心 |
| YouTube 下载/提取字幕/参考视频 | `baoyu-youtube-transcript` | 第 1 批 |
| 网页提取/下载网页/转 Markdown | `baoyu-url-to-markdown` | 第 1 批 |
| 流程图/示意图/图表 | `baoyu-diagram` | 第 1 批 |
| 翻译/多语言/字幕翻译 | `baoyu-translate` | 第 1 批 |
| 格式化/排版/Markdown 优化 | `baoyu-format-markdown` | 第 1 批 |
| PPT/幻灯片/演示文稿 | `baoyu-slide-deck` | 第 2 批 |
| 转 HTML/生成网页 | `baoyu-markdown-to-html` | 第 2 批 |
| 压缩图片/优化图片/转 WebP | `baoyu-compress-image` | 第 2 批 |
| 公众号/微信发布 | `baoyu-post-to-wechat` | 第 2 批 |
| 微博发布 | `baoyu-post-to-weibo` | 第 2 批 |
| Twitter/X 发布 | `baoyu-post-to-x` | 第 2 批 |
| 配图/插图/旁白配图 | `baoyu-article-illustrator` | 第 3 批 |
| 信息卡片/金句卡片 | `baoyu-image-cards` | 第 3 批 |
| 头脑风暴/创意/点子 | `brainstorming` | 第 3 批 |
| 高质量图片/精细图片/AI 绘画 | `baoyu-imagine` | 整合 |
| 漫画分镜/故事性视频/教育漫画 | `baoyu-comic` | 整合 |

### 触发规则

**匹配流程**：
```
1. 用户输入 → 匹配 CLAUDE.md 核心触发词
2. 精确匹配 (≥80%) → 直接触发 skill
3. 模糊匹配 (60-79%) → 自动加载 skills-trigger-map.md 精确匹配
4. 低置信度 (<40%) → 询问确认
5. 否定词 (不想/不要/不需要/别) → 不触发
```

**核心触发词**：30 技能，~140 词，常驻内存  
**完整映射表**：按需加载（模糊匹配/触发失败/用户请求时）  
**工作流**：视频制作 (25 技能) / 内容发布 (15 技能)

---

## 快捷命令

```bash
# 视频制作
./skills.sh video <主题> <时长>      # 一体化视频生成
./skills.sh youtube <URL>           # YouTube 下载+ 字幕
./skills.sh translate <文件>         # 多语言翻译

# 内容发布
./skills.sh publish <文章> <平台>    # 多平台发布
./skills.sh ppt <文章>              # 生成 PPT
./skills.sh compress <图片>          # 图片压缩

# 论文写作
./skills.sh paper <PDF/URL>         # 隔离模式
./skills.sh paper-kb <主题>         # 知识库模式

# 考试比赛
./skills.sh exam <科目> [日期]      # 考试复习
./skills.sh competition <比赛>      # 比赛备赛

# 数据分析
./skills.sh data <文件> [类型]      # 数据分析

# 日常管理
./skills.sh plan [日期]             # 周计划
./skills.sh kb <文件夹>             # 知识管理

# 工具
./skills.sh sync                    # Git 同步
./skills.sh compress <文件>         # 文档压缩
./skills.sh test "<输入>"           # 触发词测试
```

---

## 自动化规则

### 文件操作后自动同步 Git
每次创建/修改文件后：
```bash
git add . && git commit && git push
```

### 大文件自动压缩提醒
.md 文件 >500 行 → 提醒使用 `caveman-compress`

---

## 配置文件

| 文件 | 用途 | 加载时机 | Token | 版本 |
|------|------|----------|-------|------|
| `CLAUDE.md` | 核心配置 +28 技能触发词 | 常驻 | ~1,500 | v1.3 |
| `skills-index.md` | 技能索引表 (90 技能) | 常驻 | ~600 | v1.2 |
| `skills-trigger-map.md` | 完整触发词映射 | 按需 | ~3,000 | v1.4 |
| `video-production-pipeline.card` | 视频工作流 (25 技能) | 按需 | - | v4.0 |
| `content-publish-workflow/SKILL.md` | 内容发布流 (15 技能) | 按需 | - | v2.0 |
| `trigger-test.md` | 触发词测试工具 | 按需 | - | v1.0 |
| `trigger-sync-checklist.md` | 同步检查清单 | 按需 | - | v1.0 |
| **常驻总计** | - | - | **~2,100** | - |

---

## 工作流总览

### 视频制作工作流（25 技能）
```
资料收集 → 创意 → 脚本 → 配音 → 分镜 → 素材 → 视频 → 字幕 → BGM → 多语言 → 发布
```
**触发词**：做个视频/生成视频/YouTube 下载/多语言视频/漫画分镜/高质量图片

### 内容发布工作流（15 技能）
```
资料收集 → 创意 → 写作 → 视觉 → PPT → 格式化 → 多平台发布
```
**触发词**：写文章/发博客/PPT/公众号/微博/Twitter

---

## 副作用缓解措施

### 1. 核心词遗漏 → 自动加载完整映射表

```
当核心触发词匹配但置信度<80% 时：
1. 自动加载 skills-trigger-map.md
2. 进行精确匹配
3. 匹配成功后触发 skill
```

### 2. 映射表不同步 → 强制同步检查

```
每次修改触发词时：
1. 必须同时更新 CLAUDE.md 和 skills-trigger-map.md
2. 必须更新两个文件的版本号
3. 必须运行 ./skills.sh check-sync
4. 必须测试新触发词
```

详见：`trigger-sync-checklist.md`

### 3. 触发失败难调试 → 测试工具 + 日志

```
调试命令：
- ./skills.sh test "<输入>" - 测试单个输入
- ./skills.sh test-batch test-cases.md - 批量测试
- ./skills.sh check-sync - 检查同步状态
- export SKILL_DEBUG=1 - 启用调试日志
```

详见：`trigger-test.md`

---

## 相关文档

- **整合报告**：`SKILLS_INTEGRATION_REPORT.md`（23 技能整合完整说明）
- **方案 D 文档**：`.claude/docs/方案 D_*.md`
- **视频工作流**：`.claude/workflows/video-production-pipeline.card`
- **内容发布流**：`.claude/skills/content-publish-workflow/SKILL.md`

---

**完整文档**：见 `/workspace/方案 D_*.md`
