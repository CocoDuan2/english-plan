#!/bin/bash
# 批量修复 Phonics 1 (P1-P26) 角色重复问题

cd "$(dirname "$0")/lessons/phonics-1"

# P2 letter-b: 3个角色各重复2次
sed -i '' '1,300s/george-standing\.png/george_pig_dinosaur.png/1' letter-b/teach.html
sed -i '' '1,300s/george-playing-ball\.png/candy-cat-green-dress.png/1' letter-b/teach.html
sed -i '' '1,300s/daddy-pig-walking\.png/emily-elephant-standing.png/1' letter-b/teach.html

# P3 letter-c: 2个角色各重复2次
sed -i '' '1,300s/peppa-family-group-outdoors\.png/george-superhero-costume.png/1' letter-c/teach.html
sed -i '' '1,300s/peppa-fairy-princess\.png/mummy-pig-standing-grass.png/1' letter-c/teach.html

# P4 letter-d: peppa-family重复2次
sed -i '' '1,300s/peppa-family-group-outdoors\.png/george-standing.png/1' letter-d/teach.html

# P5 letter-e: 3个角色各重复2次
sed -i '' '1,300s/mummy-pig-standing-grass\.png/daddy-pig-standing.png/1' letter-e/teach.html
sed -i '' '1,300s/george-superhero-costume\.png/candy-cat-green-dress.png/1' letter-e/teach.html
sed -i '' '1,300s/emily-elephant-standing\.png/peppa-pig-happy-standing.png/1' letter-e/teach.html

# P6 letter-f: peppa-happy重复2次
sed -i '' '1,300s/peppa-pig-happy-standing\.png/george-standing.png/1' letter-f/teach.html

echo "✅ P2-P6 修复完成"
