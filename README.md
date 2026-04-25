# 我是小萌萌

一个轻量的个人静态博客，使用 Markdown 管理文章，通过 `build.py` 生成静态页面，并由 GitHub Actions 自动发布到 GitHub Pages。

线上地址：

```text
https://etcdot.github.io/
```

## 内容管理

文章源文件放在：

```text
content/posts/
```

每篇文章是一个 Markdown 文件，例如：

```text
content/posts/ai-learning.md
```

文章开头需要包含：

```md
---
title: 文章标题
date: 2026-05-01
tags: [AI, 学习]
description: 文章摘要
featured: true
---
```

## 本地构建

```bash
python3 build.py --out .
```

## 本地预览

```bash
python3 -m http.server 8000
```

然后打开：

```text
http://localhost:8000
```

## 自动发布

推送到 `main` 分支后，GitHub Actions 会运行：

```bash
python build.py --out _site
```

然后把 `_site` 发布到 GitHub Pages。

## 文档

- 用户文档：`docs/USER_GUIDE.md`
- 运维文档：`docs/OPS_GUIDE.md`
