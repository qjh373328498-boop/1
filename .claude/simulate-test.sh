#!/bin/bash

# 方案 D 意图识别模拟测试脚本
# 使用方法：./simulate-test.sh "<用户输入>"

USER_INPUT="$1"
echo "================================"
echo "测试输入：$USER_INPUT"
echo "================================"

# 定义否定词
NEGATIVE_WORDS="不想|不要|不需要|别|甭|没有|还没|尚未|怎么不|为什么不|何必"

# 定义强意图词
STRONG_INTENT="帮我|我要|需要|怎么做|准备"

# 定义弱意图词
WEAK_INTENT="了解一下|看看|问一下|是什么"

# 检查否定词
if echo "$USER_INPUT" | grep -qE "$NEGATIVE_WORDS"; then
    echo "❌ 检测到否定词 → 不触发任何 skill"
    echo "置信度：0%"
    exit 0
fi

# 定义 skill 关键词
declare -A SKILL_KEYWORDS
SKILL_KEYWORDS["exam-prep"]="复习 | 备考 | 考试 | 背题 | 划重点|中级会计 | 财务管理 | 审计"
SKILL_KEYWORDS["competition-prep"]="比赛 | 竞赛 | 备赛 | 学创杯 | 挑战杯 | 商业计划书 | 路演 PPT"
SKILL_KEYWORDS["research-paper"]="论文 | 研究报告 | 文献综述 | 写报告"
SKILL_KEYWORDS["data-analysis"]="分析 | 数据|Excel|图表 | 可视化"
SKILL_KEYWORDS["weekly-planning"]="计划 | 日程 | 周计划 | 时间管理 | 周回顾"
SKILL_KEYWORDS["knowledge-manage"]="整理 | 资料 | 批量处理 | 建立索引"
SKILL_KEYWORDS["feature-design"]="需求 | 设计 | 功能 | 规格 | feature"
SKILL_KEYWORDS["literature-search"]="文献 | 查找 | 找论文 | 引用格式"

# 匹配 skill
echo ""
echo "匹配结果:"

for skill in "${!SKILL_KEYWORDS[@]}"; do
    if echo "$USER_INPUT" | grep -qE "${SKILL_KEYWORDS[$skill]}"; then
        echo "  ✓ 匹配到：$skill"
    fi
done

# 检查意图强度
echo ""
echo "意图强度:"
if echo "$USER_INPUT" | grep -qE "$STRONG_INTENT"; then
    echo "  强意图 (×1.0)"
elif echo "$USER_INPUT" | grep -qE "$WEAK_INTENT"; then
    echo "  弱意图 (×0.6)"
else
    echo "  中性 (×1.0)"
fi

echo ""
echo "================================"
