# 方案 D v6.0：视频工作流集成版

**最后更新**: 2026-05-02  
**版本**: v6.0 (视频生成 V2.3 集成)  
**状态**: ✅ 生产就绪

---

## 核心架构（三级触发）

| 级别 | 位置 | 技能数 | Token | 加载时机 |
|------|------|--------|-------|----------|
| **L1 - 高频核心** | `CLAUDE.md` | 12 | ~600 | **常驻** |
| **L2 - 扩展触发词** | `skills-trigger-map.md` | 77 | ~2,500 | 意图明确时 |
| **L3 - 技能文档** | `skills/*/SKILL.md` | 89 | ~50,000 | 触发后 |

---

## V6.0 新增：视频生成工作流集成

### 1. 视频生成能力总览

**核心脚本**: `/workspace/.claude/scripts/make_video.sh` (1400+ 行)

**功能特性**:
- ✅ 一键视频生成（脚本→配音→分镜→图片→合成）
- ✅ 批量任务处理（JSON 配置，自动依次处理）
- ✅ 断点续传（从失败步骤继续）
- ✅ 错误重试（自动重试 N 次）
- ✅ 智能进度预估（已用时/预计剩余/完成时间）
- ✅ 质量检查（音频/图片/视频自动验证）
- ✅ BGM 背景音乐（混音支持）
- ✅ 日志记录（详细执行日志）
- ✅ JSON 配置文件
- ✅ 横屏视频预设（1280x720 ~ 3840x2160）

---

### 2. 视频工作流版本历史

| 版本 | 日期 | 主要功能 | 状态 |
|------|------|----------|------|
| V2.3 | 2026-05-02 | 批量任务 + 智能进度 + 错误恢复 | ✅ 完成 |
| V2.2 | 2026-05-02 | 配置文件 + 断点续传 + 质量检查 | ✅ 完成 |
| V2.1 | 2026-05-02 | 进度显示 + 日志记录 + BGM | ✅ 完成 |
| V2.0 | 2026-05-01 | 智能脚本生成 + 动态分镜 | ✅ 完成 |
| V1.0 | 2026-04-30 | 基础一键脚本 | ✅ 完成 |

---

### 3. 核心功能详解

#### 3.1 批量任务处理

**使用方式**:
```bash
./make_video.sh --batch tasks.json --output ./batch-output/
```

**配置文件** (`tasks.json`):
```json
[
  {"theme": "AI 绘画教程", "duration": 60, "voice": "zh-CN-YunxiNeural"},
  {"theme": "Python 入门", "duration": 90, "voice": "zh-CN-XiaoxiaoNeural"},
  {"theme": "健康饮食", "duration": 120, "voice": "zh-CN-YunjianNeural"}
]
```

**输出结构**:
```
batch-output/
├── _AI绘画教程_143022/
│   ├── script.md
│   ├── narration.mp3
│   ├── storyboard.json
│   ├── images/
│   ├── scaled/
│   └── final.mp4
├── _Python入门_143045/
│   └── ...
└── _健康饮食_143108/
    └── ...
```

#### 3.2 错误恢复机制

**错误处理策略**:
- `stop`: 立即停止（默认）
- `continue`: 跳过失败任务，继续下一个
- `retry`: 自动重试（最多 N 次）

**配置参数**:
```bash
./make_video.sh --batch tasks.json \
  --error-handling retry \
  --max-retries 3
```

**重试逻辑**:
1. 任务失败后等待 5 秒
2. 自动重试，最多 N 次
3. 超过最大重试次数后根据策略处理

#### 3.3 智能进度预估

**显示内容**:
```
⏳ 进度：[████████████████████] 100% - 合成最终视频
⏱️  已用时：2 分 15 秒 | 预计剩余：1 分 30 秒 | 完成时间：14:35:20
```

**预估算法**:
```
平均单步耗时 = 已用时间 / 已完成步数
预计剩余时间 = 平均单步耗时 × 剩余步数
预计完成时间 = 当前时间 + 预计剩余时间
```

#### 3.4 质量检查系统

