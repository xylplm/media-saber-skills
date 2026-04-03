# media-saber-skills

Media Saber 标准技能项目。

本项目用于：

- 技能包开发
- CI 验证和构建
- GitHub Actions 自动发布到 ClawHub

## 项目结构

- `media-saber-mcp/`: 单个技能包（包含 `SKILL.md` 和 `skill.json`）
- `scripts/validate_skills.py`: 技能结构和元数据验证
- `build_skill.py`: 一键打包工具
- `scripts/publish_to_clawhub.py`: 上传 zip 包到 ClawHub
- `.github/workflows/ci.yml`: PR/主分支验证和构建
- `.github/workflows/publish-clawhub.yml`: 标签/手动自动发布

## Included skills

- `media-saber-mcp`: 完整MCP能力技能（28个工具）
- `media-saber-subscribe-assistant`: 订阅工作流技能
- `media-saber-site-ops`: 站点签到/同步/诊断技能
- `media-saber-recommend-helper`: 电影/电视推荐技能
- `media-saber-cloud-assistant`: 云盘传输和离线下载技能
- `media-saber-zspace-monitor`: 极空间NAS系统监控和硬件健康检查技能

## 构建

要求：

- Python 3.9+

构建所有技能：

```powershell
cd d:\myGithub\media-saber-skills
python .\build_skill.py
```

构建单个技能：

```powershell
python .\build_skill.py --skill media-saber-mcp
```

构建时指定版本：

```powershell
python .\build_skill.py --skill media-saber-mcp --version 1.0.1
```

输出：

- Zip 文件写入 `dist/` 目录
- 脚本会为每个包输出 `sha256` 哈希值

## GitHub Actions

### CI 工作流

触发条件：

- `pull_request`
- 推送到 `main`

流程：

1. 验证技能结构和元数据
2. 构建 zip 包
3. 上传 `dist/*.zip` 作为制品

### 发布工作流（ClawHub）

触发条件：

- 推送标签如 `v1.0.0`
- 手动运行（`workflow_dispatch`）

流程：

1. 验证技能
2. 构建包
3. 将 `dist/` 中的每个 zip 发布到 ClawHub

必需的仓库密钥：

- `CLAWHUB_UPLOAD_URL`: 上传 API 端点
- `CLAWHUB_TOKEN`: 发布令牌

可选的仓库密钥：

- `CLAWHUB_TOKEN_HEADER`: 默认 `Authorization`
- `CLAWHUB_TOKEN_PREFIX`: 默认 `Bearer`
- `CLAWHUB_FILE_FIELD`: 默认 `file`
- `CLAWHUB_TIMEOUT_SECONDS`: 默认 `60`

## 手动发布（可选）

```powershell
python .\scripts\publish_to_clawhub.py
```

环境变量与 GitHub Action 密钥相同。

## OpenClaw 导入

使用以下文件之一：

- `media-saber-mcp/examples/openclaw.mcpServers.json`
- `media-saber-mcp/examples/claw-compatible.mcpServers.json`
