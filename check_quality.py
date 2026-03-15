#!/usr/bin/env python3
import re
from pathlib import Path

# 检查的3个课件
courses = [
    ("P62", "phonics-4/bl-blend"),
    ("P45", "phonics-3/u-e-magic"),
    ("P71", "phonics-4/fr-blend")
]

results = []

for code, folder in courses:
    teach_path = Path(f"lessons/{folder}/teach.html")
    review_path = Path(f"lessons/{folder}/review.html")
    
    result = {"code": code, "folder": folder}
    
    # 检查 teach.html
    if teach_path.exists():
        teach = teach_path.read_text()
        result["teach_mobile_css"] = "@media(max-width:480px)" in teach
        result["teach_playOk"] = "function playOk()" in teach or "playOk=" in teach
        result["teach_playNo"] = "function playNo()" in teach or "playNo=" in teach
        
        # 统计角色使用次数
        chars = re.findall(r'(peppa-[a-z-]+|george-[a-z-]+|daddy-pig-[a-z-]+|mummy-pig-[a-z-]+|candy-cat-[a-z-]+|emily-elephant-[a-z-]+)', teach, re.I)
        char_count = {}
        for c in chars:
            char_count[c] = char_count.get(c, 0) + 1
        result["teach_char_max"] = max(char_count.values()) if char_count else 0
        result["teach_char_repeat"] = [k for k,v in char_count.items() if v >= 3]
        
    # 检查 review.html
    if review_path.exists():
        review = review_path.read_text()
        result["review_mobile_css"] = "@media(max-width:480px)" in review
        result["review_playOk"] = "function playOk()" in review or "playOk=" in review
        result["review_playNo"] = "function playNo()" in review or "playNo=" in review
        result["review_audioCache"] = "audioCache" in review
        
        # 统计角色使用次数
        chars = re.findall(r'(peppa-[a-z-]+|george-[a-z-]+|daddy-pig-[a-z-]+|mummy-pig-[a-z-]+|candy-cat-[a-z-]+|emily-elephant-[a-z-]+)', review, re.I)
        char_count = {}
        for c in chars:
            char_count[c] = char_count.get(c, 0) + 1
        result["review_char_max"] = max(char_count.values()) if char_count else 0
        result["review_char_repeat"] = [k for k,v in char_count.items() if v >= 2]
    
    results.append(result)

# 输出结果
print("=" * 60)
print("质量检查报告 - 2026-03-15 09:07")
print("=" * 60)
for r in results:
    print(f"\n{r['code']} ({r['folder']}):")
    print(f"  teach.html:")
    print(f"    移动端CSS: {'✅' if r.get('teach_mobile_css') else '❌'}")
    print(f"    playOk函数: {'✅' if r.get('teach_playOk') else '❌'}")
    print(f"    playNo函数: {'✅' if r.get('teach_playNo') else '❌'}")
    print(f"    角色最多重复: {r.get('teach_char_max', 0)}次")
    if r.get('teach_char_repeat'):
        print(f"    重复≥3次角色: {r['teach_char_repeat']}")
    print(f"  review.html:")
    print(f"    移动端CSS: {'✅' if r.get('review_mobile_css') else '❌'}")
    print(f"    playOk函数: {'✅' if r.get('review_playOk') else '❌'}")
    print(f"    playNo函数: {'✅' if r.get('review_playNo') else '❌'}")
    print(f"    audioCache: {'✅' if r.get('review_audioCache') else '❌'}")
    print(f"    角色最多重复: {r.get('review_char_max', 0)}次")
    if r.get('review_char_repeat'):
        print(f"    重复≥2次角色: {r['review_char_repeat']}")

# 统计
total_checks = len(results) * 2  # teach + review
passed = sum([
    1 for r in results 
    if r.get('teach_mobile_css') and r.get('teach_playOk') and r.get('teach_playNo') 
    and r.get('teach_char_max', 0) < 3
])
passed += sum([
    1 for r in results 
    if r.get('review_mobile_css') and r.get('review_playOk') and r.get('review_playNo') 
    and r.get('review_audioCache') and r.get('review_char_max', 0) < 2
])

print(f"\n{'=' * 60}")
print(f"总计: {passed}/{total_checks} 通过")
print(f"{'=' * 60}")
