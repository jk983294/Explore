#!/opt/anaconda3/bin/python
from socketserver import ThreadingMixIn
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import gzip
from io import BytesIO
from threading import Thread


def gzip_encode(content):
    out = BytesIO()
    f = gzip.GzipFile(fileobj=out, mode='wb', compresslevel=5)
    f.write(content)
    f.close()
    return out.getvalue()


def make_handler_class_with_args(global_info):
    class PostServerHandler(BaseHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            self.global_info = global_info
            self.exchange = global_info['exchange']
            self.brokers = global_info['brokers']
            self.trader_data = global_info['trader_data']
            super(PostServerHandler, self).__init__(*args, **kwargs)

        def log_message(self, format, *args):
            pass

        def _set_response(self, gzip=False, length=0):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', '*')
            self.send_header("Access-Control-Allow-Headers", "*")
            if length != 0:
                self.send_header('Content-length', str(length))
            if gzip:
                self.send_header('Content-Encoding', 'gzip')
            self.end_headers()

        def print_head(self):
            return 'GET request,\nPath: %s\nHeaders:\n%s\n' % (str(self.path), str(self.headers))

        def do_OPTIONS(self):
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', '*')
            self.send_header("Access-Control-Allow-Headers", "*")
            self.end_headers()

        def do_GET(self):
            self._set_response()
            self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

        def do_POST(self):
            if self.path[0] != '/':
                self.path = '/' + self.path
            path_list = self.path.split('/')
            content_length = int(self.headers['Content-Length'])
            post_data = json.loads(self.rfile.read(content_length).decode('utf-8'))
            # print('do_POST', self.client_address[0], path_list, post_data)
            self._set_response(gzip=True)
            if path_list[1] == 'admin':
                if 'cmd' in post_data:
                    cmd = post_data['cmd']
                    ret = (False, "invalid cmd %s" % cmd)
                    if cmd == 'meters':
                        ret = True, 'test'

                    if ret is None:
                        self.wfile.write(gzip_encode(json.dumps(
                            {'status': False, 'reason': 'admin request %s returns none' % cmd}).encode('utf-8')))
                    if not ret[0]:
                        self.wfile.write(gzip_encode(json.dumps({'status': False, 'reason': ret[1]}).encode('utf-8')))
                    else:
                        self.wfile.write(gzip_encode(json.dumps({'status': True, 'result': ret[1]}).encode('utf-8')))
                else:
                    self.wfile.write(gzip_encode(json.dumps(
                        {'status': False, 'reason': "invalid admin args"}).encode('utf-8')))
            elif path_list[1] == 'results':
                array_result = []
                for trader_id, trader in self.trader_data.traders.items():
                    array_result.append(trader)

                # calculate result
                count = len(array_result)
                if count > 0:
                    array_result = sorted(array_result, key=lambda k: k['pnl'])
                    for i in range(count):
                        array_result[i]['pnl_rank'] = i + 1
                        array_result[i]['pnl_score'] = 100.0 - (100.0 / 28 * i)

                    array_result = sorted(array_result, key=lambda k: k['volume_all'])
                    for i in range(count):
                        array_result[i]['volume_rank'] = i + 1
                        array_result[i]['volume_score'] = 100.0 - (100.0 / 28 * i)

                    array_result = sorted(array_result, key=lambda k: k['market_all'])
                    for i in range(count):
                        array_result[i]['percent_rank'] = i + 1
                        array_result[i]['percent_score'] = 100.0 - (100.0 / 28 * i)

                    for result in array_result:
                        result['score'] = result['percent_score'] * 0.5 + \
                            result['pnl_score'] * 0.2 + result['volume_score'] * 0.3
                        if result['market_all'] < 0.1:
                            result['score'] = 0
                results = {
                    "time": '%s' % self.exchange._clock,
                    "traders": array_result
                }
                self.wfile.write(gzip_encode(json.dumps({'status': True, 'result': results}).encode('utf-8')))
            else:
                self.wfile.write(gzip_encode(json.dumps({'status': True, 'result': "unknown request"}).encode('utf-8')))
    return PostServerHandler


class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    def set_logger(self, logger):
        self.logger = logger


class PostServer(Thread):
    def __init__(self, addr, port, global_info):
        super().__init__()
        self.addr = addr
        self.port = port
        self.handler = make_handler_class_with_args(global_info)

    def run(self):
        server_address = (self.addr, self.port)
        httpd = ThreadingSimpleServer(server_address, self.handler)
        print('starting post server at %s:%s...' % (self.addr, str(self.port)))
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        httpd.server_close()
        print('stopping httpd...')
