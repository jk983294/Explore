-- Module is like a library that can be loaded using require and has a single global name containing a table.
-- This module can consist of a number of functions and variables.
-- All these functions and variables are wrapped in to the table which acts as a namespace.

local mymath =  {}

function mymath.add(a,b)
    return a + b
end

function mymath.sub(a,b)
    return a - b
end

function mymath.mul(a,b)
    return a * b
end

function mymath.div(a,b)
    return a / b
end

return mymath
