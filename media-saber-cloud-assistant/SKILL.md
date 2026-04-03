---
name: media-saber-cloud-assistant
description: 在 Media Saber MCP 中运行云存储和下载任务，包括 115 转移和磁力/ed2k 离线下载。
---

# Media Saber 云助手

为云任务操作使用此技能。

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

- add_offline_download(link)
- cloud_share_receive(link)
- test_network()

## 工作流

1. 验证链接类型：
   - add_offline_download: ed2k 或磁力链接
   - cloud_share_receive: 115 资源链接
2. 可选：在任务提交前运行 test_network。
3. 提交任务并返回服务器响应。
4. 如果失败，建议重试并检查链接格式。

## 防护措施

- 明确拒绝不支持的链接格式。
- 不要伪造任务 ID 或成功状态。
- 切勿暴露授权令牌。
