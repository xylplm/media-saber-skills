---
name: media-saber-site-ops
description: 通过 Media Saber MCP 进行站点操作，包括签到、数据同步、通知、消息和站点诊断。
---

# Media Saber 站点操作

通过 Media Saber MCP 使用此技能进行 PT 站点操作和诊断。

## 需要的 MCP 连接

- transport: streamable-http
- endpoint: http://localhost:22698/message
- header: Authorization: Bearer <API_KEY>

## 主要工具

- get_sites(name?)
- get_site_data(name?)
- get_site_notice(name?)
- get_site_message(name?)
- today_site_data()
- total_site_data()
- site_sign_in()
- sync_site_data()
- sync_site_notice()
- sync_site_message()
- test_site()
- test_site_rss()
- update_site_configs()

## 工作流

1. 首先使用 get_sites/get_site_data 读取当前状态。
2. 运行 site_sign_in 和必需的同步工具。
3. 使用 today_site_data 和 total_site_data 进行验证。
4. 如果发现问题，运行 test_site 和 test_site_rss。
5. 报告每个站点的结果和失败原因。

## 防护措施

- 优先选择读操作然后写操作。
- 批量操作应包括摘要输出。
- 切勿暴露授权令牌。
