#!/usr/bin/python3
#
# Usage: favbet.py 
# https://www.favbet.com/en/bets/#tour=17745&event=4198442

import json
import os
import sys
from pprint import pprint

from bs4 import BeautifulSoup
from contextlib import closing
from selenium.webdriver import Firefox 
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

BOOKIE_NAME =
BOOKIE_URL = 

class Player:
  pass

def main():
  dates, htmls = selenium()
  players = []
  for date, html in zip(dates, htmls):
    players.extend(getPlayers(html, date))
  for p in players:
    pprint (vars(p))

def selenium():
  with closing(Firefox()) as browser:
    browser.get('https://www.marathonbet.com/hr/betting/Basketball/NBA/')
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
  for a, b in pairwise(pl):
    player = Player()
    respA = json.loads(a["data-sel"])
    player.player_name = respA["mn"]
    player.player_total = respA["sn"]
    player.under = respA["epr"]
    respB = json.loads(b["data-sel"])
    player.over = respB["epr"]
    player.start_time = date
    players.append(player)
  return players

def pairwise(t):
    it = iter(t)
    return zip(it,it)

def printSoup(soup):
  for a in soup:
    print(a)
    print()

if __name__ == '__main__':
  main()