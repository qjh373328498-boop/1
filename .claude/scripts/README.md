# 🎬 一键视频生成脚本

**零配置，一键生成完整视频**

---

## 🚀 快速开始

### 1. 从零开始生成视频

```bash
cd /workspace/.claude/scripts

./make_video.sh --theme "德国心脏病桌游介绍" --duration 270
```

### 2. 使用已有脚本

```bash
./make_video.sh --script /path/to/script.md --output output/
```

### 3. 自定义配置

```bash
./make_video.sh \
  --theme "产品介绍视频" \
  --duration 180 \
  --voice zh-CN-YunxiNeural \
  --output output/
```

---

## 📋 选项说明

| 选项 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| `--theme TEXT` | `-t` | 视频主题（从零开始） | 必填 |
| `--duration NUM` | `-d` | 视频时长（秒） | 180 |
| `--script FILE` | `-s` | 已有脚本文件 | 无 |
| `--output DIR` | `-o` | 输出目录 | `./video-output-时间戳/` |
| `--voice VOICE` | `-v` | TTS 语音 | `zh-CN-YunxiNeural` |
| `--with-bgmv` | `-b` | 添加背景音乐 | 否 |
| `--help` | `-h` | 显示帮助 | - |

---

## 📦 输出文件

```
video-output-20260502-120000/
├── script.md              # 视频脚本
├── narration.mp3          # 配音音频
├── narration.vtt          # WebVTT 字幕
├── storyboard.json        # 分镜脚本
├── batch.json             # 图片生成任务
├── images/                # AI 生成的原始图片
│   ├── scene_01.png
│   ├── scene_02.png
│   └── ...
├── scaled/                # 缩放后图片（1280x720）
│   ├── scene_01.png
│   ├── scene_02.png
│   └── ...
└── final.mp4              # ⭐ 最终视频
```

---

## 🔧 依赖安装

### 必需依赖

```bash
# Python TTS
pip3 install edge-tts

# 图片生成
pip3 install requests

# 视频处理
sudo apt install ffmpeg  # Debian/Ubuntu
# 或
brew install ffmpeg      # macOS
```

### 检查依赖

```bash
./make_video.sh --check
```

---

## 🐛 故障排除

### 问题 1：edge-tts 未安装

```
⚠️  edge-tts 未安装，将跳过配音生成
```

**解决**:
```bash
pip3 install edge-tts
```

### 问题 2：图片生成失败

```
⚠️  图片生成失败，使用占位图片
```

**原因**: ModelScope API key 无效或额度不足

**解决**:
1. 检查 API key 是否正确
2. 使用 `--skip-images` 跳过图片生成
3. 手动准备图片放入 `images/` 目录

### 问题 3：FFmpeg 合成失败

```
[error] Invalid argument
```

**原因**: 图片尺寸不一致

**解决**:
```bash
cd video-output-*/
for img in images/*.png; do
  ffmpeg -y -i "$img" -vf "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1" "scaled/$(basename $img)"
done
./make_video.sh --resume
```

### 问题 4：API 超时

```
TimeoutError: 图片生成超时
```

**解决**:
```bash
# 增加超时时间
export IMAGE_GEN_TIMEOUT=180
./make_video.sh --theme "..."
```

---

## 💡 高级用法

### 分步执行

```bash
# 1. 只生成脚本
./make_video.sh --theme "..." --step 1

# 2. 生成配音
./make_video.sh --script script.md --step 2

# 3. 生成图片
./make_video.sh --output output/ --step 4

# 4. 合成视频
./make_video.sh --output output/ --step 6
```

### 断点续传

```bash
# 从步骤 4 继续（跳过前 3 步）
./make_video.sh --output output/ --resume-from 4
```

### 批量生成

```bash
# 批量任务列表
cat > themes.txt << EOF
德国心脏病桌游介绍
Python 入门教程
环保会计知识
EOF

while read theme; do
  ./make_video.sh --theme "$theme"
done < themes.txt
```

---

## ⚙️ 配置选项

### 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `IMAGE_GEN_TIMEOUT` | 图片生成超时（秒） | 120 |
| `IMAGE_GEN_WORKERS` | 并发 worker 数 | 4 |
| `MODELSCOPE_API_KEY` | ModelScope API key | 内置 |
| `FFMPEG_PRESET` | FFmpeg 预设 | `fast` |
| `FFMPEG_CRF` | 视频质量（18-28） | 23 |

### 配置文件

创建 `.env` 文件：

```bash
# 自定义 API key
MODELSCOPE_API_KEY=ms-your-key

# 调整图片生成并发
IMAGE_GEN_WORKERS=6

# 提高视频质量
FFMPEG_CRF=18
```

---

## 📊 性能参考

| 时长 | 脚本生成 | 配音 | 图片 (9 张) | 合成 | 总计 |
|------|---------|------|------------|------|------|
| 60 秒 | <1s | ~5s | ~4 分钟 | ~30s | ~5 分钟 |
| 180 秒 | <1s | ~10s | ~4 分钟 | ~30s | ~5 分钟 |
| 300 秒 | <1s | ~15s | ~4 分钟 | ~45s | ~5.5 分钟 |

---

## 📝 示例

### 示例 1：快速生成 30 秒视频

```bash
./make_video.sh -t "快速入门" -d 30 -o output/
```

### 示例 2：生成 5 分钟详细讲解

```bash
./make_video.sh \
  -t "德国心脏病桌游完整规则与策略" \
  -d 300 \
  -v zh-CN-YunxiNeural \
  -o output/
```

### 示例 3：使用已有脚本

```bash
./make_video.sh \
  -s /path/to/my_script.md \
  -o output/ \
  -b  # 添加背景音乐
```

---

## 🎯 最佳实践

### 1. 脚本编写

- 每 20-30 秒一个场景
- 每个场景对应一张图片
- 使用清晰的分段标记

### 2. 图片提示词

```bash
# 好的 prompt
"德国心脏病桌游封面，鲜艳的草莓柠檬橙子香蕉，中间金属铃铛，卡通风格，色彩明快"

# 避免
"一张好看的图"  # 太模糊
```

### 3. 视频时长

- 短视频：30-60 秒（快速传播）
- 中视频：3-5 分钟（详细讲解）
- 长视频：10-15 分钟（深度教程）

### 4. 配音选择

| 语音 | 适用场景 |
|------|---------|
| `zh-CN-YunxiNeural` | 通用男声（推荐） |
| `zh-CN-XiaoxiaoNeural` | 通用女声 |
| `zh-CN-YunjianNeural` | 体育解说 |
| `en-US-GuyNeural` | 英语男声 |

---

## 📚 相关文档

- [视频工作流完整文档](workflows/video-production-pipeline.card)
- [ModelScope API 文档](scripts/gen_image.py --help)
- [FFmpeg 参数详解](https://ffmpeg.org/documentation.html)

---

## 🆘 获取帮助

```bash
# 显示帮助
./make_video.sh --help

# 查看版本
./make_video.sh --version

# 检查依赖
./make_video.sh --check-deps

# 测试模式（不实际生成）
./make_video.sh --theme "test" --dry-run
```

---

## ❤️ 贡献

遇到问题或有改进建议？

1. 查看故障排除章节
2. 搜索已有 issues
3. 提交新的 issue

---

**最后更新**: 2026-05-02  
**版本**: v1.0  
**维护**: MonkeyCode AI
