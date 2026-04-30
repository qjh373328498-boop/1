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
- ✅ 压缩：`知识库/**/*.md`
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

## 新增工作流

### 6. 学术研究与论文写作工作流（双模式）

**⚠️ 重要：双模式设计**

根据用户是否授权参考知识库，使用不同的工作流：

| 模式 | 触发条件 | 资料来源 | 适用场景 |
|------|----------|----------|----------|
| **隔离模式（默认）** | 用户未明确提及知识库 | 仅外部文献 + 用户提供 | 正式论文、学术竞赛 |
| **知识库模式** | 用户说"参考知识库"、"用知识库的资料"等 | 外部文献 + 知识库 + 用户提供 | 课程作业、学习整理 |

**隔离模式触发条件**：
- 用户说"写论文"、"写报告"但未提及知识库
- 默认情况

**使用技能**：`research-paper-workflow-isolated`

**知识库模式触发条件**（必须明确表述）：
- "可以参考知识库"
- "用知识库的资料帮我..."
- "结合我之前的资料..."
- "参考我之前的学习笔记"
- "用我比赛的那些资料"

**使用技能**：`research-paper-workflow-with-kb`

**完整流程**：
```
资料收集 → 内容提取 → 翻译 → 格式化 → 配图 → 导出 Word/PDF
```

**快捷命令**：
```bash
# 隔离模式（默认）
/research-paper-workflow-isolated <URL 或文件>

# 知识库模式（需用户明确授权）
/research-paper-workflow-with-kb <URL 或文件>

# 仅提取
/research-paper-workflow-isolated <URL> --stage extract

# 仅翻译
/research-paper-workflow-isolated <文件> --stage translate --to zh-CN

# 导出为 Word
/research-paper-workflow-isolated <文件> --export docx

# 导出为 PPT
/research-paper-workflow-isolated <文件> --export pptx
```

**依赖 Skills**：
- `pdf` / `docx` / `xlsx` / `pptx` - 文档处理
- `baoyu-url-to-markdown` - 网页内容提取
- `baoyu-youtube-transcript` - 视频字幕下载
- `baoyu-translate` - 翻译（支持 technical/academic 风格）
- `baoyu-format-markdown` - Markdown 格式化
- `baoyu-diagram` - 流程图/架构图生成
- `baoyu-article-illustrator` - 文章配图
- `baoyu-slide-deck` - PPT 生成

---

### 7. 知识管理工作流

**触发条件**：
- 整理资料、构建知识库
- 批量处理 PDF/Word/Excel 文档
- 搜索相关内容、建立索引

**使用技能**：`knowledge-manage-workflow`

**完整流程**：
```
文档导入 → 内容提取 → 总结 → 格式化 → 知识组织 → 检索利用
```

**快捷命令**：
```bash
# 完整流程
/knowledge-manage-workflow <文件/文件夹>

# 仅总结
/knowledge-manage-workflow <文档> --stage summarize

# 批量处理
/knowledge-manage-workflow <文件夹> --batch

# 搜索
/knowledge-manage-workflow --search "关键词"

# 构建知识库
/knowledge-manage-workflow <文件夹> --build-kb
```

**知识库目录结构**：
```
knowledge-base/
├── inbox/           # 待处理文档
├── processed/       # 已处理文档
├── topics/          # 按主题分类
├── projects/        # 按项目分类
└── archive/         # 归档
```

---

### 8. 需求分析与技术设计工作流

**触发条件**：
- 用户提出新功能需求
- 需要编写需求文档和技术设计
- 项目启动前的规格定义

**使用技能**：`feature-design`

**输出文档**：
- `.monkeycode/specs/{FEATURE_NAME}/requirements.md` - 需求文档（EARS 模式）
- `.monkeycode/specs/{FEATURE_NAME}/design.md` - 技术设计文档

**需求质量标准**：
- 符合 EARS 语法（Easy Approach to Requirements Syntax）
- 通过 INCOSE 语义质量规则验证
- 每条需求可测试、无歧义

---

### 9. 内容创作与发布工作流

**触发条件**：
- 创建社交媒体内容（微信公众号、微博、X）
- 生成信息图、漫画、插图
- Markdown 转 HTML、生成封面图

**可用 Skills**：
| Skill | 用途 |
|-------|------|
| `baoyu-post-to-wechat` | 微信公众号文章发布 |
| `baoyu-post-to-weibo` | 微博发布 |
| `baoyu-post-to-x` | X(Twitter) 发布 |
| `baoyu-infographic` | 信息图表生成（21 种布局） |
| `baoyu-comic` | 漫画生成 |
| `baoyu-cover-image` | 封面图生成 |
| `baoyu-markdown-to-html` | Markdown 转 HTML |
| `baoyu-image-gen` | AI 图像生成 |
| `baoyu-imagine` | 创意图像生成 |

---

