#!/usr/bin/env python3
"""
Patch day3-body.html to add teacher-driven mode with replay buttons,
expandable teacher guides, and drill mode.
"""

import re

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def patch_css(content):
    """Add new CSS rules after .next-btn.show"""
    # Find the .next-btn.show rule
    pattern = r'(\.next-btn\.show\{[^}]+\})'

    new_css = '''

/* Button group for replay + next */
.btn-group{display:flex;gap:10px;margin-top:12px;justify-content:center;flex-wrap:wrap}
.replay-btn{background:#fff;color:#6c5ce7;border:2px solid #6c5ce7;border-radius:30px;padding:12px 36px;
  font-size:18px;font-weight:700;cursor:pointer;transition:transform .2s,opacity .3s;display:none}
.replay-btn.show{display:inline-block}
.replay-btn:active{transform:scale(.93)}
.drill-btn{background:linear-gradient(135deg,#ff6b6b,#ee5a6f);color:#fff;border:none;border-radius:30px;
  padding:12px 36px;font-size:18px;font-weight:700;cursor:pointer;transition:transform .2s;display:none}
.drill-btn.show{display:inline-block}
.drill-btn:active{transform:scale(.93)}

/* Expandable teacher guide */
.teacher-guide-wrap{background:rgba(255,255,255,.85);border-radius:10px;padding:8px 14px;
  margin-bottom:10px;width:100%}
.teacher-guide-toggle{cursor:pointer;user-select:none;font-size:13px;color:#666;
  display:flex;align-items:center;gap:6px}
.teacher-guide-toggle .arrow{transition:transform .3s;display:inline-block}
.teacher-guide-toggle .arrow.open{transform:rotate(90deg)}
.teacher-guide-expand{display:none;margin-top:8px;padding-left:20px;font-size:12px;color:#555}
.teacher-guide-expand.open{display:block}
.teacher-guide-expand ul{margin:4px 0;padding-left:16px}
.teacher-guide-expand li{margin:3px 0}

/* Drill overlay */
.drill-overlay{position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,.85);
  z-index:200;display:flex;align-items:center;justify-content:center}
.drill-card{background:#fff;border-radius:20px;padding:30px;width:90%;max-width:350px;
  display:flex;flex-direction:column;align-items:center;gap:16px;position:relative}
.drill-emoji{font-size:100px;line-height:1}
.drill-word{font-size:28px;font-weight:700;color:#333}
.drill-nav{display:flex;gap:20px;margin-top:10px}
.drill-nav button{background:#6c5ce7;color:#fff;border:none;border-radius:50%;width:50px;height:50px;
  font-size:24px;cursor:pointer;transition:transform .2s}
.drill-nav button:active{transform:scale(.9)}
.drill-close{position:absolute;top:10px;right:10px;background:none;border:none;font-size:28px;
  cursor:pointer;color:#999;transition:color .2s}
.drill-close:hover{color:#333}'''

    return re.sub(pattern, r'\1' + new_css, content)

def patch_buttons(content):
    """Replace single next buttons with btn-group containing replay + next"""

    # Module 1: Review
    content = re.sub(
        r'<button class="next-btn" id="nextBtn1" onclick="goModule\(2\)">Learn Body Parts! ➡️</button>',
        '''<div class="btn-group" id="btnGroup1">
    <button class="replay-btn" onclick="startReview()">🔄 Replay</button>
    <button class="next-btn" onclick="goModule(2)">Learn Body Parts! ➡️</button>
  </div>''',
        content
    )

    # Module 2: New Words (with drill button)
    content = re.sub(
        r'<button class="next-btn" id="nextBtn2" onclick="goModule\(3\)">Next Game! ➡️</button>',
        '''<div class="btn-group" id="btnGroup2">
    <button class="replay-btn" onclick="resetModule2()">🔄 Replay</button>
    <button class="drill-btn" onclick="enterDrill()">⚡ Drill</button>
    <button class="next-btn" onclick="goModule(3)">Next Game! ➡️</button>
  </div>''',
        content
    )

    return content

