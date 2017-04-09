#!/usr/bin/lua

-- checks whether v1 is equal to v2, without invoking any metamethod

local tab = {
    23,
    35,
    h = 1,
    w = 1,
}

function cmp_func(op1, op2)
    print("called __eq function")
end

setmetatable(tab, {__eq = cmp_func})

local newtab = {};
setmetatable(newtab, {__eq = cmp_func})


print("use rawequal result:", rawequal(tab, tab))
print("use normal method result:", tab == tab)

print("use rawequal result:", rawequal(tab, newtab))
print("use normal method result:", tab == newtab)           -- will call cmp_func
