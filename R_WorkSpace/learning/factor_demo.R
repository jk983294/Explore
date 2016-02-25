# Factors are used to categorize the data and store it as levels
data <- c("East","West","East","North","North","East","West","West","West","East","North")
factor_data <- factor(data)
is.factor(factor_data)

# Changing the order of Levels
new_order_data <- factor(factor_data,levels = c("East","West","North"))

# Generating Factor Levels
v <- gl(3, 4, labels = c("Tampa", "Seattle","Boston"))

# R treats the text column as categorical data and creates factors on it.
height <- c(132,151,162,139,166,147,122)
weight <- c(48,49,66,53,67,52,40)
gender <- c("male","male","female","female","male","female","male")
input_data <- data.frame(height,weight,gender)
is.factor(input_data$gender)