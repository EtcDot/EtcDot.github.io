# 我是小萌萌

一个参考 AstroPaper 风格制作的静态个人博客模板，适合直接部署到 GitHub Pages。

## 文件

- `index.html`：首页，包含个人简介、精选文章、最新文章
- `posts.html`：文章列表
- `tags.html`：标签页
- `archives.html`：归档页
- `about.html`：关于我
- `search.html`：纯前端搜索示例
- `styles.css`：站点样式，支持响应式和暗色模式
- `script.js`：主题切换和搜索逻辑

## 本地预览

```bash
cd ~/projects/astro-paper-clone
python3 -m http.server 8000
```

然后访问：

```text
http://localhost:8000
```

## GitHub Pages 部署

把这些文件上传到 `你的用户名.github.io` 仓库根目录，然后在仓库 Settings -> Pages 里选择 `main` 分支和 `/root` 即可。
