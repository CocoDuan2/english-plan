# Ranran English Plan 🐷

3岁幼儿英语启蒙课件（佩琪主题）

## 课程体系

### 📚 词汇课程（Day 1-40）
- 4个Level，每个Level 10课
- 故事化学习，RAZ递进式
- 每课 teach.html（外教课）+ review.html（复习游戏）
- 详见：`VOCAB-PLAN.md` + `vocab-progress.md`

### 🔤 自然拼读（P1-P101）
- 5个Phonics Level，共101课
- 牛津自然拼读标准
- 字母音 → 短元音 → 长元音 → 辅音组合 → 复杂拼读
- 详见：`PHONICS-PLAN.md` + `phonics-progress.md`

## 在线访问
https://cocoduan2.github.io/english-plan/

## 课件特色
- 佩琪深度融入每页（不是贴图装饰）
- 故事化学习（不是词汇表）
- 差异化互动（每天不同的游戏）
- 响应式设计（手机/iPad/PC）
- 撒花效果、星星系统、语音反馈

## 目录结构
```
english-plan/
├── index.html              # 主页（词汇 + 拼读入口）
├── level-1.html ~ level-4.html  # 词汇课程导航
├── phonics-index.html      # 自然拼读首页
├── phonics-1.html ~ phonics-5.html  # 拼读课程导航
├── lessons/
│   ├── level-1/ ~ level-4/  # 词汇课件
│   └── phonics-1/ ~ phonics-5/  # 拼读课件
└── assets/
    └── peppa/              # 佩琪角色图
```

## 开发
- Agent: english-tutor（OpenClaw）
- 模板：`templates/teach-template.html` + `review-template.html`
- 规范：`../AGENTS.md`
