#Exercise 1, sqlite
import sqlite3
from pprint import pprint
from collections import defaultdict
conn = sqlite3.connect('northwind.db')
conn.text_factory = lambda x: str(x, 'latin1')
    
#construct query
query = """
SELECT Orders.OrderID, Products.ProductID, Products.CategoryID,  Products.ProductName
FROM Products 
    INNER JOIN [Order Details] ON Products.ProductID = [Order Details].ProductID
    INNER JOIN Orders ON Orders.OrderID == [Order Details].OrderID
WHERE Orders.CustomerID == "ALFKI"
"""

res = conn.execute(query)

#put result into a dictionary 
d = defaultdict(dict)
for row in res:
    d[row[0]][row[1]] = {"Cat":row[2], "Name":row[3]}
    
conn.close() #Close connection to DB after we are done processing

pprint(dict(d))

"""Result:
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