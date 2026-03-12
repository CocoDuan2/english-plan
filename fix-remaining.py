#!/usr/bin/env python3
from pathlib import Path
import re

files_to_fix = [
    ('phonics-3/a-e-magic/teach.html', 'peppa-pig-happy-standing', 369),
    ('phonics-3/i-e-magic/teach.html', 'peppa-pig-happy-standing', 369),
    ('phonics-3/i-e-magic/teach.html', 'peppa-fairy-princess', 219),
    ('phonics-3/o-e-magic/teach.html', 'peppa-pig-happy-standing', 369),
    ('phonics-3/u-e-magic/teach.html', 'peppa-pig-happy-standing', 369),
    ('phonics-5/aw-au/teach.html', 'peppa-pig-happy-standing', 369),
    ('phonics-5/aw-au/teach.html', 'peppa-and-george-ooo', 219),
    ('phonics-5/ew-sound/teach.html', 'peppa-pig-happy-standing', 369),
    ('phonics-5/ew-sound/teach.html', 'george-playing-ball', 219),
    ('phonics-5/ie-sound/teach.html', 'george-standing', 369),
    ('phonics-5/ie-sound/teach.html', 'peppa-family-group-outdoors', 219),
    ('level-1/family-photo/teach.html', 'multiple', 0),
]

unused_pool = ['george-superhero-costume', 'peppa-and-george-ooo', 'george_pig_dinosaur', 
               'george-playing-ball', 'candy-cat-green-dress', 'emily-elephant-standing']

for filepath, dup_char, line_no in files_to_fix:
    path = Path('lessons') / filepath
    if not path.exists():
        continue
    
    if dup_char == 'multiple':
        # family-photo特殊处理（教学家庭成员，重复是正常的）
        continue
    
    lines = path.read_text(encoding='utf-8').split('\n')
    
    # 找到该角色的所有出现
    occurrences = []
    for i, line in enumerate(lines, 1):
        if f'assets/peppa/{dup_char}.png' in line:
            occurrences.append(i)
    
    if len(occurrences) < 2:
        continue
    
    # 替换第2次出现（保留第1次）
    target_line = occurrences[1] - 1  # 转为0-based索引
    if unused_pool:
        new_char = unused_pool.pop(0)
        lines[target_line] = lines[target_line].replace(
            f'assets/peppa/{dup_char}.png',
            f'assets/peppa/{new_char}.png'
        )
        path.write_text('\n'.join(lines), encoding='utf-8')
        print(f"✅ {filepath}: {dup_char} → {new_char}")

print("\n✅ 修复完成")