**检查项目**:
- **音频**: 时长、文件大小、内容有效性
- **图片**: 尺寸、文件大小、损坏检测
- **视频**: 时长、分辨率、文件大小、内容有效性

**输出报告**: `quality_report.txt`

#### 3.5 横屏视频预设

| 规格 | 分辨率 | 适用场景 |
|------|--------|----------|
| **HD** | 1280x720 | 默认，适合网络传播，文件小 |
| **FHD** | 1920x1080 | ⭐ 推荐，全高清，YouTube/B 站标准 |
| **QHD** | 2560x1440 | 2K 高清，高质量演示 |
| **4K** | 3840x2160 | 超高清，专业制作 |
| **超宽** | 2560x1080 | 21:9 电影感，创意视频 |

**使用方式**:
```bash
# 全高清 (推荐)
./make_video.sh --theme "产品介绍" --width 1920 --height 1080

# 4K 超高清
./make_video.sh --theme "风景纪录片" --width 3840 --height 2160 --crf 20
```

---

### 4. AI 图片生成集成（V5.0 保留）

#### 4.1 ModelScope API 配置

```python
BASE_URL = "https://api-inference.modelscope.cn/"
API_KEY = "ms-cc494f31-690a-4df6-9bea-a9a0d3311c4e"
MODEL = "Tongyi-MAI/Z-Image-Turbo"  # 通义万相高速版
```

#### 4.2 核心脚本

**`gen_image.py`** - 267 行
- 单张生成
- 批量生成（JSON 配置）
- 从 storyboard.json 自动生成
- 异步任务轮询，自动重试
- 并发控制（默认 4 个 worker）

**使用示例**:
```bash
# 单张生成
./gen_image.py "一只可爱的猫咪，阳光草地" output.jpg

# 批量生成
./gen_image.py batch.json

# 视频工作流自动调用
./make_video.sh --theme "猫咪百科" --duration 60
```

---

### 5. 技能触发词更新

#### 新增视频相关触发词（L1 高频）

| 触发词 | 技能 | 功能 |
|--------|------|------|
| 生成视频/做视频 | `make_video.sh` | 一键视频生成 |
| 批量视频 | `make_video.sh --batch` | 批量处理 |
| 横屏视频 | `--width 1920 --height 1080` | 16:9 视频 |
| 4K 视频 | `--width 3840 --height 2160` | 超高清 |
| 视频配乐 | `--with-bgm --bgm-file` | 添加 BGM |

#### 新增图片相关触发词（L2 扩展）

| 触发词 | 技能 | 功能 |
|--------|------|------|
| 生成图片 | `gen_image.py` | AI 图片生成 |
| AI 画图 | `gen_image.py` | ModelScope 绘图 |
| 批量生成图片 | `gen_image.py batch.json` | 批量处理 |

---

### 6. 配置文件示例

#### 6.1 视频生成配置 (`video-config.json`)

```json
{
  "theme": "AI 视频教程",
  "duration": 180,
  "voice": "zh-CN-YunxiNeural",
  "width": 1920,
  "height": 1080,
  "crf": 23,
  "audio-bitrate": "192k",
  "with-bgm": false,
  "quality-check": true
}
```

#### 6.2 批量任务配置 (`batch-tasks.json`)

```json
[
  {
    "theme": "Python 第一课：环境搭建",
    "duration": 120,
    "voice": "zh-CN-YunxiNeural",
    "width": 1920,
    "height": 1080
  },
  {
    "theme": "Python 第二课：基础语法",
    "duration": 120,
    "voice": "zh-CN-YunxiNeural",
    "width": 1920,
    "height": 1080
  },
  {
    "theme": "Python 第三课：函数定义",
    "duration": 120,
    "voice": "zh-CN-YunxiNeural",
    "width": 1920,
    "height": 1080
  }
]
```

---

### 7. 完整工作流示例

#### 示例 1: 从零开始生成视频

