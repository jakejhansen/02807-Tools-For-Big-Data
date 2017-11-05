from pymongo import MongoClient
from pprint import pprint
from collections import defaultdict

#Connect to Mongo-Session and the database.
client = MongoClient('localhost', 27017)
db = client["Northwind"]

#construct query
cursor = db.orders.aggregate([
    {
        "$match" : {"CustomerID" : "ALFKI"}
    },
    {
      '$lookup': {
          'from': "order-details",
          'localField': "OrderID",
          'foreignField': "OrderID",
          'as': "order"
        }
    },
    {
      '$lookup': {
          'from': "products",
          'localField': "order.ProductID",
          'foreignField': "ProductID",
          'as': "order.products"
        }
    }, 
    {
        '$project': {
            "OrderID" : 1,
            "order.products.ProductID" : 1,
            "order.products.CategoryID" : 1,
            "order.products.ProductName" : 1
        }
    }
    
])

#Put the result into a dictionary
d = defaultdict(dict)
for row in cursor:
    for product in row["order"]["products"]:
        d[row["OrderID"]][product["ProductID"]] = {"Cat" : product["CategoryID"], "Name" : product["ProductName"]}
        
pprint(dict(d))

""" Result:
{10643: {28: {'Cat': 7, 'Name': 'Rössle Sauerkraut'},
         39: {'Cat': 1, 'Name': 'Chartreuse verte'},
         46: {'Cat': 8, 'Name': 'Spegesild'}},
 10692: {63: {'Cat': 2, 'Name': 'Vegie-spread'}},
 10702: {3: {'Cat': 2, 'Name': 'Aniseed Syrup'},
         76: {'Cat': 1, 'Name': 'Lakkalikööri'}},
 10835: {59: {'Cat': 4, 'Name': 'Raclette Courdavault'},
         77: {'Cat': 2, 'Name': 'Original Frankfurter grüne Soße'}},
 10952: {6: {'Cat': 2, 'Name': "Grandma's Boysenberry Spread"},
         28: {'Cat': 7, 'Name': 'Rössle Sauerkraut'}},
 11011: {58: {'Cat': 8, 'Name': 'Escargots de Bourgogne'},
         71: {'Cat': 4, 'Name': 'Flotemysost'}}}
 """