#!/usr/bin/lua

mytable = setmetatable({ 10, 20, 30 }, {
    __tostring = function(mytable)
        sum = 0

        for k, v in pairs(mytable) do
            sum = sum + v
        end

        return "The sum of values in the table is " .. sum
    end
})

print(mytable)
