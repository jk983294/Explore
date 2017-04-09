#!/usr/bin/lua

file = io.open("test.txt", "w")
file:write("hello world\n")
file:write("-- End of the test.txt file\n")
file:close(file)
