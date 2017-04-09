#!/usr/bin/lua

-- xpcall (f, err) function calls the requested function and also sets the error handler.
-- Any error inside f is not propagated; instead, xpcall catches the error, calls the err function with the original error object, and returns a status code.

function myerrorhandler( err )
    print( "ERROR:", err )
end

function myfunction (n, dividend)
    n = n / dividend
end

status = xpcall( myfunction, myerrorhandler, 42, nil )
print( status)
