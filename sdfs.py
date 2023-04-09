import  sqlite3
conn=sqlite3.connect("login.db")
cursor = conn.execute("SELECT * from ADMIN")
print("ID\tUSERNAME\tPASSWORD")
for row in cursor:
   print ("{}\t{}\t\t{}".format(row[0],row[1],row[2]))
conn.close()