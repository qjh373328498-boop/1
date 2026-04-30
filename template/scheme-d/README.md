# 方案 D - 按需加载 Skills 配置模板

> 版本：v1.0  
> Token 优化：**-92%** (20,000 → ~1,700)

---

## 快速使用

### 方式 1：复制配置（推荐）

```bash
cd your-project
cp -r /path/to/template/scheme-d/.claude .
```

### 方式 2：使用安装脚本

```bash
cd your-project
bash /path/to/template/scheme-d/install.sh
```

### 方式 3：Git Submodule

```bash
cd your-project
git submodule add <repo-url> scheme-d-template
cp -r scheme-d-template/.claude .
```

---

## 目录结构

```
.clude/
├── CLAUDE.md                  # 主配置（必读）
├── skills-index.md            # 88 个 skill 索引
├── skills-trigger-map.md      # 关键词触发映射
├── skills-config.json         # 置信度阈值配置
└── workflows/                 # 10 个核心技能卡片
```

**可选**：
```
skills/                        # 完整 skills 目录（可选，~50MB）
└── */SKILL.md                 # 88 个完整技能文档
```

---

## 核心功能

### 10 个核心 Skills（内置）

| Skill | 触发词 | 功能 |
|-------|--------|------|
| exam-prep | 帮我复习/备考 | 考试复习、划重点、背题 |
| competition-prep | 准备比赛/学创杯 | 比赛备赛、商业计划书、PPT |
| data-analysis | 分析数据/Excel | 数据分析、图表制作 |
| weekly-planning | 周计划/日程 | 制定周计划、时间管理 |
| research-paper | 帮我写论文 | 论文写作、研究报告 |
| literature-search | 查找文献 | 检索论文、参考文献 |
| knowledge-manage | 整理资料 | 知识管理、批量处理 |
| feature-design | 需求分析/设计 | 需求文档、技术设计 |
| git-sync | 提交代码/git | Git 同步、submodule 处理 |

### 触发机制

| 置信度 | 决策 | 操作 |
|--------|------|------|
| ≥80% | 直接触发 | 执行 skill |
| 60-79% | 中置信 | 触发 + 告知 |
| 40-59% | 低置信 | 询问确认 |
| <40% | 不触发 | 正常对话 |

### 否定词（不触发）

```
不想、不要、不需要、别、没有、还没
```

---

## 安装选项

### 基础安装（推荐）

只复制 `.claude/` 配置（~1MB）：
- 包含 10 个核心技能卡片
- 包含配置和索引
- Token 优化 92%+

```bash
cp -r template/scheme-d/.claude your-project/
```

### 完整安装（可选）

额外复制 `skills/` 目录（~50MB）：
- 包含 88 个完整 skill 文档
- 适合需要全部功能的用户

```bash
cp -r template/scheme-d/skills your-project/
```

---

## 配置说明

### 1. CLAUDE.md

主配置文件，包含：
- 核心规则
- 快捷命令
- 自动化规则

### 2. skills-trigger-map.md

关键词映射，可自定义：
- 一级关键词（100% 权重）
- 二级关键词（70% 权重）
- 三级关键词（50% 权重）

### 3. skills-config.json

配置参数：
```json
{
  "threshold": {
    "direct_trigger": 80,
    "confirm_trigger": 60,
    "ask_confirm": 40
  }
}
```

### 4. workflows/*.card

技能卡片，每个卡片包含：
- 触发关键词
- 快速流程
- 确认话术
- 完整 skill 路径

---

## 自定义配置

### 添加新的 Skill

1. 创建 skill 文档：
```bash
mkdir skills/my-custom-skill
cat > skills/my-custom-skill/SKILL.md
```

2. 添加到 `skills-index.md`：
```markdown
| my-custom-skill | 关键词 | 描述 | 高 | workflows/my-custom.card |
```

3. 创建技能卡片 `workflows/my-custom.card`

4. 添加关键词到 `skills-trigger-map.md`

### 修改触发阈值

编辑 `skills-config.json`：
```json
{
  "threshold": {
    "direct_trigger": 80  // 调整此值
  }
}
```

### 自定义关键词

编辑 `skills-trigger-map.md`，添加你的关键词。

---

## 使用示例

```
用户：帮我复习中级会计
→ 触发 exam-prep-workflow (置信度 100%)
→ 读取 exam-prep/SKILL.md
→ 执行复习工作流

用户：准备学创杯比赛
→ 触发 competition-prep-workflow (置信度 100%)
→ 读取 competition-prep/SKILL.md
→ 执行备赛工作流
```

---

## 性能对比

| 指标 | 传统方式 | 方案 D | 改善 |
|------|----------|--------|------|
| 常驻 tokens | ~20,000 | ~1,700 | -92% |
| skills 加载 | 88 个常驻 | 按需加载 | 按需触发 |
| 响应速度 | 慢 | 快 | +50% |
| 误触发率 | N/A | 0% | 优秀 |

---

## 维护更新

如需更新模板：

```bash
cd your-project

# 如果使用 submodule
git submodule update --remote

# 如果手动复制
cp -r /path/to/template/scheme-d/.claude/* .claude/
```

---

## 完整文档

详细设计文档见：
- 方案设计：`docs/方案 D_*.md`
- 流程图：`docs/方案 D_完整流程图.md`
- 测试报告：`docs/方案 D_阶段 3 测试报告.md`

---

## License

MIT © 2026

---

**创建日期**：2026-04-30  
**版本**：v1.0  
**最后更新**：2026-04-30 (精简版)
