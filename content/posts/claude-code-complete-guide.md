---
title: Claude Code 完全指南：119 页官方文档的精华浓缩
date: 2026-05-05
tags: [Claude Code, AI 编程, 开发工具, 教程]
description: 花了一个晚上把 Claude Code 119 页中文官方文档全部翻了一遍，去重提炼成这份实操指南。从安装配置到企业部署，从 subagent 到 Agent SDK，该有的都有了。
featured: true
---

# Claude Code 完全指南：119 页官方文档的精华浓缩

> Claude Code 是 Anthropic 推出的代理编码工具，可以读取你的代码库、编辑文件、运行命令、与你的开发工具集成。可在终端、IDE、桌面应用和浏览器中使用。
>
> 本文基于 code.claude.com/docs/zh-CN 全部 119 页官方文档综合整理，去重重组，保持高信息密度。

---

## 一、快速上手

### 安装

| 平台 | 命令 |
|------|------|
| macOS / Linux | `curl -fsSL https://claude.ai/install.sh | bash` |
| Homebrew | `brew install --cask claude-code` |
| WinGet | `winget install Anthropic.ClaudeCode` |
| PowerShell | `irm https://claude.ai/install.ps1 | iex` |

系统要求：macOS 13+ / Windows 10 1809+ / Ubuntu 20+，最少 4GB RAM。Windows 推荐 WSL2（支持沙箱），WSL1 无沙箱。

### 认证方式（优先级从高到低）

1. 第三方云提供商环境变量（Bedrock/Vertex/Foundry）
2. `ANTHROPIC_AUTH_TOKEN`（Bearer token）
3. `ANTHROPIC_API_KEY`（API 密钥，会覆盖订阅登录）
4. `apiKeyHelper` 脚本（动态轮换凭证）
5. 订阅 OAuth（交互式 `/login`）

> 注意：如果使用 Bedrock/Vertex/Foundry，**必须手动固定模型版本**（如 `ANTHROPIC_DEFAULT_OPUS_MODEL`），否则别名解析可能指向不可用的版本。

### 最常用的几条命令

```bash
claude                      # 启动交互式会话
claude "task description"   # 一次性任务
claude -p "query"           # 非交互模式，适合 CI/脚本
claude -c                   # 继续最近的对话
claude -r "session-name"    # 恢复指定会话
claude --worktree feature-x # 在隔离 git worktree 中启动
claude commit               # 帮你生成 Git commit
```

关键标志：`--output-format json`、`--system-prompt`、`--permission-mode auto`、`--model opus`、`--effort xhigh`、`--max-turns 50`。

---

## 二、理解核心概念

### 代理循环（Agentic Loop）

Claude Code 的工作方式可以概括为三个阶段的循环：

**收集上下文 → 采取行动 → 验证结果**

它会自动读取项目文件、运行 shell 命令、搜索网络，然后根据结果决定下一步做什么。你随时可以中断引导它。

内置的工具分为几类：

- **文件操作**：Read / Write / Edit / Glob（免权限）
- **代码搜索**：Grep / LSP 代码智能（需装插件）
- **命令执行**：Bash / PowerShell（需批准）
- **网络**：WebFetch / WebSearch（需批准）

有个细节需要注意：Bash 工具的每个命令都在独立进程中运行，`cd` 在主会话中会延续，但环境变量不会跨命令持久化。如果需要跨命令共享环境变量，要用 `CLAUDE_ENV_FILE` 或 SessionStart hook。

### 上下文窗口（Context Window）管理

这是用好 Claude Code 最关键的能力。每次启动会话，以下内容会自动加载进上下文：

| 内容 | 约多少 token |
|------|------------|
| 系统提示（System prompt） | ~4,200 |
| 自动记忆（MEMORY.md） | ~680 |
| 环境信息（目录、平台、git 状态） | ~280 |
| MCP 工具描述 | ~120（延迟加载） |
| Skill 描述 | ~450 |
| 用户级 CLAUDE.md | ~320 |
| 项目级 CLAUDE.md | ~1,800 |

上下文接近上限时，Claude Code 会自动压缩（compaction）。压缩后，CLAUDE.md 和自动记忆会重新注入，但带 `paths:` 限定的 rules 会丢失（直到匹配的文件再次被读取）。Skill 内容重新注入但上限 5K tokens/skill、总共不超过 25K。

**实操建议**：常看 `/context` 了解实时用量；任务切换时用 `/clear` 而不是硬塞；用 `/compact focus on ...` 指定压缩时保留的重点。

