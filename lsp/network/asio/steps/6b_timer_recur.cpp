#include <boost/asio.hpp>
#include <boost/bind.hpp>
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

void TimerHandler(const boost::system::error_code& error, boost::shared_ptr<boost::asio::deadline_timer> timer) {
    if (error) {
        global_stream_lock.lock();
        std::cout << "[" << boost::this_thread::get_id() << "] error: " << error << std::endl;
        global_stream_lock.unlock();
    } else {
        global_stream_lock.lock();
        std::cout << "[" << boost::this_thread::get_id() << "] timerHandler " << std::endl;
        global_stream_lock.unlock();

        timer->expires_from_now(boost::posix_time::seconds(5));
        timer->async_wait(boost::bind(&TimerHandler, _1, timer));
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

    // a timer that fires every 5 seconds
    boost::shared_ptr<boost::asio::deadline_timer> timer(new boost::asio::deadline_timer(*io_service));
    timer->expires_from_now(boost::posix_time::seconds(5));
    // _1 means the first parameter, which will be supplied later
    timer->async_wait(boost::bind(&TimerHandler, _1, timer));

    std::cin.get();

    io_service->stop();
    worker_threads.join_all();
    return 0;
}
