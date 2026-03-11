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
  'phonics-2/ug-family', 'phonics-2/in-family', 'phonics-2/ip-family',
  'phonics-3/ai-ay', 'phonics-4/ng-sound', 'phonics-4/ck-sound',
  'phonics-4/bl-blend', 'phonics-5/er-sound', 'phonics-5/y-as-ee',
  'phonics-5/oo-short'
];

files.forEach(f => {
  const fp = path.join(__dirname, 'lessons', f, 'review.html');
  if (!fs.existsSync(fp)) return;
  
  let content = fs.readFileSync(fp, 'utf8');
  const used = new Set();
  let idx = 0;
  let changed = false;
  
  content = content.replace(
    /<img src="(\.\.\/\.\.\/\.\.\/assets\/peppa\/)([^"]+)(\.png"[^>]*>)/g,
    (m, pre, char, suf) => {
      if (used.has(char)) {
        let nc = chars[idx++ % chars.length];
        while (used.has(nc)) nc = chars[idx++ % chars.length];
        used.add(nc);
        changed = true;
        return `<img src="${pre}${nc}${suf}`;
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
