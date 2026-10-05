#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""交付物预检器 Deliverable Pre-checker

输入一个挑战（C1~C7、C2A、C9 等）+ 一个文件夹路径，输出五件事：
  ① 该交什么  ② 命名规范  ③ 已交了什么  ④ 缺什么  ⑤ 红线警告

纯标准库实现，零第三方依赖，可独立运行：
  python precheck.py C9  "D:/.../C2A_C9_AGI认知能力"
  python precheck.py --list
  python precheck.py --all "D:/.../某个文件夹"
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REGISTRY = os.path.normpath(os.path.join(HERE, "..", "references", "challenges.yaml"))

RED_LINE_HINT = {
    "missing_artifacts": "缺核心交付物 → 产物完整性可能被锁在低分",
    "no_ai_log": "无 AI 日志 → 复盘/AI 使用栏可能被锁在低分",
    "one_shot_ai": "疑似一句话直接交（文件过少）→ AI 使用栏可能被锁在低分",
}


# ---------------- 极简 YAML 子集解析器 ----------------
def _scalar(s):
    s = s.strip()
    if s in ("", "null", "~"):
        return None
    if s == "true":
        return True
    if s == "false":
        return False
    if len(s) >= 2 and s[0] == s[-1] and s[0] in "\"'":
        return s[1:-1]
    try:
        return int(s)
    except ValueError:
        try:
            return float(s)
        except ValueError:
            return s


def _flow(s):
    try:
        return json.loads(s)
    except Exception:
        return _scalar(s)


def _strip_comment(line):
    in_q = False
    for i, ch in enumerate(line):
        if ch == '"':
            in_q = not in_q
        elif ch == "#" and not in_q:
            return line[:i].rstrip()
    return line


def _parse_block(lines, i, indent):
    mapping, listing = {}, []
    while i < len(lines):
        raw = lines[i]
        if not raw.strip():
            i += 1
            continue
        cur = len(raw) - len(raw.lstrip())
        if cur < indent:
            break
        if cur > indent:
            i += 1
            continue
        content = raw.strip()
        if content.startswith("- "):
            item = content[2:].strip()
            listing.append(_flow(item) if item[:1] in "[{" else _scalar(item))
            i += 1
            continue
        if ":" in content:
            k, v = content.split(":", 1)
            k, v = k.strip(), v.strip()
            if v == "":
                nxt = lines[i + 1] if i + 1 < len(lines) else ""
                nxt_ind = len(nxt) - len(nxt.lstrip()) if nxt.strip() else indent
                if nxt.strip() and nxt_ind > indent:
                    sub, i = _parse_block(lines, i + 1, nxt_ind)
                    mapping[k] = sub
                    continue
                mapping[k] = None
            else:
                mapping[k] = _flow(v) if v[:1] in "[{" else _scalar(v)
            i += 1
            continue
        listing.append(_scalar(content))
        i += 1
    return mapping if mapping else listing, i


def load_registry(path):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    lines = [_strip_comment(ln) for ln in text.splitlines()]
    lines = [ln for ln in lines if ln.strip()]
    data, _ = _parse_block(lines, 0, 0)
    if isinstance(data, dict) and "challenges" in data:
        return data["challenges"]
    return data or {}


# ---------------- 文件扫描 ----------------
def list_entries(folder):
    entries = []
    for root, dirs, files in os.walk(folder):
        for d in dirs:
            rel = os.path.relpath(os.path.join(root, d), folder)
            entries.append((rel, d, True))
        for fn in files:
            rel = os.path.relpath(os.path.join(root, fn), folder)
            entries.append((rel, fn, False))
    return entries


def match(entries, patterns):
    hits = []
    for rel, name, is_dir in entries:
        low = name.lower()
        for p in patterns:
            if p.lower() in low:
                hits.append((rel, name, is_dir))
                break
    return hits


# ---------------- 挑战解析 ----------------
def norm(s):
    return "".join(ch for ch in s.lower() if ch.isalnum())


def resolve_challenge(challenges, token):
    t = norm(token)
    for key, ch in challenges.items():
        if norm(key) == t:
            return key, ch
    for key, ch in challenges.items():
        for a in ch.get("aliases", []):
            if norm(a) == t:
                return key, ch
    return None, None


def has_ai_log(entries):
    for _, name, _ in entries:
        low = name.lower()
        if "ai日志" in low or "ai_log" in low:
            return True
    return False


