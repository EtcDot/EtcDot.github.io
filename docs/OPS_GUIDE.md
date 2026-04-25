# 运维文档：Markdown 静态博客发布流程

本文档面向维护者，说明博客的目录结构、构建流程、GitHub Pages 部署方式和故障处理方法。

## 1. 架构概览

当前博客是纯静态网站，不依赖数据库和后端服务。

```text
content/posts/*.md
  ↓
build.py
  ↓
生成 HTML、标签页、归档页、搜索数据
  ↓
GitHub Actions
  ↓
GitHub Pages
  ↓
https://etcdot.github.io/
```

## 2. 关键目录和文件

```text
content/site.json              网站基础配置
content/posts/*.md             Markdown 文章源文件
build.py                       静态网站生成脚本
.github/workflows/deploy.yml   GitHub Actions 自动部署配置
docs/USER_GUIDE.md             用户写作说明
docs/OPS_GUIDE.md              运维说明
styles.css                     站点样式
about.html                     关于页，目前仍是静态页面
search.html                    搜索页壳子
```

自动生成的文件包括：

```text
index.html
posts.html
tags.html
archives.html
script.js
*.html 文章详情页
.nojekyll
```

维护原则：优先修改 `content/` 和 `styles.css`，不要手写自动生成页。

## 3. 本地构建

在仓库根目录执行：

```bash
python3 build.py --out .
```

构建成功后会看到类似输出：

```text
Built 10 posts into /path/to/repo
```

## 4. 本地预览

```bash
python3 -m http.server 8000
```

浏览器打开：

```text
http://localhost:8000
```

如果是在远程机器运行，`localhost` 只代表远程机器本身，手机无法直接访问。手机查看请使用线上地址。

## 5. GitHub Actions 部署

工作流文件：

```text
.github/workflows/deploy.yml
```

触发方式：

- 推送到 `main` 分支自动触发
- GitHub 页面手动点击 `workflow_dispatch` 触发

工作流步骤：

1. 拉取仓库
2. 安装 Python
3. 执行 `python build.py --out _site`
4. 上传 `_site` 为 Pages artifact
5. 使用 `actions/deploy-pages` 发布到 GitHub Pages

## 6. GitHub Pages 设置

仓库：

```text
EtcDot/EtcDot.github.io
```

推荐 Pages 来源：

```text
GitHub Actions
```

如果仍然是 `Deploy from branch`，也可以访问，因为仓库根目录保留了构建后的 HTML。但长期建议使用 GitHub Actions 作为 Pages 来源。

可用 GitHub CLI 检查：

```bash
gh api repos/EtcDot/EtcDot.github.io/pages --jq '{status:.status, html_url:.html_url, build_type:.build_type}'
```

## 7. 手动发布流程

```bash
python3 build.py --out .
git status --short
git add .
git commit -m "Update blog content"
git push
```

推送后检查 Actions 或 Pages 状态。

## 8. 线上验证

```bash
python3 - <<'PY'
import urllib.request
for url in ['https://etcdot.github.io/', 'https://etcdot.github.io/posts.html']:
    with urllib.request.urlopen(url, timeout=20) as r:
        print(url, r.status, r.headers.get('content-type'))
PY
```

检查某篇文章是否存在：

```bash
python3 - <<'PY'
import urllib.request
url = 'https://etcdot.github.io/ai-learning.html'
with urllib.request.urlopen(url, timeout=20) as r:
    body = r.read().decode('utf-8', errors='ignore')
print(r.status, 'AI 学习路线：从会用到会做' in body)
PY
```

## 9. Markdown front matter 规范

每篇文章必须包含：

```md
---
title: 文章标题
date: 2026-05-01
tags: [标签1, 标签2]
description: 文章摘要
featured: true
---
```

必填：

- `title`
- `date`
- `description`

可选：

- `tags`
- `featured`

`build.py` 没有依赖第三方 Markdown 库，只支持常用 Markdown：

- `#`、`##`、`###` 标题
- 段落
- `-` 无序列表
- 反引号代码
- Markdown 链接
- 粗体
- fenced code block

如果以后需要表格、图片、引用等复杂语法，可以扩展 `markdown_to_html()`，或改为引入 Python Markdown 库。

## 10. 常见故障

### Actions 成功但页面没变

可能是浏览器缓存。先强制刷新，或等待 1 到 3 分钟。

### Actions 报 Pages 权限错误

检查 workflow 权限是否包含：

```yaml
permissions:
  contents: read
  pages: write
  id-token: write
```

并确认仓库 Pages 来源设置为 GitHub Actions。

### `git push` 认证失败

如果本机使用 GitHub CLI 登录过，但 Git 推送仍失败，执行：

```bash
gh auth setup-git --hostname github.com
```

不要让用户提供 GitHub 密码。使用 GitHub 官方登录、设备码或已有本地凭据。

### 新文章构建失败

通常是 front matter 格式错误。重点检查：

- 开头和结尾是否都有 `---`
- `date` 是否是 `YYYY-MM-DD`
- `tags` 是否是 `[AI, 学习路线]` 这种格式
- `title`、`description` 是否为空

## 11. 后续可升级方向

- 把 `about.html` 也改成 Markdown 生成
- 增加 RSS feed
- 增加 sitemap.xml
- 增加图片目录 `assets/`
- 增加 Decap CMS 后台
- 增加 GitHub Actions 自动检查死链
