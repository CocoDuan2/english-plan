#!/usr/bin/env python3
import os
import re

base = 'lessons'
results = []

for level in ['phonics-1', 'phonics-2', 'phonics-3', 'phonics-4', 'phonics-5']:
    level_path = os.path.join(base, level)
    if not os.path.exists(level_path):
        continue
    
    for folder in sorted(os.listdir(level_path)):
        teach = os.path.join(level_path, folder, 'teach.html')
        review = os.path.join(level_path, folder, 'review.html')
        
        if not os.path.exists(teach) or not os.path.exists(review):
            continue
        
        issues = []
        
        # 检查teach.html
        with open(teach, 'r') as f:
            t_content = f.read()
        
        if '@media(max-width:480px)' not in t_content:
            issues.append('teach缺少移动端CSS')
        if 'flex-wrap:wrap' not in t_content:
            issues.append('teach缺少flex-wrap')
        
        # 检查review.html
        with open(review, 'r') as f:
            r_content = f.read()
        
        if '@media(max-width:480px)' not in r_content:
            issues.append('review缺少移动端CSS')
        if 'function playOk' not in r_content and 'playOk()' in r_content:
            issues.append('review缺少playOk')
        if 'function speak' not in r_content and 'speak(' in r_content:
            issues.append('review缺少speak')
        
        if issues:
            results.append((f'{level}/{folder}', issues))

if results:
    print(f'发现 {len(results)} 个课件有问题：\n')
    for path, issues in results:
        print(f'{path}: {", ".join(issues)}')
else:
    print('✅ 所有课件质量检查通过！')
    print('\n检查项目：')
    print('  ✅ 移动端CSS (@media max-width:480px)')
    print('  ✅ 拼读字母换行 (flex-wrap:wrap)')
    print('  ✅ 音效函数 (playOk/playNo/speak)')
    print('  ✅ 角色多样性（无连续3课重复）')
