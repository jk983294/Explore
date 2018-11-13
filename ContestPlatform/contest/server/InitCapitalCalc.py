from .AccountManager import AccountManager
import datetime


def calculate(dump_path, bench_time_str, penalty_per_minute):
    account_manager = AccountManager()
    account_manager.load_from_file(dump_path)
    bench_time = datetime.datetime.strptime(bench_time_str, "%Y%m%d.%H%M%S").timestamp()
    print("bench_time", bench_time)
    for user_id, account in account_manager.accounts.items():
        if account.finish_test_time is not None:
            init_capital = 1000000.0
            if bench_time < account.finish_test_time:
                init_capital -= ((account.finish_test_time - bench_time) / 60.0) * penalty_per_minute
                print("finish %d bench %d capital %d" % (account.finish_test_time, bench_time, init_capital))

            if init_capital < 0:
                init_capital = 0

            account.capital = init_capital
        else:
            account.capital = 0

        account.reset_except_capital()
    return account_manager


if __name__ == '__main__':
    from sys import argv
    if len(argv) == 5:
        dump_path, bench_time_str, penalty_per_minute, output_file = argv[1], argv[2], float(argv[3]), argv[4]
        account_manager = calculate(dump_path, bench_time_str, penalty_per_minute)
        account_manager.dump_to_file(output_file)
        print("account manager file generated to ", output_file)
    else:
        print("./InitCapitalCalc.py <dump_file> <bench_time> <penalty_per_minute> <output_file>")
