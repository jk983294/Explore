#include <boost/asio.hpp>
#include <boost/shared_ptr.hpp>
#include <boost/thread.hpp>
#include <boost/thread/mutex.hpp>
#include <iostream>

/**
 * The std::cout object is a global object.
 * Writing to it from different threads at once can cause output formatting issues
 */
boost::mutex global_stream_lock;

void WorkerThread(boost::shared_ptr<boost::asio::io_service> io_service) {
    global_stream_lock.lock();
    std::cout << "[" << boost::this_thread::get_id() << "] thread Start" << std::endl;
    global_stream_lock.unlock();

    io_service->run();

    global_stream_lock.lock();
    std::cout << "[" << boost::this_thread::get_id() << "] thread Finish" << std::endl;
    global_stream_lock.unlock();
}

int main(int argc, char* argv[]) {
    /**
     * if we were to try to use io_service with boost::bind, we would get a non-copyable error,
     * since the io_service cannot be copied and that is what boost::bind does for us behind the scenes.
     * to get around this, we must make use of shared_ptr again.
     * the same applies for many other non-copyable objects as well;
     * we have to wrap them in shared_ptrs to pass them if we need to
     */
    boost::shared_ptr<boost::asio::io_service> io_service(new boost::asio::io_service);
    boost::shared_ptr<boost::asio::io_service::work> work(new boost::asio::io_service::work(*io_service));

    global_stream_lock.lock();
    std::cout << "[" << boost::this_thread::get_id() << "] press enter to exit." << std::endl;
    global_stream_lock.unlock();

    boost::thread_group worker_threads;
    for (int x = 0; x < 4; ++x) {
        worker_threads.create_thread(boost::bind(&WorkerThread, io_service));
    }

    std::cin.get();
    io_service->stop();
    worker_threads.join_all();
    return 0;
}
