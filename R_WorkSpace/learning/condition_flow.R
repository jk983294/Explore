# if
x <- 30L
if(is.integer(x)){
    print("X is an Integer")
}

x <- c("what","is","truth")
if("Truth" %in% x){
    print("Truth is found")
} else {
    print("Truth is not found")
}

# switch
x <- switch(
    3,
    "first",
    "second",
    "third",
    "fourth"
)
print(x)

# repeat
v <- c("Hello","loop")
cnt <- 2
repeat{
    print(v)
    cnt <- cnt+1
    if(cnt > 5){
        break
    }
}

# while
while (cnt < 7){
    print(v)
    cnt = cnt + 1
}

# for
v <- LETTERS[1:6]
for ( i in v){
    if (i == "D"){
        next        # continue
    }
    print(i)
}