#!/usr/bin/python3
#
# Usage: favbet.py 
# https://www.favbet.com/en/bets/#tour=17745&event=4198442

import json
import os
import re
import sys

from bs4 import BeautifulSoup
from contextlib import closing
from selenium.webdriver import Firefox 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

import util

BOOKIE_NAME = "Wwin"
BOOKIE_URL = "https://wwin.com/sports/default.aspx?t=-60#f/0/110/0/"
# TEST_FILE = "wwin.html"

def main():
  html = getHtml(sys.argv)
  players = getPlayers(html)
  util.printPlayers(players)

def getHtml(argv):
  if len(argv) > 1:
    if argv[1] != "save":
      return open(util.TEST_FOLDER+'/'+BOOKIE_NAME.lower()+'.html', encoding='utf8')
    else:
      save()
  return selenium()

def save():
  html = selenium()
  f = open(util.TEST_FOLDER+"/"+BOOKIE_NAME.lower()+".html",'w')
  f.write(html)
  f.close()
  exit(0)

def selenium():
  with closing(Firefox()) as browser:
    browser.get(BOOKIE_URL)
    WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='item'][@fullok='430']")))
    element = browser.find_element_by_xpath("//div[@class='item'][@fullok='430']")
    element.click()
    WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.XPATH, "//span[@class='ex1 ex22']")))
    return browser.page_source

def getPlayers(html):
  soup = BeautifulSoup(html, "html.parser")
  parovi = soup.find("table", "parovi extra")
  pl = parovi.findAll("tr", {"ot" : re.compile("[0-9]*")})
  players = []
  for a in pl:
    players.append(getPlayer(a))
  return players

def getPlayer(a):
  nameAndPoints = a.find("td", "parPar").find(text=True)
  odds = a.findAll("td", "tgp")
  player = util.Player()
  player.player_name = cleanName(nameAndPoints)
  player.player_total = cleanPoints(nameAndPoints)
  player.under = odds[1].find(text=True)
  player.over = odds[0].find(text=True)
  player.start_time = "NONE"
  player.bookie_name = BOOKIE_NAME
  player.bookie_url = BOOKIE_URL
  return player

def cleanName(nameAndPoints):
  name = re.sub("^.*/", "", nameAndPoints)
  return re.sub(" [().0-9]*$", "", name)
  # names = name.split('.') # Names in form: "R.Gobert", or "Jeff Green"
  # print(names[0] + " " + names[1])
  # return names[1]
  # return names[1] + " " + names[0] + "."

def cleanPoints(nameAndPoints):
  points = re.sub("^.*\(", "", nameAndPoints)
  return re.sub("\)$", "", points)

if __name__ == '__main__':
  main()
