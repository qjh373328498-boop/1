#!/bin/bash
# 方案 D 安装脚本
# 使用方法：bash install.sh [target-directory]

set -e

TARGET_DIR="${1:-.}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "================================"
echo "方案 D 安装脚本"
echo "================================"
echo ""

# 检查目标目录
if [ ! -d "$TARGET_DIR" ]; then
    echo "❌ 错误：目标目录 '$TARGET_DIR' 不存在"
    exit 1
fi

# 检查是否已有配置
if [ -d "$TARGET_DIR/.claude" ]; then
    echo "⚠️  警告：$TARGET_DIR/.claude 已存在"
    read -p "是否覆盖？(y/N): " confirm
    if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
        echo "取消安装"
        exit 0
    fi
    echo "备份现有配置..."
    mv "$TARGET_DIR/.claude" "$TARGET_DIR/.claude.backup.$(date +%Y%m%d%H%M%S)"
fi

# 创建目录
echo "📁 创建配置目录..."
mkdir -p "$TARGET_DIR/.claude"

# 复制配置文件
echo "📋 复制核心配置 (~1MB)..."
cp "$SCRIPT_DIR/.claude/CLAUDE.md" "$TARGET_DIR/.claude/"
cp "$SCRIPT_DIR/.claude/skills-index.md" "$TARGET_DIR/.claude/"
cp "$SCRIPT_DIR/.claude/skills-trigger-map.md" "$TARGET_DIR/.claude/"
cp "$SCRIPT_DIR/.claude/skills-config.json" "$TARGET_DIR/.claude/"
cp -r "$SCRIPT_DIR/.claude/workflows" "$TARGET_DIR/.claude/"

# 可选：复制 skills 目录
echo ""
echo "📚 完整 skills 目录 (88 个，~50MB) 可选安装"
echo "   如果只需要 10 个核心技能，可以跳过此步骤"
read -p "是否复制完整的 skills 目录？(y/N): " copy_skills
if [ "$copy_skills" = "y" ] || [ "$copy_skills" = "Y" ]; then
    if [ -d "$SCRIPT_DIR/skills" ]; then
        echo "复制 skills 目录..."
        cp -r "$SCRIPT_DIR/skills" "$TARGET_DIR/"
        echo "✅ 已复制 skills/"
    else
        echo "⚠️  skills 目录不存在，跳过"
    fi
else
    echo "⊘ 跳过 skills 目录（可手动复制）"
fi

# 验证安装
echo ""
echo "✅ 验证安装..."
if [ -f "$TARGET_DIR/.claude/CLAUDE.md" ] && \
   [ -f "$TARGET_DIR/.claude/skills-index.md" ] && \
   [ -f "$TARGET_DIR/.claude/skills-trigger-map.md" ] && \
   [ -f "$TARGET_DIR/.claude/skills-config.json" ] && \
   [ -d "$TARGET_DIR/.claude/workflows" ]; then
    echo "✓ 所有核心文件已安装"
else
    echo "❌ 安装失败，请检查错误"
    exit 1
fi

# 显示摘要
echo ""
echo "================================"
echo "✅ 方案 D 安装完成！"
echo "================================"
echo ""
echo "安装位置：$TARGET_DIR/.claude/"
echo ""
echo "核心文件:"
ls -1 "$TARGET_DIR/.claude/" | sed 's/^/  /'
if [ "$copy_skills" = "y" ] || [ "$copy_skills" = "Y" ]; then
    echo "  skills/ (完整 88 个)"
fi
echo ""
echo "下一步:"
echo "1. 重启对话或重新加载配置"
echo "2. 测试触发：\"帮我复习\" 或 \"准备比赛\""
echo "3. 查看文档：cat $TARGET_DIR/.claude/CLAUDE.md"
echo ""
echo "Token 优化："
echo "  - 前：~20,000 tokens (88 skills 常驻)"
echo "  - 后：~1,700 tokens (按需加载)"
echo "  - 节省：92%+"
echo ""
