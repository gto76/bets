import glob
from pprint import pprint

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

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

def waitAndClick(browser, identifier):
  wait(browser, identifier)
  click(browser, identifier)

def wait(browser, identifier):
  WebDriverWait(browser, timeout=20).until(EC.presence_of_element_located((By.XPATH, identifier)))

def click(browser, identifier):
  browser.find_element_by_xpath(identifier).click()