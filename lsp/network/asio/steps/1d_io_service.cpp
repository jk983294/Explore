#include <boost/asio.hpp>
#include <iostream>

int main(int argc, char* argv[]) {
    boost::asio::io_service io_service;
    boost::asio::io_service::work work(io_service);

    /*
     * the poll function will not block while there is more work to do.
     * it simply executes the current set of work and then returns
     *
     * if new work was added from inside the work handler invoked by the io_service,
     * then poll should never run out of work to do since new work would always be added.
     * however, this is clearly not the case. Work is added outside the handler so everything will work as intended
     */
    for (int x = 0; x < 42; ++x) {
        io_service.poll();
        std::cout << "Counter: " << x << std::endl;
    }
    return 0;
}
