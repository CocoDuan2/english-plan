import os
import re
from collections import defaultdict

# 统计结果
issues = []
stats = defaultdict(int)

# 遍历所有课件
for root, dirs, files in os.walk('lessons'):
    for file in files:
        if not file.endswith('.html'):
            continue
        
        path = os.path.join(root, file)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查1: 移动端CSS
        if 'teach.html' in file:
            if '@media(max-width:480px)' not in content:
                issues.append(f"{path}: 缺少移动端CSS")
            else:
                stats['移动端CSS'] += 1
        
        # 检查2: review.html 关键函数
        if 'review.html' in file:
            if 'function speak(' not in content:
                issues.append(f"{path}: 缺少 speak() 函数")
            else:
                stats['speak函数'] += 1
            
            if 'function playOk(' not in content:
                issues.append(f"{path}: 缺少 playOk() 函数")
            else:
                stats['playOk函数'] += 1
            
            if 'function playNo(' not in content:
                issues.append(f"{path}: 缺少 playNo() 函数")
            else:
                stats['playNo函数'] += 1
        
        # 检查3: HTML结构完整性
        if '</body>' not in content or '</html>' not in content:
            issues.append(f"{path}: HTML结构不完整")
        else:
            stats['HTML完整'] += 1
        
        # 检查4: 角色图片统计（同一课件内）
        peppa_imgs = re.findall(r'assets/peppa/([^"\']+\.png)', content)
        img_count = defaultdict(int)
        for img in peppa_imgs:
            img_count[img] += 1
        
        # 同课件内角色重复≥3次
        for img, count in img_count.items():
            if count >= 3:
                issues.append(f"{path}: 角色 {img} 重复 {count} 次")

print("=== 质量检查报告 ===\n")
print(f"✅ 移动端CSS: {stats['移动端CSS']}")
print(f"✅ speak函数: {stats['speak函数']}")
print(f"✅ playOk函数: {stats['playOk函数']}")
print(f"✅ playNo函数: {stats['playNo函数']}")
print(f"✅ HTML完整: {stats['HTML完整']}")

if issues:
    print(f"\n⚠️  发现 {len(issues)} 个问题:\n")
    for issue in issues[:20]:  # 只显示前20个
        print(f"  - {issue}")
    if len(issues) > 20:
        print(f"  ... 还有 {len(issues)-20} 个问题")
else:
    print("\n🎉 所有检查项通过！")
