import sys
import time
import json
from .utils import generate_random_string


class Account:
    def __init__(self, name_, id_, pin_):
        self.name = name_
        self.id = id_
        self.pin = pin_
        self.session_key = generate_random_string(6)
        self.capital = 1000000
        self.pnl = 0
        self.ir = 0
        self.current_dd = 0
        self.max_dd = 0
        self.score = 0
        self.pnl_list = []
        self.is_finish_test = False
        self.finish_test_time = None
        self.is_time_penalty = False
        self.is_money_penalty = False

    def new_session_key(self):
        self.session_key = generate_random_string(6)
        return self.session_key

    def reset_except_capital(self):
        self.session_key = generate_random_string(6)
        self.pnl = 0
        self.ir = 0
        self.current_dd = 0
        self.max_dd = 0
        self.score = 0
        self.pnl_list = []
        self.is_finish_test = False
        self.finish_test_time = None
        self.is_time_penalty = False
        self.is_money_penalty = False

    def __str__(self):
        return 'account name:%s id:%d pin:%s capital:%.2f pnl:%.2f ir:%.3f current_dd:%.2f max_dd:%.2f score:%.2f' % (
            self.name,
            self.id,
            self.pin,
            self.capital,
            self.pnl,
            self.ir,
            self.current_dd,
            self.max_dd,
            self.score
        )

    def to_json(self):
        return {
            "name": self.name,
            "id": self.id,
            "pin": self.pin,
            "capital": self.capital,
            "pnl": self.pnl,
            "ir": self.ir,
            "current_dd": self.current_dd,
            "max_dd": self.max_dd,
            "score": self.score,
            "pnl_list": self.pnl_list,
            "is_finish_test": self.is_finish_test,
            "finish_test_time": self.finish_test_time,
            "is_time_penalty": self.is_time_penalty,
            "is_money_penalty": self.is_money_penalty
        }

    def from_json(self, args):
        if args is None:
            return
        self.name = args["name"]
        self.id = args["id"]
        self.pin = args["pin"]
        self.capital = args["capital"]
        self.pnl = args["pnl"]
        self.ir = args["ir"]
        self.current_dd = args["current_dd"]
        self.max_dd = args["max_dd"]
        self.score = args["score"]
        self.pnl_list = args["pnl_list"]
        self.is_finish_test = args["is_finish_test"]
        self.finish_test_time = args["finish_test_time"]
        self.is_time_penalty = args["is_time_penalty"]
        self.is_money_penalty = args["is_money_penalty"]

    def finish_test(self):
        if self.is_finish_test:
            return False, "already finish"
        else:
            self.is_finish_test = True
            self.finish_test_time = time.time()
            return True, "finished success"

    def undo_finish_test(self):
        if self.is_finish_test:
            self.is_finish_test = False
            self.finish_test_time = None
            return True, "undo finished success"
        else:
            return False, "not finish yet"

    def penalty(self, money):
        self.pnl -= min(self.capital, money)
        if self.capital > money:
            self.capital -= money
        else:
            self.capital = 0

    def set_penalty_flag(self, penalty_type, status):
        if penalty_type == 'time':
            if status:
                if self.is_time_penalty:
                    return False, "already in time penalty status"
                else:
                    self.is_time_penalty = True
                    return True, "set to time penalty status success"
            else:
                if self.is_time_penalty:
                    self.is_time_penalty = False
                    return True, "set to non time penalty status success"
                else:
                    return False, "already in non time penalty status"
        elif penalty_type == 'money':
            if status:
                if self.is_money_penalty:
                    return False, "already in money penalty status"
                else:
                    self.is_money_penalty = True
                    return True, "set to money penalty status success"
            else:
                if self.is_money_penalty:
                    self.is_money_penalty = False
                    return True, "set to non money penalty status success"
                else:
                    return False, "already in non money penalty status"
        else:
            return False, 'unknown penalty_type'


class AccountManager:
    def __init__(self):
        self.accounts = {}

    def get_account(self, user_id):
        if user_id in self.accounts:
            return self.accounts[user_id]
        return None

    def add_account(self, user_name, user_id, user_pin):
        if user_id in self.accounts:
            return False
        account = Account(user_name, user_id, user_pin)
        self.accounts[user_id] = account
        return True

    def init_from_xml(self, config):
        if config:
            user_count = 0
            for node in config.findall('account'):
                try:
                    user_name = node.find('user_name').text
                    user_id = int(node.find('user_id').text)
                    user_pin = node.find('user_pin').text

                    if user_name and user_pin and user_id and self.add_account(user_name, user_id, user_pin):
                        user_count += 1
                except Exception as err:
                    print('ERROR: Cannot initialize account. (%s)' % str(err))
                    raise err

            print("read %d accounts from config" % user_count)
            if config.find('init_dump_file') is not None:
                self.load_from_file(config.find('init_dump_file').text)
        else:
            print("no account config found.", file=sys.stderr)

    # used by front end
    def get_all_accounts(self):
        result = []
        for key, value in self.accounts.items():
            result.append(value.to_json())
        return result

    def dump_to_file(self, file_path):
        count = 0
        with open(file_path, "wt", encoding='utf-8') as f:
            for key, value in self.accounts.items():
                print(json.dumps(value.to_json(), ensure_ascii=False), file=f)
                count += 1
        result = "dump %d account to file %s" % (count, file_path)
        return True, result

    def load_from_file(self, file_path):
        count = 0
        with open(file_path, 'rt', encoding='utf-8') as f:
            lines = (line.strip() for line in f)
            for line in lines:
                account_json = json.loads(line, encoding='utf-8')
                if account_json and "id" in account_json:
                    account = self.get_account(account_json["id"])
                    if not account:
                        print("create account for ", account_json["id"])
                        self.add_account(account_json["name"], account_json["id"], account_json["pin"])
                        account = self.get_account(account_json["id"])
                    print("init account %d from file record" % account_json["id"])
                    account.from_json(account_json)
                    count += 1

        result = "load %d account from file %s" % (count, file_path)
        return True, result

    def penalty(self, user_id, money):
        account = self.get_account(user_id)
        if account:
            account.penalty(money)
            return True, 'penalty success'
        else:
            return False, 'cannot find account %d' % user_id
