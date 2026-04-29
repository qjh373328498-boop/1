# Claude Skills 使用指南

## 快速开始

### 1. 文件整理后提交

```bash
# 方式 1: 使用快捷脚本（推荐）
.claude/skills.sh commit

# 方式 2: 手动生成 commit 消息
# 告诉 AI："生成 commit 消息"，然后复制输出执行
```

**自动消息规则**：
- 知识库变更 → `docs: 更新知识库文档`
- 作业文件变更 → `chore(作业): 更新作业文件`
- 比赛资料变更 → `chore(比赛): 更新比赛资料`
- 其他 → `chore: 整理文件结构`

---

### 2. Git 同步到远程

```bash
# 使用快捷脚本
.claude/skills.sh sync

# 或手动执行
git pull --rebase origin main && git push
```

---

### 3. 压缩大文档（节省 Token）

```bash
# 压缩单个文档
.claude/skills.sh compress 知识库/01-个人文档/个人学业档案索引.md

# 或告诉 AI："压缩这个文档"
```

**压缩效果**：约节省 75% tokens，保留所有技术内容

---

### 4. 查找重复文件

```bash
# 扫描带版本号的重复文件
.claude/skills.sh duplicates
```

**输出示例**：
```
./作业/论文 (1).docx
./比赛/学创杯/策划书 V2.docx
./比赛/学创杯/策划书最终版.docx
```

---

### 5. 清理空目录

```bash
# 查找并删除空目录
.claude/skills.sh clean-dirs
```

---

## 与 AI 交互的快捷指令

| 你说 | AI 执行 |
|------|--------|
| "提交" | 调用 `caveman-commit` 生成消息并 commit |
| "同步" | 执行 `git pull --rebase && git push` |
| "压缩这个文件" | 调用 `caveman-compress` 压缩指定文档 |
| "找重复文件" | 扫描文件名带版本号的重复文件 |
| "清理空文件夹" | 删除工作区空目录 |

---

## Token 节省效果

| 场景 | 使用前 | 使用后 | 节省 |
|------|--------|--------|------|
| Commit 消息 | 50-100 tokens | 20-40 tokens | ~60% |
| 知识库文档 | 5000 tokens | 1250 tokens | ~75% |
| 文件整理对话 | 2000 tokens | 1200 tokens | ~40% |

**预计每月节省**：5000-10000 tokens（取决于使用频率）

---

## 配置文件说明

| 文件 | 用途 |
|------|------|
| `.claude/CLAUDE.md` | 核心配置，定义工作流规则 |
| `.claude/skills.sh` | 快捷脚本，命令行调用 |
| `.claude/skills/` | 技能脚本目录 |

---

## 常见问题

**Q: 如何禁用某个技能？**  
A: 在 `.claude/CLAUDE.md` 中注释掉对应规则即可

**Q: 压缩后的文档能恢复吗？**  
A: 可以，原文件备份为 `FILE.original.md`

**Q: commit 消息不满意怎么办？**  
A: 手动执行 `git commit --amend` 修改

---

**最后更新**：2026-04-29  
**维护**：根据使用反馈持续优化
