#!/bin/bash

# Claude Skills 快速启动脚本
# 用于文件整理、Git 同步、文档压缩、工作流触发等高频场景

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 命令 1: 生成 commit 消息并提交
do_commit() {
    local message="$1"
    
    if [ -z "$message" ]; then
        # 自动生成 commit 消息
        local changes=$(git diff --cached --name-only 2>/dev/null | head -5)
        
        if echo "$changes" | grep -q "知识库"; then
            message="docs: 更新知识库文档"
        elif echo "$changes" | grep -q "作业"; then
            message="chore(作业): 更新作业文件"
        elif echo "$changes" | grep -q "比赛"; then
            message="chore(比赛): 更新比赛资料"
        else
            message="chore: 整理文件结构"
        fi
    fi
    
    print_info "Commit message: $message"
    git commit -m "$message"
    print_success "Commit successful!"
}

# 命令 2: Git 同步（pull + push）
do_sync() {
    print_info "Syncing with remote..."
    
    # 检查是否有远程分支
    if git remote -v | grep -q origin; then
        print_info "Pulling from remote..."
        git pull --rebase origin main
        
        print_info "Pushing to remote..."
        git push
        
        print_success "Sync complete!"
    else
        print_error "No remote repository configured"
        exit 1
    fi
}

# 命令 3: 压缩知识库文档
do_compress() {
    local file="$1"
    local script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/skills/caveman-compress" && pwd)"
    
    if [ -z "$file" ]; then
        print_warning "Usage: $0 compress <文件路径>"
        exit 1
    fi
    
    if [ ! -f "$file" ]; then
        print_error "File not found: $file"
        exit 1
    fi
    
    print_info "Compressing: $file"
    cd "$script_dir" && python3 -m scripts "$file"
    print_success "Compression complete!"
}

# 命令 4: 查找重复文件
do_find_duplicates() {
    print_info "Scanning for duplicate files..."
    
    # 查找带版本号的重复文件
    find . -type f \( -name "*([0-9])*" -o -name "*copy*" -o -name "*备份*" -o -name "*V2*" -o -name "*最终版*" \) \
        -not -path "*/.git/*" \
        -not -path "*/node_modules/*" \
        2>/dev/null | head -50
    
    print_success "Scan complete. Review the list above."
}

# 命令 5: 清理空目录
do_clean_empty_dirs() {
    print_info "Finding empty directories..."
    
    local empty_dirs=$(find . -type d -empty -not -path "*/.git/*" 2>/dev/null)
    
    if [ -n "$empty_dirs" ]; then
        echo "$empty_dirs"
        print_warning "Found empty directories. Delete them? (y/n)"
        read -r response
        if [[ "$response" =~ ^[Yy]$ ]]; then
            echo "$empty_dirs" | xargs rmdir 2>/dev/null
            print_success "Empty directories removed!"
        fi
    else
        print_success "No empty directories found."
    fi
}

# 命令 6: 触发论文写作工作流
do_paper_workflow() {
    local input="$1"
    
    if [ -z "$input" ]; then
        print_warning "Usage: $0 paper <PDF 文件/URL>"
        print_info "示例：$0 paper 知识库/论文.pdf"
        exit 1
    fi
    
    print_info "Starting research paper workflow for: $input"
    print_info "This will: extract content → translate → format → generate diagrams"
    print_info "Please use the skill: /research-paper-workflow $input"
}

# 命令 7: 触发知识管理工作流
do_kb_workflow() {
    local input="$1"
    
    if [ -z "$input" ]; then
        print_warning "Usage: $0 kb <文件/文件夹>"
        exit 1
    fi
    
    print_info "Starting knowledge management workflow for: $input"
    print_info "This will: process documents → summarize → organize → index"
    print_info "Please use the skill: /knowledge-manage-workflow $input"
}

# 命令 8: 触发需求设计工作流
do_feature_design() {
    local description="$*"
    
    if [ -z "$description" ]; then
        print_warning "Usage: $0 feature <需求描述>"
        print_info "示例：$0 feature 添加用户登录功能"
        exit 1
    fi
    
    print_info "Starting feature design workflow"
    print_info "Feature: $description"
    print_info "This will create requirements.md and design.md using EARS patterns"
    print_info "Please use the skill: /feature-design \"$description\""
}

# 命令 9: 显示所有可用工作流
do_workflows() {
    echo "Available Workflows:"
    echo "===================="
    echo ""
    echo "1. 学术研究/论文写作工作流"
    echo "   命令：$0 paper <PDF/URL>"
    echo "   技能：/research-paper-workflow"
    echo "   用途：处理 PDF、翻译、格式化、生成配图、导出 Word/PPT"
    echo ""
    echo "2. 知识管理工作流"
    echo "   命令：$0 kb <文件/文件夹>"
    echo "   技能：/knowledge-manage-workflow"
    echo "   用途：批量处理文档、总结、分类、建立索引"
    echo ""
    echo "3. 需求分析工作流"
    echo "   命令：$0 feature <需求描述>"
    echo "   技能：/feature-design"
    echo "   用途：编写需求文档和技术设计（EARS 模式）"
    echo ""
    echo "4. 文件整理工作流"
    echo "   命令：$0 duplicates / $0 clean-dirs"
    echo "   用途：查找重复文件、清理空目录"
    echo ""
    echo "5. Git 同步工作流"
    echo "   命令：$0 sync"
    echo "   用途：git pull + push 同步到 GitHub"
    echo ""
    echo "6. 文档压缩工作流"
    echo "   命令：$0 compress <文件>"
    echo "   用途：压缩大文档节省 token"
    echo ""
}

# 命令 10: 显示帮助
do_help() {
    echo "Claude Skills 快速启动脚本"
    echo ""
    echo "用法：$0 <命令> [参数]"
    echo ""
    echo "可用命令:"
    echo "  commit [消息]     生成 commit 消息并提交"
    echo "  sync              Git pull + push 同步"
    echo "  compress <文件>   压缩指定文档"
    echo "  duplicates        查找重复文件"
    echo "  clean-dirs        清理空目录"
    echo "  paper <PDF/URL>   启动论文写作工作流"
    echo "  kb <文件/文件夹>  启动知识管理工作流"
    echo "  feature <描述>    启动需求设计工作流"
    echo "  workflows         显示所有可用工作流"
    echo "  help              显示帮助"
    echo ""
    echo "示例:"
    echo "  $0 commit \"chore: 更新文档\""
    echo "  $0 sync"
    echo "  $0 compress 知识库/01-个人文档/个人学业档案索引.md"
    echo "  $0 duplicates"
    echo "  $0 paper 知识库/论文.pdf"
    echo "  $0 kb 知识库/02-学习资料/"
    echo "  $0 feature 添加用户登录功能"
    echo ""
}

# 主程序
case "$1" in
    commit)
        do_commit "$2"
        ;;
    sync)
        do_sync
        ;;
    compress)
        do_compress "$2"
        ;;
    duplicates)
        do_find_duplicates
        ;;
    clean-dirs)
        do_clean_empty_dirs
        ;;
    paper)
        do_paper_workflow "$2"
        ;;
    kb)
        do_kb_workflow "$2"
        ;;
    feature)
        shift
        do_feature_design "$*"
        ;;
    workflows)
        do_workflows
        ;;
    help|--help|-h|"")
        do_help
        ;;
    *)
        print_error "Unknown command: $1"
        echo "使用 '$0 help' 查看可用命令"
        exit 1
        ;;
esac
