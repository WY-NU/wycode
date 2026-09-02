# WyCode

WyCode 是一个运行在终端中的 AI 编程助手，提供交互式界面、非交互式命令、工具调用、权限控制、多智能体协作、MCP 扩展和 Git Worktree 支持。

## 环境要求

- Python 3.11 或更高版本
- 可用的 OpenAI、Anthropic 或 OpenAI 兼容模型 API
- 推荐使用 [uv](https://docs.astral.sh/uv/) 管理 Python 环境和依赖

## 安装

克隆仓库：

```bash
git clone https://github.com/WY-NU/wycode.git
cd wycode
```

使用 `uv` 安装依赖：

```bash
uv sync
```

也可以使用 `pip` 以可编辑模式安装：

```bash
python -m venv .venv
```

Windows PowerShell：

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
```

macOS 或 Linux：

```bash
source .venv/bin/activate
python -m pip install -e .
```

## 配置

WyCode 按以下顺序读取并合并配置：

1. 用户配置：`~/.wycode/config.yaml`
2. 项目配置：`.wycode/config.yaml`
3. 项目本地配置：`.wycode/config.local.yaml`

至少需要配置一个模型提供商。以下是 OpenAI 配置示例：

```yaml
providers:
  - name: openai
    protocol: openai
    base_url: https://api.openai.com/v1
    model: gpt-4o

permission_mode: default
```

不要把 API Key 直接提交到配置文件。请通过环境变量设置：

Windows PowerShell：

```powershell
$env:OPENAI_API_KEY = "你的 API Key"
```

macOS 或 Linux：

```bash
export OPENAI_API_KEY="你的 API Key"
```

Anthropic 协议使用 `ANTHROPIC_API_KEY`。`openai-compat` 协议默认使用 `OPENAI_API_KEY`。

可用的 `protocol` 值：

- `openai`
- `anthropic`
- `openai-compat`

可用的 `permission_mode` 值：

- `default`：敏感操作请求确认
- `acceptEdits`：自动接受文件编辑
- `plan`：只进行分析和规划
- `bypassPermissions`：跳过权限确认，请谨慎使用

## 使用

使用 `uv` 启动交互式终端界面：

```bash
uv run wycode
```

如果已经通过 `pip` 安装：

```bash
wycode
```

### 单次提示

执行一次任务并把最终文本输出到终端：

```bash
uv run wycode -p "解释这个项目的目录结构"
```

### JSON 流输出

在非交互模式下输出 NDJSON 事件流，适合脚本或其他程序消费：

```bash
uv run wycode -p "检查当前项目" --output-format stream-json
```

### 指定权限模式

命令行参数会覆盖配置文件中的 `permission_mode`：

```bash
uv run wycode --mode plan
```

### 远程模式

启动 WebSocket 服务和浏览器界面：

```bash
uv run wycode --remote
```

服务默认监听 `0.0.0.0:18888`，本机可访问 `http://localhost:18888`。在不受信任的网络中使用前，请先做好网络隔离和访问控制。

### 查看交互命令

进入交互式界面后输入：

```text
/help
```

使用 `/help <命令名>` 可以查看单个命令的详细用法。

## 常见问题

### 提示找不到配置文件

请创建 `.wycode/config.yaml` 或 `~/.wycode/config.yaml`，并确保其中包含非空的 `providers` 列表。

### 提示缺少 API Key

确认当前终端已经设置与协议对应的环境变量。环境变量只对当前终端会话生效时，需要在同一个终端中启动 WyCode。

### `wycode` 命令不存在

使用 `uv run wycode`，或者确认已在当前虚拟环境中执行 `python -m pip install -e .`。

## 开源仓库

[github.com/WY-NU/wycode](https://github.com/WY-NU/wycode)
