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
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

def main():
  html = selenium()
  soup = BeautifulSoup(html, "html.parser")

  dates = soup.findAll("div", "gwt-Label date")
  times = soup.findAll("div", "gwt-Label time")
  pl = soup.findAll("div", "rivals")
  pa = soup.findAll("div", "selections three four")

  for date, time, a, b in zip(dates, times, pl, pa):
    name = a.find("div", "gwt-Label away").find(text=True)
    odds = b.findAll("div", "gwt-Label")
    print(date.find(text=True)+" "+time.find(text=True)+" "+name)
    for odd in odds:
      print(odd.find(text=True))
    print()

def selenium():
  with closing(Firefox()) as browser:
    browser.get('https://meridianbet.com/#!standard_betting;leagueIDs=593')
    WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='gwt-Label home']")))
    return browser.page_source

def printSoup(soup):
  for a in soup:
    print(a)
    print()

if __name__ == '__main__':
  main()
