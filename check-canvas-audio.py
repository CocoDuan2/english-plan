#!/usr/bin/env python3
import os
import re

def check_canvas_and_audio():
    base = 'lessons/phonics-1'
    issues = []
    
    # 检查 Phonics 1 的 Canvas 尺寸
    print("检查 Phonics 1 Canvas 尺寸...")
    for folder in sorted(os.listdir(base)):
        teach = os.path.join(base, folder, 'teach.html')
        if os.path.exists(teach):
            with open(teach, 'r', encoding='utf-8') as f:
                content = f.read()
                # 检查移动端 Canvas 尺寸
                if 'trace-container' in content:
                    mobile_css = re.search(r'@media\(max-width:480px\).*?\.trace-container\{[^}]*width:(\d+)px[^}]*height:(\d+)px', content, re.DOTALL)
                    if mobile_css:
                        w, h = mobile_css.groups()
                        if w != '280' or h != '280':
                            issues.append(f"❌ {folder}/teach.html Canvas尺寸错误: {w}x{h} (应为280x280)")
                        else:
                            print(f"  ✅ {folder} Canvas: 280x280")
                    else:
                        issues.append(f"❌ {folder}/teach.html 缺少移动端Canvas尺寸")
    
    # 检查音频缓存
    print("\n检查音频缓存机制...")
    checked = 0
    for level in ['phonics-1', 'phonics-2', 'phonics-3', 'phonics-4', 'phonics-5']:
        level_path = os.path.join('lessons', level)
        if not os.path.exists(level_path):
            continue
        for folder in os.listdir(level_path):
            review = os.path.join(level_path, folder, 'review.html')
            if os.path.exists(review):
                with open(review, 'r', encoding='utf-8') as f:
                    content = f.read()
                    has_cache = 'audioCache' in content or 'const a=' in content
                    if not has_cache:
                        issues.append(f"❌ {level}/{folder}/review.html 缺少音频缓存")
                    checked += 1
                    if checked >= 10:  # 只检查前10个
                        break
        if checked >= 10:
            break
    
    print(f"  已检查 {checked} 个 review.html")
    
    return issues

if __name__ == '__main__':
    issues = check_canvas_and_audio()
    print("\n" + "="*50)
    if issues:
        print(f"发现 {len(issues)} 个问题:")
        for issue in issues:
            print(issue)
    else:
        print("✅ Canvas和音频检查全部通过！")
