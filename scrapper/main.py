from classes.MatchCard import fetchSquads, getCompletedMatchesInfo, getRunningMatchesInfo, getUpcomingMatchesInfo, getUpcomingMatchesTossUpdate
from selenium.webdriver.common.by import By
import zmq
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

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
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        matchCardsUl = driver.find_element(By.CLASS_NAME, 'cb-mtch-crd-rt-itm')
        matchCardsList = matchCardsUl.find_elements(By.TAG_NAME, 'li')
        upcomingMatchesList = getUpcomingMatchesInfo(matchCardsList, driver=driver)
        runningMatchesList = getRunningMatchesInfo(matchCardsList, driver=driver)
        completedMatchesList = getCompletedMatchesInfo(matchCardsList, driver=driver)
        upcomingMatchesTossUpdateList = getUpcomingMatchesTossUpdate(matchCardsList, driver=driver)

        for item in runningMatchesList:
            matchPlayingSquads = fetchSquads(item.matchLink, driver)
            teams = matchPlayingSquads.keys()
            for team in teams:
                if team.startswith(item.team1.strip('.')):
                    item.team1Players = matchPlayingSquads[team]
                if team.startswith(item.team2.strip('.')):
                    item.team2Players = matchPlayingSquads[team]

        matches_data = {
            "upcomingMatches": upcomingMatchesList,
            "runningMatches": runningMatchesList,
            "completedMatches": completedMatchesList,
            "upcomingMatchesTossUpdate": upcomingMatchesTossUpdateList
        }
        return json.dumps(matches_data, default=lambda o: o.__dict__, indent=4)
    finally:
        driver.quit()


def zmqServer():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5556")
    print("ZMQ Server is running...")
    while True:
        try:
            message = socket.recv_json()
            task = message.get("task")
            if task == "getMatches":
                print("Received task: getMatches")
                response = getMatches()
                socket.send_json({"status": "success", "data": json.loads(response)})
            else:
                socket.send_json({"status": "error", "message": "Invalid task"})
        except Exception as e:
            print(f"Error: {e}")
            socket.send_json({"status": "error", "message": str(e)})

if __name__ == "__main__":
    zmqServer()
