#!/usr/bin/lua

file = io.open("test.txt", "r")
if file then
    for line in file:lines() do
        print(line)
    end
end
io.close(file)
