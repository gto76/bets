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
from selenium.webdriver import Firefox # pip install selenium
from selenium.webdriver import Chrome # pip install selenium
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

def main():
  dates, htmls = selenium()
  for date, html in zip(dates, htmls):
    print(date)
    processGame(html)
    print()

def selenium():
  with closing(Firefox()) as browser:
    browser.get('https://www.favbet.com/en/bets/#tour=17745')
    WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.XPATH, "//b[@class='ttt']")))
    (links, dates) = getLinksAndDates(browser.page_source)
    htmls = []
    for link in links:
      element = browser.find_element_by_xpath("//*[contains(text(), '"+link+"')]")
      element.click()
      WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.XPATH, "//ul[@class='market_groups']")))
      htmls.append(browser.page_source)
    return dates, htmls

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

def processGame(html):
  soup = BeautifulSoup(html, "html.parser")
  pl = soup.find("li", {"data-clue" : "Over/Under points (player)"})
  names = pl.findAll("span", "bets_oc ttt")
  odds = pl.findAll("button", "betbut a")
  for a, b in zip(names, odds):
    print(a.find(text=True))
    print(b.find(text=True))
    print()

if __name__ == '__main__':
  main()
