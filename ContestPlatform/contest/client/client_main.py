from __future__ import print_function
import os
import time
import copy
import os.path as path
import numpy as np
from xml.etree import ElementTree
from .QuestionClient import QuestionClient
from .ContestClient import ContestClient


def stddev(prob, payoff):
    ex2 = np.dot(prob, payoff ** 2)
    ex = np.dot(prob, payoff)
    return (ex2 - ex ** 2) ** 0.5


def corr(prob, payoff1, payoff2):
    ex = np.dot(prob, payoff1)
    ey = np.dot(prob, payoff2)
    exy = np.dot(prob, payoff1 * payoff2)
    return (exy - ex * ey) / stddev(prob, payoff1) / stddev(prob, payoff2)


def naive_answer(capital, price_distribution, payoffs):
    print(capital, price_distribution, payoffs)
    return [0.25, 0.25, 0.25, 0.25]


def answer_maxratio(capital, price_distribution, payoffs):
    result = []
    max_payoff = 0
    max_evstd = 0
    opt_std = 1
    for i in range(4):
        ev = np.dot(np.array(price_distribution), np.array(payoffs[i]))
        std = stddev(np.array(price_distribution), np.array(payoffs[i]))
        evstd = ev / std
        if abs(evstd) > abs(max_evstd):
            max_evstd = evstd
            max_payoff = i
            opt_std = std
    for i in range(4):
        weight = 0
        if max_payoff == i:
            weight = max_evstd / 0.1 * opt_std / 0.05
            if weight > 0.8:
                weight = 0.8
            elif weight < -0.8:
                weight = -0.8
        result.append(weight)
    return result


def answer_ratiocomb(capital, price_distribution, payoffs):
    result = []
    sumweight = 0
    for i in range(4):
        ev = np.dot(np.array(price_distribution), np.array(payoffs[i]))
        std = stddev(np.array(price_distribution), np.array(payoffs[i]))
        evstd = ev / std
        weight = evstd / 0.1 * std / 0.05
        sumweight += abs(weight)
        result.append(weight)
    resultpf = np.array([0.0] * 100)
    for i in range(4):
        if sumweight > 1:
            result[i] /= sumweight
        resultpf += np.array(payoffs[i]) * result[i]
    #print(3, np.dot(np.array(price_distribution), resultpf), stddev(np.array(price_distribution), resultpf))
    return result


def answer_mtcl(capital, price_distribution, payoffs, interval):
    weight = [0] * 4
    max_evstd = 0
    max_ev3std2 = 0
    opt_std = 1
    for i in range(interval + 1):
        for j in range(interval + 1 - i):
            for k in range(interval + 1 - i - j):
                for ii in range(-1, 2, 2):
                    for jj in range(-1, 2, 2):
                        for kk in range(-1, 2, 2):
                            for ll in range(-1, 2, 2):
                                l = interval - i - j - k
                                wgt = []
                                wgt.append(i * ii / interval)
                                wgt.append(j * jj / interval)
                                wgt.append(k * kk / interval)
                                wgt.append(l * ll / interval)
                                pf = np.array(payoffs[0]) * wgt[0]
                                pf += np.array(payoffs[1]) * wgt[1]
                                pf += np.array(payoffs[2]) * wgt[2]
                                pf += np.array(payoffs[3]) * wgt[3]
                                ev = np.dot(np.array(price_distribution), pf)
                                std = stddev(np.array(price_distribution), pf)
                                if ev / std > max_evstd:
                                    max_evstd = ev / std
                                    max_ev3std2 = ev ** 3 / std ** 2
                                    opt_std = std
                                    weight = copy.deepcopy(wgt)
    #print(4, max_evstd * opt_std, max_evstd)
    #f = max_evstd / (max_evstd + 0.25)
    # for i in range(4):
    #    weight[i] *= f
    return weight


