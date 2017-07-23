#include <boost/asio.hpp>
#include <boost/shared_ptr.hpp>
#include <boost/thread.hpp>
#include <boost/thread/mutex.hpp>
#include <iostream>

using namespace std;

boost::mutex global_stream_lock;

void WorkerThread(boost::shared_ptr<boost::asio::io_service> io_service) {
    global_stream_lock.lock();
    cout << "[" << boost::this_thread::get_id() << "] thread start" << endl;
    global_stream_lock.unlock();

    /**
     * the errors are propagated through the handlers to the point where a thread calls a run or poll functions.
     * user can either handle the exception through a try/switch statement or they can opt to receive the exception
     * through an error variable
     */
    try {
        io_service->run();
    } catch (std::exception& ex) {
        global_stream_lock.lock();
        std::cout << "[" << boost::this_thread::get_id() << "] exception: " << ex.what() << std::endl;
        global_stream_lock.unlock();
    }

    global_stream_lock.lock();
    cout << "[" << boost::this_thread::get_id() << "] thread finish" << endl;
    global_stream_lock.unlock();
}

void RaiseAnException(boost::shared_ptr<boost::asio::io_service> io_service) {
    global_stream_lock.lock();
    std::cout << "[" << boost::this_thread::get_id() << "] " << __FUNCTION__ << std::endl;
    global_stream_lock.unlock();

    // post work to the io_service that causes exceptions over and over, so it will end all threads in pool
    io_service->post(boost::bind(&RaiseAnException, io_service));

    throw(std::runtime_error("oops!"));
}

int main(int argc, char* argv[]) {
    boost::shared_ptr<boost::asio::io_service> io_service(new boost::asio::io_service);
    boost::shared_ptr<boost::asio::io_service::work> work(new boost::asio::io_service::work(*io_service));

    global_stream_lock.lock();
    cout << "[" << boost::this_thread::get_id() << "] the program will exit when all work has finished." << endl;
    global_stream_lock.unlock();

    boost::thread_group worker_threads;
    for (int x = 0; x < 2; ++x) {
        worker_threads.create_thread(boost::bind(&WorkerThread, io_service));
    }

    io_service->post(boost::bind(&RaiseAnException, io_service));

    /**
     * althrough we didn't clear work object, but when all threads terminated by exception,
     * eventually no thread alive, then io_service stopped
     */
    worker_threads.join_all();
    return 0;
}
