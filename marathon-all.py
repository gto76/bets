#!/usr/bin/python3
#
# Usage: favbet.py 
# https://www.favbet.com/en/bets/#tour=17745&event=4198442

import os
import sys
import json

from contextlib import closing
from selenium.webdriver import Firefox # pip install selenium
from selenium.webdriver import Chrome # pip install selenium
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup

def selenium():
  with closing(Firefox()) as browser:
    browser.get('https://www.marathonbet.com/hr/betting/Basketball/NBA/')
    WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='member-name nowrap ']")))
    browser.find_element_by_xpath("//div[@class='member-name nowrap ']").click()
    WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.XPATH, "//table[@class='table-shortcuts-menu']")))
    return browser.page_source
  
def seleniumAll():
  with closing(Firefox()) as browser:
    browser.get('https://www.marathonbet.com/hr/betting/Basketball/NBA/')
    WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='member-name nowrap ']")))
    elements = browser.find_elements_by_xpath("//div[@class='member-name nowrap ']")
    for e in elements:
      e.click()
      WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.XPATH, "//table[@class='table-shortcuts-menu']")))
      yield browser.page_source

def main():
  htmls = seleniumAll()
  soup = BeautifulSoup(htmls[0], "html.parser")

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