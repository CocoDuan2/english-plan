const fs = require('fs');

const levels = {
  1: {
    title: 'Level 1 · 日常冒险',
    subtitle: '10 个故事 · 50 个单词',
    lessons: [
      {dir:'colorful-day',theme:'Peppa\'s Colorful Day',cn:'佩琪的彩色一天',words:'red, blue, yellow, green, orange',panel:'linear-gradient(135deg,#fce4ec,#f8bbd0)',teachIcon:'assets/peppa/peppa-pig-happy-standing.png',reviewIcon:'assets/peppa/peppa-pig-red-polka-dot-dress.png',teachTone:{bg:'#ffebee',bd:'#ef5350',txt:'#c62828'},reviewTone:{bg:'#fce4ec',bd:'#f06292',txt:'#c2185b'}},
      {dir:'visit-zoo',theme:'Visit the Zoo',cn:'去动物园',words:'cat, dog, fish, bird, duck',panel:'linear-gradient(135deg,#e8f5e9,#c8e6c9)',teachIcon:'assets/peppa/george-standing.png',reviewIcon:'assets/peppa/george_pig_dinosaur.png',teachTone:{bg:'#e8f5e9',bd:'#66bb6a',txt:'#2e7d32'},reviewTone:{bg:'#c8e6c9',bd:'#4caf50',txt:'#1b5e20'}},
      {dir:'morning-routine',theme:'Morning Routine',cn:'早晨起床',words:'head, eyes, ears, nose, mouth',panel:'linear-gradient(135deg,#E8D5F5,#D1C4E9)',teachIcon:'assets/peppa/mummy-pig-standing-grass.png',reviewIcon:'assets/peppa/george_pig_bubbles.png',teachTone:{bg:'#f3e5f5',bd:'#AB47BC',txt:'#7B1FA2'},reviewTone:{bg:'#E8D5F5',bd:'#CE93D8',txt:'#6A1B9A'}},
      {dir:'peppas-picnic',theme:'Peppa\'s Picnic',cn:'野餐时间',words:'apple, banana, milk, bread, egg',panel:'linear-gradient(135deg,#e8f5e9,#fff9c4)',teachIcon:'assets/peppa/peppa-family-group-outdoors.png',reviewIcon:'assets/peppa/peppa-pig-red-polka-dot-dress.png',teachTone:{bg:'#e8f5e9',bd:'#8BC34A',txt:'#33691e'},reviewTone:{bg:'#fff9c4',bd:'#ffa726',txt:'#e65100'}},
      {dir:'family-photo',theme:'Family Photo Day',cn:'全家福',words:'mom, dad, baby, brother, sister',panel:'linear-gradient(135deg,#f3e5f5,#e1bee7)',teachIcon:'assets/peppa/peppa-family-group-outdoors.png',reviewIcon:'assets/peppa/emily-elephant-standing.png',teachTone:{bg:'#f3e5f5',bd:'#ce93d8',txt:'#7b1fa2'},reviewTone:{bg:'#e1bee7',bd:'#ab47bc',txt:'#4a148c'}},
      {dir:'getting-dressed',theme:'Getting Dressed',cn:'穿衣服',words:'hat, shoes, shirt, pants, socks',panel:'linear-gradient(135deg,#e8f5e9,#c8e6c9)',teachIcon:'assets/peppa/peppa-pig-red-polka-dot-dress.png',reviewIcon:'assets/peppa/candy-cat-green-dress.png',teachTone:{bg:'#e8f5e9',bd:'#66bb6a',txt:'#2e7d32'},reviewTone:{bg:'#c8e6c9',bd:'#43a047',txt:'#1b5e20'}},
      {dir:'toy-box-fun',theme:'Toy Box Fun',cn:'玩具箱',words:'ball, car, doll, bear, block',panel:'linear-gradient(135deg,#fff8e1,#ffecb3)',teachIcon:'assets/peppa/george_pig_dinosaur.png',reviewIcon:'assets/peppa/peppa-pig-happy-standing.png',teachTone:{bg:'#fff8e1',bd:'#ff7043',txt:'#e65100'},reviewTone:{bg:'#ffecb3',bd:'#ff5722',txt:'#bf360c'}},
      {dir:'big-and-small',theme:'Big and Small',cn:'大小世界',words:'big, small, long, short, round',panel:'linear-gradient(135deg,#e8f5e9,#c8e6c9)',teachIcon:'assets/peppa/daddy-pig-standing.png',reviewIcon:'assets/peppa/george-standing.png',teachTone:{bg:'#e8f5e9',bd:'#66bb6a',txt:'#2e7d32'},reviewTone:{bg:'#c8e6c9',bd:'#43a047',txt:'#1b5e20'}},
      {dir:'counting-game',theme:'Counting Game',cn:'数数游戏',words:'one, two, three, four, five',panel:'linear-gradient(135deg,#fff3e0,#ffe0b2)',teachIcon:'assets/peppa/george-standing.png',reviewIcon:'assets/peppa/daddy-pig-standing.png',teachTone:{bg:'#fff3e0',bd:'#ff8f00',txt:'#e65100'},reviewTone:{bg:'#ffe0b2',bd:'#ff6d00',txt:'#bf360c'}},
      {dir:'playground-fun',theme:'Playground Fun',cn:'游乐场',words:'run, jump, walk, sit, stand',panel:'linear-gradient(135deg,#e8f5e9,#c8e6c9)',teachIcon:'assets/peppa/peppa_pig_arms_open.png',reviewIcon:'assets/peppa/george-playing-ball.png',teachTone:{bg:'#e8f5e9',bd:'#4caf50',txt:'#1b5e20'},reviewTone:{bg:'#c8e6c9',bd:'#66bb6a',txt:'#2e7d32'}}
    ]
  },
  2: {
    title: 'Level 2 · 社交世界',
    subtitle: '10 个故事 · 50 个单词',
    lessons: [
      {dir:'feelings-today',theme:'Feelings Today',cn:'今天的心情',words:'happy, sad, angry, scared, sleepy',panel:'linear-gradient(135deg,#fff3e0,#ffe0b2)',teachIcon:'assets/peppa/peppa-pig-happy-standing.png',reviewIcon:'assets/peppa/george-standing.png',teachTone:{bg:'#fff3e0',bd:'#ff9800',txt:'#e65100'},reviewTone:{bg:'#ffe0b2',bd:'#ff6d00',txt:'#bf360c'}},
      {dir:'weather-watch',theme:'Weather Watch',cn:'看天气',words:'sun, rain, cloud, wind, snow',panel:'linear-gradient(135deg,#e3f2fd,#bbdefb)',teachIcon:'assets/peppa/george-standing.png',reviewIcon:'assets/peppa/daddy-pig-standing.png',teachTone:{bg:'#e3f2fd',bd:'#29b6f6',txt:'#01579b'},reviewTone:{bg:'#bbdefb',bd:'#0288d1',txt:'#01579b'}},
      {dir:'where-we-go',theme:'Where We Go',cn:'我们去哪儿',words:'home, school, park, shop, zoo',panel:'linear-gradient(135deg,#e8f5e9,#c8e6c9)',teachIcon:'assets/peppa/peppa_pig_bicycle.png',reviewIcon:'assets/peppa/peppa-pig-happy-standing.png',teachTone:{bg:'#e8f5e9',bd:'#66bb6a',txt:'#2e7d32'},reviewTone:{bg:'#c8e6c9',bd:'#43a047',txt:'#1b5e20'}},
      {dir:'rainbow-colors',theme:'Rainbow Colors',cn:'彩虹颜色',words:'pink, purple, white, black, brown',panel:'linear-gradient(135deg,#f3e5f5,#e1bee7)',teachIcon:'assets/peppa/peppa-fairy-princess.png',reviewIcon:'assets/peppa/george-standing.png',teachTone:{bg:'#f3e5f5',bd:'#ce93d8',txt:'#7b1fa2'},reviewTone:{bg:'#e1bee7',bd:'#ab47bc',txt:'#4a148c'}},
      {dir:'garden-walk',theme:'Garden Walk',cn:'花园散步',words:'tree, flower, grass, rock, water',panel:'linear-gradient(135deg,#e8f5e9,#c8e6c9)',teachIcon:'assets/peppa/peppa-pig-happy-standing.png',reviewIcon:'assets/peppa/george-standing.png',teachTone:{bg:'#e8f5e9',bd:'#8BC34A',txt:'#2e7d32'},reviewTone:{bg:'#c8e6c9',bd:'#66bb6a',txt:'#1b5e20'}},
      {dir:'kitchen-helper',theme:'Kitchen Helper',cn:'厨房小帮手',words:'cup, plate, spoon, bowl, fork',panel:'linear-gradient(135deg,#fff8e1,#ffecb3)',teachIcon:'assets/peppa/mummy-pig-standing-grass.png',reviewIcon:'assets/peppa/peppa-pig-happy-standing.png',teachTone:{bg:'#fff8e1',bd:'#FFB74D',txt:'#e65100'},reviewTone:{bg:'#ffecb3',bd:'#FFA726',txt:'#bf360c'}},
      {dir:'farm-visit',theme:'Farm Visit',cn:'农场之旅',words:'pig, cow, horse, sheep, chicken',panel:'linear-gradient(135deg,#FFE5B4,#90EE90)',teachIcon:'assets/peppa/peppa-pig-happy-standing.png',reviewIcon:'assets/peppa/george-standing.png',teachTone:{bg:'#FFE5B4',bd:'#8BC34A',txt:'#33691e'},reviewTone:{bg:'#90EE90',bd:'#66bb6a',txt:'#2e7d32'}},
      {dir:'daily-actions',theme:'Daily Actions',cn:'每天做的事',words:'eat, drink, sleep, wash, play',panel:'linear-gradient(135deg,#FFE5B4,#FFD1DC)',teachIcon:'assets/peppa/peppa-pig-happy-standing.png',reviewIcon:'assets/peppa/george-standing.png',teachTone:{bg:'#fff8e1',bd:'#ffa726',txt:'#e65100'},reviewTone:{bg:'#ffe0b2',bd:'#ff9800',txt:'#bf360c'}},
      {dir:'my-room',theme:'My Room',cn:'我的房间',words:'bed, door, window, chair, table',panel:'linear-gradient(135deg,#e8eaf6,#c5cae9)',teachIcon:'assets/peppa/peppa-pig-red-polka-dot-dress.png',reviewIcon:'assets/peppa/candy-cat-green-dress.png',teachTone:{bg:'#e8eaf6',bd:'#7e57c2',txt:'#4a148c'},reviewTone:{bg:'#c5cae9',bd:'#5e35b1',txt:'#311b92'}},
      {dir:'snack-time',theme:'Snack Time',cn:'零食时间',words:'rice, cake, juice, candy, cookie',panel:'linear-gradient(135deg,#fff8dc,#ffd89b)',teachIcon:'assets/peppa/peppa-pig-happy-standing.png',reviewIcon:'assets/peppa/george-standing.png',teachTone:{bg:'#fff8dc',bd:'#ffa500',txt:'#e65100'},reviewTone:{bg:'#ffd89b',bd:'#ff8c00',txt:'#bf360c'}}
    ]
  },
  3: {
    title: 'Level 3 · 探索之旅',
    subtitle: '10 个故事 · 50 个单词',
    lessons: [
      {dir:'going-places',theme:'Going Places',cn:'交通工具',words:'bus, bike, boat, train, plane',panel:'linear-gradient(135deg,#e3f2fd,#bbdefb)',teachIcon:'assets/peppa/peppa_pig_bicycle.png',reviewIcon:'assets/peppa/george-standing.png',teachTone:{bg:'#e3f2fd',bd:'#42a5f5',txt:'#01579b'},reviewTone:{bg:'#bbdefb',bd:'#1976d2',txt:'#0d47a1'}},
      {dir:'opposites-game',theme:'Opposites Game',cn:'相反词游戏',words:'hot, cold, up, down, fast',panel:'linear-gradient(135deg,#fff3e0,#ffe0b2)',teachIcon:'assets/peppa/peppa-pig-happy-standing.png',reviewIcon:'assets/peppa/george-standing.png',teachTone:{bg:'#fff3e0',bd:'#ff9800',txt:'#e65100'},reviewTone:{bg:'#ffe0b2',bd:'#ff6d00',txt:'#bf360c'}},
      {dir:'shapes-around-us',theme:'Shapes Around Us',cn:'形状世界',words:'circle, square, triangle, star, heart',panel:'linear-gradient(135deg,#e1bee7,#ce93d8)',teachIcon:'assets/peppa/peppa-pig-happy-standing.png',reviewIcon:'assets/peppa/george-standing.png',teachTone:{bg:'#f3e5f5',bd:'#ab47bc',txt:'#7b1fa2'},reviewTone:{bg:'#e1bee7',bd:'#9c27b0',txt:'#6a1b9a'}},
      {dir:'music-time',theme:'Music Time',cn:'音乐时间',words:'sing, dance, clap, drum, piano',panel:'linear-gradient(135deg,#FFE5B4,#FFD1DC)',teachIcon:'assets/peppa/peppa-pig-happy-standing.png',reviewIcon:'assets/peppa/george-standing.png',teachTone:{bg:'#fff8e1',bd:'#ba68c8',txt:'#7b1fa2'},reviewTone:{bg:'#ffe0b2',bd:'#9c27b0',txt:'#6a1b9a'}},
      {dir:'beach-day',theme:'Beach Day',cn:'海滩一天',words:'sand, shell, wave, crab, boat',panel:'linear-gradient(135deg,#87CEEB,#F4E4C1)',teachIcon:'assets/peppa/peppa-pig-happy-standing.png',reviewIcon:'assets/peppa/george-standing.png',teachTone:{bg:'#e3f2fd',bd:'#4fc3f7',txt:'#01579b'},reviewTone:{bg:'#b3e5fc',bd:'#0077be',txt:'#006064'}},
      {dir:'bedtime-story',theme:'Bedtime Story',cn:'睡前故事',words:'book, bed, moon, star, dream',panel:'linear-gradient(180deg,#1a1a3e,#2d2d5f)',teachIcon:'assets/peppa/peppa-pig-happy-standing.png',reviewIcon:'assets/peppa/george-standing.png',teachTone:{bg:'#e8eaf6',bd:'#5c6bc0',txt:'#1a237e'},reviewTone:{bg:'#c5cae9',bd:'#3f51b5',txt:'#0d47a1'}},
      {dir:'birthday-party',theme:'Birthday Party',cn:'生日派对',words:'cake, gift, balloon, candle, friend',panel:'linear-gradient(135deg,#FFD700,#FFA07A,#FF69B4)',teachIcon:'assets/peppa/peppa-pig-red-polka-dot-dress.png',reviewIcon:'assets/peppa/peppa-family-group-outdoors.png',teachTone:{bg:'#fff8e1',bd:'#ffd700',txt:'#e65100'},reviewTone:{bg:'#ffe0b2',bd:'#ff69b4',txt:'#bf360c'}},
      {dir:'doctor-visit',theme:'Doctor Visit',cn:'看医生',words:'doctor, nurse, sick, medicine, better',panel:'linear-gradient(135deg,#E8F5E9,#B2DFDB,#80DEEA)',teachIcon:'assets/peppa/peppa-pig-happy-standing.png',reviewIcon:'assets/peppa/candy-cat-green-dress.png',teachTone:{bg:'#e8f5e9',bd:'#66bb6a',txt:'#2e7d32'},reviewTone:{bg:'#b2dfdb',bd:'#4db6ac',txt:'#00695c'}},
      {dir:'shopping-trip',theme:'Shopping Trip',cn:'购物之旅',words:'shop, buy, money, bag, toy',panel:'linear-gradient(135deg,#FFE5B4,#FFD700,#FFA07A)',teachIcon:'assets/peppa/mummy-pig-standing-grass.png',reviewIcon:'assets/peppa/peppa-pig-happy-standing.png',teachTone:{bg:'#fff8e1',bd:'#ffd700',txt:'#e65100'},reviewTone:{bg:'#ffe0b2',bd:'#ffa500',txt:'#bf360c'}},
      {dir:'seasons-change',theme:'Seasons Change',cn:'四季变化',words:'spring, summer, fall, winter, season',panel:'linear-gradient(135deg,#e8f5e9,#fff9c4)',teachIcon:'assets/peppa/peppa-pig-happy-standing.png',reviewIcon:'assets/peppa/george-standing.png',teachTone:{bg:'#e8f5e9',bd:'#8BC34A',txt:'#2e7d32'},reviewTone:{bg:'#fff9c4',bd:'#ffa726',txt:'#e65100'}}
    ]
  },
  4: {
    title: 'Level 4 · 成长故事',
    subtitle: '5 个故事 · 25 个单词',
    lessons: [
      {dir:'helping-at-home',theme:'Helping at Home',cn:'家务小帮手',words:'clean, wash, help, tidy, sweep',panel:'linear-gradient(135deg,#FFF9C4,#FFE082,#FFD54F)',teachIcon:'assets/peppa/peppa-pig-happy-standing.png',reviewIcon:'assets/peppa/mummy-pig-standing-grass.png',teachTone:{bg:'#fff9c4',bd:'#ffd54f',txt:'#f57f17'},reviewTone:{bg:'#ffe082',bd:'#ffb300',txt:'#e65100'}},
      {dir:'school-day',theme:'School Day',cn:'上学的一天',words:'teacher, friend, learn, draw, write',panel:'linear-gradient(135deg,#FFE5B4,#FFDAB9,#FFE4B5)',teachIcon:'assets/peppa/peppa-pig-happy-standing.png',reviewIcon:'assets/peppa/candy-cat-green-dress.png',teachTone:{bg:'#ffe5b4',bd:'#ffd93d',txt:'#e65100'},reviewTone:{bg:'#ffdab9',bd:'#ffc93d',txt:'#bf360c'}},
      {dir:'pet-care',theme:'Pet Care',cn:'照顾宠物',words:'pet, feed, walk, play, love',panel:'linear-gradient(135deg,#e8f5e9,#c8e6c9,#a5d6a7)',teachIcon:'assets/peppa/peppa-pig-happy-standing.png',reviewIcon:'assets/peppa/george-standing.png',teachTone:{bg:'#e8f5e9',bd:'#66bb6a',txt:'#2e7d32'},reviewTone:{bg:'#c8e6c9',bd:'#81c784',txt:'#1b5e20'}},
      {dir:'cooking-together',theme:'Cooking Together',cn:'一起做饭',words:'cook, mix, pour, taste, yummy',panel:'linear-gradient(135deg,#ffe5d0,#ffd4a3)',teachIcon:'assets/peppa/mummy-pig-standing-grass.png',reviewIcon:'assets/peppa/peppa-pig-happy-standing.png',teachTone:{bg:'#ffe5d0',bd:'#e67e22',txt:'#bf360c'},reviewTone:{bg:'#ffd4a3',bd:'#ff9a9e',txt:'#c62828'}},
      {dir:'sports-day',theme:'Sports Day',cn:'运动会',words:'kick, throw, catch, race, win',panel:'linear-gradient(135deg,#e8f5e9,#c8e6c9)',teachIcon:'assets/peppa/peppa-pig-happy-standing.png',reviewIcon:'assets/peppa/george-standing.png',teachTone:{bg:'#e8f5e9',bd:'#66bb6a',txt:'#2e7d32'},reviewTone:{bg:'#c8e6c9',bd:'#81c784',txt:'#1b5e20'}}
    ]
  }
};

