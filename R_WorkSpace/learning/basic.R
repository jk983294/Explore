# RStudo usage
# Ctrl + Enter line by line execute

# help 
?nrow

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
ls(all.name=TRUE)                                                       # variables starting with dot(.) are hidden

# Deleting Variables
rm(var.3)
print(var.3)
rm(list=ls())
print(ls())


# packages
.libPaths()									                            # Get library locations containing R packages
library()										                        # Get the list of all the packages installed
search()										                        # Get all packages currently loaded in the R environment
install.packages("XML")				                                    # Install a New Package directly from CRAN
install.packages("E:/XML_3.98-1.3.zip", repos = NULL, type="source")	#Install package manually
install.packages("rmongodb", repos = "http://mirror.bjtu.edu.cn/cran/")
library("package Name", lib.loc="path to library")						# load package


# Mean, Median & Mode
x <- c(12,7,3,4.2,18,2,54,-21,8,-5)
result.mean <- mean(x)
result.mean <-  mean(x,trim = 0.3)  		# drop max and min values, then calculate the mean
result.mean <-  mean(x,na.rm = TRUE)	# drop NA values
median.result <- median(x)
# the value that has highest number of occurrences in a set of data
getmode <- function(v) {
   uniqv <- unique(v)
   uniqv[which.max(tabulate(match(v, uniqv)))]
}
charv <- c("o","it","the","it","it")
result <- getmode(charv)


# Linear Regression y = ax + b
x <- c(151, 174, 138, 186, 128, 136, 179, 163, 152, 131)
y <- c(63, 81, 56, 91, 47, 57, 76, 72, 62, 48)
relation <- lm(y~x)
print(relation)
print(summary(relation))

a <- data.frame(x = 170)
result <-  predict(relation,a)
print(result)
# Visualize the Regression Graphically
png(file = "linearregression.png")
plot(y,x,col = "blue",main = "Height & Weight Regression",
abline(lm(x~y)),cex = 1.3,pch = 16,xlab = "Weight in Kg",ylab = "Height in cm")
dev.off()


# Multiple Regression y = a + b1x1 + b2x2 +...bnxn
input <- mtcars[,c("mpg","disp","hp","wt")]
model <- lm(mpg~disp+hp+wt, data = input)
print(model)
cat("# # # # The Coefficient Values # # # ","\n")
a <- coef(model)[1]
print(a)
Xdisp <- coef(model)[2]
Xhp <- coef(model)[3]
Xwt <- coef(model)[4] 		# Y = a+Xdisp*x1+Xhp*x2+Xwt*x3
print(Xdisp)
print(Xhp)
print(Xwt)

# Logistic Regression y = 1/(1+e^-(a+b1x1+b2x2+b3x3+...))
input <- mtcars[,c("am","cyl","hp","wt")]
am.data = glm(formula = am ~ cyl + hp + wt, data = input, family = binomial)
print(summary(am.data))


# Normal Distribution
x <- seq(-10, 10, by = .1)
y <- dnorm(x, mean = 2.5, sd = 0.5)		# Choose the mean as 2.5 and standard deviation as 0.5.
png(file = "dnorm.png")
plot(x,y)
dev.off()

# Create a sequence of numbers between -10 and 10 incrementing by 0.2.
x <- seq(-10,10,by = .2)
cdf <- pnorm(x, mean = 2.5, sd = 2)		# Cumulative Distribution Function
png(file = "pnorm.png")
plot(x,cdf)
dev.off()

# This function takes the probability value and gives a number whose cumulative value matches the probability value.
x <- seq(0, 1, by = 0.02)
y <- qnorm(x, mean = 2, sd = 1)
png(file = "qnorm.png")
plot(x,y)
dev.off()

# Create a sample of 50 numbers which are normally distributed.
y <- rnorm(50)
png(file = "rnorm.png")
hist(y, main = "Normal DIstribution")
dev.off()


# Binomial Distribution deals with finding the probability of success of an event which has only two possible outcomes in a series of experiments.
