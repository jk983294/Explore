#include <boost/asio.hpp>
#include <iostream>

int main(int argc, char* argv[]) {
    boost::asio::io_service io_service;
    boost::asio::io_service::work work(io_service);

    /*
     * work class is to inform the io_service when it has work to do.
     * in other words, as long as an io_service has a work object associated with it,
     * it will never run out of stuff to do
     */
    io_service.run();
    std::cout << "you should not see this line since io_service has a work to do" << std::endl;
    return 0;
}
