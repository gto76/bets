#!/usr/bin/python3
#
# Usage: favbet.py 
# https://www.favbet.com/en/bets/#tour=17745&event=4198442

import os
import sys
import re

import json

from bs4 import BeautifulSoup

def main():
  html = open("meridianbet.html", encoding='utf8')
  soup = BeautifulSoup(html, "html.parser")

  pl = soup.findAll("div", "rivals")
  pa = soup.findAll("div", "selections three four")

  for a, b in zip(pl, pa):
    name = a.find("div", "gwt-Label away").find(text=True)
    odds = b.findAll("div", "gwt-Label")
    print(name)
    for odd in odds:
      print(odd.find(text=True))
    print()

def printSoup(soup):
  for a in soup:
    print(a)
    print()

if __name__ == '__main__':
  main()
