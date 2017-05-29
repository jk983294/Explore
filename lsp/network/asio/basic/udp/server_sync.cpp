#include <boost/array.hpp>
#include <boost/asio.hpp>
#include <ctime>
#include <iostream>
#include <string>

using boost::asio::ip::udp;

const int SERVER_PORT = 8023;

std::string make_daytime_string() {
    std::time_t now = time(0);
    return std::ctime(&now);
}

int main() {
    try {
        boost::asio::io_service io_service;

        udp::socket socket(io_service, udp::endpoint(udp::v4(), SERVER_PORT));

        for (;;) {
            boost::array<char, 1> recv_buf;
            // Wait for a client to initiate contact. client_endpoint will be populated by socket.receive_from()
            udp::endpoint client_endpoint;
            boost::system::error_code error;
            socket.receive_from(boost::asio::buffer(recv_buf), client_endpoint, 0, error);

            if (error && error != boost::asio::error::message_size) throw boost::system::system_error(error);

            std::string message = make_daytime_string();

            boost::system::error_code ignored_error;
            socket.send_to(boost::asio::buffer(message), client_endpoint, 0, ignored_error);
        }
    } catch (std::exception& e) {
        std::cerr << e.what() << std::endl;
    }
    return 0;
}
