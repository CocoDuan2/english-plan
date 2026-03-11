#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

// 可用角色池（排除 family-group 和 peppa-and-george，它们适合首页/结尾）
const characters = [
  'peppa-pig-happy-standing',
  'george-standing',
  'daddy-pig-standing',
  'daddy-pig-walking',
  'mummy-pig-standing-grass',
  'candy-cat-green-dress',
  'emily-elephant-standing',
  'peppa-pig-red-polka-dot-dress',
  'peppa-fairy-princess',
  'george-superhero-costume',
  'george_pig_dinosaur',
  'george-playing-ball'
];

// 需要修复的课件列表（角色重复 >= 3 次）
const filesToFix = [
  './phonics-1/letter-r/teach.html',
  './phonics-1/letter-u/teach.html',
  './phonics-1/letter-a/teach.html',
  './phonics-1/letter-t/teach.html',
  './phonics-1/letter-s/teach.html',
  './phonics-1/letter-z/teach.html',
  './phonics-1/letter-x/teach.html',
  './phonics-1/letter-v/teach.html',
  './phonics-1/letter-q/teach.html',
  './phonics-1/letter-w/teach.html',
  './phonics-1/letter-y/teach.html',
  './phonics-1/letter-l/teach.html',
  './phonics-1/letter-b/teach.html',
  './phonics-2/an-family/teach.html',
  './phonics-2/ap-family/teach.html',
  './phonics-3/e-e-magic/teach.html',
  './phonics-3/o-e-magic/teach.html',
  './phonics-3/i-e-magic/teach.html',
  './phonics-3/u-e-magic/teach.html',
  './phonics-3/a-e-magic/teach.html',
  './phonics-4/br-blend/teach.html',
  './phonics-5/grand-review/teach.html',
  './phonics-5/oi-oy/teach.html'
];

function fixFile(filePath) {
  const fullPath = path.join(__dirname, 'lessons', filePath);
  let content = fs.readFileSync(fullPath, 'utf8');
  
  // 找出所有 .pr 区块中的角色图片
  const prBlocks = content.match(/<div class="pr">[\s\S]*?<\/div>/g) || [];
  
  if (prBlocks.length === 0) return;
  
  // 统计当前使用的角色
  const usedChars = {};
  prBlocks.forEach(block => {
    const match = block.match(/peppa\/([^"]+)\.png/);
    if (match) {
      const char = match[1];
      usedChars[char] = (usedChars[char] || 0) + 1;
    }
  });
  
  // 找出重复次数最多的角色
  const sortedChars = Object.entries(usedChars).sort((a, b) => b[1] - a[1]);
  
  if (sortedChars.length === 0 || sortedChars[0][1] < 3) return;
  
  console.log(`\n修复: ${filePath}`);
  console.log(`  重复角色: ${sortedChars[0][0]} (${sortedChars[0][1]}次)`);
  
  // 替换策略：保留首页和结尾的角色，替换中间重复的
  let charIndex = 0;
  let replacementCount = 0;
  const usedInFile = new Set();
  
  // 第一遍：标记首页和结尾
  const slides = content.split(/<div class="slide"/);
  
  slides.forEach((slide, idx) => {
    if (idx === 0) return; // 跳过 head 部分
    
    const prMatch = slide.match(/<div class="pr">[\s\S]*?<img src="\.\.\/\.\.\/\.\.\/assets\/peppa\/([^"]+)\.png"/);
    if (prMatch) {
      const char = prMatch[1];
      if (idx === 1 || idx === slides.length - 1) {
        // 首页和结尾，保留
        usedInFile.add(char);
      }
    }
  });
  
  // 第二遍：替换中间重复的角色
  let newContent = content;
  const overusedChar = sortedChars[0][0];
  let occurrenceCount = 0;
  
  newContent = newContent.replace(
    /<div class="pr">([\s\S]*?)<img src="(\.\.\/\.\.\/\.\.\/assets\/peppa\/)([^"]+)(\.png"[^>]*>)([\s\S]*?)<\/div>/g,
    (match, before, pathPrefix, charName, pathSuffix, after) => {
      if (charName === overusedChar) {
        occurrenceCount++;
        // 保留第1次和最后1次，替换中间的
        if (occurrenceCount > 1 && occurrenceCount < usedChars[overusedChar]) {
          // 找一个未使用的角色
          let newChar = characters[charIndex % characters.length];
          while (usedInFile.has(newChar) || newChar === overusedChar) {
            charIndex++;
            newChar = characters[charIndex % characters.length];
          }
          usedInFile.add(newChar);
          charIndex++;
          replacementCount++;
          return `<div class="pr">${before}<img src="${pathPrefix}${newChar}${pathSuffix}${after}</div>`;
        }
      }
      return match;
    }
  );
  
  if (replacementCount > 0) {
    fs.writeFileSync(fullPath, newContent, 'utf8');
    console.log(`  ✅ 替换了 ${replacementCount} 处`);
  }
}

// 执行修复
filesToFix.forEach(fixFile);
console.log('\n✅ 修复完成！');
