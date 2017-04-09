#!/usr/bin/lua

a = 10

while( a < 20 ) do
    print("value of a:", a)
    a = a + 1

    if( a > 15) then
        break
    end
end
