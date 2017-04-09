#!/usr/bin/lua

file = io.open("test.txt", "r")
io.input(file)                      -- sets the default input file
print(io.read())
io.close(file)
