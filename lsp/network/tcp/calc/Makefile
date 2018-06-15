all: client server

client: client.cpp
	g++ -Wall -std=c++14 client.cpp -o client -lpthread

server: server.cpp
	g++ -Wall -std=c++14 server.cpp -o server -lpthread

clean:
	rm client server
