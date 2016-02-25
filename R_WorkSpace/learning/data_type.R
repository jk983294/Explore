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




# a list can contain strings, numbers, vectors and a logical values.
list_data <- list("Red", "Green", c(21,32,11), TRUE, 51.23, 119.1)

# The list elements can be given names and they can be accessed using these names.
list_data <- list(c("Jan","Feb","Mar"), matrix(c(3,9,5,1,-2,8), nrow=2), list("green",12.3))
names(list_data) <- c("1st Quarter", "A_Matrix", "A Inner list")
print(list_data)

# Accessing List Elements by index or name
list_data[2]
list_data$A_Matrix

# add, delete and update list elements
list_data[4] <- "New element"				# Add element at the end of the list.
list_data[4] <- NULL							# Remove the last element.
list_data[3] <- "updated element"			# Update the 3rd Element.

# Merging Lists
merged.list <- c(list1,list2)

# Converting List to Vector
list1 <- list(1:5)
list2 <-list(10:14)
v1 <- unlist(list1)
v2 <- unlist(list2)
result <- v1+v2


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

# Arrays can store data in more than two dimensions.  dimension (2, 3, 4) means it creates 4 rectangular matrices each with 2 rows and 3 columns
array(c(5,9,3,10,11,12,13,14,15),dim=c(3,3,2))
column.names <- c("COL1","COL2","COL3")
row.names <- c("ROW1","ROW2","ROW3")
matrix.names <- c("Matrix1","Matrix2")
result <- array(c(vector1,vector2),dim=c(3,3,2),dimnames = list(column.names,row.names,matrix.names))

# Accessing Array Elements
result[3,,2]				# the third row of the second matrix of the array.
result[1,3,1]				# the element in the 1st row and 3rd column of the 1st matrix.
result[,,2]					# the 2nd Matrix.
matrix1 <- array1[,,1]		# # create matrices from these arrays.
matrix2 <- array2[,,2]
matrix1+matrix2

# Calculations Across Array Elements, apply(array, margin, function ), margin rule: 1 indicates rows, 2 indicates columns, c(1, 2) indicates rows and columns
result <- apply(array1, c(1), sum)


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


# Create Data Frame
emp.data <- data.frame(
	emp_id = c (1:5), 
	emp_name = c("Rick","Dan","Michelle","Ryan","Gary"),
	salary = c(623.3,515.2,611.0,729.0,843.25), 
	start_date = as.Date(c("2012-01-01","2013-09-23","2014-11-15","2014-05-11","2015-03-27")),
	stringsAsFactors=FALSE
			)
t(matrix_or_dataframe)				# transpose
addresses <- cbind(c("Tampa","Seattle"),c("FL","WA"),c(33602,98104))						# Combine above three vectors (city, state, zipcode) into one data frame.
merged.dataframe <- merge(x=dataframe1, y=dataframe2, by.x=c("col1", "col2"), by.y=c("col1", "col2"))			# merge two data frames, inner join / outer join / Cartesian product 
molten.ships <- melt(ships, id = c("type","year")) 																# results is (type, year, column_name, column_value)
recasted.ship <- cast(molten.ships, type+year~variable,sum)											# group by

# Get the Structure of the Data Frame
str(emp.data)

# Summary of Data in data frame
summary(emp.data)

# Extract Data from data frame
result <- data.frame(emp.data$emp_name,emp.data$salary)				# Extract Specific columns by column name
result <- emp.data[1:2,]																		# Extract first two rows and all columns
result <- emp.data[c(3,5),c(2,4)]															# Extract 3rd and 5th row with 2nd and 4th column

# Expand data frame
emp.data$dept <- c("IT","Operations","IT","HR","Finance")					# Add column
emp.newdata <- 	data.frame(
	emp_id = c (6:8), 
	emp_name = c("Rasmi","Pranab","Tusar"),
	salary = c(578.0,722.5,632.8), 
	start_date = as.Date(c("2013-05-21","2013-07-30","2014-06-17")),
	dept = c("IT","Operations","Fianance"),
	stringsAsFactors=FALSE)
emp.finaldata <- rbind(emp.data,emp.newdata)									# Add rows




# packages
.libPaths()									# Get library locations containing R packages
library()										# Get the list of all the packages installed
search()										# Get all packages currently loaded in the R environment
install.packages("XML")				# Install a New Package directly from CRAN
install.packages("E:/XML_3.98-1.3.zip", repos = NULL, type="source")	#Install package manually
library("package Name", lib.loc="path to library")										# load package






# data interface
# CSV Files
getwd()											# Get current working directory.
setwd("/web/com")						# Set current working directory.
data <- read.csv("input.csv")
is.data.frame(data)
ncol(data)
nrow(data)
max(data$salary)
subset(data, salary == max(salary))			# Get the person detail having max salary.
subset( data, dept == "IT")						# Get all the people working in IT department
subset(data, salary > 600 & dept == "IT")	# Get the persons in IT department whose salary is greater than 600
retval <- subset(data, as.Date(start_date) > as.Date("2014-01-01"))		# Get the people who joined on or after 2014
write.csv(retval,"output.csv")
write.csv(retval,"output.csv", row.names=FALSE)									# Write filtered data into a new file.


