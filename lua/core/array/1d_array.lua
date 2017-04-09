#!/usr/bin/lua

-- index starts at index 1
array = {"Lua", "Tutorial"}

for i= 0, 2 do
    print(array[i])                 -- nill Lua Tutorial
end

-- index from -2 to 2
array = {}

for i= -2, 2 do
    array[i] = i *2
end

for i = -2, 2 do
    print(array[i])
end

-- unpack
t = {1,2,3,a = 4,b = 5}
print(unpack(t, 1, 4))              -- 1   2   3   nil
