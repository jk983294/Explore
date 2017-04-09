#!/usr/bin/lua

-- it is possible to place the elements in a sparse way
-- it is the way Lua implementation of a matrix works
array = {}

for i=1, 3 do
    array[i] = {}
    for j=1,3 do
        array[i][j] = i*j
    end
end

for i=1, 3 do
    for j=1, 3 do
        print(array[i][j])
    end
end
