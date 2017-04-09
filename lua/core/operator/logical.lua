#!/usr/bin/lua

a = 0
b = 10

print( a == 0 and b == 10 )         -- true
print( a == 0 and b ~= 10 )         -- false
print( not a )                      -- false
print( not (a < b) )                -- false
