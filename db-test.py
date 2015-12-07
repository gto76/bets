#!/usr/bin/python3
#
# Usage: db-test.py 
# 

import sys
import re

import pymysql.cursors

def main():
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
