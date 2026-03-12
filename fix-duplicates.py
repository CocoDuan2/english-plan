#!/usr/bin/env python3
import re
import os
from pathlib import Path

# 可用角色池
ALL_CHARS = [
    "peppa-pig-happy-standing",
    "peppa-pig-red-polka-dot-dress",
    "peppa-fairy-princess",
    "george-standing",
    "george-superhero-costume",
    "george-playing-ball",
    "george_pig_dinosaur",
    "daddy-pig-standing",
    "daddy-pig-walking",
    "mummy-pig-standing-grass",
    "emily-elephant-standing",
    "candy-cat-green-dress",
    "peppa-family-group-outdoors",
    "peppa-and-george-ooo"
]

def fix_file(filepath):
    """修复单个文件的角色重复"""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 统计每个角色出现的行号
    char_lines = {}
    for i, line in enumerate(lines):
        for char in ALL_CHARS:
            if f'{char}.png' in line:
                if char not in char_lines:
                    char_lines[char] = []
                char_lines[char].append(i)
    
    # 找出重复的角色（出现>=2次）
    duplicates = {char: lines_list for char, lines_list in char_lines.items() if len(lines_list) >= 2}
    
    if not duplicates:
        return False
    
    # 找出未使用的角色
    used_chars = set(char_lines.keys())
    unused_chars = [c for c in ALL_CHARS if c not in used_chars]
    
    # 替换策略：保留第一次出现，替换后续出现
    replacements = []
    unused_idx = 0
    
    for char, line_nums in duplicates.items():
        # 跳过第一次出现，替换后续的
        for line_num in line_nums[1:]:
            if unused_idx < len(unused_chars):
                old_char = char
                new_char = unused_chars[unused_idx]
                replacements.append((line_num, old_char, new_char))
                unused_idx += 1
    
    # 执行替换
    for line_num, old_char, new_char in replacements:
        lines[line_num] = lines[line_num].replace(f'{old_char}.png', f'{new_char}.png')
    
    # 写回文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    return True

# 修复所有 P1-P26
base_dir = Path('lessons/phonics-1')
fixed_count = 0

for letter_dir in sorted(base_dir.glob('letter-*')):
    teach_file = letter_dir / 'teach.html'
    if teach_file.exists():
        if fix_file(teach_file):
            fixed_count += 1
            print(f'✅ {letter_dir.name}')

print(f'\n🎉 共修复 {fixed_count} 个课件')
