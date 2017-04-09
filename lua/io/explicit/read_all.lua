#!/usr/bin/lua

file = io.open("test.txt", "r")
print(file:read("*a"))
io.close(file)
