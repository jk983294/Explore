a <- 'Start and ""end with single quote'
b <- "Start and ''end with double quotes"

# paste
a <- "Hello"
b <- 'How'
c <- "are you? "
paste(a,b,c)
paste(a,b,c, sep = "-")
paste(a,b,c, sep = "", collapse = "")

# Counting number of characters in a string
nchar("Count the number of characters")

# substring
substring("Extract", 5, 7)

# upper case, lower case
toupper("Changing To Upper")
tolower("Changing To Lower")

# formatting
format(23.123456789, digits = 9)              # Last digit rounded off.
format(c(6, 13.14521), scientific = TRUE)
format(23.47, nsmall = 5)                     # The minimum number of digits to the right of the decimal point.
format(6)                                     # Format treats everything as a string.
format(13.7, width = 6)                       # Numbers are padded with blank in the beginning for width.
format("Hello",width = 8, justify = "l")      # Left justify strings.
format("Hello",width = 8, justify = "c")      # Justfy string with center.
format("Hello",width = 8, justify = "r")      # Right justify strings.
