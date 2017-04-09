#!/usr/bin/lua

-- ipairs can only apply for array, namely the index start from 1, 2 ...
-- pairs can apply for table, use next to iterate

array = {"Lua", "Tutorial"}
local tabFiles = {
    [1] = "test1",
    [6] = "test6",
    [4] = "test4"
}

for key,value in ipairs(array) do
    print(key, value)
end

for key,value in ipairs(tabFiles) do        -- only "test1"
    print(key, value)
end

for key,value in pairs(tabFiles) do         --  "test1" "test4" "test6"
    print( key, value )
end
