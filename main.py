#!/usr/bin/env python3
"""Copy the committed front page (entry.png) to the output directory."""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

os.makedirs(OUT, exist_ok=True)
shutil.copyfile(os.path.join(HERE, "entry.png"), os.path.join(OUT, "entry.png"))
print("wrote", os.path.join(OUT, "entry.png"))
