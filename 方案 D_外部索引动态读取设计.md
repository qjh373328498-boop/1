# 方案 D：外部索引 + 动态读取

## 📋 完整设计方案

---

## 一、核心思路

**原则**：将技能定义与触发逻辑分离，只在需要时加载完整技能内容。

```
传统模式：
每次对话加载 88 个 skills (20,000+ tokens) → 检测需求 → 执行
         ↓
      90% 的 skills 从未被使用

方案 D 模式：
每次对话加载索引表 (500 tokens) → 检测需求 → 读取对应 skill → 执行
         ↓
      只加载需要的 skills
```

---

## 二、架构设计

### 2.1 文件结构

```
.claude/
├── CLAUDE.md                 # 主配置（精简到 100 行）
├── skills-index.md           # 技能索引表（核心文件）
├── skills-trigger-map.md     # 触发关键词映射
├── skills/                   # 完整 skills（88 个，按需读取）
│   ├── exam-prep-workflow/
│   │   └── SKILL.md
│   ├── competition-prep-workflow/
│   │   └── SKILL.md
│   └── ...
└── workflows/                # 工作流卡片（可选，50 行精简版）
    ├── exam-prep.card
    ├── competition-prep.card
    └── ...
```

---

### 2.2 技能索引表（skills-index.md）

```markdown
# Skills 索引表

## 使用说明
1. 检测用户输入中的关键词
2. 匹配对应的 skill
3. 读取完整 skill 文件
4. 执行工作流

## 技能列表

### 学术写作类
| 技能名 | 关键词 | 触发示例 | 文件路径 |
|--------|--------|----------|----------|
| research-paper-isolated | 写论文/写报告/论文写作 | "帮我写论文" | `skills/research-paper-workflow-isolated/SKILL.md` |
| research-paper-with-kb | 参考知识库/用知识库 | "参考知识库写论文" | `skills/research-paper-workflow-with-kb/SKILL.md` |
| literature-search | 查文献/找论文/引用格式 | "查找文献" | `skills/literature-search-workflow/SKILL.md` |

### 考试比赛类
| 技能名 | 关键词 | 触发示例 | 文件路径 |
|--------|--------|----------|----------|
| exam-prep | 考试/复习/备考/背题 | "帮我复习" | `skills/exam-prep-workflow/SKILL.md` |
| competition-prep | 比赛/竞赛/学创杯/挑战杯 | "准备比赛" | `skills/competition-prep-workflow/SKILL.md` |

### 数据分析类
| 技能名 | 关键词 | 触发示例 | 文件路径 |
|--------|--------|----------|----------|
| data-analysis | 数据分析/处理 Excel/财务分析/图表 | "分析这个数据" | `skills/data-analysis-workflow/SKILL.md` |

### 知识管理类
| 技能名 | 关键词 | 触发示例 | 文件路径 |
|--------|--------|----------|----------|
| knowledge-manage | 整理资料/知识库/批量处理 | "整理这些文件" | `skills/knowledge-manage-workflow/SKILL.md` |

### 项目管理类
| 技能名 | 关键词 | 触发示例 | 文件路径 |
|--------|--------|----------|----------|
| feature-design | 需求分析/功能设计/写需求文档 | "设计一个功能" | `skills/feature-design/SKILL.md` |

### 日常管理类
| 技能名 | 关键词 | 触发示例 | 文件路径 |
|--------|--------|----------|----------|
| weekly-planning | 周计划/计划/日程安排/周回顾 | "制定计划" | `skills/weekly-planning-workflow/SKILL.md` |

### 工具类
| 技能名 | 关键词 | 触发示例 | 文件路径 |
|--------|--------|----------|----------|
| git-sync | git/同步/commit/push | "提交代码" | `.claude/git-sync.card` |
| file-organize | 整理文件/删除重复 | "整理工作区" | `.claude/file-organize.card` |
| doc-compress | 压缩文档/节省 token | "压缩这个文件" | `.claude/doc-compress.card` |

## 总计
- 技能总数：88 个
- 常驻索引：~100 行
- 预估 Token：~500
```

---

### 2.3 触发关键词映射（skills-trigger-map.md）

