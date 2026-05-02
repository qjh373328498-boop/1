# MiniMax Music Skills 整合指南

> 版本：v1.0  
> 日期：2026-05-01  
> 状态：✅ 已完成调研

---

## 执行摘要

MiniMax AI 提供 3 个音乐相关 skills，可通过 `mmx-cli` 工具集成到现有工作流中。

### 可用技能

| 技能 | 用途 | 触发词 | GitHub |
|------|------|--------|--------|
| `minimax-music-gen` | 背景音乐/歌曲生成 | 生成音乐/背景音乐/歌曲创作 | [链接](https://github.com/MiniMax-AI/skills/tree/main/skills/minimax-music-gen) |
| `buddy-sings` | Claude 宠物配音 | 让宠物唱歌/buddy 唱歌 | [链接](https://github.com/MiniMax-AI/skills/tree/main/skills/buddy-sings) |
| `minimax-music-playlist` | 个性化歌单 | 生成歌单/推荐音乐 | [链接](https://github.com/MiniMax-AI/skills/tree/main/skills/minimax-music-playlist) |

---

## 安装步骤

### 1. 安装 mmx-cli

```bash
# 全局安装（推荐）
npm install -g mmx-cli --break-system-packages

# 验证安装
mmx --version
```

### 2. 配置 API 密钥

```bash
# 获取 API 密钥：https://platform.minimaxi.com/
mmx auth login --api-key your-api-key

# 验证登录
mmx quota show
```

### 3. 下载 Skills

```bash
# 方法 1: 克隆仓库
git clone https://github.com/MiniMax-AI/skills.git /workspace/.claude/skills/minimax-skills

# 方法 2: 手动下载单个 skill
mkdir -p /workspace/.claude/skills/minimax-music-gen
wget https://raw.githubusercontent.com/MiniMax-AI/skills/main/skills/minimax-music-gen/SKILL.md \
  -O /workspace/.claude/skills/minimax-music-gen/SKILL.md
```

---

## 整合到视频工作流

### 更新视频工作流 v6.0

在 `video-production-pipeline.card` 中添加：

**阶段 8：背景音乐生成（增强版）**

```markdown
### 阶段 8：背景音乐生成

#### 8.1 基础 BGM（现有）
```bash
# 使用现有 music-gen
python music_gen.py \
  --style "light corporate" \
  --duration 60 \
  --output bgm.mp3
```

#### 8.2 MiniMax BGM（新增）⭐
```bash
# 使用 minimax-music-gen 生成高质量 BGM
mmx music generate \
  --prompt "Upbeat corporate background music, inspiring, motivational" \
  --instrumental \
  --genre "corporate" --mood "uplifting" \
  --instruments "piano, strings, light drums" \
  --out bgm.mp3 \
  --quiet --non-interactive

# 带歌词的主题曲
mmx music generate \
  --prompt "Catchy jingle for product launch, energetic pop" \
  --lyrics-optimizer \
  --genre "pop" --vocals "energetic male vocal" \
  --out theme_song.mp3 \
  --quiet --non-interactive
```

#### 8.3 宠物配音（趣味功能）⭐
```bash
# 让 Claude 宠物为视频配音
buddy-sings \
  --theme "视频主题介绍" \
  --output pet_intro.mp3
```
```

---

## 更新 CLAUDE.md 触发词

在核心触发词表中添加：

```markdown
| 背景音乐/BGM/配乐/生成音乐 | `music-gen` | 核心 |
| **生成歌曲/MiniMax 音乐/宠物唱歌** | **`minimax-music-gen`/`buddy-sings`** | **新增** |
```

---

## 使用示例

### 示例 1：视频 BGM 生成

**用户输入**：
```
帮我生成一个轻松愉快的背景音乐用于产品介绍视频
```

**工作流**：
1. 检测意图：背景音乐生成
2. 选择技能：`minimax-music-gen`
3. 生成音乐：
```bash
mmx music generate \
  --prompt "Light cheerful background music for product demo, happy upbeat mood" \
  --instrumental \
  --genre "corporate" --mood "cheerful" \
  --instruments "piano, acoustic guitar, light percussion" \
  --out bgm_product_demo.mp3 \
  --quiet --non-interactive
```
4. 播放并确认

---

### 示例 2：宠物配音

**用户输入**：
```
让我的宠物唱一首关于今天工作的歌
```

**工作流**：
1. 读取宠物信息：`~/.claude.json` → `companion` 字段
2. 加载宠物声音配置：`~/.claude/skills/buddy-sings/voices/<name>.json`
3. 扫描今日工作内容（对话历史/记忆/Git 提交）
4. 生成个性化歌词
5. 调用音乐生成：
```bash
mmx music generate \
  --prompt "<pet vocal style> <theme song style>" \
  --lyrics "<pet perspective lyrics>" \
  --out pet_sings_work.mp3 \
  --quiet --non-interactive
```
6. 播放并收集反馈

---

## 依赖检查清单

在安装前验证：

- [ ] Node.js 已安装 (`node --version`)
- [ ] npm 已安装 (`npm --version`)
- [ ] 音频播放器（mpv/ffplay/afplay）
- [ ] MiniMax API 密钥（https://platform.minimaxi.com/）

---

## 配置文件

### ~/.mmx/credentials.json（自动创建）

```json
{
  "api_key": "your-api-key-here",
  "authenticated_at": "2026-05-01T12:00:00Z"
}
```

### ~/.claude/skills/minimax-music-gen/EXTEND.md（可选）

```markdown
# 个性化配置
default_genre: corporate
default_mood: uplifting
default_vocals: androgynous
default_instruments: piano, strings
output_dir: ~/Music/minimax-gen
auto_playback: true
```

---

## 工作流集成状态

| 工作流 | 集成状态 | 技能 |
|--------|----------|------|
| 视频制作 | ✅ Stage 8 | minimax-music-gen, buddy-sings |
| 内容发布 | ⏳ Plan | minimax-music-playlist（BGM 推荐） |
| 考试复习 | ❌ | - |
| 比赛备赛 | ❌ | - |
| 论文写作 | ❌ | - |

---

## 下一步

### 第 6 批整合（候选）

1. ✅ 安装 minimax-music-gen
2. ✅ 安装 buddy-sings
3. ⏳ 更新 CLAUDE.md 触发词表
4. ⏳ 更新 video-production-pipeline.card
5. ⏳ 测试音乐生成功能
6. ⏳ 更新整合报告

预计工作量：1-2 小时

---

## 相关链接

- [MiniMax Skills GitHub](https://github.com/MiniMax-AI/skills)
- [MiniMax Platform](https://platform.minimaxi.com/)
- [mmx-cli NPM](https://www.npmjs.com/package/mmx-cli)
- [buddy-sings Skill](https://github.com/MiniMax-AI/skills/tree/main/skills/buddy-sings)
- [minimax-music-gen Skill](https://github.com/MiniMax-AI/skills/tree/main/skills/minimax-music-gen)

---
