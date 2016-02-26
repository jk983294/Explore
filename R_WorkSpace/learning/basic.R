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
library("package Name", lib.loc="path to library")						# load package


# Pie Charts
x <- c(21, 62, 10, 53)
labels <- c("London", "New York", "Singapore", "Mumbai")
piepercent<- round(100*x/sum(x), 1)
png(file = "city.jpg")					# Give the chart file a name.
pie(x,labels)								# Plot the chart.
pie(x, labels = piepercent, main = "City pie chart",col = rainbow(length(x)))
legend("topright", c("London","New York","Singapore","Mumbai"), cex = 0.8, fill = rainbow(length(x)))
dev.off()									# Save the file.

# 3d pie charts
library(plotrix)
x <-  c(21, 62, 10,53)
lbl <-  c("London","New York","Singapore","Mumbai")
png(file = "3d_pie_chart.jpg")
pie3D(x,labels=lbl,explode=0.1, main="Pie Chart of Countries ")
dev.off()


# Bar Charts
H <- c(7,12,28,3,41)
M <- c("Mar","Apr","May","Jun","Jul")
png(file = "barchart.png")
barplot(H,names.arg = M,xlab = "Month",ylab = "Revenue",col = "blue", main = "Revenue chart",border = "red")
dev.off()

# Group Bar Chart and Stacked Bar Chart
colors <- c("green","orange","brown")
months <- c("Mar","Apr","May","Jun","Jul")
regions <- c("East","West","North")
Values <- matrix(c(2,9,3,11,9,4,8,7,3,12,5,2,8,10,11),nrow = 3,ncol = 5,byrow = TRUE)
png(file = "barchart_stacked.png")
barplot(Values,main = "total revenue",names.arg = months,xlab = "month",ylab = "revenue",col = colors)
legend("topleft", regions, cex = 1.3, fill = colors)
dev.off()


# Boxplots
input <- mtcars[,c('mpg','cyl')]
print(head(input))
png(file = "boxplot.png")
boxplot(mpg ~ cyl, data = mtcars, xlab = "Number of Cylinders",ylab = "Miles Per Gallon", main = "Mileage Data")
dev.off()

# Boxplot with Notch
png(file = "boxplot_with_notch.png")
boxplot(mpg ~ cyl, data = mtcars, 
   xlab = "Number of Cylinders",
   ylab = "Miles Per Gallon", 
   main = "Mileage Data",
   notch = TRUE, 
   varwidth = TRUE, 
   col = c("green","yellow","purple"),
   names = c("High","Medium","Low")
)
dev.off()


# Histograms
v <-  c(9,13,21,8,36,22,12,41,31,33,19)
png(file = "histogram.png")
hist(v,xlab = "Weight",col = "yellow",border = "blue")
hist(v,xlab = "Weight",col = "green",border = "red", xlim = c(0,40), ylim = c(0,5),breaks = 5)
dev.off()


# Line Graphs
v <- c(7,12,28,3,41)
png(file = "line_chart.jpg")
plot(v,type = "o")
plot(v,type = "o", col = "red", xlab = "Month", ylab = "Rain fall",main = "Rain fall chart")
dev.off()

# Multiple Lines in a Line Chart
v <- c(7,12,28,3,41)
t <- c(14,7,6,19,3)
png(file = "line_chart_2_lines.jpg")
plot(v,type = "o",col = "red", xlab = "Month", ylab = "Rain fall", main = "Rain fall chart")
lines(t, type = "o", col = "blue")
dev.off()

# Scatterplots
input <- mtcars[,c('wt','mpg')]
png(file = "scatterplot.png")
plot(x = input$wt,y = input$mpg,
   xlab = "Weight",
   ylab = "Milage",
   xlim = c(2.5,5),
   ylim = c(15,30),
   main = "Weight vs Milage"
)
dev.off()

# Scatterplot Matrices
png(file = "scatterplot_matrices.png")
pairs(~wt+mpg+disp+cyl,data = mtcars,main = "Scatterplot Matrix")
dev.off()


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
