#!/usr/bin/python3
#
# Usage: get-name.py 
# 

import sys
import re
import csv

import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials

def main():
  csvFile = open('players.csv', "rt", encoding='utf8')
  sheetPlayers = csv.reader(csvFile)
  csvFile2 = open('games.csv', "rt", encoding='utf8')
  sheetGames = csv.reader(csvFile2)

  pattern = re.compile("T.* Zeller")
  name, team = getPlayersRow(sheetPlayers, pattern)
  print(name + ", "+ team)

def getPlayersRow(sheet, name):
  for row in sheet:
    if name.match(row[1]):
      return row[1], row[2]

if __name__ == '__main__':
  main()