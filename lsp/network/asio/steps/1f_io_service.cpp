#include <boost/asio.hpp>
#include <boost/shared_ptr.hpp>
#include <boost/thread.hpp>
#include <iostream>

boost::asio::io_service io_service;

/**
 * multiple threads may call the run() function to set up a pool of threads
 * from which the io_service may execute handlers.
 * all threads that are waiting in the pool are equivalent and the io_service may
 * choose any one of them to invoke a handler
 */
void WorkerThread() {
    std::cout << "thread Start\n";
    io_service.run();
    std::cout << "thread Finish\n";
}

int main(int argc, char* argv[]) {
    boost::shared_ptr<boost::asio::io_service::work> work(new boost::asio::io_service::work(io_service));

    std::cout << "press enter to exit." << std::endl;

    /**
     * create a thread pool with 4 thread for io_service to choose to invoke handler
     * it is simple and easy to make our threaded programs scale by simply adding more worker threads
     */
    boost::thread_group worker_threads;
    for (int x = 0; x < 4; ++x) {
        worker_threads.create_thread(WorkerThread);
    }

    // because a work associated with io_service, so thread will block on io_service.run() until we stop explicitly
    std::cin.get();
    io_service.stop();
    worker_threads.join_all();
    return 0;
}
