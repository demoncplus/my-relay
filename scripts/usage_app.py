import os,json,secrets,time,hmac,threading
from pathlib import Path
from urllib.parse import parse_qs,urlsplit
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from datetime import datetime
CODES={}
for line in Path('/opt/wg-usage-app/codes.conf').read_text().splitlines():
    if line and not line.startswith('#'):
        name,code=line.split('=',1);CODES[code.strip()]=name.strip()
SESSIONS={};FAILURES={};LOCK=threading.Lock()
PAGE='''<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="refresh" content="60"><title>我的流量余量</title><style>body{font-family:system-ui,sans-serif;background:#f0f3f8;margin:0;padding:24px;color:#203047}.wrap{max-width:460px;margin:auto}.card{background:white;border-radius:16px;padding:24px;margin:16px 0;box-shadow:0 4px 20px #2030470c}h1{font-size:24px}h2{font-size:18px}.num{font-size:38px;font-weight:700;color:#15856b}.muted{font-size:13px;color:#637489;line-height:1.7}progress{width:100%;height:16px;accent-color:#15856b}input{box-sizing:border-box;width:100%;padding:14px;font-size:18px;border:1px solid #ccd4dd;border-radius:8px}button{padding:12px 24px;margin-top:16px;border:0;border-radius:8px;color:white;background:#2466bd}.error{color:#bc3345}</style></head><body><div class="wrap">BODY</div></body></html>'''
def html(body):return PAGE.replace('BODY',body)
def login(error=''):
    return html('<h1>我的流量余量</h1><div class="card"><p>输入你的访问码，查看自己的流量。</p><p class="error">'+error+'</p><form method="post" action="/usage/"><input name="code" placeholder="XXXX-XXXX" maxlength="64" autocomplete="off" required><button>登录</button></form></div>')
def card(title,used,limit,unit,extra,disabled):
    remaining=max(0,limit-used)/unit;pct=min(100,used*100/limit)
    label='GB' if unit==1_000_000_000 else 'GiB'
    status='本月已达上限，暂停至下月' if disabled or used>=limit else '可用'
    return f'<section class="card"><h2>{title}</h2><div class="num">{remaining:.2f} {label}</div><p>本月剩余</p><progress max="100" value="{pct}"></progress><p>已用 {used/unit:.2f} / {limit/unit:g} {label}</p><p>状态：{status}</p><p class="muted">{extra}</p></section>'
def dashboard(friend):
    p=Path('/var/lib/wg-quota')
    used=int((p/(friend+'.used')).read_text().strip()) if (p/(friend+'.used')).exists() else 0
    body=f'<h1>{friend} · 本月余量</h1>'
    body+=card('WireGuard',used,100*1024**3,1024**3,'每30分钟统计；100 GiB = 107.37 GB；与下方配额独立。',(p/(friend+'.disabled')).exists())
    try:
        state=json.loads(Path('/var/lib/xray-quota/state.json').read_text())
        used=state['used'].get(friend,0)
        from zoneinfo import ZoneInfo
        current=datetime.now(ZoneInfo('Asia/Shanghai')).strftime('%Y-%m')
        if state['month']!=current:used=0
        stamp=state.get('updated_at','等待首次统计')
        body+=card('VLESS + REALITY',used,100_000_000_000,1_000_000_000,'每5秒统计上传+下载。更新时间：'+stamp,used>=100_000_000_000)
    except (OSError,ValueError,KeyError):body+='<section class="card">新协议数据暂不可用，请稍后刷新。</section>'
    body+='<p class="muted">按上海时间每月1日重置。页面每60秒刷新。两种协议分别计费限额；本页不表示VPS套餐总余量。</p><form method="post" action="/usage/logout"><button>退出登录</button></form>'
    return html(body)
class H(BaseHTTPRequestHandler):
    def log_message(self,*a):pass
    def send(self,body,status=200):
        data=body.encode();self.send_response(status)
        for k,v in [('Content-Type','text/html; charset=utf-8'),('Content-Length',str(len(data))),('Cache-Control','no-store'),('X-Content-Type-Options','nosniff'),('Referrer-Policy','no-referrer'),('X-Frame-Options','DENY')]:self.send_header(k,v)
        self.end_headers();self.wfile.write(data)
    def token(self):
        try:
            c=SimpleCookie(self.headers.get('Cookie',''));return c['session'].value if 'session' in c else ''
        except Exception:return ''
    def session(self):
        t=self.token()
        with LOCK:
            entry=SESSIONS.get(t)
            if entry and entry[1]>time.time():return entry[0]
            SESSIONS.pop(t,None)
        return None
    def redirect(self,cookie):
        self.send_response(303);self.send_header('Location','/usage/');self.send_header('Set-Cookie',cookie+'; Path=/usage/; Secure; HttpOnly; SameSite=Lax');self.send_header('Cache-Control','no-store');self.end_headers()
    def do_GET(self):
        if urlsplit(self.path).path!='/usage/':self.send(html('<p>页面不存在</p>'),404);return
        friend=self.session();self.send(dashboard(friend) if friend else login())
    def do_POST(self):
        path=urlsplit(self.path).path
        if path=='/usage/logout':
            with LOCK:SESSIONS.pop(self.token(),None)
            self.redirect('session=; Max-Age=0');return
        if path!='/usage/':self.send('',404);return
        try:n=int(self.headers.get('Content-Length','0'))
        except ValueError:self.send('',400);return
        if not 0<n<=1024:self.send('',413);return
        addr=self.headers.get('X-Real-IP',self.client_address[0]);now=time.time()
        with LOCK:
            recent=[x for x in FAILURES.get(addr,[]) if now-x<900]
            FAILURES[addr]=recent
        if len(recent)>=10:self.send(login('尝试次数过多，请15分钟后重试。'),429);return
        fields=parse_qs(self.rfile.read(n).decode('utf-8',errors='replace'))
        code=fields.get('code',[''])[0].strip().upper();friend=None
        for secret,name in CODES.items():
            if hmac.compare_digest(code,secret):friend=name
        if not friend:
            with LOCK:FAILURES[addr].append(now)
            self.send(login('访问码不正确。'),401);return
        token=secrets.token_urlsafe(32)
        with LOCK:
            for key in [k for k,v in SESSIONS.items() if v[1]<now]:del SESSIONS[key]
            SESSIONS[token]=(friend,now+7*86400);FAILURES.pop(addr,None)
        self.redirect('session='+token+'; Max-Age=604800')
if __name__=='__main__':ThreadingHTTPServer(('127.0.0.1',8765),H).serve_forever()
