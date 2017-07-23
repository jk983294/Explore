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
    boost::system::error_code ec;
    io_service->run(ec);

    if (ec) {
        global_stream_lock.lock();
        std::cout << "[" << boost::this_thread::get_id() << "] exception: " << ec << std::endl;
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

    io_service->post(boost::bind(&RaiseAnException, io_service));

    /**
     * program get a crash.
     * because the error variable does not convert user exceptions to errors but rather boost::asio exceptions.
     * if we are using the io_service for user work, we have to use exception handling if the work  generate exceptions.
     * if we are using the io_service for boost::asio functions only, then we can use exception handling
     * or the error variable
     */
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

    worker_threads.join_all();
    return 0;
}
