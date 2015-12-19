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

BOOKIE_NAME = "Lsbet"
BOOKIE_URL = "https://www.lsbet.com/en-GB/sportsbook/eventpaths/multi/[223517]?utf8=%E2%9C%93&filter_options%5B%5D=450%7C209&commit=Refresh"

def main():
  htmls = util.getHtml(sys.argv, selenium, BOOKIE_NAME)
  players = []
  for html in htmls:
    players.extend(getPlayers(html))
  util.output(sys.argv, players)

def selenium():
  with closing(Firefox()) as browser:
    browser.get(BOOKIE_URL)
    WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.XPATH, "//span[@class='name ellipsis']")))
    return [browser.page_source]

def getPlayers(html):
  soup = BeautifulSoup(html, "html.parser")
  pll = soup.findAll("span", "name ellipsis")
  pl = soup.findAll("span", "formatted_price")
  players = []
  for A, B in util.pairwise(zip(pll, pl)):
    print(A[0].find(text=True))
    print(A[1].find(text=True))
    print(B[0].find(text=True))
    print(B[1].find(text=True))
    name, surname = getNameAndSurname(A[0].find(text=True))
    points = getPoints(A[0].find(text=True))
    under = A[1].find(text=True)
    over = B[1].find(text=True)
    player = util.getPlayer(name, surname, points, under, over, BOOKIE_NAME, BOOKIE_URL)
    players.append(player)
  return players

def getNameAndSurname(string):
  name = re.sub(" -.*", "", string)
  print(name)
  names = name.split(',')
  firstName = names[1].strip().split(' ')[0]
  surname = names[0]
  return firstName, surname

def getPoints(string):
  return re.sub(".* ", "", string)

if __name__ == '__main__':
  main()
