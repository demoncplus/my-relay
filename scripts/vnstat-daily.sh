#!/bin/bash
# 每日 08:30 生成流量日报到 /var/log/vnstat-daily.log
LOG=/var/log/vnstat-daily.log
{
  echo "========== $(date '+%Y-%m-%d %H:%M') =========="
  echo "--- 今日/昨日 eth0 流量 ---"
  vnstat -i eth0 -d | tail -n 6
  echo "--- 当前月份汇总 ---"
  vnstat -i eth0 -m | tail -n 6
  echo "OOM-safe: 流量单位 GiB=1024^3 bytes. 套餐额度 3TB/月。"
} >> "$LOG" 2>&1
