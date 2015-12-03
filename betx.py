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
  html = open("betx.html", encoding='utf8')
  soup = BeautifulSoup(html, "html.parser")

  pll = soup.findAll("tr", "ev_even_row")
  for p in pll:
    print(p.find("span").find(text=True))
    odds = p.findAll("td", "ev_pick_cell")
    print(odds[0].find(text=True))
    print(odds[1].find(text=True))
    print()

def printSoup(soup):
  for a in soup:
    print(a)
    print()

if __name__ == '__main__':
  main()
