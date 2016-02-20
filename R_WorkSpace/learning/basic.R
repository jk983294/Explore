# RStudo usage
# Ctrl + Enter line by line execute

# assignment
var.1 = c(0,1,2,3)           
var.2 <- c("learn","R")   
c(TRUE,1) -> var.3           

#implicit printing
cat ("var.1 is ", var.1 ,"\n")
cat ("var.2 is ", var.2 ,"\n")
cat ("var.3 is ", var.3 ,"\n")
print(x)
y

# function and invoke
f <- function(x = 5){ x + 1 }
f(2)        # by position
f(x = 2)    # by name
f()         # default value
seq(32,44)
mean(25:82)
sum(41:68)
max(41:68)
min(41:68)

# find variables
ls()
ls(pattern="var")
ls(all.name=TRUE)           # variables starting with dot(.) are hidden

# Deleting Variables
rm(var.3)
print(var.3)
rm(list=ls())
print(ls())
