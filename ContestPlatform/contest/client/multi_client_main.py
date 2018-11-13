from __future__ import print_function
import os
import time
import os.path as path
from xml.etree import ElementTree
from .client_main import run
from concurrent.futures import ThreadPoolExecutor


def main():
    if len(os.sys.argv) != 2:
        print("Missing configuration filename.")
        print("USE: python3 -m contest.client.multi_client_main config_file.xml")
        exit(0)

    config_filename = os.sys.argv[1]
    if not config_filename.endswith('.xml'):
        config_filename += '.xml'

    if not path.exists(config_filename):
        print('ERROR: Config file does not exist.')
        return

    pool = ThreadPoolExecutor(25)
    async_result = []
    config = ElementTree.parse(config_filename).getroot()
    for node in config.findall('client'):
        try:
            user_name = node.find('user_name').text
            user_id = int(node.find('user_id').text)
            user_pin = node.find('user_pin').text
            question_endpoint = node.find('question_front').text
            answer_endpoint = node.find('answer_front').text

            res = pool.submit(run, user_name, user_id, user_pin, question_endpoint, answer_endpoint)
            async_result.append(res)
            time.sleep(0.2)
        except Exception as err:
            print('ERROR: Cannot initialize client. (%s)' % str(err))
            raise err

    for ar in async_result:
        ar.result()


if __name__ == '__main__':
    main()
