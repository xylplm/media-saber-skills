---
name: media-saber-subscribe-assistant
description: 通过 Media Saber MCP 处理端到端订阅工作流，包括 tmdb 搜索、精确订阅操作和刷新。
---

# Media Saber 订阅助手

当用户想要通过 Media Saber MCP 订阅电影或电视剧时使用此技能。

## 需要的 MCP 连接

- transport: streamable-http
- endpoint: http://localhost:22698/message
- header: Authorization: Bearer <API_KEY>

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
