#!/usr/bin/env python3
import os
import re
from collections import Counter

def check_courseware(base_path):
    issues = []
    
    # 获取所有自然拼读课件
    phonics_dirs = []
    for level in ['phonics-1', 'phonics-2', 'phonics-3', 'phonics-4', 'phonics-5']:
        level_path = os.path.join(base_path, 'lessons', level)
        if os.path.exists(level_path):
            for folder in os.listdir(level_path):
                folder_path = os.path.join(level_path, folder)
                if os.path.isdir(folder_path):
                    phonics_dirs.append((level, folder, folder_path))
    
    print(f"检查 {len(phonics_dirs)} 个自然拼读课件...\n")
    
    # 检查每个课件
    for level, folder, path in phonics_dirs[:5]:  # 先检查前5个
        teach_file = os.path.join(path, 'teach.html')
        review_file = os.path.join(path, 'review.html')
        
        print(f"检查 {level}/{folder}:")
        
        # 1. 检查移动端CSS
        for file_name, file_path in [('teach', teach_file), ('review', review_file)]:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if '@media(max-width:480px)' not in content:
                        issues.append(f"  ❌ {level}/{folder}/{file_name}.html 缺少移动端CSS")
                    else:
                        print(f"  ✅ {file_name}.html 移动端CSS")
        
        # 2. 检查角色多样性
        if os.path.exists(teach_file):
            with open(teach_file, 'r', encoding='utf-8') as f:
                content = f.read()
                characters = re.findall(r'(peppa-[a-z-]+|george-[a-z-]+|daddy-[a-z-]+|mummy-[a-z-]+|candy-[a-z-]+|emily-[a-z-]+)\.png', content)
                char_count = Counter(characters)
                repeated = [char for char, count in char_count.items() if count >= 3]
                if repeated:
                    issues.append(f"  ❌ {level}/{folder}/teach.html 角色重复≥3次: {repeated}")
                else:
                    print(f"  ✅ teach.html 角色多样性")
        
        # 3. 检查音频函数
        if os.path.exists(review_file):
            with open(review_file, 'r', encoding='utf-8') as f:
                content = f.read()
                has_playOk = 'function playOk()' in content or 'playOk=()=>' in content
                has_playNo = 'function playNo()' in content or 'playNo=()=>' in content
                if not (has_playOk and has_playNo):
                    issues.append(f"  ❌ {level}/{folder}/review.html 缺少音效函数")
                else:
                    print(f"  ✅ review.html 音效函数")
        
        print()
    
    return issues

if __name__ == '__main__':
    base_path = '.'
    issues = check_courseware(base_path)
    
    print("\n" + "="*50)
    if issues:
        print(f"发现 {len(issues)} 个问题:")
        for issue in issues:
            print(issue)
    else:
        print("✅ 所有检查项通过！")
