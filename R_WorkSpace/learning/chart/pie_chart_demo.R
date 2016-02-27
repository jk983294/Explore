# Pie Charts
x <- c(21, 62, 10, 53)
labels <- c("London", "New York", "Singapore", "Mumbai")
piepercent<- round(100*x/sum(x), 1)
png(file = "city.jpg")					    # Give the chart file a name.
pie(x,labels)								# Plot the chart.
pie(x, labels = piepercent, main = "City pie chart",col = rainbow(length(x)))
legend("topright", c("London","New York","Singapore","Mumbai"), cex = 0.8, fill = rainbow(length(x)))
dev.off()									# Save the file.

# 3d pie charts
library(plotrix)
x <-  c(21, 62, 10,53)
lbl <-  c("London","New York","Singapore","Mumbai")
png(file = "3d_pie_chart.jpg")
pie3D(x,labels=lbl,explode=0.1, main="Pie Chart of Countries ")
dev.off()
