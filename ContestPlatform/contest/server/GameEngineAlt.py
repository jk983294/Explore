import random
import numpy as np


class GameEngineAlt:
    def __init__(self, prob_file, payoff_file):
        self.dist_list = []
        self.payoff_list = []
        for line in open(prob_file):
            prob = line.split(',')
            for i in range(len(prob)):
                prob[i] = float(prob[i])
            self.dist_list.append(prob)
        for line in open(payoff_file):
            payoff = line.split(',')
            for i in range(len(payoff)):
                payoff[i] = float(payoff[i])
            self.payoff_list.append(payoff)

    def get_stock_distribution(self):
        result = self.dist_list[random.randint(0, 3)]
        return result

    def get_payoffs(self, stock_dist):
        chosen_payoffs = []
        is_chosen = [False] * 25
        for itr in range(4):
            index = random.randint(0, 24)
            if is_chosen[index]:
                index = random.randint(0, 24)
            result = np.array(self.payoff_list[index])
            std = self.stddev(np.array(stock_dist), result)
            adjev = (2 * random.randint(0, 1) - 1) * np.random.normal(0.003, 0.0005, 1)[0]
            adjstd = np.random.normal(0.03, 0.003, 1)[0]
            if adjstd < 0.01:
                adjstd = 0.01
            result *= adjstd / std
            ev = np.dot(np.array(stock_dist), result)
            result += adjev - ev
            flag = True
            for i in range(len(result)):
                if abs(result[i]) > 1:
                    result[i] = abs(result[i]) / result[i]
            is_chosen[index] = True
            chosen_payoffs.append(list(result))
        return chosen_payoffs

    # Internal Function
    def stddev(self, prob, payoff):
        ex2 = np.dot(prob, payoff ** 2)
        ex = np.dot(prob, payoff)
        return (ex2 - ex ** 2) ** 0.5
