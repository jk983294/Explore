library(rmongodb)
# connect to MongoDB
mongo = mongo.create(host = "localhost")
mongo.is.connected(mongo)

# show the databases
mongo.get.databases(mongo)
# all of the collections (tables) in one of the db's.
mongo.get.database.collections(mongo, db = "prod")

# count how many documents (rows) we have in a collection.
DBNS = "prod.Stock"
mongo.count(mongo, ns = DBNS)

# query one
tmp = mongo.find.one(mongo, ns = "prod.Stock")
tmp = mongo.bson.to.list(tmp)
names(tmp)

# query all
allStockInfo = mongo.find.all(mongo, ns = "prod.StockInfo")
class(allStockInfo)
nrow(allStockInfo)

# close connection
mongo.disconnect(mongo)
mongo.destroy(mongo)
