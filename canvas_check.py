import os
import re

phonics_1_teach = []
for letter in "abcdefghijklmnopqrstuvwxyz":
    file = f"lessons/phonics-1/letter-{letter}/teach.html"
    if os.path.exists(file):
        phonics_1_teach.append(file)

canvas_sizes = []
for file in phonics_1_teach[:5]:  # 只检查前5个
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 多种匹配方式
    patterns = [
        r'canvas\.width\s*=\s*(\d+)',
        r'canvas\.height\s*=\s*(\d+)',
        r'width:\s*(\d+)px.*height:\s*(\d+)px',
    ]
    
    found = False
    for pattern in patterns:
        match = re.search(pattern, content)
        if match:
            canvas_sizes.append(f"{file.split('/')[-2]}: {match.group(1)}px")
            found = True
            break
    
    if not found:
        canvas_sizes.append(f"{file.split('/')[-2]}: 未找到Canvas")

print("Canvas尺寸检查（前5课）：")
for s in canvas_sizes:
    print(f"  {s}")

