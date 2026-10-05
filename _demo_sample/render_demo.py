# -*- coding: utf-8 -*-
"""把 precheck.py 的真实输出渲染成终端风格 demo.mp4（确定性回放，非实时录屏）。"""
import os
import textwrap
import imageio_ffmpeg
import imageio.v2 as iio
import numpy as np
from PIL import Image, ImageDraw, ImageFont

BASE = r"D:\.cogseed\userWorkSpace\我的挑战有哪些\C4_技能分享与传播\_demo_sample"
OUT = r"D:\.cogseed\userWorkSpace\我的挑战有哪些\C4_技能分享与传播\yml_C4_demo.mp4"

W, H = 1280, 720
FPS = 30
BG = (13, 17, 23)
FG = (201, 209, 217)
GREEN = (63, 185, 80)
YELLOW = (210, 153, 34)
RED = (248, 81, 73)
CYAN = (88, 166, 255)
DIM = (110, 118, 129)

FONT = r"C:\Windows\Fonts\msyh.ttc"
def f(sz):
    return ImageFont.truetype(FONT, sz, index=0)

TITLE_F = f(46)
SUB_F = f(24)
BODY_F = f(24)
CMD_F = f(26)

def wrap(text, font, maxw):
    out = []
    for line in text.split("\n"):
        if not line.strip():
            out.append("")
            continue
        # 逐字符折行
        cur = ""
        for ch in line:
            t = cur + ch
            if font.getlength(t) <= maxw:
                cur = t
            else:
                out.append(cur)
                cur = ch
        out.append(cur)
    return out

def colorize(line):
    if line.startswith("🔴") or "missing_artifacts" in line:
        return RED
    if line.startswith("✅") or line.startswith("👉"):
        return GREEN
    if line.startswith("❌"):
        return RED
    if line.startswith("⚠️"):
        return YELLOW
    if line.startswith("【") or line.startswith("===") or line.startswith("--"):
        return CYAN
    if line.startswith("  ["):
        return YELLOW
    return FG

def draw_text(draw, x, y, text, font, fill):
    draw.text((x, y), text, font=font, fill=fill)

def scene_title(draw):
    draw.rectangle([0, 0, W, H], fill=BG)
    draw_text(draw, W//2, 240, "C4 技能 Demo", TITLE_F, CYAN)
    draw_text(draw, W//2, 320, "交付物预检器 · 提交前必查", SUB_F, FG)
    draw_text(draw, W//2, 400, "python precheck.py <挑战> <文件夹>", SUB_F, DIM)
    draw_text(draw, W//2, 450, "纯标准库 · 数据驱动 · 红线告警", SUB_F, DIM)

def scene_cmd_header(draw, cmd):
    draw.rectangle([0, 0, W, H], fill=BG)
    draw.rectangle([0, 0, W, 56], fill=(22, 27, 34))
    draw_text(draw, 40, 12, "> " + cmd, CMD_F, GREEN)

def load_lines(path):
    with open(path, encoding="utf-8") as fp:
        raw = fp.read()
    return raw.split("\n")

def render_block(draw, lines, maxh, top=72):
    """把一组行渲染进画面，超长滚动；返回已渲染行数。"""
    y = top
    for ln in lines:
        c = colorize(ln)
        draw_text(draw, 40, y, ln, BODY_F, c)
        y += 34

def make_scene(cmd, filepath, hold=24):
    header = ["命令：" + cmd]
    body_lines = load_lines(filepath)
    # 去掉空行、折叠过长行
    flat = []
    maxw = W - 80
    for ln in body_lines:
        flat.extend(wrap(ln, BODY_F, maxw))
    frames = []
    # 逐行揭示
    for i in range(1, len(flat) + 1):
        img = Image.new("RGB", (W, H), BG)
        d = ImageDraw.Draw(img)
        scene_cmd_header(d, cmd)
        visible = flat[:i]
        y = 72
        for ln in visible[-20:]:  # 最多显示 20 行，超出顶部滚动
            d.text((40, y), ln, font=BODY_F, fill=colorize(ln))
            y += 34
        frames.append(np.array(img))
    # 停留
    last = frames[-1]
    for _ in range(hold):
        frames.append(last)
    return frames

def main():
    scenes = []
    # 开场
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    scene_title(d)
    scenes.extend([np.array(img)] * 45)

    # --list
    scenes.extend(make_scene("python precheck.py --list", os.path.join(BASE, "capture_list.txt")))
    # gap
    scenes.extend(make_scene("python precheck.py C6 _demo_sample/gap", os.path.join(BASE, "capture_gap.txt")))
    # complete
    scenes.extend(make_scene("python precheck.py C6 _demo_sample/complete", os.path.join(BASE, "capture_complete.txt")))

    # 结尾
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, H], fill=BG)
    d.text((W//2, 260), "预检通过 = 五件套齐全 + 命名规范 + 零红线", font=SUB_F, fill=GREEN)
    d.text((W//2, 330), "缺核心交付物 → 自动触发 missing_artifacts 红线", font=SUB_F, fill=RED)
    d.text((W//2, 410), "数据驱动：加挑战只需改 challenges.yaml，零代码", font=SUB_F, fill=CYAN)
    scenes.extend([np.array(img)] * 60)

    writer = iio.get_writer(OUT, fps=FPS, codec="libx264", quality=8)
    for fr in scenes:
        writer.append_data(fr)
    writer.close()
    print("WROTE", OUT, len(scenes), "frames", round(len(scenes)/FPS, 1), "s")

if __name__ == "__main__":
    main()
