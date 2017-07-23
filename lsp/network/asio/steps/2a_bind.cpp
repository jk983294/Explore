#include <boost/bind.hpp>
#include <iostream>

void F1() { std::cout << __FUNCTION__ << std::endl; }

void F2(int i, float f) {
    std::cout << "i: " << i << std::endl;
    std::cout << "f: " << f << std::endl;
}

class MyClass {
public:
    void F3(int i, float f) {
        std::cout << "i: " << i << std::endl;
        std::cout << "f: " << f << std::endl;
    }
};

int main(int argc, char* argv[]) {
    /*
     * the run() function blocks until all work has finished and there are no more handlers to be dispatched,
     * or until the io_service has been stopped.
     * we are not really giving it anything to do explicitly, so the function should not block
     */
    auto f1 = boost::bind(&F1);
    f1();

    auto f2 = boost::bind(&F2, 42, 3.14f);
    f2();

    MyClass c;
    auto f3 = boost::bind(&MyClass::F3, &c, 42, 3.14f);
    f3();
    return 0;
}
