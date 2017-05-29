#include <boost/array.hpp>
#include <boost/asio.hpp>
#include <boost/bind.hpp>
#include <boost/shared_ptr.hpp>
#include <ctime>
#include <iostream>
#include <string>

using boost::asio::ip::udp;

const int SERVER_PORT = 8023;

std::string make_daytime_string() {
    std::time_t now = time(0);
    return std::ctime(&now);
}

class udp_server {
public:
    udp_server(boost::asio::io_service& io_service) : socket_(io_service, udp::endpoint(udp::v4(), SERVER_PORT)) {
        start_receive();
    }

private:
    void start_receive() {
        socket_.async_receive_from(
            boost::asio::buffer(recv_buffer_),        // buffer for client's send_to msg
            client_endpoint_,                         // populate with client info
            boost::bind(&udp_server::handle_receive,  // callback for client connection
                        this, boost::asio::placeholders::error, boost::asio::placeholders::bytes_transferred));
    }

    void handle_receive(const boost::system::error_code& error, std::size_t bytes_transferred) {
        if (!error || error == boost::asio::error::message_size) {
            // message keep alive while async send to
            boost::shared_ptr<std::string> message(new std::string(make_daytime_string()));

            socket_.async_send_to(boost::asio::buffer(*message), client_endpoint_,
                                  boost::bind(&udp_server::handle_send,  // callback for further client actions
                                              this, message, boost::asio::placeholders::error,
                                              boost::asio::placeholders::bytes_transferred));

            start_receive();  // start to serve next client
        }
    }

    void handle_send(boost::shared_ptr<std::string> message, const boost::system::error_code& error,
                     std::size_t bytes_transferred) {
        // further client action here
    }

    udp::socket socket_;
    udp::endpoint client_endpoint_;
    boost::array<char, 1> recv_buffer_;
};

int main() {
    try {
        boost::asio::io_service io_service;
        udp_server server(io_service);
        io_service.run();
    } catch (std::exception& e) {
        std::cerr << e.what() << std::endl;
    }
    return 0;
}
