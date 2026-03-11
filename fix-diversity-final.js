#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const chars = [
  'peppa-pig-happy-standing', 'george-standing', 'daddy-pig-standing',
  'daddy-pig-walking', 'mummy-pig-standing-grass', 'candy-cat-green-dress',
  'emily-elephant-standing', 'peppa-pig-red-polka-dot-dress',
  'peppa-fairy-princess', 'george-superhero-costume',
  'george_pig_dinosaur', 'george-playing-ball'
];

const files = [
  'phonics-1/letter-r', 'phonics-1/letter-u', 'phonics-1/letter-a',
  'phonics-1/letter-t', 'phonics-1/letter-s', 'phonics-1/letter-z',
  'phonics-1/letter-x', 'phonics-1/letter-v', 'phonics-1/letter-q',
  'phonics-1/letter-y', 'phonics-1/letter-l', 'phonics-1/letter-b',
  'phonics-2/an-family', 'phonics-2/ap-family',
  'phonics-3/e-e-magic', 'phonics-3/o-e-magic', 'phonics-3/i-e-magic',
  'phonics-3/u-e-magic', 'phonics-3/a-e-magic', 'phonics-4/br-blend',
  'phonics-5/grand-review', 'phonics-5/oi-oy'
];

files.forEach(f => {
  const fp = path.join(__dirname, 'lessons', f, 'teach.html');
  if (!fs.existsSync(fp)) return;
  
  let content = fs.readFileSync(fp, 'utf8');
  const used = new Set();
  let idx = 0;
  let changed = false;
  
  content = content.replace(
    /<div class="pr">([\s\S]*?)<img src="(\.\.\/\.\.\/\.\.\/assets\/peppa\/)([^"]+)(\.png"[^>]*>)([\s\S]*?)<\/div>/g,
    (m, b, pre, char, suf, a) => {
      if (used.has(char)) {
        let nc = chars[idx++ % chars.length];
        while (used.has(nc)) nc = chars[idx++ % chars.length];
        used.add(nc);
        changed = true;
        return `<div class="pr">${b}<img src="${pre}${nc}${suf}${a}</div>`;
      }
      used.add(char);
      return m;
    }
  );
  
  if (changed) {
    fs.writeFileSync(fp, content);
    console.log(`✅ ${f}`);
  }
});
