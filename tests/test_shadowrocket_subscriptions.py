import base64
import importlib.util
from pathlib import Path
import unittest
from urllib.parse import urlsplit, parse_qs

path = Path(__file__).resolve().parents[1] / 'scripts/build_shadowrocket_subscriptions.py'
spec = importlib.util.spec_from_file_location('subs', path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class SubscriptionTests(unittest.TestCase):
    def test_roundtrip_and_reality(self):
        meta = dict(address='192.0.2.1', port=2053, serverName='example.com', publicKey='test-public-key', shortId='1234')
        user = dict(name='friend1', id='00000000-0000-4000-8000-000000000001')
        payload = module.subscription(meta, user)
        decoded = base64.b64decode(payload, validate=False).decode()
        self.assertEqual(decoded, module.node_uri(meta, user) + '\n')
        uri = urlsplit(decoded.strip())
        self.assertEqual(uri.scheme, 'vless')
        self.assertEqual(uri.username, user['id'])
        self.assertEqual(uri.port, 2053)
        query = parse_qs(uri.query)
        for key, expected in dict(security='reality', flow='xtls-rprx-vision', type='tcp', pbk='test-public-key', sid='1234', sni='example.com').items():
            self.assertEqual(query[key], [expected])
        self.assertNotIn(b'[Rule]', payload)

if __name__ == '__main__':
    unittest.main()
