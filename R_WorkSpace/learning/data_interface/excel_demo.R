# Excel File
install.packages("xlsx", repos = "http://mirror.bjtu.edu.cn/cran/")
any(grepl("xlsx",installed.packages()))			# Verify the package is installed.
library("xlsx")
data <- read.xlsx("input.xlsx", sheetIndex = 1)