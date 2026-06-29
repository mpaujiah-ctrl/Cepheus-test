import re

path = 'kernel/drivers/kernelsu/core_hook.c'
with open(path, 'r') as f:
    content = f.read()

# Tambah include kalau belum ada
if 'susfs.h' not in content:
    content = content.replace(
        '#include <linux/fs.h>',
        '#include <linux/fs.h>\n#ifdef CONFIG_KSU_SUSFS\n#include <linux/susfs.h>\n#endif',
        1
    )
    print("OK: include susfs.h ditambah")

# Cari fungsi ksu_core_init dengan regex
pattern = r'(void\s+ksu_core_init\s*\(\s*void\s*\)\s*\{)'
replacement = r'\1\n#ifdef CONFIG_KSU_SUSFS\n    susfs_init();\n#endif'

new_content, count = re.subn(pattern, replacement, content)
if count > 0:
    print("OK: susfs_init ditambah ke ksu_core_init")
else:
    print("GAGAL: fungsi ksu_core_init tidak ditemukan")

with open(path, 'w') as f:
    f.write(new_content)
