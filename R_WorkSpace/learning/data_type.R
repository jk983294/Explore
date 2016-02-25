# vriable
l <- TRUE                   # boolean
i <- 123L                   # integer
n <- 123.45                 # numeric
v <- 2+5i                   # complex
v <- charToRaw("hello")     # raw
c <- "ABC 123"              # character

# vector, hold elements of different classes, c stands for concatenation
v <- c(1, 2, 3)     
s <- 1:5

# matrix  two dimensions
m <- matrix(data = 1:6, nrow = 2, ncol = 3)   
M = matrix( c('a','a','b','c','b','a'), nrow=2,ncol=3,byrow = TRUE)

# array, any number of dimensions
a <- array(data = 1:8, dim = c(2, 2, 2))
a <- array(c('green','yellow'),dim=c(3,3,2))

# list
list1 <- list(TRUE, 1L, 2.34, "abc") 
list2 <- list(c(2,5,3), 21.3, sin)

# facor stores the vector along with the distinct values of the elements in the vector as labels
apple_colors <- c('green','green','yellow','red','red','red','green')
factor_apple <- factor(apple_colors)
nlevels(factor_apple)
levels(factor_apple)
unclass(factor_apple)

# data frame, tabular data objects, each column can contain different modes of data, a list of vectors of equal length.
BMI <- 	data.frame(
    gender = c("Male", "Male","Female"), 
    height = c(152, 171.5, 165), 
    weight = c(81,93, 78),
    Age =c(42,38,26)
)
BMI