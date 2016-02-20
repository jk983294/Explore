# six types of atomic vectors. They are - logical, integer, double, complex, character and raw.

# single element vector
print("abc");
print(12.5)
print(63L)
print(TRUE)
print(2+3i)
print(charToRaw('hello'))

# colon operator 
print(5:13)
print(6.6:12.6)
print(3.8:11.4)         # If the final element specified does not belong to the sequence then it is discarded.

# Seq operator
seq(5, 9, by=0.4)

# c() function, non-character values are coerced to character type if one of the elements is a character.
c('apple','red',5,TRUE)

# Accessing Vector Elements, Indexing starts with position 1
t <- c("Sun","Mon","Tue","Wed","Thurs","Fri","Sat")
t[c(2,3,6)]
t[c(TRUE,FALSE,FALSE,FALSE,FALSE,TRUE,FALSE)]
t[c(0,0,0,0,0,0,1)]     # only get index 1
t[c(-2,-5)]             # drop index 2 and index 5

# Vector element recycling
v1 <- c(3,8,4,5,0,11)
v2 <- c(4,11)
v1+v2                   # the shorter vector are recycled to complete the operations

# sorting
v <- c(3,8,4,5,0,11, -9, 304)
sort.result <- sort(v)
sort.result
sort(v, decreasing = TRUE)
