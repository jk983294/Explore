# Arrays can store data in more than two dimensions.  dimension (2, 3, 4) means it creates 4 rectangular matrices each with 2 rows and 3 columns
array(c(5,9,3,10,11,12,13,14,15),dim=c(3,3,2))
column.names <- c("COL1","COL2","COL3")
row.names <- c("ROW1","ROW2","ROW3")
matrix.names <- c("Matrix1","Matrix2")
result <- array(c(vector1,vector2),dim=c(3,3,2),dimnames = list(column.names,row.names,matrix.names))

# Accessing Array Elements
result[3,,2]				# the third row of the second matrix of the array.
result[1,3,1]				# the element in the 1st row and 3rd column of the 1st matrix.
result[,,2]					# the 2nd Matrix.
matrix1 <- array1[,,1]		# create matrices from these arrays.
matrix2 <- array2[,,2]
matrix1+matrix2

# Calculations Across Array Elements, apply(array, margin, function ), margin rule: 1 indicates rows, 2 indicates columns, c(1, 2) indicates rows and columns
result <- apply(array1, c(1), sum)