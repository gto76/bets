from pprint import pprint
import glob

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

def getHtml(argv, selenium, bookieName):
  if len(argv) > 1:
    if argv[1] != "save":
      return getFiles(bookieName)
    else:
      save(selenium, bookieName)
  return selenium()

def getFiles(bookieName):
  files = []
  filenames = glob.glob(TEST_FOLDER+'/'+bookieName.lower()+'*.html')
  for filename in filenames:
    files.append(open(filename, encoding='utf8'))
  return files

def save(selenium, bookieName):
  htmls = selenium()
  i = 0
  for html in htmls:
    filename = TEST_FOLDER+"/"+bookieName.lower()+str(i)+".html"
    f = open(filename,'w')
    f.write(html)
    f.close()
    i += 1
  exit(0)