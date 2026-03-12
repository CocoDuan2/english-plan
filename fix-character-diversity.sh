#!/bin/bash
# 修复 Phonics 1 角色重复问题

cd "$(dirname "$0")/lessons/phonics-1"

# P7 letter-g: 第1个candy-cat改为peppa-happy
sed -i '' 's|candy-cat-green-dress.png" alt="Candy">|peppa-pig-happy-standing.png" alt="Peppa">|' letter-g/teach.html

# P11 letter-l: 第1个george-standing改为peppa-fairy
sed -i '' '0,/george-standing.png" alt="George">/s//peppa-fairy-princess.png" alt="Peppa">/' letter-l/teach.html

# P17 letter-r: 第2个emily改为peppa-red-polka
sed -i '' '0,/emily-elephant-standing.png" alt="Emily">/!s/emily-elephant-standing.png" alt="Emily">/peppa-pig-red-polka-dot-dress.png" alt="Peppa">/' letter-r/teach.html

# P18 letter-s: 第2个george-superhero改为peppa-happy
sed -i '' '0,/george-superhero-costume.png" alt="George">/!s/george-superhero-costume.png" alt="George">/peppa-pig-happy-standing.png" alt="Peppa">/' letter-s/teach.html

# P19 letter-t: 第2个daddy-walking改为emily
sed -i '' '0,/daddy-pig-walking.png" alt="Daddy">/!s/daddy-pig-walking.png" alt="Daddy">/emily-elephant-standing.png" alt="Emily">/' letter-t/teach.html

# P20 letter-u: 第2个mummy改为peppa-fairy
sed -i '' '0,/mummy-pig-standing-grass.png" alt="Mummy">/!s/mummy-pig-standing-grass.png" alt="Mummy">/peppa-fairy-princess.png" alt="Peppa">/' letter-u/teach.html

# P21 letter-v: 第2个george-playing-ball改为candy-cat
sed -i '' '0,/george-playing-ball.png" alt="George">/!s/george-playing-ball.png" alt="George">/candy-cat-green-dress.png" alt="Candy">/' letter-v/teach.html

# P22 letter-w: 第2个george-standing改为peppa-happy
sed -i '' '0,/george-standing.png" alt="George">/!s/george-standing.png" alt="George">/peppa-pig-happy-standing.png" alt="Peppa">/' letter-w/teach.html

# P23 letter-x: 第2个daddy-standing改为emily
sed -i '' '0,/daddy-pig-standing.png" alt="Daddy">/!s/daddy-pig-standing.png" alt="Daddy">/emily-elephant-standing.png" alt="Emily">/' letter-x/teach.html

# P24 letter-y: 第2个candy-cat改为mummy
sed -i '' '0,/candy-cat-green-dress.png" alt="Candy">/!s/candy-cat-green-dress.png" alt="Candy">/mummy-pig-standing-grass.png" alt="Mummy">/' letter-y/teach.html

# P25 letter-z: 第2个peppa-and-george改为peppa-family
sed -i '' '0,/peppa-and-george-ooo.png" alt="Peppa & George">/!s/peppa-and-george-ooo.png" alt="Peppa & George">/peppa-family-group-outdoors.png" alt="Peppa Family">/' letter-z/teach.html

echo "✅ 同课内重复修复完成"

# 修复连续课程重复
# P4 letter-d: george_pig_dinosaur改为mummy-pig (避免P3-P4重复)
sed -i '' '0,/george_pig_dinosaur.png" alt="George">/s//mummy-pig-standing-grass.png" alt="Mummy">/' letter-d/teach.html

# P5 letter-e: daddy-pig-standing改为george-superhero (避免P4-P5重复)
sed -i '' 's|daddy-pig-standing.png" alt="Daddy">|george-superhero-costume.png" alt="George">|' letter-e/teach.html

# P6 letter-f: daddy-pig-walking改为peppa-fairy (避免P5-P6重复)
sed -i '' '0,/daddy-pig-walking.png" alt="Daddy">/s//peppa-fairy-princess.png" alt="Peppa">/' letter-f/teach.html

echo "✅ 连续课程重复修复完成"
