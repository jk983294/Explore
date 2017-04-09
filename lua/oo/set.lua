#!/usr/bin/lua

Set = {}
local mt = {}

function Set.new(l)
    local set = {}
    setmetatable(set, mt)
    for _, v in pairs(l) do set[v] = true end
    return set
end

function Set.union(a, b)
    if getmetatable(a) ~= mt or getmetatable(b) ~= mt then      -- prevent set3 = set1 + 8 error
        error("metatable error.")
    end

    local retSet = Set.new{}
    for v in pairs(a) do retSet[v] = true end
    for v in pairs(b) do retSet[v] = true end
    return retSet
end

function Set.intersection(a, b)
    local retSet = Set.new{}
    for v in pairs(a) do retSet[v] = b[v] end
    return retSet
end

function Set.toString(set)
     local tb = {}
     for e in pairs(set) do
          tb[#tb + 1] = e
     end
     return "{" .. table.concat(tb, ", ") .. "}"
end

function Set.print(s)
     print(Set.toString(s))
end

mt.__add = Set.union
mt.__tostring = Set.toString

-- test
local set1 = Set.new({10, 20, 30})
local set2 = Set.new({1, 2})
print(getmetatable(set1))
print(getmetatable(set2))

local set3 = set1 + set2
Set.print(set3)
print(set3)
assert(getmetatable(set1) == getmetatable(set2))                -- share the same metatable
