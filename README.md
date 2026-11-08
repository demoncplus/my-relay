# my-relay

RackNerd VPS 涓婄殑 New API 涓浆绔欓儴缃蹭粨搴撱€?

> 鏈粨搴撳悓鏃跺寘鍚瘧璇嶉€氾紙TransWord锛夌殑闅旂缈昏瘧寮曟搸涓庣敓璇嶆湰鍚屾鍙嶅悜浠ｇ悊閰嶇疆銆傜浉鍏虫湇鍔″彧浣跨敤 `/transword-engine/`銆乣/transword-sync/` 涓や釜鐙珛璺緞锛屼笉鏀瑰彉 New API 鏍硅矾寰勩€乂PN銆佽闃呭拰浣欓噺鏌ヨ鏈嶅姟銆?

> **姝や粨搴撴案涔呬繚鐣欙紝涓嶅緱鍒犻櫎銆?* 鎵€鏈変腑杞珯鐨勯儴缃叉枃浠躲€佽繍缁磋剼鏈€佸彉鏇磋褰曢兘浠ユ湰浠撳簱涓哄噯銆?

## 鏈嶅姟鍣?

| 椤?| 鍊?|
|---|---|
| VPS | RackNerd锛宍107.175.122.81` |
| 绯荤粺 | Ubuntu锛? vCPU / 4 GB RAM |
| 瀵瑰鍩熷悕 | `https://107-175-122-81.sslip.io`锛圠et's Encrypt 璇佷功锛?|
| SSH | 浠?8443 绔彛锛岀敤鎴?`deploy`锛堝瘑閽ョ櫥褰曪級 |
| 鏃跺尯 | Asia/Shanghai |

## 缁勪欢

| 缁勪欢 | 璇存槑 |
|---|---|
| New API | 涓浆绔欎富浣擄紝瀹瑰櫒 `calciumion/new-api`锛岀洃鍚?`127.0.0.1:3000` |
| PostgreSQL 15 | New API 鏁版嵁搴擄紝瀹瑰櫒鍐呯綉 |
| Redis 7 | 缂撳瓨涓庝細璇?|
| Nginx | TLS 缁堟锛屽弽浠?`/` 鈫?3000锛宍/usage/` 鈫?8765锛宍/sub/`銆乣/wg/` 闈欐€佷笅鍙?|
| usage_app.py | 娴侀噺浣欓噺鏌ヨ椤碉紙鐧诲綍鍒讹紝`127.0.0.1:8765`锛?|
| Xray REALITY / WireGuard | 閰嶅 VPN 鏈嶅姟锛堣剼鏈湪 `scripts/`銆乣systemd/`锛?|

## 鐩綍缁撴瀯

```
my-relay/
鈹溾攢鈹€ my-relay.md            # 寮哄埗绾﹀畾锛堟敼鍔ㄥ繀椤?commit + 蹇呴』杩囨祴璇曪級
鈹溾攢鈹€ README.md              # 鏈枃浠?
鈹溾攢鈹€ .env.example           # 鐜鍙橀噺妯℃澘锛堢湡瀹?.env 涓嶅叆搴擄級
鈹溾攢鈹€ deploy/
鈹?  鈹溾攢鈹€ compose.yaml       # New API + PostgreSQL + Redis
鈹?  鈹溾攢鈹€ init.py            # 棣栨鍒濆鍖栫鐞嗗憳
鈹?  鈹斺攢鈹€ nginx/new-api.conf # Nginx 绔欑偣閰嶇疆
鈹溾攢鈹€ scripts/               # 杩愮淮鑴氭湰锛堥厤棰濄€佺敤閲忛〉銆丷EALITY 绠＄悊锛?
鈹溾攢鈹€ systemd/               # systemd 鍗曞厓鏂囦欢
鈹溾攢鈹€ tests/                 # 鍋ュ悍妫€鏌ユ祴璇?
鈹斺攢鈹€ docs/deploy.md         # 浠庨浂鎭㈠閮ㄧ讲鐨勫畬鏁存楠?
```

## 閮ㄧ讲 / 鎭㈠

瑙?[docs/deploy.md](docs/deploy.md)銆?

## 娴嬭瘯

```bash
bash tests/relay_healthcheck.sh
```

瑕嗙洊锛氫腑杞珯 API銆佷綑閲忛〉銆丆lash 璁㈤槄銆乄ireGuard 涓嬭浇閾炬帴銆?

- 2026-11-03: **淇 2053 澶囩敤鍏ョ珯**鈥斺€攔eality_manager 姝ゅ墠鍙粰 4001 濉厖鐢ㄦ埛锛?053 澶囩敤鐩磋繛鍙ｈ嚜 11/1 杩佺Щ璧?clients 涓虹┖锛坒ast-fail锛夛紱鐜版敼涓哄～鍏呮墍鏈?vless 鍏ョ珯锛岃妭鐐?锛坧c-stable-US锛夋仮澶嶇嫭绔嬪彲鐢ㄣ€傜湅闂ㄧ嫍 v2.2 鏂板鑺傜偣2姣忓皬鏃舵帰娴嬨€?

