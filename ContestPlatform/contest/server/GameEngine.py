import random


class GameEngine:
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

    def get_payoffs(self):
        chosen_payoffs = []
        is_chosen = [False] * 25
        for itr in range(4):
            index = random.randint(0, 24)
            while is_chosen[index]:
                index = random.randint(0, 24)
            chosen_payoffs.append(self.payoff_list[index])
            is_chosen[index] = True
        return chosen_payoffs
