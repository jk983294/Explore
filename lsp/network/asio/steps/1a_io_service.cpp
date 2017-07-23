#include <boost/asio.hpp>
#include <iostream>

int main(int argc, char* argv[]) {
    boost::asio::io_service io_service;

    /*
     * the run() function blocks until all work has finished and there are no more handlers to be dispatched,
     * or until the io_service has been stopped.
     * we are not really giving it anything to do explicitly, so the function should not block
     */
    io_service.run();
    std::cout << "you should see this line since io_service has no work to do" << std::endl;
    return 0;
}
