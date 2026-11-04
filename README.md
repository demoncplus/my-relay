# my-relay

RackNerd VPS 上的 New API 中转站部署仓库。

> 本仓库同时包含译词通（TransWord）的隔离翻译引擎与生词本同步反向代理配置。相关服务只使用 `/transword-engine/`、`/transword-sync/` 两个独立路径，不改变 New API 根路径、VPN、订阅和余量查询服务。

> **此仓库永久保留，不得删除。** 所有中转站的部署文件、运维脚本、变更记录都以本仓库为准。

## 服务器

| 项 | 值 |
|---|---|
| VPS | RackNerd，`107.175.122.81` |
| 系统 | Ubuntu，3 vCPU / 4 GB RAM |
| 对外域名 | `https://107-175-122-81.sslip.io`（Let's Encrypt 证书） |
| SSH | 仅 8443 端口，用户 `deploy`（密钥登录） |
| 时区 | Asia/Shanghai |

## 组件

| 组件 | 说明 |
|---|---|
| New API | 中转站主体，容器 `calciumion/new-api`，监听 `127.0.0.1:3000` |
| PostgreSQL 15 | New API 数据库，容器内网 |
| Redis 7 | 缓存与会话 |
| Nginx | TLS 终止，反代 `/` → 3000，`/usage/` → 8765，`/sub/`、`/wg/` 静态下发 |
| usage_app.py | 流量余量查询页（登录制，`127.0.0.1:8765`） |
| Xray REALITY / WireGuard | 配套 VPN 服务（脚本在 `scripts/`、`systemd/`） |

## 目录结构

```
my-relay/
├── my-relay.md            # 强制约定（改动必须 commit + 必须过测试）
├── README.md              # 本文件
├── .env.example           # 环境变量模板（真实 .env 不入库）
├── deploy/
│   ├── compose.yaml       # New API + PostgreSQL + Redis
│   ├── init.py            # 首次初始化管理员
│   └── nginx/new-api.conf # Nginx 站点配置
├── scripts/               # 运维脚本（配额、用量页、REALITY 管理）
├── systemd/               # systemd 单元文件
├── tests/                 # 健康检查测试
└── docs/deploy.md         # 从零恢复部署的完整步骤
```

## 部署 / 恢复

见 [docs/deploy.md](docs/deploy.md)。

## 测试

```bash
bash tests/relay_healthcheck.sh
```

覆盖：中转站 API、余量页、Clash 订阅、WireGuard 下载链接。

- 2026-11-03: **修复 2053 备用入站**——reality_manager 此前只给 4001 填充用户，2053 备用直连口自 11/1 迁移起 clients 为空（fast-fail）；现改为填充所有 vless 入站，节点2（pc-stable-US）恢复独立可用。看门狗 v2.2 新增节点2每小时探测。

- 2026-11-03: **完整事件复盘** docs/incident-2026-10-31-hk-outage.md（香港中断3天 → 443应急迁移 → 2053修复 → 恢复回切，含经验教训6条）

- 2026-11-04: **新增荐福禅寺导览 AI 大脑服务**（`dafeiyu-brain.service`，监听 `0.0.0.0:18765`，ufw 已放行）。程序在 `/opt/dafeiyu-brain`（brain.py + 静态导览页 + Live2D 模型 + venv），弹幕经 bilibili-api 匿名连接（wbi 签名可过风控），回复走本机 New API（`http://127.0.0.1:3000/v1`，模型 `glm-4.5-air`，专用令牌 `dafeiyu-brain` 属 default 分组），语音用 edge-tts。不改 Nginx、不占 80/443，与中转站互不影响。端口 8765/8766/8787 已被既有服务占用，故用 18765。

## 约定（必须遵守）

1. 每次改动完成后，必须创建一个对应的 Git commit。
2. 每次改动后，必须编写或更新相关测试，并在交付前确保全部测试通过。
3. 任何密钥、密码、私钥、UUID 一律不写入仓库；用 `.env` 或服务器本地文件。
4. 本仓库不得删除。

详细约定见 [my-relay.md](my-relay.md)。