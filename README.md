Nba Players
===========

How to run on Linux
-------------------

### LAMP stack
```
sudo apt-get install apache2
sudo apt-get install mysql-client
sudo apt-get install mysql-server
sudo apt-get install php5 php-pear php5-mysql
```

### Python libraries
```
sudo apt-get install python3
sudo apt-get install python3-pip

sudo pip3 install PyMySQL
sudo pip3 install selenium
sudo pip3 install oauth2client
sudo apt-get install libssl-dev (, libffi-dev)
sudo pip3 install PyOpenSSL
sudo pip3 install gspread
sudo pip3 install beautifulsoup4
```

### With Headless Firefox
```
sudo apt-get install xvfb
DISPLAY=:99 xvfb-run -a ./wwin-all.py
```

Project Description
-------------------

Please only those who have experience in extracting betting odds apply. This project is for personal use only, therefore aesthetics isn't important. I need an odds comparison data table that contains a database of specific odds from specific bookies. The odds are NBA player points ONLY and the list of bookies is below. You need to extract the odds by scraping or if you have bookie APIs. The data table needs to have: 

* name of bookie, 
* time of event, (single)
* player name, 
* number of points, 
* odds for over, 
* odds for under 
* and if possible team of player. (single)

Time of evend and team can be scraped from a single bookie. Output table has to be sortable by several levels. Default sort would be: player name, number of points, odds. 

Of course, the output data table needs to be online so I can refresh the table when needed. Fetching can be manual. 
Below are the bookies that are needed and the best possible link that leads to NBA player points. Some bookies have the same link each day, some create links with event ids daily. I will upload the screenshots of several bookies so that you can easily see which odds are needed.
Note: not all bookies have the same player name structure, so the database needs to match similar expressions. 

1. Marathonbet: https://www.marathonbet.com/hr/betting/Basketball/NBA/

2. Favbet: https://www.favbet.com/en/bets/#tour=17745 event example: 
https://www.favbet.com/en/bets/#tour=17745&event=4198442

3. WWin: https://wwin.com/sports/#f/0/110/0/

4. Meridianbet: https://meridianbet.com/#!standard_betting;leagueIDs=593

5. LSbet: https://www.lsbet.com/en-GB/sportsbook/eventpaths/multi/[223517]?utf8=%E2%9C%93&filter_options%5B%5D=450%7C209&commit=Refresh 

6. Betx: https://www.betx.sk/SportBetting 

7. William Hill: http://sports.williamhill.com/bet/en-gb/betting/t/266/NBA.html 

8. Betsafe: https://www.betsafe.com/en/odds#/#/Special/87 BEATIFULSOUP
or https://apostas.dhoze.com/en/#/#/Special/87

9. Orakulas: http://orakulas.lt/nba SELINIUM

10. Betfair: https://www.betfair.com/sport/basketball/event?eventId=27557166 ODDS IN PERCENTAGES
event example: 
https://www.betfair.com/sport/basketball/event?eventId=27557168 FAIL

11. Bet top sport: https://www.bettopsport.com/odds/all/2/0/676 NE NADZEM
event example: 
https://www.bettopsport.com/odds/all/2/0/676/5000393


There are 4 more bookies that need to be fetched however those are already available in a data table done by a freelancer that had to give up before finishing. He gave me links and passwords to data and mysql tables as well as the code, so fetching/scraping them shouldn't be a problem.
