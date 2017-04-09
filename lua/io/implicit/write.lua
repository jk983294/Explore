#!/usr/bin/lua

file = io.open("test.txt", "w")
io.output(file)                             -- sets the default output file
io.write("hello world\n")
io.write("-- End of the test.txt file\n")
io.close(file)
