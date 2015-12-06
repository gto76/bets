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

BOOKIE_NAME = "WilliamHill"
BOOKIE_URL = "http://sports.williamhill.com/bet/en-gb/betting/g/5131733/Player-Performance.html"

def main():
  htmls = util.getHtml(sys.argv, selenium, BOOKIE_NAME)
  players = []
  for html in htmls:
    players.extend(getPlayers(html))
  util.printPlayers(players)

def selenium():
  with closing(Firefox()) as browser:
    browser.get(BOOKIE_URL)
    util.wait(browser, "//div[@id='contentHead']")
    links = getMatchLinks(browser.page_source)



def getPlayers(html):
  soup = BeautifulSoup(html, "html.parser")
  pll = soup.findAll("tr", "ev_even_row")
  players = []
  for p in pll:
    nameAndPoints = p.find("span").find(text=True)
    odds = p.findAll("td", "ev_pick_cell")
    under = odds[0].find(text=True)
    over = odds[1].find(text=True)
    player = util.Player()
    player.nameAndPoints = nameAndPoints
    player.under = under
    player.over = over
    players.append(player)
  return players

if __name__ == '__main__':
  main()
