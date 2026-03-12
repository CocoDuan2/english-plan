#!/usr/bin/env python3
"""检查游戏多样性"""
import re
from pathlib import Path
from collections import Counter

def extract_game_type(filepath):
    """提取课件的游戏类型"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # teach.html 的游戏在 S12 左右
    game_match = re.search(r'<!-- S1[0-2].*?Game.*?-->(.*?)<!-- S1[3-4]', content, re.DOTALL)
    if not game_match:
        return None
    
    game_content = game_match.group(1)
    
    # 识别游戏类型
    if 'onclick' in game_content and 'apple' in game_content.lower():
        return 'find-apples'
    elif 'drag' in game_content.lower():
        return 'drag-drop'
    elif 'match' in game_content.lower():
        return 'matching'
    elif 'onclick' in game_content and ('fish' in game_content.lower() or 'star' in game_content.lower()):
        return 'click-collect'
    elif 'balloon' in game_content.lower():
        return 'balloon-pop'
    elif 'onclick' in game_content:
        return 'click-game'
    else:
        return 'other'

def main():
    games = []
    
    for phonics_level in ['phonics-1', 'phonics-2', 'phonics-3', 'phonics-4', 'phonics-5']:
        level_dir = Path('lessons') / phonics_level
        if not level_dir.exists():
            continue
        
        for lesson_dir in sorted(level_dir.iterdir()):
            if not lesson_dir.is_dir():
                continue
            
            teach_file = lesson_dir / 'teach.html'
            if teach_file.exists():
                game_type = extract_game_type(teach_file)
                games.append({
                    'level': phonics_level,
                    'lesson': lesson_dir.name,
                    'game': game_type
                })
    
    print("=" * 70)
    print("🎮 游戏多样性检查")
    print("=" * 70)
    
    # 统计游戏类型
    game_types = Counter([g['game'] for g in games])
    print("\n游戏类型分布:")
    for game_type, count in game_types.most_common():
        print(f"  {game_type}: {count}次")
    
    # 检查连续重复
    print("\n连续3课使用相同游戏:")
    consecutive = []
    for i in range(len(games) - 2):
        if games[i]['game'] == games[i+1]['game'] == games[i+2]['game']:
            consecutive.append(f"  {games[i]['level']}: {games[i]['lesson']}, {games[i+1]['lesson']}, {games[i+2]['lesson']} ({games[i]['game']})")
    
    if consecutive:
        for c in consecutive[:10]:
            print(c)
        if len(consecutive) > 10:
            print(f"  ... 还有 {len(consecutive) - 10} 个")
    else:
        print("  ✅ 无连续3课使用相同游戏")

if __name__ == '__main__':
    main()
