import os
import re
from collections import defaultdict

# 检查连续课件的游戏类型和首页角色
phonics_1 = [f"lessons/phonics-1/letter-{c}/teach.html" for c in "abcdefghijklmnopqrstuvwxyz"]

# 检查游戏多样性（S9页面的游戏类型）
game_types = []
first_chars = []

for i, file in enumerate(phonics_1[:10]):  # 只检查前10课
    if not os.path.exists(file):
        continue
    
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取S9游戏类型
    s9_match = re.search(r'<!-- S9.*?-->(.*?)<!-- S10', content, re.DOTALL)
    if s9_match:
        s9_content = s9_match.group(1)
        if 'Find' in s9_content or 'find' in s9_content:
            game_types.append(f"P{i+1}: Find游戏")
        elif 'Match' in s9_content or 'match' in s9_content:
            game_types.append(f"P{i+1}: Match游戏")
        elif 'Catch' in s9_content or 'catch' in s9_content:
            game_types.append(f"P{i+1}: Catch游戏")
        else:
            game_types.append(f"P{i+1}: 其他游戏")
    
    # 提取首页角色（S1）
    s1_match = re.search(r'<!-- S1.*?assets/peppa/([\w-]+)\.png', content, re.DOTALL)
    if s1_match:
        first_chars.append(s1_match.group(1))

print("游戏类型分布（P1-P10）：")
for g in game_types:
    print(f"  {g}")

print("\n首页角色分布（P1-P10）：")
char_count = defaultdict(int)
for c in first_chars:
    char_count[c] += 1

for char, count in sorted(char_count.items(), key=lambda x: -x[1]):
    print(f"  {char}: {count}次")

# 检查连续重复
consecutive = []
for i in range(len(first_chars)-2):
    if first_chars[i] == first_chars[i+1] == first_chars[i+2]:
        consecutive.append(f"P{i+1}-P{i+3}: {first_chars[i]}")

if consecutive:
    print("\n⚠️ 发现连续3课相同角色：")
    for c in consecutive:
        print(f"  {c}")
else:
    print("\n✅ 无连续3课相同角色")

