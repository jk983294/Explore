#!/usr/bin/lua

-- pcall (f, arg1, ...) function calls the requested function in protected mode
-- some error occurs in function f, it does not throw an error. it just returns the status of error.

function myfunction (n, dividend)
    n = n / dividend
end

if pcall(myfunction, 42, nil) then
    print("Success")
else
    print("Failure")
end