def answer_mtcl2(capital, price_distribution, payoffs, interval):
    weight = [0] * 4
    max_evstd = 0
    max_ev3std2 = 0
    opt_std = 1
    for i in range(interval + 1):
        for j in range(interval + 1 - i):
            for k in range(interval + 1 - i - j):
                for ii in range(-1, 2, 2):
                    for jj in range(-1, 2, 2):
                        for kk in range(-1, 2, 2):
                            for ll in range(-1, 2, 2):
                                l = interval - i - j - k
                                wgt = []
                                wgt.append(i * ii / interval)
                                wgt.append(j * jj / interval)
                                wgt.append(k * kk / interval)
                                wgt.append(l * ll / interval)
                                pf = np.array(payoffs[0]) * wgt[0]
                                pf += np.array(payoffs[1]) * wgt[1]
                                pf += np.array(payoffs[2]) * wgt[2]
                                pf += np.array(payoffs[3]) * wgt[3]
                                ev = np.dot(np.array(price_distribution), pf)
                                std = stddev(np.array(price_distribution), pf)
                                if ev ** 3 / std ** 2 > max_ev3std2:
                                    max_evstd = ev / std
                                    max_ev3std2 = ev ** 3 / std ** 2
                                    opt_std = std
                                    weight = copy.deepcopy(wgt)
    #print(5, max_evstd * opt_std, max_evstd)
    #f = max_ev3std2 / (max_ev3std2 + 0.04 * 0.003)
    # for i in range(4):
    #    weight[i] *= f
    return weight


def run(user_name, user_id, user_pin, question_endpoint, answer_endpoint, mode='test'):
    try:
        print(user_name, user_id, user_pin, question_endpoint, answer_endpoint)
        # Create clients
        question_client = QuestionClient(question_endpoint, user_id)
        contest_client = ContestClient(answer_endpoint)
        print("clients init success")
    except Exception as err:
        print('ERROR: Cannot initialize client. (%s)' % str(err))
        raise err

    time.sleep(0.5)  # Wait for server connection

    print("going to login")
    is_success, reason, init_capital, session_key = contest_client.login(user_id, user_pin)

    if not is_success:
        print('login failed due to ', reason)
        return

    print("login success with init capital %d session key %s" % (init_capital, session_key))
    for question in question_client.get_question():
        invest_ratio = []
        if user_id == 1:
            invest_ratio = naive_answer(question["capital"], question["price_distribution"], question["payoffs"])
        elif user_id == 2:
            invest_ratio = answer_maxratio(question["capital"], question["price_distribution"], question["payoffs"])
        elif user_id == 3:
            invest_ratio = answer_ratiocomb(question["capital"], question["price_distribution"], question["payoffs"])
        elif user_id == 4:
            invest_ratio = answer_mtcl(question["capital"], question["price_distribution"], question["payoffs"], 30)
        elif user_id == 5:
            invest_ratio = answer_mtcl2(question["capital"], question["price_distribution"], question["payoffs"], 30)
        else:
            invest_ratio = naive_answer(question["capital"], question["price_distribution"], question["payoffs"])

        print(user_id, invest_ratio)
        response = contest_client.submit_answer(question["sequence"], invest_ratio)
        if not response["accepted"]:
            print(response["reason"])

    print("finish all question")


def main():
    if len(os.sys.argv) != 2:
        print("Missing configuration filename.")
        print("USE: python3 -m contest.client.client_main config_file.xml")
        exit(0)

    config_filename = os.sys.argv[1]
    if not config_filename.endswith('.xml'):
        config_filename += '.xml'

    if not path.exists(config_filename):
        print('ERROR: Config file does not exist.')
        return

    mode = 'test'
    try:
        root = ElementTree.parse(config_filename).getroot()
        if root.find('mode') is not None:
            mode = root.find('mode').text
        config = ElementTree.parse(config_filename).getroot().find('client')
        user_name = config.find('user_name').text
        user_id = int(config.find('user_id').text)
        user_pin = config.find('user_pin').text
        question_endpoint = config.find('question_front').text
        answer_endpoint = config.find('answer_front').text
    except Exception as err:
        print('ERROR: Cannot initialize client. (%s)' % str(err))
        raise err

    run(user_name, user_id, user_pin, question_endpoint, answer_endpoint, mode)


if __name__ == '__main__':
    main()
