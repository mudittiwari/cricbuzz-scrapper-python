from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
import time
class UpcomingMatchCard:
    def __init__(self, matchLink, team1, team2, matchType, matchTiming):
        self.matchLink = matchLink
        self.team1 = team1
        self.team2 = team2
        self.matchType = matchType
        self.matchTiming = matchTiming

    def __repr__(self):
        return (f"UpcomingMatchCard(match_link='{self.matchLink}', "
                f"team1='{self.team1}', team2='{self.team2}', "
                f"match_type='{self.matchType}', "
                f"match_timing='{self.matchTiming}')")
class RunningMatchCard:
    def __init__(self, matchLink, team1, team2, matchType, team1Players, team2Players):
        self.matchLink = matchLink
        self.team1 = team1
        self.team2 = team2
        self.matchType = matchType
        self.team1Players = team1Players
        self.team2Players = team2Players

    def __repr__(self):
        return (f"RunningMatchCard(matchLink='{self.matchLink}', "
                f"team1='{self.team1}', team2='{self.team2}', "
                f"matchType='{self.matchType}', "
                f"team2Players='{self.team2Players}', "
                f"team1Players='{self.team1Players}')")    

def getUpcomingMatchesInfo(matchCardsList,driver):
    matchesList=[]
    for item in matchCardsList:
        try:
            matchLinkElement = item.find_element(By.TAG_NAME, 'a')
            matchLink = matchLinkElement.get_attribute('href')
        except NoSuchElementException:
            print("Match link element not found, skipping this match. \n\n")
            continue
        
        try:
            matchTypeElement = item.find_element(By.CLASS_NAME, 'cb-card-match-format')
            matchType=driver.execute_script("return arguments[0].textContent;", matchTypeElement).strip()
        except NoSuchElementException:
            print("Match type element not found, skipping this match. \n\n")
            continue
        try:
            previewElement = item.find_element(By.CLASS_NAME, 'cb-ovr-flo.cb-mtch-crd-time.cb-font-12.cb-text-preview')
            previewText = driver.execute_script("return arguments[0].textContent;", previewElement).strip()
        except NoSuchElementException:
            print("Preview element not found, skipping this match. \n\n")
            continue
        
        if previewText.startswith("Today"):
            teamElements = item.find_elements(By.CLASS_NAME, 'cb-hmscg-bat-txt')
            if len(teamElements) >= 2:
                try:
                    spanElement1 = teamElements[0].find_element(By.TAG_NAME, 'span')
                    spanElement2 = teamElements[1].find_element(By.TAG_NAME, 'span')
                    team1 = driver.execute_script("return arguments[0].textContent;", spanElement1).strip()
                    team2 = driver.execute_script("return arguments[0].textContent;", spanElement2).strip()
                    matchCard = UpcomingMatchCard(
                        matchLink=matchLink,
                        team1=team1,
                        team2=team2,
                        matchType=matchType,
                        matchTiming=previewText
                    )
                    matchesList.append(matchCard)
                except Exception as e:
                    print("An error occurred while fetching team names:", str(e))
            else:
                print("Could not find both teams using the 'cb-hmscg-bat-txt' class.")
    return matchesList

def getLastBallAction(matchUrl, driver):
    try:
        driver.get(matchUrl)
        time.sleep(3)
        try:
            recentScoreContainer = driver.find_element(By.CSS_SELECTOR, 'div.cb-min-rcnt')
            recentScoreSpan = recentScoreContainer.find_elements(By.TAG_NAME, "span")[1]
            recentScoreSpanText = driver.execute_script("return arguments[0].textContent;", recentScoreSpan).strip()
        except Exception as e:
            print(f"Error locating or retrieving score: {e}")
            recentScoreSpanText = ""
        try:
            recentCommentaryContent = driver.find_element(By.CSS_SELECTOR, 'p.cb-com-ln')
            recentCommentaryContentText = driver.execute_script("return arguments[0].textContent;", recentCommentaryContent).strip()
        except Exception as e:
            print(f"Error locating or retrieving commentary: {e}")
            recentCommentaryContentText = ""
        try:
            recentCommentarySplitList = recentCommentaryContentText.split(',')
            playersInvolvedStringList = recentCommentarySplitList[0].split('to')
            bowler = playersInvolvedStringList[0].strip() if len(playersInvolvedStringList) > 0 else "Unknown"
            batsman = playersInvolvedStringList[1].strip() if len(playersInvolvedStringList) > 1 else "Unknown"
        except Exception as e:
            print(f"Error parsing player names: {e}")
            bowler = "Unknown"
            batsman = "Unknown"
        lastBallAction = {
            "scoreDone": recentScoreSpanText.split()[-1].strip() if recentScoreSpanText else "N/A",
            "bowler": bowler,
            "batsman": batsman
        }
        print(lastBallAction)
        
    except Exception as e:
        print(f"Error in getLastBallAction function: {e}")
        lastBallAction = {
            "scoreDone": "N/A",
            "bowler": "Unknown",
            "batsman": "Unknown"
        }
    return lastBallAction

