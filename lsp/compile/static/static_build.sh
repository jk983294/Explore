g++ -c first.cpp -o first.o
g++ -c second.cpp -o second.o
ar rcs libstaticlib.a first.o second.o
g++ -c main.cpp -o main.o
g++ main.o -o main_static -I. -L. -lstaticlib
