#!/usr/bin/python3
#
# Usage: db-test.py 
# 

# import MySQLdb
import sys
import re

import pymysql.cursors
# import pyodbc

def main():
  # db = MySQLdb.connect(host="denis.afiniti.org",    # your host, usually localhost
  #                      user="denis",         # your username
  #                      passwd="Klada1977&",  # your password
  #                      db="odds")        # name of the data base

  # # you must create a Cursor object. It will let
  # #  you execute all the queries you need
  # cur = db.cursor()

  # # Use all the SQL you like
  # cur.execute("SELECT * FROM ODDS")

  # # print all the first cell of all the rows
  # for row in cur.fetchall():
  #     print(row[0])
  # DB_CONNECT_STRING = 'DRIVER={MySQL ODBC 3.51 Driver};SERVER=denis.afiniti.org;DATABASE=stave;UID=denis;PWD=Klada1977&'


  # DB_CONNECT_STRING = 'DRIVER={SQL Server};SERVER=denis.afiniti.org;DATABASE=stave;UID=denis;PWD=Klada1977&'
  # cnxn = pyodbc.connect(DB_CONNECT_STRING)
  # cursor = cnxn.cursor()
  # sql="SELECT * FROM ODDS"
  # rows= cursor.execute(sql).fetchall()
  # print(rows)
  # cnxn.commit()     

  # Connect to the database
  connection = pymysql.connect(host='denis.afiniti.org',
                               user='denis',
                               password='Klada1977&',
                               db='odds',
                               charset='utf8mb4',
                               cursorclass=pymysql.cursors.DictCursor)

  try:
    # with connection.cursor() as cursor:
      # Create a new record
    #   sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
    #   cursor.execute(sql, ('webmaster@python.org', 'very-secret'))

    # # connection is not autocommit by default. So you must commit to save
    # # your changes.
    # connection.commit()

    with connection.cursor() as cursor:
      # Read a single record
      sql = "SELECT * FROM `odds`"
      cursor.execute(sql)#, ('webmaster@python.org',))
      result = cursor.fetchone()
      print(result)
  finally:
    connection.close()    

if __name__ == '__main__':
  main()
