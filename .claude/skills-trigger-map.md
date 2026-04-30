# Skills 触发关键词映射

> 版本：v1.0  
> 最后更新：2026-04-30

---

## 映射规则

1. **优先级**：精确匹配 > 模糊匹配 > 上下文推断
2. **多关键词匹配**：选择权重最高的
3. **无匹配**：不触发任何 skill，正常对话

---

## 一级关键词（权重 100%，直接触发）

### exam-prep-workflow
```
- 帮我复习
- 我要备考
- 准备考试
- 背题
- 划重点
```

### competition-prep-workflow
```
- 准备比赛
- 参加比赛
- 备赛
- 帮我写商业计划书
- 做路演 PPT
```

### research-paper-workflow-isolated
```
- 帮我写论文
- 写研究报告
- 写文献综述
- 论文写作
- 论文
- 写报告
- 你看看这个论文
- 看看这个报告
```

### research-paper-workflow-with-kb
```
- 参考知识库写论文
- 用知识库的资料
- 结合我之前的资料
```

### literature-search-workflow
```
- 查找文献
- 找论文
- 生成参考文献
- 引用格式
```

### data-analysis-workflow
```
- 帮我分析
- 分析一下
- 分析数据
- 处理 Excel
- 财务分析
- financial analysis
- analysis
- 制作图表
- 用 Python 分析数据
```

### weekly-planning-workflow
```
- 制定周计划
- 安排日程
- 时间管理
- 周回顾
- 周计划
- 日程安排
```

### knowledge-manage-workflow
```
- 帮我整理这些资料
- 整理资料
- 整理文件
- 批量处理文档
- 建立索引
```

### feature-design
```
- 需求分析
- 功能设计
- 写需求文档
- 设计一个功能
```

---

## 二级关键词（权重 70%，需要确认）

### exam-prep-workflow
```
- 复习
- 备考
- 考试
- 课程名 + 时间词（如"中级会计 + 下周"）
```

### competition-prep-workflow
```
- 比赛名 + 参加/准备
- 学创杯
- 挑战杯
- 国创赛
```

### research-paper-workflow-isolated
```
- 论文
- 写报告
- 文献
```

### data-analysis-workflow
```
- 帮我分析这个数据
- 分析一下这个数据
- 分析一下 Excel
- 帮我分析这个 Excel
- 分析这个数据
- 处理 Excel
- 财务分析
- 制作图表
- 用 Python 分析数据
```

### weekly-planning-workflow
```
- 计划
- 日程
- 安排
```

---

## 三级关键词（权重 50%，需要询问确认）

### 课程名 → exam-prep
```
- 中级财务会计
- 财务管理
- 审计学
- 税法
- 成本会计
- 管理会计
```

### 比赛名 → competition-prep
```
- 互联网 +
- 案例大赛
- 数学建模
```

### 文件名 → 对应 skill
```
- .xlsx 文件 → data-analysis 或 xlsx
- .pdf 文件 → pdf 或 literature-search
- .docx 文件 → docx
```

---

## 关键词组合（权重 80%）

```
"考试" + "复习" → exam-prep
"比赛" + "准备" → competition-prep
"论文" + "写" → research-paper
"数据" + "分析" → data-analysis
"文献" + "查找" → literature-search
"计划" + "周" → weekly-planning
```

---

## 否定词列表（不触发）

### 明确否定（中文）
```
- 不想
- 不要
- 不需要
- 别
- 甭
- 没有
- 还没
- 尚未
```

### 明确否定（英文）
```
- don't
- do not
- won't
- would not
- no need
- never
```

### 疑问否定
```
- 怎么不
- 为什么不
- 何必
```

### 否定示例
```
❌ "我不想写论文" → 不触发
❌ "还没开始复习" → 不触发
❌ "别整理文件" → 不触发
```

---

## 意图强度识别

### 强意图（系数 ×1.0）
```
- 帮我 XXX
- 我要 XXX
- 需要 XXX
- 怎么做 XXX
- 准备 XXX
```

### 弱意图（系数 ×0.6）
```
- 了解一下 XXX
- 看看 XXX
- 问一下 XXX
- XXX 是什么
```

### 无意图（系数 ×0）
```
- XXX 怎么样
- XXX 好不好
- 知道 XXX 吗
- 你好/谢谢/再见
```

---

## 置信度决策阈值

```json
{
  "direct_trigger": 80,
  "confirm_trigger": 60,
  "ask_confirm": 40
}
```

