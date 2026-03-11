#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

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

const filesToFix = [
  './phonics-1/letter-r/teach.html',
  './phonics-1/letter-u/teach.html',
  './phonics-1/letter-a/teach.html',
  './phonics-1/letter-t/teach.html',
  './phonics-1/letter-s/teach.html',
  './phonics-1/letter-z/teach.html',
  './phonics-1/letter-x/teach.html',
  './phonics-1/letter-v/teach.html',
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
  './phonics-4/br-blend/teach.html'
];

function fixFile(filePath) {
  const fullPath = path.join(__dirname, 'lessons', filePath);
  let content = fs.readFileSync(fullPath, 'utf8');
  
  const usedChars = {};
  const prMatches = [...content.matchAll(/<div class="pr">[\s\S]*?peppa\/([^"]+)\.png/g)];
  
  prMatches.forEach(m => {
    usedChars[m[1]] = (usedChars[m[1]] || 0) + 1;
  });
  
  const maxUsage = Math.max(...Object.values(usedChars));
  if (maxUsage < 3) return;
  
  console.log(`\n${filePath}`);
  console.log(`  最多重复: ${maxUsage}次`);
  
  const usedInFile = new Set();
  let charIndex = 0;
  let count = 0;
  
  const newContent = content.replace(
    /<div class="pr">([\s\S]*?)<img src="(\.\.\/\.\.\/\.\.\/assets\/peppa\/)([^"]+)(\.png"[^>]*>)([\s\S]*?)<\/div>/g,
    (match, before, prefix, charName, suffix, after) => {
      count++;
      // 首页和最后一页保留
      if (count === 1 || count === prMatches.length) {
        usedInFile.add(charName);
        return match;
      }
      
      // 如果这个角色已经用过，换一个
      if (usedInFile.has(charName)) {
        let newChar = characters[charIndex % characters.length];
        let attempts = 0;
        while (usedInFile.has(newChar) && attempts < characters.length) {
          charIndex++;
          newChar = characters[charIndex % characters.length];
          attempts++;
        }
        if (!usedInFile.has(newChar)) {
          usedInFile.add(newChar);
          charIndex++;
          return `<div class="pr">${before}<img src="${prefix}${newChar}${suffix}${after}</div>`;
        }
      }
      
      usedInFile.add(charName);
      return match;
    }
  );
  
  fs.writeFileSync(fullPath, newContent, 'utf8');
  console.log(`  ✅ 已优化`);
}

filesToFix.forEach(fixFile);
console.log('\n✅ 完成！');
