#!/usr/bin/python3
#
# Usage: favbet.py 
# https://www.favbet.com/en/bets/#tour=17745&event=4198442

import json
import os
import re
import sys
import glob

from bs4 import BeautifulSoup
from contextlib import closing
from selenium.webdriver import Firefox 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

import util

BOOKIE_NAME = "Marathonbet"
BOOKIE_URL = "https://www.marathonbet.com/hr/betting/Basketball/NBA/"
# TEST_FILE = "marathonbet.html"

def main():
  dates, htmls = getHtml(sys.argv)
  players = []
  for date, html in zip(dates, htmls):
    date = cleanDate(date)
    players.extend(getPlayers(html, date))
  util.printPlayers(players)

def getHtml(argv):
  if len(argv) > 1:
    if argv[1] != "save":
      return getFiles()
      # return (['\n   06 pro 02:30\n    '], [open(TEST_FILE, encoding='utf8')])
    else:
      save()
  return selenium()

def getFiles():
  files = []
  dates = []
  filenames = glob.glob(util.TEST_FOLDER+'/'+BOOKIE_NAME.lower()+'*.html')
  for filename in filenames:
    files.append(open(filename, encoding='utf8'))
    dates.append('\n   06 pro 02:30\n    ')
  return dates, files

def save():
  _, htmls = selenium()
  i = 0
  for html in htmls:
    filename = util.TEST_FOLDER+"/"+BOOKIE_NAME.lower()+str(i)+".html"
    f = open(filename,'w')
    f.write(html)
    f.close()
    i += 1
  exit(0)

def selenium():
  with closing(Firefox()) as browser:
    browser.get(BOOKIE_URL)
    WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='member-name nowrap ']")))
    dates = getDates(browser.page_source)
    elements = browser.find_elements_by_xpath("//div[@class='member-name nowrap ']")
    out = []
    for e in elements[::2]:
      e.click()
      WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.XPATH, "//table[@class='table-shortcuts-menu']")))
      out.append(browser.page_source)
      e.click()
    return (dates, out)

def getDates(html):
  soup = BeautifulSoup(html, "html.parser")
  pl = soup.findAll("td", "date")
  out = []
  for p in pl:
    out.append( p.find(text=True))
  return out
  
def getPlayers(html, date):
  soup = BeautifulSoup(html, "html.parser")
  players = []
  pl = soup.findAll("td", "price width30")
  for a, b in util.pairwise(pl):
    player = util.Player()
    respA = json.loads(a["data-sel"])
    player.player_name = cleanName(respA["mn"])
    player.player_total = cleanPoints(respA["sn"])
    player.under = respA["epr"]
    respB = json.loads(b["data-sel"])
    player.over = respB["epr"]
    player.start_time = date
    player.bookie_name = BOOKIE_NAME
    player.bookie_url = BOOKIE_URL
    players.append(player)
  return players

def cleanDate(date):
  date = re.sub("^\n *", "", date)
  return re.sub("\n *$", "", date)

def cleanName(name):
  name = re.sub("Points \(", "", name)
  return re.sub("[,)]", "", name)

def cleanPoints(points):
  return re.sub("^[^0-9]*", "", points)

if __name__ == '__main__':
  main()