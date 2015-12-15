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

BOOKIE_NAME = "Orakulas"
BOOKIE_URL = "http://orakulas.lt/nba"

def main():
  htmls = getHtml(sys.argv)
  players = []
  for html in htmls:
    players.extend(getPlayers(html))
  util.printPlayers(players)

def getHtml(argv):
  if len(argv) > 1:
    if argv[1] != "save":
      return getFiles()
    else:
      save()
  return selenium()

def getFiles():
  files = []
  filenames = glob.glob(util.TEST_FOLDER+'/'+BOOKIE_NAME.lower()+'*.html')
  for filename in filenames:
    files.append(open(filename, encoding='utf8'))
  return files

def save():
  htmls = selenium()
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
    htmls = []
    browser.get(BOOKIE_URL)
    WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.XPATH, "//span[@class='extra-events']")))
    for i in [2]:
      # browser.refresh()
      elements = browser.find_elements_by_xpath("//span[@class='extra-events']")
      # icons other icon-other-gourmands
      e = elements[i]
      e.click()
      # WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='event-outcomes']")))
      WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.XPATH, "//span[@class='extra-events selected']")))
      htmls.append(browser.page_source)
      element = browser.find_element_by_xpath("//span[@class='extra-events selected']")
      element.click()
      WebDriverWait(browser, timeout=10).until(EC.invisibility_of_element_located((By.XPATH, "//div[@class='subgroup-header with-hover with-extra-icons extra-icons-small']")))
    return htmls

# def getNumberOfLinks():
#   with closing(Firefox()) as browser:
#     browser.get(BOOKIE_URL)
#     WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.XPATH, "//span[@class='extra-events']")))
#     elements = browser.find_elements_by_xpath("//span[@class='extra-events']")
#     return len(elements)

# def selenium():
#   with closing(Firefox()) as browser:
#     browser.get(BOOKIE_URL)
#     WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.XPATH, "//span[@class='extra-events']")))
#     elements = browser.find_elements_by_xpath("//span[@class='extra-events']")
#     htmls = []
#     for e in elements:
#       e.click()
#       WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='name']")))
#       htmls.append(browser.page_source)
#       e.click()
#       WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.XPATH, "//span[@class='extra-events']")))
#     return htmls

def getPlayers(html):
  soup = BeautifulSoup(html, "html.parser")
  # <div class="order-title"><div>Miami Heat - Oklahoma City Thunder</div>
  pl = soup.findAll("span", "ev-outcome")
  playersJson = []
  for a in pl:
    if not a.has_attr("onclick"):
      continue
    onclick = a["onclick"]
    onclick = re.sub("^[^{]*{[^{]*", "", onclick)
    onclick = re.sub("[^}]*}$", "", onclick)
    #print(onclick)
    resp = json.loads(onclick)
    if "Player total" in resp["alt_name"]:
      playersJson.append(resp)
      # print(resp["option"])
      # print(resp["coef"])
      # print()
  players = []
  for a, b in util.pairwise(playersJson):
    player = util.Player()
    player.player_name = cleanName(a["option"])
    player.player_total = cleanPoints(a["option"])
    player.under = a["coef"]
    player.over = a["coef"]
    player.start_time = "NONE"
    player.bookie_name = BOOKIE_NAME
    player.bookie_url = BOOKIE_URL
    players.append(player)
  return players

def cleanName(name):
  return name

def cleanPoints(points):
  return points

if __name__ == '__main__':
  main()
