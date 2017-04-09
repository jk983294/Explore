#!/usr/bin/lua

function average(...)
    result = 0
    local arg= {...}
    for i,v in ipairs(arg) do
        result = result + v
    end
    return result / #arg
end

print("The average is", average(10, 5, 3, 4, 5, 6))

-- select('#',...) gives total length
-- select(i,...) gives array[i]
function average2(...)
    local sum = 0
    local valid_number_count = 0
    local arg
    for i=1, select('#',...) do
        arg = select(i,...)
        if arg then
            valid_number_count = valid_number_count + 1
            sum = sum + arg
        end
    end
    return sum / valid_number_count
end
print(average2(10, 5, 3, 4, nil, 5, 6))                     -- select can prevent element not be visited after nil
