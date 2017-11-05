from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client["Northwind"]

cursor = db.orders.aggregate([
    {
        "$group": {
        "_id": "$EmployeeID",
        "count": { "$sum": 1 }
        }
    },
    {
        "$sort": { "count": -1 } 
    },
    {
        "$lookup" : {
          'from': "employees",
          'localField': "_id",
          'foreignField': "EmployeeID",
          'as': "empl"
        }
    },
    {
        "$project" : {
            "EmployeeID" : 1,
            "count" : 1,
            "empl.FirstName": 1,
            "empl.LastName": 1
        }
    }
])

print("(ID, Number of Orders, First name, Last name)")
for row in cursor:
    print(row["_id"], row["count"], row["empl"][0]["FirstName"], row["empl"][0]["LastName"], sep=', ')
    
"""Result:
(ID, Number of Orders, First name, Last name)
4, 156, Margaret, Peacock
3, 127, Janet, Leverling
1, 123, Nancy, Davolio
8, 104, Laura, Callahan
2, 96, Andrew, Fuller
7, 72, Robert, King
6, 67, Michael, Suyama
9, 43, Anne, Dodsworth
5, 42, Steven, Buchanan
"""