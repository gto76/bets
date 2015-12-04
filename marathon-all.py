#!/usr/bin/python3
#
# Usage: favbet.py 
# https://www.favbet.com/en/bets/#tour=17745&event=4198442

import os
import sys
import json

from bs4 import BeautifulSoup
from contextlib import closing
from selenium.webdriver import Firefox 
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

def getDates(html):
  soup = BeautifulSoup(html, "html.parser")
  pl = soup.findAll("td", "date")
  for p in pl:
    yield p.find(text=True)

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
    return (dates, browser.page_source)

def main():
  dates, html = selenium()
  print(dates)
  exit()
  
  soup = BeautifulSoup(html, "html.parser")

  pl = soup.findAll("td", "price width30")
  for a in pl:
    text = a["data-sel"]
    resp = json.loads(text)
    print(resp["mn"])
    print(resp["sn"])
    print(resp["epr"])
    print()

def printSoup(soup):
  for a in soup:
    print(a)
    print()

if __name__ == '__main__':
  main()