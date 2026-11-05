# Nestbolt

[English](https://github.com/skulitom/Nestbolt/blob/main/README.md) · 简体中文 · [日本語](https://github.com/skulitom/Nestbolt/blob/main/README.ja.md)

> 本页是英文 README 开头部分的摘要翻译。如有出入，以[英文 README](https://github.com/skulitom/Nestbolt/blob/main/README.md) 为准。

Nestbolt 是免费、开源（MIT）的排样（套料）工具，面向在**固定尺寸板材**上切割的用户：激光切割机、CNC 雕刻机、等离子、水刀，以及布料和皮革。它会排布零件，让用料尽可能少。它可以[在浏览器中运行](https://skulitom.github.io/Nestbolt/)（不上传任何文件），也可以作为命令行工具，或作为供 AI 智能体调用的 MCP 服务器。

[打开浏览器版](https://skulitom.github.io/Nestbolt/) ·
[下载发布版本](https://github.com/skulitom/Nestbolt/releases) ·
[连接 AI 智能体](https://github.com/skulitom/Nestbolt/blob/main/docs/AGENT_INTERFACE.md)

## 对比结果

在冻结的 v1 基准测试中，在相同的 60 秒时间预算下，与每个任务上 Deepnest、SVGnest 和 Sparrow 三者中最好的结果相比，按中位数计 Nestbolt **少用 8.5% 的材料**；在 300 秒预算下少用 9.6%。这是最终基准运行的结果（使用新的随机种子，并包含十个未参与调参的任务）。在 60 秒预算下，Sparrow 仍在 56 个任务中的 8 个上胜出。

| 时间预算 | Nestbolt 有效排样数 | 比最佳竞品少用的材料（中位数） | 胜出或持平 |
| --- | ---: | ---: | ---: |
| 60 秒 | 375/375 | **8.5%** | 56 个中的 48 个 |
| 300 秒（长任务子集） | 60/60 | **9.6%** | 11 个中的 11 个 |

最终验收运行（2026-10-13）：75 个冻结的板材任务（35 个学术任务、40 个创客任务，其中十个从未参与调参），各工具时间预算相同、各用一个 CPU 核心、每个任务五个新的随机种子，每个排样结果都经过独立验证器检查。详细数据见[英文 README 的对比部分](https://github.com/skulitom/Nestbolt/blob/main/README.md#how-it-compares)和[全部结果](https://skulitom.github.io/Nestbolt/results/)。

## 示例

![451 个字母轮廓排在一张板材上，小字母放在大字母的孔洞里](docs/images/showcase.png)

在一个 CPU 核心上用 120 秒，把 451 个零件排在一张 850 × 425 mm 的板材上：四种尺寸的 DejaVu Sans Bold 字形，使用精确的贝塞尔轮廓、90° 旋转和 1 mm 间距。其中 29 个字母放在其他字母的孔洞里，剩余材料在顶部保留为一整块干净的余料。该排样已通过独立验证器检查。

## 版本

- **稳定版 v0.1.0** 仍可下载。托管的浏览器版运行来自 `main` 分支的预览构建，比 v0.2.0-alpha.1 更新。
- **[v0.2.0-alpha.1 预览版](https://github.com/skulitom/Nestbolt/releases/tag/v0.2.0-alpha.1)**：可编辑的 LightBurn 项目排样（**预览功能**）、引入线（lead-in）余量，以及对大型曲线图纸的改进。提供 Windows x64、Linux x64 和 macOS Apple 芯片版工具，以及 Windows MCP 包。导入验收和共边切割的用料仍在开发中；v1.1 计划已完成 60%。上面的基准数据属于冻结的 `75cbb32` 构建，该预览版没有与竞品做新的对比。

## 供 AI 智能体使用

MCP 服务器 `nestbolt-mcp` 有五个工具：`import_parts`、`nest`、`validate_layout`、`export_layout` 和 `estimate_sheets`。它不需要网络、账号或凭据，所有路径必须位于其工作区内，并且从不覆盖文件。`estimate_sheets` 只给出下限，不是排样结果。Nestbolt 不提供任何机器安全或适配认证。

在 Claude Code 中也可以安装插件（需先把 v0.1.0 发布包里的 `nestbolt-mcp` 放到 PATH 中）：

```text
/plugin marketplace add https://raw.githubusercontent.com/skulitom/Nestbolt/main/.claude-plugin/marketplace.json
/plugin install nestbolt@nestbolt
```

Claude Code 插件附带 `nestbolt` 技能。对于 Codex、Cursor、Kimi Code、OpenCode 以及开源 [skills CLI](https://skills.sh) 支持的其他智能体，可以用 `npx skills add skulitom/nestbolt-plugin` 安装同一个技能。这个小仓库里有同样的技能，所以 CLI 不必克隆本仓库（其中的基准测试结果约占 5 GB）。技能本身不会启动服务器，仍需另外注册 `nestbolt-mcp`（Kimi Code、OpenCode 和 DeepSeek Harness 见下文，Codex 等客户端见[智能体接口文档](https://github.com/skulitom/Nestbolt/blob/main/docs/AGENT_INTERFACE.md#connecting)）。技能自带的安装说明是按 Claude Code 写的；在其他智能体中，请按这里的方式注册服务器。skills CLI 需要 Node.js 22.20 或更高版本；除非设置了 `DISABLE_TELEMETRY=1` 或 `DO_NOT_TRACK=1`，它会把安装次数报告给 skills.sh 排行榜。

**Kimi Code、OpenCode 和 DeepSeek Harness。** 从 [v0.1.0 发布页](https://github.com/skulitom/Nestbolt/releases/tag/v0.1.0)下载对应平台的压缩包（可用 `SHA256SUMS` 校验），解压出 `nestbolt-mcp`，并填写它的绝对路径（Windows 上是 `nestbolt-mcp.exe`，可以使用正斜杠，例如 `C:/Tools/nestbolt-mcp.exe`）。请把 `NESTBOLT_WORKSPACE` 设为存放切割文件的文件夹，因为各客户端启动服务器时所在的文件夹并不相同。一次 `nest` 调用最长可运行 300 秒；Kimi Code 和 DeepSeek Harness 默认只等待工具 60 秒，所以下面的配置都允许 330 秒；OpenCode 的 `timeout` 同样适用于工具调用。

- **Kimi Code CLI：** 写入 `~/.kimi-code/mcp.json`（或受信任项目中的 `.kimi-code/mcp.json`），`/mcp` 会显示它：

  ```json
  {
    "mcpServers": {
      "nestbolt": {
        "command": "/absolute/path/to/nestbolt-mcp",
        "args": [],
        "env": { "NESTBOLT_WORKSPACE": "/absolute/path/to/your/cutting/files" },
        "toolTimeoutMs": 330000
      }
    }
  }
  ```

- **OpenCode：** 添加到 `opencode.json`（项目中的，或 `~/.config/opencode/opencode.json`）的 `mcp` 下，`opencode mcp list` 会显示已连接：

  ```json
  {
    "$schema": "https://opencode.ai/config.json",
    "mcp": {
      "nestbolt": {
        "type": "local",
        "command": ["/absolute/path/to/nestbolt-mcp"],
        "environment": { "NESTBOLT_WORKSPACE": "/absolute/path/to/your/cutting/files" },
        "timeout": 330000
      }
    }
  }
  ```

- **DeepSeek Harness：** 添加到 `~/.dsh/cordis.patch.yml`，工具会以 `mcp__nestbolt__nest` 这样的名称出现：

  ```yaml
  - insert:
      - id: mcp-nestbolt
        name: '@deepseek-ai/dsh-mcp-client'
        config:
          serverName: nestbolt
          transport: stdio
          command: /absolute/path/to/nestbolt-mcp
          args: []
          env:
            NESTBOLT_WORKSPACE: /absolute/path/to/your/cutting/files
          toolCallTimeoutMs: 330000
  ```

2026 年 11 月 5 日在 Windows 上用 v0.1.0 服务器检查过：OpenCode 1.19.5 显示已连接；Kimi Code 2.5.0 找到全部五个工具；DeepSeek Harness 0.2.1-rc.5 能正确解析这段配置；但 DeepSeek Harness 本身需要 DeepSeek 密钥才能启动，所以这次没有用它实际启动服务器。直接通过 stdio 从其他文件夹启动时，服务器只在 `NESTBOLT_WORKSPACE` 内读写文件。

详见[智能体接口文档](https://github.com/skulitom/Nestbolt/blob/main/docs/AGENT_INTERFACE.md)（英文）。

## 许可

Nestbolt 采用 [MIT](https://github.com/skulitom/Nestbolt/blob/main/LICENSE) 许可。jagua-rs 是未经修改的 MPL-2.0 依赖；`crates/core/src/separate.rs` 中的分离器改编自 Sparrow（MIT）。