# Excel File
install.packages("xlsx")
any(grepl("xlsx",installed.packages()))			# Verify the package is installed.
library("xlsx")
data <- read.xlsx("input.xlsx", sheetIndex = 1)

# Binary Files
write.table(mtcars, file = "mtcars.csv",row.names=FALSE, na="",col.names=TRUE, sep=",")		# Read the "mtcars" data frame as a csv file and store only the columns "cyl","am" and "gear".
new.mtcars <- read.table("mtcars.csv",sep=",",header=TRUE,nrows = 5)									# Store 5 records from the csv file as a new data frame.
write.filename = file("/web/com/binmtcars.dat", "wb")																	# Create a connection object to write the binary file using mode "wb".
writeBin(colnames(new.mtcars), write.filename)																			# Write the column names of the data frame to the connection object.
writeBin(c(new.mtcars$cyl,new.mtcars$am,new.mtcars$gear), write.filename)							# Write the records in each of the column to the file.
close(write.filename)																													# Close the file for writing so that it can be read by other program.

read.filename <- file("/web/com/binmtcars.dat", "rb")																		# Create a connection object to read the file in binary mode using "rb".
column.names <- readBin(read.filename, character(),  n = 3)														# First read the column names. n=3 as we have 3 columns.
read.filename <- file("/web/com/binmtcars.dat", "rb")																		# Next read the column values. n=18 as we have 3 column names and 15 values.
bindata <- readBin(read.filename, integer(),  n = 18)
cyldata = bindata[4:8]																													# Read the values from 4th byte to 8th byte which represents "cyl".
amdata = bindata[9:13]																												# Read the values form 9th byte to 13th byte which represents "am".
geardata = bindata[14:18]																											# Read the values form 9th byte to 13th byte which represents "gear".
finaldata = cbind(cyldata, amdata, geardata)																				# Combine all the read values to a dat frame.
colnames(finaldata) = column.names
print(finaldata)


# XML Files
install.packages("XML")
library("XML")
library("methods")
result <- xmlParse(file="input.xml")
rootnode <- xmlRoot(result)
rootsize <- xmlSize(rootnode)
rootnode[1]
rootnode[[1]][[1]]								# Get the first element of the first node.
rootnode[[1]][[5]]								# Get the fifth element of the first node.
rootnode[[3]][[2]]								# Get the second element of the third node.
xmldataframe <- xmlToDataFrame("input.xml")			# Convert the input xml file to a data frame.


# JSON File
install.packages("rjson")
library("rjson")
result <- fromJSON(file="input.json")
json_data_frame <- as.data.frame(result)			# Convert JSON file to a data frame.


# Web Data
install.packages("RCurl")
install.packages("XML")
install.packages("stringr")
install.packages("pylr")
url <- "http://www.geos.ed.ac.uk/~weather/jcmb_ws/"							# Read the URL.
links <- getHTMLLinks(url)																	# Gather the html links present in the webpage.
filenames <- links[str_detect(links, "JCMB_2015")]								# Identify only the links which point to the JCMB 2015 files. 
filenames_list <- as.list(filenames)														# Store the file names as a list.
downloadcsv <- function (mainurl,filename){										# Create a function to download the files by passing the URL and filename list.
	filedetails <- str_c(mainurl,filename)
	download.file(filedetails,filename)
}
l_ply(filenames,downloadcsv,mainurl="http://www.geos.ed.ac.uk/~weather/jcmb_ws/")				# Now apply the l_ply function and save the files into the current R working directory.


# Databases
install.packages("RMySQL")
mysqlconnection = dbConnect(MySQL(), user='root', password='', dbname='sakila', host='localhost')			# Create a connection Object to MySQL database.
dbListTables(mysqlconnection)																													# List the tables available in this database.
result = dbSendQuery(mysqlconnection, "select * from actor")																		# Query the "actor" tables to get all the rows.
data.frame = fetch(result, n=5)																														# Store the result in a R data frame object. n=5 is used to fetch first 5 rows.
data.frame = fetch(result, n=-1)																													# Fetch all the records
dbSendQuery(mysqlconnection, "update mtcars set disp = 168.5 where hp = 110")
dbSendQuery(mysqlconnection,
"insert into mtcars(row_names, mpg, cyl, disp, hp, drat, wt, qsec, vs, am, gear, carb)
values('New Mazda RX4 Wag', 21, 6, 168.5, 110, 3.9, 2.875, 17.02, 0, 1, 4, 4)"
)
dbWriteTable(mysqlconnection, "mtcars", mtcars[, ], overwrite = TRUE)
dbSendQuery(mysqlconnection, 'drop table if exists mtcars')
