#!/opt/anaconda3/bin/python
from socketserver import ThreadingMixIn
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import gzip
from io import BytesIO
from .GlobalInfo import GlobalInfo


def gzip_encode(content):
    out = BytesIO()
    f = gzip.GzipFile(fileobj=out, mode='wb', compresslevel=5)
    f.write(content)
    f.close()
    return out.getvalue()


def make_handler_class_with_args(global_info: GlobalInfo):
    class PostServerHandler(BaseHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            self.global_info = global_info
            self.question_publisher = global_info.question_publisher
            self.account_manager = global_info.accountManager
            super(PostServerHandler, self).__init__(*args, **kwargs)

        def log_message(self, format, *args):
            try:
                log_str = format % args
                self.server.logger.debug(log_str)
            except Exception as e:
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
            print('do_POST', self.client_address[0], path_list, post_data)
            self._set_response(gzip=True)
            if path_list[1] == 'admin':
                if 'cmd' in post_data:
                    cmd = post_data['cmd']
                    ret = (False, "invalid cmd %s" % cmd)
                    if cmd == 'dump_user':
                        ret = self.account_manager.dump_to_file(post_data["path"])
                    elif cmd == 'load_user':
                        ret = self.account_manager.load_from_file(post_data["path"])
                    elif cmd == 'pause':
                        ret = self.question_publisher.pause_publish()
                    elif cmd == 'resume':
                        ret = self.question_publisher.resume_publish()
                    elif cmd == 'penalty':
                        if "user_id" not in post_data or "money" not in post_data:
                            ret = False, "cmd format not correct"
                        else:
                            ret = self.account_manager.penalty(post_data["user_id"], post_data["money"])
                    elif cmd == 'add_user':
                        if "user_id" not in post_data or "user_name" not in post_data or "user_pin" not in post_data:
                            ret = False, "cmd format not correct"
                        else:
                            ret = self.account_manager.add_account(
                                post_data["user_name"], post_data["user_id"], post_data["user_pin"])
                            if ret:
                                ret = True, 'success'
                            else:
                                ret = False, 'failed'

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
            elif path_list[1] == 'all_users':
                result = self.account_manager.get_all_accounts()
                seq = self.question_publisher.sequence
                mode = self.global_info.mode
                self.wfile.write(gzip_encode(json.dumps(
                    {'status': True, 'result': result, 'sequence': seq, 'mode': mode}).encode('utf-8')))
            elif path_list[1] == 'finish_test':
                if "user_id" not in post_data:
                    self.wfile.write(gzip_encode(json.dumps(
                        {'status': False, 'reason': 'user id must be provided'}).encode('utf-8')))
                    return
                account = self.account_manager.get_account(post_data['user_id'])
                if account:
                    success, reason = account.finish_test()
                    if success:
                        self.wfile.write(gzip_encode(json.dumps({'status': True, 'result': reason}).encode('utf-8')))
                    else:
                        self.wfile.write(gzip_encode(json.dumps({'status': False, 'reason': reason}).encode('utf-8')))
                else:
                    self.wfile.write(gzip_encode(json.dumps(
                        {'status': False, 'reason': 'user not found'}).encode('utf-8')))
            elif path_list[1] == 'undo_finish_test':
                if "user_id" not in post_data:
                    self.wfile.write(gzip_encode(json.dumps(
                        {'status': False, 'reason': 'user id must be provided'}).encode('utf-8')))
                    return
                account = self.account_manager.get_account(post_data['user_id'])
                if account:
                    success, reason = account.undo_finish_test()
                    if success:
                        self.wfile.write(gzip_encode(json.dumps({'status': True, 'result': reason}).encode('utf-8')))
                    else:
                        self.wfile.write(gzip_encode(json.dumps({'status': False, 'reason': reason}).encode('utf-8')))
                else:
                    self.wfile.write(gzip_encode(json.dumps(
                        {'status': False, 'reason': 'user not found'}).encode('utf-8')))
            elif path_list[1] == 'penalty':
                if "user_id" not in post_data or "penalty_type" not in post_data or "status" not in post_data:
                    self.wfile.write(gzip_encode(json.dumps(
                        {'status': False, 'reason': 'format not correct'}).encode('utf-8')))
                    return
                account = self.account_manager.get_account(post_data['user_id'])
                if account:
                    success, reason = account.set_penalty_flag(post_data['penalty_type'], post_data['status'])
                    if success:
                        self.wfile.write(gzip_encode(json.dumps({'status': True, 'result': reason}).encode('utf-8')))
                    else:
                        self.wfile.write(gzip_encode(json.dumps({'status': False, 'reason': reason}).encode('utf-8')))
                else:
                    self.wfile.write(gzip_encode(json.dumps(
                        {'status': False, 'reason': 'user not found'}).encode('utf-8')))
            else:
                self.wfile.write(gzip_encode(json.dumps({'status': True, 'result': "unknown request"}).encode('utf-8')))
    return PostServerHandler


class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    def set_logger(self, logger):
        self.logger = logger


class PostServer(object):
    def __init__(self, addr, port, global_info: GlobalInfo, logger):
        self.addr = addr
        self.port = port
        self.handler = make_handler_class_with_args(global_info)
        self.logger = logger

    def run(self):
        server_address = (self.addr, self.port)
        httpd = ThreadingSimpleServer(server_address, self.handler)
        httpd.set_logger(self.logger)
        self.logger.info('starting post server at %s:%s...' % (self.addr, str(self.port)))
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        httpd.server_close()
        self.logger.info('stopping httpd...')
