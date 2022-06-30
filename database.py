"""Module database"""
import mysql.connector

class Database:
    """Database class"""

    mydb = mysql.connector.connect(
    host="localhost",
    user="kent",
    password="kent",
    database="yatzy"
    )

    def __init__(self):
        """Initialize class"""
        self.mycursor = self.mydb.cursor()

    def insert_score(self, namn, value):
        """Insert name, score and date"""
        sql = "INSERT INTO score (namn, total) VALUES (%s, %s)"
        val = (namn, value)
        self.mycursor.execute(sql, val)

        self.mydb.commit()

        print(self.mycursor.rowcount, "record inserted.")

        self.mycursor.execute("SELECT * FROM score")

        myresult = self.mycursor.fetchall()

        for x in myresult:
            print(x)

