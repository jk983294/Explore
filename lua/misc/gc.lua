#!/usr/bin/lua

-- collectgarbage("collect") − Runs one complete cycle of garbage collection.
-- collectgarbage("count") − Returns the amount of memory currently used by the program in Kilobytes.
-- collectgarbage("restart") − If the garbage collector has been stopped, it restarts it.
-- collectgarbage("setpause") − Sets the value given as second parameter divided by 100 to the garbage collector pause variable. Its uses are as discussed a little above.
-- collectgarbage("setstepmul") − Sets the value given as second parameter divided by 100 to the garbage step multiplier variable. Its uses are as discussed a little above.
-- collectgarbage("step") − Runs one step of garbage collection. The larger the second argument is, the larger this step will be. The collectgarbage will return true if the triggered step was the last step of a garbage-collection cycle.
-- collectgarbage("stop") − Stops the garbage collector if its running.

mytable = {"apple", "orange", "banana"}

print(collectgarbage("count"))

mytable = nil

print(collectgarbage("count"))

print(collectgarbage("collect"))

print(collectgarbage("count"))
