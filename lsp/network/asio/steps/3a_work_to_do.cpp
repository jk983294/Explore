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

    io_service->run();

    global_stream_lock.lock();
    cout << "[" << boost::this_thread::get_id() << "] thread finish" << endl;
    global_stream_lock.unlock();
}

size_t fib(size_t n) {
    if (n <= 1) {
        return n;
    }
    boost::this_thread::sleep(boost::posix_time::milliseconds(1000));
    return fib(n - 1) + fib(n - 2);
}

void CalculateFib(size_t n) {
    global_stream_lock.lock();
    cout << "[" << boost::this_thread::get_id() << "] now calculating fib( " << n << " ) " << endl;
    global_stream_lock.unlock();

    size_t f = fib(n);

    global_stream_lock.lock();
    cout << "[" << boost::this_thread::get_id() << "] fib( " << n << " ) = " << f << endl;
    global_stream_lock.unlock();
}

int main(int argc, char* argv[]) {
    boost::shared_ptr<boost::asio::io_service> io_service(new boost::asio::io_service);
    boost::shared_ptr<boost::asio::io_service::work> work(new boost::asio::io_service::work(*io_service));

    global_stream_lock.lock();
    cout << "[" << boost::this_thread::get_id() << "] the program will exit when all work has finished." << endl;
    global_stream_lock.unlock();

    // two threads to handle three works, then one thread must execute two works
    boost::thread_group worker_threads;
    for (int x = 0; x < 2; ++x) {
        worker_threads.create_thread(boost::bind(&WorkerThread, io_service));
    }

    /**
     * post function is used to ask the io_service to execute the given handler,
     * but without allowing the io_service to call the handler from inside this function.
     * dispatch function guarantees that the handler will only be called in a thread
     * in which the run(), run_one(), poll() or poll_one() member functions is currently being invoked.
     * The handler may be executed inside this function if the guarantee can be met.
     *
     * the fundamental difference is that dispatch will execute the work right away if it can and queue it otherwise
     * while post queues the work no matter what
     */
    io_service->post(boost::bind(CalculateFib, 3));
    io_service->post(boost::bind(CalculateFib, 4));
    io_service->post(boost::bind(CalculateFib, 5));

    // reset the work object to signal once the work has been completed that we wish to exit
    work.reset();
    worker_threads.join_all();
    return 0;
}