def patch_teacher_guides(content):
    """Replace teacher-guide divs with expandable versions"""

    guides = [
        {
            'old': r'<div class="teacher-guide">🎤 <b>老师说：</b>"Let\'s remember what we learned! 还记得这些吗？Tap the right one!"</div>',
            'new': '''<div class="teacher-guide-wrap">
    <div class="teacher-guide-toggle" onclick="toggleGuide(this)">
      <span class="arrow">▶</span>
      <span>🎤 <b>老师说：</b>"Let's remember what we learned! 还记得这些吗？Tap the right one!"</span>
    </div>
    <div class="teacher-guide-expand">
      <ul>
        <li>Point and ask: "What color is this?" "What animal?"</li>
        <li>Encourage: "Can you find the RED one?"</li>
      </ul>
    </div>
  </div>'''
        },
        {
            'old': r'<div class="teacher-guide">🎤 <b>老师说：</b>"Let\'s learn body parts! Tap each gray picture to see what it is! 点击灰色图片看看是什么！"</div>',
            'new': '''<div class="teacher-guide-wrap">
    <div class="teacher-guide-toggle" onclick="toggleGuide(this)">
      <span class="arrow">▶</span>
      <span>🎤 <b>老师说：</b>"Let's learn body parts! Tap each gray picture to see what it is! 点击灰色图片看看是什么！"</span>
    </div>
    <div class="teacher-guide-expand">
      <ul>
        <li>Touch your own head/eyes/ears and say the word</li>
        <li>Ask: "Where is YOUR nose?" (point to child)</li>
        <li>Use Drill button for rapid review after learning</li>
      </ul>
    </div>
  </div>'''
        },
        {
            'old': r'<div class="teacher-guide" id="balloonGuide">🎤 <b>老师说：</b>"Pop the balloon! 点击有正确图片的气球！"</div>',
            'new': '''<div class="teacher-guide-wrap">
    <div class="teacher-guide-toggle" onclick="toggleGuide(this)">
      <span class="arrow">▶</span>
      <span id="balloonGuide">🎤 <b>老师说：</b>"Pop the balloon! 点击有正确图片的气球！"</span>
    </div>
    <div class="teacher-guide-expand">
      <ul>
        <li>Say the target word out loud together</li>
        <li>Cheer when they pop the correct balloon!</li>
      </ul>
    </div>
  </div>'''
        },
        {
            'old': r'<div class="teacher-guide" id="listenGuide">🎤 <b>老师说：</b>"Where is the HEAD\? 找到头！Tap it!"</div>',
            'new': '''<div class="teacher-guide-wrap">
    <div class="teacher-guide-toggle" onclick="toggleGuide(this)">
      <span class="arrow">▶</span>
      <span id="listenGuide">🎤 <b>老师说：</b>"Where is the HEAD? 找到头！Tap it!"</span>
    </div>
    <div class="teacher-guide-expand">
      <ul>
        <li>Read the prompt together: "Find: HEAD"</li>
        <li>Point to your own head as a hint</li>
      </ul>
    </div>
  </div>'''
        },
        {
            'old': r'<div class="teacher-guide" id="connectGuide">🎤 <b>老师说：</b>"Match the word to the picture! Tap a word, then tap its picture! 把单词和图片配对！"</div>',
            'new': '''<div class="teacher-guide-wrap">
    <div class="teacher-guide-toggle" onclick="toggleGuide(this)">
      <span class="arrow">▶</span>
      <span id="connectGuide">🎤 <b>老师说：</b>"Match the word to the picture! Tap a word, then tap its picture! 把单词和图片配对！"</span>
    </div>
    <div class="teacher-guide-expand">
      <ul>
        <li>Read each word together first</li>
        <li>Help: "Which picture shows EYES?"</li>
      </ul>
    </div>
  </div>'''
        }
    ]

    for guide in guides:
        content = re.sub(guide['old'], guide['new'], content)

    return content

def patch_javascript(content):
    """Remove auto-advances and add new functions"""

    # Remove auto-advance from balloon game (line ~427)
    content = re.sub(
        r"setTimeout\(function\(\)\{ goModule\(4\); \}, 1500\);",
        "showBtnGroup(3);",
        content
    )

    # Remove auto-advance from listen game (line ~536)
    content = re.sub(
        r"setTimeout\(function\(\)\{ goModule\(5\); \}, 1500\);",
        "showBtnGroup(4);",
        content
    )

    # Remove auto-advance from connect game (line ~661)
    content = re.sub(
        r"setTimeout\(function\(\)\{ goModule\(6\); \}, 1500\);",
        "showBtnGroup(5);",
        content
    )

    # Add new functions before // === INIT ===
    new_functions = '''
// === TEACHER-DRIVEN MODE ===
function showBtnGroup(moduleNum) {
  var btnGroup = document.getElementById('btnGroup' + moduleNum);
  if(btnGroup) {
    var btns = btnGroup.querySelectorAll('button');
    btns.forEach(function(btn){ btn.classList.add('show'); });
  }
}

function resetModule2() {
  revealedCount = 0;
  revealedSet = {};
  initNewWords();
  document.getElementById('btnGroup2').querySelectorAll('button').forEach(function(btn){
    btn.classList.remove('show');
  });
}

function toggleGuide(el) {
  var arrow = el.querySelector('.arrow');
  var expand = el.parentElement.querySelector('.teacher-guide-expand');
  if(expand) {
    expand.classList.toggle('open');
    arrow.classList.toggle('open');
  }
}

// === DRILL MODE ===
var drillWords = [];
var drillIndex = 0;

function enterDrill() {
  drillWords = BODY.slice();
  drillIndex = 0;
  showDrillCard();
  document.getElementById('drillOverlay').style.display = 'flex';
}

function exitDrill() {
  document.getElementById('drillOverlay').style.display = 'none';
}

function showDrillCard() {
  if(drillIndex < 0) drillIndex = 0;
  if(drillIndex >= drillWords.length) drillIndex = drillWords.length - 1;
  var word = drillWords[drillIndex];
  document.getElementById('drillEmoji').textContent = word.emoji;
  document.getElementById('drillWord').textContent = word.name.toUpperCase();
  document.getElementById('drillCounter').textContent = (drillIndex + 1) + ' / ' + drillWords.length;
}

function drillPrev() {
  if(drillIndex > 0) {
    drillIndex--;
    showDrillCard();
  }
}

function drillNext() {
  if(drillIndex < drillWords.length - 1) {
    drillIndex++;
    showDrillCard();
  }
}

'''

    content = re.sub(
        r'// === INIT ===',
        new_functions + '// === INIT ===',
        content
    )

    # Modify showReviewPrompt to show btn-group instead of just next button
    content = re.sub(
        r"document\.getElementById\('reviewPrompt'\)\.textContent = '🎉 Great memory!';\s+document\.getElementById\('nextBtn1'\)\.classList\.add\('show'\);",
        "document.getElementById('reviewPrompt').textContent = '🎉 Great memory!';\n    showBtnGroup(1);",
        content
    )

    # Modify revealWord to show btn-group instead of just next button
    content = re.sub(
        r"document\.getElementById\('nextBtn2'\)\.classList\.add\('show'\);",
        "showBtnGroup(2);",
        content
    )

    return content

