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
list_data[4] <- NULL						# Remove the last element.
list_data[3] <- "updated element"			# Update the 3rd Element.

# Converting List to Vector
list1 <- list(1:5)
list2 <-list(10:14)
v1 <- unlist(list1)
v2 <- unlist(list2)
result <- v1+v2

# Merging Lists
merged.list <- c(list1,list2)