#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const altChars = {
  'peppa-pig-happy-standing': 'peppa-pig-red-polka-dot-dress',
  'george-standing': 'george_pig_dinosaur',
  'daddy-pig-standing': 'daddy-pig-walking',
  'mummy-pig-standing-grass': 'emily-elephant-standing',
  'candy-cat-green-dress': 'peppa-fairy-princess',
  'emily-elephant-standing': 'candy-cat-green-dress',
  'peppa-pig-red-polka-dot-dress': 'peppa-fairy-princess',
  'peppa-fairy-princess': 'peppa-pig-red-polka-dot-dress',
  'george-superhero-costume': 'george-playing-ball',
  'george_pig_dinosaur': 'george-superhero-costume',
  'george-playing-ball': 'george_pig_dinosaur',
  'daddy-pig-walking': 'daddy-pig-standing'
};

const dirs = fs.readdirSync(path.join(__dirname, 'lessons'), {withFileTypes: true})
  .filter(d => d.isDirectory() && d.name.startsWith('phonics-'))
  .map(d => d.name);

dirs.forEach(dir => {
  const subDirs = fs.readdirSync(path.join(__dirname, 'lessons', dir), {withFileTypes: true})
    .filter(d => d.isDirectory());
  
  subDirs.forEach(sub => {
    const fp = path.join(__dirname, 'lessons', dir, sub.name, 'teach.html');
    if (!fs.existsSync(fp)) return;
    
    let content = fs.readFileSync(fp, 'utf8');
    const s1Match = content.match(/<!-- S1:.*?-->([\s\S]*?)<!-- S2:/);
    const s2Match = content.match(/<!-- S2: Hello -->([\s\S]*?)<!-- S3:/);
    
    if (!s1Match || !s2Match) return;
    
    const s1Char = s1Match[1].match(/peppa\/([^"]+)\.png/)?.[1];
    const s2Char = s2Match[1].match(/peppa\/([^"]+)\.png/)?.[1];
    
    if (s1Char && s2Char && s1Char === s2Char && altChars[s1Char]) {
      const newChar = altChars[s1Char];
      content = content.replace(
        /<!-- S2: Hello -->([\s\S]*?)<img src="[^"]*peppa\/[^"]+\.png"/,
        `<!-- S2: Hello -->$1<img src="../../../assets/peppa/${newChar}.png"`
      );
      fs.writeFileSync(fp, content);
      console.log(`✅ ${dir}/${sub.name}`);
    }
  });
});
