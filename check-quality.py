#!/usr/bin/env python3
import os
import re

issues = []

# 检查的3个课件
check_dirs = [
    'lessons/phonics-1/letter-d',
    'lessons/phonics-2/og-family', 
    'lessons/phonics-4/br-blend'
]

for dir_path in check_dirs:
    teach_file = f'{dir_path}/teach.html'
    review_file = f'{dir_path}/review.html'
    
    print(f'\n📋 检查: {dir_path}')
    
    # 检查 teach.html
    if os.path.exists(teach_file):
        with open(teach_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 1. 移动端 CSS
        if '@media(max-width:480px)' not in content:
            issues.append(f'❌ {dir_path}/teach.html: 缺少移动端CSS')
        else:
            print('  ✅ teach.html: 移动端CSS')
        
        # 2. playOk/playNo 函数
        has_ok = 'function playOk' in content
        has_no = 'function playNo' in content
        if has_ok and has_no:
            print('  ✅ teach.html: playOk/playNo')
        else:
            issues.append(f'❌ {dir_path}/teach.html: 缺少音效函数')
        
        # 3. 角色多样性（同课内重复≥3次）
        roles = re.findall(r'assets/peppa/([^"]+\.png)', content)
        role_counts = {}
        for role in roles:
            role_counts[role] = role_counts.get(role, 0) + 1
        
        max_repeat = max(role_counts.values()) if role_counts else 0
        if max_repeat >= 3:
            issues.append(f'❌ {dir_path}/teach.html: 角色重复{max_repeat}次')
        else:
            print(f'  ✅ teach.html: 角色多样性 (最多{max_repeat}次)')
    
    # 检查 review.html
    if os.path.exists(review_file):
        with open(review_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 1. 移动端 CSS
        if '@media(max-width:480px)' not in content:
            issues.append(f'❌ {dir_path}/review.html: 缺少移动端CSS')
        else:
            print('  ✅ review.html: 移动端CSS')
        
        # 2. playOk/playNo 函数
        has_ok = 'function playOk' in content
        has_no = 'function playNo' in content
        if has_ok and has_no:
            print('  ✅ review.html: playOk/playNo')
        else:
            issues.append(f'❌ {dir_path}/review.html: 缺少音效函数')
        
        # 3. audioCache
        if 'audioCache' in content:
            print('  ✅ review.html: audioCache')
        else:
            issues.append(f'❌ {dir_path}/review.html: 缺少audioCache')

print('\n' + '='*50)
if issues:
    print(f'\n❌ 发现 {len(issues)} 个问题:')
    for issue in issues:
        print(issue)
else:
    print('\n🎉 所有检查项目通过！')
