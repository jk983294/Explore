# Binary Files
write.table(mtcars, file = "mtcars.csv",row.names=FALSE, na="",col.names=TRUE, sep=",")		# Read the "mtcars" data frame as a csv file and store only the columns "cyl","am" and "gear".
new.mtcars <- read.table("mtcars.csv",sep=",",header=TRUE,nrows = 5)						# Store 5 records from the csv file as a new data frame.
write.filename = file("/web/com/binmtcars.dat", "wb")										# Create a connection object to write the binary file using mode "wb".
writeBin(colnames(new.mtcars), write.filename)												# Write the column names of the data frame to the connection object.
writeBin(c(new.mtcars$cyl,new.mtcars$am,new.mtcars$gear), write.filename)					# Write the records in each of the column to the file.
close(write.filename)																		# Close the file for writing so that it can be read by other program.

read.filename <- file("/web/com/binmtcars.dat", "rb")										# Create a connection object to read the file in binary mode using "rb".
column.names <- readBin(read.filename, character(),  n = 3)									# First read the column names. n=3 as we have 3 columns.
read.filename <- file("/web/com/binmtcars.dat", "rb")										# Next read the column values. n=18 as we have 3 column names and 15 values.
bindata <- readBin(read.filename, integer(),  n = 18)
cyldata = bindata[4:8]																		# Read the values from 4th byte to 8th byte which represents "cyl".
amdata = bindata[9:13]																		# Read the values form 9th byte to 13th byte which represents "am".
geardata = bindata[14:18]																	# Read the values form 9th byte to 13th byte which represents "gear".
finaldata = cbind(cyldata, amdata, geardata)												# Combine all the read values to a dat frame.
colnames(finaldata) = column.names
print(finaldata)