g++ -E -P function.c -o function.i
g++ -c function.c -o function.o
g++ -c main.c -o main.o
g++ function.o main.o -o main

objdump -D -M intel function.o > function.s
objdump -D -M intel main.o > main.s
objdump -D -M intel main > main.s.s
