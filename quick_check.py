#!/usr/bin/env python3
import re
from pathlib import Path

files = [
    "lessons/level-4/helping-at-home/teach.html",
    "lessons/phonics-5/tion-sion/teach.html",
    "lessons/level-2/where-we-go/teach.html",
    "lessons/level-2/daily-actions/teach.html",
    "lessons/phonics-1/letter-h/teach.html"
]

for f in files:
    path = Path(f)
    if not path.exists():
        print(f"❌ {f}: 文件不存在")
        continue
    
    content = path.read_text()
    
    # 检查移动端CSS
    mobile_css = len(re.findall(r'@media\s*\(\s*max-width\s*:\s*480px\s*\)', content))
    
    # 检查角色图片使用次数
    chars = re.findall(r'assets/peppa/([\w-]+)\.png', content)
    char_counts = {}
    for c in chars:
        char_counts[c] = char_counts.get(c, 0) + 1
    max_repeat = max(char_counts.values()) if char_counts else 0
    
    # 检查HTML完整性
    has_body_end = '</body>' in content and '</html>' in content
    
    print(f"\n✅ {path.parent.name}/{path.name}")
    print(f"   移动端CSS: {mobile_css}个")
    print(f"   角色重复: 最多{max_repeat}次")
    print(f"   HTML完整: {'✅' if has_body_end else '❌'}")
    
    if max_repeat >= 3:
        print(f"   ⚠️  角色重复≥3次: {[k for k,v in char_counts.items() if v>=3]}")

print("\n检查完成")
