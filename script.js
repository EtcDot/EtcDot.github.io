const root = document.documentElement;
const button = document.querySelector('#theme-toggle');
const storedTheme = localStorage.getItem('theme');
const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

function applyTheme(theme) {
  root.classList.toggle('dark', theme === 'dark');
  if (button) button.textContent = theme === 'dark' ? '☀️' : '🌙';
  localStorage.setItem('theme', theme);
}

applyTheme(storedTheme || (prefersDark ? 'dark' : 'light'));

button?.addEventListener('click', () => {
  applyTheme(root.classList.contains('dark') ? 'light' : 'dark');
});

const searchInput = document.querySelector('#search-input');
const searchResults = document.querySelector('#search-results');
const posts = [
  {
    "title": "AI 学习路线：从会用到会做",
    "desc": "参考 DeepLearning.AI、Google 机器学习课程和 Hugging Face 学习资料，整理一条普通人也能跟上的 AI 入门路线：先会用工具，再理解模型，最后做出自己的小项目。",
    "tags": [
      "AI",
      "学习路线"
    ],
    "body": "AI 学习路线：从会用到会做 AI 学习不一定要从复杂公式开始。更适合普通人的路线，是先把工具用起来，再理解背后的基本概念，最后用一个小项目把知识串起来。 第一阶段：先会用 AI 工具 先熟悉 ChatGPT、Claude、Gemini 这类对话工具，重点练习三件事： 把问题说清楚：说明背景、目标、限制和输出格式。 让 AI 帮你拆解任务：比如写作、学习、代码、翻译、总结。 学会追问和修正：不要期待一次回答完美，要像和同事讨论一样迭代。 可以每天拿一个真实任务练习，比如整理一篇文章、生成学习计划、改写文案、分析一个产品页面。 第二阶段：理解机器学习基础 当你会用 AI 之后，再去理解一些基础概念会更容易： 数据集：模型从什么材料里学习。 训练：模型如何从数据里调整参数。 推理：模型如何根据输入生成输出。 过拟合：模型记住了训练题，却不会做新题。 评估：如何判断模型结果好不好。 这一阶段可以参考 Google Machine Learning Crash Course 这类入门资料，不需要一开始就啃很厚的数学书。 第三阶段：认识大语言模型 大语言模型的核心能力，是根据上下文预测和生成文本。你可以重点理解这些关键词： Token：模型处理文字的基本单位。 上下文窗口：模型一次能看到多少内容。 Prompt：你给模型的任务说明。 Embedding：把文字变成可以计算的向量。 RAG：让模型先查资料，再基于资料回答。 理解这些概念后，你会更容易判断 AI 什么时候靠谱、什么时候容易胡说。 第四阶段：做一个小项目 学习 AI 最有效的方法，是做一个能跑起来的小项目。可以从这些方向开始： 个人知识库问答：把自己的笔记变成可查询资料库。 文章总结助手：输入一篇长文，输出摘要、要点和行动清单。 提示词模板库：整理常用工作场景的 Prompt。 简单客服机器人：基于固定文档回答常见问题。 项目不用大，关键是完整走一遍：输入、处理、输出、改进。 推荐学习顺序 每天用 AI 解决一个真实问题。 学会写结构化 Prompt。 了解机器学习和大语言模型基础概念。 学会调用一个 AI API。 做一个自己的小工具。 记录过程，形成自己的方法论。 参考资源方向 DeepLearning.AI 的 AI 入门课程，适合建立整体认知。 Google Machine Learning Crash Course，适合理解机器学习基础。 Hugging Face Learn，适合了解模型、数据集和开源生态。 OpenAI 文档，适合学习提示词、API 和应用开发。 最重要的是：不要只收藏资料。每学一个概念，就把它用在自己的文章、工具或工作流里。",
    "url": "ai-learning.html"
  },
  {
    "title": "现代 CSS 布局完全指南",
    "desc": "从 Flexbox 到 Grid，从容器查询到层叠上下文，系统梳理现代 CSS 布局方案的选型思路与实践技巧。",
    "tags": [
      "CSS",
      "设计"
    ],
    "body": "现代 CSS 布局完全指南 这是一篇占位示例文章，用来展示博客的文章列表、标签和归档效果。 适合使用 Flexbox 的场景 Flexbox 适合一维布局，比如导航栏、按钮组、卡片内部元素对齐。 适合使用 Grid 的场景 Grid 适合二维布局，比如仪表盘、作品集、复杂页面骨架。",
    "url": "modern-css-layout.html"
  },
  {
    "title": "Web 性能优化实战手册",
    "desc": "总结多年前端性能优化经验，涵盖加载时、运行时、网络三个维度的实用优化建议。",
    "tags": [
      "性能",
      "优化"
    ],
    "body": "Web 性能优化实战手册 这是一篇占位示例文章。你可以把它替换成自己的性能优化笔记。 加载时优化 减少关键资源体积，压缩图片，合理拆分脚本。 运行时优化 减少不必要的重排和重绘，避免长任务阻塞主线程。",
    "url": "web-performance-guide.html"
  },
  {
    "title": "React 18 并发特性初探",
    "desc": "React 18 引入了新的并发渲染机制，本文介绍 Suspense、useTransition、useDeferredValue 等核心 API。",
    "tags": [
      "React"
    ],
    "body": "React 18 并发特性初探 这是一篇占位示例文章，可以替换为你的 React 学习记录。",
    "url": "react-18-concurrent.html"
  },
  {
    "title": "2026 年第一季度读书总结",
    "desc": "本季度读了 12 本书，涵盖技术、哲学、小说三个类别。分享每本书的核心观点与个人感悟。",
    "tags": [
      "阅读"
    ],
    "body": "2026 年第一季度读书总结 这是一篇占位示例文章，可以替换为你的读书笔记。",
    "url": "quarterly-reading-notes.html"
  },
  {
    "title": "我的开发工具链 2026",
    "desc": "每年更新一次的工具链分享，从编辑器到终端，从版本管理到 CI/CD，精选每一款提高效率的工具。",
    "tags": [
      "工具"
    ],
    "body": "我的开发工具链 2026 这是一篇占位示例文章，可以替换为你自己的工具链整理。",
    "url": "dev-toolchain-2026.html"
  },
  {
    "title": "微前端架构选型指南",
    "desc": "对比 Module Federation、qiankun、Micro-app 等主流方案，结合真实项目经验给出选型建议。",
    "tags": [
      "架构"
    ],
    "body": "微前端架构选型指南 这是一篇占位示例文章，可以替换为你的架构学习记录。",
    "url": "micro-frontend-guide.html"
  },
  {
    "title": "TypeScript 类型体操入门",
    "desc": "从内置工具类型出发，逐步掌握条件类型、映射类型、模板字面量类型等高级类型编程技巧。",
    "tags": [
      "TypeScript"
    ],
    "body": "TypeScript 类型体操入门 这是一篇占位示例文章，可以替换为你的 TypeScript 笔记。",
    "url": "typescript-types.html"
  },
  {
    "title": "Node.js 事件循环详解",
    "desc": "理解 Node.js 事件循环的六个阶段，掌握微任务与宏任务的执行顺序，写出更可预测的异步代码。",
    "tags": [
      "Node.js"
    ],
    "body": "Node.js 事件循环详解 这是一篇占位示例文章，可以替换为你的 Node.js 学习记录。",
    "url": "node-event-loop.html"
  },
  {
    "title": "CSS 动画性能优化技巧",
    "desc": "合理使用 transform 和 opacity、避免强制重排、利用 will-change 等技巧，让动画流畅运行。",
    "tags": [
      "CSS",
      "动画"
    ],
    "body": "CSS 动画性能优化技巧 这是一篇占位示例文章，可以替换为你的动画性能笔记。",
    "url": "css-animation-performance.html"
  }
];

