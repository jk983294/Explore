#include <boost/asio.hpp>
#include <boost/lexical_cast.hpp>
#include <boost/shared_ptr.hpp>
#include <boost/thread.hpp>
#include <boost/thread/mutex.hpp>
#include <iostream>

using namespace std;

boost::mutex global_stream_lock;

void WorkerThread(boost::shared_ptr<boost::asio::io_service> io_service) {
    global_stream_lock.lock();
    std::cout << "[" << boost::this_thread::get_id() << "] thread start" << std::endl;
    global_stream_lock.unlock();

    while (true) {
        try {
            boost::system::error_code ec;
            io_service->run(ec);
            if (ec) {
                global_stream_lock.lock();
                std::cout << "[" << boost::this_thread::get_id() << "] error: " << ec << std::endl;
                global_stream_lock.unlock();
            }
            break;
        } catch (std::exception& ex) {
            global_stream_lock.lock();
            std::cout << "[" << boost::this_thread::get_id() << "] exception: " << ex.what() << std::endl;
            global_stream_lock.unlock();
        }
    }

    global_stream_lock.lock();
    std::cout << "[" << boost::this_thread::get_id() << "] thread finish" << std::endl;
    global_stream_lock.unlock();
}

void OnConnect(const boost::system::error_code& ec, boost::shared_ptr<boost::asio::ip::tcp::socket> sock) {
    if (ec) {
        global_stream_lock.lock();
        std::cout << "[" << boost::this_thread::get_id() << "] error: " << ec << std::endl;
        global_stream_lock.unlock();
    } else {
        global_stream_lock.lock();
        std::cout << "[" << boost::this_thread::get_id() << "] connected!" << std::endl;
        global_stream_lock.unlock();
    }
}

int main(int argc, char* argv[]) {
    boost::shared_ptr<boost::asio::io_service> io_service(new boost::asio::io_service);
    boost::shared_ptr<boost::asio::io_service::work> work(new boost::asio::io_service::work(*io_service));

    global_stream_lock.lock();
    std::cout << "[" << boost::this_thread::get_id() << "] press enter to exit." << std::endl;
    global_stream_lock.unlock();

    boost::thread_group worker_threads;
    for (int x = 0; x < 2; ++x) {
        worker_threads.create_thread(boost::bind(&WorkerThread, io_service));
    }

    /**
     * we have to use a boost::shared_ptr with most boost::asio objects if we wish to pass them around.
     * this is because the objects themselves are non-copyable and we have to ensure
     * the object remains valid while the handler is waiting to be called
     */
    boost::shared_ptr<boost::asio::ip::tcp::socket> sock(new boost::asio::ip::tcp::socket(*io_service));

    try {
        boost::asio::ip::tcp::resolver resolver(*io_service);
        boost::asio::ip::tcp::resolver::query query("www.baidu.com", boost::lexical_cast<std::string>(80));
        boost::asio::ip::tcp::resolver::iterator iterator = resolver.resolve(query);
        boost::asio::ip::tcp::endpoint endpoint = *iterator;

        global_stream_lock.lock();
        std::cout << "connecting to: " << endpoint << std::endl;  // netstat -n can look up this address
        global_stream_lock.unlock();

        sock->async_connect(endpoint, boost::bind(OnConnect, _1, sock));
    } catch (std::exception& ex) {
        global_stream_lock.lock();
        std::cout << "[" << boost::this_thread::get_id() << "] exception: " << ex.what() << std::endl;
        global_stream_lock.unlock();
    }

    std::cin.get();

    boost::system::error_code ec;
    sock->shutdown(boost::asio::ip::tcp::socket::shutdown_both, ec);
    sock->close(ec);
    io_service->stop();
    worker_threads.join_all();
    return 0;
}
