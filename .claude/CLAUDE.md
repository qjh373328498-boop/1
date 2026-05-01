# Claude 配置 — 工作流集成（极简版）

> **方案 D v3.0：三级触发 + 动态加载**  
> **常驻 Token**：~1,200（12 高频技能 + 精简索引）  
> **按需加载**：78 技能触发词（延迟加载）  
> **最后更新**：2026-05-01  
> **版本**：v3.0（Token 极限优化）

---

## Token 优化机制（新版）

### 1. 三级触发架构（节省 ~8,000 tokens）

| 级别 | 位置 | 技能数 | Token | 加载时机 |
|------|------|--------|-------|----------|
| **L1 - 高频核心** | `CLAUDE.md` | 12 | ~600 | **常驻** |
| **L2 - 扩展触发词** | `skills-trigger-map.md` | 78 | ~2,500 | 意图明确时 |
| **L3 - 技能文档** | `skills/*/SKILL.md` | 90 | ~50,000 | 触发后 |

### 2. 动态加载策略

```
触发条件：
1. 用户输入 → 匹配 L1 核心词（12 技能）
2. 精确匹配 (≥80%) → 直接触发 skill
3. 置信度 (50-79%) → 加载 L2 扩展词表
4. 模糊意图 (<50%) → 询问确认
5. 否定词 → 不触发
```

### 3. 技能索引精简

`skills-index.md` 仅保留：
- 技能名 → 文件路径映射
- 不含触发词/关键词
- 常驻：~400 tokens

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

## 核心触发词（L1 - 高频常驻）

| 触发词 | 技能 | 频率 |
|--------|------|------|
| 复习/备考/考试 | `exam-prep` | 🔥 |
| 比赛/竞赛/备赛 | `competition-prep` | 🔥 |
| 写论文/写报告 | `research-paper-isolated` | 🔥 |
| 分析数据/Excel | `data-analysis` | 🔥 |
| 周计划/日程 | `weekly-planning` | ⭐ |
| 整理资料/文件 | `knowledge-manage` | ⭐ |
| 剪辑视频/剪视频 | `video-use` | 🔥 |
| 生成视频/做视频 | `hyperframes` | 🔥 |
| 转语音/TTS/配音 | `tts-voice` | 🔥 |
| BGM/配乐/音乐 | `music-gen` | 🔥 |
| YouTube 下载/字幕 | `baoyu-youtube-transcript` | 🔥 |
| 网页提取/转 Markdown | `baoyu-url-to-markdown` | 🔥 |

**常驻总计**：12 技能，~50 触发词，~600 tokens

### 触发规则

**匹配流程**：
```
1. 用户输入 → 匹配 L1 核心词（12 技能）
2. 精确匹配 (≥80%) → 直接触发 skill
3. 置信度 (50-79%) → 加载 L2 扩展词表
4. 模糊意图 (<50%) → 询问确认
5. 否定词 (不想/不要/不需要/别) → 不触发
```

**L2 扩展触发词**：78 技能，~500 词，存储于 `skills-trigger-map.md`  
**加载时机**：置信度 50-79% 时按需加载

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
| `CLAUDE.md` | L1 核心配置 (12 技能) | 常驻 | ~600 | v3.0 |
| `skills-index.md` | 技能路径索引 (90 技能) | 常驻 | ~400 | v3.0 |
| `skills-trigger-map.md` | L2 扩展触发词 (78 技能) | 按需 | ~2,500 | v3.0 |
| `video-production-pipeline.card` | 视频工作流 (27+ 技能) | 按需 | - | v6.0 |
| `content-publish-workflow/SKILL.md` | 内容发布流 (15 技能) | 按需 | - | v2.0 |
| `trigger-test.md` | 触发词测试工具 | 按需 | - | v1.0 |
| **常驻总计** | - | - | **~1,000** | - |

---

## 工作流总览

### 视频制作工作流（27+ 技能）
```
资料收集 → 创意 → 脚本 → 配音 → 分镜 → 素材 → 视频 → 字幕 → **BGM/音乐** → 多语言 → 发布
```
**触发词**：做个视频/生成视频/YouTube 下载/多语言视频/漫画分镜/高质量图片/背景音乐

### 内容发布工作流（15 技能）
```
资料收集 → 创意 → 写作 → 视觉 → PPT → 格式化 → 多平台发布
```
**触发词**：写文章/发博客/PPT/公众号/微博/Twitter

---

## 副作用缓解

### 1. 核心词遗漏

```
置信度 50-79% → 自动加载 skills-trigger-map.md
```

### 2. 映射表不同步

```
修改触发词时：
1. 同步更新 CLAUDE.md + skills-trigger-map.md
2. 更新两个文件的版本号
3. 运行 ./skills.sh check-sync
```

详见：`trigger-sync-checklist.md`

### 3. 触发失败调试

```
调试命令：
- ./skills.sh test "<输入>" - 单个测试
- ./skills.sh test-batch - 批量测试
- ./skills.sh check-sync - 同步检查
- export SKILL_DEBUG=1 - 调试日志
```

详见：`trigger-test.md`

---

## 相关文档

- **整合报告**：`SKILLS_INTEGRATION_REPORT.md`（v6.0）
- **MiniMax 音乐**：`MINIMAX_MUSIC_INTEGRATION.md`
- **音频调研**：`AUDIO_SKILL_RESEARCH.md`
- **方案 D 文档**：`.claude/docs/方案 D_*.md`
- **视频工作流**：`.claude/workflows/video-production-pipeline.card`
- **内容发布流**：`.claude/skills/content-publish-workflow/SKILL.md`

---
