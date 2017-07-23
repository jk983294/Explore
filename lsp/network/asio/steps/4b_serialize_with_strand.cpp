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

void PrintNum(int x) { std::cout << "[" << boost::this_thread::get_id() << "] x: " << x << std::endl; }

int main(int argc, char* argv[]) {
    boost::shared_ptr<boost::asio::io_service> io_service(new boost::asio::io_service);
    boost::shared_ptr<boost::asio::io_service::work> work(new boost::asio::io_service::work(*io_service));
    boost::asio::io_service::strand strand(*io_service);

    global_stream_lock.lock();
    cout << "[" << boost::this_thread::get_id() << "] the program will exit when all work has finished." << endl;
    global_stream_lock.unlock();

    boost::thread_group worker_threads;
    for (int x = 0; x < 4; ++x) {
        worker_threads.create_thread(boost::bind(&WorkerThread, io_service));
    }

    /**
     * the output remains clean though, but the order is just not as expected
     * because the work we are passing is guaranteed to be executed serially,
     * but there is no guarantee to which the order of the work actually takes place
     *
     * So if order is important, we have to go through the strand object API itself.
     * If order is not important, then we can post across the io_service object and wrap our handler through the strand.
     */
    boost::this_thread::sleep(boost::posix_time::milliseconds(100));
    io_service->post(strand.wrap(boost::bind(&PrintNum, 1)));
    io_service->post(strand.wrap(boost::bind(&PrintNum, 2)));

    boost::this_thread::sleep(boost::posix_time::milliseconds(100));
    io_service->post(strand.wrap(boost::bind(&PrintNum, 3)));
    io_service->post(strand.wrap(boost::bind(&PrintNum, 4)));

    boost::this_thread::sleep(boost::posix_time::milliseconds(100));
    io_service->post(strand.wrap(boost::bind(&PrintNum, 5)));
    io_service->post(strand.wrap(boost::bind(&PrintNum, 6)));

    work.reset();
    worker_threads.join_all();
    return 0;
}
