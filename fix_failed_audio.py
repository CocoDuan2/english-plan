#!/usr/bin/env python3
"""
修复16个无法自动升级的课件（单词为纯字符串数组格式）
"""
import os
import re

# 新版 speak() 函数模板
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

# 各课件的单词列表
WORD_LISTS = {
    'phonics-1/letter-e': ['egg', 'elephant', 'elbow', 'exit'],
    'phonics-1/letter-j': ['jump', 'juice', 'jelly', 'jar'],
    'phonics-2/ip-family': ['zip', 'tip', 'lip', 'ship', 'trip'],
    'phonics-2/ug-family': ['bug', 'hug', 'mug', 'rug', 'tug'],
    'phonics-2/un-family': ['sun', 'run', 'fun', 'bun', 'gun'],
    'phonics-2/ut-family': ['cut', 'nut', 'hut', 'but', 'shut'],
    'phonics-3/ai-ay': ['rain', 'train', 'play', 'day'],
    'phonics-3/ue-sound': ['blue', 'glue', 'true', 'clue'],
    'phonics-4/bl-blend': ['blue', 'black', 'block', 'blow'],
    'phonics-4/ck-sound': ['duck', 'clock', 'black', 'truck'],
    'phonics-4/gl-blend': ['glass', 'glove', 'glad', 'glue'],
    'phonics-4/ng-sound': ['sing', 'ring', 'king', 'long'],
    'phonics-5/er-sound': ['her', 'fern', 'term', 'verb'],
    'phonics-5/grand-review': ['apple', 'cat', 'bike', 'boat', 'clap', 'star', 'book', 'night'],
    'phonics-5/oo-short': ['book', 'look', 'cook', 'good'],
    'phonics-5/y-as-ee': ['happy', 'baby', 'funny', 'sunny'],
}

def find_func_end(s, start):
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

def build_preload_and_cache(words):
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

base = '/Users/cass/.openclaw/workspace-english-tutor/english-plan/lessons'
upgraded = 0
failed = []

print("=== 修复 16 个失败的课件 ===\n")

for rel_path, words in WORD_LISTS.items():
    filepath = os.path.join(base, rel_path, 'review.html')
    if not os.path.exists(filepath):
        print(f"  ⚠️  文件不存在: {rel_path}")
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # 1. 替换 speak() 函数
    speak_start = content.find('function speak(')
    if speak_start == -1:
        print(f"  ❌ {rel_path}: no speak() function")
        failed.append(rel_path)
        continue
    
    brace_start = content.find('{', speak_start)
    brace_end = find_func_end(content, brace_start)
    if brace_end == -1:
        print(f"  ❌ {rel_path}: unmatched brace")
        failed.append(rel_path)
        continue
    
    old_speak = content[speak_start:brace_end+1]
    content = content.replace(old_speak, NEW_SPEAK_FUNC, 1)
    
    # 2. 移除旧预加载代码
    content = re.sub(
        r'//\s*Preload audio\s*\n\s*const preloadWords\s*=\s*\[[^\]]*\];\s*\n\s*preloadWords\.forEach\([^;]+;\s*\}\);\s*',
        '', content
    )
    content = re.sub(
        r'const preloadWords\s*=\s*\[[^\]]*\];\s*\npreloadWords\.forEach\([^;]+;\s*\}\);\s*',
        '', content
    )
    content = re.sub(r'const audioCache\s*=\s*\{\};\s*\n', '', content)
    
    # 3. 插入 audioCache 初始化
    cache_code = build_preload_and_cache(words)
    speak_pos = content.find('function speak(')
    if speak_pos != -1:
        content = content[:speak_pos] + cache_code + '\n' + content[speak_pos:]
    
    if content == original:
        print(f"  ⚠️  {rel_path}: no change")
    else:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        upgraded += 1
        print(f"  ✅ {rel_path}: upgraded ({len(words)} words: {', '.join(words[:4])}{'...' if len(words)>4 else ''})")

print(f"\n=== 完成 ===")
print(f"成功: {upgraded} 个")
print(f"失败: {len(failed)} 个")
