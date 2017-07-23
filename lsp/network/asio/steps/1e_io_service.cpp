#include <boost/asio.hpp>
#include <boost/shared_ptr.hpp>
#include <iostream>

int main(int argc, char* argv[]) {
    boost::asio::io_service io_service;
    boost::shared_ptr<boost::asio::io_service::work> work(new boost::asio::io_service::work(io_service));

    /*
     * this type of functionality is important in the case we want to gracefully
     * finish all pending work but not stop it prematurely.
     */
    work.reset();
    io_service.run();
    std::cout << "you should see this line since work is removed" << std::endl;
    return 0;
}
