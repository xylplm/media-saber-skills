---
name: media-saber-recommend-helper
description: 通过 Media Saber MCP 生成带有结构化过滤器和可解释选择的电影和电视推荐。
---

# Media Saber 推荐助手

在推荐场景中使用此技能。

## 需要的 MCP 连接

- transport: streamable-http
- endpoint: http://localhost:22698/message
- header: Authorization: Bearer <API_KEY>

## 主要工具

- recommend_movies(country?, sort?, tag?, year?)
- recommend_tvs(country?, sort?, tag?, year?)
- get_tmdb_info(tmdbId, mediaType)

## 推荐策略

1. 向用户询问媒体类型和偏好维度。
2. 将偏好转换为工具过滤器。
3. 调用 recommend_movies 或 recommend_tvs。
4. 使用 get_tmdb_info 补充热门选择。
5. 返回简明的候选列表并说明理由。

## 防护措施

- 将过滤值保持在服务器允许的枚举集内。
- 如果用户给出不支持的值，映射到空值（全部）并解释。
- 切勿暴露授权令牌。
