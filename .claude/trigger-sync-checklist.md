# 触发词同步检查清单

> 每次修改触发词时必须执行

---

## 修改流程

### 添加新触发词

```
□ 1. 判断是否为高频词（日均≥10 次）
       ↓ 是
□ 2. 添加到 CLAUDE.md 核心触发词表
       ↓
□ 3. 添加到 skills-trigger-map.md 完整映射表
       ↓
□ 4. 更新 CLAUDE.md 版本号
       ↓
□ 5. 更新 skills-trigger-map.md 版本号
       ↓
□ 6. 运行同步检查：./skills.sh check-sync
       ↓
□ 7. 测试新触发词：./skills.sh test "新触发词"
       ↓
□ 8. 提交 Git（包含两个文件的变更）
```

### 删除触发词

```
□ 1. 检查触发词使用频率（近 30 天）
□ 2. 确认可以删除（使用频率=0 或有替代词）
□ 3. 从 CLAUDE.md 删除（如存在）
□ 4. 从 skills-trigger-map.md 删除
□ 5. 更新版本号
□ 6. 运行同步检查
□ 7. 提交 Git
```

### 修改触发词

```
□ 1. 确认修改原因（用户反馈/匹配失败）
□ 2. 更新 CLAUDE.md
□ 3. 更新 skills-trigger-map.md
□ 4. 更新两个文件的版本号
□ 5. 运行同步检查
□ 6. 测试修改后的触发词
□ 7. 提交 Git
```

---

## 同步检查命令

```bash
# 完整同步检查
./skills.sh check-sync

# 只检查版本号
./skills.sh check-version

# 只检查触发词一致性
./skills.sh check-triggers
```

---

## 同步失败处理

### 失败场景 1：版本号不一致

```
❌ CLAUDE.md: v1.1
❌ skills-trigger-map.md: v1.0

✅ 修复：
1. 确认哪个版本是最新的
2. 更新另一个文件的版本号
3. 运行 ./skills.sh check-sync 验证
```

### 失败场景 2：核心触发词缺失

```
❌ CLAUDE.md 包含"考前冲刺" → exam-prep
❌ skills-trigger-map.md 不包含"考前冲刺"

✅ 修复：
1. 在 skills-trigger-map.md 的 exam-prep 部分添加"考前冲刺"
2. 更新版本号
3. 运行 ./skills.sh check-sync 验证
```

### 失败场景 3：高频词未升级到核心

```
⚠️ skills-trigger-map.md 中"刷题"使用频率：日均 25 次
⚠️ 但未在 CLAUDE.md 核心触发词中

✅ 修复：
1. 添加到 CLAUDE.md exam-prep 核心触发词
2. 更新两个文件的版本号
3. 运行 ./skills.sh check-sync 验证
```

---

## 版本命名规则

```
格式：v<主版本>.<次版本>

主版本更新（X.0 → Y.0）：
- 新增技能
- 删除技能
- 触发机制重大变更

次版本更新（1.X → 1.Y）：
- 添加触发词
- 删除触发词
- 修改触发词
- 修复同步问题

示例：
v1.0 → v1.1：添加 3 个触发词
v1.1 → v2.0：新增 video-edit 技能
v2.0 → v2.1：修复触发词匹配问题
```

---

## Git 提交规范

### 添加触发词

```bash
git commit -m "feat(triggers): 添加考前冲刺→exam-prep v1.1→v1.2"
```

### 删除触发词

```bash
git commit -m "chore(triggers): 删除废弃触发词 v1.2→v1.3"
```

### 修复同步问题

```bash
git commit -m "fix(triggers): 同步 CLAUDE.md 和 trigger-map 版本号 v1.1→v1.2"
```

### 新增技能

```bash
git commit -m "feat(skill): 新增 video-edit 技能 v1.9→v2.0"
```

---

## 检查频率

| 检查类型 | 频率 | 执行时机 |
|----------|------|----------|
| 同步检查 | 每次修改 | 修改触发词后 |
| 版本检查 | 每周 | 周五自动检查 |
| 频率分析 | 每月 | 月初分析上月使用情况 |
| 完整测试 | 每季度 | 季度末运行完整测试集 |

---

## 自动化检查（待实现）

### GitHub Action

```yaml
# .github/workflows/sync-check.yml
name: Trigger Sync Check

on:
  push:
    paths:
      - '.claude/CLAUDE.md'
      - '.claude/skills-trigger-map.md'

jobs:
  sync-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Check sync
        run: ./skills.sh check-sync
```

### 提交前检查

```bash
# .git/hooks/pre-commit
#!/bin/bash
./skills.sh check-sync
if [ $? -ne 0 ]; then
  echo "触发词同步检查失败，请先修复"
  exit 1
fi
```

---

## 记录维护日志

每次同步检查后记录：

```markdown
## 2026-05-01 同步检查

- 检查人：monkeycode-ai
- 检查结果：✅ 通过
- 版本号：v1.1 → v1.2
- 变更内容：添加 14 个核心触发词到 CLAUDE.md
- 测试用例：38/38 通过
```

---

## 版本历史

| 版本 | 日期 | 变更内容 |
|------|------|----------|
| v1.0 | 2026-05-01 | 初始版本，创建同步检查清单 |
