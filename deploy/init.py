import json,time,urllib.request
for i in range(120):
 try:
  urllib.request.urlopen('http://127.0.0.1:3000/api/status',timeout=3);break
 except Exception:time.sleep(2)
else:raise RuntimeError('New API readiness timed out')
cred=json.load(open('/opt/new-api/admin.json'))
payload=dict(username=cred['username'],password=cred['password'],confirmPassword=cred['password'],SelfUseModeEnabled=True,DemoSiteEnabled=False)
r=urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:3000/api/setup',data=json.dumps(payload).encode(),headers={'Content-Type':'application/json'}))
data=json.load(r)
assert data.get('success'),data
print('NEW_API_INITIALIZED')
