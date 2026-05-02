# 音频/音效 Skill 调研报告

> 日期：2026-05-01  
> 状态：✅ 完成调研  

---

## 执行摘要

通过搜索 baoyu-skills 官方仓库和第三方技能市场，发现以下音频/音效相关技能：

### 已有技能（baoyu-skills）

| 技能 | 用途 | 状态 |
|------|------|------|
| `music-gen` | 背景音乐生成 | ✅ 已集成到视频工作流 |
| `tts-voice` | 语音合成（TTS） | ✅ 已集成到视频工作流 |
| `auto-subtitles` | 字幕生成 | ✅ 已集成到视频工作流 |

### 缺失技能（需要新增）

| 技能 | 用途 | 优先级 | 来源 |
|------|------|--------|------|
| 音效生成 | 视频转场/强调/环境音效 | 🔴 高 | MiniMax AI |
| 音频增强 | 降噪/音量标准化/呼吸声消除 | 🔴 高 | 需要开发 |
| 音频分析 | 音频特征提取/BPM 检测 | 🟡 中 | 需要开发 |

---

## 第三方技能发现

### MiniMax AI Skills

MiniMax 提供了 3 个音乐相关技能，可直接安装到 Claude Code：

#### 1. buddy-sings
- **功能**：读取 Agent 宠物性格，匹配音色和风格，根据上下文写词作曲
- **GitHub**: https://github.com/MiniMax-AI/skills/tree/main/skills/buddy-sings
- **适用场景**：角色配音、吉祥物唱歌

#### 2. minimax-music-gen
- **功能**：核心生成引擎，支持人声歌曲、纯音乐、翻唱三种模式
- **GitHub**: https://github.com/MiniMax-AI/skills/tree/main/skills/minimax-music-gen
- **适用场景**：背景音乐、主题曲生成

#### 3. minimax-music-playlist
- **功能**：分析听歌偏好，构建品味画像，自动生成原创歌单
- **GitHub**: https://github.com/MiniMax-AI/skills/tree/main/skills/minimax-music-playlist
- **适用场景**：个性化推荐

### 安装方式

```bash
# 使用 MMX-CLI（推荐）
npx skil add minimax-music-gen

# 或使用 ClawHub CLI
npx clawhub@latest install music-generation
```

---

## 其他音频生成工具

### Audiocraft (Meta AI)
- **项目地址**: https://gitcode.com/gh_mirrors/au/audiocraft
- **功能**：深度学习音频生成库
- **特点**：
  - EnCodec 高保真神经音频编解码器
  - MusicGen 音乐生成模型
  - AudioGen 音效生成模型
  - 支持 32kHz 立体声音频
- **适用场景**：游戏音效、影视配乐

### Suno AI
- **官网**: https://sunnoai.com/
- **功能**：AI 音乐生成平台
- **特点**：
  - 完整歌曲生成（包括人声、歌词）
  - 支持多种音乐风格
  - 可生成 radio-ready 质量音频
- **API**: 提供 RESTful API 供开发者集成

---

## 建议方案

### 方案 A：集成 MiniMax Skills（推荐）

**优点**：
- ✅ 现成可用，无需开发
- ✅ 与 baoyu-skills 兼容
- ✅ 支持中文
- ✅ 有完善的文档

**集成步骤**：
1. 安装 minimax-music-gen（背景音乐）
2. 安装 buddy-sings（角色配音）
3. 更新视频工作流文档
4. 添加到 CLAUDE.md 触发词表

**预计工作量**：1-2 小时

### 方案 B：自行开发音效生成 skill

**功能范围**：
- 转场音效（whoosh、hit、riser 等）
- 强调音效（ding、pop、click 等）
- 环境音效（雨声、咖啡厅、自然等）

**技术方案**：
1. 使用 Audiocraft AudioGen 模型
2. 或使用 Suno AI API
3. 封装为 baoyu-sound-effects skill

**预计工作量**：3-5 天

### 方案 C：音频增强 skill

**功能范围**：
- 降噪处理
- 音量标准化（-16LUFS）
- 呼吸声消除
- 音频修复

**技术方案**：
1. 集成 openai-whisper（语音识别 + 时间戳）
2. 使用 pydub 进行音频处理
3. 集成 adobe-podcast API（如有）

**预计工作量**：5-7 天

---

## 推荐优先级

### 第 1 优先级（本周）
- ✅ 集成 minimax-music-gen（背景音乐增强）
- ✅ 集成 buddy-sings（角色配音）

### 第 2 优先级（下周）
- ⏳ 开发 baoyu-sound-effects（音效库）
- ⏳ 集成 Audiocraft AudioGen

### 第 3 优先级（后续）
- ⏳ 开发 baoyu-audio-enhance（音频增强）
- ⏳ 集成 Suno AI API（歌曲生成）

---

## 视频工作流增强建议

### 当前工作流（v4.0）

```
资料收集 → 创意 → 脚本 → 配音 → 分镜 → 素材 → 视频 → 字幕 → BGM → 多语言 → 发布
```

### 增强后工作流（v5.0 建议）

```
资料收集 → 创意 → 脚本 → 配音 → 分镜 → 素材 → 视频 → 字幕 → BGM → **音效** → **音频增强** → 多语言 → 发布
```

**新增技能**：
- Step 10: 音效生成（转场/强调/环境）
- Step 11: 音频增强（降噪/标准化）

---

## 下一步行动

### 立即执行
1. ✅ 安装 minimax-music-gen
2. ✅ 安装 buddy-sings
3. ✅ 测试音频生成功能

### 计划执行
1. ⏳ 开发 baoyu-sound-effects（Week 2）
2. ⏳ 集成 Audiocraft（Week 3）
3. ⏳ 开发 baoyu-audio-enhance（Week 4）

---

## 相关链接

- [baoyu-skills GitHub](https://github.com/JimLiu/baoyu-skills)
- [MiniMax AI Skills](https://github.com/MiniMax-AI/skills)
- [Audiocraft GitCode](https://gitcode.com/gh_mirrors/au/audiocraft)
- [Suno AI](https://sunnoai.com/)

---
