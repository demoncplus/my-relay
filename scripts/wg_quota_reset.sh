#!/bin/bash
# 每月 1 号 00:05 重置 friend1~friend6 配额并恢复被摘除的 peer
set -u
STATEDIR=/var/lib/wg-quota
mkdir -p $STATEDIR

for name in friend1 friend2 friend3 friend4 friend5 friend6; do
  rm -f $STATEDIR/$name.used $STATEDIR/$name.base $STATEDIR/$name.disabled
done

# syncconf 会把 wg0.conf 里定义的全部 peer 重新加载（恢复被摘除的 friend）
wg syncconf wg0 <(wg-quick strip /etc/wireguard/wg0.conf) && \
  logger -t wg-quota "monthly reset done, all peers re-synced"
