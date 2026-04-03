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
3. 使用 ClawHub CLI 发布到 ClawHub（自动检测所有skills并发布）
4. 在 GitHub 创建 Release 并上传 zip 包

## GitHub 配置（必需）

### 第1步：获取 ClawHub API Token

1. 登录 [clawhub.ai](https://clawhub.ai)
2. 进入账户个人设置 → **API Token** 或 **Settings**
3. 复制你的 API Token（长字符串）

### 第2步：配置 GitHub Secret

1. 进入仓库 → **Settings** → **Secrets and variables** → **Actions**
2. 点击 **New repository secret**
3. 添加以下 Secret：

| 密钥名 | 值 | 说明 |
|------|-----|------|
| `CLAWHUB_TOKEN` | 从 clawhub.ai 复制的 Token | **必需** - 用于认证发布 |
| `CLAWHUB_REGISTRY` | https://clawhub.ai/api | 可选 - 如需自定义注册中心 |

### 第3步：配置 skill.json（重要）

每个技能文件夹的 `skill.json` 中必须包含以下字段：

| 字段 | 说明 | 示例 |
|------|------|------|
| `id` | Slug - 技能的唯一标识 | `media-saber-mcp` |
| `name` | Display Name - 显示名称 | `Media Saber MCP` |
| `version` | 语义化版本号 | `1.0.0` |
| `author` | 作者/所有者 | `Media Saber` |
| `description` | 技能描述 | `用于通过 MCP 控制 Media Saber` |
| `tags` | 标签数组 | `["mcp", "media-saber"]` |

**示例（skill.json）：**

```json
{
  "schema_version": "1.0",
  "id": "media-saber-mcp",
  "name": "Media Saber MCP",
  "version": "1.0.0",
  "author": "Media Saber",
  "license": "MIT",
  "description": "用于通过 MCP 控制 Media Saber 的技能",
  "entry": "SKILL.md",
  "tags": ["mcp", "media-saber"]
}
```

### 第4步：触发发布

**自动发布（推荐）**

创建并推送版本标签：

```powershell
git tag v1.0.0
git push origin v1.0.0
```

> 标签中的版本号会被识别并用于发布（v1.0.0 会匹配 skill.json 中的 version: "1.0.0"）

**手动发布**

1. 进入仓库 → **Actions**
2. 选择 **发布技能包到ClawHub和GitHub**
3. 点击 **Run workflow**

## 手动发布（本地测试）

### 1. 安装 ClawHub CLI

```powershell
npm install -g clawhub
```

### 2. 认证

```powershell
clawhub login --token <your-api-token> --no-browser
```

### 3. 发布

```powershell
# 自动扫描并发布所有 skills
clawhub sync --all

# 或发布单个 skill
clawhub skill publish ./media-saber-mcp --version 1.0.0 --tags latest
```

### 4. 查看结果

发布成功后可以在 [clawhub.ai](https://clawhub.ai) 上搜索你的技能

## OpenClaw 导入

使用以下文件之一：

- `media-saber-mcp/examples/openclaw.mcpServers.json`
- `media-saber-mcp/examples/claw-compatible.mcpServers.json`
