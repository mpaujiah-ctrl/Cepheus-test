#!/usr/bin/env python3
import re

path = "kernel/drivers/kernelsu/core_hook.c"

with open(path, "r") as f:
    lines = f.readlines()

out = []
found_include = False
inside_core_init = False
inserted_init = False

for line in lines:
    # pastikan include susfs.h ada
    if "#include <linux/susfs.h>" in line:
        found_include = True
    if line.startswith("#include") and not found_include:
        out.append("#include <linux/susfs.h>\n")
        found_include = True

    # deteksi awal fungsi ksu_core_init
    if re.match(r"\s*void\s+ksu_core_init\s*\(", line):
        inside_core_init = True

    # kalau sudah di dalam ksu_core_init, cari sebelum '}' terakhir
    if inside_core_init and re.match(r"\s*}\s*", line) and not inserted_init:
        out.append("    susfs_init();\n")
        inserted_init = True
        inside_core_init = False

    out.append(line)

with open(path, "w") as f:
    f.writelines(out)

# 🔎 Pengecekan hasil patch
with open(path, "r") as f:
    content = f.read()

funcs = re.findall(r'void\s+\w+\s*\(void\)', content)
print("Fungsi void di core_hook.c:", funcs[:10])

if "susfs_init();" in content:
    print("✅ susfs_init SUDAH ADA di ksu_core_init")
else:
    print("❌ susfs_init BELUM ADA")
