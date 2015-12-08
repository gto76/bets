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
from selenium.webdriver import PhantomJS
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

import util

BOOKIE_NAME = "Betx"
BOOKIE_URL = "https://www.betx.sk/SportBetting"

def main():
  htmls = util.getHtml(sys.argv, selenium, BOOKIE_NAME)
  players = []
  for html in htmls:
    players.extend(getPlayers(html))
  util.output(sys.argv, players)

def selenium():
  with closing(Firefox()) as browser:
  # with closing(PhantomJS()) as browser:
    browser.get(BOOKIE_URL)
    util.waitAndClick(browser, "//li[@id='sportMenuItem_391']")
    util.waitAndClick(browser, "//li[@id='cId_2462']")
    util.waitAndClick(browser, "//li[@id='league_13945']")
    util.wait(browser, "//span[contains(text(), 'Basketball / USA / NBA - Player points (-/+)')]")
    return [browser.page_source]

def getPlayers(html):
  soup = BeautifulSoup(html, "html.parser")
  pll = soup.findAll("tr", "ev_even_row")
  players = []
  for p in pll:
    nameAndPoints = p.find("span").find(text=True)
    name, surname = getNames(nameAndPoints)
    points = getPoints(nameAndPoints)
    odds = p.findAll("td", "ev_pick_cell")
    under = re.sub(",", ".", odds[0].find(text=True))
    over = re.sub(",", ".", odds[1].find(text=True))
    player = util.getPlayer(name, surname, points, under, over, BOOKIE_NAME, BOOKIE_URL)
    players.append(player)
  return players

def getNames(nameAndPoints):
  name = re.sub(".*: ", "", nameAndPoints)
  names = re.sub(" [^ ]*$", "", name).split(',')
  return names[1].strip(), names[0].strip()

def getPoints(nameAndPoints):
  points = re.sub(".* \(", "", nameAndPoints)
  return re.sub("\)", "", points)

if __name__ == '__main__':
  main()
