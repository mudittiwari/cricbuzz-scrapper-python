from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from classes.MatchCard import getUpcomingMatchesInfo,getRunningMatchesInfo,fetchSquads


def getMatches():
    url = "https://www.cricbuzz.com/"
    options = Options()
    options.headless = True
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--tz=Asia/Kolkata")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    try:
        matchCardsUl = driver.find_element(By.CLASS_NAME, 'cb-mtch-crd-rt-itm')
        matchCardsList = matchCardsUl.find_elements(By.TAG_NAME, 'li')
        upcomingMatchesList=getUpcomingMatchesInfo(matchCardsList,driver=driver)
        runningMatchesList=getRunningMatchesInfo(matchCardsList,driver=driver)
        for item in runningMatchesList:
            matchPlayingSquads=fetchSquads(item.matchLink,driver)
            teams=matchPlayingSquads.keys()
            for team in teams:
                if(team.startswith(item.team1.strip('.'))):
                    item.team1Players=matchPlayingSquads[team]
                if(team.startswith(item.team2.strip('.'))):
                    item.team2Players=matchPlayingSquads[team]

        print(upcomingMatchesList)
        print("\n\n\n\n")
        print(runningMatchesList)
    finally:
        driver.quit()

getMatches()