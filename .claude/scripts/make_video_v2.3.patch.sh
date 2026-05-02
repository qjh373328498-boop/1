#!/bin/bash
# V2.3 升级补丁 - 批量任务 + 智能进度 + 错误恢复

PATCH_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_FILE="$PATCH_DIR/make_video.sh"

echo "🔧 应用 V2.3 补丁到 $TARGET_FILE"

# 1. 添加批量任务参数（在 AUDIO_BITRATE 后面）
sed -i '/^AUDIO_BITRATE=/a\
\
# 批量任务参数\
BATCH_MODE=false\
BATCH_FILE=""\
TASK_LIST=()\
TASK_INDEX=0\
TASK_TOTAL=0\
MAX_RETRIES=3\
RETRY_COUNT=0\
CONCURRENT_LIMIT=1\
ERROR_HANDLING="stop"' "$TARGET_FILE"

# 2. 添加 load_batch_tasks 函数（在 validate_config 后面）
cat >> "$TARGET_FILE" << 'INSERT_AFTER_VALIDATE_CONFIG'

# ==================== 批量任务功能 ====================

load_batch_tasks() {
    if [ -n "$BATCH_FILE" ] && [ -f "$BATCH_FILE" ]; then
        echo "📋 加载批量任务：$BATCH_FILE"
        
        mapfile -t TASK_LIST < <(python3 << PYTHON
import json

with open('$BATCH_FILE', 'r', encoding='utf-8') as f:
    tasks = json.load(f)

for i, task in enumerate(tasks):
    print(json.dumps(task, ensure_ascii=False))
PYTHON
)
        TASK_TOTAL=${#TASK_LIST[@]}
        echo "  共加载 $TASK_TOTAL 个任务"
    fi
}

# ==================== 智能进度预估 ====================

START_TIME=0

calc_eta() {
    local current=$1
    local total=$2
    local elapsed=$(($(date +%s) - START_TIME))
    
    if [ $current -gt 0 ]; then
        local avg_time=$((elapsed / current))
        local remaining=$((total - current))
        local eta=$((avg_time * remaining))
        local eta_min=$((eta / 60))
        local eta_sec=$((eta % 60))
        echo "⏱️  已用时：$((elapsed / 60))分$((elapsed % 60))秒 | 预计剩余：${eta_min}分${eta_sec}秒"
    fi
}

# ==================== 错误处理 ====================

handle_error() {
    local step_name="$1"
    local error_msg="$2"
    
    log_error "$step_name 失败：$error_msg"
    
    case $ERROR_HANDLING in
        stop)
            print_error "$step_name 失败，停止执行"
            exit 1
            ;;
        continue)
            print_warning "$step_name 失败，继续下一步"
            return 1
            ;;
        retry)
            if [ $RETRY_COUNT -lt $MAX_RETRIES ]; then
                RETRY_COUNT=$((RETRY_COUNT + 1))
                print_warning "$step_name 失败，重试 $RETRY_COUNT/$MAX_RETRIES"
                sleep 5
                return 2
            else
                print_error "$step_name 失败，已达最大重试次数 ($MAX_RETRIES)"
                exit 1
            fi
            ;;
    esac
}

INSERT_AFTER_VALIDATE_CONFIG

echo "✅ V2.3 补丁应用完成"