### 六种权限模式

通过 `Shift+Tab` 快速切换：

| 模式 | 行为 | 适合 |
|------|------|------|
| **default** | 读取不用问，写文件和跑命令要批准 | 默认推荐 |
| **acceptEdits** | 自动批准文件编辑和常见文件系统命令 | 迭代改代码 |
| **plan** | 只能读，不能写，用来做分析出计划 | 复杂修改前 |
| **auto** | 后台分类器自动安全检查 | 长时间任务 |
| **dontAsk** | 只允许预批准的操作，其他直接拒绝 | 锁定 CI |
| **bypassPermissions** | 跳过所有检查 | 仅隔离容器/VM |

`auto` 模式需要 Max/Team/Enterprise 计划，适合长时间运行减少提示疲劳。`bypassPermissions` 需要 `--dangerously-skip-permissions` 标志才能启用。

### 扩展生态一览

Claude Code 的扩展能力可以按"复杂程度"从低到高排列：

| 方式 | 作用 | 上下文成本 | 典型用途 |
|------|------|-----------|---------|
| **CLAUDE.md** | 每次会话加载的持久指令 | 每个请求 | 项目约定、编码规范 |
| **Rules** | 按文件路径条件加载的说明 | 仅匹配文件时 | 分目录规则 |
| **Skills** | 按需加载的知识/工作流 | 仅描述 | 参考文档、重复任务 |
| **MCP** | 连接外部工具/服务 | 每个请求 | 数据库、Slack、浏览器 |
| **Subagents** | 隔离上下文运行专门助手 | 不占主上下文 | 并行研究、代码审查 |
| **Agent Teams** | 多实例协调（实验性） | 高 | 多角度调试 |
| **Hooks** | 生命周期事件触发的脚本 | 零 | 格式化、通知、阻止 |
| **Plugins** | 打包上述功能的单元 | 取决于内含 | 分发和复用 |

**选择建议**：始终需要的放 CLAUDE.md（控制在 200 行以内）；偶尔才用的知识放 Skills；要隔离上下文的任务用 Subagents；需要确定性自动化用 Hooks。

---

## 三、配置你的环境

### 设置体系的四层作用域

Claude Code 的设置优先级从高到低：

**托管策略（Managed） > CLI 参数 > 本地覆盖（Local） > 项目共享（Project） > 用户全局（User）**

- **Managed**：Claude.ai 管理控制台或 MDM/注册表推送，用户无法覆盖
- **User**：`~/.claude/settings.json`，个人跨项目偏好
- **Project**：`.claude/settings.json`，提交到 git 给团队共享
- **Local**：`.claude/settings.local.json`，自动 gitignored

数组类型的配置会跨层级合并（连接+去重），标量值会被高层覆盖。运行 `/status` 可以看到当前生效的全部设置及来源。

### 模型配置

内置模型别名系统：

- `sonnet` / `opus` / `haiku` — 各自档位的最新版本
- `opusplan` — Plan Mode 用 Opus 推理，切到执行时自动切回 Sonnet
- `sonnet[1m]` / `opus[1m]` — 100 万上下文（Max/Team/Enterprise 包含）

Effort 级别控制思考深度：

| 模型 | 支持的级别 |
|------|-----------|
| Opus 4.7 | low / medium / high / **xhigh**（默认）/ max |
| Opus 4.6 / Sonnet 4.6 | low / medium / high / max |

`/effort` 调级别，v16 版本之后支持交互式滑块。

### 其他你可能想改的东西

- **快捷键**：`~/.claude/keybindings.json`，支持 20+ 上下文，改完立即生效
- **主题**：`/theme` 切换，内置色盲友好主题
- **全屏模式**（研究预览）：`/tui fullscreen` 消除闪烁，增加鼠标支持
- **语音输入**：`/voice` 切换，支持 20 种语言，会自动识别 `regex`、`OAuth` 这类技术术语
- **状态行**：自定义底部显示模型、成本、上下文使用率等信息

---

## 四、日常使用工作流

### 理解新代码库

从宽泛的问题开始——"这个项目是做什么的？架构怎么设计的？"——让 Claude 先浏览一遍，然后逐步缩小到特定领域。使用代码智能插件（LSP）可以获得"转到定义"和"查找引用"能力。

### 修复 Bug

分享完整的错误消息或堆栈跟踪，告诉 Claude 这个 Bug 是偶发的还是必现的。修复后让它自己验证。如果是运行时问题，可以用 Monitor 工具实时跟踪日志。

