#!/usr/bin/env python3
import os
import re

# 缺少 playOk 的课件列表
missing_dirs = [
    'phonics-1/letter-b',
    'phonics-1/letter-d',
    'phonics-1/letter-e',
    'phonics-1/letter-n',
    'phonics-1/letter-p',
    'phonics-2/ap-family',
    'phonics-3/ea-sound',
    'phonics-3/oa-sound',
    'phonics-3/ue-sound',
    'phonics-4/ck-sound',
    'phonics-4/gr-blend',
    'phonics-4/ng-sound',
    'phonics-4/nk-sound',
    'phonics-4/tr-blend',
    'phonics-5/ar-sound',
    'phonics-5/er-sound',
    'phonics-5/igh-sound',
    'phonics-5/ir-sound',
    'phonics-5/le-ending',
    'phonics-5/or-sound',
    'phonics-5/soft-g',
    'phonics-5/ur-sound'
]

playok_code = '''function playOk(){
  const ctx=new AudioContext();
  const osc=ctx.createOscillator();
  const gain=ctx.createGain();
  osc.connect(gain);gain.connect(ctx.destination);
  osc.frequency.value=523;gain.gain.value=0.3;
  osc.start();osc.stop(ctx.currentTime+0.2);
}
'''

for dir_path in missing_dirs:
    file_path = f'lessons/{dir_path}/teach.html'
    if not os.path.exists(file_path):
        print(f'❌ 文件不存在: {file_path}')
        continue
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否已有 playOk
    if 'function playOk' in content:
        print(f'✅ 已有 playOk: {dir_path}')
        continue
    
    # 在 showConfetti 函数后添加 playOk
    if 'function showConfetti' in content:
        content = content.replace(
            'function showConfetti(){',
            playok_code + '\nfunction showConfetti(){'
        )
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f'✅ 修复完成: {dir_path}')
    else:
        print(f'⚠️  未找到 showConfetti: {dir_path}')

print('\n🎉 批量修复完成！')
