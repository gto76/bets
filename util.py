from pprint import pprint

TEST_FOLDER = "htmls"

class Player:
  pass

def pairwise(t):
    it = iter(t)
    return zip(it,it)

def printSoup(soup):
  for a in soup:
    print(a)
    print()

def printPlayers(players):
  for p in players:
    pprint (vars(p))
