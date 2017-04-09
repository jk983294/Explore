#!/usr/bin/lua

function reverseTable(tab)
    local tmp = {}
    for i = 1, #tab do
        local key = #tab
        tmp[i] = table.remove(tab)
    end
    return tmp
end

function containsKey(t, element)
    for key, value in ipairs(t) do
        if key == element then
            return true
        end
    end
    return false
end

function containsValue(t, element)
    for key, value in ipairs(t) do
        if value == element then
            return true
        end
    end
    return false
end

fruits = {"banana","orange","apple"}

-- Concatenation
print(table.concat(fruits))                     -- bananaorangeapple
print(table.concat(fruits, ", "))               -- banana, orange, apple
print(table.concat(fruits, ", ", 2, 3))         -- orange, apple

-- Insert and Remove
table.insert(fruits,"mango")                    -- banana, orange, apple, mango
table.insert(fruits, 2, "grapes")               -- banana, grapes, orange, apple, mango

-- largest numeric index
print(table.maxn(fruits))                       -- 5

-- Removes the value from the table.
table.remove(fruits)                            -- banana, grapes, orange, apple
table.remove(fruits, 2)                         -- banana, orange, apple

-- Sort
table.sort(fruits)                              -- apple, banana, orange
sortFunc = function(a, b) return b < a end
table.sort(fruits, sortFunc)                    -- orange, banana, apple

-- reverse
r = reverseTable(fruits)                        -- apple, banana, orange
print(table.concat(r, ", "))

-- contains
print(containsKey(r, "apple"))
print(containsValue(r, "apple"))
