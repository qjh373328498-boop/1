# 视频工作流问题诊断报告

**日期**: 2026-05-02  
**状态**: 🔴 需要紧急修复

---

## 🐛 核心问题

### 问题 1：文档冗长但不可执行

**现状**:
- `video-production-pipeline.card` 517 行，全是配置说明
- **没有一键执行的总控脚本**
- 用户需要手动复制粘贴命令

**影响**:
- 用户不知道从哪里开始
- 每个步骤都要手动执行
- 无法批量自动化

### 问题 2：脚本分散无组织

**现有脚本**:
```
.claude/scripts/
├── gen_image.py          # 只有图片生成
└── test_gen_image.sh     # 只是测试
```

**缺失脚本**:
- ❌ 没有一键视频生成脚本
- ❌ 没有从脚本到配音的自动化
- ❌ 没有从图片到视频的自动化
- ❌ 没有 BGM 集成

### 问题 3：错误处理空白

**当前状态**:
- API 失败后没有重试机制
- 图片生成失败没有备选方案
- FFmpeg 合成失败没有调试指南

### 问题 4：输入输出不清晰

**用户困惑**:
- "我应该准备什么文件？"
- "脚本放哪里？"
- "输出在哪里找？"
- "如何查看进度？"

---

## 📊 对比优秀工作流

### TTS 配音工作流（参考）

**优点**:
```bash
# 一行命令完成
python3 -m edge_tts --voice zh-CN-YunxiNeural --file script.txt --write-media narration.mp3
```

**特点**:
- ✅ 单一入口
- ✅ 参数清晰
- ✅ 输出明确

### 视频工作流（应该达到）

```bash
# 一行命令完成全部
./make_video.sh --theme "德国心脏病桌游" --duration 270 --output output/
```

---

## ✅ 修复方案

### 阶段 1：创建总控脚本（今天）

**文件**: `.claude/scripts/make_video.sh`

```bash
#!/bin/bash
# 一键视频生成脚本
# 用法：./make_video.sh [选项]

THEME=""        # 主题
DURATION=180    # 时长（秒）
SCRIPT=""       # 脚本文件（可选）
OUTPUT=""       # 输出目录

# 步骤：
# 1. 如果没有脚本，用 AI 生成
# 2. 生成配音
# 3. 生成分镜
# 4. AI 生成图片
# 5. 合成视频
# 6. 添加 BGM（可选）
# 7. 输出最终视频
```

### 阶段 2：完善子脚本（今天）

**需要的脚本**:
1. `gen_script.sh` - 生成视频脚本
2. `gen_voice.sh` - 生成配音
3. `gen_storyboard.sh` - 生成分镜
4. `gen_images.sh` - AI 生成图片
5. `make_video.sh` - 合成视频
6. `add_bgm.sh` - 添加背景音乐

### 阶段 3：添加配置管理（明天）

**文件**: `.claude/config/video.json`

```json
{
  "modelscope_api_key": "ms-xxx",
  "tts_voice": "zh-CN-YunxiNeural",
  "video_resolution": "1280x720",
  "video_fps": 30,
  "bgm_volume": 0.3
}
```

### 阶段 4：错误处理（明天）

- API 失败自动重试（3 次）
- 图片生成失败使用备用图片
- FFmpeg 失败提供调试命令

---

## 🎯 预期效果

### 用户使用流程（简化后）

```bash
# 场景 1：已有脚本
./make_video.sh --script script.md --output output/

# 场景 2：从零开始
./make_video.sh --theme "德国心脏病桌游介绍" --duration 270

# 场景 3：自定义配置
./make_video.sh \
  --theme "产品介绍" \
  --duration 180 \
  --voice zh-CN-YunxiNeural \
  --with-bgmv \
  --output output/
```

### 输出

```
output/
├── script.md              # 视频脚本
├── narration.mp3          # 配音
├── narration.vtt          # 字幕
├── storyboard.json        # 分镜
├── images/                # AI 图片
│   ├── cover.png
│   ├── components.png
│   └── ...
├── scaled/                # 缩放后图片
└── final.mp4              # 最终视频 ⭐
```

---

## 📋 实施清单

### 紧急修复（今天完成）
- [ ] 创建 `make_video.sh` 总控脚本
- [ ] 创建 5 个子脚本
- [ ] 添加配置管理
- [ ] 添加进度显示
- [ ] 添加错误处理

### 优化增强（明天完成）
- [ ] 添加 BGM 支持
- [ ] 添加多语言字幕
- [ ] 添加质量检查
- [ ] 添加日志记录
- [ ] 添加帮助文档

### 测试验证
- [ ] 测试从零开始生成视频
- [ ] 测试已有脚本生成
- [ ] 测试错误恢复
- [ ] 性能测试（9 张图片）

---

## 💡 关键改进

| 改进点 | 之前 | 之后 |
|--------|------|------|
| **入口数量** | 7 个独立命令 | 1 个总控脚本 |
| **配置方式** | 硬编码 | JSON 配置 |
| **错误处理** | ❌ 无 | ✅ 自动重试 + 备选 |
| **进度显示** | ❌ 无 | ✅ 实时百分比 |
| **文档长度** | 517 行 | 50 行核心 + 按需查看 |
| **上手难度** | 困难 | 简单（1 行命令） |

---

**报告生成时间**: 2026-05-02  
**优先级**: 🔴 紧急  
**预计完成**: 今天 2 小时内
