#!/usr/bin/env python3
import re
from pathlib import Path
from collections import defaultdict

ALL_CHARS = [
    'peppa-pig-happy-standing', 'george-standing', 'daddy-pig-standing',
    'daddy-pig-walking', 'mummy-pig-standing-grass', 'candy-cat-green-dress',
    'emily-elephant-standing', 'peppa-pig-red-polka-dot-dress', 'peppa-fairy-princess',
    'george-superhero-costume', 'peppa-family-group-outdoors', 'peppa-and-george-ooo',
    'george_pig_dinosaur', 'george-playing-ball'
]

def fix_file(path):
    content = path.read_text(encoding='utf-8')
    lines = content.split('\n')
    
    # 找所有角色使用（行号+角色名）
    uses = []
    for i, line in enumerate(lines):
        m = re.search(r'assets/peppa/([^"]+)\.png', line)
        if m:
            uses.append((i, m.group(1)))
    
    # 统计每个角色出现次数
    char_count = defaultdict(list)
    for line_no, char in uses:
        char_count[char].append(line_no)
    
    # 找重复角色
    dups = {c: lines for c, lines in char_count.items() if len(lines) >= 2}
    if not dups:
        return False
    
    # 找未使用角色
    used = set(char_count.keys())
    unused = [c for c in ALL_CHARS if c not in used]
    
    if not unused:
        return False
    
    # 替换：保留第1次，替换第2次及以后
    modified = False
    for char, line_nos in dups.items():
        for line_no in line_nos[1:]:  # 跳过第1次
            if not unused:
                break
            new_char = unused.pop(0)
            old = f'assets/peppa/{char}.png'
            new = f'assets/peppa/{new_char}.png'
            lines[line_no] = lines[line_no].replace(old, new)
            modified = True
    
    if modified:
        path.write_text('\n'.join(lines), encoding='utf-8')
    return modified

fixed = 0
for f in sorted(Path('lessons').rglob('*.html')):
    if fix_file(f):
        print(f"✅ {f.relative_to('lessons')}")
        fixed += 1

print(f"\n✅ 修复 {fixed} 个文件")
