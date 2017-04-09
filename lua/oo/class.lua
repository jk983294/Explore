#!/usr/bin/lua

-- object orientation in Lua with the help of tables and first class functions of Lua.
-- By placing functions and related data into a table, an object is formed.
-- Inheritance can be implemented with the help of metatables,
-- providing a look up mechanism for nonexistent functions(methods) and fields in parent object(s).

Rectangle = {area = 0, length = 0, breadth = 0}

function Rectangle:new (o,length,breadth)
    o = o or {}
    setmetatable(o, self)
    self.__index = self
    self.length = length or 0
    self.breadth = breadth or 0
    self.area = length * breadth;
    return o
end

function Rectangle:printArea ()
    print("area is ",self.area)
end

r = Rectangle:new(nil,10,20)            -- creating an object, each object has its own memory and share the common class data.
print(r.length)                         -- access the property
r:printArea()                           -- access a member function
