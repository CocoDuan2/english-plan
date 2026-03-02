# AGENTS.md - English Tutor Agent

## 角色
3岁幼儿英语启蒙课件生成器（佩琪主题）。

## 任务
1. 按 progress.md 生成下一课的两套课件（teach.html + review.html）
2. 更新 progress.md 和 index.html
3. git commit + push 部署

## 工作目录
- `english-plan/` — 课件项目根目录
- `english-plan/README.md` — 课程总设计
- `english-plan/progress.md` — 当前进度
- `english-plan/lessons/` — 课件目录

## 输出格式
```
english-plan/lessons/dayN-topic/
  teach.html   ← 外教课件
  review.html  ← 课后复习游戏
```

---

## 🐷 佩琪深度融入（核心设计原则）

佩琪不是贴图装饰，是课堂的引导角色。

### 素材
- 目录：`assets/peppa/`，课件中用 `../../assets/peppa/xxx.png`
- 详见 `assets/peppa/README.md`

### 佩琪在课件中的角色
- **引导者**：每页都有佩琪（或 George/家人）出现，用对话气泡说句式
- **故事串联**：每课有简单故事线（如"帮佩琪找颜色""和 George 去动物园"）
- **庆祝者**：答对/完成时用 peppa-jumping / peppa-george-jumping 庆祝
- **佩琪气泡样式**：白色圆角气泡 + 底部小三角 + 橙色粗体文字

### ⚠️ 佩琪元素的度
- 每页都要有佩琪角色出现（60-100px），但不抢主视觉
- 主视觉是 SVG 画的物品（见下方）
- 佩琪图片轮换使用不同角色（Peppa/George/Daddy/Mummy/朋友们）

---

## 🎨 物品视觉规范（Twemoji + SVG 混合）

### 策略
- **颜色主题**（Colors, More Colors）→ 手写 SVG（需要精确控制颜色）
- **其他所有主题** → Twemoji CDN（辨识度最高，3岁小孩一眼认出）

### Twemoji 用法
- CDN：`https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/svg/{code}.svg`
- 用 `<img>` 标签引用，设置 width 控制大小
- 常用码点示例：
  - 🐱 cat = `1f431`，🐶 dog = `1f436`，🐟 fish = `1f41f`
  - 🍎 apple = `1f34e`，🍌 banana = `1f34c`，🥛 milk = `1f95b`
  - 👩 mom = `1f469`，👨 dad = `1f468`，👶 baby = `1f476`
- 查码点：https://emojipedia.org/ 搜索 emoji 名称

### Twemoji 示例
```html
<img src="https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/svg/1f431.svg" width="120" alt="cat">
```

### SVG 手写规范（仅颜色主题）
- 尺寸：160x160 viewBox，实际显示按需缩放
- 风格：圆润、简洁、2-3个基本形状组合
- 颜色：主体用当天教学颜色
- 禁止：复杂路径、渐变、滤镜

---

## 🎭 故事化课程设计（核心理念）

### 为什么要故事化
- 3岁小孩不是在"学单词"，而是在"听故事"
- 孤立的词汇（red, blue, yellow）→ 无聊，记不住
- 故事情境（Peppa穿红裙子去动物园）→ 有画面，能记住
- 情感连接：小孩能想象自己和佩琪一起做这件事

### 每课必须有的故事元素
1. **故事标题**：不是"Colors"，而是"Peppa's Colorful Day"
2. **故事线**：有开始（Hello）、发展（新词在情境中出现）、结尾（Bye）
3. **情境**：每个新词都在真实场景中出现（不是孤立展示）
4. **情感**：使用第一人称（I see/I like/I can），让小孩有代入感
5. **连贯性**：前后课之间有故事延续（昨天去了动物园，今天野餐...）

### RAZ 句式重复原则（核心！）
- **每课只有一个句式**，反复用在不同词上
- 例如 Day 1: "It's ___!" 用 5 次（red/blue/yellow/green/orange）
- 例如 Day 2: "I see a ___!" 用 5 次（cat/dog/fish/bird/duck）
- **故事化 ≠ 改句式**，故事化体现在场景描述（老师说的话/Teacher Notes）
- 气泡里的句式必须统一，不能每个词换一个句子

### 正确的故事化方式
- ❌ 错误：每个词用不同句子（"I wear red" / "Look at blue sky" / "Play with yellow ball"）
- ✅ 正确：统一句式 + 场景描述
  - 气泡：It's red! / It's blue! / It's yellow!（句式统一）
  - Teacher Notes：Peppa wears a red dress / Look at the blue sky / Play with a yellow ball（场景描述）


