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

BOOKIE_NAME = "Meridianbet"
BOOKIE_URL = "https://meridianbet.com/#!standard_betting;leagueIDs=593"
# TEST_FILE = "meridianbet.html"

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
    WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='gwt-Label home']")))
    return browser.page_source

def getPlayers(html):
  soup = BeautifulSoup(html, "html.parser")
  dates = soup.findAll("div", "gwt-Label date")
  times = soup.findAll("div", "gwt-Label time")
  pl = soup.findAll("div", "rivals")
  pa = soup.findAll("div", "selections three four")
  players = []
  for date, time, a, b in zip(dates, times, pl, pa):
    players.append(getPlayer(date, time, a, b))
  return players

def getPlayer(date, time, a, b):
  odds = b.findAll("div", "gwt-Label")
  player = util.Player()
  player.player_name = a.find("div", "gwt-Label away").find(text=True)
  player.player_total = odds[7].find(text=True)
  player.under = odds[1].find(text=True)
  player.over = odds[5].find(text=True)
  player.start_time = date.find(text=True)+" "+time.find(text=True)
  player.bookie_name = BOOKIE_NAME
  player.bookie_url = BOOKIE_URL
  return player

if __name__ == '__main__':
  main()
