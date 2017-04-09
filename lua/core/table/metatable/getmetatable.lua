#!/usr/bin/lua

local t = {}
print(getmetatable(t))                          -- nil

local t1 = {}
setmetatable(t, t1)
assert(getmetatable(t) == t1)

print(getmetatable("Hello World"))              -- only string and table has metatable
print(getmetatable(10))
