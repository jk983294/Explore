# Bar Charts
H <- c(7,12,28,3,41)
M <- c("Mar","Apr","May","Jun","Jul")
png(file = "barchart.png")
barplot(H,names.arg = M,xlab = "Month",ylab = "Revenue",col = "blue", main = "Revenue chart",border = "red")
dev.off()

# Group Bar Chart and Stacked Bar Chart
colors <- c("green","orange","brown")
months <- c("Mar","Apr","May","Jun","Jul")
regions <- c("East","West","North")
Values <- matrix(c(2,9,3,11,9,4,8,7,3,12,5,2,8,10,11),nrow = 3,ncol = 5,byrow = TRUE)
png(file = "barchart_stacked.png")
barplot(Values,main = "total revenue",names.arg = months,xlab = "month",ylab = "revenue",col = colors)
legend("topleft", regions, cex = 1.3, fill = colors)
dev.off()