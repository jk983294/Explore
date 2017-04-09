#!/usr/bin/lua

local function add(a,b)
    assert(type(a) == "number", "a is not a number")
    assert(type(b) == "number", "b is not a number")
    return a+b
end

add(10)                 -- lua: assert.lua:5: b is not a number
