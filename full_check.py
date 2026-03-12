import os
import re
from collections import defaultdict

# 全量检查所有自然拼读课件
all_files = []
for root, dirs, files in os.walk('lessons'):
    if 'phonics-' in root:
        for f in files:
            if f in ['teach.html', 'review.html']:
                all_files.append(os.path.join(root, f))

all_files.sort()

issues = []
stats = {
    'total': len(all_files),
    'mobile_css': 0,
    'audio_funcs': 0,
    'canvas_ok': 0,
    'char_repeat': 0
}

for file in all_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. 移动端CSS
    if '@media(max-width:480px)' in content or '@media (max-width:480px)' in content:
        stats['mobile_css'] += 1
    else:
        issues.append(f"{file}: 缺少移动端CSS")
    
    # 2. 音效函数（review.html）
    if 'review.html' in file:
        has_ok = 'playOk' in content
        has_no = 'playNo' in content
        if has_ok and has_no:
            stats['audio_funcs'] += 1
        else:
            if not has_ok:
                issues.append(f"{file}: 缺少playOk")
            if not has_no:
                issues.append(f"{file}: 缺少playNo")
    
    # 3. Canvas尺寸（Phonics 1 teach.html）
    if 'phonics-1' in file and 'teach.html' in file:
        canvas_match = re.search(r'canvas\.width\s*=\s*(\d+)', content)
        if canvas_match:
            size = int(canvas_match.group(1))
            if size >= 280:
                stats['canvas_ok'] += 1
            else:
                issues.append(f"{file}: Canvas尺寸{size}px < 280px")
    
    # 4. 同课内角色重复≥3次
    chars = re.findall(r'assets/peppa/([\w-]+)\.png', content)
    char_count = defaultdict(int)
    for c in chars:
        char_count[c] += 1
    
    has_repeat = False
    for char, count in char_count.items():
        if count >= 3:
            issues.append(f"{file}: 角色{char}重复{count}次")
            has_repeat = True
    
    if not has_repeat:
        stats['char_repeat'] += 1

print(f"检查范围：{stats['total']}个文件")
print(f"移动端CSS：{stats['mobile_css']}/{stats['total']}")
print(f"音效函数：{stats['audio_funcs']}/{len([f for f in all_files if 'review.html' in f])}")
print(f"Canvas尺寸：{stats['canvas_ok']}/26")
print(f"角色多样性：{stats['char_repeat']}/{stats['total']}")

if issues:
    print(f"\n发现 {len(issues)} 个问题：")
    for i in issues[:10]:  # 只显示前10个
        print(f"  - {i}")
    if len(issues) > 10:
        print(f"  ... 还有 {len(issues)-10} 个问题")
else:
    print("\n✅ 全量检查通过，所有课件质量完美")

