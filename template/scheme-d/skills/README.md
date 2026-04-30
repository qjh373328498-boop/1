# Skills 备份目录

本目录包含所有已安装的 MonkeyCode Skills 备份，用于快速恢复和迁移。

## 目录结构

```
skills/
├── baoyu-*              # 宝玉系列 skills (内容创作/发布)
├── brainstorming        # 头脑风暴 skill
├── content-publish-workflow  # 工作流 skills
├── debug-troubleshoot-workflow
├── knowledge-manage-workflow
├── research-paper-workflow
├── software-dev-workflow
├── pdf                  # 文档处理 skills
├── docx
├── xlsx
├── pptx
└── ...                  # 其他 skills
```

## 总计

- **Skills 总数**: 73 个
- **官方 Skills**: 68 个 (来自 MonkeyCode Official Plugins、Anthropic Official Skills、obra/superpowers、JimLiu/baoyu-skills)
- **自定义工作流**: 5 个 (research-paper-workflow, software-dev-workflow, content-publish-workflow, debug-troubleshoot-workflow, knowledge-manage-workflow)

## 恢复方法

如果需要恢复 skills，将所有子目录复制到 `~/.claude/skills/` 目录即可：

```bash
# 备份恢复示例
cp -r skills/* ~/.claude/skills/
```

## Skills 分类

### 内容创作与发布
- baoyu-cover-image - 封面图生成
- baoyu-article-illustrator - 文章配图
- baoyu-diagram - 流程图/架构图
- baoyu-infographic - 信息图表
- baoyu-slide-deck - PPT 生成
- baoyu-post-to-wechat - 微信公众号发布
- baoyu-post-to-weibo - 微博发布
- baoyu-post-to-x - Twitter/X 发布
- baoyu-xhs-images - 小红书卡片图生成

### 文档处理
- baoyu-url-to-markdown - 网页转 Markdown
- baoyu-youtube-transcript - YouTube 字幕下载
- baoyu-translate - 翻译
- baoyu-format-markdown - Markdown 格式化
- baoyu-markdown-to-html - Markdown 转 HTML
- pdf - PDF 文档处理
- docx - Word 文档处理
- xlsx - Excel 表格处理
- pptx - PPT 处理

### 工作流 Skills
- research-paper-workflow - 学术研究/论文写作工作流
- software-dev-workflow - 软件开发全流程工作流
- content-publish-workflow - 内容创作与发布工作流
- debug-troubleshoot-workflow - 调试与问题解决工作流
- knowledge-manage-workflow - 文档处理与知识管理工作流

### 开发辅助
- brainstorming - 头脑风暴与需求探索
- deploy-website - 网站部署与预览

## 更新日期

最后更新：2026-04-28
