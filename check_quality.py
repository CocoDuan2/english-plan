#!/usr/bin/env python3
import re
from pathlib import Path

# 检查的课件
courses = [
    "lessons/phonics-1/letter-u",
    "lessons/phonics-1/letter-v", 
    "lessons/phonics-4/cl-blend"
]

results = []

for course in courses:
    course_path = Path(course)
    course_name = course_path.name
    
    # 检查 teach.html
    teach_file = course_path / "teach.html"
    teach_content = teach_file.read_text()
    
    teach_checks = {
        "移动端CSS": "@media(max-width:480px)" in teach_content,
        "playOk函数": "function playOk()" in teach_content or "playOk=()=>" in teach_content,
        "playNo函数": "function playNo()" in teach_content or "playNo=()=>" in teach_content,
        "speak函数": "function speak(" in teach_content or "speak=(" in teach_content,
    }
    
    # 检查 Canvas (仅 Phonics 1)
    if "phonics-1" in course:
        teach_checks["Canvas尺寸280px"] = "280px" in teach_content and "280px" in teach_content
        teach_checks["Canvas resize触发"] = "i===3" in teach_content and "resizeCanvas" in teach_content
    
    # 检查角色多样性（统计角色出现次数）
    roles = re.findall(r'assets/peppa/([\w-]+)\.png', teach_content)
    role_counts = {}
    for role in roles:
        role_counts[role] = role_counts.get(role, 0) + 1
    max_repeat = max(role_counts.values()) if role_counts else 0
    teach_checks["角色多样性(≤2次)"] = max_repeat <= 2
    
    # 检查 review.html
    review_file = course_path / "review.html"
    review_content = review_file.read_text()
    
    review_checks = {
        "移动端CSS": "@media(max-width:480px)" in review_content,
        "playOk函数": "function playOk()" in review_content or "playOk=()=>" in review_content,
        "playNo函数": "function playNo()" in review_content or "playNo=()=>" in review_content,
        "speak函数": "function speak(" in review_content or "speak=(" in review_content,
        "audioCache": "audioCache" in review_content,
    }
    
    # 检查角色多样性
    roles_r = re.findall(r'assets/peppa/([\w-]+)\.png', review_content)
    role_counts_r = {}
    for role in roles_r:
        role_counts_r[role] = role_counts_r.get(role, 0) + 1
    max_repeat_r = max(role_counts_r.values()) if role_counts_r else 0
    review_checks["角色多样性(≤2次)"] = max_repeat_r <= 2
    
    results.append({
        "course": course_name,
        "teach": teach_checks,
        "review": review_checks,
        "teach_roles": role_counts,
        "review_roles": role_counts_r
    })

# 输出结果
for r in results:
    print(f"\n{'='*60}")
    print(f"课件: {r['course']}")
    print(f"{'='*60}")
    
    print("\n📝 teach.html:")
    for k, v in r['teach'].items():
        status = "✅" if v else "❌"
        print(f"  {status} {k}")
    print(f"  角色统计: {len(r['teach_roles'])}种角色")
    for role, count in sorted(r['teach_roles'].items(), key=lambda x: -x[1])[:3]:
        print(f"    - {role}: {count}次")
    
    print("\n📝 review.html:")
    for k, v in r['review'].items():
        status = "✅" if v else "❌"
        print(f"  {status} {k}")
    print(f"  角色统计: {len(r['review_roles'])}种角色")
    for role, count in sorted(r['review_roles'].items(), key=lambda x: -x[1])[:3]:
        print(f"    - {role}: {count}次")

# 总结
print(f"\n{'='*60}")
print("总结")
print(f"{'='*60}")
all_pass = all(
    all(r['teach'].values()) and all(r['review'].values())
    for r in results
)
if all_pass:
    print("✅ 所有检查项通过")
else:
    print("❌ 发现问题，需要修复")
