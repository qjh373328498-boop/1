# 技能删除记录

> 日期：2026-05-01  
> 操作：删除重复/废弃技能  
> 目标：精简技能数量，减少 Token 占用

---

## 已删除技能

### 1. baoyu-image-gen ❌

**删除日期**：2026-05-01

**删除原因**：
- 技能自身已标记为 **Deprecated**
- `SKILL.md` description 明确写明："Deprecated: use baoyu-imagine"
- 功能完全被 `baoyu-imagine` 替代

**替代方案**：
- ✅ 使用 `baoyu-imagine` 替代
- 触发词："生成图片"、"画图"、"AI 画图"、"高质量图片"、"AI 绘画"

**影响范围**：
- 无功能影响（已废弃技能）
- 历史配置文件自动迁移（EXTEND.md 自动重命名）

**文件变更**：
```
删除：/workspace/.claude/skills/baoyu-image-gen/
更新：/workspace/.claude/skills-index.md
更新：/workspace/.claude/skills-trigger-map.md
更新：/workspace/.claude/workflows/video-production-pipeline.card
更新：/workspace/.claude/skills/content-publish-workflow/SKILL.md
```

**Token 节省**：
- 删除 SKILL.md：~13KB 文件
- skills-index.md 引用：~50 tokens
- 触发词映射：~30 tokens
- **总计**：~80 tokens（非常小）

---

## 待评估技能

### 2. 文档处理类（pdf/docx/xlsx/pptx）

**状态**：待评估

**问题**：
- 4 个技能可能功能重叠
- 都是文件类型处理器
- 底层实现可能相似

**建议**：
- 如果实现通用，可合并为 `document-handler`
- 如果各有专长，保留现状

### 3. Caveman 系列（caveman-commit/caveman-review）

**状态**：待评估

**问题**：
- `caveman` 是基础编码规则
- `caveman-commit`、`caveman-review` 是专用技能
- 触发词有交叉

**建议**：
- 合并到 `caveman` 统一入口
- 通过参数区分不同用途

---

## 优化效果

### 技能数量变化

| 操作前 | 删除 | 操作后 | 变化 |
|--------|------|--------|------|
| 90 个 | 1 个 | 89 个 | -1.1% |

### Token 节省

| 项目 | 节省 |
|------|------|
| 文件存储 | ~13KB |
| 索引引用 | ~80 tokens |
| 触发词映射 | ~30 tokens |

---

## 迁移说明

### 用户配置迁移

如果用户有 `.baoyu-skills/baoyu-image-gen/EXTEND.md`：
- `baoyu-imagine` 会自动重命名并迁移配置
- 用户无需手动操作

### 触发词迁移

原触发词 "生成图片"、"画图"、"AI 画图" 现已映射到：
- ✅ `baoyu-imagine`

### 工作流更新

- 视频工作流：阶段 5.1 "通用图片" → "图片生成（baoyu-imagine）"
- 内容发布流：图片技能列表更新

---

## 后续计划

1. ✅ 删除 baoyu-image-gen
2. ⏳ 评估文档处理技能（pdf/docx/xlsx/pptx）
3. ⏳ 评估 Caveman 系列技能
4. ⏳ 检查其他潜在重复

---

## Git 提交

```bash
git add . && git commit -m "refactor: 删除废弃技能 baoyu-image-gen

删除原因:
- 技能已标记为 deprecated
- 功能完全被 baoyu-imagine 替代

影响:
- 删除 skills/baoyu-image-gen/ 目录
- 更新 skills-index.md
- 更新 skills-trigger-map.md
- 更新 video-production-pipeline.card
- 更新 content-publish-workflow/SKILL.md

Token 节省：~80 tokens"
```
