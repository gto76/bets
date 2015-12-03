#!/usr/bin/python3
#
# Usage: favbet.py 
# https://www.favbet.com/en/bets/#tour=17745&event=4198442

import os
import sys

import json

from bs4 import BeautifulSoup

def main():
  html = open("marathonbet.html", encoding='utf8')
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
