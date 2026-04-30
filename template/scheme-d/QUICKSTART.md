# 方案 D 快速开始指南

## 5 分钟快速配置

### 步骤 1：复制配置

```bash
cd your-project
cp -r /path/to/template/scheme-d/.claude .
```

### 步骤 2：验证安装

```bash
ls .claude/
# 应看到：
# - CLAUDE.md
# - skills-index.md
# - skills-trigger-map.md
# - skills-config.json
# - workflows/
```

### 步骤 3：测试触发

在对话中测试：

```
帮我复习
准备比赛
帮我写论文
分析一下这个数据
```

### 步骤 4：添加完整 Skills（可选）

```bash
# 如果需要完整的 88 个 skills
cp -r /path/to/template/scheme-d/skills .
```

---

## 常用命令

### 查看触发关键词

```bash
cat .claude/skills-trigger-map.md | grep "一级关键词" -A 50
```

### 添加自定义关键词

编辑 `.claude/skills-trigger-map.md`，添加你的关键词。

### 查看技能卡片

```bash
cat .claude/workflows/exam-prep.card
```

### 自定义置信度阈值

编辑 `.claude/skills-config.json`：

```json
{
  "threshold": {
    "direct_trigger": 80,
    "confirm_trigger": 60,
    "ask_confirm": 40
  }
}
```

---

## 故障排除

**问题**：skill 不触发  
**解决**：检查关键词是否在 `skills-trigger-map.md` 中

**问题**：Token 使用量高  
**解决**：检查是否复制了完整的 `skills/` 目录，应只保留必要的 skill

**问题**：置信度太低  
**解决**：调整 `skills-config.json` 中的阈值

---

## 下一步

1. 查看完整文档：`docs/方案 D_*.md`
2. 自定义关键词映射
3. 添加你自己的 skill
4. 分享你的配置

---

**开始时间**：< 5 分钟  
**Token 节省**：92%+
