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
  html = open("lsbet.html", encoding='utf8')
  soup = BeautifulSoup(html, "html.parser")


  pll = soup.findAll("span", "name ellipsis")
  pl = soup.findAll("span", "formatted_price")

  for a, b in zip(pll, pl):
    print(a.find(text=True))
    print(b.find(text=True))

def printSoup(soup):
  for a in soup:
    print(a)
    print()

if __name__ == '__main__':
  main()
