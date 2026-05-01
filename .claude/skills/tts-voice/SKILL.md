# TTS 语音生成 Skill

## 描述

基于 edge-tts 的文本转语音工具，使用微软 Edge 语音合成引擎，完全免费，无需 API key。

## 安装

```bash
# 环境已预装
pip install edge-tts
```

## 快速使用

### 方法 1：直接调用
```bash
python3 -m edge_tts --voice <语音名称> --text "<文字>" --write-media output.mp3
```

### 方法 2：使用脚本
```bash
cd /workspace/.claude/skills/tts-voice
./tts.sh "你好，这是测试" output.mp3
```

## 常用命令

### 列出所有语音
```bash
python3 -m edge_tts --list-voices
```

### 按语言筛选
```bash
# 查看所有中文语音
python3 -m edge_tts --list-voices | grep zh-CN

# 查看所有英语语音
python3 -m edge_tts --list-voices | grep en-US
```

### 生成语音
```bash
# 单句文字
python3 -m edge_tts --voice zh-CN-YunxiNeural --text "你好世界" --write-media hello.mp3

# 从文件读取
python3 -m edge_tts --voice zh-CN-XiaoxiaoNeural --file script.txt --write-media audio.mp3

# 带语速调整（+20%）
python3 -m edge_tts --voice zh-CN-YunxiNeural --text "你好" --rate=+20% --write-media fast.mp3

# 带音调调整（+10Hz）
python3 -m edge_tts --voice zh-CN-XiaoxiaoNeural --text "你好" --pitch=+10Hz --write-media high.mp3
```

### 生成字幕
```bash
python3 -m edge_tts --voice zh-CN-YunxiNeural \
  --text "你好世界" \
  --write-media output.mp3 \
  --write-subtitles output.vtt
```

## 批量处理

```bash
# 批量转换文本文件
for file in *.txt; do
  python3 -m edge_tts --voice zh-CN-YunxiNeural \
    --file "$file" \
    --write-media "${file%.txt}.mp3"
done
```

## 语音推荐

| 场景 | 推荐语音 | 说明 |
|------|----------|------|
| 新闻播报 | zh-CN-YunyangNeural | 专业男声 |
| 小说朗读 | zh-CN-YunxiNeural | 阳光男声 |
| 儿童故事 | zh-CN-YunxiaNeural | 可爱男声 |
| 温馨旁白 | zh-CN-XiaoxiaoNeural | 温暖女声 |
| 卡通动画 | zh-CN-XiaoyiNeural | 活泼女声 |
| 东北特色 | zh-CN-liaoning-XiaobeiNeural | 东北话女声 |
| 粤语内容 | zh-HK-HiuMaanNeural | 粤语女声 |
| 英语内容 | en-US-JennyNeural | 温暖女声 |

## 参数说明

| 参数 | 说明 | 默认值 | 示例 |
|------|------|--------|------|
| --voice | 语音名称 | - | zh-CN-YunxiNeural |
| --text | 要转换的文字 | - | "你好世界" |
| --file | 文字文件路径 | - | script.txt |
| --write-media | 输出音频文件 | - | output.mp3 |
| --write-subtitles | 输出字幕文件 | - | output.vtt |
| --rate | 语速调整 | +0% | +20% / -10% |
| --pitch | 音调调整 | +0Hz | +10Hz / -5Hz |
| --volume | 音量调整 | +0% | +50% / -20% |

## 环境要求

- Python 3.7+
- 网络连接（需要访问微软服务）
- edge-tts 包

## 常见问题

### Q: 生成失败
A: 检查网络连接，确保能访问微软服务

### Q: 想要更快的语速
A: 使用 `--rate=+50%` 参数

### Q: 声音太机械
A: 尝试不同的语音，推荐 Xiaoxiao 或 Yunxi

### Q: 长文本如何处理
A: 分段生成，每段控制在 5000 字以内

## 相关文件

- 工作流卡片：`/workspace/.claude/workflows/tts-voice.card`
- 脚本目录：`/workspace/.claude/skills/tts-voice/`

## 参考资料

- GitHub: https://github.com/rany2/edge-tts
- PyPI: https://pypi.org/project/edge-tts/
