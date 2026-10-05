# C4 技能分享与传播 · 交付物预检器（Deliverable Pre-checker）

> Elite20 挑战体系 C4 挑战提交仓库 —— 作者：虞梦琳（yml）

## 这是什么

提交挑战前，30 秒查出「该交什么 / 已交什么 / 缺什么 / 命名对不对 / 有没有踩红线」。

- **输入**：挑战名（C1~C7 / C2A / C9 或别名）+ 文件夹路径
- **输出**：交付物清单逐条 ✅/❌ + 命名警告 + 红线警告

纯 Python 标准库，零第三方依赖，Windows 下直接跑。

## 仓库内容

| 文件/目录 | 说明 |
|---|---|
| `deliverable-prechecker/` | 技能源码（SKILL.md + precheck.py + challenges.yaml + README） |
| `yml_C4_交付物预检器.skill` | 打包好的可安装技能包（tar.gz） |
| `yml_C4_skill说明.md` | 技能说明（解决什么问题、输入输出、使用步骤、真实案例） |
| `yml_C4_教学说明.md` | 教学说明（上手、常见坑、优化技巧） |
| `yml_C4_AI日志.md` | AI 使用日志（怎么指挥 AI、迭代几轮、做了什么） |
| `yml_C4_demo.mp4` | Demo 演示视频 |
| `yml_C4_群发布文案.md` | 群发布文案 |
| `yml_C4_试用反馈表.md` | 试用反馈收集表 |

## 快速开始（1 分钟）

```bash
python deliverable-prechecker/scripts/precheck.py C4 <你的挑战文件夹路径>
```

## C4 交付物（五件套）

按 CHALLENGE.md 要求，5 个必交文件全部齐全：

| 要求 | 文件 | 状态 |
|---|---|---|
| Skill 说明文档 | `yml_C4_skill说明.md` | ✅ |
| 可执行内容 | `yml_C4_交付物预检器.skill` | ✅ |
| Demo | `yml_C4_demo.mp4` | ✅ |
| 教学说明 | `yml_C4_教学说明.md` | ✅ |
| AI 日志 | `yml_C4_AI日志.md` | ✅ |
