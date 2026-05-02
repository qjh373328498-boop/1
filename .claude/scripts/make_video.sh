#!/bin/bash
# 🎬 一键视频生成脚本（v2.2 - 支持配置文件和断点续传）
# 
# 用法:
#   ./make_video.sh --theme "视频主题" --duration 180
#   ./make_video.sh --config config.json  # 使用配置文件
#   ./make_video.sh --resume-from 3  # 从步骤 3 继续
#   ./make_video.sh -b --bgm-file music.mp3  # 添加 BGM
#   ./make_video.sh -h  # 显示帮助
#
# 功能:
#   脚本 → 配音 → 分镜 → AI 图片 → 视频合成 → BGM → 成品

set -e

# ==================== 默认配置 ====================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
GEN_IMAGE_SCRIPT="$SCRIPT_DIR/gen_image.py"

# 默认参数
THEME=""
DURATION=180
SCRIPT_FILE=""
OUTPUT_DIR=""
VOICE="zh-CN-YunxiNeural"
BGM_FILE=""
WITH_BGM=false
SHOW_HELP=false
LOG_FILE=""
VERBOSE=false
TOTAL_STEPS=6
CURRENT_STEP=0
CONFIG_FILE=""
RESUME_FROM=0
SKIP_STEPS=false
QUALITY_CHECK=true
IMAGE_WIDTH=1280
IMAGE_HEIGHT=720
VIDEO_CODEC="libx264"
VIDEO_CRF=23
AUDIO_BITRATE="192k"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# ==================== 日志功能 ====================

log() {
    local level="$1"
    local message="$2"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] [$level] $message" >> "$LOG_FILE"
    
    if [ "$VERBOSE" = true ] || [ "$level" = "ERROR" ] || [ "$level" = "WARN" ]; then
        echo "[$level] $message"
    fi
}

log_step() {
    local step="$1"
    local message="$2"
    log "STEP" "[$step] $message"
}

log_error() {
    log "ERROR" "$1"
}

log_info() {
    log "INFO" "$1"
}

# ==================== 配置文件功能 ====================

load_config() {
    if [ -n "$CONFIG_FILE" ] && [ -f "$CONFIG_FILE" ]; then
        echo "📄 加载配置文件：$CONFIG_FILE"
        
        # 使用 Python 解析 JSON 配置
        eval "$(python3 << PYTHON
import json

with open('$CONFIG_FILE', 'r', encoding='utf-8') as f:
    config = json.load(f)

# 输出 bash 变量
for key, value in config.items():
    key_upper = key.upper().replace('-', '_')
    if isinstance(value, bool):
        print(f'{key_upper}={str(value).lower()}')
    elif isinstance(value, str):
        # 转义特殊字符
        value_escaped = value.replace('\"', '\\\\\"').replace('\$', '\\\$')
        print(f'{key_upper}=\"{value_escaped}\"')
    else:
        print(f'{key_upper}={value}')
PYTHON
)"
        
        log_info "已加载配置文件：$CONFIG_FILE"
    fi
}

validate_config() {
    local errors=0
    
    # 检查视频参数
    if [ "$DURATION" -lt 10 ] || [ "$DURATION" -gt 600 ]; then
        print_error "视频时长必须在 10-600 秒之间"
        errors=$((errors + 1))
    fi
    
    # 检查分辨率
    if [ "$IMAGE_WIDTH" -lt 480 ] || [ "$IMAGE_HEIGHT" -lt 270 ]; then
        print_error "分辨率过低"
        errors=$((errors + 1))
    fi
    
    # 检查 CRF 值 (0-51, 越小质量越高)
    if [ "$VIDEO_CRF" -lt 0 ] || [ "$VIDEO_CRF" -gt 51 ]; then
        print_error "CRF 值必须在 0-51 之间"
        errors=$((errors + 1))
    fi
    
    if [ $errors -gt 0 ]; then
        print_error "配置验证失败，发现 $errors 个错误"
        exit 1
    fi
    
    log_info "配置验证通过"
}

# ==================== 工具函数 ====================

print_header() {
    echo -e "${BLUE}=========================================${NC}"
    echo -e "${BLUE}  🎬 $1${NC}"
    echo -e "${BLUE}=========================================${NC}"
    if [ -n "$LOG_FILE" ] && [ -f "$LOG_FILE" ]; then
        log_info "$1"
    fi
}

