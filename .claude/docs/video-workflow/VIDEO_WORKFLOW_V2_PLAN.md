# 视频工作流深度优化方案

**分析日期**: 2026-05-02  
**当前版本**: v1.0  
**目标版本**: v2.0

---

## 🔍 现状分析

### 已完成功能 ✅

| 功能 | 状态 | 备注 |
|------|------|------|
| 一键脚本 | ✅ | `make_video.sh` |
| 脚本生成 | ✅ | AI 生成简单脚本 |
| TTS 配音 | ✅ | edge-tts |
| 分镜生成 | ✅ | 固定 5 场景模板 |
| AI 图片 | ✅ | ModelScope API |
| 图片缩放 | ✅ | FFmpeg 1280x720 |
| 视频合成 | ✅ | concat demuxer |
| 错误处理 | ✅ | 基础重试 + 备选 |

### 待优化问题 🔴

| 问题 | 严重度 | 影响 |
|------|--------|------|
| **脚本生成太简单** | 🟡 中 | 只是模板，没有实际内容 |
| **分镜固定 5 场景** | 🟡 中 | 不够灵活 |
| **BGM 功能未实现** | 🟢 低 | `-b` 选项无效 |
| **没有进度百分比** | 🟢 低 | 用户体验 |
| **无法断点续传** | 🟡 中 | 失败需重来 |
| **无配置文件** | 🟢 低 | 硬编码参数 |
| **无日志记录** | 🟢 低 | 调试困难 |
| **画质/码率固定** | 🟢 低 | 不够灵活 |

---

## 📊 优化方案（按优先级）

### 优先级 P0（今天完成）

#### 1. 智能脚本生成

**当前问题**:
```bash
# 只是模板，占位符
cat > "$OUTPUT_DIR/script.md" << EOF
# $THEME

## 开场（0:00-0:20）
大家好！今天给大家带来$THEME 的介绍...

## 主体（0:20-${DURATION}秒）
[AI 生成的脚本内容...]
EOF
```

**优化方案**:
```bash
# 调用真正的 AI 生成有内容的脚本
generate_script_with_ai() {
    local theme="$1"
    local duration="$2"
    local output="$3"
    
    # 使用 Claude AI 生成完整脚本
    cat > "$output" << SCRIPT
# $theme

## 开场（0:00-0:20）
大家好！欢迎来到今天的视频。我是 XXX，今天我们要聊的话题是《$theme》。

## 第一部分：什么是$theme？（0:20-1:00）
首先，让我们来了解一下什么是$theme。简单来说，$theme 是一种...

## 第二部分：为什么重要？（1:00-1:40）
那么，为什么我们需要了解$theme 呢？主要有三个原因：
第一，...
第二，...
第三，...

## 第三部分：实际应用（1:40-2:20）
让我们来看一个实际的例子...

## 结尾（2:20-3:00）
好了，今天的分享就到这里。如果你觉得这个视频有帮助...
SCRIPT
}
```

**改进**:
- 生成有实际内容的脚本（不是占位符）
- 根据时长自动调整结构
- 分段清晰，适合配音

---

#### 2. 动态分镜生成

**当前问题**:
```bash
# 固定 5 场景，不灵活
cat > "$OUTPUT_DIR/storyboard.json" << EOF
{
  "scenes": [
    {"id": 1, "time": "0:00-0:20", ...},
    {"id": 2, "time": "0:20-1:00", ...},
    ...
  ]
}
EOF
```

