#include <boost/asio.hpp>
#include <iostream>
#include <string>
#include "boost/bind.hpp"

const short multicast_port = 30001;

class receiver {
public:
    receiver(boost::asio::io_service& io_service, const boost::asio::ip::address& listen_address,
             const boost::asio::ip::address& multicast_address)
        : socket_(io_service) {
        boost::asio::ip::udp::endpoint listen_endpoint(listen_address, multicast_port);
        socket_.open(listen_endpoint.protocol());
        socket_.set_option(boost::asio::ip::udp::socket::reuse_address(true));

        /**
         * bind a UDP socket when receiving multicast means to specify an address and port from which to receive data
         * the socket will only receive datagrams sent to that multicast address & port,
         * no matter what groups are subsequently joined by the socket.
         */
        socket_.bind(listen_endpoint);

        socket_.set_option(boost::asio::ip::multicast::join_group(multicast_address));

        socket_.async_receive_from(boost::asio::buffer(data_, max_length), sender_endpoint_,
                                   boost::bind(&receiver::handle_receive_from, this, boost::asio::placeholders::error,
                                               boost::asio::placeholders::bytes_transferred));
    }

    void handle_receive_from(const boost::system::error_code& error, size_t bytes_recvd) {
        if (!error) {
            std::cout.write(data_, bytes_recvd);
            std::cout << std::endl;

            socket_.async_receive_from(
                boost::asio::buffer(data_, max_length), sender_endpoint_,
                boost::bind(&receiver::handle_receive_from, this, boost::asio::placeholders::error,
                            boost::asio::placeholders::bytes_transferred));
        }
    }

private:
    boost::asio::ip::udp::socket socket_;
    boost::asio::ip::udp::endpoint sender_endpoint_;
    enum { max_length = 1024 };
    char data_[max_length];
};

int main(int argc, char* argv[]) {
    try {
        /**
         * When you bind to "0.0.0.0" (INADDR_ANY), you are basically telling the TCP/IP layer to choose the best NIC
         * for sending/receiving. when you want to send/receive on a specific network adapter, then you don't set it to
         * "0.0.0.0"
         */
        std::string listen_address = "0.0.0.0";
        std::string multicast_address = "239.255.80.23";

        boost::asio::io_service io_service;
        receiver r(io_service, boost::asio::ip::address::from_string(listen_address),
                   boost::asio::ip::address::from_string(multicast_address));
        io_service.run();
    } catch (std::exception& e) {
        std::cerr << "Exception: " << e.what() << "\n";
    }
    return 0;
}
