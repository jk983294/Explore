#!/opt/anaconda3/bin/python
"""
Very simple HTTP server in python for logging requests
Usage: ./PostClient.py <host> <port> <path> <args_json>
       ./PostClient.py localhost 56703 'finish_test' '{"user_id": 1}'
"""
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import traceback
import sys
import json


class PostClient(object):
    def __init__(self, addr=None, port=None):
        if addr is None:
            raise ValueError('cannot find address %s' % addr)
        self.port = int(port)
        self.addr_line = 'http://%s:%d' % (addr, port)
        requests.adapters.DEFAULT_RETRIES = 3

    def post(self, prefix, payload, jsondata=None, timeout=5):
        s = requests.session()
        s.keep_alive = False
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        s.mount('http://', adapter)
        s.mount('https://', adapter)

        if len(prefix) != 0 and prefix[0] != '/':
            prefix = '/' + prefix
        if jsondata is not None:
            jsondata['type'] = payload['type']
            try:
                ret = s.post(self.addr_line + prefix, json=jsondata, timeout=timeout)
            except Exception as e:
                traceback.print_exception(*sys.exc_info())
                return {'status': False, 'code': 400, 'reason': str(e)}
        else:
            jsondata = {'type': payload['type']}
            try:
                ret = s.post(self.addr_line + prefix, json=jsondata, timeout=timeout)
            except Exception as e:
                return {'status': False, 'code': 400, 'reason': str(e)}
        if ret.reason != 'OK':
            return {'status': False, 'code': ret.status_code, 'reason': ret.reason}
        if ret.text.strip() == '':
            return {'status': True, 'data': {}}
        return ret.json()


def test():
    client = PostClient('localhost', 56703)
    print(client.post('/all_users', {'type': 'query'}))
    print(client.post('/finish_test', {'type': 'query'}, {'user_id': 1}))
    print(client.post('/undo_finish_test', {'type': 'query'}, {'user_id': 1}))
    print(client.post('/admin', {'type': 'query'}, {'cmd': 'pause'}))
    print(client.post('/admin', {'type': 'query'}, {'cmd': 'resume'}))
    print(client.post('/admin', {'type': 'query'}, {'cmd': 'dump_user', 'path': '/tmp/contest.users'}))
    print(client.post('/admin', {'type': 'query'}, {'cmd': 'load_user', 'path': '/tmp/contest.users'}))


if __name__ == '__main__':
    from sys import argv
    if len(argv) == 5:
        host, port, path, args_json = argv[1], int(argv[2]), argv[3], argv[4]
        if not path.startswith('/'):
            path = '/' + path
        client = PostClient(host, port)
        result = client.post(path, {'type': 'query'}, json.loads(args_json))
        print(result)
    elif len(argv) == 1:
        test()
    else:
        print("./PostClient.py <host> <port> <path> <args_json>")