### Plan Mode 流程

1. 输入 `/plan` 进入只读模式
2. Claude 分析代码库，创建详细实施计划
3. `Ctrl+G` 在编辑器中打开计划直接修改
4. 退出 Plan Mode 开始执行

### 自动保存点（Checkpointing）

Claude Code 每次在编辑文件前都会自动创建快照（30 天后自动过期）。按两次 `Esc` 或输入 `/rewind` 会提供四种选择：

1. 同时恢复代码和对话
2. 只恢复对话（保留当前代码）
3. 只恢复代码（保留对话）
4. 从此处开始压缩（不等同于撤销）

需要注意的是：通过 Bash 命令（`sed -i`、`echo >` 等）做的修改不会被跟踪，只能回滚 Write/Edit 工具的修改。

### Git 工作流

- **自动提交**：`claude commit`
- **Worktree 隔离**：`claude -w feature-x` 创建隔离的 git worktree，防止并行会话互相干扰。`.worktreeinclude` 文件可以把 `.env` 这类 gitignored 文件自动复制过去。
- **PR 监控**：分支有 PR 时，页脚会显示彩色链接（绿=已批准，黄=待审查，红=请求更改）

---

## 五、各平台怎么选

| 平台 | 最大优势 | 注意事项 |
|------|---------|---------|
| **CLI** | 功能最完整，支持第三方提供商 | 纯终端 |
| **VS Code** | 编辑器内嵌，内联 diff，多对话标签 | 需要 VS Code 1.98+ |
| **JetBrains** | IDE 深度集成 | WSL 下要额外配网络 |
| **桌面版** | 并行会话、app 预览、Computer use | 需要付费订阅 |
| **网页版** | 云端运行，关浏览器也不停 | 只能连 GitHub 仓库 |

### Remote Control

在工位开始干活，躺沙发上用手机继续——`claude --remote-control` 开启服务模式，通过 claude.ai 或手机 App 连接。数据始终在本地执行，不会上传到云端。网络断开超过 10 分钟会自动超时。

### Computer Use（macOS 研究预览）

需要 Pro/Max 计划。Claude 可以打开 Mac 原生应用、点击 UI 元素、看屏幕截图。工具选择有优先级：**MCP Server > Bash > Chrome > 屏幕控制**。屏幕控制只用于前三个搞不定的场景。每次会话都要单独授权某个应用。

### CI/CD 集成

- **GitHub Actions**：在 PR/Issue 评论里写 `@claude` 就能触发。v1.0 GA，支持 Bedrock 和 Vertex AI。
- **GitLab CI/CD**（Beta）：事件驱动，自动把 Issue 变成 MR。需 `node:24-alpine3.21` 镜像。
- **Code Review**（研究预览）：多代理并行审查 diff，每次约 $15-25。可以用 `REVIEW.md` 自定义审查规则。
- **Slack**：在频道里 `@Claude` 委派编码任务，自动路由到云端会话。

---

## 六、扩展生态详解

### CLAUDE.md 和 Rules——记忆系统

CLAUDE.md 分四个层级：项目级（`./CLAUDE.md`）→ 用户级（`~/.claude/CLAUDE.md`）→ 本地级（`./CLAUDE.local.md`）→ 托管级（Enterprise）。

**编写原则**：控制在 200 行以内，指令要可验证（比如"用 2 空格缩进"而不是"好好格式化"）。`/init` 命令可以自动分析代码库生成初版 CLAUDE.md。如果想引用 README 或其他文件的内容，用 `@path/to/file` 语法。

**Rules**（`.claude/rules/*.md`）比 CLAUDE.md 更灵活——可以通过 frontmatter 的 `paths:` 字段限定只在处理某些路径下的文件时加载，节省上下文。支持符号链接跨项目共享。

**自动记忆**：Claude 会自己积累笔记，存在 `~/.claude/projects/<project>/memory/`，每个会话自动加载前 200 行或 25KB。纯 Markdown 格式，你可以手动编辑或删除。

### Skills——可重用工作流

Skills 是带 YAML frontmatter 的 SKILL.md 文件。放在 `~/.claude/skills/`（个人）或 `.claude/skills/`（项目）。通过 `/skill-name` 调用或让 Claude 自动触发。

几个实用的 frontmatter 字段：

- `description` — 决定 Claude 什么时候自动触发
- `disable-model-invocation: true` — 只有你能调用
- `allowed-tools: [Bash, Read, Write]` — 预批准的工具
- `context: fork` — 在 subagent 中运行（隔离上下文）

