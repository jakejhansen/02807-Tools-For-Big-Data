import sqlite3
conn = sqlite3.connect('northwind.db')
conn.text_factory = lambda x: str(x, 'latin1')
    
query = """
SELECT Orders.EmployeeID, count(*), Employees.FirstName, Employees.LastName
    FROM Orders INNER JOIN Employees ON Orders.EmployeeID = Employees.EmployeeID
GROUP BY Orders.EmployeeID
ORDER BY count(*) DESC
"""
cursor = conn.execute(query)
print("(ID, Number of Orders, First name, Last name)")
for row in cursor:
    print(row)
    
conn.close()

"""Result:
(ID, Number of Orders, First name, Last name)
(4, 156, 'Margaret', 'Peacock')
(3, 127, 'Janet', 'Leverling')
(1, 123, 'Nancy', 'Davolio')
(8, 104, 'Laura', 'Callahan')
(2, 96, 'Andrew', 'Fuller')
(7, 72, 'Robert', 'King')
(6, 67, 'Michael', 'Suyama')
(9, 43, 'Anne', 'Dodsworth')
(5, 42, 'Steven', 'Buchanan')
"""