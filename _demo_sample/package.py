# -*- coding: utf-8 -*-
"""把 deliverable-prechecker 目录打包成 yml_C4_交付物预检器.skill（zip 归档）。"""
import os
import zipfile

SKILL_DIR = r"D:\.cogseed\userWorkSpace\我的挑战有哪些\C4_技能分享与传播\deliverable-prechecker"
OUT = r"D:\.cogseed\userWorkSpace\我的挑战有哪些\C4_技能分享与传播\yml_C4_交付物预检器.skill"

with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    for root, dirs, files in os.walk(SKILL_DIR):
        for fn in files:
            fp = os.path.join(root, fn)
            rel = os.path.relpath(fp, os.path.dirname(SKILL_DIR))
            z.write(fp, rel)
            print("ADD", rel)

print("WROTE", OUT, os.path.getsize(OUT), "bytes")
