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

# 命令 6: 触发论文写作工作流（隔离模式 - 默认）
do_paper_workflow() {
    local input="$1"
    
    if [ -z "$input" ]; then
        print_warning "Usage: $0 paper <PDF 文件/URL>"
        print_info "示例：$0 paper 知识库/论文.pdf"
        print_info ""
        print_info "⚠️ 注意：默认使用隔离模式（不参考知识库）"
        print_info "如需参考知识库，请使用：$0 paper-kb <主题>"
        exit 1
    fi
    
    print_info "Starting research paper workflow (ISOLATED mode) for: $input"
    print_info "⚠️ 隔离模式：不参考本地知识库，确保学术诚信"
    print_info "This will: extract content → translate → format → generate diagrams"
    print_info "Please use the skill: /research-paper-workflow-isolated $input"
}

# 命令 7: 触发论文写作工作流（知识库模式 - 需用户明确授权）
do_paper_workflow_with_kb() {
    local input="$1"
    
    if [ -z "$input" ]; then
        print_warning "Usage: $0 paper-kb <主题>"
        print_info "示例：$0 paper-kb 环境会计研究"
        print_info ""
        print_info "⚠️ 注意：此模式会参考知识库中的个人资料"
        print_info "适用于：课程作业、学习整理、比赛报告"
        print_info "不适用于：正式学术论文（请用 paper 命令）"
        exit 1
    fi
    
    print_info "Starting research paper workflow (WITH KNOWLEDGE BASE) for: $input"
    print_info "✅ 知识库模式：可参考个人学习笔记、比赛资料等"
    print_info "This will: scan knowledge base → extract → translate → format"
    print_info "Please use the skill: /research-paper-workflow-with-kb $input"
}

# 命令 8: 触发知识管理工作流
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

# 命令 9: 触发需求设计工作流
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

# 命令 10: 触发考试复习工作流
do_exam_prep() {
    local subject="$1"
    local exam_date="$2"
    
    if [ -z "$subject" ]; then
        print_warning "Usage: $0 exam <科目名> [考试日期]"
        print_info "示例：$0 exam 中级财务会计 2026-06-15"
        exit 1
    fi
    
    print_info "Starting exam preparation workflow for: $subject"
    if [ -n "$exam_date" ]; then
        print_info "Exam date: $exam_date"
    fi
    print_info "This will: extract knowledge points → mindmap → flashcards → study plan"
    print_info "Please use the skill: /exam-prep-workflow $subject"
}

# 命令 11: 触发比赛备赛工作流
do_competition_prep() {
    local competition="$1"
    local deadline="$2"
    
    if [ -z "$competition" ]; then
        print_warning "Usage: $0 competition <比赛名> [截止日期]"
        print_info "示例：$0 competition 学创杯 2026-07-15"
        exit 1
    fi
    
    print_info "Starting competition preparation workflow for: $competition"
    if [ -n "$deadline" ]; then
        print_info "Deadline: $deadline"
    fi
    print_info "This will: rules → plan → materials → PPT → Q&A"
    print_info "Please use the skill: /competition-prep-workflow $competition"
}

# 命令 12: 触发文献检索工作流
do_literature_search() {
    local topic="$1"
    local style="$2"
    
    if [ -z "$topic" ]; then
        print_warning "Usage: $0 literature <研究主题> [引用格式]"
        print_info "示例：$0 literature 环境会计 APA"
        print_info "支持的引用格式：GB/T 7714, APA, MLA, Chicago"
        exit 1
    fi
    
    print_info "Starting literature search workflow for: $topic"
    if [ -n "$style" ]; then
        print_info "Citation style: $style"
    fi
    print_info "This will: search → manage → note → cite → review"
    print_info "Please use the skill: /literature-search-workflow $topic"
}

# 命令 13: 显示所有可用工作流
do_workflows() {
    echo "Available Workflows:"
    echo "===================="
    echo ""
    echo "1. 学术研究/论文写作工作流（隔离模式 - 默认）"
    echo "   命令：$0 paper <PDF/URL>"
    echo "   技能：/research-paper-workflow-isolated"
    echo "   用途：处理 PDF、翻译、格式化、生成配图、导出 Word/PPT"
    echo "   特点：❌ 不参考知识库，确保学术诚信"
    echo "   适用：正式论文、学术竞赛"
    echo ""
    echo "2. 学术研究/论文写作工作流（知识库模式）"
    echo "   命令：$0 paper-kb <主题>"
    echo "   技能：/research-paper-workflow-with-kb"
    echo "   用途：同上，但可参考个人资料"
    echo "   特点：✅ 可参考个人笔记、比赛资料"
    echo "   适用：课程作业、学习整理、比赛报告"
    echo ""
    echo "3. 考试复习与备考工作流 ⭐ 新增"
    echo "   命令：$0 exam <科目名> [考试日期]"
    echo "   技能：/exam-prep-workflow"
    echo "   用途：知识点提取、思维导图、记忆卡片、复习计划"
    echo "   适用：期末考试、考证复习"
    echo ""
    echo "4. 比赛备赛工作流 ⭐ 新增"
    echo "   命令：$0 competition <比赛名> [截止日期]"
    echo "   技能：/competition-prep-workflow"
    echo "   用途：规则解读、备赛计划、商业计划书、PPT、答辩"
    echo "   适用：学创杯、挑战杯、国创赛等"
    echo ""
    echo "5. 学术文献检索与引用工作流 ⭐ 新增"
    echo "   命令：$0 literature <研究主题> [引用格式]"
    echo "   技能：/literature-search-workflow"
    echo "   用途：文献搜索、管理、笔记、引用生成、综述"
    echo "   支持：GB/T 7714, APA, MLA, Chicago 等格式"
    echo ""
    echo "6. 知识管理工作流"
    echo "   命令：$0 kb <文件/文件夹>"
    echo "   技能：/knowledge-manage-workflow"
    echo "   用途：批量处理文档、总结、分类、建立索引"
    echo ""
    echo "7. 需求分析工作流"
    echo "   命令：$0 feature <需求描述>"
    echo "   技能：/feature-design"
    echo "   用途：编写需求文档和技术设计（EARS 模式）"
    echo ""
    echo "8. 文件整理工作流"
    echo "   命令：$0 duplicates / $0 clean-dirs"
    echo "   用途：查找重复文件、清理空目录"
    echo ""
    echo "9. Git 同步工作流"
    echo "   命令：$0 sync"
    echo "   用途：git pull + push 同步到 GitHub"
    echo ""
    echo "10. 文档压缩工作流"
    echo "   命令：$0 compress <文件>"
    echo "   用途：压缩大文档节省 token"
    echo ""
    echo ""
    echo "📌 重要提示："
    echo "   - 写论文默认使用隔离模式（不参考知识库）"
    echo "   - 仅当明确说\"参考知识库\"时才使用知识库模式"
    echo "   - 这确保学术诚信，避免引用不可靠的个人资料"
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
    echo "  paper <PDF/URL>   启动论文写作工作流（隔离模式，默认）"
    echo "  paper-kb <主题>   启动论文写作工作流（知识库模式）"
    echo "  exam <科目>       启动考试复习工作流 ⭐"
    echo "  competition <比赛> 启动比赛备赛工作流 ⭐"
    echo "  literature <主题> 启动文献检索工作流 ⭐"
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
    paper-kb)
        do_paper_workflow_with_kb "$2"
        ;;
    exam)
        do_exam_prep "$2" "$3"
        ;;
    competition)
        do_competition_prep "$2" "$3"
        ;;
    literature)
        do_literature_search "$2" "$3"
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
