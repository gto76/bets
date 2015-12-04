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
  # with closing(Firefox()) as browser:
  browser = Firefox()
  browser.wait = WebDriverWait(browser, 2)
  # browser.get('https://wwin.com/sports/#f/0/110/0/')
  browser.get('https://wwin.com/sports/default.aspx?t=-60#f/0/110/0/')
  #browser.manage().timeouts().implicitlyWait(3, TimeUnit.SECONDS);

  WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='item'][@fullok='430']")))


  element = browser.find_element_by_xpath("//div[@class='item'][@fullok='430']")
  element.click()
  # ActionChains(browser).move_to_element(element).click(element).perform()

  WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.XPATH, "//span[@class='ex1 ex22']")))

  bla = browser.page_source
  print(bla)

def main():
  selenium()
  exit()
  html = open("wwin.html", encoding='utf8')
  soup = BeautifulSoup(html, "html.parser")

  pl = soup.findAll("tr", {"ot" : "60652800"})

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