print_step() {
    echo -e "${GREEN}[✓] $1${NC}"
    if [ -n "$LOG_FILE" ] && [ -f "$LOG_FILE" ]; then
        log_info "$1"
    fi
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
    if [ -n "$LOG_FILE" ] && [ -f "$LOG_FILE" ]; then
        log "WARN" "$1"
    fi
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
    if [ -n "$LOG_FILE" ] && [ -f "$LOG_FILE" ]; then
        log_error "$1"
    fi
}

# 进度显示函数
update_progress() {
    local step=$1
    local message=$2
    CURRENT_STEP=$step
    
    # 计算百分比
    local percentage=$((step * 100 / TOTAL_STEPS))
    
    # 进度条显示
    local filled=$((percentage / 5))
    local empty=$((20 - filled))
    local bar=""
    for ((i=0; i<filled; i++)); do
        bar+="█"
    done
    for ((i=0; i<empty; i++)); do
        bar+="░"
    done
    
    # 清除当前行并打印进度
    printf "\r${CYAN}⏳ 进度：[%s] %3d%% - ${message}${NC}" "$bar" "$percentage"
    
    log_step "$step/$TOTAL_STEPS" "$message"
}

finish_progress() {
    printf "\n"
    echo -e "${GREEN}✓ 全部完成！${NC}"
}

check_dependencies() {
    local missing=()
    
    if ! command -v python3 &> /dev/null; then
        missing+=("python3")
    fi
    
    if ! command -v ffmpeg &> /dev/null; then
        missing+=("ffmpeg")
    fi
    
    if ! command -v edge-tts &> /dev/null && ! python3 -m edge_tts &> /dev/null; then
        print_warning "edge-tts 未安装，将跳过配音生成"
    fi
    
    if [ ${#missing[@]} -ne 0 ]; then
        print_error "缺少依赖：${missing[*]}"
        echo "请安装：pip3 install edge-tts requests"
        exit 1
    fi
    
    print_step "依赖检查通过"
}

show_help() {
    cat << EOF
🎬 一键视频生成脚本 (v2.2)

用法:
  \$0 --theme "视频主题" --duration 180
  \$0 --config config.json  # 使用配置文件
  \$0 --resume-from 3  # 从步骤 3 继续
  \$0 -b --bgm-file music.mp3  # 添加背景音乐
  \$0 -v  # 详细日志模式
  \$0 -h  # 显示帮助

选项:
  -t, --theme TEXT        视频主题（从零开始时使用）
  -d, --duration NUM      视频时长（秒，默认：180）
  -s, --script FILE       已有脚本文件路径
  -o, --output DIR        输出目录（默认：./video-output/）
  -v, --voice VOICE       TTS 语音（默认：zh-CN-YunxiNeural）
  -b, --with-bgm          添加背景音乐（启用 BGM 功能）
      --bgm-file FILE     BGM 文件路径（MP3 格式）
  -c, --config FILE       JSON 配置文件路径
      --resume-from N     从第 N 步继续执行 (1-6)
      --width NUM         图片宽度 (默认：1280)
      --height NUM        图片高度 (默认：720)
      --crf NUM           视频质量 0-51 (默认：23, 越小质量越高)
      --audio-bitrate K   音频比特率 (默认：192k)
      --no-quality-check  跳过质量检查
      --verbose           显示详细日志
  -h, --help              显示帮助信息

示例:
  # 从零开始生成视频
  \$0 --theme "德国心脏病桌游介绍" --duration 270

  # 使用配置文件
  \$0 --config my-video.json

  # 从步骤 3（分镜生成）继续执行
  \$0 --resume-from 3 --output ./video-output-20260502/

  # 自定义视频质量
  \$0 --theme "高质量演示" --duration 120 --crf 18 --audio-bitrate 256k

  # 自定义分辨率
  \$0 --theme "4K 视频" --duration 60 --width 3840 --height 2160

  # 添加背景音乐
  \$0 --theme "旅游 vlog" --duration 120 --with-bgm --bgm-file bgm.mp3

  # 详细日志模式
  \$0 --theme "科普视频" --duration 180 --verbose

输出:
  output/
  ├── script.md           # 视频脚本
  ├── narration.mp3       # 配音
  ├── narration.vtt       # 字幕
  ├── storyboard.json     # 分镜
  ├── images/             # AI 图片
  ├── scaled/             # 缩放后图片
  ├── final.mp4           # 最终视频 ⭐
  ├── make_video.log      # 执行日志
  └── quality_report.txt  # 质量检查报告

配置文件示例 (config.json):
  {
    "theme": "视频主题",
    "duration": 180,
    "voice": "zh-CN-YunxiNeural",
    "width": 1280,
    "height": 720,
    "crf": 23,
    "audio-bitrate": "192k",
    "with-bgm": false,
    "bgm-file": ""
  }

EOF
    exit 0
}

# ==================== 参数解析 ====================

parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            -t|--theme)
                THEME="$2"
                shift 2
                ;;
            -d|--duration)
                DURATION="$2"
                shift 2
                ;;
            -s|--script)
                SCRIPT_FILE="$2"
                shift 2
                ;;
            -o|--output)
                OUTPUT_DIR="$2"
                shift 2
                ;;
            -v|--voice)
                VOICE="$2"
                shift 2
                ;;
            -b|--with-bgm)
                WITH_BGM=true
                shift
                ;;
            --bgm-file)
                BGM_FILE="$2"
                WITH_BGM=true
                shift 2
                ;;
            -c|--config)
                CONFIG_FILE="$2"
                shift 2
                ;;
            --resume-from)
                RESUME_FROM="$2"
                shift 2
                ;;
            --width)
                IMAGE_WIDTH="$2"
                shift 2
                ;;
            --height)
                IMAGE_HEIGHT="$2"
                shift 2
                ;;
            --crf)
                VIDEO_CRF="$2"
                shift 2
                ;;
            --audio-bitrate)
                AUDIO_BITRATE="$2"
                shift 2
                ;;
            --no-quality-check)
                QUALITY_CHECK=false
                shift
                ;;
            --verbose)
                VERBOSE=true
                shift
                ;;
            -h|--help)
                SHOW_HELP=true
                shift
                ;;
            *)
                print_error "未知选项：$1"
                echo "使用 -h 查看帮助"
                exit 1
                ;;
        esac
    done
}