### 10. 前端开发工作流

**触发条件**：
- 创建前端项目
- UI/UX 设计
- 组件开发、调试

**可用 Skills**：
| Skill | 用途 |
|-------|------|
| `frontend-project-creator` | 创建前端项目 |
| `frontend-design` | 前端设计 |
| `ui-ux-pro-max` | UI/UX 设计 |
| `design-system-patterns` | 设计系统模式 |
| `web-artifacts-builder` | Web 组件构建 |
| `webapp-testing` | Web 应用测试 |
| `tailwindcss-helper` | Tailwind CSS 辅助 |
| `shadcnui-helper` | shadcn/ui 组件辅助 |
| `mui-helper` | Material-UI 辅助 |
| `deploy-website` | 网站部署预览 |

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

### 规则 4：文件操作自动同步 Git
```bash
# 每次创建/修改文件后自动执行
git add . && git commit -m "auto: <操作描述>" && git push
```

### 规则 5：Skills 自动调用
- 检测到 PDF/Word/Excel 文件 → 自动调用对应处理 skill
- 检测到 URL → 自动调用 `baoyu-url-to-markdown`
- 用户提到"翻译" → 自动调用 `baoyu-translate`
- 用户提到"画图"、"配图" → 自动调用 `baoyu-diagram` 或 `baoyu-infographic`

---

### 11. 考试复习与备考工作流

**触发条件**：
- 用户需要备考、复习、整理知识点
- 制作记忆卡片、思维导图
- 整理错题本、制定复习计划

**使用技能**：`exam-prep-workflow`

**完整流程**：
```
资料收集 → 知识点提取 → 思维导图 → 记忆卡片 → 习题整理 → 复习计划
```

**快捷命令**：
```bash
# 完整复习流程
/exam-prep-workflow {课程名}

# 指定考试日期
/exam-prep-workflow {课程名} --exam-date 2026-06-15

# 仅生成思维导图
/exam-prep-workflow {课程名} --stage mindmap

# 仅制作记忆卡片
/exam-prep-workflow {课程名} --stage cards
```

**输出产物**：
- 知识点摘要.md
- 思维导图（SVG）
- 记忆卡片（Anki/Quizlet 格式）
- 错题本.md
- 复习计划.md

---

### 12. 比赛备赛工作流

**触发条件**：
- 参加学科竞赛（学创杯、挑战杯、国创赛等）
- 需要写商业计划书、路演 PPT
- 准备答辩、模拟演练

**使用技能**：`competition-prep-workflow`

**完整流程**：
```
规则解读 → 备赛计划 → 材料准备 → PPT 优化 → 答辩题库 → 模拟演练
```

**快捷命令**：
```bash
# 完整备赛流程
/competition-prep-workflow {比赛名}

# 指定截止日期
/competition-prep-workflow {比赛名} --deadline 2026-07-15

# 仅 PPT 优化
/competition-prep-workflow {比赛名} --stage ppt

# 仅答辩题库
/competition-prep-workflow {比赛名} --stage qa
```

**支持的比赛**：
- 学创杯（财务决策模拟）
- 挑战杯（创业计划）
- 国创赛（创新创业）
- 互联网+大赛
- 案例分析大赛

---

### 13. 学术文献检索与引用工作流

**触发条件**：
- 查找学术文献
- 管理参考文献
- 生成引用格式
- 撰写文献综述

**使用技能**：`literature-search-workflow`

**完整流程**：
```
文献搜索 → 文献管理 → 阅读笔记 → 引用生成 → 文献综述
```

**快捷命令**：
```bash
# 完整文献检索流程
/literature-search-workflow {研究主题}

# 指定引用格式
/literature-search-workflow {主题} --citation-style APA
/literature-search-workflow {主题} --citation-style "GB/T 7714"

# 导出参考文献
/literature-search-workflow {主题} --export bibtex
```

**支持的引用格式**：
- GB/T 7714-2015（中国国家标准）
- APA（第 7 版）
- MLA
- Chicago
- BibTeX

**推荐数据库**：
- 中国知网（CNKI）
- Google Scholar
- Web of Science
- 会计专业数据库（CSMAR/Wind）

---

## 快捷键 / 命令别名

| 命令 | 功能 |
|------|------|
| `/commit` | 生成 commit 消息并提交 |
| `/compress <文件>` | 压缩指定文档 |
| `/organize` | 自动整理工作区文件 |
| `/sync` | Git pull + push 同步 |
| `/paper <文件/URL>` | 启动论文写作工作流 |
| `/kb <文件/文件夹>` | 启动知识管理工作流 |
| `/feature <需求描述>` | 启动需求分析工作流 |
| `/design` | UI/UX 设计辅助 |
| `/deploy` | 部署网站预览 |

---

## 配置文件说明

