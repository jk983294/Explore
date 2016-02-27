# Line Graphs
v <- c(7,12,28,3,41)
png(file = "line_chart.jpg")
plot(v,type = "o")
plot(v,type = "o", col = "red", xlab = "Month", ylab = "Rain fall",main = "Rain fall chart")
dev.off()

# Multiple Lines in a Line Chart
v <- c(7,12,28,3,41)
t <- c(14,7,6,19,3)
png(file = "line_chart_2_lines.jpg")
plot(v,type = "o",col = "red", xlab = "Month", ylab = "Rain fall", main = "Rain fall chart")
lines(t, type = "o", col = "blue")
dev.off()