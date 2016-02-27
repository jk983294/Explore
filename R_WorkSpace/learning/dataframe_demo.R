# Create Data Frame
emp.data <- data.frame(
    emp_id = c (1:5), 
    emp_name = c("Rick","Dan","Michelle","Ryan","Gary"),
    salary = c(623.3,515.2,611.0,729.0,843.25), 
    start_date = as.Date(c("2012-01-01","2013-09-23","2014-11-15","2014-05-11","2015-03-27")),
    stringsAsFactors=FALSE
)
t(matrix_or_dataframe)				                                                                            # transpose
addresses <- cbind(c("Tampa","Seattle"),c("FL","WA"),c(33602,98104))						                    # Combine above three vectors (city, state, zipcode) into one data frame.
merged.dataframe <- merge(x=dataframe1, y=dataframe2, by.x=c("col1", "col2"), by.y=c("col1", "col2"))			# merge two data frames, inner join / outer join / Cartesian product 
molten.ships <- melt(ships, id = c("type","year")) 																# results is (type, year, column_name, column_value)
recasted.ship <- cast(molten.ships, type+year~variable,sum)											            # group by

# Get the Structure of the Data Frame
str(emp.data)

# Summary of Data in data frame
summary(emp.data)

# Extract Data from data frame
emp.data[1, 2]                                              # by row and column
emp.data[1, ]                                               # by row
emp.data[, 2]                                               # by column
emp.data[["emp_name"]]                                      # by column
emp.data$emp_name                                           # by column
emp.data[c(TRUE,TRUE,FALSE,FALSE,FALSE),]
emp.data[emp.data$emp_id < 3,]
emp.data[emp.data$emp_name %in% c("Rick", "Dan"),]
result <- data.frame(emp.data$emp_name,emp.data$salary)		# Extract Specific columns by column name
result <- emp.data[1:2,]									# Extract first two rows and all columns
result <- emp.data[c(3,5),c(2,4)]							# Extract 3rd and 5th row with 2nd and 4th column

# Expand data frame
emp.data$dept <- c("IT","Operations","IT","HR","Finance")					    # Add column
emp.newdata <- 	data.frame(
    emp_id = c (6:8), 
    emp_name = c("Rasmi","Pranab","Tusar"),
    salary = c(578.0,722.5,632.8), 
    start_date = as.Date(c("2013-05-21","2013-07-30","2014-06-17")),
    dept = c("IT","Operations","Fianance"),
    stringsAsFactors=FALSE)
emp.finaldata <- rbind(emp.data,emp.newdata)									# Add rows