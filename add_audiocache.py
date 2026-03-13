#!/usr/bin/env python3
import re
from pathlib import Path

files = [
    "lessons/level-4/helping-at-home/review.html",
    "lessons/level-2/where-we-go/review.html",
    "lessons/level-2/daily-actions/review.html"
]

for f in files:
    path = Path(f)
    content = path.read_text()
    
    # 提取单词列表（从 alt 属性）
    words = list(set(re.findall(r'alt="(\w+)"', content)))
    words = [w for w in words if len(w) > 2]  # 过滤短词
    
    if 'audioCache' in content:
        print(f"✅ {f}: 已有 audioCache，跳过")
        continue
    
    # 构建 audioCache 代码
    cache_code = f"var audioCache={{}};\nvar words={words};\nwords.forEach(function(w){{var a=new Audio('https://dict.youdao.com/dictvoice?audio='+w+'&type=2');a.load();audioCache[w]=a}});\n"
    
    # 在 speak 函数前插入
    content = re.sub(
        r'(function speak\()',
        cache_code + r'\1',
        content,
        count=1
    )
    
    # 修改 speak 函数使用缓存
    old_speak = r"function speak\(t\)\{[^}]+var a=new Audio\(primary\);[^}]+\}"
    new_speak = """function speak(t,cb){
if(audioCache[t]){
audioCache[t].currentTime=0;
audioCache[t].play().then(function(){cb&&cb()}).catch(function(){});
}else{
var primary='https://dict.youdao.com/dictvoice?audio='+encodeURIComponent(t)+'&type=2';
var a=new Audio(primary);
a.play().then(function(){cb&&cb()}).catch(function(){});
}}"""
    
    content = re.sub(old_speak, new_speak, content, flags=re.DOTALL)
    
    path.write_text(content)
    print(f"✅ {f}: audioCache 已添加（{len(words)}个单词）")

print("\n完成")
