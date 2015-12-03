#!/usr/bin/python3
#
# Usage: favbet.py 
# https://www.favbet.com/en/bets/#tour=17745&event=4198442

import os
import sys

import json

from bs4 import BeautifulSoup

def main():
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
