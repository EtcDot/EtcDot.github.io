#!/usr/bin/env python3
"""Build the static blog from Markdown files in content/posts."""
from __future__ import annotations

import argparse
import html
import json
import re
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
POST_DIR = ROOT / "content" / "posts"
SITE_CONFIG = ROOT / "content" / "site.json"
STATIC_FILES = ["styles.css", "about.html", "search.html"]


@dataclass
class Post:
    title: str
    date: str
    tags: list[str]
    description: str
    slug: str
    body: str
    featured: bool = False

    @property
    def url(self) -> str:
        return f"{self.slug}.html"

    @property
    def date_label(self) -> str:
        try:
            return datetime.strptime(self.date, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            return self.date


def parse_front_matter(raw: str) -> tuple[dict[str, object], str]:
    if not raw.startswith("---\n"):
        return {}, raw
    end = raw.find("\n---\n", 4)
    if end == -1:
        raise ValueError("front matter is missing closing ---")
    header = raw[4:end]
    body = raw[end + 5 :]
    meta: dict[str, object] = {}
    for line in header.splitlines():
        if not line.strip() or ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value.startswith("[") and value.endswith("]"):
            meta[key] = [item.strip().strip('"\'') for item in value[1:-1].split(",") if item.strip()]
        elif value.lower() in {"true", "false"}:
            meta[key] = value.lower() == "true"
        else:
            meta[key] = value.strip('"\'')
    return meta, body.strip()


def slugify(path: Path) -> str:
    return path.stem.lower().replace(" ", "-")


def load_posts() -> list[Post]:
    posts: list[Post] = []
    for path in sorted(POST_DIR.glob("*.md")):
        meta, body = parse_front_matter(path.read_text(encoding="utf-8"))
        missing = [key for key in ["title", "date", "description"] if not meta.get(key)]
        if missing:
            raise ValueError(f"{path} missing metadata: {', '.join(missing)}")
        tags = meta.get("tags", [])
        if isinstance(tags, str):
            tags = [tags]
        posts.append(
            Post(
                title=str(meta["title"]),
                date=str(meta["date"]),
                tags=[str(tag) for tag in tags],
                description=str(meta["description"]),
                slug=slugify(path),
                body=body,
                featured=bool(meta.get("featured", False)),
            )
        )
    return sorted(posts, key=lambda post: post.date, reverse=True)


def markdown_inline(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    return text


def markdown_to_html(markdown: str) -> str:
    lines = markdown.splitlines()
    out: list[str] = []
    paragraph: list[str] = []
    in_list = False
    in_code = False
    code_lines: list[str] = []

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            out.append(f"<p>{markdown_inline(' '.join(paragraph))}</p>")
            paragraph = []

    def close_list() -> None:
        nonlocal in_list
        if in_list:
            out.append("</ul>")
            in_list = False

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            if in_code:
                out.append("<pre><code>" + html.escape("\n".join(code_lines)) + "</code></pre>")
                code_lines = []
                in_code = False
            else:
                flush_paragraph()
                close_list()
                in_code = True
            continue
        if in_code:
            code_lines.append(line)
            continue
        if not stripped:
            flush_paragraph()
            close_list()
            continue
        if stripped.startswith("# "):
            flush_paragraph()
            close_list()
            out.append(f"<h1>{markdown_inline(stripped[2:])}</h1>")
        elif stripped.startswith("## "):
            flush_paragraph()
            close_list()
            out.append(f"<h2>{markdown_inline(stripped[3:])}</h2>")
        elif stripped.startswith("### "):
            flush_paragraph()
            close_list()
            out.append(f"<h3>{markdown_inline(stripped[4:])}</h3>")
        elif stripped.startswith("- "):
            flush_paragraph()
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li>{markdown_inline(stripped[2:])}</li>")
        else:
            paragraph.append(stripped)
    flush_paragraph()
    close_list()
    return "\n".join(out)


def clean_for_index(text: str) -> str:
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"\*([^*]+)\*", r"\1", text)
    text = re.sub(r"^#+\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*[-*+]\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*\d+\.\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def load_site() -> dict[str, str]:
    return json.loads(SITE_CONFIG.read_text(encoding="utf-8"))


def nav(active: str, site: dict[str, str]) -> str:
    links = [
        ("index.html", "首页", "index"),
        ("about.html", "关于", "about"),
        ("posts.html", "文章", "posts"),
        ("tags.html", "标签", "tags"),
        ("archives.html", "归档", "archives"),
        ("search.html", "搜索", "search"),
    ]
    link_html = "\n".join(
        f'          <a href="{href}"{(" class=\"active\"" if key == active else "")}>{label}</a>'
        for href, label, key in links
    )
    return f"""  <header class="site-header">
    <div class="container">
      <nav class="nav">
        <a href="index.html" class="logo">{html.escape(site['title'])}</a>
        <div class="nav-links">
{link_html}
        </div>
        <button id="theme-toggle" aria-label="切换主题">🌙</button>
      </nav>
    </div>
  </header>"""


def page(title: str, body: str, active: str, site: dict[str, str], extra_class: str = "") -> str:
    class_attr = f' class="container {extra_class}"' if extra_class else ' class="container"'
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(title)} | {html.escape(site['title'])}</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
{nav(active, site)}

  <main{class_attr}>
{body}
  </main>

  <footer class="site-footer">
    <div class="container">
      <p>&copy; {html.escape(site['year'])} {html.escape(site['title'])}. 使用 GitHub Pages 托管。</p>
      <p class="footer-stats">
        本站总访客 <span id="busuanzi_value_site_uv"></span> 人 ·
        总浏览量 <span id="busuanzi_value_site_pv"></span> 次
      </p>
    </div>
  </footer>

  <script src="script.js"></script>
  <script async src="//busuanzi.ibruce.info/busuanzi/2.3/busuanzi.pure.mini.js"></script>
</body>
</html>
"""


def tags_html(tags: list[str]) -> str:
    return "".join(f'<a href="tags.html">{html.escape(tag)}</a>' for tag in tags)


def post_card(post: Post) -> str:
    return f"""        <article class="post-card">
          <div class="post-meta"><time>{html.escape(post.date_label)}</time><span class="post-tags">{tags_html(post.tags)}</span></div>
          <h3><a href="{post.url}">{html.escape(post.title)}</a></h3>
          <p>{html.escape(post.description)}</p>
        </article>"""


def write(out_dir: Path, name: str, content: str) -> None:
    path = out_dir / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def build(out_dir: Path) -> None:
    site = load_site()
    posts = load_posts()
    if out_dir.exists() and out_dir != ROOT:
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    write(out_dir, ".nojekyll", "")

    for filename in STATIC_FILES:
        source = ROOT / filename
        if source.exists() and out_dir != ROOT:
            shutil.copy2(source, out_dir / filename)

    featured = [post for post in posts if post.featured][:3]
    recent = [post for post in posts if post not in featured][:5]
    index_body = f"""    <section class="hero">
      <h1>你好，我是小萌萌</h1>
      <p class="hero-desc">{html.escape(site['description'])}</p>
      <div class="hero-links">
        <a href="{html.escape(site['github'])}" target="_blank">GitHub</a>
        <a href="{html.escape(site['twitter'])}" target="_blank">Twitter</a>
        <a href="about.html">关于我 →</a>
      </div>
    </section>

    <section class="featured-posts">
      <h2>精选文章</h2>
      <div class="post-list">
{chr(10).join(post_card(post) for post in featured)}
      </div>
    </section>

    <section class="recent-posts">
      <h2>最新文章</h2>
      <div class="post-list">
{chr(10).join(post_card(post) for post in recent)}
      </div>
      <div class="section-footer">
        <a href="posts.html">查看全部文章 →</a>
      </div>
    </section>"""
    write(out_dir, "index.html", page(site["title"], index_body, "index", site))

    posts_body = "    <h1>全部文章</h1>\n    <div class=\"post-list\">\n" + "\n".join(post_card(post) for post in posts) + "\n    </div>"
    write(out_dir, "posts.html", page("全部文章", posts_body, "posts", site, "page"))

    tag_map: dict[str, list[Post]] = {}
    for post in posts:
        for tag in post.tags:
            tag_map.setdefault(tag, []).append(post)
    tag_sections = []
    for tag in sorted(tag_map):
        tag_id = "tag-" + re.sub(r"[^0-9A-Za-z\u4e00-\u9fff_-]+", "-", tag).strip("-")
        items = "".join(f'<li><a href="{post.url}">{html.escape(post.title)}</a> <time>{html.escape(post.date_label)}</time></li>' for post in tag_map[tag])
        tag_sections.append(f"<section class=\"tag-section\" id=\"{html.escape(tag_id)}\"><h2>#{html.escape(tag)}</h2><ul>{items}</ul></section>")
    tag_links = []
    for tag in sorted(tag_map):
        tag_id = "tag-" + re.sub(r"[^0-9A-Za-z\u4e00-\u9fff_-]+", "-", tag).strip("-")
        tag_links.append(f'<a href="#{html.escape(tag_id)}">{html.escape(tag)}</a>')
    tags_body = "    <h1>标签</h1>\n    <div class=\"tag-cloud\">" + "".join(tag_links) + "</div>\n" + "\n".join(tag_sections)
    write(out_dir, "tags.html", page("标签", tags_body, "tags", site, "page"))

    archive_items = "".join(f'<li><time>{html.escape(post.date_label)}</time><a href="{post.url}">{html.escape(post.title)}</a></li>' for post in posts)
    archives_body = f"    <h1>归档</h1>\n    <ul class=\"archive-list\">{archive_items}</ul>"
    write(out_dir, "archives.html", page("归档", archives_body, "archives", site, "page"))

    for post in posts:
        article = f"""    <article class="article-content">
      <div class="post-meta">
        <time>{html.escape(post.date_label)}</time>
        <span class="post-tags">{tags_html(post.tags)}</span>
        <span class="post-views">· 阅读量 <span id="busuanzi_value_page_pv"></span></span>
      </div>
{markdown_to_html(post.body)}
    </article>"""
        write(out_dir, post.url, page(post.title, article, "posts", site, "page"))

    post_data = [{
        "title": post.title,
        "desc": post.description,
        "tags": post.tags,
        "body": clean_for_index(post.body),
        "url": post.url,
    } for post in posts]
    script = f"""const root = document.documentElement;
const button = document.querySelector('#theme-toggle');
const storedTheme = localStorage.getItem('theme');
const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

function applyTheme(theme) {{
  root.classList.toggle('dark', theme === 'dark');
  if (button) button.textContent = theme === 'dark' ? '☀️' : '🌙';
  localStorage.setItem('theme', theme);
}}

applyTheme(storedTheme || (prefersDark ? 'dark' : 'light'));

button?.addEventListener('click', () => {{
  applyTheme(root.classList.contains('dark') ? 'light' : 'dark');
}});

const searchInput = document.querySelector('#search-input');
const searchResults = document.querySelector('#search-results');
const posts = {json.dumps(post_data, ensure_ascii=False, indent=2)};

function renderResults(keyword = '') {{
  if (!searchResults) return;
  const raw = keyword.trim();
  const keywords = raw.toLowerCase().split(/\\s+/).filter(Boolean);

  const scored = posts.map(post => {{
    const title = post.title.toLowerCase();
    const desc = post.desc.toLowerCase();
    const tags = (post.tags || []).join(' ').toLowerCase();
    const body = (post.body || '').toLowerCase();
    let score = 0;
    const reasons = [];

    for (const kw of keywords) {{
      let hit = false;
      if (title.includes(kw)) {{ score += 100; hit = true; if (!reasons.includes('标题匹配')) reasons.push('标题匹配'); }}
      if (tags.includes(kw)) {{ score += 50; hit = true; if (!reasons.includes('标签匹配')) reasons.push('标签匹配'); }}
      if (desc.includes(kw)) {{ score += 30; hit = true; if (!reasons.includes('描述匹配')) reasons.push('描述匹配'); }}
      if (body.includes(kw)) {{ score += 10; hit = true; if (!reasons.includes('正文匹配')) reasons.push('正文匹配'); }}
      if (!hit) return null;
    }}

    return {{ ...post, score, reasons }};
  }});

  const matched = scored.filter(Boolean).sort((a, b) => b.score - a.score);

  searchResults.innerHTML = matched.map(post => `
    <article class="post-card">
      <div class="post-meta"><time>${{post.reasons.join(' / ') || '搜索结果'}}</time></div>
      <h3><a href="${{post.url}}">${{post.title}}</a></h3>
      <p>${{post.desc}}</p>
    </article>
  `).join('') || '<p class="hint">没有找到相关文章，换个关键词试试。</p>';
}}

if (searchInput) {{
  renderResults();
  searchInput.addEventListener('input', event => renderResults(event.target.value));
}}
"""
    write(out_dir, "script.js", script)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the blog from content/posts/*.md")
    parser.add_argument("--out", default=".", help="output directory, defaults to repository root")
    args = parser.parse_args()
    out_dir = (ROOT / args.out).resolve() if not Path(args.out).is_absolute() else Path(args.out)
    build(out_dir)
    print(f"Built {len(load_posts())} posts into {out_dir}")


if __name__ == "__main__":
    main()
