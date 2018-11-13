import os
import sys
import time
import os.path as path
from xml.etree import ElementTree
from .GlobalInfo import GlobalInfo
from .QuestionPublisher import QuestionPublisher
from .AnswerService import AnswerService
from .PnlService import PnlService
from .GameEngineAlt import GameEngineAlt
from .PostServer import PostServer
import logging


def run_modules(config_filename):
    """Run modules as configured in the given XML file."""
    if not path.exists(config_filename):
        print('ERROR: Config file does not exist.')
        return

    global_info = GlobalInfo()

    try:
        root = ElementTree.parse(config_filename).getroot()
        accounts_config = root.find('accounts')
        global_info.accountManager.init_from_xml(accounts_config)
        if root.find('mode') is not None:
            global_info.mode = root.find('mode').text
        print("server mode: ", global_info.mode)
        modules_config = root.find('modules')
        assert modules_config, 'Node "modules" does not exist.'
    except (ElementTree.ParseError, AssertionError):
        print('ERROR: Invalid config file.')
        return

    log_file = '/tmp/contest.log'
    dump_prefix = '/tmp/contest.dump.'
    if root.find('log') is not None:
        log_file = root.find('log').find('file').text
        dump_prefix = root.find('log').find('dump_prefix').text

    log_file = log_file + '.' + time.strftime("%Y%m%d.%H%M%S", time.localtime())
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(levelname)s:%(asctime)s:%(message)s'
    )
    global_info.logger = logging
    print("log to file ", log_file)

    global_info.dump_prefix = dump_prefix
    print("account dump to %s* every sequence" % dump_prefix)

    print('Starting modules...')

    # init GameEngine
    game_engine = None
    for node in modules_config.findall('game_engine'):
        try:
            dist_file = node.find('distribution_file').text
            payoff_file = node.find('payoff_file').text
            game_engine = GameEngineAlt(dist_file, payoff_file)
            global_info.game_engine = game_engine
        except Exception as err:
            print('Error: Cannot initialize game engine. (%s)' % str(err))
            raise err

    # init AnswerService
    answer_service = None
    for node in modules_config.findall('answer_front'):
        try:
            port = int(node.find('port').text)
        except (AttributeError, ValueError):
            print('ERROR: AnswerService must specify a port.')
            return

        try:
            answer_service = AnswerService(port, global_info)
            answer_service.start()
            global_info.answer_service = answer_service
        except Exception as err:
            print('ERROR: Cannot initialize answer service. (%s)' % str(err))
            raise err

        global_info.server_info['answer'] = port

    # init QuestionPublisher
    question_publisher = None
    for node in modules_config.findall('question_front'):
        try:
            port = int(node.find('port').text)
            total_round = None
            if node.find('round') is not None:
                total_round = int(node.find('round').text)
                print("will only publish %d questions" % total_round)
            question_publisher = QuestionPublisher(port, total_round, global_info)
            question_publisher.start()
            global_info.question_publisher = question_publisher
        except Exception as err:
            print('ERROR: Cannot initialize question publisher. (%s)' % str(err))
            raise err

        global_info.server_info['question'] = port

    pnl_service = None
    try:
        pnl_service = PnlService(global_info)
        pnl_service.start()
        global_info.pnl_service = pnl_service
    except Exception as err:
        print('ERROR: Cannot initialize pnl service. (%s)' % str(err))
        raise err

    # Print server endpoints...
    print('────────────────────────────────────────────────────────')
    print('  Endpoints:                                  ')
    for name in sorted(global_info.server_info.keys()):
        print('  %20s: %-22s' % (name, global_info.server_info[name]))
    print('────────────────────────────────────────────────────────')

    post_server_node = modules_config.find('post_server')
    if post_server_node:
        try:
            port = int(post_server_node.find('port').text)
        except (AttributeError, ValueError):
            print('ERROR: PostServer must specify a port.')
            return

        try:
            post_server = PostServer('0.0.0.0', port, global_info, logging)
            post_server.run()
        except Exception as err:
            print('ERROR: Cannot initialize post server. (%s)' % str(err))
            raise err


def main():
    print('────────────────────────────────────────────────')
    print('              Contest Platform                  ')
    print('────────────────────────────────────────────────')

    if len(os.sys.argv) != 2:
        print("Missing configuration filename.")
        print("USE: python3 -m contest.server.server_main config_file.xml")
        exit(0)

    filename = os.sys.argv[1]
    if not filename.endswith('.xml'):
        filename += '.xml'

    run_modules(filename)


if __name__ == '__main__':
    main()
