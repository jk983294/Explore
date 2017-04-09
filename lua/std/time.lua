#!/usr/bin/lua

-- Date with format
io.write("The date is ", os.date("%m/%d/%Y"),"\n")          -- 03/23/2017

-- Date and time
io.write("The date and time is ", os.date(),"\n")           -- Thu Mar 23 20:14:31 2017

-- Time
io.write("The OS time is ", os.time(),"\n")                 -- 1490271271

-- Wait for some time
for i=1,1000000 do
end

-- Time since Lua started
io.write("Lua started before ", os.clock(),"\n")            -- 0.020914
