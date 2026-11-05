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
