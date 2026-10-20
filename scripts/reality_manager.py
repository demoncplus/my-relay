#!/usr/bin/env python3
"""Supervise Xray, persist monthly per-user accounting, enforce quota by restart."""
import json, os, signal, subprocess, time
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
ROOT=Path('/etc/xray-reality')
STATE=Path('/var/lib/xray-quota/state.json')
API='127.0.0.1:10085'
XRAY='/usr/local/bin/xray'
running=True

def month(): return datetime.now(ZoneInfo('Asia/Shanghai')).strftime('%Y-%m')
def load(p): return json.loads(p.read_text())
def save(p,data):
    tmp=p.with_suffix('.tmp')
    tmp.write_text(json.dumps(data,ensure_ascii=False,indent=2))
    os.chmod(tmp,0o600)
    os.replace(tmp,p)
def rollover(state, current_month):
    if state['month'] != current_month:
        return {'month':current_month,'used':{}}
    return state

def account(state, totals, bases):
    for name,current in totals.items():
        previous=bases.get(name,0)
        state['used'][name]=state['used'].get(name,0)+max(0,current-previous)
        bases[name]=current

def query():
    p=subprocess.run([XRAY,'api','statsquery','--server='+API,'-pattern','user>>>'],capture_output=True,text=True,timeout=8,check=True)
    data=json.loads(p.stdout)
    totals={}
    for row in data.get('stat',[]):
        parts=row['name'].split('>>>')
        if len(parts)==4 and parts[0]=='user' and parts[2]=='traffic':
            totals[parts[1]]=totals.get(parts[1],0)+int(row.get('value',0))
    return totals

def effective(users,state):
    config=load(ROOT/'base.json')
    clients=[]
    disabled=[]
    for u in users:
        if u['limit'] and state['used'].get(u['name'],0)>=u['limit']:
            disabled.append(u['name'])
        else:
            clients.append({'id':u['id'],'email':u['name'],'flow':'xtls-rprx-vision','level':0})
    config['inbounds'][0]['settings']['clients']=clients
    return config,disabled

def main():
    global running
    signal.signal(signal.SIGTERM,lambda *_:stop())
    signal.signal(signal.SIGINT,lambda *_:stop())
    users=load(ROOT/'users.json')
    state=load(STATE) if STATE.exists() else {'month':month(),'used':{}}
    state=rollover(state,month())
    proc=None;bases={};disabled=[]
    def launch():
        nonlocal proc,bases,disabled
        conf,disabled=effective(users,state)
        save(ROOT/'effective.json',conf)
        save(STATE,state)
        proc=subprocess.Popen([XRAY,'run','-config',str(ROOT/'effective.json')])
        bases={}
    def terminate():
        if proc and proc.poll() is None:
            proc.terminate()
            try:proc.wait(timeout=10)
            except subprocess.TimeoutExpired:proc.kill();proc.wait()
    launch()
    try:
        while running:
            time.sleep(5)
            if proc.poll() is not None:
                print('Xray exited; restarting',flush=True);launch();continue
            try:account(state,query(),bases)
            except Exception as e:
                print('Stats unavailable; restarting to restore accounting: '+str(e),flush=True)
                terminate();launch();continue
            state=rollover(state,month())
            state['updated_at']=datetime.now(ZoneInfo('Asia/Shanghai')).isoformat()
            _,new_disabled=effective(users,state)
            save(STATE,state)
            if new_disabled!=disabled:
                print('Quota membership changed: '+str(new_disabled),flush=True)
                terminate();launch()
    finally:
        try:account(state,query(),bases)
        except Exception:pass
        save(STATE,state)
        terminate()

def stop():
    global running
    running=False
if __name__=='__main__':main()
