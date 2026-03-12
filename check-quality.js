const fs = require('fs');
const path = require('path');

const levels = [
  { name: 'phonics-1', range: [1, 26] },
  { name: 'phonics-2', range: [27, 41] },
  { name: 'phonics-3', range: [42, 52] },
  { name: 'phonics-4', range: [62, 81] },
  { name: 'phonics-5', range: [82, 101] }
];

const issues = [];
let totalChecked = 0;

// 检查单个HTML文件
function checkFile(filePath, lessonNum, type) {
  if (!fs.existsSync(filePath)) return;
  
  const content = fs.readFileSync(filePath, 'utf8');
  const folder = path.basename(path.dirname(filePath));
  
  // 1. 移动端CSS检查
  if (!content.includes('@media(max-width:480px)') && !content.includes('@media (max-width:480px)')) {
    issues.push(`P${lessonNum} ${type}: 缺少移动端CSS`);
  }
  
  // 2. 拼读字母换行检查（teach.html需要）
  if (type === 'teach' && content.includes('blend-box') && !content.includes('flex-wrap:wrap')) {
    issues.push(`P${lessonNum} ${type}: blend-box缺少flex-wrap:wrap`);
  }
  
  // 3. Canvas尺寸检查（Phonics 1需要280x280）
  if (lessonNum <= 26 && type === 'teach') {
    if (content.includes('traceCanvas') && !content.includes('280px')) {
      issues.push(`P${lessonNum} ${type}: Canvas尺寸不是280x280px`);
    }
  }
  
  // 4. 音效函数检查（review.html需要）
  if (type === 'review') {
    if (!content.includes('function playOk()') && !content.includes('playOk=()=>')) {
      issues.push(`P${lessonNum} ${type}: 缺少playOk函数`);
    }
    if (!content.includes('function playNo()') && !content.includes('playNo=()=>')) {
      issues.push(`P${lessonNum} ${type}: 缺少playNo函数`);
    }
  }
  
  // 5. 角色多样性检查（同课内重复≥3次）
  const characters = [
    'peppa-pig-happy-standing', 'george-standing', 'daddy-pig-standing',
    'daddy-pig-walking', 'mummy-pig-standing-grass', 'candy-cat-green-dress',
    'emily-elephant-standing', 'peppa-pig-red-polka-dot-dress',
    'peppa-fairy-princess', 'george-superhero-costume',
    'peppa-family-group-outdoors', 'peppa-and-george-ooo',
    'george_pig_dinosaur', 'george-playing-ball'
  ];
  
  const charCounts = {};
  characters.forEach(char => {
    const regex = new RegExp(char, 'g');
    const matches = content.match(regex);
    if (matches && matches.length >= 3) {
      charCounts[char] = matches.length;
    }
  });
  
  if (Object.keys(charCounts).length > 0) {
    const details = Object.entries(charCounts).map(([c, n]) => `${c}×${n}`).join(', ');
    issues.push(`P${lessonNum} ${type}: 角色重复≥3次 (${details})`);
  }
  
  totalChecked++;
}

// 遍历所有课件
levels.forEach(level => {
  const [start, end] = level.range;
  const lessonsDir = path.join(__dirname, 'lessons', level.name);
  
  if (!fs.existsSync(lessonsDir)) return;
  
  const folders = fs.readdirSync(lessonsDir);
  folders.forEach(folder => {
    const folderPath = path.join(lessonsDir, folder);
    if (!fs.statSync(folderPath).isDirectory()) return;
    
    // 从文件夹名推断课程编号
    const lessonNum = folders.indexOf(folder) + start;
    if (lessonNum > end) return;
    
    checkFile(path.join(folderPath, 'teach.html'), lessonNum, 'teach');
    checkFile(path.join(folderPath, 'review.html'), lessonNum, 'review');
  });
});

// 输出结果
console.log(`\n=== 自然拼读课件质量检查报告 ===`);
console.log(`检查文件数: ${totalChecked}`);
console.log(`发现问题数: ${issues.length}\n`);

if (issues.length === 0) {
  console.log('🎉 所有课件质量完美达标！');
} else {
  console.log('⚠️ 发现以下问题:\n');
  issues.forEach((issue, i) => {
    console.log(`${i + 1}. ${issue}`);
  });
}
