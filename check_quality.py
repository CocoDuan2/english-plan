#!/usr/bin/env python3
import re
from pathlib import Path

files = [
    'lessons/phonics-2/ip-family/teach.html',
    'lessons/phonics-2/ip-family/review.html',
    'lessons/phonics-4/bl-blend/teach.html',
    'lessons/phonics-4/bl-blend/review.html',
    'lessons/phonics-2/ig-family/teach.html',
    'lessons/phonics-2/ig-family/review.html',
]

results = []

for f in files:
    path = Path(f)
    if not path.exists():
        results.append(f'{f}: ❌ 文件不存在')
        continue
    
    content = path.read_text()
    
    # 1. 移动端CSS
    has_mobile = '@media(max-width:480px)' in content or '@media (max-width:480px)' in content
    
    # 2. 音效函数
    has_playOk = 'function playOk()' in content or 'function playOk(' in content
    has_playNo = 'function playNo()' in content or 'function playNo(' in content
    has_speak = 'function speak(' in content
    
    # 3. audioCache (review only)
    has_audioCache = 'audioCache' in content if 'review' in f else True
    
    # 4. 角色重复检查（同课内≥3次）
    roles = re.findall(r'assets/peppa/([\w-]+)\.png', content)
    role_counts = {}
    for r in roles:
        role_counts[r] = role_counts.get(r, 0) + 1
    max_repeat = max(role_counts.values()) if role_counts else 0
    
    # 5. flex-wrap (teach only, 有blend-box的)
    has_flex_wrap = True
    if 'teach' in f and 'blend-box' in content:
        has_flex_wrap = 'flex-wrap:wrap' in content
    
    issues = []
    if not has_mobile: issues.append('缺少移动端CSS')
    if not has_playOk: issues.append('缺少playOk')
    if not has_playNo: issues.append('缺少playNo')
    if not has_speak: issues.append('缺少speak')
    if not has_audioCache: issues.append('缺少audioCache')
    if max_repeat >= 3: issues.append(f'角色重复{max_repeat}次')
    if not has_flex_wrap: issues.append('缺少flex-wrap')
    
    status = '✅' if not issues else '❌'
    results.append(f'{path.name}: {status} {" | ".join(issues) if issues else "完美"}')

print('\n'.join(results))
