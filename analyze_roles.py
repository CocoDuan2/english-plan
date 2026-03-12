#!/usr/bin/env python3
import os
import re
from collections import Counter

base = 'lessons'
phonics_levels = ['phonics-1', 'phonics-2', 'phonics-3', 'phonics-4', 'phonics-5']

first_roles = []
all_courses = []

for level in phonics_levels:
    level_path = os.path.join(base, level)
    if not os.path.exists(level_path):
        continue
    
    folders = sorted([f for f in os.listdir(level_path) if os.path.isdir(os.path.join(level_path, f))])
    
    for folder in folders:
        teach_path = os.path.join(level_path, folder, 'teach.html')
        if not os.path.exists(teach_path):
            continue
        
        with open(teach_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        s1_match = re.search(r'<!-- S1:.*?-->(.*?)<!-- S2:', content, re.DOTALL)
        if s1_match:
            roles = re.findall(r'assets/peppa/([\w-]+)\.png', s1_match.group(1))
            if roles:
                first_roles.append(roles[0])
                all_courses.append(f'{level}/{folder}')

print(f'=== 自然拼读首页角色分析（共{len(first_roles)}课）===\n')

role_counts = Counter(first_roles)
print('角色使用频率（降序）：')
for role, count in sorted(role_counts.items(), key=lambda x: -x[1])[:15]:
    pct = count * 100 / len(first_roles)
    print(f'  {role}: {count}次 ({pct:.1f}%)')

print('\n=== 连续3课使用相同角色 ===')
consecutive = []
for i in range(len(first_roles) - 2):
    if first_roles[i] == first_roles[i+1] == first_roles[i+2]:
        consecutive.append((i, first_roles[i], all_courses[i:i+3]))

if consecutive:
    for idx, role, courses in consecutive:
        print(f'⚠️  {role}: {", ".join([c.split("/")[1] for c in courses])}')
else:
    print('✅ 无连续3课使用相同角色')

print(f'\n总计：{len(first_roles)}课，{len(role_counts)}种角色')