const template = (level, data) => `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>${data.title}</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{
  --ink:#2c3e50;
  --muted:#667085;
}
body{
  font-family:'Segoe UI',system-ui,sans-serif;
  min-height:100vh;
  background:
    radial-gradient(circle at 12% 10%,#ffd9e7 0,transparent 35%),
    radial-gradient(circle at 88% 12%,#c9f0ff 0,transparent 32%),
    linear-gradient(160deg,#fff4f8,#f8fbff 52%,#f5fff4);
  padding:20px 16px 28px;
  color:var(--ink);
}
.container{max-width:760px;margin:0 auto}
.back{
  display:inline-flex;align-items:center;gap:6px;
  text-decoration:none;color:var(--ink);
  font-size:14px;font-weight:700;
  margin-bottom:12px;
  padding:8px 12px;
  background:rgba(255,255,255,.7);
  border-radius:12px;
  transition:background .2s;
}
.back:hover{background:rgba(255,255,255,.9)}
.hero{
  text-align:center;
  background:rgba(255,255,255,.72);
  border:2px solid rgba(255,255,255,.9);
  border-radius:22px;
  padding:14px 14px 16px;
  box-shadow:0 10px 26px rgba(32,56,90,.08);
}
h1{font-size:28px;line-height:1.1;color:#394867}
.sub{margin-top:4px;font-size:14px;color:#6b7280}
.lesson-group{margin-top:14px}
.lesson-head{
  display:flex;align-items:center;justify-content:space-between;
  border-radius:14px;
  padding:10px 12px;
  font-weight:800;
  font-size:17px;
  color:#263238;
}
.lesson-head small{font-size:12px;font-weight:700;opacity:.78}
.cards{margin-top:8px;display:grid;gap:8px}
.card{
  text-decoration:none;
  color:var(--ink);
  background:rgba(255,255,255,.9);
  border:2px solid rgba(255,255,255,.95);
  border-radius:16px;
  padding:10px 12px;
  display:flex;
  align-items:center;
  gap:10px;
  box-shadow:0 4px 16px rgba(30,58,95,.08);
  transition:transform .18s ease,box-shadow .18s ease;
}
.card:active{transform:scale(.98)}
.icon-wrap{
  width:52px;height:52px;border-radius:14px;
  display:flex;align-items:center;justify-content:center;
}
.icon-wrap img{width:42px;height:42px;object-fit:contain}
.info{flex:1;min-width:0}
.row{display:flex;align-items:center;gap:8px}
.title{font-size:17px;font-weight:900;line-height:1.1}
.badge{
  font-size:11px;font-weight:800;padding:3px 7px;border-radius:999px;
  border:2px solid transparent;
}
.desc{margin-top:4px;font-size:12px;color:var(--muted);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.theme-title{font-size:15px;line-height:1.2}
.theme-cn{font-size:13px;opacity:.85;margin-top:2px}
@media(min-width:700px){
  .cards{grid-template-columns:1fr 1fr}
  .card{padding:12px}
}
</style>
</head>
<body>
<div class="container">
  <a class="back" href="index.html">← 返回主页</a>
  <div class="hero">
    <h1>${data.title}</h1>
    <div class="sub">${data.subtitle}</div>
  </div>
  <div id="lessons"></div>
</div>
<script>
var lessons=${JSON.stringify(data.lessons)};

function cardHtml(kind,l){
  var isTeach=kind==='teach';
  var title=isTeach?'老师课件':'练习课件';
  var icon=isTeach?l.teachIcon:l.reviewIcon;
  var tone=isTeach?l.teachTone:l.reviewTone;
  var tip=isTeach?'大屏跟读':'互动游戏';
  return '<a class="card" href="lessons/level-${level}/'+l.dir+'/'+kind+'.html">'+
    '<div class="icon-wrap" style="background:'+tone.bg+';border:2px solid '+tone.bd+'">'+
      '<img src="'+icon+'" alt="'+title+'">'+
    '</div>'+
    '<div class="info">'+
      '<div class="row">'+
        '<div class="title">'+title+'</div>'+
        '<div class="badge" style="background:'+tone.bg+';border-color:'+tone.bd+';color:'+tone.txt+'">'+tip+'</div>'+
      '</div>'+
      '<div class="desc">'+l.words+'</div>'+
    '</div>'+
  '</a>';
}

var wrap=document.getElementById('lessons');
lessons.forEach(function(l){
  var g=document.createElement('section');
  g.className='lesson-group';
  g.innerHTML=
    '<div class="lesson-head" style="background:'+l.panel+'">'+
      '<div>'+
        '<div class="theme-title">'+l.theme+'</div>'+
        '<div class="theme-cn">'+l.cn+'</div>'+
      '</div>'+
      '<small>5 words</small>'+
    '</div>'+
    '<div class="cards">'+cardHtml('teach',l)+cardHtml('review',l)+'</div>';
  wrap.appendChild(g);
});
</script>
</body>
</html>`;

[1,2,3,4].forEach(level => {
  fs.writeFileSync(`level-${level}.html`, template(level, levels[level]));
  console.log(`Fixed level-${level}.html`);
});
