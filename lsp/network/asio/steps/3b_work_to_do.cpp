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

void Dispatch(int x) {
    global_stream_lock.lock();
    std::cout << "[" << boost::this_thread::get_id() << "] " << __FUNCTION__ << " x = " << x << std::endl;
    global_stream_lock.unlock();
}

void Post(int x) {
    global_stream_lock.lock();
    std::cout << "[" << boost::this_thread::get_id() << "] " << __FUNCTION__ << " x = " << x << std::endl;
    global_stream_lock.unlock();
}

/**
 * output was out of order.
 * because dispatched events can execute from the current worker thread
 * even if there are other pending events queued up.
 * The posted events have to wait until the handler completes before being allowed to be executed.
 *
 * we can easily code ourselves into serious bugs if we depend on the order of such events!
 */
void Run3(boost::shared_ptr<boost::asio::io_service> io_service) {
    for (int x = 0; x < 3; ++x) {
        io_service->dispatch(boost::bind(&Dispatch, x * 2));
        io_service->post(boost::bind(&Post, x * 2 + 1));
        boost::this_thread::sleep(boost::posix_time::milliseconds(1000));
    }
}

int main(int argc, char* argv[]) {
    boost::shared_ptr<boost::asio::io_service> io_service(new boost::asio::io_service);
    boost::shared_ptr<boost::asio::io_service::work> work(new boost::asio::io_service::work(*io_service));

    global_stream_lock.lock();
    cout << "[" << boost::this_thread::get_id() << "] the program will exit when all work has finished." << endl;
    global_stream_lock.unlock();

    boost::thread_group worker_threads;
    for (int x = 0; x < 1; ++x) {
        worker_threads.create_thread(boost::bind(&WorkerThread, io_service));
    }

    io_service->post(boost::bind(&Run3, io_service));

    work.reset();
    worker_threads.join_all();
    return 0;
}
