import mysql.connector


mydb = mysql.connector.connect(
  host="localhost",
  user="kent",
  password="kent",
  database="yatzy"
)


mycursor = mydb.cursor()

""" sql = "INSERT INTO players (name, point) VALUES (%s, %s)"
val = ("Snolep", 450)
mycursor.execute(sql, val)

mydb.commit()

print(mycursor.rowcount, "record inserted.")
 """
mycursor.execute("SELECT * FROM players")

myresult = mycursor.fetchall()

for x in myresult:
  print(x)

