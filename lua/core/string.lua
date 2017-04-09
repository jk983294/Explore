#!/usr/bin/lua

-- initilize
string1 = "Lua "
string2 = 'Tutorial '
string3 = [[Lua Tutorial]]

print(string1, string2, string3)

print(string.upper(string1))
print(string.lower(string1))
sub = string.gsub(string3,"Tutorial","Language")
print("substituted string", sub)
findResultFrom, findResultTo = string.find(string3,"Tutorial")
print("find result", findResultFrom, findResultTo)
print(string.reverse(string3))
print("Concatenated string",string1..string2)
print("Length of string1 is ", string.len(string1))
print("Length of string1 is ", #string1)
print(string.rep(string1,3))                                -- repeating strings

-- format
number1 = 10
number2 = 20
year, month, day = 2014, 1, 2
print(string.format("Basic formatting %s %s",string1,string2))
print(string.format("Basic formatting %d %d",number1,number2))
print(string.format("Date formatting %02d/%02d/%03d", day, month, year))
print(string.format("%.4f",1/3))                            -- decimal formatting
