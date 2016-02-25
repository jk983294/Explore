# Matrices elements are arranged in a two-dimensional rectangular layout. Elements are the same atomic types.
matrix(c(3:14), nrow=4, byrow=TRUE)
P <- matrix(c(3:14), nrow=4, byrow=TRUE, dimnames=list(c("row1", "row2", "row3", "row4"), c("col1", "col2", "col3")))

# Accessing Elements of a Matrix
P[1,3]
P[2,]			# Access only the  2nd row.
P[,3]			# Access only the 3rd column.

# Matrix Computations
matrix1 <- matrix(c(3, 9, -1, 4, 2, 6), nrow=2)
matrix2 <- matrix(c(5, 2, 0, 9, 3, 4), nrow=2)
matrix1 + matrix2
matrix1 - matrix2
matrix1 * matrix2
matrix1 / matrix2