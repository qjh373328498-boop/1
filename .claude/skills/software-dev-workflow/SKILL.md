---
name: software-dev-workflow
description: 软件开发完整工作流。当用户需要开发新功能、编写代码、做项目时自动触发。串联需求分析→头脑风暴→设计文档→实施计划→编码执行→代码审查→测试验证全流程。
---

# 软件开发完整工作流

这是一个端到端的软件开发工作流，整合了 brainstorming、规划、实施、审查、测试等多个 skills，实现从想法到可运行代码的完整交付。

## 触发场景

当用户提到以下需求时自动触发：
- "帮我开发一个功能"、"写个 XXX 系统"、"做个网站"
- "添加用户登录"、"实现支付功能"
- "重构代码"、"优化性能"
- "修复这个 bug"、"调试问题"
- "写个 API"、"创建组件"

## 工作流程图

```
┌─────────────┐
│  1. 需求分析  │
│  探索意图   │
└──────┬──────┘
       ↓
┌─────────────┐
│  2. 头脑风暴  │
│  设计方案   │
└──────┬──────┘
       ↓
┌─────────────┐
│  3. 设计文档  │
│  架构规划   │
└──────┬──────┘
       ↓
┌─────────────┐
│  4. 实施计划  │
│  任务拆解   │
└──────┬──────┘
       ↓
┌─────────────┐
│  5. 编码执行  │
│  TDD 开发    │
└──────┬──────┘
       ↓
┌─────────────┐
│  6. 代码审查  │
│  质量检查   │
└──────┬──────┘
       ↓
┌─────────────┐
│  7. 测试验证  │
│  确保通过   │
└──────┬──────┘
       ↓
┌─────────────┐
│  8. 部署/    │
│  交付        │
└─────────────┘
```

## 完整工作流程

### 阶段 1：需求分析

**1.1 项目上下文探索**
```
动作：
- 读取 package.json/requirements.txt
- 检查现有代码结构
- 查看最近提交记录
- 了解技术栈和约定
```

**1.2 需求澄清**
```
调用：brainstorming skill
- 一次问一个问题
- 理解业务目标
- 明确成功标准
- 识别约束条件
```

### 阶段 2：头脑风暴与设计

**核心原则**：
- <HARD-GATE>在完成设计和用户批准前，绝不编写任何实现代码</HARD-GATE>

**2.1 探索方案**
```
调用：brainstorming skill
- 提出 2-3 个方案
- 分析利弊取舍
- 给出推荐方案
```

**2.2 设计评审**
```
产出：docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md
内容：
- 架构图
- 组件设计
- 数据流
- 接口定义
- 错误处理
```

**2.3 设计自审**
```
检查清单：
- 有无 TBD/TODO 占位符
- 内部一致性
- 范围是否合理
- 消除歧义
```

### 阶段 3：实施计划

**3.1 任务拆解**
```
调用：implementation-planner skill
输入：设计文档
输出：详细任务列表
- 每个任务 2-5 分钟
- 精确文件路径
- 完整代码示例
- 验证步骤
```

**3.2 测试策略**
```
包含：
- 单元测试用例
- 集成测试点
- 验收标准
```

### 阶段 4：编码执行

**4.1 执行模式选择**

**模式 A：Subagent 驱动（推荐）**
```
调用：subagent-driven-development skill
- 分发任务给子代理
- 两阶段审查（规范合规→代码质量）
- 自动迭代直到通过
```

**模式 B：批量执行**
```
调用：executing-plans skill
- 批量执行任务
- 人类检查点
- 适合关键决策点
```

**4.2 TDD 开发**
```
调用：test-driven-development skill
RED-GREEN-REFACTOR 循环：
1. 写失败测试
2. 观察失败
3. 写最少代码
4. 观察通过
5. 重构优化
6. 提交代码
```

### 阶段 5：代码审查

**5.1 任务间审查**
```
调用：requesting-code-review skill
审查内容：
- 符合设计规范
- 代码质量标准
- 安全问题
- 性能考虑
```

**5.2 问题分级处理**
```
Critical（严重）：
- 阻塞进度
- 必须修复

Major（主要）：
- 记录在案
- 尽快修复

Minor（次要）：
- 可选优化
- 技术债记录
```

### 阶段 6：测试验证

**6.1 验证完成**
```
调用：verification-before-completion skill
检查：
- 所有测试通过
- 功能符合需求
- 无回归问题
- 文档已更新
```

**6.2 系统调试（如有问题）**
```
调用：systematic-debugging skill
4 阶段流程：
1. 问题定位
2. 根因分析
3. 方案设计
4. 修复验证
```

### 阶段 7：分支完成

