#!/usr/bin/lua

i = 42
local i = 0

f = loadstring("i = 1 + i; print(i)");      -- use global i

g = function ()
    i = 1 + i;                              -- use loacal i
    print(i)
end

f()
g()
