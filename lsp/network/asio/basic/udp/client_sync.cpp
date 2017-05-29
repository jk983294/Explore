#include <boost/array.hpp>
#include <boost/asio.hpp>
#include <iostream>

using boost::asio::ip::udp;

int main(int argc, char* argv[]) {
    try {
        boost::asio::io_service io_service;

        udp::resolver resolver(io_service);
        udp::resolver::query query(udp::v4(), "localhost", "8023");  // no need v6
        udp::endpoint receiver_endpoint = *resolver.resolve(query);  // only v4 version endpoint

        udp::socket socket(io_service);
        socket.open(udp::v4());

        // udp not connect concept, so need to send to server once then get data back
        boost::array<char, 1> send_buf = {{0}};
        socket.send_to(boost::asio::buffer(send_buf), receiver_endpoint);

        boost::array<char, 128> recv_buf;
        udp::endpoint sender_endpoint;
        size_t len = socket.receive_from(boost::asio::buffer(recv_buf), sender_endpoint);

        std::cout.write(recv_buf.data(), len);
    } catch (std::exception& e) {
        std::cerr << e.what() << std::endl;
    }

    return 0;
}
