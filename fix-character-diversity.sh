#!/bin/bash
# 批量修复课件角色多样性问题

# 可用角色池（按使用频率排序，避免过度使用某个角色）
CHARS=(
  "peppa-pig-red-polka-dot-dress.png"
  "george-superhero-costume.png"
  "candy-cat-green-dress.png"
  "daddy-pig-walking.png"
  "mummy-pig-standing-grass.png"
  "emily-elephant-standing.png"
  "george_pig_dinosaur.png"
  "peppa-fairy-princess.png"
  "peppa-and-george-ooo.png"
  "george-playing-ball.png"
  "daddy-pig-standing.png"
  "george-standing.png"
  "peppa-pig-happy-standing.png"
  "peppa-family-group-outdoors.png"
)

# 检查并修复单个文件
fix_file() {
  local file=$1
  local lesson=$2
  
  # 统计每个角色使用次数
  local most_used=$(grep -o 'assets/peppa/[^"]*' "$file" | sort | uniq -c | sort -rn | head -1)
  local count=$(echo "$most_used" | awk '{print $1}')
  
  if [ "$count" -ge 5 ]; then
    echo "  ⚠️  $lesson: 最高使用 $count 次 - 需要修复"
    # 这里可以添加自动替换逻辑
  fi
}

# 扫描所有课件
echo "🔍 扫描 Phonics 2-5 课件..."
for level in phonics-{2,3,4,5}; do
  if [ -d "lessons/$level" ]; then
    echo ""
    echo "=== $level ==="
    for dir in lessons/$level/*/; do
      if [ -f "$dir/teach.html" ]; then
        lesson=$(basename "$dir")
        fix_file "$dir/teach.html" "$lesson"
      fi
    done
  fi
done

echo ""
echo "✅ 扫描完成"