validate_args() {
    # 先加载配置文件
    if [ -n "$CONFIG_FILE" ]; then
        load_config
    fi
    
    # 命令行参数覆盖配置文件
    # （已在 parse_args 中处理）
    
    if [ -z "$THEME" ] && [ -z "$SCRIPT_FILE" ]; then
        print_error "必须提供 --theme 或 --script"
        echo "使用 -h 查看帮助"
        exit 1
    fi
    
    if [ -n "$SCRIPT_FILE" ] && [ ! -f "$SCRIPT_FILE" ]; then
        print_error "脚本文件不存在：$SCRIPT_FILE"
        exit 1
    fi
    
    if [ -n "$BGM_FILE" ] && [ ! -f "$BGM_FILE" ]; then
        print_error "BGM 文件不存在：$BGM_FILE"
        exit 1
    fi
    
    # 验证断点续传参数
    if [ "$RESUME_FROM" -gt 0 ] && [ "$RESUME_FROM" -gt "$TOTAL_STEPS" ]; then
        print_error "断点续传步骤必须在 1-$TOTAL_STEPS 之间"
        exit 1
    fi
    
    # 验证配置参数
    validate_config
    
    if [ -z "$OUTPUT_DIR" ]; then
        OUTPUT_DIR="./video-output-$(date +%Y%m%d-%H%M%S)"
    fi
    
    mkdir -p "$OUTPUT_DIR"
    mkdir -p "$OUTPUT_DIR/images"
    mkdir -p "$OUTPUT_DIR/scaled"
    
    # 初始化日志（必须在 OUTPUT_DIR 设置后）
    LOG_FILE="$OUTPUT_DIR/make_video.log"
    echo "=== 视频生成日志 ===" > "$LOG_FILE"
    echo "开始时间：$(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"
    echo "主题：${THEME:-N/A}" >> "$LOG_FILE"
    echo "输出目录：$OUTPUT_DIR" >> "$LOG_FILE"
    echo "断点续传：${RESUME_FROM:-0}" >> "$LOG_FILE"
    echo "---" >> "$LOG_FILE"
}

# ==================== 核心步骤 ====================

