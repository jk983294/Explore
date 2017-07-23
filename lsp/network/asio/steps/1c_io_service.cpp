#include <boost/asio.hpp>
#include <iostream>

int main(int argc, char* argv[]) {
    boost::asio::io_service io_service;

    /*
     * The poll() function runs handlers that are ready to run, without blocking,
     * until the io_service has been stopped or there are no more ready handlers.
     *
     * To get the io_service working for us, we have to use the run or poll family of functions.
     * Run will block and wait for work if we assign it a work object while the poll function does not
     */
    for (int x = 0; x < 42; ++x) {
        io_service.poll();
        std::cout << "Counter: " << x << std::endl;
    }
    return 0;
}