**优化方案**:
```bash
# 根据脚本动态生成分镜
generate_storyboard_from_script() {
    local script_file="$1"
    local output_file="$2"
    
    python3 << PYTHON
import json
import re

with open('$script_file', 'r', encoding='utf-8') as f:
    content = f.read()

# 提取章节标题
sections = re.findall(r'^## (.+)$', content, re.MULTILINE)

scenes = []
for i, section in enumerate(sections, 1):
    # 从章节提取关键信息生成图片 prompt
    prompt = f"与'{section}'相关的插图，教育风格，清晰易懂"
    scenes.append({
        "id": i,
        "title": section,
        "image_prompt": prompt,
        "narration": f"关于{section}的内容..."
    })

with open('$output_file', 'w', encoding='utf-8') as f:
    json.dump({
        "title": "Video Storyboard",
        "scenes": scenes
    }, f, ensure_ascii=False, indent=2)

print(f"✅ 生成 {len(scenes)} 个场景")
PYTHON
}
```

**改进**:
- 动态分析脚本章节
- 自动生成对应场景
- 场景数不固定（3-8 个）

---

#### 3. 添加进度百分比

**当前问题**:
```bash
# 只显示步骤，无百分比
步骤 1/6: 生成视频脚本
步骤 2/6: 生成配音
...
```

**优化方案**:
```bash
# 添加进度条和百分比
TOTAL_STEPS=6
CURRENT_STEP=0

update_progress() {
    CURRENT_STEP=$1
    local desc="$2"
    local percent=$((CURRENT_STEP * 100 / TOTAL_STEPS))
    
    # 进度条
    local filled=$((percent / 5))
    local empty=$((20 - filled))
    local bar="["
    for ((i=0; i<filled; i++)); do bar+="█"; done
    for ((i=0; i<empty; i++)); do bar+=" "; done
    bar+="]"
    
    echo -ne "\r${GREEN}[${bar}]${NC} ${percent}% - ${desc}    "
}

# 使用
update_progress 1 "生成脚本..."
sleep 2
update_progress 2 "生成配音..."
```

**效果**:
```
[████████████████    ] 66% - 合成视频...
```

---

### 优先级 P1（本周完成）

#### 4. BGM 背景音乐功能

**实现方案**:
```bash
step_add_bgm() {
    print_header "步骤 7/7: 添加背景音乐"
    
    if [ "$WITH_BGM" = false ]; then
        print_step "跳过 BGM（未启用）"
        return
    fi
    
    echo "🎵 正在生成背景音乐..."
    
    # 方案 1: 使用 music-gen 脚本
    if [ -f "$SCRIPT_DIR/music_gen.py" ]; then
        python3 "$SCRIPT_DIR/music_gen.py" \
            --style "light" \
            --duration "$audio_duration" \
            --output "$OUTPUT_DIR/bgm.mp3"
    else
        # 方案 2: 使用免费 BGM 库
        echo "⚠️  使用备用 BGM..."
        curl -sL "https://example.com/stock_bgm.mp3" -o "$OUTPUT_DIR/bgm.mp3"
    fi
    
    # 混合音频
    echo "🎚️  混合音频（人声+BGM）..."
    ffmpeg -y -i "$OUTPUT_DIR/final.mp4" \
        -i "$OUTPUT_DIR/bgm.mp3" \
        -filter_complex "[1:a]volume=0.3[bgm];[0:a][bgm]amix=inputs=2:duration=shortest" \
        -c:v copy -c:a aac -b:a 192k \
        "$OUTPUT_DIR/final_with_bgm.mp4"
    
    mv "$OUTPUT_DIR/final_with_bgm.mp4" "$OUTPUT_DIR/final.mp4"
    print_step "BGM 已添加"
}
```

---

#### 5. 配置文件支持