**动态上下文注入**（高级用法）：在 SKILL.md 里写 `` !`command` ``，执行前会先跑 shell 命令，把输出替换进去。适合动态获取当前 git 分支、时间戳等信息。

### Subagents——隔离上下文执行专门任务

Subagents 在自己的上下文窗口里工作，只把最终摘要返回给你。适合并行研究、代码审查、数据库查询等场景。

创建方式：在 `.claude/agents/` 下写 Markdown 文件，加上 YAML frontmatter：

```yaml
---
name: "reviewer"
description: "审查代码变更，检查潜在 Bug 和安全问题"
model: sonnet
permissionMode: plan
memory: project
---
```

关键配置项：`tools`（允许的工具）、`disallowedTools`（禁止的）、`permissionMode`、`background: true`（后台运行不阻塞）、`memory: project`（持久记忆跨会话）。

### Agent Teams（实验性）

需要设置 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`。与 Subagent 的区别：Subagent 单向汇报，不能互相通信；Team 的队友之间可以直接对话、共享任务列表、自我协调。适合需要多角色协作的场景。建议 3-5 个队友起步，token 消耗会线性增长。

### MCP——连接外部服务

MCP（Model Context Protocol）是把 Claude Code 连接到外部服务的标准方式。安装命令：

```bash
claude mcp add --transport http <name> <url>      # HTTP 远程
claude mcp add --transport stdio <name> -- <command> # 本地进程
```

分三个范围：local（仅当前项目你）、project（`.mcp.json` 共享给团队）、user（跨项目）。断线后自动指数退避重连，最多 5 次。

### Hooks——生命周期自动化

Hooks 是确定性脚本，在特定事件触发时自动执行。配置在 `settings.json` 的 `"hooks"` 键下。

**常用事件**（约 30 个）：

- `PreToolUse` — 在工具执行前拦截（return code 2 阻止操作）
- `PostToolUse` — 文件编辑后自动跑格式化
- `PermissionRequest` — 自动批准某些操作
- `Notification` — 发送桌面通知
- `SessionStart` / `SessionEnd` — 会话开始/结束
- `CwdChanged` — 目录切换时自动加载 direnv

**五种处理程序**：

1. `command` — 执行 shell 脚本（最常用）
2. `http` — POST 到 URL
3. `mcp_tool` — 调用 MCP 工具
4. `prompt` — 用 Haiku 做 LLM 评估
5. `agent` — 多轮 subagent 验证（实验性）

### Plugins——打包分享的扩展包

Plugin 可以把 Skills、Subagents、Hooks、MCP servers、LSP servers、Monitors、Themes 打包成可分享的单元。

最小结构：`.claude-plugin/plugin.json`（清单）+ 组件目录。

安装：`/plugin install <name>@<marketplace>`。官方市场 `claude-plugins-official` 自动可用。装完后 `/reload-plugins` 热加载，不用重启。

---

## 七、Agent SDK——把 Claude Code 当库用

Claude Agent SDK 让你在自己的 Python 或 TypeScript 程序里使用 Claude Code 的全部能力。

### 安装

```bash
# Python
pip install claude-agent-sdk

# TypeScript
npm install @anthropic-ai/claude-agent-sdk
```

### 核心用法

```python
from claude_agent_sdk import query

result = await query(
    systemPrompt="你是代码审查助手，检查代码质量",
    allowedTools=["Read", "Grep", "Glob"],
    permissionMode="acceptEdits",
)
```

核心函数 `query()` 返回异步迭代器，支持两种输入模式：
- **流式模式**（推荐）：持久化交互，支持图片、hooks、多轮对话
- **单条模式**：一次性查询，适合 Lambda/CI

### Hooks（编程式）

```python
async def pre_tool_hook(tool_name, tool_input, context):
    if tool_name == "Bash" and "rm -rf" in tool_input.get("command", ""):
        return {"permissionDecision": "deny"}
    return {}