```markdown
# 触发关键词映射

## 映射规则
1. 优先级：精确匹配 > 模糊匹配
2. 多关键词匹配时，选择权重最高的
3. 无匹配时，使用默认工作流或不触发

## 关键词权重

### 高优先级（精确匹配）
```
"写论文" → research-paper-isolated
"参考知识库" → research-paper-with-kb
"复习" → exam-prep
"比赛" → competition-prep
"数据分析" → data-analysis
"周计划" → weekly-planning
```

### 中优先级（模糊匹配）
```
"论文" + "写" → research-paper-isolated
"考试" + "准备" → exam-prep
"文献" + "找" → literature-search
```

### 低优先级（上下文推断）
```
课程名 → exam-prep
比赛名 → competition-prep
数据文件 → data-analysis
```

## 负向触发词（不触发任何 skill）
- 你好
- 谢谢
- 在吗
- 测试
- 123
```

---

### 2.4 工作流卡片（精简版，可选）

**目的**：对于常用技能，保留精简版本作为快速参考

**文件格式**（`.card` 文件，~50 行）：

```markdown
---
name: exam-prep-card
type: workflow-card
trigger: 考试/复习/备考
---

# 考试复习工作流（精简版）

## 触发
用户提到：考试、复习、备考、背题

## 快速流程
1. 询问科目和考试日期
2. 读取课程资料（笔记/PPT）
3. 提取知识点
4. 生成思维导图
5. 制作记忆卡片
6. 制定复习计划

## 输出
- 知识点摘要.md
- 思维导图.svg
- 记忆卡片（Anki 格式）
- 复习计划.md

## 完整技能
读取：`skills/exam-prep-workflow/SKILL.md`
```

**卡片好处**：
- 仅 50 行，token 占用小
- 快速了解技能功能
- 需要时再读完整版

---

## 三、工作流程

### 3.1 标准流程

```
Step 1: 用户输入
    ↓
Step 2: 读取技能索引（500 tokens）
    ↓
Step 3: 检测用户需求
    ├─ 有匹配 → 读取对应 skill 文件（+300 tokens）
    └─ 无匹配 → 正常对话
    ↓
Step 4: 按 skill 执行任务
    ↓
Step 5: 清理上下文（释放 skill 内容）
```

### 3.2 示例对话

**场景 1：用户要复习考试**

```
用户：我要准备中级会计的考试，下周三考

模型操作：
1. 读取 skills-index.md（500 tokens）
2. 检测关键词："考试" → 匹配 exam-prep
3. 读取 skills/exam-prep-workflow/SKILL.md（300 行，~2,000 tokens）
4. 按 workf low 执行：
   - 询问是否有课程笔记
   - 提取知识点
   - 生成复习计划
5. 释放 skill 内容，保留对话

Total: ~2,500 tokens（vs 原来的 20,000+）
```

**场景 2：闲聊**

```
用户：你今天怎么样？

模型操作：
1. 读取 skills-index.md（500 tokens）
2. 检测关键词：无匹配
3. 不读取任何 skill
4. 正常对话

Total: ~500 tokens
```

**场景 3：复杂任务（多 skill）**

```
用户：帮我写论文，需要查文献和数据分析

模型操作：
1. 读取 skills-index.md（500 tokens）
2. 检测多需求：
   - "写论文" → research-paper-isolated
   - "查文献" → literature-search
   - "数据分析" → data-analysis
3. 依次读取 3 个 skills（~6,000 tokens）
4. 整合执行

Total: ~6,500 tokens（vs 原来的 20,000+, 仍然节省 65%+）
```

---

## 四、实施方案

### 4.1 阶段 1：创建索引文件

**任务**：
1. 创建 `skills-index.md`（100 行）
2. 创建 `skills-trigger-map.md`（50 行）
3. 精简 `CLAUDE.md`（100 行）

**Token 占用**：~700

### 4.2 阶段 2：创建常用技能卡片

**选择最常用的 10 个技能**：
- exam-prep-workflow
- competition-prep-workflow
- data-analysis-workflow
- weekly-planning-workflow
- research-paper-isolated
- research-paper-with-kb
- literature-search
- knowledge-manage
- feature-design
- git-sync

