# Scatterplots
input <- mtcars[,c('wt','mpg')]
png(file = "scatterplot.png")
plot(x = input$wt,y = input$mpg,
     xlab = "Weight",
     ylab = "Milage",
     xlim = c(2.5,5),
     ylim = c(15,30),
     main = "Weight vs Milage"
)
dev.off()

# Scatterplot Matrices
png(file = "scatterplot_matrices.png")
pairs(~wt+mpg+disp+cyl,data = mtcars,main = "Scatterplot Matrix")
dev.off()