# JSON File
install.packages("rjson")
library("rjson")
result <- fromJSON(file="input.json")
json_data_frame <- as.data.frame(result)			# Convert JSON file to a data frame.
