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
  [
    "AI 学习路线：从会用到会做",
    "参考 DeepLearning.AI、Google 机器学习课程和 Hugging Face 学习资料，整理一条普通人也能跟上的 AI 入门路线：先会用工具，再理解模型，最后做出自己的小项目。 AI 学习路线",
    "ai-learning.html"
  ],
  [
    "现代 CSS 布局完全指南",
    "从 Flexbox 到 Grid，从容器查询到层叠上下文，系统梳理现代 CSS 布局方案的选型思路与实践技巧。 CSS 设计",
    "modern-css-layout.html"
  ],
  [
    "Web 性能优化实战手册",
    "总结多年前端性能优化经验，涵盖加载时、运行时、网络三个维度的实用优化建议。 性能 优化",
    "web-performance-guide.html"
  ],
  [
    "React 18 并发特性初探",
    "React 18 引入了新的并发渲染机制，本文介绍 Suspense、useTransition、useDeferredValue 等核心 API。 React",
    "react-18-concurrent.html"
  ],
  [
    "2026 年第一季度读书总结",
    "本季度读了 12 本书，涵盖技术、哲学、小说三个类别。分享每本书的核心观点与个人感悟。 阅读",
    "quarterly-reading-notes.html"
  ],
  [
    "我的开发工具链 2026",
    "每年更新一次的工具链分享，从编辑器到终端，从版本管理到 CI/CD，精选每一款提高效率的工具。 工具",
    "dev-toolchain-2026.html"
  ],
  [
    "微前端架构选型指南",
    "对比 Module Federation、qiankun、Micro-app 等主流方案，结合真实项目经验给出选型建议。 架构",
    "micro-frontend-guide.html"
  ],
  [
    "TypeScript 类型体操入门",
    "从内置工具类型出发，逐步掌握条件类型、映射类型、模板字面量类型等高级类型编程技巧。 TypeScript",
    "typescript-types.html"
  ],
  [
    "Node.js 事件循环详解",
    "理解 Node.js 事件循环的六个阶段，掌握微任务与宏任务的执行顺序，写出更可预测的异步代码。 Node.js",
    "node-event-loop.html"
  ],
  [
    "CSS 动画性能优化技巧",
    "合理使用 transform 和 opacity、避免强制重排、利用 will-change 等技巧，让动画流畅运行。 CSS 动画",
    "css-animation-performance.html"
  ]
];

function renderResults(keyword = '') {
  if (!searchResults) return;
  const normalized = keyword.trim().toLowerCase();
  const matched = posts.filter(([title, desc]) =>
    !normalized || `${title} ${desc}`.toLowerCase().includes(normalized)
  );

  searchResults.innerHTML = matched.map(([title, desc, href]) => `
    <article class="post-card">
      <div class="post-meta"><time>搜索结果</time></div>
      <h3><a href="${href}">${title}</a></h3>
      <p>${desc}</p>
    </article>
  `).join('') || '<p class="hint">没有找到相关文章，换个关键词试试。</p>';
}

if (searchInput) {
  renderResults();
  searchInput.addEventListener('input', event => renderResults(event.target.value));
}
