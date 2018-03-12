#include <sys/epoll.h>
#include <sys/timerfd.h>
#include <unistd.h>
#include <cstring>
#include <iostream>

using namespace std;

bool destroy_timer(int* timerFd) {
    struct itimerspec newTime = {{0, 0}, {0, 0}};
    struct itimerspec oldTime = {{0, 0}, {0, 0}};
    if (timerfd_settime(*timerFd, 0, &newTime, &oldTime) < 0) {
        cout << "Failed to reset timer " << *timerFd << " :" << errno << " " << strerror(errno);
    }
    close(*timerFd);
    *timerFd = -1;
    return true;
}

bool create_timer(uint32_t intervalMilliseconds, int* timerFd) {
    bool rc = true;

    int fd = timerfd_create(CLOCK_REALTIME, TFD_NONBLOCK | TFD_CLOEXEC);
    if (fd < 0) {
        cout << "Failed to make timerFd " << errno << " " << strerror(errno);
        rc = false;
    } else {
        *timerFd = fd;
        uint32_t s = intervalMilliseconds / 1000;
        uint32_t m = intervalMilliseconds - s * 1000;
        struct itimerspec newTime = {{s, m * 1000000}, {s, m * 1000000}};
        if (timerfd_settime(*timerFd, 0, &newTime, nullptr) < 0) {
            cout << "Failed to arm timer" << errno << " " << strerror(errno);
            destroy_timer(timerFd);
            rc = false;
        }
    }
    return rc;
}

int main() {
    int nfds, fdEpoll{-1}, fdHeartbeatTimer{-1};
    epoll_event inEvent;
    epoll_event outEvent[128];

    if ((fdEpoll = epoll_create(1)) < 0) {
        cout << "Failed on epoll_create " << errno << " " << strerror(errno);
        return -1;
    }

    inEvent.events = EPOLLIN;

    if (create_timer(1 * 1000, &fdHeartbeatTimer)) {
        inEvent.data.fd = fdHeartbeatTimer;
        epoll_ctl(fdEpoll, EPOLL_CTL_ADD, fdHeartbeatTimer, &inEvent);
    }

    while (1) {
        nfds = epoll_wait(fdEpoll, outEvent, sizeof(outEvent) / sizeof(outEvent[0]), 1);
        if (nfds == -1) {
            cout << "ERROR: epoll_wait  " << strerror(errno);
            continue;
        }
        for (int n = 0; n < nfds; ++n) {
            int fdReady = outEvent[n].data.fd;
            if (fdReady == fdHeartbeatTimer) {
                uint64_t dummy;
                read(fdReady, &dummy, sizeof(dummy));
                cout << "heart beat" << endl;
            }
        }
    }
    return 0;
}
