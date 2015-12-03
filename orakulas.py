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
  html = open("orakulas.html", encoding='utf8')
  soup = BeautifulSoup(html, "html.parser")

  # <div class="order-title"><div>Miami Heat - Oklahoma City Thunder</div>
  pl = soup.findAll("span", "ev-outcome")
  for a in pl:
    if not a.has_attr("onclick"):
      continue
    onclick = a["onclick"]
    onclick = re.sub("^[^{]*{[^{]*", "", onclick)
    onclick = re.sub("[^}]*}$", "", onclick)
    resp = json.loads(onclick)
    if "Player total" in resp["alt_name"]:
      print(resp["option"])
      print(resp["coef"])
      print()

def printSoup(soup):
  for a in soup:
    print(a)
    print()

if __name__ == '__main__':
  main()
