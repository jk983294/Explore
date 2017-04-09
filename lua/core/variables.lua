#!/usr/bin/lua

local a , b = 5 ,10         -- local variables.
c , d = 5, 10;              -- global variables.
e, f = 10                   --[[ global variables. Here value of f is nil --]]

print(a, b, c, d, e, f)

a, b = b, a                 -- swap
print(a, b, c, d, e, f)
