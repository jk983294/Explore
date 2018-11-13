from .AccountManager import AccountManager


class GlobalInfo:
    def __init__(self):
        self.accountManager = AccountManager()
        self.server_info = {}
        self.question_publisher = None
        self.answer_service = None
        self.game_engine = None
        self.pnl_service = None
        self.mode = 'test'              # test final
        self.logger = None
        self.dump_prefix = '/tmp/contest.dump.'
        self.update_interval = 5        # seconds
