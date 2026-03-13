#!/usr/bin/env python3
"""
批量升级自然拼读 review.html 的音频缓存机制
将 speak() 函数升级为 audioCache 模式，并添加预加载
"""
import os
import re
import glob

# 新版 speak() 函数模板（带 audioCache）
NEW_SPEAK_FUNC = '''function speak(w,cb){
  const finish=()=>{if(cb)cb()};
  if(audioCache[w]){
    audioCache[w].currentTime=0;
    audioCache[w].play().then(()=>{
      audioCache[w].onended=finish;
      setTimeout(finish,4000);
    }).catch(()=>{
      const u2=`https://fanyi.baidu.com/gettts?lan=en&text=${encodeURIComponent(w)}&spd=4&source=web`;
      const a2=new Audio(u2);
      a2.play().then(()=>{a2.onended=finish;setTimeout(finish,4000)}).catch(()=>{
        finish();
        if(typeof showAudioError==='function')showAudioError();
      });
    });
  }else{
    const u=`https://dict.youdao.com/dictvoice?audio=${encodeURIComponent(w)}&type=2`;
    const a=new Audio(u);
    a.play().then(()=>{a.onended=finish;setTimeout(finish,4000)}).catch(()=>{
      const u2=`https://fanyi.baidu.com/gettts?lan=en&text=${encodeURIComponent(w)}&spd=4&source=web`;
      const a2=new Audio(u2);
      a2.play().then(()=>{a2.onended=finish;setTimeout(finish,4000)}).catch(()=>{
        finish();
        if(typeof showAudioError==='function')showAudioError();
      });
    });
  }
}'''

def extract_words_from_review(content):
    """从 review.html 中提取单词列表"""
    # 尝试多种模式
    patterns = [
        # words = [{w:'apple', ...}, ...]
        r"const\s+words\s*=\s*\[(.*?)\]",
        # words=[{w:'...'},...]
        r"words\s*=\s*\[(.*?)\]",
    ]
    for pat in patterns:
        m = re.search(pat, content, re.DOTALL)
        if m:
            arr_str = m.group(1)
            # 提取所有 w:'...' 或 w:"..."
            words = re.findall(r"w\s*:\s*['\"]([^'\"]+)['\"]", arr_str)
            if words:
                return list(dict.fromkeys(words))  # 去重保序
    
    # 尝试 blendWords
    m = re.search(r"blendWords\s*=\s*\[(.*?)\]", content, re.DOTALL)
    if m:
        words = re.findall(r"['\"]([a-z]+)['\"]", m.group(1))
        if words:
            return list(dict.fromkeys(words))
    
    return []

def build_preload_and_cache(words):
    """生成 audioCache 初始化 + 预加载代码"""
    if not words:
        return ""
    
    words_js = "['" + "','".join(words) + "']"
    return f"""
// Audio cache
const audioCache={{}};
(function(){{
  const words={words_js};
  words.forEach(w=>{{
    const a=new Audio(`https://dict.youdao.com/dictvoice?audio=${{encodeURIComponent(w)}}&type=2`);
    a.load();
    audioCache[w]=a;
  }});
}})();"""

def upgrade_review_html(filepath):
    """升级单个 review.html 文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # 检查是否已有完整 audioCache 模式（audioCache 对象定义）
    if 'const audioCache=' in content or 'const audioCache =' in content:
        # 已有 audioCache，只检查 speak() 是否是旧版
        if 'audioCache[w]' in content:
            # 已是最新版，跳过
            return False, "already_upgraded"
    
    # 提取单词列表
    words = extract_words_from_review(content)
    if not words:
        return False, "no_words_found"
    
    # 1. 替换 speak() 函数
    # 匹配各种格式的 speak 函数
    speak_patterns = [
        # function speak(w,cb){...}
        r'function speak\(w(?:,cb)?\)\s*\{[^}]*(?:\{[^}]*\}[^}]*)*\}',
        # function speak(w){...} 含嵌套
    ]
    
    # 使用更健壮的方式：找到 function speak 开始，然后匹配括号
    def find_func_end(s, start):
        """找到函数的结束括号位置"""
        depth = 0
        i = start
        while i < len(s):
            if s[i] == '{':
                depth += 1
            elif s[i] == '}':
                depth -= 1
                if depth == 0:
                    return i
            i += 1
        return -1
    
    speak_start = content.find('function speak(')
    if speak_start == -1:
        return False, "no_speak_func"
    
    # 找函数体开始的 {
    brace_start = content.find('{', speak_start)
    if brace_start == -1:
        return False, "no_speak_brace"
    
    brace_end = find_func_end(content, brace_start)
    if brace_end == -1:
        return False, "unmatched_brace"
    
    old_speak = content[speak_start:brace_end+1]
    content = content.replace(old_speak, NEW_SPEAK_FUNC, 1)
    
    # 2. 移除旧的 preloadWords 代码
    # 模式1: // Preload audio\nconst preloadWords=[...]\npreloadWords.forEach(...)
    content = re.sub(
        r'//\s*Preload audio\s*\n\s*const preloadWords\s*=\s*\[[^\]]*\];\s*\n\s*preloadWords\.forEach\([^;]+;\s*\}\);\s*',
        '',
        content
    )
    # 模式2: const preloadWords=[...]; preloadWords.forEach(...)
    content = re.sub(
        r'const preloadWords\s*=\s*\[[^\]]*\];\s*\npreloadWords\.forEach\([^;]+;\s*\}\);\s*',
        '',
        content
    )
    
    # 移除旧的简单 audioCache 定义（如果只是部分实现）
    content = re.sub(r'const audioCache\s*=\s*\{\};\s*\n', '', content)
    
    # 3. 在 speak() 函数前面插入 audioCache 初始化代码
    cache_code = build_preload_and_cache(words)
    
    # 找插入位置（speak 函数之前）
    speak_pos = content.find('function speak(')
    if speak_pos != -1:
        content = content[:speak_pos] + cache_code + '\n' + content[speak_pos:]
    
    if content == original:
        return False, "no_change"
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True, f"upgraded ({len(words)} words: {', '.join(words[:4])}{'...' if len(words)>4 else ''})"

# 处理所有自然拼读课件
base = '/Users/cass/.openclaw/workspace-english-tutor/english-plan/lessons'
phonics_dirs = sorted(glob.glob(os.path.join(base, 'phonics-*')))

total = 0
upgraded = 0
skipped = 0
failed = []

print("=== 批量升级自然拼读 review.html 音频缓存 ===\n")

for phonics_dir in phonics_dirs:
    lesson_dirs = sorted(os.listdir(phonics_dir))
    for lesson in lesson_dirs:
        review_path = os.path.join(phonics_dir, lesson, 'review.html')
        if not os.path.exists(review_path):
            continue
        total += 1
        success, msg = upgrade_review_html(review_path)
        short_path = review_path.replace(base + '/', '')
        if success:
            upgraded += 1
            print(f"  ✅ {short_path}: {msg}")
        elif msg == "already_upgraded":
            skipped += 1
            # print(f"  ⏭  {short_path}: already upgraded")
        elif msg == "no_change":
            skipped += 1
        else:
            failed.append((short_path, msg))
            print(f"  ❌ {short_path}: {msg}")

print(f"\n=== 完成 ===")
print(f"总计: {total} 个课件")
print(f"升级: {upgraded} 个")
print(f"跳过: {skipped} 个（已是最新版）")
print(f"失败: {len(failed)} 个")
if failed:
    print("\n失败列表:")
    for path, msg in failed:
        print(f"  {path}: {msg}")
