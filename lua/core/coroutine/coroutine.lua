#!/usr/bin/lua

-- at any given time, only one coroutine runs and this running coroutine only suspends its execution when it explicitly requests to be suspended
-- coroutine interact with main function with yield & resume
-- main use resume to send coroutine parameters
-- coroutine use yield to send main parameters

co = coroutine.create(function (value1,value2)
    local tempvar3 =10
    print("coroutine section 1", value1, value2, tempvar3)                      -- coroutine section 1	3	2	10

    local tempvar1 = coroutine.yield(value1+1,value2+1)                         -- main	true	4	3
    tempvar3 = tempvar3 + value1
    print("coroutine section 2",tempvar1 ,tempvar2, tempvar3)                   -- coroutine section 2	12	nil	13

    local tempvar1, tempvar2= coroutine.yield(value1+value2, value1-value2)     -- main	true	5	1
    tempvar3 = tempvar3 + value1
    print("coroutine section 3",tempvar1,tempvar2, tempvar3)                    -- coroutine section 3	5	6	16
    return value2, "end"                                                        -- main	true	2	end
end)

print("main", coroutine.resume(co, 3, 2))
print("main", coroutine.resume(co, 12,14))
print("main", coroutine.resume(co, 5, 6))
print("main", coroutine.resume(co, 10, 20))                                     -- main	false	cannot resume dead coroutine
