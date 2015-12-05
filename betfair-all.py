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
  htmls = selenium()
  for html in htmls:
    parse(html)

def selenium():
  with closing(Firefox()) as browser:
    browser.get('https://www.betfair.com/sport/basketball')
    WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.XPATH, "//span[@class='section-header-label']")))
    element = browser.find_element_by_xpath("//*[contains(text(), 'NBA 2015-2016')]")
    element.click()
    WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.XPATH, "//span[@class='section-header-label']")))
    elementsA = browser.find_elements_by_xpath("//li[@class='com-coupon-line avb-row market-avb large ']")
    numOfElements = len(elementsA)

    htmls = []
    for i in range(0, numOfElements):
      element = browser.find_element_by_xpath("//*[contains(text(), 'NBA 2015-2016')]")
      element.click()
      WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.XPATH, "//span[@class='away-team-name']")))
      # elements = browser.find_elements_by_xpath("//li[@class='com-coupon-line avb-row market-avb large ']")
      elements = browser.find_elements_by_xpath("//div[@class='details-event']")
      print(i)
      elements[i].click()
      WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='ui-expandable ui-expandable-selected com-expandable-header-anchor has-deeplink']")))
      htmls.append(browser.page_source)
      browser.back()
      WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.XPATH, "//span[@class='section-header-label']")))
    return htmls 


#   numOfElements = getNumberOfElements()
#   # print(numOfElements)
#   htmls = []
#   for i in range(0, numOfElements):
#     htmls.append(getHtmlFromElementIndex(i))
#   return htmls

# def getNumberOfElements():
#   with closing(Firefox()) as browser:
#     browser.get('https://www.betfair.com/sport/basketball')
#     WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.XPATH, "//span[@class='section-header-label']")))
#     element = browser.find_element_by_xpath("//*[contains(text(), 'NBA 2015-2016')]")
#     element.click()
#     WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.XPATH, "//span[@class='section-header-label']")))
#     elements = browser.find_elements_by_xpath("//li[@class='com-coupon-line avb-row market-avb large ']")
#     return len(elements)

# def getHtmlFromElementIndex(index):
#   with closing(Firefox()) as browser:
#     browser.get('https://www.betfair.com/sport/basketball')
#     WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.XPATH, "//span[@class='section-header-label']")))
#     element = browser.find_element_by_xpath("//*[contains(text(), 'NBA 2015-2016')]")
#     element.click()
#     WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.XPATH, "//span[@class='section-header-label']")))
#     elements = browser.find_elements_by_xpath("//li[@class='com-coupon-line avb-row market-avb large ']")
#     elements[index].click()
#     WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='ui-expandable ui-expandable-selected com-expandable-header-anchor has-deeplink']")))
#     return browser.page_source

def parse(html):
  soup = BeautifulSoup(html, "html.parser")
  pll = soup.findAll("div", "mod yui3-widget yui3-module yui3-minimarketview")
  for p in pll:
    player = p.find("span", text = re.compile(".*Total Points $"), attrs =  {"class": "title"})
    if player:
      printSoup(player)
      printOther(p)

def printOther(p):
  pp = p.findAll("li", attrs={'class': "runner-item"})
  for bla in pp:
    printOdd(bla)

def printOdd(bla):
  spans = bla.findAll("span")
  points = spans[2].find(text=True)
  odd = spans[1].find(text=True)
  print(points)
  print(odd)

def printSoup(soup):
  for a in soup:
    print(a)
    print()

if __name__ == '__main__':
  main()
