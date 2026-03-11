#!/usr/bin/env python3
import re
import os
from pathlib import Path

# 角色池（14个角色轮换使用）
CHARS = [
    "peppa-pig-red-polka-dot-dress.png",
    "george-superhero-costume.png", 
    "candy-cat-green-dress.png",
    "daddy-pig-walking.png",
    "mummy-pig-standing-grass.png",
    "emily-elephant-standing.png",
    "george_pig_dinosaur.png",
    "peppa-fairy-princess.png",
    "peppa-and-george-ooo.png",
    "george-playing-ball.png",
    "daddy-pig-standing.png",
    "george-standing.png",
    "peppa-pig-happy-standing.png",
    "peppa-family-group-outdoors.png"
]

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 找到所有 <img src="../../../assets/peppa/XXX.png"
    pattern = r'<img src="../../../assets/peppa/([^"]+)"'
    matches = list(re.finditer(pattern, content))
    
    if len(matches) < 5:
        return False
    
    # 统计使用次数
    from collections import Counter
    usage = Counter(m.group(1) for m in matches)
    most_common = usage.most_common(1)[0]
    
    if most_common[1] < 5:
        return False
    
    print(f"  修复 {filepath.name}: {most_common[0]} 用了 {most_common[1]} 次")
    
    # 替换策略：保留 S1/S12，其他页面轮换
    replacements = []
    char_idx = 0
    
    for i, match in enumerate(matches):
        old_char = match.group(1)
        # S1 (Title) 和 S12 (All Together) 可以保留
        if i == 0 or i == len(matches) - 2:
            continue
        # 如果是过度使用的角色，替换
        if old_char == most_common[0]:
            new_char = CHARS[char_idx % len(CHARS)]
            replacements.append((match.start(1), match.end(1), new_char))
            char_idx += 1
    
    # 从后往前替换（避免位置偏移）
    for start, end, new_char in reversed(replacements):
        content = content[:start] + new_char + content[end:]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

# 扫描并修复
base = Path('lessons')
fixed = 0

for level in ['phonics-2', 'phonics-3', 'phonics-4', 'phonics-5']:
    level_path = base / level
    if not level_path.exists():
        continue
    
    print(f"\n=== {level} ===")
    for lesson_dir in sorted(level_path.iterdir()):
        if lesson_dir.is_dir():
            teach_file = lesson_dir / 'teach.html'
            if teach_file.exists():
                if fix_file(teach_file):
                    fixed += 1

print(f"\n✅ 修复完成：{fixed} 个文件")
