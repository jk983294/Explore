#include <memory.h>
#include <netdb.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <zconf.h>
#include <algorithm>
#include <iostream>
#include <numeric>
#include <thread>
#include <vector>
#include "Data.h"

using namespace std;

double compute(const Data &data) {
    double result = 0;
    for (long i = 0; i < data.i; ++i) {
        result += (data.d1 * data.d2) * (i % 8);
    }
    return result;
}

void error(const char *msg) {
    perror(msg);
    exit(0);
}

template <typename Iterator, typename T>
struct accumulate_block {
    void operator()(Iterator first, Iterator last, T &result) {
        double localResult = 0;
        for (auto i = first; i < last; ++i) {
            localResult += compute(*i);
        }
        result = localResult;
    }
};

template <typename Iterator, typename T>
T parallel_accumulate(Iterator first, Iterator last, T init) {
    long const length = std::distance(first, last);

    if (!length) return init;

    unsigned long const min_per_thread = 25;
    unsigned long const max_threads = (length + min_per_thread - 1) / min_per_thread;
    unsigned long const hardware_threads = std::thread::hardware_concurrency();  // hint number
    unsigned long const num_threads = std::min(hardware_threads != 0 ? hardware_threads : 2, max_threads);
    unsigned long const block_size = length / num_threads;

    std::vector<T> results(num_threads, 0);
    std::vector<std::thread> threads(num_threads - 1);

    Iterator block_start = first;
    for (unsigned long i = 0; i < (num_threads - 1); ++i) {
        Iterator block_end = block_start;
        std::advance(block_end, block_size);
        threads[i] = std::thread(accumulate_block<Iterator, T>(), block_start, block_end, std::ref(results[i]));
        block_start = block_end;
    }
    accumulate_block<Iterator, T>()(block_start, last, std::ref(results[num_threads - 1]));

    std::for_each(threads.begin(), threads.end(), std::mem_fn(&std::thread::join));  // wait for all finish
    return std::accumulate(results.begin(), results.end(), init);
}

int main(int argc, char *argv[]) {
    if (argc < 3) {
        cout << "usage: ./client <ip> <port>" << endl;
        return -1;
    }

    struct sockaddr_in serv_addr;

    short portno = atoi(argv[2]);
    int sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0) error("ERROR opening socket");

    struct hostent *server;
    server = gethostbyname(argv[1]);  // DNS resolve to server info
    if (server == NULL) error("ERROR, no such host");

    memset(&serv_addr, 0, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    memcpy(&serv_addr.sin_addr.s_addr, server->h_addr, server->h_length);
    serv_addr.sin_port = htons(portno);

    if (connect(sockfd, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0) error("ERROR connecting");

    Data data[1000];
    memset(&data, 0, sizeof(serv_addr) * 1000);
    char *buffer = reinterpret_cast<char *>(data);
    int recved = 0, rtn, toRecv = sizeof(Data) * 1000;
    while (recved < toRecv) {
        rtn = read(sockfd, buffer, toRecv - recved);
        if (rtn <= 0) {
            printf("recv failed, sockfd:%d, errno:%d, already recved:%d, rtn:%d\n", sockfd, errno, recved, rtn);
            exit(1);
        }
        recved += rtn;
        buffer += rtn;
    }
    close(sockfd);

    double result = parallel_accumulate(begin(data), end(data), 0.0);
    //    double result = 0;
    //    for (int i = 0; i < 1000; ++i) {
    //        result += compute(data[i]);
    //    }

    printf("average is %f\n", result / 1000);  // average is 1709399998.947490
    return 0;
}
