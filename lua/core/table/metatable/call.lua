#!/usr/bin/lua

-- adding behavior of method call is done using __call statement.
-- example shows return the sum of values in main table with the passed table.
mytable = setmetatable({10}, {
    __call = function(mytable, newtable)
        sum = 0

        for i = 1, table.maxn(mytable) do
            sum = sum + mytable[i]
        end

        for i = 1, table.maxn(newtable) do
            sum = sum + newtable[i]
        end

        return sum
    end
})

newtable = {10,20,30}
print(mytable(newtable))
