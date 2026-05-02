#!/bin/bash
# ModelScope AI 图片生成快速测试
# 用法：./test_gen_image.sh

set -e

echo "=========================================="
echo "🎨 ModelScope AI 图片生成测试"
echo "=========================================="

# 创建测试目录
TEST_DIR="/tmp/modelscope-test"
mkdir -p "$TEST_DIR"
cd "$TEST_DIR"

echo "📂 测试目录：$TEST_DIR"
echo ""

# 测试 1：单张图片生成
echo "[测试 1] 单张图片生成..."
python3 /workspace/.claude/scripts/gen_image.py \
  "一只可爱的橘猫，蓝色眼睛，坐在彩虹上，卡通风格" \
  test_cat.png

if [ -f test_cat.png ]; then
  echo "✅ 单张测试通过"
  ls -lh test_cat.png
else
  echo "❌ 单张测试失败"
  exit 1
fi

echo ""

# 测试 2：批量生成
echo "[测试 2] 批量生成..."

cat > batch.json << 'EOF'
[
  ["德国心脏病桌游封面，鲜艳的草莓柠檬橙子香蕉，中间金属铃铛，卡通风格", "cover.png"],
  ["桌游配件展示，56 张卡牌散开，四种水果图案，金属抢答铃", "components.png"]
]
EOF

python3 /workspace/.claude/scripts/gen_image.py batch.json

# 检查结果
generated_count=$(ls -1 *.png 2>/dev/null | wc -l)
if [ "$generated_count" -ge 2 ]; then
  echo "✅ 批量测试通过"
  ls -lh *.png
else
  echo "❌ 批量测试失败 (仅生成 $generated_count 张)"
fi

echo ""
echo "=========================================="
echo "✅ 全部测试完成！"
echo "=========================================="
echo ""
echo "查看生成的图片:"
echo "  cd $TEST_DIR"
echo "  ls -lh *.png"
