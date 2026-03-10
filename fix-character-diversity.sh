#!/bin/bash

# 批量优化 Phonics 1 课件的角色多样性
# 策略：在每个课件中随机分配不同的角色图片

CHARS=(
  "peppa-pig-happy-standing"
  "george-standing"
  "daddy-pig-standing"
  "daddy-pig-walking"
  "mummy-pig-standing-grass"
  "candy-cat-green-dress"
  "emily-elephant-standing"
  "peppa-pig-red-polka-dot-dress"
  "peppa-fairy-princess"
  "george-superhero-costume"
  "george_pig_dinosaur"
  "george-playing-ball"
)

# 为每个字母课件分配不同的角色组合
declare -A LESSON_CHARS

# P8-P26 (跳过已优化的 P7)
LESSON_CHARS["letter-h"]="george-standing,mummy-pig-standing-grass,daddy-pig-walking,candy-cat-green-dress,emily-elephant-standing"
LESSON_CHARS["letter-i"]="peppa-fairy-princess,george_pig_dinosaur,daddy-pig-standing,emily-elephant-standing,candy-cat-green-dress"
LESSON_CHARS["letter-j"]="george-playing-ball,peppa-pig-red-polka-dot-dress,mummy-pig-standing-grass,daddy-pig-walking,george-standing"
LESSON_CHARS["letter-k"]="candy-cat-green-dress,george-superhero-costume,peppa-pig-happy-standing,daddy-pig-standing,emily-elephant-standing"
LESSON_CHARS["letter-l"]="emily-elephant-standing,peppa-fairy-princess,george_pig_dinosaur,mummy-pig-standing-grass,daddy-pig-walking"
LESSON_CHARS["letter-m"]="daddy-pig-standing,george-playing-ball,peppa-pig-red-polka-dot-dress,candy-cat-green-dress,george-standing"
LESSON_CHARS["letter-n"]="mummy-pig-standing-grass,peppa-pig-happy-standing,george-superhero-costume,emily-elephant-standing,daddy-pig-walking"
LESSON_CHARS["letter-o"]="george_pig_dinosaur,candy-cat-green-dress,peppa-fairy-princess,daddy-pig-standing,george-standing"
LESSON_CHARS["letter-p"]="peppa-pig-red-polka-dot-dress,emily-elephant-standing,george-playing-ball,mummy-pig-standing-grass,daddy-pig-walking"
# P17 letter-q 已经使用 peppa-fairy-princess，跳过
LESSON_CHARS["letter-r"]="george-standing,daddy-pig-standing,peppa-pig-happy-standing,candy-cat-green-dress,emily-elephant-standing"
LESSON_CHARS["letter-s"]="daddy-pig-walking,george-superhero-costume,mummy-pig-standing-grass,peppa-fairy-princess,george_pig_dinosaur"
LESSON_CHARS["letter-t"]="candy-cat-green-dress,peppa-pig-red-polka-dot-dress,george-playing-ball,daddy-pig-standing,emily-elephant-standing"
LESSON_CHARS["letter-u"]="emily-elephant-standing,george-standing,peppa-pig-happy-standing,mummy-pig-standing-grass,daddy-pig-walking"
LESSON_CHARS["letter-v"]="george_pig_dinosaur,daddy-pig-standing,candy-cat-green-dress,peppa-fairy-princess,george-superhero-costume"
LESSON_CHARS["letter-w"]="peppa-pig-red-polka-dot-dress,mummy-pig-standing-grass,emily-elephant-standing,george-playing-ball,daddy-pig-walking"
LESSON_CHARS["letter-x"]="daddy-pig-standing,peppa-pig-happy-standing,george-standing,candy-cat-green-dress,emily-elephant-standing"
LESSON_CHARS["letter-y"]="george-superhero-costume,peppa-fairy-princess,daddy-pig-walking,mummy-pig-standing-grass,george_pig_dinosaur"
LESSON_CHARS["letter-z"]="candy-cat-green-dress,emily-elephant-standing,peppa-pig-red-polka-dot-dress,george-playing-ball,daddy-pig-standing"

cd lessons/phonics-1

for lesson in "${!LESSON_CHARS[@]}"; do
  echo "Processing $lesson..."
  
  IFS=',' read -ra CHARS_ARRAY <<< "${LESSON_CHARS[$lesson]}"
  
  # 替换 teach.html 中的角色（保留首页和Bye页的 family-group）
  # S2 Hello
  sed -i '' "s|george-standing.png\" alt=\"George\"|${CHARS_ARRAY[0]}.png\" alt=\"Character\"|g" "$lesson/teach.html"
  
  # S3 Letter Show
  sed -i '' "s|candy-cat-green-dress.png\" alt=\"Candy\"|${CHARS_ARRAY[1]}.png\" alt=\"Character\"|g" "$lesson/teach.html"
  
  # S4 Trace
  sed -i '' "s|emily-elephant-standing.png\" alt=\"Emily\"|${CHARS_ARRAY[2]}.png\" alt=\"Character\"|g" "$lesson/teach.html"
  
  # S5-S8 Words (4个单词页)
  # 这里需要更精确的替换，避免误替换
  
  echo "  ✓ $lesson updated"
done

echo "Done!"