### 故事化 vs 词汇表对比

❌ **错误示例（词汇表式）**：
- Title: "Colors"
- S1: Hello! Today we learn colors.
- S2: red (展示红色方块)
- S3: blue (展示蓝色方块)

✅ **正确示例（故事化）**：
- Title: "Peppa's Colorful Day"
- S1: Hello! Come with me! Let's find colors!
- S2: Peppa wears a red dress! (佩琪穿红裙子)
- S3: Look! The sky is blue! (看蓝天)
- S4: Peppa plays with a yellow ball! (玩黄球)

### 故事主题示例（参考 README.md）
- Day 1: Peppa's Colorful Day（佩琪的彩色一天）
- Day 2: Visit the Zoo（去动物园）
- Day 3: Morning Routine（早晨起床）
- Day 4: Peppa's Picnic（野餐时间）
- Day 5: Family Photo Day（全家福）

### 生成课件时的检查清单
- [ ] 标题是故事化的（不是单纯的主题词）
- [ ] Hello 页有佩琪的邀请（Come with me!）
- [ ] 每个新词都在情境中出现（不是孤立展示）
- [ ] 使用第一人称句式（I see/I like/I can）
- [ ] Bye 页有故事结尾（回顾今天的冒险）

---

## teach.html 规范（外教课件）

### 定位
外教屏幕共享，老师控制翻页节奏。**幻灯片，不是游戏。**

### 结构（10页，固定）
1. **Title** — 故事标题 + 主题预览
2. **Hello** — 引导页（Come with me! 今天要做什么）
3-7. **New Words** — 每词一页：佩琪气泡说句式 + Twemoji/SVG 物品 + 大单词
8. **第一个互动** — 听词互动（每天不同，见下方规划）
9. **第二个互动** — 游戏互动（每天不同，见下方规划）
10. **Bye** — 佩琪庆祝 + 预告明天

### 互动差异化（核心！）
- **禁止每天都用同样的互动**（如每天都 Tap to Reveal）
- 每课的互动页（Listen & Say 后面）必须有差异化设计
- 示例：
  - Day 1: Tap to Reveal（点灰盒揭示）
  - Day 2: Animal Sounds（听叫声点动物）
  - Day 3: Simon Says（老师说 Touch your nose，小孩做动作）
  - Day 4: Shopping Basket（点食物装篮子）
  - Day 5: Family Match（配对家人照片）
- 互动要符合故事主题，不是为了互动而互动

1. **Title** — 故事标题 + 主题预览
2-6. **New Words** — 每词一页：佩琪气泡说句式 + SVG/Twemoji 物品 + 大单词
7. **第一个互动** — 听声音按钮（可多次点击）
8. **第二个互动** — 差异化互动（每课不同）
9. **第三个互动** — 所有词网格，老师随机指问
10. **Bye** — 佩琪庆祝 + 预告明天
2. **Hello** — 佩琪打招呼，介绍今天要做什么（简单故事线）
2-6. **New Words** — 每词一页：佩琪气泡说句式 + SVG物品大图 + 大单词 + 句式
8. **Tap to Reveal** — 灰色方块点击揭示（唯一互动，老师操作）
9. **All Together** — 所有词网格，老师随机指问
10. **Bye** — 佩琪跳泥坑庆祝

### 每页布局（宁大勿小！3岁小孩要看得清）
### 每页布局（宁大勿小！3岁小孩要看得清）
- 佩琪角色图（.pr img）：75px
- 首页/Hello/Bye 页角色图：110px
- 对话气泡：26px+ 字号，加粗
- SVG/Twemoji 物品：160px（obj-wrap）
- 大单词：88px+（桌面 100px+），加粗
- 句式：34px+（桌面 38px+）
- **避免重复句式**：若页面上方气泡已说完整句式（如 `It's red!` / `I see a cat!`），下方不再重复同一句；下方仅保留大单词。
- 标题：42px+
- 副标题：22px+
- 揭示方块：130x130（桌面 150x150）
- All Together 网格：SVG/Twemoji 80px+，文字 24px+
- All Together 页家庭图：120px
- 背景：每个主题对应不同渐变背景
- ⚠️ 宁可太大也不要太小，屏幕共享后会缩小

### 技术规格

### 听声音按钮（Listen & Say 页）
- 圆形按钮，100px（手机 80px），渐变背景
- 可多次点击，每次都播放语音
- 按钮内显示 emoji 或 Twemoji 图标
- 按下有 scale(.9) 动画反馈
- 示例：`.sound-btn{width:100px;height:100px;border-radius:50%;background:linear-gradient(135deg,#a8e6cf,#88d8b0)}`

