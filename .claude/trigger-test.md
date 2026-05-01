# 触发词测试工具

> 用途：测试用户输入能否正确匹配到 skill  
> 使用方法：`./skills.sh test "<用户输入>"`

---

## 测试命令

```bash
# 测试单个输入
./skills.sh test "帮我复习中级会计"

# 测试多个输入
./skills.sh test-batch test-cases.md

# 检查同步状态
./skills.sh check-sync
```

---

## 测试用例格式

### 单条测试
```bash
./skills.sh test "<输入>" [--expect <预期 skill>]
```

### 批量测试 (test-cases.md)
```markdown
# 触发词测试用例

## 应该触发 (正向测试)
| 输入 | 预期 skill | 置信度 |
|------|------------|--------|
| 帮我复习 | exam-prep | ≥80% |
| 准备比赛 | competition-prep | ≥80% |
| 写论文 | research-paper-isolated | ≥80% |
| 分析数据 | data-analysis | ≥80% |

## 不应触发 (负向测试)
| 输入 | 预期结果 |
|------|----------|
| 不想写论文 | 不触发 |
| 今天好累 | 不触发 |
| 学创杯是什么 | 不触发 (纯咨询) |

## 边界测试
| 输入 | 预期 skill | 置信度 |
|------|------------|--------|
| 了解一下比赛 | competition-prep | 50-60% |
| 数据作业 | data-analysis | 60-70% |
```

---

## 同步检查

### 检查项目

```bash
./skills.sh check-sync
```

检查内容：
1. ✅ CLAUDE.md 核心触发词是否都在 skills-trigger-map.md 中
2. ✅ skills-trigger-map.md 新增触发词是否已同步到 CLAUDE.md（高频词）
3. ✅ 版本号是否一致
4. ✅ 最后更新日期是否更新

### 同步失败示例

```
❌ 同步检查失败

问题 1: skills-trigger-map.md 新增触发词"考前冲刺"未在 CLAUDE.md 中
建议：添加到 exam-prep 核心触发词

问题 2: CLAUDE.md 版本号 v1.1，skills-trigger-map.md 版本号 v1.0
建议：统一更新为 v1.2
```

---

## 调试模式

### 启用调试日志

```bash
export SKILL_DEBUG=1
./skills.sh test "帮我复习"
```

### 调试输出

```
[DEBUG] 用户输入：帮我复习
[DEBUG] 匹配核心触发词：复习 → exam-prep
[DEBUG] 置信度：95%
[DEBUG] 决策：直接触发
[DEBUG] 加载 skill：skills/exam-prep-workflow/SKILL.md
[DEBUG] 执行工作流：exam-prep-workflow
```

---

## 常见问题

### Q1: 触发失败怎么办？

```bash
# 1. 检查是否命中否定词
./skills.sh test "不想复习" --debug

# 2. 检查置信度
./skills.sh test "了解一下考试" --debug

# 3. 检查完整映射表
grep -A5 "exam-prep" skills-trigger-map.md
```

### Q2: 如何添加新触发词？

```bash
# 1. 添加到 CLAUDE.md（高频词）
# 2. 添加到 skills-trigger-map.md（完整列表）
# 3. 更新版本号
# 4. 运行同步检查
./skills.sh check-sync

# 5. 测试新触发词
./skills.sh test "新触发词" --expect exam-prep
```

### Q3: 如何判断触发词是否高频？

```
高频触发词标准（满足任一）：
- 日均使用 ≥10 次
- 周均使用 ≥50 次
- 月均使用 ≥200 次

低频触发词：
- 保留在 skills-trigger-map.md
- 不添加到 CLAUDE.md（节省常驻 Token）
```

---

## 版本历史

| 版本 | 日期 | 变更内容 |
|------|------|----------|
| v1.0 | 2026-05-01 | 初始版本，创建测试工具文档 |
