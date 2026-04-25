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
  ['AI 学习路线：从会用到会做', 'AI 入门、提示词、机器学习、RAG、小项目', 'ai-learning.html'],
  ['现代 CSS 布局完全指南', 'Flexbox、Grid、容器查询、设计', 'posts.html'],
  ['Web 性能优化实战手册', '加载优化、运行时优化、网络优化', 'posts.html'],
  ['React 18 并发特性初探', 'Suspense、useTransition、并发渲染', 'posts.html'],
  ['我的开发工具链 2026', '编辑器、终端、Git、CI/CD', 'posts.html'],
  ['TypeScript 类型体操入门', '条件类型、映射类型、模板字面量类型', 'posts.html']
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
