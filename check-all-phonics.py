#!/usr/bin/env python3
import os
import re
from collections import Counter

def get_first_character(html_path):
    """获取课件首页使用的角色"""
    if not os.path.exists(html_path):
        return None
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
        # 查找第一个角色图片（通常在首页）
        match = re.search(r'assets/peppa/([a-z-]+)\.png', content)
        return match.group(1) if match else None

def check_all_phonics():
    base = 'lessons'
    all_courses = []
    
    # 收集所有课件
    for level in ['phonics-1', 'phonics-2', 'phonics-3', 'phonics-4', 'phonics-5']:
        level_path = os.path.join(base, level)
        if os.path.exists(level_path):
            for folder in sorted(os.listdir(level_path)):
                folder_path = os.path.join(level_path, folder)
                if os.path.isdir(folder_path):
                    teach = os.path.join(folder_path, 'teach.html')
                    first_char = get_first_character(teach)
                    all_courses.append({
                        'level': level,
                        'folder': folder,
                        'path': folder_path,
                        'first_char': first_char
                    })
    
    print(f"检查 {len(all_courses)} 个自然拼读课件\n")
    
    # 检查连续3课首页角色重复
    issues = []
    for i in range(len(all_courses) - 2):
        c1, c2, c3 = all_courses[i:i+3]
        if c1['first_char'] == c2['first_char'] == c3['first_char'] and c1['first_char']:
            issues.append(f"连续3课使用相同首页角色 {c1['first_char']}: {c1['folder']}, {c2['folder']}, {c3['folder']}")
    
    # 统计首页角色分布
    first_chars = [c['first_char'] for c in all_courses if c['first_char']]
    char_dist = Counter(first_chars)
    
    print("首页角色分布:")
    for char, count in char_dist.most_common():
        print(f"  {char}: {count}次")
    
    print(f"\n连续重复检查:")
    if issues:
        for issue in issues:
            print(f"  ❌ {issue}")
    else:
        print("  ✅ 无连续3课使用相同首页角色")
    
    return len(issues) == 0

if __name__ == '__main__':
    check_all_phonics()
