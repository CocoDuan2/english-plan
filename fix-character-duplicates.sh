#!/bin/bash
# 修复 Phonics 1 (P1-P26) 同课内角色重复问题

# 可用角色池（按使用频率排序，优先使用低频角色）
CHARS=(
  "george-superhero-costume"
  "george-playing-ball"
  "george_pig_dinosaur"
  "peppa-and-george-ooo"
)

# P1: 替换第269行（S4）、413行（S10）的重复角色
sed -i.bak '269s/peppa-pig-happy-standing/george-superhero-costume/' english-plan/lessons/phonics-1/letter-a/teach.html
sed -i '413s/peppa-pig-red-polka-dot-dress/george-playing-ball/' english-plan/lessons/phonics-1/letter-a/teach.html

echo "✅ P1 修复完成"
