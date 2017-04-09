#!/usr/bin/lua

-- if a key exists in the main table, it just updates it.
-- when a key is not available in the maintable, it adds that key to the metatable.

mymetatable = {}
mytable = setmetatable({key1 = "value1"}, { __newindex = mymetatable })

print(mytable.key1)

mytable.newkey = "new value 2"
print(mytable.newkey,mymetatable.newkey)

mytable.key1 = "new  value 1"
print(mytable.key1,mymetatable.newkey1)
