#include <boost/asio.hpp>
#include <boost/bind.hpp>
#include <boost/enable_shared_from_this.hpp>
#include <boost/shared_ptr.hpp>
#include <ctime>
#include <iostream>
#include <string>

using boost::asio::ip::tcp;

const int SERVER_PORT = 8023;

std::string make_daytime_string() {
    std::time_t now = time(0);
    return std::ctime(&now);
}

class tcp_connection : public boost::enable_shared_from_this<tcp_connection> {
public:
    typedef boost::shared_ptr<tcp_connection> pointer;

    static pointer create(boost::asio::io_service& io_service) { return pointer(new tcp_connection(io_service)); }

    tcp::socket& socket() { return socket_; }

    void start() {
        message_ = make_daytime_string();

        // rather than ip::tcp::socket::async_write_some(), it ensure that the entire block of data is sent
        boost::asio::async_write(
            socket_, boost::asio::buffer(message_),
            boost::bind(&tcp_connection::handle_write,  // callback
                        shared_from_this(),             // allows shared_ptr obtained within member function
                        boost::asio::placeholders::error, boost::asio::placeholders::bytes_transferred));
    }

private:
    tcp_connection(boost::asio::io_service& io_service) : socket_(io_service) {}

    void handle_write(const boost::system::error_code& error, size_t bytes_transferred) {
        // any further actions for this client connection are here
    }

    tcp::socket socket_;

    // use class member so that we keep the data valid until the asynchronous operation is complete
    std::string message_;
};

class tcp_server {
public:
    tcp_server(boost::asio::io_service& io_service) : acceptor_(io_service, tcp::endpoint(tcp::v4(), SERVER_PORT)) {
        start_accept();
    }

private:
    void start_accept() {
        tcp_connection::pointer new_connection = tcp_connection::create(acceptor_.get_io_service());

        acceptor_.async_accept(
            new_connection->socket(),  // client socket reference
            boost::bind(&tcp_server::handle_accept, this, new_connection, boost::asio::placeholders::error));
    }

    //  it services the client request, and then calls start_accept() to initiate the next accept operation.
    void handle_accept(tcp_connection::pointer new_connection, const boost::system::error_code& error) {
        if (!error) {
            new_connection->start();
        }
        start_accept();
    }

    tcp::acceptor acceptor_;
};

int main() {
    try {
        boost::asio::io_service io_service;
        tcp_server server(io_service);
        io_service.run();
    } catch (std::exception& e) {
        std::cerr << e.what() << std::endl;
    }
    return 0;
}