| 文件 | 用途 |
|------|------|
| `.claude/CLAUDE.md` | 本配置文件 |
| `.claude/skills/` | 技能脚本目录（**80+ skills**） |
| `.claude/README.md` | Skills 使用指南 |
| `.claude/skills.sh` | 命令行快捷脚本 |
| `知识库/00-索引/` | 快速检索表 |
| `MEMORY.md` | 用户偏好记忆 |

## 可用 Skills 完整列表（80+）

### 核心技能
| Skill | 用途 |
|-------|------|
| `caveman-commit` | 自动生成 commit 消息 |
| `caveman-compress` | 文档压缩（节省 token） |
| `caveman-review` | 代码审查 |
| `build` | 项目构建 |
| `check` | 项目检查 |
| `spec` | 规格定义 |
| `backprop` | 错误回溯分析 |

### 工作流技能
| Skill | 用途 |
|-------|------|
| `research-paper-workflow-isolated` | 论文写作（隔离模式） |
| `research-paper-workflow-with-kb` | 论文写作（知识库模式） |
| `knowledge-manage-workflow` | 知识管理工作流 |
| `feature-design` | 需求分析与技术设计 |
| `feature-implementer` | 功能实现 |
| `software-dev-workflow` | 软件开发工作流 |
| `debug-troubleshoot-workflow` | 调试排错工作流 |
| `content-publish-workflow` | 内容发布工作流 |
| `exam-prep-workflow` | **考试复习与备考** ⭐ 新增 |
| `competition-prep-workflow` | **比赛备赛** ⭐ 新增 |
| `literature-search-workflow` | **文献检索与引用** ⭐ 新增 |

### 文档处理
| Skill | 用途 |
|-------|------|
| `pdf` | PDF 文档处理 |
| `docx` | Word 文档处理 |
| `xlsx` | Excel 表格处理 |
| `pptx` | PPT 幻灯片处理 |
| `doc-coauthoring` | 文档协作撰写 |

### 内容创作（Baoyu 系列）
| Skill | 用途 |
|-------|------|
| `baoyu-translate` | 翻译（支持多种风格） |
| `baoyu-format-markdown` | Markdown 格式化 |
| `baoyu-markdown-to-html` | Markdown 转 HTML |
| `baoyu-url-to-markdown` | 网页内容提取 |
| `baoyu-youtube-transcript` | YouTube 字幕下载 |
| `baoyu-diagram` | 流程图/架构图生成 |
| `baoyu-infographic` | 信息图表生成 |
| `baoyu-article-illustrator` | 文章配图 |
| `baoyu-cover-image` | 封面图生成 |
| `baoyu-image-gen` / `baoyu-imagine` | AI 图像生成 |
| `baoyu-comic` | 漫画生成 |
| `baoyu-slide-deck` | PPT 生成 |
| `baoyu-post-to-wechat` | 微信公众号发布 |
| `baoyu-post-to-weibo` | 微博发布 |
| `baoyu-post-to-x` | X(Twitter) 发布 |

### 前端开发
| Skill | 用途 |
|-------|------|
| `frontend-design` | 前端设计 |
| `frontend-project-creator` | 创建前端项目 |
| `ui-ux-pro-max` | UI/UX 设计 |
| `design-system-patterns` | 设计系统模式 |
| `tailwindcss-helper` | Tailwind CSS 辅助 |
| `shadcnui-helper` | shadcn/ui 辅助 |
| `mui-helper` | Material-UI 辅助 |
| `web-artifacts-builder` | Web 组件构建 |
| `webapp-testing` | Web 应用测试 |
| `deploy-website` | 网站部署预览 |
| `react-code-fix-linter` | React 代码修复 |
| `react-native-ui-animation` | React Native 动画 |

### 后端开发
| Skill | 用途 |
|-------|------|
| `golang-patterns` | Go 语言模式 |
| `golang-testing` | Go 语言测试 |
| `golang-code-review` | Go 代码审查 |

### 项目管理
| Skill | 用途 |
|-------|------|
| `implementation-planner` | 实施计划制定 |
| `executing-plans` | 计划执行 |
| `finishing-a-development-branch` | 完成开发分支 |
| `project-wiki` | 项目 Wiki 生成 |

### 其他工具
| Skill | 用途 |
|-------|------|
| `brainstorming` | 头脑风暴 |
| `skill-creator` | 创建新 skill |
| `mcp-builder` | MCP 构建器 |
| `dispatching-parallel-agents` | 并行 Agent 调度 |
| `subagent-driven-development` | Subagent 开发 |
| `systematic-debugging` | 系统化调试 |
| `security-review-audit` | 安全审查 |
| `test-driven-development` | 测试驱动开发 |
| `verification-before-completion` | 完成前验证 |
| `requesting-code-review` | 请求代码审查 |
| `receiving-code-review` | 接受代码审查 |

---

**最后更新**：2026-04-30  
**维护**：根据使用场景持续优化
