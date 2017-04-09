#!/usr/bin/lua

local ta = {}
print(#ta)                  -- 0
print(next(ta))             -- nil

local ta1 = { [1] = "ma" }
print(#ta1)                 -- 1
print(next(ta1))            -- 1	ma

local ta = { rr = "ma" }
print(#ta)                  -- 0
print(next(ta))             -- rr	ma
