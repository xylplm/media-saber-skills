---
name: media-saber-cloud-assistant
description: 在 Media Saber MCP 中运行云存储和下载任务，包括 115 转移和磁力/ed2k 离线下载。
---

# Media Saber 云助手

为云任务操作使用此技能。

## 需要的 MCP 连接

- transport: streamable-http
- endpoint: http://localhost:22698/message
- header: Authorization: Bearer <API_KEY>

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
