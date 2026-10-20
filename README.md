# my-relay

RackNerd VPS 上的 New API 中转站部署仓库。

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

## 约定（必须遵守）

1. 每次改动完成后，必须创建一个对应的 Git commit。
2. 每次改动后，必须编写或更新相关测试，并在交付前确保全部测试通过。
3. 任何密钥、密码、私钥、UUID 一律不写入仓库；用 `.env` 或服务器本地文件。
4. 本仓库不得删除。

详细约定见 [my-relay.md](my-relay.md)。