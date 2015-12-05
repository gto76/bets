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

def selenium():
  with closing(Firefox()) as browser:
    browser.get('https://wwin.com/sports/default.aspx?t=-60#f/0/110/0/')
    WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='item'][@fullok='430']")))
    element = browser.find_element_by_xpath("//div[@class='item'][@fullok='430']")
    element.click()
    WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.XPATH, "//span[@class='ex1 ex22']")))
    return browser.page_source

def main():
  html = selenium()
  soup = BeautifulSoup(html, "html.parser")
  parovi = soup.find("table", "parovi extra")
  pl = parovi.findAll("tr", {"ot" : re.compile("[0-9]*")})
  for a in pl:
    print(a.find("td", "parPar").find(text=True))
    odds = a.findAll("td", "tgp")
    print(odds[0].find(text=True))
    print(odds[1].find(text=True))
    print()

def printSoup(soup):
  for a in soup:
    print(a)
    print()

if __name__ == '__main__':
  main()