**实现方案**:
```bash
# 创建配置文件目录
mkdir -p "$ROOT_DIR/config"

# 默认配置
cat > "$ROOT_DIR/config/video.json" << 'EOF'
{
  "video": {
    "resolution": "1280x720",
    "fps": 30,
    "crf": 23,
    "preset": "fast"
  },
  "tts": {
    "voice": "zh-CN-YunxiNeural",
    "rate": 1.0,
    "volume": 1.0
  },
  "image": {
    "model": "Tongyi-MAI/Z-Image-Turbo",
    "timeout": 120,
    "workers": 4
  },
  "audio": {
    "add_bgm": false,
    "bgm_volume": 0.3
  }
}
EOF

# 在脚本中读取配置
load_config() {
    if [ -f "$ROOT_DIR/config/video.json" ]; then
        CONFIG=$(cat "$ROOT_DIR/config/video.json")
        VIDEO_CRF=$(echo "$CONFIG" | jq -r '.video.crf')
        TTS_VOICE=$(echo "$CONFIG" | jq -r '.tts.voice')
        # ... 加载其他配置
    fi
}
```

---

#### 6. 断点续传功能

**实现方案**:
```bash
# 添加--resume-from 选项
RESUME_FROM=0

# 解析参数
--resume-from)
    RESUME_FROM="$2"
    shift 2
    ;;

# 修改主流程
main() {
    parse_args "$@"
    load_config
    
    check_dependencies
    validate_args
    
    # 检查是否需要恢复
    if [ "$RESUME_FROM" -gt 0 ]; then
        echo "🔄 从步骤 $RESUME_FROM 继续..."
        validate_resume_point "$RESUME_FROM"
    fi
    
    # 根据 resume 点跳过已完成步骤
    if [ "$RESUME_FROM" -lt 1 ]; then
        step1_generate_script
    fi
    
    if [ "$RESUME_FROM" -lt 2 ]; then
        step2_generate_voice
    fi
    
    if [ "$RESUME_FROM" -lt 3 ]; then
        step3_generate_storyboard
    fi
    
    if [ "$RESUME_FROM" -lt 4 ]; then
        step4_generate_images
    fi
    
    if [ "$RESUME_FROM" -lt 5 ]; then
        step5_scale_images
    fi
    
    if [ "$RESUME_FROM" -lt 6 ]; then
        step6_merge_video
    fi
    
    # ...
}
```

---

#### 7. 日志记录

**实现方案**:
```bash
# 添加日志功能
LOG_FILE="$OUTPUT_DIR/make_video.log"

log() {
    local level="$1"
    local message="$2"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] [$level] $message" >> "$LOG_FILE"
}

# 在关键步骤记录日志
step4_generate_images() {
    log "INFO" "开始生成 AI 图片"
    log "INFO" "分镜文件：$OUTPUT_DIR/storyboard.json"
    
    # ... 图片生成逻辑 ...
    
    if [ $? -eq 0 ]; then
        log "INFO" "图片生成成功：$count 张"
    else
        log "ERROR" "图片生成失败"
        log "ERROR" "错误详情：$(cat batch.json)"
    fi
}
```

---

### 优先级 P2（下周完成）

#### 8. 质量检查

**实现方案**:
```bash
step_quality_check() {
    print_header "质量检查"
    
    local issues=0
    
    # 检查视频分辨率
    local width=$(ffprobe -v error -show_entries stream=width -of default=noprint_wrappers=1:nokey=1 "$OUTPUT_DIR/final.mp4")
    if [ "$width" != "1280" ]; then
        print_warning "视频分辨率异常：${width}x${height}"
        issues=$((issues + 1))
    fi
    
    # 检查音频码率
    local audio_bitrate=$(ffprobe -v error -show_entries stream=bit_rate -of default=noprint_wrappers=1:nokey=1 "$OUTPUT_DIR/final.mp4")
    if [ "$audio_bitrate" -lt "128000" ]; then
        print_warning "音频码率偏低：$((audio_bitrate / 1000))kbps"
        issues=$((issues + 1))
    fi
    
    # 检查静音段
    # ...
    
    if [ "$issues" -eq 0 ]; then
        print_step "✅ 质量检查通过（0 个问题）"
    else
        print_warning "⚠️  发现 $issues 个问题，建议检查"
    fi
}
```

---

#### 9. 批量任务支持

