from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from classes.MatchCard import getUpcomingMatchesInfo,getRunningMatchesInfo,fetchSquads, getCompletedMatchesInfo, getUpcomingMatchesTossUpdate
import time
import json



def serializeRunningMatches(runningMatches):
    serializedMatches = []
    for match in runningMatches:
        serializedMatch = {
            "matchLink": match.matchLink,
            "team1": match.team1,
            "team2": match.team2,
            "matchType": match.matchType,
            "team1Players": match.team1Players,
            "team2Players": match.team2Players
        }
        serializedMatches.append(serializedMatch)
    return serializedMatches

def getMatches():
    url = "https://www.cricbuzz.com/"
    options = Options()
    options.headless = True
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--tz=Asia/Kolkata")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    # while True:
    #     print(getLastBallAction("https://www.cricbuzz.com/live-cricket-scores/94404/rsa-vs-sl-1st-test-sri-lanka-tour-of-south-africa-2024",driver))
    #     time.sleep(10)
    driver.get(url)
    try:
        matchCardsUl = driver.find_element(By.CLASS_NAME, 'cb-mtch-crd-rt-itm')
        matchCardsList = matchCardsUl.find_elements(By.TAG_NAME, 'li')
        upcomingMatchesList=getUpcomingMatchesInfo(matchCardsList,driver=driver)
        runningMatchesList=getRunningMatchesInfo(matchCardsList,driver=driver)
        completedMatchesList=getCompletedMatchesInfo(matchCardsList,driver=driver)
        upcomingMatchesTossUpdateList=getUpcomingMatchesTossUpdate(matchCardsList,driver=driver)
        for item in runningMatchesList:
            matchPlayingSquads=fetchSquads(item.matchLink,driver)
            teams=matchPlayingSquads.keys()
            for team in teams:
                if(team.startswith(item.team1.strip('.'))):
                    item.team1Players=matchPlayingSquads[team]
                if(team.startswith(item.team2.strip('.'))):
                    item.team2Players=matchPlayingSquads[team]

        # print(upcomingMatchesList)
        # print("\n\n\n\n")
        # print(completedMatchesList)
        # print("\n\n\n\n")
        # print(upcomingMatchesTossUpdateList)
        # print("\n\n\n\n")
        # for item in runningMatchesList:
        #     print(item.matchLink)
        #     print(getLastBallAction(item.matchLink,driver=driver))
        matches_data = {
            "upcomingMatches": upcomingMatchesList,
            "runningMatches": runningMatchesList,
            "completedMatches": completedMatchesList,
            "upcomingMatchesTossUpdate": upcomingMatchesTossUpdateList
        }
        print(json.dumps(matches_data, default=lambda o: o.__dict__, indent=4))
    finally:
        driver.quit()

getMatches()



