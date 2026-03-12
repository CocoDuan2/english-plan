import os
import re
import random

# 从每个 Phonics 阶段随机抽取2个课件
phonics_dirs = {
    'phonics-1': [],
    'phonics-2': [],
    'phonics-3': [],
    'phonics-4': [],
    'phonics-5': []
}

for phonics in phonics_dirs.keys():
    path = f'lessons/{phonics}'
    if os.path.exists(path):
        folders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
        phonics_dirs[phonics] = folders

# 随机抽取
samples = []
for phonics, folders in phonics_dirs.items():
    if len(folders) >= 2:
        selected = random.sample(folders, 2)
        for folder in selected:
            samples.append((phonics, folder))

print(f"抽样检查 {len(samples)} 个课件：")
for phonics, folder in samples:
    print(f"  - {phonics}/{folder}")

# 检查项目
issues = []

for phonics, folder in samples:
    teach_path = f'lessons/{phonics}/{folder}/teach.html'
    review_path = f'lessons/{phonics}/{folder}/review.html'
    
    # 检查 teach.html
    if os.path.exists(teach_path):
        with open(teach_path, 'r', encoding='utf-8') as f:
            teach_content = f.read()
        
        # 1. 移动端CSS
        if '@media(max-width:480px)' not in teach_content:
            issues.append(f"{phonics}/{folder}/teach.html 缺少移动端CSS")
        
        # 2. Canvas尺寸（仅Phonics 1）
        if phonics == 'phonics-1':
            canvas_match = re.search(r'\.trace-container\s*\{[^}]*width:\s*(\d+)px', teach_content)
            if canvas_match and canvas_match.group(1) != '300':
                issues.append(f"{phonics}/{folder}/teach.html Canvas宽度不是300px")
        
        # 3. 角色多样性（同课内重复≥3次）
        roles = re.findall(r'assets/peppa/([\w-]+)\.png', teach_content)
        role_counts = {}
        for role in roles:
            role_counts[role] = role_counts.get(role, 0) + 1
        for role, count in role_counts.items():
            if count >= 3:
                issues.append(f"{phonics}/{folder}/teach.html 角色{role}重复{count}次")
    
    # 检查 review.html
    if os.path.exists(review_path):
        with open(review_path, 'r', encoding='utf-8') as f:
            review_content = f.read()
        
        # 1. 移动端CSS
        if '@media(max-width:480px)' not in review_content:
            issues.append(f"{phonics}/{folder}/review.html 缺少移动端CSS")
        
        # 2. 音效函数
        if 'function playOk()' not in review_content:
            issues.append(f"{phonics}/{folder}/review.html 缺少playOk函数")
        if 'function playNo()' not in review_content:
            issues.append(f"{phonics}/{folder}/review.html 缺少playNo函数")
        
        # 3. 角色多样性
        roles = re.findall(r'assets/peppa/([\w-]+)\.png', review_content)
        role_counts = {}
        for role in roles:
            role_counts[role] = role_counts.get(role, 0) + 1
        for role, count in role_counts.items():
            if count >= 3:
                issues.append(f"{phonics}/{folder}/review.html 角色{role}重复{count}次")

print(f"\n检查结果：")
if issues:
    print(f"发现 {len(issues)} 个问题：")
    for issue in issues:
        print(f"  ❌ {issue}")
else:
    print("✅ 所有抽样课件质量完美，无问题")

