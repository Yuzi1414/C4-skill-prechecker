# C4 技能分享 · 群发布文案（yml）

> 直接复制下面这段发到 Elite20 群即可。发完把「试用反馈表」一起丢群里，方便收集真实反馈。

---

大家好，这是我的 C4 技能——**交付物预检器 Deliverable Pre-checker** 🎯

> **输入**：挑战名（C1~C7 / C2A / C9 或别名）+ 你的文件夹路径
> **输出**：该交什么 / 已交什么 / 缺什么 / 命名对不对 / 有没有踩红线

**为什么有用**：每个挑战都要交 3~5 个文件，名字有规范、还分核心/次要、踩红线（缺核心交付物）会锁低分。人工核对必漏——这个工具 30 秒自动扫一遍，提交前先抓出漏交和命名错误。

**怎么用（1 分钟，零依赖）**：

```bash
python scripts/precheck.py --list                    # 看支持哪些挑战
python scripts/precheck.py C6 "D:\...\C6文件夹"      # 预检 C6
python scripts/precheck.py 论文 "D:\...\C2_AI4Math"   # 别名也认
```

纯 Python 标准库，不用装任何东西，Windows 直接跑。

**已支持 8 个挑战**：C1 / C2 / C2A / C3 / C4 / C6 / C7 / C9。

欢迎大家试用，跑完顺手填一下反馈表（30 秒）——哪一步卡住了、报得准不准、还想要哪个挑战，我根据反馈迭代 v2！🙏

---
📦 文件：`deliverable-prechecker/`（SKILL.md + precheck.py + challenges.yaml + README.md）
