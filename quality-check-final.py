#!/usr/bin/env python3
"""自然拼读课件最终质量检查"""
import re
from pathlib import Path
from collections import Counter

def check_mobile_css(content):
    """检查移动端CSS"""
    return bool(re.search(r'@media\s*\(\s*max-width\s*:\s*480px\s*\)', content))

def check_flex_wrap(content):
    """检查拼读字母换行"""
    mobile_section = re.search(r'@media\s*\(\s*max-width\s*:\s*480px\s*\).*?(?=@media|</style>|$)', content, re.DOTALL)
    if mobile_section:
        return 'flex-wrap' in mobile_section.group(0)
    return False

def check_canvas_size(content):
    """检查Canvas尺寸（仅Phonics 1需要）"""
    mobile_section = re.search(r'@media\s*\(\s*max-width\s*:\s*480px\s*\).*?(?=@media|</style>|$)', content, re.DOTALL)
    if mobile_section:
        canvas_match = re.search(r'\.trace-container\s*\{[^}]*width\s*:\s*(\d+)px', mobile_section.group(0))
        if canvas_match:
            return int(canvas_match.group(1)) >= 280
    return True  # 如果没有Canvas，视为通过

def check_audio_functions(content):
    """检查音效函数（review.html）"""
    has_speak = 'function speak(' in content or 'const speak=' in content
    has_playok = 'function playOk(' in content or 'const playOk=' in content
    has_playno = 'function playNo(' in content or 'const playNo=' in content
    return has_speak and has_playok and has_playno

def extract_characters(content):
    """提取课件中使用的角色图片"""
    chars = re.findall(r'assets/peppa/([a-z-]+)\.png', content)
    return chars

def check_consecutive_chars(files):
    """检查连续课件是否使用相同首页角色"""
    first_chars = []
    for f in sorted(files):
        content = f.read_text(encoding='utf-8')
        # 提取首页角色（通常在S1或开始页）
        s1_match = re.search(r'<!--\s*S1[:\s].*?-->(.*?)<!--\s*S2', content, re.DOTALL)
        if s1_match:
            chars = re.findall(r'assets/peppa/([a-z-]+)\.png', s1_match.group(1))
            if chars:
                first_chars.append((f.name, chars[0]))
    
    # 检查连续3课
    issues = []
    for i in range(len(first_chars) - 2):
        if first_chars[i][1] == first_chars[i+1][1] == first_chars[i+2][1]:
            issues.append(f"{first_chars[i][0]}, {first_chars[i+1][0]}, {first_chars[i+2][0]} 连续使用 {first_chars[i][1]}")
    return issues

def check_same_lesson_chars(content, filename):
    """检查同一课件内角色重复≥3次"""
    chars = extract_characters(content)
    counter = Counter(chars)
    repeated = {char: count for char, count in counter.items() if count >= 3}
    return repeated

# 主检查
base = Path('lessons')
issues = []

print("🔍 开始全量质量检查...\n")

# 1. 移动端CSS检查
print("1️⃣ 检查移动端CSS...")
no_mobile_css = []
for f in base.rglob('*.html'):
    content = f.read_text(encoding='utf-8')
    if not check_mobile_css(content):
        no_mobile_css.append(str(f))

if no_mobile_css:
    print(f"❌ {len(no_mobile_css)} 个文件缺少移动端CSS")
    for f in no_mobile_css[:5]:
        print(f"   - {f}")
else:
    print("✅ 全部通过")

# 2. 拼读字母换行检查
print("\n2️⃣ 检查拼读字母换行...")
no_flex_wrap = []
for f in base.rglob('teach.html'):
    content = f.read_text(encoding='utf-8')
    if not check_flex_wrap(content):
        no_flex_wrap.append(str(f))

if no_flex_wrap:
    print(f"❌ {len(no_flex_wrap)} 个teach.html缺少flex-wrap")
    for f in no_flex_wrap[:5]:
        print(f"   - {f}")
else:
    print("✅ 全部通过")

# 3. Canvas尺寸检查（仅Phonics 1）
print("\n3️⃣ 检查Canvas尺寸（Phonics 1）...")
wrong_canvas = []
for f in (base / 'phonics-1').rglob('teach.html'):
    content = f.read_text(encoding='utf-8')
    if not check_canvas_size(content):
        wrong_canvas.append(str(f))

if wrong_canvas:
    print(f"❌ {len(wrong_canvas)} 个文件Canvas尺寸不正确")
    for f in wrong_canvas:
        print(f"   - {f}")
else:
    print("✅ 全部通过")

# 4. 音效函数检查（review.html）
print("\n4️⃣ 检查音效函数（review.html）...")
missing_audio = []
for f in base.rglob('review.html'):
    content = f.read_text(encoding='utf-8')
    if not check_audio_functions(content):
        missing_audio.append(str(f))

if missing_audio:
    print(f"❌ {len(missing_audio)} 个review.html缺少音效函数")
    for f in missing_audio[:5]:
        print(f"   - {f}")
else:
    print("✅ 全部通过")

# 5. 角色多样性检查
print("\n5️⃣ 检查角色多样性...")

# 5a. 同课内角色重复≥3次
print("   5a. 同课内角色重复...")
same_lesson_issues = []
for f in base.rglob('*.html'):
    content = f.read_text(encoding='utf-8')
    repeated = check_same_lesson_chars(content, f.name)
    if repeated:
        same_lesson_issues.append((str(f), repeated))

if same_lesson_issues:
    print(f"❌ {len(same_lesson_issues)} 个课件存在同课内角色重复≥3次")
    for f, chars in same_lesson_issues[:5]:
        print(f"   - {f}: {chars}")
else:
    print("✅ 全部通过")

# 5b. 连续3课使用相同首页角色
print("   5b. 连续课件首页角色...")
teach_files = sorted(base.rglob('teach.html'))
consecutive = check_consecutive_chars(teach_files)

if consecutive:
    print(f"❌ 发现 {len(consecutive)} 处连续重复")
    for issue in consecutive:
        print(f"   - {issue}")
else:
    print("✅ 全部通过")

# 总结
print("\n" + "="*60)
total_issues = len(no_mobile_css) + len(no_flex_wrap) + len(wrong_canvas) + len(missing_audio) + len(same_lesson_issues) + len(consecutive)
if total_issues == 0:
    print("🎉 全部检查通过！所有课件质量达标！")
else:
    print(f"⚠️  发现 {total_issues} 个问题需要修复")
