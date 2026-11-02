"""Build private Shadowrocket node subscriptions; never commit generated output."""
import argparse
import base64
import json
import secrets
from pathlib import Path
from urllib.parse import urlencode, quote


def node_uri(meta, user):
    query = urlencode(dict(encryption='none', security='reality', sni=meta['serverName'], fp='chrome', pbk=meta['publicKey'], sid=meta['shortId'], type='tcp', flow='xtls-rprx-vision', spx='/'))
    return f"vless://{user['id']}@{meta['address']}:{meta['port']}?{query}#{quote('RackNerd-' + user['name'])}"


def subscription(meta, user):
    return base64.b64encode((node_uri(meta, user) + '\n').encode()) + b'\n'


def build(accounts, root, vendor):
    import sys
    sys.path.insert(0, str(vendor))
    import qrcode
    data = json.loads(accounts.read_text(encoding='utf-8'))
    out = root / 'Shadowrocket-首页订阅-私密'
    out.mkdir(exist_ok=True)
    manifest_path = out / 'manifest.json'
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    for user in data['users']:
        name = user['name']
        if name not in ['friend' + str(i) for i in range(1, 7)]:
            continue
        token = manifest.get(name, {}).get('token', secrets.token_hex(24))
        url = f'https://107-175-122-81.sslip.io/sr/nodes/{token}.txt'
        manifest[name] = dict(token=token, url=url)
        (out / (token + '.txt')).write_bytes(subscription(data['meta'], user))
        folder = root / name / 'Shadowrocket'
        (folder / (name + '-首页订阅链接.txt')).write_text(url + '\n', encoding='utf-8')
        qrcode.make(url).save(folder / (name + '-首页订阅二维码.png'))
        (folder / '首页订阅使用说明.txt').write_text('首页 → + → 类型 Subscribe（订阅），粘贴本目录的首页订阅链接。也可在首页扫描首页订阅二维码。\n选择 RackNerd-' + name + ' 节点，开启连接。首次使用可将全局路由设为「代理」。\n本订阅仅提供节点，不安装分流规则。已有规则保持不变。链接相当于密码，请勿公开。\n', encoding='utf-8')
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    print('Built', len(manifest), 'private subscriptions; credentials omitted.')


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--accounts', type=Path, required=True)
    p.add_argument('--root', type=Path, required=True)
    p.add_argument('--vendor', type=Path, required=True)
    a = p.parse_args()
    build(a.accounts, a.root, a.vendor)