### 图片存在性检查（必须！）
- 生成课件前必须检查 `assets/peppa/` 目录，确认所有引用的图片文件存在
- 可用的角色图：peppa-pig-happy-standing, george-standing, daddy-pig-standing, mummy-pig-standing-grass, candy-cat-green-dress, emily-elephant-standing, peppa-pig-red-polka-dot-dress, peppa-fairy-princess, george-superhero-costume, peppa-family-group-outdoors, peppa-and-george-ooo, george_pig_dinosaur
- 不存在的图片不要用（如 suzy-sheep, danny-dog, pedro-pony, peppa-george-jumping）
- 如需新角色，从可用列表中选择替代
- 纯单文件 HTML，无外部依赖（除佩琪 PNG）
- 全英文，无中文
- Teacher Notes：右下角 FAB，按 T 切换
- 导航：底部 Back/页码/Next，键盘左右箭头

### 首屏与次屏（Title + Hello）幼儿友好硬约束
- **前2页必须图片主导**：以角色图 + 大图标/SVG 为主，文字只保留极少量关键词。
- **禁止首屏词墙**：不要在前2页堆 5 个英文单词文本（3岁儿童不识字）。
- **禁止抽象提问文案**：如 `What color is it?`、`Can you say: I see a ___!` 这类放在首屏/次屏。
- **句式延后**：核心句式从第3页开始进入（新词页），前2页只做情境导入。


### 响应式布局（必须兼容手机/iPad/PC）
- 所有课件必须包含三档 media query：
  - `@media(max-width:480px)` — 手机：缩小字号、SVG、网格列数
  - `@media(min-width:481px) and (max-width:767px)` — iPad
  - `@media(min-width:768px)` — PC
- teach "All Together" 总览页：手机 2 列网格，SVG 70px，词标签 20px
- review 模块：复习和新词必须分开为独立模块（不能挤在同一页）
- 禁止水平溢出，所有内容 max-width 不超过视口宽度

### 课程体系（RAZ 递进式）
- 无专门复习日，每天都是新主题新词汇
- 旧词通过复习桥接页和故事线自然复现
- 主题不循环，持续推进新领域
- 详见 README.md 课程规划表

---

## review.html 规范（课后复习游戏）

### 定位
课后小孩自己玩，家长辅助。**游戏，不是幻灯片。**

### 结构（6个模块，固定）
0. **开始页** — 佩琪大图 + 当天词汇SVG预览 + "Let's Play!"（解锁 AudioContext）
1. **学新词** — 点击灰色卡片揭示 Twemoji/SVG 物品 + 发音
2. **主题游戏** — 跟主题相关的互动（每课不同）
3. **听力游戏** — 听单词找图片（带🔊重听按钮）
4. **记忆翻牌** — 配对游戏
5. **Done 页** — 佩琪全家庆祝 + "All Done" + Play Again







### 佩琪在 review 中
- 开始页：佩琪大图（140px）邀请玩游戏
- 每个游戏都有佩琪引导：角色图（75px）+ 气泡提示
- 答对：佩琪跳动动画（@keyframes peppa-jump，向上30px，0.6s）+ 撒花 + 庆祝音效
- 角色轮换：不同游戏用不同角色（Peppa/George/Candy Cat 等）
- 完成：佩琪全家福（120px）






### 语音
- **review 游戏中只读单词，不读句子**（句子播放慢且易失败，体验差）
- 游戏提示用中文显示，语音只读目标单词
- 例如：显示"找到 cat"，语音只说 "cat"（不说 "Find cat"）
- 单词：有道 `https://dict.youdao.com/dictvoice?audio={word}&type=2`
- 句子：百度 `https://fanyi.baidu.com/gettts?lan=en&text={text}&spd=4&source=web`
- `speak(text, cb)` 统一入口，4秒安全超时
- speak() fallback 策略：单词用有道优先百度备用，句子用百度优先有道备用
- 含空格的文本视为句子，用百度；单词用有道
- 生成课件后必须检查所有 speak() 调用的文本能正常播放
- 音效用 AudioContext 合成，不依赖外部文件
- 禁止 Web Speech API

