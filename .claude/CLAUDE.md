# Claude 配置 — 工作流集成（精简版）

> 方案 D：按需加载技能  
> 常驻 Token：~1,200（核心触发词 + 索引）  
> 最后更新：2026-05-01  
> 触发词外部化：核心词常驻，完整表按需加载

---

## 核心规则

### 1. Git 同步
```bash
git add . && git commit -m "auto: <描述>" && git push
```

### 2. 文件整理
- 删除重复文件（带 (1)(2) 版本号）
- 分类到：作业/比赛/知识库
- 清理空目录

### 3. Token 策略
- 单次读取 ≤200 行
- 大文件分段读取
- 按需加载 skills

---

## 工作流触发

**机制**：检测关键词 → 读取对应 skill → 执行

### 核心触发词（Level 1 - 直接触发）

| 触发词 | 技能 |
|--------|------|
| 复习/备考/考试/背题/划重点 | `exam-prep` |
| 比赛/竞赛/备赛/学创杯/挑战杯 | `competition-prep` |
| 写论文/写报告/论文写作/文献综述 | `research-paper-isolated` |
| 参考知识库/用知识库/结合之前资料 | `research-paper-with-kb` |
| 查文献/找论文/引用格式/参考文献 | `literature-search` |
| 分析数据/处理 Excel/财务分析/图表 | `data-analysis` |
| 周计划/日程安排/时间管理/周回顾 | `weekly-planning` |
| 整理资料/整理文件/批量处理/索引 | `knowledge-manage` |
| 需求分析/功能设计/写需求文档 | `feature-design` |
| 剪辑视频/剪视频/去废话/加字幕 | `video-use` |
| 生成视频/做视频/动画视频/从零开始 | `hyperframes` |
| 转语音/TTS/配音/语音合成/朗读 | `tts-voice` |
| 背景音乐/BGM/配乐/生成音乐 | `music-gen` |
| Git/同步/commit/push | `git-sync` |

### 触发规则

- **Level 1**：精确匹配 → 直接触发（置信度≥80%）
- **Level 2**：模糊匹配 → 告知用户后触发（置信度 60-79%）
- **Level 3**：低置信度 → 询问确认（置信度 40-59%）
- **否定词**：不想/不要/不需要/别 → 不触发

**完整映射表**：`skills-trigger-map.md`（按需加载）  
**技能索引**：`skills-index.md`

---

## 快捷命令

```bash
# 论文写作
./skills.sh paper <PDF/URL>        # 隔离模式
./skills.sh paper-kb <主题>        # 知识库模式

# 考试比赛
./skills.sh exam <科目> [日期]     # 考试复习
./skills.sh competition <比赛>     # 比赛备赛

# 数据分析
./skills.sh data <文件> [类型]     # 数据分析

# 日常管理
./skills.sh plan [日期]            # 周计划
./skills.sh kb <文件夹>            # 知识管理

# 工具
./skills.sh sync                   # Git 同步
./skills.sh compress <文件>        # 文档压缩
```

---

## 自动化规则

### 文件操作后自动同步 Git
每次创建/修改文件后：
```bash
git add . && git commit && git push
```

### 大文件自动压缩提醒
.md 文件 >500 行 → 提醒使用 `caveman-compress`

---

## 配置文件

| 文件 | 用途 | 加载时机 | Token |
|------|------|----------|-------|
| `CLAUDE.md` | 核心配置 + 触发词 | 常驻 | ~800 |
| `skills-index.md` | 技能索引表 | 常驻 | ~500 |
| `skills-trigger-map.md` | 完整触发词映射 | 按需 | ~3,000 |
| `skills-config.json` | 配置参数 | 按需 | ~200 |
| `MEMORY.md` | 用户偏好记忆 | 常驻 | ~800 |
| **常驻总计** | - | - | **~2,100** |

---

**完整文档**：见 `/workspace/方案 D_*.md`
