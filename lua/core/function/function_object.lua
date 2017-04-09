#!/usr/bin/lua

myprint = function(param)
    print("This is my print function -   ##",param,"##")
end

function add(num1, num2, functionObj)
    result = num1 + num2
    functionObj(result)
end

add(2, 5, myprint)
