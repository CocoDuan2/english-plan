import os
import re
from collections import defaultdict

print("=== 自然拼读课件最终质量检查 ===\n")

stats = {
    '移动端CSS': 0,
    'speak函数': 0,
    'playOk函数': 0,
    'playNo函数': 0,
    'HTML完整': 0,
    'Canvas移动端尺寸': 0,
    '角色重复≥3次': 0
}

issues = []

# 遍历自然拼读课件
for root, dirs, files in os.walk('lessons'):
    # 只检查自然拼读课件
    if not any(x in root for x in ['phonics-1', 'phonics-2', 'phonics-3', 'phonics-4', 'phonics-5']):
        continue
    
    for file in files:
        if not file.endswith('.html'):
            continue
        
        path = os.path.join(root, file)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查1: teach.html 移动端CSS
        if 'teach.html' in file:
            if '@media(max-width:480px)' in content:
                stats['移动端CSS'] += 1
                
                # Phonics 1 Canvas移动端尺寸检查
                if 'phonics-1' in root:
                    if '.trace-container{width:280px;height:280px' in content:
                        stats['Canvas移动端尺寸'] += 1
                    else:
                        issues.append(f"{path}: Canvas移动端尺寸不是280px")
            else:
                issues.append(f"{path}: 缺少移动端CSS")
        
        # 检查2: review.html 关键函数
        if 'review.html' in file:
            has_speak = 'function speak(' in content
            has_playOk = 'function playOk(' in content
            has_playNo = 'function playNo(' in content
            
            if has_speak:
                stats['speak函数'] += 1
            else:
                issues.append(f"{path}: 缺少 speak() 函数")
            
            if has_playOk:
                stats['playOk函数'] += 1
            else:
                issues.append(f"{path}: 缺少 playOk() 函数")
            
            if has_playNo:
                stats['playNo函数'] += 1
            else:
                issues.append(f"{path}: 缺少 playNo() 函数")
        
        # 检查3: HTML完整性
        if '</body>' in content and '</html>' in content:
            stats['HTML完整'] += 1
        else:
            issues.append(f"{path}: HTML结构不完整")
        
        # 检查4: 角色重复
        peppa_imgs = re.findall(r'assets/peppa/([^"\']+\.png)', content)
        img_count = defaultdict(int)
        for img in peppa_imgs:
            img_count[img] += 1
        
        for img, count in img_count.items():
            if count >= 3:
                stats['角色重复≥3次'] += 1
                issues.append(f"{path}: {img} 重复 {count} 次")

# 输出统计
print("📊 统计结果：")
print(f"  ✅ teach.html 移动端CSS: {stats['移动端CSS']}/92")
print(f"  ✅ review.html speak函数: {stats['speak函数']}/92")
print(f"  ✅ review.html playOk函数: {stats['playOk函数']}/92")
print(f"  ✅ review.html playNo函数: {stats['playNo函数']}/92")
print(f"  ✅ HTML结构完整: {stats['HTML完整']}/184")
print(f"  ✅ Phonics 1 Canvas移动端尺寸: {stats['Canvas移动端尺寸']}/26")
print(f"  ✅ 角色重复≥3次: {stats['角色重复≥3次']} 个")

# 输出问题
if issues:
    print(f"\n⚠️  发现 {len(issues)} 个问题：")
    for issue in issues[:10]:
        print(f"  - {issue}")
    if len(issues) > 10:
        print(f"  ... 还有 {len(issues)-10} 个问题")
else:
    print("\n🎉 所有检查项通过！课件质量达标！")
