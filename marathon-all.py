#!/usr/bin/python3
#
# Usage: favbet.py 
# https://www.favbet.com/en/bets/#tour=17745&event=4198442

from contextlib import closing
from selenium.webdriver import Firefox # pip install selenium
from selenium.webdriver import Chrome # pip install selenium
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

import os
import sys

import json

from bs4 import BeautifulSoup

def selenium():
  browser = Firefox()
  browser.wait = WebDriverWait(browser, 2)
  browser.get('https://www.marathonbet.com/hr/betting/Basketball/NBA/')

  WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='member-name nowrap ']")))

  element = browser.find_element_by_xpath("//div[@class='member-name nowrap ']")
  element.click()

  WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.XPATH, "//table[@class='table-shortcuts-menu']")))

  bla = browser.page_source
  return bla
  #print(bla)

def main():
  #html = open("marathonbet.html", encoding='utf8')
  html = selenium()
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