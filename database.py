"""Module database"""
import mysql.connector
from table import Tableprint

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

    def get_all_scores(self):
        """Getting all scores"""
        self.mycursor.callproc('show_all_score')
        for result in self.mycursor.stored_results():
            res = result.fetchall()
        table_print = Tableprint()
        table_print.print_all_scores(res)
