#!/usr/bin/env python3
import re
from pathlib import Path

files = [
    "lessons/level-4/helping-at-home/review.html",
    "lessons/phonics-5/tion-sion/review.html",
    "lessons/level-2/where-we-go/review.html",
    "lessons/level-2/daily-actions/review.html",
    "lessons/phonics-1/letter-h/review.html"
]

for f in files:
    path = Path(f)
    if not path.exists():
        print(f"❌ {f}: 文件不存在")
        continue
    
    content = path.read_text()
    
    # 检查关键函数
    has_playOk = 'function playOk()' in content or 'playOk=()=>' in content
    has_playNo = 'function playNo()' in content or 'playNo=()=>' in content
    has_speak = 'function speak(' in content or 'speak=(' in content
    
    # 检查移动端CSS
    mobile_css = len(re.findall(r'@media\s*\(\s*max-width\s*:\s*480px\s*\)', content))
    
    # 检查audioCache
    has_audioCache = 'audioCache' in content
    
    print(f"\n✅ {path.parent.name}/{path.name}")
    print(f"   playOk: {'✅' if has_playOk else '❌'}")
    print(f"   playNo: {'✅' if has_playNo else '❌'}")
    print(f"   speak: {'✅' if has_speak else '❌'}")
    print(f"   移动端CSS: {mobile_css}个")
    print(f"   audioCache: {'✅' if has_audioCache else '❌'}")

print("\n检查完成")
