---
name: media-saber-subscribe-assistant
description: 通过 Media Saber MCP 处理端到端订阅工作流，包括 tmdb 搜索、精确订阅操作和刷新。
---

# Media Saber 订阅助手

当用户想要通过 Media Saber MCP 订阅电影或电视剧时使用此技能。

## ⚠️ 必须配置：MCP 服务连接

在使用此技能前，**您必须配置以下信息**：

### 1. MCP 地址配置（需要用户填写）

- **transport**: `streamable-http`
- **endpoint**: `<MCP_ENDPOINT_URL>` （例如：http://localhost:22698/message 或你的其他部署地址）
- **需要用户填写实际的 MCP 服务地址**

### 2. 认证信息配置（需要用户填写）

**请在以下位置之一配置您的 API_KEY**：

#### 方式 A：OpenClaw 配置（推荐）

在 `~/.claw/mcpServers.json` 中配置 Media Saber 连接：

```json
{
  "mcpServers": {
    "MediaSaber": {
      "transport": "streamable-http",
      "url": "http://localhost:22698/message",
      "headers": {
        "Authorization": "Bearer sk-YOUR_API_KEY_HERE"
      }
    }
  }
}
```

**替换 `sk-YOUR_API_KEY_HERE` 为您的实际 API 密钥**

#### 方式 B：环境变量配置

- 设置环境变量：`MEDIA_SABER_API_KEY=sk-your-api-key`
- 该密钥将被自动注入到请求头中

### 3. 获取 API_KEY

请从 Media Saber 系统获取您的 API 密钥：
- 访问 Media Saber Web 界面
- 进入 "设置" → "API 密钥"
- 复制您的密钥（通常以 `sk-` 开头）

**安全提示**：
- ⚠️ **切勿将 API_KEY 硬编码在代码、提示词或文档中**
- ⚠️ **切勿通过不安全的通道传输 API_KEY**
- ⚠️ **定期轮换您的 API_KEY**
- ⚠️ **不要与他人共享您的 API_KEY**

## 主要工具

- search_tmdb(query, mediaType)
- subscribe_movie(tmdbId)
- subscribe_tv(tmdbId, season, beginEpisode?, episodes?)
- refresh_subscribe()
- get_media_status(tmdbId, mediaType)
- get_miss_episodes()

## 工作流

1. 使用 search_tmdb 查找候选内容。
2. 当存在多个候选项时，要求用户确认确切目标。
3. 使用严格的参数调用 subscribe_movie 或 subscribe_tv。
4. 立即调用 refresh_subscribe。
5. 使用 get_media_status 报告最终状态。

## 防护措施

- 不要猜测 tmdbId。
- 未经用户意图确认，不要订阅。
- 切勿暴露授权令牌。
