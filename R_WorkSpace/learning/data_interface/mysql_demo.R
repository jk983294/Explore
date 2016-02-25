# Databases
install.packages("RMySQL")
mysqlconnection = dbConnect(MySQL(), user='root', password='', dbname='sakila', host='localhost')   # Create a connection Object to MySQL database.
dbListTables(mysqlconnection)																		# List the tables available in this database.
result = dbSendQuery(mysqlconnection, "select * from actor")										# Query the "actor" tables to get all the rows.
data.frame = fetch(result, n=5)																		# Store the result in a R data frame object. n=5 is used to fetch first 5 rows.
data.frame = fetch(result, n=-1)																	# Fetch all the records
dbSendQuery(mysqlconnection, "update mtcars set disp = 168.5 where hp = 110")
dbSendQuery(mysqlconnection,
            "insert into mtcars(row_names, mpg, cyl, disp, hp, drat, wt, qsec, vs, am, gear, carb)
            values('New Mazda RX4 Wag', 21, 6, 168.5, 110, 3.9, 2.875, 17.02, 0, 1, 4, 4)"
)
dbWriteTable(mysqlconnection, "mtcars", mtcars[, ], overwrite = TRUE)
dbSendQuery(mysqlconnection, 'drop table if exists mtcars')
