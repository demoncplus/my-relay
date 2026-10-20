# 从零恢复部署

以下步骤在全新 Ubuntu VPS 上恢复中转站。所有命令以具备 sudo 权限的用户执行。

## 1. 基础环境

```bash
sudo apt update && sudo apt install -y docker.io docker-compose-plugin nginx certbot python3-certbot-nginx curl
sudo systemctl enable --now docker nginx
```

## 2. 部署 New API

```bash
sudo mkdir -p /opt/new-api && cd /opt/new-api
sudo cp <仓库>/deploy/compose.yaml .
sudo cp <仓库>/.env.example .env
sudo nano .env                     # 填写 POSTGRES_PASSWORD、SESSION_SECRET
sudo docker compose up -d
```

等待 healthy：

```bash
sudo docker compose ps
curl -s http://127.0.0.1:3000/api/status | head -c 200
```

## 3. 初始化管理员（仅首次）

```bash
sudo tee /opt/new-api/admin.json >/dev/null <<'EOF'
{"username":"admin","password":"<强密码>"}
EOF
sudo chmod 600 /opt/new-api/admin.json
sudo python3 <仓库>/deploy/init.py
# 输出 NEW_API_INITIALIZED 即成功，随后删除 admin.json
sudo rm -f /opt/new-api/admin.json
```

## 4. Nginx + TLS

```bash
sudo cp <仓库>/deploy/nginx/new-api.conf /etc/nginx/sites-available/new-api
sudo ln -sf /etc/nginx/sites-available/new-api /etc/nginx/sites-enabled/new-api
sudo nginx -t && sudo systemctl reload nginx
sudo certbot --nginx -d <你的域名>
```

`/usage/` 需要 8765 端口有服务，见下一步；无则先注释该 location。

## 5. 余量查询页

```bash
sudo mkdir -p /opt/wg-usage-app
sudo cp <仓库>/scripts/usage_app.py /opt/wg-usage-app/app.py
sudo tee /opt/wg-usage-app/codes.conf >/dev/null <<'EOF'
# 名字=访问码，每行一个
friend1=XXXX-XXXX
EOF
sudo cp <仓库>/systemd/wg-usage-app.service /etc/systemd/system/
sudo systemctl daemon-reload && sudo systemctl enable --now wg-usage-app
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8765/usage/
```

## 6. 配额与 VPN 脚本

```bash
sudo cp <仓库>/scripts/*.sh /usr/local/bin/ && sudo chmod 755 /usr/local/bin/*.sh
sudo cp <仓库>/scripts/reality_manager.py /usr/local/bin/ && sudo chmod 700 /usr/local/bin/reality_manager.py
sudo cp <仓库>/systemd/*.service /etc/systemd/system/
sudo systemctl daemon-reload
```

VPN 配置（WireGuard `wg0`、Xray REALITY）含私钥，按服务器本地文件维护，不入库。

## 7. 验收

```bash
bash tests/relay_healthcheck.sh
```

全部 PASS 即恢复完成。

## 已知限制

- 配额统计按 5 秒轮询，允许轻微超额
- 触发限额时会重启 Xray（VLESS 用户短暂重连），不影响 WireGuard 与 New API
- 服务器崩溃可能丢失最后几秒的计费