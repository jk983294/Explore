setwd("E:/GitHub/Explore/R_WorkSpace/learning/data_clean")

mydata <- read.table(
    file = "to_process.txt",
    sep = ",",
    header = TRUE,
    quote = "\""
)

# peek at data
head(mydata)

# names of column
names(mydata)

# rename column
names(mydata)[4] <- "start_date"

# missing values
sum(is.na(mydata))

# exclude missing value rows
mydata <- na.omit(mydata)

# remove units
salary <- as.character(mydata$salary)
head(salary)
class(salary)
salary <- sub(" dollor", "", salary)
head(salary)
mydata$salary <- as.double(salary)
head(mydata$salary)
class(mydata$salary)

# convert units to single unit (K/M/Bn -> real number)
convertMoney <- function(money){
    stringMoney <- as.character(money)
    replacedStringMoney <- gsub("[$|K|M|Bn]", "", stringMoney)
    numericMoney <- as.numeric(replacedStringMoney)
    if(grepl("M", money)){
        numericMoney * 1000000
    } else if(grepl("Bn", money)){
        numericMoney * 1000000000
    } else if(grepl("K", money)){
        numericMoney * 1000
    } else {
        numericMoney
    }
}
mydata$bouns <- sapply(mydata$bouns, convertMoney)
mean(mydata$bouns)

# save data to csv
write.csv(mydata, "mydata.csv")
