#!/bin/bash
# WireGuard 月度配额监控：friend1~friend6 各 100GB/月，超限摘除，月初自动恢复
# 由 root cron 每 30 分钟运行；统计后自动生成公开的剩余流量页面
set -u
LIMIT=$((100 * 1024 * 1024 * 1024))   # 100GiB per friend per month
STATEDIR=/var/lib/wg-quota
OUTDIR=/var/www/wg-usage
mkdir -p $STATEDIR $OUTDIR; chmod 700 $STATEDIR

# friend1 -> .5, friend2 -> .6, friend3~6 -> .8~.11（与 wg0.conf 中允许 IP 对应）
declare -A NAMES=(
  [friend1]="/etc/wireguard/clients/friend1.pub"
  [friend2]="/etc/wireguard/clients/friend2.pub"
  [friend3]="/etc/wireguard/clients/friend3.pub"
  [friend4]="/etc/wireguard/clients/friend4.pub"
  [friend5]="/etc/wireguard/clients/friend5.pub"
  [friend6]="/etc/wireguard/clients/friend6.pub"
)

TRANSFER=$(wg show wg0 transfer 2>/dev/null) || TRANSFER=""

SUMMARY=""
for name in friend1 friend2 friend3 friend4 friend5 friend6; do
  pub=$(cat "${NAMES[$name]}")
  used_file=$STATEDIR/$name.used
  base_file=$STATEDIR/$name.base
  [ -f $used_file ] || echo 0 > $used_file
  [ -f $base_file ] || echo 0 > $base_file
  used=$(cat $used_file); base=$(cat $base_file)

  disabled=0
  [ -f $STATEDIR/$name.disabled ] && disabled=1

  cur=$(echo "$TRANSFER" | awk -v k="$pub" '$1==k{print $2+$3}' 2>/dev/null)
  [ -z "$cur" ] && cur=0

  # 计数器回绕（服务器/wg 重启后 transfer 从 0 重新累计）
  if [ "$cur" -lt "$base" ]; then base=0; fi
  delta=$((cur - base))
  used=$((used + delta))
  echo "$cur" > $base_file
  echo "$used" > $used_file

  if [ $disabled -eq 0 ] && [ $used -ge $LIMIT ]; then
    wg set wg0 peer "$pub" remove
    touch $STATEDIR/$name.disabled
    logger -t wg-quota "$name reached monthly limit (${used} bytes), peer removed until month reset"
  fi

  gb_used=$(awk -v b=$used 'BEGIN{printf "%.1f", b/1073741824}')
  GB=100
  remaining=$(awk -v u=$used -v l=$LIMIT 'BEGIN{r=(l-u)/1073741824; printf "%.1f", (r<0 ? 0 : r)}')
  pct_used=$(awk -v u=$used -v l=$LIMIT 'BEGIN{printf "%.1f", u*100/l}')
  bars=""
  if [ $disabled -eq 1 ]; then
    status_opt="<span style=\"color:#c0392b;font-weight:bold\">· 本月超限，已暂停</span>"
  else
    status_opt=""
  fi
  SUMMARY="$SUMMARY
  <div class=\"box\">
    <h3>$name</h3>
    <div class=\"bar-wrap\"><div class=\"bar\" style=\"width:${pct_used}%\"></div></div>
    <table>
      <tr><td>已用</td><td>$gb_used GB</td></tr>
      <tr><td>剩余</td><td>$remaining GB</td></tr>
      <tr><td>状态</td><td>$status_opt</td></tr>
    </table>
    <div class=\"muted\">每 30 分钟自动刷新</div>
  </div>"
done

# 生成所有 friend 的总览页 index.html
cat > $OUTDIR/index.html << EOF
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="refresh" content="1800">
<title>VPN 流量余量</title>
<style>
  body { font-family: -apple-system, "Segoe UI", "Microsoft YaHei", sans-serif; background: #f5f5f5; margin: 0; padding: 24px; }
  h1 { text-align: center; font-size: 20px; color: #333; }
  .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 16px; max-width: 1000px; margin: 30px auto; }
  .box { background: #fff; border-radius: 12px; padding: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
  .box h3 { margin: 0 0 12px; font-size: 18px; color: #333; }
  .bar-wrap { background: #eee; border-radius: 6px; height: 10px; overflow: hidden; margin-bottom: 12px; }
  .bar { background: linear-gradient(90deg, #3498db, #2ecc71); height: 100%; }
  table { width: 100%; border-collapse: collapse; font-size: 14px; }
  td { padding: 5px 0; }
  td:first-child { color: #777; width: 60px; }
  .muted { color: #aaa; font-size: 12px; margin-top: 10px; text-align: right; }
</style>
</head>
<body>
<h1>📶 朋友们本月 VPN 流量余量</h1>
<div class="grid">$SUMMARY
</div>
<p style="text-align:center;color:#888;font-size:12px;">更新时间：$(date '+%Y-%m-%d %H:%M') · 每月 1 号自动清零 · 超过 100GB 自动断开至下月</p>
</body>
</html>
EOF
chmod 644 $OUTDIR/index.html

# 单人查看页：/usage/friendN 独立小页面（更友好分享）
for name in friend1 friend2 friend3 friend4 friend5 friend6; do
  used=$(cat $STATEDIR/$name.used)
  gb_used=$(awk -v b=$used 'BEGIN{printf "%.1f", b/1073741824}')
  remaining=$(awk -v u=$used -v l=$LIMIT 'BEGIN{r=(l-u)/1073741824; printf "%.1f", (r<0 ? 0 : r)}')
  pct_used=$(awk -v u=$used -v l=$LIMIT 'BEGIN{printf "%.1f", u*100/l}')
  if [ -f $STATEDIR/$name.disabled ]; then
    status_line="本月超限，已暂停（下月自动恢复）"
  else
    status_line="正常使用中"
  fi
  cat > $OUTDIR/$name.html << EOF
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="refresh" content="1800">
<title>$name · 我的 VPN 流量</title>
<style>
  body { font-family: -apple-system, "Segoe UI", "Microsoft YaHei", sans-serif; background: #f0f2f5; margin: 0; padding: 40px 20px; display: flex; justify-content: center; }
  .card { background: #fff; border-radius: 16px; box-shadow: 0 4px 16px rgba(0,0,0,0.08); padding: 32px; max-width: 360px; width: 100%; text-align: center; }
  .num { font-size: 42px; font-weight: 700; color: #2ecc71; }
  .unit { font-size: 16px; color: #666; }
  .label { margin-top: 24px; color: #888; font-size: 13px; }
  .bar-wrap { background: #eee; border-radius: 8px; height: 14px; overflow: hidden; margin: 16px 0 8px; }
  .bar { background: linear-gradient(90deg, #3498db, #2ecc71); height: 100%; }
  .status { margin-top: 20px; font-size: 15px; color: #333; }
</style>
</head>
<body>
<div class="card">
  <div class="num">$remaining<span class="unit"> GB</span></div>
  <div>本月剩余流量</div>
  <div class="bar-wrap"><div class="bar" style="width:${pct_used}%"></div></div>
  <div style="color:#999;font-size:13px;">已用 $gb_used GB / 100 GB</div>
  <div class="status">状态：$status_line</div>
  <div class="label">每 30 分钟自动更新 · 每月 1 号清零</div>
</div>
</body>
</html>
EOF
  chmod 644 $OUTDIR/$name.html
done
echo PAGES_GENERATED
