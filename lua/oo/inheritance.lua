#!/usr/bin/lua

-- Inheritance can be implemented with the help of metatables,
-- providing a look up mechanism for nonexistent functions(methods) and fields in parent object(s).

Shape = {area = 0}

function Shape:new (o,side)
    o = o or {}
    setmetatable(o, self)
    self.__index = self
    side = side or 0
    self.area = side*side;
    return o
end

function Shape:printArea ()
    print("The area is ",self.area)
end

-- derived class
Square = Shape:new()

function Square:new (o,side)
    o = o or Shape:new(o,side)
    setmetatable(o, self)
    self.__index = self
    return o
end

function Square:printArea ()
    print("The area of square is ",self.area)
end

Rectangle = Shape:new()

function Rectangle:new (o,length,breadth)
    o = o or Shape:new(o)
    setmetatable(o, self)
    self.__index = self
    self.area = length * breadth
    return o
end

function Rectangle:printArea ()
    print("The area of Rectangle is ",self.area)
end

-- test
mysquare = Square:new(nil,10)
mysquare:printArea()
myrectangle = Rectangle:new(nil,10,20)
myrectangle:printArea()