def add_drill_overlay(content):
    """Add drill overlay HTML before closing </div> of main"""

    drill_html = '''
<!-- Drill Overlay -->
<div class="drill-overlay" id="drillOverlay" style="display:none">
  <div class="drill-card">
    <button class="drill-close" onclick="exitDrill()">✕</button>
    <div class="drill-emoji" id="drillEmoji">🧑</div>
    <div class="drill-word" id="drillWord">HEAD</div>
    <div style="font-size:14px;color:#999" id="drillCounter">1 / 5</div>
    <div class="drill-nav">
      <button onclick="drillPrev()">◀</button>
      <button onclick="drillNext()">▶</button>
    </div>
  </div>
</div>

'''

    # Find the closing </div> before </div> (before line 221)
    # Insert before the last </div> of main
    content = re.sub(
        r'(</div>\s*</div>\s*<script>)',
        drill_html + r'</div>\n\n<script>',
        content
    )

    return content

def add_balloon_btn_group(content):
    """Add btn-group for balloon game"""
    # After balloon game module, add hidden btn-group
    balloon_btn = '''  <div class="btn-group" id="btnGroup3">
    <button class="replay-btn" onclick="startBalloonGame()">🔄 Replay</button>
    <button class="next-btn" onclick="goModule(4)">Next Game! ➡️</button>
  </div>
'''

    content = re.sub(
        r'(<div class="balloon-score" id="balloonScore"></div>\s*</div>)',
        r'\1\n' + balloon_btn,
        content
    )

    return content

def add_listen_btn_group(content):
    """Add btn-group for listen game"""
    listen_btn = '''  <div class="btn-group" id="btnGroup4">
    <button class="replay-btn" onclick="startListenGame()">🔄 Replay</button>
    <button class="next-btn" onclick="goModule(5)">Next Game! ➡️</button>
  </div>
'''

    content = re.sub(
        r'(<div class="card-grid" id="listenGrid"></div>\s*</div>)',
        r'\1\n' + listen_btn,
        content
    )

    return content

def add_connect_btn_group(content):
    """Add btn-group for connect game"""
    connect_btn = '''  <div class="btn-group" id="btnGroup5">
    <button class="replay-btn" onclick="startConnectGame()">🔄 Replay</button>
    <button class="next-btn" onclick="goModule(6)">Complete! ➡️</button>
  </div>
'''

    content = re.sub(
        r'(<div class="connect-area" id="connectArea">.*?</div>\s*</div>\s*</div>)',
        r'\1\n' + connect_btn,
        content,
        flags=re.DOTALL
    )

    return content

def main():
    input_file = 'lessons/day3-body.html'

    print(f"Reading {input_file}...")
    content = read_file(input_file)
    original_lines = content.count('\n')
    print(f"Original file: {original_lines} lines")

    print("Patching CSS...")
    content = patch_css(content)

    print("Patching buttons...")
    content = patch_buttons(content)

    print("Patching teacher guides...")
    content = patch_teacher_guides(content)

    print("Adding button groups for games...")
    content = add_balloon_btn_group(content)
    content = add_listen_btn_group(content)
    content = add_connect_btn_group(content)

    print("Patching JavaScript...")
    content = patch_javascript(content)

    print("Adding drill overlay...")
    content = add_drill_overlay(content)

    new_lines = content.count('\n')
    print(f"Patched file: {new_lines} lines (added {new_lines - original_lines} lines)")

    print(f"Writing to {input_file}...")
    write_file(input_file, content)

    print("✅ Done! File patched successfully.")

if __name__ == '__main__':
    main()
