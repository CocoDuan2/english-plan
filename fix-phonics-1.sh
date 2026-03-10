#!/bin/bash
# 批量修复 Phonics 1 (P7-P26) 课件问题
# 1. 角色多样化
# 2. 修复游戏启动 bug
# 3. 添加音频预加载

LETTERS=(g h i j k l m n o p q r s t u v w x y z)
ROLES=(
  "george-standing"
  "candy-cat-green-dress"
  "emily-elephant-standing"
  "mummy-pig-standing-grass"
  "daddy-pig-standing"
  "daddy-pig-walking"
  "peppa-pig-red-polka-dot-dress"
  "peppa-fairy-princess"
  "george-superhero-costume"
  "peppa-and-george-ooo"
  "george_pig_dinosaur"
  "george-playing-ball"
)

for i in "${!LETTERS[@]}"; do
  letter="${LETTERS[$i]}"
  dir="lessons/phonics-1/letter-$letter"
  
  if [ ! -f "$dir/teach.html" ]; then
    echo "跳过 $letter (文件不存在)"
    continue
  fi
  
  echo "处理 P$((i+7)) Letter ${letter^^}..."
  
  # 1. 修复游戏启动 bug (currentSlide===9 -> goTo触发)
  sed -i '' 's/if(currentSlide===9)startListenGame();//g' "$dir/teach.html"
  sed -i '' 's/function goTo(i){$/function goTo(i){\
  if(i<0||i>=ts)return;\
  document.querySelectorAll(".slide").forEach((s,idx)=>s.classList.toggle("active",idx===i));\
  ci=i;\
  document.getElementById("curr").textContent=i+1;\
  document.getElementById("prevBtn").disabled=i===0;\
  document.getElementById("nextBtn").disabled=i===ts-1;\
  if(i===9)setTimeout(startListenGame,300);\
}/g' "$dir/teach.html"
  
  # 2. 添加音频预加载
  if ! grep -q "audioCache" "$dir/teach.html"; then
    sed -i '' 's/let ci=0,ts=13;/let ci=0,ts=13;\
let audioCache={};\
\
function preloadAudio(){\
  const words=["word1","word2","word3","word4"];\
  words.forEach(w=>{\
    const u=`https:\/\/dict.youdao.com\/dictvoice?audio=${encodeURIComponent(w)}\&type=2`;\
    const a=new Audio(u);\
    a.preload="auto";\
    audioCache[w]=a;\
  });\
}/g' "$dir/teach.html"
    
    sed -i '' 's/goTo(0);$/preloadAudio();\
goTo(0);/g' "$dir/teach.html"
  fi
  
  echo "✓ P$((i+7)) 修复完成"
done

echo "全部完成！"
