v <- c( 2, 5.5, 6, 9)
t <- c(8, 3, 4, 9)

# Arithmetic Operators
v + t
v - t
v * t
v / t
v %% t          # Give the remainder of the first vector with the second
v %/% t         # The result of division of first vector with second
v ^ t           # pow(v1, v2)

# Relational Operators
v > t
v < t
v == t
v <= t
v >= t
v != t

# Logical Operators, All numbers greater than 1 are considered as logical value TRUE
v & t
v | t
!v
v && t          # take first element
v || t          # take first element

# Assignment Operators
v1 <- c(3,1,TRUE,2+3i)
v2 <<- c(3,1,TRUE,2+3i)
v3 = c(3,1,TRUE,2+3i)
c(3,1,TRUE,2+3i) -> v1
c(3,1,TRUE,2+3i) ->> v2 

# Miscellaneous Operators
t <- 1:10           # creates the series of numbers in sequence for a vector
v1 <- 8
print(v1 %in% t)    #  identify if an element belongs to a vector.
M = matrix( c(2,6,5,1,10,4), nrow=2,ncol=3,byrow = TRUE)
t = M %*% t(M)      # multiply a matrix with its transpose

