#!/usr/bin/lua

-- place the two Lua files in the same directory
-- or you can place the module file in the package path and it needs additional setup
-- module name and its file name should be the same.

local mymath = require "mymath"
print(mymath.add(1, 2))
