# Claude 配置 — 工作流集成

## 核心规则

### 1. Git Commit 消息生成

**触发条件**：
- 用户说"commit"、"提交"、"生成 commit 消息"
- 执行 `git add` 后准备提交时

**使用技能**：`caveman-commit`

**配置**：
```bash
# 提交前自动生成简洁 commit 消息
git add . && git commit -m "$(caveman-commit generate)"
```

**默认行为**：
- 类型：`chore`（文件整理、文档更新）
- 类型：`feat`（新功能）
- 类型：`fix`（bug 修复）
- 主体 ≤50 字，仅在必要时添加正文

---

### 2. 知识库文档压缩

**触发条件**：
- 知识库 `.md` 文件 > 500 行
- 用户说"压缩文档"、"optimize memory"、"节省 token"

**使用技能**：`caveman-compress`

**配置**：
```bash
# 压缩单个文档
python3 .claude/skills/caveman-compress/scripts <目标文件路径>

# 批量压缩知识库
find 知识库 -name "*.md" -size +50k -exec python3 .claude/skills/caveman-compress/scripts {} \;
```

**压缩范围**：
- ✅ 压缩：`知识库/**/*`.md`
- ✅ 压缩：`CLAUDE.md`、`MEMORY.md`
- ❌ 不压缩：代码文件、配置文件、数据文件

---

### 3. 文件整理工作流

**标准流程**：

```bash
# 1. 扫描重复文件（按文件名模式）
find . -type f -name "*([0-9])*" -o -name "*copy*" -o -name "*备份*"

# 2. 移动到目标分类目录
mv <源文件> <目标分类>/

# 3. 清理空目录
find . -type d -empty -delete

# 4. Git 追踪变更
git add .

# 5. 生成 commit 消息并提交
# 使用 caveman-commit 生成简洁消息
```

**自动分类规则**：

| 文件类型 | 目标目录 |
|---------|---------|
| `*论文*`、`*作业*` | `作业（论文或笔记）/` |
| `*比赛*`、`*竞赛*`、`*杯*` | `比赛/` |
| `*申请*`、`*表*`、`*评优*` | `各类申请表/` |
| `*.md`（索引文档） | `知识库/` |

---

### 4. Git 同步工作流

**标准流程**：

```bash
# 1. 检查状态
git status

# 2. 检查分支
git branch

# 3. 如果有 diverge，先 pull
git pull --rebase origin main

# 4. 推送
git push
```

**Commit 消息模板**：

| 场景 | 消息格式 |
|------|---------|
| 文件整理 | `chore: 整理文件结构，删除重复文件` |
| 文档更新 | `docs: 更新索引文档` |
| 新作业 | `chore(作业): 添加 <课程名> 作业` |
| 新比赛资料 | `chore(比赛): 添加 <比赛名> 资料` |

---

### 5. Token 节省策略

**文件读取**：
- 单次读取 ≤200 行
- 大文件分段读取（offset + limit）
- 优先使用 `grep` 搜索关键词定位

**对话历史**：
- 长对话后清理上下文
- 仅保留关键决策和文件路径

**Git 操作**：
- 合并多个 git 命令为链式调用
- 使用 `git add . && git commit -m "..." && git push`

---

## 自动化规则

### 规则 1：Commit 前自动检查
```bash
# 如果有未暂存的改动，提醒用户
git status --porcelain
# 输出不为空 → 询问是否 commit
```

### 规则 2：知识库变更自动更新索引
```bash
# 如果 知识库/ 目录有变更
# 检查是否需要更新 快速检索表.md
```

### 规则 3：大文件自动压缩提醒
```bash
# 如果创建/更新的 .md 文件 > 500 行
# 提醒用户使用 caveman-compress
```

---

## 快捷键 / 命令别名

| 命令 | 功能 |
|------|------|
| `/commit` | 生成 commit 消息并提交 |
| `/compress <文件>` | 压缩指定文档 |
| `/organize` | 自动整理工作区文件 |
| `/sync` | Git pull + push 同步 |

---

## 配置文件说明

| 文件 | 用途 |
|------|------|
| `.claude/CLAUDE.md` | 本配置文件 |
| `.claude/skills/` | 技能脚本目录 |
| `知识库/00-索引/` | 快速检索表 |
| `MEMORY.md` | 用户偏好记忆 |

---

**最后更新**：2026-04-29  
**维护**：根据使用场景持续优化