### 排版尺寸（宁大勿小！小孩要看得清）
- 顶栏标题：26px+ 粉色(#e91e8c)加粗
- 顶栏中文提示：20px+ 橙色(#e67e22)加粗
- 顶栏中文提示样式（.tz）：emoji图标开头（👆💦👂🎴等）+ 渐变背景（#ff6b9d→#ffa07a）+ 白色文字 + 圆角25px + 增强阴影 + ::after伪元素底部装饰，禁止灰底纯文本。
- 每天提示框颜色要变化（按主题色设 `--tip-accent` / `--tip-bg`），例如 Colors=橙粉，Animals=绿色，Body=蓝色。
- 星星栏：22px+
- 角色图片（.pr img）：75px
- 对话气泡：22px+ 加粗
- 学习/听力卡片 SVG：90px+，标签 20px+
- 泥坑按钮：105px+，内部 SVG 75px+
- 记忆翻牌网格：宽 440px+（桌面 560px+），卡面 emoji 44px+，背面 SVG 70px+，文字 18px+
- 开始页 Peppa：110px，按钮 32px+
- ⚠️ 宁可太大也不要太小，手机上小孩要能戳得到


### Done 页（必须有）
- review 结束必须进入独立 Done 页面，不能只停留在 Memory Flip
- Done 页要有：佩琪全家图、"All Done!" 大标题、鼓励文案、Play Again 按钮
- Done 页星星显示满星，给到明确完成反馈
- Done 页家庭图/角色图：120px

### 交互规范
- 可点击区域最小 80x80px
- 答对：playOk() + speak(word) + 1200ms 后继续
- 答对视觉效果：playOk() 必须触发 showConfetti() 撒花动画（20个彩色圆点飘落）
- 答错：playNo() + speak(正确词) + 不跳转
- 星星样式：已得⭐（黄色emoji），未得★（灰色实心星 color:#bbb），禁止用黑色空心☆或灰心🩶
- 已揭示卡片可重复点击发音
- 每模块独立 busy lock 防重复点击
- 中文提示口语化：「点一点，哪个是 red？」「答对啦！」

### 开场文案与模块限制（3岁可理解）
- review 开场页不做文字密集说明；优先“角色+图形+按钮”。
- 不使用抽象语言指令，避免长句；单句不超过 6 个词为优先。
- 模块提示以动作词为主（tap/find/match/jump/listen），减少口号式句式教学。

- teach 新词页遵循“气泡一句 + 下方单词”结构，不要做“气泡句 + 页面句”双重重复。

### 导航（review 必须有完整导航）
- 底部 Back/页码/Next（三栏布局，和 teach 一致）
- 记忆翻牌完成后自动跳转 Done 页
- Done 页保留 Play Again 按钮，回到开始页

---


## index.html 规范（首页）

- 首页主标题固定：**跟着佩琪学英语**
- 不要使用游戏感图标（如 🎮、🕹️）
- 卡片图标优先用佩琪角色小图（Peppa/George 等 PNG）
- 首页风格与课程一致：童趣、清晰、非游戏厅风格

---

## 差异化生成约束（防止 Day1/Day2 同质）

- Day2 及后续课程禁止复用 Day1 的页面顺序、游戏机制和视觉布局；至少更换 2 个模块形态（例如：揭示玩法、听力玩法、配对玩法）。
- teach.html 必须有独立故事线（例如 parade/rescue/picnic），标题与过渡页文案不可与前一课重复。
- review.html 的 4 个核心玩法（学词、主题游戏、听声找图、记忆类）必须和前一课在交互上有明确差异，不能只是换词。
- 角色图要轮换（Peppa/George/父母/朋友），同一角色不能连续主导所有页面。
- 每课至少 3 处主视觉版式变化（网格、卡片比例、互动容器、收尾页构图）。

## 页面比例和谐（核心视觉约束）

### 原则
- 同一课件内所有页面的元素比例必须和谐统一，不能上一页大下一页小
- 以 Day1 为基准，后续课件严格对齐

### teach.html 统一尺寸
- 首页/Hello/Bye 页角色图：110px
- 新词页角色图（.pr img）：75px
- 新词页 SVG/Twemoji 物品：160px
- Tap Reveal 角色图：75px
- All Together 角色图：120px，网格 SVG：80px，词标签：24px
- 标题 .ttl：42px，单词 .word：88px（桌面100px），句式 .sent：34px，气泡 .bbl：26px

### review.html 统一尺寸
- 开始页角色图：110px
- 模块内角色图（.pr img）：75px
- 学习卡片 SVG/Twemoji：90px
- 互动按钮：最小 80x80px
- Done 页角色图：110px
- 英文标题：26px，中文提示：20px，气泡：22px

### 移动端
- 可点区域不少于 80x80px
- 三档响应式 media query 必须包含

## 共通规范

### 低龄认知优先
- 图片优先于文字；同一页英文可读文本尽量控制在 1-3 行。
- 新词先“看图+听音”，再出现大单词文本；不要先上文字。
- 前2页只做兴趣唤起，不做句式考核。

### 每课只有1个核心句式
- 句式贯穿 teach 和 review
- 只替换关键词，句式不变
- 复习词必须能搭配当天句式


---

## Git 配置
- repo: CocoDuan2/english-plan
- user.email: 627941117@qq.com
- user.name: CocoDuan2
- GitHub Pages: https://cocoduan2.github.io/english-plan/

## 生成前必读
- `english-plan/README.md` — 课程设计
- `english-plan/progress.md` — 当前进度
- 最近一课的 teach.html 和 review.html — 了解风格


## index.html 规范（课程首页）
- 首页主标题固定为：`跟着佩琪学英语`
- 不使用“游戏”图标风格（如 🎮），练习入口用中性学习图标（如 📝）
- 风格统一：可爱、干净、学习导向，不做游戏厅视觉

## 📚 Day 1-6 Teach 互动差异化规范

### 核心原则
- **S7/S8/S9 每天都必须不同**，不能重复使用相同的互动方式
- 互动要符合当天的故事主题
- 三个页面递进：S7 听词 → S8 互动游戏 → S9 总复习

### Day 1: Peppa's Colorful Day
- S7: **Color Buttons** — 5个彩色圆按钮，点击听颜色
- S8: **Find in Picture** — 佩琪房间场景图，点击物品说颜色
- S9: **Color Parade** — 5个颜色横排展示，老师随机指

### Day 2: Visit the Zoo
- S7: **Animal Sounds** — 5个动物按钮，点击听叫声
- S8: **Zoo Map** — 动物园地图，点击区域看动物
- S9: **Animal Parade** — 5个动物横排，老师随机指

### Day 3: Morning Routine
- S7: **Mirror Game** — 镜子里的脸，点击部位听词
- S8: **Wash Sequence** — 按顺序点击洗脸步骤
- S9: **Body Check** — 5个部位网格，老师随机指

### Day 4: Peppa's Picnic
- S7: **Picnic Basket** — 篮子里的食物，点击听词
- S8: **Pack the Basket** — 点击食物装入篮子（带动画）
- S9: **Picnic Spread** — 野餐布上的食物，老师随机指

### Day 5: Family Photo Day
- S7: **Family Tree** — 家谱树，点击每个人听词
- S8: **Photo Album** — 翻页相册，每页一个家人
- S9: **Family Portrait** — 全家福，老师随机指

### Day 6: Getting Dressed
- S7: **Wardrobe** — 衣柜，点击衣物听词
- S8: **Dress Up** — 点击给佩琪穿衣服
- S9: **Outfit Check** — 穿好的衣服展示，老师随机指

### 设计要点
- S7 必须可点击，每个词都能听
- S8 要有明确的互动目标（找、装、排序等）
- S9 是静态展示，供老师随机指问
- 避免重复：不要每天都用网格、按钮、翻牌等相同形式

---

## 📋 生成检查清单（每次生成必查）

### Teach 课件
- [ ] 10 页结构：Title → Hello → 5新词 → 2互动 → Bye
- [ ] 句式统一（每课只有一个句式，重复5次）
- [ ] 故事化标题（如 "Peppa's Colorful Day"，不是 "Colors"）
- [ ] Hello 页有引导（Come with me! Let's...）
- [ ] S8-S9 互动符合当天规划（见 Day 1-6 规范）
- [ ] 所有角色图尺寸统一（75px 模块内，110px 首页/Bye）
- [ ] Twemoji CDN 正确（twitter/twemoji@14.0.2）
- [ ] Bye 页有预告明天

### Review 课件
- [ ] 5 模块：Start → Learn → Game → Memory → Done
- [ ] 游戏语音只读单词（不读句子）
- [ ] 点错不读单词（只播放错误音效）
- [ ] 答对有撒花效果
- [ ] 星星用 ⭐/🩶
- [ ] 导航完整（Back/页码/Next）
- [ ] Done 页有 Play Again 按钮

### 通用规范
- [ ] 所有图片路径存在（检查 assets/peppa/）
- [ ] speak() 有 fallback（单词有道优先，句子百度优先）
- [ ] 响应式三档 media query
- [ ] 无 JavaScript 错误
- [ ] 初始化调用存在（teach: goTo(0), review: goM(0)）
