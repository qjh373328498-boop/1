#!/bin/bash
# 🎵 背景音乐生成脚本 (v1.0)
# 
# 用法:
#   ./gen_music.sh --prompt "提示词" --duration 60
#   ./gen_music.sh --batch tasks.json
#   ./gen_music.sh --method suno|musicgen|library
#   ./gen_music.sh -h  # 显示帮助

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="./music-output"
PROMPT=""
DURATION=60
STYLE="instrumental"
METHOD="suno"
BATCH_FILE=""
SHOW_HELP=false
SUNO_API_KEY="${SUNO_API_KEY:-}"
SUNO_BASE_URL="https://api.suno.ai/v1"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_header() {
    echo -e "${BLUE}=========================================${NC}"
    echo -e "${BLUE}  🎵 $1${NC}"
    echo -e "${BLUE}=========================================${NC}"
}

print_step() {
    echo -e "${GREEN}[✓] $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

show_help() {
    cat << 'HELP'
🎵 背景音乐生成脚本 (v1.0)

用法:
  ./gen_music.sh --prompt "提示词" --duration 60
  ./gen_music.sh --batch tasks.json
  ./gen_music.sh --method suno|musicgen|library

选项:
  -p, --prompt TEXT     音乐提示词
  -d, --duration NUM    时长（秒，默认：60）
  -s, --style TEXT      音乐风格（默认：instrumental）
  -m, --method METHOD   suno/musicgen/library (默认：suno)
  -o, --output DIR      输出目录
      --batch FILE      批量任务 JSON 文件
      --api-key KEY     Suno API Key
  -h, --help            显示帮助

示例:
  ./gen_music.sh --prompt "light corporate background" --duration 60
  ./gen_music.sh --batch music-tasks.json --method suno
  ./gen_music.sh --prompt "piano music" --method musicgen
HELP
    exit 0
}

parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            -p|--prompt)
                PROMPT="$2"
                shift 2
                ;;
            -d|--duration)
                DURATION="$2"
                shift 2
                ;;
            -s|--style)
                STYLE="$2"
                shift 2
                ;;
            -m|--method)
                METHOD="$2"
                shift 2
                ;;
            -o|--output)
                OUTPUT_DIR="$2"
                shift 2
                ;;
            --batch)
                BATCH_FILE="$2"
                shift 2
                ;;
            --api-key)
                SUNO_API_KEY="$2"
                shift 2
                ;;
            -h|--help)
                SHOW_HELP=true
                shift
                ;;
            *)
                print_error "未知选项：$1"
                exit 1
                ;;
        esac
    done
}

validate_args() {
    if [ -z "$BATCH_FILE" ] && [ -z "$PROMPT" ]; then
        print_error "必须提供 --prompt 或 --batch"
        exit 1
    fi
    mkdir -p "$OUTPUT_DIR"
}

generate_with_suno() {
    local prompt="$1"
    local duration="$2"
    local output="$3"
    
    print_step "使用 Suno AI 生成..."
    echo "提示词：$prompt | 时长：${duration}s"
    
    if [ -z "$SUNO_API_KEY" ]; then
        print_warning "未提供 SUNO_API_KEY，使用占位音频"
        ffmpeg -y -f lavfi -i "sine=frequency=440:duration=$duration" -c:a libmp3lame "$output" 2>/dev/null
        print_step "已生成占位音频 (请配置 SUNO_API_KEY 使用真实 API)"
        return 0
    fi
    
    # Suno API 调用
    local response=$(curl -s -X POST "$SUNO_BASE_URL/generate" \
        -H "Authorization: Bearer $SUNO_API_KEY" \
        -H "Content-Type: application/json" \
        -d "{\"prompt\": \"$prompt\", \"style\": \"$STYLE\", \"duration\": $duration}")
    
    local task_id=$(echo "$response" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('id',''))" 2>/dev/null)
    
    if [ -z "$task_id" ]; then
        print_error "Suno API 调用失败"
        return 1
    fi
    
    print_step "任务 ID: $task_id"
    
    # 轮询状态
    for i in $(seq 1 24); do
        sleep 5
        local status=$(curl -s "$SUNO_BASE_URL/status/$task_id" \
            -H "Authorization: Bearer $SUNO_API_KEY" | \
            python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('status',''))" 2>/dev/null)
        
        if [ "$status" = "complete" ]; then
            local audio_url=$(curl -s "$SUNO_BASE_URL/status/$task_id" \
                -H "Authorization: Bearer $SUNO_API_KEY" | \
                python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('audio_url',''))" 2>/dev/null)
            
            if [ -n "$audio_url" ]; then
                curl -s "$audio_url" -o "$output"
                print_step "音乐已生成：$output"
                return 0
            fi
        elif [ "$status" = "failed" ]; then
            print_error "音乐生成失败"
            return 1
        fi
        echo -ne "\r等待生成... ${i}s"
    done
    
    print_error "等待超时"
    return 1
}