```bash
# 简单模式
./make_video.sh --theme "德国心脏病桌游介绍" --duration 270

# 自定义配置
./make_video.sh --theme "产品介绍" \
  --duration 120 \
  --width 1920 \
  --height 1080 \
  --crf 20 \
  --audio-bitrate 256k \
  --with-bgm \
  --bgm-file bgm.mp3
```

#### 示例 2: 批量生成系列视频

```bash
# 批量处理（失败继续）
./make_video.sh --batch python-series.json \
  --output ./python-tutorials/ \
  --error-handling continue \
  --max-retries 2 \
  --verbose
```

#### 示例 3: 断点续传

```bash
# 从步骤 4（图片生成）继续
./make_video.sh --resume-from 4 \
  --output ./video-output-20260502/
```

#### 示例 4: 多语言版本

```bash
# 同一内容生成多语言版本
./make_video.sh --batch multi-lang.json \
  --output ./company-intro-multi-lang/
```

**multi-lang.json**:
```json
[
  {"theme": "公司介绍", "duration": 60, "voice": "zh-CN-YunxiNeural"},
  {"theme": "公司介绍", "duration": 60, "voice": "en-US-JennyNeural"},
  {"theme": "公司介绍", "duration": 60, "voice": "ja-JP-NanamiNeural"}
]
```

---

### 8. 技术栈

| 组件 | 技术 | 说明 |
|------|------|------|
| **主脚本** | Bash (1400+ 行) | 流程控制、参数解析 |
| **图片生成** | Python + ModelScope API | AI 图片生成 |
| **语音合成** | edge-tts | Microsoft Azure TTS |
| **视频合成** | FFmpeg | 编解码、滤镜、混音 |
| **分镜脚本** | Python | 智能分析脚本生成 JSON |
| **质量检查** | FFprobe + Bash | 媒体文件验证 |

---

### 9. 文档位置

| 文档 | 路径 | 说明 |
|------|------|------|
| V2.3 计划 | `.claude/docs/video-workflow/VIDEO_WORKFLOW_V2.3_PLAN.md` | 功能规划 |
| V2 报告 | `.claude/docs/video-workflow/VIDEO_WORKFLOW_V2_REPORT.md` | V2 实现报告 |
| 测试报告 | `.claude/docs/video-workflow/VIDEO_WORKFLOW_TEST_REPORT.md` | 测试验证 |
| 改进报告 | `.claude/docs/video-workflow/VIDEO_WORKFLOW_IMPROVEMENT_REPORT.md` | 优化建议 |
| 问题诊断 | `.claude/docs/video-workflow/VIDEO_WORKFLOW_ISSUES.md` | 问题分析 |

---

### 10. Token 优化机制

**常驻 Token**: ~1,200
- CLAUDE.md: 600 (L1 核心技能)
- skills-index.md: 400 (技能索引)
- 新增视频触发词：~200

**按需加载**: ~2,700
- skills-trigger-map.md: 2,500 (L2 扩展词)
- 视频工作流文档：按需读取

**总占用**: ~3,900 tokens（远优于 v5.0 的 ~5,000）

---

## 下一步计划

### P3 优先级（未来改进）
1. **并发任务处理** (--concurrent N) - 同时处理多个任务
2. **进度保存/恢复** (checkpoint) - 支持中断后恢复
3. **Web 界面** - 可视化任务管理
4. **API 接口** - 集成到其他系统
5. **任务优先级** - 支持任务队列优先级
6. **资源监控** - CPU/内存/磁盘监控

---

## 总结

方案 D v6.0 在 v5.0 的基础上：

✅ **保留**: AI 图片生成能力（ModelScope API）  
✅ **新增**: 完整视频生成工作流（V2.3）  
✅ **增强**: 批量任务处理、错误恢复、智能进度  
✅ **优化**: Token 占用从 5000 降至 3900  
✅ **完善**: 横屏视频预设、质量检查、日志记录

**适用场景**:
- 教学视频批量制作
- 产品多语言介绍
- 社交媒体短视频
- 知识分享系列视频

**性能指标**:
- 单个视频 (60 秒): ~5-8 分钟
- 批量任务 (3 个): ~15-20 分钟
- 成功率：>95%（带重试机制）