**7.1 完成检查**
```
调用：finishing-a-development-branch skill
- 运行完整测试
- 更新文档
- 清理临时文件
```

**7.2 合并选项**
```
提供选项：
- 合并到主分支
- 创建 Pull Request
- 保持分支
- 废弃更改
```

### 阶段 8：部署交付

**8.1 本地预览**
```
调用：deploy-website skill（如为 Web 项目）
- 启动开发服务器
- 提供预览链接
```

**8.2 Git 工作流**
```
调用：using-git-worktrees skill
- 创建工作树
- 隔离开发环境
- 保持主分支清洁
```

## 快捷命令模式

```bash
# 完整流程
/software-dev-workflow "开发用户登录功能"

# 仅设计阶段
/software-dev-workflow "用户系统" --stage design

# 仅规划阶段
/software-dev-workflow "支付模块" --stage plan

# 仅执行阶段（已有设计文档）
/software-dev-workflow --stage execute --spec docs/specs/xxx-design.md

# 仅代码审查
/software-dev-workflow --stage review --pr 123

# 调试模式
/software-dev-workflow --stage debug "登录失败问题"

# 快速原型（跳过部分审查）
/software-dev-workflow "快速原型" --mode fast
```

## 输出产物

```
docs/superpowers/
├── specs/
│   └── YYYY-MM-DD-<topic>-design.md    # 设计文档
├── plans/
│   └── YYYY-MM-DD-<topic>-plan.md      # 实施计划
└── tasklist.md                          # 任务清单

src/
├── 新增/修改的代码文件
└── tests/
    └── 对应的测试文件

.git/
├── branches/
│   └── YYMMDD-<type>-<feature>        # 功能分支
└── commits/
    └── 提交历史
```

## 使用示例

### 示例 1：开发新功能

用户："帮我添加用户登录功能"

工作流：
1. brainstorming：探索需求（OAuth2？JWT？）
2. 设计文档：架构、接口、数据模型
3. 实施计划：拆解为具体任务
4. TDD 开发：先写测试，再实现
5. 代码审查：检查质量和安全
6. 验证完成：确保测试全通过

### 示例 2：Bug 修复

用户："登录后页面空白，帮我修复"

工作流：
1. systematic-debugging：4 阶段调试
2. 根因分析：查看日志和代码
3. 修复方案：设计修复
4. test-driven-development：写测试→修复→验证
5. verification-before-completion：确认修复

### 示例 3：重构代码

用户："这个模块太乱了，重构一下"

工作流：
1. brainstorming：理解重构目标
2. 设计文档：新架构设计
3. 实施计划：分步重构任务
4. executing-plans：批量执行（带检查点）
5. 代码审查：确保质量

## 依赖 Skills

| Skill | 阶段 | 用途 |
|-------|------|------|
| brainstorming | 2 | 需求探索和设计方案 |
| implementation-planner | 3 | 任务拆解 |
| subagent-driven-development | 4 | 多 Agent 并行开发 |
| executing-plans | 4 | 批量执行任务 |
| test-driven-development | 4 | TDD 开发 |
| requesting-code-review | 5 | 代码审查 |
| verification-before-completion | 6 | 验证完成 |
| systematic-debugging | 6 | 系统调试 |
| finishing-a-development-branch | 7 | 分支完成 |
| using-git-worktrees | 8 | Git 工作树 |

## 模式说明

### 标准模式（默认）

完整 8 阶段流程，适合：
- 新功能开发
- 重要模块
- 团队项目
- 生产代码

### 快速模式

```bash
--mode fast
```

跳过部分审查，适合：
- 原型开发
- 个人项目
- 一次性脚本
- 实验性代码

流程：需求→简版设计→快速实现→基础测试

### 紧急修复模式

```bash
--mode hotfix
```

最小化流程，适合：
- 生产事故
- 紧急 Bug
- 线上问题

流程：定位问题→快速修复→关键测试→部署

## 进阶配置

创建 `.software-dev-workflow/EXTEND.md` 自定义：

```yaml
# 默认开发模式
default_mode: standard

# Git 分支命名
branch_naming:
  format: "YYMMDD-{type}-{feature}"
  types:
    feat: 新功能
    fix: Bug 修复
    refactor: 重构
    chore: 杂项

# 代码审查规则
code_review:
  auto_review: true
  critical_block: true
  style_guide: "项目规范"

# 测试要求
testing:
  min_coverage: 80%
  required_types:
    - unit
    - integration
```

## 最佳实践

1. **永远不要跳过设计阶段**：即使"简单"的功能也要先设计
2. **TDD 是必须的**：先写测试，后写代码
3. **小步提交**：每个任务独立提交
4. **持续审查**：任务间自动审查，不要等到最后
5. **验证驱动**：只有验证通过才算完成
