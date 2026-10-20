#!/usr/bin/env bash
# my-relay 线上健康检查
# 用法: bash tests/relay_healthcheck.sh [BASE_URL]
set -uo pipefail

BASE_URL="${1:-https://107-175-122-81.sslip.io}"
PASS=0
FAIL=0

check() {
  local name="$1" url="$2" expect="${3:-200}"
  local code
  code=$(curl -s -o /dev/null --max-time 15 -w '%{http_code}' "$url" 2>/dev/null)
  if [ "$code" = "$expect" ]; then
    echo "PASS  $name  HTTP $code  $url"
    PASS=$((PASS+1))
  else
    echo "FAIL  $name  HTTP $code (expect $expect)  $url"
    FAIL=$((FAIL+1))
  fi
}

check "New API 状态"      "$BASE_URL/api/status"              200
check "余量查询页"         "$BASE_URL/usage/"                  200
check "Clash 订阅 thinkpad" "$BASE_URL/sub/thinkpad-clash.yaml" 200
check "Clash 订阅 pc"      "$BASE_URL/sub/pc-clash.yaml"       200
check "Clash 订阅 android" "$BASE_URL/sub/android-clash.yaml"  200
check "Clash 订阅 backup"  "$BASE_URL/sub/backup-clash.yaml"   200

# /api/status 必须返回 success:true
STATUS_JSON=$(curl -s --max-time 15 "$BASE_URL/api/status" 2>/dev/null)
if echo "$STATUS_JSON" | grep -q '"success":true'; then
  echo "PASS  /api/status success=true"
  PASS=$((PASS+1))
else
  echo "FAIL  /api/status success != true"
  FAIL=$((FAIL+1))
fi

# 已下线的订阅必须 404
check "iphone 订阅已下线"  "$BASE_URL/sub/iphone-clash.yaml"  404
check "ipad 订阅已下线"    "$BASE_URL/sub/ipad-clash.yaml"    404

echo "----------------------------------------"
echo "PASS=$PASS FAIL=$FAIL"
[ "$FAIL" -eq 0 ]