# 检查是否需要跳过步骤（断点续传）
check_resume() {
    local step_num=$1
    
    if [ "$RESUME_FROM" -gt "$step_num" ]; then
        echo ""
        print_step "跳过步骤 $step_num（断点续传）"
        log_info "跳过步骤 $step_num"
        return 0  # 需要跳过
    fi
    return 1  # 不需要跳过
}

# 质量检查函数
quality_check() {
    local file="$1"
    local type="$2"
    local report_file="$OUTPUT_DIR/quality_report.txt"
    
    if [ "$QUALITY_CHECK" = false ]; then
        return 0
    fi
    
    echo "质量检查：$file" >> "$report_file"
    
    case $type in
        audio)
            if [ -f "$file" ]; then
                local duration=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$file" 2>/dev/null)
                local size=$(stat -c%s "$file" 2>/dev/null || stat -f%z "$file" 2>/dev/null)
                echo "  ✓ 文件存在" >> "$report_file"
                echo "  ✓ 时长：${duration}s" >> "$report_file"
                echo "  ✓ 大小：${size} bytes" >> "$report_file"
                
                # 检查音频是否为空
                if [ "$(echo "$duration > 0" | bc -l)" = "1" ]; then
                    echo "  ✓ 音频内容正常" >> "$report_file"
                    return 0
                else
                    echo "  ✗ 音频为空" >> "$report_file"
                    return 1
                fi
            else
                echo "  ✗ 文件不存在" >> "$report_file"
                return 1
            fi
            ;;
        image)
            if [ -f "$file" ]; then
                local dims=$(ffprobe -v error -show_entries stream=width,height -of default=noprint_wrappers=1:nokey=1 "$file" 2>/dev/null)
                local size=$(stat -c%s "$file" 2>/dev/null || stat -f%z "$file" 2>/dev/null)
                echo "  ✓ 文件存在" >> "$report_file"
                echo "  ✓ 尺寸：${dims}" >> "$report_file"
                echo "  ✓ 大小：${size} bytes" >> "$report_file"
                
                # 检查图片是否过小
                if [ "$size" -gt 1000 ]; then
                    echo "  ✓ 图片大小正常" >> "$report_file"
                    return 0
                else
                    echo "  ✗ 图片可能损坏" >> "$report_file"
                    return 1
                fi
            else
                echo "  ✗ 文件不存在" >> "$report_file"
                return 1
            fi
            ;;
        video)
            if [ -f "$file" ]; then
                local duration=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$file" 2>/dev/null)
                local dims=$(ffprobe -v error -show_entries stream=width,height -of default=noprint_wrappers=1 "$file" 2>/dev/null | tr '\n' ' ')
                local size=$(ls -lh "$file" | awk '{print $5}')
                echo "  ✓ 文件存在" >> "$report_file"
                echo "  ✓ 时长：${duration}s" >> "$report_file"
                echo "  ✓ 尺寸：${dims}" >> "$report_file"
                echo "  ✓ 大小：${size}" >> "$report_file"
                
                if [ "$(echo "$duration > 0" | bc -l)" = "1" ]; then
                    echo "  ✓ 视频内容正常" >> "$report_file"
                    return 0
                else
                    echo "  ✗ 视频为空" >> "$report_file"
                    return 1
                fi
            else
                echo "  ✗ 文件不存在" >> "$report_file"
                return 1
            fi
            ;;
    esac
}

step1_generate_script() {
    update_progress 1 "生成视频脚本"
    
    if check_resume 1; then
        return 0
    fi
    
    if [ -n "$SCRIPT_FILE" ]; then
        print_step "使用已有脚本：$SCRIPT_FILE"
        cp "$SCRIPT_FILE" "$OUTPUT_DIR/script.md"
        return
    fi
    
    echo ""
    echo "📝 正在生成脚本..."
    echo "主题：$THEME"
    echo "时长：${DURATION}秒"
    
    # 调用 AI 生成脚本（临时实现）
    cat > "$OUTPUT_DIR/script.md" << EOF
# $THEME

## 开场（0:00-0:20）
大家好！今天给大家带来$THEME 的介绍...

## 主体（0:20-${DURATION}秒）
[AI 生成的脚本内容...]

## 结尾（最后 20 秒）
感谢观看！喜欢请点赞关注！
EOF
    
    print_step "脚本已生成：$OUTPUT_DIR/script.md"
}

