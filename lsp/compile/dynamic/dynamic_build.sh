g++ -fPIC -c first.cpp -o first.o
g++ -fPIC -c second.cpp -o second.o
g++ -shared first.o second.o -o libdynamiclib.so
# cp libdynamiclib.so /lib/libdynamiclib.so           # need root perm
g++ -c main.cpp -o main.o
g++ main.o -o main_dynamic -I. -L. -ldynamiclib
./main_dynamic

g++ load_dynamic_lib.cpp -o load_dynamic_lib -ldl
./load_dynamic_lib
