#!/usr/bin/env python3
"""自然拼读课件质量检查脚本"""
import os
import re
from pathlib import Path
from collections import Counter

# 检查项目
issues = []
stats = {
    'total_files': 0,
    'mobile_css_ok': 0,
    'flex_wrap_ok': 0,
    'canvas_size_ok': 0,
    'audio_functions_ok': 0,
    'character_diversity': Counter()
}

def check_file(filepath):
    """检查单个HTML文件"""
    global stats
    stats['total_files'] += 1
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    filename = filepath.name
    lesson_name = filepath.parent.name
    
    # 1. 检查移动端CSS
    if '@media(max-width:480px)' in content or '@media (max-width:480px)' in content:
        stats['mobile_css_ok'] += 1
    else:
        issues.append(f"❌ {lesson_name}/{filename}: 缺少移动端CSS")
    
    # 2. 检查拼读字母换行（teach.html）
    if 'teach.html' in filename:
        if 'flex-wrap:wrap' in content or 'flex-wrap: wrap' in content:
            stats['flex_wrap_ok'] += 1
        else:
            issues.append(f"⚠️ {lesson_name}/{filename}: 拼读字母可能无法换行")
    
    # 3. 检查Canvas尺寸（Phonics 1）
    if 'phonics-1' in str(filepath) and 'teach.html' in filename:
        if '280' in content and 'canvas' in content.lower():
            stats['canvas_size_ok'] += 1
        else:
            issues.append(f"⚠️ {lesson_name}/{filename}: Canvas尺寸可能不是280px")
    
    # 4. 检查音效函数（review.html）
    if 'review.html' in filename:
        has_speak = 'function speak(' in content or 'const speak=' in content
        has_playok = 'function playOk(' in content or 'const playOk=' in content
        has_playno = 'function playNo(' in content or 'const playNo=' in content
        
        if has_speak and has_playok and has_playno:
            stats['audio_functions_ok'] += 1
        else:
            missing = []
            if not has_speak: missing.append('speak')
            if not has_playok: missing.append('playOk')
            if not has_playno: missing.append('playNo')
            issues.append(f"❌ {lesson_name}/{filename}: 缺少音效函数 {missing}")
    
    # 5. 统计角色使用（首页）
    if 'teach.html' in filename:
        # 提取首页角色（S1 Hello页）
        s1_match = re.search(r'<!-- S1.*?-->(.*?)<!-- S2', content, re.DOTALL)
        if s1_match:
            s1_content = s1_match.group(1)
            char_match = re.search(r'assets/peppa/([\w-]+)\.png', s1_content)
            if char_match:
                char_name = char_match.group(1)
                stats['character_diversity'][char_name] += 1

def main():
    base_dir = Path('lessons')
    
    # 遍历所有自然拼读课件
    for phonics_level in ['phonics-1', 'phonics-2', 'phonics-3', 'phonics-4', 'phonics-5']:
        level_dir = base_dir / phonics_level
        if not level_dir.exists():
            continue
        
        for lesson_dir in sorted(level_dir.iterdir()):
            if not lesson_dir.is_dir():
                continue
            
            teach_file = lesson_dir / 'teach.html'
            review_file = lesson_dir / 'review.html'
            
            if teach_file.exists():
                check_file(teach_file)
            if review_file.exists():
                check_file(review_file)
    
    # 输出报告
    print("=" * 60)
    print("📊 自然拼读课件质量检查报告")
    print("=" * 60)
    print(f"\n总文件数: {stats['total_files']}")
    print(f"移动端CSS: {stats['mobile_css_ok']}/{stats['total_files']}")
    print(f"拼读字母换行: {stats['flex_wrap_ok']} 个 teach.html")
    print(f"Canvas尺寸正确: {stats['canvas_size_ok']} 个 Phonics 1 teach.html")
    print(f"音效函数完整: {stats['audio_functions_ok']} 个 review.html")
    
    print("\n" + "=" * 60)
    print("🎭 首页角色使用统计（teach.html）")
    print("=" * 60)
    for char, count in stats['character_diversity'].most_common():
        print(f"{char}: {count}次")
    
    # 检查连续重复
    print("\n" + "=" * 60)
    print("🔍 连续3课首页角色重复检查")
    print("=" * 60)
    
    consecutive_issues = []
    for phonics_level in ['phonics-1', 'phonics-2', 'phonics-3', 'phonics-4', 'phonics-5']:
        level_dir = Path('lessons') / phonics_level
        if not level_dir.exists():
            continue
        
        chars = []
        lessons = []
        for lesson_dir in sorted(level_dir.iterdir()):
            if not lesson_dir.is_dir():
                continue
            teach_file = lesson_dir / 'teach.html'
            if teach_file.exists():
                with open(teach_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                s1_match = re.search(r'<!-- S1.*?-->(.*?)<!-- S2', content, re.DOTALL)
                if s1_match:
                    char_match = re.search(r'assets/peppa/([\w-]+)\.png', s1_match.group(1))
                    if char_match:
                        chars.append(char_match.group(1))
                        lessons.append(lesson_dir.name)
        
        # 检查连续3个
        for i in range(len(chars) - 2):
            if chars[i] == chars[i+1] == chars[i+2]:
                consecutive_issues.append(f"{phonics_level}: {lessons[i]}, {lessons[i+1]}, {lessons[i+2]} 都用 {chars[i]}")
    
    if consecutive_issues:
        for issue in consecutive_issues:
            print(f"❌ {issue}")
    else:
        print("✅ 无连续3课使用相同角色")
    
    # 输出问题列表
    if issues:
        print("\n" + "=" * 60)
        print("⚠️ 发现的问题")
        print("=" * 60)
        for issue in issues[:20]:  # 只显示前20个
            print(issue)
        if len(issues) > 20:
            print(f"\n... 还有 {len(issues) - 20} 个问题")
    else:
        print("\n✅ 所有检查项目通过！")

if __name__ == '__main__':
    main()