| 置信度 | 决策 | 操作 |
|--------|------|------|
| ≥80% | 高置信 | 直接触发 skill |
| 60-79% | 中置信 | 触发 + 告知用户 |
| 40-59% | 低置信 | 询问用户确认 |
| <40% | 不触发 | 正常对话 |

---

## 上下文系数

```
上文有相关讨论 ×1.2
首次提及 ×1.0
上文无关 ×0.8
```

---

## 多意图处理

### 优先级
```
P0：明确指定 skill 名
P1：一级关键词匹配
P2：二级关键词匹配
P3：三级关键词匹配
```

### 冲突解决
```
如果多个 skill 置信度接近：
1. 询问用户确认
2. 按顺序执行
3. 选择最可能的一个
```

### 示例
```
用户："帮我写论文，需要查文献和数据分析"

识别结果：
- research-paper: 100%
- literature-search: 100%
- data-analysis: 100%

决策：全部触发，按顺序执行
```

---

## 版本历史

| 版本 | 日期 | 变更内容 |
|------|------|----------|
| v1.0 | 2026-04-30 | 初始版本 |

---

## 多意图优先级规则

### 意图优先级顺序

当一句话包含多个意图时，按以下优先级选择：

1. **第一意图优先** - 句子的第一个 skill 意图
2. **连接词后意图优先** - "先/但/然后/最后" 后的意图
3. **高权重意图优先** - 一级关键词>二级>三级

### 连接词识别

```
- 先 XXX，然后 YYY → 优先 X
- 主要 XXX，顺便 YYY → 优先 X
- 虽然 XXX，但是 YYY → 优先 Y
- 除了 XXX，还要 YYY → 优先 X (主)，Y (次)
```

### 示例

```
"帮我写论文，需要查找文献" → research-paper (第一意图)
"先制定周计划，然后帮我复习" → weekly-planning (先连接词)
"主要是复习，顺便整理" → exam-prep (主要连接词)
```

---

## 文件类型推断

当用户提到文件名或上传文件时：

| 文件扩展名 | 推断 skill | 关键词补充 |
|-----------|-----------|-----------|
| .xlsx / .xls | data-analysis | "Excel", "表格", "数据" |
| .pdf | research-paper / literature-search | "论文", "文献", "PDF" |
| .docx / .doc | knowledge-manage / feature-design | "文档", "Word", "需求" |
| .ppt / .pptx | competition-prep | "PPT", "演示", "路演" |

### 示例

```
"exam.xlsx 帮我分析" → data-analysis
"thesis.pdf 看看" → research-paper
"report.docx 整理" → knowledge-manage
```

---

---

## 多意图处理策略

### 优先级规则

1. **第一意图优先** - 句子开头的意图权重最高
2. **连接词后优先** - "先 X 然后 Y" → X 优先
3. **转折后优先** - "X 但 Y" → Y 优先
4. **高优先级 skill** - research-paper > competition > exam > feature > data > weekly > knowledge

### 意图权重

```
research-paper-isolated: 10 (最高)
competition-prep: 9
exam-prep: 8
feature-design: 7
data-analysis: 6
weekly-planning: 5
knowledge-manage: 4
literature-search: 3
```

### 示例

```
✅ "帮我写论文，需要查找文献" → research-paper (第一意图 + 高权重)
✅ "先制定周计划，然后复习" → weekly-planning (连接词优先)
✅ "主要是复习，顺便整理" → exam-prep (主要连接词)
⚠️ "设计功能，但先分析数据" → 需要实现转折词识别
```

---

## 第四轮优化成果 (新增)

### 1. 转折词识别 ✅
- "但/但是/不过"后的意图权重 ×1.5
- 解决："设计功能，但先分析数据" → data-analysis

### 2. 条件句过滤 ✅
- "如果...再说"结构被忽略
- 解决："帮我整理，如果需要分析再说" → knowledge-manage

### 3. 特殊字符预处理 ✅
- 去除连续的"."、"-"等特殊字符
- 解决："复..习..考..试" → exam-prep

### 4. 文件类型推断增强 ✅
- .pdf/thesis → research-paper
- "看看" + 文件上下文 → 对应 skill
- 解决："thesis.pdf 帮我看看" → research-paper

### 5. 否定词增强 ✅
- 添加："还没"、"尚未"
- 解决："还没开始复习" → 不触发

### 6. 意图权重调整 ✅
- research-paper: 10 → 7
- literature-search: 3 → 6
- weekly-planning: 5 → 6
- 解决："文献文献找论文" → literature-search

---

**第四轮通过率**: 90.9% (较第三轮 88.2% ↑ 2.7%)
