#!/usr/bin/lua

print(tonumber(123))                -- 123
print(tonumber("123"))              -- 123
print(tonumber("abc"))              -- nil
print(tonumber("FFFF", 16))         -- 65535
print(tonumber("101", 2))           -- 5

function func()
    print("this is a function")
end

t = {name = "table"}

print(tostring(123))                -- 123
print(tostring("abc"))              -- abc
print(tostring(func))               -- function: 0x14ecd30
print(tostring(t))                  -- table: 0x14ecc10
