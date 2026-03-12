#!/usr/bin/env python3
"""修复课件中同课内角色重复使用的问题"""
import re
import sys
from pathlib import Path
from collections import Counter

# 所有可用角色
ALL_CHARS = [
    'peppa-pig-happy-standing',
    'george-standing',
    'daddy-pig-standing',
    'daddy-pig-walking',
    'mummy-pig-standing-grass',
    'candy-cat-green-dress',
    'emily-elephant-standing',
    'peppa-pig-red-polka-dot-dress',
    'peppa-fairy-princess',
    'george-superhero-costume',
    'peppa-family-group-outdoors',
    'peppa-and-george-ooo',
    'george_pig_dinosaur',
    'george-playing-ball'
]

def fix_file(filepath):
    """修复单个文件的角色重复"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 找出所有角色使用
    pattern = r'assets/peppa/([^"]+\.png)'
    matches = re.findall(pattern, content)
    
    # 统计重复
    counter = Counter(matches)
    duplicates = {char: count for char, count in counter.items() if count >= 2}
    
    if not duplicates:
        return False
    
    # 找出已使用的角色（去重）
    used_chars = set(m.replace('.png', '') for m in matches)
    
    # 找出未使用的角色
    unused = [c for c in ALL_CHARS if c not in used_chars]
    
    if not unused:
        print(f"  ⚠️  {filepath.name}: 所有角色已用完，无法完全去重")
        return False
    
    # 替换重复角色（保留第一次出现，替换后续）
    modified = False
    for dup_char, count in duplicates.items():
        char_name = dup_char.replace('.png', '')
        # 找到所有出现位置
        positions = []
        for m in re.finditer(rf'assets/peppa/{re.escape(dup_char)}', content):
            positions.append(m.start())
        
        # 替换第2次及以后的出现
        for i in range(1, len(positions)):
            if not unused:
                break
            replacement = unused.pop(0)
            # 从后往前替换，避免位置偏移
            old_path = f'assets/peppa/{dup_char}'
            new_path = f'assets/peppa/{replacement}.png'
            
            # 找到第i次出现的位置并替换
            parts = content.split(old_path)
            if len(parts) > i:
                content = old_path.join(parts[:i+1]) + new_path + old_path.join(parts[i+1:])
                modified = True
    
    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    lessons_dir = Path('lessons')
    fixed_count = 0
    
    for html_file in sorted(lessons_dir.rglob('*.html')):
        if fix_file(html_file):
            print(f"✅ {html_file.relative_to(lessons_dir)}")
            fixed_count += 1
    
    print(f"\n修复完成：{fixed_count} 个文件")

if __name__ == '__main__':
    main()