# ---------------- 主检查 ----------------
def check(ch_key, ch, folder):
    entries = list_entries(folder)
    required = ch.get("required", [])
    prefix = ch.get("name_prefix", "")
    red_lines = set(ch.get("red_lines", []))

    print("=" * 62)
    print("交付物预检：{}（{}）".format(ch_key, ch.get("title", "")))
    print("=" * 62)
    print("目录：{}".format(folder))
    print("扫描到 {} 个条目（含子目录）".format(len(entries)))
    if prefix:
        print("命名前缀：{}_*.md / {}_*".format(prefix, prefix))
    print()

    print("【① 该交什么】")
    print("-" * 62)
    for it in required:
        tag = "核心" if it.get("core") else "次要"
        print("  [{}] {} — {}".format(tag, it.get("key"), it.get("label", "")))

    print()
    print("【② 已交 / 缺失】")
    print("-" * 62)
    missing_core, missing_minor = [], []
    naming_warn = []
    for it in required:
        hits = match(entries, it.get("patterns", []))
        label = it.get("label", it.get("key"))
        if hits:
            shown = "、".join(h[1] for h in hits[:3])
            more = " 等 {} 个".format(len(hits)) if len(hits) > 3 else ""
            print("  ✅ {} → 命中：{}{}".format(label, shown, more))
            for rel, name, is_dir in hits:
                if prefix and not is_dir and os.sep not in rel and prefix.lower() not in name.lower():
                    naming_warn.append(name)
        elif it.get("core"):
            missing_core.append(it)
            print("  ❌ {} 【核心·缺失】".format(label))
        else:
            missing_minor.append(it)
            print("  ⚠️  {} 【次要·缺失】".format(label))

    print()
    print("【③ 红线警告】")
    print("-" * 62)
    fired = []
    if missing_core and "missing_artifacts" in red_lines:
        fired.append("missing_artifacts")
    if "no_ai_log" in red_lines and not has_ai_log(entries):
        fired.append("no_ai_log")
    if "one_shot_ai" in red_lines and len(entries) <= 1:
        fired.append("one_shot_ai")
    if not fired:
        print("  ✅ 未触发红线")
    for f in fired:
        print("  🔴 {}：{}".format(f, RED_LINE_HINT.get(f, "")))

    if naming_warn:
        print()
        print("【④ 命名不规范】")
        print("-" * 62)
        for n in sorted(set(naming_warn)):
            print("  ⚠️  {}（未带前缀 {}）".format(n, prefix))

    n_core = sum(1 for it in required if it.get("core"))
    n_core_ok = n_core - len(missing_core)
    print()
    print("【小结】核心 {} 项：交 {} / 缺 {}；次要缺失 {} 项；红线 {} 条".format(
        n_core, n_core_ok, len(missing_core), len(missing_minor), len(fired)))
    if not missing_core and not fired:
        print("👉 预检通过，可以提交（仍请人工复核内容质量）。")
    else:
        print("👉 建议先补齐上述 ❌/🔴 再提交。")
    print("=" * 62)


def cmd_list(challenges):
    print("可用挑战：")
    for key, ch in challenges.items():
        alias = "、".join(ch.get("aliases", []))
        print("  {} — {}  [别名: {}]".format(key, ch.get("title", ""), alias or "—"))


def cmd_all(challenges, folder):
    entries = list_entries(folder)
    if not entries:
        print("目录为空或不存在：{}".format(folder))
        return
    print("目录 {} 共 {} 个条目，匹配结果：".format(folder, len(entries)))
    scores = []
    for key, ch in challenges.items():
        found = 0
        for it in ch.get("required", []):
            if match(entries, it.get("patterns", [])):
                found += 1
        if found:
            scores.append((found, key, ch))
    scores.sort(key=lambda x: -x[0])
    if not scores:
        print("  未匹配到任何已知挑战的交付物，请核对文件或补充注册表。")
        return
    for found, key, ch in scores:
        print("  {} — {}：命中 {} 项".format(key, ch.get("title", ""), found))


def main(argv):
    if not os.path.exists(REGISTRY):
        print("找不到注册表：{}".format(REGISTRY))
        return 2
    challenges = load_registry(REGISTRY)
    if not challenges:
        print("注册表为空或解析失败：{}".format(REGISTRY))
        return 2

    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    if argv[0] == "--list":
        cmd_list(challenges)
        return 0
    if argv[0] == "--all":
        if len(argv) < 2:
            print("用法：python precheck.py --all \"<文件夹>\"")
            return 2
        cmd_all(challenges, argv[1])
        return 0

    token = argv[0]
    folder = argv[1] if len(argv) > 1 else "."
    key, ch = resolve_challenge(challenges, token)
    if key is None:
        print("未知挑战：{}".format(token))
        cmd_list(challenges)
        return 2
    if not os.path.isdir(folder):
        print("文件夹不存在：{}".format(folder))
        return 2
    check(key, ch, folder)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
