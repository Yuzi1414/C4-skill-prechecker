---
name: deliverable-prechecker
description: >
  提交挑战前，检查你的交付物是否齐全、命名是否规范、有没有踩红线。
  输入「挑战名（C1~C7 / C2A / C9）+ 文件夹路径」，输出该交什么 / 缺什么 / 命名警告 / 红线警告。
  触发短语：「预检我的交付物」「检查挑战交付物」「C9 还缺什么」「提交前检查」
  "precheck my deliverables" "what's missing for C9" "check submission folder"。
---

# 交付物预检器 Deliverable Pre-checker

## Purpose
Elite20 每个挑战要交 3~5 个文件，名字有规范、还分核心/次要产物。提交前人工核对容易漏。
本技能把「该交什么」做成数据驱动的注册表，用脚本自动比对文件夹，30 秒告诉你缺什么、命名对不对、有没有踩红线。

## 输入 / 输出
- 输入：挑战标识（C1~C7、C2A、C9，或别名如「论文」「benchmark」）+ 一个文件夹路径
- 输出：① 该交什么 ② 命名规范 ③ 已交了什么（逐条 ✅/❌）④ 缺什么 ⑤ 红线警告

## Workflow
### Step 1 — 确认挑战
先确定用户要检查哪个挑战；不确定时运行 `python scripts/precheck.py --list` 列出所有挑战。
### Step 2 — 运行预检
```
python scripts/precheck.py <挑战> "<文件夹路径>"
```
Windows 路径用双引号包起来；路径含中文没问题（脚本已用 utf-8）。
### Step 3 — 读报告
逐条看 ✅/❌；把「❌ 缺失」和「🔴 红线」原样转述给用户，并给出补交建议。
### Step 4 — 全部 ✅ 再提交
只有核心产物全部 ✅ 且无红线警告，才建议用户提交；否则先补齐。

## Edge Cases
- 挑战名写错/用了别名：脚本自动匹配别名；仍不中则报「未知挑战」并打印可用清单。
- 文件夹不存在或为空：报告「目录为空或不存在」并提示核对路径。
- benchmark 这类「目录型交付物」：脚本把目录名也纳入匹配，不会误报缺失。
- 文件在子目录里：脚本递归扫描；但命名规范只检查顶层文件名（子目录内容不要求带前缀）。
- 一个文件命中多个交付物：逐条列出命中，用户自行确认是否重复/漏拆。

## Examples
- `python scripts/precheck.py C9 "D:/.../C2A_C9_AGI认知能力"` → 检查 C9 五个交付物
- `python scripts/precheck.py 论文 "D:/.../C2_AI4Math"` → 用别名「论文」检查 C2
- `python scripts/precheck.py --all "D:/.../某文件夹"` → 判断这个文件夹到底对应哪个挑战

## 注册表（新增挑战）
编辑 `references/challenges.yaml`：复制一个已有挑战条目，改 title / id / name_prefix / required 即可，不用改代码。
