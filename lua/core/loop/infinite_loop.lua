#!/usr/bin/lua

function sleep(n)
    local t0 = os.clock()
    while os.clock() - t0 <= n do end
end

while( true ) do
    print("This loop will run forever.")
    sleep(5)
end
