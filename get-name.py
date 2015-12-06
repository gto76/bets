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
  csvFile3 = open('teams.csv', "rt", encoding='utf8')
  sheetTeams = csv.reader(csvFile3)

  pattern = re.compile("K.* Bryant")
  name, team = getPlayersRow(sheetPlayers, pattern)
  print(name + ", "+ team)

  teamFull = getFullTeam(sheetTeams, team)
  print(teamFull)

  time = getTime(sheetGames, teamFull)
  print(time)

def getPlayersRow(sheet, name):
  for row in sheet:
    if name.match(row[1]):
      return row[1], row[2]

def getFullTeam(sheet, team):
  for row in sheet:
    if row[1] == team:
      return row[0]

def getTime(sheet, team):
  for row in sheet:
    if row[1] == team or row[2] == team:
      return row[8]


if __name__ == '__main__':
  main()