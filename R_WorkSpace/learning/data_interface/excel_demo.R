# Excel File
install.packages("xlsx")
any(grepl("xlsx",installed.packages()))			# Verify the package is installed.
library("xlsx")
data <- read.xlsx("input.xlsx", sheetIndex = 1)