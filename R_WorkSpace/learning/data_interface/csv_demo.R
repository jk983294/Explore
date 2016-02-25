# CSV Files
getwd()											                        # Get current working directory.
setwd("E:/GitHub/Explore/R_WorkSpace/learning/data_interface")	        # Set current working directory.
data <- read.csv("input.csv")
is.data.frame(data)
ncol(data)
nrow(data)
max(data$salary)
subset(data, salary == max(salary))			                            # Get the person detail having max salary.
subset( data, dept == "IT")						                        # Get all the people working in IT department
subset(data, salary > 600 & dept == "IT")	                            # Get the persons in IT department whose salary is greater than 600
retval <- subset(data, as.Date(start_date) > as.Date("2014-01-01"))		# Get the people who joined on or after 2014
write.csv(retval,"output.csv")
write.csv(retval,"output.csv", row.names=FALSE)							# Write filtered data into a new file.
