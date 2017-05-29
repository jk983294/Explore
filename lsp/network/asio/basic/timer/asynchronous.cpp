#include <boost/asio.hpp>
#include <boost/date_time/posix_time/posix_time.hpp>
#include <iostream>

void print(const boost::system::error_code& e) { std::cout << "Hello, world!" << std::endl; }

int main() {
    boost::asio::io_service io;

    boost::asio::deadline_timer t(io, boost::posix_time::seconds(5));
    boost::asio::deadline_timer t1(io, boost::posix_time::seconds(3));

    t.async_wait(&print);
    t1.async_wait(&print);

    io.run();
    return 0;
}
