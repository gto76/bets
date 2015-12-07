import csv
import glob
from pprint import pprint
import re

import pymysql.cursors
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

TEST_FOLDER = "htmls"

class Player:
  pass

def pairwise(t):
    it = iter(t)
    return zip(it,it)

def printSoup(soup):
  for a in soup:
    print(a)
    print()

def printPlayers(players):
  for p in players:
    pprint (vars(p))

def getHtml(argv, selenium, bookieName):
  if len(argv) > 1:
    if argv[1] != "save":
      return getFiles(bookieName)
    else:
      save(selenium, bookieName)
  return selenium()

def getFiles(bookieName):
  files = []
  filenames = glob.glob(TEST_FOLDER+'/'+bookieName.lower()+'*.html')
  for filename in filenames:
    files.append(open(filename, encoding='utf8'))
  return files

def save(selenium, bookieName):
  htmls = selenium()
  i = 0
  for html in htmls:
    filename = TEST_FOLDER+"/"+bookieName.lower()+str(i)+".html"
    f = open(filename,'w')
    f.write(html)
    f.close()
    i += 1
  exit(0)

############
# Selenium #
############

def waitAndClick(browser, identifier):
  wait(browser, identifier)
  click(browser, identifier)

def wait(browser, identifier):
  WebDriverWait(browser, timeout=20).until(EC.presence_of_element_located((By.XPATH, identifier)))

def click(browser, identifier):
  browser.find_element_by_xpath(identifier).click()

#######
# CSV #
#######

sheetPlayers = ""
sheetTeams = ""
sheetGames = ""

def checkSheets():
  if sheetPlayers == "":
    setSheets()

def setSheets():
  global sheetPlayers
  global sheetTeams
  global sheetGames
  sheetPlayers = getSheet('players.csv')
  sheetTeams = getSheet('teams.csv')
  sheetGames = getSheet('games.csv')

def getSheet(filename):
  with open(filename, "rt", encoding='utf8') as csvFile:
    sheet = csv.reader(csvFile)
    return list(sheet)

def getFullNameAndTime(name, surname):
  pattern = name+".* "+surname
  nameFull, team = getPlayersRow(pattern)
  teamFull = getFullTeam(team)
  time = getTime(teamFull)
  return nameFull+" ("+team+")", time

def getPlayersRow(pattern):
  global sheetPlayers
  checkSheets()
  for row in sheetPlayers:
    if re.match(pattern, row[1]):
      return row[1], row[2]
  return "FAIL_NAME", "FAIL"

def getFullTeam(team):
  checkSheets()
  for row in sheetTeams:
    if row[1] == team:
      return row[0]

def getTime(team):
  checkSheets()
  for row in sheetGames:
    if row[1] == team or row[2] == team:
      time = re.sub("\n", "", row[8])
      return re.sub(" ", "", time)
  return "FAIL"

###########
# PyMySql #
###########

def insertPlayersInDb(players):
  connection = pymysql.connect(host='denis.afiniti.org',
                               user='denis',
                               password='Klada1977&',
                               db='odds',
                               charset='utf8mb4',
                               cursorclass=pymysql.cursors.DictCursor)
  try:
    with connection.cursor() as cursor:
      for player in players:
        sql = "INSERT INTO `odds` (`bookie_name`, `bookie_url`, `start_time`, `player_name`, `player_total`, `over`, `under`) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (player.bookie_name ,player.bookie_url ,player.start_time ,player.player_name ,player.player_total ,player.over ,player.under))
    connection.commit()
  finally:
    connection.close()  

