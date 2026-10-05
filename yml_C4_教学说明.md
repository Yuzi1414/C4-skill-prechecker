# 交付物预检器 · 教学说明（yml_C4）

## 教学目标

让任何一个同学都能：① 用起来（1 分钟跑通）；② 看得懂（理解内部三个文件怎么配合）；③ 改得动（给自己的挑战加规则、或复制思路做自己的小工具）。

## 第一层：用起来（1 分钟）

```bash
python precheck.py --list                      # 看支持哪些挑战
python precheck.py C6 "D:\...\C6文件夹"        # 预检 C6
```

预期：一个「完整文件夹」返回全✅+零红线；一个「缺文件的文件夹」返回❌+`missing_artifacts`红线。看 `_demo_sample/complete` 与 `_demo_sample/gap` 两个对照样例。

## 第二层：内部怎么工作（三文件分工）

| 文件 | 职责 | 修改频率 |
|------|------|----------|
| `SKILL.md` | 元数据 + 使用说明，给 AI/人看 | 低 |
| `scripts/precheck.py` | 通用引擎：读注册表 → 扫文件夹 → 匹配 → 判红线 | 几乎不改 |
| `references/challenges.yaml` | 数据：每个挑战交什么、命名前缀、红线 | 常改（加挑战） |

核心设计：**引擎与数据分离**。加新挑战不动代码，只加数据。

## 第三层：怎么加一个挑战（动手练习）

在 `challenges.yaml` 的 `challenges:` 下加一条：

```yaml
  C9:
    title: "AGI 认知能力 · 基准测试"
    id: "ch-20260717031352-tlg70p"
    name_prefix: "yml_C9"
    aliases: ["基准", "benchmark", "c9"]
    red_lines: ["missing_artifacts", "no_ai_log"]
    required:
      - {"key": "benchmark", "label": "基准 benchmark", "patterns": ["benchmark"], "core": true}
      - {"key": "test_result", "label": "测试结果", "patterns": ["测试结果"], "core": true}
      - {"key": "ai_log", "label": "AI 日志", "patterns": ["ai日志", "ai_log"], "core": false}
```

字段含义：`core: true` = 核心交付物，缺失会触发 `missing_artifacts` 红线；`patterns` = 文件名匹配关键词（大小写不敏感）。

## 关键实现细节（教学要点）

1. **命名检查只看顶层文件**：子目录里的文件（如 `benchmark/` 下的 `README.md`）不强制要求 `yml_Cx_` 前缀，避免误报。
2. **一条红线 = 缺任一核心交付物**：`missing_artifacts` 是「产物完整性」锁低分的触发条件，所以核心缺失必须醒目标红。
3. **极简 YAML 解析**：注册表用内建解析器（双引号字符串、2 空格缩进），避免第三方 yaml 依赖。

## 可复制到你自己的项目

这套「引擎 + YAML 注册表 + 红线告警」的思路，可以迁移到任何「规则清单核对」场景：合同条款检查、简历要件核对、发布 checklist 等——把规则写成数据，引擎保持不变。

## 常见问题

- **Q：为什么不用现成的 TODO 清单？** A：TODO 清单靠人自觉勾选，本工具靠文件名/关键词**自动扫描**，能防漏交。
- **Q：文件命名不规范但内容对，会报吗？** A：会。命名规范本身是评分项，⚠️ 提醒你改。