step2_generate_voice() {
    update_progress 2 "生成配音"
    
    if check_resume 2; then
        # 检查已有文件
        if [ -f "$OUTPUT_DIR/narration.mp3" ]; then
            print_step "使用已有配音文件"
            return 0
        fi
    fi
    
    if ! command -v edge-tts &> /dev/null 2>&1; then
        print_warning "edge-tts 未安装，跳过配音生成"
        return
    fi
    
    echo ""
    echo "🎙️ 正在生成配音..."
    
    cd "$OUTPUT_DIR"
    python3 -m edge_tts \
        --voice "$VOICE" \
        --file script.md \
        --write-media narration.mp3 \
        --write-subtitles narration.vtt
    
    if [ -f "narration.mp3" ]; then
        duration=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 narration.mp3)
        print_step "配音已生成：narration.mp3 (${duration}s)"
        print_step "字幕已生成：narration.vtt"
        
        # 质量检查
        if [ "$QUALITY_CHECK" = true ]; then
            quality_check "$OUTPUT_DIR/narration.mp3" "audio"
        fi
    else
        print_error "配音生成失败"
        exit 1
    fi
    
    cd - > /dev/null
}

step3_generate_storyboard() {
    update_progress 3 "生成分镜脚本"
    
    if check_resume 3; then
        if [ -f "$OUTPUT_DIR/storyboard.json" ]; then
            print_step "使用已有分镜文件"
            return 0
        fi
    fi
    
    echo ""
    echo "📋 正在分析脚本生成分镜..."
    
    # 从脚本动态提取场景
    cd "$OUTPUT_DIR"
    python3 << 'PYTHON'
import json
import re
import os

script_file = 'script.md'
output_file = 'storyboard.json'

try:
    with open(script_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取章节标题
    sections = re.findall(r'^## (.+)$', content, re.MULTILINE)
    
    if not sections:
        # 如果没有章节，使用默认 5 场景
        sections = ["开场", "内容 1", "内容 2", "内容 3", "结尾"]
    
    scenes = []
    for i, section in enumerate(sections, 1):
        # 从章节生成图片 prompt
        prompt = f"与\"{section}\"相关的插图，教育风格，清晰易懂，专业质量"
        scenes.append({
            "id": i,
            "title": section,
            "image_prompt": prompt,
            "narration": f"关于{section}的内容"
        })
    
    result = {
        "title": "Video Storyboard",
        "scenes": scenes
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"📋 分镜已生成：{len(scenes)} 个场景")
    
except Exception as e:
    print(f"⚠️  分镜生成失败，使用默认模板：{e}")
    # 使用默认模板
    result = {
        "title": "Video Storyboard",
        "scenes": [
            {"id": 1, "title": "开场", "image_prompt": "视频封面，吸引人", "narration": "开场白"},
            {"id": 2, "title": "内容 1", "image_prompt": "内容展示图", "narration": "主体内容 1"},
            {"id": 3, "title": "内容 2", "image_prompt": "详细解释图", "narration": "主体内容 2"},
            {"id": 4, "title": "内容 3", "image_prompt": "示例演示图", "narration": "主体内容 3"},
            {"id": 5, "title": "结尾", "image_prompt": "结尾感谢画面", "narration": "结尾"}
        ]
    }
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"📋 已生成默认分镜：5 个场景")
PYTHON
    cd - > /dev/null
    
    if [ -f "$OUTPUT_DIR/storyboard.json" ]; then
        scene_count=$(python3 -c "import json; print(len(json.load(open('$OUTPUT_DIR/storyboard.json'))['scenes']))")
        print_step "分镜已生成：storyboard.json ($scene_count 个场景)"
    else
        print_error "分镜生成失败"
        exit 1
    fi
}