- 2026-11-03: **瀹屾暣浜嬩欢澶嶇洏** docs/incident-2026-10-31-hk-outage.md锛堥娓腑鏂?澶?鈫?443搴旀€ヨ縼绉?鈫?2053淇 鈫?鎭㈠鍥炲垏锛屽惈缁忛獙鏁欒6鏉★級

- 2026-11-04: **鏂板鑽愮绂呭瀵艰 AI 澶ц剳鏈嶅姟**锛坄dafeiyu-brain.service`锛岀洃鍚?`0.0.0.0:18765`锛寀fw 宸叉斁琛岋級銆傜▼搴忓湪 `/opt/dafeiyu-brain`锛坆rain.py + 闈欐€佸瑙堥〉 + Live2D 妯″瀷 + venv锛夛紝寮瑰箷缁?bilibili-api 鍖垮悕杩炴帴锛坵bi 绛惧悕鍙繃椋庢帶锛夛紝鍥炲璧版湰鏈?New API锛坄http://127.0.0.1:3000/v1`锛屾ā鍨?`glm-4.5-air`锛屼笓鐢ㄤ护鐗?`dafeiyu-brain` 灞?default 鍒嗙粍锛夛紝璇煶鐢?edge-tts銆備笉鏀?Nginx銆佷笉鍗?80/443锛屼笌涓浆绔欎簰涓嶅奖鍝嶃€傜鍙?8765/8766/8787 宸茶鏃㈡湁鏈嶅姟鍗犵敤锛屾晠鐢?18765銆?

## 绾﹀畾锛堝繀椤婚伒瀹堬級

1. 姣忔鏀瑰姩瀹屾垚鍚庯紝蹇呴』鍒涘缓涓€涓搴旂殑 Git commit銆?
2. 姣忔鏀瑰姩鍚庯紝蹇呴』缂栧啓鎴栨洿鏂扮浉鍏虫祴璇曪紝骞跺湪浜や粯鍓嶇‘淇濆叏閮ㄦ祴璇曢€氳繃銆?
3. 浠讳綍瀵嗛挜銆佸瘑鐮併€佺閽ャ€乁UID 涓€寰嬩笉鍐欏叆浠撳簱锛涚敤 `.env` 鎴栨湇鍔″櫒鏈湴鏂囦欢銆?
4. 鏈粨搴撲笉寰楀垹闄ゃ€?

璇︾粏绾﹀畾瑙?[my-relay.md](my-relay.md)銆

- 2026-11-05: **荐福禅寺导览页形象/声音改为小沙弥**——`/opt/dafeiyu-brain/temple.html` 用自绘 SVG 小沙弥（光头+香疤+袈裟+合掌）替换女仆 Live2D；edge-tts 音色 `zh-CN-XiaoyiNeural`（女童）→ `zh-CN-YunxiNeural`（少年男声）；brain.py 人设同步为「导览小沙弥·小满」。服务已重启并验证渲染。

- 2026-11-07: **导览形象定稿为专业插画小沙弥**——此前自绘 SVG 版被用户否决（太丑），改用 いらすとや（irasutoya，免费商用授权）的「お坊さんの男の子」插画（`monk.png`，379×600 透明底）。页面从 Live2D/SVG 全部换为 `<img>` + CSS 动画（浮动、摇摆、说话蹦跳、26s 合掌鞠躬），并保留少年男声 `zh-CN-YunxiNeural`。已部署 `/opt/dafeiyu-brain/`，验证：temple.html/monk.png 均 200、/health ok、/llm 回归 200（4.8s）。备注：中转站无可用画图渠道（gpt-image-2 上游欠费、cline 分组无渠道），故弃用 AI 生图路线。

- 2026-11-07: **导览页三连改进**——①形象可自选：设置面板内置 4 张 irasutoya 形象（默认改为合掌念经款 monk2.png）＋「相册上传」任意图片（canvas 压缩后存 localStorage）；②提速：发现 glm-4.5-air 为思考型模型，加 `thinking:{type:disabled}` 后 3.5s→1s，且修复了 max_tokens=400 时思考 token 挤空正文导致的空回复 bug；publish 改两段式（文字先上桌、语音后补）；③音质：页面提问不再用手机系统 TTS，改走新端点 `POST /api/ask`（token 同 page_token，入队走弹幕同款 LLM→edge-tts 管线），设置面板新增 4 音色选择（云希/云夏/云健/晓晓，localStorage 持久化、按请求传给大脑）。实测：点击提问→字幕 1.5s→语音 4s，mp3 可下载。中转站其余聊天渠道（kimi/deepseek/qwen/glm-4.6 等）实测全部失效（余额/密钥/无渠道），glm-4.5-air 为唯一可用渠道。

- 2026-11-08: **用户令停播，大脑服务彻底下线**——核实 B站房间 1946292432 live_status=0（未开播）、近 6h 弹幕 0 条、本机无推流进程；确认无任何对外直播后，`systemctl stop + disable dafeiyu-brain`（切断开机自启与崩溃自动拉起），18765 端口已拒绝连接。文件保留在 `/opt/dafeiyu-brain/` 未动；恢复命令 `sudo systemctl enable --now dafeiyu-brain`。
