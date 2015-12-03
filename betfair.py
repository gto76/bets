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
  html = open("betfair.html", encoding='utf8')
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
