#!/usr/bin/lua

--Random
math.randomseed(os.time())
io.write("Random number between 0 and 1 is ",math.random(),"\n")
io.write("Random number between 1 and 100 is ",math.random(1,100),"\n")         --Random between 1 to 100


io.write("Floor of 10.5055 is ", math.floor(10.5055),"\n")
io.write("Ceil of 10.5055 is ", math.ceil(10.5055),"\n")
io.write("Square root of 16 is ",math.sqrt(16),"\n")
io.write("10 power 2 is ",math.pow(10,2),"\n")
io.write("100 power 0.5 is ",math.pow(100,0.5),"\n")
io.write("Absolute value of -10 is ",math.abs(-10),"\n")
io.write("Maximum in the input array is ",math.max(1,100,101,99,999),"\n")
io.write("Minimum in the input array is ",math.min(1,100,101,99,999),"\n")

-- trigonometric functions
radianVal = math.rad(math.pi / 2)
io.write(radianVal,"\n")
io.write(string.format("%.1f ", math.sin(radianVal)),"\n")
io.write(string.format("%.1f ", math.cos(radianVal)),"\n")
io.write(string.format("%.1f ", math.tan(radianVal)),"\n")
io.write(string.format("%.1f ", math.cosh(radianVal)),"\n")
io.write(math.deg(math.pi),"\n")                                                -- pi Value in degrees
