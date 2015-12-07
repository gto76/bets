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

BOOKIE_NAME = "Marathonbet"
BOOKIE_URL = "https://www.marathonbet.com/hr/betting/Basketball/NBA/"

def main():
  htmls = util.getHtml(sys.argv, selenium, BOOKIE_NAME)
  players = []
  for html in htmls:
    players.extend(getPlayers(html))
  util.printPlayers(players)
  util.insertPlayersInDb(players)

def selenium():
  with closing(Firefox()) as browser:
    browser.get(BOOKIE_URL)
    WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='member-name nowrap ']")))
    dates = getDates(browser.page_source)
    elements = browser.find_elements_by_xpath("//div[@class='member-name nowrap ']")
    htmls = []
    for e in elements[::2]:
      e.click()
      WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.XPATH, "//table[@class='table-shortcuts-menu']")))
      htmls.append(browser.page_source)
      e.click()
    return htmls

def getDates(html):
  soup = BeautifulSoup(html, "html.parser")
  pl = soup.findAll("td", "date")
  out = []
  for p in pl:
    out.append( p.find(text=True))
  return out
  
def getPlayers(html):
  soup = BeautifulSoup(html, "html.parser")
  players = []
  pl = soup.findAll("td", "price width30")
  for a, b in util.pairwise(pl):
    player = util.Player()
    respA = json.loads(a["data-sel"])
    name, surname = cleanName(respA["mn"])
    fullName, time = util.getFullNameAndTime(name, surname)
    player.player_name = fullName
    player.player_total = cleanPoints(respA["sn"])
    player.under = "%.2f" % float(respA["epr"])
    respB = json.loads(b["data-sel"])
    player.over = "%.2f" % float(respB["epr"])
    player.start_time = time
    player.bookie_name = BOOKIE_NAME
    player.bookie_url = BOOKIE_URL
    players.append(player)
  return players

def cleanName(name):
  name = re.sub("Points \(", "", name)
  name = re.sub("[,)]", "", name)
  names = name.split(' ')
  # McCollum Christian James -> C.J. McCollum
  if len(names) == 3:
    return names[1][0]+"."+names[2][0]+".", names[0]
  else:
    return names[1], names[0]

def cleanPoints(points):
  return re.sub("^[^0-9]*", "", points)

if __name__ == '__main__':
  main()