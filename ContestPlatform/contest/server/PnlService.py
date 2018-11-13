import time
import threading
import random
import numpy as np


class PnlService:
    def __init__(self, global_info):
        self._is_started = False
        self.questions = global_info.question_publisher.questions
        self.answers = global_info.answer_service.answers
        self.account_manager = global_info.accountManager
        self.dump_prefix = global_info.dump_prefix
        self.mode = global_info.mode
        self._update_interval = global_info.update_interval  # seconds
        self.logger = global_info.logger

        self._updater = threading.Thread(target=self.calculation_thread)

    def start(self):
        if self._is_started:
            raise NotImplementedError

        self._is_started = True
        self._updater.start()

    def stop(self):
        if not self._is_started:
            raise NotImplementedError
        self._is_started = False

    def calculation_thread(self):
        while True:
            ts = time.time()
            if self.questions and (len(self.questions) > 1 or (ts - self.questions[0]["timestamp"] > self._update_interval)):
                question = self.questions.popleft()
                this_round_answers = self.get_current_round_answers(question["sequence"])
                # print("calculation_thread", question, this_round_answers)
                # calculate pnl and update accounts in account_manager
                this_round_scenario = self.get_current_round_scenario(question["distribution"])
                this_round_pnl = {}
                for i in self.account_manager.accounts:
                    this_round_pnl[i] = 0
                for i in range(len(this_round_answers)):
                    user_id = this_round_answers[i]["user_id"]
                    for j in range(4):
                        this_round_pnl[user_id] += (
                            this_round_answers[i]["invest_ratio"][j] *
                            question["payoffs"][j][this_round_scenario] *
                            self.account_manager.accounts[user_id].capital
                        )
                    self.account_manager.accounts[user_id].capital += this_round_pnl[user_id]

                for user_id, account in self.account_manager.accounts.items():
                    if account.is_money_penalty:
                        account.penalty(1000)
                        self.logger.info("%d money penalty 1000" % user_id)

                    account.pnl_list.append(this_round_pnl[user_id])
                    account.pnl += this_round_pnl[user_id]
                    mean = np.mean(np.array(account.pnl_list))
                    std = np.std(np.array(account.pnl_list))

                    if len(account.pnl_list) >= 2:
                        if std == 0:
                            if mean > 0:
                                account.ir = float("inf")
                            elif mean < 0:
                                account.ir = float("-inf")
                            else:
                                account.ir = 0.0
                        else:
                            account.ir = mean / std

                    account.current_dd -= this_round_pnl[user_id]
                    if account.current_dd < 0:
                        account.current_dd = 0
                    if account.current_dd > account.max_dd:
                        account.max_dd = account.current_dd
                    account.score = account.pnl - 2 * account.max_dd

                    # print(
                    #     "user_id:%d sequence:%d this_round_pnl:%f capital:%f ir:%f max_dd:%f score:%f" %
                    #     (i, question["sequence"], this_round_pnl[user_id], account.capital,
                    #         account.ir, account.max_dd, account.score))

                self.account_manager.dump_to_file("%s.%d" % (self.dump_prefix, question["sequence"]))
            else:
                time.sleep(0.2)

    def get_current_round_answers(self, sequence):
        result_dict = {}
        while True:
            if self.answers:
                if self.answers[0]["sequence"] < sequence:
                    self.answers.popleft()
                elif self.answers[0]["sequence"] == sequence:
                    user_id = self.answers[0]["user_id"]
                    if user_id in result_dict:
                        pass
                        # print("find dupe answer for id", user_id)
                    result_dict[user_id] = self.answers.popleft()
                else:
                    break
            else:
                break
        return list(result_dict.values())

    def get_current_round_scenario(self, distribution):
        rand = random.random()
        sum_prob = 0
        for i in range(len(distribution)):
            sum_prob += distribution[i]
            if sum_prob > rand:
                return i
        return len(distribution) - 1
