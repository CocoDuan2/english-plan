# 课件模板使用说明

## 模板设计原则

**只保留框架结构，不包含具体内容**

- ✅ 保留：CSS 样式、导航、通用函数、HTML 结构
- ❌ 不保留：具体词汇、游戏逻辑、动画细节

## 文件说明

### review-template.html
纯框架模板，包含：
- 完整的 CSS 样式（.top/.te/.tz/.sb/.pr/.bbl 等）
- 响应式 @media 样式
- 6 个模块容器（m0-m5）
- 导航栏结构
- 通用函数：speak/playOk/playNo/showConfetti/stars/goM
- 占位符注释：`/* {{PLACEHOLDER}} */`

**agent 需要填充：**
- 词汇数组 W
- M0 开始页内容
- M1-M5 各模块的 initM 函数
- M2 游戏的自定义样式

### teach-template.html
纯框架模板，包含：
- 完整的 CSS 样式
- 响应式 @media 样式
- 10 个幻灯片容器（.sl）
- 导航栏结构
- 通用函数：speak/goTo/tn
- Teacher Notes 功能
- 占位符注释：`<!-- {{PLACEHOLDER}} -->`

**agent 需要填充：**
- 10 页幻灯片内容（Title/Hello/5新词/Listen/Game/All/Bye）
- Teacher Notes 对象 N
- 自定义样式（如果需要）

## 使用流程

1. **读取模板** - agent 先读取对应模板文件
2. **理解结构** - 了解哪些是固定的，哪些需要填充
3. **填充内容** - 只修改占位符标记的部分
4. **保持一致** - 不改变 CSS 类名、函数名、结构

## 关键约束

- **禁止从零生成** - 必须基于模板修改
- **保持类名** - 不要改 CSS 类名
- **完整的 goM** - review 必须包含 initM1-5 所有调用
- **响应式样式** - 不要删除 @media 样式
- **通用函数** - speak/playOk/stars 等不要改

## 占位符说明

### review-template.html
```javascript
/* {{WORDS_ARRAY}} */ - 词汇数组
/* {{M0_START_PAGE}} */ - 开始页
/* {{M1_LEARN}} */ - 学新词
/* {{M2_GAME}} */ - 主题游戏（每天不同）
/* {{M3_LISTEN}} */ - 听力游戏
/* {{M4_MEMORY}} */ - 记忆翻牌
/* {{M5_DONE}} */ - 完成页
/* {{CUSTOM_STYLES}} */ - 自定义样式
```

### teach-template.html
```html
<!-- {{SLIDES}} --> - 10 页幻灯片
<!-- {{TEACHER_NOTES}} --> - Teacher Notes
<!-- {{CUSTOM_STYLES}} --> - 自定义样式
```

## 示例

**错误方式：**
```javascript
// 从零生成，容易遗漏
function goM(d){
  curM+=d;
  // 忘记写 initM3/initM4 调用
}
```

**正确方式：**
```javascript
// 基于模板，goM 已经完整
function goM(d){
  curM+=d;if(curM<0)curM=0;if(curM>5)curM=5;
  // ... 模板已包含所有 initM1-5 调用
  if(curM===1)initM1();
  if(curM===2)initM2();
  if(curM===3)initM3();
  if(curM===4)initM4();
  if(curM===5)initM5();
}
// agent 只需实现各个 initM 函数
```