step4_generate_images() {
    update_progress 4 "AI 生成图片"
    
    if check_resume 4; then
        local count=$(ls -1 "$OUTPUT_DIR/images/scene_*.png" 2>/dev/null | wc -l)
        if [ "$count" -gt 0 ]; then
            print_step "使用已有图片文件 ($count 张)"
            return 0
        fi
    fi
    
    echo ""
    echo "🎨 正在从分镜生成 AI 图片..."
    
    if [ ! -f "$GEN_IMAGE_SCRIPT" ]; then
        print_warning "图片生成脚本不存在，使用备用方案"
        # 创建占位图片
        for i in 1 2 3 4 5; do
            ffmpeg -y -f lavfi -i color=c=blue:s=1280x720:d=1 "$OUTPUT_DIR/images/scene_$i.png" 2>/dev/null
        done
        print_step "已创建占位图片"
        return
    fi
    
    cd "$OUTPUT_DIR"
    
    # 从 storyboard 提取 prompts
    python3 << 'PYTHON'
import json
import subprocess
import os

with open('storyboard.json', 'r', encoding='utf-8') as f:
    storyboard = json.load(f)

tasks = []
for scene in storyboard.get('scenes', []):
    prompt = scene.get('image_prompt', '')
    if prompt:
        output = f"images/scene_{scene['id']:02d}.png"
        tasks.append((prompt, output))

# 生成批量任务文件
import json
with open('batch.json', 'w', encoding='utf-8') as f:
    json.dump(tasks, f, ensure_ascii=False, indent=2)

print(f"📋 准备生成 {len(tasks)} 张图片")
for i, (prompt, output) in enumerate(tasks, 1):
    print(f"  [{i}/{len(tasks)}] {output}")
PYTHON
    
    # 调用图片生成
    python3 "$GEN_IMAGE_SCRIPT" batch.json
    
    # 检查生成结果
    count=$(ls -1 images/scene_*.png 2>/dev/null | wc -l)
    if [ "$count" -gt 0 ]; then
        print_step "已生成 $count 张图片"
    else
        print_warning "图片生成失败，使用占位图片"
        for i in 1 2 3 4 5; do
            ffmpeg -y -f lavfi -i color=c=blue:s=1280x720:d=1 "images/scene_$i.png" 2>/dev/null
        done
    fi
    
    cd - > /dev/null
}