```

编程式 Hooks 是进程内回调，比文件系统 Hooks 更灵活。支持 `PreToolUse`、`PostToolUse`、`Stop` 等 20+ 事件。

### 自定义工具

通过 SDK 内置的 in-process MCP server 可以定义你自己的函数工具。四要素：Name、Description、Input Schema（Zod/Pydantic）、Handler。工具名格式 `mcp__{server}__{tool}`，需要在 `allowedTools` 里放行。

### 结构化输出

```typescript
const result = await query({
  outputFormat: {
    type: "json_schema",
    schema: {
      type: "object",
      properties: {
        bugs: { type: "array", items: { type: "string" } },
        score: { type: "number" }
      }
    }
  }
});
```

Agent 完成多轮工具调用后，会返回通过 schema 验证的 JSON。

### 部署模式

| 模式 | 场景 |
|------|------|
| 临时会话 | 每次任务新建容器，用完销毁 |
| 长运行会话 | 持久容器跑多个 Agent 进程 |
| 混合会话 | 临时容器 + 状态恢复 |
| 单容器多进程 | 一个容器跑多个 SDK 进程（注意防互覆盖） |

隔离级别从低到高：Sandbox runtime > Docker > gVisor > Firecracker VM。

---

## 八、企业部署要点

### 部署决策流程

1. **选提供商**：Teams/Enterprise（推荐）> Console API > Bedrock > Vertex > Foundry
2. **设置分发**：Server-managed（Claude.ai 控制台）> MDM/plist/注册表 > 文件
3. **强制执行**：权限规则 + 沙箱 + MCP/插件限制 + Hook 限制 + 最低版本
4. **可见性**：OpenTelemetry（通用） / Analytics Dashboard（仅 Anthropic）
5. **数据处理**：商业计划不训练模型。ZDR（零数据保留）仅 Enterprise，需联系账户团队。

### 成本优化十大策略

1. **主动管理上下文**——`/clear` 切换任务，`/compact` 自定义总结
2. **选对模型**——复杂题目用 Opus，日常用 Sonnet，简单子任务用 Haiku
3. **减少 MCP 开销**——优先用 gh/aws 这些 CLI 工具，关掉不用的 MCP servers
4. **装代码智能插件**——LSP 精确导航代替 grep + 多文件读取
5. **Hooks 预处理**——过滤日志只返回错误行
6. **知识搬出 CLAUDE.md**——放 Skill 里按需加载，别让它每次都膨胀上下文
7. **调低 Effort**——不需要深度推理时用 medium 甚至 low
8. **Subagents 处理高量操作**——冗长输出关在子上下文里
9. **提示写具体**——减少 Claude 做广泛扫描的 token
10. **先 Plan 后做**——少走弯路就是省钱

按 Anthropic 公布的数据，每个开发者每天约 $13，每月 $150-250，90% 的用户每天不到 $30。

### 常见问题速查

| 症状 | 怎么办 |
|------|--------|
| 高 CPU/内存 | 定期 `/compact`，大目录加 `.gitignore` |
| 自动压缩反复触发 | 小块读文件、subagent 处理大文件 |
| 命令卡死了 | Ctrl+C 取消，`claude --resume` 恢复 |
| 搜索不出东西 | 缺 ripgrep；WSL 文件放 `/home/` 下 |
| 403/认证错 | `/login` 重登；`/status` 看当前凭证 |
| 插件不生效 | `/reload-plugins`；检查 `allowedTools` 放行 |

运行 `/doctor` 可以做一站式诊断。

---

## 九、最近更新速览（W13-W17）

| 周 | 亮点 |
|----|------|
| W17 | `/ultrareview` 公开研究预览、会话摘要、自定义主题、网页版重设计 |
| W16 | Opus 4.7（新增 xhigh 级别）、Routines 网页版、`/usage` 分解、原生二进制 |
| W15 | Ultraplan 云计划、Monitor 工具、`/loop` 自动调速、`/autofix-pr` |
| W14 | Computer Use 进入 CLI、`/powerup` 课程、无闪烁渲染 |
| W13 | Auto Mode 研究预览、PowerShell 工具、条件 hooks |

---

## 附：常用术语

| 术语 | 说明 |
|------|------|
| Agentic Loop | 收集→行动→验证的循环 |
| Compaction | 上下文窗口满时的自动压缩 |
| Effort | 思考深度（low → max） |
| Auto mode | 后台分类器替你做权限批准 |
| Worktree isolation | `-w` 参数在隔离 worktree 中运行 |
| Bare mode | `--bare` 跳过所有自动发现，最快启动 |
| Teleport | 把云端会话拉到本地终端 |
| Bundled skills | 内置的 `/batch`、`/simplify`、`/debug` 等工作流 |

---

*本文基于 code.claude.com/docs/zh-CN 全部 119 页官方文档综合整理。数据收集由 3 个并行 subagent 流水线完成，主 agent 去重重组后输出。*
