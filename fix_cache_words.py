#!/usr/bin/env python3
"""
修复 audioCache 单词列表不完整的课件
"""
import os
import re

# 需要修复的课件和正确的单词列表
FIXES = {
    'phonics-5/aw-au': ['saw', 'paw', 'draw', 'sauce'],
    'phonics-5/ew-sound': ['new', 'few', 'blew', 'stew'],
    'phonics-5/ie-sound': ['pie', 'tie', 'lie', 'die'],
    'phonics-5/oi-oy': ['coin', 'oil', 'boy', 'toy'],
    'phonics-5/ou-ow': ['house', 'mouse', 'cow', 'now'],
}

base = '/Users/cass/.openclaw/workspace-english-tutor/english-plan/lessons'

print("=== 修复 audioCache 单词列表 ===\n")

for rel_path, correct_words in FIXES.items():
    filepath = os.path.join(base, rel_path, 'review.html')
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 找到并替换 audioCache 初始化块中的 words 数组
    # 模式: const words=['saw'];
    old_pattern = re.compile(r"(const audioCache=\{\};\s*\(function\(\)\{\s*const words=\[)[^\]]*(\];)")
    new_words_str = "'" + "','".join(correct_words) + "'"
    
    new_content = old_pattern.sub(r'\g<1>' + new_words_str + r'\g<2>', content)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  ✅ {rel_path}: {correct_words}")
    else:
        # 尝试更宽松的模式
        old_pattern2 = re.compile(r"(const audioCache=\{\};\s*\(function\(\)\{[^}]*?const words=\[)[^\]]*(\])", re.DOTALL)
        m = old_pattern2.search(content)
        if m:
            new_content = old_pattern2.sub(r'\g<1>' + new_words_str + r'\g<2>', content)
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"  ✅ {rel_path}: {correct_words} (pattern2)")
            else:
                print(f"  ⚠️  {rel_path}: no change")
        else:
            print(f"  ❌ {rel_path}: pattern not found")
            # 打印相关内容供调试
            m2 = re.search(r'const audioCache=\{', content)
            if m2:
                print(f"     context: {content[m2.start():m2.start()+200]}")

print("\n=== 验证 ===")
for rel_path, correct_words in FIXES.items():
    filepath = os.path.join(base, rel_path, 'review.html')
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    # 检查所有单词是否都在 audioCache 初始化中
    cache_block = re.search(r'const audioCache=\{\}.*?\}\)\(\);', content, re.DOTALL)
    if cache_block:
        block = cache_block.group()
        missing = [w for w in correct_words if f"'{w}'" not in block]
        if missing:
            print(f"  ❌ {rel_path}: missing {missing}")
        else:
            print(f"  ✅ {rel_path}: all {len(correct_words)} words cached")
