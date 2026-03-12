#!/usr/bin/env python3
"""检查同课件内角色重复使用"""
import re
from pathlib import Path
from collections import Counter

def check_lesson(filepath):
    """检查单个课件内的角色使用"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取所有角色图片
    chars = re.findall(r'assets/peppa/([\w-]+)\.png', content)
    char_count = Counter(chars)
    
    # 找出重复使用的角色
    repeated = {char: count for char, count in char_count.items() if count >= 2}
    
    return repeated, len(chars)

def main():
    issues = []
    
    for phonics_level in ['phonics-1', 'phonics-2', 'phonics-3', 'phonics-4', 'phonics-5']:
        level_dir = Path('lessons') / phonics_level
        if not level_dir.exists():
            continue
        
        for lesson_dir in sorted(level_dir.iterdir()):
            if not lesson_dir.is_dir():
                continue
            
            for html_file in [lesson_dir / 'teach.html', lesson_dir / 'review.html']:
                if not html_file.exists():
                    continue
                
                repeated, total = check_lesson(html_file)
                if repeated:
                    for char, count in repeated.items():
                        if count >= 3:
                            issues.append(f"❌ {phonics_level}/{lesson_dir.name}/{html_file.name}: {char} 出现 {count} 次")
                        elif count == 2:
                            issues.append(f"⚠️ {phonics_level}/{lesson_dir.name}/{html_file.name}: {char} 出现 2 次")
    
    print("=" * 70)
    print("🔍 同课件内角色重复检查")
    print("=" * 70)
    
    if issues:
        critical = [i for i in issues if i.startswith('❌')]
        warnings = [i for i in issues if i.startswith('⚠️')]
        
        if critical:
            print(f"\n❌ 严重问题（≥3次）: {len(critical)} 个")
            for issue in critical[:10]:
                print(issue)
            if len(critical) > 10:
                print(f"... 还有 {len(critical) - 10} 个")
        
        if warnings:
            print(f"\n⚠️ 轻微问题（2次）: {len(warnings)} 个")
            for issue in warnings[:10]:
                print(issue)
            if len(warnings) > 10:
                print(f"... 还有 {len(warnings) - 10} 个")
    else:
        print("\n✅ 所有课件内角色都不重复！")

if __name__ == '__main__':
    main()
