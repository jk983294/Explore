import random


def get_stock_distribution():
    result = []
    for itr in range(5):
        result.append(random.random())
    return result


def get_payoff():
    result = []
    for itr in range(5):
        result.append(random.random())
    return result


def get_payoffs():
    result = []
    for itr in range(4):
        result.append(get_payoff())
    return result
