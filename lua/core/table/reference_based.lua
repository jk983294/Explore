#!/usr/bin/lua

-- table is reference based

mytable = {}
mytable["wow"] = "foo"
alternatetable = mytable                -- refer to same table

print(alternatetable["wow"])

alternatetable["wow"] = "bar"

print(mytable["wow"])

alternatetable = nil

print(mytable["wow"])                   -- mytable is still accessible

mytable = nil                           -- now mytable cannot access
print(mytable)
