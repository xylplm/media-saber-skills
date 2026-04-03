---
name: media-saber-mcp
description: Media Saber 完整MCP工具集（28个工具）用于订阅、站点操作、推荐、云任务和系统检查。已针对OpenClaw和兼容客户端优化。
---

# Media Saber MCP 技能

这是 Media Saber MCP 的基础完整能力技能。

## 验证的连接配置

默认使用此配置：

- type/transport: streamable-http
- url: http://localhost:22698/message
- headers.Authorization: Bearer <API_KEY>

## 该技能可以做什么

- 搜索和检查 TMDB 媒体数据。
- 使用结构化参数订阅电影和电视内容。
- 刷新订阅并检查缺失的剧集。
- 运行站点签到、同步数据/通知/消息和诊断。
- 触发磁力/ed2k 和115转移链接的云任务。
- 查询媒体服务器并运行库同步。
- 运行系统网络和极空间检查。

## 工具契约规则

- 仅使用服务器公开的工具名称。
- 精确执行必需的参数。
- 对于推荐工具中的枚举式过滤器，仅传递允许的值。
- 将无参数工具视为无参数调用。

## 建议的默认工作流

**订阅工作流**:

1. search_tmdb(query, mediaType)
2. 用户确认候选项
3. subscribe_movie 或 subscribe_tv
4. refresh_subscribe
5. get_media_status

**站点操作工作流**:

1. get_sites/get_site_data
2. site_sign_in
3. sync_site_data/sync_site_notice/sync_site_message
4. today_site_data/total_site_data
5. 如需要运行 test_site/test_site_rss

**推荐工作流**:

1. 选择 recommend_movies 或 recommend_tvs
2. 应用过滤器（country/sort/tag/year）
3. 用 get_tmdb_info 补充热门选择

**云任务工作流**:

1. 验证链接类型
2. add_offline_download 或 cloud_share_receive
3. 清晰返回任务响应

## 安全规则

- 切勿打印API密钥或授权值。
- 在日志和示例中屏蔽敏感令牌。
- 当用户意图不清楚时，为有写入影响的操作请求确认。

## 配套技能

对于聚焦场景，还可使用：

- media-saber-subscribe-assistant
- media-saber-site-ops
- media-saber-recommend-helper
- media-saber-cloud-assistant

详细参数和示例见: docs/tool-reference.md