def getSquadsUrl(liveScoresUrl):
    return liveScoresUrl.replace("live-cricket-scores", "cricket-match-squads")
    

def fetchSquads(liveScoresUrl, driver):
    try:
        squadsUrl = getSquadsUrl(liveScoresUrl)
        driver.get(squadsUrl)
        time.sleep(3)
        squadsContainer = driver.find_element(By.CSS_SELECTOR, 'div.cb-col.cb-col-67.cb-sqds-lft-col')
        teamHeaders = squadsContainer.find_element(By.CLASS_NAME, 'cb-teams-hdr')
        leftSquad = squadsContainer.find_element(By.CSS_SELECTOR, 'div.cb-col.cb-play11-lft-col').find_elements(By.CSS_SELECTOR, '.cb-player-card-left')
        rightSquad = squadsContainer.find_element(By.CSS_SELECTOR, 'div.cb-col.cb-play11-rt-col').find_elements(By.CSS_SELECTOR, '.cb-player-card-right')

        teamsInfo = {}
        team1List = []
        team2List = []
        for item in leftSquad:
            try:
                playerName = item.find_element(By.CSS_SELECTOR, '.cb-player-name-left').text.split('\n')[0]
                team1List.append(playerName)
            except Exception as e:
                print(f"Error extracting player from left squad: {e}")
        for item in rightSquad:
            try:
                playerName = item.find_element(By.CSS_SELECTOR, '.cb-player-name-right').text.split('\n')[0]
                team2List.append(playerName)
            except Exception as e:
                print(f"Error extracting player from right squad: {e}")
        try:
            teamsInfo[teamHeaders.text.split('\n')[0]] = team1List
            teamsInfo[teamHeaders.text.split('\n')[1]] = team2List
            return teamsInfo
        except Exception as e:
            print(f"Error extracting team names: {e}")

    except Exception as e:
        print(f"An error occurred while fetching squads: {e}")


def getRunningMatchesInfo(matchCardsList, driver):
    matchesList = []
    for item in matchCardsList:
        try:
            matchStateElement = item.find_element(By.CLASS_NAME, 'cb-mtch-crd-state')
            matchStateClass = matchStateElement.get_attribute('class')
            if 'cb-text-apple-red' not in matchStateClass:
                continue
            matchLinkElement = item.find_element(By.TAG_NAME, 'a')
            matchLink = matchLinkElement.get_attribute('href')
        except NoSuchElementException:
            print("Match link or state element not found, skipping this match. \n\n")
            continue

        try:
            matchTypeElement = item.find_element(By.CLASS_NAME, 'cb-card-match-format')
            matchType = driver.execute_script("return arguments[0].textContent;", matchTypeElement).strip()
        except NoSuchElementException:
            print("Match type element not found, skipping this match. \n\n")
            continue

        try:
            team1Element = item.find_element(By.CLASS_NAME, 'cb-hmscg-bat-txt').find_element(By.TAG_NAME, 'span')
            team2Element = item.find_element(By.CLASS_NAME, 'cb-hmscg-bwl-txt').find_element(By.TAG_NAME, 'span')
            team1 = driver.execute_script("return arguments[0].textContent;", team1Element).strip()
            team2 = driver.execute_script("return arguments[0].textContent;", team2Element).strip()
            matchCard = RunningMatchCard(matchLink, team1, team2, matchType, [], [])
            matchesList.append(matchCard)
        except NoSuchElementException:
            print("Error finding teams of the match. \n\n")
            continue

    return matchesList
