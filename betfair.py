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
  html = open("bettopsport.html", encoding='utf8')
  soup = BeautifulSoup(html, "html.parser")

  pl = soup.findAll("tr", "offers_line event-filter-all")
  for p in pl:
    name = p.find("td", "betsPrefix").find(text=True)
    points = p.findAll("span", "fora")[0].find(text=True)
    odds = p.findAll("div", "pull-right rate")
    if len(odds) < 3:
      continue
    odd1 = odds[0].find(text=True)
    odd2 = odds[2].find(text=True)
    print(name)
    print(points)
    print(odd1)
    print(odd2)
    print()

def printSoup(soup):
  for a in soup:
    print(a)
    print()

if __name__ == '__main__':
  main()