generate_with_musicgen() {
    local prompt="$1"
    local duration="$2"
    local output="$3"
    
    print_step "使用 MusicGen 本地生成..."
    
    if ! python3 -c "import audiocraft" 2>/dev/null; then
        print_warning "未安装 audiocraft"
        echo "请运行：pip3 install --break-system-packages audiocraft"
        return 1
    fi
    
    python3 << PYTHON
from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write

model = MusicGen.get_pretrained('small')
model.set_generation_params(duration=$duration)

descriptions = ["$prompt"]
wav = model.generate(descriptions)

for idx, one_wav in enumerate(wav):
    audio_write("$output".replace('.mp3', ''), one_wav.cpu(), model.sample_rate, strategy="loudness")

print("✅ 音乐已生成")
PYTHON
    
    if [ -f "${output%.mp3}.wav" ]; then
        mv "${output%.mp3}.wav" "$output" 2>/dev/null || true
        print_step "音乐已生成：$output"
        return 0
    fi
    
    print_error "MusicGen 生成失败"
    return 1
}

select_from_library() {
    local prompt="$1"
    local output="$2"
    
    print_step "推荐免版权音乐库:"
    cat << 'LIBS'

1. YouTube Audio Library
   https://www.youtube.com/audiolibrary

2. FreePD
   https://freepd.com/

3. Bensound
   https://www.bensound.com/

4. NCS (No Copyright Sounds)
   https://ncs.io/

5. Pixabay Music
   https://pixabay.com/music/

LIBS
    print_warning "请手动从以上网站下载音乐"
    return 0
}

process_batch() {
    local batch_file="$1"
    
    if [ ! -f "$batch_file" ]; then
        print_error "批量任务文件不存在：$batch_file"
        exit 1
    fi
    
    print_header "批量音乐生成"
    echo "任务文件：$batch_file"
    
    mapfile -t tasks < <(python3 -c "
import json
with open('$batch_file', 'r', encoding='utf-8') as f:
    data = json.load(f)
for i, task in enumerate(data):
    prompt = task.get('prompt', '')
    duration = task.get('duration', 60)
    style = task.get('style', 'instrumental')
    print(f'{i}|{prompt}|{duration}|{style}')
")
    
    local total=${#tasks[@]}
    local success=0
    local failed=0
    
    echo "共 $total 个任务"
    echo ""
    
    for task_line in "${tasks[@]}"; do
        IFS='|' read -r idx prompt duration style <<< "$task_line"
        
        print_header "任务 $((idx+1))/$total"
        echo "提示词：$prompt"
        echo "时长：${duration}s | 风格：$style"
        
        local output="$OUTPUT_DIR/music_$(printf '%03d' $((idx+1))).mp3"
        
        if generate_music "$prompt" "$duration" "$style" "$output"; then
            success=$((success + 1))
        else
            failed=$((failed + 1))
        fi
        echo ""
    done
    
    print_header "批量任务完成"
    echo "成功：$success / $total"
    [ $failed -gt 0 ] && echo "失败：$failed"
    
    [ $failed -gt 0 ] && return 1
    return 0
}

generate_music() {
    local prompt="$1"
    local duration="$2"
    local style="$3"
    local output="$4"
    
    case $METHOD in
        suno)
            generate_with_suno "$prompt" "$duration" "$output"
            ;;
        musicgen)
            generate_with_musicgen "$prompt" "$duration" "$output"
            ;;
        library)
            select_from_library "$prompt" "$output"
            ;;
        *)
            print_error "未知方法：$METHOD"
            return 1
            ;;
    esac
}

main() {
    parse_args "$@"
    
    [ "$SHOW_HELP" = true ] && show_help
    
    print_header "背景音乐生成"
    echo "方法：$METHOD | 输出：$OUTPUT_DIR"
    echo ""
    
    validate_args
    
    if [ -n "$BATCH_FILE" ]; then
        process_batch "$BATCH_FILE"
        exit $?
    fi
    
    local output="$OUTPUT_DIR/music_$(date +%H%M%S).mp3"
    
    print_header "生成背景音乐"
    echo "提示词：$PROMPT"
    echo "时长：${DURATION}s | 风格：$STYLE"
    echo "输出：$output"
    echo ""
    
    if generate_music "$PROMPT" "$DURATION" "$STYLE" "$output"; then
        print_header "完成！"
        echo "音乐文件：$output"
        [ -f "$output" ] && ls -lh "$output"
    else
        print_error "音乐生成失败"
        exit 1
    fi
}

main "$@"