**创建 `.card` 文件**（每个 50 行，共 500 行）

**Token 占用**：~3,000

### 4.3 阶段 3：实现动态读取逻辑

**方法 A：使用子代理**
```
主对话：保持轻量，只加载索引
子代理：按需启动，加载完整 skill
```

**方法 B：手动读取**
```
检测需求 → 手动读取 skill → 提示用户"正在加载技能..."
```

### 4.4 阶段 4：优化关键词匹配

**优化方向**：
- 同义词扩展（如 "备考" = "复习" = "考试"）
- 上下文理解（结合对话历史）
- 多意图识别（同时匹配多个 skill）

---

## 五、对比分析

### 5.1 Token 占用对比

| 场景 | 原始模式 | 方案 D | 节省 |
|------|---------|--------|------|
| 闲聊 | 20,000+ | 500 | 97% |
| 单任务 | 20,000+ | 2,500 | 87% |
| 多任务 | 20,000+ | 6,500 | 67% |
| 平均 | 20,000+ | ~2,500 | 87% |

### 5.2 响应速度对比

| 模式 | 首次响应 | 执行效率 |
|------|---------|---------|
| 原始 | 快（已加载） | 快 |
| 方案 D | 略慢（需读取） | 快 |

**差异**：方案 D 首次响应延迟约 1-2 秒（读取 skill 的时间）

### 5.3 功能完整性

| 维度 | 原始模式 | 方案 D |
|------|---------|--------|
| 功能数量 | 88 个 | 88 个（完整保留） |
| 功能深度 | 完整版 | 完整版 |
| 灵活性 | 固定 | 可动态扩展 |

---

## 六、优缺点总结

### ✅ 优点

1. **Token 节省巨大**：87%+ 的节省率
2. **功能完整**：不损失任何技能
3. **易于扩展**：添加新技能只需更新索引
4. **场景适配**：多任务时仍然节省
5. **可维护性**：索引和技能分离，便于管理

### ⚠️ 缺点

1. **首次响应延迟**：需额外读取 skill（1-2 秒）
2. **识别依赖关键词**：可能出现误判
3. **实现复杂度增加**：需要额外的读取逻辑

### 🔧 改进方向

1. **缓存常用 skills**：对于高频 skill，预加载精简版
2. **智能预测**：根据对话上下文预测下一个 skill
3. **批量加载**：相关的 skills 一起预加载

---

## 七、实施建议

### 建议 1：渐进式实施

```
第 1 周：创建索引 + 精简 CLAUDE.md
第 2 周：创建 10 个常用技能卡片
第 3 周：测试优化关键词匹配
第 4 周：全面实施
```

### 建议 2：保留回退机制

```
如果识别失败或用户明确指定：
→ 直接加载完整 skill
→ 或手动选择要使用的技能
```

### 建议 3：收集使用数据

```
记录：
- 哪些 skills 最常用
- 哪些关键词匹配率高
- 用户的反馈

优化：
- 高频 skills 预加载
- 优化关键词映射
```

---

## 八、效果预估

### Token 使用对比（假设每天 10 轮对话）

| 模式 | 日均 Token | 月均 Token | 节省 |
|------|-----------|-----------|------|
| 原始 | 200,000 | 6,000,000 | - |
| 方案 D | 25,000 | 750,000 | 87.5% |

### 对话长度对比

| 模式 | 可用对话轮数 | 限制因素 |
|------|-------------|---------|
| 原始 | 10-15 轮 | Context Window |
| 方案 D | 80-100 轮 | 无 |

---

## 九、决策建议

**如果你选择方案 D，你将获得**：

✅ Token 使用减少 87%+
✅ 对话长度增加 5-8 倍
✅ 功能完整保留
✅ 易于扩展和维护

**你需要接受**：

⚠️ 首次响应略慢 1-2 秒
⚠️ 需要创建索引文件
⚠️ 需要调整使用习惯

**我的建议**：
- 如果 Token 是主要瓶颈 → **强烈推荐**方案 D
- 如果追求极致响应速度 → 考虑方案 A 或 E
- 如果想要最大节省 → 方案 D 是最优选择
