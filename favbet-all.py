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

BOOKIE_NAME = "Favbet"
BOOKIE_URL = "https://www.favbet.com/en/bets/#tour=17745"

def main():
  htmls = util.getHtml(sys.argv, selenium, BOOKIE_NAME)
  players = []
  for html in htmls:
    players.extend(getPlayers(html))
  util.output(sys.argv, players)

def selenium():
  with closing(Firefox()) as browser:
    browser.get(BOOKIE_URL)
    WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.XPATH, "//b[@class='ttt']")))
    (links, dates) = getLinksAndDates(browser.page_source)
    htmls = []
    for link in links:
      element = browser.find_element_by_xpath("//*[contains(text(), '"+link+"')]")
      element.click()
      WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.XPATH, "//ul[@class='market_groups']")))
      htmls.append(browser.page_source)
    return htmls

def getLinksAndDates(html):
  soup = BeautifulSoup(html, "html.parser")
  pl = soup.findAll("ul", "sel-itm cl")
  links = []
  dates = []
  for p in pl:
    link = p.find("li", "col0").find("span").find(text=True)
    links.append(link)
    date = p.find("li", "col1").find("span").find(text=True)
    dates.append(date)
  return (links, dates)

def getPlayers(html):
  soup = BeautifulSoup(html, "html.parser")
  pl = soup.find("li", {"data-clue" : "Over/Under points (player)"})
  players = []
  names = pl.findAll("span", "bets_oc ttt")
  odds = pl.findAll("button", "betbut a")
  for a, b in util.pairwise(zip(names, odds)):
    player = util.Player()
    name, surname = cleanName(a[0].find(text=True))
    fullName, time = util.getFullNameAndTime(name, surname)
    player.player_name = fullName
    player.player_total = cleanPoints(a[0].find(text=True))
    player.under = a[1].find(text=True)
    player.over = b[1].find(text=True)
    player.start_time = time
    player.bookie_name = BOOKIE_NAME
    player.bookie_url = BOOKIE_URL
    players.append(player)
  return players
  
def cleanName(name):
  name = re.sub("^Over [0-9()\. ]*", "", name)
  names = name.split(' ')
  return names[0], names[1]

def cleanPoints(points):
  points = re.sub("^.*\(", "", points)
  return re.sub("\).*$", "", points)

if __name__ == '__main__':
  main()
