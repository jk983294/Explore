from .PostClient import PostClient
import json
import os
import time

if __name__ == '__main__':
    from sys import argv

    host = 'localhost'
    port = 52922
    if len(argv) == 3:
        host, port = argv[1], int(argv[2])

    client = PostClient(host, port)

    dump_directory = "./result_dump"
    if not os.path.isdir(dump_directory):
        os.makedirs(dump_directory)

    while True:
        time.sleep(5)
        try:
            result = client.post('results', {'type': 'query'}, json.loads('{}'))
            file_path = './result_dump/%d_%s.log' % (port, time.strftime("%Y%m%d.%H%M%S", time.localtime()))
            with open(file_path, "wt", encoding='utf-8') as f:
                print(json.dumps(result, ensure_ascii=False), file=f)
            print('dump to ', file_path)
        except:
            print('error happen')