function renderResults(keyword = '') {
  if (!searchResults) return;
  const raw = keyword.trim();
  const keywords = raw.toLowerCase().split(/\s+/).filter(Boolean);

  const scored = posts.map(post => {
    const title = post.title.toLowerCase();
    const desc = post.desc.toLowerCase();
    const tags = (post.tags || []).join(' ').toLowerCase();
    const body = (post.body || '').toLowerCase();
    let score = 0;
    const reasons = [];

    for (const kw of keywords) {
      let hit = false;
      if (title.includes(kw)) { score += 100; hit = true; if (!reasons.includes('标题匹配')) reasons.push('标题匹配'); }
      if (tags.includes(kw)) { score += 50; hit = true; if (!reasons.includes('标签匹配')) reasons.push('标签匹配'); }
      if (desc.includes(kw)) { score += 30; hit = true; if (!reasons.includes('描述匹配')) reasons.push('描述匹配'); }
      if (body.includes(kw)) { score += 10; hit = true; if (!reasons.includes('正文匹配')) reasons.push('正文匹配'); }
      if (!hit) return null;
    }

    return { ...post, score, reasons };
  });

  const matched = scored.filter(Boolean).sort((a, b) => b.score - a.score);

  searchResults.innerHTML = matched.map(post => `
    <article class="post-card">
      <div class="post-meta"><time>${post.reasons.join(' / ') || '搜索结果'}</time></div>
      <h3><a href="${post.url}">${post.title}</a></h3>
      <p>${post.desc}</p>
    </article>
  `).join('') || '<p class="hint">没有找到相关文章，换个关键词试试。</p>';
}

if (searchInput) {
  renderResults();
  searchInput.addEventListener('input', event => renderResults(event.target.value));
}
