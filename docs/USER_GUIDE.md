# 用户文档：如何管理博客内容

这个博客现在已经改成「Markdown 写文章 + 脚本自动生成网站 + GitHub Actions 自动发布」的流程。

你平时只需要关心 `content/posts/` 里面的 Markdown 文章。

## 1. 写一篇新文章

在 `content/posts/` 目录中新建一个 `.md` 文件，例如：

```text
content/posts/my-new-post.md
```

文件名建议使用英文、小写和短横线，最后会变成文章网址：

```text
my-new-post.md -> https://etcdot.github.io/my-new-post.html
```

## 2. 文章格式

每篇文章开头都要有一段信息，叫 front matter：

```md
---
title: 我的第一篇新文章
date: 2026-05-01
tags: [生活, 记录]
description: 这是一篇文章摘要，会显示在首页、文章列表和搜索结果里。
featured: true
---

# 我的第一篇新文章

这里开始写正文。

## 小标题

- 可以写列表
- 可以写链接
- 可以写代码
```

字段说明：

- `title`：文章标题
- `date`：发布日期，格式固定为 `年-月-日`，比如 `2026-05-01`
- `tags`：标签，可以写多个，比如 `[AI, 学习路线]`
- `description`：文章摘要，会出现在首页和文章列表
- `featured`：是否放到首页「精选文章」，可写 `true`，也可以不写

## 3. 发布文章

如果你在电脑上操作，流程是：

```bash
python3 build.py --out .
git add .
git commit -m "Add new post"
git push
```

推送到 GitHub 后，GitHub Actions 会自动构建并发布网站。

如果你只是在 GitHub 网页上新增或修改 Markdown 文件，也可以直接提交。提交后 GitHub Actions 会自动发布，不一定要自己运行 `build.py`。

## 4. 修改已有文章

找到对应的 Markdown 文件，例如：

```text
content/posts/ai-learning.md
```

直接修改正文、标题、标签或摘要，然后提交即可。

不要手动改这些自动生成的页面：

```text
index.html
posts.html
tags.html
archives.html
script.js
*.html 文章页
```

这些文件会由 `build.py` 自动生成。

## 5. 修改网站名称和个人简介

修改这个文件：

```text
content/site.json
```

常用字段：

```json
{
  "title": "我是小萌萌",
  "description": "一名热爱技术、阅读与思考的开发者。",
  "author": "我是小萌萌",
  "year": "2026",
  "github": "https://github.com/EtcDot",
  "twitter": "https://twitter.com"
}
```

改完提交，网站会自动更新。

## 6. 本地预览

如果你在电脑上，可以先本地预览：

```bash
python3 build.py --out .
python3 -m http.server 8000
```

然后打开：

```text
http://localhost:8000
```

## 7. 推荐日常流程

最轻松的写作流程：

```text
打开 content/posts/
  ↓
复制一篇旧文章作为模板
  ↓
改文件名、标题、日期、标签、摘要
  ↓
写正文
  ↓
提交到 GitHub
  ↓
等待 GitHub Actions 自动发布
```

## 8. 常见问题

### 首页为什么没有出现我的文章？

检查文章开头是否有正确的 `date`、`title`、`description`。首页会优先显示 `featured: true` 的文章和最新文章。

### 标签页为什么没有更新？

标签页由 `tags` 自动生成。确认格式类似：

```md
tags: [AI, 学习路线]
```

### 搜索为什么搜不到？

搜索数据由 `script.js` 自动生成。提交 Markdown 后，等待 GitHub Actions 构建完成再刷新页面。

### 手机能不能写？

可以。你可以用 GitHub 手机网页编辑 `content/posts/*.md` 文件并提交。提交后会自动发布。
