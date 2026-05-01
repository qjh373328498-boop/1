#!/bin/bash

# TTS 语音生成快捷脚本
# 用法：./tts.sh "要转换的文字" [输出文件] [语音名称]

TEXT="$1"
OUTPUT="${2:-output.mp3}"
VOICE="${3:-zh-CN-YunxiNeural}"

if [ -z "$TEXT" ]; then
    echo "用法：$0 \"要转换的文字\" [输出文件.mp3] [语音名称]"
    echo ""
    echo "常用语音："
    echo "  zh-CN-YunxiNeural      - 阳光男声（默认）"
    echo "  zh-CN-XiaoxiaoNeural   - 温暖女声"
    echo "  zh-CN-YunyangNeural    - 专业男声（新闻）"
    echo "  zh-CN-XiaoyiNeural     - 活泼女声（卡通）"
    echo "  zh-CN-liaoning-XiaobeiNeural - 东北话"
    echo ""
    echo "示例："
    echo "  $0 \"你好世界\" hello.mp3"
    echo "  $0 \"你好\" output.mp3 zh-CN-XiaoxiaoNeural"
    exit 1
fi

echo "正在生成语音..."
echo "文字：$TEXT"
echo "语音：$VOICE"
echo "输出：$OUTPUT"

python3 -m edge_tts --voice "$VOICE" --text "$TEXT" --write-media "$OUTPUT"

if [ $? -eq 0 ]; then
    echo "✅ 语音生成成功：$OUTPUT"
else
    echo "❌ 语音生成失败，请检查网络连接"
    exit 1
fi
