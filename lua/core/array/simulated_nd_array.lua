#!/usr/bin/lua

-- multi-dimensional arrays can be implemented by single dimensional array by manipulating indices

array = {}

maxRows = 3
maxColumns = 3

for row=1,maxRows do
    for col=1,maxColumns do
        array[row*maxColumns +col] = row*col
    end

end

for row=1,maxRows do
    for col=1,maxColumns do
        print(array[row*maxColumns +col])
    end
end