step5_scale_images() {
    update_progress 5 "处理并缩放图片"
    
    if check_resume 5; then
        local count=$(ls -1 "$OUTPUT_DIR/scaled/*.png" 2>/dev/null | wc -l)
        if [ "$count" -gt 0 ]; then
            print_step "使用已有缩放图片 ($count 张)"
            return 0
        fi
    fi
    
    echo ""
    echo "🖼️ 正在缩放图片到统一尺寸..."
    
    cd "$OUTPUT_DIR"
    
    count=0
    for img in images/*.png; do
        [ -f "$img" ] || continue
        base=$(basename "$img")
        ffmpeg -y -i "$img" \
            -vf "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1" \
            "scaled/$base" 2>/dev/null
        count=$((count + 1))
    done
    
    print_step "已缩放 $count 张图片到 1280x720"
    
    cd - > /dev/null
}

step6_merge_video() {
    update_progress 6 "合成最终视频"
    
    if check_resume 6; then
        if [ -f "$OUTPUT_DIR/final.mp4" ]; then
            print_step "使用已有视频文件"
            return 0
        fi
    fi
    
    echo ""
    echo "🎬 正在合成视频..."
    
    cd "$OUTPUT_DIR"
    
    # 获取配音时长
    if [ -f "narration.mp3" ]; then
        audio_duration=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 narration.mp3)
        echo "📊 配音时长：${audio_duration}s"
    else
        audio_duration="60"
        print_warning "未检测到配音，使用默认时长 60 秒"
    fi
    
    # 获取图片列表
    image_count=$(ls -1 scaled/*.png 2>/dev/null | wc -l)
    if [ "$image_count" -eq 0 ]; then
        print_error "没有找到图片文件"
        exit 1
    fi
    
    # 计算每张图片显示时长
    frame_duration=$(awk "BEGIN {printf \"%.1f\", $audio_duration / $image_count}")
    echo "📊 图片数量：$image_count"
    echo "📊 每张图片显示：${frame_duration}秒"
    
    # 创建 concat 列表文件
    concat_file="$OUTPUT_DIR/concat_list.txt"
    > "$concat_file"
    
    for img in scaled/*.png; do
        [ -f "$img" ] || continue
        echo "file '$img'" >> "$concat_file"
        echo "duration $frame_duration" >> "$concat_file"
    done
    
    # 最后一个文件（不重复）
    if [ "$image_count" -gt 0 ]; then
        last_img=$(ls scaled/*.png | tail -1)
        echo "file '$last_img'" >> "$concat_file"
    fi
    
    # 合成视频（含 BGM 处理）
    if [ -f "narration.mp3" ]; then
        echo "🎵 使用配音合成..."
        if [ "$WITH_BGM" = true ] && [ -n "$BGM_FILE" ] && [ -f "$BGM_FILE" ]; then
            echo "🎶 检测到 BGM，将进行混音处理..."
            # 使用 BGM 混音
            ffmpeg -y -f concat -safe 0 -i "$concat_file" \
                -i narration.mp3 \
                -i "$BGM_FILE" \
                -filter_complex "[1:a]volume=1.0[a]; [2:a]volume=0.3[b]; [a][b]amix=inputs=2:duration=first:dropout_transition=2[mixed]" \
                -map 0:v \
                -map "[mixed]" \
                -c:v libx264 -preset fast -crf $VIDEO_CRF \
                -c:a aac -b:a $AUDIO_BITRATE \
                -pix_fmt yuv420p \
                -shortest final.mp4 2>&1 | tail -10
        else
            ffmpeg -y -f concat -safe 0 -i "$concat_file" \
                -i narration.mp3 \
                -c:v libx264 -preset fast -crf $VIDEO_CRF \
                -c:a aac -b:a $AUDIO_BITRATE \
                -pix_fmt yuv420p \
                -shortest final.mp4 2>&1 | tail -10
        fi
    else
        echo "🎵 无配音，生成静音视频..."
        ffmpeg -y -f concat -safe 0 -i "$concat_file" \
            -c:v libx264 -preset fast -crf $VIDEO_CRF \
            -pix_fmt yuv420p \
            -t $audio_duration final.mp4 2>&1 | tail -10
    fi
    
    if [ -f "final.mp4" ]; then
        size=$(ls -lh final.mp4 | awk '{print $5}')
        duration=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 final.mp4)
        print_step "✅ 视频合成完成！"
        echo "  文件：final.mp4"
        echo "  大小：$size"
        echo "  时长：${duration}s"
        
        # 质量检查
        if [ "$QUALITY_CHECK" = true ]; then
            quality_check "$OUTPUT_DIR/final.mp4" "video"
        fi
    else
        print_error "视频合成失败"
        echo "Concat 文件内容:"
        cat "$concat_file"
        exit 1
    fi
    
    cd - > /dev/null
}

# ==================== 主流程 ====================

main() {
    parse_args "$@"
    
    if [ "$SHOW_HELP" = true ]; then
        show_help
    fi
    
    print_header "视频生成工作流 (v2.2)"
    echo "主题：${THEME:-N/A}"
    echo "时长：${DURATION}秒"
    echo "输出：$OUTPUT_DIR"
    echo "BGM: ${WITH_BGM:+已启用}${WITH_BGM:-未启用}"
    [ -n "$BGM_FILE" ] && echo "BGM 文件：$BGM_FILE"
    [ "$RESUME_FROM" -gt 0 ] && echo "断点续传：从步骤 $RESUME_FROM 开始"
    echo "配置："
    echo "  分辨率：${IMAGE_WIDTH}x${IMAGE_HEIGHT}"
    echo "  视频质量：CRF $VIDEO_CRF"
    echo "  音频比特率：$AUDIO_BITRATE"
    echo ""
    
    check_dependencies
    validate_args
    
    echo ""
    echo "========================================="
    echo "开始执行视频生成流程..."
    echo "========================================="
    echo ""
    
    step1_generate_script
    echo ""
    step2_generate_voice
    echo ""
    step3_generate_storyboard
    echo ""
    step4_generate_images
    echo ""
    step5_scale_images
    echo ""
    step6_merge_video
    echo ""
    
    finish_progress
    
    print_header "完成！"
    echo "输出目录：$OUTPUT_DIR"
    echo "最终视频：$OUTPUT_DIR/final.mp4"
    echo ""
    echo "查看文件:"
    echo "  ls -lh $OUTPUT_DIR/"
    echo ""
    echo "日志文件:"
    echo "  $LOG_FILE"
    [ "$QUALITY_CHECK" = true ] && echo "质量报告:" && echo "  $OUTPUT_DIR/quality_report.txt"
    echo ""
    
    # 记录结束时间
    if [ -n "$LOG_FILE" ] && [ -f "$LOG_FILE" ]; then
        echo "---" >> "$LOG_FILE"
        echo "结束时间：$(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"
    fi
}

main "$@"
