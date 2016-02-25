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
xmldataframe <- xmlToDataFrame("input.xml")		# Convert the input xml file to a data frame.