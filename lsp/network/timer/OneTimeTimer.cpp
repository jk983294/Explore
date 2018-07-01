#include <iostream>
#include <thread>

using namespace std;
using namespace std::chrono;

class OneTimeTimer {
public:
    OneTimeTimer() {
        innerThread = std::thread([this] { work(); });
    }

    ~OneTimeTimer() {
        if (innerThread.joinable()) {
            innerThread.join();
        }
    }

    void work() {
        time_t sleepTime = sleep_time();
        cout << "timer will wake up after " << sleepTime << " seconds" << endl;
        std::this_thread::sleep_for(std::chrono::seconds(sleepTime));

        cout << "do work" << endl;
    }

    int sleep_time() {
        time_t now = time(nullptr);
        struct tm myTm;
        localtime_r(&now, &myTm);
        time_t secondSinceMidnight = myTm.tm_hour * 60 * 60 + myTm.tm_min * 60 + myTm.tm_sec;
        int targetHour = 21;
        int targetMinute = 24;

        int targetWakeUpTime = static_cast<int>(now - secondSinceMidnight + targetHour * 60 * 60 + targetMinute * 60);
        int sleepTime = static_cast<int>(targetWakeUpTime - now);
        if (sleepTime < 0) {
            sleepTime += 24 * 60 * 60;  // next day's target time
        }
        return sleepTime;
    }

private:
    std::thread innerThread;
};

int main() {
    OneTimeTimer test;
    return 0;
}
