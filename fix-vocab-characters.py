#!/usr/bin/env python3
import os
import re
from collections import defaultdict

CHARACTERS = [
    'peppa-pig-happy-standing', 'george-standing', 'daddy-pig-standing',
    'daddy-pig-walking', 'mummy-pig-standing-grass', 'candy-cat-green-dress',
    'emily-elephant-standing', 'peppa-pig-red-polka-dot-dress', 'peppa-fairy-princess',
    'george-superhero-costume', 'peppa-family-group-outdoors', 'peppa-and-george-ooo',
    'george_pig_dinosaur', 'george-playing-ball'
]

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 记录每个角色第一次出现的行号
    char_first_line = {}
    char_usage = defaultdict(list)
    
    for i, line in enumerate(lines):
        matches = re.findall(r'assets/peppa/([^"]+)\.png', line)
        for char in matches:
            char_usage[char].append(i)
            if char not in char_first_line:
                char_first_line[char] = i
    
    # 找出重复≥3次的角色
    duplicates = {char: lines_list for char, lines_list in char_usage.items() if len(lines_list) >= 3}
    
    if not duplicates:
        return False
    
    print(f"\n修复: {filepath}")
    
    # 获取已使用的角色
    used_chars = set(char_usage.keys())
    available = [c for c in CHARACTERS if c not in used_chars]
    
    # 替换：保留第一次，替换后续
    for char, line_nums in duplicates.items():
        print(f"  {char}: {len(line_nums)}次", end='')
        first_line = char_first_line[char]
        
        for line_num in line_nums:
            if line_num != first_line and available:
                replacement = available.pop(0)
                lines[line_num] = lines[line_num].replace(
                    f'assets/peppa/{char}.png',
                    f'assets/peppa/{replacement}.png'
                )
                print(f" → {replacement}", end='')
        print()
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    return True

fixed = 0
for level in ['level-1', 'level-2', 'level-3', 'level-4']:
    path = f'lessons/{level}'
    if not os.path.exists(path):
        continue
    for folder in os.listdir(path):
        for file in ['teach.html', 'review.html']:
            fp = os.path.join(path, folder, file)
            if os.path.exists(fp) and fix_file(fp):
                fixed += 1

print(f"\n✅ 修复完成: {fixed} 个文件")