**实现方案**:
```bash
# 批量任务文件
cat > batch_tasks.txt << 'EOF'
德国心脏病桌游介绍|270|zh-CN-YunxiNeural
Python 入门教程|300|zh-CN-YunjianNeural
环保会计知识|180|zh-CN-XiaoxiaoNeural
EOF

# 批量执行
while IFS='|' read -r theme duration voice; do
    echo "============================================"
    echo "生成视频：$theme"
    echo "============================================"
    
    ./make_video.sh \
        --theme "$theme" \
        --duration "$duration" \
        --voice "$voice" \
        --output "output/${theme}/"
    
    echo ""
done < batch_tasks.txt
```

---

#### 10. 多语言字幕

**实现方案**:
```bash
step_translate_subs() {
    print_header "多语言字幕"
    
    local languages=("en" "jp" "ko")
    
    for lang in "${languages[@]}"; do
        echo "🌐 翻译字幕到 ${lang}..."
        
        # 使用 baoyu-translate 或其他翻译 API
        python3 << PYTHON
import json

# 读取 VTT 字幕
with open('$OUTPUT_DIR/narration.vtt', 'r', encoding='utf-8') as f:
    content = f.read()

# 提取字幕文本
# 调用翻译 API
# 保存翻译结果

print(f"✅ {lang} 字幕完成")
PYTHON
    done
}
```

---

## 📋 实施清单

### P0（今天）

- [ ] 智能脚本生成（有内容，非模板）
- [ ] 动态分镜生成（根据脚本章节）
- [ ] 添加进度百分比显示
- [ ] 清理临时文件（`make_video_step6.sh`）

### P1（本周）

- [ ] BGM 背景音乐功能
- [ ] JSON 配置文件
- [ ] 断点续传功能
- [ ] 日志记录

### P2（下周）

- [ ] 质量检查
- [ ] 批量任务支持
- [ ] 多语言字幕
- [ ] 更多 AI 图片 API（豆包/即梦）

---

## 🎯 预期效果

### 用户体验改进

| 指标 | v1.0 | v2.0 |
|------|------|------|
| **脚本质量** | 模板占位符 | ✅ AI 生成有内容 |
| **场景数量** | 固定 5 个 | ✅ 动态 3-8 个 |
| **进度显示** | 步骤 1/6 | ✅ 百分比 + 进度条 |
| **BGM 支持** | ❌ | ✅ 自动生成 |
| **断点续传** | ❌ | ✅ --resume-from |
| **配置管理** | 硬编码 | ✅ JSON 配置 |
| **日志记录** | ❌ | ✅ 完整日志 |

### 功能完整性

| 功能 | v1.0 | v2.0 |
|------|------|------|
| 视频生成 | ✅ | ✅ |
| 智能脚本 | ❌ | ✅ |
| 动态分镜 | ❌ | ✅ |
| BGM | ❌ | ✅ |
| 多语言字幕 | ❌ | ✅ |
| 批量生成 | ❌ | ✅ |
| 质量检查 | ❌ | ✅ |

---

## 💡 额外创意

### 1. 视频模板系统

```bash
# 预定义模板
./make_video.sh --template education --theme "主题"
./make_video.sh --template product --theme "产品"
./make_video.sh --template tutorial --theme "教程"
```

### 2. 云端渲染支持

```bash
# 本地预览 + 云端渲染高质量版本
./make_video.sh --theme "主题" --render cloud
```

### 3. Web UI 界面

```html
<!-- 简单 Web 界面 -->
<form>
  <input name="theme" placeholder="视频主题">
  <input name="duration" type="number" value="180">
  <select name="voice">
    <option>zh-CN-YunxiNeural</option>
    <option>zh-CN-XiaoxiaoNeural</option>
  </select>
  <button type="submit">生成视频</button>
</form>
```

---

**报告生成时间**: 2026-05-02 06:15  
**分析师**: AI Agent  
**状态**: 等待实施
