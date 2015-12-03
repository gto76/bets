#!/usr/bin/python3
#
# Usage: favbet.py 
# https://www.favbet.com/en/bets/#tour=17745&event=4198442

import os
import sys

from bs4 import BeautifulSoup

def main():
  html = open("favbet.html", encoding='utf8')
  soup = BeautifulSoup(html, "html.parser")
  pl = soup.find("li", {"data-clue" : "Over/Under points (player)"})
  
  names = pl.findAll("span", "bets_oc ttt")
  odds = pl.findAll("button", "betbut a")


  for a, b in zip(names, odds):
    print(a.find(text=True))
    print(b.find(text=True))
    print()

if __name__ == '__main__':
  main()
