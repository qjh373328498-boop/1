# 方案 D 完整工作流程图

> 版本：v1.0  
> 最后更新：2026-04-30

---

## 主流程图

```mermaid
graph TD
    A[用户输入任务/指令] --> B{检测否定词}
    B -->|不想/不要/还没 | C[正常对话处理]
    B -->|无否定词 | D{关键词匹配}
    
    D -->|一级关键词 | E1[置信度 100%]
    D -->|二级关键词 | E2[置信度 70%]
    D -->|三级关键词 | E3[置信度 50%]
    D -->|无匹配 | C
    
    E1 --> F{置信度决策}
    E2 --> F
    E3 --> F
    
    F -->|≥80% | G1[直接触发 skill]
    F -->|60-79% | G2[触发 + 告知用户]
    F -->|40-59% | G3[询问用户确认]
    F -->|<40% | C
    
    G1 --> H[读取对应 skill 卡片]
    G2 --> H
    G3 -->|用户确认 | H
    G3 -->|用户否认 | C
    
    H --> I[读取完整 skill/SKILL.md]
    I --> J[执行 skill 工作流]
    
    J --> K{是否需要写文件？}
    K -->|是 | L{当前分支是 master/main?}
    K -->|否 | Q
    
    L -->|是 | M[获取日期 YYMMDD]
    L -->|否 | Q
    
    M --> N[生成分支名<br>YYMMDD-type-desc]
    N --> O[创建并切换分支<br>git checkout -b]
    O --> Q
    
    Q --> R[执行文件写操作<br>Edit/Write]
    R --> S{是否包含<br>Git Submodules?}
    
    S -->|是 | T[检查 submodule 改动<br>git submodule foreach]
    S -->|否 | U
    
    T -->|有改动 | V[对每个 submodule:<br>1. 创建分支 2. 提交 3. push]
    T -->|无改动 | U
    
    V --> W[更新主项目 submodule 引用]
    W --> U
    
    U --> X[提交主项目<br>git add + commit + push]
    X --> Y{是否需要<br>前端预览？}
    
    Y -->|是 | Z[执行 /deploy-website<br>启动开发服务器]
    Y -->|否 | AA
    
    Z --> AA[任务完成]
    AA --> AB[更新 MEMORY.md<br>记录用户指令/项目知识]
    AB --> AC[结束]
```

---

## 子流程详解

### 子流程 1：意图识别与置信度计算

```mermaid
graph LR
    A[用户输入] --> B[提取关键词]
    B --> C{匹配 skill}
    
    C -->|一级关键词 | D1[基础权重 100%]
    C -->|二级关键词 | D2[基础权重 70%]
    C -->|三级关键词 | D3[基础权重 50%]
    C -->|组合关键词 | D4[基础权重 80%]
    
    D1 --> E{检查意图强度}
    D2 --> E
    D3 --> E
    D4 --> E
    
    E -->|强意图<br>帮我/我要 | F1[×1.0]
    E -->|弱意图<br>了解一下/看看 | F2[×0.6]
    E -->|中性 | F3[×1.0]
    
    F1 --> G{上下文系数}
    F2 --> G
    F3 --> G
    
    G -->|上文相关 | H1[×1.2]
    G -->|首次提及 | H2[×1.0]
    G -->|上文无关 | H3[×0.8]
    
    H1 --> I[最终置信度]
    H2 --> I
    H3 --> I
```

---

### 子流程 2：Skill 触发决策

```mermaid
graph TD
    A[计算置信度] --> B{置信度 ≥80%?}
    B -->|是 | C[直接触发 skill]
    B -->|否 | D{置信度 ≥60%?}
    
    D -->|是 | E[触发 + 告知用户<br>我帮你执行 XXX skill]
    D -->|否 | F{置信度 ≥40%?}
    
    F -->|是 | G[询问用户确认<br>你要不要执行 XXX？]
    F -->|否 | H[不触发，正常对话]
    
    G -->|用户确认 | C
    G -->|用户否认 | H
```

---

### 子流程 3：分支创建流程（写操作前）

```mermaid
graph TD
    A[准备写文件] --> B{是 git 仓库？}
    B -->|否 | C[直接写文件]
    B -->|是 | D{当前分支是<br>master/main?}
    
    D -->|否 | C
    D -->|是 | E{修改的是<br>.monkeycode 目录？}
    
    E -->|是 | F[不创建分支<br>直接修改文档]
    E -->|否 | G[获取当前日期 YYMMDD]
    
    G --> H[分析任务类型<br>feat/fix/chore/refactor]
    H --> I[生成任务摘要<br>英文小写连字符]
    
    I --> J[组合分支名<br>YYMMDD-type-desc]
    J --> K[创建并切换分支<br>git checkout -b]
    K --> L[写文件]
```

---

### 子流程 4：Git Submodule 处理

```mermaid
graph TD
    A[准备提交] --> B{存在.gitmodules?}
    B -->|否 | H
    B -->|是 | C[检查 submodule 状态<br>git submodule foreach]
    
    C --> D{有改动？}
    D -->|否 | H
    D -->|是 | E[对每个有改动的 submodule]
    
    E --> F[进入 submodule]
    F --> G[创建分支并提交]
    G --> H[push 到远程<br>-o merge_request.create]
    H --> I{还有 submodule?}
    
    I -->|是 | E
    I -->|否 | J[返回主项目]
    J --> K[更新 submodule 引用<br>git add <path>]
    K --> L[提交主项目]
```

