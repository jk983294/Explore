#!/usr/bin/lua

Window = {}

Window.prototype = {x = 0 ,y = 0 ,width = 100 ,height = 100,}
Window.mt = {}

function Window.new(o)
    setmetatable(o ,Window.mt)
    return o
end

Window.mt.__index = function (t ,key)
    return 1000
end

Window.mt.__newindex = function (table ,key ,value)
    if key == "missingKey" then
        rawset(table ,"missingKey" ,"found in newindex")
    end
end

-- test
w = Window.new{x = 10 ,y = 20}
print(w.missingKey)                     -- call __index
print(rawget(w ,w.missingKey))          -- nil

w.missingKey = "missing"                -- call __newindex
print(w.missingKey)                     -- found in newindex
print(rawget(w ,w.missingKey))          -- nil