---

### 子流程 5：Git 提交流程

```mermaid
graph TD
    A[文件修改完成] --> B[git status 检查]
    B --> C[git diff 查看改动]
    C --> D[生成 commit message<br><类型>: <描述>]
    D --> E[git add .]
    E --> F[git commit -m]
    F --> G[git push]
    
    G --> H{需要前端预览？}
    H -->|是 | I[执行 /deploy-website]
    H -->|否 | J[任务完成]
    
    I --> J
```

---

### 子流程 6：MEMORY.md 更新流程

```mermaid
graph TD
    A[任务执行中/完成] --> B{发现新的用户指令<br>或项目知识？}
    B -->|否 | E
    B -->|是 | C[读取.memory.md]
    
    C --> D{检查重复？}
    D -->|已存在 | D1[跳过或合并]
    D -->|不重复 | E[追加新条目]
    
    E --> F[格式化条目<br>日期 + 上下文 + 指令]
    F --> G[写回.memory.md]
    G --> H[git 提交]
```

---

## 完整示例：用户说"帮我复习中级会计"

```mermaid
graph TD
    A["用户：帮我复习中级会计"] --> B[检测否定词 ❌]
    B --> C[关键词匹配<br>"帮我"+"复习"+"中级会计"]
    C --> D[置信度计算<br>一级关键词 100% × 强意图 1.0 = 100%]
    
    D --> E{置信度 ≥80%?}
    E -->|是 | F[直接触发 exam-prep-workflow]
    
    F --> G[读取 skills/exam-prep/SKILL.md]
    G --> H[执行工作流]
    
    H --> I[1. 询问：科目 + 考试日期 + 资料]
    I --> J["用户：中级会计，下周五，有教材"]
    
    J --> K[2. 读取教材/笔记]
    K --> L[3. 提取知识点、重点、公式]
    L --> M[4. 生成文件]
    
    M --> N[创建分支<br>260430-feat-exam-prep]
    N --> O[写文件<br>知识点摘要.md/复习计划.md]
    O --> P[git add + commit + push]
    P --> Q[更新 MEMORY.md<br>记录用户备考偏好]
    Q --> R[任务完成]
```

---

## 触发条件总结表

| 阶段 | 触发条件 | 执行动作 | 输出 |
|------|----------|----------|------|
| **意图识别** | 用户输入包含关键词 | 计算置信度 | skill 名称 + 置信度 |
| **Skill 触发** | 置信度 ≥80% | 直接执行 | 读取完整 skill |
| | 置信度 60-79% | 告知用户 | 读取完整 skill |
| | 置信度 40-59% | 询问确认 | 用户确认后执行 |
| | 置信度 <40% | 不触发 | 正常对话 |
| **分支创建** | 写操作 + master/main 分支 | 创建日期分支 | 新分支 |
| **Submodule** | 存在.gitmodules+ 改动 | 分别提交 push | 更新引用 |
| **Git 提交** | 文件修改完成 | commit + push | 远程仓库 |
| **前端预览** | Web 项目改动 | /deploy-website | 开发服务器 |
| **Memory 更新** | 新指令/知识发现 | 追加条目 | .memory.md |

---

## 关键决策点

| 决策点 | 条件 | 分支 A | 分支 B |
|--------|------|--------|--------|
| 否定词检测 | 包含"不想/不要" | 正常对话 | 继续流程 |
| 置信度阈值 | ≥80% | 直接触发 | 告知/询问 |
| 写操作检查 | 修改文件 | 检查分支 | 直接执行 |
| 分支检查 | master/main | 创建分支 | 当前分支 |
| Submodule 检查 | 存在.gitmodules | 处理 submodule | 直接提交 |
| 前端预览 | Web 项目 | 启动服务 | 直接完成 |

---

## 文件读取优先级

```
1. skills-index.md (常驻) - 技能列表
2. skills-trigger-map.md (常驻) - 关键词映射
3. skills-config.json (常驻) - 配置参数
4. workflows/*.card (按需) - 技能卡片
5. skills/*/SKILL.md (按需) - 完整技能文档
6. .memory.md (常驻) - 用户偏好
```

---

## Token 使用优化

| 文件 | 大小 | 加载策略 | 常驻 Token |
|------|------|----------|-----------|
| CLAUDE.md | ~100 行 | 常驻 | ~1,000 |
| skills-index.md | ~200 行 | 常驻 | ~300 |
| skills-trigger-map.md | ~250 行 | 常驻 | ~300 |
| .memory.md | 可变 | 常驻 | ~100 |
| workflows/*.card | ~40 行×10 | 按需 | 0 |
| skills/*/SKILL.md | ~200 行×88 | 按需 | 0 |
| **总计** | | | **~1,700** |

**对比原方案**：88 个 skill 常驻 ~20,000 tokens → **节省 91.5%**

---

**流程图文档完成时间**：2026-04-30  
**版本**：v1.0
